# Weekly Planning Task

## File locations

This file lives at: `weekly-plan/TASK.md`

Referenced input files (relative to the project folder):
- `Actions/PENDING_ACTIONS.md` — all open action items with priority, deadline, and context
- `Actions/ACTIONS.md` — latest daily briefing and flagged priorities

Output files are saved to: `Actions/WeekPlans/`

---

## Step 0A — Pre-Run Git Snapshot

```bash
cd "[PROJECT_ROOT]"
git add -A
git diff --cached --quiet || git commit -m "pre-run: friday-weekly-plan $(date -u +%Y-%m-%d)"
```

Captures state entering this run. Skip silently if no changes. Do not block if git fails.

---

## Step 0B — Check for duplicate run

Before doing any work, check whether `Actions/WeekPlans/` already contains a file matching the coming Monday's date (format: `YYYY-MM-DD_weekplan.md`). If a matching file exists, skip to Step 5 and present the existing plan with a note that it was already generated today.

---

## Step 0C — Bootstrap Check

Before reading state files, verify they exist. For each missing file, copy from `bootstrap/`:

- `RUN_LOG.md` → copy from `../../bootstrap/weekly-plan/RUN_LOG.md`
- `IMPROVEMENTS.md` → copy from `../../bootstrap/weekly-plan/IMPROVEMENTS.md`
- `ISSUES_LOG.md` → copy from `../../bootstrap/weekly-plan/ISSUES_LOG.md`

If bootstrap files are also missing, create the file with empty structure (see `bootstrap/` for schemas). Note any bootstrapped files in this run's RUN_LOG entry: "Bootstrap: first run — [files] initialised."

---

## Step 1 — Read open actions

Read both of these files:

- `Actions/PENDING_ACTIONS.md` — all open action items with priority, deadline, and context
- `Actions/ACTIONS.md` — latest daily briefing and any flagged priorities

---

## Step 2 — Check the calendar

Use the Outlook calendar search tool to retrieve all events for **next Monday through Friday**. Convert all times to **[YOUR_TIMEZONE_ABBR] ([YOUR_UTC_OFFSET])**.

For each day, identify what meetings are booked and which gaps exist within working hours. Treat the following recurring blocks as infrastructure, not scheduling targets:

- **Focus Time** (07:00–08:30): available for deep work if a long block is needed
- **Lunch** (~11:30–12:00): skip as a scheduling target
- **Finish Day / Finish Week** (~16:00): treat as the end of the productive day

---

## Step 3 — Propose blocks

Match open actions to free slots using these principles:

**Small actions** — check if someone replied, send a single email, quick review — do NOT get a 30–60 min slot. Batch multiple small actions into one 15–20 min block, or note they can be handled during normal email flow.

**Substantive work items** — writing a plan or document, preparing a major meeting, deep analysis, modelling, cross-functional coordination — get a real 60–90 min block in a meaningful free slot.

**Reactive / waiting actions** — where [USER] is blocked on someone else — do not need a dedicated slot unless a deadline is approaching and escalation may be needed.

**Meeting preparation** — scan next week's calendar for meetings that need a prep block. Default to no prep block unless at least one of these is true: (a) [USER] is presenting or has a deliverable due, (b) it is a SteerCo or equivalent formal governance meeting, (c) it is a first/one-off external call with a clear agenda. Light recurring syncs and 1:1s do not get prep blocks.

**Avoid Fridays** unless there is a hard deadline — they are typically packed with recurring meetings.

For each proposed block, state:
- Day and time ([YOUR_TIMEZONE_ABBR])
- Duration
- Purpose (which action or work item)
- What specifically to do in that slot

---

## Step 4 — Save the plan as files

Determine the Monday date of the coming week (format: `YYYY-MM-DD`).

### 4a — Markdown file

Save `Actions/WeekPlans/YYYY-MM-DD_weekplan.md` — clean markdown version of the full plan: open actions table, proposed blocks, notes.

### 4b — HTML file (scripted)

Build a JSON data file at `Actions/WeekPlans/YYYY-MM-DD_plan_data.json` using this schema:

```json
{
  "monday_date": "YYYY-MM-DD",
  "week_label": "Week of DD Month YYYY",
  "proposed_blocks": [
    {
      "day": "monday",
      "date": "YYYY-MM-DD",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "duration_min": 90,
      "title": "...",
      "description": "...",
      "type": "deep",
      "action_ids": ["PA-XXXX"]
    }
  ],
  "existing_meetings": {
    "monday": [{"start_time": "HH:MM", "end_time": "HH:MM", "title": "..."}],
    "tuesday": [], "wednesday": [], "thursday": [], "friday": []
  },
  "open_actions": [
    {"id": "PA-XXXX", "title": "...", "priority": "SOON", "deadline": "YYYY-MM-DD"}
  ]
}
```

Block `type` values: `deep` (blue), `quick` (green), `prep` (amber), `conditional` (dashed grey).

Then run:

```bash
python3 tasks/weekly-plan/generate_weekplan_html.py \
  --input Actions/WeekPlans/YYYY-MM-DD_plan_data.json \
  --output Actions/WeekPlans/YYYY-MM-DD_weekplan.html
```

If the script fails, fall back to composing the HTML directly (same spec as before) and log the error in `weekly-plan/RUN_LOG.md`.

**Issue logging:** If any issue was encountered during this run (script failure, calendar data gap, deduplication ambiguity, connector anomaly), append one entry to `weekly-plan/ISSUES_LOG.md` using the standard format. If no issues: skip.

**SYSTEM_STATUS.md update:** After saving plan files, update `../../SYSTEM_STATUS.md` — targeted Edit of the `## weekly-plan` section only:

```
## weekly-plan
Last run: YYYY-MM-DD HH:MM [YOUR_TIMEZONE_ABBR] | Result: OK
Last 3: [this result] [previous] [previous]
```

Use `OK` if the run completed without errors; `FAIL` if a critical error (script failure, calendar data missing) occurred. Edit **only** the `## weekly-plan` section.

---

## Step 4C — Post-Run Git Commit

```bash
cd "[PROJECT_ROOT]"
git add -A
git diff --cached --quiet || git commit -m "run: friday-weekly-plan $(date -u +%Y-%m-%d) — plan saved"
```

Captures the weekplan markdown, JSON data file, HTML output, RUN_LOG.md, SYSTEM_STATUS.md. Do not block if git fails.

---

## Step 5 — Present the plan in chat

Output the proposed blocks as a clean list in the conversation. Be direct and practical — no filler. Close with links to the two saved files and a note that calendar creation is not automated.

Do not send emails, Teams messages, or create calendar events autonomously.

---

## Output format

```
**Monday 30 March — 10:20–10:40 (20 min)**
*Quick actions: [PA-XXXX] + [PA-YYYY]*
Brief description of what to do.

**Tuesday 31 March — 08:30–10:00 (90 min)**
*[Topic] — deep work*
Brief description.
```
