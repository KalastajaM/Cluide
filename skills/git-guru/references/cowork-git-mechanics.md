# Cowork git mechanics — device mounts, sessions, and their traps

Hard-won environment facts. Read before running git on any Cowork
device mount (`/sessions/<session>/mnt/...`). These are not style preferences;
each one was a real failure.

## The mount refuses deletes — so git locks stick

**Check first whether deletion can be granted.** Live-verified 2026-10-15 in a
Cowork cloud session linked to a Mac: deletes were refused by default
("Operation not permitted"), but the session offered a delete-permission
request; once the person approved it for the connected folder, `rm` and
ordinary git (`checkout -b`, `commit`, lock cleanup) worked for the rest of the
session. Where that request exists, ask for it once, naming the repo's folder,
and skip the rituals below. Where it does not, or the person declines,
everything in this section applies. Anthropic documents that Cowork asks before
permanently deleting files ([Use Claude Cowork safely](https://support.claude.com/en/articles/13364135-use-claude-cowork-safely));
the folder-wide grant observed here is live-verified only, so re-check it
after a desktop update.

git creates lock files (`index.lock`, `HEAD.lock`, `ORIG_HEAD.lock`) and deletes
them when done. On Cowork device mounts **deletes fail**, so every git command
leaves its lock behind, and the next command refuses to start. The mount does
allow **moves** — that is the whole trick:

```bash
unlock() { find .git -name "*.lock" -type f 2>/dev/null | \
  while read -r l; do mv "$l" "${l%.lock}.stale-$(date +%s%N)"; done; true; }
```

(The find-based version also catches ref locks like
`refs/heads/<branch>.lock`, `packed-refs.lock` and `config.lock`, any of which
block their operation just as hard as `index.lock`. Do not bound it with
`-maxdepth`: a branch ref lock sits at depth 3 and a namespaced one
(`refs/heads/feat/x.lock`) at depth 4, and the one you miss is the one that
wedges the next command.)

- Call `unlock` before **every** git command: `unlock; git add -A`,
  `unlock; git commit -m "..."`, `unlock; git log --oneline -1`.
- **And sweep again after the last git command of the turn, before handing
  anything over.** The mount is not a private copy — it is the user's own
  working tree, so the lock this session left behind is the one *their* next
  command dies on. Verify with `find .git -name "*.lock"` returning nothing,
  and treat that check as part of the handover, not as tidiness.
- **A stranded lock does not just block — it can silently revert the user's
  files.** `git checkout <branch>` updates the working tree first and writes
  `HEAD` second: hitting a stale `HEAD.lock` at that second step leaves the
  files rewritten to the target branch's content while `HEAD` still points at
  the old branch. Nothing errors afterwards. Everything the user runs next —
  `git tag`, `git commit`, a build — operates on a tree that is not the branch
  they think they are on. This has published a release tag on the wrong commit.
  When a user reports a mid-block `cannot lock ref` failure, do not just retry:
  re-derive `HEAD`, the branch refs, and whether the working tree matches the
  commit it claims (`git show HEAD:<path> | cmp - <path>`), because the failed
  command may have half-succeeded.
- **Shell state does not persist between tool calls** — each device_bash call
  is a fresh `bash -c`. Inline the `unlock` definition and the identity exports
  in every call; a function defined last call does not exist now.
- `warning: unable to unlink … tmp_obj_…` on every command is **normal** here
  and does not mean failure — trust `git log --oneline -1`, not the warnings.
- Renamed `.git/stale-*` files accumulate; sweep them into the repo's
  quarantine folder occasionally (never delete — move). Use the location the
  repo's profile names; the conventional default is `_to_delete/`, which must
  be gitignored in the same change. A repo that keeps all non-shipping files
  under one ignored folder (e.g. `development/_to_delete/`) wants it there, not
  at the root, where it would show up as an untracked folder in a published
  tree.
- **One git command per tool call**, lock sweep first. Filtering the
  `unable to unlink` noise with `| grep -v` is fine on read-only and
  index-only commands, but the pipe makes `$?` the grep's exit code: verify with
  `git log -1` or `git diff --cached --name-only`, never `echo $?`. **Never
  filter it on a command that touches the working tree** — there the unlink
  line *is* the failure.
- A repo with a **live** lock and no running git process was left by an earlier
  session: move it aside and proceed. This exact condition has silently
  frozen repos for weeks — uncommitted work piling up behind a lock nobody saw.

## Commands that rewrite tracked files fail — and fail half-way

Any git operation that replaces an existing tracked file unlinks it first, and
the mount refuses unlink. That rules out `git checkout <branch>`,
`git switch`, `git checkout -b <new> <other-base>`, `git merge` **including
fast-forwards**, `git reset --hard`, `git stash pop/apply`, `git restore`,
`git checkout -- <path>`, and the multi-lock commands (`cherry-pick`, `rebase`,
conflicted merges), which also cannot release their own lock between internal
steps.

The failure is not clean. `git checkout -b <new> main` has been seen to create
the branch and repoint HEAD, then fail to update the working tree; a checkout of
an existing branch moves HEAD while the files stay on the old branch's content,
and the only symptom is a list of `M <path>` lines that looks like ordinary
dirt. If a command prints modifications you did not make, that is what
happened: do not "clean up" by committing them.

Safe on the mount: `add`, `commit`, `branch <name>` (creates a ref without
touching files), `log`, `show`, `diff`, `rev-parse`, `update-ref`, mixed
`reset` (index only).

**Create and switch to a new branch without touching files** — the new branch
starts at the current HEAD, so the tree already matches:

```bash
git branch <new> && git symbolic-ref HEAD refs/heads/<new>
```

If either command trips over a lock it cannot clear, the field-proven fallback
writes the refs as files (redirection never unlinks; for a branch name with a
slash, `mkdir -p` its directory under `.git/refs/heads/` first):

```bash
git rev-parse HEAD > .git/refs/heads/<new> && echo "ref: refs/heads/<new>" > .git/HEAD && git reset -q
```

To start a branch from a *different* commit than the current one, the tree must
change: hand that to the user's terminal, or repair the tree as below.

**Restore a file to HEAD:** `git show HEAD:<path> > <path>` — redirection
truncates in place and never unlinks. Never `git checkout -- <path>`.

**Repair a stranded tree wholesale** (HEAD right, files from another branch):

```bash
git --no-optional-locks diff --name-only | while read -r p; do git show "HEAD:$p" > "$p"; done
```

then move aside any untracked paths that came from the other branch. This is
far better than handing the user a `git checkout -- .`, which asks them to
discard files they did not create.

**Commit part of a dirty tree:** `git add <explicit paths>` then commit — the
commit takes the index, not the tree, so an unrelated one-file fix can land on
the right parent before (or without) repairing the rest.

**Editing tracked files in place:** append with `>>`, rewrite with Python
`open(p, "w")` or `shutil.copyfile`; `sed -i` and `tar x` over existing files
replace by unlink and fail (tar silently skips existing files). For a small
change stranded on another commit, re-apply the diff by hand and reference the
source sha in the commit message instead of cherry-picking. For anything
bigger, hand the operation to the user's terminal.

## Deleting branches: move the ref file

`git branch -d` needs to unlink the ref file — refused on these mounts. Instead:
resolve the sha with `git rev-parse <branch>` (works whether the ref is loose
or packed) into a manifest, then `mv` the loose ref file out (into the repo's
quarantine folder). **Check `.git/packed-refs` too**: a ref that has been packed
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
Either way, add a `Co-Authored-By: Claude <noreply@anthropic.com>` trailer to
agent-made commits: `blame` then always distinguishes the agent's hand from the
user's, whichever identity authored the commit.

## Two execution environments, split capabilities

- **device_bash** (the user's machine via the Cowork VM): sees the real repos
  and runs git against them. Its network follows the account's egress
  allowlist and has varied by session: on 2026-08-04 it had none, on 2026-10-15
  `git fetch` and `git ls-remote` against a public GitHub repo worked. Test with
  `git ls-remote origin` instead of assuming either way; a push still needs
  credentials the VM may not hold.
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
- One writer per working tree at a time across machines and sessions; when
  cloud and local sessions may both touch a repo, fetch/compare at every
  session start. Detect a concurrent writer before staging:
  `find . -path ./.git -prune -o -newermt '-10 minutes' -type f -print` — files
  you did not touch that keep moving mean another session is live; stage
  explicit paths only.

## Syncing a mount from a networked clone

When the mount has no network but another environment does (a cloud container
with a clone), move objects with a bundle and file contents by direct write:

1. Networked side: `git fetch origin && git bundle create /tmp/x.bundle <mount-HEAD>..origin/main`.
2. Copy the bundle into the mount's quarantine folder (the host's file
   transfer tool).
3. Mount side: `git bundle list-heads <bundle>` to read the ref name inside,
   then `git fetch <bundle> <that-ref>:refs/remotes/origin/main`.
4. File contents outside git: for a few files, write them directly; for many,
   `git archive origin/main | gzip` on the networked side, extract to a folder
   **outside** the repo, then `cp -R <extracted>/. .` (cp truncates in place).
   Files deleted upstream must be moved away by hand.
5. `git update-ref refs/heads/main origin/main`, then plain `git reset`
   (mixed) so the index matches.

Verify with `git status --porcelain` via `--no-optional-locks`: an empty result
means tree, index and HEAD agree.
