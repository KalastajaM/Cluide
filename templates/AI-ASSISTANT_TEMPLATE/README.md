# AI Assistant Template — Setup Instructions

> A turn-key personal business assistant: monitors work email, Teams, and calendar via the Microsoft 365 connector, produces a daily briefing with action items and draft messages, and maintains its own profile and knowledge base over time.
> Based on the patterns in Guides 04 (Memory & Profile), 06 (Task Efficiency), and 07 (Self-Improvement).

---

## What's in This Folder

```
AI-ASSISTANT_TEMPLATE/
├── CLAUDE.md                    ← Project instructions: identity, rules, file map
├── SYSTEM_STATUS.md             ← Health monitor for all scheduled tasks
├── bootstrap/
│   ├── SETUP.md                 ← START HERE — one-time setup guide
│   └── ...                      ← State-file stubs copied into place at setup
└── tasks/
    ├── daily/                   ← Daily briefing task (the core of the assistant)
    ├── midday/                  ← Mid-day urgent scan task
    ├── weekly-plan/             ← Friday weekly planner task
    ├── weekly-maint/            ← Monday weekly maintenance task
    └── maintenance/             ← On-demand maintenance procedure (not scheduled)
```

**Created during setup / by the tasks themselves:**

```
Knowledge/                       ← Topic knowledge files (created at setup)
Actions/                         ← Briefings and pending-action views (created at setup)
Profile/                         ← Populated by the daily task's first run — no pre-seeding needed
```

---

## How to Set Up

The setup entry point is **`bootstrap/SETUP.md`**. It covers the prerequisites (Cowork or Claude Code with scheduled tasks, the Microsoft 365 connector, optionally Atlassian), the `[YOUR_*]` placeholders to fill in, the state-file copy commands, and registering the scheduled tasks.

## The Four Scheduled Tasks

| Task | Folder | Schedule | What it does |
|------|--------|----------|--------------|
| Daily briefing | `tasks/daily/` | Every weekday morning | Analyzes email, Teams, calendar, and flagged items; updates profile and knowledge; regenerates the briefing and pending actions |
| Mid-day urgent scan | `tasks/midday/` | Weekday afternoons | Catches urgent items that arrived since the morning briefing |
| Weekly planner | `tasks/weekly-plan/` | Friday | Plans the coming week's focus blocks around the calendar |
| Weekly maintenance | `tasks/weekly-maint/` | Monday | Profile hygiene, hypothesis review, and system health checks |

A fifth, on-demand procedure (`tasks/maintenance/`) analyzes any of the four tasks and generates improvement proposals — run it manually when you want a maintenance review.

---

## Giving This Template to Claude

> "Read `AI-ASSISTANT_TEMPLATE/README.md` and `bootstrap/SETUP.md`, copy the template to [destination], and walk me through the setup: ask me for the `[YOUR_*]` placeholder values, run the bootstrap copy commands, and tell me which four tasks to register in Cowork."
