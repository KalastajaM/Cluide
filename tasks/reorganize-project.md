# Task: Reorganize Project

> **Cluide task** — safely restructure one project's folder layout without breaking it.
> **Source guide:** 24 (Project Folder Structure) defines the target; this task moves an existing project toward it.

## Purpose

Bring a project whose folders have drifted (outputs piled at the root, duplicate and versioned files, junk-drawer folders, no clear home for things) back to a clean layout, moving files and rewiring every reference so nothing breaks. Read-only until a plan is approved; it never moves anything on assumption.

Use it when a project has grown messy and you want it tidy, or after an audit flags structure findings (Guide 24, or a maintenance structure audit).

## Instructions

> **Clarifying questions:** for any fixed-option choice, use `AskUserQuestion` rather than free text.

### Step 0 — Confirm the target and read local rules

Confirm the project folder is mounted and accessible; if not, stop and ask for it. Read the project's own `CLAUDE.md` and `README` first. Its local layout rules are authoritative: this task tidies toward the standard, it does not override a deliberate local structure. Flag any conflict for the user to decide.

### Step 1 — Inventory the current layout (read-only)

List the folder tree and classify what exists: instructions, source-of-truth files, generated outputs, scratch, archives, and anything uncategorised. Note the specific drift: files at the root that belong in a home, duplicate or versioned copies (`foo copy`, `foo (1)`, `final_v3`), oversized junk-drawer folders, outputs mixed with sources. Report facts only, no changes.

### Step 2 — Diagnose against the standard

Compare the inventory to Guide 24: which of the five homes (instructions, source of truth, outputs, scratch, archive) are missing or muddled? Which naming and archive conventions are violated? Produce a short findings list.

### Step 3 — Propose the target layout and get sign-off

Present an explicit **old path → new path** table for every file or folder that would move, rename, or be archived, plus any new folders to create. Group by kind. State what stays untouched. Note anything irreversible, and state the **restore point** you will take (see Step 4). Then **stop and wait for approval.** Do not proceed on assumed approval.

### Step 4 — Take a restore point

Before moving anything, create a restore point so a botched reorg can be undone, and confirm it exists first:

- **If the project is under git**, commit or tag the current state as a labelled snapshot. This is the cleanest option: precise, diffable, no clutter. Use it when the user manages the project's history that way; otherwise ask.
- **If it is not under git**, create a dated zip of the folders being changed and store it **outside the project working tree** (or in an ignored `_backups/` location), never loose in the project root where it becomes clutter or gets swept into the reorg.
- **Scope the backup to what changes.** Back up only the affected subtree unless the reorg is project-wide; do not zip a large project wholesale for a small move.

Retire the restore point once Step 6 confirms the result is good.

### Step 5 — Apply as move-and-rewire

For each approved move, in one unit of work:

1. Move (or rename) the file. Prefer a history-preserving move if the project is under git.
2. Rewire every reference to it: paths in `CLAUDE.md`, the README file map, skills, tasks, and cross-file links on both sides. A move without its rewires is a dead reference.
3. Prefer archiving over deleting: move superseded files into an `[ARCHIVE]`/`_archive/` folder rather than removing them.

Apply only the approved rows. If applying reveals something the plan missed, stop and present a revised plan rather than improvising.

### Step 6 — Verify

Confirm no dead references remain (grep the project for the old paths), the file map in `CLAUDE.md` matches the new tree, and any scheduled tasks or skills still resolve. If the project runs a workflow, do a dry read-through to confirm it still finds its inputs. Report what moved and confirm the tree is clean. Once verified, retire the restore point: a git snapshot stays in history, so just delete any zip you created.

## Output

A findings list (Step 2), an approved old→new move table (Step 3), and a short confirmation after Step 6 that references resolve and the layout matches Guide 24. This task writes only to the target project, and only the approved moves.

## Constraints

- Read-only until Step 3 is approved. Never move on assumption.
- Take the approved restore point and confirm it exists before the first move (Step 4). No bulk move without a way back.
- Respect the project's own `CLAUDE.md`; flag conflicts rather than overriding.
- Archive, do not delete, unless deletion is explicitly approved for a specific file.
- Never touch `.git/` internals, secrets, or raw source data marked do-not-modify. Taking a normal git commit or tag as the Step 4 restore point is fine.
- Make the smallest set of moves that achieves a clean layout; do not opportunistically rewrite file contents beyond the reference rewiring a move requires.
