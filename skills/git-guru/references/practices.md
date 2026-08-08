# Git practices — the judgment layer

The rules of thumb a professional applies without thinking. Each section says
what to do, when, and why — so the why can be passed on as the one-liner.

## Branch taxonomy

For solo projects, trunk-based development with short-lived
branches is the professional norm. No `develop` branch, no gitflow — those solve
team-coordination problems a solo developer doesn't have, and add ceremony
they'd pay for daily.

- **main (or master)** — always releasable. Every commit on it should leave the
  project in a state you'd be comfortable coming back to in six months.
- **feature/<slug>** — new capability. Branch when the work might take more than
  one sitting, might be abandoned, or touches something other work depends on.
- **fix/<slug>** — bug fix. Same lifecycle, usually shorter.
- **chore/<slug>** — mechanical work: dependency bumps, reorganization, cleanup.
- Branches live days, not weeks. A branch older than ~a week is a smell: finish
  it, merge it, or delete it deliberately.

**When to commit straight to trunk** (no branch): solo local-only bookkeeping
repos (registries, logs, ledgers); single-file doc fixes; anything where a PR
would have no reviewer and no gate — ceremony without benefit. The repo's
profile records which mode applies; when in doubt, branch — an unneeded branch
costs one command, an unwanted trunk commit costs a revert.

## Commit style

- Small and thematic: one logical change per commit. If the message needs "and",
  consider two commits.
- The message's first line says **why/what moved**, not which files changed —
  git already knows the files. ~60 chars, imperative or descriptive, consistent
  within a repo. Conventional prefixes (`feat:`, `fix:`, `docs:`, `chore:`) are
  nice but consistency matters more than convention.
- Data and code in separate commits when both changed (a future bisect over the
  scripts should not step through data) — some repos codify this in their own close procedure; honor it.

## Sync discipline — the stale-base problem

The single biggest source of solo-developer git pain: work starting on files that are
behind the remote or behind another machine/session.

- **Fetch before starting work** in any repo with a remote; compare ahead/behind.
- **`git pull --ff-only`**, never a bare `git pull` — a merge-pull silently
  creates merge commits that entangle histories. If `--ff-only` refuses, local
  and remote have diverged: stop and look before doing anything.
- Divergence playbook: local-only commits on top of a moved remote → rebase them
  (`git pull --rebase`) if unpushed *(terminal-only on device mounts — no
  network there, and rebase half-applies; hand it over)*; if the local work is
  experimental, branch it out (`git branch rescue/<slug>`) and reset trunk to
  origin with `git reset --hard origin/<branch>` — **propose-first, always**:
  `--hard` discards uncommitted working-tree state, which has no reflog.
- Treat parallel writers (cloud session + local session + another machine) like
  a single-writer database: **one writer at a time per repo**, and a sync check
  at every session boundary.

## Squash, rebase, and history judgment

- **Squash-merge a branch** when its commit trail is WIP noise ("fix", "fix 2",
  "works now") — main gets one meaningful commit, the branch kept its scratch
  history until deletion. `gh pr merge --squash` (GitHub) or
  `git merge --squash <branch>` then `git commit` (local — `--squash` stages
  but does not commit).
- **Merge normally (no squash)** when the branch's commits are individually
  meaningful and worth preserving on main.
- **Rebase** is for unpushed local commits only (cleaning up before sharing).
  The iron rule: **never rewrite history that has been pushed** — someone
  (including a cloud session) may have based work on it. Amend/rebase freely
  before pushing; after pushing, fix forward with new commits or `git revert`.
- **Undo judgment**: pushed → `git revert <sha>` (new commit that undoes);
  unpushed → `git reset --soft HEAD~1` (uncommits, keeps the changes staged) or
  `--mixed` (keeps them unstaged); `--hard` discards them and is propose-first,
  always. When unsure whether it was pushed, revert.

## Releases and tags

Solo projects version with **tags on main**, not release branches:
`git tag -a v1.2.0 -m "..." && git push origin v1.2.0`. A GitHub release on top
of the tag (`gh release create v1.2.0 --notes "..."`) adds a download page and
notes — worth it when anyone else consumes the project. Keep a CHANGELOG.md when
anything downstream consumes the project; update it in the same branch as the
change. **Large files**: GitHub rejects files >100 MB and warns >50 MB — data
snapshots and binaries belong in .gitignore or git-lfs, decided *before* the
first commit containing them (removing them later means rewriting history).

## .gitignore

Baseline for every repo — extend per project type:

```
.DS_Store
Thumbs.db
*.log
*.tmp
.env
.env.*
node_modules/
__pycache__/
dist/
build/
```

Plus per-repo: data snapshots, generated outputs, backup folders, quarantine
folders like `_to_delete/` — and whenever the `_to_delete/` quarantine pattern
is used in a repo (it lives at the repo root), the ignore rule for it is
mandatory in the same change, or it haunts every status. Two checks whenever
touching ignore files: (1) is anything **tracked** that the rules would ignore —
if so it stays tracked until `git rm --cached`; (2) does an ignore rule cover
one artifact but not its near-identical sibling.

## Secrets and personal data

- Scan **staged diffs**, not just files: `git diff --cached` before commit in
  any public-remote repo. Patterns: `key`, `token`, `secret`, `password`,
  `BEGIN.*PRIVATE`, `.env` content, long high-entropy strings, IBANs, personal
  addresses, health terms, absolute paths with usernames.
- Unknown visibility = public. Check with `gh repo view --json visibility` or
  the GitHub UI before the first push, then record it in the repo's profile.
- **If a secret already reached pushed history**: removing it requires history
  rewriting (`git filter-repo`) AND rotating the secret — the rewrite alone is
  not enough, because clones and caches exist. This is exactly why the scan
  runs before commit, not before push: unpushed mistakes cost one reset,
  pushed ones cost a rotation.

## New repo / first publish

The lifecycle stage most likely to be asked for as "get this onto GitHub":

1. `git init -b main` (name the trunk deliberately; `development` if the
   profile will say so), first `.gitignore` **before** the first commit (junk
   committed now is history forever), first commit.
2. **Visibility is a decision, not a default**: private unless there is a
   reason to publish (this skill's own stance: unknown = public, so decide and
   record it). `gh repo create <name> --private --source . --push` creates the
   repo, wires the remote, and pushes in one step; `--public` only after the
   secrets/personal-data scan of the whole tree, not just the diff.
3. Write the repo's profile (`## Git` section) immediately — a repo born with
   its flow documented never joins the mess backlog.

## Merge conflicts

- **Recognize**: the command stops with `CONFLICT`, `git status` shows
  `both modified`, files contain `<<<<<<<`/`=======`/`>>>>>>>` markers.
- **First decision — resolve or abort**: `git merge --abort` /
  `git rebase --abort` returns cleanly to the pre-attempt state at zero cost.
  Abort when the conflict is a surprise; resolve when the overlap was expected
  and understood.
- **Resolve**: open each conflicted file, keep the intended lines, remove the
  markers, `git add <file>`, then `git commit` (merge) or
  `git rebase --continue`. Never commit a file that still contains markers —
  search for `<<<<<<<` before committing.
- **On device mounts**: conflicted merges half-apply (multi-lock); don't start
  them there. Hand the whole operation over with this shape: the exact merge
  command, the abort command as the escape hatch, and "paste me the conflict
  list if you want the resolution decided together."

## Stash — and why a branch usually beats it

`git stash` shelves uncommitted changes ("save my work" mid-task). It is the
right tool for a minutes-long interruption on the same branch. For anything
longer, prefer a WIP branch (`git checkout -b wip/<slug>` + commit): stashes
are invisible in `git branch`, easy to forget, and `stash drop`/`clear` losses
are unrecoverable — which is also why dropping a stash is propose-first.
`git stash list` belongs in the diagnose step; a repo with old stashes has
forgotten work in it.

## Cleanup recipes

- **Stale branches**: `git branch --merged main` lists branches whose commits
  are ancestors of main — safe to delete. **Squash-merged branches never show
  up there** (the squash creates a new commit; the branch's own commits are not
  ancestors), so under this skill's default flow `--merged` proves little. The
  checks that actually answer "is this branch's work in main": an empty
  `git diff main...<branch>`, `git cherry main <branch>` showing only `-` lines,
  or `gh pr list --state merged --head <branch>`. A branch failing all three
  gets a look before deletion: `git log main..<branch> --oneline` shows what
  would be lost.
- **A pile of uncommitted changes of mixed vintage** (a repo left uncommitted for weeks):
  don't guess. Diff-review the changes, group them into thematic commits
  (`git add -p` or explicit paths), commit each with a message reconstructing
  the why, and only then sync with the remote.
- **Untangling "I did things and now it's weird"**: reflog first
  (`git reflog -15`) — it shows what actually happened, and nearly everything
  is recoverable from it. Diagnose before touching anything.
