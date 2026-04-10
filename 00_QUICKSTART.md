# Quickstart: Your First Working Setup in 20 Minutes

*Last reviewed: April 2026*

> Build something real before reading anything else. This guide walks you through creating a working CLAUDE.md and your first skill — step by step, with the exact files you need. You do not need to read the other guides first.

> **What you'll build:** A personal assistant that knows who you are, and a skill that helps you plan your day. No external tools required. Everything runs in a plain text editor and Cowork.

---

## Before You Start

You need two things:
1. **A text editor** — Windows Notepad, macOS TextEdit, or VS Code all work. You are creating plain `.md` text files.
2. **Access to Cowork** — the Claude interface where you run your assistant.

**Where do the files live?**

Claude reads files from a special folder on your computer:
- Windows: `C:\Users\[your username]\.claude\`
- Mac/Linux: `~/.claude/`

If this folder doesn't exist yet, create it. Everything you build goes inside it.

---

## Step 1: Create Your CLAUDE.md (5 minutes)

`CLAUDE.md` is the instruction file Claude loads at the start of every session. It tells Claude who you are and how you want it to behave.

**Create this file at:** `.claude/CLAUDE.md`

Here is a starting template — replace the placeholders with your own details:

```markdown
## Who I Am
- I am [your name], working as [your role] at [your organisation]
- Based in [your city], timezone [your timezone, e.g. Europe/Helsinki]
- I communicate primarily in [your language]; respond in English unless I write in another language

## How I Work
- I prefer concise, structured responses — use bullet points and headers
- When I ask for a draft (email, message, document), produce it directly without commentary
- When something is unclear, ask one clarifying question before proceeding

## Standing Rules
- Never add unnecessary caveats or disclaimers
- If you are unsure about a fact, say so rather than guessing
```

**Keep it short.** 15–25 lines is ideal. Every line you add is loaded into every session — make each one count.

> **Tip:** The more specific you are, the better the results. "I work in cybersecurity sales, my main contacts are IT managers and CISOs" is more useful than "I work in tech."

---

## Step 2: Create Your First Skill (10 minutes)

A skill is a reusable instruction set for a specific task. Once it exists, you trigger it by describing what you need — Claude recognises the description and follows the skill instructions automatically.

**You will build:** A "plan my day" skill that takes your list of priorities and returns a structured daily schedule.

**First, create the folder:**
```
.claude/skills/plan-my-day/
```

**Then create the skill file at:** `.claude/skills/plan-my-day/SKILL.md`

```markdown
---
name: plan-my-day
description: >
  Use this skill when the user wants to plan their day, prioritise tasks,
  structure their schedule, or organise what they need to get done today.
  Triggers on phrases like "help me plan today", "what should I focus on",
  "let's structure my day", or "I need to prioritise".
---

## Purpose
Help the user produce a clear, actionable daily plan from a list of tasks,
meetings, and priorities. The output is a structured schedule they can
follow for the rest of the day.

## Workflow
1. Read everything the user has provided: tasks, meetings, deadlines, and
   available hours if mentioned
2. Identify the 1–3 most important items (time-sensitive or high-impact)
3. Group remaining tasks into: Focus blocks, Quick tasks (<15 min), and
   Defer (can wait until tomorrow)
4. Produce the plan in the output format below

## Output Format
```
## Today's Plan — [Day, Date]

### Must Do
- [Top priority item]
- [Second priority if applicable]

### Focus Blocks
- [Time or slot]: [Task]
- [Time or slot]: [Task]

### Quick Tasks
- [Task] (~10 min)
- [Task] (~5 min)

### Defer
- [Task] → tomorrow or [specific date]

### Notes
[Any observations about workload, conflicts, or suggestions]
```

## Edge Cases
- If the user provides no time information, skip time slots and organise
  by priority only
- If the list is very short (1–2 items), skip grouping and just confirm
  the priorities with a brief comment
- If there are more than 10 items, flag potential overload and suggest
  which items to move to tomorrow
```

---

## Step 3: Test It in Cowork (5 minutes)

Open a **new Cowork conversation** and try this:

> "Help me plan my day. I have: a 10am team meeting, three client emails to reply to, a proposal draft that's due tomorrow, and a quick call at 3pm."

Claude should recognise the trigger phrases and apply your skill automatically. You will see the structured output format from your SKILL.md.

**If it doesn't work:**
- Check that the skill file is at exactly `.claude/skills/plan-my-day/SKILL.md`
- Make sure the file was saved as plain text (not `.md.txt` or a Word document)
- Start a fresh Cowork conversation — skill changes only take effect in new sessions
- See [Guide 14 — Troubleshooting](./14_TROUBLESHOOTING.md) for more help

---

## Step 4 (Optional): Add a Scheduled Task

A scheduled task runs automatically — without you asking — on a schedule you define. This is optional for your first setup; you can add it later.

Here is the minimal structure for a weekly planning task. This example runs every Monday morning and asks you to review the week ahead:

**Create the folder:**
```
.claude/tasks/weekly-planner/
```

**Create the task file at:** `.claude/tasks/weekly-planner/TASK.md`

```markdown
# Weekly Planner Task

## Purpose
Produce a Monday morning summary to start the week focused.
Run this task every Monday before 9am.

## Steps
1. Check today's date and calculate the current week number
2. Ask the user: "What are your top 3 priorities for this week?"
3. Produce a weekly plan in the same format as the plan-my-day skill,
   but structured by day (Mon–Fri) rather than time blocks

## Output
Write the weekly plan as a clear message the user can read and act on.
Save a one-line summary to LAST_RUN.md with the date and top priority.

## Run log
- Read LAST_RUN.md at the start of each run to see when it last ran
- Write LAST_RUN.md at the end of each run with the date and a one-line summary
```

**To schedule it:** Open Cowork, go to your scheduled tasks panel, and create a new task pointing at this file. Set it to run every Monday at your preferred time.

---

## What to Build Next

You now have the foundation. Here is the natural next step for each direction:

| If you want to... | Read next |
|---|---|
| Make the assistant smarter about who you are | [Guide 03 — Memory & Profile](./03_MEMORY_AND_PROFILE.md) |
| Build skills for email, calendar, and Teams | [Guide 08 — MCP Servers](./08_MCP_SERVERS.md) |
| Create more skills (better descriptions, edge cases) | [Guide 02 — Skills](./02_SKILLS.md) |
| Make the assistant learn from each task run | [Guide 05 — Task Self-Improvement](./05_TASK_LEARNING_GUIDE.md) |
| See all best practices in one place | [Guide 07 — Best Practices](./07_BEST_PRACTICES.md) |

---

## Troubleshooting

**"Claude isn't applying my CLAUDE.md"**
Make sure the file is at `.claude/CLAUDE.md` (not inside a project subfolder). Start a fresh Cowork conversation — CLAUDE.md changes take effect in new sessions only.

**"The skill isn't triggering"**
The description field in the skill frontmatter controls when it triggers. Make sure it includes the phrases you actually use. If you say "can you plan my day?" and the description only mentions "organise tasks", Claude may not match them. Edit the description to include your natural phrasing.

**"The output format is wrong"**
The output format section in SKILL.md should contain a code block showing exactly what the output should look like — including headers, bullet style, and field names. Vague descriptions like "produce a structured plan" are much weaker than a concrete template.

**Something else isn't working?**
See [Guide 14 — Troubleshooting](./14_TROUBLESHOOTING.md) for a full problem-by-problem guide.

---

## Giving This to Claude

You can ask Claude to build this setup for you instead of doing it manually:

> "Read 00_QUICKSTART.md. Build the CLAUDE.md and plan-my-day skill it describes for me. Ask me for my name, role, timezone, and any preferences before writing the files."

> "I followed 00_QUICKSTART.md but my skill isn't triggering. Here is my SKILL.md: [paste it]. What's wrong?"
