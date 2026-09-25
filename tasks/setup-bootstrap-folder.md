# Task: Setup Bootstrap Folder

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/setup-bootstrap-folder.md`
> **Source guide:** `11_GIT_INTEGRATION.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Purpose
Create a `bootstrap/` folder containing empty, non-personal stub versions of all runtime state files that are gitignored. This ensures the project works on a fresh clone without manual setup — and optionally adds self-bootstrap logic to task files so they detect and create missing state automatically.

**When to use:** Any project where tasks manage state files (JSON state, run logs, profile files) that are gitignored because they contain personal data or are generated at runtime.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Scan for gitignored runtime state files

```bash
# List all gitignored files that look like runtime state
git ls-files -o --exclude-standard 2>/dev/null
git ls-files 2>/dev/null | xargs -I{} git check-ignore -q {} 2>/dev/null; echo ""

# Show what patterns are in .gitignore
cat .gitignore 2>/dev/null
```

Also look for common state file patterns even if not currently ignored:
- `*_state.json`, `*_archive.json`, `pending_*.json`, `recent_*.json`
- `RUN_LOG.md`, `LAST_RUN.md`, `IMPROVEMENTS.md`
- `PROFILE_*.md`, `KNOWLEDGE_*.md`, `HYPOTHESES.md`
- `.auto-memory/*.md`

List candidates and use the available question tool, or ask in chat, for each file (or as a group):
> "I found these files that look like runtime state. Which ones need a bootstrap stub?"
> Buttons: `All of them` / `Let me choose` / `None`
> (If "Let me choose": ask about each file individually with `Yes` / `Skip` buttons.)

Skip:
- Files that are committed and already tracked (they clone automatically)
- Files that tasks create themselves on first use
- Large binary or data files

### Step 2 — Check existing bootstrap folder

```bash
ls bootstrap/ 2>/dev/null && echo "exists" || echo "missing"
```

If `bootstrap/` already exists, read its contents. Report what stubs are present and what's missing.

### Step 3 — Create stubs

For each approved state file, create a stub in `bootstrap/` with this approach:

**JSON state files** — empty structure with the correct top-level schema, no real data:
```json
{
  "last_updated": "[placeholder]",
  "items": []
}
```
Inspect the actual file (if it exists) to mirror the top-level structure. Replace all values with `[placeholder]`, empty arrays/objects, or `0`/`null`. **No real names, emails, paths, or company data.**

**Markdown logs** (RUN_LOG.md, etc.) — headers only, no run entries:
```markdown
# [Task Name] — Run Log

| Run | Date | Summary |
|-----|------|---------|
```

**Profile files** (PROFILE_*.md) — section headings with `[placeholder]` values:
```markdown
# Profile: [Section]

## [Heading]
[placeholder]
```

**IMPROVEMENTS.md** — use the self-improving task template structure with counters reset to 0 and no entries.

**Rule for all stubs:** If someone published the stub on GitHub, no personal data would be exposed. Test this mentally before writing each stub.

### Step 4 — Handle .gitignore negation rules

Some gitignored patterns are bare filenames (e.g. `RUN_LOG.md`) rather than path-specific patterns. Git will also ignore the `bootstrap/` copy of these files, making them untrackable.

For each stub that matches a bare `.gitignore` pattern, add a negation rule:

```bash
# Check which bootstrap stubs are being ignored
git check-ignore -v bootstrap/* 2>/dev/null
```

For each match, add to `.gitignore`:
```
# Bootstrap stubs — explicitly included despite global ignore rules
!bootstrap/[filename]
```

Negation rules must come after the pattern they override. After adding, verify:
```bash
git check-ignore -v bootstrap/[filename]
# Should show the negation rule, not the global pattern
```

### Step 5 — Create bootstrap/SETUP.md

Write `bootstrap/SETUP.md` with the exact copy commands for a fresh clone:

```markdown
# Bootstrap Setup

Run these commands after cloning the repository to initialise the runtime state files.
Run only for a new installation, not recovery of missing operational knowledge.
Each copy command must leave existing state intact.

## State files
[generated copy commands for each stub]
```

Generate the copy commands based on which stubs were created and where they belong (their runtime location relative to the project root).

Example:
```bash
test -e tasks/email-digest/pending_actions.json || cp bootstrap/pending_actions.json tasks/email-digest/pending_actions.json
test -e tasks/email-digest/RUN_LOG.md || cp bootstrap/RUN_LOG.md tasks/email-digest/RUN_LOG.md
mkdir -p Profile
test -e Profile/PROFILE_SUMMARY.md || cp bootstrap/PROFILE_SUMMARY.md Profile/PROFILE_SUMMARY.md
```

### Step 6 — Optionally add self-bootstrap to task files

Ask:
> "Would you like me to add first-run detection to the task files? This means each task can initialise missing state only when this is confirmed as a new installation — no manual setup needed on a fresh clone."

If yes, ask which tasks to update.

For each task's `TASK.md`, add a first-run check at the top of the run procedure (Step 0 or the Read State step):

```markdown
**First-run check:** Confirm this is a new installation before initialising missing state.
If previously populated state is unexpectedly absent, stop dependent work and recover its backup.
For a new installation only, check each file and never overwrite an existing destination:
- If `[state-file]` does not exist:
  - Copy from `bootstrap/[state-file]` if available
  - Otherwise create with empty structure: `[structure]`
  - Note "Bootstrap: first run — [file] initialised" in this run's log entry
```

Show the exact insertion for each task and ask for approval before writing.

### Step 7 — Verify

```bash
git ls-files bootstrap/
```

Confirm all stubs are tracked (none are accidentally ignored after negation rules were added).

Tell the user the results.

### Step 8 — Confirm

Tell the user:
- Which stubs were created
- Which negation rules were added to `.gitignore`
- Whether self-bootstrap was added to task files
- "Test this works: delete one of the state files and run the task — it should recreate the file from the bootstrap stub automatically."
- "Update the stubs whenever the state file schema changes (new fields, new sections). Stubs should always mirror the current schema — just without real data."

## Initialization is not recovery

Stubs are for a genuinely new, empty installation. Never overwrite existing state. If populated memory or operational state unexpectedly disappears, pause dependent work and recover the approved backup; do not seed blanks and report recovery complete. State this distinction in the generated bootstrap instructions and test that an existing synthetic file survives unchanged.

<!-- harvested: 2026-09-22 from a generic executive-support framework review; design review, not production validation -->
