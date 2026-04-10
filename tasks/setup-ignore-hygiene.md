# Task: Setup Ignore Hygiene

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-ignore-hygiene.md`
> **Source guides:** `11_GIT_INTEGRATION.md`, `12_SECURITY.md`

## Purpose
Audit the project for files that should be ignored by git and/or Claude, update `.gitignore` and `.claudeignore` accordingly, and optionally install a PostToolUse hook (or CLAUDE.md rule) that flags newly created files that should be ignored.

This task is designed to be portable and run on any project. Do not assume any files or directories already exist — check first.

---

## Instructions

Execute the following steps in order. Stop and ask the user before making any changes.

### Step 1 — Scan the project

Use `git ls-files -o --exclude-standard` to list untracked files and `git ls-files` to list tracked files. Also do a broad directory listing. Identify files and patterns that likely belong in `.gitignore` or `.claudeignore` based on the categories below.

**Should go in `.gitignore`** (keep out of version control):
- OS noise: `.DS_Store`, `Thumbs.db`, `desktop.ini`
- Build artifacts: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `dist/`, `build/`, `*.egg-info/`
- Dependency directories: `node_modules/`, `.venv/`, `env/`, `venv/`
- Log files: `*.log`, `*.log.*`
- Temp/backup files: `*.tmp`, `*.bak`, `*.swp`, `*~`
- Secrets: `.env`, `.env.*`, `*.pem`, `*.key`, `secrets.*`
- Runtime state files: files named `*_state.json`, `*_archive.json`, `pending_*.json`, `recent_*.json`
- Generated outputs: `*.html` in project root (if clearly generated, not source), `*.pdf` (generated)
- IDE/editor directories: `.vscode/`, `.idea/`, `*.code-workspace`
- Personal/private data directories (Profile/, personal data folders)

**Should go in `.claudeignore`** (keep out of Claude context, but may still be in git):
- `.git/` directory
- Large generated archives or history directories (e.g. `Actions/History/`, `*.archive/`)
- Compiled or bundled skill files
- Large data dumps
- Anything in `.gitignore` that would also bloat Claude's context

### Step 2 — Present proposal

Show the user a categorized proposal in this format:

```
Proposed additions to .gitignore:
  [category]: pattern1, pattern2, ...

Proposed additions to .claudeignore:
  [category]: pattern1, pattern2, ...

Already covered (no changes needed):
  pattern1, pattern2, ...
```

For each category, briefly explain why. Do NOT propose removing existing entries.

Ask: "Shall I apply these changes? You can also tell me which ones to skip."

### Step 3 — Apply ignore file changes

After the user approves (in full or partially):

1. Check if `.gitignore` exists. If not, create it with a header comment. If yes, append the approved additions.
2. Check if `.claudeignore` exists. If not, create it using the template below. If yes, append the approved additions.

**`.claudeignore` header template** (use when creating from scratch):
```
# .claudeignore — files excluded from Claude's context window
# These files remain on disk and in git (if tracked), but Claude will not load them.
# Reference: https://docs.anthropic.com/en/docs/claude-code/claudeignore

```

### Step 4 — Handle already-tracked files

Run:
```bash
git ls-files
```

Cross-reference with the newly added `.gitignore` patterns. If any tracked files now match ignored patterns, list them and ask:

"These files are already tracked by git and would not be ignored automatically. Do you want me to run `git rm --cached` on them? (This removes them from git tracking without deleting the files.)"

Only proceed with `git rm --cached` if the user explicitly says yes.

### Step 5 — Ongoing enforcement (choose one option)

Ask the user:

> "Would you also like ongoing enforcement — so future files that should be ignored get flagged automatically?
>
> **Option A — PostToolUse hook** (recommended): installs a shell script and updates `.claude/settings.json`. Requires `.claude/` directory in the project.
>
> **Option B — CLAUDE.md rule**: adds a standing instruction to `CLAUDE.md` (or creates one) telling Claude to flag ignore-worthy files whenever it creates or edits them. Works without any hook infrastructure.
>
> **Option C — Skip**: rely on manual re-runs of this task."

Proceed based on the user's choice:

---

#### Option A — Install the PostToolUse hook

1. Check if `.claude/hooks/` directory exists. Create it if not.
2. Write the file `.claude/hooks/check-ignore.sh` using the template below.
3. Make it executable: `chmod +x .claude/hooks/check-ignore.sh`
4. Check if `.claude/settings.json` exists:
   - If not: create it with the hook configuration below.
   - If yes: read it, merge in the hook entry under `hooks.PostToolUse` without overwriting other settings, and write it back.

**Hook script template** — write this exactly to `.claude/hooks/check-ignore.sh`:

```bash
#!/usr/bin/env bash
# check-ignore.sh — PostToolUse hook
# Checks newly written files against .gitignore/.claudeignore heuristics
# and emits a warning to stderr if the file looks like it should be ignored.

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Nothing to check if no file path in payload
[ -z "$FILE_PATH" ] && exit 0

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$FILE_PATH")" rev-parse --show-toplevel 2>/dev/null || echo "")}"
[ -z "$PROJECT_DIR" ] && exit 0

# Check against .gitignore patterns using git check-ignore
if git -C "$PROJECT_DIR" check-ignore -q "$FILE_PATH" 2>/dev/null; then
  echo "⚠ File '$FILE_PATH' matches a .gitignore pattern. Consider whether it should also be in .claudeignore. If it is already tracked by git, run: git rm --cached '$FILE_PATH'" >&2
  exit 0
fi

# Check against .claudeignore patterns (simple substring/extension check)
FILENAME=$(basename "$FILE_PATH")
RELPATH="${FILE_PATH#$PROJECT_DIR/}"

# Heuristic patterns — extend as needed
SUSPICIOUS=0
case "$FILENAME" in
  *.log|*.bak|*.tmp|*.swp|*~) SUSPICIOUS=1 ;;
  .DS_Store|Thumbs.db) SUSPICIOUS=1 ;;
  *.pyc|*.pyo) SUSPICIOUS=1 ;;
esac

case "$RELPATH" in
  __pycache__/*|node_modules/*|.venv/*|dist/*|build/*) SUSPICIOUS=1 ;;
  *_state.json|*_archive.json|pending_*.json|recent_*.json) SUSPICIOUS=1 ;;
esac

if [ "$SUSPICIOUS" -eq 1 ]; then
  echo "⚠ File '$FILE_PATH' looks like it may belong in .gitignore or .claudeignore (matched heuristic pattern). Please check and add it if appropriate." >&2
fi

exit 0
```

**Hook config to merge into `.claude/settings.json`**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/check-ignore.sh"
          }
        ]
      }
    ]
  }
}
```

When merging: if `hooks.PostToolUse` already exists as an array, append the new entry. Do not duplicate if the entry already exists.

---

#### Option B — Add CLAUDE.md rule

Check if `CLAUDE.md` exists in the project root.
- If not: create it with a header comment and the rule below.
- If yes: append the rule under a `## File Hygiene` section (or add that section if it doesn't exist).

**Rule to add:**
```markdown
## File Hygiene

When creating or editing files, check whether the file belongs in `.gitignore` or `.claudeignore`:
- **Add to `.gitignore`**: run logs, output files, auto-generated bundles, any file containing personal data (paths, names, company names), secrets, temp files.
- **Add to `.claudeignore`**: large generated files that don't need to be loaded as context (compiled bundles, output archives, large data dumps).

If a newly created file should be ignored but is already tracked by git, flag it and suggest: `git rm --cached <file>`
```

---

### Step 6 — Confirm

Tell the user:
- What was added to `.gitignore` and `.claudeignore`
- Whether any files were untracked from git
- Which enforcement option was set up (hook, CLAUDE.md rule, or none)
- What the enforcement does: "Going forward, whenever a file is written or edited in this project, I'll check it against ignore patterns and flag anything that looks like it should be ignored."

If the user skipped enforcement, note: "You can re-run this task at any time to audit new files."
