# 25 — Project Instruction Layers

> A project needs an identity, instructions available before sources are read, and an authored policy. These layers differ across Cowork, ChatGPT projects and Codex. Keep the shared contract versioned and verify each native entry point; a mirror records configuration but does not apply it.

## The three layers

| Layer | Cowork / conversational Claude | ChatGPT uploaded-source project | Codex repository session |
|---|---|---|---|
| Identity | Native project name/description where exposed | Native project identity and project instructions | Selected repository/workspace and task |
| Bootstrap | Project instructions request the accessible policy | Project instructions name the uploaded/connected policy revision | Native `AGENTS.md` discovery; inspect overrides |
| Authored policy | Shared `AGENTS.md` via `CLAUDE.md` adapter or explicit source read | Authored policy supplied as a project source; refresh manually | Shared root `AGENTS.md` and scoped descendant instructions |
| Native continuity | Platform's own memory, sessions and settings | Platform's own memory, chats and source access | Runtime-local state and settings |

The invariant is one authored policy, not one universal loader. App fields can provide a bootstrap when files are unavailable; repository files provide reviewable history. Never assume a project description is injected into another product's prompt or that every app has the same fields.

The Cowork-specific examples below illustrate the pattern. For ChatGPT, use its project instructions and accessible sources; for Codex, use the native instruction chain. See [Guide 01](./01_CLAUDE_MD.md) for the contract's contents and [Guide 35](./35_DUAL_PLATFORM_PROJECTS.md) for current product facts. Official loading/source documentation checked 2026-09-14: [OpenAI projects](https://learn.chatgpt.com/docs/projects), [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude memory and instructions](https://code.claude.com/docs/en/memory).

---

## The description field

One to three sentences stating what the project is and does, naming the domain entities involved. It helps you recognize the project; on surfaces that provide it to the assistant, it also orients the session. Verify that behaviour per product.

A good description:

- starts with what the project does, not how ("Tracks tax, ownership, and tenancy details for the family's properties…");
- names the concrete entities (accounts, parcels, people, systems) that make it unmistakable which project this is;
- contains no rules — behavior belongs in the instructions field or CLAUDE.md;
- is unique. A duplicated or copy-pasted description is not cosmetic: it can misidentify the project wherever the product supplies it as context.
- fits the actual field limit shown by the current product; do not copy a Cowork character limit into ChatGPT or Codex guidance.

The failure mode to guard against: a wrong description (stale after the project's purpose shifted, or accidentally pasted from another project) can supply a stale project identity, and because the field is unversioned nothing in git will ever show it changed. Three fixes, cheapest first: a periodic scan of the project list; the mirror block below, which puts a checkable copy in CLAUDE.md; and an audit that reads the field directly (see *Reading the app-side fields*) — the only one that catches a description you never look at.

## The project instructions field

Only things that must hold from the first token of the session, before any file is read:

1. **Bootstrap**: where the real rules live and that they must be read first — "Read CLAUDE.md in this project folder in full before doing anything else."
2. **Mount verification**: confirm the folder(s) this project depends on are actually connected, by name, and stop and ask rather than proceed on assumptions if one is missing.
3. **Hard safety rules**, deliberately restated from CLAUDE.md: never send, sign, pay, file, trade, or edit the live system. This is the one sanctioned duplication across layers (see below).
4. **Session-level posture** that matters before any file is read: working language, persona, draft-only mode.

Keep it short — a few sentences to a few short paragraphs. Anything long or evolving belongs in CLAUDE.md, because the field is unversioned: every line you put here is a line with no history, no diff, and no review when it changes. Readable is not the same as reviewable.

## Reading the app-side fields

Read the fields through the current app UI or a documented connector when available. Record the product, project/account identity, observed text and verification date. If the host cannot inspect a field, mark it **unverified** and provide ready-to-paste text; do not claim it was applied.

Earlier Cowork workflows inspected a macOS `spaces.json` cache under the Claude application-support directory. That is an internal implementation detail, not a shared configuration API or an OpenAI path. A stale cache is not evidence of the current UI value, and writing it can be overwritten by the app. Do not make this path a required audit dependency or expand filesystem grants just to reach it.

Use a supported UI or tool to apply changes. Afterward, read back the actual fields and run a fresh-session check. Keep separate mirror entries for Claude, ChatGPT and local Codex setup; missing access on one side does not invalidate a check on another.

---

## Four patterns that work

**1. Bootstrap guard** — for projects whose CLAUDE.md is authoritative and where acting without it is dangerous (control centers, maintenance projects, anything with an approval protocol):

> At the start of every session, read CLAUDE.md in full before doing anything else, including responding to my first message. It is authoritative for this project; if anything I say in chat seems to conflict with it, flag the conflict instead of silently picking one. Before starting work, verify which folders are actually mounted and name them; if a required one is missing, ask me to mount it. If CLAUDE.md cannot be read for any reason, stop and tell me.

This is the strongest pattern: it makes the folder layer load-bearing while using the app layer to request loading, with a fresh-session check to verify it.

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

## OpenAI Bootstrap and Source Refresh

For a ChatGPT project, a short project-instructions bootstrap can say:

> Read the supplied `AGENTS.md` policy and the source revision record before using project material. Identify missing sources before making claims about them. Follow the project output contract and state whether a result was only drafted, delivered as a file, or written to an authorized destination.

Upload the policy and only the sources needed by this project. Record the commit or dated revision in `UI-FIELDS.md`. After changing the authored policy, replace the uploaded copy, read back the project instructions and test a fresh chat against a prewritten expected result.

For Codex, the bootstrap is the repository instruction chain, not a ChatGPT project field. Open the intended directory, inspect `AGENTS.override.md` files that may supersede `AGENTS.md`, and start a fresh session after instruction changes. Keep account-level Codex defaults and project rules non-overlapping. A ChatGPT project's native memory is not proof that a local Codex session received its instructions.

Mirror example:

```text
Surface: ChatGPT uploaded-source project
Project: <name>
Policy revision: <commit or date>
Instructions: <verbatim applied text>
Applied/read-back date: <date, or not applied>
Fresh-session result: <pass / fail / untested, with evidence>
```

---

## Chat projects (no folder)

A project without a connected folder can still have uploaded policy sources. The instructions field must bootstrap those sources or carry the compact contract itself. Structure it like a mini CLAUDE.md: purpose, what to establish before starting, the workflow, conventions, output rules. Headings and short sections work fine inside the field. Keep a copy of the field's text in a versioned location once it grows past a few paragraphs (for example a notes repo, or the mirror-block file of a related folder project) — losing it to an accidental edit is otherwise silent.

## Keeping the app-side fields honest

The single-owner principle (Guide 23) applies across layers just as it does across projects: every rule and fact has exactly one home, and the only sanctioned duplication is a hard safety rule restated in the instructions field.

Because the fields are unversioned, the folder needs a record of them:

- **Mirror block.** Keep the current text of both fields verbatim in the project folder — a short `## App-side fields` section at the bottom of CLAUDE.md (or a `UI-FIELDS.md` when the instructions are long) with a last-verified date. This is documentation of an external surface, not a second copy of rules: the field is the live text, the mirror is the versioned record of it. Reading the live field tells you what it says today; only the mirror records its earlier reviewed form.
- **Update triggers.** When CLAUDE.md's purpose or hard rules change, check the app-side fields the same session. When you edit a field in the app, update the mirror. Either direction without the other reintroduces the drift.
- **Audit checklist.** A maintenance sweep over a project should check: description matches the project's current purpose and is not a duplicate of another project's; instructions contain a bootstrap or pointer plus the project's hard rule (or are deliberately empty for a low-stakes project); the mirror block exists and matches the live field. Read the live values through an available supported surface; if that is unavailable, mark the comparison unverified and request only the missing field when needed.

`tasks/tune-instruction-layers.md` runs this checklist end to end.

## The account layers above the project

Account-level preferences and managed instructions sit above the project in product-specific ways. Claude account/Cowork preferences, ChatGPT customization and Codex global guidance are separate surfaces; editing one does not update the others.

Put broadly applicable style and identity preferences in the native account layer, and project-specific rules in the project policy. Inspect managed organization instructions when visible and obey enforced organizational controls; do not treat a local prose file as overriding them. Avoid assuming field names, character limits or injection order from another product.

Keep a private mirror for each configured account/surface with applied text, date and verification status. Edit the authored proposal, apply it through supported controls, read it back, and run a fresh-session check. If a field is inaccessible, record that limitation rather than claiming it is empty. `tasks/tune-instruction-layers.md` and [`templates/ACCOUNT_INSTRUCTIONS_TEMPLATE.md`](./templates/ACCOUNT_INSTRUCTIONS_TEMPLATE.md) provide the review and starter.

---

## Short version

1. One authored contract; native loaders and app fields differ by surface.
2. Put identity in the available identity field, bootstrap and essential action constraints in instructions, and evolving detail in the shared policy.
3. Keep `CLAUDE.md` thin when `AGENTS.md` owns the shared rules.
4. Record uploaded-source revisions and refresh them after policy changes.
5. Inspect and mirror each platform separately; proposed text is not applied configuration.
6. Use supported UI/tools for app changes, not undocumented state-file writes.
7. Verify a fresh session on every supported surface; record untested surfaces honestly.
8. Use `tasks/tune-instruction-layers.md` to review the layers together.

---
