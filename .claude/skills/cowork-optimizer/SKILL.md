---
name: cowork-optimizer
description: >
  Analyze and optimize a Cowork task or project to make it run faster, use fewer tokens, reduce unnecessary steps, and improve overall structure. Use this skill whenever the user shares a Cowork task or project and asks to optimize, improve, speed up, refactor, or reduce Claude usage. Also trigger when the user says things like "make this more efficient", "this task is slow", "can we trim this down", "review my task", or pastes a Cowork task/project definition and asks for feedback.
---
 
# Cowork Optimizer

Analyze a Cowork task or project definition, identify optimization opportunities, present a prioritized plan, get user sign-off, then implement agreed changes.

> This skill applies the patterns from [04_TASK_EFFICIENCY_GUIDE.md](../04_TASK_EFFICIENCY_GUIDE.md) and [05_TASK_LEARNING_GUIDE.md](../05_TASK_LEARNING_GUIDE.md). Read those guides if you want to understand the reasoning behind any recommendation.

## Rules

- Always use this skill before making any edits to a Cowork task or project — even if the user just says "take a look at my task."
- Do not silently apply changes beyond what was agreed in Phase 3.
- Flag tradeoffs explicitly — do not silently optimize toward one axis (speed vs. thoroughness).
 
---
 
## Phase 1: Ingest

**If the content is already in the conversation, skip to Phase 2 immediately.**

Otherwise, attempt to locate the task autonomously before asking the user:

```bash
find /sessions -maxdepth 6 -name "TASK.md" 2>/dev/null
```

If one or more TASK.md files are found, present the list and ask which task to audit. If none are found, ask the user to share the task. They can provide:
- The task instructions pasted directly
- A path to the task file (`.task` or `.md`)
- A Cowork project folder path

If files are referenced inside the instructions (e.g., skill files, reference docs, templates), read those too — optimization depends on understanding the full dependency chain.
 
**Read any referenced skill files.** If the task invokes one or more skills (via `/skill-name` or a `skills:` directive), read those SKILL.md files before auditing. A task may be doing manually what a skill already handles better, or may be loading a skill for a narrow use case that doesn't justify the overhead.
 
Also check whether the task folder contains any of these companion files — they're highly informative for the audit:
- `IMPROVEMENTS.md` — tracks applied fixes, pending proposals, and known issues
- `RUN_LOG.md` — reveals which steps fail repeatedly or take long
- `KNOWLEDGE_SUMMARY.md` — indicates whether state is being carried efficiently between runs
 
**If the content is already in the conversation, skip asking and proceed directly to Phase 2.**
 
---
 
## Phase 2: Audit

Analyze the task/project across these dimensions. For each finding, note: what it is, why it's a problem, and the effort to fix (Low / Medium / High).

**Work through dimensions in order — they are ranked by typical ROI.** Stop when you are confident there are no further significant findings. Dimensions 2.1 and 2.2 almost always yield the highest savings; 2.7 and 2.8 are lower-ROI and can be skipped if the task is already efficient.
 
### 2.1 Token & Context Efficiency
 
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
 
### 2.2 External Data Fetching Efficiency
 
**Two-pass triage**
- When fetching external data (emails, API responses, documents), is the task fetching full content for everything, or does it use cheap metadata first (snippets, subject lines, summaries) to filter what's worth a full fetch? Fetching full content to classify is one of the most avoidable token costs.
- Pattern: Pass 1 = lightweight metadata/snippets → Pass 2 = full content only for items that pass the filter.
 
**Digest collapsing for bulk senders**
- Are there high-volume senders or message categories that consistently produce no direct action? These should be collapsed into a single summary line rather than processed individually. Build a named list of these senders into the task and update it as new recurring-noise patterns emerge.
 
**Per-item recency skips**
- For items tracked across many runs (flagged reminders, open tickets, tracked contacts), is the task re-fetching full metadata every run even when the item is unlikely to have changed? Apply tiered skips: within 24h → carry forward stored data; within 7 days + low-volatility → skip unless deadline trigger fires; far-future deadline (>30 days) → skip entirely.
 
**Connector query assumptions**
- Does the task assume that query parameters search the expected fields? Connector behavior varies — a name search may scan message bodies rather than sender fields, returning 0 results silently. Confirmed connector behaviors should be logged in a compact "Connector Notes" section in TASK.md so they're not re-discovered each run.
 
### 2.3 Run Flow Efficiency
 
**Fast-path skip**
- On tasks that run frequently, is there a content-based fast-path that exits early when there's nothing to process? After initial data fetch, evaluate: 0 new items + no imminent deadlines + no time-sensitive state → write a minimal log entry and exit. Without this, quiet runs still consume tokens doing nothing.
 
**Run deduplication**
- Can the task be triggered multiple times per day? If so, is there logic to skip if a full run completed recently (e.g., < 30 min ago) or to use the last run's timestamp as the fetch boundary rather than yesterday?
 
**Conditional regeneration**
- Does the task regenerate "human-readable view" files (e.g., a markdown summary from a JSON source of truth) on every run, even when the source didn't change? Add a skip condition: only regenerate when the source was modified this run.
 
**Step merging and sequencing**
- Are there sequential steps that could run in parallel, or redundant checks that could be merged?
- Are there early-exit opportunities (fail fast before expensive steps)?
 
### 2.4 Edit Efficiency
 
**Targeted edits vs. full read/write**
- Does the task do full file reads and rewrites for minor updates (changing 2 lines in a 200-line file)? Use grep + targeted edit instead. Saves ~1–3K tokens per file per update — multiplies quickly if multiple files are updated per run.
- Exception: files under ~30 lines — full read/write is fine.
 
### 2.5 Output Generation & Script Offloading

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
 
---
 
### 2.7 Instruction Clarity
 
- Are instructions ambiguous in ways likely to cause Claude to ask clarifying questions mid-task (wasted turns)?
- Are success criteria missing or unclear?
- Are edge cases unhandled that would cause the task to stall?
- Are scope boundaries explicit? ("Update section 3 only, leave everything else unchanged" is often as important as the actual instruction.)
- Are there implicit assumptions that should be stated explicitly?
 
### 2.8 Structural / Architectural Issues
 
- Is the task trying to do too much? Should it be split?
- Is logic embedded in instructions that should be a script (deterministic operations → bash/python)?
- Are there hardcoded values that should be parameters?
- Is the task missing a skill that already exists and handles part of the job better?
 
### 2.9 Self-Improvement Infrastructure
 
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
 
---
 
## Phase 3: Present the Plan

**If no findings exceed ~500 tokens per run in estimated impact and none are qualitatively significant (clarity, correctness, structural), say so explicitly and stop:** "This task is already well-optimized. No changes recommended." Do not generate a thin list of minor findings just to appear thorough.

Otherwise, produce a structured audit report in the conversation. Format:

**Summary** — one sentence characterizing the main issues and rough token cost estimate if calculable.

Then a prioritized list of findings, highest ROI first. For each:
- **Finding title** (e.g., "Unconditional large file load in step 3")
- What the problem is
- Proposed fix
- Effort: Low / Medium / High
- Impact: token savings estimate, speed improvement, or qualitative benefit
 
**Token estimation guide:**
| Component | Rough cost |
|-----------|------------|
| Task instruction file | ~15 tokens/line |
| Each "read every run" file | ~15 tokens/line |
| Each external API fetch (full) | 200–2,000 tokens |
| Each file write (generated output) | ~15 tokens/line |
| Script execution | ~50 tokens |
 
**Flag tradeoffs explicitly.** If a proposed change trades thoroughness for speed, say so. Let the user decide — don't silently optimize toward one axis.
 
**Scope note:** Self-improvement infrastructure (IMPROVEMENTS.md, RUN_LOG.md, KNOWLEDGE_SUMMARY.md) is valuable but represents a meaningful addition, not just a cleanup. Present it as an optional enhancement, not a required fix, unless the task already has partial scaffolding.
 
End with: "Which of these would you like me to implement? You can say 'all of them', pick specific numbers, or tell me to skip any."
 
---
 
## Phase 4: Implement
 
Once the user confirms which changes to make:
 
1. **Back up before editing.** Preferred: `git add` and commit the current state so there's a clean restore point. If git is not available, copy the file with a `.bak` suffix. Note the backup location in your response.
2. Apply changes one finding at a time.
3. After each non-trivial change, briefly note what you changed and why (one line).
4. Present the final revised task/project.
5. If the task has test prompts or a known test workflow, suggest running it to verify behavior is unchanged.

**To roll back:** restore from git (`git checkout -- <file>`) or copy the `.bak` file back to its original path and delete the modified version.
 
**Apply vs. propose discipline:**
- Apply directly (no further confirmation): clearly correct, low-risk, narrow-scope changes — typos, wrong dates, confirmed facts, adding a named sender to a noise list.
- Flag and ask before applying: anything that affects behavior in a non-obvious way, restructures how information is tracked, modifies core logic, touches 3+ files, or where you're not certain the user would agree.
 
**Do not silently apply changes beyond what was agreed.** If you spot something while implementing that wasn't in the plan, flag it and ask.
 
---
 
## Phase 5: Wrap-up
 
After implementation:
- Summarize what changed vs. what was left alone (and why, if relevant).
- Note the new estimated TASK.md line count and token cost per run if measurably improved.
- Offer to package/export if the user needs to reinstall the task or share it.
- If the frontmatter `description` is vague or seems to trigger unreliably, offer to rewrite it: a good description names concrete user phrases, specific file types, and clear exclusions. Rewriting it is low-effort and can significantly improve how reliably Claude picks up the skill.