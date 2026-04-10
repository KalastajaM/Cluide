# Personal Claude Setup — Guide Index

> A collection of best-practice guides for building a personal AI assistant with Claude.
> Based on real-world experience. Each guide is standalone but they form a coherent system together.

*Written for Claude Code with Claude Sonnet/Opus models (2025–2026). Core concepts apply to any Claude setup; tool names and hooks syntax may differ across versions.*

---

## What This Is

These guides capture what actually works when setting up Claude as a persistent personal assistant — not theoretical advice, but patterns refined through real use. The goal is to give you both the knowledge to understand the system and the concrete instructions to hand to Claude so it can set things up for you.

**Two ways to use these guides:**

1. **Read them yourself** and set things up manually — useful if you want full control.
2. **Give them to Claude as input** and ask it to create or improve a specific part of your setup. Claude can read a guide and then build the component it describes (write your CLAUDE.md, create a skill, set up a task file, etc.).

---

## The System at a Glance

A well-configured Claude personal assistant has four layers:

| Layer | What it does | Where it lives |
|-------|-------------|----------------|
| **CLAUDE.md** | Standing rules loaded into every session — who you are, how you want Claude to respond | `.claude/CLAUDE.md` |
| **Skills** | Instructions for specific recurring tasks — triggered when you ask for them | `.claude/skills/[skill-name]/SKILL.md` |
| **Memory** | Facts Claude learns across sessions — preferences, corrections, project state | `.auto-memory/` |
| **Scheduled Tasks** | Automated workflows that run on a schedule without you asking | Managed by the task scheduler |

Each layer has its own guide below.

---

## What Should I Build?

Not sure where to start? Use this table:

| You want to... | Build | Guide |
|---|---|---|
| Claude always responds a certain way | CLAUDE.md | [01](./01_CLAUDE_MD.md) |
| Do the same task when you ask for it | Skill | [02](./02_SKILLS.md) |
| Run something automatically on a schedule | Scheduled Task | [04](./04_TASK_EFFICIENCY_GUIDE.md) |
| Claude remembers things across sessions | Memory | [03](./03_MEMORY_AND_PROFILE.md) |
| A task that gets smarter over time | Task + IMPROVEMENTS.md | [05](./05_TASK_LEARNING_GUIDE.md) |
| Answer a one-off question | Chat | — |

---

## The Guides

### [Quickstart — Your First Setup](./00_QUICKSTART.md)
`[New user]` · `~20 min`

A hands-on walkthrough: build a working CLAUDE.md and your first skill in 20 minutes. No other guides required first. Includes exact file contents to copy, how to test in Cowork, and what to build next.

**Use this when:** you're new and want something working before you read anything else.

---

### [01 — CLAUDE.md](./01_CLAUDE_MD.md)
`[All users]` · `~10 min`

*The foundation: what goes in your always-loaded instruction file.*

Covers: what to put in CLAUDE.md, how to structure it, what not to include, and how to keep it lean and effective. Includes a real-world example.

**Use this when:** you're setting up Claude for the first time, or the assistant keeps behaving in ways you have to correct session after session.

---

### [02 — Skills](./02_SKILLS.md)
`[All users]` · `~15 min`

*How to design skills for recurring tasks.*

Covers: the anatomy of a SKILL.md file, writing descriptions that trigger reliably, structuring workflow steps, output formats, and edge cases. Includes real examples from a working setup.

**Use this when:** there's a task you do repeatedly (checking email for actions, drafting messages in a second language, building a shopping list) and you want Claude to handle it consistently every time.

---

### [03 — Memory & Profile](./03_MEMORY_AND_PROFILE.md)
`[All users]` · `~15 min`

*Three persistence layers: native memory, auto-memory, and profile files.*

Covers: native Claude memory (built-in, zero setup) vs. the `.auto-memory/` folder system (structured, project-specific), profile files for complex recurring agents, what to store, how to keep files lean, and the hypothesis system.

**Use this when:** you want Claude to remember things across sessions — your preferences, corrections, ongoing projects, and key contacts.

---

### [04 — Task Efficiency](./04_TASK_EFFICIENCY_GUIDE.md)
`[Scheduled tasks]` · `~15 min`

*How to design and optimize scheduled tasks for minimal token consumption.*

Covers: splitting instruction files, scripting fixed-format output, targeted file edits, two-pass triage for external data, hard size limits, run deduplication, and the two scheduling mechanisms (remote/scheduled triggers vs. SessionStart hooks).

**Use this when:** you have a scheduled task running regularly and want to audit it for efficiency — or want to set one up correctly from the start.

---

### [05 — Task Self-Improvement](./05_TASK_LEARNING_GUIDE.md)
`[Scheduled tasks]` · `~20 min`

*A framework for building tasks that get better over time.*

Covers: what to learn and how to store it, detecting feedback signals, the apply-vs-propose decision, the hypothesis lifecycle, the refactoring system, and the improvements log.

**Use this when:** you have a scheduled task up and running and want it to evolve — fixing its own mistakes, codifying patterns, and proposing improvements rather than repeating errors.

---

### [06 — Self-Improvement Template](./06_SELFIMPROVE_TEMPLATE.md)
`[Scheduled tasks]` · `~5 min`

*How to install and use the IMPROVEMENTS.md template.*

Explains the structure of the template, walks through installation (copy → fill in task name → wire into TASK.md), and documents how to respond to proposals. The template itself lives at [`templates/TASK_TEMPLATE/IMPROVEMENTS.md`](./templates/TASK_TEMPLATE/IMPROVEMENTS.md).

**Use this when:** you're creating a new scheduled task and want the self-improvement system set up from run 1.

---

### [07 — Best Practices](./07_BEST_PRACTICES.md)
`[All users]` · `~10 min`

*Lessons from real use — a shareable summary.*

Covers: giving Claude good inputs, working effectively session-to-session, building a setup that compounds over time, and knowing when not to use Claude. Includes a 15-point short version for quick reference.

**Use this when:** you want a quick overview of what actually matters, or you want something to share with someone just getting started.

---

### [08 — MCP Servers](./08_MCP_SERVERS.md)
`[All users]` · `~15 min`

*How Claude connects to external tools — Gmail, Calendar, GitHub, and more.*

Covers: what MCP servers are, global vs. project-level configuration, the most useful servers for personal assistants (including Claude in Chrome and Computer Use), how to reference tool names in skills, and credential security.

**Use this when:** you're setting up a skill that uses external tools (email, calendar, files, browser, desktop) and need to understand where those tools come from — or when a skill isn't finding the tools it needs.

---

### [09 — Git Integration](./09_GIT_INTEGRATION.md)
`[Power user]` · `~20 min`

*Version control for your assistant's state — pre-run snapshots, rollback, and history.*

Covers: what to track in git, what belongs in `.gitignore` vs `.claudeignore`, automating file hygiene through `CLAUDE.md`, the pre-run commit pattern (snapshot before every task run), post-run commits, automating commits via hooks, useful git commands for assistant files, and meaningful commit message conventions.

**Use this when:** you have a scheduled task running regularly and want the ability to roll back bad runs, see what changed between runs, or track how your assistant's knowledge and instructions have evolved over time.

---

### [10 — Development and Execution Workflow](./10_DEV_EXECUTION_WORKFLOW.md)
`[Power user]` · `~15 min`

*Using Claude Code and Cowork as two distinct tools with two distinct roles — and how to work effectively with Cowork alone.*

Covers: the development/execution split (Claude Code for building and maintaining, Cowork for running), file architecture that works cleanly in both tools, a Cowork-only workflow for users without Claude Code, Plan Mode for reviewing changes before executing, subagents for parallel exploration and planning, the workflow for adding or changing something, debugging broken runs, reviewing and applying self-improvement proposals, and a new-features checklist.

**Use this when:** you want a clear workflow for how to build, maintain, and iterate on your setup — whether you use Claude Code or work entirely within Cowork.

---

### [11 — Personal Data Layer](./11_PERSONAL_DATA_LAYER.md)
`[Power user]` · `~20 min`

*Five patterns for getting personal data into Claude's hands.*

Covers: Python scripts as data feeders, JSON as a personal database, browser JavaScript extraction for apps with no API, Claude Vision for screenshot ingestion, and multi-step instruction files for complex workflows.

**Use this when:** you want Claude to reason about personal data (investments, spending, bank transactions) but the data lives in apps that have no API, in raw files too large to paste in directly, or in formats Claude can't parse without help.

---

### [12 — LLM Wiki](./12_LLM_WIKI.md)
`[Power user]` · `~20 min`

*The LLM wiki pattern: building a persistent, compounding knowledge base.*

Covers: the difference between RAG and a wiki, the three-layer architecture (sources, wiki, schema), the three operations (ingest, query, lint), index and log conventions, writing a schema, practical applications (threat intel, research, competitive analysis), tooling tips (Obsidian, Marp, Dataview, qmd), and git integration.

**Use this when:** you want to build a domain knowledge base that compounds over time — where adding a new source enriches every related page, and answers are already synthesised before you ask the question.

---

### [13 — Security](./13_SECURITY.md)
`[All users]` · `~15 min`

*Operational security for using Claude Code and Cowork safely.*

Covers: credential hygiene (where secrets belong and where they must not go), MCP server trust evaluation, permission controls and PreToolUse execution guard hooks, session data hygiene (transcripts, shell snapshots), supply chain awareness when Claude installs packages, prompt injection risks in autonomous tasks, file hygiene (`.gitignore` and `.claudeignore` for sensitive materials and sharing), and autonomous task safety principles.

**Use this when:** you're setting up a new Claude environment and want it secured from the start, auditing an existing setup, adding a new MCP server, or designing an autonomous task that handles sensitive data or takes consequential actions.

---

### [14 — Troubleshooting](./14_TROUBLESHOOTING.md)
`[All users]` · `~10 min (reference)`

*When things don't work — problem by problem.*

Covers: skill not triggering, CLAUDE.md being ignored, memory not persisting, MCP tools failing, output format drifting, slow tasks, confusing improvement proposals, and recovering from broken changes.

**Use this when:** something isn't working and you want a structured guide to diagnosing and fixing it.

---

### [15 — Prompting Basics](./15_PROMPTING_BASICS.md)
`[All users]` · `~15 min`

*Writing instructions that produce consistent, high-quality output.*

Covers: the anatomy of a good instruction (context + task + constraints + output format), why examples outperform descriptions, how to specify what NOT to do, writing skill trigger descriptions that actually work, debugging a bad prompt, and the most common mistakes with before/after fixes.

**Use this when:** Claude's output isn't what you expected, you're writing a new skill or task instruction, or you want to improve the quality of your setup systematically.

---

## Templates: Copy-Paste Starting Points

Four ready-to-copy folder structures are included in the `templates/` folder. Use them when you want to start a new project or task without building from scratch.

### [PROJECT_TEMPLATE/](./templates/PROJECT_TEMPLATE/README.md)
A complete project folder with `CLAUDE.md`, `Profile/`, and `Knowledge/` pre-structured and filled with placeholder text. Copy it, rename it, fill in the placeholders, and you have a working persistent assistant context from run 1.

**Use this when:** starting any new Claude project that needs cross-session memory, profile tracking, or topic knowledge files.

### [TASK_TEMPLATE/](./templates/TASK_TEMPLATE/README.md)
A complete scheduled task folder with `TASK.md`, `IMPROVEMENTS.md`, `KNOWLEDGE_SUMMARY.md`, and `RUN_LOG.md` — all pre-structured and ready to fill in. Implements the patterns from Guide 04 (efficiency) and Guide 05 (self-improvement) out of the box.

**Use this when:** creating a new scheduled automated task. Copy the folder, rename it `[TaskName]-Task`, and fill in the domain-specific logic.

### [AI-ASSISTANT_TEMPLATE/](./templates/AI-ASSISTANT_TEMPLATE/SETUP.md)
A complete personal business assistant setup. Monitors your email, Teams, and calendar via Microsoft 365, maintains a live profile of your work context, and delivers a daily briefing. Four coordinated scheduled tasks are included out of the box: daily morning briefing, mid-day urgent scan, Friday weekly planner, and Monday maintenance. Includes a pre-structured `CLAUDE.md`, `Profile/`, `Knowledge/`, and `Actions/` system.

**Use this when:** you want a turn-key personal assistant that monitors your inbox and calendar and delivers daily briefings — with all the task scaffolding already built.

### [PMO_TEMPLATE/](./templates/PMO_TEMPLATE/README.md)
A project workspace for managing a product migration initiative. Includes a `CLAUDE.md` with routing rules, a project guide, an initiative charter, and a full PMO register suite: risk register, action tracker, dependency register, decision tracker, and a running knowledge base.

**Use this when:** managing a structured programme or migration initiative where you want Claude to maintain registers, capture decisions, and track actions across sessions.

---

## Tasks: One-Command Setup and Auditing

Tasks are standalone instruction files you run by saying `Claude, run tasks/[task-name].md`. Each task handles a specific setup or audit job end-to-end — interviewing you, proposing changes, and applying them after approval.

**Three ways to use the guides in this project:**
1. **Read them yourself** and set things up manually
2. **Give a guide to Claude** — `"Read 01_CLAUDE_MD.md and help me write my CLAUDE.md"`
3. **Run a task** — faster, guided, no reading required

Tasks are designed to be portable: copy any task file to another project's `tasks/` directory and run it there. Each task includes a `Source guide:` reference so you can trace it back here.

### Setup tasks (one-time)

| Task | What it does | Source guide |
|------|-------------|-------------|
| `tasks/onboard-project.md` | End-to-end project setup — orchestrates the tasks below in the right order; optionally starts from a template | 01, 03, 08, 09, 13 |
| `tasks/setup-claude-md.md` | Interview → generate `CLAUDE.md` | 01 |
| `tasks/setup-memory.md` | Create `.auto-memory/` with initial memory files | 03 |
| `tasks/setup-mcp.md` | Audit and add MCP server connections | 08 |
| `tasks/setup-security.md` | Credential scan, permission audit, install PreToolUse hook | 13 |
| `tasks/setup-github.md` | Init git, create GitHub repo, set up ongoing sync | 09 |
| `tasks/setup-ignore-hygiene.md` | Audit `.gitignore`/`.claudeignore`, install check hook | 09, 13 |
| `tasks/setup-self-improving-task.md` | Add `IMPROVEMENTS.md` + self-improvement loop to any task | 05, 06 |
| `tasks/setup-wiki.md` | Create LLM wiki structure for a topic | 12 |
| `tasks/setup-bootstrap-folder.md` | Create `bootstrap/` stubs for gitignored runtime state files | 09 |
| `tasks/setup-skill.md` | Interview → generate a `SKILL.md` with reliable triggering and full structure | 02 |
| `tasks/setup-scheduled-task.md` | Scaffold a new scheduled task with efficiency + self-improvement built in | 04, 05, 06 |
| `tasks/setup-data-layer.md` | Set up data patterns for personal data (Python feeder, JSON DB, browser extraction, vision) | 11 |

### Audit tasks (re-runnable)

| Task | What it does | Source guide |
|------|-------------|-------------|
| `tasks/audit-claude-md.md` | Review `CLAUDE.md` — dead rules, missing sections, over-length | 01, 07 |
| `tasks/audit-task-efficiency.md` | Token efficiency checklist for any task file | 04 |
| `tasks/audit-memory.md` | Check memory files for staleness, duplicates, misplaced content | 03 |
| `tasks/audit-skill.md` | Review a `SKILL.md` — trigger quality, workflow, output format, edge cases | 02, 15 |

### Maintenance (Claude Teacher only)

| Task | What it does |
|------|-------------|
| `tasks/review-tasks.md` | Detect guide updates and flag tasks that need syncing — run after editing any guide |

---

## Skills Included in This Project

Four installable skills are bundled with this project. Each skill is self-contained — install only the ones you need.

### Installing in Claude Code

Skills are loaded automatically from the `~/.claude/skills/` directory. Copy any skill folder there:

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/skill-folder ~/.claude/skills/
```

Claude Code will detect and activate the skill immediately — no restart needed.

### Installing in Claude.ai (Personal Skills)

Claude.ai has a built-in Personal Skills feature that accepts skill uploads directly.

Pre-packaged `.skill` files are included in `./skills/` — no zipping required.

Go to **claude.ai → Skills → Upload skill** and drag in the `.skill` file for the skill you want.

Claude.ai reads the `name:` and `description:` frontmatter in `SKILL.md` to name the skill and trigger it automatically — the same way Claude Code does.

---

### ai-assistant-setup

An interactive setup coach. All guides are bundled into this skill. Instead of reading guides and acting on them manually, install this skill once and describe what you want — Claude reads the relevant guides and does the work.

**Install:** Copy `ai-assistant-setup/` to `~/.claude/skills/` (Claude Code), or upload `ai-assistant-setup.skill` to Claude.ai Personal Skills.

**Use when:**
- Setting up Claude as a personal assistant from scratch
- Improving or auditing an existing setup
- Adding a specific component (skill, memory system, data pattern)

**Example prompts:**
> "Help me set up Claude as a personal assistant from scratch."

> "I have an investments project — help me add browser extraction to it."

> "Create a skill for drafting messages in Finnish."

---

### template-exporter

Turns any existing Claude setup — a chat system prompt, Cowork task, Cowork project, or skill — into a clean, shareable template. Strips personal and business identifiers, adds placeholder annotations, and produces a dual-audience output: a human-readable README and a Claude setup prompt.

**Install:** Copy `template-exporter/` to `~/.claude/skills/` (Claude Code), or upload `template-exporter.skill` to Claude.ai Personal Skills.

**Use when:**
- You want to share a setup you've built (with someone else, or across projects)
- You've refined a skill or task and want to preserve a clean, reusable copy
- You want to turn a one-off Claude workflow into something repeatable

**Example prompts:**
> "Turn this skill into a shareable template."

> "Export my Cowork task as a template I can give to a colleague."

> "Make this system prompt reusable."

---

### cowork-optimizer

Audits a Cowork task or project for token efficiency, run speed, and structural quality. Identifies concrete improvements across 9 dimensions, presents a prioritized plan, and implements agreed changes.

**Install:** Copy `cowork-optimizer/` to `~/.claude/skills/` (Claude Code), or upload `cowork-optimizer.skill` to Claude.ai Personal Skills.

**Use when:**
- A scheduled task is slow or expensive to run
- You want to review a task before deploying it
- A task has grown over time and needs a structural cleanup

**Example prompts:**
> "My scheduled task is running slowly. Audit it for token efficiency."

> "Review my task and tell me what can be improved."

> "This task is too long — help me split it."

---

### security-review

A structured, phased security audit of the Claude Code environment and a target project. Covers credential exposure, MCP server risk, permission controls and execution guard hooks, session data hygiene, supply chain scanning, and malware detection. Read-only assessment phases run automatically; mutating phases (hook installation, tool installs) pause for approval before making any changes.

**Install:** Copy `security-review/` to `~/.claude/skills/` (Claude Code).

**Use when:**
- Auditing a Claude Code setup for security issues
- Setting up PreToolUse execution guard hooks for the first time
- Adding a new MCP server and wanting a trust assessment
- Scanning a project for accidentally committed secrets

**Example prompts:**
> "Review my Claude Code setup for security issues."

> "Set up security hooks for my Claude environment."

> "Audit this project for exposed credentials."

---

## Quick Start Without the Skill (5 minutes)

Prefer to do it manually? Start here:

1. Follow **[00_QUICKSTART.md](./00_QUICKSTART.md)** — build your first CLAUDE.md and skill in 20 minutes with exact file templates.
2. Come back for the rest when you've used it a few times and know what you want next.

Or for just the minimum:
1. Read **Guide 01** — takes 5 minutes.
2. Ask Claude: *"Read 01_CLAUDE_MD.md and help me write my CLAUDE.md. Ask me what you need to know."*
3. Save the result to `.claude/CLAUDE.md`.

---

## Recommended Starting Path

If you're new to this, go in this order:

1. **Start with [00_QUICKSTART.md](./00_QUICKSTART.md)** — get something working first.
2. **Then 01** — refine your CLAUDE.md once you've seen how it behaves.
3. **Then 02** — create your first real skill for whatever you do most often.
4. **Then 03** — enable cross-session memory so the assistant learns over time.
5. **Only then 04 + 05 + 06** — once you have scheduled tasks running, optimise and teach them to improve.

**Quick reference while building:** Keep [CHEATSHEET.md](./CHEATSHEET.md) open as a one-page reference for file structures, skeletons, and common patterns.
**If something breaks:** Go to [Guide 14 — Troubleshooting](./14_TROUBLESHOOTING.md).

---

## Giving a Guide to Claude Directly

Each guide is also written so Claude can read it and act on it without the skill installed:

> "Read 02_SKILLS.md and then create a skill for drafting project status updates."

> "Read 01_CLAUDE_MD.md and help me write my own CLAUDE.md based on what you know about me."

> "Read 04_TASK_EFFICIENCY_GUIDE.md and audit my existing email digest task for token efficiency."
