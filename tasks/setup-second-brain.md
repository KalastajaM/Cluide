# Task: Setup Second Brain

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-second-brain.md`
> **Source guide:** `28_SECOND_BRAIN.md` (see also `15_LLM_WIKI.md` for the boundary against a curated domain wiki)

## Purpose

Build or repair the personal knowledge layer that sits above a user's projects: the four homes sorted by relevance decay, an index cheap enough to always load, an inbox with an emptying rule, and a review pass that prunes and resolves contradictions. Use it when a user keeps notes scattered across apps, when a notes folder has grown past the point where anyone opens it, or when `analyze-project.md` dimension 16 reports a second-brain finding — a notes tree with no index, an `inbox/` with permanent residents, notes contradicting each other with nothing marked superseded, or curated domain material mixed in with general working notes.

This is not the wiki task. `setup-wiki.md` builds one curated domain where every source enriches existing pages; this builds a many-domain layer where the job is triage. A project that needs both gets both, in separate roots.

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons rather than plain text.

### Step 0 — Preconditions

Confirm you can read and write the folder the layer will live in, and that it is a folder Claude can mount — markdown files on disk, not an app database. If the user's notes are currently in Notion, Roam, Evernote or similar, say plainly that the layer cannot be built where it is and that the first decision is an export, not a folder structure. Guide 28's *Format beats features* is the reasoning; do not restate it, point at it.

Establish whether this is a **new** layer or a **repair** of an existing one. The two run different steps: a repair does Steps 1, 2, 5 and 6; a new build does 1 through 4 and 6.

### Step 1 — Test whether it is worth building (read-only)

Guide 28 opens with an objection and the task honours it. Ask what the user currently keeps and where, then apply the guide's filter: a second brain earns its keep when it holds synthesis, decisions and their reasons, material whose source is unreliable or unsearchable, or cross-cutting connections. Material that will still be searchable in its own system next year is a link and a sentence, not a note.

If nothing the user described passes that filter, say so and stop. Recommending a structure for material that does not need one is the failure this guide exists to prevent. Offer the alternatives instead: `04_MEMORY_AND_PROFILE.md` for facts about the user, `14_PERSONAL_DATA_LAYER.md` for structured data, `15_LLM_WIKI.md` for one deep domain.

### Step 2 — Interview

Ask, in this order, and stop asking once you have enough to place notes:

1. **Where should the root live**, and is any of it material that should not sit beside the rest (a client's material next to the user's own)? Separate roots, not separate top-level folders — `23_MULTI_PROJECT_SETUPS.md` covers the split.
2. **What is currently in flight** — the things with an end date. These become the initial `projects/` subfolders.
3. **What the user maintains indefinitely** — finances, a property, health records, a domain they own at work. These become `areas/`.
4. **How material arrives** — browser clipper, a running text file, meeting dumps, or Claude writing the note at the end of a session. The last route produces the best notes and is the one users forget they have.
5. **What cadence the user will actually hold** for emptying the inbox. Take the answer at face value and size the capture filter to it; do not negotiate them up to weekly.

### Step 3 — Present the plan and get sign-off

Show the proposed root path, the folder tree, the initial `projects/` and `areas/` subfolders drawn from the interview, the capture route, and the review cadence. Name anything you are deliberately not creating and why — an empty `resources/` taxonomy, for instance, because the guide's sorting rule fills it on demand.

Then **stop and wait.** Do not create anything on assumed approval.

### Step 4 — Create the structure (new build)

Create the root and the five folders, plus `index.md`:

```
second-brain/
├── index.md
├── inbox/
├── projects/
├── areas/
├── resources/
└── archive/
```

`index.md` is the part most often missing and the part that makes the difference. Write it as a map, not a table of contents: what lives in each home, the current `projects/` and `areas/` entries one line each, and a recently-changed section the review pass updates. Keep it small enough to load on every question.

Write the capture frontmatter into `inbox/README.md` so the shape is available at capture time rather than remembered:

```markdown
---
captured: YYYY-MM-DD
source: <url, person, meeting, or "own thinking">
why: <the question this was saved for>
---
```

Say in that README that `why` is the field that makes triage possible and the one most often skipped, and that the inbox is emptied rather than managed.

### Step 5 — Migrate existing notes (repair, or a new build with material to move)

**Take a restore point before the first move**: a git commit or tag if the notes are under version control, otherwise a dated zip of the notes root stored outside it. Confirm it exists before moving anything. A migration that mis-sorts a hundred notes is recoverable only if there is a way back.

Then sort read-only first and present the result before moving:

- Place each note by **when it stops being relevant**, not by topic. The same subject can land in three homes; that is the rule working, not a mistake.
- **When in doubt, `resources/`.** The review pass moves it if it was wrong. Hesitating is the friction that kills the habit.
- Flag, do not silently resolve, notes that **contradict each other**. Present the pairs; the user decides which is current, and the loser gets a `superseded_by:` field rather than deletion.
- Flag material that belongs to a **curated domain** rather than this layer, and route it to `setup-wiki.md` instead of filing it.
- Flag notes that are **tasks in disguise**. They go where tasks live and leave the layer.
- Do not flatten folders when archiving. Move them intact.

### Step 6 — Wire the review and the return leg

**The review.** Set up the cadence agreed in Step 2 as a scheduled task if the user wants it automated — `setup-scheduled-task.md` owns that shape, do not build a rival one here. The pass empties `inbox/`, moves anything the sorting rule placed wrongly, prunes `resources/`, resolves contradictions by editing rather than by keeping both versions, and refreshes `index.md`'s recently-changed section.

**The return leg.** A second brain that only ever receives from the user misses the material worth the most: the conclusions Claude and the user reach together. Offer to add a return-leg block to the CLAUDE.md files of the projects that produce conclusions — a short standing instruction to write a note to `inbox/` when a session settles a question, with the `captured` / `source` / `why` frontmatter. `templates/BLOCKS.md` carries the block; a project's own CLAUDE.md is where it goes.

State plainly what a return leg must not capture: routine work, in-progress state, and figures another project owns. A layer that receives everything a session touches becomes an archive nobody opens, which is the failure mode in Guide 28's anti-patterns.

## Output

A created or repaired notes root with the five homes and an `index.md`; a capture convention written where capture happens; where notes were migrated, a list of what moved, what was flagged as contradictory, and what was routed elsewhere; and either a scheduled review task or an agreed manual cadence.

## Constraints

- Read-only until Step 3 is approved.
- **Restore point before the first move** in Step 5. No bulk migration without a way back.
- Never delete a note. Deletion is the user's call during triage, per note, and this task only proposes it.
- Never resolve a contradiction between two notes by picking one. Present the pair.
- Do not build a tag taxonomy. Status, review date, confidence, source and `superseded_by:` earn their keep; topical tags do not.
- Do not merge this layer with a Guide 15 wiki, and do not create one here. Separate roots.
- Respect an existing structure that works. A layout that differs from the guide but empties its inbox is a working layout, not a finding.
