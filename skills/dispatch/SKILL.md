---
name: dispatch
description: >
  Route delegated work to the right model tier and effort level. Use whenever the session is about
  to spawn subagents, split a task into parallel or independent parts, or choose a model or effort
  for a subtask, workflow stage or scheduled task; when the user says "dispatch", "route this",
  "orchestrate", "fan out", "run in parallel", "which model should this use"; or for multi-step
  work with bulk, mechanical or independent parts, including "sweep all X", "check every Y", "audit
  the Z", "fix what's broken across". Load it ALONGSIDE any playbook skill that also triggers: that
  skill says what to do, this one says which tier does each part. Also use when creating or editing
  a scheduled task, to propose its tier. This is model-tier routing, not the Cowork Dispatch sidebar
  agent. Do NOT use for choosing the session's own model; a session cannot switch that.
---

# Dispatch — model-aware orchestration

This skill is the routing policy for delegated work: the session plans and reviews at its own
tier, sends the bulk of the token volume to cheaper workers, and uses verification as the safety
net. It pays for two reasons. In most real tasks the bulk of the volume is mechanical — reading,
extracting, sweeping, applying agreed edits — and does not need the top tier. And workers burn
their own context windows, which keeps the orchestrator's clear for planning and review. Rates
change; for an actual comparison use current provider pricing (Guide 10 §What Things Actually
Cost names the sources) and measured usage, never a remembered spread.

Use it only when delegation is available and permitted by the host and the user's scope. Sections
1–4 and 7 apply on every platform. Section 5 is the Claude binding, section 6 the OpenAI one: model
identifiers and tool parameters are native to each runtime, and neither is a translation of the
other. Not to be confused with any product feature also named Dispatch.

## 1. When to dispatch

When a task decomposes into two or more independent or mechanical subtasks, **plan** the
decomposition and the tier of each part, **dispatch** with self-contained briefs (independent
ones in parallel, in one message or one fan-out), then **review** the results against the
verification rules and synthesize.

**Inline floor.** Do a subtask inline when any of these holds: it takes fewer than about five
tool calls; it reduces to a few greps or one script, however many files it touches; it needs most
of the main context anyway; or the brief would be longer than the work. Dispatch has real fixed
costs — routing everything is as wrong as routing nothing. A consulted-but-inline decision still
gets a log line with key `inline` (§7), so the log shows the policy was applied, not skipped.

**Size the fan-out in batches, not items.** How many workers a task splits into usually moves
cost more than which tier runs them: every spawn re-buys its briefing, its context, and its
overhead. Batch homogeneous items so each worker gets meaningful volume — one scout per fifty
files, not per file. Split finer only when items are truly independent *and* wall-clock matters.

**Return summaries, not payloads.** Every worker returns a compact summary. One that may write
puts its full output in a file and returns the path; a read-only worker returns a bounded summary
inline. An orchestrator that reads every worker's full output back has re-bought the tokens it
saved, and clogs its own context besides.

**Past roughly five concurrent agents, or when stages need verifying between them, propose a
Workflow** where the host has one — within its stated size guideline, and only with the user's
explicit opt-in.

**Composing with playbook skills.** This skill decides *who runs each part*, not *what the parts
are*. When another skill provides the procedure (a maintenance playbook, a review protocol, a
setup task), follow that skill for the steps and this one for the tier of each step. One skill
loading does not displace the other. Because policy skills lose trigger races to playbooks, a
project that delegates should carry a load hook in its always-loaded instructions (§5, Project
overrides).

## 2. The brief

Assume the worker sees nothing of this conversation — context inheritance depends on the host
and the spawn mode, and a brief that relies on it breaks on the next surface. Every brief carries:

```
Goal and done-when:   what finished looks like, in checkable terms
Context:              the facts and decisions the worker needs, stated, not referenced
Visible scope:        exactly which files or sources it has been given
May write:            its own file set, or "nothing"
Output:               full result to <path> and a summary of at most N lines plus the path;
                      read-only workers return the bounded summary inline
Verification scope:   verifier briefs only: full recheck, or a sample of stated size
```

- **Visible scope is a claim limit.** A worker that was given a subset must report "not in what I
  was given", never "missing". Absence findings from a partial view are false findings.
- **Parallel writers get disjoint file sets.** One owner per file; the orchestrator merges.
- **Quote, don't summarise, what must be exact** — a figure, a rule, the wording to apply.

## 3. Verification

- **Figure-bearing and legal-domain checks never run below the mid tier.** Extraction may run
  cheap; the check on anything that will be relied on does not.
- **State the scope.** Bulk cheap-tier output gets a sample by default — a full recheck at the
  verify tier can cost more than doing the work one tier up would have, which erases the saving.
  Reserve full rechecks for figure-bearing and legal-domain content that will be relied on.
- **Keep the verifier independent.** Give it the artefact and the criteria or spec, not the
  author's reasoning and not your own view; write its brief before you state a conclusion. A
  spawn that inherits the conversation (a fork) is not an independent check (Guides 26, 27).
- **Re-read what ships.** A lookup or extraction worker can misread its source. A claim that will
  be published or relied on is checked against the primary source by the orchestrator before it
  is used, and any correction is logged (§7).
- **When in doubt between two tiers, take the cheaper one and attach verification.** The
  escalation ladder makes this rational — except for work whose failure is expensive to detect
  or to retry: code, or anything that re-reads a large context. Per-token price is not per-task
  cost. Every turn and every retry re-sends the worker's whole context, so a cheaper tier that
  fails once can cost more than the tier above getting it right first time. Start that work at
  the tier that usually succeeds.

## 4. Escalation ladder

Dispatch cheap → check the result → on failure, re-dispatch **one tier up**, quoting the failure
in the new brief so the retry doesn't repeat it. One escalation maximum; if the second attempt
also fails, do the work inline. Where the host exposes no higher tier (a single configured model),
the ladder is one retry with the failure quoted, then inline. This turns "which model is good
enough?" from a prediction into a cheap empirical loop, and escalations and corrections are the
learning signal (§7).

**Effort before tier.** Where the surface sets effort per call (§5 says where the Claude dial
exists), the one escalation may instead be an effort step at the same tier — `medium` to `high`.
Take it when the worker had the right approach but stopped short: a shallow answer, a fix at one
layer when the fault spans two. Take the tier step when it misread the task or lacked the
capability. Extra reasoning on one attempt usually costs less than a retry loop. Log either kind as
escalated, and name the step in the outcome.

## 5. Claude binding

Tier names below are model families — the values the `model` parameters accept — not versions.
Confirm the names against the active tool schema before dispatch; if the lineup has changed since
this skill was last edited, follow the schema and current product documentation, not this table.

### Routing table

| Archetype | Log keys | Tier | Effort | Verification |
|---|---|---|---|---|
| Bulk read / extract / classify / OCR; file inventories and sweeps; format conversion; mechanical renames | `bulk-extract`, `sweep`, `convert` | haiku | low | orchestrator spot-checks a sample |
| Web research; lookups in docs, logs and test output; structured drafting from a clear spec; applying agreed edits whose wording the brief gives | `research`, `docs-lookup`, `draft-to-spec`, `apply-edits` | sonnet | medium | orchestrator reviews the output |
| Writing or changing code, including routine code to a clear spec | `code` | opus | medium | the worker runs the code or its tests; orchestrator reviews the diff |
| Judgment calls; sensitive drafting (legal, financial, anything with figures and dates that will be used); synthesis across sources; verifying lower-tier work | `judgment`, `sensitive-draft`, `synthesis`, `verify` | opus | high | second independent pass only if high-stakes |
| Hardest planning; longest-horizon synthesis; long unsupervised runs and problems with no existing pattern, where the result matters more than the token price | `plan` | fable | high | rarely dispatched — usually the session itself |

Code sits on the top working tier at `medium`, not on sonnet: a wrong first attempt at code is
expensive to detect and to retry, so the cheaper tier rarely stays cheaper per task (§3). This
follows Anthropic's guidance for the current lineup — smaller models "for lookups, not for writing
code" ([What a task costs on Opus 5.5](https://claude.com/blog/what-a-task-costs-on-opus-5-5), 2026-09-22) — and is a starting point
for calibration (§7), not a finding of any routing log. The `code` key keeps its name, so the log
can demote it again if it never escalates.

The Effort column is a per-row default, not a range. Drop to `low` for anything whose output is a
label, a list, or a lookup; raise to `high` on sonnet for drafting that needs real care, and to
`xhigh` only for the hardest verification or planning stages. Do not pay `high` effort for
mechanical work because it is the default. `max` is a setting for a single session, not a worker
default.

**Where the effort dial exists.** Workflow stages expose per-call `effort`, and Claude Code agent
frontmatter pins it per agent (`effort:` — the starter pack does this). A Cowork Agent-tool spawn
has **no effort parameter**: it sets tier only, and effort comes from the agent definition. Route
effort-sensitive stages through a Workflow (opt-in required) or accept the definition's default;
never claim an effort level the surface cannot set.

### Make every spawn's model explicit

- **Never leave the tier to inheritance.** A spawn's model resolves in this order: the per-spawn
  `model` parameter, the agent definition's `model`, any configured default subagent model, then
  the **main conversation's model**. So pass `model` on every spawn of a type whose definition
  sets none (general-purpose, for example): in an Opus or Fable session a forgotten
  parameter runs a mechanical worker at the top tier, silently. For a type that pins its tier
  (the starter pack), omit it or pass the same tier — a passed value overrides the pin.
- **Forks ignore routing.** A fork runs on the parent's model whatever you pass, and inherits the
  whole conversation. Never use one for cheap-tier work or for independent verification; name a
  non-fork type.
- **Agent type is a second, separate choice.** The type decides tools and standing instructions
  (a read-only type for scouting; a docs-lookup type for product questions — some have no Write
  tool, so ask for the result inline); `model` decides the tier. Choose both.

### Surfaces

**Cowork:** route via the Agent tool's `model` parameter per spawn (tier only; see effort above).
The Workflow threshold in §1 applies; workflows require the user's explicit opt-in ("use a workflow"
/ ultracode), so ask — plain Agent-tool dispatch needs no opt-in. Agent definition files do not
persist between Cowork sessions; this skill plus per-spawn parameters are the mechanism.

**Claude Code:** prefer the named agents from the starter pack if installed (`scout`, `builder`,
`verifier`, `researcher` — see `templates/AGENT_STARTER_PACK/` in Cluide), since their frontmatter
sets tier and effort by default, without re-deciding them per prompt. `builder` is pinned to
sonnet; for code, spawn it with `model: opus`, which overrides the pin. Otherwise pass the
per-invocation `model` parameter. Recommended session default for orchestrating work: `opus` (or
`opusplan` where plan and execute phases are distinct). From v2.1.251, `CLAUDE_CODE_SUBAGENT_MODEL`
is only a fallback default — a definition's model or a per-spawn model still wins; on earlier
versions it overrode both, so no routing took effect while it was set.
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (v2.1.257+) restores that override deliberately: it ignores
every definition's `model` field and blocks per-spawn models. Check for both variables, and the
version, before routing.

**Enforcement, and its limit.** A permission deny rule such as `Agent(model:opus)` refuses calls
that pass that literal alias. It does not match a call that omits `model` — which inherits the
session's model — nor one that names a full model ID. It blocks explicit requests, not
inheritance, so pair it with the rule above. For a real ceiling, use an `availableModels`
allowlist: it applies to the session model, definitions, the Agent tool's `model` parameter and
`CLAUDE_CODE_SUBAGENT_MODEL`, so inheritance cannot escape it, and routing below the ceiling
still works (`enforceAvailableModels`, managed settings only, extends it to the Default option).
`_FORCE=1` is a pin, not a ceiling, and it removes routing.

**Scheduled tasks:** propose the cheapest available tier that meets the task's hardest step, and
name the step that set it. Never change an existing scheduled task's model without the user
asking.

### Project overrides

Before routing, check the project's always-loaded Claude instructions — the `CLAUDE.md` adapter,
or the project instructions field in an app project — for a **Dispatch Overrides** section. It
takes precedence over the table for this project and holds:

- the load hook: "load `dispatch` alongside any playbook skill when a task has bulk, parallel or
  mechanical parts" — the reliable fix for the trigger race in §1;
- the default worker tier — say whether it replaces the table's cheap tier or only covers work no
  row places;
- content types that must never go below a named tier;
- archetypes proven safe on the cheap tier (from calibration, §7);
- where the routing log lives.

Without overrides, use the table above. Local instructions always win over this skill.

## 6. OpenAI binding

Use only the delegation controls exposed in the active Codex or ChatGPT session. Retain the
configured model unless the user requests a supported alternative or the project's explicit
policy selects one; never translate a Claude tier name into a guessed OpenAI identifier. A task in
the app sidebar, a subagent, and an API call are different resources — do not create a user-owned
task as a hidden worker. Sections 1–4 apply unchanged: self-contained brief, restricted write
ownership, summaries back, stated verification scope. Record the actual model and effort in the
log rather than a Claude analogue, and if settings are not exposed, say so and retain the
defaults. Verify the host's context-inheritance behaviour before calling a reviewer independent.
If the surface has no delegation tool, execute inline and record that limitation. OpenAI routing
decisions live in the project's `PLATFORM_SETUP.md`, not in the Claude adapter.

## 7. Routing log

If the project keeps a routing log (`ROUTING_LOG.md` at the root, or `development/ROUTING_LOG.md`),
append one line per dispatched subtask and per consulted-but-inline decision:

```
| 2026-09-23 | bulk-extract: 34 receipts | haiku | low | N | 0 | spot-check clean |
```

Columns: date, archetype, tier, effort, escalated (Y/N), corrected, one-line outcome.

- **Archetype** starts with one log key from the §5 table's Log keys column (or `inline`),
  optionally followed by a colon and detail. The keys name the kind of work, not a Claude tier,
  so OpenAI rows use them too. Free-text labels cannot be grouped, and a calibration that cannot
  group never fires.
- **Corrected** is the number of worker output items the orchestrator had to fix or discard
  (`—` for inline rows). A correction is a failure the ladder did not see; count it as one.

Calibration (`tasks/review-tasks.md` step 4d in Cluide) groups rows by key. A key with ~10+
dispatches and no escalations or corrections is a candidate to demote a tier; one failing — escalated
or corrected — more than ~1 in 3 is a candidate to promote. Both are proposals for the user;
approved changes go into Dispatch Overrides (Claude) or the OpenAI routing section of
`PLATFORM_SETUP.md`, never into the log. If the project has no routing
log, skip logging — do not create the file unasked.

## What this skill does not do

- It cannot switch the session's own model; that is set by the user at task start. If the session
  model is clearly mismatched to the task, say so once and continue.
- It does not start workflows on its own authority (opt-in required, see above).
- It does not override a project's own rules; local instructions always win.
