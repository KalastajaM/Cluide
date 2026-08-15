# Cluide — The Claude Guide

*Guides last reviewed: August 2026 — the guides are maintained and reviewed as a set, so individual guides no longer carry their own "last reviewed" dates. This line is the single source of truth.*

> A complete framework for building, running, and improving a persistent Claude assistant.
> Includes architecture guides, runnable setup tasks, installable skills, and copy-paste templates.

*Written for Claude Code and Cowork with current Claude models (Haiku, Sonnet, Opus, Fable); the core concepts are model-agnostic.*

---

## What This Is

Cluide is an operational framework for building Claude assistants that persist, learn, and improve over time — not a collection of tips, but a complete system you can actually install and run. It covers the full lifecycle: initial setup, scheduled automation, self-improvement, security, and long-term maintenance.

The deliverables are concrete: a set of interlocking guides that define the architecture, a library of runnable task files that do the setup work for you, a set of installable skills, and the ready-to-use templates in `templates/`. The guides are documentation for the system; the tasks are its installation scripts.

A well-configured Claude personal assistant has four layers:

| Layer | What it does | Where it lives |
|-------|-------------|----------------|
| **CLAUDE.md** | Standing rules loaded into every session | `.claude/CLAUDE.md` |
| **Skills** | Instructions for specific recurring tasks | `.claude/skills/[skill-name]/SKILL.md` |
| **Memory** | Facts Claude learns across sessions | `.auto-memory/` |
| **Scheduled Tasks** | Automated workflows that run on a schedule | Managed by the task scheduler |

---

## How This Was Built

Cluide is AI-assisted work — openly and deliberately. The patterns, lessons, and opinions in these guides come from real hands-on use, but Claude did the building: it turned those learnings into the guides, tasks, skills, and templates that make up this repository, and it maintains and reviews them as a set. The project practices what it teaches — it was built, and is kept current, using the same workflow it documents.

---

## Three Ways to Use This

1. **Read the guides yourself** and set things up manually — useful if you want full control.
2. **Give a guide to Claude** — `"Read 01_CLAUDE_MD.md and help me write my CLAUDE.md."` Claude reads the guide and builds the component it describes.
3. **Run a task** — faster, guided, no reading required. Say `"Run tasks/onboard-project.md"` to start a full interactive setup.

---

## Getting Started

**New here?** Start with [00_QUICKSTART.md](./00_QUICKSTART.md) — build a working CLAUDE.md and your first skill in 20 minutes.

**Prefer guided setup?** Install the `ai-assistant-setup` skill (see [Skills](#skills-included) below), then say:
> "Help me set up Claude as a personal assistant from scratch."

**Quick reference while building:** Keep [CHEATSHEET.md](./CHEATSHEET.md) open for file skeletons and common patterns.

---

## Guides

| # | Guide | Audience | Topic |
|---|-------|----------|-------|
| — | [Quickstart](./00_QUICKSTART.md) | New users | Build a working setup in 20 minutes |
| 01 | [CLAUDE.md](./01_CLAUDE_MD.md) | All | Writing effective always-loaded instructions |
| 02 | [Prompting Basics](./02_PROMPTING_BASICS.md) | All | Writing instructions that produce consistent output |
| 03 | [Skills](./03_SKILLS.md) | All | Designing skills for recurring tasks |
| 04 | [Memory & Profile](./04_MEMORY_AND_PROFILE.md) | All | Persistence across sessions |
| 05 | [MCP Servers](./05_MCP_SERVERS.md) | All | Connecting Claude to Gmail, Calendar, GitHub, etc. |
| 06 | [Task Efficiency](./06_TASK_EFFICIENCY_GUIDE.md) | Scheduled tasks | Minimizing token use in automated tasks |
| 07 | [Task Self-Improvement](./07_TASK_LEARNING_GUIDE.md) | Scheduled tasks | Tasks that learn and improve over time |
| 08 | [Self-Improvement Template](./08_SELFIMPROVE_TEMPLATE.md) | Scheduled tasks | Merged into Guide 07 (Part 9) — kept as a pointer stub |
| 09 | [Multi-Task Orchestration](./09_MULTI_TASK_ORCHESTRATION.md) | Power users | Coordinating tasks with shared state and dependencies; routing delegated work across model tiers |
| 10 | [Cost & Performance](./10_COST_PERFORMANCE.md) | Scheduled tasks | Tracking costs and finding expensive operations |
| 11 | [Git Integration](./11_GIT_INTEGRATION.md) | Power users | Version control for your assistant's state |
| 12 | [Security](./12_SECURITY.md) | All | Credential hygiene, MCP trust, safe automation |
| 13 | [Dev & Execution Workflow](./13_DEV_EXECUTION_WORKFLOW.md) | Power users | Claude Code vs. Cowork — build vs. run |
| 14 | [Personal Data Layer](./14_PERSONAL_DATA_LAYER.md) | Power users | Getting personal data into Claude's hands |
| 15 | [LLM Wiki](./15_LLM_WIKI.md) | Power users | Building a compounding knowledge base |
| 16 | [Best Practices](./16_BEST_PRACTICES.md) | All | Lessons from real use |
| 17 | [Troubleshooting](./17_TROUBLESHOOTING.md) | All | When things don't work |
| 18 | [End-to-End Walkthrough](./18_END_TO_END_WALKTHROUGH.md) | All | From zero to running assistant — the full journey |
| 19 | [Output Formatting](./19_OUTPUT_FORMATTING.md) | All | Markdown & HTML output patterns |
| 20 | [Interactive Prompting](./20_INTERACTIVE_PROMPTING.md) | All | File references, plan mode, question dialogs, context hygiene |
| 21 | [Company Policies](./21_COMPANY_POLICIES.md) | Power users | Embedding company policies as tiered guardrails without shipping policy content in the repo |
| 22 | [Personal Helper Apps](./22_HELPER_APPS.md) | Power users | Collaboration patterns for small locally-run tools you vibe-code for yourself — invariants, helper index, verification gates |
| 23 | [Multi-Project Setups](./23_MULTI_PROJECT_SETUPS.md) | Power users | Keeping several linked projects consistent: when and how to split, handling overlap, single-owner data, and changing one without breaking the others |
| 24 | [Project Folder Structure](./24_PROJECT_FOLDER_STRUCTURE.md) | Power users | Standard single-project folder layout and how to keep it clean as it grows; the `incoming/` intake queue for material arriving outside chat; standard formats for recurring files; safely reorganizing a project without breaking it |
| 25 | [Project Instruction Layers](./25_PROJECT_INSTRUCTION_LAYERS.md) | Power users | What belongs in a project's app-side description and instructions fields vs. CLAUDE.md, and how to keep the app-side fields from drifting unseen |
| 26 | [Context Scoping and Prompt Construction](./26_CONTEXT_SCOPING.md) | Power users | Deciding what a session should and should not see; blind vs. in-context review passes; designing a one-shot prompt in one session and running it clean in another |
| 27 | [Independent Judgment](./27_INDEPENDENT_JUDGMENT.md) | All users | Getting a judgment Claude reached on its own: anchoring and agreement pressure, commit-then-reveal, blinded reconciliation, and why two Claude runs agreeing is not corroboration |
| 28 | [Second Brain](./28_SECOND_BRAIN.md) | Power users | A personal knowledge layer Claude can read: the test for whether it is worth building, the four homes, inbox discipline, distilling for a conclusion rather than a summary, and the weekly review |

**Recommended order:** Quickstart → 01 → 02 → **20** → 03 → 04 → 05 → (06–10 once you have scheduled tasks running). The guide numbers are stable addresses, not a reading order — see the [Reading Tracks in 00_INDEX.md](./00_INDEX.md#reading-tracks) for per-goal paths, or follow [Guide 18](./18_END_TO_END_WALKTHROUGH.md) for a guided path through all stages.

For detailed per-guide descriptions, reading times, and usage guidance, see [00_INDEX.md](./00_INDEX.md).

---

## Tasks

Tasks are standalone instruction files for setup and auditing. Run them by saying `"Run tasks/[task-name].md"`. Copy any task file to another project's `tasks/` directory to use it there.

### Setup tasks

| Task | What it does |
|------|-------------|
| `tasks/onboard-project.md` | Full end-to-end setup — orchestrates all tasks below in order |
| `tasks/setup-claude-md.md` | Interview → generate `CLAUDE.md` |
| `tasks/setup-skill.md` | Interview → scaffold a new `SKILL.md` |
| `tasks/setup-scheduled-task.md` | Scaffold a new scheduled task with efficiency + self-improvement |
| `tasks/setup-memory.md` | Create `.auto-memory/` with initial memory files |
| `tasks/setup-mcp.md` | Audit and add MCP server connections |
| `tasks/setup-security.md` | Credential scan, permission audit, install guard hooks |
| `tasks/setup-policies.md` | Wire company policies into the `policies-validator` skill + `CLAUDE.md` with tiered enforcement (T1 block / T2 alert / T3 guidance) |
| `tasks/setup-github.md` | Init git, create GitHub repo, set up ongoing sync |
| `tasks/setup-self-improving-task.md` | Add `IMPROVEMENTS.md` + self-improvement loop to any task |
| `tasks/setup-orchestration.md` | Wire multi-task coordination — shared state, run order, handoff files |
| `tasks/setup-wiki.md` | Create an LLM wiki structure for a topic |
| `tasks/setup-second-brain.md` | Build or repair a personal knowledge layer — four homes, index, inbox rule, review pass |
| `tasks/setup-data-layer.md` | Set up data patterns (Python feeder, JSON DB, browser extraction) |
| `tasks/setup-ignore-hygiene.md` | Audit `.gitignore`/`.claudeignore`, install check hook |
| `tasks/setup-bootstrap-folder.md` | Create `bootstrap/` stubs for gitignored runtime state files |
| `tasks/tune-instruction-layers.md` | Review all three instruction layers — the app-side description and instructions fields plus `CLAUDE.md` |

### Audit & maintenance tasks

| Task | What it does |
|------|-------------|
| `tasks/audit-claude-md.md` | Review `CLAUDE.md` — dead rules, missing sections, over-length |
| `tasks/audit-task-efficiency.md` | Token efficiency checklist for any task file |
| `tasks/audit-cost.md` | Audit a task's token economics — file budgets, model tier, run metrics |
| `tasks/audit-memory.md` | Check memory for staleness and duplicates across all three layers (native, `.auto-memory/`, profile files) |
| `tasks/audit-skill.md` | Review a `SKILL.md` — triggering, workflow, output format, `allowed-tools` enforcement |
| `tasks/audit-file-hygiene.md` | Sweep clutter — OS junk, lock/temp files, duplicate families, and trees that are gitignored but still loading as context |
| `tasks/analyze-project.md` | Analyze *another* Claude project (local or GitHub) against the full guide set → write a `CLUIDE_IMPROVEMENT_PLAN.md` into it (read-only, plan-only) |
| `tasks/reorganize-project.md` | Safely restructure a project's folders — move files and rewire every reference without breaking it; takes a restore point first |
| `tasks/relocate-project.md` | Move a project (or a whole projects root) elsewhere — sweeps the project, scheduled-task, and app-config layers |
| `tasks/review-tasks.md` | Cluide maintenance — detect guide changes and flag tasks, skill bundles, and templates that drifted |
| `tasks/harvest-from-projects.md` | Cluide maintenance — the inverse of `review-tasks.md`: harvest proven patterns from your live projects back into the guides, tasks, templates, and skills |

---

## Skills Included

The installable skills bundled in `skills/` are listed below. Install only the ones you need.

**Claude Code:** copy the skill folder to `~/.claude/skills/`
**Claude.ai:** zip the skill folder (e.g. `cd skills && zip -r dispatch.zip dispatch/` — or ask Claude to bundle it), then upload the `.zip` via **Settings → Skills → Upload skill**

| Skill | What it does |
|-------|-------------|
| `ai-assistant-setup` | Interactive setup coach — all guides bundled. Describe what you want and Claude does the work. |
| `template-exporter` | Turns any Claude setup into a clean, shareable template |
| `cowork-optimizer` | Audits a Cowork task for token efficiency and structural quality |
| `review-protocol` | Structured review that stays independent of your own view — commit-then-reveal, finding schema, blinded reconciliation |
| `security-review` | Structured security audit of a Claude Code environment and project |
| `policies-validator` | Tiered company-policy guardrail (T1 block / T2 alert / T3 soft guidance) — ships as a template; fill the Policy Registry before use |
| `git-guru` | Full-lifecycle git and GitHub management — diagnoses the repo's real state, acts where it safely can, hands over validated commands where it can't (Guide 11 companion) |
| `dispatch` | Routes delegated work — subagents, workflow stages, scheduled tasks — to the right model tier and effort, with an escalation ladder and per-project overrides (Guide 09 §Model-Aware Dispatch) |

---

## Templates

The copy-paste starting points in `templates/`:

| Template | What it is |
|----------|-----------|
| `PROJECT_TEMPLATE/` | The default project layout: `CLAUDE.md` with a file map and an app-side mirror block, `Outputs/`, `Working/`, `_archive/`, plus the memory, intake, and routing blocks ready to keep or delete |
| `TASK_TEMPLATE/` | Scheduled task folder with `TASK.md`, `IMPROVEMENTS.md`, `RUN_LOG.md` |
| `AI-ASSISTANT_TEMPLATE/` | Full personal business assistant — email, calendar, Teams, daily briefings |
| `PMO_TEMPLATE/` | Programme workspace with risk register, action tracker, and decision log |
| `ACCOUNT_INSTRUCTIONS_TEMPLATE.md` | The two account-level instruction fields (preferences + Cowork-wide), ready to fill and paste |
| `AGENT_STARTER_PACK/` | Four model-pinned Claude Code subagents (scout, builder, verifier, researcher) — the structural binding for the `dispatch` skill |
| `BLOCKS.md` | Catalogue of the optional blocks a project adds to that core, and the task that installs each |

---

## Repository Structure

```
/
├── 00_INDEX.md               # Full annotated guide index
├── 00_QUICKSTART.md          # Start here if you're new
├── 01_CLAUDE_MD.md – 28_SECOND_BRAIN.md
├── CHEATSHEET.md             # One-page quick reference
├── tasks/                    # Setup and audit task files
├── skills/                   # Bundled installable skills
└── templates/                # Copy-paste project starters
```
