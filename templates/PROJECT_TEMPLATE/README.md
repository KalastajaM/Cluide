# Project Template — Setup Instructions

> The default layout for a Claude project: a small core that every project wants, plus optional
> blocks you keep or delete. Implements the standard layout in Guide 24
> (`24_PROJECT_FOLDER_STRUCTURE.md`), the three instruction layers in Guide 25, and the profile
> pattern in Guide 04.

---

## Core and blocks

The folder ships with everything in place, so setting a project up is mostly **deleting what it
does not need**. That is deliberate: a block deleted on day one costs nothing, while a home that
was never created is where files quietly pile up at the root.

What you copied:

```
CLAUDE.md      ← instructions, file map, and the mirror of the app-side fields
README.md      ← this file; how the layout works and how to set it up
Outputs/       ← finished deliverables, generated from the sources
Working/       ← scratch and in-progress material
_archive/      ← superseded material, never read back
.gitignore.template
Profile/  Knowledge/  Incoming/  ROUTING_LOG.md   ← blocks; keep or delete each
```

That covers four of the five kinds of home in Guide 24's standard layout: instructions, generated
outputs, scratch, and archive. The fifth — the source of truth, the material the project is
actually *about* — is the one no template can supply, because it is different in every project.
In this template the memory block stands in for it; in yours it might be case files, a dataset, a
codebase, or a folder per tracked entity.

The listing above says what exists. `CLAUDE.md`'s **File Map** says what each thing is *for* and
what Claude may write to — that table is what a session actually reads, and it is the one to keep
current as the project changes.

**The blocks:**

| Block | Folder / file | Keep it when |
|---|---|---|
| Memory | `Profile/`, `Knowledge/` | Claude needs context that outlives a session — who people are, where topics stand |
| Intake | `Incoming/` | material reaches this project outside a chat (`Incoming/README.md` has the cases) |
| Dispatch routing | `ROUTING_LOG.md` + the *Dispatch Overrides* section of `CLAUDE.md` | work here gets delegated to subagents, workflow stages, or scheduled tasks |

`templates/BLOCKS.md` is the full catalogue: these three, plus the blocks a project installs later
from a task or another template, each with what it costs per session and where its installation
procedure lives.

---

## Setting it up

### Step 1 — Copy and rename

Copy `PROJECT_TEMPLATE/` to where the project should live and rename it.

### Step 2 — Delete the blocks you don't need

Work down the block table above. For each block you drop, delete **all** of its pieces: the folder
or file, its section in `CLAUDE.md`, and its rows in the file map. Dropping the memory block also
means replacing the auto-read line above that table, which names `Profile/PROFILE_SUMMARY.md`. A
rule pointing at a folder that no longer exists is worse than no rule, and it sits in the part of
`CLAUDE.md` that loads in every session.

### Step 3 — Fill in CLAUDE.md

Replace every `[PLACEHOLDER]`; search for `[` to find them. The sections that need real thought:

- **About** — delete it outright for a project that is not about a person.
- **Context** — what this project covers, specifically enough that a stranger could tell it apart
  from your other projects.
- **Critical Rules** — hard constraints only, the ones that override default behavior.
- **File Map** — prune and extend it to match what the folder actually holds.
- **App-side fields** — leave it until Step 5.

### Step 4 — Seed the memory block (if you kept it)

In `Profile/PROFILE_SUMMARY.md`, fill in who you are, what is active right now, and the people
Claude will meet in this project. Leave the Open Action Items table empty; it fills itself.

In `Profile/PROFILE_detail.md`, add entries for anyone or anything Claude needs context on from
day one. `Knowledge/` starts with just its index; topic files get created when a topic earns one.

### Step 5 — Set the two app-side fields

A Cowork project speaks to Claude through three channels, and the folder is only one of them
(Guide 25). In the app's project settings:

- **Description** — one to three sentences on what the project is and does, naming the concrete
  entities involved. No rules. It is injected as the project's identity in every session, so a
  stale or copy-pasted one is expensive.
- **Instructions** — only what must hold before any file is read: point at `CLAUDE.md`, have
  Claude verify the folder is connected, and restate the project's single hardest safety rule.

Then paste both texts into the **App-side fields** block at the bottom of `CLAUDE.md` and date it.
The fields have no version history; that block is the only record of what they used to say.

### Step 6 — Connect it and check

Open the project with the folder connected and ask something the project should be able to answer
without being told where to look — "what are my active priorities?" if you kept the memory block,
otherwise anything `CLAUDE.md` covers. If Claude has to be pointed at a file, the file map or the
auto-read line is wrong.

### Step 7 — Add blocks as the project earns them

Nothing else needs deciding up front. When the project starts producing a recurring run, or
accumulating a domain worth a wiki, or needing its own skill, open `templates/BLOCKS.md` and
install that block then. `tasks/onboard-project.md` walks all of this interactively, including the
git, ignore-hygiene, and security passes this file does not cover.

---

## How the project grows

**The profile maintains itself; you correct it.** After seeding, Claude updates the profile files
as it learns things — in conversation, from a task run, or when you tell it to remember something.
The hypothesis system in `PROFILE_detail.md` tracks what Claude believes but has not confirmed;
review those occasionally and mark them `[CONFIRMED]` or delete them.

**Files split before they sprawl.** A profile or knowledge file past roughly 150 lines splits into
topic files with the index updated. Update the file map in `CLAUDE.md` when it does.

**Outputs never accumulate at the root.** That is one of the failures this layout exists to
prevent, and it happens one "just this once" at a time. `Outputs/README.md` carries the naming
convention for deliverables that go through versions.

To fix a project that has already drifted, run `tasks/reorganize-project.md` — it takes a restore
point first, then moves files and rewires every reference to them.

---

## This template vs. the others

| | PROJECT_TEMPLATE | TASK_TEMPLATE | PMO_TEMPLATE |
|--|---|---|---|
| **What it is** | A project workspace — the container Claude operates in | One scheduled automated workflow | A programme workspace with registers |
| **When Claude runs** | On demand, in your sessions | On a schedule | On demand, in your sessions |
| **Primary file** | `CLAUDE.md` (always loaded) | `TASK.md` (loaded per run) | `CLAUDE.md` + `PROJECT_GUIDE.md` |
| **Memory** | Profile + Knowledge files | `KNOWLEDGE_SUMMARY.md` + `IMPROVEMENTS.md` | The register suite |
| **Self-improvement** | Your corrections in conversation | The Step 6 self-improvement loop | The cross-reference audit task |

A project contains tasks, not the other way round: a task folder from `TASK_TEMPLATE` is dropped
*into* a project and reads and updates that project's files.

---

## Handing this template to Claude

To set up a new project:

> "Read `templates/PROJECT_TEMPLATE/README.md`, copy the folder to [destination], rename it
> [project name], and walk me through Steps 2–6. Here is what the project is: [describe it, the
> domain, and any hard rules]."

To add a block to a project that already exists:

> "Read `templates/BLOCKS.md` and install the [block name] block in [path]. Ask me what you need."

To retrofit this layout onto a project that grew without one:

> "Read `tasks/reorganize-project.md` and run it against [path], targeting the layout in
> `templates/PROJECT_TEMPLATE/README.md`."
