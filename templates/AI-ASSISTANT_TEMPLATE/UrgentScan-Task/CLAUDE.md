# Working Folder File Map (UrgentScan-Task)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the mid-day urgent scan |
| `LAST_URGENT_SCAN.txt` | Single-line ISO 8601 UTC timestamp of the previous scan start (created on first run) |
| `SCAN_LOG.md` | Append-only history of scan runs (created on first run) |

Output file: `../Actions/ACTIONS_URGENT.html` (archived to `../Actions/History/` before each run).
