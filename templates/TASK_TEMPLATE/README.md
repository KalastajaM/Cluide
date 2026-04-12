# Task Template — Setup Instructions

> A ready-to-copy starter for self-learning, token-efficient Claude tasks.
> Implements the patterns from Guide 06 (efficiency) and Guide 07 (self-improvement).

---

## What's in This Folder

| File | Purpose | Loaded |
|------|---------|--------|
| `TASK.md` | Run procedure — the task's "brain" | Every run |
| `IMPROVEMENTS.md` | Self-improvement log, run counter, proposals | Every run |
| `KNOWLEDGE_SUMMARY.md` | Compact context that grows smarter over time | Every run |
| `RUN_LOG.md` | Append-only history of every run | Last 2 entries |

Two optional files can be added as the task matures:
- `TASK_REFERENCE.md` — schemas, format templates, and edge-case rules — loaded on demand, not every run.
- `LESSONS.md` — append-only reasoning history: why each fix was made, root causes, connector quirks. Useful when IMPROVEMENTS.md Applied Fixes is growing and the *why* behind changes is getting lost. See Guide 07 Part 6.

---

## How to Create a New Task

### Step 1 — Copy this folder

Copy `TASK_TEMPLATE/` to your task's location and rename it. Example:

```
MyProject/
└── DailyDigest-Task/
    ├── TASK.md
    ├── IMPROVEMENTS.md
    ├── KNOWLEDGE_SUMMARY.md
    └── RUN_LOG.md
```

### Step 2 — Fill in the placeholders

Open `TASK.md` and replace every `[PLACEHOLDER]`. Search for `[` to find them all. Key ones:

- `[TASK NAME]` — appears in all four files; replace everywhere
- Purpose paragraph — be specific about what the task monitors and produces
- Step 2 (Fetch External Data) — define your noise patterns and recency skip conditions
- Step 3 (Primary Work) — this is the domain-specific core of your task
- Rules section — add any hard constraints for your domain

### Step 3 — Set the refactor threshold

In `IMPROVEMENTS.md`, set `refactor_threshold`:
- Daily runs → 25–30
- Weekly runs → 10–15
- Multiple times per day → 15–20

### Step 4 — Delete the template instructions

Remove the "How to Use This Template" section and the template note at the top of `TASK.md`. The task should read as a clean run procedure, not a template.

### Step 5 — Run it manually first

Before scheduling, trigger one manual run and verify:
- The fast-path check works correctly (doesn't skip when it shouldn't)
- The output file is created in the right location
- The run log and IMPROVEMENTS.md counters increment correctly
- TASK.md is within the 250-line target (trim if not)

### Step 6 — Schedule it

Use the schedule skill or task scheduler. Suggested prompt:

> "Schedule [MyTask] to run [daily at 8am]. The task file is at [path/to/MyTask/TASK.md]."

---

## Key Design Decisions to Make Upfront

**What triggers a fast-path skip?** Define the conditions under which the task should exit early because there's nothing meaningful to process. Getting this right from the start saves the most tokens.

**What is always noise?** Identify 2–3 sources or patterns that will never produce actionable output. Add them to the Noise Filters section of `IMPROVEMENTS.md` immediately — don't wait for 5 observations if you already know.

**What does the task need to remember?** Seed `KNOWLEDGE_SUMMARY.md` with any context you already know: relevant people, known system quirks, standing rules. Don't start from zero if you don't have to.

**What's the output?** Decide upfront whether output is a regenerated file (use conditional regeneration), a script-rendered artifact (write the script once), or a direct Claude composition. Scripted and conditional output are significantly cheaper at scale.

---

## Giving This Template to Claude

To have Claude set up a new task for you:

> "Read TASK_TEMPLATE/README.md, then copy the TASK_TEMPLATE folder to [destination], rename it [task name], and fill in all the placeholders based on the following: [describe what your task should do, what data sources it uses, what output it produces, and any domain-specific rules]."

To add self-improvement to an existing task:

> "Read 07_TASK_LEARNING_GUIDE.md and add the self-improvement system to my task at [path/to/TASK.md]. Set up an IMPROVEMENTS.md using TASK_TEMPLATE/IMPROVEMENTS.md as the base."

To audit an existing task for efficiency:

> "Read 06_TASK_EFFICIENCY_GUIDE.md and audit my task at [path/to/TASK.md] for token efficiency. Apply the checklist and propose specific changes."

---

## Size Targets (enforce from run 1)

| File | Hard limit | What to do when exceeded |
|------|-----------|--------------------------|
| TASK.md | 250 lines | Extract to TASK_REFERENCE.md; propose in IMPROVEMENTS.md |
| KNOWLEDGE_SUMMARY.md | 40 lines | Trim before writing — compress, archive, or remove stale entries |
| RUN_LOG.md (active section) | 3 full entries | Compress older entries to 1-line summaries |
| IMPROVEMENTS.md Applied Fixes | 10 entries | Rotate oldest to Archived Fixes |

---

## What Makes a Task Self-Learning

The self-improvement loop in Step 6 of TASK.md does the work. Each run, the task:

1. **Detects signals** — corrections, ignored proposals, failed queries, repeated patterns
2. **Acts on them** — applies low-risk fixes immediately; proposes larger changes for review
3. **Tracks what it learns** — in KNOWLEDGE_SUMMARY.md (context) and IMPROVEMENTS.md (changes)
4. **Refactors periodically** — structural cleanup every N runs to prevent drift and bloat

The result is a task that makes the same mistake at most twice: once to detect it, once to fix it.

See [Guide 07](../../07_TASK_LEARNING_GUIDE.md) for the full framework behind this system.
