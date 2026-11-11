# CONFIG.md — Tunable Thresholds
> Read in Step 1 alongside IMPROVEMENTS.md and PROFILE_SUMMARY.md; `../weekly-maint/TASK.md` also reads it.
> Change values here; the task files reference these by name.

| Parameter | Value | Description |
|-----------|-------|-------------|
| `TIMEZONE` | [YOUR_TIMEZONE] | IANA zone name, e.g. `Europe/Helsinki`. Read by all four `generate_*.py` scripts (daylight saving time is applied per date); unset or unknown → UTC |
| `PA_STALENESS_DAYS` | 14 | Open PA with no progress beyond N days → flag stale (Step 5C) |
| `SNOOZE_WAKE_DAYS` | 14 | Snoozed PA whose `reminder_date` is within N days of today → move back to `open` (daily Step 5D, weekly-maint Step 4) |
| `PORTAL_STALENESS_DAYS` | 7 | PORTAL_PENDING / WAITING_OTHER PA with no update + deadline within N days → escalate to URGENT |
| `FLAGGED_SKIP_WINDOW_HOURS` | 3 | Skip Step 3E (flagged items sync) if analysis window is < N hours (Step 3E) |
| `PROFILE_SUMMARY_LINE_LIMIT` | 40 | Hard line limit for PROFILE_SUMMARY.md — trigger canary + write-time trim (Step 1, Step 4) |
| `RUN_LOG_KEEP_RUNS` | 20 | Entries kept in full in each task's RUN_LOG.md; once a log passes ~30 entries, older ones move to `RUN_LOG_ARCHIVE.md` (same rule as Guide 06) |
| `RESOLVED_KEEP_DAYS` | 30 | Days to retain resolved PA entries (any status) in pending_actions.json before purging (daily §PA-Schema, weekly-maint Step 4) |
| `RESOLVED_INLINE_CAP` | 10 | Max resolved entries to keep inline in pending_actions.json; overflow → resolved_archive.json |
| `PROACTIVE_CAP` | 5 | Max ❓ proactive suggestion items per run |
