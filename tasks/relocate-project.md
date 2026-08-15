# Task: Relocate Project

> **Cluide task** — move a project, several projects, or an entire projects root to a new location without leaving broken references behind.
> **Source guides:** `11_GIT_INTEGRATION.md`, `24_PROJECT_FOLDER_STRUCTURE.md`. Where `reorganize-project.md` tidies *inside* one project, this moves the project itself.
> **Per-layer detail:** `relocate-project-reference.md` — load it at Step 2 or Step 5, not before.

## Purpose

Relocate one or more project folders and rewire every reference to them — in the projects, in the scheduled tasks that run unattended, and in the desktop app's own configuration. Absolute paths are recorded in all three places and all three break silently when a folder moves.

Use it when moving projects to a new disk or parent folder, consolidating scattered projects, renaming a projects root, or recovering from a move that has already broken things.

The reason this is its own task: a move looks like a filesystem operation and is actually a reference-rewiring operation with a filesystem step in the middle. The scheduled-task layer is the one that hurts — a broken scheduled task fails quietly on a schedule and nobody notices for weeks.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 0 — Preconditions

Confirm all of these before touching anything:

- **The destination is on local disk, and specifically not inside a streaming sync folder.** See *Why not a sync folder* below. This is the one precondition that has actually destroyed data.
- The old location is still fully readable, or a complete backup of it is. Never start from a half-copied tree.
- Every git repository in scope is committed and clean. Check, don't assume.
- The parent of everything being moved is mounted, plus any project that references it.
- If the config layer is in scope: the Filesystem MCP server is connected with `~/Library/Application Support/Claude` in its `allowed_directories` — the folder picker refuses that path (Guide 05).

### Why not a sync folder

**Streaming vs. backup matters, and only one of them is dangerous.**

*Streaming* modes — Google Drive "My Drive", iCloud Drive with Optimise Storage, OneDrive Files On-Demand, Dropbox Smart Sync — replace file contents with cloud placeholders. What goes wrong:

- **Git repositories get destroyed.** A `.git/objects/` can simply not survive. The reflog still names the commits, the objects are gone, nothing is recoverable. Sibling repos in the same tree may survive untouched — the damage is arbitrary, which makes it worse, not better, because a spot check proves nothing.
- **Sync daemons fight git for lockfiles.** Commits fail on a stale `.git/index.lock` or `HEAD.lock` that no process holds.
- **Streamed files are invisible to the shell.** A placeholder has a size in Finder and no bytes on disk. `find`, `grep` and Python silently skip it — so an audit reports "clean" on files it never read. This is the failure that makes every other check untrustworthy.

*Backup/mirror* modes (e.g. Drive's "folders from your computer") keep real bytes on disk and are materially safer. Lock contention still applies: exclude `.git` from the backup selection if the client allows it. Working directories the client leaves behind (`.tmp.drivedownload`, `.tmp.driveupload`) are normal there rather than a warning sign.

If the user wants the destination inside a sync folder anyway, state which mode it is and what specifically breaks, then let them decide. Do not proceed silently.

### Step 1 — Inventory before touching anything (read-only)

Record the starting state so anything that fails to arrive is detectable afterwards:

```bash
find <old-root> -maxdepth 1 -type d | sort          # the project list
du -sh <old-root>/*                                  # sizes
```

Per project: `git -C <project> rev-parse HEAD` and `git -C <project> status --porcelain`. Commit anything dirty now, before the move, not after.

Keep this inventory. Projects do go missing in bulk moves, and diffing this list against the destination is how you find out.

### Step 2 — Build the reference inventory (read-only)

Search the whole scope for the **old** path. Do not trust one pattern — paths are written several ways:

```bash
grep -rIn -e "<old-root>" -e "<old-root-with-~>" -e "<old-root-url-encoded>" \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist <scope>
```

Sweep three layers. The second and third are outside the projects and are the ones a naive grep misses:

| Layer | Where | Why it breaks |
|---|---|---|
| **Projects** | The moved project(s), plus any *other* project that points at them | `CLAUDE.md` file maps, READMEs, task files, cross-project pointers |
| **Scheduled tasks** | Definitions under `<CLAUDE_ROOT>/Scheduled/*/`, and their registrations in `scheduled-tasks.json` | They run unattended: a broken one fails quietly on a schedule, and the folder and the registration break separately |
| **Artifacts** | `<CLAUDE_ROOT>/Artifacts/<id>/index.html` and whatever generates them | An artifact fed by a broken generator keeps rendering stale data with no error anywhere |
| **Claude Code state** | `~/.claude/projects/` (one directory per project, named after its path) and `~/.claude.json` | A move orphans the project's whole transcript history under a dead name, and orphans can be garbage-collected |
| **Config** | `~/Library/Application Support/Claude/` — including `spaces.json`, which records `folders[].path` per project | The app's own record of where each project's folder is |

`<CLAUDE_ROOT>` is the Claude data root, recorded as `coworkUserFilesPath` in `claude_desktop_config.json`. Read it there rather than assuming a location.

Classify every hit before proposing a fix. A path inside a code fence in a guide is documentation; a path in a scheduled task's definition is load-bearing; a path in a dated report is history and must not be rewritten at all. They get different treatment, and telling them apart is the point of classifying.

**Read `relocate-project-reference.md` for the per-layer mechanics before sweeping any layer beyond the projects themselves.** Each of the other four has a failure mode a path grep does not see, and three of them cannot be repaired from a session at all.

### Step 3 — Propose the plan and get sign-off

Present:

- The **old → new** mapping for every folder that moves.
- The reference-rewiring table: file, layer, what changes. Group by layer.
- What stays untouched.
- The **restore point** you will take (Step 4).
- Anything irreversible.

Gate the **config layer separately.** It is the app's own state, the blast radius reaches every project rather than the ones being moved, and it is the layer the user is least able to inspect. A yes to moving folders is not a yes to editing app configuration.

Then **stop and wait.**

### Step 4 — Take a restore point

Before moving anything, and confirmed to exist before the first change:

- **Under git:** commit or tag the current state on every repo in scope.
- **Not under git:** a dated archive of the affected tree, stored **outside** both the old and new locations.
- **Always:** back up any config file you will edit, alongside itself (`spaces.json.bak-YYYY-MM-DD`).

Retire the restore point only once Step 6 verifies the result.

### Step 5 — Move, then rewire

1. **Quit the desktop app before touching its config.** It rewrites its state files wholesale from memory, so an edit made while it runs is silently discarded (Guide 25). This is the single most common way a config fix appears to work and doesn't.
2. **Move the folders.** Prefer a copy-then-verify-then-remove over an in-place move when crossing volumes.
3. **Verify arrival before rewiring:** diff the Step 1 project list against the destination, and re-run `git -C <project> rev-parse HEAD` on every repo. A repo that reports a different HEAD, or fails, stops the run.
4. **Rewire each approved reference.** Never bulk-replace blind across the whole tree: a global search-and-replace on a path string will rewrite documentation, historical logs, and other projects' records of where things used to be. Apply the classified table from Step 2, row by row, using the anchored-replacement rules in `relocate-project-reference.md` — replace complete strings only, assert before and after, and check for the doubled slash an unanchored replace leaves behind, which POSIX hides from the shell while every string-matching consumer breaks on it.
5. **Restart the app** and confirm the projects resolve.

If applying reveals something the plan missed, stop and present a revised plan.

### Step 6 — Verify

- No references to the old path remain outside the ones deliberately kept (re-run the Step 2 grep).
- Every project from the Step 1 list is present at the destination, with matching HEADs.
- Every scheduled task resolves to a path that exists. Read each definition; do not infer from the folder existing. A repaired folder with a stale registration is still broken (reference, *The scheduled-task layer*).
- Every generator task has been re-run and each artifact's own as-of date has advanced. A stale artifact is the one failure in this list that shows no error.
- `~/.claude/projects/` has a directory under the new path name, and the old one has been merged or renamed rather than left to be collected.
- The app lists every project and each opens its folder.
- No lock files (`index.lock`, `HEAD.lock`) left behind in any repository.

Report what moved, what was rewired per layer, and what was deliberately left alone. Then retire the restore point.

## Output

A pre-move inventory (Step 1), a classified reference table (Step 2), an approved move-and-rewire plan with the config layer gated separately (Step 3), and a post-move verification report (Step 6).

## Constraints

- Read-only until Step 3 is approved. The config layer needs its own separate approval.
- **Never relocate into a streaming sync folder.** If the user insists after being told what breaks, that is their call — record it in the plan.
- Never bulk search-and-replace a path across a tree. Rewire the classified rows only.
- Never edit the app's config while the app is running.
- Confirm the restore point exists before the first move.
- Verify arrival *before* rewiring references — rewiring toward a tree that didn't fully arrive turns a recoverable problem into a scattered one.
- Never touch `.git/` internals beyond normal commit/tag operations.
