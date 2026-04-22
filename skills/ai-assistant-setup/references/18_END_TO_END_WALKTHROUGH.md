# 18 — End-to-End Walkthrough: From Zero to Running Assistant

*Last reviewed: April 2026*

> Build a complete personal assistant from scratch, seeing how each guide contributes to the whole.

This walkthrough takes you from nothing to a fully operational system with skills, memory, scheduled tasks, and security — over roughly two weeks. Each stage builds on the previous one. Unlike the [Quickstart](./00_QUICKSTART.md), which gives you a working setup in 20 minutes, this guide shows the full journey and explains why each piece matters.

---

## Companion Guides

Every Cluide guide plays a role in this walkthrough. Here is the full set, in the order they appear:

| Stage | Guides used |
|---|---|
| Foundation | [01 — CLAUDE.md](./01_CLAUDE_MD.md), [02 — Prompting Basics](./02_PROMPTING_BASICS.md) |
| First Skill | [03 — Skills](./03_SKILLS.md), [05 — MCP Servers](./05_MCP_SERVERS.md) |
| Memory | [04 — Memory & Profile](./04_MEMORY_AND_PROFILE.md) |
| First Scheduled Task | [06 — Task Efficiency](./06_TASK_EFFICIENCY_GUIDE.md), [07 — Task Self-Improvement](./07_TASK_LEARNING_GUIDE.md), [08 — Self-Improvement Template](./08_SELFIMPROVE_TEMPLATE.md) |
| Security Check | [12 — Security](./12_SECURITY.md), [11 — Git Integration](./11_GIT_INTEGRATION.md) |
| Growing the System | [09 — Multi-Task Orchestration](./09_MULTI_TASK_ORCHESTRATION.md), [10 — Cost & Performance](./10_COST_PERFORMANCE.md), [15 — LLM Wiki](./15_LLM_WIKI.md) |

Supporting guides that apply throughout: [13 — Dev Execution Workflow](./13_DEV_EXECUTION_WORKFLOW.md), [14 — Personal Data Layer](./14_PERSONAL_DATA_LAYER.md), [16 — Best Practices](./16_BEST_PRACTICES.md), [17 — Troubleshooting](./17_TROUBLESHOOTING.md).

---

## Stage 1: Foundation (Day 1)

**What you are building:** The instruction file that shapes every conversation — your CLAUDE.md.

**Read first:** [Guide 01](./01_CLAUDE_MD.md) (10 min), then [Guide 02](./02_PROMPTING_BASICS.md) (15 min).

**Action — create your CLAUDE.md:**

```
"Read 01_CLAUDE_MD.md and help me write my CLAUDE.md. Ask me what you need to know."
```

Claude will interview you about your identity, timezone, communication preferences, and standing rules. The result is a 15-25 line file at `.claude/CLAUDE.md`.

**What the result looks like:** A short file with sections for identity, communication style, and standing rules. Every line changes how Claude behaves — no filler.

**Check before moving on:**
- Open a fresh conversation and give a simple instruction. Does Claude apply your timezone, language preference, and style rules without being asked?
- If something feels off, edit the line that governs it and test again. Guide 02 explains why phrasing matters.

---

## Stage 2: First Skill (Day 1-2)

**What you are building:** A reusable skill for a task you do regularly — something concrete enough to test immediately.

**Read first:** [Guide 03](./03_SKILLS.md) (15 min). If your skill needs external tools (email, calendar, files), also read [Guide 05](./05_MCP_SERVERS.md) (15 min).

**Action — create your first skill:**

```
"Read 03_SKILLS.md and create a skill for [your task]. Ask me about the workflow, 
output format, and edge cases."
```

Good first skills: planning your day, drafting emails in a second language, summarising meeting notes, building a weekly shopping list.

If the skill needs MCP tools (e.g., reading email requires the Gmail MCP server), connect those first:

```
"Read 05_MCP_SERVERS.md and help me set up the MCP servers I need for this skill."
```

**What the result looks like:** A `SKILL.md` file at `.claude/skills/[skill-name]/SKILL.md` with frontmatter (name, description), a workflow section, an output format template, and edge case handling.

**Check before moving on:**
- Start a fresh conversation and trigger the skill using natural phrasing — not the exact description text
- Verify the output matches the format you specified
- If the skill does not trigger, check the `description:` field in the frontmatter — it controls matching. See [Guide 17](./17_TROUBLESHOOTING.md) if stuck

---

## Stage 3: Memory (Day 2-3)

**What you are building:** A persistence layer so Claude remembers corrections, preferences, and key facts across sessions.

**Read first:** [Guide 04](./04_MEMORY_AND_PROFILE.md) (15 min).

**Action — set up memory:**

```
"Read 04_MEMORY_AND_PROFILE.md and set up my memory system. Ask me about the key 
facts and preferences you should remember."
```

Or run the setup task directly:

```
"Run tasks/setup-memory.md"
```

This creates the `.auto-memory/` folder with structured memory files. Claude will ask about contacts, ongoing projects, and preferences worth persisting.

**What the result looks like:** A small set of memory files — typically an index, a preferences file, and one or two topic files (contacts, projects). Each file is compact and specific.

**Check before moving on:**
- Start a fresh conversation and reference something stored in memory (a contact name, a project abbreviation, a preference)
- Claude should recall it without you re-explaining
- If memory is not loading, confirm the files are in the right location. Guide 04 covers the folder structure

---

## Stage 4: First Scheduled Task (Week 1)

**What you are building:** An automated task that runs on a schedule without you asking — and improves itself over time.

**Read first:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) (15 min) for efficiency patterns. [Guide 07](./07_TASK_LEARNING_GUIDE.md) (20 min) for the self-improvement framework. [Guide 08](./08_SELFIMPROVE_TEMPLATE.md) (5 min) for the template.

**Action — scaffold the task:**

```
"Run tasks/setup-scheduled-task.md"
```

This creates a task folder with `TASK.md`, `IMPROVEMENTS.md`, `KNOWLEDGE_SUMMARY.md`, and `RUN_LOG.md` — all pre-structured. You can also copy `templates/TASK_TEMPLATE/` and fill it in manually.

Good first tasks: a daily email digest, a weekly calendar summary, a morning briefing that pulls from email and calendar.

**Action — add self-improvement:**

If you used the task template, self-improvement is already wired in. If you built the task manually:

```
"Run tasks/setup-self-improving-task.md against my task at [path/to/TASK.md]"
```

**Action — schedule it:**

Set up the task to run on a schedule through Cowork's scheduled tasks panel. Start with a low frequency (daily or weekly) so you can review the output before it runs unattended.

**What the result looks like:** A task folder containing the instruction file, an improvements log, a knowledge summary, and a run log. After a few runs, the improvements log will contain observations and proposals the task has generated from its own output.

**Check before moving on:**
- Run the task manually once and review the output
- Check that `RUN_LOG.md` was updated with a timestamp and summary
- Verify the task reads only what it needs — Guide 06's audit checklist is useful here
- After 3-5 runs, check `IMPROVEMENTS.md` for proposals. Review and approve or reject each one

---

## Stage 5: Security Check (Week 1)

**What you are building:** A secured environment — credentials protected, permissions controlled, file hygiene enforced.

**Read first:** [Guide 12](./12_SECURITY.md) (15 min), then [Guide 11](./11_GIT_INTEGRATION.md) (20 min).

**Action — run the security audit:**

```
"Run tasks/setup-security.md"
```

This scans for exposed credentials, audits MCP server permissions, and optionally installs a PreToolUse execution guard hook.

**Action — set up git and file hygiene:**

```
"Run tasks/setup-github.md"
```

Then:

```
"Run tasks/setup-ignore-hygiene.md"
```

This initialises version control, creates a GitHub repo if you want one, and audits `.gitignore` and `.claudeignore` to ensure sensitive and large files are excluded.

**What the result looks like:** A clean git repository with proper ignore rules. No credentials in tracked files. A PreToolUse hook that blocks dangerous operations if you chose to install one.

**Check before moving on:**
- Run `git status` — no sensitive files should appear in the tracked list
- Check `.gitignore` includes run logs, output files, and anything containing personal data
- Check `.claudeignore` includes large generated files that do not need to be loaded as context
- If you installed a PreToolUse hook, test it by asking Claude to perform an action the hook should block

---

## Stage 6: Growing the System (Week 2+)

With the foundation solid, you can expand in any direction. Here are the most common next steps.

### Add more tasks and orchestrate them

**Read:** [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) (20 min).

When you have two or more tasks that share data or need to run in sequence, orchestration prevents them from stepping on each other. Common pattern: an email scan task writes a summary file, and a briefing task reads it.

```
"Read 09_MULTI_TASK_ORCHESTRATION.md and help me connect my [task A] and [task B] 
so they share data cleanly."
```

### Monitor costs

**Read:** [Guide 10](./10_COST_PERFORMANCE.md) (15 min).

Once tasks run regularly, track what they cost. Guide 10 covers per-run metrics, budget checks, and finding expensive operations.

```
"Read 10_COST_PERFORMANCE.md and set up cost tracking for my scheduled tasks."
```

### Build a knowledge base

**Read:** [Guide 15](./15_LLM_WIKI.md) (20 min).

The LLM wiki pattern creates a persistent, compounding knowledge base — where adding a new source enriches every related page.

```
"Run tasks/setup-wiki.md"
```

Good first wikis: competitive intelligence, personal finance research, technical domain notes.

### Connect personal data

**Read:** [Guide 14](./14_PERSONAL_DATA_LAYER.md) (20 min).

When you need Claude to reason about data from apps without APIs — bank transactions, investment portfolios, spending reports — Guide 14 covers five patterns for getting that data in.

```
"Read 14_PERSONAL_DATA_LAYER.md and help me set up a data feeder for [your data source]."
```

### Use the development workflow

**Read:** [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) (15 min).

As your system grows, having a clear workflow for building vs. running matters. Guide 13 covers the Claude Code / Cowork split, Plan Mode, and debugging broken runs.

---

## The Full Picture

After completing all stages, your system looks like this:

```
~/.claude/
  CLAUDE.md                          # Standing rules (Stage 1)
  skills/
    [skill-name]/SKILL.md            # Reusable skills (Stage 2)
  tasks/
    [task-name]/
      TASK.md                        # Task instructions (Stage 4)
      IMPROVEMENTS.md                # Self-improvement log (Stage 4)
      KNOWLEDGE_SUMMARY.md           # Learned patterns (Stage 4)
      RUN_LOG.md                     # Run history (Stage 4)
  .auto-memory/                      # Cross-session persistence (Stage 3)
  settings.json                      # Hooks and permissions (Stage 5)

.gitignore                           # File hygiene (Stage 5)
.claudeignore                        # Context hygiene (Stage 5)
```

Each piece reinforces the others: CLAUDE.md sets the baseline, skills handle recurring work, memory accumulates knowledge, tasks automate what skills cannot, and git preserves the history of it all.

---

## Giving This Guide to Claude

You can hand this guide to Claude and ask it to walk you through any stage:

> "Read 18_END_TO_END_WALKTHROUGH.md and help me complete Stage 1. I'm starting from scratch."

> "Read 18_END_TO_END_WALKTHROUGH.md. I've done Stages 1-3 already. Walk me through Stage 4."

> "Read 18_END_TO_END_WALKTHROUGH.md and tell me which stage I should focus on next based on my current setup."

For the 20-minute minimal version, see [00_QUICKSTART.md](./00_QUICKSTART.md). For a one-page reference while building, see [CHEATSHEET.md](./CHEATSHEET.md). If something breaks, see [Guide 17 — Troubleshooting](./17_TROUBLESHOOTING.md).
