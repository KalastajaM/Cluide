# Cost and Performance Monitoring

*Last reviewed: April 2026*

> Scheduled tasks run unattended. Without monitoring, costs creep silently — a task that used to cost $0.10 per run can drift to $0.50 after a few profile updates and nobody notices. This guide covers how to measure, budget, and control what your tasks cost.

> **Companion guides:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) covers how to reduce costs once you've found the expensive parts. This guide covers how to find them.

> **Giving this guide to Claude:**
> "Read 10_COST_PERFORMANCE.md and add run metrics tracking to my task at [path/to/TASK.md]. Set up a budget check and alerting."

---

## What to Measure

Track these four metrics at the end of every task run:

| Metric | Why it matters | How to get it |
|---|---|---|
| **Input tokens** | What the task reads — instructions, files, API responses | Estimated from file sizes and tool responses |
| **Output tokens** | What the task generates — output files, tool calls, reasoning | Estimated from generated content length |
| **Wall-clock time** | How long the run takes end-to-end | Timestamp at start and end |
| **API calls** | Number of MCP tool calls made | Count each tool invocation |

You don't need exact numbers. Rough estimates are enough to spot trends and catch regressions.

---

## What Things Actually Cost

Claude pricing (as of early 2026) uses per-token rates that differ by model tier. Rough reference:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| **Sonnet** | ~$3 | ~$15 |
| **Opus** | ~$15 | ~$75 |

These are API list prices. Batch API pricing is typically 50% cheaper (see "Batch vs. Interactive" below). Caching drops input costs further when the same context is reused across calls.

**Typical task costs per run (Sonnet):**

| Task type | Input tokens | Output tokens | Estimated cost |
|---|---|---|---|
| Email digest (triage 20 emails, write summary) | ~12K | ~3K | ~$0.08 |
| Weekly planner (read calendar + profile, write plan) | ~8K | ~2K | ~$0.05 |
| Data ingestion (parse 5 pages, update wiki) | ~20K | ~5K | ~$0.14 |
| Full morning briefing (email + calendar + profile + output) | ~25K | ~6K | ~$0.17 |
| Complex research task (multi-step, 50K context) | ~50K | ~10K | ~$0.30 |

At one run per day, the morning briefing costs roughly $5/month on Sonnet. The same task on Opus would cost roughly $25/month — five times more for the same token volume.

---

## Model Tier Selection: Sonnet vs. Opus

Not every task needs the most capable model. Choose based on what the task actually does:

**Use Sonnet for:**
- Structured extraction (parsing emails, reading calendar events)
- Template-driven output (briefings, digests, status updates)
- Triage and classification tasks
- Any task where the instructions are clear and the output format is fixed

**Use Opus for:**
- Tasks requiring nuanced judgment (prioritizing ambiguous items, drafting sensitive replies)
- Complex multi-step reasoning with large context
- Tasks where output quality directly affects decisions
- Self-improvement proposal generation (the review step in Guide 07)

**The hybrid approach:** Run the data-gathering steps on Sonnet and the synthesis/judgment step on Opus. A morning briefing that fetches and triages on Sonnet, then drafts the narrative on Opus, can cut costs by 40–60% compared to running everything on Opus while keeping output quality high.

In practice, most scheduled tasks work well on Sonnet. Reserve Opus for the tasks where you've noticed Sonnet's output isn't good enough.

---

## The Run Metrics Pattern

At the end of every task run, append a metrics block to `RUN_LOG.md`:

```markdown
## [2026-04-10] Run #47

**Duration:** ~3 min
**Tokens (est.):** ~8K input, ~2K output
**API calls:** 12 (gmail_search: 1, gmail_read: 8, gcal_list: 1, write_file: 2)
**Notes:** Normal run. 8 emails processed, 2 action items found.
```

Add this as the final step in your `TASK.md`:

```markdown
Step [last]: Append a metrics block to RUN_LOG.md with duration, estimated tokens, API call count, and a one-line summary.
```

**Keep RUN_LOG.md lean.** Each entry should be 4–6 lines. After 30 runs, archive older entries to `RUN_LOG_ARCHIVE.md` — keep only the last 10–15 runs in the active file so it stays fast to read.

---

## Quick Token Estimation

You don't need a token counter. Use these rough conversions:

| Content type | Approximate tokens |
|---|---|
| 1 line of markdown | ~15 tokens |
| 1 page of text (~40 lines) | ~600 tokens |
| A typical email body | ~200–500 tokens |
| TASK.md (200 lines) | ~3,000 tokens |
| PROFILE_SUMMARY.md (40 lines) | ~600 tokens |

For a fuller estimation model, see [Guide 06, "Quick Estimation"](./06_TASK_EFFICIENCY_GUIDE.md).

---

## Budgeting

Set a per-task monthly budget based on the first few runs. The formula:

```
Monthly budget = (average cost per run) × (runs per month) × 1.5
```

The 1.5x multiplier gives headroom for occasional expensive runs (more emails than usual, larger API responses).

**Example:** A daily email digest averaging $0.08/run on Sonnet: $0.08 x 30 x 1.5 = **$3.60/month budget**. If actual spend crosses $3.60, something changed.

**Adding a budget check to your task:**

Add this as Step 0 (before the main procedure) in `TASK.md`:

```markdown
Step 0: Read the last 5 entries in RUN_LOG.md. If the average token count
has increased by more than 2x compared to the earliest entry, add a warning
to IMPROVEMENTS.md: "Token usage trending up — review what changed."
```

This catches gradual drift before it becomes expensive. It costs almost nothing — reading 5 short log entries adds ~100 tokens to the run.

---

## Identifying Expensive Operations

When a task is costing more than expected, find where the tokens go. The most common culprits:

**Full file reads when partial reads would do.** Reading a 500-line file costs ~7,500 tokens. Reading 50 relevant lines costs ~750 tokens. If a task reads reference files cover-to-cover every run, switch to section reads.

**Fetching message bodies when subjects suffice.** A triage step that reads 20 full email bodies costs ~5,000–10,000 tokens. Reading just subjects and senders costs ~500 tokens. Triage first, then fetch only the emails that need action.

**Regenerating unchanged output.** If the task generates the same output format every run and most of it doesn't change, check whether the previous output can be updated rather than rewritten from scratch.

**Verbose MCP responses.** Some tools return large JSON objects. If you only need 2 fields from a 50-field response, note that in the skill so Claude knows to extract early and discard the rest.

**The token heat map:** annotate each step in your task with its rough token cost using the estimation table above. This makes the expensive steps obvious at a glance:

```markdown
Step 1: Read TASK.md                          ~3,000 tokens
Step 2: Read PROFILE_SUMMARY.md               ~600 tokens
Step 3: Search Gmail (1 API call)              ~200 tokens
Step 4: Read 10 email bodies                   ~4,000 tokens  ← expensive
Step 5: Read calendar events                   ~500 tokens
Step 6: Generate briefing                      ~1,500 tokens
Step 7: Write output file                      ~100 tokens
Step 8: Log metrics                            ~100 tokens
                                        Total: ~10,000 tokens
```

Step 4 is 40% of the total. That's where optimisation effort should go.

---

## Optimization Case Studies

### Case 1: Email digest — triage before fetch

**Before:** Read all 25 email bodies, then summarize. ~12,500 input tokens from email alone.

**After:** Fetch subjects and senders only (~500 tokens). Triage to 6 actionable emails. Fetch those 6 bodies (~2,400 tokens). Total email tokens: ~2,900.

**Saving:** ~77% reduction in email-related tokens. Per-run cost dropped from ~$0.12 to ~$0.05 on Sonnet.

### Case 2: Weekly planner — stop re-reading static context

**Before:** Task read PROFILE_SUMMARY.md (600 tokens), KNOWLEDGE_SUMMARY.md (1,200 tokens), and full TASK.md (3,000 tokens) every run. These files change rarely.

**After:** Split TASK.md into a slim procedure file (800 tokens) and a reference file read only when the procedure says to. Profile summary trimmed to essentials (300 tokens). Knowledge summary accessed by section.

**Saving:** Fixed overhead dropped from ~4,800 to ~1,100 tokens per run. Over 52 weekly runs: ~192K tokens saved/year, roughly $0.60/year on Sonnet. Small per-run, but it compounds and keeps the task fast.

### Case 3: Data ingestion — batch similar operations

**Before:** Five separate MCP calls to read five pages, each returning full page metadata. ~20K input tokens.

**After:** Single batch query returning only content fields for all five pages. ~8K input tokens. Added a deduplication check to skip pages unchanged since last run — typical run now processes 2–3 pages.

**Saving:** Average run dropped from ~$0.14 to ~$0.06.

---

## Cost Trajectory Patterns

After 10+ runs, your RUN_LOG.md reveals one of three patterns:

**Stable (healthy).** Token counts stay within a narrow band (say 8K–12K). Small spikes correlate with more input data (more emails on Monday). No action needed.

**Step increase (something changed).** Tokens jump from ~10K to ~18K and stay there. Common causes: a profile file grew, a new step was added to TASK.md, or an MCP response format changed. Check what changed around the date of the step.

**Gradual upward drift (accumulation).** Tokens creep up 5–10% per week. Common causes: a knowledge file grows without pruning, run log isn't being archived, or the task is appending to a file it also reads. This is the dangerous pattern — each run is only slightly more expensive, so no single run triggers the 2x alert. Add a secondary check: compare the current average against the average from 20 runs ago, not just 5.

**How to add the drift check:**

```markdown
After logging metrics: if RUN_LOG.md has 20+ entries, compare the average
of the last 5 runs to the average of runs 16–20. If the recent average
exceeds the older average by more than 50%, flag in IMPROVEMENTS.md:
"Gradual cost drift detected — token usage up [X]% over 15 runs."
```

---

## Batch vs. Interactive Cost Profiles

Claude's Batch API processes requests asynchronously (results within 24 hours) at roughly half the per-token cost. This matters for tasks that don't need immediate results.

**Good candidates for batch:**
- Weekly reports and planners (not time-sensitive)
- Bulk data ingestion or wiki updates
- Periodic audits and reviews
- Any task scheduled to run overnight

**Keep interactive:**
- Morning briefings needed before a specific time
- Urgent email scans
- Anything triggered by a real-time event

If a task runs daily at 3 AM and you read the output at 8 AM, batch processing saves ~50% with no practical impact on your workflow.

Note: Cowork scheduled tasks currently run interactively. Batch API applies when you're calling Claude programmatically via the API. If you use the API for some tasks, the cost difference is worth structuring around.

---

## Alerting

Add a simple alerting rule to catch cost spikes. In the metrics step of your task:

```markdown
After logging metrics: compare this run's estimated token count to the
rolling average of the last 5 runs. If this run exceeds 2x the average,
append to IMPROVEMENTS.md:

"⚠ Run #[N] token usage was [X] tokens — 2x above the 5-run average of [Y].
Investigate: did the input data grow, or did the task process more items than usual?"
```

This surfaces problems in `IMPROVEMENTS.md` where the self-improvement cycle (see [Guide 07](./07_TASK_LEARNING_GUIDE.md)) will pick them up and propose a fix.

---

## Optional: Dashboard Script

For tasks that run daily, a simple script can parse `RUN_LOG.md` and produce a summary. Here's the minimal version:

```python
#!/usr/bin/env python3
"""Parse RUN_LOG.md metrics and print a cost summary."""
import re, sys
from pathlib import Path

log = Path(sys.argv[1]).read_text()
runs = re.findall(
    r'## \[(\d{4}-\d{2}-\d{2})\].*?\n'
    r'.*?Tokens \(est\.\):\s*~(\d+)K input,\s*~(\d+)K output',
    log, re.DOTALL
)

print(f"{'Date':<12} {'Input':>8} {'Output':>8} {'Total':>8}")
print("-" * 40)
total = 0
for date, inp, out in runs:
    t = int(inp) + int(out)
    total += t
    print(f"{date:<12} {inp+'K':>8} {out+'K':>8} {str(t)+'K':>8}")
print("-" * 40)
print(f"{'Total':<12} {'':>8} {'':>8} {str(total)+'K':>8}")
print(f"Runs: {len(runs)}  |  Avg: {total // max(len(runs), 1)}K tokens/run")
```

Run with: `python3 dashboard.py path/to/RUN_LOG.md`

This is optional — the in-task metrics and alerting are the core pattern. Add the dashboard when you want a periodic overview across many runs.

---

## Checklist

When setting up cost monitoring for a task:

- [ ] Add a metrics block template to the final step of `TASK.md`
- [ ] Add a Step 0 budget check that reads the last 5 log entries
- [ ] Annotate each task step with its rough token cost (token heat map)
- [ ] Add the 2x alerting rule to the metrics step
- [ ] Add the gradual drift check (compare against 20 runs ago)
- [ ] Set a monthly budget based on the first 3–5 runs
- [ ] Choose the right model tier for each task (Sonnet vs. Opus)
- [ ] Archive old `RUN_LOG.md` entries after 30 runs
