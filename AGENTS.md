# Cluide — Shared Project Instructions

## About This Project

Cluide is being extended from a Claude guide into a guide for Claude and ChatGPT, including Codex for repository work. This folder contains an operational framework for building, running, and improving a persistent AI assistant. It includes architecture guides, runnable setup and audit tasks, installable skills, and copy-paste templates — covering the full lifecycle from initial setup to scheduled automation, self-improvement, and security. The guides are human-readable and can be supplied to either assistant. The existing distribution is still Claude-focused; do not claim its tasks, skills, or templates are portable until reviewed.

**When working in this project, apply the guides to your own behavior.** You have access to all of them as context. Use them:

- When asked to help set up or improve an assistant, follow the patterns described in the relevant guide
- When writing or editing project instruction files, skills, tasks, or memory files for the user, apply the structure and principles from the guides
- Apply the relevant guide's principles, but verify platform-specific commands, paths, tools, permissions, and feature availability against the actual runtime and current official documentation. Do not execute Claude-only instructions as if they were OpenAI instructions.

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
| `09_MULTI_TASK_ORCHESTRATION.md` | Coordinating multiple tasks with shared state; model-aware dispatch |
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
| `24_PROJECT_FOLDER_STRUCTURE.md` | Project folder layout — homes for definitions, state, and outputs; the `incoming/` intake queue; growth hygiene |
| `25_PROJECT_INSTRUCTION_LAYERS.md` | Project description and instructions fields vs. CLAUDE.md — what belongs in which layer, drift control |
| `26_CONTEXT_SCOPING.md` | Context scoping — what a session should see; blind vs. in-context review passes; building one-shot prompts |
| `27_INDEPENDENT_JUDGMENT.md` | Independent judgment — anchoring and agreement pressure, commit-then-reveal, blinded reconciliation, false independence |
| `28_SECOND_BRAIN.md` | Personal knowledge layer — capture and inbox discipline, the four homes, distillation, index-first retrieval, weekly review |
| `29_SPEC_BEFORE_REBUILD.md` | Specifying a grown artefact before rebuilding it — compensating-machinery triggers, normative specs with divergence markers, the old version as acceptance oracle, prevention over detection |
| `30_CONTROLLED_DOCUMENTS.md` | Documents with owners and approvals — tracked-change review with comments, no silent edits, acceptance as a human act, filename/state separation, one authored register with generated views, tracker merge safety |
| `31_BEHAVIOUR_TESTS.md` | Behaviour tests — cases as prompt plus checkable graders, negative trigger neighbours, fixtures not live data, three runners, when to run the suite, sorting a failure into model / accretion / marginal / platform |
| `32_ACTION_AUTHORITY.md` | Action authority — four classes by consequence, standing approvals with scope and expiry, the proposal contract, outbox and action log for unattended runs, structural enforcement before prose |
| `33_RETIRING_AND_LEAVING.md` | Retiring and leaving — the inventory of everything still pointing at a project, ownership transfer before archive, the freeze, registrations deleted not disabled, the account / folder / machine layer table for a departure |
| `34_IMPORTING_FROM_OTHER_ASSISTANTS.md` | Importing from other assistants — the self-export prompt (ask the assistant, not the product), the category-to-home routing table, the export as data, additive and never destructive, the import as the audit, confirm before writing; no vendor steps by rule |
| `35_DUAL_PLATFORM_PROJECTS.md` | Dual-platform projects — one shared policy with thin native adapters, four homes for rules and state, capability gaps as verified / none / untested, one scheduler owner per job, a fresh-session check per surface, product facts in one dated table |

When the user asks a question or makes a request that a guide covers, read the relevant guide before responding.

---

## File Hygiene

**Everything that is not part of the distribution goes in `development/`.** The repo root holds only what a reader of the published guide would open: the numbered guides, `00_INDEX.md`, `README.md`, `CHEATSHEET.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, `PLATFORM_SETUP.md`, `LICENSE`, and the `skills/`, `tasks/`, `templates/` and `.github/` folders. Review feedback, dated review passes, planning notes, scratch output, editor and tool configs, and the `_to_delete/` staging area all live under `development/`, which is gitignored as a whole — so a new working file needs no new ignore rule, it just needs the right home. Before creating a file at the root, ask whether it ships; if not, create it in `development/` instead. See `development/README.md`.

*Optional paragraph — delete it if you are not developing Cluide itself.* `development/` is gitignored as a whole, so a fresh clone does not contain it and the `development/README.md` reference above will not resolve. Create the folder when you start making changes to Cluide, or remove the paragraph if you cloned this to use the guides rather than to change them. Nothing else in this file depends on it.

When creating new files, check whether they belong in `.gitignore` or `.claudeignore`:
- **Add to `.gitignore`**: run logs, output files, auto-generated bundles, any file containing personal data (paths, names, company names)
- **Add to `.claudeignore`**: large generated files that don't need to be loaded as context (compiled skill bundles, output archives, etc.)

If a newly created file should be ignored but is already tracked by git, run `git rm --cached <file>` to untrack it.

---

## Platform and Dispatch Boundaries

- This file is the canonical repository policy. `CLAUDE.md` imports it for Claude Code. See `PLATFORM_SETUP.md` for ChatGPT and other conversational surfaces.
- Repository examples under `templates/` and `skills/` are distribution content, not instructions to install or run a personal assistant while maintaining this repository.
- Use only tools, models, skills, and permissions actually available in the current session. Never translate Claude model names into guessed OpenAI equivalents.
- For Claude delegation, consult `skills/dispatch/SKILL.md`: default sonnet, opus or above for published prose and review verdicts, haiku only for mechanical checks. For OpenAI delegation, retain the configured model unless the user requests a supported alternative. Follow the host's delegation rules.
- Keep working notes and routing logs under `development/`. Read root guides on demand; bundled references are distribution copies and should only be read for bundle checks.
- `.claudeignore` is not an OpenAI configuration file or a security boundary. Respect actual sandbox and connector permissions; do not infer access restrictions from ignore files.
- Share versioned definitions; keep credentials, app settings, native memory, scheduler registrations, and session history platform-local. Coordinate edits through branches or worktrees rather than concurrent writes to the same checkout.

---

## Branching and Releases

Cluide is trunk-based. Work happens on a short-lived branch per change, merged into `main` by PR, branch deleted on merge. `main` is always the current, self-consistent guide set.

**Do not add a `develop` or release branch.** A stabilisation branch solves a problem this repo does not have: one maintainer, no build step, no artefact anyone pins. A fresh clone and the private companion project both read `main` directly, so a second integration branch would add a merge that catches nothing while leaving the consumed working tree unprotected. Version by content event instead — see *Releases* below.

**When the maintainer asks to merge a branch, run this gate first.** Name each check and its result, and stop at the first failure rather than merging past it.

1. **Whole unit.** The branch is a complete change, not one batch of a larger sweep. A half-applied sweep is a stop however clean the diff looks — `main` is public, and a partial guide set is what a stranger clones. Check the diff against the scope written into the branch's first commit message, not against your recollection of it: this is the one check in the gate where the session grades its own earlier decision, and recollection always finds it complete.
2. **Guide-set coverage.** Run `tasks/review-tasks.md` step 4c and fix everything it names. Do not restate its assertions here or anywhere else; run the check.
3. **Bundled copies and registration.** Whenever the branch touches a root guide or index, run `tasks/review-tasks.md` step 4a: every copy under *any* `skills/*/references/` — not only `ai-assistant-setup` — must be byte-identical to its root counterpart, with `skills/ai-assistant-setup/references/00_INDEX.md` the one permitted variant, whose diff must be confined to the link-stripping that step describes. Do not restate the loop here; run it. When the branch adds or renames a guide, also assert registration completeness: step 4c proves a guide is scored, not that it is registered everywhere, so every `.md` citing the previous guide's number must also cite the new one. Stale bundled copies and partial registration are this repo's two known drift modes — two consecutive merges left copies outside `ai-assistant-setup` behind while this check named only that skill.
4. **Consumed surface is append-only.** Dimension numbers, `tasks/` filenames, and guide numbers may be added, never renumbered, and a retired number is never reused. A branch that renumbers is a stop, not a judgement call.
5. **Downstream links** *(maintainer-only — skip this check if you cloned Cluide to use the guides).* Cluide is consumed by a private companion project that runs its own link check against this repo; if that project is mounted, run its `scripts/check-cluide-links.sh`. If it is not mounted, report the check as skipped — never assume it passes.
6. **Squash.** Merge with squash so `main` only ever gains complete units of work.

Check the current session’s GitHub connectivity and authorization. When authorized and available, push, open the PR, and merge after the gate passes. If a runtime cannot access GitHub, report the actual blocker and provide the remaining commands; do not assume that every cloud or desktop session has the same limitations.

**Releases are content events, not a calendar.** Never cut a version on a schedule and never propose one. Tag when guides are added, a reading track restructures, or the consumed surface changes: minor for additions and restructures, patch for corrections. Tags are `vMAJOR.MINOR.PATCH`, continuing from `v1.0.0`. A major bump means the append-only rule in check 4 was deliberately broken, which should effectively never happen. At each tag, record what changed in `CHANGELOG.md`, built from `git log <previous tag>..HEAD`; create that file at the first tag if it does not exist. Nothing accumulates there between tags: a pull request never edits `CHANGELOG.md`, and there is no `## [Unreleased]` section to write under. That puts the whole weight of the changelog on commit subjects, which is why check 1 above grades the diff against the scope written into the branch's first commit message — an unscoped subject is a changelog entry nobody can write later.

## App-side Fields

See `PLATFORM_SETUP.md` for proposed bootstrap text. These are setup instructions, not a claim that any app-side setting has been changed or verified. Existing Claude app fields were last reported by the maintainer on 2026-08-07: a Claude-only description and empty instructions. Re-verify before treating those fields as current; record each platform separately when actually configured.
