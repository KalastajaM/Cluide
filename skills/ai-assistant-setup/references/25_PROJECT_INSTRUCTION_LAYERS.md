# 25 — Project Instruction Layers

> A Cowork project speaks to Claude through three channels: the **description** field in the app, the **project instructions** field in the app, and **CLAUDE.md** in the connected folder. This guide covers what belongs in which layer, the patterns that work, and how to keep the two app-side fields — which no audit or git history can see — from drifting unnoticed. Guide 01 covers how to write CLAUDE.md itself; this guide covers the division of labor around it.

## The three layers

| Layer | Lives in | Claude sees it | Versioned / auditable |
|---|---|---|---|
| Description | The app (project settings) | Injected into every session at start; also what you scan in the project list | No — invisible to git and file-based audits |
| Project instructions | The app (project settings) | Injected into every session at start, before any file is read | No — invisible to git and file-based audits |
| CLAUDE.md | The project folder | Read when the folder is connected | Yes — in the folder, in git, visible to audits |

The asymmetry between the layers drives everything in this guide:

- The **app-side fields are always there** — they reach Claude even when the folder fails to connect, is mounted late, or CLAUDE.md is never read. But they are invisible to every file-based process: git, maintenance audits, cross-project consistency checks, and Claude itself when working on the folder in another context.
- **CLAUDE.md is visible to tooling** and can be versioned, audited, and improved in-session — but it only takes effect when the folder is connected and actually read.

So: durable, evolving substance belongs in CLAUDE.md; the app-side fields carry only what must hold *before* any file is read, plus a safety net for when no file ever is.

## The description field

One to three sentences stating what the project is and does, naming the domain entities involved. It serves two readers at once: you scanning the project list, and Claude orienting itself at session start (the description is injected as context).

A good description:

- starts with what the project does, not how ("Tracks tax, ownership, and tenancy details for the family's properties…");
- names the concrete entities (accounts, parcels, people, systems) that make it unmistakable which project this is;
- contains no rules — behavior belongs in the instructions field or CLAUDE.md;
- is unique. A duplicated or copy-pasted description is not cosmetic: it is injected into every session as the project's identity.

The failure mode to guard against: because the field lives outside every audit, a wrong description (stale after the project's purpose shifted, or accidentally pasted from another project) is injected as the project's identity in every session and nothing will ever flag it. The mirror block below is the systematic fix; a periodic manual scan of the project list is the cheap one.

## The project instructions field

Only things that must hold from the first token of the session, before any file is read:

1. **Bootstrap**: where the real rules live and that they must be read first — "Read CLAUDE.md in this project folder in full before doing anything else."
2. **Mount verification**: confirm the folder(s) this project depends on are actually connected, by name, and stop and ask rather than proceed on assumptions if one is missing.
3. **Hard safety rules**, deliberately restated from CLAUDE.md: never send, sign, pay, file, trade, or edit the live system. This is the one sanctioned duplication across layers (see below).
4. **Session-level posture** that matters before any file is read: working language, persona, draft-only mode.

Keep it short — a few sentences to a few short paragraphs. Anything long or evolving belongs in CLAUDE.md, because the field is invisible to git and audits: every line you put here is a line no tooling can check.

## Three patterns that work

**1. Bootstrap guard** — for projects whose CLAUDE.md is authoritative and where acting without it is dangerous (control centers, maintenance projects, anything with an approval protocol):

> At the start of every session, read CLAUDE.md in full before doing anything else, including responding to my first message. It is authoritative for this project; if anything I say in chat seems to conflict with it, flag the conflict instead of silently picking one. Before starting work, verify which folders are actually mounted and name them; if a required one is missing, ask me to mount it. If CLAUDE.md cannot be read for any reason, stop and tell me.

This is the strongest pattern: it makes the folder layer load-bearing while using the app layer as the guarantee that it actually loads.

**2. Pointer + hard rules** — the default for working projects:

> [Two or three sentences: what the project is, where the full context lives.] Full context in CLAUDE.md — read it before any work here. Draft and plan only: never sign, pay, file, or send on my behalf without my explicit go-ahead.

The summary orients; the pointer defers to the folder; the restated hard rule holds even in a session where the folder never connects.

**3. Behavior here, reference there** — instructions field holds the behavioral guidance and workflows, CLAUDE.md holds the reference data (rosters, contacts, folder layout, labels), and each side states what the other holds. This split works and reads well, but it puts long, evolving behavioral text in the unversioned field. Use it only when the behavior text is genuinely stable; otherwise prefer pattern 1 or 2 and keep the behavior in CLAUDE.md.

**Empty instructions** are acceptable only when the description is accurate, CLAUDE.md is strong, and nothing safety-critical depends on the folder being connected. For any project with real-world stakes — money, medical data, legal filings, a live external system — do not leave the field empty: restate the one hard rule there (pattern 2), so a session with a failed or missing mount still has the guardrail.

## Chat projects (no folder)

A project with no connected folder has no CLAUDE.md layer, so the instructions field is the whole contract. Structure it like a mini CLAUDE.md: purpose, what to establish before starting, the workflow, conventions, output rules. Headings and short sections work fine inside the field. Since no versioned copy exists anywhere, keep a copy of the field's text in a versioned location once it grows past a few paragraphs — losing it to an accidental edit is otherwise silent.

## Keeping the app-side fields honest

The single-owner principle (Guide 23) applies across layers just as it does across projects: every rule and fact has exactly one home, and the only sanctioned duplication is a hard safety rule restated in the instructions field.

Because the fields live outside the folder, the folder needs a record of them:

- **Mirror block.** Keep the current text of both fields verbatim in the project folder — a short `## App-side fields` section at the bottom of CLAUDE.md (or a `UI-FIELDS.md` when the instructions are long) with a last-verified date. This is documentation of an external surface, not a second copy of rules: the field is the live text, the mirror is what lets an audit see it.
- **Update triggers.** When CLAUDE.md's purpose or hard rules change, check the app-side fields the same session. When you edit a field in the app, update the mirror. Either direction without the other reintroduces the drift.
- **Audit checklist.** A maintenance sweep over a project should check: description matches the project's current purpose and is not a duplicate of another project's; instructions contain a bootstrap or pointer plus the project's hard rule (or are deliberately empty for a low-stakes project); the mirror block exists and matches what the app shows (this last check needs you, since only you can see the app).

## Short version

1. Three layers: description and instructions in the app (always injected, never auditable), CLAUDE.md in the folder (auditable, but only loaded when connected).
2. Description: one to three sentences, what the project is and does, concrete entities, no rules, unique — it is injected as the project's identity every session.
3. Instructions field: only what must hold before any file is read — bootstrap to CLAUDE.md, mount verification, restated hard rules, session posture.
4. Everything else lives in CLAUDE.md.
5. For any project with real-world stakes, restate the one hard safety rule in the instructions field; never leave it to depend on a mount succeeding.
6. Chat projects: the instructions field is the whole contract — structure it like a mini CLAUDE.md and keep a versioned copy of the text.
7. Mirror both fields into the folder with a last-verified date, and re-check them whenever CLAUDE.md's purpose or rules change — otherwise no audit can ever catch them drifting.
