# Cluide — The Claude Guide: Project Instructions

## About This Project

This folder contains a complete operational framework for building, running, and improving a persistent AI assistant with Claude. It includes architecture guides, runnable setup and audit tasks, installable skills, and copy-paste templates — covering the full lifecycle from initial setup to scheduled automation, self-improvement, and security. The guides are both human-readable and intended as direct input to Claude.

**When working in this project, apply the guides to your own behavior.** You have access to all of them as context. Use them:

- When asked to help set up or improve a Claude assistant, follow the patterns described in the relevant guide
- When writing or editing `CLAUDE.md` files, skills, tasks, or memory files for the user, apply the structure and principles from the guides
- When something you're doing is covered by a guide, do it the way the guide describes — don't invent a different approach

**Guide map** (read `00_INDEX.md` for full descriptions):

| Guide | Topic |
|---|---|
| `01_CLAUDE_MD.md` | Writing effective CLAUDE.md files |
| `02_PROMPTING_BASICS.md` | Writing instructions that produce consistent output |
| `03_SKILLS.md` | Designing skills |
| `04_MEMORY_AND_PROFILE.md` | Memory and profile files |
| `05_MCP_SERVERS.md` | MCP server setup and usage |
| `06_TASK_EFFICIENCY_GUIDE.md` | Making tasks run efficiently |
| `07_TASK_LEARNING_GUIDE.md` | Tasks that learn and improve over time |
| `08_SELFIMPROVE_TEMPLATE.md` | Self-improving task template (merged into Guide 07 Part 9; stub) |
| `09_MULTI_TASK_ORCHESTRATION.md` | Coordinating multiple tasks with shared state |
| `10_COST_PERFORMANCE.md` | Tracking token usage, budgeting, and cost monitoring |
| `11_GIT_INTEGRATION.md` | Git integration, `.gitignore`, `.claudeignore` |
| `12_SECURITY.md` | Security best practices for Claude Code and Cowork |
| `13_DEV_EXECUTION_WORKFLOW.md` | Development execution workflow |
| `14_PERSONAL_DATA_LAYER.md` | Personal data and profile layer |
| `15_LLM_WIKI.md` | LLM wiki pattern |
| `16_BEST_PRACTICES.md` | General best practices |
| `17_TROUBLESHOOTING.md` | Diagnosing and fixing common problems |
| `18_END_TO_END_WALKTHROUGH.md` | End-to-end walkthrough from zero to running assistant |
| `19_OUTPUT_FORMATTING.md` | Output formatting — Markdown & HTML |
| `20_INTERACTIVE_PROMPTING.md` | Interactive prompting — file references, plan mode, question dialogs, context hygiene |
| `21_COMPANY_POLICIES.md` | Embedding existing company policies as tiered guardrails — without shipping policy content in the repo |
| `22_HELPER_APPS.md` | Collaboration patterns for small locally-run tools you vibe-code for yourself — invariants, helper index, verification gates |
| `23_MULTI_PROJECT_SETUPS.md` | When and how to split work across projects; converging overlaps, single-owner data, cross-project links |
| `24_PROJECT_FOLDER_STRUCTURE.md` | Project folder layout — homes for definitions, state, and outputs; growth hygiene |
| `25_PROJECT_INSTRUCTION_LAYERS.md` | Project description and instructions fields vs. CLAUDE.md — what belongs in which layer, drift control |
| `26_CONTEXT_SCOPING.md` | Context scoping — what a session should see; blind vs. in-context review passes; building one-shot prompts |
| `27_INDEPENDENT_JUDGMENT.md` | Independent judgment — anchoring and agreement pressure, commit-then-reveal, blinded reconciliation, false independence |

When the user asks a question or makes a request that a guide covers, read the relevant guide before responding.

---

## File Hygiene

**Everything that is not part of the distribution goes in `development/`.** The repo root holds only what a reader of the published guide would open: the numbered guides, `00_INDEX.md`, `README.md`, `CHEATSHEET.md`, `CHANGELOG.md`, `CLAUDE.md`, `LICENSE`, and the `skills/`, `tasks/`, `templates/` and `.github/` folders. Review feedback, dated review passes, planning notes, scratch output, editor and tool configs, and the `_to_delete/` staging area all live under `development/`, which is gitignored as a whole — so a new working file needs no new ignore rule, it just needs the right home. Before creating a file at the root, ask whether it ships; if not, create it in `development/` instead. See `development/README.md`.

*Optional paragraph — delete it if you are not developing Cluide itself.* `development/` is gitignored as a whole, so a fresh clone does not contain it and the `development/README.md` reference above will not resolve. Create the folder when you start making changes to Cluide, or remove the paragraph if you cloned this to use the guides rather than to change them. Nothing else in this file depends on it.

When creating new files, check whether they belong in `.gitignore` or `.claudeignore`:
- **Add to `.gitignore`**: run logs, output files, auto-generated bundles, any file containing personal data (paths, names, company names)
- **Add to `.claudeignore`**: large generated files that don't need to be loaded as context (compiled skill bundles, output archives, etc.)

If a newly created file should be ignored but is already tracked by git, run `git rm --cached <file>` to untrack it.

---

## Branching and Releases

Cluide is trunk-based. Work happens on a short-lived branch per change, merged into `main` by PR, branch deleted on merge. `main` is always the current, self-consistent guide set.

**Do not add a `develop` or release branch.** A stabilisation branch solves a problem this repo does not have: one maintainer, no build step, no artefact anyone pins. A fresh clone and the `CoWork Project Maintenance` project both read `main` directly, so a second integration branch would add a merge that catches nothing while leaving the consumed working tree unprotected. Version by content event instead — see *Releases* below.

**When the maintainer asks to merge a branch, run this gate first.** Name each check and its result, and stop at the first failure rather than merging past it.

1. **Whole unit.** The branch is a complete change, not one batch of a larger sweep. A half-applied sweep is a stop however clean the diff looks — `main` is public, and a partial guide set is what a stranger clones. Check the diff against the scope written into the branch's first commit message, not against your recollection of it: this is the one check in the gate where the session grades its own earlier decision, and recollection always finds it complete.
2. **Guide-set coverage.** Run `tasks/review-tasks.md` step 4c and fix everything it names. Do not restate its assertions here or anywhere else; run the check.
3. **Registration completeness** (only when the branch adds or renames a guide). Step 4c proves a guide is scored; it does not prove the guide is registered everywhere. Assert it mechanically: every `.md` citing the previous guide's number must also cite the new one, and every guide and index present both at the repo root and in `skills/ai-assistant-setup/references/` must be byte-identical (`diff -q`) — with `00_INDEX.md` the one permitted variant, whose diff must be confined to the link-stripping described in `tasks/review-tasks.md` step 4a exception 2. Partial registration is this repo's known drift mode.
4. **Consumed surface is append-only.** Dimension numbers, `tasks/` filenames, and guide numbers may be added, never renumbered, and a retired number is never reused. A branch that renumbers is a stop, not a judgement call.
5. **Downstream links** *(maintainer-only — skip this check if you cloned Cluide to use the guides).* Cluide is consumed by a private companion project that runs its own link check against this repo; if that project is mounted, run its `scripts/check-cluide-links.sh`. If it is not mounted, report the check as skipped — never assume it passes.
6. **Squash.** Merge with squash so `main` only ever gains complete units of work.

A cloud session can commit on the device but cannot push, fetch, or open a PR. Finish the gate, then hand the maintainer the `git push -u origin <branch>` and `gh pr create` commands to run in their own terminal.

**Releases are content events, not a calendar.** Never cut a version on a schedule and never propose one. Tag when guides are added, a reading track restructures, or the consumed surface changes: minor for additions and restructures, patch for corrections. Tags are `vMAJOR.MINOR.PATCH`, continuing from `v1.0.0`. A major bump means the append-only rule in check 4 was deliberately broken, which should effectively never happen. At each tag, record what changed in `CHANGELOG.md`, built from `git log <previous tag>..HEAD`; create that file at the first tag if it does not exist.
