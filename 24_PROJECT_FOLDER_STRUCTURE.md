# 24 — Project Folder Structure

> How to lay out a single project's folders so Claude always knows where things live, and how to keep that layout from rotting as the project grows. For structure *across* several projects, see Guide 23; for the note layer sitting above all of them, see Guide 28. This guide is about one project's internal shape.

A project's folder layout is an interface Claude reads every session. When it is predictable, Claude finds the right file on the first try and puts new files where they belong. When it drifts (outputs piling at the root, three versions of the same document, a `notes` folder that became a junk drawer), Claude wastes context hunting and starts guessing. Structure is cheap to get right early and expensive to retrofit, so it is worth a small standard.

## The standard layout

Every project, whatever its purpose, wants a home for each of these kinds of thing. The names matter less than having exactly one obvious place for each:

- **Instructions** at the root: `CLAUDE.md` (how Claude should behave here) and, if a human will open the project, `README.md`. These are read first.
- **Source of truth**: the canonical data or working files the project is actually about. Markdown is the source of truth; see Guide 19.
- **Generated outputs**: finished deliverables (Word, PPT, PDF, exports) that are produced *from* the source of truth. These live in their own home, not scattered at the root, because they are regenerable and should never be confused with the source.
- **Scratch / working files**: transient in-progress material, clearly separated so it does not masquerade as a deliverable.
- **Archive**: old material kept for reference, in a folder that is never read back (see naming below).
- **Intake**, when material reaches the project outside a chat: one `incoming/` folder where new documents land before anyone has decided where they belong. The only conditional home on this list, and the only one whose correct steady state is empty. See the next section.

Cluide ships four templates (see `00_INDEX.md` for all of them); two are project-layout starting points relevant here: `PROJECT_TEMPLATE/` for a lean assistant-style project (`CLAUDE.md` + `Profile/` + `Knowledge/`), and `PMO_TEMPLATE/` for a richer project with deliverables and registers. Copy whichever is closer rather than inventing a layout.

## Intake: the `incoming/` folder

A project whose material only ever arrives through chat does not need this folder. You attach a file, Claude reads it and writes it to the right home in the same turn, and an intake folder is just a stop the file passes through. It earns its place when material arrives with no session attached to it: scans and downloads, photos from a phone, an email export, a family member or colleague dropping documents into a shared folder, a scheduled task fetching statements. Those files land somewhere. Without a named home, the somewhere is the project root.

Treat it as a queue rather than a home. Four rules keep it one:

- **`incoming/` is emptied, not managed.** Permanent residents mean it has quietly become a `resources/` folder with a misleading name, and once that happens nobody trusts it enough to drop anything in. Clear it on a cadence you will actually keep — weekly for most projects, or at the start of the next session that opens the project.
- **Filing is proposed, not silent.** Claude is moving *your* files, and a wrong destination is expensive to notice three months later. Have it list what it found and where each item would go before it moves anything, or let it move and leave a short manifest of source and destination. Either works; doing neither is how a document goes missing.
- **Nothing is deleted out of `incoming/`.** Material that turns out not to belong goes to the archive like everything else in the project. Deletion is a decision to make later, with the file in front of you.
- **File by content, not by filename.** Routing inbound material through Claude is worth doing precisely because `IMG_4821.pdf` and `Scan_2026-08-14.pdf` say nothing. Claude opens the file, works out what it is, and renames it to the project's convention on the way in. When it cannot tell, the item stays in `incoming/` with a question attached rather than being filed on a guess.

Then say in `CLAUDE.md` what should happen to the folder: which destinations are legal, whether Claude may file without asking or must propose first, and whether it checks the folder every session or only when told. An intake folder nobody has told Claude to look at is a folder that fills up.

Casing follows whatever convention the project already uses — `Incoming/` in a project whose folders are capitalised, `incoming/` in one whose folders are not. The Cluide project templates ship the capitalised form to match their existing layout.

**This is not the second brain's `inbox/` (Guide 28), even though the discipline is nearly identical.** `incoming/` holds material whose destination is inside *this* project, where the only open question is which folder. The second brain's `inbox/` holds material whose destination is your whole working life, and triage there decides whether the item survives at all. If you run both, keeping the two names distinct is worth the small effort, so that "put it in the inbox" has exactly one meaning.

## Core principles

- **One obvious home per file kind.** Before creating a file, there should be no doubt where it goes. If there is doubt, the layout is missing a folder or you are about to make a junk drawer.
- **Separate definitions from generated outputs.** The thing you edit and the thing you export are different categories. Keep them in different folders so a regenerated PDF never overwrites a source, and so cleanup can safely target outputs.
- **One folder per tracked entity, same artifact set in each.** When a project tracks many like items (properties, cases, applications, deals), give each its own folder holding the same named files, created from a template and indexed by a central tracker. The tracker is the index; the folder is the workspace. See the "one folder per tracked entity, the same artifact set in each" practice in Guide 16 (item 21 of its Short Version).
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

1. Give every file kind one obvious home: instructions, source of truth, generated outputs, scratch, archive — plus intake, if material reaches the project outside a chat.
2. Copy a template (`PROJECT_TEMPLATE` or `PMO_TEMPLATE`) instead of inventing a layout.
3. Keep generated outputs out of the root and separate from their sources.
4. One folder per tracked entity, same artifact set, indexed by a central tracker.
5. Document the layout as a file map in `CLAUDE.md`, ideally with a read-only vs updatable column.
6. Give each recurring file kind a standard format too, as a template or a documented Format section, kept in one place.
7. Archive (never delete) into `[ARCHIVE]`/`_archive/` folders that are never read back; mark the active version `_LATEST`.
8. Split oversized files and junk-drawer folders early; run `reorganize-project` to fix a project that has already drifted.
9. Route inbound material through one `incoming/` folder: file by content, propose destinations before moving, archive rather than delete, and keep it empty.
