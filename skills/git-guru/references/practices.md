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
  (`git pull --rebase`) if unpushed *(terminal-only on delete-refusing mounts:
  rebase rewrites tracked files and half-applies there; hand it over)*; if the local work is
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
- **A stack of dependent PRs** squash-merged in order needs an explicit merge
  base after each squash, or every later PR looks conflicting:
  `references/stacked-prs.md`.
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

Solo projects version with **tags on main**, not release branches. Write the
annotation from a heredoc so multi-line and non-ASCII text survives shell
quoting:

```bash
git tag -a v1.2.0 -F - <<'EOF'
v1.2.0 — what this release is
EOF
git push origin v1.2.0
```

Three ordering rules, each of which has cost a re-done release:

- **Tag only a commit that is already on the trunk in its final form.** Where
  the trunk squash-merges, the merged commit is a *new* sha, so a tag created
  on the pre-merge branch points at a commit the trunk never reaches — and
  under branch protection that tag cannot be fixed by pushing the branch. Land
  the PR, pull, then tag the merged commit.
- **Never push a branch and a tag in one command.** `git push origin main
  v1.2.0` pushes the two refs independently: a protected trunk refuses the
  branch and the tag lands anyway, publishing a tag pointing at unreachable
  history. Push the branch, confirm it landed, then push the tag.
- **Verify a tag by peeling it, not by the push succeeding**: `git ls-remote
  origin refs/heads/main "refs/tags/vX.Y.Z*"` and check `refs/tags/vX.Y.Z^{}`
  equals the trunk tip. Deleting and re-pushing a tag nobody has consumed yet
  is cheap; a wrong tag left in place is not.

On a trunk with branch protection, the release commit — changelog included —
goes through a PR like any other change. Read the repo profile's Gates field
before proposing a direct commit to trunk; proposing one on a protected repo
wastes a round trip and, if a tag rides along, leaves a mess to clean up.

**Where the user will see it.** A pushed tag appears in the repository's Tags
view and the branch/tag dropdown. The Releases page stays empty until a Release
object exists: `gh release create v1.2.0 --notes-file notes.md` adds the page,
notes and downloads — worth it when anyone else consumes the project. Say which
view to check, or a correct tag gets reported as "missing".

**Changelog: two models, and the profile picks one.** Keep a `CHANGELOG.md`
when anything downstream consumes the project.

- *Per change*: each PR adds its entry (often under `## [Unreleased]`), and the
  release renames the section. Simple, but parallel PRs conflict on the same
  lines, and stacked squash merges make every later PR look conflicting.
- *At tag time*: no PR touches the changelog; the release commit writes the
  entry from `git log <previous-tag>..HEAD`. No conflicts, but the whole record
  rests on commit subjects, so they must say what changed and why.

Never mix them: under the tag-time model, an entry added by a feature PR is a
defect, and an `[Unreleased]` section invites one. When the profile says
nothing, ask before adding the first entry rather than guessing. **Large files**: GitHub rejects files >100 MB and warns >50 MB — data
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
is used in a repo (at the location the repo's profile names; `_to_delete/` at
the root only when the repo has no ignored working folder), the ignore rule for
it is mandatory in the same change, or it haunts every status. Two checks whenever
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
4. When `gh` or a push fails unexpectedly, check auth first: `gh auth status`,
   then `gh auth login` — it is the cause of most first-publish failures.

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

## Worktrees — parallel work without the stash dance

`git worktree add ../repo-feature feature/x` gives a second working directory
sharing the same `.git`: two branches checked out at once, separate index and
tree, one history. When to reach for it:

- **Parallel agents or agent + human on one repo.** The one-writer-per-repo
  rule applies to a *working tree*, not the repo: give each writer its own
  worktree on its own branch and parallel work is safe. Claude Code does this
  natively (`.claude/worktrees/`).
- Reviewing or testing one branch while mid-work on another.
- A long-running experiment kept physically separate from the trunk checkout.

Not a substitute for branches — a worktree is *where* a branch is checked out,
nothing more. Clean up with `git worktree remove <path>` and
`git worktree prune`; a forgotten worktree pins its branch (git refuses to
delete a branch checked out anywhere). On Cowork device mounts, creation works
but removal needs deletes the mount refuses — create there if useful, clean up
from the user's terminal.

## Enforcement — physics where rules are prose

This skill's "never force-push" and "scan before commit" are instructions. For
any repo where agents operate, add enforcement that holds even on an agent's or
a human's bad day, and record what is enabled in the profile's Gates field.

- **Protect the trunk and stable line.** Require pull requests, block direct
  pushes, force-pushes and deletion. GitHub offers classic branch protection
  and the newer **rulesets** (Settings → Rules → Rulesets): rulesets can be
  switched between active and evaluate, have explicit bypass lists, can also
  target tags (protecting release tags from deletion or moving), and layer —
  where several apply, the most restrictive version of each rule wins. Prefer
  rulesets for new setups; both kinds can coexist.
- **Turn on secret scanning push protection** where the plan offers it
  (Settings → Advanced Security). It rejects a push containing a recognised
  secret before it reaches the remote — the server-side version of the staged
  scan. Individual users can also enable push protection for their own
  account, which covers their pushes to any public repository.
- **Give agent work its own branch namespace** (`claude/…`, `codex/…`), and,
  where the platform allows, restrict agent credentials to that namespace.
  GitHub's own coding agent works this way: it can only push to `copilot/`
  branches, stays subject to branch protection and required checks, and cannot
  approve or merge its pull requests. The namespace makes agent branches easy
  to find, review and clean up.
- **Local hooks catch what remote rules see too late.** A pre-commit secrets
  scanner (gitleaks, detect-secrets) or formatter runs before the commit
  exists. An agent never bypasses them (`--no-verify`); a host that supports
  tool hooks can block the bypass flags mechanically. Hooks are local and
  skippable, so they complement remote rules rather than replace them.
- **Signed commits.** If a ruleset requires signed commits, an agent without a
  signing key cannot satisfy it: commits are rejected at push. Record the
  requirement in the profile so the session knows to hand the commit over
  instead of failing at push time.

One-time setup per repo; the UI is clearer than `gh api` for a one-off.

## Cleanup recipes

- **Stale branches**: `git branch --merged main` lists branches whose commits
  are ancestors of main — safe to delete. **Squash-merged branches never show
  up there** (the squash creates a new commit; the branch's own commits are not
  ancestors), so under this skill's default flow `--merged` proves little. The
  checks that actually answer "is this branch's work in main": the containment
  test from `stacked-prs.md`, which holds when merging the branch into main
  changes nothing (needs git 2.38 or newer, for `merge-tree --write-tree`):

  ```bash
  [ "$(git merge-tree --write-tree main "$branch" | head -1)" = \
    "$(git rev-parse 'main^{tree}')" ] && echo "contained in main" || echo "NOT contained"
  ```

  or `gh pr list --state merged --head <branch>` (needs network), or
  `git cherry main <branch>` showing only `-` lines (single-commit branches
  only: patch-ids of a squashed multi-commit branch never match). A branch
  failing the containment test gets a look before deletion:
  `git log main..<branch> --oneline` shows what would be lost. A three-dot
  diff (`main...<branch>`) is no check here: it compares against the old fork
  point and is never empty for a branch that has changes.
- **A pile of uncommitted changes of mixed vintage** (a repo left uncommitted for weeks):
  don't guess. Diff-review the changes, group them into thematic commits
  (explicit paths; to split one file's hunks without the interactive
  `git add -p`, write the wanted hunks to a patch and `git apply --cached` it),
  commit each with a message reconstructing
  the why, and only then sync with the remote.
- **Untangling "I did things and now it's weird"**: reflog first
  (`git reflog -15`) — it shows what actually happened, and nearly everything
  is recoverable from it. Diagnose before touching anything.
