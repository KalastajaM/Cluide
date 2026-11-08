# Repo profile template — the canonical shape

Every onboarded repo gets one `## Git` section, in the first of these that
exists: `AGENTS.md` (when the repo keeps shared, cross-assistant policy there),
`CLAUDE.md`, a root `GIT.md`. If the repo already has a section covering its
flow under another heading (e.g. "Branching and Releases"), that section is the
profile: add the missing fields there instead of creating a second one.

Use exactly these fields, in this order. One shape everywhere — a profile
written last month must parse the same as one written today. A field missing
from an older profile means its conservative default (shown in brackets).

## Fields

- **Remote** — URL, or `local-only`. If a remote: **visibility** (`private` /
  `public`) with the date verified. Unknown visibility is treated as public
  until verified.
- **Trunk** — the branch work lands on, and the mode: `branch-per-change`
  (short-lived branches, squash-merge) or `trunk-commits` (direct commits;
  justified for solo local-only bookkeeping repos).
- **Stable/release line** — if one exists (e.g. `main` fast-forwarded + tagged
  at bless moments), how it advances. Omit if the trunk is the only line.
- **Gates** — anything that must pass before a merge (checks, scripts, review
  steps), as pointers to where they're defined, not restatements. Include
  what GitHub enforces: branch protection or rulesets on the trunk/stable line
  and tags, secret scanning push protection, required signed commits.
  [none known: verify before relying on any]
- **Authority** — standing approvals for actions that leave the machine, each
  naming one exact action shape: e.g. `auto-push: session-authored
  fast-forwards to non-trunk branches of this private remote`, or `push, open
  PR and merge after the gate passes`. Anything not named here is proposed
  first. [none: every push, PR and merge is proposed]
- **Changelog** — `per-change` (each PR adds its entry), `at-tag` (written at
  release from `git log <prev>..HEAD`; PRs never touch it), or `none`.
  [ask before adding the first entry]
- **Special rules** — pointers to repo-native procedures (a close procedure, a
  data/code commit split, vendoring consumers, single-writer constraints).
- **Identity** — the commit author to use when the environment has none
  configured, and any identity that must *not* be used here (e.g. a work
  address in a personal public repo). [repo or global git config; agent
  identity as the last resort, said so in the commit proposal]
- **Environment notes** — anything about where this repo is worked on (e.g.
  "Cowork device mount: mode-only diffs are phantom; unlock procedure applies;
  quarantine folder is `development/_to_delete/`").

## Filled example

```markdown
## Git
<!-- git-guru profile, added YYYY-MM-DD -->

- Remote: `github.com/example/app` — **private** (verified YYYY-MM-DD).
- **`development` is the working trunk**: branch-per-change (`feature/…`,
  `fix/…`, `chore/…`), squash-merged.
- **`main` is the stable line**: fast-forwarded from development and tagged
  when a state is blessed. Never commit to main directly.
- Gates: test suite green before merge (`npm test`); see CONTRIBUTING.md.
  Ruleset on `main` and `development`: PRs required, no force-push; tag
  ruleset protects `v*`. Push protection on (verified YYYY-MM-DD).
- Authority: auto-push of session-authored fast-forwards to `feature/…`,
  `fix/…` and `chore/…` branches. PRs and merges are proposed.
- Changelog: at-tag, from `git log <prev-tag>..HEAD`; PRs never edit it.
- Special rules: data exports and code in separate commits (see
  `docs/close-procedure.md`).
- Environment: worked on via Cowork device mounts — mode-only diffs are
  phantom (mount strips exec bits); lock-file unlock procedure applies.
```

A profile is updated in the same session (same commit where possible) as any
change to the repo's flow — a stale profile is worse than none, because the
skill trusts it.
