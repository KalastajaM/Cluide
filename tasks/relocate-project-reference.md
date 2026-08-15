# Relocate Project — Reference

> Companion to `tasks/relocate-project.md`. Load it when you reach Step 2 or Step 5 and need the
> detail for a specific layer. The task owns the procedure and the gates; this file owns the
> per-layer mechanics, which are long, mostly mechanical, and only relevant once a move is actually
> happening.
>
> **Source guides:** `11_GIT_INTEGRATION.md`, `24_PROJECT_FOLDER_STRUCTURE.md`, `05_MCP_SERVERS.md`
> (reaching protected directories), `25_PROJECT_INSTRUCTION_LAYERS.md` (why app state cannot be
> edited from a session).

Paths below are macOS. The layers exist on other platforms under different roots; the failure modes
do not change, but verify the location before acting on it rather than assuming.

`<CLAUDE_ROOT>` in this file and in the task means the Claude data root — the folder holding
`Scheduled/`, `Artifacts/` and the projects tree. It is recorded as `coworkUserFilesPath` in
`claude_desktop_config.json`; read it there rather than guessing, because it is user-configurable
and a wrong value makes every path below wrong.

---

## Anchored replacement: why a bulk find/replace is the most likely way to break the move

A rollback done with an unanchored find/replace can strip an old root and leave its trailing
slash, producing `/Users/you//Claude/Projects/…`. POSIX collapses a doubled slash mid-path, so the
shell and Python keep working and nothing looks wrong — while every consumer that matches on the
literal string breaks. The two forms are not equally serious:

- A **mid-path** double (`/Users/you//Claude/…`) is cosmetic at the filesystem level and breaks only
  string-matching consumers.
- A **leading** double (`//Users/you/Claude/…`) is rejected outright by the folder connector, so
  those mounts genuinely fail. Fix leading doubles first.

Rules for every rewrite:

- Replace **complete anchored strings**, old-full → new-full. Never replace a fragment.
- Assert before and after. In Python: `assert old in s` before; `assert old not in s` and no `//`
  after.
- Re-parse every JSON file you touch (`json.loads`) before writing it.
- Byte-compile every Python file you touch (`python3 -m py_compile`).
- Do one class of file at a time and verify between classes, so a mistake is attributable to a
  class rather than to the whole run.
- Order replacements so a later one cannot re-match an earlier one's output, and test that ordering
  before running it for real.

---

## The scheduled-task layer

For each task definition under `<CLAUDE_ROOT>/Scheduled/*/`, check three failure modes. A task can
have more than one at once, so check all three rather than stopping at the first.

- **Stale root in a path.** The obvious one, and the only one a grep finds.
- **Session-scoped paths.** A path of the form `/sessions/<name>/mnt/…` is valid only inside the
  session that created it. Hardcoded into a scheduled task it never resolves again. These
  accumulate, because they look correct in the session where they were written.
- **Dead targets.** The path is well-formed but the folder no longer exists — archived, renamed, or
  superseded. A move does not cause these; a move is when you find them.

Also check whether every MCP server a task depends on is still defined in
`claude_desktop_config.json`. `"mcpServers": {}` under a task that calls one is a break no path
sweep will catch.

**Retiring a task takes two steps.** The folder under `Scheduled/` holds only the task body; the
registration lives in `scheduled-tasks.json` (below). A session can move or repair the folder, but
it cannot safely rewrite the registration while the app is running. Move the folder **and** tell the
user to delete or disable that task in the app UI, by name. Moving the folder alone converts a
wrong-path failure into a missing-file failure, which is not an improvement.

---

## Artifacts: classify, do not hand-edit

Artifacts under `<CLAUDE_ROOT>/Artifacts/<id>/index.html` are self-contained pages with inline CSS,
JS and data. They are the one class where hunting for paths is usually the wrong question: a
well-built artifact contains no absolute filesystem paths at all, because it does not read the
filesystem at runtime. Path-shaped strings in one are typically display text, a build comment, or a
key into an in-memory bundle.

Ask what feeds it instead:

| Kind | How to tell | Effect of a move |
|---|---|---|
| **Connector-driven** | Calls an MCP tool at load time | Immune. Nothing to do. |
| **Remote-file-backed** | Downloads one file by title or a hardcoded file ID | Immune, but the hardcoded ID is a separate fragility worth reporting. |
| **Inert snapshot** | A `const DATA = {…}` literal or an inline JSON block baked in at build time | Immune, but frozen at whatever date it was generated. |

For inert snapshots the fix is never to edit the HTML. The real dependency is a chain:

```
artifact  ←  generator (a scheduled task or build script)  ←  project files
```

Repair the generator, re-run it, and let the artifact rebuild. A hand-edit to the HTML is silently
discarded by the next regeneration.

**The trap:** if the generator was itself broken by the move, the artifact keeps rendering old data
with no error anywhere — the page looks fine, and its data is weeks stale. So after repairing the
task layer, **re-run every generator task and confirm each artifact's own as-of date advances.**
That is the only check that proves the chain end to end.

Ignore `Artifacts/*/versions/*.html`; those are historical snapshots and rewriting them is covered
by *Do not rewrite history* below.

---

## Claude Code's own state, and why it is urgent

Claude Code keeps global state in `~/.claude/` and `~/.claude.json`, separately from the desktop
app's config. The part that matters is `~/.claude/projects/`, which holds one directory per project
**named after its absolute path with slashes replaced by dashes** — `/Users/you/Claude/Projects/Foo`
becomes `-Users-you-Claude-Projects-Foo`. `~/.claude.json` carries a matching path-keyed map of
per-project settings.

A move orphans both. Claude Code opens the project at its new path, finds no directory, and starts
with blank history, while the old transcripts sit invisible under a dead name.

**Do this early in the relocation, not last.** Orphaned directories can disappear on their own —
observed once within about ten minutes, with no action from the session and no hook that prunes
them. The mechanism was not established, so treat orphaned entries as garbage-collectable: the
history is on a clock from the moment the folder moves.

To rename without guessing the mangling scheme — non-ASCII characters are replaced, so a folder
named `Café Notes` becomes something like `Caf--Notes` — find an entry already under the current
root, use it to confirm the format, then substitute **only the differing path segment** and leave
every other character byte-identical. Check for collisions first; if a directory already exists
under the new name, merge the `.jsonl` files rather than overwriting.

Also sweep `~/.claude/backups/`, which holds `.claude.json` snapshots predating the move that will
reintroduce dead roots if restored. Rename them with a warning suffix rather than deleting.

`~/.claude` is not reachable through the folder picker. Add it to the Filesystem MCP server's
`allowed_directories` in the desktop UI, then **restart the app**: that list is read once at
startup, so the old one stays in force until it is.

---

## The desktop app's own state, and the catch-22

Under `~/Library/Application Support/Claude/local-agent-mode-sessions/<accountId>/<profileId>/` the
app keeps live state as plain JSON. Three files hold absolute paths:

- **`spaces.json`** — one entry per project: `name`, `description`, `instructions`,
  `folders[].path`, `id`, `updatedAt`. The folder mounts are what a move breaks. This is also the
  file `tasks/tune-instruction-layers.md` reads rather than asking the user to paste field texts.
- **`scheduled-tasks.json`** — `{"scheduledTasks": [...]}`, one entry per scheduled task: `id`
  (equal to the folder name under `Scheduled/`), `enabled`, `filePath` to the task body,
  `userSelectedFolders`, `spaceId`, optional `cronExpression` or `fireAt`, `lastRunAt`. **This is
  the live registration store, not a mirror** — deleting a task in the UI removes it from here
  within minutes.
- **`remote-session-spaces.json`** — per-session folder and memory state.
- A sibling `spaces copy.json`, if present, is a stale duplicate. Neutralise it; do not read it.

**The catch-22.** These files are rewritten wholesale from the app's in-memory state, so an edit
made while the app runs is silently discarded at the next flush. But the only remote write path into
that directory is the Filesystem MCP server, which is a desktop-app extension and stops with the
app. Quitting the app to make the edit safe removes the ability to make it, and the directory cannot
be connected as a project folder because it is a protected location.

So **do not attempt these edits from a session.** Write a shell script and hand it to the user, to
be run locally with the app quit. Make the script refuse to run if the app process is alive, back up
every file it touches, apply literal anchored replacements, re-parse each result as JSON and roll
back on failure, and print before/after counts.

While in `scheduled-tasks.json`, check two things a path sweep misses: tasks whose
`userSelectedFolders` name a project since archived or removed, and how many tasks actually carry a
`cronExpression` or `fireAt` at all. **A task with neither never fires on its own regardless of
`enabled`**, which users routinely assume otherwise. Prefer `"enabled": false` over deleting an
entry: it keeps `lastRunAt` and is reversible.

---

## The config layer

In `claude_desktop_config.json`:

- `coworkUserFilesPath` — the Claude data root. Wrong here and everything downstream is wrong.
- `mcpServers.*.args` — absolute script paths.
- `localAgentModeTrustedFolders`, `remoteFolderConsentMemory` — stale entries mean re-prompting.
- `remoteSessionFolderGrants` — per-session and historical. Stale entries are harmless; strip ones
  naming a root that no longer exists so they are not mistaken for live config.

Then the extension settings files (the Filesystem server's `allowed_directories` lives there) and
any per-project memory files the app keeps alongside its space state.

**`.bak` config files:** check them. If one carries a dead root, either delete it or rename it so
nobody restores a config that re-breaks the setup.

**Ignore** per-session upload and output snapshots under `local-agent-mode-sessions/`. They are
historical copies of a file as it was that day, not live config, and there can be dozens.

---

## Do not rewrite history

Dated audit reports, log entries and executed plans describe where things *were*. Rewriting them to
the new path is falsification, and it destroys the only record of what the old layout was — which is
exactly what you need if the move has to be undone.

If a bulk replace has already mangled them, restore the path that was true when the file was
written rather than substituting the current one.
