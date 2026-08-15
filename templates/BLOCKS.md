# Building Blocks

> The catalogue of optional pieces a project adds on top of the core layout. The core is
> `templates/PROJECT_TEMPLATE/` — instructions, generated outputs, scratch, archive, and whatever
> holds this project's source of truth. Everything below is a block: something a project earns
> rather than starts with.

## How to use this

A project keeps only the blocks it can already use. The three shipped inside PROJECT_TEMPLATE are
kept or deleted during setup; everything else is added later, when the need actually appears. Two
things make that the right order:

- **Every always-loaded block is paid for in every session**, including the sessions that never
  touch it. The *Loaded* column says which blocks carry that cost. Blocks that load on demand are
  close to free until used; blocks that load per run cost nothing in your sessions at all.
- **An unused block is worse than a missing one.** An empty `Incoming/` nobody drops files into, a
  routing log with no rows, a wiki with three stub pages — each one teaches the next session that
  this project's conventions are decorative.

Installing late is also cheap: the *Install* column names where each block's procedure lives, and
by the time you run it the project has real material to organise rather than a guess.

## Blocks shipped inside PROJECT_TEMPLATE

Delete these during setup if the project does not need them — they are in the folder so the
decision is a deletion rather than an addition.

| Block | What it adds | Add it when | Loaded | Install |
|---|---|---|---|---|
| **Profile & knowledge** | `Profile/PROFILE_SUMMARY.md`, `Profile/PROFILE_detail.md`, `Knowledge/INDEX.md` + topic files | Claude needs context that outlives a session: who people are, where topics stand, what was decided | Summary auto-reads every session; detail and topics on demand | Ships in the template. To retrofit, copy the two folders from `templates/PROJECT_TEMPLATE/` and follow Guide 04 — there is no task for this layer |
| **Intake** | `Incoming/` plus the *Incoming* section of `CLAUDE.md` | Material reaches the project outside a chat — `Incoming/README.md` lists the cases | On demand | Ships in the template; to retrofit, copy the folder and its `CLAUDE.md` section (Guide 24) |
| **Dispatch routing** | `ROUTING_LOG.md` plus the *Dispatch Overrides* section of `CLAUDE.md` | Work here is delegated to subagents, workflow stages, or scheduled tasks | The overrides section auto-loads; the log is read only at calibration | Ships in the template; to retrofit, copy both. The `dispatch` skill is the policy they override (Guide 09) |

## Blocks installed from a task or another template

| Block | What it adds | Add it when | Loaded | Install |
|---|---|---|---|---|
| **Auto-memory** | `.auto-memory/` with an index and memory files, plus the read instruction in `CLAUDE.md` | You want Claude's own cross-session memory layer, alongside profile files or instead of them | The index auto-reads | `tasks/setup-memory.md` (Guide 04) |
| **Scheduled task** | A `[Name]-Task/` folder: `TASK.md`, run log, knowledge summary, improvements log | The same work should happen on a schedule without you starting it | Per run only — invisible to your sessions | `templates/TASK_TEMPLATE/`, via `tasks/setup-scheduled-task.md` (Guides 06, 07) |
| **Self-improving loop** | The improvements and lessons machinery inside an existing task | A task has run enough times that its own output shows what to fix | Per run only | `tasks/setup-self-improving-task.md` (Guide 07) |
| **Task orchestration** | Shared state and hand-off conventions between two or more tasks | A second scheduled task needs to see what the first one did | Per run only | `tasks/setup-orchestration.md` (Guide 09) |
| **Subagent definitions** | `scout`, `builder`, `verifier`, `researcher` with the model tier pinned in frontmatter | You orchestrate work in Claude Code and want delegation to land on the right tier by default | Not in project context — they live in `~/.claude/agents/` | `templates/AGENT_STARTER_PACK/` (Guide 09). Claude Code only; Cowork routes per spawn instead |
| **Registers** | Risk, action, decision, and dependency registers with cross-reference rules | The project tracks linked items where an orphaned ID is a real failure, not a tidiness complaint | On demand, but the cross-reference checklist auto-loads | Copy from `templates/PMO_TEMPLATE/PMO/` and add the checklist to `CLAUDE.md` (Guide 01) |
| **Personal data layer** | A structured home for personal or financial data, with the access rules around it | The project holds data about you that Claude should reason over rather than just store | On demand | `tasks/setup-data-layer.md` (Guide 14) |
| **Wiki** | A curated reference on one subject, index-first | One domain is deep enough that scattered notes keep getting re-explained | On demand, index first | `tasks/setup-wiki.md` (Guide 15) |
| **Project skill** | A `SKILL.md` that triggers on this project's recurring request shapes | You have written the same instructions into three sessions in a row | Description always in context; body on trigger | `tasks/setup-skill.md` (Guide 03) |
| **Policy guardrails** | Tiered rules derived from policies that must not ship in the repo | Work here is bounded by rules you did not write and cannot paste | Depends on tier — see the guide | `tasks/setup-policies.md` (Guide 21) |
| **MCP servers** | Connections to mail, calendar, a filesystem outside the folder, a browser, an API | Claude needs to reach a system rather than a file | Tool schemas load per session — curate the loadout | `tasks/setup-mcp.md` (Guide 05) |
| **Git and ignore hygiene** | `git init`, a remote, `.gitignore` / `.claudeignore` matching what this project holds | Anything here would hurt to lose, or would hurt to commit | Not loaded | `tasks/setup-github.md`, `tasks/setup-ignore-hygiene.md` (Guides 11, 12) |
| **Security hardening** | A credential scan, permission audit, and the shell-command guard hook | Claude runs commands here, or the folder sits near anything sensitive | The hook is not context | `tasks/setup-security.md` (Guide 12) |
| **Reference companion** | `CLAUDE_REFERENCE.md` beside `CLAUDE.md`, with triggers written into the parent | Rules genuinely belong in `CLAUDE.md`, apply rarely, and are expensive to get wrong | On trigger only — that is the point of it | No task: Guide 01, *When CLAUDE.md Cannot Be Short* |
| **Helper app** | A small locally-run tool with its invariants and verification gates written down | You keep asking for the same computed answer and a script would settle it | Not loaded | No task: Guide 22 |
| **Second-brain link** | A one-way return leg from this project to your notes layer | You run a notes layer above your projects and this project produces conclusions worth keeping | Not loaded | No task: Guide 28 |

## What is not a block

Two things that look like blocks and are not:

- **A second purpose.** If the project needs a block because it has quietly become two projects,
  the fix is a split into linked projects, not another folder (Guide 23).
- **The app-side description and instructions fields.** Every Cowork project has all three
  instruction layers whether or not anyone filled them in, so they are part of the core setup,
  not an optional extra (Guide 25).
