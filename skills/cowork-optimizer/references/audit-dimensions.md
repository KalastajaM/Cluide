# Audit Dimensions — Detailed Reference

> Referenced from SKILL.md Phase 2. Work through dimensions in order — they are ranked by typical ROI. Dimensions 2.1 and 2.2 almost always yield the highest savings; 2.7 and 2.8 are lower-ROI and can be skipped if the task is already efficient.

## 2.1 Token & Context Efficiency

**Instruction file size**
- Is TASK.md over ~250 lines? If so, it likely contains reference material (schemas, templates, error procedures, design principles) that only needs to be read on demand — not every run. These should move to a `TASK_REFERENCE.md` and be referenced inline with `See TASK_REFERENCE.md §Section`.
- Target: TASK.md ≤ 250 lines loaded every run; reference material in a separate file loaded only when needed.
- A 500-line TASK.md costs ~7.5K tokens per run just to load. Splitting to 200 lines saves ~4.5K per run — 225K tokens over 50 runs.

**Always-loaded files**
- Are there summary, state, or knowledge files loaded every run without a hard size cap? Without caps, these drift upward and compound the cost of every future run.
- Recommended caps: profile/knowledge summary ≤ 40 lines; run log active section ≤ 3 full entries (older entries compressed to 1-line summaries).

**Lazy loading**
- Are large reference files, schemas, or format templates loaded at the start of every run "just in case"? They should only be loaded when the step that needs them is actually reached.
- Does a `TASK_REFERENCE.md` exist? If so, check whether it is loaded on demand (correct) or unconditionally at the start of every run (fix: make it lazy). If it doesn't exist and TASK.md is over ~250 lines, extracting one is the single highest-ROI change available.

**Redundant content**
- Are reference files or prompts duplicated across steps? Is there boilerplate that could be compressed without loss?

## 2.2 External Data Fetching Efficiency

**Two-pass triage**
- When fetching external data (emails, API responses, documents), is the task fetching full content for everything, or does it use cheap metadata first (snippets, subject lines, summaries) to filter what's worth a full fetch? Fetching full content to classify is one of the most avoidable token costs.
- Pattern: Pass 1 = lightweight metadata/snippets → Pass 2 = full content only for items that pass the filter.

**Digest collapsing for bulk senders**
- Are there high-volume senders or message categories that consistently produce no direct action? These should be collapsed into a single summary line rather than processed individually. Build a named list of these senders into the task and update it as new recurring-noise patterns emerge.

**Per-item recency skips**
- For items tracked across many runs (flagged reminders, open tickets, tracked contacts), is the task re-fetching full metadata every run even when the item is unlikely to have changed? Apply tiered skips: within 24h → carry forward stored data; within 7 days + low-volatility → skip unless deadline trigger fires; far-future deadline (>30 days) → skip entirely.

**Connector query assumptions**
- Does the task assume that query parameters search the expected fields? Connector behavior varies — a name search may scan message bodies rather than sender fields, returning 0 results silently. Confirmed connector behaviors should be logged in a compact "Connector Notes" section in TASK.md so they're not re-discovered each run.

## 2.3 Run Flow Efficiency

**Fast-path skip**
- On tasks that run frequently, is there a content-based fast-path that exits early when there's nothing to process? After initial data fetch, evaluate: 0 new items + no imminent deadlines + no time-sensitive state → write a minimal log entry and exit. Without this, quiet runs still consume tokens doing nothing.

**Run deduplication**
- Can the task be triggered multiple times per day? If so, is there logic to skip if a full run completed recently (e.g., < 30 min ago) or to use the last run's timestamp as the fetch boundary rather than yesterday?

**Conditional regeneration**
- Does the task regenerate "human-readable view" files (e.g., a markdown summary from a JSON source of truth) on every run, even when the source didn't change? Add a skip condition: only regenerate when the source was modified this run.

**Step merging and sequencing**
- Are there sequential steps that could run in parallel, or redundant checks that could be merged?
- Are there early-exit opportunities (fail fast before expensive steps)?

## 2.4 Edit Efficiency

**Targeted edits vs. full read/write**
- Does the task do full file reads and rewrites for minor updates (changing 2 lines in a 200-line file)? Use grep + targeted edit instead. Saves ~1–3K tokens per file per update — multiplies quickly if multiple files are updated per run.
- Exception: files under ~30 lines — full read/write is fine.

## 2.5 Output Generation & Script Offloading

For every step that generates output, ask: **is Claude making a decision here, or just transforming data?**

If the format is fixed and only the data varies, it's a script candidate — not a Claude task. Script execution costs ~50 tokens (bash call + output) vs. hundreds or thousands for Claude composing the same artifact from scratch every run.

**Common offload candidates:**

| Task type | Claude doing it | Better as |
|-----------|----------------|-----------|
| Rendering HTML/PDF from structured data | Claude writes markup | Python (Jinja2, WeasyPrint, reportlab) |
| Formatting markdown → Word/PDF | Claude generates document | Python (pandoc, python-docx) |
| Building CSV/Excel from JSON | Claude writes rows | Python (csv, openpyxl) |
| Sending templated emails | Claude fills + sends | Python with string templates |
| Archiving / rotating log entries | Claude trims and rewrites | Python script on the file directly |
| Copying, moving, renaming files | Claude calls file tools | Bash or Python |
| Parsing structured API responses | Claude extracts fields | Python with json/jq |
| Generating charts/graphs from data | Claude produces SVG/code | Python (matplotlib, plotly) |

**How to surface this in findings:**
- Name the specific step (e.g., "Step 4: Generate weekly HTML report")
- Estimate the token cost of the current Claude-based approach
- Propose the script equivalent with a rough input → output contract
- Effort: Low if the format is already well-defined; Medium if some design is needed

**Caveat:** only propose offloading when the output format is stable and the transformation is fully deterministic. If the step involves judgment — deciding *what* to include, adapting tone, summarizing variable content — keep it with Claude.

## 2.7 Instruction Clarity

- Are instructions ambiguous in ways likely to cause Claude to ask clarifying questions mid-task (wasted turns)?
- Are success criteria missing or unclear?
- Are edge cases unhandled that would cause the task to stall?
- Are scope boundaries explicit? ("Update section 3 only, leave everything else unchanged" is often as important as the actual instruction.)
- Are there implicit assumptions that should be stated explicitly?

## 2.8 Structural / Architectural Issues

- Is the task trying to do too much? Should it be split?
- Is logic embedded in instructions that should be a script (deterministic operations → bash/python)?
- Are there hardcoded values that should be parameters?
- Is the task missing a skill that already exists and handles part of the job better?

## 2.9 Self-Improvement Infrastructure

Does the task have the scaffolding to improve over time? Check for:
- `IMPROVEMENTS.md` — run counter, applied fixes, pending proposals, known issues backlog
- `RUN_LOG.md` — append-only execution record
- `KNOWLEDGE_SUMMARY.md` — compact state digest with a hard line cap
- `REVIEWED.md` — deduplication log preventing the same finding from being re-surfaced across runs (relevant for tasks that scan external sources for learnings)

If missing, consider proposing these as additions (see Phase 3 note on scope).

Also check:
- Are proposals in IMPROVEMENTS.md being applied and logged atomically? (A fix applied to TASK.md must be recorded in the same run — divergence makes the log unreliable.)
- Is the improvements log being kept compact, or has it become a graveyard of stale proposals?
- Is the task surfacing suggestions that are consistently ignored? If so, stop generating them.
