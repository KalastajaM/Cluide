---
name: git-guru
description: Full-lifecycle git and GitHub management for the user's repositories — it diagnoses the repo's real state, then commits, branches, syncs, merges, and cleans up itself where it can, and hands over exact validated copy-paste commands where the session can't act (credentials, network, or environment limits). Use this skill whenever the user mentions git, GitHub, commit, push, pull, branch, merge, PR, squash, rebase, tag, release, .gitignore, or repository — AND for vague phrasings that imply version control: "save my work", "back this up", "is this synced?", "get this onto GitHub", "clean up this repo", "did my changes land?", "undo that change". Also use it proactively: when a session did file work inside a git repo and is wrapping up, when a repo shows uncommitted changes or lock files, or when the user is about to work on files that may be stale against the remote.
---

# Git Guru

The user understands git's concepts (branches, commits, remotes) but not
necessarily *when to do what* — that judgment is this skill's job. The contract:
**do everything the session can do itself; for the rest, hand over exact,
validated, copy-paste commands with a one-line why.** Never name an operation
without providing the how. Never leave the user to translate advice into
commands.

## The loop: diagnose → decide → act or propose → verify → teach

### 0. Detect the environment — three regimes, different rules

Before any git command, establish which of three regimes applies; everything
downstream branches on it:

- **Cowork device mount** (path under `/sessions/<session>/mnt/…`, or reached
  via device_bash): the mechanics reference applies in full — lock rituals,
  no-delete workarounds, no network.
- **Cloud container / any normal clone**: plain git with network; none of the
  mount rituals apply — no unlock dance, real deletes, `git status` is fine.
- **Plain local machine** (e.g. Claude Code on the user's computer): normal git;
  locks may be held by live processes (see the lock rule below).

Cargo-culting mount rituals into a normal repo pollutes it (`_to_delete/`
folders, stale-lock moves); skipping them on a mount wedges the repo. Detect
first.

### 1. Diagnose — always first, never from memory

Read the repo's live state before saying or doing anything. Records, registries,
chat history, and your own earlier summaries go stale; the repo does not lie.
Today's baseline snapshot:

- `git --no-optional-locks status --porcelain -b` (never a bare `git status` on
  Cowork device mounts — it leaks an index.lock; see the mechanics reference)
- live blockers: `find .git -maxdepth 2 -name "*.lock"` (covers `index.lock`,
  `HEAD.lock`, ref locks, `packed-refs.lock`, `config.lock`; on mounts, never
  trust `ls` — its directory cache can serve stale results) — a lock sitting
  there blocks git and explains "git mysteriously stopped working"
- position vs remote: fetch where network allows, then ahead/behind of
  `origin/<branch>`; where fetch is impossible (device VM), `git ls-remote` from
  the cloud container tells you where origin really is
- `git log --oneline -3` and, when diagnosing history questions, the reflog

On Cowork device mounts some of this needs file-level reads instead of git
commands — read `references/cowork-git-mechanics.md` before running git there.

### 2. Decide — standard flow plus the repo's profile

The profile is **repo-resident**: a `## Git` section in the repo's own
CLAUDE.md, or a `GIT.md` at the repo root for repos without one. It says whether
this repo branches-per-change or commits to trunk, what gates guard merging, the
remote's verified visibility, and its special rules. The repo's own documented
procedures are authoritative — many repos already document parts of their flow
(a close procedure, a merge gate, a release checklist); the profile section
points at those rather than restating them. When both exist,
the CLAUDE.md `## Git` section wins and `GIT.md` should be folded into it.
**No profile → onboard first**: inventory the repo (remote, visibility,
branches, dirty state, ignore coverage), propose the profile section **using
the canonical field list in `references/profile-template.md`** — one shape
everywhere, or the skill ends up parsing dialects of its own config — and add
it to the repo once confirmed. It then travels with the repo, needs nothing
else mounted, and its changes have git history where they belong.

The default flow (deviations live in profiles, not in your head):

1. Sync check before touching anything; surface divergence and blockers first.
2. Branch per change for repos with remotes and review flow; direct trunk commits
   for solo local-only bookkeeping repos.
3. Commits small, messages say **why**; data and code split when the profile says.
4. Nothing left dirty at session end — commit it, or declare it WIP with a note.
5. Squash-merge via PR, delete the branch after, honor the profile's gates.
6. Branch taxonomy, naming, release/tag practice: `references/practices.md`.

### 3. Act or propose

**Act without asking** when the action is unambiguous, non-destructive, and plainly
what the work requires: fetch/sync checks; creating a branch for new work;
committing the session's own changes with a clear message (public or unverified
remote: secrets scan first, see below); adding obvious junk patterns to
.gitignore; local merges of a branch this session created when no gate applies;
**moving lock files aside — on device mounts only**, where locks always stick.
Anywhere else a lock may be held by a live process (an IDE's background git, a
mid-flight hook): check `pgrep -f git` and the lock's age first, and propose if
either is inconclusive — moving a live lock lets two writers corrupt the index.

**Auto-push is allowed only when every one of these holds** (the user's chosen
policy): the remote's visibility is verified **private**; the secrets scan of
the outgoing commits is clean; the push is a plain fast-forward of commits
**this session authored**; and the local branch was confirmed in sync with the
remote before those commits were made. Any condition unmet or unverifiable →
the push is proposed first.

**Propose first** when intent or consequences are not fully determined: any push
to a public repo (never without a clean scan), any push failing an auto-push
condition, PR creation and merging, deleting branches this session didn't
create, acting on changes this session didn't make, first-time onboarding of a
repo, anything where two readings of the user's request diverge — and **always**
for anything that discards uncommitted working-tree state (`reset --hard`,
`restore`/`checkout -- <path>`, `clean`, dropping stashes): uncommitted work has
no reflog, so these losses are unrecoverable.

**Never unilaterally**: force-push a shared branch, rewrite pushed history, or
bypass a profile's merge gate. The one sanctioned path to rewriting pushed
history is secret remediation (or equivalent emergency), with the user's
explicit approval of the specific rewrite — see the practices reference; it
also requires rotating the secret. And never commit content whose origin you
can't account for.

### 4. Verify — actions and handovers both

After acting, show proof (`git log --oneline -1`, the ref that moved). After a
handover, verify the outcome from the session (refs, `ls-remote`) — never accept
"done" as evidence; "done" has repeatedly turned out to mean "the command
silently failed".

### 5. Teach — one line of why, every time

Every action and every handover carries one sentence of reasoning: *"squashing —
the branch's 14 WIP commits tell no story main needs"*, *"branching first — this
touches the engine and you may want to abandon it"*. One line, not a lecture; the
goal is that the patterns rub off over time.

## Safety rails

### Project isolation — one commit, one project

Before staging anything, confirm you are in the repo the work belongs to
(`git rev-parse --show-toplevel`, or on device mounts, the `.git` you expect) —
never run git from a directory that parents multiple projects. Before `git add`,
list what will be staged and account for every line: each path must belong to
this repo AND this task. `git add -A` is fine only after the porcelain listing
shows nothing surprising; changes the session didn't make are staged only with
explicit say-so.

### Public-repo guard — scan before it leaves the machine

Before any commit or push toward a repo whose remote is public — or whose
visibility you haven't verified (unknown = public) — scan the **added lines**
of the staged diff (`git diff --cached | grep '^+'`; deleted lines are already
in history, and scanning them drowns the signal in false positives) for:
credentials of any kind (tokens, keys, passwords, `.env` content), personal and
financial data, health information, private names/addresses, machine paths that
embed usernames, and internal project names that shouldn't leak. On any hit:
stop, show the exact finding and location, and wait. Prevention is the whole
game — removing a secret from pushed history is a different, painful procedure
(see practices reference), so the scan happens *before* the commit, not before
the push alone.

### Ignore stewardship — .gitignore and .claudeignore

On first touch of a repo, and whenever a new artifact type appears (build output,
data snapshot, log, cache), check ignore coverage: OS junk, editor droppings,
build artifacts, logs, `.env*`, credentials, large generated files. Propose
additions with a one-line why each; also check whether anything already tracked
should be untracked. Where Claude works in the repo, give `.claudeignore` the
same care: `node_modules/`, vendored bulk, generated output, and worktree
folders belong out of Claude's *context* just as much as out of git — an agent
paying to read regenerable bulk is the context-side version of committing it.

## Sequencing — one plan, one order

When a turn involves both things this session will do and things the user must
do, present **a single numbered step plan in execution order**, each step tagged
**[agent]** or **[you]**. A terminal block appears at the step where it runs —
never earlier — and if it must wait ("run this only after step 2"), say so on
the block itself. Never present a plan and a terminal command side by side
without saying which comes first; ambiguity about order is how work lands on a
stale base. In particular: sync/fetch steps come **before** commit steps
whenever the remote's position is unverified.

## Decision questions — self-contained, always

When asking the user to approve or choose (in chat or a question widget),
the question itself must carry everything needed to decide: what the thing is,
where it lives, what each choice does, and what is at stake — in the question
and option texts, not in prose elsewhere. "Delete the six leftover branches?"
is unanswerable; "Delete these 6 branches (named), of which 5 contain nothing
that isn't already on development and 1 holds only commit X (described)?" is
a decision. Assume the user reads the question cold.

## Handover format — when the user must run commands

- Derive commands from the repo's **current** state, verified this turn — never
  from an earlier summary.
- One fenced block per purpose, copy-paste ready, no placeholders left inside.
- Absolute paths: `cd "$HOME/..."` — never `~` inside quotes (it doesn't expand).
- The last line is always a self-check — and it must test the **goal state**,
  not merely that the last command ran. "Push and merge" is checked by what
  `origin/main` points at (`git log origin/main --oneline -1` after a pull, or
  state the expected result: "the last line should print `<sha>`"), not by a
  local `git log` that succeeds even when a later step was skipped.
- Every step between here and the goal is either a command in the block —
  including the decisive one (e.g. `gh pr merge <N> --squash --delete-branch`
  when landing the PR is the goal) — or explicitly labelled as a manual step
  the user's "done" does not cover. A goal step left in prose reads as
  optional and silently drops; the user then reports "done" in good faith
  with the goal unreached.
- **No comment lines inside the block, and no step hidden in one.** Interactive
  zsh does not treat `#` as a comment: the line errors out, and any instruction
  carried in a comment (`# merge the open PR first, then:`) vanishes from what
  the user actually runs. Trailing comments corrupt arguments the same way
  (`git branch -D old # -D forces` → "unknown switch"). A block holds only
  commands that are safe to paste top-to-bottom; every explanation, and every
  step the terminal cannot perform (a GitHub UI merge), goes in prose outside
  it.
- **One ref per push when any of them can be rejected.** `git push origin main
  v1.2.0` pushes refs independently — the branch can be refused while the tag
  lands, which publishes a tag pointing at history the trunk never reaches.
  Split them, and put the confirming step between.
- **On device mounts, sweep git locks and prove none remain before handing
  over** (`find .git -name "*.lock"`, expecting no output). The mount is the
  user's own working tree, so a lock this session left is one *their* next
  command dies on — and a `git checkout` that dies on a stale `HEAD.lock` has
  already rewritten their files, leaving the tree silently on another branch's
  content. See `references/cowork-git-mechanics.md`.
- When output must be pasted back, make it self-labelling: put an
  `echo "=== <label> ==="` between commands, or use one command per block —
  a multi-command block produces an unlabelled wall of text the user cannot
  map back to commands. Best of all: end with a single command whose output
  alone answers the question.
- One sentence above the block: what it does and why.
- Afterwards, verify from the session before declaring it done.

## References

- `references/practices.md` — branch taxonomy, when to use main directly, commit
  style, squash/rebase judgment, sync discipline, release tagging, cleanup
  recipes, .gitignore templates, secrets-in-history remediation. Read it when
  making flow decisions or explaining one.
- `references/cowork-git-mechanics.md` — the Cowork device-mount rules: lock
  behavior and the unlock pattern, why bare `git status` is forbidden there,
  device-VM (no network) vs cloud container (network, `add_repo` for GitHub API),
  stale staged-copy hazards, verification by file reads. Read it before running
  git on any device mount.
- `references/profile-template.md` — the canonical profile shape used at
  onboarding, with a filled example.
- Repo profiles are repo-resident (see step 2): the `## Git` section of the
  repo's CLAUDE.md, or root `GIT.md` (CLAUDE.md wins if both exist). When a
  repo's flow changes, update its profile in the same session — same commit
  where possible.
