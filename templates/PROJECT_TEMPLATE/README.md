# Project Template — Setup Instructions

> A ready-to-copy folder structure for a Claude project with persistent context, knowledge management, and optional scheduled tasks.
> Based on the patterns in Guide 04 (Memory & Profile) and the TASK_TEMPLATE.

---

## What's in This Folder

```
PROJECT_TEMPLATE/
├── CLAUDE.md                    ← Project instructions: who you are, rules, file map
├── Profile/
│   ├── PROFILE_SUMMARY.md       ← Compact digest — read every session (≤ 50 lines)
│   └── PROFILE_detail.md        ← Full detail: people, projects, patterns, hypotheses
└── Knowledge/
    └── INDEX.md                 ← Index of topic files + template for creating new ones
```

**Created automatically as the project evolves:**

```
Knowledge/[TOPIC].md             ← One file per topic/project (created as needed)
[TaskName]-Task/                 ← Scheduled task folders (from TASK_TEMPLATE)
```

---

## How to Set Up a New Project

### Step 1 — Copy this folder

Copy `PROJECT_TEMPLATE/` to your project's location and rename it. Example:

```
Projects/
└── MyProject/
    ├── CLAUDE.md
    ├── Profile/
    └── Knowledge/
```

### Step 2 — Fill in CLAUDE.md

Open `CLAUDE.md` and replace all `[PLACEHOLDER]` text. Search for `[` to find them. Key sections:

- **About** — your name, role, timezone
- **Context** — 2–4 lines describing what this project covers
- **Critical Rules** — hard constraints only (things that override default behavior)
- **File Map** — update the table as you add or remove files

### Step 3 — Seed the Profile

Open `Profile/PROFILE_SUMMARY.md` and fill in:
- Who you are (2–3 lines)
- Active priorities (what matters most right now)
- Key contacts (people Claude will encounter in this project)

Leave the Open Action Items table empty — it will fill in naturally.

Open `Profile/PROFILE_detail.md` and add initial entries for anyone or any project you know Claude will need context on from day one.

### Step 4 — Open in Claude Code

Point Claude Code at your new project folder. Test with a question like: "What are my active priorities?" — Claude should read `PROFILE_SUMMARY.md` and answer from it.

### Step 5 — Add scheduled tasks (optional)

If this project needs automated runs, copy `TASK_TEMPLATE/` into your project folder for each task you want:

```
MyProject/
├── CLAUDE.md
├── Profile/
├── Knowledge/
└── DailyDigest-Task/            ← from TASK_TEMPLATE, renamed and filled in
```

See `TASK_TEMPLATE/README.md` for full task setup instructions.

---

## File Map & Lookup Patterns

| File | What it contains |
|------|-----------------|
| `Profile/PROFILE_SUMMARY.md` | Compact digest: who I am, active priorities, key contacts. **Read first for any task.** |
| `Profile/PROFILE_detail.md` | Full detail: people, projects, patterns, history |
| `Knowledge/INDEX.md` | Index of all topic knowledge files |
| `Knowledge/[TOPIC].md` | Per-topic file: key facts, decisions, current status, open questions |

Common lookups:
- **"What's the status of [project]?"** → `Knowledge/INDEX.md` → relevant `Knowledge/[TOPIC].md`
- **"Who is [person]?"** → `Profile/PROFILE_detail.md`
- **General context** → Always start with `Profile/PROFILE_SUMMARY.md`

> **Note:** For simple projects, Claude's built-in `.auto-memory/` system (see Guide 04) may be sufficient. Profile files are the richer option when you need structured, multi-file context.

---

## How the Profile Grows Over Time

**You seed it once; Claude maintains it from then on.**

After setup, Claude updates the profile files automatically when:
- It learns new facts about people, projects, or topics in conversation
- A task run surfaces new information
- You explicitly ask it to remember something

**You review and correct periodically.** The hypothesis system in `PROFILE_detail.md` lets Claude track things it's reasonably confident about but hasn't confirmed with you — check these occasionally and mark them `[CONFIRMED]` or delete them.

**Profile files split when they grow.** When `PROFILE_detail.md` exceeds ~150 lines, split it into `PROFILE_people.md`, `PROFILE_projects.md`, etc. Update the file map in `CLAUDE.md` accordingly.

---

## How Knowledge Files Work

The `Knowledge/` folder stores deep, structured context on specific topics — clients, projects, systems, decisions. It grows organically: Claude creates a new `Knowledge/[TOPIC].md` when a topic warrants its own file, and updates it as new facts emerge.

`Knowledge/INDEX.md` is the entry point — Claude reads it first to know what files exist, then opens only what's needed. This keeps token cost low on sessions that only touch one or two topics.

The template for a topic file is embedded in `Knowledge/INDEX.md`.

---

## Key Differences from TASK_TEMPLATE

| | PROJECT_TEMPLATE | TASK_TEMPLATE |
|--|-----------------|---------------|
| **What it is** | A project workspace — the container Claude operates in | A scheduled automated workflow |
| **When Claude runs** | On demand, during your sessions | On a schedule, automatically |
| **Primary file** | `CLAUDE.md` (always loaded) | `TASK.md` (loaded at each run) |
| **Memory** | Profile + Knowledge files | KNOWLEDGE_SUMMARY.md + IMPROVEMENTS.md |
| **Self-improvement** | Through your corrections in conversation | Through the Step 6 self-improvement loop |

A project can contain multiple tasks. Tasks operate within (and update) the project's profile and knowledge files.

---

## Giving This Template to Claude

To set up a new project from scratch:

> "Read `PROJECT_TEMPLATE/README.md`, copy the folder to [destination], rename it [project name], and fill in all the placeholders. I'll tell you what I need: [describe the project, domain, and any critical rules]."

To add a profile system to an existing project:

> "Read `04_MEMORY_AND_PROFILE.md` and create profile files for my project at [path]. Start with `PROFILE_SUMMARY.md` — ask me what you need to seed it correctly."

To add a scheduled task to an existing project:

> "Read `TASK_TEMPLATE/README.md` and create a new task in [path/to/project/] called [TaskName]-Task. The task should [describe what it does]."
