# Claude Task Efficiency Guide

> How to design and optimize Claude tasks for minimal token consumption.
> Use as a one-time audit checklist when setting up a new task, or as a periodic optimization pass on an existing one.

> **Companion guides:** This guide covers efficiency (keeping token use low). [Guide 05](./05_TASK_LEARNING_GUIDE.md) covers self-improvement (making the task smarter over time). [Guide 06](./06_SELFIMPROVE_TEMPLATE.md) is a ready-to-use template that implements Guide 05.

> **Giving this guide to Claude:**
> "Read 04_TASK_EFFICIENCY_GUIDE.md and audit my existing task at [path/to/TASK.md] for token efficiency. Apply the checklist and propose specific changes."

---

## Core Principle
Every token Claude reads or writes costs usage. The goal is to ensure Claude only loads what it needs for the current run, and only generates what it can't delegate to a script.

The four main levers:
1. **Reduce what Claude reads** — smaller instruction files, partial file reads
2. **Reduce what Claude writes** — skip unchanged outputs, delegate fixed-format generation to scripts
3. **Reduce API calls** — triage before fetching full content
4. **Keep frequently-read files compact** — hard size limits on files loaded every run

---

## One-Time Audit Checklist

### 1. Split the instruction file (TASK.md)

The task instruction file is loaded on every run. Keep it to **~200 lines / ~3K tokens** of core procedure. Everything else moves to a `TASK_REFERENCE.md` that Claude reads only when it specifically needs it.

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
| TASK.md | ≤ 250 | Every run |
| TASK_REFERENCE.md | any | On demand |

---

### 2. Script fixed-format artifact generation

If the task generates a structured output file (HTML report, PDF, formatted document) from a structured input (markdown, JSON), Claude should not compose it from scratch every run.

**Write a script once. Claude runs it.**

Ask: *does the output format change between runs, or just the data?*
- Format is fixed, data varies → write a script
- Format varies based on run content → Claude composes it

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

Claude's step becomes: run the script, show the output link. On failure, fall back to composing directly and log the error.

---

### 3. Apply targeted edit policy for file updates

If Claude updates a file that it reads every run, it should use partial reads and targeted edits rather than full read + full write.

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

When fetching external data (emails, API responses, documents), many items will be noise. Use a cheap first pass to classify, and only fetch full content for items that pass.

**Gmail pattern:**
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

Any file that is loaded every run must have a hard size cap. Without it, these files drift upward over time and compound the token cost of every future run.

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
| Run log (active section) | 3 full entries, older compressed to 1-line summaries |
| Pending actions summary | proportional to open item count; archive resolved promptly |

**Design choice — full history vs. latest only:**
Tasks can keep either an append-only `RUN_LOG.md` (full history) or a `LAST_RUN.md` (only the most recent run). Full history is better for detecting patterns across runs ("this issue has appeared 3 times"). Latest-only saves tokens. If your task runs daily, use `RUN_LOG.md` with the 3-entry rolling window above. If it runs very frequently or you only need to debug the last run, `LAST_RUN.md` is sufficient.

---

### 7. Add run deduplication

If the task can be triggered multiple times per day, add duplicate detection to avoid redundant full runs.

```
Step 0: Record run start timestamp
Step 2: Check if a full run already completed today
  → If yes: use that run's timestamp as the fetch boundary (not yesterday)
  → If < 30 min ago: skip entirely
```

---

## Recurring Optimization Pass

Run this every 20–30 task executions, or whenever you notice usage spikes.

### Checklist

**Instruction file drift**
- [ ] Is TASK.md still ≤ 250 lines? If not, extract the new additions to TASK_REFERENCE.md.
- [ ] Are there steps in TASK.md that are never executed? Flag them for removal or move to reference.

**Always-loaded files**
- [ ] Is PROFILE_SUMMARY.md (or equivalent) still within its line cap? If not, trim.
- [ ] Is the run log still compact, or have full entries accumulated beyond the cap?

**Output generation**
- [ ] Are there new structured output files that could be scripted? (Apply checklist item 2.)
- [ ] Is any existing script producing errors and falling back to Claude generation? Fix the script.

**Fetch efficiency**
- [ ] Are there new high-frequency senders that are always noise? Add them to the digest/collapse list.
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
| Script execution | ~50 tokens | Just the bash call + output |

**Example:** A 500-line TASK.md costs ~7.5K tokens per run just to load. Splitting it to 200 lines saves ~4.5K per run — which over 50 runs saves 225K tokens.

---

## How Scheduled Tasks Are Triggered

Tasks do not run themselves — they need a trigger. Claude Code supports **hooks**: shell commands that fire automatically in response to events. Hooks are configured in `~/.claude/settings.json`.

The most useful hook for personal assistants is **SessionStart**, which runs a command every time a new Claude session opens.

**Minimal SessionStart example:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "claude -p 'Read .claude/tasks/daily-digest/TASK.md and run the daily digest.'"
          }
        ]
      }
    ]
  }
}
```

This runs the daily digest task automatically when you open Claude — no manual trigger needed.

**Other useful hook events:**
- **PostToolUse** — fires after a specific tool is used. Useful for follow-up actions (e.g., after a file is written, trigger a summary update).
- **PreToolUse** — fires before a tool runs. Useful for validation or logging.

**Practical notes:**
- A SessionStart hook runs once per session, not once per day. If you open multiple sessions in a day, the task runs multiple times. Add run deduplication (checklist item 7 above) to prevent redundant full runs.
- The `matcher` field filters by context (e.g., directory). Leave it empty (`""`) to fire on all sessions.

For the full hooks reference, see the [Claude Code documentation on hooks](https://docs.anthropic.com/en/docs/claude-code/hooks).

A common use of the `SessionStart` hook is to commit task state files before every run — creating a restore point if a run goes wrong. See [Guide 09 — Git Integration](./09_GIT_INTEGRATION.md).

---

## Anti-Patterns to Avoid

**Full-file read + write for small updates.** If you're changing 2 lines in a 200-line file, use Grep + Edit, not Read + Write.

**Regenerating unchanged outputs.** If the source didn't change, don't regenerate the view.

**Composing fixed-format artifacts.** If the format is the same every run, write it once as a script.

**Unbounded files.** Any file that grows without a trim/archive policy will become expensive over time.

**Fetching full content to classify.** Use cheap metadata (snippets, summaries, subject lines) to decide what's worth a full fetch.

**Loading reference material preemptively.** Don't load schemas, format templates, or principles at the start of every run "just in case." Load them when actually needed.
