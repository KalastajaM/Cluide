# Task: Setup Self-Improving Task

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-self-improving-task.md` (then specify which task to upgrade)
> **Source guides:** `07_TASK_LEARNING_GUIDE.md`, `08_SELFIMPROVE_TEMPLATE.md`

## Purpose
Add the self-improvement scaffolding from Guide 07 to an existing task: an `IMPROVEMENTS.md` file, a self-improvement step wired into the run procedure, and optionally a `LESSONS.md` for reasoning history. After setup, the task will track its own evolution and get measurably better with each run.

**Prerequisites:** The target task should already have a working `TASK.md`. Run `tasks/audit-task-efficiency.md` first if the task file is large — a lean task is easier to self-improve.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Identify the task

Ask: "Which task should I add self-improvement to? Provide the path to the task folder (e.g. `tasks/email-digest/`)."

Read the `TASK.md` in that folder. Understand:
- What the task does
- What state files it manages
- What its current final step is
- Whether it already has an `IMPROVEMENTS.md`

If `IMPROVEMENTS.md` already exists: read it, tell the user what's already in place, and skip to Step 3 to fill any gaps.

### Step 2 — Ask a few questions

> 1. How often does this task run?
>    Use `AskUserQuestion` with buttons: `Daily` / `Weekly` / `On demand`
> 2. Does the task manage knowledge or profile files that accumulate over time? If so, which files?
> 3. Should I also create a `LESSONS.md` for reasoning history? (Recommended for tasks with external connectors or complex logic that runs 30+ times.)
>    Use `AskUserQuestion` with buttons: `Yes` / `No`

Based on the run frequency, set the refactor threshold:
- Daily runs → 25
- Weekly runs → 10
- On demand → 15 (default)

### Step 3 — Create IMPROVEMENTS.md

Write `[task-folder]/IMPROVEMENTS.md` using the template below:

```markdown
# [TASK NAME] — Improvements Log

## Counters
{
  "total_runs": 0,
  "runs_since_last_refactor": 0,
  "refactor_threshold": [N]
}

## Noise Filters
*(Patterns to collapse rather than process individually — add as the task runs.)*

| Pattern | Action |
|---------|--------|
| *(none yet)* | |

## Applied Fixes
*(Newest first. Archive when > 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|

## Archived Fixes
*(Older entries rotated out of Applied Fixes.)*

## Pending Proposals
*(Proposals awaiting user input. Archive after 2 ignored runs.)*

| ID | Proposed | Title | Status |
|----|----------|-------|--------|

## Known Issues
*(Active issues being monitored.)*

| ID | Description | First seen | Status |
|----|-------------|------------|--------|

## Improvement Ideas Backlog
*(Low-priority observations not yet ready to propose.)*

---

## Self-Improvement Step Instructions

Run these instructions at the end of every run (after primary work, before writing the run log).

### A. Feedback Signal Detection

Scan for:
- User annotations on output files since last run ([DONE] / [SKIP] / [WRONG] / corrections)
- Manual edits to state files managed by this task — reconcile and extract the lesson
- Items open/unresolved for 14+ days — flag and review priority
- Any query or operation that failed or produced unexpected output
- Recurring patterns (3+ observations) not yet codified as a rule

### B. Refactor Trigger Check

Check `runs_since_last_refactor`. If ≥ `refactor_threshold`:
1. Review all always-loaded files — remove stale, duplicate, contradictory entries
2. Review TASK.md — remove steps no longer followed or now outdated
3. Review pending/open state — identify orphaned or obsolete items
4. Archive Applied Fixes entries beyond the 10 most recent
5. Reset `runs_since_last_refactor` to 0
6. Note "Refactor: [summary of what was found]" in the run log

### C. Auto-apply vs. Propose

**Apply directly** (all must be true): clearly correct with HIGH confidence AND low-risk AND narrow scope AND purely additive.

**Propose in IMPROVEMENTS.md** (if any is true): affects behaviour in a non-obvious way, restructures tracking, modifies core logic, touches 3+ files or 10+ lines, confidence below HIGH, user hasn't explicitly requested it.

Use proposal format:
```json
{
  "id": "PROP-NNN",
  "proposed": "YYYY-MM-DD",
  "title": "Short description",
  "rationale": "Why this improves the task",
  "change": "Exactly what would change and in which files",
  "confidence": "HIGH | MEDIUM | LOW",
  "status": "PENDING"
}
```

The two-run rule: archive proposals not responded to after 2 runs.

### D. Update IMPROVEMENTS.md

At end of every run:
1. Increment `total_runs` and `runs_since_last_refactor`
2. Move any APPROVED proposals to Applied Fixes; record what changed
3. Archive REJECTED proposals
4. Add any new proposals from signal detection
5. Add new known issues discovered this run
6. Add low-priority observations to Improvement Ideas Backlog
```

### Step 4 — Wire into TASK.md

Add two references to the task's `TASK.md`:

**1. Near the top of the run procedure** (in the "Read State" step, or as a new Step 0 if none exists):

```markdown
Read `IMPROVEMENTS.md`. Note the current `runs_since_last_refactor` — you will increment it at the end.
Act on any proposals marked [APPROVED], [REJECTED], or [MODIFY: ...] before proceeding.
```

**2. As the final step before writing the run log:**

```markdown
## Final Step: Self-Improvement

Run the Self-Improvement step: follow sections A–D in `IMPROVEMENTS.md`
(Feedback Signal Detection → Refactor Trigger Check → Auto-apply vs. Propose → Update IMPROVEMENTS.md).

Then write the run log entry.
```

Show the user the exact diff — the two insertions — and ask for approval before writing.

### Step 5 — Create LESSONS.md (if requested)

If the user asked for `LESSONS.md`, create `[task-folder]/LESSONS.md`:

```markdown
# [TASK NAME] — Lessons Log

Append-only. Never edit existing entries — only prepend new ones.
Write an entry when: applying an approved proposal, fixing a connector bug, or resolving a logic error.

Format:
## [YYYY-MM-DD] Short description (FIX-NNN or PROP-NNN)
**What happened:** Brief description.
**Root cause:** Why it happened.
**Fix applied:** What changed and why this approach was chosen.

---
*(No entries yet — first entry added after the first applied fix.)*
```

### Step 6 — Confirm

Tell the user:
- What was created (`IMPROVEMENTS.md`, optionally `LESSONS.md`)
- Where the two wiring points were added in `TASK.md`
- The refactor threshold that was set and why
- "On the next run, the task will start tracking its own evolution. Respond to proposals by writing [APPROVED], [REJECTED], or [MODIFY: ...] directly in `IMPROVEMENTS.md` or in the task's output."
