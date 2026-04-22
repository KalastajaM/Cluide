# Cluide — The Claude Guide

*Last reviewed: April 2026*

> A complete framework for building, running, and improving a persistent AI assistant with Claude.
> Includes architecture guides, runnable setup tasks, installable skills, and copy-paste templates.

*Written for Claude Code with Claude Haiku, Sonnet, and Opus models (2026). Core concepts apply to any Claude setup.*

---

## What This Is

Cluide is an operational framework for building AI assistants that persist, learn, and improve over time — not a collection of tips, but a complete system you can actually install and run. It covers the full lifecycle: initial setup, scheduled automation, self-improvement, security, and long-term maintenance.

The deliverables are concrete: 18 interlocking guides that define the architecture, 19 runnable task files that do the setup work for you, 4 bundled skills, and 4 ready-to-use templates. The guides are documentation for the system; the tasks are its installation scripts.

A well-configured Claude personal assistant has four layers:

| Layer | What it does | Where it lives |
|-------|-------------|----------------|
| **CLAUDE.md** | Standing rules loaded into every session | `.claude/CLAUDE.md` |
| **Skills** | Instructions for specific recurring tasks | `.claude/skills/[skill-name]/SKILL.md` |
| **Memory** | Facts Claude learns across sessions | `.auto-memory/` |
| **Scheduled Tasks** | Automated workflows that run on a schedule | Managed by the task scheduler |

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
| 08 | [Self-Improvement Template](./08_SELFIMPROVE_TEMPLATE.md) | Scheduled tasks | Installing the IMPROVEMENTS.md template |
| 09 | [Multi-Task Orchestration](./09_MULTI_TASK_ORCHESTRATION.md) | Power users | Coordinating tasks with shared state and dependencies |
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

**Recommended order:** Quickstart → 01 → 02 → **20** → 03 → 04 → 05 → (06–10 once you have scheduled tasks running). Or follow [Guide 18](./18_END_TO_END_WALKTHROUGH.md) for a guided path through all stages.

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
| `tasks/setup-github.md` | Init git, create GitHub repo, set up ongoing sync |
| `tasks/setup-self-improving-task.md` | Add `IMPROVEMENTS.md` + self-improvement loop to any task |
| `tasks/setup-wiki.md` | Create an LLM wiki structure for a topic |
| `tasks/setup-data-layer.md` | Set up data patterns (Python feeder, JSON DB, browser extraction) |

### Audit tasks

| Task | What it does |
|------|-------------|
| `tasks/audit-claude-md.md` | Review `CLAUDE.md` — dead rules, missing sections, over-length |
| `tasks/audit-task-efficiency.md` | Token efficiency checklist for any task file |
| `tasks/audit-memory.md` | Check memory files for staleness and duplicates |
| `tasks/audit-skill.md` | Review a `SKILL.md` — triggering, workflow, output format |

---

## Skills Included

Five installable skills are bundled in `skills/`. Install only the ones you need.

**Claude Code:** copy the skill folder to `~/.claude/skills/`
**Claude.ai:** upload the `.skill` file from `skills/` via **Settings → Skills → Upload skill**

| Skill | What it does |
|-------|-------------|
| `ai-assistant-setup` | Interactive setup coach — all guides bundled. Describe what you want and Claude does the work. |
| `template-exporter` | Turns any Claude setup into a clean, shareable template |
| `cowork-optimizer` | Audits a Cowork task for token efficiency and structural quality |
| `security-review` | Structured security audit of a Claude Code environment and project |
| `backlog` | Portable backlog manager — prioritised work items, grooming, decision logging |

---

## Templates

Four copy-paste starting points in `templates/`:

| Template | What it is |
|----------|-----------|
| `PROJECT_TEMPLATE/` | Project folder with `CLAUDE.md`, `Profile/`, and `Knowledge/` pre-structured |
| `TASK_TEMPLATE/` | Scheduled task folder with `TASK.md`, `IMPROVEMENTS.md`, `RUN_LOG.md` |
| `AI-ASSISTANT_TEMPLATE/` | Full personal business assistant — email, calendar, Teams, daily briefings |
| `PMO_TEMPLATE/` | Programme workspace with risk register, action tracker, and decision log |

---

## Repository Structure

```
/
├── 00_INDEX.md               # Full annotated guide index
├── 00_QUICKSTART.md          # Start here if you're new
├── 01_CLAUDE_MD.md – 18_END_TO_END_WALKTHROUGH.md
├── CHEATSHEET.md             # One-page quick reference
├── tasks/                    # Setup and audit task files
├── skills/                   # Bundled installable skills
└── templates/                # Copy-paste project starters
```
