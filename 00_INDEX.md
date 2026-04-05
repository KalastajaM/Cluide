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

## The Guides

### [01 — CLAUDE.md](./01_CLAUDE_MD.md)
*The foundation: what goes in your always-loaded instruction file.*

Covers: what to put in CLAUDE.md, how to structure it, what not to include, and how to keep it lean and effective. Includes a real-world example.

**Use this when:** you're setting up Claude for the first time, or the assistant keeps behaving in ways you have to correct session after session.

---

### [02 — Skills](./02_SKILLS.md)
*How to design skills for recurring tasks.*

Covers: the anatomy of a SKILL.md file, writing descriptions that trigger reliably, structuring workflow steps, output formats, and edge cases. Includes real examples from a working setup.

**Use this when:** there's a task you do repeatedly (checking email for actions, drafting messages in a second language, building a shopping list) and you want Claude to handle it consistently every time.

---

### [03 — Memory & Profile](./03_MEMORY_AND_PROFILE.md)
*Two complementary persistence systems.*

Covers: the auto-memory system (lightweight, always-on), profile files (structured, richly maintained for complex recurring agents), what to store, how to keep files lean, and the hypothesis system.

**Use this when:** you want Claude to remember things across sessions — your preferences, corrections, ongoing projects, and key contacts.

---

### [04 — Task Efficiency](./04_TASK_EFFICIENCY_GUIDE.md)
*How to design and optimize scheduled tasks for minimal token consumption.*

Covers: splitting instruction files, scripting fixed-format output, targeted file edits, two-pass triage for external data, hard size limits, and run deduplication.

**Use this when:** you have a scheduled task running regularly and want to audit it for efficiency — or want to set one up correctly from the start.

---

### [05 — Task Self-Improvement](./05_TASK_LEARNING_GUIDE.md)
*A framework for building tasks that get better over time.*

Covers: what to learn and how to store it, detecting feedback signals, the apply-vs-propose decision, the hypothesis lifecycle, the refactoring system, and the improvements log.

**Use this when:** you have a scheduled task up and running and want it to evolve — fixing its own mistakes, codifying patterns, and proposing improvements rather than repeating errors.

---

### [06 — Self-Improvement Template](./06_SELFIMPROVE_TEMPLATE.md)
*A ready-to-use IMPROVEMENTS.md template.*

A concrete template file that implements the system described in Guide 05. Drop it into any task folder and it's ready to use.

**Use this when:** you're creating a new scheduled task and want the self-improvement system set up from run 1.

---

### [07 — Best Practices](./07_BEST_PRACTICES.md)
*Lessons from real use — a shareable summary.*

Covers: giving Claude good inputs, working effectively session-to-session, building a setup that compounds over time, and knowing when not to use Claude. Includes a 15-point short version for quick reference.

**Use this when:** you want a quick overview of what actually matters, or you want something to share with someone just getting started.

---

### [08 — MCP Servers](./08_MCP_SERVERS.md)
*How Claude connects to external tools — Gmail, Calendar, GitHub, and more.*

Covers: what MCP servers are, how to configure them in Claude Code, the most useful servers for personal assistants, how to reference tool names in skills, and credential security.

**Use this when:** you're setting up a skill that uses external tools (email, calendar, files) and need to understand where those tools come from — or when a skill isn't finding the tools it needs.

---

### [09 — Git Integration](./09_GIT_INTEGRATION.md)
*Version control for your assistant's state — pre-run snapshots, rollback, and history.*

Covers: what to track in git, the pre-run commit pattern (snapshot before every task run), post-run commits, automating commits via hooks, useful git commands for assistant files, and meaningful commit message conventions.

**Use this when:** you have a scheduled task running regularly and want the ability to roll back bad runs, see what changed between runs, or track how your assistant's knowledge and instructions have evolved over time.

---

## Quick Start (5 minutes)

Not ready to read all the guides? Start with just one thing:

1. Read **Guide 01** — takes 5 minutes.
2. Ask Claude: *"Read 01_CLAUDE_MD.md and help me write my CLAUDE.md. Ask me what you need to know."*
3. Save the result to `.claude/CLAUDE.md`.

That's it. Come back for the rest when you've used it a few times and know what you want to improve.

---

## Recommended Starting Path

If you're new to this, read and act on the guides in this order:

1. **Start with 01** — get your CLAUDE.md right. It affects every interaction.
2. **Then 02** — create your first skill for whatever you do most often.
3. **Then 03** — enable cross-session memory so the assistant learns over time.
4. **Only then 04 + 05 + 06** — once you have scheduled tasks running, optimize and teach them to improve.

---

## Giving a Guide to Claude

Each guide is written so Claude can read it and act on it. For example:

> "Read 02_SKILLS.md and then create a skill for drafting project status updates. The skill should follow all the best practices in the guide."

> "Read 01_CLAUDE_MD.md and help me write my own CLAUDE.md based on what you know about me."

> "Read 04_TASK_EFFICIENCY_GUIDE.md and audit my existing email digest task for token efficiency."

Claude will follow the guide's recommendations when creating or updating the relevant component.
