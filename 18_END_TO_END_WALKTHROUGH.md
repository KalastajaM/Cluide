# 18 — End-to-End Walkthrough: From Zero to Running Assistant

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
| First Scheduled Task | [06 — Task Efficiency](./06_TASK_EFFICIENCY_GUIDE.md), [07 — Task Self-Improvement](./07_TASK_LEARNING_GUIDE.md) (incl. Part 9: the template) |
| Security Check | [12 — Security](./12_SECURITY.md), [11 — Git Integration](./11_GIT_INTEGRATION.md) |
| Growing the System | [09 — Multi-Task Orchestration](./09_MULTI_TASK_ORCHESTRATION.md), [10 — Cost & Performance](./10_COST_PERFORMANCE.md), [15 — LLM Wiki](./15_LLM_WIKI.md) |

Supporting guides that apply throughout: [13 — Dev Execution Workflow](./13_DEV_EXECUTION_WORKFLOW.md), [14 — Personal Data Layer](./14_PERSONAL_DATA_LAYER.md), [16 — Best Practices](./16_BEST_PRACTICES.md), [17 — Troubleshooting](./17_TROUBLESHOOTING.md).

---

## Choose a Route and a Shared Starter

Use a small, connector-free planner before adding live email or schedules. The outcome is the same on each surface: a dated plan from supplied task notes, no outbound actions, and one accepted place to save the result.

**Claude local route:** open a project folder in Claude Code or connect it in Cowork. Create root `AGENTS.md` with purpose, timezone, draft-only action rule and `outputs/` as the output home; create `CLAUDE.md` with `@AGENTS.md` and an explicit read fallback. For Cowork, add the project-instructions bootstrap from [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md).

**Codex local route:** open the same folder as the workspace. Codex reads the native `AGENTS.md` chain. Inspect any override, then ask it to read a small `tasks/planner/TASK.md` and `tasks/planner/INPUT.md` and save `outputs/plan.md`. The task can simply group the supplied items into must-do, focus blocks and defer; it needs no external app.

**ChatGPT uploaded-source route:** create a project, add the shared policy, task and input as sources, and put a short instruction in project settings to read them first. Record their revision. Ask for the same plan as a downloadable Markdown file or reusable text; incorporate that result into the authored project explicitly. Do not ask this route to write to a laptop path it cannot access.

**Acceptance prompt for every route:** "Use the supplied planner task and input. State the input revision, apply the project's timezone, and produce the plan in the requested format. Report whether it was saved to the project or delivered for incorporation. Do not send anything."

Check against an expected plan written before running: every input item accounted for, correct timezone, correct output home/delivery, no external actions. Start a fresh session to test policy loading. Then change one source item and repeat after reloading or refreshing sources. These are documented starter procedures, not claims that your account has passed them. Record each result as passed, failed or untested.

The stages below develop this starter. Claude-only paths are labelled; choose the equivalent native path explicitly for OpenAI rather than copying a dot-directory.

---

## Stage 1: Foundation (Day 1)

**What you are building:** The shared operating contract and its native entry point: `AGENTS.md`, with `CLAUDE.md` as the Claude adapter or project instructions for source-only use.

**Read first:** [Guide 01](./01_CLAUDE_MD.md) (10 min), then [Guide 02](./02_PROMPTING_BASICS.md) (15 min).

**Action — create the shared policy and native entry point:**

```
"Read 01_CLAUDE_MD.md and help me write the shared policy for my chosen surface.
Create AGENTS.md and the appropriate adapter or project bootstrap. Ask only for
identity, timezone, style and action rules that are not already known."
```

Or run the setup task directly:

```
"Run tasks/setup-claude-md.md"
```

The assistant establishes your identity, timezone, communication preferences and standing rules. Keep the personal policy compact ([Guide 01](./01_CLAUDE_MD.md)); the selected route above determines its entry point. Use root `AGENTS.md` for the shared starter.

**What the result looks like:** A short file with sections for identity, communication style, and standing rules. Every line changes the intended behaviour — no filler.

**Check before moving on:**
- Open a fresh conversation and give a simple instruction. Does the assistant apply your timezone, language preference, and style rules without being asked?
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

Or run the setup task directly:

```
"Run tasks/setup-skill.md"
```

Good first skills: planning your day, drafting emails in a second language, summarising meeting notes, building a weekly shopping list.

If the skill needs external data, inspect existing tools first. Reading email may use a native app connector or MCP; connect only the missing capability:

```
"Read 05_MCP_SERVERS.md and help me set up the MCP servers I need for this skill."
```

(or run `tasks/setup-mcp.md` directly).

**What the result looks like:** A `SKILL.md` file at `.claude/skills/[skill-name]/SKILL.md` for Claude Code, `.agents/skills/[skill-name]/SKILL.md` for Codex, or the available app installation surface, with frontmatter (name, description), a workflow section, an output format template, and edge case handling.

**Check before moving on:**
- Start a fresh conversation and trigger the skill using natural phrasing — not the exact description text
- Verify the output matches the format you specified
- If the skill does not trigger, check the `description:` field in the frontmatter — it controls matching. See [Guide 17](./17_TROUBLESHOOTING.md) if stuck

---

## Stage 3: Memory (Day 2-3)

**What you are building:** A persistence layer so the assistant can recover corrections, preferences, and key facts across sessions.

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

This creates the `.auto-memory/` folder with structured memory files. The assistant will ask about contacts, ongoing projects, and preferences worth persisting.

**What the result looks like:** A small set of memory files — typically an index, a preferences file, and one or two topic files (contacts, projects). Each file is compact and specific.

**Check before moving on:**
- Start a fresh conversation and reference something stored in memory (a contact name, a project abbreviation, a preference)
- The assistant should retrieve the recorded fact without you re-explaining
- If memory is not loading, confirm the files are in the right location. Guide 04 covers the folder structure

---

## Stage 4: First Scheduled Task (Week 1)

**What you are building:** An automated task that runs on a schedule without you asking — and improves itself over time.

**Read first:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) (15 min) for efficiency patterns. [Guide 07](./07_TASK_LEARNING_GUIDE.md) (20 min) for the self-improvement framework. Guide 07 Part 9 (5 min) for installing the template.

**Action — scaffold the task:**

```
"Run tasks/setup-scheduled-task.md"
```

This creates a task folder with `TASK.md`, `IMPROVEMENTS.md`, `TASK_REFERENCE.md`, and `RUN_LOG.md` — all pre-structured. You can also copy `templates/TASK_TEMPLATE/` and fill it in manually.

Good first tasks: a daily email digest, a weekly calendar summary, a morning briefing that pulls from email and calendar.

**Action — add self-improvement:**

If you chose self-improvement in the setup interview (or started from the task template), it is already wired in. If you built the task manually or skipped it:

```
"Run tasks/setup-self-improving-task.md against my task at [path/to/TASK.md]"
```

**Action — schedule it:**

Choose one scheduler owner: Cowork for the Claude route, or OpenAI Scheduled for a supported local/web task. Give it a stable job ID, timezone, source revision and output contract. Test manually first, then review the first scheduled run. Keep local hosts awake where required. Do not register the same job on both platforms; [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) explains the native paths.

**What the result looks like:** A task folder containing the instruction file, an improvements log, a task reference, and a run log. After a few runs, the improvements log will contain observations and proposals the task has generated from its own output.

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

This reviews credentials and actual runtime permissions. Claude Code may use a tested PreToolUse hook; Codex uses its native sandbox/approval controls. ChatGPT uses its source access and app grants. Do not install a Claude hook as an OpenAI safeguard.

**Action — set up git and file hygiene:**

```
"Run tasks/setup-github.md"
```

Then:

```
"Run tasks/setup-ignore-hygiene.md"
```

This initializes version control, creates a GitHub repository if wanted, and audits `.gitignore` plus the selected runtime's actual context and permission controls. Review `.claudeignore` only for a Claude surface that supports it; do not create it as a Codex requirement or treat it as a security boundary.

**What the result looks like:** A clean git repository with proper ignore rules. No credentials in tracked files. A harmless fixture demonstrating the chosen native access boundary.

**Check before moving on:**
- For a local versioned project, inspect tracked files and `git status` for sensitive material; a source-only project instead checks its supplied source package
- For a local versioned project, check `.gitignore` covers private run logs, generated outputs and personal data. For a source-only project, exclude that material from the uploaded/connected package unless explicitly needed
- For Claude only, check supported `.claudeignore` patterns for large generated context. For Codex, verify native permissions and explicit source-scoping instructions; for ChatGPT, inspect the uploaded/connected source set
- Test an intended denial with harmless fixture data on each enabled surface; never use a real destructive operation as the test

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

As your system grows, having a clear workflow for building vs. running matters. Guide 13 covers development/execution roles across Claude and OpenAI, plan mode and evidence-based debugging.

---

## The Full Picture

After completing the applicable stages, the authored project has these homes:

```text
[project]/
  AGENTS.md                         # Shared standing rules
  CLAUDE.md                         # Claude adapter
  PLATFORM_SETUP.md                 # Source revisions, native setup and test results
  .auto-memory/                     # Explicit private project memory
  tasks/[task-name]/
    TASK.md                         # Task instructions
    TASK_REFERENCE.md               # On-demand reference
    IMPROVEMENTS.md                  # Accepted/proposed learning
    RUN_LOG.md                      # Run history, private when personal
  outputs/                          # Deliverables
  .gitignore                        # Version-control hygiene
```

Install skill entry points and configure permissions separately: Claude Code uses its `.claude` locations, Codex uses `.agents/skills` and its own configuration, and conversational projects use their available installation and source controls. Guide 03 and Guide 12 give those paths. Do not copy native runtime state into the shared project.

Keep a fresh-session result for every supported surface and a single owner for each recurring job. A source-only route additionally records upload revision and delivery status. The project is ready for unattended use only after the actual scheduled environment has passed the required checks.

---

## Giving This Guide to an Assistant

You can hand this guide to Claude and ask it to walk you through any stage:

> "Read 18_END_TO_END_WALKTHROUGH.md and help me complete Stage 1. I'm starting from scratch."

> "Read 18_END_TO_END_WALKTHROUGH.md. I've done Stages 1-3 already. Walk me through Stage 4."

> "Read 18_END_TO_END_WALKTHROUGH.md and tell me which stage I should focus on next based on my current setup."

For the 20-minute minimal version, see [00_QUICKSTART.md](./00_QUICKSTART.md). For a one-page reference while building, see [CHEATSHEET.md](./CHEATSHEET.md). If something breaks, see [Guide 17 — Troubleshooting](./17_TROUBLESHOOTING.md).
