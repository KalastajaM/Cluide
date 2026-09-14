# Quickstart: Your First Working Setup

Build a small assistant that plans your day from information you supply. Use Claude, ChatGPT, or Codex; the same instructions and sample input should produce the same useful outcome. No calendar connection, native memory, or scheduled job is required.

## Before You Start

Choose the surface you will actually use:

| Surface | Where your project lives | How to supply instructions |
|---|---|---|
| Claude Code | An ordinary project folder | Root `CLAUDE.md` imports the shared `AGENTS.md` |
| Codex | An ordinary project folder opened as the workspace | Root `AGENTS.md` |
| Claude project / Cowork | Project sources or a connected folder | Project instructions explicitly ask it to read the supplied shared policy |
| ChatGPT project | Uploaded or connected project sources | Project instructions explicitly ask it to read the supplied shared policy |

For the last two, access to a source is not proof of write access to the original folder. The [official instruction and project references in Guide 35](./35_DUAL_PLATFORM_PROJECTS.md) explain the differences. Use a text editor for local files, or ask the assistant to produce files you can add to the project.

## Step 1: Create the Shared Policy

Create a folder named `My Assistant`. Add `AGENTS.md` at its root, replacing the placeholders:

```markdown
# My Assistant

## Purpose
Help me organise work from the information I supply.

## Who I Am
- Name: [your name]
- Role: [your role]
- Timezone: [your timezone, e.g. Europe/Helsinki]

## Working Rules
- Use concise English unless I write in another language.
- Distinguish supplied facts from assumptions; do not invent calendar access.
- Draft a plan when I ask. Do not send messages or create events from a planning request.
- Read plan-my-day/SKILL.md when I ask to plan my day.
- Tell me whether output was saved to my project or only drafted in chat.
```

For Claude Code, add a root `CLAUDE.md`:

```markdown
# Claude Entry Point
@AGENTS.md

If this interface does not resolve imports, read AGENTS.md before working.
```

For a conversational project, supply `AGENTS.md` as a project source and put this in its project instructions:

> Read the supplied AGENTS.md before working. If it is unavailable, tell me what is missing. Follow the shared rules and use only information and tools available in this conversation.

Keep a note of the source revision or upload date. Replacing a repository file does not automatically replace an uploaded copy. Start a new session after changing the policy and verify the rules it received.

## Step 2: Create Your First Reusable Workflow

Create `plan-my-day/SKILL.md` beside `AGENTS.md`. This starter uses an explicit read instruction, so it works even before a native skill is installed.

````markdown
---
name: plan-my-day
description: Plan a day from supplied tasks, meetings, deadlines, and available hours. Use for "plan my day" or "prioritise today's work"; not for booking events or sending messages.
---

## Workflow
1. Read the supplied tasks, fixed meetings, deadlines, and available hours.
2. Keep fixed meetings at their stated times. Identify the 1–3 priorities.
3. Fit focus work around meetings. Do not invent duration or availability;
   label suggested durations and flag overload.
4. Group short tasks together and defer lower-priority work if needed.
5. Return the plan below. Do not create events or send messages.

## Output
```text
Today's Plan — [supplied date, or date unspecified]
Must do: [highest priorities]
Fixed meetings: [times as supplied]
Focus blocks: [suggested work and times, if hours are known]
Quick tasks: [short items]
Defer: [items that can wait]
Assumptions or conflicts: [only if needed]
```

## Edge Cases
- With no available hours, order priorities without inventing times.
- With 1–2 tasks, keep the plan brief.
- When asked to book or send, explain that this workflow only drafts;
  use a separately authorised tool workflow for the external action.
````

For ChatGPT or Claude project sources, supply this file too. For local work, keep it in the folder. Native installation is optional: [Guide 03](./03_SKILLS.md) gives separately scoped installation steps. Do not assume a folder uploaded as a source is an installed skill.

## Step 3: Test a Fresh Session

First ask:

> Which shared policy did you read? What should happen if I ask you to book a meeting?

Then use this fixed input on each surface you intend to support:

> Read plan-my-day/SKILL.md and plan my day for 14 September 2026. I work 09:00–17:00 Europe/Helsinki. Fixed meetings are 10:00–10:30 and 15:00–15:15. I need to reply to three client emails and draft a proposal due tomorrow. Draft only; don't contact anyone or create events.

Check that both meetings retain their times, the proposal is prioritised, suggested durations are labelled, and no external actions occur. Repeat with “I have two tasks but no available hours”; the assistant should avoid invented time slots.

Record `surface / model if shown / source revision / date / pass or fail / observed result`. A written check is not a recorded pass. If you cannot run a surface, mark it **untested**. The project template’s behavior cases (`templates/PROJECT_TEMPLATE/tests/behaviour/README.md` in the Cluide checkout) extend this check to source freshness, unavailable tools, output delivery, handoffs, and schedules.

## Step 4 (Optional): Schedule Only After the Manual Run Works

Use `tasks/setup-scheduled-task.md` to choose an available scheduler. First provide all inputs in a file or a connected source that the scheduled run can actually read; an unattended task cannot rely on you answering an interview midway through its run.

For a weekly planner, record a stable job ID such as `weekly-plan`, one scheduler owner, your timezone, the weekly time slot, the input source, and the output destination. Check existing registrations on both platforms before adding one. Register on one platform only, verify the next run, and record its native registration ID. If no scheduler is available, keep the workflow manual. Merely creating `TASK.md` does not register anything.

## What to Build Next

| If you want to… | Read next |
|---|---|
| Improve standing instructions | [01 — Project Instructions](./01_PROJECT_INSTRUCTIONS.md) |
| Install the workflow as a native skill | [03 — Skills](./03_SKILLS.md) |
| Keep shared knowledge between sessions | [04 — Memory & Profile](./04_MEMORY_AND_PROFILE.md) |
| Connect email or calendar tools | [05 — MCP Servers](./05_MCP_SERVERS.md) |
| Let recurring work improve from evidence | [07 — Task Learning](./07_TASK_LEARNING_GUIDE.md) |
| Move from another assistant | [34 — Importing](./34_IMPORTING_FROM_OTHER_ASSISTANTS.md) |
| Keep both platforms working on one project | [35 — Dual-Platform Projects](./35_DUAL_PLATFORM_PROJECTS.md) |

## Troubleshooting

If rules are missing, check the current folder or supplied source revision, then start a fresh session. If a native skill does not trigger, explicitly ask it to read the workflow first; if that works, investigate installation and discovery using Guide 03. If the assistant cannot read a local folder, upload the required sources or use a local workspace. [Guide 17](./17_TROUBLESHOOTING.md) covers the full diagnostic path.

## Giving This to an Assistant

> Read 00_QUICKSTART.md and build its small planning setup for my chosen surface. Ask only for missing identity, timezone, and preference details. Create the files or provide them for upload, then walk through the fresh-session checks. Report what was actually tested.
