# git-guru

Full-lifecycle git and GitHub management for AI assistants. The skill diagnoses
a repository's live state, acts where the session safely can (branch, commit,
sync checks, cleanup), and hands over exact, self-checking commands where it
can't (credentials, network, protected branches, delete-refusing mounts).

Version 2.0.0 · MIT licence · source: Cluide, `skills/git-guru/`.

## Contents

| Path | Loaded | Purpose |
|---|---|---|
| `SKILL.md` | on trigger | The loop, safety rails, agent command hygiene, handover format. Self-sufficient: the rules marked (core) hold even if nothing else was installed. |
| `references/practices.md` | on demand | Flow judgment: branching, commits, sync, undo, releases, changelog models, enforcement (rulesets, push protection, hooks), cleanup. |
| `references/cowork-git-mechanics.md` | on demand | Working on a mounted folder that refuses deletes: locks, branch creation and file restore without unlink, tree repair, syncing from a networked clone. |
| `references/stacked-prs.md` | on demand | Building and landing a stack of dependent PRs without redundant CI. |
| `references/profile-template.md` | on demand | The per-repo `## Git` profile the skill writes and reads. |
| `scripts/scan-staged.sh` | run | Secrets and personal-data scan of staged added lines; never prints the matched value. Exit 0 clean, 1 findings, 2 could not scan. |
| `scripts/verify-tag.sh` | run | Fail-closed check that a remote tag peels to the remote trunk tip. |
| `scripts/land-stack.sh` | run | Restartable squash-merge of a PR stack (needs git ≥ 2.40, `gh`, `jq`). |

Scripts are bash, need only git (plus `gh`/`jq` for
`land-stack.sh`), and run from any working directory inside the target repo.

## Install

Install the **whole folder**. An install that keeps only `SKILL.md` still runs
safely, but loses the references and scripts; check after installing that
`references/` and `scripts/` are present.

| Surface | Route |
|---|---|
| Claude (claude.ai / desktop account skills) | Upload `git-guru.zip` (this folder, zipped) as a skill. Do not paste `SKILL.md` into an editor: that keeps the one file only. |
| Claude Code | Copy the folder to `~/.claude/skills/git-guru/` (personal) or `.claude/skills/git-guru/` (project). |
| Codex | Copy the folder to `~/.agents/skills/git-guru/` or the repository's `.agents/skills/git-guru/`. |
| Antigravity (documented, untested) | Workspace `.agents/skills/git-guru/`. |
| Gemini app (documented, untested) | Upload the `.zip` on the Skills page. An upload is a copy: re-upload after each update. |
| Hosts without skill install | Supply `SKILL.md` as a source and invoke it explicitly. |

After installing, test three cases: a git request that should trigger it
("is this repo synced?"), a neighbouring request that should not ("explain what
a hash function is"), and a session without network, where it should hand over
commands rather than claim a push.

## Recommended per-repo setup

The skill reads a `## Git` profile from the repo's `AGENTS.md`, `CLAUDE.md` or
`GIT.md` and offers to write one on first use. Pushes, PRs and merges are
proposed, not performed, unless that profile's **Authority** field grants a
standing approval for the exact action. Pair it with server-side enforcement:
branch protection or rulesets on the trunk, and secret scanning push protection.
