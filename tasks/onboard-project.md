# Task: Onboard Project

> **Cluide task** — run this to set up a new project end-to-end:
> `Claude, run tasks/onboard-project.md`
> **Source guides:** `01_CLAUDE_MD.md`, `04_MEMORY_AND_PROFILE.md`, `05_MCP_SERVERS.md`, `11_GIT_INTEGRATION.md`, `12_SECURITY.md`, `24_PROJECT_FOLDER_STRUCTURE.md`, `25_PROJECT_INSTRUCTION_LAYERS.md`

## Purpose
Set up a new project end-to-end, in the right order, without the user having to know which
individual setup tasks exist. It installs the default layout first (Guide 24), sets all three
instruction layers (Guide 25), and only then offers the optional blocks from
`templates/BLOCKS.md`. Git, ignore hygiene, and security run last, over a project that already
has its real shape.

This task orchestrates the other setup tasks rather than duplicating their logic: it reads the
relevant task files and runs them in sequence.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 0 — Locate Cluide and the destination

Confirm the Cluide folder is reachable (the templates and tasks below are read from it) and that
the destination folder for the new project exists or can be created. If Cluide is not mounted,
stop and ask for it rather than reconstructing a layout from memory.

### Step 1 — Understand the project

Ask:
> 1. What is this project? (one sentence)
> 2. Is this a new empty folder, an existing codebase, or a pile of material that needs organising?
> 3. What will Claude mainly help with here — writing, code, documents, research, scheduled runs?
> 4. What does it produce? (documents, code, reports, nothing tangible)
> 5. Does material arrive here outside a chat — scans, downloads, exports, files from other people?
> 6. Will it use external tools: email, calendar, GitHub, a database?
> 7. Will it hold sensitive data, credentials, or personal information?

Question 4 decides the outputs home and question 5 the intake block; do not skip either because
the user's one-sentence answer to question 1 sounded complete.

### Step 2 — Choose the starting point

Use `AskUserQuestion` with buttons:

> "Which starting point fits this project?"
>
> Buttons: `PROJECT_TEMPLATE (default)` / `PMO_TEMPLATE` / `AI-ASSISTANT_TEMPLATE` / `Existing folder, retrofit the layout`
>
> - **PROJECT_TEMPLATE** — the default layout: instructions, outputs, scratch, archive, plus the
>   memory, intake, and routing blocks ready to keep or delete. Right for almost everything.
> - **PMO_TEMPLATE** — the same idea with a full register suite (risk, action, decision,
>   dependency) already built. Right for a structured programme.
> - **AI-ASSISTANT_TEMPLATE** — a turn-key personal assistant with Microsoft 365 and four
>   coordinated scheduled tasks. It has its own setup procedure.
> - **Existing folder** — the project already has material. The layout gets retrofitted around it.

Recommend one based on Step 1 rather than leaving the choice open, then route the three
non-default answers explicitly:

- **PMO_TEMPLATE** — run Step 3 against `templates/PMO_TEMPLATE/` and follow
  `templates/PMO_TEMPLATE/README.md` rather than PROJECT_TEMPLATE's, then continue at Step 4. Its
  registers replace the blocks PROJECT_TEMPLATE ships; do not offer both.
- **AI-ASSISTANT_TEMPLATE** — follow `templates/AI-ASSISTANT_TEMPLATE/bootstrap/SETUP.md`
  instead of Steps 3–5, then rejoin at Step 6.
- **Existing folder** — run `tasks/reorganize-project.md` (it takes a restore point before
  moving anything) targeting the layout in `templates/PROJECT_TEMPLATE/README.md`. That task moves
  files; it does not write a `CLAUDE.md`. Rejoin at Step 3, skipping only its copy sub-step, so the
  project still gets its instructions file and file map.

### Step 3 — Install the core

Copy the chosen template to the destination and rename it:

```bash
cp -r "<CLUIDE>/templates/<chosen template>" "<destination>/<Project Name>"
```

Then work through the core with the user, following that template's `README.md` Steps 2–4. For
PROJECT_TEMPLATE that means:

1. **Delete the blocks this project does not need**, using the Step 1 answers. No material
   arriving outside chat means `Incoming/` and its `CLAUDE.md` section go. No delegation means
   `ROUTING_LOG.md` and the *Dispatch Overrides* section go. Deleting a block means deleting all of
   its pieces — folder, `CLAUDE.md` section, and file-map rows — never one without the
   others. Dropping the memory block also means replacing the auto-read line above the file map,
   which names `Profile/PROFILE_SUMMARY.md`: that line sits in the part of `CLAUDE.md` that loads
   in every session, so a stale one is the most expensive leftover in the file.
2. **Fill in `CLAUDE.md`**: identity, context, communication style, critical rules, and the file
   map. Prune the file map rows for deleted blocks and add a row for each folder this project
   needs that the template does not ship.
3. **Seed the memory block** if it was kept: `Profile/PROFILE_SUMMARY.md` first, then any
   `Profile/PROFILE_detail.md` entries Claude will need from day one. Where the project needs a
   layer the template does not ship — native memory or `.auto-memory/` rather than profile files —
   run `tasks/setup-memory.md`; it owns the choice between the three layers and this task does
   not restate it.

For a project whose rules need drawing out rather than typing in — an unfamiliar domain, hard
constraints the user has not articulated, an existing codebase with conventions worth capturing —
run `tasks/setup-claude-md.md` for its interview and bring the result into the template's file
rather than replacing the file with its output. The template's file map and app-side block are
not part of that task's output and must survive.

Do not fill in the *App-side fields* block yet — Step 4 produces its text.

### Step 4 — Set all three instruction layers

The folder is one of three channels a Cowork project speaks through, and it is the only one this
task can write directly. **`tasks/tune-instruction-layers.md` owns this step** — run its Step 1
(read the fields as they currently stand), Step 3 (draft and present both texts) and Step 5
(update the mirror block once the user confirms they have pasted them). It carries the state-file
path, the absent-versus-empty rule, the freshness caveat and the sibling files to ignore; none of
that is repeated here, because a second copy of an app-internal detail is a second thing to
re-verify after every app update.

Two things this task adds on top, because they are specific to a project being created rather
than tuned:

1. **A new project has no fields to read.** Where Step 1 finds nothing, that is the expected state,
   not a finding — draft both texts from the Step 1 answers and the template's own purpose.
2. **Leave the instructions field empty only for a project with no real-world stakes**, and say so
   explicitly rather than by omission, so the empty field reads as a decision.

Where this task and `tune-instruction-layers.md` appear to differ, that task wins.

### Step 5 — Offer the blocks

Read `templates/BLOCKS.md` and present only the blocks the Step 1 answers actually point at.
Do not read the catalogue out. For each one offered, say what it adds and what it costs per
session, then install it by following its *Install* column — a task for most, a guide section or
a copy from another template for the rest.

Recommend deferring anything the project cannot yet use. A wiki with no material, a scheduled
task with nothing to run, and a skill for a workflow that has happened once are all better added
in a month, and the catalogue is where the user will find them.

### Step 6 — Ignore hygiene

Follow `tasks/setup-ignore-hygiene.md` — scan, propose, apply, handle already-tracked files. The
template ships a `.gitignore.template`; rename it to `.gitignore` and treat it as the starting
point, not the answer.

For the enforcement option in that task, recommend Option A (PostToolUse hook) for a code
project and Option B (CLAUDE.md rule) otherwise.

### Step 7 — Git and GitHub

Ask:
> "Should this project be on GitHub? (Yes / No / It already is)"

- **Yes:** follow `tasks/setup-github.md` — init, create the repo, first commit, ongoing sync.
- **Already is:** check whether ongoing sync is set up; offer Step 8 of `setup-github.md` if not.
- **No:** `git init` and one local commit. A project holding anything worth keeping gets version
  control even with no remote.

### Step 8 — Security

Follow Steps 1–3 of `tasks/setup-security.md` — credential scan, permission audit, file hygiene.

Then ask whether to install the PreToolUse hook that blocks dangerous shell commands, and follow
Step 6 Fix A of that task if yes. Recommend it whenever the project's work involves running
commands.

### Step 9 — Optional: MCP servers

If Step 1 named external systems, follow Steps 2–4 of `tasks/setup-mcp.md` for those servers
only. Curate the loadout rather than enabling everything available — Guide 05 covers why the
wrong-tool cost matters more than the token cost.

### Step 10 — Confirm

Report what was set up:

```
Project Onboarding Complete
────────────────────────────
✓ Layout — core installed at [path]; blocks kept: [list]; blocks deleted: [list]
✓ CLAUDE.md — [N lines], file map covers [N] homes
✓ Instruction layers — description set, instructions [set / deliberately empty], mirror block dated [date]
✓ .gitignore / .claudeignore — [N patterns]
✓ Git / GitHub — [local only / github.com/...]
✓ Security — [clean / N issues found and fixed]
[✓ Blocks installed — [names]]
[✓ MCP servers — [names]]
⚠ Placeholders still to fill — [file and section for each, or "none"]
```

Then name the one or two blocks most likely to be needed next and where they live, so the user
does not have to remember this task existed.

---

## Output

A project folder containing the core layout, a filled-in `CLAUDE.md` with a file map and a dated
app-side mirror block, whichever blocks the project needed, git and ignore hygiene, and a
security pass. Plus two texts handed to the user for pasting into the app's project settings.

## Constraints

- **The app-side fields are written by the user, never by this task.** Produce ready-to-paste
  text and confirm afterwards; do not edit the app's state file.
- **Never fill placeholders with plausible guesses.** An unanswered question stays a placeholder
  and is named in the Step 10 report.
- **Retrofitting an existing folder goes through `tasks/reorganize-project.md`**, which takes a
  restore point first. Do not move a user's existing files directly from this task.
- **Blocks are offered, not installed by default.** Every always-loaded block is paid for in
  every session, including the ones that never use it.
