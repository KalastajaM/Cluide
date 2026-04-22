# Working Folder File Map (daily)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the daily business assistant (production only) |
| `RUN_LOG.md` | Append-only history of automated runs |
| `LAST_RUN.txt` | Single-line ISO 8601 UTC timestamp of the previous run start |
| `pending_actions.json` | Source of truth for all open action items |
| `IMPROVEMENTS.md` | Run counter, pending proposals, applied fixes |
| `LESSONS.md` | Append-only log of mistakes and improvements |
| `ISSUES_LOG.md` | Append-only log of issues encountered during production runs (input to maintenance) |
