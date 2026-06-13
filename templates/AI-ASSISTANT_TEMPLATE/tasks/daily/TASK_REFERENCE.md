# Business Assistant — Reference Material

> Read on demand only. Not loaded every run. Referenced from TASK.md as `See TASK_REFERENCE.md §Section-Name`.

---

## §File-Structure

```
AI-Assistant/
├── Profile/
│   ├── PROFILE_SUMMARY.md       ← READ EVERY RUN. Compact digest (~1 page).
│   ├── PROFILE_identity.md      ← Role, org chart, key people, manual inputs.
│   ├── PROFILE_clients.md       ← Active clients, deals, accounts, status.
│   ├── PROFILE_patterns.md      ← Communication style, preferences, decision-making.
│   ├── PROFILE_hypotheses.md    ← Hypotheses and confirmed beliefs.
│   └── PROFILE_archive.md       ← Closed deals, completed projects.
├── Knowledge/
│   ├── INDEX.md                 ← Index of all topics. Read each run.
│   └── [TOPIC].md               ← One file per project/topic.
├── Actions/
│   ├── PENDING_ACTIONS.md       ← Generated view of pending_actions.json. Regenerated each run.
│   ├── ACTIONS.md               ← Daily briefing (Markdown). Regenerated each run.
│   ├── ACTIONS.html             ← Daily briefing (styled HTML). Regenerated each run.
│   └── History/                 ← Archived ACTIONS.html files (ACTIONS-YYYY-MM-DD_HHMM.html).
└── daily/
    ├── TASK.md                  ← Run procedure.
    ├── TASK_REFERENCE.md        ← This file. Read on demand only.
    ├── CONFIG.md                ← Tunable thresholds. Read every run (Step 1).
    ├── RUN_LOG.md               ← Append-only run history.
    ├── LAST_RUN.txt             ← Single line: ISO 8601 UTC timestamp of previous run start.
    ├── pending_actions.json     ← SOURCE OF TRUTH for all open actions.
    ├── resolved_archive.json    ← Overflow for resolved entries beyond RESOLVED_INLINE_CAP.
    ├── IMPROVEMENTS.md          ← Run counter, pending proposals, known issues (slim — loaded every run).
    ├── IMPROVEMENTS_DETAIL.md   ← Full fix history and all proposals (on demand — maintenance only).
    ├── SIGNAL_LOG.md            ← Structured operational signal log (on demand — maintenance reads).
    ├── LESSONS.md               ← Append-only log of mistakes and improvements.
    ├── generate_actions_html.py ← Script: ACTIONS.md → ACTIONS.html (Step 8).
    └── generate_pending_actions_md.py ← Script: pending_actions.json → PENDING_ACTIONS.md (Step 6).
```

---

## §Connector-Quirks

O365 connector syntax notes (confirmed against the live connectors; update with a date when they change):

- **Email search:** `query: "*"` → syntax error. Use `"[YOUR_COMPANY_KEYWORD]"` for inbox, `"[YOUR_NAME_LOWERCASE]"` as fallback. Sent items: add `sender: "[YOUR_EMAIL]"` — **never** `folderName: "Sent Items"` (NOT_FOUND on this account).
- **Flagged email:** `query: "isflagged:true"` (KQL, confirmed 2026-03-20). Full flag metadata via `read_resource` on the individual message.
- **Calendar:** `query: "*"` works (confirmed Run 9); keyword queries may miss events. **Do NOT pass `limit`** — the connector coerces the integer to a string and fails ("Expected number, received string"); omit it and the API default applies.
- **Teams (`chat_message_search`):** filter by participant (`recipient:`) + `afterDateTime`; **do NOT pass `limit`** (same coercion bug). See §Teams-Search.

---

## §Triage-Gate

Step 3B Pass 1 — decide whether to call `read_resource` (full body) from the search snippet alone.

**Call `read_resource` if any of:**
- Sender is unknown or not yet in the profile
- Snippet contains action words: reply, deadline, confirm, urgent, invoice, meeting, escalat-, decision, approve, contract
- Email relates to an active PA (sender or subject match)
- Sender is a tracked contact in `PROFILE_identity.md`
- Snippet is cut off and context is ambiguous

**Skip `read_resource` if all of:**
- Sender matches the Digest Senders table in IMPROVEMENTS.md
- Snippet is clearly promotional with no action keywords
- Automated system notification with no PA match (CI/CD, standup bots, calendar boilerplate)
- Thread is an exact duplicate of one already processed this run

---

## §Extraction-Categories

Step 3B Pass 2 (and Step 3C Teams) — what to extract from full bodies:

- **Profile signals:** people & relationships, deals & projects, communication patterns, decisions & priorities, commitments in both directions, recurring patterns.
- **Decisions (explicit — all runs):** what was decided, by whom, when, which topic. Flag contradictions with prior direction in ❓. Material only.
- **Actionable items:** emails awaiting reply, deadlines, follow-ups, invoices, commitments made in either direction, meeting prep needed.
- **Skip:** marketing/newsletters (unless [USER] engages), spam, automated system notifications (unless revealing), mailing lists where [USER] doesn't participate, calendar invite boilerplate.
- **Keep even if automated:** invoices/payments, contract notifications, subscription changes, CRM/ticketing on active deals.

---

## §Teams-Search

**Why filter by participant, not content (fixed 2026-03-25 — root cause of all prior 0-result runs):** `query: "[YOUR_NAME_LOWERCASE]"` searches message *content* for that word, which is almost never present in bodies. Filter by participant instead.

Two passes (**never pass `limit`** — see §Connector-Quirks):
1. `chat_message_search`: `query: "[YOUR_COMPANY_KEYWORD]"`, `recipient: "[YOUR_EMAIL]"`, `afterDateTime: LAST_RUN_UTC` — returns messages in chats where [USER] participates.
2. If pass 1 returns 0 **and today is not Saturday or Sunday:** fallback with `query: "[YOUR_COMPANY_KEYWORD]"` and a recent contact name as `recipient` (e.g. `[EXAMPLE_COLLEAGUE_EMAIL]`) to catch chats not indexed by [USER]'s address. Log both passes in RUN_LOG. Skip on weekends — 0 is expected.

**Zero-result email proxy for PA resolution (2026-03-25):** if both passes return 0 AND open PAs have `resolution_check.type = "teams_search"`, run a targeted `outlook_email_search` (inbox + sent) using each such PA's `resolution_check.query` as a proxy — Teams decisions frequently surface in email notifications, follow-up threads, or sent items. Carry any proxy evidence into Step 5A. Note all proxy searches in RUN_LOG.

**Permanent filters:** skip `[EXAMPLE_TEAMS_CHANNEL_TO_SKIP]` entirely; skip bot/CI-CD/standup channels and non-business banter (personal chat, jokes, social).

---

## §Calendar-Rules

**Timezone rule (apply to every event individually — errors have occurred three times; never mix approaches within a run):**
- `isOrganizer: true` ([USER] organized) → connector timestamp IS the local time. Display as-is; do NOT add offset.
- `isOrganizer: false` (someone else organized) → connector timestamp is true UTC. Add the current offset ([YOUR_UTC_OFFSET] [YOUR_TIMEZONE_ABBR] Oct–Mar / [YOUR_UTC_OFFSET] [YOUR_TIMEZONE_ABBR] Mar–Oct) to get local time; confirm the current offset from `RUN_TIME_HEL`'s timezone string first.
- Exception: `isOrganizer: true` AND `recurrence ≠ null` AND a large cross-team meeting → treat as true UTC and flag "connector time — verify local time".
- Never compare raw UTC against `RUN_DATE_HEL` (`T22:00:00Z` = midnight [YOUR_TIMEZONE_ABBR] = start of the next calendar day).

**Solo block:** any event where organizer = [USER] with no other participants — a personal work reservation; [USER] can freely attend other meetings during it.

**Conflict detection (PROP-0002):** sort events by start time and scan for overlapping pairs where **both** are non-solo and at least one has named external attendees or known colleagues. For each real overlap: log both event names, the overlap duration, and all named attendees; flag ⚠️ in a **Scheduling Conflicts** sub-section at the top of `📅 Meeting Prep`. Ambiguous connector time → "possible overlap — verify [YOUR_TIMEZONE_ABBR] times". No conflicts → "none detected". An overlap where one event is a solo block is not a conflict — note simply that the meeting falls inside a personal work block.

---

## §Flagged-Sync

Step 3E full sync logic. `outlook_email_search` `query: "isflagged:true"`, `limit: 50` returns the current flagged `messageId`s. Process all results, plus check tracked PAs for removals:

1. **New flag** (messageId NOT in any existing PA's `outlook_message_id`): call `read_resource` for `flag.dueDateTime`. Dedup against existing PAs by subject/sender/context. Match → merge (add `outlook_message_id` + `outlook_flag_due`; update deadline if the flag date is earlier). No match → new PA with `"source": "outlook-flag"`.
2. **Tracked flag still present** (messageId IS in current results): call `read_resource` for `flag.dueDateTime`. Changed vs the PA's `outlook_flag_due` → update deadline; unchanged → no write.
3. **Tracked flag absent** (existing PA's `outlook_message_id` NOT in current results) → EXPIRED or RESOLVED. No `read_resource` — absence is sufficient.

**Cost rule (PROP-0003, 2026-03-24):** skip `read_resource` for (a) removed/completed flags (case 3 — absence is sufficient); (b) tracked flags where `outlook_flag_due` is > 30 days from today AND `last_reviewed` is within 7 days (far-future stable flags — carry the stored `outlook_flag_due` forward unchanged). All other present flags — new or tracked — require `read_resource` to catch due-date changes. Note (b) skips in RUN_LOG.

---

## §Resolution-Checks

Step 5A throttling and backoff for PAs with a `resolution_check`.

**Throttle — check `next_resolution_check` first:**
- Set and > today → **skip this PA** (note "PA-NNNN resolution check deferred to YYYY-MM-DD" in RUN_LOG); do not run the search.
- Exception: `deadline` within 3 days of today → always run regardless.
- Exception: `hard_deadline` set and today ≥ it → escalate the PA to URGENT immediately regardless of any deferral; never skip.
- Null or ≤ today → run the search normally.

**After a failed check** (search ran, no resolution found), set `next_resolution_check` by PA age: created ≤ 7 days ago → tomorrow; 8–21 days ago → today + 3 days; > 21 days ago → today + 5 days.

**After a successful resolution:** clear `next_resolution_check` (set null), mark RESOLVED.

Run the specified search — matching message → RESOLVED; `portal` type → cannot auto-check, leave pending.

**Teams 0-result email fallback (2026-03-25):** if the Teams search returned 0 this run AND the PA has `resolution_check.type = "teams_search"`, also run `outlook_email_search` (inbox + sent) using the PA's query as a proxy. Proxy resolves it → RESOLVED with note `[resolved via email proxy — Teams search returned 0]`. No proxy evidence → leave PENDING, note "Teams search 0; email proxy also negative" in ACTIONS.md ❓ section.

---

## §Run-Quality

Step 9 detail.

**9A Efficiency scan — flag in 🔧 if any are true:**
- A connector was called and returned 0 results it could never plausibly return (query too narrow or redundant)
- The same resource was read more than once without new information being needed
- `read_resource` was called on a flag that turned out to be a tracked, unchanged PA (case 3 in §Flagged-Sync)
- A step ran in full but produced no output and no update (candidate for fast-path extension)
- Total tool calls this run exceeded 30 (flag as high — log the count in RUN_LOG)

**9B Issue-log entry** (append to `ISSUES_LOG.md`):
```
## YYYY-MM-DD Run Issue (Run #N)
- Type: connector-error | logic-issue | missed-item | efficiency | other
- Description: <what happened>
- Steps involved: <e.g., Step 3C, Step 5A>
- Status: open
```

**9E Signal types** (append to `SIGNAL_LOG.md` as `YYYY-MM-DD HH:MM | TYPE | description`):
- `QUERY_ZERO` — a connector returned 0 results unexpectedly
- `MISSED_ACTION` — an actionable item was missed in a prior run
- `FALSE_URGENT` — an URGENT item turned out not to be
- `PA_STALE` — any PA flagged stale this run
- `PROFILE_SIZE` — a profile file near or over its line limit
- `PROFILE_REPEAT` — same profile section updated 3+ consecutive runs
- `RENDER_FAIL` — a Python script returned non-zero or error output
- `RESOLUTION_FAIL` — same `resolution_check` returned 0 five+ consecutive runs
- `PA_OVERLOAD` — open PA count > 15
- `OTHER` — anything else requiring maintenance attention

---

## §PA-Schema

Full JSON schema for pending action entries in `pending_actions.json`:

```json
{
  "id": "PA-NNNN",
  "title": "Short description",
  "status": "PENDING",
  "priority": "URGENT | SOON | LOW",
  "created": "YYYY-MM-DD",
  "deadline": "YYYY-MM-DD or null",
  "source": "email | teams-dm | teams-channel | calendar | outlook-flag",
  "context": "What [USER] needs to know",
  "action": "What [USER] should do",
  "resolution_check": {
    "type": "inbox_search | sent_search | teams_search | portal",
    "query": "search query string",
    "note": "Human-readable note"
  },
  "draft": "Optional pre-written message",
  "draft_channel": "email | teams-dm | teams-channel",
  "resolution_evidence": "What would count as resolved",
  "last_reviewed": "YYYY-MM-DD",
  "outlook_message_id": "Optional",
  "outlook_flag_due": "Optional ISO 8601",
  "sub_status": "PORTAL_PENDING | WAITING_OTHER | null",
  "next_resolution_check": "YYYY-MM-DD or null",
  "hard_deadline": "YYYY-MM-DD or null"
}
```

`sub_status`: `PORTAL_PENDING` → 🔑 section; `WAITING_OTHER` → 🔄 section; `null` → standard 🔴/🟡.

`hard_deadline`: Optional. When set and today ≥ `hard_deadline`, escalate the PA to URGENT regardless of `next_resolution_check` or other deferral logic. Use for truly immovable deadlines (e.g., SteerCo agenda cut-off, legal filing date). Leave `null` when absent.

Resolved entry format: `{ "id", "title", "status": "RESOLVED|SUPERSEDED|EXPIRED", "resolved_date", "resolution" }`. Retain in `resolved_last_30_days` for `RESOLVED_KEEP_DAYS` days (→ CONFIG.md); remove older. Cap inline at `RESOLVED_INLINE_CAP` entries (→ CONFIG.md) — move excess (oldest first) to `resolved_archive.json` (`archived_resolved` array).

---

## §PENDING_ACTIONS-Template

Fallback template if `generate_pending_actions_md.py` fails:

```markdown
# Pending Actions [GENERATED VIEW]
> Source of truth is pending_actions.json. Do not edit — regenerated each run.
> To resolve: tell the assistant "mark PA-NNNN as done", or add [DONE]/[SKIP]/[IGNORE] to this file.

## Action Counter
**N open** (generated YYYY-MM-DD) | Next ID: PA-NNNN

## Summary Table

| ID | Priority | Deadline | Topic | Action |
|----|----------|----------|-------|--------|
[one row per open PA, URGENT → SOON → LOW; within group: overdue → today → no deadline → future ascending; action truncated to ~80 chars]

---

## 🔑 In Your Court (portal/action required)
[PA-ID, portal name, required action]

## 🔴 Urgent / Time-Sensitive
## 🟡 Needs Attention Soon
## 🔵 Low Priority
## 💤 Snoozed
## ✅ Recently Resolved (last 30 days)
| Date | ID | Resolution |
```

Sort order within each section: overdue → due today → no deadline → future ascending.

---

## §ACTIONS-Template

Section structure for `ACTIONS.md`. All sections must be present (use empty or "none" if no content):

```markdown
# Business Assistant Briefing — YYYY-MM-DD

## ⏳ Pending Actions Summary
[table: ID | Description | Priority | Deadline | Channel — URGENT→SOON→LOW; within group: overdue→today→no deadline→ascending]

## 🔴 Urgent / Time-Sensitive
## 🔑 In Your Court (portal required)
## 🟡 Needs Attention Soon
## 📋 Meeting Briefs
*Meeting briefs are generated on demand. Tell the assistant which meeting to prep for.*

## 📅 Meeting Prep
[Scheduling Conflicts sub-section at top]

## 💬 Teams Follow-ups
## 💡 Proactive Suggestions
## 📝 Draft Messages
[PA-ID, recipient, channel label (Email / Teams), draft text]

## 🔄 Follow-Ups (Waiting on Others)
## ✅ Recently Resolved
## 📊 Profile & Knowledge Updates
## 🗂️ Decisions This Run
[Date · Topic · What was decided · Who]

## 🔧 Self-Improvement
[Applied this run | Pending proposals | Refactor status]

## ❓ Questions for [USER]
```

---

## §RUN_LOG-Format

**Canonical format (Runs 31+):** h2 header with run number and day name. Older h3 entries are grandfathered — do not reformat them.

Append to `RUN_LOG.md` after each run:

```markdown
## Run N — YYYY-MM-DD (Day)
- **Run start:** YYYY-MM-DDTHH:MM:SSZ | **Local time:** HH:MM [YOUR_TIMEZONE_ABBR]
- **Analysis window:** YYYY-MM-DDTHH:MMZ → YYYY-MM-DDTHH:MMZ (~Xh — [single day / multi-day])
- **Emails analyzed:** [brief summary of key emails processed]
- **Teams:** [N results — brief note, or "no business messages"]
- **Calendar (dates):** [key events noted]
- **Flagged items sync:** [what was checked/resolved]
- **PA resolution checks:** [summary of checks and outcomes]
- **Profile files updated:** [list or "none"]
- **Knowledge base updated:** [list or "none"]
- **Actions: new:** N | **resolved:** N | **still pending:** N | **overdue:** N
- **Fast-path:** yes/no
- **Tool calls:** N
- **Notable:** [1–2 sentences or "nothing significant"]
```

Keep last 20 runs in full (per `RUN_LOG_KEEP_RUNS` in CONFIG.md); summarize older entries as a single compact block at the top of the file.

---

## §Knowledge-Topic-Format

Template for new topic files in `../../Knowledge/`:

```markdown
# [Topic Name]
> Last updated: YYYY-MM | Status: ACTIVE / CLOSED / ON HOLD

## Background
## Key Facts
## Decisions Log
| Date | Decision | Made by | Notes |

## Current Status
## Open Questions
## History / Context
```

Filenames: descriptive (`VCP_Initiative_8.md`, `FF1_EOL.md`). Avoid generic names.

---

## §Evidence-Tiers

Append a letter to `[updated: YYYY-MM]` tags when writing profile entries to indicate how the information was obtained:

| Letter | Meaning | Example |
|--------|---------|---------|
| `E` | Directly observed in email or Teams content | `[updated: 2026-04 E]` |
| `I` | Inferred from an observed pattern | `[updated: 2026-04 I]` |
| `C` | [USER] confirmed an inference | `[updated: 2026-04 C]` |

`[confirmed: YYYY-MM]` tags imply tier `C` or a direct statement — no letter needed. `[USER]` and `[USER-CONFIRMED]` tags are the highest tier — never overwrite.

Do **not** retroactively tag existing entries. Apply to new additions only.

---

## §LESSONS-Format

Append to `LESSONS.md` before changing TASK.md (log-first rule):

```markdown
### YYYY-MM-DD — [Short title]
- **Type:** mistake | connector | optimization
- **What happened:** [What went wrong or what improvement was noticed]
- **Correction:** [What changed]
- **Rule change:** [What was updated in TASK.md, or "none"]
```

---

## §PROP-Format

```markdown
### PROP-NNNN — [Short title]
- **Status:** PENDING | APPROVED | REJECTED | APPLIED
- **Raised:** YYYY-MM-DD
- **Type:** schema | run-procedure | output-template | profile | connector | other
- **Rationale:** [Why this improves the assistant]
- **Confidence:** LOW | MEDIUM | HIGH
- **Proposed change:** [Precise enough to apply without ambiguity]
- **Risk:** [What could go wrong]
```

IDs are sequential. Once approved, apply in Step 9C and move to Applied Fixes table in IMPROVEMENTS.md.

---

## §Backfill

DISABLED. If re-enabled: process 2 years of email in monthly batches backwards from RUN_LOG cursor; profile signals only (no action items); mark `[observed: ~YYYY-QN]`. Skip Teams.

---

## §Hypothesis-System

Format: `[HYPOTHESIS] Description. Evidence: ... Confidence: LOW|MEDIUM|HIGH|CONFIRMED. First observed: YYYY-MM. Last checked: YYYY-MM.`

[USER] validates → `[USER-CONFIRMED]` + `[confirmed: YYYY-MM]`. Contradicting evidence → downgrade. No evidence 6+ months → `[POSSIBLY OUTDATED]`. Surface MEDIUM-confidence in ❓ when confirmation would help.

---

## §Communication-Style

- Direct, no fluff. Priority emoji system: 🔴🔑🟡📋📅💬💡📝🔄✅📊🗂️🔧❓
- Each action: 1–3 lines max. Reference PA-ID.
- Draft messages: match [USER]'s observed style. Always label: **Email** or **Teams**.
- Teams drafts: shorter and more conversational than email equivalents.

---

## §Error-Handling

- **Connector errors / rate limits:** Process what you can; note skipped in RUN_LOG.
- **Teams unavailable:** Email-only; note in ACTIONS.md.
- **Empty results:** Still regenerate ACTIONS.md; log the run.
- **Missing files:** Create empty with standard header; note in ACTIONS.md.
- **Corrupted RUN_LOG:** Default to last 7 days; note the issue.

---

## §Self-Improvement-Boundaries

- Never remove or weaken rules unless [USER] explicitly approves or a self-review confirms them genuinely dead (log rationale in LESSONS.md).
- Never change Core Principles without explicit [USER] approval.
- If a lesson contradicts an existing rule, flag in ❓ — do not override.
- Optimization means doing the same or better with less — never doing less.

---

## §Privacy-Sensitivity

- **M&A / legal / HR:** Note existence; don't log specifics unless [USER] marks relevant.
- **Financial:** Track counterparties and deal patterns — not specific figures unless marked.
- **Client relationships:** Relationship nature and status only; minimize conflict/negative sentiment detail.
- **Confidential:** `[PRIVATE]` or `[CONFIDENTIAL]` markers → do not reference in ACTIONS.md unless asked.

---

## §Cowork-Optimizer-Checklist

Checklist used by the cowork-optimizer skill during periodic structural reviews (Step 9E). Run `/cowork-optimizer business-assistant task` in a fresh conversation — do not execute inline.

1. **Redundancy** — same instructions in multiple places?
2. **Dead rules** — workarounds for solved problems, obsolete connector notes?
3. **Step efficiency** — steps producing no value?
4. **Output quality** — sections empty 5+ consecutive runs?
5. **File hygiene** — RUN_LOG growing large (target: last 30 runs full, older summarised).
6. **TASK.md length** — target under 250 lines (extract detail into this reference file).
7. **Credit efficiency audit** — review tool-call counts over last 10 runs. Identify most expensive step. Is the fast-path triggering at an appropriate rate?
8. **Cross-task signals** — check MAINTENANCE_REPORT.md Task Health section for improvement candidates.
