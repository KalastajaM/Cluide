# Task: Analyze Project

> **Cluide task** — run this from a Cluide checkout to analyze *another* Claude project end-to-end:
> `Assistant, run tasks/analyze-project.md`
> **Source guides:** the full Cluide set (01–35). Per-dimension criteria and the output template live
> in `tasks/analyze-project-reference.md` (read on demand).

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Purpose
Analyze another assistant project — Claude, ChatGPT or Codex, from a **local folder**, **GitHub repo**, or **project sources** —
against the full Cluide guide set, and write a single **improvement plan** into that project:
`CLUIDE_IMPROVEMENT_PLAN.md`. The plan scores every applicable dimension, lists prioritised findings,
and tells the user exactly which `setup-*` / `audit-*` task or skill implements each fix.

This task is **read-only on the target** except for writing that one plan file. It **does not implement
any changes** — it produces a reviewed plan and stops. Implementation is a separate, deliberate step the
user starts later, guided by the plan. It is the project-wide counterpart to the per-component
`audit-*` tasks: where each `audit-*` task inspects one component, this sweeps the whole project and
consolidates the result into one actionable document.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 0 — Locate the target and confirm Cluide is available

This task **reads** another project and writes **one** file into it. Two things must be true to start:

1. **Cluide guides are present.** Confirm the current working directory is a Cluide checkout (it
   contains `00_INDEX.md` and a `tasks/` folder). The dimension criteria reference the root guides. If
   Cluide is not the working repo, stop and ask the user to run this from Cluide.
2. **The target is reachable.** For source-only projects, inventory supplied files and project instructions; mark missing sources and return a downloadable/inline plan if no write path exists. Otherwise: Ask whether the target project is a **local folder** or a **GitHub
   repo** (using the available question tool or chat). Then handle the mode — see
   `analyze-project-reference.md § Input handling` for the detail:
   - **Local folder** — a path to the project directory (e.g. `~/Projects/my-assistant`). Confirm you
     can list it.
   - **GitHub repo** — in a remote/web session you can only read repos **added to the session's scope**.
     Once scoped, read files with the GitHub MCP tools (`get_file_contents`, `search_code`). If the repo
     is not in scope, **say so plainly and stop** — do not guess at its contents. Tell the user exactly
     what to do: add the repo to this session's scope, or re-run locally where the folder exists.

If the target cannot be reached, report: "The target project isn't reachable from this session. Add the
repo to scope (cloud) or run this task locally where the project folder exists, then re-run." — and stop.

### Step 1 — Detect project type and inventory

Scan the target for the canonical files that make up a surface-appropriate project (see
`analyze-project-reference.md § Project-type detection`):

`AGENTS.md` · `CLAUDE.md` · project instructions/source revisions · `.agents/skills/` · `.codex/config.toml` · `.claude/` · `skills/` · `tasks/` (or scheduled-task definitions) · `.auto-memory/` ·
`settings.json` · `.gitignore` / `.claudeignore` · MCP config · `README`.

From what's present, classify the project: **Claude Code**, **Cowork**, **ChatGPT sources**, **Codex local**, or a named combination — and note any
narrower shape (helper-app, knowledge-base/wiki). Report a **factual inventory only** — what exists and
where. Do not judge yet.

```
Target: [path or owner/repo]   |   Type: [named surfaces + separate purpose]
Inventory:
  CLAUDE.md           [present (N lines) | missing]
  Skills              [N found: names | none]
  Tasks / scheduled   [N found: names | none]
  Memory (.auto-memory) [present | missing]
  MCP config          [present | missing]
  settings.json       [present | missing]
  Ignore hygiene      [.gitignore: y/n · .claudeignore: y/n]
  README / purpose    [one line from README or CLAUDE.md]
```

### Step 2 — Clarify intent

Use an available question tool or concise chat to resolve only the ambiguities that change which dimensions **apply** or what to
recommend. Don't ask what the inventory already answered. Cover, as needed:

- **Purpose** — code project / personal assistant / knowledge base / small helper tool?
- **Surface** — Claude Code, Cowork, ChatGPT sources, Codex local, or which combination?
- **Automation** — does it run (or should it run) scheduled/automated tasks?
- **Sensitive data** — does it handle credentials, personal, or confidential data?

The answers gate dimension applicability in Step 3 (e.g. no automation → scheduled-task efficiency,
self-improvement, cost, and orchestration are **N/A**, not gaps).

### Step 3 — Analyze against the dimensions (read-only)

Walk the dimension table in `analyze-project-reference.md § Dimension criteria`. For each **applicable**
dimension, apply its checks against the target and the relevant guide. For each, record:

- **Status** — ✓ Healthy / ⚠ Partial / ✗ Missing / — N/A
- **Findings** — concrete, with `file:line` evidence from the target
- **Priority** — HIGH / MEDIUM / LOW by impact (mirrors `audit-task-efficiency.md`)
- **Confidence** — high / medium / low, on any finding that is a judgement rather than a file being present
  or absent
- **Would drop it if** — the evidence that would make you withdraw the finding. No answer means it is an
  opinion, and it does not go in the plan
- **Fix** — the exact `setup-*` / `audit-*` task or skill that implements it

Do **not** write anything to the target in this step. Never copy secret or credential **values** into
your notes or the plan — reference their location only.

### Step 4 — Commit the draft, then present it

Write the full draft to a file **before** you say anything about what you found — in your own working
area, not into the target, which still receives exactly one file in Step 6. Then present it in chat.
Writing first is the point: a verdict given in conversation is cheap to soften once the user reacts, and
the softening leaves no trace (`27_INDEPENDENT_JUDGMENT.md`). Do not ask the user what they think is
wrong with the project before that file exists.

Use the structure in `analyze-project-reference.md § Improvement-plan template`: summary, scorecard,
prioritised findings, open questions, recommended implementation order, and the "How to implement"
handoff.

### Step 5 — Review loop

Fold in the user's answers and edits: drop dimensions they mark N/A, re-prioritise, refine wording, and
resolve the open questions you can.

Two rules keep this a reconciliation rather than a negotiation. A finding the user disputes is removed
only when they supply evidence that meets its would-drop-it-if line; otherwise it stays, with their
objection recorded beside it. And every finding that was dropped or changed priority after the draft
gets a line in *Revised in review*, so the written plan still shows what the draft said. Iterate until
the open questions are resolved, not until the draft stops attracting objections.

### Step 6 — Write the final plan and stop

Write the agreed plan to **`CLUIDE_IMPROVEMENT_PLAN.md` at the target project's root**.

- If that file already exists, ask (using the available question tool or chat): overwrite, or write a date-suffixed copy
  (`CLUIDE_IMPROVEMENT_PLAN_YYYY-MM-DD.md`)?
- For a GitHub target, create the file via the GitHub MCP write path on the user's working branch — only
  after they confirm. For a local target, write it directly.

Confirm what was written:
```
Improvement plan written: [target]/CLUIDE_IMPROVEMENT_PLAN.md
  Dimensions analysed: N applicable (M N/A)   |   Findings: H high · M medium · L low
  Top recommendation: [task/skill]
```

**Stop here.** Do not implement any changes. The plan's "How to implement" section names the tasks and
skills the user runs next — point them to it (e.g. "When you're ready, start with
`tasks/onboard-project.md` or the specific tasks listed in the plan").

---

## Hard rules

- **Read-only on the target**, except writing the single `CLUIDE_IMPROVEMENT_PLAN.md` file.
- **Plan-only.** Never edit the target's `CLAUDE.md`, skills, tasks, settings, or config.
- **No secrets in the plan.** Reference the location of a credential/secret; never copy its value.
- **Don't guess at unreachable targets.** If the repo isn't in scope or the folder can't be listed, stop
  with the message in Step 0.
- **Applicability over completeness.** A dimension that doesn't fit the project is **N/A**, not a gap —
  don't pad the plan with recommendations the project doesn't need.
