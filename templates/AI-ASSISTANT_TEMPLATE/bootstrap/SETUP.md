# Bootstrap Setup

Run these commands after cloning / copying the template to initialise the runtime state files.
Only needed once on a fresh clone — each task also self-bootstraps on first run.

## Prerequisites

1. Read `../PLATFORM_SETUP.md`. Choose a runner with verified filesystem, script execution and Microsoft 365 search/read access; optionally Atlassian. ChatGPT uploaded sources alone cannot execute this file-backed workflow. Test the actual connector coverage before registration.
2. Search this tree for `[YOUR_*]` and `[EXAMPLE_*]` placeholders and fill them in. At minimum:
   - `[YOUR_NAME]`, `[YOUR_ROLE]`, `[YOUR_EMAIL]`
   - `[YOUR_COMPANY]`, `[YOUR_COMPANY_DOMAIN]` (your own email domain — separates colleagues from external senders), `[YOUR_INDUSTRY]`
   - `[YOUR_COMPANY_KEYWORD]` (single-word email search keyword — usually the company name in lowercase)
   - `[YOUR_NAME_LOWERCASE]` (used as a Teams fallback recipient)
   - `[YOUR_TIMEZONE]` (IANA, e.g. `Europe/Helsinki`) — it also fills the `TIMEZONE` row of `tasks/daily/CONFIG.md`, the one place all four `generate_*.py` scripts read the zone from (left unfilled, they use UTC); `[YOUR_TIMEZONE_ABBR]` (e.g. `EET`); `[YOUR_UTC_OFFSET_STANDARD]` (e.g. `UTC+2`) and `[YOUR_UTC_OFFSET_DST]` (e.g. `UTC+3`; the same value as the standard offset if your zone has no daylight saving time)
   - `[YOUR_M365_TENANT]` (e.g. `example.com`)
   - `[YOUR_ATLASSIAN_DOMAIN]` (e.g. `example.atlassian.net`, leave blank if unused)
   - `[YOUR_EXCLUDED_TOPICS]` (private threads or topics the assistant must not track)
   - `[EXAMPLE_TEAMS_CHANNEL_TO_SKIP]`, `[EXAMPLE_COLLEAGUE_EMAIL]` (sample entries showing the shape — replace or delete them)
   - `[YOUR_FOCUS_BLOCK]`, `[YOUR_LUNCH_BLOCK]`, `[YOUR_END_OF_DAY_MARKER]`, `[YOUR_BUSIEST_WEEKDAY]` in `tasks/weekly-plan/TASK.md` (or delete that paragraph, as it says)
   - `[paste exact rule]` in the bootstrap text in `../PLATFORM_SETUP.md`
   - `[PROJECT_ROOT]` (absolute path to this folder — used in the git snapshot and `python3` commands inside each TASK.md)
   - Leave `[USER]` as written: it stands for the person the assistant works for, and `[USER]` / `[USER-CONFIRMED]` are also literal provenance tags in the profile rules, so a find-and-replace would break them.
3. After a supervised run and duplicate-guard verification, register on exactly one chosen scheduler: `tasks/daily`, `tasks/midday`, `tasks/weekly-plan`, `tasks/weekly-maint`. Each points at `TASK.md` inside its folder.
4. The generator scripts need Python 3.9+ (for `zoneinfo`); the weekly planner also needs `pip install jinja2`. Without jinja2 its HTML step fails and the task falls back to composing the HTML by hand.
5. Optional script settings, each with a safe default: `USER_EMAIL_DOMAIN` (ICS event IDs) and `BUSIEST_WEEKDAY` (the weekday shown faded; match `[YOUR_BUSIEST_WEEKDAY]`) in the `USER CONFIG` block of `tasks/weekly-plan/generate_weekplan_html.py`, and `BRIEFING_TITLE` in `tasks/daily/generate_actions_html.py`.

## Copy state files

```bash
mkdir -p tasks/daily tasks/midday tasks/weekly-maint tasks/weekly-plan

cp -n bootstrap/daily/pending_actions.json   tasks/daily/pending_actions.json
cp -n bootstrap/daily/resolved_archive.json  tasks/daily/resolved_archive.json
cp -n bootstrap/daily/RUN_LOG.md             tasks/daily/RUN_LOG.md
cp -n bootstrap/daily/IMPROVEMENTS.md        tasks/daily/IMPROVEMENTS.md
cp -n bootstrap/daily/IMPROVEMENTS_DETAIL.md tasks/daily/IMPROVEMENTS_DETAIL.md
cp -n bootstrap/daily/ISSUES_LOG.md          tasks/daily/ISSUES_LOG.md
cp -n bootstrap/daily/LAST_RUN.txt           tasks/daily/LAST_RUN.txt
cp -n bootstrap/daily/LESSONS.md             tasks/daily/LESSONS.md

cp -n bootstrap/midday/urgent_data.json      tasks/midday/urgent_data.json
cp -n bootstrap/midday/RUN_LOG.md            tasks/midday/RUN_LOG.md
cp -n bootstrap/midday/IMPROVEMENTS.md       tasks/midday/IMPROVEMENTS.md
cp -n bootstrap/midday/ISSUES_LOG.md         tasks/midday/ISSUES_LOG.md
cp -n bootstrap/midday/LAST_RUN.txt          tasks/midday/LAST_RUN.txt

cp -n bootstrap/weekly-maint/RUN_LOG.md      tasks/weekly-maint/RUN_LOG.md
cp -n bootstrap/weekly-maint/IMPROVEMENTS.md tasks/weekly-maint/IMPROVEMENTS.md
cp -n bootstrap/weekly-maint/ISSUES_LOG.md   tasks/weekly-maint/ISSUES_LOG.md
cp -n bootstrap/weekly-maint/LAST_RUN.txt    tasks/weekly-maint/LAST_RUN.txt

cp -n bootstrap/weekly-plan/RUN_LOG.md       tasks/weekly-plan/RUN_LOG.md
cp -n bootstrap/weekly-plan/IMPROVEMENTS.md  tasks/weekly-plan/IMPROVEMENTS.md
cp -n bootstrap/weekly-plan/ISSUES_LOG.md    tasks/weekly-plan/ISSUES_LOG.md
cp -n bootstrap/weekly-plan/LAST_RUN.txt     tasks/weekly-plan/LAST_RUN.txt

cp -n bootstrap/SYSTEM_STATUS.md             SYSTEM_STATUS.md

mkdir -p Knowledge Actions
cp -n bootstrap/knowledge/INDEX.md           Knowledge/INDEX.md
# Copy bootstrap/knowledge/TOPIC_TEMPLATE.md to Knowledge/[Topic]_[Qualifier].md for each topic you need.
```

## Rename .gitignore

```bash
mv .gitignore.template .gitignore
```

## Git snapshots and backup

The pre-run and post-run commits in each TASK.md need a git repository, and the template does not create one. To use them, initialise a repository once, after renaming the ignore file:

```bash
git init -b main
git add -A
git commit -m "initial template"
```

These commits cover task-definition edits only: `TASK.md`, `TASK_REFERENCE.md`, `CONFIG.md` and the `generate_*.py` scripts. The ignore file keeps personal runtime state out of git on purpose — `Actions/`, `Profile/`, `Knowledge/`, `pending_actions.json`, the logs and `SYSTEM_STATUS.md` — so a git snapshot cannot restore that state after a bad run. Back it up yourself: copy the project folder to a location outside it before runs you do not trust, and on whatever schedule you can keep. Never add a public remote to this repository. Without `git init` the git steps fail harmlessly (the tasks never block on them) and nothing is committed.

## Notes

- Each task also performs a self-bootstrap check at startup (Step 0B): if a state file is missing, it copies from `bootstrap/` automatically, and it creates `Actions/` and `Knowledge/` if absent. On a first run with an empty `LAST_RUN.txt` and no run-log entry, the daily and midday tasks use a 24-hour window. Manual setup via this file is only needed if you want state files in place before the first run.
- Update stubs whenever the state file schema changes (new fields, new sections). Stubs should always mirror the current schema — just without real data.
- `Profile/` is populated by the daily task on first successful run. You do not need to pre-create profile files.
