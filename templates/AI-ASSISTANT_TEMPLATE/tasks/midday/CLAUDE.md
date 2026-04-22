# Working Folder File Map (midday)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the mid-day urgent scan (production) |
| `LAST_RUN.txt` | Single-line ISO 8601 UTC timestamp of the previous scan start |
| `RUN_LOG.md` | Append-only history of scan runs |
| `ISSUES_LOG.md` | Append-only log of operational issues encountered during production runs |
| `IMPROVEMENTS.md` | Pending proposals and run counter |

Output file: `../../Actions/ACTIONS_URGENT.html` (archived to `../../Actions/History/` before each run).
