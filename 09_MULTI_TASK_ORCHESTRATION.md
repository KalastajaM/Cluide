# Multi-Task Orchestration

*Last reviewed: April 2026*

> When multiple scheduled tasks share data, run in a specific order, or produce a combined output, you need orchestration. This guide covers how to coordinate tasks without overengineering.

> **Companion guides:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) for keeping orchestrated tasks efficient. [Guide 07](./07_TASK_LEARNING_GUIDE.md) for self-improvement across coordinated tasks. [Guide 10](./10_COST_PERFORMANCE.md) for monitoring costs when multiple tasks run daily.

> **Giving this guide to Claude:**
> "Read 09_MULTI_TASK_ORCHESTRATION.md and help me coordinate my existing tasks at [paths]. They need to [share data / run in order / produce a combined output]."

---

## When You Need This

Most setups don't need orchestration. Use this decision table:

| Situation | What to use |
|---|---|
| One task, runs on a schedule, self-contained | Single task — no orchestration needed |
| Two tasks that happen to run at different times, no shared data | Independent tasks — no orchestration needed |
| Task A produces output that Task B consumes | **Sequential chain** — this guide |
| Multiple tasks run independently but share a state file | **Shared state** — this guide |
| Task C can only run after both Task A and Task B have finished | **Dependency graph** — this guide |
| A single complex task that does too many things | Split into a skill with phases, not separate tasks |

**Rule of thumb:** if your tasks don't read each other's output and don't need to run in a specific order, you don't need this guide. Run them independently.

---

## Three Orchestration Patterns

### Pattern 1: Sequential Chain

Task A runs first and writes output. Task B runs second and reads that output.

```
[Task A: Email Digest] → writes action_items.json → [Task B: Briefing Composer]
```

**Implementation:**

1. Task A writes its output to a known location with a predictable name:
   ```
   shared/action_items_2026-04-10.json
   ```

2. Task B's Step 1 reads from that location:
   ```markdown
   Step 1: Read `shared/action_items_[today's date].json`.
   If the file doesn't exist or is older than 24 hours, skip and note:
   "Email digest has not run yet today — skipping action items."
   ```

3. Schedule Task A to run before Task B with enough gap (e.g., Task A at 07:00, Task B at 07:30).

**Key rule:** Task B must handle the case where Task A hasn't run yet. Never assume the upstream task succeeded. Check for the file and its freshness.

### Pattern 2: Shared State

Multiple tasks read and write a shared state file. Each task updates its section; no task overwrites another's.

```
[Email Digest]  ──→  shared/STATE.json  ←──  [Calendar Check]
                          ↑
                    [Pipeline Tracker]
```

**The STATE.json convention:**

```json
{
  "last_updated_by": "email-digest",
  "last_updated_at": "2026-04-10T07:15:00",
  "email_digest": {
    "action_items": ["Reply to client X", "Review proposal Y"],
    "updated_at": "2026-04-10T07:15:00"
  },
  "calendar": {
    "today_events": 3,
    "conflicts": [],
    "updated_at": "2026-04-10T07:20:00"
  }
}
```

**Rules for shared state:**
- Each task owns its own section (keyed by task name)
- No task modifies another task's section
- Always include `updated_at` timestamps so consumers know how fresh the data is
- Read the full file before writing — use targeted edits, not full overwrites
- Keep the file small (<100 lines / <2K tokens) — it's read on every run of every task

### Pattern 3: Dependency Graph

Task C depends on both Task A and Task B completing first.

**Use an orchestrator task** rather than complex scheduling. The orchestrator is a lightweight task that checks prerequisites and dispatches work:

```markdown
# ORCHESTRATOR.md

## Purpose
Coordinate the morning workflow. Run at 07:30 daily.

## Steps

Step 1: Check prerequisites.
  - Read `shared/email_digest_[today].json`. If missing → log "Email digest not ready" and stop.
  - Read `shared/calendar_[today].json`. If missing → log "Calendar check not ready" and stop.

Step 2: Both inputs are ready. Proceed with briefing generation.
  - Read both input files.
  - Generate the combined morning briefing.
  - Write to `output/briefing_[today].md`.

Step 3: Log completion to RUN_LOG.md with metrics.
```

**Timing:** schedule upstream tasks early enough that they finish before the orchestrator runs. Leave buffer. If email digest takes ~5 minutes and calendar check takes ~2 minutes, schedule them at 07:00 and the orchestrator at 07:15 (not 07:07).

---

## Data Passing Between Tasks

### File-Based Handoff

The simplest and most reliable method. Task A writes a file; Task B reads it.

**Naming convention:** `shared/[task-name]_[date].json` (or `.md`). Include the date so stale data is obvious.

**Schema contracts:** document what the output looks like in a `shared/SCHEMA.md`:

```markdown
# Shared Data Schema

## email_digest_[date].json
Written by: email-digest task
Read by: briefing-composer task

Fields:
- action_items: array of strings — items requiring user action
- summary: string — 2-3 sentence overview of today's email
- flagged_senders: array of strings — senders marked as important
```

This prevents silent breakage when one task changes its output format. When Task A's schema changes, update `SCHEMA.md` and verify all consumers still work.

### What Belongs in Shared State vs. Per-Task State

| Shared state | Per-task state |
|---|---|
| Data another task needs to consume | Intermediate working data |
| Final outputs and summaries | Draft outputs being refined |
| Completion markers and timestamps | Run-specific logs |
| Cross-task action items | Task-internal metrics |

Keep shared state minimal. If only one task reads a piece of data, it belongs in that task's own folder — not in `shared/`.

---

## Scheduling Orchestrated Runs

### Avoiding Collisions

If two tasks write to `STATE.json` at the same time, one write can overwrite the other. Prevent this:

- **Stagger schedules** with at least 10-minute gaps between tasks that write to the same file
- **Use separate output files** per task (the `shared/[task-name]_[date].json` pattern) instead of a single shared file when possible
- **Use the orchestrator pattern** for anything more complex than two tasks -- it serializes execution naturally

### Timing Template

A typical morning workflow:

| Time | Task | Writes |
|---|---|---|
| 07:00 | Email digest | `shared/email_digest_2026-04-10.json` |
| 07:05 | Calendar check | `shared/calendar_2026-04-10.json` |
| 07:15 | Orchestrator / Briefing | `output/briefing_2026-04-10.md` |

Schedule conservatively. A task that usually takes 3 minutes might take 10 on a busy day.

---

## Failure Handling

Orchestrated tasks need explicit failure strategies. When an upstream task fails or produces bad output, downstream tasks must not silently break.

**Three failure modes to handle:**

1. **Missing output.** The upstream task did not run or did not write its output file. Downstream tasks should check for file existence and freshness (see Pattern 1 above), then either skip that input gracefully or stop with a clear log message.

2. **Partial or malformed output.** The upstream task ran but wrote incomplete or invalid data. Validate the schema before consuming: check that required fields exist and contain expected types. Log what was wrong and fall back.

3. **Stale output.** The file exists but is from a previous day. Freshness checks (comparing `updated_at` or the filename date against today) catch this. Treat stale data the same as missing data.

**Logging failures.** Every orchestrated task should log its outcome (success, skipped, or failed with reason) to `RUN_LOG.md`. When the orchestrator detects a failure, include which upstream task was the cause so debugging is straightforward.

---

## Real Example: Morning Workflow

Three tasks coordinated into a daily briefing:

**Task A — Email Digest** (runs 07:00)
- Reads Gmail via MCP
- Writes `shared/email_digest_[date].json` with action items, flagged senders, summary

**Task B — Calendar Check** (runs 07:05)
- Reads Google Calendar via MCP
- Writes `shared/calendar_[date].json` with today's events, conflicts, free slots

**Task C — Briefing Composer** (runs 07:15)
- Reads both shared files
- Reads `PROFILE_SUMMARY.md` for user context
- Generates `output/briefing_[date].md`: combined summary, prioritised action items, schedule overview
- Falls back gracefully if either input is missing

The orchestrator (Task C) handles missing inputs:
```markdown
If email digest file is missing: include "[Email digest not available — check task logs]"
in the briefing and continue with calendar data only.
```

---

## Anti-Patterns

**Implicit ordering.** Tasks that depend on running in a specific order but don't check for it. If Task B assumes Task A has run because "it's scheduled first," it breaks when Task A fails or runs late. Always check for the expected input.

**Shared files without size limits.** A `STATE.json` that grows unbounded because tasks append but never trim. Set a max size and archive old data.

**Circular dependencies.** Task A reads Task B's output and Task B reads Task A's output. This creates an ordering paradox. Redesign: extract the shared data into a separate state file that both tasks read from but neither exclusively owns.

**Over-orchestrating.** Two independent tasks that happen to run at the same time don't need an orchestrator. Only add coordination when tasks genuinely depend on each other's output.

**Giant shared state.** Putting everything in one `STATE.json`. If it exceeds 100 lines, you are probably conflating shared state with per-task state. Split.

---

## Checklist

When setting up multi-task orchestration:

- [ ] Confirm you actually need orchestration (see decision table)
- [ ] Choose the right pattern (sequential chain, shared state, or dependency graph)
- [ ] Create `shared/` directory with `SCHEMA.md` documenting data contracts
- [ ] Add freshness checks to every task that reads shared data
- [ ] Stagger schedules with 10+ minute gaps between writers
- [ ] Add fallback handling for missing, malformed, and stale inputs in downstream tasks
- [ ] Log task outcomes (success/skipped/failed) to `RUN_LOG.md`
- [ ] Set up cost monitoring ([Guide 10](./10_COST_PERFORMANCE.md)) across all coordinated tasks
