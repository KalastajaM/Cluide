# AI Assistant — Maintenance Task

Run this task to analyze one or more assistant tasks, catalog issues, and generate improvement proposals. This is a generic procedure that targets any of the four assistant tasks, or all of them at once.

**Trigger:** Run manually when [USER] requests a maintenance review, or on a scheduled basis.

---

## How to Target

Specify a target at the start of the run:

- **Single task:** `target: daily` (or `midday`, `weekly-maint`, `weekly-plan`)
- **All tasks:** `target: all`

When `target: all` — run Steps 1–7 for each task sequentially, then write a combined summary to `../../Actions/MAINTENANCE_REPORT.md`.

---

## Task Registry

Use this table in Steps 1 and 2 to know which files to read and what to look for.

| Task | Folder | Run log | Extra files | Log anomaly signals |
|------|--------|---------|-------------|---------------------|
| daily | `../daily/` | `RUN_LOG.md` | `LESSONS.md`, `TASK_REFERENCE.md`, `IMPROVEMENTS_DETAIL.md`, `SIGNAL_LOG.md` | Tool calls > 30; connector returning 0 results repeatedly; LESSONS.md recurring mistake types (same type ≥ 2 entries); fast-path anomalies; SIGNAL_LOG types appearing 3+ times |
| midday | `../midday/` | `RUN_LOG.md` | — | 0-result windows (emails or Teams); fast-path rate ≥ 4/5 weekdays; flags count unchanged across many consecutive scans; tool calls > 12 |
| weekly-maint | `../weekly-maint/` | `RUN_LOG.md` | — | Same step finding nothing for 3+ consecutive runs; tool calls > 20; hypothesis/profile steps consistently empty; window gaps or duplicate-run skips |
| weekly-plan | `../weekly-plan/` | `RUN_LOG.md` | — | Python script failures; duplicate-run guard triggering unexpectedly; calendar gaps causing poor block placement; planning accuracy issues |

---

## Step 1: Read State

For the target task, read:

1. `[Task]/TASK.md` — current production run procedure
2. `[Task]/IMPROVEMENTS.md` — run counter, pending proposals, applied fixes
3. `[Task]/[Run log]` — last 20 entries (see Task Registry for filename)
4. `[Task]/ISSUES_LOG.md` — all entries with `Status: open`
5. Extra files listed in Task Registry (if any) — e.g., `LESSONS.md`, `TASK_REFERENCE.md`, `IMPROVEMENTS_DETAIL.md`, and `SIGNAL_LOG.md` for daily
6. Optional cross-task signals (read if time permits or [USER] requests):
   - Other tasks' IMPROVEMENTS.md for shared patterns worth mirroring

Note in the maintenance plan which files were read.

---

## Step 2: Catalog Issues

Collect all concrete problems from the sources read in Step 1. Group by source:

**From ISSUES_LOG.md (open entries):**
- List each open issue with its type, description, and step involved.

**From run log (anomalies):**
- Apply the task-specific anomaly signals from the Task Registry.
- For daily: also scan LESSONS.md for recurring mistake types (same type appearing ≥ 2 times); scan SIGNAL_LOG.md and group by type — surface any type appearing 3+ times.

**From IMPROVEMENTS.md (pending decisions):**
- List any PROP-NNN with status = PENDING — these need a decision before new proposals are raised.

Output a clean issue list with an ID (ISSUE-N) for each item. Each entry: source, type, description, severity (low / medium / high).

---

## Step 3: Analyze Opportunities

Review the target task's TASK.md holistically and the issue list from Step 2. Identify candidates in each category:

### 🐛 Bug fixes
Issues where the current procedure produces incorrect output, skips items, or fails silently. Source: ISSUES_LOG.md open entries, run log error patterns. Highest priority.

### 🔧 Minor improvements
Small procedural tweaks, connector parameter notes, formatting, or rule clarifications that can be applied directly to TASK.md without structural change. Low risk, low effort.

### 🔧 Major improvements
Structural changes to run steps, output templates, or multi-step logic. Higher risk — require [USER] approval via PROP-NNN.

### ✨ Minor new features
Small additions to existing flows (e.g., a new field in the run log, an additional fast-path condition). Low risk.

### ✨ Major new features
New steps, new output files, new data sources, or significant scope expansions. Require [USER] approval.

### ⚡ Refactoring
Changes that preserve behaviour but improve speed, tool-call efficiency, clarity, or Claude prompt optimization. Examples: merging redundant steps, simplifying decision trees, reducing conditional complexity.

For each candidate: note the category, the specific change, and the rationale. Do not generate PROP-NNNs yet — this step is analysis only.

---

## Step 4: Review Pending Proposals

Check `[Task]/IMPROVEMENTS.md` for any PROP-NNN with status = PENDING.

If PENDING proposals exist:
- Surface each one with its title, rationale, and proposed change.
- Ask [USER] to approve, reject, or defer before proceeding.
- Do **not** generate new proposals in Step 5 until the PENDING set is resolved.

If no PENDING proposals exist: proceed to Step 5.

---

## Step 5: Generate Proposals

For each candidate identified in Step 3 that warrants a PROP-NNN (structural changes, major items, or anything requiring [USER] approval before applying):

1. Assign the next sequential PROP-NNN ID (check `[Task]/IMPROVEMENTS.md` for the last used ID).
2. Write the proposal using this format:

```
### PROP-NNNN — [Short title]
- **Status:** PENDING
- **Raised:** YYYY-MM-DD
- **Type:** run-procedure | output-template | connector | schema | other
- **Category:** bug-fix | minor-improvement | major-improvement | minor-feature | major-feature | refactoring
- **Rationale:** [Why this improves the task]
- **Confidence:** LOW | MEDIUM | HIGH
- **Proposed change:** [Precise enough to apply without ambiguity]
- **Risk:** [What could go wrong]
- **Source issue:** [ISSUE-N or log entry date, if applicable]
```

3. For **minor improvements** that can be applied directly (no structural risk): apply immediately to `[Task]/TASK.md`, note as APPLIED — no PROP-NNN needed.

Append all new PROP-NNNs to `[Task]/IMPROVEMENTS.md` (single Write call).

**Priority bias:** Bug fixes > efficiency refactoring > minor improvements > major improvements > features.

---

## Step 6: Output MAINTENANCE_PLAN.md

Write `[Task]/MAINTENANCE_PLAN.md` — a human-readable summary for [USER] review.

If a previous MAINTENANCE_PLAN.md exists in that task folder: move it to `../../Actions/History/MAINTENANCE_PLAN_[Task]_YYYY-MM-DD.md` before writing the new one.

### Structure

```markdown
# [Task] Maintenance Plan — YYYY-MM-DD

## Summary
- Issues catalogued: N (N open in ISSUES_LOG.md, N from run log anomalies)
- Minor improvements applied directly: N
- Proposals generated: N (PROP-NNNN to PROP-MMMM)
- Proposals awaiting decision: N

## Open Issues
[Table: ID | Type | Description | Severity | Source]

## Proposals Generated This Run
[Table: PROP-NNN | Category | Title | Confidence]

## Pending Proposals (need decision)
[List any PENDING proposals, with approve/reject options]

## Applied Directly (no approval needed)
[List of minor fixes applied this run]
```

---

## Step 7: Update IMPROVEMENTS.md

In a single Write call, update `[Task]/IMPROVEMENTS.md`:
1. Add all new PROP-NNNs to the Proposals section.
2. Mark any ISSUES_LOG.md entries as resolved if a PROP-NNN addresses them (note the PROP-NNN ID).
3. Update `last_maintenance_date` in the Run Counter.

Do **not** apply APPROVED proposals here — that is done explicitly after [USER] approves.

---

## When `target: all`

Run Steps 1–7 for each task in this order: daily → midday → weekly-maint → weekly-plan.

After all four are processed, write a combined summary to `../../Actions/MAINTENANCE_REPORT.md`:

```markdown
# Maintenance Report — YYYY-MM-DD

## Summary
[2–3 sentences covering what was found across all tasks.]

## Per-Task Status
| Task | Issues Found | Proposals Generated | Applied Directly | Pending Proposals |
|------|-------------|--------------------|-----------------|--------------------|
| daily | N | N | N | N |
| midday | N | N | N | N |
| weekly-maint | N | N | N | N |
| weekly-plan | N | N | N | N |

## Needs Attention
[Items requiring [USER] input or decision. If none: "Nothing requires action."]
```
