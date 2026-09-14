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
  when creating or editing a scheduled task, to propose its model tier. This is model-tier routing,
  not the Cowork Dispatch sidebar agent, which runs long background tasks and is unrelated to model
  routing. Do NOT use for choosing the session's own model — a session cannot switch that.
---

# Dispatch — model-aware orchestration

Use this skill only when delegation is available and permitted by the host and the user's scope. Start by listing the actual supported models and effort controls. The same workflow can be used with Claude or OpenAI, but model identifiers and tool parameters are native to each runtime.

For OpenAI, retain the configured model unless the user requests a supported alternative or the project's explicit policy selects one. Do not translate Claude tier names. If the surface has no delegation tool, execute the task inline and record that limitation. For Claude, the table below is a routing policy using Claude family names; verify that the requested names are available before invoking them.

Cost comparison belongs in Guide 10. Use measured usage and current provider rates where available; do not assume a fixed price spread. This skill concerns model routing, not any product feature also named Dispatch.

## Orchestrator stance

When a task decomposes into two or more independent or mechanical subtasks, plan, dispatch, and
review rather than executing everything inline:

1. **Plan** the decomposition and select the native controls: retain configured OpenAI defaults, or use the Claude routing table for available Claude models.
2. **Dispatch** with self-contained prompts. Context inheritance depends on the host and spawn mode; every prompt
   must carry its own context, file paths, output format, and done-criteria. Independent
   dispatches go out in parallel (in one message / one fan-out).
3. **Review** results against the verification column, then synthesize.

**Size the fan-out in batches, not items.** How many workers a task splits into usually moves
cost more than which tier runs them: every spawn re-buys its briefing, its context, and its
overhead. Batch homogeneous items so each worker gets meaningful volume — one scout per fifty
files, not per file. Split finer only when items are truly independent *and* wall-clock matters,
and past roughly five concurrent agents propose a Workflow instead (see Surface bindings).

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

## Claude routing table

| Archetype | Tier | Effort | Verification |
|---|---|---|---|
| Bulk read / extract / classify / OCR; file inventories and sweeps; format conversion; mechanical renames | haiku | low | orchestrator spot-checks a sample |
| Web research legwork; structured drafting from a clear spec; routine code; applying agreed edits | sonnet | medium | orchestrator reviews the output |
| Judgment calls; sensitive drafting (legal, financial, anything with figures and dates that will be used); synthesis across sources; verifying lower-tier work | opus | high | second independent pass only if high-stakes |
| Longest-horizon synthesis needing very large context; hardest planning | fable | high | rarely dispatched — usually the session itself |

The Effort column is a per-row default, not a range; when and how to deviate is the Effort
section's job. Three standing rules ride on this table:

- **Never route figure-bearing or legal-domain verification below the mid tier.** Extraction may
  run cheap; the check on anything that will be relied on does not.
- **When in doubt between two tiers, take the cheaper one and attach verification.** The
  escalation ladder makes this rational.
- **A dispatched verification states its scope in the brief: full recheck, or a sample of stated
  size.** Bulk cheap-tier output gets a sample by default — a full recheck at the verify tier can
  cost more than doing the work one tier up would have, which erases the saving routing exists to
  capture. Reserve full rechecks for what the first rule mandates: figure-bearing and legal-domain
  content that will be relied on.

## Claude escalation ladder

Dispatch cheap → check the result → on failure, re-dispatch **one tier up**, quoting the failure
in the new prompt so the retry doesn't repeat it. One escalation maximum; if the second attempt
also fails, do the work inline. This converts "which model is good enough?" from a prediction
into a cheap empirical loop — and escalation frequency is the learning signal (see Routing log).

## Claude effort defaults

Effort is a second dial on top of tier. Default to the table above; drop to `low` for anything
whose output is a label, a list, or a lookup; raise to `high` on sonnet for drafting that needs
real care, and to `xhigh` only for the hardest verification or planning stages. Do not pay `high`
effort for mechanical work just because it is the default.

Know where the dial actually exists. Workflow stages expose per-call `effort`, and Claude Code
agent frontmatter pins it per agent (that is what the starter pack does). A plain Cowork Agent
spawn has **no effort parameter** — it controls tier only, and effort comes from the agent
definition. So in Cowork, route effort-sensitive stages through a Workflow (opt-in required) or
accept the definition's default; do not claim an effort level the surface cannot set.

## Project overrides

Before routing, check the shared policy and native adapter (or the project instructions field)
for a **Dispatch Overrides** section. It takes precedence over the table for this project:
default worker tier, content types that must never go below a named tier, and archetypes proven
safe on the cheap tier. For Claude without overrides, use the Claude table. For OpenAI without overrides, retain configured defaults.

## Surface bindings

**OpenAI:** use only the delegation controls exposed in the active Codex/ChatGPT session. A task in the app sidebar, a subagent, and an API call are different resources; do not create a user-owned task as a hidden worker. Supply a self-contained brief, restrict write ownership, and record actual model/effort rather than a Claude analogue. If settings are not exposed, retain the defaults and state that. Verify the host's context-inheritance behavior before calling a reviewer independent.

**Claude examples below:** these bindings require the named tools to be present. Check current product documentation or the active tool schema before dispatch; do not infer support from a name in this skill.

**Cowork:** route via the Agent tool's `model` parameter per spawn (tier only — there is no
per-spawn effort parameter; see Effort). When a fan-out would exceed
roughly five agents or needs staged verification, propose a Workflow instead — but workflows
require the user's explicit opt-in ("use a workflow" / ultracode), so ask; plain Agent-tool
dispatch needs no opt-in. Agent definition files do not persist between Cowork sessions; this
skill plus per-spawn parameters are the mechanism.

**Claude Code:** prefer the named agents from the starter pack if installed (`scout`, `builder`,
`verifier`, `researcher` — see `templates/AGENT_STARTER_PACK/` in Cluide), since their frontmatter
pins tier structurally. Otherwise pass the per-invocation `model` parameter. Recommended session
default for orchestrating work: `opus` (or `opusplan` where plan/execute phases are distinct).
Check that `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is not set: at `1` it ignores the `model` field of
every subagent definition and blocks passing a model per spawn, so no routing in this skill takes
effect. In the other direction, a permission deny rule of the form `Agent(model:<tier>)` enforces a
ceiling that project overrides can otherwise only advise.

**Scheduled tasks:** for Claude, propose the cheapest available tier that meets the task's hardest step. For OpenAI, retain the configured model unless an alternative is requested and supported. Never change an existing scheduled
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
