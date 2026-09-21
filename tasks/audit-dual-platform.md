# Task: Audit Dual Platform

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/audit-dual-platform.md`
> **Source guides:** `35_DUAL_PLATFORM_PROJECTS.md` (§7 State/Schedules/Handoffs, §8
> Verifying Each Surface, §9 Platform Facts and counterparts table), `23_MULTI_PROJECT_SETUPS.md`
> ("Requesting the mount, on demand"), `17_TROUBLESHOOTING.md` (common failure causes this
> task checks for directly), `24_PROJECT_FOLDER_STRUCTURE.md` (file map conventions).

## Runtime route

Name the target surface and available tools before running steps. Run each check only
on a surface this session can actually reach. A surface this session cannot reach
(most often the ChatGPT side, from a Claude session) is reported as **ask the user**,
never silently skipped and never assumed fine.

## Purpose

A short, re-runnable sanity check for a project already set up as dual-platform
(`setup-dual-platform.md` has run at least once): are the files and folders the setup
actually depends on still there and reachable, right now, on this surface? This is the
mechanical half of Guide 35 §8 — whether the pieces resolve — not the conversational
half (whether a fresh session behaves correctly on loading them), which stays a
separate, heavier check. Run this one often; it is read-only, fast, and produces a
short table, not an interview.

Use it after `setup-dual-platform.md`'s own Step 6, on a cadence (monthly, or whenever
a session feels like it's missing context it should have), after any edit to the
shared policy or an app-side field, and any time a sibling-project or device-bridge
folder request has failed or looked wrong.

## Instructions

### Step 0 — Locate the target

Confirm the project folder is mounted on this surface. If it is not, stop: report
that as the first and only finding (per Guide 17, this is the single most common
dual-platform failure) rather than trying to check anything else from memory.

### Step 1 — Run the checklist (read-only)

For each check, record **OK**, **Missing**, **Stale**, **Unreachable**, or **Ask
user** (for anything this surface cannot check directly) — never silently omit a row.

| # | Check | How |
|---|---|---|
| 1 | Shared policy and adapter exist | `AGENTS.md` (or the project's Claude-only `CLAUDE.md`) and, for dual-platform, a `CLAUDE.md` that imports it, are present and non-empty |
| 2 | Setup page exists and matches reality | `PLATFORM_SETUP.md` (or equivalent) is present; its surface table, capability-gap list and scheduler-owner table are not stubs |
| 3 | Every referenced path resolves | Extract every relative link and backticked path from `AGENTS.md`, `CLAUDE.md` and `PLATFORM_SETUP.md`; confirm each exists on disk. A dead reference is exactly what Guide 23's "Keeping linked projects consistent" calls a broken pointer |
| 4 | Every named sibling/cross-project folder is reachable *right now* | For each "Sibling project access" (or similarly named) section, check whether this session can currently read that path. Do not assume a past grant still holds — Guide 23's "Requesting the mount, on demand" section records that Claude Cowork grants have been observed not to persist across sessions |
| 5 | Fresh-session check table is current | Compare each surface's last-verified date in `PLATFORM_SETUP.md` against the date of the most recent edit to the shared policy, adapter, or an app-side field. A check older than the last edit is stale, not passing |
| 6 | Scheduler ownership is intact | Each row in the scheduler-owner table names one platform; where this surface can list actual registrations (e.g. Claude scheduled tasks), confirm the named owner still exists and no duplicate has appeared on the other platform |
| 7 | Capability-gap and Platform Facts entries carry dates | Flag any row with no date, or a date old enough that the underlying product likely changed (a judgement call — say why, per Step 2's confidence discipline) |
| 8 | ChatGPT-side state (revision, project fields) | Almost never checkable from a Claude session — record as **Ask user**: "is the uploaded source current, and do the project instructions match what's in the setup page's app-side text block?" For a ChatGPT local project, also ask whether the repository is the project's primary folder: only the primary folder's `AGENTS.md`, skills and `config.toml` are discovered (Guide 23) |

### Step 2 — Present findings

One table, in the order above, columns: **#**, **Check**, **Status**, **Fix** (one
line — what to do, not why). Keep the whole table short enough to read at a glance;
this task exists specifically so the answer to "is it still working" doesn't take a
full review to get. For anything resting on judgement rather than a file being present
or absent (checks 5 and 7), carry a **confidence** (high/medium/low) next to the row
rather than stating it flatly.

State plainly if every row is OK — a clean result is a valid, short report, not a
reason to keep looking for something to flag.

### Step 3 — Apply what's safe inline; propose the rest

Two different kinds of fix:

- **Safe to do immediately, no approval needed:** re-requesting an unreachable
  sibling/device-bridge folder this session's tools can request directly (Guide 23).
  This changes nothing on disk and is reversible by construction — the person is
  already prompted for it.
- **Everything else waits for approval:** fixing a dead reference, updating a stale
  date, correcting a scheduler-owner row, editing `PLATFORM_SETUP.md`. Present the
  specific edit next to its finding and wait before writing.

## Output

A short findings table (Step 2) plus, where approved, the specific edits applied
(Step 3) and a note of what still needs the user's own action (ChatGPT-side checks,
anything declined).

## Constraints

- Read-only through Step 2. Only a folder-access re-request (Step 3, first bullet)
  happens before approval; everything else waits.
- Never report a surface or check as OK without actually checking it on that surface
  this run — "probably still fine" is **Unreachable** or **Ask user**, not OK.
- Do not fold this into a full `setup-dual-platform.md` re-run. If findings suggest
  the shared-policy/adapter split itself is wrong (not just stale or unreachable),
  say so and hand off to that task rather than trying to fix structure here.
- Keep the report short. A long write-up defeats the purpose of a check meant to be
  run often.
