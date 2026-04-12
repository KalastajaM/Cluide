# Git Integration: Versioning Your Assistant's State

*Last reviewed: April 2026*

> Git gives your assistant files one thing nothing else provides: rollback. When a run overwrites something it shouldn't, you undo it in seconds. This guide covers what to track, how to automate commits around task runs, and how to use git history to understand evolution.

---

## Why This Is Worth Setting Up

Without version control, state files are edited in place on every run. One bad run silently overwrites weeks of accumulated state. With git:

- **Every run is recoverable.** A pre-run commit means the prior state is always restorable.
- **You can see what changed.** `git diff` shows exactly what a run updated.
- **Evolution is visible.** `git log` on `IMPROVEMENTS.md` shows how a task has learned over time.
- **Collaboration is possible.** Sharing a task setup is a `git clone` away.

---

## What to Track

Not everything in your Claude setup belongs in git. Use this as a guide:

**Track:**
- `CLAUDE.md` — standing rules; changes should be reversible
- `skills/*/SKILL.md` — skill definitions; treat like code
- `tasks/*/TASK.md` and `TASK_REFERENCE.md` — task procedures
- `tasks/*/IMPROVEMENTS.md` — the learning log; most valuable file to version
- `tasks/*/RUN_LOG.md` — append-only run history
- Profile files (`PROFILE_*.md`, `.auto-memory/*.md`) — cross-session knowledge
- Scripts (`scripts/*.py`) — reusable scripts called by tasks

**Do not track (add to `.gitignore`):**
- `tasks/*/LAST_RUN.md` — replaced wholesale every run, so diffs are meaningless. Use `RUN_LOG.md` for history.
- Credentials (OAuth tokens, API keys, `.env`, `.json` credential files) — never commit secrets

**LLM wikis** (see [Guide 15](./15_LLM_WIKI.md)) — track the `wiki/` folder and `CLAUDE.md` schema. The `log.md` file is append-only, producing clean git history: `git log -- wiki/log.md` reads as a timeline of evolution, and `git diff HEAD~1 HEAD -- wiki/` shows what a single ingest changed.

See the next section for a complete breakdown of what belongs in `.gitignore` vs `.claudeignore`.

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

Claude loads files as context when reading a project. Excluding large or redundant files keeps context lean.

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

Add this rule to your project's `CLAUDE.md` so Claude maintains ignore files automatically:

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

**To add this rule to an existing `CLAUDE.md`:**
> "Read 11_GIT_INTEGRATION.md and add the File Hygiene section to my CLAUDE.md at [path]."

---

## The Pre-Run Commit Pattern

A commit immediately before each task run creates a stable snapshot you can always restore to.

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

### As a hook (all sessions)

To snapshot automatically at session start, add a `SessionStart` hook in `.claude/settings.json`:

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

The `|| true` prevents the hook from blocking when the working tree is clean. Replace `/path/to/your/assistant` with your actual path.

---

## The Post-Run Commit

Commit outputs as the last step in a task's `TASK.md`:

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

Together with the pre-run commit, this gives a clean before/after pair for every run.

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

A consistent format makes history easy to scan.

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

Before your first commit, Git needs an identity. Set it once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
```

The `--global` flag writes to `~/.gitconfig` (all repos on your machine). Use `--local` to override per-repo. Verify with `git config --list`.

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

Every run is bracketed: restore to any pre-run state in one command, or see what changed with a single diff.

---

## Using VS Code with Claude and Git

VS Code's built-in Source Control panel (`Cmd+Shift+G`) lets you review diffs, stage files, and commit without leaving the editor — useful for inspecting what Claude changed before committing.

**Key workflow:**
1. Ask Claude to update a task or skill file
2. Open Source Control to review the diff
3. Stage and commit from the panel or the integrated terminal

**Workspace file:** Open `Cluide.code-workspace` to load the project with saved settings in one click (`code Cluide.code-workspace` from terminal).

**Recommended extensions:**
- **GitLens** — inline blame and rich commit history; useful for seeing which run introduced a change
- **Git Graph** — visual commit graph; helpful for navigating many pre/post-run commits

---

## Bootstrap Pattern: Fresh Clone Readiness

When runtime state files are gitignored, a fresh clone is missing the files tasks need. The bootstrap pattern solves this without committing personal data.

### The Solution: a `bootstrap/` folder

Commit empty, non-personal stub versions of each required file under `bootstrap/`. These stubs contain structure only — enough to prevent first-run failures.

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

If the gitignored pattern is a bare filename (e.g. `RUN_LOG.md`), git also ignores the copy in `bootstrap/`. Fix with negation rules:

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

Tasks can detect and handle missing state files themselves. Add a first-run check at the top of Step 0 in `TASK.md`:

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

This makes the task self-contained on a fresh clone. The bootstrap files are the authoritative stubs; the task logic is the fallback.

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
> "Read 11_GIT_INTEGRATION.md and add the pre-run and post-run commit steps to my task at [path/to/TASK.md]. Use the commit message format from the guide."

**To add the pre-session hook:**
> "Read 11_GIT_INTEGRATION.md and add a SessionStart hook to my `.claude/settings.json` that commits any uncommitted changes before each session. My assistant files are at [path]."

**Faster alternatives:** `tasks/setup-github.md` handles full GitHub setup including ongoing sync. `tasks/setup-ignore-hygiene.md` audits and fixes `.gitignore`/`.claudeignore`. `tasks/setup-bootstrap-folder.md` creates bootstrap stubs for gitignored runtime files.

**To review what a recent run changed:**
> "Run `git diff HEAD~1 HEAD -- [task-folder]/` and summarise what changed in the last run."
