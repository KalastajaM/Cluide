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
- [ ] Set a monthly budget based on the first 3–5 runs
- [ ] Archive old `RUN_LOG.md` entries after 30 runs
