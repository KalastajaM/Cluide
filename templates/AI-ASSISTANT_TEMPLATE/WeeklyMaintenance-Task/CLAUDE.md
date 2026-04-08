# Working Folder File Map (WeeklyMaintenance-Task)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the Monday weekly maintenance |
| `LAST_MAINTENANCE.txt` | Single-line ISO 8601 UTC timestamp of the previous maintenance run (created on first run) |
| `MAINTENANCE_LOG.md` | Append-only history of maintenance runs (created on first run) |

Output file: `../Actions/MAINTENANCE_REPORT.md` (overwritten each run).
