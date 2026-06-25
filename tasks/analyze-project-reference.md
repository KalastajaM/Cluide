# Reference: Analyze Project

> Companion to `tasks/analyze-project.md` — read on demand. Holds the per-dimension criteria, the
> project-type detection signals, the input-handling detail, and the `CLUIDE_IMPROVEMENT_PLAN.md`
> output template. Keeping this out of the procedure file keeps the always-loaded task lean
> (Guide 06, the `TASK.md` / `TASK_REFERENCE.md` split).

---

## § Project-type detection

Classify the target from what's present. The shape decides which dimensions apply.

| Signal | Points to |
|--------|-----------|
| `.claude/` folder, `.claude/settings.json`, `.claude/skills/`, PreToolUse/SessionStart hooks | **Claude Code** |
| Cowork scheduled-tasks (task folders with `TASK.md` + `IMPROVEMENTS.md` / `RUN_LOG.md`), no `.claude/settings.json` | **Cowork** |
| Both of the above | **Hybrid** (built in Claude Code, run in Cowork — the Guide 13 split) |
| A single small app + `CLAUDE.md` with a helper index / domain invariant, tight permission allowlist | **Helper-app** (Guide 22) |
| `Knowledge/` or a wiki structure with an `INDEX.md` + sources + schema | **Knowledge-base / wiki** (Guide 15) |

A project can be more than one shape. Record the primary shape plus any secondary one — both affect
applicability (e.g. a hybrid that's also a knowledge base gets the wiki dimension too).

---

## § Dimension criteria

For each dimension: what **healthy** looks like, the **checks** to run against the target, the **guide**
it's judged against, and the **fix** task/skill the plan recommends. Apply read-only. Criteria are
summarised from the existing `audit-*` tasks and the guides — when you need depth, open the cited guide
or audit task rather than re-deriving it here.

### 1. Project type & structure — guides 13, 18 → `onboard-project`
- **Healthy:** definition files and state files live together and both tools can read them; the layout matches the Guide 18 "full picture" for the project's type.
- **Checks:** is there a coherent `.claude/` (or Cowork task) layout? Are state files (`RUN_LOG.md`, `IMPROVEMENTS.md`) co-located with definitions? Any orphaned or duplicated config?

### 2. CLAUDE.md quality — guides 01, 16, 02 → `setup-claude-md` / `audit-claude-md`
- **Healthy:** present, lean (~30 lines of real content), has Identity / Communication / Critical Rules, no dead or contradictory rules, current.
- **Checks:** exists? Over-length or bloated? Missing core sections? Stale or contradicted-by-behaviour rules? Vague instructions that should be examples (Guide 02)?

### 3. Skills — guides 03, 02 → `setup-skill` / `audit-skill`
- **Healthy:** each skill has a trigger-quality `description` (concrete phrases), a complete workflow, a specified output format, named tools, and edge-case handling.
- **Checks:** weak/generic descriptions that won't trigger; missing output format; unnamed tools; no edge cases; skill that should be a task (or vice-versa, per Guide 03).

### 4. Memory & profile — guides 04, 14 → `setup-memory` / `audit-memory`
- **Healthy:** `.auto-memory/` (or profile files) exist where cross-session persistence is needed; compact summaries (`KNOWLEDGE_SUMMARY.md` ≤ 40 lines); no stale/duplicate/misplaced facts.
- **Checks:** persistence expected but absent? Bloated always-loaded memory? Stale or duplicated entries? Facts that belong in a profile vs memory?

### 5. Scheduled-task efficiency — guide 06 → `setup-scheduled-task` / `audit-task-efficiency`
- **Healthy:** `TASK.md` ≤ 250 lines, heavy detail split to `TASK_REFERENCE.md`, fixed-format output scripted, partial reads, two-pass triage, hard size limits, run dedup.
- **Checks:** run `audit-task-efficiency.md`'s six checks read-only against each task file. Flag oversized always-loaded files, un-scripted fixed-format generation, full-file reads, unbounded logs.

### 6. Task self-improvement — guides 07, 08 → `setup-self-improving-task`
- **Healthy:** recurring tasks carry `IMPROVEMENTS.md` with counters, apply-vs-propose discipline, refactor triggers, and a run log.
- **Checks:** scheduled task without a self-improvement loop? `IMPROVEMENTS.md` present but unbounded (> 150 lines, Applied Fixes never archived)? No refactor threshold?

### 7. Cost & performance — guide 10 → `audit-cost`
- **Healthy:** per-run metrics captured, model tier matches the work, file budgets respected, no cost spikes.
- **Checks:** any run metrics at all? Over-tier model for a simple task? Expensive steps with no triage?

### 8. Orchestration — guide 09 → `setup-orchestration`
- **Healthy:** multiple coordinated tasks use shared state with `updated_at`, clear ownership, freshness/skip handling.
- **Checks:** multiple tasks sharing data via implicit coupling? Missing freshness checks? One task editing another's section?

### 9. MCP servers — guide 05 → `setup-mcp`
- **Healthy:** servers configured at the right scope (global vs project), tool names referenced correctly in skills, credentials handled per Guide 12.
- **Checks:** skills referencing tools from unconfigured servers? Over-broad server scope? Credentials in the wrong place (see Security)?

### 10. Security — guide 12 → `setup-security` / `security-review` skill
- **Healthy:** no committed secrets, MCP servers trust-evaluated, PreToolUse guard hook where Claude runs bash, session-data hygiene, prompt-injection awareness in autonomous tasks.
- **Checks:** grep for credential patterns (report **location only**, never values); permission breadth; missing guard hook on a bash-running project; autonomous task handling untrusted input without guardrails. For a deeper pass, recommend the `security-review` skill.

### 11. Git & ignore hygiene — guide 11 → `setup-github` / `setup-ignore-hygiene`
- **Healthy:** `.gitignore` excludes run logs / outputs / personal data; `.claudeignore` excludes large generated context; tracked files that should be ignored are untracked.
- **Checks:** missing ignore files? Run logs / `LAST_RUN.md` / secrets tracked? Personal-data files committed?

### 12. Output formatting — guide 19 → `html-report` skill
- **Healthy:** user-facing output has a specified, consistent format; standalone reports use the self-contained HTML skeleton.
- **Checks:** tasks/skills producing wall-of-text output? A briefing/dashboard that would benefit from the `html-report` skill?

### 13. Interactive prompting — guide 20 → guidance only
- **Healthy:** tasks/skills use `AskUserQuestion` for fixed-option choices, `@` references, and plan-mode-style review where it helps.
- **Checks:** fixed-option decisions asked as free text? Note as LOW-priority guidance — no dedicated fix task.

### 14. Company policies — guide 21 → `setup-policies` / `policies-validator` skill
- **Healthy (only if the org has policies):** tiered enforcement (T1 block / T2 alert / T3 guidance) wired via the validator skill, policy content kept out of the repo.
- **Checks:** org policies that Claude should honour but doesn't? Policy text pasted into `CLAUDE.md` instead of referenced? **N/A** if no org policies apply.

### 15. Personal data layer — guide 14 → `setup-data-layer`
- **Healthy (only if the project reasons over personal data):** a deliberate pattern (Python feeder, JSON DB, browser extraction, vision) rather than ad-hoc pasting.
- **Checks:** large/no-API personal data handled by hand? **N/A** if the project has no personal-data inputs.

### 16. LLM wiki — guide 15 → `setup-wiki`
- **Healthy (knowledge-base projects only):** sources / wiki / schema layers, ingest-query-lint operations, index + log conventions.
- **Checks:** a knowledge project using flat notes instead of a compounding wiki? **N/A** otherwise.

### 17. Helper-app patterns — guide 22 → guidance only
- **Healthy (small local tools only):** domain invariant + helper index + verification gates in `CLAUDE.md`, tight permission allowlist.
- **Checks:** a vibe-coded helper drifting (duplicated helpers, stale CLAUDE.md, no verification gates)? Guidance only. **N/A** otherwise.

### 18. Cowork-specific efficiency — guides 06, 13 → `cowork-optimizer` skill
- **Healthy (Cowork projects):** tasks structured for fast, cheap Cowork runs (the `cowork-optimizer` 9-dimension view).
- **Checks:** a Cowork task that's slow/expensive or structurally heavy? Recommend running the `cowork-optimizer` skill for the deep optimisation pass. **N/A** for pure Claude Code projects.

---

## § Input handling

**Local folder.** Take a path; confirm you can list it (`ls [path]`). Read files directly. Write the
plan directly to `[path]/CLUIDE_IMPROVEMENT_PLAN.md`.

**GitHub repo.** In a remote/web session you can only read repos **added to the session's scope**.
- If scoped: read with the GitHub MCP tools — `get_file_contents` for known paths, `search_code` to
  discover structure (e.g. find `CLAUDE.md`, `SKILL.md`, `TASK.md`). List the tree to inventory.
- To check/extend scope, use the host's repo tools (`list_repos`, `add_repo`) where available.
- Write the plan via the GitHub MCP write path (`create_or_update_file`) on the user's working branch,
  **only after they confirm** — never push to an unexpected branch.
- If the repo is **not** in scope and can't be added: stop with —
  > "The target project isn't reachable from this session. Add the repo to scope (cloud) or run this
  > task locally where the project folder exists, then re-run."

Never guess at the contents of an unreachable target.

---

## § Improvement-plan template

The exact structure to write to `CLUIDE_IMPROVEMENT_PLAN.md`. Fill the placeholders; drop empty
priority sections; keep findings concrete and evidence-backed.

```markdown
# Cluide Improvement Plan — <project name>

> Generated <YYYY-MM-DD> · Project type: <Claude Code | Cowork | hybrid> · Analyzed against Cluide (full guide set)
> This is a proposal, not a change. Review it, then run the tasks named under "How to implement".

## Summary
<2–3 sentences: what the project is, overall health, and the headline gaps.>

## Scorecard
| Dimension | Status | Priority |
|-----------|--------|----------|
| CLAUDE.md | ⚠ Partial | HIGH |
| Skills | ✓ Healthy | — |
| Security | ✗ Missing | HIGH |
| … | … | … |
<One row per applicable dimension. Status: ✓ Healthy / ⚠ Partial / ✗ Missing / — N/A.>

## Findings (prioritised)

### HIGH
- **<dimension>: <short finding>**
  - Now: <evidence — file:line / what's missing>
  - Guide: <NN> · Fix: run `<task or skill>`

### MEDIUM
- **<dimension>: <short finding>** — Now: <evidence> · Guide <NN> · Fix: `<task/skill>`

### LOW / optional
- **<dimension>: <short finding>** — <evidence> · Fix: `<task/skill>` (or guidance only)

## Open questions
<Anything still ambiguous that should be answered before implementing. Omit the section if none.>

## Recommended implementation order
1. `<task/skill>` — <why first (usually security + CLAUDE.md before everything else)>
2. `<task/skill>` — <why next>
…

## How to implement
Each fix maps to a Cluide task or skill. When you're ready, run them in the order above — for example:
- `Claude, run tasks/onboard-project.md` — for end-to-end setup of missing pieces
- `Claude, run tasks/<specific-setup-or-audit>.md` — for a single dimension
- the `<skill>` skill — for <deep-dive, e.g. security-review / cowork-optimizer>

*The analysis stops at this plan. No changes have been made to the project.*
```
