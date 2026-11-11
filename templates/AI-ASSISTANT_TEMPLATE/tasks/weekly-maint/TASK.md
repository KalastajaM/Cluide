# Weekly Maintenance — Run Procedure

**Before any run:** read local `AGENTS.md`, `../../AGENTS.md` and
`../../PLATFORM_SETUP.md`. Verify required tools, source freshness, the active job owner,
and the shared duplicate-run/write guard before state changes. If unavailable, stop dependent
work and report the exact gap. Do not fabricate a successful fetch, saved output or registration.
Tool names below describe the required operation; bind them to this session's verified tools.


## Scope

Works only with **existing files**. Does NOT fetch email, Teams, or calendar data. Does NOT generate ACTIONS.md or ACTIONS.html.

---

## Run Procedure

### Step 0A: Pre-Run Git Snapshot

```bash
cd "[PROJECT_ROOT]"
git add -A
git diff --cached --quiet || git commit -m "pre-run: weekly-maintenance $(date -u +%Y-%m-%d)"
git rev-parse HEAD
```

Commits task-definition edits only: runtime state is git-ignored and not captured (see `../../bootstrap/SETUP.md` §Git snapshots and backup). Record the printed hash as `Restore commit` in this run's RUN_LOG entry. Skip silently if no changes. Do not block if git fails.

---

### Step 0B: Bootstrap Check

Before reading state files, verify they exist. For each missing file, copy from `bootstrap/`:

- `LAST_RUN.txt` → copy from `../../bootstrap/weekly-maint/LAST_RUN.txt`
- `RUN_LOG.md` → copy from `../../bootstrap/weekly-maint/RUN_LOG.md`
- `IMPROVEMENTS.md` → copy from `../../bootstrap/weekly-maint/IMPROVEMENTS.md`
- `ISSUES_LOG.md` → copy from `../../bootstrap/weekly-maint/ISSUES_LOG.md`

If bootstrap files are also missing, create the file with empty structure (see `bootstrap/` for schemas). Create `../../Actions/` and `../../Knowledge/` if absent, and copy `../../bootstrap/knowledge/INDEX.md` to `../../Knowledge/INDEX.md` if absent. Note any bootstrapped files in MAINTENANCE_REPORT.md: "Bootstrap: first run — [files] initialised."

---

### Step 0C: Duplicate-Run Guard

Read `LAST_RUN.txt`. If it is empty (first run), continue. If the timestamp is less than 12 hours ago (compare against current UTC time via bash), write a single-line note to `../../Actions/MAINTENANCE_REPORT.md` — "Maintenance skipped: already ran at [timestamp]" — and exit. Do not proceed to Step 1.

---

### Step 1: Read State

1. `LAST_RUN.txt` — note when maintenance last ran
2. `../../Profile/PROFILE_SUMMARY.md`
3. `../../Profile/PROFILE_identity.md`
4. `../../Profile/PROFILE_clients.md`
5. `../../Profile/PROFILE_hypotheses.md`
6. `../../Knowledge/INDEX.md`
7. `../daily/pending_actions.json`
8. `../daily/CONFIG.md` — thresholds (`PA_STALENESS_DAYS`, `SNOOZE_WAKE_DAYS`, `RESOLVED_KEEP_DAYS`, `RUN_LOG_KEEP_RUNS`); use these names, not fixed numbers

Do NOT read full knowledge topic files yet — use INDEX.md metadata to decide which (if any) to open.

---

### Step 1A: Capture Run Timestamp

```bash
TZ=[YOUR_TIMEZONE] date +"%Y-%m-%d %H:%M %Z"
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

Store local time as **`MAINT_TIME_LOCAL`**. Store UTC as **`MAINT_START_UTC`** (written to `LAST_RUN.txt` in Step 7).

---

### Step 2: Profile Hygiene

**Stale contacts (`PROFILE_identity.md`):** Flag any contact with `[updated: YYYY-MM]` older than 3 months as `[POSSIBLY INACTIVE]`. Do not delete. Note names in the report.

**Closed deals/projects (`PROFILE_clients.md`):** Identify entries with status CLOSED, COMPLETED, or LOST. Move them to `../../Profile/PROFILE_archive.md`. Update the clients file. Note what was archived.

**PROFILE_SUMMARY.md accuracy:** Compare the summary against the current profile files. If a priority, deal status, or key contact has materially changed but the summary hasn't been updated, rewrite the affected section. Full Write only if changes are material; otherwise note "no update needed."

**PROFILE_patterns.md:** Check the `Last updated` timestamp at the top of the file. If > 6 weeks old, note in the report that it may be stale — do not edit the file itself.

---

### Step 3: Knowledge Base Audit

Using `../../Knowledge/INDEX.md` metadata only — each line carries `STATUS · last updated YYYY-MM-DD`; do not read every topic file:

- **Stale ACTIVE topics:** `Last updated` > 45 days → flag in report as potentially stale.
- **Topics to close:** If the topic metadata clearly indicates a project is complete or cancelled, read that file and update its status to CLOSED or ON HOLD. Update INDEX.md.
- **Open questions:** Note any topic with open questions that look likely resolved based on current context. Do not auto-resolve — surface in report.
- **Long-open questions:** For any topic where the open questions section has entries older than 30 days (infer from `Last updated` date as a proxy, or from explicit dates if present), flag them as `[LONG OPEN]` in the maintenance report. Do not edit the topic file — surface for [USER]'s review only.

Read a topic file only if its metadata indicates it needs a status change.

---

### Step 4: Pending Actions Cleanup

Working from `../daily/pending_actions.json` (file shape: `../daily/TASK_REFERENCE.md §PA-Schema`):

**Purge old resolved:** Remove `resolved_last_30_days` entries (status RESOLVED, SUPERSEDED or EXPIRED alike) whose `resolved_date` is more than `RESOLVED_KEEP_DAYS` before today — the same retention as daily Step 5D-1. Overflow beyond `RESOLVED_INLINE_CAP` stays daily's job.

**Snooze reminders:** Any `snoozed` entry whose `reminder_date` is within `SNOOZE_WAKE_DAYS` of today → move back to `open` (same rule as daily Step 5D).

**Deadline escalation:** Any PA with `priority: SOON` and `deadline` within 2 calendar days → upgrade to `priority: URGENT`. Note IDs in report.

**Stale flag:** Any PA open `PA_STALENESS_DAYS`+ days with no `last_reviewed` update → set `"stale": true` if not already set.

**Size check:** After purging, if total entry count still exceeds 100, log a warning in the report: "pending_actions.json has N entries — may need manual review."

Write back `pending_actions.json` in a single Write call if any changes were made, then regenerate the view so it matches:

```bash
python3 "[PROJECT_ROOT]/tasks/daily/generate_pending_actions_md.py"
```

If it fails, note it in the report and continue — the next daily run regenerates the view.

---

### Step 5: Hypothesis Review

Working from `../../Profile/PROFILE_hypotheses.md`:

- Any `[HYPOTHESIS]` with `Last checked` > 6 months → change to `[POSSIBLY OUTDATED]`.
- Any `[HYPOTHESIS]` with `Confidence: MEDIUM` → add to report as a candidate for confirmation.

Write back only if changes were made (full Write).

---

### Step 6: Generate MAINTENANCE_REPORT.md

Write to `../../Actions/MAINTENANCE_REPORT.md`. Overwrite each run.

```markdown
# Weekly Maintenance Report — YYYY-MM-DD HH:MM [YOUR_TIMEZONE_ABBR]

## Summary
[2–3 sentences: what was cleaned, what was flagged, whether anything needs [USER]'s attention.]

## Profile
- Stale contacts flagged: N — [names or "none"]
- Deals/projects archived: N — [names or "none"]
- PROFILE_SUMMARY.md: [updated / no update needed]
- PROFILE_patterns.md: [stale — last updated YYYY-MM / current]

## Knowledge Base
- Stale ACTIVE topics (>45 days): N — [names or "none"]
- Topics closed/put on hold: N — [names or "none"]
- Open questions to review: [brief note or "none"]
- Long-open questions (>30 days): [topic names and question summaries, or "none"]

## Pending Actions
- Old resolved entries purged: N
- Snoozed PAs returned to open: N — [IDs or "none"]
- Priority escalations (SOON→URGENT): N — [IDs or "none"]
- Stale PAs flagged: N — [IDs or "none"]
- Size warning: [note if > 100 entries, otherwise omit]

## Hypotheses
- Downgraded to POSSIBLY OUTDATED: N — [brief descriptions or "none"]
- Candidates for confirmation: [list or "none"]

## Needs Attention
[Items requiring [USER]'s input or decision. If none: "Nothing requires action."]
```

---

### Step 7: Write LAST_RUN.txt and Append to RUN_LOG.md

Write `MAINT_START_UTC` to `weekly-maint/LAST_RUN.txt` as a single line (overwrite).

Increment `runs_total` in `weekly-maint/IMPROVEMENTS.md` (targeted Edit of the counter line), then append to `weekly-maint/RUN_LOG.md` with that value as `N` (use the same `N` in any ISSUES_LOG entry). Retention: keep the last `RUN_LOG_KEEP_RUNS` entries in full; once the log exceeds ~30 entries, move older ones to `weekly-maint/RUN_LOG_ARCHIVE.md`.

```markdown
## YYYY-MM-DD Run #N
- **Local time:** HH:MM [YOUR_TIMEZONE_ABBR]
- **Profile:** N contacts flagged | N archived
- **Knowledge:** N stale topics | N closed
- **PA:** N purged | N escalated | N snoozed→open | N stale flagged
- **Hypotheses:** N downgraded
- **Tool calls:** N
- **Tokens (est.):** ~XK input, ~YK output
- **Restore commit:** [hash printed by Step 0A, or "no repo"]
```

**Issue logging:** If any operational issue was encountered during this run (unreadable file, unexpected data, ambiguity requiring a judgment call, workaround applied), append one entry to `weekly-maint/ISSUES_LOG.md` using the standard format. If no issues: skip.

**SYSTEM_STATUS.md update:** After writing RUN_LOG, update `../../SYSTEM_STATUS.md` — targeted Edit of the `## weekly-maint` section only:

```
## weekly-maint
Last run: YYYY-MM-DD HH:MM [YOUR_TIMEZONE_ABBR] | Result: OK
Last 3: [this result] [previous] [previous]
```

Use `OK` if the run completed without errors; `FAIL` if a critical error occurred. Edit **only** the `## weekly-maint` section.

---

### Step 8: Post-Run Git Commit

```bash
cd "[PROJECT_ROOT]"
git add -A
git diff --cached --quiet || git commit -m "run: weekly-maintenance $(date -u +%Y-%m-%d) — maintenance complete"
```

Commits task-definition edits only; the report, profile edits, pending_actions.json, RUN_LOG.md and SYSTEM_STATUS.md are git-ignored and not captured. Do not block if git fails.

---

## Rules

- Never delete profile entries — archive or flag only.
- Never auto-resolve open PAs — escalate or flag only.
- If pending_actions.json is unreadable: skip Step 4, note the error in the report, continue with other steps.
- Output in English.
