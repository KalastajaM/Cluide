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
6. **TASK.md length** — target under 400 lines.
7. **Credit efficiency audit** — review tool-call counts over last 10 runs. Identify most expensive step. Is the fast-path triggering at an appropriate rate?
8. **Cross-task signals** — check MAINTENANCE_REPORT.md Task Health section for improvement candidates.
