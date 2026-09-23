# Task: Review Platform Changes Against the Guides

> **Cluide maintenance task** — run this after every model launch, or monthly, whichever comes first.
> `Assistant, run tasks/review-platform-changes.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Purpose
Detect what Anthropic and OpenAI have shipped since Cluide's last sweep — in Claude Code, Cowork, claude.ai, the
Claude API, ChatGPT projects/apps/tasks, Codex, the OpenAI API and the MCP specification — and turn it into findings against the guides, tasks, skills and
templates. Every "as of <month>" in this repo was placed by hand and has no owner; a price, a default
mode or a "not supported" statement goes stale silently, and nothing internal to Cluide can catch it.

This is the outward-facing leg of a three-way maintenance loop:

| Task | Direction |
|------|-----------|
| `review-tasks.md` | A Cluide **guide** changed → flag the tasks, skill bundles and templates that drifted |
| `harvest-from-projects.md` | A live **project** evolved → flag the patterns Cluide does not yet capture |
| `review-platform-changes.md` (this task) | The **platform** moved → flag the claims Cluide makes that are no longer true, and the features it does not yet cover |

## Hard rules

- **Read-only until Step 6.** Steps 1–5 change nothing; the findings report is the deliverable.
- **Primary sources only** for anything that lands in a guide. A blog summary can point you at a change;
  the sentence you write cites the relevant vendor’s official page that states it.
- **A claim you cannot re-verify is a C finding, not an edit.** Write "re-verify" with the date, never a
  plausible replacement value.
- **Consumed surface stays append-only** (see `CLAUDE.md`). A platform rename never renumbers a guide,
  a dimension or a task file.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Fix the boundary

The sweep covers everything shipped since the last one. Take the later of:

```bash
git log -1 --format='%ad %s' --date=short "$(git describe --tags --abbrev=0)"   # last release
git log -1 --format='%ad %s' --date=short --grep='Platform sweep'                 # last sweep commit
```

Fix the boundary **per platform**, not once. A sweep commit may cover only one vendor (every sweep before 2026-09-21 covered only Anthropic), so read the versions a "Platform sweep" subject names and treat any platform it does not name as unswept since its last dated check (for OpenAI, the "checked" date in Guide 35 §9). Record the boundary date and the versions separately for each platform at the boundary (product/app versions and available models) from the previous sweep's report if one exists under `development/reviews/`.

### Step 2 — Read the sources, boundary forward

Fixed list. Read each page from the boundary date to today; do not sample.

| Source | What it settles |
|--------|-----------------|
| https://code.claude.com/docs/en/whats-new (weekly digest) and https://code.claude.com/docs/en/changelog | Claude Code CLI, Desktop, web, Agent SDK: commands, flags, settings, hooks, subagents, skills, memory, permission modes |
| https://claude.com/docs/cowork/changelog and the pages under https://claude.com/docs/cowork/ | Cowork: projects, scheduled tasks, Dispatch, plugins, folder access, permission prompts |
| https://support.claude.com/en/articles/12138966-release-notes | claude.ai and the apps: memory, artifacts, connectors, Claude in Chrome, plan changes |
| https://platform.claude.com/docs/en/release-notes/overview and https://platform.claude.com/docs/en/about-claude/pricing | Model launches, retirements, prices, context windows, effort levels, API features |
| https://learn.chatgpt.com/docs/changelog (ChatGPT and Codex changelog), https://learn.chatgpt.com/docs/whats-new and https://help.openai.com/en/articles/6825453-chatgpt-release-notes | OpenAI product documentation and ChatGPT releases; follow current links to Codex and project-source behavior |
| https://learn.chatgpt.com/docs/agent-configuration/agents-md and https://learn.chatgpt.com/docs/build-skills | Codex instructions, nested discovery, limits and native skill metadata |
| https://learn.chatgpt.com/codex/extend/mcp, https://learn.chatgpt.com/codex/permission-modes and https://learn.chatgpt.com/docs/agent-approvals-security | Codex MCP configuration, effective sandbox and approval controls |
| https://learn.chatgpt.com/codex/automations and https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt | ChatGPT scheduled tasks and Codex automations; verify each surface separately |
| https://learn.chatgpt.com/codex/projects (local projects) and https://help.openai.com/en/articles/10169521-projects-in-chatgpt (cloud projects) | Local-project folders and primary-folder discovery; cloud project instructions, sources, memory and refresh behavior |
| https://learn.chatgpt.com/codex/customization/memories | ChatGPT memory versus local Codex memory |
| https://agentskills.io/specification | Skill frontmatter limits every host inherits (`name`, `description` length) |
| https://developers.openai.com/api/docs/changelog and https://developers.openai.com/api/docs/pricing | OpenAI API changes, current model identifiers, deprecations and API pricing; not subscription allowance |
| https://modelcontextprotocol.io/specification (latest changelog) | MCP transports, deprecations, auth |
| https://code.claude.com/docs/llms.txt | Index of Claude Code pages, including each weekly `whats-new` digest; use it to find pages the table does not name |

The desktop changelog groups entries under General, Code, Cowork and 3P. **3P entries describe
organisation-managed third-party-platform deployments**, not consumer accounts; say so when citing one.

Write a dated change list to `development/reviews/YYYY-MM-DD-platform-changes.md`: date, product, change,
one-sentence meaning, source URL, checked date, affected surfaces and verification result. This is bulk reading — dispatch it per source to the cheap tier (see
Dispatch below) and keep the judgement for later steps.

### Step 3 — Build the claim register

The guides mark their own version-sensitive statements. Grep them:

```bash
grep -rniE "as of (january|february|march|april|may|june|july|august|september|october|november|december) 20[0-9]{2}|verified (in )?[a-z]* ?20[0-9]{2}|currently|not (yet )?(supported|possible|available|documented)|research preview|rolling out|\\\$[0-9]+ ?/|per (1M|MTok)" \
  *.md tasks/*.md skills/*/SKILL.md templates/**/*.md 2>/dev/null | grep -v "^development/"
```

Add every statement of limitation ("cannot", "no way to", "only in Claude Code", "manual-only"): these
are the claims most often superseded. Each hit is one row: file, line, claim, product/surface, source URL, source date, checked date, verification result, category (model/pricing,
CLI, settings, hooks, permissions, memory, skills, agents, Cowork, MCP, API).

### Step 4 — Extract the reference facts

From the current reference pages, pull the authoritative lists into a scratch fact sheet and diff each
against the guide that carries it:

| Reference page | Guide(s) that must agree |
|----------------|--------------------------|
| Pricing table, model lineup, default model per plan | `10`, `16`, `17`, `tasks/audit-cost.md`, `CHEATSHEET.md` |
| Permission modes, settings keys and permission-rule syntax (including `Tool(param:value)` rules) | `09`, `12`, `20`, `tasks/setup-security.md`, `skills/security-review/`, `skills/dispatch/` |
| Hook events | `06`, `11`, `12`, `31` |
| SKILL.md frontmatter fields | `03`, `tasks/audit-skill.md`, `tasks/setup-skill.md` |
| Subagent frontmatter fields, model resolution order, fork mode, concurrency | `09`, `26`, `27`, `skills/dispatch/`, `templates/AGENT_STARTER_PACK/` |
| Memory (auto memory, account memory, project memory, the `import-memory` skill) | `04`, `14`, `17`, `33`, `34`, `35`, `tasks/audit-memory.md`, `tasks/setup-memory.md`, `tasks/retire-project.md` |
| `claude mcp` subcommands, result limits, MCP spec status | `05`, `15`, `tasks/setup-mcp.md` |
| Cowork project fields, scheduled tasks, folder access | `25`, `06`, `tasks/tune-instruction-layers.md`, `tasks/relocate-project.md` |
| Artifacts, Claude in Chrome | `19`, `05`, `12`, `22` |
| Print mode flags (`claude -p`), `claude plugin eval` availability and case format, `/skill-doctor` | `31`, `tasks/setup-behaviour-tests.md` |
| `CLAUDE.md` locations, imports and the loaded-files view | `01`, `25`, `35`, `tasks/setup-dual-platform.md` |

Re-check **every** Guide 35 §9 row for both platforms using its current official source. Follow official redirects; an inaccessible page or absent product detail is a C finding, never a silent pass. Search all root guides, tasks, skill entry points and nested templates for dependent claims, not just Guide 35. Distinguish API billing, subscription allowances and measured runtime usage.

### Step 5 — Findings report

Write `development/reviews/YYYY-MM-DD-platform-currency.md` with four sections, each item carrying the
guide, line, the claim as written, what the source says, and the URL:

- **A. Wrong now** — a reader following the guide gets the current platform wrong.
- **B. Stale or incomplete** — still usable, but missing what a reader now needs.
- **C. Could not verify** — no primary source either way; name the test or re-check that would settle it.
- **D. Process** — new sources to add to the table above, name collisions, repository state.

Close with a change plan grouped into PR-sized units (one branch per unit; the merge gate in `CLAUDE.md`
requires each to be a whole change) and the registration touchpoints each unit needs. A unit that adds a
`tasks/` file grows the consumed surface: say so, because the next tag is then minor, not patch.

Present the report and **stop**. Ask which units to apply.

### Step 6 — Apply with approval

For each approved unit: branch from `main`, apply the edits, mirror every changed guide byte-identically
into every `skills/*/references/` copy that carries it (the bundled `00_INDEX.md` takes the same patch
with links stripped per `review-tasks.md` step 4a), run `review-tasks.md` steps 4a and 4c, and re-stamp every touched
"as of" marker with the sweep month. Put the boundary for the next run into the commit subject:

```
Platform sweep 2026-09b: <what changed> (Claude Code v2.1.278, desktop v2.2553.1, Codex CLI 0.155.1)
```

### Step 7 — Confirm

Tell the user which sources were read and to what date, how many claims were checked, the A/B/C/D counts,
what was applied, and what stays open in C with its test. Remind them the account-installed copies of any
edited skill (`dispatch`, `security-review`, `git-guru`) must be reinstalled from the repo to take effect. Claude Code v2.1.275 and later syncs skills enabled on the claude.ai account into terminal sessions, so one account reinstall also reaches those sessions; a Codex or ChatGPT copy is a separate install.

---

## Dispatch

Use the current runtime's supported delegation policy. On Claude, apply the repository's Claude dispatch rules; on OpenAI, retain the configured model unless the user requested a supported alternative. Source extraction may be delegated only when the host permits it; every shipped claim is checked against its cited primary source by the reviewer. Record routing under `development/` without inventing cross-vendor model equivalents.

## Scheduled-task variant

Run read-only through Step 5 under one named scheduler owner (Cowork or Codex app when available), with explicit folder/source and web access, timezone, stable job ID and run deduplication. Record findings and notify only on a meaningful change or required action. Do not edit published content unattended. Inventory both platforms before registration; use `setup-scheduled-task.md` for registration and handoff. Model launches trigger an extra review; cadence alone does not justify a release.
