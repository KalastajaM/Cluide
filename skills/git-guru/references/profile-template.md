# Repo profile template — the canonical shape

Every onboarded repo gets a `## Git` section (in its CLAUDE.md, or root
`GIT.md` when no CLAUDE.md exists; CLAUDE.md wins if both exist) with exactly
these fields, in this order. One shape everywhere — a profile the skill wrote
last month must parse the same as one written today.

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
  steps), as pointers to where they're defined, not restatements.
- **Special rules** — pointers to repo-native procedures (a close procedure, a
  data/code commit split, vendoring consumers, single-writer constraints).
- **Identity** — the commit author to use when the environment has none
  configured (optional; agent identity is the last resort).
- **Environment notes** — anything about where this repo is worked on (e.g.
  "Cowork device mount: mode-only diffs are phantom; unlock procedure applies").

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
- Special rules: data exports and code in separate commits (see
  `docs/close-procedure.md`).
- Environment: worked on via Cowork device mounts — mode-only diffs are
  phantom (mount strips exec bits); lock-file unlock procedure applies.
```

A profile is updated in the same session (same commit where possible) as any
change to the repo's flow — a stale profile is worse than none, because the
skill trusts it.
