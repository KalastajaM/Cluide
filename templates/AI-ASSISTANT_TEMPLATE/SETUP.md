# AI Business Assistant — Setup Guide

A personal business assistant for Claude Cowork that monitors your email, Teams, and calendar, manages pending actions, maintains a live profile of your work context, and delivers a daily briefing. Four scheduled tasks work together: a daily morning briefing, a mid-day urgent scan, a Friday weekly planner, and a Monday maintenance run.

---

## Prerequisites

- **Claude Cowork** installed and running
- **Microsoft 365 connector** connected in Cowork (covers Outlook email, calendar, and Teams)
- **Atlassian connector** (optional — used to fetch Jira ticket context when emails reference them)

---

## Step 0 — Copy bootstrap files (fresh clone only)

If you cloned this repository from GitHub, the gitignored runtime files don't exist yet. Copy the stubs from `bootstrap/` before running any task:

```bash
# State files
cp bootstrap/pending_actions.json Assistant-Task/pending_actions.json
cp bootstrap/RUN_LOG.md Assistant-Task/RUN_LOG.md

# Profile files
mkdir -p Profile
cp bootstrap/PROFILE_SUMMARY.md Profile/PROFILE_SUMMARY.md
cp bootstrap/PROFILE_projects.md Profile/PROFILE_projects.md
cp bootstrap/PROFILE_patterns.md Profile/PROFILE_patterns.md
```

These stubs are empty placeholders — no content to fill in yet. The tasks will populate them on their first run. If the `bootstrap/` folder doesn't exist in your repo, skip this step — the tasks will create the files automatically on first run.

---

## Step 1 — Fill in your details

Open `CLAUDE.md` in this folder and replace every placeholder in the **About** and **Business Context** sections:

| Placeholder | Replace with |
|-------------|-------------|
| `[YOUR_NAME]` | Your full name |
| `[YOUR_ROLE]` | Your job title |
| `[YOUR_EMAIL]` | Your work email address |
| `[YOUR_TIMEZONE]` | Your timezone (e.g. `Europe/Helsinki`, `America/New_York`) |
| `[YOUR_COMPANY]` | Your company name |
| `[YOUR_M365_TENANT]` | Your M365 tenant domain (e.g. `yourcompany.com`) |

Then open each `*/TASK.md` file and replace the same placeholders. A full list of what appears in each file:

**All TASK.md files:**
- `[YOUR_NAME]` — your name, used in identity line and prose references
- `[YOUR_EMAIL]` — used in email search queries (sent items filter)
- `[YOUR_TIMEZONE]` — used in bash `TZ=` commands (e.g. `Europe/Helsinki`)
- `[YOUR_TIMEZONE_ABBR]` — short timezone label shown in outputs (e.g. `EET`, `CET`, `EST`)
- `[YOUR_UTC_OFFSET]` — UTC offset for display and time conversion notes (e.g. `UTC+2`, `UTC-5`)

**Assistant-Task/TASK.md additionally:**
- `[YOUR_COMPANY_KEYWORD]` — a single word used as the email search query (e.g. your company name or domain prefix). Avoid `*` — it causes a syntax error on O365 search.
- `[YOUR_ATLASSIAN_DOMAIN]` — your Atlassian cloud ID (e.g. `yourcompany.atlassian.net`). Remove the Atlassian section entirely if you don't use Jira.

**WeeklyPlanner-Task/TASK.md additionally:**
- `[YOUR_WORKING_HOURS]` — your typical working day, e.g. `09:00–17:30`
- `[YOUR_FOCUS_BLOCK]` — optional recurring focus/deep work block at the start of the day, or remove that paragraph

---

## Step 2 — Create your project folder

Create a folder on your computer where the assistant will store its files. For example:
```
Documents/AI-Assistant/
```

Copy all files and folders from this template into that folder, preserving the subfolder structure:
```
AI-Assistant/
├── CLAUDE.md
├── Assistant-Task/
├── UrgentScan-Task/
├── WeeklyMaintenance-Task/
└── WeeklyPlanner-Task/
```

The assistant will create the following folders automatically on its first runs — you do not need to create them:
```
Profile/        ← built up over time from email/Teams analysis
Knowledge/      ← per-topic files created as topics emerge
Actions/        ← daily briefing, pending actions, urgent scan output
WeekPlan/       ← weekly plan files (created by Friday task)
```

---

## Step 3 — Add project instructions to Cowork

1. Open Claude Cowork and select your `AI-Assistant` folder as the project folder.
2. In the top-right **Instructions** panel, paste the following:

```
Never send emails, post Teams messages, or create calendar events autonomously. Always propose drafts and wait for explicit confirmation before anything is sent or posted.

Be direct, no fluff. Prose only for conversational replies — no bullet points or headers unless the content genuinely calls for it. No emojis. Always label draft messages as Email or Teams.

Before answering questions or starting any substantive task, read the relevant files in this folder first. Start with Profile/PROFILE_SUMMARY.md for general context, then Actions/PENDING_ACTIONS.md for open items. Full file map and context is in CLAUDE.md.
```

---

## Step 4 — Create the four scheduled tasks

In Claude Cowork, open the **Scheduled** panel (sidebar) and create each task below. The **prompt** is what Claude receives each time the task fires — keep it short; the full instructions are in TASK.md.

---

### Task 1: Daily morning briefing

| Field | Value |
|-------|-------|
| **Task ID** | `business-assistant` |
| **Description** | Daily business assistant — profiles work context and generates a morning briefing |
| **Schedule** | Every day at your preferred morning time (e.g. `0 7 * * *` for 7:00 AM) |
| **Prompt** | See `Assistant-Task/Prompt.md` |

---

### Task 2: Mid-day urgent scan

| Field | Value |
|-------|-------|
| **Task ID** | `urgent-scan` |
| **Description** | Mid-day scan for urgent items since the morning briefing |
| **Schedule** | Weekdays at your preferred mid-day time (e.g. `0 13 * * 1-5` for 1:00 PM) |
| **Prompt** | See `UrgentScan-Task/Prompt.md` |

---

### Task 3: Friday weekly planner

| Field | Value |
|-------|-------|
| **Task ID** | `friday-weekly-plan` |
| **Description** | Weekly planner — proposes calendar blocks for next week based on open actions |
| **Schedule** | Fridays at your preferred time (e.g. `0 14 * * 5` for 2:00 PM) |
| **Prompt** | See `WeeklyPlanner-Task/Prompt.md` |

---

### Task 4: Monday maintenance

| Field | Value |
|-------|-------|
| **Task ID** | `weekly-maintenance` |
| **Description** | Monday cleanup — profile hygiene, knowledge audit, PA purge, hypothesis review |
| **Schedule** | Mondays, 30 minutes before your morning briefing (e.g. `30 6 * * 1` for 6:30 AM) |
| **Prompt** | See `WeeklyMaintenance-Task/Prompt.md` |

> **Note on cron times:** All cron expressions use your **local timezone** — enter times as they appear on your clock, not UTC.

---

## Step 5 — Pre-approve tool permissions

Scheduled tasks pause for permission approval the first time they try to use a connector. To avoid this on automated runs, **run each task once manually** after creating it (click "Run now" in the Scheduled panel). Approve any tool prompts that appear. These approvals are stored and applied automatically to all future runs.

Run them in this order:
1. `business-assistant` — needs O365 (email, calendar, Teams)
2. `urgent-scan` — needs O365 (email, Teams)
3. `weekly-maintenance` — file access only, no connectors
4. `friday-weekly-plan` — needs O365 (calendar)

---

## What to expect

**First morning briefing run:** The assistant has no profile yet, so it will start building one from scratch. Expect a longer first run as it reads your recent email and Teams history to establish baseline context. It will create the `Profile/`, `Knowledge/`, and `Actions/` folders and populate initial files.

**First week:** The profile improves noticeably run by run. By end of week one, the assistant should have a reasonable picture of your active projects, key contacts, and communication patterns.

**Ongoing:** The profile evolves continuously. The weekly maintenance task keeps it clean. The Friday planner gets more useful as the pending actions list fills in. The urgent scan is a safety net — on quiet days it will produce a "nothing urgent" file, which is the intended behaviour.

---

## Optional customisation

**Teams channel filters** (`Assistant-Task/TASK.md`, Step 3C): Add any Teams channels you want to permanently skip (e.g. noisy bot channels, social channels). Format: `Skip "[Channel name]" entirely.`

**Digest senders** (`Assistant-Task/IMPROVEMENTS.md`): As the assistant runs, it identifies high-volume automated senders and collapses them into single summary lines. You can pre-populate the Digest Senders table with known senders to skip from day one.

**Recurring calendar blocks** (`WeeklyPlanner-Task/TASK.md`, Step 2): The planner treats certain recurring blocks as infrastructure. Update the list to match your actual calendar conventions (focus time, lunch, end-of-day blocks).
