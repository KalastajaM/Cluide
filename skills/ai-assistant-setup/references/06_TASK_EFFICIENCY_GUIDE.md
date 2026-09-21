# Assistant Task Efficiency Guide

> How to design and optimize the assistant tasks for minimal token consumption.
> Use as a one-time audit checklist when setting up a new task, or as a periodic optimization pass on an existing one.

> **Companion guides:** This guide covers efficiency (keeping token use low). [Guide 07](./07_TASK_LEARNING_GUIDE.md) covers self-improvement (making the task smarter over time). The ready-to-use template that implements Guide 07 is installed via Guide 07 Part 9.

> **Giving this guide to an assistant:**
> "Read 06_TASK_EFFICIENCY_GUIDE.md and audit my existing task at [path/to/TASK.md] for token efficiency. Apply the checklist and propose specific changes."
>
> **Faster alternative:** `tasks/audit-task-efficiency.md` runs this checklist end-to-end. `tasks/setup-scheduled-task.md` scaffolds a new task with efficiency patterns built in from the start.

---

## Core Principle

Every token the assistant reads or writes costs usage. The goal: the assistant only loads what it needs for the current run and only generates what it cannot delegate to a script.

The four main levers:
1. **Reduce what the assistant reads** — smaller instruction files, partial file reads
2. **Reduce what the assistant writes** — skip unchanged outputs, delegate fixed-format generation to scripts
3. **Reduce API calls** — triage before fetching full content
4. **Keep frequently-read files compact** — hard size limits on files loaded every run

---

## One-Time Audit Checklist

### 1. Split the instruction file (TASK.md)

The task instruction file is loaded on every run. Keep it to **~200 lines / ~3K tokens** of core procedure (target ~200 lines; hard cap 250). Move everything else to a `TASK_REFERENCE.md` that the assistant reads only when needed.

**Extract to TASK_REFERENCE.md:**
- JSON schemas and data formats
- Full output format templates (markdown/HTML)
- Backfill or migration strategies
- Error handling procedures
- Privacy and sensitivity guidelines
- Design principles and philosophy
- Anything that isn't a step in the run procedure

**In TASK.md, replace extracted sections with:**
> See `TASK_REFERENCE.md §Section Name`

**Rough targets:**
| File | Lines | When read |
|------|-------|-----------|
| TASK.md | ~200 target, 250 hard cap | Every run |
| TASK_REFERENCE.md | any | On demand |

These figures carry a tolerance band. See §6, *Tolerance: enforce the band, not the digit*.

---

### 2. Script fixed-format artifact generation

If the task generates a structured output file (HTML report, PDF, formatted document) from structured input (markdown, JSON), the assistant should not compose it from scratch every run. Write a script once; the assistant runs it.

Ask: *does the output format change between runs, or just the data?*
- Format is fixed, data varies → write a script
- Format varies based on run content → the assistant composes it

**Common candidates:**
- HTML reports from markdown briefings → Python script with fixed CSS
- Formatted PDFs from structured data → Python with reportlab or similar
- Excel/CSV exports from JSON → Python with openpyxl/csv
- Templated emails → Python with string templates

**Script contract:**
```
input:  path to source data file (markdown, JSON, etc.)
output: rendered artifact file + optional archive copy
usage:  python3 render.py [project_folder]
```

The assistant's step becomes: run the script, report the output path. On failure, fall back to composing directly and log the error.

---

### 3. Apply targeted edit policy for file updates

When the assistant updates a file it reads every run, it should use partial reads and targeted edits rather than full read + full write.

**Policy:**
- Use `Grep` to find the relevant section
- Use `Edit` for targeted changes
- Only do a full `Read` + `Write` when making structural changes (new sections, reordering, etc.)

**Saves:** ~1–3K tokens per file per update. Multiplies quickly if multiple files are updated per run.

**Exception:** files under ~30 lines — just read and write the whole thing.

---

### 4. Add conditional regeneration for view files

If the task generates a "human-readable view" of a machine-readable source of truth (e.g., PENDING_ACTIONS.md from pending_actions.json), only regenerate it when the source actually changed.

```
# In the run procedure:
Step N: Regenerate VIEW_FILE.md
  SKIP if SOURCE_FILE was not modified this run.
```

**Saves:** ~1–3K tokens per skipped regeneration on quiet runs.

---

### 5. Add two-pass triage for external data fetching

When fetching external data (emails, API responses, documents), many items are noise. Use a cheap first pass to classify, then fetch full content only for items that pass.

**Gmail pattern** (illustrative tool names — confirm yours with "what tools do you have?"):
- `gmail_search_messages` returns snippets — use those for triage
- Only call `gmail_read_message` for emails that pass an actionability filter
- Define skip conditions: known-noisy senders, promotional subject lines, routine automated notifications

**General pattern:**
```
Pass 1: fetch lightweight metadata / summaries (cheap)
Pass 2: fetch full content only for items flagged in Pass 1
```

**Saves:** proportional to noise ratio. High-volume, high-noise runs (10+ emails) see the most benefit.

---

### 6. Enforce hard size limits on always-loaded files

Any file loaded every run must have a hard size cap. Without one, these files grow over time and compound the token cost of every future run.

**Apply to:** summary files, state files, any "read every run" file.

```
# In the update instructions for that file:
Hard limit: N lines / ~M tokens. Trim before writing.
Trim strategy: compress older entries, remove superseded items, archive resolved items.
```

**Recommended caps:**
| File type | Cap |
|-----------|-----|
| Profile summary | 40 lines / ~600 tokens |
| Run log (RUN_LOG.md) | last 20 full entries; archive older ones once past ~30 (see below) |
| Pending actions summary | proportional to open item count; archive resolved promptly |

**Run log format and retention:**
Each `RUN_LOG.md` entry uses the header `## [YYYY-MM-DD] Run #N` and includes a `**Tokens (est.):** ~XK input, ~YK output` line. Keep the last 20 entries in full — [Guide 10](./10_COST_PERFORMANCE.md)'s drift monitoring compares recent runs against runs 16–20, so it needs them. Once the file exceeds ~30 entries, archive older ones to `RUN_LOG_ARCHIVE.md`. Tasks that only ever need to debug the most recent run can keep a `LAST_RUN.md` instead — cheaper, but it gives up cross-run pattern detection and Guide 10's monitoring.

**Tolerance: enforce the band, not the digit.**

Every size figure in this guide, and every one the `audit-*` tasks check against, is a target with a tolerance band of roughly 5%. A 260-line TASK.md is inside the band; a 310-line one is not. Do not raise a finding, block a merge, or restructure a file to shave four lines off a cap. These caps exist to hold down the cost of files that load on every run, and a 2% overshoot does not measurably change that, while treating the number as exact produces findings that are noise — and a check that fires on noise is one people learn to skip.

The band is not licence to drift. A file that lands just inside tolerance twice running is growing, and the answer is the split the cap was pointing at, not a third round of trimming.

**Technical cliffs are hard caps and get no tolerance.** Where a number is enforced by something outside the project — a loader, an API, a context window — one line past it is not slightly worse, it is a different outcome. The instance in this framework is native memory's auto-load limit: only the first 200 lines / 25KB of `MEMORY.md` reaches a session, so line 201 is invisible rather than expensive (see [Guide 04](./04_MEMORY_AND_PROFILE.md)). Treat every externally enforced limit the same way. If you cannot name what enforces a number, it is a target and the band applies.

---

### 7. Add run deduplication

If the task can run multiple times per day, add duplicate detection to avoid redundant full runs.

```
Step 0: Record run start timestamp
Step 1: Check if a full run already completed today
  → If yes: use that run's timestamp as the fetch boundary (not yesterday)
  → If < 30 min ago: skip entirely
```

---

## Recurring Optimization Pass

Run this every 20–30 task executions, or whenever you notice usage spikes.

### Checklist

**Instruction file drift**
- [ ] Is TASK.md still within the ~200-line target (250 hard cap)? If not, extract the new additions to TASK_REFERENCE.md.
- [ ] Are there steps in TASK.md that are never executed? Flag them for removal or move to reference.

**Always-loaded files**
- [ ] Is PROFILE_SUMMARY.md (or equivalent) still within its line cap? If not, trim.
- [ ] Is the run log still compact, or have entries accumulated beyond ~30 without being archived?

**Output generation**
- [ ] Are there new structured output files that could be scripted? (Apply checklist item 2.)
- [ ] Is any existing script producing errors and falling back to the assistant generation? Fix the script.

**Fetch efficiency**
- [ ] Are there new high-frequency senders that are always noise? Add them to the Noise Filters list (see `templates/TASK_TEMPLATE/IMPROVEMENTS.md` and [Guide 07 Part 9](./07_TASK_LEARNING_GUIDE.md)).
- [ ] Is the two-pass triage filter accurate? False negatives (missed actionable items) → loosen. False positives (noise fetched in full) → tighten.

**Edit efficiency**
- [ ] Are there profile/state files being fully read and rewritten for minor changes? Apply targeted edit policy.
- [ ] Are view files being regenerated even when their source didn't change? Add skip condition.

---

## Quick Estimation: Token Cost Per Run

Use this to roughly estimate per-run cost and identify the highest-leverage improvements:

| Component | Rough cost | Notes |
|-----------|------------|-------|
| Task instruction file | ~15 tokens/line | Loaded every run |
| Each "read every run" file | ~15 tokens/line | |
| Each external API fetch (full) | 200–2000 tokens | Varies by content size |
| Each file write (generated output) | ~15 tokens/line | |
| Script execution | Depends on call and output size | Keep output compact; this is not the script's CPU or API bill |

**Example:** A 500-line TASK.md costs ~7.5K tokens per run just to load. Splitting it to 200 lines saves ~4.5K per run — which over 50 runs saves 225K tokens.

---

## How Scheduled Tasks Are Triggered

Choose by trigger: a recurring schedule needs a scheduler, session initialization needs a lifecycle hook, and a temporary watch needs a task that stays active or a supported follow-up mechanism. These are different lifetimes. Codex also documents lifecycle hooks; see [Guide 35 §9](./35_DUAL_PLATFORM_PROJECTS.md#9-platform-facts). Use the selected host's configuration and test the event; the Claude hook JSON below is not an OpenAI installation recipe.

Choose the owning execution surface before registering anything. The procedure can be shared, but one job has one active scheduler owner, stable identity, timezone, input revision and output destination. Native registrations stay on that platform. An interval is not a lock: overlapping runs need an atomic claim or an execution service that prevents concurrent writes.

---

### OpenAI: Scheduled Tasks with Local or Cloud Inputs

OpenAI uses two names: ChatGPT **scheduled tasks** (the Scheduled page in the ChatGPT sidebar) run in ChatGPT, and **Codex automations** run in Codex. Prepare and manually test the task first. In the ChatGPT app, use Scheduled or the exposed scheduling tool to create the registration; whether the Codex CLI and IDE offer schedule management is not documented, so prepare the workflow there and register it where the management interface is actually present. Scheduled tasks can use plugins and skills. Choose a recurring task in the current chat for a follow-up that needs its context, or a standalone task when each run should start from a saved prompt, following the host's available controls.

A desktop task that needs local files needs the computer on and the app running; it runs in the project directory or an isolated worktree. Scheduled runs are unattended: they use your default sandbox settings and `approval_policy = "never"` where organisational policy permits, so the task must not depend on an approval prompt. A task created in a ChatGPT project cannot access that project's uploaded files or files stored in the project — do not plan a scheduled job around project uploads. On web and mobile, eligible plans can also trigger tasks from supported app events (event-triggered tasks need Plus or higher). Record which mode owns the job and verify the first run's inputs and saved output. A notification alone does not prove successful execution. Checked 2026-09-21: [Codex automations](https://learn.chatgpt.com/codex/automations) and the help article [Scheduled tasks in ChatGPT](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt).

For a transfer, pause the old schedule and confirm no run is in flight, test the new owner once with outbound effects disabled, then remove the old registration and activate the new schedule. Keep the same deduplication key across the transfer. Guide 35 (in the Cluide guide set) carries the full handoff.

---

### Option A: Cowork Scheduled Tasks

Cowork's scheduled tasks are a built-in feature: they run on a schedule **independently of any open Claude session** — no session needed, no manual trigger. Since July 2026 they run cloud-side, so they fire even with your computer asleep — except a task that needs local files or apps, which still runs on your computer and needs it awake. When the model is unreachable a run is retried automatically after 5, 15 and 30 minutes. The task form also carries a 1M-context model row for tasks that need one. This is the proper approach for daily digests, automated monitoring tasks, and anything that should run reliably on a fixed schedule.

**To set up a scheduled task, just ask the assistant in natural language:**
> "Run this task every weekday at 7am."

The assistant will configure the task and set the schedule. You can also ask the assistant to list, update, or stop your scheduled tasks.

This approach avoids the main problem with SessionStart hooks: tasks running multiple times if you open several sessions in a day.

---

### Option B: Claude Code Routines (cloud, for repo-attached automation)

Routines are Claude Code's own cloud scheduled tasks, set up on the web. They run on Anthropic's infrastructure with no local machine involved, and can be triggered by a schedule, a GitHub event, or an API call. The minimum interval is one hour. Reach for these when the work belongs to a repository rather than to a Cowork project — a nightly check on a branch, a response to a pull request.

---

<a id="option-c-loop-session-scoped-for-work-you-are-watching"></a>

### Option C: Claude Code `/loop` (session-scoped, for work you are watching)

`/loop` sets up a recurring task inside the current CLI session: `/loop 5m <prompt>` for a fixed interval, `/loop <prompt>` to let Claude pace itself, `/loop` alone for the built-in maintenance prompt (replaceable via `.claude/loop.md`). It dies with the session, so it is the wrong tool for a daily digest and the right one for "keep checking this while I work".

---

<a id="option-d-sessionstart-hooks-simpler-for-session-triggered-automation"></a>

### Option D: Claude Code SessionStart Hooks (simpler, for session-triggered automation)

Hooks are shell commands that fire automatically in response to Claude Code events. Configure them in `~/.claude/settings.json` (global) or `.claude/settings.json` (project-level).

**SessionStart** fires every time a new Claude Code session opens — useful for lightweight pre-session setup (git snapshots, loading context) rather than full task execution.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cd /path/to/project && git add -A && git commit -m 'pre-session snapshot' 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Other hook events:**
- **PreToolUse** — fires before a tool runs. Useful for validation or logging. Unlike CLAUDE.md instructions (guidance Claude can overlook), a PreToolUse hook is an enforcement layer — it can hard-block a tool call.
- **PostToolUse** — fires after a tool completes. Useful for follow-up actions (e.g., after a file write, trigger a view regeneration).
- **PostToolUseFailure** — fires when a tool call fails. Useful for logging what actually breaks in autonomous runs.
- **UserPromptSubmit** — fires when a prompt is submitted, before the assistant processes it. Useful for injecting context or validating input.
- **Stop** — fires when the assistant ends a response. A Stop hook can return `additionalContext`, which pushes text back into the session rather than only blocking or logging.
- **SubagentStart / SubagentStop** — fire around each delegated subagent. Useful for tracking fan-out cost and for logging what workers returned.
- **SessionEnd** — fires when a session closes. Useful for cleanup or end-of-session logging.
- **Setup** — fires for `claude -p --init` and `--maintenance` runs, which is where scheduled and headless work starts.
- **InstructionsLoaded** — fires once the instruction files are in. It logs which files loaded and why, which is the fastest way to answer "did my CLAUDE.md actually load?" ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)).
- **PreModelSwitch / PostModelSwitch** — fire around a model change within a session.
- **PreCompact** — fires before context compaction. Useful for saving state that would otherwise be summarized away.
- **Notification** — fires when the assistant sends a notification.

**Hook practical notes:**
- SessionStart fires once per session. Multiple sessions per day = multiple hook runs. Add deduplication (checklist item 7) if running full tasks via hooks.
- The `matcher` field filters by context. Leave it empty (`""`) to fire on all sessions.
- For git pre-session snapshots, the hook approach is the right fit. See [Guide 11 — Git Integration](./11_GIT_INTEGRATION.md).

For the full hooks reference: [Claude Code documentation on hooks](https://code.claude.com/docs/en/hooks).

---

## Anti-Patterns to Avoid

**Full-file read + write for small updates.** If you're changing 2 lines in a 200-line file, use Grep + Edit, not Read + Write.

**Regenerating unchanged outputs.** If the source didn't change, don't regenerate the view.

**Composing fixed-format artifacts.** If the format is the same every run, write it once as a script.

**Unbounded files.** Any file that grows without a trim/archive policy will become expensive over time.

**Fetching full content to classify.** Use cheap metadata (snippets, summaries, subject lines) to decide what's worth a full fetch.

**Loading reference material preemptively.** Don't load schemas, format templates, or principles at the start of every run "just in case." Load them when actually needed.
