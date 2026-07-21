# Tasks

Runnable procedures Claude executes on request against a Claude project. A task is the "how": a repeatable, ordered set of steps. It is distinct from a **guide** (the "why" and "what", the knowledge a task draws on) and from a **template** (a copy-paste folder scaffold). A task usually implements one guide.

Run one with, for example: `Claude, run tasks/audit-skill.md`.

## Categories

- **`setup-*`**: interactive. Interview the user, then create or configure something (a CLAUDE.md, skill, memory, MCP server, scheduled task, or data layer).
- **`audit-*`**: inspect one component read-only against its guide, report findings, then optionally apply approved fixes.
- **`analyze-project`**: sweep a whole project against the full guide set and write an improvement plan (criteria in `analyze-project-reference.md`).
- **`onboard-project`**: classify and inventory an existing project.
- **Framework maintenance** (`harvest-from-projects`, `review-tasks`): keep Cluide itself consistent. These operate on the framework, not on a user project.

## Standard format

Every task file follows the same shape so they stay predictable:

```
# Task: <Name>

> One-line description of what running this does.
> Source guide: <the guide(s) this implements>.

## Purpose
What it accomplishes, and when to use it (one short paragraph).

## Instructions
### Step 0 — <precondition / locate target>
### Step 1 — <first action>
### Step N — <...>

## Output        (what the run produces)
## Constraints   (limits, safety rules, what not to touch)
```

`Output` and `Constraints` are required for any task that writes or changes files; a purely interactive setup task may fold them into the steps. Setup tasks interview before creating; audit tasks run a checklist read-only before proposing fixes.

## Conventions

- **Read-only before mutating.** Inspect and report first; make changes only in a later, clearly marked step.
- **Approve before writing.** A task that changes a user's project presents its plan and waits for explicit approval. It does not act on assumption.
- **Restore point before bulk or irreversible changes.** Before a task moves, renames, or deletes many files, take a way back first: a git commit or tag when the project is under version control, otherwise a dated zip of just the affected folders stored outside the working tree. Confirm it exists before the first change, and retire it once the result is verified.
- **Cite the guide.** Name the guide the task implements, so criteria live in one place and the task does not restate them.
- **Ordered, self-contained steps.** Each step is a discrete action; a reader can follow the task without external context.
- **Name `verb-noun.md`.** For example `setup-skill.md`, `audit-memory.md`, `reorganize-project.md`.
- **One task, one job.** If a task grows two purposes, split it.
