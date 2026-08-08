# Cowork git mechanics — device mounts, sessions, and their traps

Hard-won environment facts. Read before running git on any Cowork
device mount (`/sessions/<session>/mnt/...`). These are not style preferences;
each one was a real failure.

## The mount refuses deletes — so git locks stick

git creates lock files (`index.lock`, `HEAD.lock`, `ORIG_HEAD.lock`) and deletes
them when done. On Cowork device mounts **deletes fail**, so every git command
leaves its lock behind, and the next command refuses to start. The mount does
allow **moves** — that is the whole trick:

```bash
unlock() { find .git -maxdepth 3 -name "*.lock" -type f 2>/dev/null | \
  while read -r l; do mv "$l" "${l%.lock}.stale-$(date +%s%N)"; done; true; }
```

(The find-based version also catches ref locks like
`refs/heads/<branch>.lock`, `packed-refs.lock` and `config.lock`, any of which
block their operation just as hard as `index.lock`.)

- Call `unlock` before **every** git command: `unlock; git add -A`,
  `unlock; git commit -m "..."`, `unlock; git log --oneline -1`.
- **Shell state does not persist between tool calls** — each device_bash call
  is a fresh `bash -c`. Inline the `unlock` definition and the identity exports
  in every call; a function defined last call does not exist now.
- `warning: unable to unlink … tmp_obj_…` on every command is **normal** here
  and does not mean failure — trust `git log --oneline -1`, not the warnings.
- Renamed `.git/stale-*` files accumulate; sweep them into `_to_delete/`
  occasionally (never delete — move).
- A repo with a **live** lock and no running git process was left by an earlier
  session: move it aside and proceed. This exact condition has silently
  frozen repos for weeks — uncommitted work piling up behind a lock nobody saw.

## Multi-lock commands fail — avoid cherry-pick/rebase/merge-with-conflicts

Commands that cycle the index lock repeatedly inside one run (`cherry-pick`,
`rebase`, conflicted merges) die midway on these mounts: they cannot release
their own lock between internal steps, so they half-apply and abort. Single-lock
commands (`add`, `commit`, `branch`, `log`, fast-forward merges) work with the
unlock pattern. For a small change stranded on another commit, recreate it
manually (apply the diff by hand, `add` + `commit`, reference the source sha in
the message) instead of cherry-picking. For anything bigger, hand the operation
to the user's terminal.

## Deleting branches: move the ref file

`git branch -d` needs to unlink the ref file — refused on these mounts. Instead:
resolve the sha with `git rev-parse <branch>` (works whether the ref is loose
or packed) into a manifest, then `mv` the loose ref file out (e.g. into
`_to_delete/`). **Check `.git/packed-refs` too**: a ref that has been packed
(automatic after `git gc`/`pack-refs`) has no loose file, survives the mv, and
the `find` verification below never sees it — grep packed-refs for the branch;
if present, rewrite packed-refs without that line via write-new-then-rename
(moves work here), or hand the deletion to the user's terminal. Same effect,
fully recoverable. Branch names
with slashes live in subdirectories (`refs/heads/feat/x`); the emptied namespace
dirs cannot be rmdir'd (that's a delete) but git ignores them. Beware: directory
listings on these mounts can serve stale cache — verify ref deletion with
`find .git/refs/heads -type f`, not `ls`.

## Never run a bare `git status`

It refreshes the index, which takes `index.lock`, which sticks (above). Use
`git --no-optional-locks status --porcelain` when you need status, or read
state from files: `.git/HEAD`, `.git/refs/heads/*`, `.git/logs/HEAD` (reflog),
`.git/packed-refs`. File reads can never leave a lock.

## Author identity

Commits abort without an identity. Resolve in this order: (1) the repo's or
global `git config user.name`/`user.email` — use it if set; (2) an identity
recorded in the repo's profile; (3) only as a last resort, and saying so in the
commit proposal, the agent identity:

```bash
export GIT_AUTHOR_NAME="Claude" GIT_AUTHOR_EMAIL="noreply@anthropic.com"
export GIT_COMMITTER_NAME="Claude" GIT_COMMITTER_EMAIL="noreply@anthropic.com"
```

On a repo that may ever go public, agent-attributed commits mislead blame and
contribution history — prefer the user's identity whenever it is configured.

## Two execution environments, split capabilities

- **device_bash** (the user's machine via the Cowork VM): sees the real repos,
  runs git against them — but has **no network**. No fetch, no push, no gh.
- **Cloud container Bash**: has network — `git ls-remote <https-url>` works for
  checking where origin's branches really are — but GitHub **API** calls are
  proxied and need the repo attached to the session (`add_repo`); unattached
  repos return an access error.
- Consequence: pushes, PR creation, and merges need either an attached repo
  (then the session can do them) or the user's terminal (then use the handover
  format from SKILL.md). Verification of "did it land on GitHub" is always
  possible via `ls-remote` from the container.

## Staged copies go stale — trust hashes, not metadata

`device_stage_files` snapshots a file into the container. Two traps:

1. A partial staging makes absent files look missing — never conclude "file
   doesn't exist" from a staged tree; check the device.
2. Re-staging a file **modified earlier in the same session** can serve the old
   bytes even while the tool reports the new size/mtime (mount dir-cache).
   Before basing an edit on a re-staged file, compare `sha256sum` device-side vs
   container-side; keep your own copy of anything you wrote as the authoritative
   base.

## Session-boundary rules

- A file edited on the device after the last commit is an **uncommitted change
  aging silently** — surface it at session start, resolve it by session end.
- Verify handovers: a user's "done" has twice meant "the command silently
  failed" (a `cd "~/..."` that never expanded; a gh command on a deleted
  branch). Check refs/`ls-remote` after every handover.
- One writer per repo at a time across machines and sessions; when cloud and
  local sessions may both touch a repo, fetch/compare at every session start.
