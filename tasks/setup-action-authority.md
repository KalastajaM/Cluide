# Task: Setup Action Authority

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-action-authority.md`
> **Source guide:** `32_ACTION_AUTHORITY.md` (see also `12_SECURITY.md` §8 and *Recording What a Refactor Must Not Weaken*, `07_TASK_LEARNING_GUIDE.md` Part 3 for the self-improvement instance)

## Purpose

Give a project an explicit boundary between what Claude does, what it prepares and proposes, and what it never does — classified by consequence rather than by tool — and turn any recurring "yes" into a written standing approval with a scope, a limit, an expiry and the evidence that earned it. The task inventories the actions the project's tasks and skills can actually take by reading connector scopes and tool lists, classifies them under Guide 32 §2, drafts the CLAUDE.md block from §8, proposes standing approvals only where the run history supports them, and wires the outbox and action log for unattended runs.

Use it when a project has scheduled tasks with connectors that can act (send, post, delete, move), when the user keeps being asked the same permission question, when a task has taken an action the user did not expect, or when `analyze-project.md` dimension 24 reports authority decided per request — actions not classified, approvals inferred from chat, a task that sends or deletes with no approval row to cite.

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons rather than plain text.

### Step 0 — Preconditions

Confirm the project is mounted, and that you can read its `CLAUDE.md`, every task definition, every skill, and the project's MCP or connector configuration (`.mcp.json`, or the connector list the user reads out from Cowork's settings — a session cannot read the app's connector scopes itself; ask).

If the project already has an action-authority block, this is a **review** run: Steps 1, 2, 4 and 6, comparing what the block says against what the inventory finds.

### Step 1 — Inventory the actions (read-only)

Build the table Guide 32 §1 says is missing: every action, not every tool.

For each connector, MCP server, app grant and file operation the project's tasks and skills can reach, list the distinct actions it enables. A mail connector is at least *read*, *label or file*, *draft*, *send*, *delete*; a filesystem grant is *read*, *write in place*, *create*, *move or rename*, *delete*; a git remote is *commit*, *push to private*, *push to public*. Read the scopes: a connector with no send scope does not get a *send* row, and that absence is recorded as a property in Step 4.

Then, for each scheduled task and each skill, which of those actions its instructions actually invoke, and which it *could* invoke because nothing stops it. The second column is the finding.

Present the inventory as a table: source (connector / grant / operation), action, which tasks and skills use it, which could.

### Step 2 — Classify (read-only)

Assign each action a class under Guide 32 §2 — A local and reversible, B local and costly to reverse, C leaves the user's hands, D binding or irreversible in the world — by asking the two questions: can it be undone and by whom, and does anyone else see it. Do not classify by tool; the same connector spans classes.

Two checks that change the answer:

- **Is the folder under git?** If yes, in-place edits to tracked files are Class A; if not, they are Class B. Say which, and if not under git, note that `setup-github.md` would move a whole class of actions down a tier.
- **Does any unattended task hold a Class C or D capability?** List each one. These are the rows Step 4 tries to remove structurally before any prose is written.

Present the classified table. Ask the user to confirm or move any row; the classification is theirs to own, since it encodes their tolerance for each consequence.

### Step 3 — Mine the history for standing-approval candidates (read-only)

Read `RUN_LOG.md`, `IMPROVEMENTS.md` (the *Pending Proposals* and *Applied Fixes* sections), the maintenance or approval log if the project keeps one, and any chat-recorded approvals the user can point at.

A candidate is a Class B action (or a narrowly shaped Class C one) that has been **proposed and approved unchanged** repeatedly. For each, draft a row in Guide 32 §3's form — action shape, scope, limit, evidence, proposed expiry — with the evidence quoted from the log (dates and counts). Do not propose a row without evidence; "the user would probably say yes" is not a row.

If nothing qualifies, say so. A project with no standing approvals and an honest default-deny is a correct state, not an incomplete one.

### Step 4 — Present the plan and get sign-off

Show, in this order:

1. **Structural removals first.** Every Class C or D capability an unattended task holds that the connector or grant would let you remove — a send scope to drop, an app grant to withdraw, a token to narrow. Each becomes a row in the project's security-properties table (Guide 12, *Recording What a Refactor Must Not Weaken*), with the change that would break it. Where a capability cannot be removed, say so, so the gap is known.
2. **The CLAUDE.md block** from Guide 32 §8, filled in: outbox path, log location, notification wording, and the four lines to lift into the account-level instructions if they are not already there.
3. **The standing-approvals table**, with the Step 3 candidates and their evidence. Each row is approved separately.
4. **The outbox and log wiring** for each unattended task: where Class C actions will be written instead of taken, and the extra column in `RUN_LOG.md` naming the approval row for each Class B action.

Mark anything irreversible (withdrawing a grant that is hard to re-obtain, for instance). Then **stop and wait.** Approval of the block is not approval of the standing-approval rows; approval of one row is not approval of the next.

### Step 5 — Take a restore point, then apply

Step 5 rewrites `CLAUDE.md` and every unattended task's instruction file — Class B under the guide this task installs, so it obeys the guide's own rule first. Under git: commit or tag the current state and confirm it. Not under git: a dated copy of every file this step will touch, stored outside the working tree. Confirm the restore point exists before the first edit; retire it after Step 6 verifies.

Then apply only the approved rows:

- Add the block and the approved standing approvals to `CLAUDE.md`; add the four class lines to the account-level instructions template or ask the user to paste them into the account field (Guide 25 — a session cannot write the app-side fields).
- Add the security-properties rows.
- For each unattended task: add the outbox step to its `TASK.md` so Class C actions are written to `<outbox path>` with a reason and an identifier each, and never taken; add the approval-row column to its `RUN_LOG.md` template; change its notification text to counts of actions taken and queued, and to send nothing on a run that did nothing.
- Add a one-line delegation rule if the project spawns subagents or workflow stages: they inherit the classes and approvals and gain none.

Record the connector and grant changes the user made themselves (a session cannot make them) with the date, in the security-properties table's *Why it holds* column.

### Step 6 — Verify

- Every action in the Step 1 inventory has a class in the block or a structural removal in the properties table. Nothing is unclassified.
- No unattended task holds a Class C or D capability that could have been removed. Where one remains, the properties table says it remains and why.
- Every standing-approval row carries all six fields; none lacks evidence or expiry.
- Each unattended task's `TASK.md` writes Class C actions to the outbox and cites an approval row for Class B ones.
- If the project has a behaviour-test suite (`31_BEHAVIOUR_TESTS.md`), propose a case per Class C boundary — `tool_used` on the send tool at zero is the canonical one — and offer to add it through `setup-behaviour-tests.md`.

Report what was classified, what was removed structurally, what was granted as standing, and what remains prose-only.

## Output

An action inventory by source and by task (Step 1); a classified table the user has confirmed (Step 2); standing-approval candidates with quoted evidence (Step 3); an approved plan (Step 4); a restore point, then the CLAUDE.md block, security-properties rows, and per-task outbox and log wiring applied (Step 5); and a verification report naming any boundary that is enforced only by prose (Step 6).

## Constraints

- Read-only until Step 4 is approved, and row by row: the block, each standing approval, and each structural removal are separate approvals.
- Confirm the restore point exists before the first edit in Step 5.
- Never propose a standing approval without quoted evidence from a log. Never infer one from a chat "yes".
- Never grant the session running this task any authority in the course of running it. The task writes rules; it does not act under them.
- Never widen a connector scope or grant to make a step easier. If a task's design needs a Class C capability, that is a finding for the user, not a scope change.
- Do not restate Guide 32's classes in the block beyond the §8 text; cite the guide for the reasoning.
