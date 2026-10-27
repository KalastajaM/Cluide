# Stacked pull requests: build, fix, land

A stack is a series of dependent changes, one pull request each, every branch
built on the one before: a list of review fixes, a staged refactor, an
overnight agent run. Review stays small and the series lands in order. This
file covers building the stack, fixing an earlier branch while a worktree is
busy, testing any revision without a checkout, and squash-merging the stack
without rerunning CI on trees CI has already tested. The why is in
Guide 11 §Stacks of Pull Requests.

## Building the stack

- **Every PR targets the trunk** when the repository does not delete merged
  head branches. A PR that targets its predecessor's branch stays pointed at
  that branch after the predecessor merges, and merging it then lands in a
  dead branch. Targeting the trunk means each PR's diff also shows its
  predecessors' commits, so each description says: "Part N of M. Merge in
  order after #X. Review only the top commit."
- **Check containment after every fix to an earlier branch.** A fix pushed to
  branch k is not in branches k+1 to n until it is merged forward. A branch
  contains its predecessor when merging the predecessor in changes nothing:

  ```bash
  [ "$(git merge-tree --write-tree "$branch" "$prev" | head -1)" = \
    "$(git rev-parse "$branch^{tree}")" ] || echo "$branch is missing $prev"
  ```

- **A side branch is the untested combination.** A PR built off the stack so
  it can be skipped must, once kept, be merged into every later branch. The
  tree that combines it with those branches is the one CI never saw on its
  own; it gets the full check before landing.
- **Record each branch's tip before the first merge.** Landing rewrites the
  tips (see below), and the original tips are the merge bases the landing
  needs.

## Fixing an earlier branch while the working tree is busy

When another agent or session is working in the only checkout, switching
branches would pull its files out from under it. Build the fix commit with
plumbing and a temporary index instead. Write the corrected file anywhere
outside the worktree first, then:

```bash
B=fix-03                                   # branch to fix
old=$(git rev-parse "refs/heads/$B")
export GIT_INDEX_FILE="$(mktemp -d)/index"
git read-tree "$old"
blob=$(git hash-object -w --path=src/app.py /path/to/edited/app.py)
git update-index --cacheinfo "100644,$blob,src/app.py"
new=$(git commit-tree "$(git write-tree)" -p "$old" -m "fix: <why>")
unset GIT_INDEX_FILE
git update-ref "refs/heads/$B" "$new" "$old"   # refuses if B moved meanwhile
git push origin "$B"                           # fast-forward, never --force
```

Use it only on a branch no worktree has checked out (`git worktree list`):
moving a checked-out branch's ref leaves that worktree looking as if its
files were edited. Then merge the fix forward and rerun the containment check.

## Testing any revision on an exported copy

```bash
dir=$(mktemp -d)
git archive "$rev" | tar -x -C "$dir"
# install dependencies and run the project's full check inside "$dir"
```

The export touches no worktree, index or HEAD, so it can check a branch, a
plumbing commit or a computed merge result while other sessions keep working.
It contains tracked files only: local config the check needs (an env file,
built assets) has to be supplied or rebuilt.

## Landing the stack without redundant CI

**The problem.** Squashing PR k puts one new commit on the trunk that is not
an ancestor of branch k+1. GitHub still computes the merge from the old trunk,
so every append-only file both sides touched (a changelog) conflicts, and
PR k+1 shows as conflicting although nothing has changed.

**The fix is an explicit merge base.** Branch k's original tip is the real
base of branch k+1:

```bash
git merge-tree --write-tree --merge-base="$base" origin/main "$head"
```

When the first line of the output (the result tree) equals
`git rev-parse "$head^{tree}"`, landing PR k+1 puts on the trunk exactly the
tree CI already tested on branch k+1. Then:

1. Make a merge commit with that tree and push it to the branch normally (it
   is a fast-forward, so no force):
   `git commit-tree "$tree" -p "$head" -p origin/main -m "Merge main into <branch>"`.
2. Squash at once with `gh pr merge <n> --squash --match-head-commit <sha>`,
   which refuses if anyone pushed to the branch in between. GitHub reports
   the PR as `UNSTABLE` because checks on the new merge commit are pending;
   that is expected. `BLOCKED` means branch protection requires the checks,
   and this shortcut does not apply.
3. After each merge, assert `git rev-parse origin/main^{tree}` equals the
   tree you computed. Stop on a mismatch: someone else's commit landed, or
   the squash produced something you did not test.

**Where the tree is new**, CI has not tested it: a kept side branch, or
another commit that reached the trunk mid-run. Run the full check on an
exported copy of the final combined tree and wait for CI on the last PR only;
the earlier trees in that run are prefixes of a tree that passed.

**Precondition:** every PR's own CI was green before the run starts. The
shortcut reuses that result; it does not replace it.

**The rule holds when CI depends only on the tree.** Jobs that read event
metadata, or skip themselves by path filters, may not have run on the tested
commit. Check what actually ran before treating a skipped job as a pass.

In the run this comes from, a 19-PR stack of fixes, waiting for CI on each PR
would have cost about 28 minutes each across 17 PRs whose trees were already
tested: roughly eight hours of retesting identical content.

## Running the landing unattended

- **Retry transient failures** of every `git fetch` and `gh` call, with a
  pause. One 502 from the GitHub API ended a run that had no retry.
- **Treat "already merged" as progress.** The owner may merge a PR by hand
  mid-run. Before failing on a merge error, check the PR's state; `MERGED` is
  success, and an error response alone does not prove nothing happened.
- **Log enough to restart at any PR:** time, PR, head sha, computed tree,
  decision. The script takes a starting PR.
- **Stop at the first surprise** (conflict, red CI, unexpected trunk tree,
  unknown state) rather than guessing past it.
- **Keep automation from interfering.** A CI monitor or bot that syncs the
  checked-out branch with the trunk, or answers conflicts, does not know the
  run's order. Detach HEAD in the worktree the run uses (`git switch
  --detach`) so nothing merges into a branch out of turn, and answer its
  conflict reports with one line saying the run handles them in order.

## Script template

Requires git 2.40 or newer (`merge-tree --merge-base`), `gh` signed in, and
`jq`. Plan file, one PR per line in merge order: the PR number, its branch,
and the original tip of the branch it was built on (`-` for the first, which
is built on the trunk). Record those tips before the first merge.

```
101 fix-01 -
102 fix-02 3f9c2a1e...   # original tip of fix-01
103 fix-03 8b04d7c2...   # original tip of fix-02
```

```bash
#!/usr/bin/env bash
# Squash-merge a stack of PRs in order. Skips CI reruns where the landed tree
# is the tree CI already tested; waits for CI where the tree is new.
# Usage: REPO=owner/name land-stack.sh <plan-file> [first-pr]
set -euo pipefail
PLAN=$1 START=${2:-0} REPO=${REPO:?set REPO=owner/name}
log(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die(){ log "STOP: $*"; exit 1; }
retry(){ local i; for i in 1 2 3 4 5; do "$@" && return 0; log "retry $i: $*"; sleep $((i * 20)); done; return 1; }

ci(){ # prints green, pending or failed for a commit's check runs
  local j; j=$(retry gh api "repos/$REPO/commits/$1/check-runs?per_page=100") || die "check-runs $1"
  jq -r 'if .total_count == 0 then "pending"
    elif any(.check_runs[]; .status == "completed" and
      (.conclusion | IN("success", "skipped", "neutral") | not)) then "failed"
    elif any(.check_runs[]; .status != "completed") then "pending"
    else "green" end' <<<"$j"
}
wait_green(){ local i s; for i in $(seq 120); do s=$(ci "$1"); [ "$s" = pending ] || break; sleep 60; done
  [ "$s" = green ] || die "CI $s on $1"; }
pr_state(){ retry gh pr view "$1" --json state,mergeable,mergeStateStatus,headRefOid \
  --jq '"\(.state) \(.mergeable) \(.mergeStateStatus) \(.headRefOid)"'; }

while read -r pr branch base _; do
  [ -z "${pr:-}" ] || [ "$pr" -lt "$START" ] && continue
  retry git fetch -q origin || die "fetch"
  read -r state _ _ _ <<<"$(pr_state "$pr")"
  [ "$state" = MERGED ] && { log "#$pr already merged, skipping"; continue; }
  head=$(git rev-parse "origin/$branch")
  [ "$base" = - ] && base=$(git merge-base origin/main "$head")
  out=$(git merge-tree --write-tree --merge-base="$base" origin/main "$head") \
    || die "#$pr conflicts with main: $out"
  tree=$(head -1 <<<"$out")
  own=$head   # on a restart, judge by the branch's own commit, not our merge commit
  [ "$(git log -1 --format=%s "$head")" = "Merge main into $branch" ] && own=$(git rev-parse "$head^1")
  tested=no; [ "$tree" = "$(git rev-parse "$own^{tree}")" ] && tested=yes
  [ "$(ci "$own")" = green ] || die "#$pr: CI on its own commit $own is not green"
  if ! git merge-base --is-ancestor origin/main "$head"; then
    head=$(git commit-tree "$tree" -p "$head" -p origin/main -m "Merge main into $branch")
    retry git push -q origin "$head:refs/heads/$branch" || die "push $branch"
    log "#$pr pushed merge commit $head (tree already tested: $tested)"
  fi
  [ "$tested" = no ] && { log "#$pr has a new tree, waiting for CI"; wait_green "$head"; }
  for i in $(seq 20); do
    read -r state mergeable status sha <<<"$(pr_state "$pr")"
    [ "$sha" = "$head" ] && [ "$mergeable" = MERGEABLE ] &&
      { [ "$status" = CLEAN ] || { [ "$status" = UNSTABLE ] && [ "$tested" = yes ]; }; } && break
    sleep 15
  done
  [ "$sha" = "$head" ] && [ "$mergeable" = MERGEABLE ] || die "#$pr state: $mergeable $status $sha"
  retry gh pr merge "$pr" --squash --match-head-commit "$head" >/dev/null \
    || [ "$(pr_state "$pr" | cut -d' ' -f1)" = MERGED ] || die "merge #$pr"
  retry git fetch -q origin || die "fetch"
  [ "$(git rev-parse 'origin/main^{tree}')" = "$tree" ] || die "main after #$pr is not the computed tree"
  log "merged #$pr as $(git rev-parse --short origin/main)"
done < "$PLAN"
log "all done"
```

Run it from a worktree with a detached HEAD, log to a file
(`land-stack.sh plan.txt 2>&1 | tee -a land.log`), and restart from the PR it
stopped at once the cause is fixed. It waits for CI on every new tree; where
several new trees come at the end, running the full check on an exported copy
of the final tree and waiting only on the last PR is faster and equally safe.
