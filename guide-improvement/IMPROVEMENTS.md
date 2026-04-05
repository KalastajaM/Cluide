# Guide Improvement Log — Claude Teacher

> Managed by the guide-improvement task. Read at the start of every run (Step 1). Updated at the end of every run (Step 7).
> Respond to proposals by annotating them [APPROVED], [REJECTED], or [MODIFY: ...] directly in this file.

---

## Counters

```json
{
  "total_runs": 2,
  "runs_since_last_refactor": 2,
  "refactor_threshold": 6,
  "last_refactor_date": null,
  "next_refactor_due_at_run": 6
}
```

*Threshold of 6 assumes monthly runs → refactor every ~6 months.*

---

## Applied Fixes

*(Auto-applied fixes, newest first. Archive to "Archived Fixes" when this list exceeds 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|
| 2026-04-01 | FIX-002 | `05_TASK_LEARNING_GUIDE.md` | Applied Fixes template table header: "What changed" → "What was changed"; added "File" column | Inconsistency with Guide 06 template and actual IMPROVEMENTS.md which both include a "File" column |
| 2026-03-26 | FIX-001 | `00_INDEX.md` | "13-point short version" → "14-point short version" | Guide 07 has 14 items in its short version, not 13 |

---

## Archived Fixes

*(Rotated out of Applied Fixes when the table exceeds 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|
| *(none yet)* | | | | |

---

## Pending Proposals

*(Larger changes awaiting your input. Annotate with [APPROVED], [REJECTED], or [MODIFY: ...].)*

```json
[
  {
    "id": "PROP-001",
    "proposed": "2026-04-01",
    "title": "Add cross-link from Guide 03 to Guide 05's hypothesis lifecycle system",
    "rationale": "Guide 03 introduces the hypothesis concept with a simple inline format (H-001 notation, 'Would confirm:' field). Guide 05 Part 4 covers a more structured system (confidence stages LOW→MEDIUM→HIGH→CONFIRMED, lifecycle rules, surfacing criteria, expiry). There is no cross-reference between them, which means readers of Guide 03 may not know the full system exists, and a reader following both may be confused by the format differences.",
    "change": "In Guide 03, at the end of 'The Hypothesis System' section, add one sentence: 'For the full hypothesis lifecycle — confidence stages, when to surface them, and expiry rules — see [Guide 05, Part 4](./05_TASK_LEARNING_GUIDE.md#part-4-the-hypothesis-system).'",
    "confidence": "HIGH",
    "status": "PENDING"
  },
  {
    "id": "PROP-002",
    "proposed": "2026-04-01",
    "title": "Add 'File' column to Applied Fixes table in Guide 06 template",
    "rationale": "Guide 05's Applied Fixes template was updated this run (FIX-002) to include a 'File' column, matching the actual IMPROVEMENTS.md implementation. Guide 06 still lacks this column. Aligning them makes both templates consistent.",
    "change": "In Guide 06, change the Applied Fixes table header from '| Date | ID | What was changed | Why |' to '| Date | ID | File | What was changed | Why |' and update the placeholder row accordingly.",
    "confidence": "HIGH",
    "status": "PENDING"
  }
]
```

---

## Known Issues

*(Unresolved limitations or bugs observed in operation.)*

| ID | Description | First observed | Status |
|----|-------------|----------------|--------|
| ISS-001 | TASK.md contains hardcoded session path (`/sessions/busy-exciting-hypatia/`) which differs per session. The scheduled task prompt works around this, but the file itself is stale. | 2026-03-26 | ACCEPTED |

---

## Improvement Backlog

*(Unvalidated learnings and low-priority ideas. Each entry notes what evidence would promote it to a proposal.)*

- **Skills-first setup path (2 observations):** Setup shows 11 skills (many are platform plugins) but no CLAUDE.md or auto-memory across two runs. May suggest the "recommended starting path" (01 → 02 → 03) is unnecessarily rigid, or that platform-level config replaces CLAUDE.md for some users. *Promote to proposal if:* a third observation confirms user-created skills active without CLAUDE.md/memory, or user reports the ordering advice was unhelpful. Note: most skills observed appear to be third-party platform plugins, which weakens this signal.
