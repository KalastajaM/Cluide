# Weekly Planning Task

## File locations

This file lives at: `WeeklyPlanner-Task/TASK.md`

Referenced input files (relative to the project folder):
- `Actions/PENDING_ACTIONS.md` — all open action items with priority, deadline, and context
- `Actions/ACTIONS.md` — latest daily briefing and flagged priorities

Output files are saved to: `WeekPlan/`

---

## Step 1 — Read open actions

Read both of these files:

- `Actions/PENDING_ACTIONS.md` — all open action items with priority, deadline, and context
- `Actions/ACTIONS.md` — latest daily briefing and any flagged priorities

---

## Step 2 — Check the calendar

Use the Outlook calendar search tool to retrieve all events for **next Monday through Friday**. Convert all times to **[YOUR_TIMEZONE_ABBR] ([YOUR_UTC_OFFSET])**.

For each day, identify what meetings are booked and which gaps exist within working hours (`[YOUR_WORKING_HOURS]`). Treat the following recurring blocks as infrastructure, not scheduling targets:

- **[YOUR_FOCUS_BLOCK]** (e.g. Focus Time 07:00–08:30): available for deep work if a long block is needed
- **Lunch** (~midday): skip as a scheduling target
- **End of day block** (~[YOUR_DAY_END]): treat as the end of the productive day

*(Update the block descriptions above to match your actual recurring calendar conventions.)*

---

## Step 3 — Propose blocks

Match open actions to free slots using these principles:

**Small actions** — check if someone replied, send a single email, quick review — do NOT get a 30–60 min slot. Batch multiple small actions into one 15–20 min block, or note they can be handled during normal email flow.

**Substantive work items** — writing a plan or document, preparing a major meeting, deep analysis, modelling, cross-functional coordination — get a real 60–90 min block in a meaningful free slot.

**Reactive / waiting actions** — where [YOUR_NAME] is blocked on someone else — do not need a dedicated slot unless a deadline is approaching and escalation may be needed.

**Meeting preparation** — scan next week's calendar for meetings that typically require preparation: meetings where [YOUR_NAME] is the organizer, external calls, major reviews, and any meeting with a formal agenda or deliverable. Propose a prep block (30–60 min) earlier in the week for each such meeting. Light recurring syncs generally do not need prep blocks unless there is a specific agenda item.

**Avoid Fridays** unless there is a hard deadline — they are typically packed with recurring meetings.

For each proposed block, state:
- Day and time ([YOUR_TIMEZONE_ABBR])
- Duration
- Purpose (which action or work item)
- What specifically to do in that slot

---

## Step 4 — Save the plan as files

Determine the Monday date of the coming week and save two files to `WeekPlan/`:

1. **`YYYY-MM-DD_weekplan.md`** — clean markdown version of the full plan (open actions table, proposed blocks, notes).
2. **`YYYY-MM-DD_weekplan.html`** — calendar-booking-friendly HTML version. Use a five-column layout (one column per day, Mon–Fri). For each day show: existing meetings as light grey blocks, and proposed work blocks as coloured cards (colour-coded by type: deep work = blue, quick actions = green, meeting prep = amber, conditional = dashed grey). Each proposed block card must show: start time, end time, duration, title, a brief description, and a **📅 Add to Outlook** button. The button uses a JavaScript Blob to generate and download a `.ics` file (iCalendar format) for that block when clicked. Use UTC times in the `.ics` (convert from local time by subtracting [YOUR_UTC_OFFSET_HOURS] hours). Include a SUMMARY, DTSTART, DTEND, DESCRIPTION, and UID in each VEVENT. Friday should be visually muted with a note that no blocks are scheduled unless a hard deadline forces one. Include a legend and an open actions table at the top.

Use `YYYY-MM-DD` = the date of the coming Monday.

---

## Step 5 — Present the plan in chat

Output the same proposed blocks as a clean list in the conversation. Be direct and practical — no filler. Close with links to the two saved files and a note that calendar creation is not automated.

Do not send emails, Teams messages, or create calendar events autonomously.

---

## Step 6 — Self-Improvement

Read `IMPROVEMENTS.md`. Apply any `[APPROVED]` proposals. Then:

1. **Feedback signals:** Did the user edit or discard last week's plan? Extract the lesson. Did a proposed block type consistently get ignored? Recalibrate.
2. **Refactor check:** If `runs_since_last_refactor` ≥ threshold, review TASK.md for dead rules or unclear steps.
3. **Apply or propose:** Minor fixes (typo, wrong format) → apply directly. Structural changes → add to `IMPROVEMENTS.md` as a proposal.
4. **Update IMPROVEMENTS.md:** Increment counters, add fixes/proposals.

---

## Step 7 — Append Run Log

Append to `RUN_LOG.md`. Keep last 3 runs in full; compress older to 1-line summaries.

```markdown
### Run [N] — YYYY-MM-DD
- **Open actions reviewed:** [N]
- **Calendar events scanned:** [N]
- **Blocks proposed:** [N]
- **Improvements:** applied [N] / proposed [N]
```

---

## Output format

```
**Monday [Date] — HH:MM–HH:MM (N min)**
*Quick actions: [PA-XXXX] + [PA-YYYY]*
Brief description of what to do.

**Tuesday [Date] — HH:MM–HH:MM (N min)**
*[Topic] — deep work*
Brief description.
```
