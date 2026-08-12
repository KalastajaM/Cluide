# Working Folder File Map (midday)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the mid-day urgent scan (production) |
| `LAST_RUN.txt` | Single-line ISO 8601 UTC timestamp of the previous scan start |
| `RUN_LOG.md` | Append-only history of scan runs |
| `ISSUES_LOG.md` | Append-only log of operational issues encountered during production runs |
| `IMPROVEMENTS.md` | Pending proposals and run counter |
| `urgent_data.json` | Structured scan output written each run (input to the HTML generator) |
| `generate_urgent_html.py` | Script: renders the urgent-actions HTML from urgent_data.json |

Output file: `../../Actions/ACTIONS_URGENT.html` (archived to `../../Actions/History/` before each run).
