# Task: Setup Dual Platform

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-dual-platform.md`
> The steps are written so Codex can run them from the same folder; that path has not yet been tested end to end.
> **Source guides:** `35_DUAL_PLATFORM_PROJECTS.md` (the model this task installs), `25_PROJECT_INSTRUCTION_LAYERS.md` (layers and field mirrors), `01_CLAUDE_MD.md` (the adapter body), `24_PROJECT_FOLDER_STRUCTURE.md` (where shared and platform-local files live), `11_GIT_INTEGRATION.md` (branches, worktrees and handoffs). See also `09_MULTI_TASK_ORCHESTRATION.md` for single-owner shared state and `34_IMPORTING_FROM_OTHER_ASSISTANTS.md` for moving native memory. Worked example: Cluide's own `AGENTS.md`, `CLAUDE.md` and `PLATFORM_SETUP.md`.

## Purpose

Make one project usable from both Claude and ChatGPT — including Codex for repository work — through a single shared policy, without duplicating rules and without pretending that one product's mechanisms exist in the other. The task inventories every instruction-bearing and platform-bound file, sorts each rule into one home (shared policy, Claude adapter, OpenAI-specific, or platform-local state), lists every capability that has no verified counterpart, and installs the shared file, the thin adapter, a per-surface setup page and ready-to-paste app-side text. It finishes with a fresh-session check on each surface, and reports any surface it could not test as untested rather than working.

Use it when a Claude project should also be worked on from ChatGPT or Codex (or the reverse), when a project already has both `CLAUDE.md` and `AGENTS.md` and they have started to disagree, or when switching assistants has lost state or run a scheduled job twice.

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use the host's question tool with buttons (`AskUserQuestion` in Claude Code) rather than plain text, where one is available.

### Step 0 — Preconditions, surfaces and sources

- The target project folder is mounted. If not, stop and ask for it.
- Read the target's own instruction files and `README` first. A deliberate local convention is a **conflict to confirm**, not a defect to fix.
- Ask which surfaces the project must support (multi-select): **Claude Code**, **conversational Claude / Cowork**, **ChatGPT project** (uploaded or connected sources), **Codex** (local or cloud repository access). "Dual-platform" means at least one Claude surface and at least one OpenAI surface. Claude Code plus Cowork is a different combination, and this task does not apply to it.
- **Verify the platform facts before relying on them.** For each selected surface, read the current official documentation (Anthropic for Claude, OpenAI for ChatGPT and Codex) on instruction-file discovery, precedence, and nested or override files; import support; project-instruction size limits; the project instructions and description fields; and how uploaded or connected sources refresh. Record each fact with its URL and today's date. If this session has no web access, mark every such fact **unverified** in the plan and say so. Do not fill the gap from memory.

If the target already has a shared policy file and a platform adapter, this is a **review** run: Steps 1, 2 and 5–7, comparing what the files say against what the inventory finds.

### Step 1 — Inventory (read-only)

List every artefact that carries instructions or binds the project to one platform, with its current owner platform:

| Kind | Look for |
|---|---|
| Instruction files | root and nested `CLAUDE.md`, `AGENTS.md`, any override variants the Step 0 sources name, and the imports between them |
| App-side fields | Claude project description and instructions (read them as `tune-instruction-layers.md` Step 1 does); ChatGPT project instructions (a session cannot read these, so ask the user to paste them) |
| Platform configuration | `.claude/` settings, hooks, agents and skills; `.mcp.json`; `.claudeignore`; any OpenAI-side configuration the sources name |
| Skills and tasks | skill folders, `tasks/`, scheduled-task definitions, and the platform each one is registered on |
| State | native memory on each platform, `.auto-memory/` and profile files, run logs, scheduler registrations |
| Generators | templates or tasks inside the project that write instruction files and would reinstall single-platform assumptions |

Classify the starting point: **Claude-first** (`CLAUDE.md`, no shared file), **OpenAI-first** (`AGENTS.md`, no Claude adapter), **overlapping** (both exist and state the same rules twice), or **already structured** (review run).

### Step 2 — Sort every rule into one home (read-only)

Read the instruction files rule by rule and assign each one home:

1. **Shared policy** → the shared file (`AGENTS.md` unless the Step 0 sources say otherwise). Anything true whichever assistant is working: purpose, file hygiene, conventions, approval rules, merge gate, hard safety rules.
2. **Claude adapter** → `CLAUDE.md`. The import of the shared file, an explicit "read `AGENTS.md`" fallback for interfaces that do not resolve imports, and only the rules that depend on a Claude mechanism.
3. **OpenAI-specific** → a clearly labelled place the Step 0 sources support: a labelled section of the shared file, or the setup page. Never invent a configuration file or directory to mirror Claude's.
4. **Platform-local, never shared** → credentials, app settings, native memory, scheduler registrations and session history. The setup page names where each lives. Nothing in a shared file synchronises them.

Then produce three lists that change the plan:

- **Capability gaps.** Each Claude-only mechanism the project relies on (a hook, an `allowed-tools` allowlist, `.claudeignore`, a skill loader, a scheduled task, a subagent definition), with a verified OpenAI counterpart and its source, or **no verified counterpart**, or **untested**. Where Claude enforces something structurally, say plainly that a prose rule on the other platform is not the same guarantee (`12_SECURITY.md`). The same goes the other way for OpenAI sandbox or approval controls.
- **Scheduler ownership.** Each recurring job gets exactly one owning platform, its timezone and a stable identity. A job registered on both is a duplicate-run finding, and copying `TASK.md` does not move a registration.
- **Concurrent writers.** Files both assistants may write, and the rule that prevents conflicting edits: separate branches or worktrees reconciled through git, or one named writer (`11_GIT_INTEGRATION.md`).

Also flag every model name, tool name or path in a shared rule that belongs to one product. Never translate a Claude model name into a guessed OpenAI equivalent, or the reverse.

### Step 3 — Present the plan and get sign-off

Show, in this order:

1. **Shared file** — the full proposed `AGENTS.md`, with each rule's source line in the current files.
2. **Adapter** — the reduced `CLAUDE.md` (import, fallback, Claude-only rules), with a table of every rule that moves out and where it goes. For an OpenAI-first project, the new adapter. For nested instruction files, the same treatment one folder at a time.
3. **Setup page** — `PLATFORM_SETUP.md` or an agreed equivalent: a table giving each selected surface's entry point, how sources refresh, the verified facts with URL and date, the capability-gap list, the scheduler-owner table, the concurrent-writer rule, a handoff record (branch, commit, changed files, verification results, outstanding work), and the fresh-session check question from Step 6.
4. **App-side text** — ready-to-paste description and instructions for each platform's project, in separate fenced blocks with the current text alongside. The instructions field carries only bootstrap, source check, hard safety rules and posture (Guide 25).
5. **Not proposed** — findings deliberately left alone, and why.

Then **stop and wait.** Approval of the shared file is not approval of the adapter, and neither is approval of the field texts.

### Step 4 — Take a restore point, then apply

Under git: commit or tag the current state and confirm it. Not under git: a dated copy of every file this step will touch, stored outside the working tree. Confirm the restore point exists before the first edit.

Apply only what was approved:

- **Move rules; do not copy them.** Each rule leaves its old home in the same edit that adds it to the new one.
- Keep the shared file within the smallest instruction-size limit found in Step 0, and report its size.
- Rewire every reference to a moved rule or renamed file in the same unit of work (Guide 23).
- Leave platform configuration (`.claude/`, connectors, registrations) untouched unless a change was approved row by row. Where the user must change something in an app, record what they changed and the date.

### Step 5 — Verify on disk

- Every rule has exactly one home: search for a distinctive phrase from each moved rule and expect one hit. The only sanctioned duplicate is a hard safety rule restated in an app-side instructions field.
- `CLAUDE.md` imports the shared file, carries the read fallback, and restates nothing from it.
- Relative links in every changed file resolve, and the shared file is within its size limit.
- No shared rule names a product-specific model, tool or path. The capability-gap list and the scheduler-owner table exist, and every recurring job has one owner.

### Step 6 — Verify in a fresh session on each surface

Write one check question tailored to the project. For example: "Which instruction files did you load? Where do working notes go, what must you never do, and which parts of this project are platform-specific?" Also write the answer a correct session gives.

- Run it where this session can start a fresh session (Guide 26: a session that has not seen this run). In Claude Code, also confirm the imported file is listed as loaded.
- For every other surface, hand the question and expected answer to the user and record what they report. For a ChatGPT project, also confirm the uploaded source revision is current. A merge does not refresh uploaded copies.
- Record each surface as **verified (date)**, **failed (what differed)** or **untested**. Untested is a valid result. Reporting it as working is not.

### Step 7 — Mirror and report

Once the user confirms they have pasted the field texts, update the mirror block in `CLAUDE.md` or the setup page per Guide 25, per platform, with each field's last-verified date. If they have not pasted them, leave the mirror and say what is outstanding.

## Output

A per-artefact inventory with the starting-point classification (Step 1); a rule-by-rule home assignment, capability-gap list, scheduler-owner table and concurrent-writer rule (Step 2); an approved plan (Step 3); a restore point, then the shared file, adapter, setup page and rewired references (Step 4); on-disk verification (Step 5); a per-surface verified / failed / untested record (Step 6); and updated mirrors plus a closing note naming every unpasted field, untested surface and capability with no verified counterpart (Step 7).

## Constraints

- Read-only until Step 3 is approved, and file by file.
- Confirm the restore point exists before the first edit in Step 4.
- Never state a platform fact without an official source and date, or an explicit **unverified** label.
- Never mechanically convert `.claude/` into an OpenAI directory, invent an OpenAI ignore file, or translate model names. `.claudeignore` is not a security boundary on either platform.
- Never move credentials, native memory, app settings or scheduler registrations into a shared file, and never register a second copy of a recurring job on the other platform.
- Never write app-state files. Field changes are always ready-to-paste text applied by the user.
- Never report a surface as working without a fresh-session check on that surface.
- Respect the target's local conventions and filenames that other things point at. Flag conflicts rather than overriding.
