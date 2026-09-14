# Project Template — Setup Instructions

Start with `PLATFORM_SETUP.md`: choose Claude or OpenAI and verify source access. `AGENTS.md`
is shared policy; `CLAUDE.md` is its thin Claude adapter. ChatGPT needs the explicit project-source
bootstrap; Codex uses the repository workspace. No surface is verified merely by copying files.


> The default layout for a assistant project: a small core that every project wants, plus optional
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
AGENTS.md      ← shared instructions and file map
CLAUDE.md      ← thin Claude adapter
PLATFORM_SETUP.md ← source bootstrap, settings mirror and verification
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

The listing above says what exists. `AGENTS.md`'s **File Map** says what each thing is *for* and
what the assistant may write to — that table is what a session actually reads, and it is the one to keep
current as the project changes.

**The blocks:**

| Block | Folder / file | Keep it when |
|---|---|---|
| Memory | `Profile/`, `Knowledge/` | the assistant needs context that outlives a session — who people are, where topics stand |
| Intake | `Incoming/` | material reaches this project outside a chat (`Incoming/README.md` has the cases) |
| Dispatch routing | `ROUTING_LOG.md` + the *Delegation* section of `AGENTS.md` | work here gets delegated to subagents, workflow stages, or scheduled tasks |

`templates/BLOCKS.md` is the full catalogue: these three, plus the blocks a project installs later
from a task or another template, each with what it costs per session and where its installation
procedure lives.

---

## Setting it up

### Step 1 — Copy and rename

Copy `PROJECT_TEMPLATE/` to where the project should live and rename it.

### Step 2 — Delete the blocks you don't need

Work down the block table above. For each block you drop, delete **all** of its pieces: the folder
or file, its section in `AGENTS.md`, and its rows in the file map. Dropping the memory block also
means replacing the auto-read line above that table, which names `Profile/PROFILE_SUMMARY.md`. A
rule pointing at a folder that no longer exists is worse than no rule, and it sits in the part of
`AGENTS.md` that loads in every session.

### Step 3 — Fill in AGENTS.md

Replace every `[PLACEHOLDER]`; search for `[` to find them. The sections that need real thought:

- **About** — delete it outright for a project that is not about a person.
- **Context** — what this project covers, specifically enough that a stranger could tell it apart
  from your other projects.
- **Critical Rules** — hard constraints only, the ones that override default behavior.
- **File Map** — prune and extend it to match what the folder actually holds.
- **Platform setup** — complete the separate `PLATFORM_SETUP.md` in Step 5.

### Step 4 — Seed the memory block (if you kept it)

In `Profile/PROFILE_SUMMARY.md`, fill in who you are, what is active right now, and the people
the assistant will meet in this project. Leave the Open Action Items table empty; it fills itself.

In `Profile/PROFILE_detail.md`, add entries for anyone or anything the assistant needs context on from
day one. `Knowledge/` starts with just its index; topic files get created when a topic earns one.

### Step 5 — Configure the selected surfaces

Follow `PLATFORM_SETUP.md` and its bootstrap, source manifest and per-surface settings mirror.
For ChatGPT upload the shared policy and required sources; for Codex open the repository.
For Claude Code retain the adapter; for Cowork connect the folder and set its bootstrap.

### Step 6 — Check in fresh sessions

Run `tests/behaviour/README.md` on each selected surface. Record the actual result separately.
Uploaded source refresh and shared policy changes require a new check.

### Step 7 — Add blocks as the project earns them

Nothing else needs deciding up front. When the project starts producing a recurring run, or
accumulating a domain worth a wiki, or needing its own skill, open `templates/BLOCKS.md` and
install that block then. `tasks/onboard-project.md` walks all of this interactively, including the
git, ignore-hygiene, and security passes this file does not cover.

---

## How the project grows

**The profile maintains itself; you correct it.** After seeding, the assistant updates the profile files
as it learns things — in conversation, from a task run, or when you tell it to remember something.
The hypothesis system in `PROFILE_detail.md` tracks what the assistant believes but has not confirmed;
review those occasionally and mark them `[CONFIRMED]` or delete them.

**Files split before they sprawl.** A profile or knowledge file past roughly 150 lines splits into
topic files with the index updated. Update the file map in `AGENTS.md` when it does.

**Outputs never accumulate at the root.** That is one of the failures this layout exists to
prevent, and it happens one "just this once" at a time. `Outputs/README.md` carries the naming
convention for deliverables that go through versions.

To fix a project that has already drifted, run `tasks/reorganize-project.md` — it takes a restore
point first, then moves files and rewires every reference to them.

---

## This template vs. the others

| | PROJECT_TEMPLATE | TASK_TEMPLATE | PMO_TEMPLATE |
|--|---|---|---|
| **What it is** | A project workspace — the container The assistant operates in | One scheduled automated workflow | A programme workspace with registers |
| **When the assistant runs** | On demand, in your sessions | On a schedule | On demand, in your sessions |
| **Primary file** | `AGENTS.md` (load verified per surface) | `TASK.md` (loaded per run) | `AGENTS.md` + `PROJECT_GUIDE.md` |
| **Memory** | Profile + Knowledge files | `KNOWLEDGE_SUMMARY.md` + `IMPROVEMENTS.md` | The register suite |
| **Self-improvement** | Your corrections in conversation | The Step 6 self-improvement loop | The cross-reference audit task |

A project contains tasks, not the other way round: a task folder from `TASK_TEMPLATE` is dropped
*into* a project and reads and updates that project's files.

---

## Handing this template to your assistant

To set up a new project:

> "Read `templates/PROJECT_TEMPLATE/README.md`, copy the folder to [destination], rename it
> [project name], and walk me through Steps 2–6. Here is what the project is: [describe it, the
> domain, and any hard rules]."

To add a block to a project that already exists:

> "Read `templates/BLOCKS.md` and install the [block name] block in [path]. Ask me what you need."

To retrofit this layout onto a project that grew without one:

> "Read `tasks/reorganize-project.md` and run it against [path], targeting the layout in
> `templates/PROJECT_TEMPLATE/README.md`."
