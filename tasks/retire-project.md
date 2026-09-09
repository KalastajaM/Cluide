# Task: Retire Project

> **Cluide task** — end a project, or a single scheduled task, so that nothing current points at it afterwards: transfer what it owned, remove what referenced it, freeze what remains.
> **Source guides:** `33_RETIRING_AND_LEAVING.md`, `23_MULTI_PROJECT_SETUPS.md`, `24_PROJECT_FOLDER_STRUCTURE.md`. Where `relocate-project.md` moves a project that continues, this ends one. The two share the reference-layer inventory; this task adds memory, credentials and ownership, which a move does not need.
> **Leaving an organisation or account** is Guide 33 §5 and is a checklist rather than a task, because most of its steps happen in app settings and on the user's own decisions. This task runs per project inside that checklist.

## Purpose

Retire a project (or one task) without leaving live wires. A stopped project keeps a scheduled task that fails or runs stale, a registry row that owns facts nobody updates, memory lines in the present tense, an app-side description that loads as identity, grants nobody watches, and a public remote that keeps publishing. None of it breaks visibly, which is why the task exists: it inventories every layer that can point at the project, transfers ownership of anything it owned, rewires or removes every load-bearing reference, and freezes the folder in a state a future session recognises as ended.

Use it when a project's purpose has ended, when a project is being absorbed into another (run this on the absorbed one after `23_MULTI_PROJECT_SETUPS.md`'s merge), when a scheduled task has outlived its event, or when `analyze-project.md` dimension 25 reports a retired-looking project with live references — a disabled task, a present-tense memory line, an owner row for a project nobody opens.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 0 — Preconditions and scope

Confirm:

- The project is mounted, plus every project that references it and the coordinator or maintenance project if one keeps a registry. A retirement with the consumers unmounted rewires nothing and reports success.
- The project is fully readable — the transfer in Step 3 needs the source intact. Never retire from a half-archived tree.
- Its git repository, if any, is committed and clean. Commit anything dirty now; the retirement's final commit is not the place to discover uncommitted work.
- Whether the scope is the **whole project** or **one task** in it. A single task runs Steps 1 to 4, then Step 6 instead of Step 5, then Step 7; the whole project runs everything except Step 6.

Ask the user for the **reason** and the **successor**, if any. Both go into `RETIRED.md`, and the successor is where Step 3 transfers to.

### Step 1 — Inventory what points at it (read-only)

Sweep every layer in Guide 33 §2's table and record each hit. Do not trust one search pattern: the project is referenced by name, by path, by its task names, and by its registry identifier.

```bash
grep -rIn -e "<project name>" -e "<project path>" -e "<task names>" \
  --exclude-dir=.git --exclude-dir=node_modules <projects root> <coordinator project>
```

Beyond the grep, read directly:

| Layer | Read |
|---|---|
| Scheduled tasks | Every task definition and registration on the surface(s) the user runs — Cowork's task registrations, Claude Code Routines, hooks with schedules. Read each; do not infer from folder names |
| Orchestration | Shared-state and handoff files, and any chain that names this project's task as a stage |
| Ownership registry | Every row naming this project as owner |
| Memory | Account memory and the project's own per-project store (ask the user to search both in the app for the project's name and read out what is there — a session cannot); Claude Code auto memory for the project; `.auto-memory/` files in *other* projects; profile files in tasks |
| Second brain | Index entries and notes linking into the project |
| App-side fields | The project's description and instructions (from the mirror block, or pasted by the user); its `spaces.json` row where the Filesystem MCP reaches it |
| Artifacts | Published pages fed by the project's tasks |
| Grants | Connector authorisations, computer-use grants and tokens scoped to the project (ask the user for the connector list; read `.env` names — never values — and keychain entries the project documents) |
| Claude Code state | Under `~/.claude/projects/`: the transcript directory keyed by path and the auto-memory directory keyed by repository — Guide 33 §2 says they are located separately |
| Git | The remote's visibility, open branches, other repos that reference it |

Classify every hit before proposing anything, as `relocate-project.md` does: **history** (a dated report, a log entry — stays untouched), **pointer** (another project's link or memory line — needs a new target or removal), or **load-bearing** (a task registration, a registry owner row, a chain stage — must go or be re-pointed).

### Step 2 — Inventory what it owns (read-only)

From the ownership registry and from the project's own `CLAUDE.md` file map, list every shared fact, file or dataset the project is the source of truth for, and which consumers read it. If there is no registry, derive it: anything another project's files reference by path or by name is owned here.

For each, propose one of Guide 33 §3's three outcomes — **transferred** (to the named successor), **retired with the project**, or **frozen** (historical, stays in the archive, consumers rewired to what replaced it as current). Propose; do not decide.

### Step 3 — Present the plan and get sign-off

Present, grouped by layer:

1. **Ownership outcomes** for every Step 2 item, with the successor named for each transfer.
2. **The rewiring table** for every pointer and load-bearing hit from Step 1: file, layer, what changes (re-pointed to the successor, or removed).
3. **What stays** as history, listed so the user can see it was seen.
4. **The freeze**: `RETIRED.md` contents, the git tag, what happens to the remote (archive on the host, or make private), which scheduled-task registrations are deleted, the app-side field text, which grants are revoked, and the archive destination.
5. **The restore point** you will take (Step 4).
6. **Anything irreversible**, first: revoking a grant that is hard to re-obtain, deleting a registration, making a remote private.

Gate three things **separately**: the grant revocations, the app-side field changes, and the remote's visibility. Each reaches beyond the folder, and the first two the user does by hand — a session cannot revoke a connector or write an app-side field; it produces the ready-to-paste text and the list of grants, and the user confirms each.

Then **stop and wait.**

### Step 4 — Take a restore point

Before any change, and confirmed to exist:

- **Under git:** a final commit and the tag `retired-YYYY-MM-DD` on it, before anything is moved. The tag is both the restore point and the archive marker.
- **Not under git:** a dated archive of the project, stored outside the projects root.
- **Always:** a copy of every *other* file the rewiring will edit — other projects' `CLAUDE.md` and memory files, the registry, orchestration files — alongside itself with a dated suffix.

Retire the restore point only after Step 7 verifies.

### Step 5 — Transfer, rewire, freeze (whole-project scope)

Three phases, in this order, because each needs the previous one's state. The end state of each is defined in Guide 33; this step is the order and the hand-offs, not a restatement.

1. **Transfer ownership** (Guide 33 §3). Move, never copy; leave a pointer behind; update the registry row; rewire every consumer of a transferred or frozen item, with a freshness check where a task now reads a file another project produces (Guide 23, step 6).
2. **Rewire and remove references.** Apply the Step 3 table row by row, never as a bulk replace across the tree. Scheduled-task registrations are **deleted**, not disabled; orchestration stages are taken out and their downstream dependencies rewritten; artifacts are re-pointed or retired with a final as-of note. The user removes account-memory and per-project-store entries by hand and confirms; the session removes the on-disk lines.
3. **Freeze** (Guide 33 §4), in the order that section gives: the user pastes the retired app-side text and the session updates the mirror block, then the project leaves the app; the user revokes grants and confirms each; the session writes `RETIRED.md`, archives the folder, renames the Claude Code state directories alongside, and reports what the remote needs (archive on the host, or private), which the user does.

If applying reveals something the plan missed — a consumer not in the inventory, a fact with no successor — stop and present a revised plan.

### Step 6 — Retire a single task (task scope)

Disable the schedule first, so nothing runs mid-procedure. Then apply the approved Step 3 rows for the task: remove it from orchestration chains and shared-state files; remove memory lines and profile files that existed only for it; the user revokes credentials it alone held; move its folder to `_archive/` with a dated note; **delete** its registration; remove it from the project's `CLAUDE.md` file map.

If the task is being **succeeded** rather than ended, do not run this until the successor has run alongside for enough cycles to trust (Guide 33 §6, Guide 29 on keeping the old version as the oracle).

### Step 7 — Verify

Run Guide 33 §4's verification list in full — it is the definition of done and is not shortened here — plus the two checks only this task can make:

- Re-run the Step 1 sweep with the same patterns. Every remaining hit is a classified history mention.
- No lock files left in any repository touched.

Report by layer: transferred, rewired, removed, revoked, and deliberately left as history. Then retire the restore point.

## Output

A classified inventory of everything pointing at the project (Step 1); the ownership outcomes (Step 2); an approved plan with grants, config and remote gated separately (Step 3); the transfer, rewiring and freeze applied (Step 5, or Step 6 for a task); and a verification report by layer (Step 7).

## Constraints

- Read-only until Step 3 is approved. Grant revocations, app-side field changes, and the remote's visibility need their own separate approvals, and the user performs them.
- Transfer before archive, always. Never archive a project whose owned facts have no recorded outcome.
- Never delete the folder. Archive it.
- Never leave a scheduled-task registration disabled as the end state; delete it, or move it under `relocate-project.md` if a successor needs it.
- Never bulk search-and-replace the project's name across a tree. Apply the classified rows only; history mentions stay.
- Never write the app's state files (`spaces.json` or any other). Produce ready-to-paste text; the file is the mirror, not the control (Guide 25).
- Never read credential values; read names and scopes, and have the user perform revocations.
- Confirm the restore point exists before the first change.
