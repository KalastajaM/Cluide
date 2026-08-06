# Task: Tune Instruction Layers

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/tune-instruction-layers.md`
> **Source guides:** `25_PROJECT_INSTRUCTION_LAYERS.md` (the layer split), `01_CLAUDE_MD.md` (the CLAUDE.md body).

## Purpose

Review one project's three instruction layers — the app-side **description** field, the app-side **project instructions** field, and **CLAUDE.md** — so each carries what belongs in it and nothing else, and so the three do not contradict each other.

Use it when a project's purpose has shifted, when a session behaved as though it had rules you don't recognise, when the app-side fields were last touched at setup and never since, or as the fix for a dimension-20 finding from `analyze-project.md`.

The asymmetry that shapes this task: the app-side fields are **readable but unversioned**, and **you apply them, not Claude**. So this task reads all three layers, but produces two different kinds of output — approval-gated edits for CLAUDE.md, and ready-to-paste text for the fields.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 0 — Preconditions

- The target project folder is mounted. If not, stop and ask for it.
- Read the target's own `CLAUDE.md` and `README` first. Local conventions are authoritative: a deliberate deviation from Guide 25 is a **conflict to confirm**, not a defect to fix.
- Read Guide 25, and Guide 01 for the CLAUDE.md body.

### Step 1 — Read the app-side fields

Both fields are on disk in the desktop app's state file (Guide 25, *Reading the app-side fields*):

```bash
ls ~/Library/Application\ Support/Claude/local-agent-mode-sessions/*/*/spaces.json
```

Read the entry whose `name` (or `folders[].path`) matches the target. Take `description`, `instructions`, `folders`, and `updatedAt`.

Three things to get right:

- **Absent ≠ empty.** `description` and `instructions` are missing keys when unset, not empty strings. "No instructions field" and "an instructions field containing nothing" are the same state here — report it as *unset*.
- **Report freshness.** Convert `updatedAt` (epoch ms) to a readable date and state it alongside anything you quote. If it predates a change the user says they made, ask them to confirm that one field rather than distrusting the whole file.
- **Ignore the siblings.** `remote-session-spaces.json` holds session/folder state only; any `spaces copy.json` is a stale duplicate.

**If the file is unreachable** — no Filesystem MCP access to `~/Library/Application Support` (the folder picker refuses it; see Guide 05), or this is not a Cowork project — say so plainly and ask the user to paste the two field texts. Do not guess, and do not silently review only CLAUDE.md: a two-layer review reported as a three-layer review is the failure this task exists to prevent.

For a **chat project** (no folder), there is no CLAUDE.md layer: the instructions field is the whole contract. Review only the two fields, judged as a mini CLAUDE.md (Guide 25, *Chat projects*), and skip Steps 4 and 5.

### Step 2 — Diagnose each layer (read-only)

Against Guide 25:

**Description.** States what the project does (not how)? Names the concrete entities that make it unmistakable? Free of rules? Unique — not a duplicate of another project's, which is worth checking directly since you have every entry in `spaces.json` in front of you? Still true after whatever the project has become?

**Instructions.** Contains only what must hold before any file is read — bootstrap, mount verification, restated hard safety rules, session posture, bridge guard? Anything long, evolving, or reference-shaped that belongs in CLAUDE.md instead? Conversely, for a project with real-world stakes: is the one hard safety rule present, or does it depend entirely on a mount succeeding?

**CLAUDE.md.** Judged against Guide 01 for the body. For this task specifically: does it contradict either field? Is there a mirror block, is it labelled as a mirror, and does it match the live text you just read?

**Across layers.** Every rule and fact has exactly one home (Guide 23's single-owner principle applied across layers). The one sanctioned duplication is a hard safety rule restated in the instructions field. Anything else stated twice is a finding — name which layer should own it.

Produce a short findings list, one line each, with the layer and the guide section — and name the layers
you checked and found sound. A project whose three layers are healthy should read as healthy, not as an
empty findings list.

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

### Step 3 — Present the plan and get sign-off

Two separate blocks, because they are applied by different hands:

1. **CLAUDE.md edits** — an itemised list of what changes and why. Approval-gated.
2. **Field texts** — the full proposed replacement text for the description and/or instructions field, each in its own fenced block, ready to paste. Show the current text alongside so the user can see what changes. Do not propose a field edit that only reformats.

State explicitly which findings you are *not* proposing to fix and why (usually: a deliberate local convention).

Then **stop and wait**. Do not proceed on assumed approval.

### Step 4 — Apply the CLAUDE.md edits

Apply only what was approved. If applying reveals something the plan missed, stop and present a revised plan rather than improvising.

### Step 5 — Update the mirror block

Once the user confirms they have pasted the field texts into the app, update the mirror block in the target's `CLAUDE.md` (a `## App-side fields` section, or `UI-FIELDS.md` when the instructions are long) to the new verbatim text, with today's date as last-verified.

If the user has not pasted them yet, do **not** update the mirror — a mirror that describes text nobody applied is worse than a stale one, because it reads as verified. Leave it and say what is outstanding.

## Output

1. A three-layer findings list (Step 2).
2. A change plan: CLAUDE.md edits + ready-to-paste field texts (Step 3).
3. On approval: applied CLAUDE.md edits and an updated, dated mirror block.
4. A closing note naming anything still outstanding — specifically any field text the user has not yet pasted.

## Constraints

- Read-only until Step 3 is approved.
- **Never write to `spaces.json`.** The app rewrites it wholesale from memory, so an edit made while the app runs is silently discarded — and a change the user believes is applied but isn't is the worst outcome this task can produce. Field changes are always ready-to-paste text.
- Never report a partial review as a full one. If a layer could not be read, say which and why.
- Respect the target's own `CLAUDE.md`; flag conflicts rather than overriding.
- Quote a field only with its `updatedAt` date attached.
- Do not touch other projects' entries in `spaces.json`, even read-only, beyond the description-uniqueness check — and report that check as a comparison, never by quoting another project's content.
