# Git Integration: Versioning Your Assistant's State

*Last reviewed: April 2026*

> Putting your assistant's files under git version control gives you one thing that nothing else provides: the ability to roll back. When a task run updates the wrong thing, overwrites a profile section you wanted to keep, or produces outputs that break something downstream, git means you can undo it in seconds. This guide covers what to track, how to automate commits around task runs, and how to use git history to understand how your assistant has evolved.

---

## Why This Is Worth Setting Up

Without version control, your assistant's state files — profiles, improvement logs, task outputs — are edited in place on every run. One bad run can silently overwrite weeks of accumulated state. With git:

- **Every run is recoverable.** A pre-run commit means the state before the run is always restorable.
- **You can see what changed.** `git diff` tells you exactly what a run updated — useful when debugging unexpected outputs.
- **Evolution is visible.** `git log` on `IMPROVEMENTS.md` shows the history of how a task has learned and adapted over time.
- **Collaboration is possible.** Sharing a task setup with someone else is a `git clone` away.

---

## What to Track

Not everything in your Claude setup belongs in git. Use this as a guide:

**Track:**
- `CLAUDE.md` — your standing rules; changes here matter and should be reversible
- `skills/*/SKILL.md` — skill definitions; treat them like code
- `tasks/*/TASK.md` and `TASK_REFERENCE.md` — task procedures
- `tasks/*/IMPROVEMENTS.md` — the learning log; this is the most valuable file to version
- `tasks/*/RUN_LOG.md` — append-only run history (the full log belongs in git)
- Profile files (`PROFILE_*.md`, `.auto-memory/*.md`) — cross-session knowledge
- Scripts (`scripts/*.py`) — reusable scripts called by tasks

**Do not track (add to `.gitignore`):**
- `tasks/*/LAST_RUN.md` — this is just the latest run's output, not history. The full history lives in `RUN_LOG.md`. Tracking `LAST_RUN.md` produces meaningless commits every run with no diff value — it is always replaced wholesale. Gitignore it; read `RUN_LOG.md` when you need history.

**LLM wikis** (see [Guide 12](./12_LLM_WIKI.md)) — track the `wiki/` folder and `CLAUDE.md` schema. The `log.md` file inside a wiki is append-only, which produces a particularly clean git history: each commit adds exactly one entry, so `git log -- wiki/log.md` reads as a precise timeline of the wiki's evolution. `git diff HEAD~1 HEAD -- wiki/` shows exactly what a single ingest changed across all pages.

**Do not track:**
- Credentials files (OAuth tokens, API keys, `.json` credential files) — these should never be committed
- `.env` files
- Any file containing passwords or secrets

**Add to `.gitignore`:**
```
# Credentials — never commit
credentials.json
token.json
*.oauth
.env

# OS and editor noise
.DS_Store
*.swp
__pycache__/
```

See the next section for a more complete breakdown of what belongs in `.gitignore` vs `.claudeignore`, and how to automate this through `CLAUDE.md`.

---

## .gitignore and .claudeignore: What Goes Where

Two separate ignore files serve different purposes:

- **`.gitignore`** — files git will not track or commit
- **`.claudeignore`** — files Claude will not load as context (but git may still track them)

They are independent: a file can be in one, both, or neither.

### What belongs in `.gitignore`

| Category | Examples | Why |
|---|---|---|
| Credentials & secrets | `credentials.json`, `token.json`, `.env`, `*.oauth` | Never commit secrets |
| Personal data | files with full paths, company names, usernames | Not shareable across machines/users |
| Local config | `.claude/settings.local.json` | Machine-specific permission allowlists |
| Run output & logs | `LAST_RUN.md`, `RUN_LOG.md`, `output/` | Auto-generated; git history of these is noise |
| Compiled/bundled output | `skills/*.skill` | Generated from source in `skills/*/SKILL.md` |
| OS noise | `.DS_Store`, `*.swp` | Never intentional |

**Starter `.gitignore`:**
```
# Credentials
credentials.json
token.json
*.oauth
.env

# Personal / local config
.claude/settings.local.json

# Run output
**/LAST_RUN.md
**/RUN_LOG.md

# Compiled skill bundles
skills/*.skill

# OS and editor noise
.DS_Store
*.swp
__pycache__/
```

### What belongs in `.claudeignore`

Claude loads files as context when it reads a project. Excluding large or redundant files keeps context lean and responses faster.

| Category | Examples | Why |
|---|---|---|
| Git internals | `.git/` | Never useful as context |
| Compiled outputs | `skills/*.skill` | Source files are already in context |
| Dependencies | `node_modules/`, `.venv/` | Too large, not relevant |
| Duplicate reference copies | `skills/*/references/` | Already present in the root |
| Log files | `*.log` | Rarely useful as context |

**Starter `.claudeignore`:**
```
# Version control
.git/

# Dependencies
node_modules/
.venv/
__pycache__/
*.pyc

# Compiled outputs
skills/*.skill

# OS and editor noise
.DS_Store
*.log
```

### Untracking a file already in git

If you add a file to `.gitignore` that was already committed, git still tracks it. Untrack it without deleting it:

```bash
git rm --cached path/to/file
git commit -m "chore: untrack <file> — added to .gitignore"
```

For a whole directory:
```bash
git rm --cached -r path/to/folder/
```

---

## Automating File Hygiene Through CLAUDE.md

You can instruct Claude to maintain `.gitignore` and `.claudeignore` automatically by adding a rule to your project's `CLAUDE.md`. This means you never have to manually review new files — Claude will flag and exclude them as part of its normal workflow.

**Add to your project's `CLAUDE.md`:**

```markdown
## File Hygiene

When creating new files, check whether they belong in `.gitignore` or `.claudeignore`:
- **Add to `.gitignore`**: run logs, output files, auto-generated bundles,
  any file containing personal data (paths, names, company names), local config
- **Add to `.claudeignore`**: large generated files that don't need to be
  loaded as context (compiled skill bundles, output archives, etc.)

If a newly created file should be ignored but is already tracked by git,
run `git rm --cached <file>` to untrack it.
```

With this in place, Claude will add new files to the appropriate ignore file at the time of creation — without needing to be reminded.

**To add this rule to an existing `CLAUDE.md`:**
> "Read 09_GIT_INTEGRATION.md and add the File Hygiene section to my CLAUDE.md at [path]."

---

## The Pre-Run Commit Pattern

The most valuable git integration is a commit immediately before each task run. This creates a stable snapshot you can always restore to, regardless of what the run does.

### As a task step (recommended for scheduled tasks)

Add this as the first step in any task's `TASK.md`:

```markdown
## Step 0: Snapshot current state

Before doing anything else, commit the current state of the task folder:

```bash
git add tasks/[task-name]/
git commit -m "pre-run: [task-name] run $(date +%Y-%m-%d)"
```

If the working tree is clean (nothing changed since the last commit), skip this step.
This creates a restore point. If this run produces unwanted changes, `git checkout HEAD~1 -- tasks/[task-name]/` restores the pre-run state.
```

### As a hook (for all sessions)

To snapshot automatically at the start of every Claude session — before any task runs — add a `SessionStart` hook in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cd /path/to/your/assistant && git add -A && git commit -m 'pre-session snapshot $(date +%Y-%m-%d %H:%M)' 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

The `|| true` at the end prevents the hook from blocking the session if the working tree is clean (nothing to commit).

Replace `/path/to/your/assistant` with the actual path to your Claude setup directory.

---

## The Post-Run Commit

After a task run completes, commit the outputs. This is typically the last step in a task's `TASK.md`:

```markdown
## Final Step: Commit run outputs

Commit all files updated this run:

```bash
git add tasks/[task-name]/
git commit -m "run: [task-name] run [N] — [one-line summary of what changed]"
```

Include the run number and a brief summary in the commit message. Examples:
- `run: email-digest run 14 — 3 tasks extracted, 1 profile update`
- `run: guide-improvement run 3 — FIX-003 applied, PROP-001 closed`
```

This gives you a clean before/after pair for every run: the pre-run commit captures the state going in, the post-run commit captures the state coming out.

---

## Useful Git Commands for Assistant Files

**See what changed in the last run:**
```bash
git diff HEAD~1 HEAD -- tasks/[task-name]/
```

**See the full history of the improvements log:**
```bash
git log --oneline -- tasks/[task-name]/IMPROVEMENTS.md
```

**Restore a file to its pre-run state:**
```bash
git checkout HEAD~1 -- tasks/[task-name]/IMPROVEMENTS.md
```

**Compare today's profile against last week's:**
```bash
git diff HEAD@{7.days.ago} -- PROFILE_SUMMARY.md
```

**See which runs changed which files:**
```bash
git log --stat -- tasks/[task-name]/
```

---

## Meaningful Commit Messages

The value of the git history depends on the quality of the commit messages. A consistent format makes it easy to scan.

**For pre-run snapshots:**
```
pre-run: [task-name] [date]
pre-run: email-digest 2026-04-05
```

**For post-run commits:**
```
run: [task-name] run [N] — [what changed]
run: email-digest run 14 — 3 tasks extracted, 1 new hypothesis
run: guide-improvement run 3 — FIX-003 applied, no proposals pending
```

**For manual changes to CLAUDE.md or skills:**
```
update: CLAUDE.md — add Finnish timezone note
update: gmail-skill — tighten trigger description
fix: grocery-skill — add edge case for recipe requests
```

Ask Claude to follow this convention when it updates files:
> "When updating any task file, commit after with the format: `run: [task-name] run N — [what changed]`."

---

## Configuring Git for the First Time

Before you can make your first commit, Git needs to know who you are. This identity is embedded in every commit and cannot be changed after the fact without rewriting history.

**Set your identity:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

The `--global` flag writes this to your user-level config (`~/.gitconfig`), so it applies to every repository on your machine. Use `--local` instead to override it for a specific repo.

**Set your default editor** (VS Code is a good choice — see the VS Code section below):
```bash
git config --global core.editor "code --wait"
```

**Set the default branch name** to `main` (avoids the legacy `master` default):
```bash
git config --global init.defaultBranch main
```

**Verify your configuration:**
```bash
git config --list
```

This shows the merged view of all config levels. To check a specific value:
```bash
git config user.name
```

The three config scopes, in order of precedence (highest to lowest): `--local` (this repo only, stored in `.git/config`) → `--global` (your user account, stored in `~/.gitconfig`) → `--system` (all users on the machine, rarely needed).

---

## Setting Up a New Repository

If your Claude assistant files are not yet in git:

```bash
# Navigate to your .claude folder or wherever your assistant files live
cd /path/to/your/claude-setup

# Initialise
git init

# Add a .gitignore before the first commit
cat > .gitignore << 'EOF'
credentials.json
token.json
*.oauth
.env
.DS_Store
*.swp
__pycache__/
EOF

# First commit
git add .
git commit -m "initial: claude assistant setup"
```

From here, every session starts with a clean baseline.

---

## What Good Looks Like

A mature git history for an assistant task looks like this:

```
2026-04-05  run: email-digest run 14 — 3 tasks, 1 hypothesis promoted
2026-04-05  pre-run: email-digest 2026-04-05
2026-04-04  run: email-digest run 13 — quiet run, no changes
2026-04-04  pre-run: email-digest 2026-04-04
2026-04-03  update: PROFILE_contacts.md — confirmed Sara's new role
2026-04-03  run: email-digest run 12 — FIX-007 applied
2026-04-03  pre-run: email-digest 2026-04-03
```

The alternating pre/post pattern means every run is bracketed. You can restore to any pre-run state in one command, and you can see exactly what changed in any run with a single diff.

---

## Using VS Code with Claude and Git

VS Code has first-class Git support built in, making it a natural companion to Claude for managing your assistant files. You get a visual diff viewer, one-click staging and committing, and a terminal — all in one window.

### Source Control Panel

Click the branch icon in the left sidebar (or press `Ctrl+Shift+G` / `Cmd+Shift+G`) to open the Source Control panel. From here you can:

- See all modified files at a glance
- Stage individual files or hunks by clicking the `+` icon
- Write a commit message and commit without leaving the editor
- View inline diffs by clicking any changed file

This is a good alternative to the CLI for day-to-day commits, especially when reviewing what Claude has changed before committing.

### Setting VS Code as Your Git Editor

When Git needs you to write a message interactively (e.g. during a rebase), it will open VS Code and wait:

```bash
git config --global core.editor "code --wait"
```

The `--wait` flag tells Git to block until you close the file tab, so Git knows when you're done.

### Opening Your Project with the Workspace File

The `Claude-Teacher.code-workspace` file in your folder opens the project with any saved VS Code settings (panel layout, recommended extensions, etc.) in one click. Use **File → Open Workspace from File** and select it, or from the terminal:

```bash
code Claude-Teacher.code-workspace
```

### Integrated Terminal

Use the VS Code integrated terminal (`Ctrl+\`` / `Ctrl+\``) to run Claude Code and git commands side by side with your files. A typical workflow:

1. Ask Claude to update a task or skill file
2. Switch to Source Control to review the diff
3. Stage and commit from the panel, or run `git add` / `git commit` in the terminal

### Recommended Extensions

- **GitLens** — adds inline blame, rich commit history, and line-by-line authorship directly in the editor. Particularly useful for understanding which run introduced a specific change.
- **Git Graph** — visual branch and commit graph; helpful when you have many pre/post-run commits and want to navigate them quickly.

---

## Bootstrap Pattern: Fresh Clone Readiness

When runtime state files are gitignored, a fresh clone of your repository is missing the files that tasks need to exist before their first run. The bootstrap pattern solves this without committing personal data.

### The Problem

A task like the assistant runs every day and relies on files like `pending_actions.json` (action state), `RUN_LOG.md` (run history), and profile files. These are gitignored because they contain personal data. On a fresh clone, they don't exist — and the task will fail or behave incorrectly on first run.

### The Solution: a `bootstrap/` folder

Commit empty, non-personal stub versions of each required file under `bootstrap/`. These stubs contain structure, not content — they are enough to prevent first-run failures.

**Folder layout:**
```
bootstrap/
├── SETUP.md                   ← copy instructions for a fresh clone
├── pending_actions.json       ← empty action state
├── RUN_LOG.md                 ← headers-only run log
├── PROFILE_SUMMARY.md         ← placeholder profile stub
├── PROFILE_projects.md        ← placeholder projects stub
└── PROFILE_patterns.md        ← placeholder patterns stub
```

**What makes a good stub:**
- JSON state files → empty arrays/objects with the correct top-level structure
- Markdown logs → headers and a one-line description, no run entries
- Profile files → section headings with `[placeholder]` values
- No real names, emails, paths, or company data — the stub should be safe to share publicly

### Negation rules for globally-ignored filenames

If the gitignored pattern is a bare filename (e.g. `RUN_LOG.md`, `pending_actions.json`) rather than a path-specific pattern, git will also ignore the copy in `bootstrap/`. Fix this with negation rules at the bottom of `.gitignore`:

```
# Bootstrap stubs are explicitly included despite global ignore rules
!bootstrap/pending_actions.json
!bootstrap/RUN_LOG.md
```

Negation rules must come after the pattern they override. After adding them, verify with:
```bash
git check-ignore -v bootstrap/pending_actions.json
# should show the !bootstrap/ negation rule, not the global pattern
```

### SETUP.md: copy commands for a fresh clone

Commit a `bootstrap/SETUP.md` with the exact shell commands needed. Anyone (or Claude) cloning the repo for the first time can run these before starting:

```bash
# State files
cp bootstrap/pending_actions.json Assistant-Task/pending_actions.json
cp bootstrap/RUN_LOG.md Assistant-Task/RUN_LOG.md

# Profile files
mkdir -p Profile
cp bootstrap/PROFILE_SUMMARY.md Profile/PROFILE_SUMMARY.md
cp bootstrap/PROFILE_projects.md Profile/PROFILE_projects.md
cp bootstrap/PROFILE_patterns.md Profile/PROFILE_patterns.md
```

### Self-bootstrapping tasks

Rather than relying on a human to run the setup commands, tasks can detect and handle a missing state file themselves. Add a first-run check at the top of Step 0 in `TASK.md`:

```markdown
## Step 0 — Locate working directory and check first-run state

[standard find command]

**First-run check:** Before reading any state file, verify it exists:
- If `pending_actions.json` does not exist → copy from `bootstrap/pending_actions.json`.
  If bootstrap copy also missing → create with empty structure: `{"open":[],"resolved_today":[]}`
- If `RUN_LOG.md` does not exist → copy from `bootstrap/RUN_LOG.md`.
  If bootstrap copy also missing → create with header only.
- Note "Bootstrap: first run — state files initialized" in the run log entry for this run.
```

This makes the task self-contained: it will run correctly on a fresh clone without any manual setup step. The bootstrap files are the authoritative stubs; the task logic is the fallback.

### Checklist: bootstrap-ready repository

- [ ] All gitignored runtime files have a stub in `bootstrap/`
- [ ] Stubs contain structure only — no personal data
- [ ] `.gitignore` negation rules allow `bootstrap/` exceptions where needed
- [ ] `bootstrap/SETUP.md` lists the exact copy commands
- [ ] Each task's Step 0 includes a first-run check that copies or creates missing state files
- [ ] `git ls-files bootstrap/` confirms all stubs are tracked

---

## Giving This to Claude

**To set up git integration for an existing task:**
> "Read 09_GIT_INTEGRATION.md and add the pre-run and post-run commit steps to my task at [path/to/TASK.md]. Use the commit message format from the guide."

**To add the pre-session hook:**
> "Read 09_GIT_INTEGRATION.md and add a SessionStart hook to my `.claude/settings.json` that commits any uncommitted changes before each session. My assistant files are at [path]."

**Faster alternatives:** `tasks/setup-github.md` handles full GitHub setup including ongoing sync. `tasks/setup-ignore-hygiene.md` audits and fixes `.gitignore`/`.claudeignore`. `tasks/setup-bootstrap-folder.md` creates bootstrap stubs for gitignored runtime files.

**To review what a recent run changed:**
> "Run `git diff HEAD~1 HEAD -- [task-folder]/` and summarise what changed in the last run."
