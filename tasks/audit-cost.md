# Task: Audit Task Cost

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/audit-cost.md` (then specify which task folder to audit)
> **Source guide:** `10_COST_PERFORMANCE.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Purpose
Audit a task folder's token economics against Guide 10: always-loaded file sizes vs. budgets, model tier appropriateness, run-metrics instrumentation, and monthly budget vs. the plan's usage allowance. Returns a prioritised list of findings and applies the agreed fixes.

**Companion:** `tasks/audit-task-efficiency.md` covers *how* to reduce tokens (file splitting, triage, trim policies). This task covers *what the task costs* and whether that cost is visible, budgeted, and on the right model tier. Run both for a full picture.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Identify the task to audit

Ask: "Which task folder should I audit? Provide the path (e.g. `tasks/my-task/`)."

Read `TASK.md` and list the folder contents. Identify:
- Every file the task reads on every run (always-loaded files)
- Whether `RUN_LOG.md` exists and what each entry records
- How often the task runs (from TASK.md, or ask)
- Which model tier it runs on (ask if not stated)
  Use only model identifiers exposed by the current runtime; record unknown when the model is unavailable.

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

Identify the provider, actual configured model and supported alternatives from the current runtime. Compare quality, latency and measured usage on representative fixtures before recommending a cheaper option. Separate mechanical extraction from judgment only when the host supports that dispatch and the savings justify it. Claude model names are not aliases for OpenAI models.

Use Guide 10 and the provider's current official pricing/model documentation. Do not copy a cached lineup into this task. Retain the configured model if no supported alternative or comparable measurement is available.

#### Check 3: Run metrics instrumentation

Does `RUN_LOG.md` capture per-run metrics? Each entry should record (Guide 10 §Run Metrics Pattern): duration, estimated input/output tokens, tool/API call count, one-line summary.

- Metrics present → check for trend patterns: stable / step increase / gradual drift (compare last 5 runs vs. runs 16–20 if 20+ entries exist)
- Metrics absent → flag: "No cost visibility — add the metrics block" (offered in Step 4)

#### Check 4: Budget check and alerting

Does TASK.md contain a budget check (Step 0 reading recent log entries, 2x alert rule, drift check)? If not, flag — it costs ~100 tokens/run and catches drift before it gets expensive.

#### Check 5: Plan usage fit (scheduled tasks)

Identify the billing surface: API billing, subscription allowance, or an app-specific meter. For API calls, use measured token categories and current vendor prices, then estimate runs/month with stated headroom. For subscription runs, use the account's current usage/reset tools or settings; never divide an API dollar estimate by a subscription price to invent a remaining allowance. Record unavailable usage as unknown. Check whether scheduled runs share an allowance using the actual product's current official source.

Report token estimates, measured metrics and billed dollars in separate fields. Do not invent token counts when the runtime does not expose them.

### Step 3 — Present findings

```
Cost Audit: [task name]
──────────────────────────────
Fixed overhead per run: ~N tokens (always-loaded files)
Estimated cost per run: ~$N on [tier]  |  per month: ~$N of [plan allowance]

HIGH IMPACT:
  ⚠ [Check N]: [description] — estimated saving: ~$N/month or ~N tokens/run

MEDIUM IMPACT:
  ⚠ [Check N]: [description]

LOW IMPACT / OPTIONAL:
  ℹ [Check N]: [description]

No issues:
  ✓ [Check N]: [description]
```

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

Ask:
> "Would you like me to apply these? I can:
> - (A) Instrument RUN_LOG.md — add the per-run metrics block to TASK.md's final step
> - (B) Add a budget-check Step 0 and the 2x alert rule
> - (C) Note the recommended model tier (per step, if hybrid) in TASK.md
> - (D) All of the above
> - (E) Findings only — no changes"

Use the available question tool, or ask in chat: `A` / `B` / `C` / `All` / `Findings only`

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
