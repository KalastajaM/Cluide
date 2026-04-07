# Git Integration: Versioning Your Assistant's State

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
- `tasks/*/LAST_RUN.md` — latest output; useful to compare run-to-run
- `tasks/*/RUN_LOG.md` — append-only run history
- Profile files (`PROFILE_*.md`, `.auto-memory/*.md`) — cross-session knowledge
- Scripts (`scripts/*.py`) — reusable scripts called by tasks

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

## Giving This to Claude

**To set up git integration for an existing task:**
> "Read 09_GIT_INTEGRATION.md and add the pre-run and post-run commit steps to my task at [path/to/TASK.md]. Use the commit message format from the guide."

**To add the pre-session hook:**
> "Read 09_GIT_INTEGRATION.md and add a SessionStart hook to my `.claude/settings.json` that commits any uncommitted changes before each session. My assistant files are at [path]."

**To review what a recent run changed:**
> "Run `git diff HEAD~1 HEAD -- [task-folder]/` and summarise what changed in the last run."
