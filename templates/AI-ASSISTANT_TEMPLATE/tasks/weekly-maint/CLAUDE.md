# Working Folder File Map (weekly-maint)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the Monday weekly maintenance (production) |
| `LAST_RUN.txt` | Single-line ISO 8601 UTC timestamp of the previous maintenance run |
| `RUN_LOG.md` | Append-only history of maintenance runs |
| `ISSUES_LOG.md` | Append-only log of operational issues encountered during production runs |
| `IMPROVEMENTS.md` | Pending proposals, applied fixes, and recurring observations |

Output file: `../../Actions/MAINTENANCE_REPORT.md` (overwritten each run).
