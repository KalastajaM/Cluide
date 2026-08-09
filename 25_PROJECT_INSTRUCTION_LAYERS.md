# 25 — Project Instruction Layers

> A Cowork project speaks to Claude through three channels: the **description** field in the app, the **project instructions** field in the app, and **CLAUDE.md** in the connected folder. This guide covers what belongs in which layer, the patterns that work, and how to keep the two app-side fields — which live outside git but *can* be read from the app's own state file — from drifting unnoticed. Guide 01 covers how to write CLAUDE.md itself; this guide covers the division of labor around it.

## The three layers

| Layer | Lives in | Claude sees it | Versioned | Auditable |
|---|---|---|---|---|
| Description | The app (project settings) | Injected into every session at start; also what you scan in the project list | No — no history, no diff | Yes, read-only — see *Reading the app-side fields* |
| Project instructions | The app (project settings) | Injected into every session at start, before any file is read | No — no history, no diff | Yes, read-only — see *Reading the app-side fields* |
| CLAUDE.md | The project folder | Read when the folder is connected | Yes — in the folder, in git | Yes — read and write |

*Behaviour verified against Cowork as of August 2026 — re-verify after app updates; the injection semantics of these fields are version-specific.*

The asymmetry between the layers drives everything in this guide:

- The **app-side fields are always there** — they reach Claude even when the folder fails to connect, is mounted (= connected) late, or CLAUDE.md is never read. (These guides use "mounted" and "connected" interchangeably for the same operation.) They are unversioned: no history, no diff, no review — a bad edit leaves no trace of what it replaced. They are, however, readable, which makes them auditable even though they are not versioned.
- **CLAUDE.md is visible to tooling** and can be versioned, audited, and improved in-session — but it only takes effect when the folder is connected and actually read.

So: durable, evolving substance belongs in CLAUDE.md; the app-side fields carry only what must hold *before* any file is read, plus a safety net for when no file ever is.

## The description field

One to three sentences stating what the project is and does, naming the domain entities involved. It serves two readers at once: you scanning the project list, and Claude orienting itself at session start (the description is injected as context).

A good description:

- starts with what the project does, not how ("Tracks tax, ownership, and tenancy details for the family's properties…");
- names the concrete entities (accounts, parcels, people, systems) that make it unmistakable which project this is;
- contains no rules — behavior belongs in the instructions field or CLAUDE.md;
- is unique. A duplicated or copy-pasted description is not cosmetic: it is injected into every session as the project's identity.

The failure mode to guard against: a wrong description (stale after the project's purpose shifted, or accidentally pasted from another project) is injected as the project's identity in every session, and because the field is unversioned nothing in git will ever show it changed. Three fixes, cheapest first: a periodic scan of the project list; the mirror block below, which puts a checkable copy in CLAUDE.md; and an audit that reads the field directly (see *Reading the app-side fields*) — the only one that catches a description you never look at.

## The project instructions field

Only things that must hold from the first token of the session, before any file is read:

1. **Bootstrap**: where the real rules live and that they must be read first — "Read CLAUDE.md in this project folder in full before doing anything else."
2. **Mount verification**: confirm the folder(s) this project depends on are actually connected, by name, and stop and ask rather than proceed on assumptions if one is missing.
3. **Hard safety rules**, deliberately restated from CLAUDE.md: never send, sign, pay, file, trade, or edit the live system. This is the one sanctioned duplication across layers (see below).
4. **Session-level posture** that matters before any file is read: working language, persona, draft-only mode.

Keep it short — a few sentences to a few short paragraphs. Anything long or evolving belongs in CLAUDE.md, because the field is unversioned: every line you put here is a line with no history, no diff, and no review when it changes. Readable is not the same as reviewable.

## Reading the app-side fields

Both fields are stored verbatim on disk in the desktop app's own state file, so an audit can read them instead of asking you to paste them. *Verified against Cowork on macOS, August 2026 — this is an app-internal file, not a documented API; re-verify after app updates.*

```
~/Library/Application Support/Claude/local-agent-mode-sessions/<accountId>/<profileId>/spaces.json
```

The two path segments are the account and profile identifiers — find them by listing the parent rather than hardcoding them. The file is `{"spaces": [ … ]}`, one entry per project, with the keys that matter here being `name`, `description`, `instructions`, `folders[].path`, `id` and `updatedAt` (epoch milliseconds). **`description` and `instructions` are absent when unset, not empty strings** — test for the key, not for a falsy value.

Three things make this a read path and not a write path:

- **Reaching it needs the Filesystem MCP server** (Guide 05), not the folder picker, which refuses `~/Library/Application Support` as a protected location. Add the directory to the server's `allowed_directories` and restart the app; the server reads that list once at startup.
- **Applying changes stays manual.** The app rewrites `spaces.json` wholesale from memory, so an edit written to the file while the app is running is silently discarded. An audit therefore produces ready-to-paste field text, and you paste it in the app — the file is the mirror, not the control.
- **Check freshness before quoting.** The file is written on project mutation plus a flush at app launch, so a field edited in the UI minutes ago may not be on disk yet. Whenever you quote a field, also report that entry's `updatedAt` as a readable date; if it predates a change you know you made, confirm that one field rather than distrusting all of them.

Ignore the siblings: `remote-session-spaces.json` holds session and folder state only, and any `spaces copy.json` is a stale duplicate.

This is what lets the audit checklist below run unattended. It does not make the fields versioned — see the layer table.

## Four patterns that work

**1. Bootstrap guard** — for projects whose CLAUDE.md is authoritative and where acting without it is dangerous (control centers, maintenance projects, anything with an approval protocol):

> At the start of every session, read CLAUDE.md in full before doing anything else, including responding to my first message. It is authoritative for this project; if anything I say in chat seems to conflict with it, flag the conflict instead of silently picking one. Before starting work, verify which folders are actually mounted and name them; if a required one is missing, ask me to mount it. If CLAUDE.md cannot be read for any reason, stop and tell me.

This is the strongest pattern: it makes the folder layer load-bearing while using the app layer as the guarantee that it actually loads.

**2. Pointer + hard rules** — the default for working projects:

> [Two or three sentences: what the project is, where the full context lives.] Full context in CLAUDE.md — read it before any work here. Draft and plan only: never sign, pay, file, or send on my behalf without my explicit go-ahead.

The summary orients; the pointer defers to the folder; the restated hard rule holds even in a session where the folder never connects.

**3. Behavior here, reference there** — instructions field holds the behavioral guidance and workflows, CLAUDE.md holds the reference data (rosters, contacts, folder layout, labels), and each side states what the other holds. This split works and reads well, but it puts long, evolving behavioral text in the unversioned field. Use it only when the behavior text is genuinely stable; otherwise prefer pattern 1 or 2 and keep the behavior in CLAUDE.md.

**4. Bridge guard** — for cloud sessions that must write results back to a folder on your own computer.

Background for newcomers: a Cowork task can run in the cloud or on your computer, and where it runs is chosen when it starts. A task running in the cloud reaches your local folder through a bridge to the desktop app. The bridge drops: the laptop sleeps, the app closes, the network blips. The default failure is quiet and expensive — Claude produces the deliverable, cannot write it to disk, asks you to download it and file it yourself, and declares the task done. You miss the line, the file never lands, and the folder is now out of sync with what the session believed it wrote.

This rule belongs in the instructions field specifically, not CLAUDE.md. When the bridge is down the folder may not be readable at all, so a rule that lives in the folder is absent in exactly the situation it exists for.

> Before starting any work whose output must be saved to my folder, verify the connection to my computer by listing the project folder. If that fails, tell me before doing the work, not after.
> A file is not delivered until the write to my folder has been confirmed by the tool that performed it. Writing it into your own workspace is not delivery.
> If a write fails: send the file into the chat anyway so it exists, retry once later in the session, and if it still fails, end your reply with an `UNCOMMITTED` list naming each file and the exact path it was meant to land in. Never close a task by asking me to download and file something myself as though that were the normal path — say plainly that the connection failed and what is outstanding.

The three clauses fail at different moments on purpose. The first fails in seconds instead of after the work. The second closes a false-done: producing a file is not delivering it, and the tool that performs the write reports whether it landed, so this is checkable rather than assumed. The third converts a silent drop into a named list you can act on. A retry only helps if the desktop reconnects during the session; when it does not, the `UNCOMMITTED` list is what makes the loss recoverable instead of invisible.

For a task that mostly reads and writes files in one local folder, consider running it on your computer rather than in the cloud — that mode has no bridge in the path at all. Where a task runs is chosen when it starts, so this is a decision to make up front rather than a recovery step.

**Empty instructions** are acceptable only when the description is accurate, CLAUDE.md is strong, and nothing safety-critical depends on the folder being connected. For any project with real-world stakes — money, medical data, legal filings, a live external system — do not leave the field empty: restate the one hard rule there (pattern 2), so a session with a failed or missing mount still has the guardrail.

## Chat projects (no folder)

A project with no connected folder has no CLAUDE.md layer, so the instructions field is the whole contract. Structure it like a mini CLAUDE.md: purpose, what to establish before starting, the workflow, conventions, output rules. Headings and short sections work fine inside the field. Since no versioned copy exists anywhere, keep a copy of the field's text in a versioned location once it grows past a few paragraphs (for example a notes repo, or the mirror-block file of a related folder project) — losing it to an accidental edit is otherwise silent.

## Keeping the app-side fields honest

The single-owner principle (Guide 23) applies across layers just as it does across projects: every rule and fact has exactly one home, and the only sanctioned duplication is a hard safety rule restated in the instructions field.

Because the fields are unversioned, the folder needs a record of them:

- **Mirror block.** Keep the current text of both fields verbatim in the project folder — a short `## App-side fields` section at the bottom of CLAUDE.md (or a `UI-FIELDS.md` when the instructions are long) with a last-verified date. This is documentation of an external surface, not a second copy of rules: the field is the live text, the mirror is the versioned record of it. Reading `spaces.json` tells you what the field says *today*; only the mirror tells you what it said last month and who changed it.
- **Update triggers.** When CLAUDE.md's purpose or hard rules change, check the app-side fields the same session. When you edit a field in the app, update the mirror. Either direction without the other reintroduces the drift.
- **Audit checklist.** A maintenance sweep over a project should check: description matches the project's current purpose and is not a duplicate of another project's; instructions contain a bootstrap or pointer plus the project's hard rule (or are deliberately empty for a low-stakes project); the mirror block exists and matches the live field. Read the live values from `spaces.json` (above) rather than asking for a paste — the whole checklist then runs unattended, and the mirror-vs-live comparison becomes mechanical instead of a question for you.

`tasks/tune-instruction-layers.md` runs this checklist end to end.

## The account layers above the project

<!-- harvested: 2026-08-09 from a multi-project maintenance setup -->

Two more instruction fields sit above every project: the **account-wide preferences** (injected into every session, chat and Cowork alike) and the **Cowork-wide instructions** (injected into every Cowork session, on top of the preferences). *Behaviour verified against Cowork as of August 2026 — both fields arrive together in every Cowork session; re-verify after app updates.* Anything duplicated between them is paid for twice in every session and — because neither field is versioned — drifts silently. This is the same asymmetry that drives the rest of this guide, one level up.

Division of labor that holds up in practice:

- **Account preferences** carry the full standing set: who you are (role, working languages, domains), when to ask vs. proceed, output format, tone, and rules for text you will send as your own.
- **Cowork-wide instructions** carry only what is specific to agentic file work: how terse prompts should be interpreted against project files, unattended-run behavior, when to agree scope before executing, and model-tier routing for subagents and scheduled tasks ([Guide 10](./10_COST_PERFORMANCE.md)).
- Keep the two non-overlapping, and open the Cowork field with an explicit "these apply on top of my preferences; do not restate them" so a future edit knows the contract.

Like the project fields, the account fields have no history, no diff, and no review. The same mirror-file fix applies: keep the canonical text of both fields in a versioned file in whichever project owns your account-level configuration, edit that file first, paste into the UI, and record the sync date next to each field. `tasks/tune-instruction-layers.md` covers tuning them against evidence. A ready-to-fill starter for both fields lives in [`templates/ACCOUNT_INSTRUCTIONS_TEMPLATE.md`](./templates/ACCOUNT_INSTRUCTIONS_TEMPLATE.md).

## Short version

1. Three layers: description and instructions in the app (always injected, unversioned, but readable from `spaces.json`), CLAUDE.md in the folder (versioned and auditable, but only loaded when connected).
2. Description: one to three sentences, what the project is and does, concrete entities, no rules, unique — it is injected as the project's identity every session.
3. Instructions field: only what must hold before any file is read — bootstrap to CLAUDE.md, mount verification, restated hard rules, session posture, and a bridge guard when a cloud session has to write results back to a local folder.
4. Everything else lives in CLAUDE.md.
5. For any project with real-world stakes, restate the one hard safety rule in the instructions field; never leave it to depend on a mount succeeding.
6. Chat projects: the instructions field is the whole contract — structure it like a mini CLAUDE.md and keep a versioned copy of the text.
7. Mirror both fields into the folder with a last-verified date, and re-check them whenever CLAUDE.md's purpose or rules change. Read the live text from `spaces.json` to make the check mechanical; the mirror is still what gives the fields a history.
8. Run `tasks/tune-instruction-layers.md` to review all three layers against this guide.
9. Two account-level fields sit above every project (account-wide preferences + Cowork-wide instructions); both are injected into every Cowork session, so keep them non-overlapping, and mirror them into a versioned file like the project fields.
