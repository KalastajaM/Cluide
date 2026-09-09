# Task: Review Platform Changes Against the Guides

> **Cluide maintenance task** — run this after every model launch, or monthly, whichever comes first.
> `Claude, run tasks/review-platform-changes.md`

## Purpose
Detect what Anthropic has shipped since Cluide's last sweep — in Claude Code, Cowork, claude.ai, the
Claude API and the MCP specification — and turn it into findings against the guides, tasks, skills and
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
  the sentence you write cites the Anthropic page that states it.
- **A claim you cannot re-verify is a C finding, not an edit.** Write "re-verify" with the date, never a
  plausible replacement value.
- **Consumed surface stays append-only** (see `CLAUDE.md`). A platform rename never renumbers a guide,
  a dimension or a task file.

---

## Instructions

> **Clarifying questions:** for any step with a fixed set of options, use `AskUserQuestion` with buttons
> rather than plain text.

### Step 1 — Fix the boundary

The sweep covers everything shipped since the last one. Take the later of:

```bash
git log -1 --format='%ad %s' --date=short "$(git describe --tags --abbrev=0)"   # last release
git log -1 --format='%ad %s' --date=short --grep='Platform sweep'                 # last sweep commit
```

Record the boundary date and the platform versions at the boundary (Claude Code version, desktop app
version, model lineup) from the previous sweep's report if one exists under `development/reviews/`.

### Step 2 — Read the sources, boundary forward

Fixed list. Read each page from the boundary date to today; do not sample.

| Source | What it settles |
|--------|-----------------|
| https://code.claude.com/docs/en/whats-new (weekly digest) and https://code.claude.com/docs/en/changelog | Claude Code CLI, Desktop, web, Agent SDK: commands, flags, settings, hooks, subagents, skills, memory, permission modes |
| https://claude.com/docs/cowork/changelog and the pages under https://claude.com/docs/cowork/ | Cowork: projects, scheduled tasks, Dispatch, plugins, folder access, permission prompts |
| https://support.claude.com/en/articles/12138966-release-notes | claude.ai and the apps: memory, artifacts, connectors, Claude in Chrome, plan changes |
| https://platform.claude.com/docs/en/release-notes/overview and https://platform.claude.com/docs/en/about-claude/pricing | Model launches, retirements, prices, context windows, effort levels, API features |
| https://modelcontextprotocol.io/specification (latest changelog) | MCP transports, deprecations, auth |

The desktop changelog groups entries under General, Code, Cowork and 3P. **3P entries describe
organisation-managed third-party-platform deployments**, not consumer accounts; say so when citing one.

Write a dated change list to `development/reviews/YYYY-MM-DD-platform-changes.md`: date, product, change,
one-sentence meaning, source URL. This is bulk reading — dispatch it per source to the cheap tier (see
Dispatch below) and keep the judgement for later steps.

### Step 3 — Build the claim register

The guides mark their own version-sensitive statements. Grep them:

```bash
grep -rniE "as of (january|february|march|april|may|june|july|august|september|october|november|december) 20[0-9]{2}|verified (in )?[a-z]* ?20[0-9]{2}|currently|not (yet )?(supported|possible|available|documented)|research preview|rolling out|\\\$[0-9]+ ?/|per (1M|MTok)" \
  *.md tasks/*.md skills/*/SKILL.md templates/**/*.md 2>/dev/null | grep -v "^development/"
```

Add every statement of limitation ("cannot", "no way to", "only in Claude Code", "manual-only"): these
are the claims most often superseded. Each hit is one row: file, line, claim, category (model/pricing,
CLI, settings, hooks, permissions, memory, skills, agents, Cowork, MCP, API).

### Step 4 — Extract the reference facts

From the current reference pages, pull the authoritative lists into a scratch fact sheet and diff each
against the guide that carries it:

| Reference page | Guide(s) that must agree |
|----------------|--------------------------|
| Pricing table, model lineup, default model per plan | `10`, `16`, `17`, `tasks/audit-cost.md`, `CHEATSHEET.md` |
| Permission modes and settings keys | `12`, `20`, `tasks/setup-security.md`, `skills/security-review/` |
| Hook events | `06`, `11`, `12`, `31` |
| SKILL.md frontmatter fields | `03`, `tasks/audit-skill.md`, `tasks/setup-skill.md` |
| Subagent frontmatter fields, fork mode, concurrency | `09`, `26`, `27`, `skills/dispatch/`, `templates/AGENT_STARTER_PACK/` |
| Memory (auto memory, account memory, project memory) | `04`, `14`, `17`, `33`, `tasks/audit-memory.md`, `tasks/setup-memory.md`, `tasks/retire-project.md` |
| `claude mcp` subcommands, result limits, MCP spec status | `05`, `15`, `tasks/setup-mcp.md` |
| Cowork project fields, scheduled tasks, folder access | `25`, `06`, `tasks/tune-instruction-layers.md`, `tasks/relocate-project.md` |
| Artifacts, Claude in Chrome | `19`, `05`, `12`, `22` |
| Print mode flags (`claude -p`), `claude plugin eval` availability and case format, `/skill-doctor` | `31`, `tasks/setup-behaviour-tests.md` |

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
Platform sweep 2026-09: <what changed> (Claude Code v2.1.263, desktop v1.46388.4)
```

### Step 7 — Confirm

Tell the user which sources were read and to what date, how many claims were checked, the A/B/C/D counts,
what was applied, and what stays open in C with its test. Remind them the account-installed copies of any
edited skill (`dispatch`, `security-review`, `git-guru`) must be reinstalled from the repo to take effect.

---

## Dispatch

Load the `dispatch` skill. Step 2 (reading sources) and Step 3 (grepping and tabulating claims) are
bulk extraction: sonnet at low or medium effort, one worker per source or per ten guides, returning file
paths and counts rather than content. Step 4's diff and Step 5's findings are judgement and stay with the
session. Step 6 writes prose that ships, so Cluide's Dispatch Overrides apply: opus or above, and every
edit is re-read by the session against the cited page before commit. Log the routing to
`development/ROUTING_LOG.md`.

## Scheduled-task variant

The same task runs unattended as a Cowork scheduled task that stops at Step 5: read the sources, build
the register, write the report, and post its A/B/C/D counts. Requirements: the Cluide folder connected,
web fetch enabled, model sonnet for Steps 2–3 with the report paragraphs on opus. Monthly is the right
cadence; a model launch is the right trigger to run it by hand in between.
