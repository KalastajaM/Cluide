# 24 — Project Folder Structure

> How to lay out a single project's folders so Claude always knows where things live, and how to keep that layout from rotting as the project grows. For structure *across* several projects, see Guide 23; this guide is about one project's internal shape.

A project's folder layout is an interface Claude reads every session. When it is predictable, Claude finds the right file on the first try and puts new files where they belong. When it drifts (outputs piling at the root, three versions of the same document, a `notes` folder that became a junk drawer), Claude wastes context hunting and starts guessing. Structure is cheap to get right early and expensive to retrofit, so it is worth a small standard.

## The standard layout

Every project, whatever its purpose, wants a home for each of these five kinds of thing. The names matter less than having exactly one obvious place for each:

- **Instructions** at the root: `CLAUDE.md` (how Claude should behave here) and, if a human will open the project, `README.md`. These are read first.
- **Source of truth**: the canonical data or working files the project is actually about. Markdown is the source of truth; see Guide 19.
- **Generated outputs**: finished deliverables (Word, PPT, PDF, exports) that are produced *from* the source of truth. These live in their own home, not scattered at the root, because they are regenerable and should never be confused with the source.
- **Scratch / working files**: transient in-progress material, clearly separated so it does not masquerade as a deliverable.
- **Archive**: old material kept for reference, in a folder that is never read back (see naming below).

Two concrete starting points ship with Cluide: `PROJECT_TEMPLATE/` for a lean assistant-style project (`CLAUDE.md` + `Profile/` + `Knowledge/`), and `PMO_TEMPLATE/` for a richer project with deliverables and registers. Copy whichever is closer rather than inventing a layout.

## Core principles

- **One obvious home per file kind.** Before creating a file, there should be no doubt where it goes. If there is doubt, the layout is missing a folder or you are about to make a junk drawer.
- **Separate definitions from generated outputs.** The thing you edit and the thing you export are different categories. Keep them in different folders so a regenerated PDF never overwrites a source, and so cleanup can safely target outputs.
- **One folder per tracked entity, same artifact set in each.** When a project tracks many like items (properties, cases, applications, deals), give each its own folder holding the same named files, created from a template and indexed by a central tracker. The tracker is the index; the folder is the workspace. See Best Practice 21 in Guide 16.
- **Document the layout in CLAUDE.md as a file map.** List the folders and what each holds. The strongest version adds a "where to look / where to update" split so Claude knows which files are read-only inputs and which it may append to. `PMO_TEMPLATE/PROJECT_GUIDE.md` shows this pattern.
- **Mark file-access tiers.** Note what Claude should auto-read every session, what it should read only on demand, and what it should never touch (raw source data, archives, secrets). Guide 01 covers the tiers.

## Standard formats for recurring files

Folders give each file a predictable home; a standard format gives each recurring *kind* of file a predictable shape. When a project has a file type that recurs (task files, registers, per-entity briefs, meeting or decision logs, status reports), define one format for it and hold every instance to that format. The payoff mirrors consistent folders: Claude and any human can predict where a fact sits, produce a new instance without improvising, and see at a glance when one has drifted.

Capture the format one of two ways:

- **A template file** when instances get created often. A copy-paste skeleton with the sections and placeholders already in place (this is what the `templates/` folder is for). Creating a new instance becomes copy, rename, fill in, rather than reinvention.
- **A documented "Format" section** when a template does not fit but the shape still matters. A short spec placed where those files live, listing the sections each file must contain and what belongs in each. Cluide's `tasks/README.md` does this for task files: it lists the required sections rather than shipping a blank template.

Keep the format definition in one place and point to it; do not restate it inside every file. When the format itself changes, update the single definition and bring existing files into line (`reorganize-project` helps when that means reshaping or moving many of them).

## Keeping it clean as it grows

Messiness is not one event; it is a slow accumulation of small "I will sort it later" decisions. These conventions stop it:

- **Outputs never pile at the root.** Route them to a dedicated outputs home (or the relevant entity folder) the moment there is more than one.
- **Archive, do not delete.** Move superseded material into an archive folder rather than deleting it, and never read from it. Prefix such folders `[ARCHIVE]` (or use a single `_archive/`) so both you and Claude skip them by default.
- **Name versions consistently.** While there is one copy, use a plain name. Once a file goes through versioned iterations, mark the active one with a `_LATEST` suffix and move older revisions into an archive folder. Use dates (`YYYYMMDD`) for point-in-time snapshots. Pick one casing convention and hold it.
- **Split a file when it grows.** A profile or knowledge file past roughly 150 lines should split into topic files, with the index updated. A folder holding dozens of mixed files should gain subfolders by kind or entity.
- **No duplicated facts.** If the same fact would live in two files, keep it in one and link from the other. Duplication is how a project starts contradicting itself.
- **Tidy on a cadence, not on a crisis.** A short periodic pass catches drift while it is one file out of place. To reorganize a project that has already drifted, use the `reorganize-project` task, which takes a restore point first, then moves files and rewires every reference without breaking the project.

## When one project is not enough

If the layout is straining because the project is really two purposes sharing a folder, the fix is not another subfolder but a split into linked projects. Guide 23 covers when and how.

## Short version

1. Give every file kind one obvious home: instructions, source of truth, generated outputs, scratch, archive.
2. Copy a template (`PROJECT_TEMPLATE` or `PMO_TEMPLATE`) instead of inventing a layout.
3. Keep generated outputs out of the root and separate from their sources.
4. One folder per tracked entity, same artifact set, indexed by a central tracker.
5. Document the layout as a file map in `CLAUDE.md`, ideally with a read-only vs updatable column.
6. Give each recurring file kind a standard format too, as a template or a documented Format section, kept in one place.
7. Archive (never delete) into `[ARCHIVE]`/`_archive/` folders that are never read back; mark the active version `_LATEST`.
8. Split oversized files and junk-drawer folders early; run `reorganize-project` to fix a project that has already drifted.
