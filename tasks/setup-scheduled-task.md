# Task: Setup Scheduled Task

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-scheduled-task.md`
> **Source guides:** `04_TASK_EFFICIENCY_GUIDE.md`, `05_TASK_LEARNING_GUIDE.md`, `06_SELFIMPROVE_TEMPLATE.md`

## Purpose
Scaffold a new scheduled task from scratch with efficiency and self-improvement patterns built in from run 1: a lean `TASK.md`, a `TASK_REFERENCE.md` for detail content, a `RUN_LOG.md`, and an `IMPROVEMENTS.md`. The result is a task ready to run and improve from its first execution.

**For adding self-improvement to an *existing* task:** use `tasks/setup-self-improving-task.md` instead.

---

## Instructions

### Step 1 — Interview the user

Ask the following. Collect all answers before writing anything.

**What the task does:**
> 1. What should this task do? Describe it in 2–3 sentences.
> 2. What triggers it — and how often does it run? (e.g. daily at 8am, weekly on Monday, on demand)
> 3. What inputs does it need each run? (e.g. reads email, reads a file, receives user input, no inputs)
> 4. What outputs does it produce? (e.g. a markdown report, a JSON file, a draft email, updates a state file)

**State and memory:**
> 5. Does it need to remember things between runs? (e.g. what it processed last time, a running log, a knowledge file)
> 6. Are there any state files it manages — files it reads and updates on every run?

**Self-improvement:**
> 7. Should it learn and improve over time? (Recommended for tasks that run regularly — adds `IMPROVEMENTS.md` and a self-improvement step.)
> 8. If yes: how often does it run? (This sets the refactor threshold — daily → 25, weekly → 10.)

After collecting answers: "Thanks — I'll scaffold the task now."

### Step 2 — Determine task name and location

Derive a kebab-case name (e.g. `email-digest`, `weekly-review`, `portfolio-tracker`).

Ask: "I'll create this at `tasks/[name]/`. Does that work, or should it go somewhere else?"

```bash
ls tasks/[name]/ 2>/dev/null && echo "exists" || echo "new"
```

If the folder already exists, read its contents and report. Ask whether to continue or abort.

### Step 3 — Create the task folder and files

Create the folder and all files below.

#### `tasks/[name]/TASK.md`

Write a lean instruction file (target: ≤ 250 lines). Structure:

```markdown
# [Task Name]

## Purpose
[2–3 sentences from the interview.]

Run frequency: [daily/weekly/on demand]

---

## Step 0 — Read state

Read `IMPROVEMENTS.md`. Note `runs_since_last_refactor` — increment it this run.
Act on any proposals marked [APPROVED], [REJECTED], or [MODIFY: ...] before proceeding.

[If state files exist:]
Read [state file]. If it does not exist, copy from `bootstrap/[file]` if available,
otherwise create with empty structure: [structure].

---

## Step 1 — [First meaningful step]
[Concrete instructions. Name exact MCP tools. Specify what to do if a step fails.]

## Step 2 — [Next step]
...

[Continue for all steps derived from the interview]

---

## Final Step — Self-improvement and run log

Run the Self-Improvement step: follow sections A–D in `IMPROVEMENTS.md`
(Feedback Signal Detection → Refactor Trigger Check → Auto-apply vs. Propose → Update IMPROVEMENTS.md).

Append to `RUN_LOG.md`:
| [run number] | [YYYY-MM-DD] | [one-line summary of what happened this run] |
```

Put workflow details, schemas, output format templates, and error handling procedures in `TASK_REFERENCE.md` — reference them from TASK.md with `See TASK_REFERENCE.md § [Section]`.

#### `tasks/[name]/TASK_REFERENCE.md`

```markdown
# [Task Name] — Reference

*Read on demand — not loaded every run. Referenced from TASK.md.*

[Populate with sections for any schemas, output templates, error handling, or domain reference content
identified during the interview. Leave empty with placeholder sections if nothing yet.]

## Output Format
[Template for the task's output, if it produces a structured artifact]

## Error Handling
[What to do when inputs are missing, tools fail, or state files are corrupt]
```

#### `tasks/[name]/RUN_LOG.md`

```markdown
# [Task Name] — Run Log

| Run | Date | Summary |
|-----|------|---------|
```

#### `tasks/[name]/IMPROVEMENTS.md` (if self-improvement was requested)

Use the full template from `setup-self-improving-task.md`, with:
- `total_runs: 0`
- `runs_since_last_refactor: 0`
- `refactor_threshold: [25 for daily / 10 for weekly / 15 for on-demand]`
- Task name filled in
- All placeholder rows removed

If self-improvement was not requested, skip this file and omit the Step 0 and Final Step from TASK.md.

### Step 4 — Efficiency check on the draft

Before writing, review the draft TASK.md against these targets:
- TASK.md ≤ 250 lines — if over, identify what to move to TASK_REFERENCE.md
- No JSON schemas or output templates in TASK.md — move to TASK_REFERENCE.md
- No fixed-format artifact generation in TASK.md — if the task produces a structured output file (HTML, formatted report), note: "Consider writing a generation script once the format stabilises — Claude runs it rather than composing from scratch."

Show the user TASK.md line count and flag any efficiency issues before writing.

### Step 5 — Write all files

Write all files. Show the list of files created.

### Step 6 — Optional: schedule the task

Ask:
> "Would you like me to set up scheduling? Options:
> - (A) SessionStart hook — runs automatically when you open Claude Code in this project
> - (B) Manual trigger — you run it by saying 'run tasks/[name]/TASK.md'
> - (C) Scheduled trigger — I'll note the schedule in TASK.md and you set it up in your scheduler"

For option A, add a SessionStart hook to `.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "echo 'Run tasks/[name]/TASK.md to execute [task name]'" }]
      }
    ]
  }
}
```
(This reminds Claude to run the task at session start rather than auto-executing it without confirmation.)

### Step 7 — Confirm

Tell the user:
- Files created and their locations
- TASK.md line count
- Whether IMPROVEMENTS.md was included and the refactor threshold set
- Run frequency and how to trigger the task
- "To audit for efficiency after a few runs: `tasks/audit-task-efficiency.md`. To add self-improvement later: `tasks/setup-self-improving-task.md`."
