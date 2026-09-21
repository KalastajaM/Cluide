# Task: Setup Scheduled Task

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/setup-scheduled-task.md`
> **Source guides:** `06_TASK_EFFICIENCY_GUIDE.md`, `07_TASK_LEARNING_GUIDE.md` (incl. Part 9)

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

Choose the owning scheduler before scaffolding: Cowork, Codex app, another explicitly supported scheduler, or manual. Record stable job ID, definition path/revision, owning surface, timezone, schedule, output/state paths and duplicate-run key in a project owner table. Inventory existing registrations on all used surfaces before creating one; update the matching job instead of duplicating it.

**Codex app:** after writing/reviewing the files, use the exposed automation tool and its current schema to register the requested schedule against the intended project/task. Follow the runtime's heartbeat-versus-standalone rule; do not write scheduler storage directly. Verify the returned registration and one safe fixture run. If the tool is absent, provide the exact prompt/schedule/project for the native scheduling UI and mark registration pending.

**ChatGPT:** the feature is ChatGPT scheduled tasks (sidebar page Scheduled); Codex automations are the Codex-side equivalent. Verify whether the task can access all required sources/tools, and only register when those capabilities support this workflow. A desktop run that needs local files needs the computer on and the app running, and runs in the project directory or an isolated worktree. Runs are unattended — default sandbox settings and `approval_policy = "never"` where organisational policy permits — so the generated `TASK.md` must not wait on an approval. A task created in a ChatGPT project cannot access that project's uploaded files or files stored in the project, so uploading `TASK.md` neither registers it nor gives the run its inputs; a local file-processing task with no folder access stays on Codex/Cowork or manual execution. On web and mobile, eligible plans can also trigger tasks from supported app events (Plus or higher). Whether the Codex CLI and IDE offer schedule management is not documented.

**Cowork:** use the available native scheduler tool/UI, verify the project folder and connectors, and inspect one fixture run. **Claude Code SessionStart** below is a session reminder, not a time-based scheduler.

For a handoff, pause the old trigger and confirm no run is active; create the new registration paused or with future activation, verify an isolated run, then delete the old registration and activate exactly one owner. Record IDs, timezone, cutover, verification and rollback plan. Never leave both triggers live while testing. Generated `TASK.md` Step 0 must check the owner, run key and existing in-progress/completed record before doing work; use an atomic claim where available, otherwise serialize runners. File-backed state is explicit input, not native memory.

See [Codex automations](https://learn.chatgpt.com/codex/automations) and the help article [Scheduled tasks in ChatGPT](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt) (checked 2026-09-21); verify the actual runtime before registration.

## Purpose
Scaffold a new scheduled task from scratch with efficiency and self-improvement patterns built in from run 1: a lean `TASK.md`, a `TASK_REFERENCE.md` for detail content, a `RUN_LOG.md`, and an `IMPROVEMENTS.md`. The result is a task ready to run and improve from its first execution.

**For adding self-improvement to an *existing* task:** use `tasks/setup-self-improving-task.md` instead.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

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
>    Use the available question tool, or ask in chat: `Yes` / `No`
> 8. If yes: how often does it run? (This sets the refactor threshold — daily → 25, weekly → 10.)
>    Use the available question tool, or ask in chat: `Daily` / `Weekly` / `On demand`

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

Verify this job’s owning scheduler and timezone. Claim its run key; skip if already complete or in progress.
[Only if self-improvement is enabled:]
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

If self-improvement is enabled, run the Self-Improvement section below (A–D). Always append an entry to `RUN_LOG.md` in the canonical format (Guide 06/10):

## [YYYY-MM-DD] Run #[N]
**Duration:** ~[X] min
**Tokens (est.):** ~[X]K input, ~[Y]K output
**Notes:** [one-line summary of what happened this run]

Keep the last 20 entries in full; once the file exceeds ~30 entries, archive older ones to `RUN_LOG_ARCHIVE.md`.

---

## Self-Improvement (A–D)

[The A–D instructions live here in TASK.md — IMPROVEMENTS.md stores state only (Guide 07 Part 9).
Copy this section from the canonical version in `templates/TASK_TEMPLATE/TASK.md` Step 6. Outside a
Cluide checkout, `tasks/setup-self-improving-task.md` Step 4 carries the same block verbatim — a
mirror, not a shorter variant. If the copy you can reach lacks the refactor-trigger table or the
LESSONS.md line, it has drifted: say so rather than shipping the shorter one.
A: Feedback Signal Detection → B: Refactor Trigger Check → C: Auto-apply vs. Propose → D: Update IMPROVEMENTS.md]
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

*Entry format (canonical — Guide 06/10; keep last 20 full entries, archive past ~30 to RUN_LOG_ARCHIVE.md):*

## [YYYY-MM-DD] Run #[N]
**Duration:** ~[X] min
**Tokens (est.):** ~[X]K input, ~[Y]K output
**Notes:** [one-line summary]
```

#### `tasks/[name]/IMPROVEMENTS.md` (if self-improvement was requested)

Copy `templates/TASK_TEMPLATE/IMPROVEMENTS.md` **verbatim**. If that file is not available (this task was copied to another project), use the inline copy in `tasks/setup-self-improving-task.md` Step 3 — it is a verbatim copy of the same template. Then customise:
- `total_runs: 0`, `runs_since_last_refactor: 0`
- `refactor_threshold` and `next_refactor_due_at_run`: 25 for daily / 10 for weekly / 15 for on-demand
- Task name filled in
- All placeholder rows removed (Noise Filters example row; Pending Proposals JSON example → `[]`)

IMPROVEMENTS.md stores **state only** — do not write the A–D instructions into it. Those belong in the generated TASK.md (see the Self-Improvement section in the skeleton above).

If self-improvement was not requested, skip `IMPROVEMENTS.md` and omit only its reads, proposal handling, learning counters and the Self-Improvement (A–D) section. Always retain Step 0’s scheduler ownership/timezone check, run-key claim and duplicate-run guard, plus any task-state loading/bootstrap. Keep the Final Step’s run-log entry and retention rules; rename it “Final Step — Run log” and omit only the call to self-improvement.

### Step 4 — Efficiency check on the draft

Before writing, review the draft TASK.md against these targets:
- TASK.md ≤ 250 lines — if over, identify what to move to TASK_REFERENCE.md
- No JSON schemas or output templates in TASK.md — move to TASK_REFERENCE.md
- No fixed-format artifact generation in TASK.md — if the task produces a structured output file (HTML, formatted report), note: "Consider writing a generation script once the format stabilises — Claude runs it rather than composing from scratch."

Show the user TASK.md line count and flag any efficiency issues before writing.

### Step 5 — Write all files

Write all files. Show the list of files created.

### Step 6 — Register through the selected native route

If scheduling was already requested, proceed using that authorization and the native implementation above. Otherwise offer only supported routes. The following options describe the **Claude Code/manual branch**:
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
