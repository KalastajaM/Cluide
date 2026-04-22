# Bootstrap Setup

Run these commands after cloning / copying the template to initialise the runtime state files.
Only needed once on a fresh clone — each task also self-bootstraps on first run.

## Prerequisites

1. Install prerequisites: Cowork (or Claude Code with scheduled tasks), the Microsoft 365 connector, and — optionally — Atlassian.
2. Search this tree for `[YOUR_*]` placeholders and fill them in. At minimum:
   - `[YOUR_NAME]`, `[YOUR_ROLE]`, `[YOUR_EMAIL]`
   - `[YOUR_COMPANY]`, `[YOUR_COMPANY_KEYWORD]` (single-word email search keyword — usually the company name in lowercase)
   - `[YOUR_NAME_LOWERCASE]` (used as a Teams fallback recipient)
   - `[YOUR_TIMEZONE]` (IANA, e.g. `Europe/Helsinki`), `[YOUR_TIMEZONE_ABBR]` (e.g. `EET`), `[YOUR_UTC_OFFSET]` (e.g. `UTC+2`)
   - `[YOUR_M365_TENANT]` (e.g. `example.com`)
   - `[YOUR_ATLASSIAN_DOMAIN]` (e.g. `example.atlassian.net`, leave blank if unused)
   - `[PROJECT_ROOT]` (absolute path to this folder — used in a couple of git snapshot commands inside each TASK.md)
3. Register the four scheduled tasks in Cowork: `tasks/daily`, `tasks/midday`, `tasks/weekly-plan`, `tasks/weekly-maint`. Each points at `TASK.md` inside its folder.

## Copy state files

```bash
mkdir -p tasks/daily tasks/midday tasks/weekly-maint tasks/weekly-plan

cp bootstrap/daily/pending_actions.json   tasks/daily/pending_actions.json
cp bootstrap/daily/resolved_archive.json  tasks/daily/resolved_archive.json
cp bootstrap/daily/RUN_LOG.md             tasks/daily/RUN_LOG.md
cp bootstrap/daily/IMPROVEMENTS.md        tasks/daily/IMPROVEMENTS.md
cp bootstrap/daily/ISSUES_LOG.md          tasks/daily/ISSUES_LOG.md
cp bootstrap/daily/LAST_RUN.txt           tasks/daily/LAST_RUN.txt
cp bootstrap/daily/LESSONS.md             tasks/daily/LESSONS.md

cp bootstrap/midday/urgent_data.json      tasks/midday/urgent_data.json
cp bootstrap/midday/RUN_LOG.md            tasks/midday/RUN_LOG.md
cp bootstrap/midday/IMPROVEMENTS.md       tasks/midday/IMPROVEMENTS.md
cp bootstrap/midday/ISSUES_LOG.md         tasks/midday/ISSUES_LOG.md
cp bootstrap/midday/LAST_RUN.txt          tasks/midday/LAST_RUN.txt

cp bootstrap/weekly-maint/RUN_LOG.md      tasks/weekly-maint/RUN_LOG.md
cp bootstrap/weekly-maint/IMPROVEMENTS.md tasks/weekly-maint/IMPROVEMENTS.md
cp bootstrap/weekly-maint/ISSUES_LOG.md   tasks/weekly-maint/ISSUES_LOG.md
cp bootstrap/weekly-maint/LAST_RUN.txt    tasks/weekly-maint/LAST_RUN.txt

cp bootstrap/weekly-plan/RUN_LOG.md       tasks/weekly-plan/RUN_LOG.md
cp bootstrap/weekly-plan/IMPROVEMENTS.md  tasks/weekly-plan/IMPROVEMENTS.md
cp bootstrap/weekly-plan/ISSUES_LOG.md    tasks/weekly-plan/ISSUES_LOG.md

cp bootstrap/SYSTEM_STATUS.md             SYSTEM_STATUS.md

mkdir -p Knowledge
cp bootstrap/knowledge/INDEX.md           Knowledge/INDEX.md
# Copy bootstrap/knowledge/TOPIC_TEMPLATE.md to Knowledge/<TOPIC>.md for each topic you need.
```

## Rename .gitignore

```bash
mv .gitignore.template .gitignore
```

## Notes

- Each task also performs a self-bootstrap check at startup (Step 0B): if a state file is missing, it copies from `bootstrap/` automatically. Manual setup via this file is only needed if you want state files in place before the first run.
- Update stubs whenever the state file schema changes (new fields, new sections). Stubs should always mirror the current schema — just without real data.
- `Profile/` is populated by the daily task on first successful run. You do not need to pre-create profile files.
