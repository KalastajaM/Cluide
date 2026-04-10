# Business Assistant — Reference Material

> Load on demand. Not read every run — referenced from TASK.md when needed.

---

## PA Schema (Full)

```json
{
  "id": "PA-NNNN",
  "title": "Short description",
  "status": "PENDING",
  "priority": "URGENT | SOON | LOW",
  "created": "YYYY-MM-DD",
  "deadline": "YYYY-MM-DD or null",
  "source": "email | teams-dm | teams-channel | calendar | outlook-flag",
  "context": "What [YOUR_NAME] needs to know",
  "action": "What [YOUR_NAME] should do",
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
  "sub_status": "PORTAL_PENDING | WAITING_OTHER | null"
}
```

`sub_status`: `PORTAL_PENDING` → 🔑 section; `WAITING_OTHER` → 🔄 section; `null` → standard 🔴/🟡.

Resolved entry: `{ "id", "title", "status": "RESOLVED|SUPERSEDED|EXPIRED", "resolved_date", "resolution" }`. Keep `resolved_last_30_days` for 30 days; remove older.

---

## ACTIONS.html CSS Mapping

**Emoji → CSS class:** `⏳`→`summary`, `🔴`→`urgent`, `🔑`→`portal`, `🟡`→`soon`, `📋`→`briefs`, `📅`→`meeting`, `💬`→`teams`, `💡`→`suggest`, `📝`→`drafts`, `🔄`→`waiting`, `✅`→`resolved`, `📊`→`profile`, `🗂️`→`decisions`, `🔧`→`improvements`, `❓`→`questions`

**Markdown → HTML:** `#`→`<h1>`, `##`→`<h2 class="...">`, tables→`<table>`, `>`→`<blockquote>`, `**`→`<strong>`, `-`→`<ul><li>`, `---`→`<hr>`, priority badges→`<span class="badge-urgent/soon/low">`.

---

## PROP-NNN Format

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

## LESSONS.md Entry Format

```markdown
### YYYY-MM-DD — [Short title]
- **Type:** mistake | connector | optimization
- **What happened:** [What went wrong or what improvement was noticed]
- **Correction:** [What changed]
- **Rule change:** [What was updated in TASK.md, or "none"]
```

---

## Privacy & Sensitivity Rules

- **M&A / legal / HR:** Note existence; don't log specifics unless [YOUR_NAME] marks relevant.
- **Financial:** Track counterparties and deal patterns — not specific figures unless marked.
- **Client relationships:** Relationship nature and status only; minimize conflict/negative sentiment detail.
- **Confidential:** `[PRIVATE]` or `[CONFIDENTIAL]` markers → do not reference in ACTIONS.md unless asked.

---

## Knowledge Base Topic File Format

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

Filenames: descriptive (e.g. `ProjectName.md`, `Initiative_X.md`). Avoid generic names.
