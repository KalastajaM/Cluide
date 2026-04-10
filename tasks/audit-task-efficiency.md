# Task: Audit Task Efficiency

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-task-efficiency.md` (then specify which task file to audit)
> **Source guide:** `04_TASK_EFFICIENCY_GUIDE.md`

## Purpose
Audit a task file against the token efficiency checklist from Guide 04. Goal: keep always-loaded files compact, delegate fixed-format generation to scripts, and reduce unnecessary reads. Returns a prioritised list of improvements and applies them after approval.

---

## Instructions

### Step 1 — Identify the task to audit

Ask: "Which task file should I audit? Provide the path (e.g. `tasks/my-task/TASK.md`)."

Read the task file. Also check if a `TASK_REFERENCE.md` exists alongside it.

Report:
```
Task: [path]
Lines: N
Estimated tokens: ~N (rough: lines × 8)
TASK_REFERENCE.md: [exists / missing]
```

### Step 2 — Run the efficiency checklist

#### Check 1: Instruction file size

Target: TASK.md ≤ 250 lines. Everything else in TASK_REFERENCE.md (read on demand).

Scan for content that should be extracted:
- JSON schemas or data format definitions
- Full output format templates (HTML, markdown structures)
- Error handling procedures longer than 3 lines
- Privacy or sensitivity guidelines
- Design principles or philosophy
- Backfill or migration strategies
- Any section not directly needed to execute a single run step

Flag each candidate with estimated line savings.

#### Check 2: Fixed-format artifact generation

Does the task generate structured output files (HTML reports, formatted documents, CSV exports)?

If yes, ask: "Does the output format change between runs, or just the data?"
- Format is fixed, data varies → should be a script, not Claude composing from scratch
- Flag with: "Consider writing a script for [output type] — Claude runs it, doesn't compose it."

#### Check 3: Unnecessary full-file reads

Does the task read large files in full when it only needs a portion?

Look for instructions like "read [large file]" without a specified range or section. Flag with: "Consider using partial reads or a summary script to extract only what's needed."

#### Check 4: Redundant API calls

Does the task fetch full content when triage would suffice?

Pattern: fetching full email bodies when a subject-line scan would determine relevance. Flag with: "Consider a two-stage read: scan subjects/headers first, fetch full content only for relevant items."

#### Check 5: Always-loaded file sizes

For every file the task reads on every run, check size:
- TASK.md / core instruction file: target ≤ 250 lines
- KNOWLEDGE_SUMMARY.md or equivalent: target ≤ 50 lines
- IMPROVEMENTS.md: target ≤ 150 lines (archive Applied Fixes when > 10 entries)

Flag any over-limit file.

#### Check 6: Output file growth

Does the task append to a log or output file without a trim/archive policy?

An unbounded log costs more tokens every run. Flag with: "Add a trim policy — e.g. keep last N entries, archive the rest."

### Step 3 — Present findings

```
Efficiency Audit: [task name]
──────────────────────────────
Current size: N lines (~N tokens)

Issues found (prioritised by impact):

HIGH IMPACT:
  ⚠ [Check N]: [description] — estimated saving: ~N lines / ~N tokens/run

MEDIUM IMPACT:
  ⚠ [Check N]: [description]

LOW IMPACT / OPTIONAL:
  ℹ [Check N]: [description]

No issues:
  ✓ [Check N]: [description]
```

Ask:
> "Would you like me to apply these improvements? I can:
> - (A) Extract sections to TASK_REFERENCE.md (high-impact, recommended first)
> - (B) Add trim policies to log files
> - (C) Flag script candidates (you'd write the scripts)
> - (D) All of the above
> - (E) Walk through each issue together"

### Step 4 — Apply fixes

**For option A (extract to TASK_REFERENCE.md):**

1. If `TASK_REFERENCE.md` doesn't exist, create it with a header.
2. Move the flagged sections, replacing each with a reference in `TASK.md`:
   > See `TASK_REFERENCE.md § [Section Name]`
3. Show before/after line counts for TASK.md.

**For option B (trim policies):**

Add to the relevant task step:
```markdown
Trim policy: keep the last [N] entries. Move older entries to [ARCHIVE_FILE] or delete if no longer needed.
```

**For option C (script candidates):**

List the output types that should be scripted, with a brief spec for each:
```
Script needed: generate-report.py
  Input: [data file]
  Output: [output format]
  Claude's role after: run the script, use its output — don't compose the format manually
```

### Step 5 — Confirm

Tell the user:
- Line count before and after
- Estimated token saving per run
- Any remaining manual steps (writing scripts, etc.)
- "Re-run this audit after adding major new steps to the task, or if runs start feeling slow."
