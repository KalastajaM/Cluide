# CONFIG.md — Tunable Thresholds
> Read in Step 1 alongside IMPROVEMENTS.md and PROFILE_SUMMARY.md.
> Change values here; TASK.md references these by name.

| Parameter | Value | Description |
|-----------|-------|-------------|
| `PA_STALENESS_DAYS` | 14 | Open PA with no progress beyond N days → flag stale (Step 5C) |
| `PORTAL_STALENESS_DAYS` | 7 | PORTAL_PENDING / WAITING_OTHER PA with no update + deadline within N days → escalate to URGENT |
| `FLAGGED_SKIP_WINDOW_HOURS` | 3 | Skip Step 3E (flagged items sync) if analysis window is < N hours (Step 3E) |
| `PROFILE_SUMMARY_LINE_LIMIT` | 60 | Hard line limit for PROFILE_SUMMARY.md — trigger canary + write-time trim (Step 1, Step 4) |
| `RUN_LOG_KEEP_RUNS` | 20 | Runs to keep in RUN_LOG.md before archiving older entries |
| `RESOLVED_KEEP_DAYS` | 30 | Days to retain resolved PA entries in pending_actions.json before purging |
| `RESOLVED_INLINE_CAP` | 10 | Max resolved entries to keep inline in pending_actions.json; overflow → resolved_archive.json |
| `PROACTIVE_CAP` | 5 | Max ❓ proactive suggestion items per run |
