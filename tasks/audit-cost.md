# Task: Audit Task Cost

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-cost.md` (then specify which task folder to audit)
> **Source guide:** `10_COST_PERFORMANCE.md`

## Purpose
Audit a task folder's token economics against Guide 10: always-loaded file sizes vs. budgets, model tier appropriateness, run-metrics instrumentation, and monthly budget vs. the usage-credit pool. Returns a prioritised list of findings and applies the agreed fixes.

**Companion:** `tasks/audit-task-efficiency.md` covers *how* to reduce tokens (file splitting, triage, trim policies). This task covers *what the task costs* and whether that cost is visible, budgeted, and on the right model tier. Run both for a full picture.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Identify the task to audit

Ask: "Which task folder should I audit? Provide the path (e.g. `tasks/my-task/`)."

Read `TASK.md` and list the folder contents. Identify:
- Every file the task reads on every run (always-loaded files)
- Whether `RUN_LOG.md` exists and what each entry records
- How often the task runs (from TASK.md, or ask)
- Which model tier it runs on (ask if not stated)
  Use `AskUserQuestion` with buttons: `Haiku` / `Sonnet` / `Opus` / `Fable` / `Don't know`

Report:
```
Task: [path]
Run frequency: [daily/weekly/on demand]
Model tier: [tier or unknown]
Always-loaded files: [list with line counts]
RUN_LOG.md: [exists with metrics / exists without metrics / missing]
```

### Step 2 — Run the cost checklist

#### Check 1: Always-loaded file budgets

For every file read on every run, compare against the hard limits (Guides 06/07 and the TASK_TEMPLATE):

| File | Limit |
|------|-------|
| TASK.md | ≤ 250 lines |
| KNOWLEDGE_SUMMARY.md (or equivalent) | ≤ 40 lines |
| IMPROVEMENTS.md | ≤ 150 lines (archive Applied Fixes when > 10 entries) |
| Any other always-loaded file | ≤ 300 lines |

Estimate the per-run fixed overhead: total always-loaded lines × ~15 tokens/line. Flag every over-limit file with its overage cost.

#### Check 2: Model tier appropriateness

Match the task's work against the current lineup (Guide 10 §Model Tier Selection):

| Tier | Right for |
|------|-----------|
| **Haiku 4.5** | Triage, classification, bulk extraction — output is a label or short record |
| **Sonnet 4.6** | The default — template-driven output, clear instructions, fixed format |
| **Opus 4.8** | Judgment-heavy review, sensitive drafting, complex multi-step reasoning |
| **Fable 5** | Hardest long-horizon synthesis; 1M context holds whole projects — advantage grows with task length |

Flag mismatches in both directions:
- Triage/extraction steps running on Sonnet or above → "drop to Haiku"
- A whole task on Opus/Fable when only one step needs the judgment → "hybrid: gather on Haiku/Sonnet, synthesise on Opus"
- Short tasks on Fable → "the 2x-over-Opus price rarely pays off below long-horizon scale"

#### Check 3: Run metrics instrumentation

Does `RUN_LOG.md` capture per-run metrics? Each entry should record (Guide 10 §Run Metrics Pattern): duration, estimated input/output tokens, tool/API call count, one-line summary.

- Metrics present → check for trend patterns: stable / step increase / gradual drift (compare last 5 runs vs. runs 16–20 if 20+ entries exist)
- Metrics absent → flag: "No cost visibility — add the metrics block" (offered in Step 4)

#### Check 4: Budget check and alerting

Does TASK.md contain a budget check (Step 0 reading recent log entries, 2x alert rule, drift check)? If not, flag — it costs ~100 tokens/run and catches drift before it gets expensive.

#### Check 5: Usage-credit pool fit (scheduled tasks)

If the task runs on a schedule: remind the user that as of June 15, 2026, non-interactive runs (scheduled/automated, Agent SDK, `claude -p`) draw from a **separate monthly usage-credit pool** — $20 Pro / $100 Max 5x / $200 Max 20x (`/usage-credits` shows the balance).

Estimate: cost per run × runs per month × 1.5 headroom. Ask which plan the user is on, then report what fraction of the pool this task consumes — and flag if the sum across the user's scheduled tasks plausibly exceeds the pool.
Use `AskUserQuestion` with buttons: `Pro` / `Max 5x` / `Max 20x` / `Skip this check`

### Step 3 — Present findings

```
Cost Audit: [task name]
──────────────────────────────
Fixed overhead per run: ~N tokens (always-loaded files)
Estimated cost per run: ~$N on [tier]  |  per month: ~$N of [plan pool]

HIGH IMPACT:
  ⚠ [Check N]: [description] — estimated saving: ~$N/month or ~N tokens/run

MEDIUM IMPACT:
  ⚠ [Check N]: [description]

LOW IMPACT / OPTIONAL:
  ℹ [Check N]: [description]

No issues:
  ✓ [Check N]: [description]
```

Ask:
> "Would you like me to apply these? I can:
> - (A) Instrument RUN_LOG.md — add the per-run metrics block to TASK.md's final step
> - (B) Add a budget-check Step 0 and the 2x alert rule
> - (C) Note the recommended model tier (per step, if hybrid) in TASK.md
> - (D) All of the above
> - (E) Findings only — no changes"

Use `AskUserQuestion` with buttons: `A` / `B` / `C` / `All` / `Findings only`

### Step 4 — Apply fixes

**For option A (metrics instrumentation):** add to TASK.md's final step:

```markdown
Append a metrics block to RUN_LOG.md:
**Duration:** ~N min | **Tokens (est.):** ~NK input, ~NK output | **Tool calls:** N ([breakdown]) | **Notes:** [one line]
```

**For option B (budget check):** add as Step 0 in TASK.md:

```markdown
Step 0: Read the last 5 entries in RUN_LOG.md. If this run's expected scope, or the
average token count, has increased by more than 2x vs. the earliest of the 5, add a
warning to IMPROVEMENTS.md: "Token usage trending up — review what changed."
```

**For option C (model tier):** add a one-line note under the task's Purpose: `Model tier: [tier] ([reason])` — or per-step notes if hybrid.

Show each insertion and get approval before writing. File-size overages (Check 1) are `audit-task-efficiency.md`'s job — offer to run it rather than duplicating the extraction work here.

### Step 5 — Confirm

Tell the user:
- Estimated cost per run and per month, before and after any tier change
- What instrumentation was added
- Remaining manual steps (e.g. changing the model in the scheduler)
- "Re-run after 10+ runs to read the cost trajectory from RUN_LOG.md — stable, step increase, or gradual drift (Guide 10 §Cost Trajectory Patterns)."
