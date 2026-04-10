# Task: Setup GitHub

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-github.md`
> **Source guide:** `11_GIT_INTEGRATION.md`

## Purpose
Make a local project available on GitHub: initialize git if needed, create or connect a remote repository, make the first commit, and set up ongoing sync so future changes are committed automatically.

This task is designed to be portable and run on any project. Do not assume any state — check everything first.

**Prerequisite:** If the project has no `.gitignore` yet, suggest running `tasks/setup-ignore-hygiene.md` first. Proceed if the user says it's fine to skip.

---

## Instructions

Execute the following steps in order. Stop and ask the user before making any changes.

### Step 1 — Check current state

Run the following checks and report findings before proposing anything:

```bash
# Is git initialized?
git rev-parse --is-inside-work-tree 2>/dev/null && echo "yes" || echo "no"

# Is there already a remote?
git remote -v 2>/dev/null

# Is there already a commit history?
git log --oneline -5 2>/dev/null

# Is the GitHub CLI available and authenticated?
gh auth status 2>/dev/null

# Is there a .gitignore?
ls .gitignore 2>/dev/null && echo "exists" || echo "missing"
```

Report what you found in a brief summary, e.g.:
```
State: git not initialized | remote: none | gh CLI: authenticated as @username | .gitignore: missing
```

If `.gitignore` is missing, say:
> "There is no `.gitignore` yet. I recommend running `tasks/setup-ignore-hygiene.md` first to avoid accidentally committing files that shouldn't be tracked. Shall I proceed anyway, or run that task first?"

If `gh` is not authenticated, say:
> "The GitHub CLI is not authenticated. Please run `gh auth login` and follow the prompts, then re-run this task."
> Stop here until the user confirms.

### Step 2 — Propose the plan

Based on the state found in Step 1, propose what needs to be done. Use only the steps that apply:

```
Here's what I'll do:
  [ ] Initialize git (git init)
  [ ] Create a minimal .gitignore (if missing and user chose to proceed)
  [ ] Create a new GitHub repository  OR  connect to existing repo: <name>
  [ ] Stage and make the first commit
  [ ] Push to GitHub
  [ ] Set up ongoing sync (you'll choose how)

Shall I proceed?
```

For the repository step, ask:
> "Should I create a new GitHub repository, or connect to an existing one?
> - **New repo**: I'll create it using `gh repo create`. What should it be named? Public or private?
> - **Existing repo**: Paste the repo URL or name (e.g. `username/repo-name`)."

### Step 3 — Initialize git (if needed)

If git is not yet initialized:

```bash
git init
git config --local init.defaultBranch main
```

If `user.name` or `user.email` are not set globally, check and prompt:
```bash
git config user.name
git config user.email
```
If either is missing, ask the user for their name and email and set them:
```bash
git config --global user.name "<name>"
git config --global user.email "<email>"
```

### Step 4 — Create minimal .gitignore (if missing and user chose to proceed)

If `.gitignore` does not exist and the user wants to continue without running `setup-ignore-hygiene.md`, create a minimal one:

```
# OS noise
.DS_Store
Thumbs.db

# Secrets — never commit
.env
*.pem
*.key
credentials.json
token.json

# Editor
.vscode/
.idea/

# Dependencies
node_modules/
.venv/
__pycache__/
*.pyc
```

Tell the user: "This is a minimal `.gitignore`. Run `tasks/setup-ignore-hygiene.md` later for a more thorough audit."

### Step 5 — Create or connect the GitHub repository

**If creating a new repo:**
```bash
gh repo create <name> --<public|private> --source=. --remote=origin --push
```
Note: `--source=. --remote=origin --push` initializes the remote and pushes in one step. Skip Steps 6 and 7 if this succeeds — `gh repo create --push` handles them.

**If connecting to an existing repo:**
```bash
git remote add origin <url>
```
Verify: `git remote -v`

### Step 6 — Stage and make the first commit

```bash
git add .
git status
```

Show the user the list of files that will be committed. Ask:
> "These files will be included in the first commit. Anything you'd like to exclude before I commit?"

After confirmation:
```bash
git commit -m "initial: project setup"
```

### Step 7 — Push to GitHub

```bash
git push -u origin main
```

If the push fails because the remote has commits (e.g. it was initialized with a README), say:
> "The remote has existing commits. Run `git pull origin main --allow-unrelated-histories` to merge them, then push again. Want me to do that?"

### Step 8 — Set up ongoing sync

Ask the user:

> "Would you like me to set up ongoing sync so future changes are committed automatically?
>
> **Option A — SessionStart hook**: auto-commits any uncommitted changes at the start of every Claude session. Modifies `.claude/settings.json`.
>
> **Option B — CLAUDE.md rule**: adds a standing instruction telling Claude to commit after completing any task that modifies files. Works without hook infrastructure.
>
> **Option C — Both**: hook for automatic safety snapshots + CLAUDE.md rule for meaningful post-task commits.
>
> **Option D — Skip**: commit manually when you choose."

Proceed based on the user's choice:

---

#### Option A — SessionStart hook

Check if `.claude/settings.json` exists. If not, create it. Merge in the following under `hooks.SessionStart`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && git add -A && git commit -m \"pre-session snapshot $(date +%Y-%m-%d\\ %H:%M)\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

When merging: if `hooks.SessionStart` already exists as an array, append the entry. Do not duplicate if already present.

---

#### Option B — CLAUDE.md rule

Check if `CLAUDE.md` exists. If not, create it. Add or append a `## Git Sync` section:

```markdown
## Git Sync

After completing any task that modifies files, commit the changes:

```bash
git add -A
git commit -m "update: <brief description of what changed>"
git push
```

Use a meaningful commit message that describes what changed, not just "update files".
If the working tree is already clean, skip the commit step.
```

---

#### Option C — Both

Apply Option A and Option B.

---

### Step 9 — Confirm

Tell the user:
- The GitHub repository URL
- The commit that was pushed
- Which ongoing sync option was set up (if any)
- The command to check status at any time: `git status` and `git log --oneline -10`

If sync was skipped, note: "To commit future changes manually: `git add -A && git commit -m 'your message' && git push`"
