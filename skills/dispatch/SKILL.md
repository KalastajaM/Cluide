---
name: dispatch
description: >
  Model-tier routing for delegated work. Use right before spawning a subagent (Agent or Task
  tool), when planning a fan-out or workflow stages, or when setting the model or effort of a
  subtask or scheduled task; also when the user asks which model delegated work should use, or
  says "route this", "tier routing" or "fan out". Load it alongside any playbook skill: the
  playbook says what to do, this says which tier does each part. Not for the session's own model
  (a session cannot switch it) and not the Cowork Dispatch background agent.
---

# Dispatch — model-tier routing for delegated work

The session plans and reviews at its own tier, sends the bulk of the volume to cheaper workers,
and uses verification as the safety net. Workers also burn their own context, which keeps the
orchestrator's clear. Precedence: the host's rules on whether to delegate at all, then the
project's **Dispatch Overrides** (§7), then this skill.

## 1. Inline or delegate

**Inline floor.** Do it inline when any holds: under about five tool calls; a few greps or one
script, however many files; it needs most of the main context; the brief would be longer than the
work. Routing everything is as wrong as routing nothing.

**Split by context, not by kind of work.** Every handoff loses detail. Good candidates need little
from the rest and return a compact result: an independent research path, a component with a clean
interface, a black-box verification. Steps that chain on each other's output stay in one loop.
Never build researcher → writer → editor chains.

**Batch the fan-out.** Worker count usually moves cost more than tier: each spawn re-buys its brief,
its context and its own prompt cache. One worker per ~50 homogeneous items, not per item. Split
finer only when items are independent *and* wall-clock matters. Send independent spawns in one
message.

**Summaries, not payloads.** A writing worker puts full output in a file and returns the path plus
a bounded summary; a read-only worker returns the bounded summary inline. Reading every full
output back re-buys the saved tokens.

**Past ~5 concurrent workers, or stages that need checks between them,** propose a Workflow where
the host has one, and only start it with the user's explicit opt-in.

## 2. Routing table (Claude)

Tier = the `model` value (family alias, not a version). Effort = the `effort` value: pass it
explicitly on every spawn as given here; this table is the instruction to set it.

| Archetype | Log key | model | effort | Verification |
|---|---|---|---|---|
| Bulk read/extract/classify/OCR, inventories, sweeps, format conversion, mechanical renames | `bulk-extract` `sweep` `convert` | haiku | low | orchestrator samples |
| Web research, lookups in docs/logs/test output, drafting to a clear spec, applying edits whose wording the brief gives | `research` `docs-lookup` `draft-to-spec` `apply-edits` | sonnet | medium | orchestrator reviews |
| Writing or changing code, even routine code to spec | `code` | opus | medium | worker runs code/tests; orchestrator reviews diff |
| Judgment; sensitive drafting (legal, financial, figures and dates that will be used); cross-source synthesis; verifying lower-tier work | `judgment` `sensitive-draft` `synthesis` `verify` | opus | high | second independent pass only if high-stakes |
| Hardest planning, longest-horizon synthesis, novel problems where the result outweighs price | `plan` | fable | high | rarely dispatched; usually the session itself |

- Code sits on opus because a wrong first attempt is expensive to find and retry; per-token price
  is not per-task cost. Calibration (§8) may demote it.
- Effort column is a default, not a range: `low` for anything returning a label, list or lookup;
  `high` on sonnet for drafting that needs care; `xhigh` only for the hardest verify or plan stage;
  never `max` on a worker. A level the model lacks silently falls back to the highest it supports.
- `fable` carries extra safeguards in biology, cybersecurity and AI R&D; if a fable worker is
  limited there, use opus.
- If the Agent tool's schema lists different `model` values than this table, follow the schema
  and current product docs, and say the table is stale.

## 3. Every spawn

- **Name the model.** Resolution: per-spawn `model` → agent definition's `model` → configured
  default subagent model → **the session's model**. An unpinned type (general-purpose, for
  example) with no `model` in an Opus or Fable session runs bulk work at the top tier,
  silently. For a type whose definition pins a tier, omit `model` or pass the same value; a passed
  value overrides the pin.
- **Name the effort.** Resolution in Claude Code: `CLAUDE_CODE_EFFORT_LEVEL` (if set, it wins and
  the per-spawn parameter disappears) → per-spawn `effort` → definition's `effort:` →
  `CLAUDE_CODE_SUBAGENT_EFFORT` (v2.1.316+) → the session's level. If the schema has no `effort`,
  say so; never claim a level the surface cannot set.
- **No forks for routed work.** A fork runs on the parent's model and inherits the whole
  conversation whatever you pass. Never use one for cheap-tier work or independent review.
- **Type is a separate choice.** Type decides tools and standing instructions (read-only for
  scouting; some types lack Write, so ask for results inline); `model` decides tier. Choose both.
  Prefer a project's model-pinned agent types where they exist.
- **Claude Code settings that change routing — check before routing:** `CLAUDE_CODE_SUBAGENT_MODEL`
  (fallback default only), `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (pins every subagent, routing off),
  `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` (all workflow agents on one model), `maxEffortLevel` (caps
  effort), `availableModels` (a real ceiling inheritance cannot escape). A deny rule like
  `Agent(model:opus)` blocks only calls naming that alias, not inheritance.
- **Session default for orchestrating** (user's choice, not this skill's): `opus`, or `opusplan`
  where plan and execute phases are distinct.
- **Cowork:** per-spawn `model` and `effort` are the whole mechanism; agent definitions do not
  persist between sessions.
- **Scheduled tasks:** propose the cheapest tier that meets the hardest step, and name that step.
  Never change an existing task's model unasked.

## 4. The brief

Assume the worker sees nothing of this conversation.

```
Goal and done-when:  what finished looks like, in checkable terms
Context:             facts and decisions it needs, stated, not referenced
Visible scope:       exactly which files or sources it has
May write:           its own file set, or "nothing"
Output:              full result to <path>, summary of at most N lines; read-only: summary inline
Verification scope:  verifier briefs only: full recheck, or sample of stated size
```

- Visible scope limits claims: a worker given a subset reports "not in what I was given", never
  "missing".
- Parallel writers get disjoint file sets; the orchestrator merges.
- Quote, don't summarise, anything that must be exact: a figure, a rule, the wording to apply.

## 5. Verification

- Figure-bearing and legal checks never run below sonnet; extraction may run cheap, the check on
  anything relied on does not.
- State the scope. Bulk output: sample ~1 in 5, minimum 3; a failed sample fails the batch. Full
  recheck only for figure-bearing or legal content that will be relied on.
- Keep the verifier independent: a non-fork type, given the artefact and the criteria, not the
  author's reasoning or your view. Write its brief before stating your own conclusion.
- Re-read what ships: a claim that will be published or relied on is checked against the primary
  source by the orchestrator, and corrections are logged.
- Unsure between two tiers: take the cheaper and attach verification, except for code or anything
  re-reading a large context, where a retry costs more than the tier gap. Start those at the tier
  that usually succeeds.

## 6. Escalation ladder

Dispatch → check → on failure, re-dispatch **one step up**, quoting the failure in the new brief.
One escalation; if it also fails, do it inline. The step is an effort raise at the same tier when
the worker had the right approach but stopped short, a tier raise when it misread the task or
lacked capability. With only one model available: one retry with the failure quoted, then inline.
Log either kind as escalated and name the step in the outcome.

## 7. Project overrides

Before routing, check the project's always-loaded instructions (CLAUDE.md, or the app project's
instructions field) for a **Dispatch Overrides** section. It wins over §2 and holds:

- the load hook: "Load `dispatch` alongside any playbook skill when a task has bulk, parallel or
  mechanical parts." Policy skills lose trigger races to playbooks; this line is the reliable fix.
- the default worker tier, and whether it replaces the cheap rows or only fills gaps;
- never-below floors for named content types (dated if added after a failure, so calibration does
  not treat them as cost tuning);
- archetypes proven safe on the cheap tier;
- where the routing log lives.

Without overrides, use §2.

## 8. Routing log and calibration

If the project has a `ROUTING_LOG.md` (root or `development/`), append one row per dispatched
subtask and per consulted-but-inline decision. Never create the log unasked.

```
| 2026-11-08 | bulk-extract: 34 receipts | haiku | low | N | 0 | sample clean |
```

Columns: date, archetype (a §2 log key or `inline`, optional `: detail`), model, effort,
escalated Y/N, corrected (items the orchestrator fixed or discarded; `—` for inline), outcome.

Calibration groups rows by key. ~10+ rows with no escalations or corrections: propose demoting one
tier. Failing more than ~1 in 3: propose promoting. Under ~10 rows: "insufficient data". Proposals
go to the user; approved changes go into Dispatch Overrides, never into the log.

## 9. Other platforms

On OpenAI (Codex, ChatGPT) or Google (Antigravity, Jules, Gemini app) hosts, §1 and §4–§6 apply
unchanged. Use only the delegation controls the session exposes, keep the configured model unless
the user picks a supported alternative, and never map a Claude tier onto a guessed model name. Log
the actual model and effort. Check whether a spawned reviewer inherits context before calling it
independent. A user-visible task in an app sidebar is not a hidden worker; do not create one as
such. No delegation tool: do it inline and say so.

## Does not do

- Switch the session's own model. If it is clearly mismatched, say so once and continue.
- Start a Workflow without the user's opt-in.
- Override host rules or a project's own instructions.
