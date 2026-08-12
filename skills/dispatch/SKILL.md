---
name: dispatch
description: >
  Route delegated work to the right model tier and effort level. Use this skill whenever the
  session is about to spawn subagents, split a task into parallel or independent parts, choose a
  model or effort for a subtask, workflow stage, or scheduled task, or when the user says things
  like "dispatch", "route this", "orchestrate", "fan out", "run in parallel", "which model should
  this use", or asks for a multi-step task that contains bulk, mechanical, or independent parts —
  including sweeps, audits, and fixes phrased as "sweep all X", "check every Y", "audit the Z",
  "fix what's broken across". Load it ALONGSIDE any playbook or maintenance skill that also
  triggers: that skill says what to do, this one says what model tier does each part. Also use
  when creating or editing a scheduled task, to propose its model tier. Do NOT use for choosing
  the session's own model — a session cannot switch that.
---

# Dispatch — model-aware orchestration

When work is delegated (subagents, workflow stages, scheduled tasks), the model and effort for
each piece are choosable. This skill is the routing policy: it makes the session behave as an
orchestrator that plans and reviews at its own tier while routing the bulk of token volume to
cheaper tiers, with verification as the safety net. The cost spread makes this worthwhile — see
Guide 10 §What Things Actually Cost for the canonical pricing table; the spread between the
cheapest and most expensive tier is roughly 10x.

## Orchestrator stance

When a task decomposes into two or more independent or mechanical subtasks, plan, dispatch, and
review rather than executing everything inline:

1. **Plan** the decomposition and decide tier + effort per subtask from the routing table below.
2. **Dispatch** with self-contained prompts. Subagents do not see the conversation — every prompt
   must carry its own context, file paths, output format, and done-criteria. Independent
   dispatches go out in parallel (in one message / one fan-out).
3. **Review** results against the verification column, then synthesize.

**Return summaries, not payloads.** Instruct every subagent to return a compact summary plus file
paths to its full output — never the full content. An orchestrator that reads every worker's full
output back has re-bought the tokens it saved, and clogs its own context besides.

**Inline floor.** If a subtask is smaller than the cost of briefing a worker — roughly under two
minutes of work, or it would need most of the main context anyway — do it inline. Dispatch has
real fixed costs; routing everything is as wrong as routing nothing. A whole task can land under
the floor: a sweep that reduces to a few grep or script invocations is inline work however many
files it touches. When that happens, note the routing decision anyway (one log line, tier
"inline") so the log shows the policy was consulted, not skipped.

**Composing with playbook skills.** This skill decides *who runs each part*, not *what the parts
are*. When another skill provides the procedure (a maintenance playbook, a review protocol, a
setup task), follow that skill for the steps and this one for the tier of each step. One skill
loading does not displace the other.

## Routing table

| Archetype | Tier | Effort | Verification |
|---|---|---|---|
| Bulk read / extract / classify / OCR; file inventories and sweeps; format conversion; mechanical renames | haiku | low | orchestrator spot-checks a sample |
| Web research legwork; structured drafting from a clear spec; routine code; applying agreed edits | sonnet | medium–high | orchestrator reviews the output |
| Judgment calls; sensitive drafting (legal, financial, anything with figures and dates that will be used); synthesis across sources; verifying lower-tier work | opus | high | second independent pass only if high-stakes |
| Longest-horizon synthesis needing very large context; hardest planning | fable | high–xhigh | rarely dispatched — usually the session itself |

Two standing rules ride on this table:

- **Never route figure-bearing or legal-domain verification below the mid tier.** Extraction may
  run cheap; the check on anything that will be relied on does not.
- **When in doubt between two tiers, take the cheaper one and attach verification.** The
  escalation ladder makes this rational.

## Escalation ladder

Dispatch cheap → check the result → on failure, re-dispatch **one tier up**, quoting the failure
in the new prompt so the retry doesn't repeat it. One escalation maximum; if the second attempt
also fails, do the work inline. This converts "which model is good enough?" from a prediction
into a cheap empirical loop — and escalation frequency is the learning signal (see Routing log).

## Effort

Effort is a second dial on top of tier. Default to the table above; drop to `low` for anything
whose output is a label, a list, or a lookup; raise to `xhigh` only for the hardest verification
or planning stages. Do not pay `high` effort for mechanical work just because it is the default.

## Project overrides

Before routing, check the project's instructions (CLAUDE.md or the project instructions field)
for a **Dispatch Overrides** section. It takes precedence over the table for this project:
default worker tier, content types that must never go below a named tier, and archetypes proven
safe on the cheap tier. If the project has none, the table above applies unmodified.

## Surface bindings

**Cowork:** route via the Agent tool's `model` parameter per spawn. When a fan-out would exceed
roughly five agents or needs staged verification, propose a Workflow instead — but workflows
require the user's explicit opt-in ("use a workflow" / ultracode), so ask; plain Agent-tool
dispatch needs no opt-in. Agent definition files do not persist between Cowork sessions; this
skill plus per-spawn parameters are the mechanism.

**Claude Code:** prefer the named agents from the starter pack if installed (`scout`, `builder`,
`verifier`, `researcher` — see `templates/AGENT_STARTER_PACK/` in Cluide), since their frontmatter
pins tier structurally. Otherwise pass the per-invocation `model` parameter. Recommended session
default for orchestrating work: `opus` (or `opusplan` where plan/execute phases are distinct).

**Scheduled tasks:** when creating or editing one, propose the cheapest tier the task's hardest
step needs, per the table — and say which step set the tier. Never change an existing scheduled
task's model without the user asking (standing rule).

## Routing log

If the project contains a `ROUTING_LOG.md`, append one line per dispatched subtask:

```
| 2026-08-12 | bulk-extract | haiku | low | N | 34 receipts parsed, spot-check clean |
```

Columns: date, archetype, tier, effort, escalated (Y/N), one-line outcome. This log is the
learning loop's input: a periodic review demotes archetypes that never escalate and promotes
those escalating more than ~1 in 3, as proposals for the user to approve. If the project has no
routing log, skip logging — do not create the file unasked.

## What this skill does not do

- It cannot switch the session's own model; that is set by the user at task start. If the session
  model is clearly mismatched to the task, say so once and continue.
- It does not start workflows on its own authority (opt-in required, see above).
- It does not override a project's own rules; local instructions always win.
