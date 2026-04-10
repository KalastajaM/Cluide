# [TASK NAME] — Run Procedure

> **Template.** Replace all `[PLACEHOLDER]` text with your domain-specific content.
> Delete this note and the How-To-Use section once configured.
> See `README.md` in this folder for setup instructions.
> Companion guides: [04 Efficiency](../06_TASK_EFFICIENCY_GUIDE.md) · [05 Learning](../07_TASK_LEARNING_GUIDE.md) · [06 IMPROVEMENTS Template](../08_SELFIMPROVE_TEMPLATE.md)

---

## How to Use This Template

1. Copy this folder (`TASK_TEMPLATE/`) into your task's location and rename it.
2. Replace every `[PLACEHOLDER]` — search for `[` to find them all.
3. Delete this "How to Use" section and the template note above.
4. Set `refactor_threshold` in `IMPROVEMENTS.md` (25–30 for daily runs, 10–15 for weekly).
5. Schedule the task and run it once manually to verify.

---

## Purpose

[One paragraph: what this task does, what it monitors or processes, and what it produces. Be specific — vague purposes create scope creep.]

---

## File Structure

```
[task-folder]/
├── TASK.md               ← This file (loaded every run, keep ≤ 250 lines)
├── TASK_REFERENCE.md     ← Schemas, format templates, edge-case rules (load on demand)
├── IMPROVEMENTS.md       ← Self-improvement log and run counter (loaded every run)
├── KNOWLEDGE_SUMMARY.md  ← Compact context (loaded every run, hard limit: 40 lines)
└── RUN_LOG.md            ← Append-only run history
```

---

## Step 0 — Locate Working Directory and Check First-Run State

```bash
find /sessions -maxdepth 5 -path '*/[task-folder]/TASK.md' 2>/dev/null | head -1
```

Derive all file paths from this result.

**First-run check:** Before reading any state file, verify the required files exist. If missing, initialize from bootstrap stubs (see `bootstrap/` at the project root) or create minimal empty versions:

| File | Bootstrap source | Empty fallback |
|------|-----------------|----------------|
| `RUN_LOG.md` | `bootstrap/RUN_LOG.md` | `# Run Log\n\n---\n` |
| `[state_file].json` | `bootstrap/[state_file].json` | `{}` or `[]` as appropriate |

If any file was initialized this way, note "Bootstrap: first run — [filename] initialized" in the run log entry for this run. Do not treat this as an error.

---

## Step 1 — Read State

Read in this order:

1. `IMPROVEMENTS.md` — note `total_runs` and `runs_since_last_refactor`. Act on any proposals marked `[APPROVED]`, `[REJECTED]`, or `[MODIFY: ...]`.
2. `KNOWLEDGE_SUMMARY.md` — load compact context. Hard limit: 40 lines; trim if over.
3. `RUN_LOG.md` — skim the last 2 entries only for recent context.

**Fast-path check** — after reading state, evaluate before continuing:

Conditions (ALL must be true to skip):
- [ ] [Domain condition 1 — e.g. "0 new items fetched since last run"]
- [ ] [Domain condition 2 — e.g. "No pending items with deadlines within N days"]
- [ ] No open issues in IMPROVEMENTS.md with `OPEN` status that are now resolvable

If all conditions are met → write a minimal log entry to `RUN_LOG.md` ("Fast-path — [reason]"), increment counters in `IMPROVEMENTS.md`, and exit.

---

## Step 2 — Fetch External Data

### Pass 1 — Cheap triage (metadata / snippets only)

[Describe what cheap data to fetch first: e.g. email subject lines, API event headers, file modified timestamps.]

**Skip conditions** — do not fetch full content for:
- [Noise pattern 1 — e.g. "Automated digest from X — always identical, no actionable content"]
- [Noise pattern 2 — e.g. "Status updates from system Y when subject contains 'routine'"]

*(Add new noise patterns after observing 5+ structurally identical instances. See `IMPROVEMENTS.md` Noise Filters.)*

**Recency skip** — for items tracked across multiple runs:
- Reviewed within 24h → carry forward stored data; skip fetch
- Low-volatility item, reviewed within 7 days → skip unless deadline trigger fires
- Deadline > 30 days away → skip; re-check as deadline approaches

### Pass 2 — Full content

Fetch full content only for items that passed the Pass 1 filter. Log how many were skipped vs. fetched in the run log.

---

## Step 3 — [Primary Work Step Name]

[Replace with the core logic of your task. Use numbered sub-steps. Be explicit about what Claude should do with the data fetched in Step 2.]

Sub-steps:
1. [e.g. "For each item, classify as: actionable / informational / noise"]
2. [e.g. "For actionable items, extract: who needs to do what, by when"]
3. [e.g. "For each knowledge entity mentioned, check against KNOWLEDGE_SUMMARY.md and update if new information found"]

**Classify, don't assume:**
- When uncertain between two classifications, choose the more conservative one and note the uncertainty.
- If classifying a type of item not covered by existing rules, flag it explicitly rather than guessing.

---

## Step 4 — [Additional Work Step, if needed]

[Add or remove steps as needed. Common step types: "Resolve pending actions", "Update knowledge files", "Generate output".]

**Conditional regeneration:** skip this step if the source data was not modified this run.

---

## Step 5 — Generate Output

[Describe the output: file type, location, format. Reference `TASK_REFERENCE.md §Output Format` if the format is complex.]

Output file: `[path/to/OUTPUT.md]`

If a script handles formatting: `python3 render.py [task-folder]`
On script failure: compose directly and log the error as a known issue.

**Skip regeneration** if no source data changed this run (fast-path runs excluded — they don't reach this step).

---

## Step 6 — Self-Improvement

Run after primary work, before writing the run log.

### A. Feedback Signal Detection

From the user:
- Did the user correct anything in an output file since last run? → Extract the lesson. Apply or propose a fix.
- Did the user annotate output with `[DONE]` / `[SKIP]` / `[WRONG]`? → Process annotations; extract the general rule.
- Did a proposal sit `PENDING` for 2+ runs with no response? → Archive it in IMPROVEMENTS.md.
- Did an item resolve unusually fast? → Priority calibration was correct; reinforce.
- Did an item sit open 14+ days with no action? → Review priority or action clarity.

Operational signals:
- Did any query return 0 results when it should have found something? → Log as known issue; try alternative syntax next run.
- Did the task miss something only apparent later? → Add a detection rule.
- Is the same section of KNOWLEDGE_SUMMARY.md being rewritten every run? → Consider a structural improvement.
- Did any file operation fail? → Log as known issue.

### B. Refactor Trigger Check

| Trigger | Condition | Action |
|---------|-----------|--------|
| Run count | `runs_since_last_refactor` ≥ threshold | Run full refactor this run |
| File size | TASK.md > 250 lines | Propose consolidation |
| File size | Any always-loaded file > 300 lines | Propose consolidation |
| Stale content | Any section not updated in 3+ months | Flag in output |
| Accumulated state | > 8 open items at once | Review and reprioritize |
| Repeated failure | Same check failing 5+ runs | Revise the check |

When a full refactor runs:
1. Review all tracked files for stale, duplicate, or contradictory content — consolidate.
2. Review TASK.md for steps that are unclear, never followed, or outdated.
3. Review open items — close or merge where possible.
4. Reset `runs_since_last_refactor` to 0. Summarize findings in the run log.

### C. Apply or Propose

**Apply directly** (no confirmation needed) when ALL are true:
- Change is clearly correct and low-risk
- Scope is a single field, sentence, or entry in a single file
- Change is purely additive or corrects a confirmed error

**Propose in IMPROVEMENTS.md** when ANY is true:
- Change affects behavior in a non-obvious way
- Change restructures how information is tracked
- Change modifies core logic (step order, priority rules, thresholds)
- Change touches 3+ files or 10+ lines
- Confidence is below HIGH

### D. Update IMPROVEMENTS.md

- Increment `total_runs` and `runs_since_last_refactor`
- Add new applied fixes (newest first; archive when list exceeds 10)
- Add/update pending proposals
- Add/update known issues
- Archive resolved items

---

## Step 7 — Append Run Log

Append to `RUN_LOG.md`. Keep the last 3 runs in full; compress older entries to 1-line summaries.

```markdown
### Run [N] — [YYYY-MM-DD]
- **Fetched:** [N] items ([N] skipped as noise, [N] via fast-path)
- **Processed:** [N] actionable / [N] informational / [N] noise
- **Knowledge updates:** [brief or "none"]
- **Improvements:** applied [N] (FIX-NNN...) / proposed [N] (PROP-NNN...)
- **Tool calls:** [N]
- **TASK.md lines:** [N]
```

---

## Rules

- [Domain rule 1 — e.g. "Never send an external message without explicit user confirmation"]
- [Domain rule 2 — e.g. "Always read the full thread before classifying an email as noise"]
- TASK.md hard limit: **250 lines**. Propose a refactor when this is breached, not after.
- KNOWLEDGE_SUMMARY.md hard limit: **40 lines**. Trim before writing.
- Execute resolution checks as actual tool calls — never infer or assume results.
- Never apply a change touching 3+ files without a proposal in IMPROVEMENTS.md.
- Output in [language].
