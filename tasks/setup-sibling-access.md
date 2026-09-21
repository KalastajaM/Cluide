# Task: Setup Sibling Access

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/setup-sibling-access.md`
> **Source guide:** `23_MULTI_PROJECT_SETUPS.md` ("Requesting the mount, on demand");
> see also `17_TROUBLESHOOTING.md` for the Cowork mid-session-request mechanism this
> task installs against.

## Runtime route

Name the target surface and available tools before running steps. On Claude Cowork
with the device bridge, this installs an instruction the assistant follows using
`device_request_folder_access` mid-session. On Claude Code or a local Codex session
already working inside the filesystem, no request step is needed — say so and skip to
recording the paths for reference. On a ChatGPT project, this task can only produce
the section text; whether the ChatGPT surface can request a folder mid-task is
unverified (Guide 23), so record every sibling folder needed and tell the user each
one must be attached through "Add folder" at project setup instead.

## Purpose

Give a project on-demand access to specific sibling projects that hold master data it
treats as read-only reference (parcel facts, ownership, a shared estate settlement, a
notes layer) — without duplicating that data into this project, and without requesting
every sibling's folder at the start of every session regardless of whether the task at
hand needs it. Use it when a project's shared policy already says "X is owned by
project Y" (or should) but nothing tells the assistant how, or when, to actually reach
Y.

## Instructions

### Step 0 — Locate the target and its siblings

Confirm the project's shared policy file (`AGENTS.md`, or `CLAUDE.md` for a
Claude-only project) and identify which other projects it already names as owning
specific facts. If none are named yet but the user describes a dependency in chat,
note it here — this task also writes new relationship lines, not only wires up
existing ones.

For each sibling, get: the sibling's absolute local path, and the fact-types this
project would need from it (be concrete — "parcel ownership and tax facts," not
"everything").

### Step 1 — Present the list and get sign-off

Show the user the sibling projects found, their paths, and the fact-types you will
write triggers for. Stop and wait for confirmation before writing — a wrong trigger
list means the assistant either never asks (and silently guesses at a fact) or asks
too often (and spends a permission prompt on work that didn't need it).

### Step 2 — Write the section

Add a "Sibling project access" section to the project's Claude-side policy file,
filling in this template (do not omit any of the four parts — each is load-bearing,
see Constraints):

```markdown
## Sibling project access (Cowork / device bridge)

This project's own local-folder connection reaches only the <THIS PROJECT> folder
itself, not its siblings. <SIBLING A> holds <what kind of master data>; <SIBLING B>
holds <what kind of master data>. Treat these as read-only reference from here.

Request access to a sibling folder only when the task actually needs it — e.g.
<concrete example fact> from <SIBLING A>, <concrete example fact> from <SIBLING B>.
Do not request any of them as a blanket step at the start of a session: most
<THIS PROJECT> work never touches them, and each grant is a permission prompt for
<user>, so don't spend one unless the work in front of you requires it.

When a task does need one, and it is not already reachable, request only that
specific folder (not all of them by default):

- <SIBLING A>: `<absolute path>`
- <SIBLING B>: `<absolute path>`

If access is declined or the tool is unavailable, say so and work from whatever is
already reachable rather than guessing at facts you can't verify.
```

Fill every placeholder from Step 0's list — do not ship a bracketed placeholder into
the live file.

### Step 3 — Cross-check the owner side

If the sibling project's own policy does not yet say it is referenced by this project,
add or update its ownership registry / "referenced by" note per Guide 23's ownership
registry convention, so the relationship is visible from both ends.

### Step 4 — Verify

In a fresh session against the target project, give it a prompt that does need a
sibling fact and confirm it requests only that one folder; then give it a prompt that
clearly does not touch any sibling and confirm it requests nothing. Record the result
(pass/fail, date, surface) in the project's `PLATFORM_SETUP.md` fresh-session check
table if it has one.

## Output

An added or updated "Sibling project access" section in the target project's
Claude-side policy, naming each sibling, its path, and its request trigger; optionally
an updated ownership registry entry on the sibling side.

## Constraints

- Never copy a sibling's data into the target project as a workaround for access
  friction — that recreates the staleness problem cross-project linking exists to
  avoid (Guide 23, "Duplicating instead of pointing").
- Do not write a trigger for a sibling access request without a concrete example
  fact — a vague trigger degrades back into "ask every time," which this task exists
  to prevent.
- Verified/unverified claims about a platform's mid-session request behavior must
  carry a date; do not assert Claude's device-bridge behavior for ChatGPT or vice
  versa.
