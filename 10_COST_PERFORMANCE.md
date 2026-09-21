# Cost and Performance Monitoring

> Scheduled tasks run unattended. Without monitoring, costs creep silently — a task that used to cost $0.10 per run can drift to $0.50 after a few profile updates and nobody notices. This guide covers how to measure, budget, and control what your tasks cost.

> **Companion guides:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) covers how to reduce costs once you've found the expensive parts. This guide covers how to find them.

> **Giving this guide to an assistant:**
> "Read 10_COST_PERFORMANCE.md and add run metrics tracking to my task at [path/to/TASK.md]. Set up a budget check and alerting."

---

## What to Measure

Track these four metrics at the end of every task run:

| Metric | Why it matters | How to get it |
|---|---|---|
| **Input tokens** | What the task reads — instructions, files, API responses | Estimated from file sizes and tool responses |
| **Output tokens** | What the task generates — output files, tool calls, reasoning | Estimated from generated content length |
| **Wall-clock time** | How long the run takes end-to-end | Timestamp at start and end |
| **Tool calls** | Calls to connectors, MCP and native tools | Count calls separately from billable model API requests |

Prefer measured counters. Label estimates and compare like workloads on the same surface and model; rough estimates are useful for trends, not invoices.

---

## What Things Actually Cost

Separate three ledgers: **API spend**, **subscription allowance**, and **runtime effort**. A token estimate helps compare runs; it does not tell you how much of a ChatGPT or Claude subscription remains.

| Ledger | Record | Use it for |
|---|---|---|
| Anthropic or OpenAI API | Exact model identifier, provider, pricing date, uncached/cached input, output, extra tool charges | Money budgets and invoice reconciliation |
| Claude / ChatGPT subscription | Plan and actual account usage windows, reset times and available usage display | Capacity planning; do not convert dollars from API list prices into subscription credits |
| Task execution | Duration, processed items, retries, tool calls, measured tokens when exposed | Detecting regressions across comparable runs |

For an API estimate, use `(uncached input × input rate + cached input × cache rate + output × output rate) / 1,000,000`, then add applicable tool charges. Record cache writes separately where priced. Missing counters are **unavailable**, not zero. File-length estimates omit repeated prompts, reasoning, images and provider tokenization effects.

The pricing source of truth is the provider's current table, not a model-tier alias. Checked source locations 2026-09-14: [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing) and [OpenAI API pricing](https://developers.openai.com/api/docs/pricing). Select the actual API model before copying a rate; do not use a subscription price as a token rate. This guide deliberately carries no static price catalogue.

**Illustrative arithmetic, not a vendor quote:** 12K input at $2/M and 3K output at $10/M would cost $0.054 before tools and caching. Thirty such runs would cost $1.62. Replace both rates with checked prices before budgeting.

---

## Model Tier Selection

Choose a model from the actual host inventory, then compare quality and cost on representative fixtures. Extraction, triage, synthesis and review are different workloads; a cheap first pass is useful only if its errors do not make the later pass more expensive.

For Claude, the repository's `dispatch` policy assigns available Claude tiers; it is a Claude routing policy, not a cross-vendor equivalence table. Effort is the other Claude cost lever: the Claude Code `maxEffortLevel` setting caps effort on every provider, which bounds what a delegated or scheduled run can spend on reasoning regardless of what its prompt or agent definition asks for ([Claude Code changelog](https://code.claude.com/docs/en/changelog), v2.1.263–269). For OpenAI, retain the configured model unless the user or host policy authorizes another supported identifier. Never translate Haiku, Sonnet or Opus into a guessed OpenAI model.

Use three checks before changing a recurring task's model: the candidate is available to that execution surface, the fixture output passes the same graders, and measured allowance/spend or latency improves. Record the exact model returned by the run. A task prompt can request routing only where the host exposes that control; changing prose does not change the running session's model.

[Guide 09](./09_MULTI_TASK_ORCHESTRATION.md#model-aware-dispatch) covers workload routing and [Guide 31](./31_BEHAVIOUR_TESTS.md) the acceptance tests.

---

## Prompt Caching

Caching can reduce repeated-input costs, but eligibility, rates, retention and counters depend on the API and model. Keep a stable reusable prefix, avoid unnecessary repetition, and inspect the actual cache usage returned by the provider before assigning savings. Do not assume a daily task reuses yesterday's cache.

Subscription usage displays are not API cache invoices. For Claude Code, use the usage and cost controls present in the installed version; for Codex or ChatGPT, use the host's account usage display or exposed usage tool. If only elapsed time and item counts are available, record those. A cache hit or exact token count cannot be reconstructed reliably from the length of the final answer.

---

## The Run Metrics Pattern

At the end of every task run, append a metrics block to `RUN_LOG.md`:

```markdown
## [2026-04-10] Run #47

**Surface/model/source:** [product, exact model, measured or estimated]
**Duration:** ~3 min
**Tokens (est.):** ~8K input, ~2K output
**Tool calls:** 12 (gmail_search: 1, gmail_read: 8, gcal_list: 1, write_file: 2)
**Notes:** Normal run. 8 emails processed, 2 action items found.
```

Add this as the final step in your `TASK.md`:

```markdown
Step [last]: Append a metrics block to RUN_LOG.md with duration, estimated tokens, API call count, and a one-line summary.
```

**Keep RUN_LOG.md lean.** Each entry should be 4–6 lines, using the `## [YYYY-MM-DD] Run #N` header and `**Tokens (est.):** ~XK input, ~YK output` line shown above. Keep the last 20 entries in full — the drift check below compares the last 5 runs against runs 16–20, so it needs them. Once the file exceeds ~30 entries, archive older ones to `RUN_LOG_ARCHIVE.md`.

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

**Illustrative API example:** A daily email digest averaging $0.05/run: $0.05 × 30 × 1.5 = **$2.25/month budget**. If actual spend crosses $2.25, something changed.

**Adding a budget check to your task:**

Add this as Step 0 (before the main procedure) in `TASK.md`:

```markdown
Step 0: Read the last 5 entries in RUN_LOG.md. If the average token count
has increased by more than 2x compared to the earliest of those 5 entries, add a warning
to IMPROVEMENTS.md: "Token usage trending up — review what changed."
```

This catches gradual drift before it becomes expensive. It costs almost nothing — reading 5 short log entries adds ~100 tokens to the run.

---

## Non-Interactive Usage and Your Plan

Scheduled runs, CLI automation and direct API calls may use different authentication and billing arrangements. Record the identity and execution surface before estimating capacity. Check current plan controls and actual usage; do not infer a dollar-denominated allowance from the monthly subscription price.

For Claude, inspect the account and authentication mode used by the scheduled task or CLI. For OpenAI, distinguish a subscription-authenticated Codex/ChatGPT run from an API-key application. Both need headroom for retries and interactive work, but their accounting is not interchangeable. A missing usage display is a reporting limitation, not unlimited capacity.

Use [Guide 35's scheduler-owner record](./35_DUAL_PLATFORM_PROJECTS.md#7-state-schedules-and-handoffs) to associate every recurring job with the account whose usage it consumes.

---

## Identifying Expensive Operations

When a task is costing more than expected, find where the tokens go. The most common culprits:

**Full file reads when partial reads would do.** Reading a 500-line file costs ~7,500 tokens. Reading 50 relevant lines costs ~750 tokens. If a task reads reference files cover-to-cover every run, switch to section reads.

**Fetching message bodies when subjects suffice.** A triage step that reads 20 full email bodies costs ~5,000–10,000 tokens. Reading just subjects and senders costs ~500 tokens. Triage first, then fetch only the emails that need action.

**Regenerating unchanged output.** If the task generates the same output format every run and most of it doesn't change, check whether the previous output can be updated rather than rewritten from scratch.

**Verbose MCP responses.** Some tools return large JSON objects. If you only need 2 fields from a 50-field response, note that in the skill so the assistant knows to extract early and discard the rest.

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

These examples illustrate the measurement method. Their token estimates and dollar figures are not current model quotes or subscription usage conversions.

### Case 1: Email digest — triage before fetch

**Before:** Read all 25 email bodies, then summarize. ~12,500 input tokens from email alone.

**After:** Fetch subjects and senders only (~500 tokens). Triage to 6 actionable emails. Fetch those 6 bodies (~2,400 tokens). Total email tokens: ~2,900.

**Saving:** ~77% reduction in email-related tokens. Measure the full run to determine the cost reduction.

### Case 2: Weekly planner — stop re-reading static context

**Before:** Task read PROFILE_SUMMARY.md (600 tokens), KNOWLEDGE_SUMMARY.md (1,200 tokens), and full TASK.md (3,000 tokens) every run. These files change rarely.

**After:** Split TASK.md into a slim procedure file (800 tokens) and a reference file read only when the procedure says to. Profile summary trimmed to essentials (300 tokens). Knowledge summary accessed by section.

**Saving:** Fixed overhead dropped from ~4,800 to ~1,100 tokens per run. Over 52 weekly runs: ~192K tokens saved/year, an input-token saving whose dollar value depends on the checked rate. Small per-run, but it compounds and keeps the task fast.

### Case 3: Data ingestion — batch similar operations

**Before:** Five separate MCP calls to read five pages, each returning full page metadata. ~20K input tokens.

**After:** Single batch query returning only content fields for all five pages. ~8K input tokens. Added a deduplication check to skip pages unchanged since last run — typical run now processes 2–3 pages.

**Saving:** Average run dropped from ~$0.14 to ~$0.06 (output also fell to ~2.4K tokens after deduplication).

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

Batch processing is an API execution choice, separate from scheduling a conversational task. For either provider, check the supported model, discount, completion window and retry semantics in current API documentation before using it. A scheduler does not automatically submit requests to a Batch API.

Bulk ingestion and non-urgent audits can tolerate delayed results. A morning briefing with a strict deadline usually needs a different path. Test the whole completion window: an overnight submission whose service allows a day to finish cannot promise delivery five hours later. Budget duplicate submissions and retries, and use stable request identities.

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
    r'.*?\*\*Tokens \(est\.\):\*\*\s*~(\d+(?:\.\d+)?)K input,\s*~(\d+(?:\.\d+)?)K output',
    log, re.DOTALL
)

print(f"{'Date':<12} {'Input':>8} {'Output':>8} {'Total':>8}")
print("-" * 40)
total = 0.0
for date, inp, out in runs:
    t = float(inp) + float(out)
    total += t
    print(f"{date:<12} {inp+'K':>8} {out+'K':>8} {f'{t:g}K':>8}")
print("-" * 40)
print(f"{'Total':<12} {'':>8} {'':>8} {f'{total:g}K':>8}")
print(f"Runs: {len(runs)}  |  Avg: {total / max(len(runs), 1):.1f}K tokens/run")
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
- [ ] Set a monthly budget based on the first 3–5 runs — and keep API money budgets separate from subscription usage headroom
- [ ] Choose an available model using the same acceptance fixtures; record provider and exact identifier
- [ ] Archive old `RUN_LOG.md` entries after 30 runs
