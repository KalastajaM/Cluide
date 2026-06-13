# Task: Setup Multi-Task Orchestration

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-orchestration.md`
> **Source guide:** `09_MULTI_TASK_ORCHESTRATION.md`

## Purpose
Wire coordination between existing scheduled tasks per Guide 09: a shared-state convention, run-order and dependency handling, documented handoff files between feeder tasks and a synthesis task, and failure handling so downstream tasks never silently break.

**Prerequisites:** Two or more tasks with working `TASK.md` files. If you only have one task, you don't need orchestration — stop here.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Identify the tasks and the coupling

Ask: "Which tasks should I coordinate? Provide the paths to their task folders."

Read each `TASK.md`. Then establish what actually couples them:

> 1. What is the relationship between these tasks?
>    Use `AskUserQuestion` with buttons: `A feeds B (sequential)` / `They share state` / `C needs both A and B (dependency)` / `Not sure`
> 2. What data needs to pass between them? (e.g. action items, a daily summary, a status flag)
> 3. When does each task run today, and is the schedule fixed?

**Check the decision table first** (Guide 09 §When You Need This). If the tasks don't read each other's output and don't need a specific order, say so plainly: "These tasks are independent — no orchestration needed. Run them on their own schedules." and stop.

### Step 2 — Propose the pattern

Based on the answers, propose exactly one of the three patterns:

| Coupling | Pattern | What gets built |
|---|---|---|
| A's output → B's input | **Sequential chain** | Dated handoff file + freshness check in B |
| Several tasks, common state | **Shared state** | `shared/STATE.json` with per-task sections |
| C waits on A and B | **Dependency graph** | Lightweight orchestrator task that checks prerequisites |

Present the proposal before writing anything:
```
Orchestration Plan
──────────────────
Pattern: [sequential chain / shared state / dependency graph]
Shared directory: shared/
Handoff files: shared/[task-name]_[date].json  (written by: X, read by: Y)
Schema contract: shared/SCHEMA.md
Schedule: [task A at HH:MM] → [10+ min gap] → [task B at HH:MM]
Edits to TASK.md files: [list of insertions per task]
```

Use `AskUserQuestion` with buttons: `Apply as proposed` / `Adjust first` / `Cancel`

### Step 3 — Create the shared-state scaffolding

1. Create the `shared/` directory at the project root (or next to the task folders — confirm location).

2. Write `shared/SCHEMA.md` documenting every handoff file:

```markdown
# Shared Data Schema

## [task-name]_[date].json
Written by: [feeder task]
Read by: [consumer task(s)]

Fields:
- [field]: [type] — [meaning]
- updated_at: ISO 8601 timestamp — freshness check

When this schema changes: update this file first, then verify all consumers.
```

3. **If shared state (Pattern 2):** also write `shared/STATE.json` with one section per task:

```json
{
  "last_updated_by": null,
  "[task-a-name]": { "updated_at": null },
  "[task-b-name]": { "updated_at": null }
}
```

Rules to record in SCHEMA.md: each task owns its own section; no task modifies another's; always set `updated_at`; targeted edits, not full overwrites; keep under 100 lines.

### Step 4 — Wire the tasks

Show each insertion as a diff and get approval before writing.

**Feeder tasks** — add as the final output step:

```markdown
Write the handoff file `shared/[task-name]_[today YYYY-MM-DD].json` per `shared/SCHEMA.md`.
Set `updated_at` to now. Log "handoff written" in RUN_LOG.md.
```

**Consumer / synthesis tasks** — add as an early step:

```markdown
Read `shared/[feeder-name]_[today]​.json`. Freshness check: if the file is missing,
malformed (required fields absent), or dated before today — treat as unavailable.
Note "[feeder] not available — continuing without it" in the output, or stop with a
clear log message if the input is essential. Never assume the upstream task succeeded.
```

**If dependency graph (Pattern 3):** create `tasks/orchestrator/TASK.md` — a lean task that checks each prerequisite file, stops with a named cause if any is missing, and otherwise runs the synthesis and logs the outcome (success / skipped / failed + which upstream caused it) to its RUN_LOG.md. Follow the ORCHESTRATOR.md skeleton in Guide 09 §Pattern 3.

### Step 5 — Set the schedule

Propose run times with collision margins (Guide 09 §Scheduling Orchestrated Runs):
- Feeders first, 10+ minute gaps between tasks writing to the same file
- Orchestrator/synthesis last, with buffer for slow runs (a 3-minute task can take 10 on a busy day)

Present a timing table and remind the user to update their scheduled tasks (Cowork's scheduled-tasks feature / the `schedule` skill) to match.

### Step 6 — Confirm

Tell the user:
- The pattern chosen and why
- Files created (`shared/SCHEMA.md`, `STATE.json` or handoff conventions, orchestrator task if any)
- The insertions made to each TASK.md
- The agreed schedule
- "Test it once end-to-end: run the feeder(s) manually, then the consumer, and check the handoff files and RUN_LOG entries. To watch what the coordination costs, run `tasks/audit-cost.md` across the coordinated tasks after a week."
