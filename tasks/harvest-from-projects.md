# Task: Harvest Patterns From Live Projects

> **Cluide maintenance task** — run this when your real assistant projects have evolved and you want
> their proven patterns folded back into Cluide.
> `Claude, run tasks/harvest-from-projects.md`

## Purpose
Scan one or more **live** Claude projects (e.g. a running personal assistant, a PMO workspace) and
surface the patterns they use in production that Cluide's guides, tasks, templates, or skills do **not
yet teach** — then propose folding the *generalized* version of each back into Cluide.

This is the inverse of `tasks/review-tasks.md`. Together they form a two-way maintenance loop:

| Task | Direction |
|------|-----------|
| `review-tasks.md` | A Cluide **guide** changed → flag the tasks/skills/templates that drifted out of sync |
| `harvest-from-projects.md` (this task) | A live **project** evolved → flag the patterns Cluide doesn't yet capture |

**Hard rule:** Cluide is a public, content-free framework. Never import project-specific content
verbatim. Only the *shape* of a pattern crosses over — every candidate passes the redaction gate in
Step 3 before it can be proposed.

---

## Harvest dimensions → Cluide destinations

Each thing worth harvesting maps to where it belongs in Cluide. Use this table in Step 2 and Step 4.

| Dimension | What to look for in the project | Lands in Cluide |
|-----------|--------------------------------|-----------------|
| CLAUDE.md patterns | Standing rules / file-map structures that work in production but Cluide doesn't teach | `01_CLAUDE_MD.md`, `16_BEST_PRACTICES.md`, templates |
| Skills | Skills the project relies on that Cluide doesn't ship or teach | `03_SKILLS.md`, `skills/` |
| Scheduled-task structure | Efficiency tricks, self-improvement loops, run-log conventions proven across real runs | `06`, `07`, `08`, `templates/TASK_TEMPLATE/` |
| Memory / profile schema | Profile and knowledge file shapes that earned their keep | `04_MEMORY_AND_PROFILE.md`, `14_PERSONAL_DATA_LAYER.md`, templates |
| MCP / hooks / security | Connector setups, guard hooks, permission patterns, credential handling | `05_MCP_SERVERS.md`, `12_SECURITY.md`, `setup-*` tasks |
| Output formatting | HTML / Markdown report generators worth generalizing | `19_OUTPUT_FORMATTING.md`, `html-report` skill |
| Troubleshooting / quirks | Logged connector bugs and their fixes (often dated notes in a reference file) | `17_TROUBLESHOOTING.md` |
| Orchestration / data layer | Multi-task coordination, shared state, Python feeders, JSON "databases", browser extraction | `09`, `14`, `setup-orchestration.md`, `setup-data-layer.md` |

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons
> instead of plain text.

### Step 0 — Confirm Cluide is the working repo

This task **reads** other projects but **writes only to Cluide**. Confirm the current working directory
is the Cluide repo (it contains `00_INDEX.md` and a `tasks/` folder). If not, stop and ask the user to
run it from Cluide.

### Step 1 — Locate the projects

Where the projects live depends on how this session was started. Ask the user, then handle the mode:

- **Local machine** — a parent folder containing the project directories
  (e.g. `~/Documents/Claude/Projects`). Confirm you can list it.
- **Cloud / web session** — a fresh remote session sees **only the repo it cloned**. The other repos
  must be added to the session's scope first (via the host's repo-add mechanism, or by starting a web
  session that includes them). If they aren't reachable, say so plainly and stop — do **not** guess at
  their contents. Tell the user exactly what to do: add the target repos to this session, or re-run
  locally.

Then list candidate projects and confirm with `AskUserQuestion` which to harvest from:

```
Projects available to harvest:
  [project] — [one-line description from its README / CLAUDE.md]
  ...

Which should I harvest from? (multi-select)
```

If nothing is reachable, report: "No live projects are reachable from this session. Add the target
repos to scope (cloud) or run this task locally where the project folders exist, then re-run."

### Step 2 — Inventory each project against the harvest dimensions

For each selected project, walk the dimension table above. For each dimension, note concrete artifacts:
file paths, skill names, task structures, hook configs, schemas. Keep it factual — you are taking
inventory, not yet judging.

Report per project:
```
[project name]
  CLAUDE.md patterns:      [what's notable, with file:line]
  Skills:                  [skill names + one-line purpose]
  Scheduled-task structure:[patterns observed]
  Memory / profile schema: [files and shapes]
  MCP / hooks / security:  [setups observed]
  Output formatting:       [generators / report styles]
  Troubleshooting / quirks:[logged fixes worth generalizing]
  Orchestration / data:    [coordination / data patterns]
```

### Step 3 — Generalize + redact (mandatory gate)

Before *any* candidate can be proposed for Cluide, strip everything personal or business-specific, per
`14_PERSONAL_DATA_LAYER.md` and this repo's File-Hygiene rule in `CLAUDE.md`. Remove or placeholder:

- Names, email addresses, phone numbers, usernames
- Company / client / account names, internal project names, deal data
- Absolute home paths (`/Users/<name>/…`, `/home/<name>/…`) → `[PROJECT_ROOT]` or `~`
- Tenant domains, API endpoints, credentials, tokens, IDs
- Any real content (message text, document bodies, financial figures)

Only the **shape** survives: the structure, the rule, the schema, the workflow. If a pattern cannot be
cleanly separated from its content, **drop it** and note why. State this explicitly in the report so the
user can see the gate ran.

### Step 4 — Diff each candidate against existing Cluide

For every generalized candidate, read the mapped Cluide destination(s) from the dimension table and
classify:

- **Already covered** — Cluide already teaches this. Skip (note it, so the user knows you checked).
- **Partially covered** — Cluide touches it but the project's version is better / more complete. Propose
  an **enhancement** to the existing guide/task/template/skill.
- **Net-new** — Cluide doesn't cover it at all. Propose an **addition**, and name the exact destination.

Do not propose anything a guide, task, template, or skill already does. When unsure, search Cluide:
```bash
grep -rin "[keyword for the pattern]" --include="*.md" . | grep -v "/skills/.*/references/"
```

### Step 5 — Present the harvest report

Group by Cluide destination, sort by impact. One block per proposal:

```
Harvest Report
──────────────
Projects harvested: [list]   |   Candidates found: N   |   After redaction gate: M   |   Proposals: K

PROPOSAL 1 — [Add | Enhance]: [destination, e.g. "17_TROUBLESHOOTING.md → new entry"]
  Source (generalized): [project, what was observed — already redacted]
  Pattern:              [the reusable shape]
  Why Cluide needs it:  [gap it fills]
  Cluide status:        [net-new | partially covered by <X>]
  Draft:                [the actual snippet/section to insert, content-free]

PROPOSAL 2 — ...

Checked but skipped (already covered):
  [pattern] — already taught in [guide/task/template/skill]

Dropped at redaction gate:
  [pattern] — couldn't be generalized without leaking [what]
```

### Step 6 — Apply with approval

Ask:
> "Would you like me to apply any of these? I'll show each change (old → new) before writing, and only
> touch the files you approve."

For each approved proposal, show the specific edit, then write it. After applying, stamp the changed
Cluide file with an invisible marker so the next harvest/review can see provenance:
```markdown
<!-- harvested: YYYY-MM-DD from <generalized project descriptor> -->
```

If a proposal adds a new task or skill, also add it to the discoverability surfaces: `README.md`,
`00_INDEX.md`, and — for tasks tied to a guide — the mapping table in `tasks/review-tasks.md`.

### Step 7 — Confirm

Tell the user:
- Which projects were harvested and how many candidates survived the redaction gate
- What was added, what was enhanced, and what was skipped as already-covered
- A reminder: "Re-run after major project changes, or quarterly alongside `tasks/review-tasks.md` —
  one pulls project learnings in, the other keeps the tasks in sync with the guides."
