#!/usr/bin/env bash
# Squash-merge a stack of PRs in order. Skips CI reruns where the landed tree
# is the tree CI already tested; waits for CI where the tree is new.
# Usage: REPO=owner/name [TRUNK=main] land-stack.sh <plan-file> [first-pr]
set -euo pipefail
PLAN=$1 START=${2:-0} REPO=${REPO:?set REPO=owner/name} TRUNK=${TRUNK:-main}
M=origin/$TRUNK
log(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }   # stderr: callers capture stdout
die(){ log "STOP: $*"; exit 1; }
retry(){ local i; for i in 1 2 3 4 5; do "$@" && return 0; log "retry $i: $*"; sleep $((i * 20)); done; return 1; }

ci(){ # prints green, pending or failed for a commit's check runs
  local j; j=$(retry gh api "repos/$REPO/commits/$1/check-runs?per_page=100") || { echo failed; return; }
  jq -r 'if .total_count == 0 then "pending"
    elif any(.check_runs[]; .status == "completed" and
      (.conclusion | IN("success", "skipped", "neutral") | not)) then "failed"
    elif any(.check_runs[]; .status != "completed") then "pending"
    else "green" end' <<<"$j"
}
wait_green(){ local i s; for i in $(seq 120); do s=$(ci "$1"); [ "$s" = pending ] || break; sleep 60; done
  [ "$s" = green ] || die "CI $s on $1"; }
pr_state(){ retry gh pr view "$1" -R "$REPO" --json state,mergeable,mergeStateStatus,headRefOid \
  --jq '"\(.state) \(.mergeable) \(.mergeStateStatus) \(.headRefOid)"'; }

while read -r pr branch base _ <&3 || [ -n "${pr:-}" ]; do
  case "${pr:-#}" in \#*) continue;; esac
  [ "$pr" -lt "$START" ] && continue
  retry git fetch -q origin || die "fetch"
  read -r state _ _ _ <<<"$(pr_state "$pr")"
  [ "$state" = MERGED ] && { log "#$pr already merged, skipping"; continue; }
  [ "$state" = OPEN ] || die "#$pr state '$state'"
  head=$(git rev-parse "origin/$branch")
  [ "$base" = - ] && base=$(git merge-base "$M" "$head")
  out=$(git merge-tree --write-tree --merge-base="$base" "$M" "$head") \
    || die "#$pr conflicts with $TRUNK: $out"
  tree=$(head -1 <<<"$out")
  own=$head   # on a restart, judge by the branch's own commit, not our merge commit
  [ "$(git log -1 --format=%s "$head")" = "Merge $TRUNK into $branch" ] && own=$(git rev-parse "$head^1")
  tested=no; [ "$tree" = "$(git rev-parse "$own^{tree}")" ] && tested=yes
  [ "$(ci "$own")" = green ] || die "#$pr: CI on its own commit $own is not green"
  if ! git merge-base --is-ancestor "$M" "$head"; then
    head=$(git commit-tree "$tree" -p "$head" -p "$M" -m "Merge $TRUNK into $branch")
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
  [ "$sha" = "$head" ] && [ "$mergeable" = MERGEABLE ] &&
    { [ "$status" = CLEAN ] || [ "$status" = UNSTABLE ]; } || die "#$pr state: $mergeable $status $sha"
  retry gh pr merge "$pr" -R "$REPO" --squash --match-head-commit "$head" >/dev/null \
    || [ "$(pr_state "$pr" | cut -d' ' -f1)" = MERGED ] || die "merge #$pr"
  retry git fetch -q origin || die "fetch"
  [ "$(git rev-parse "$M^{tree}")" = "$tree" ] || die "$TRUNK after #$pr is not the computed tree"
  log "merged #$pr as $(git rev-parse --short "$M")"
done 3< "$PLAN"
log "all done"
