# Working Folder File Map (Assistant-Task)

All project-level context (user identity, communication style, critical rules, business context, profile/knowledge/actions file map) is in `../CLAUDE.md`.

| File | What it contains |
|------|-----------------|
| `TASK.md` | Full run procedure for the daily business assistant |
| `TASK_REFERENCE.md` | Schemas, format templates, privacy rules (loaded on demand, not every run) |
| `RUN_LOG.md` | Append-only history of automated runs (created on first run) |
| `LAST_RUN.txt` | Single-line ISO 8601 UTC timestamp of the previous run start (created on first run) |
| `pending_actions.json` | Source of truth for all open action items (created on first run) |
| `IMPROVEMENTS.md` | Run counter, pending proposals, applied fixes, known issues |
| `LESSONS.md` | Append-only log of mistakes and improvements (created on first run) |
