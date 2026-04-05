# Guide Improvement Log — Claude Teacher

> Managed by the guide-improvement task. Read at the start of every run (Step 1). Updated at the end of every run (Step 7).
> Respond to proposals by annotating them [APPROVED], [REJECTED], or [MODIFY: ...] directly in this file.

---

## Counters

```json
{
  "total_runs": 3,
  "runs_since_last_refactor": 3,
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
| 2026-04-05 | FIX-007 | `guide-improvement/IMPROVEMENTS.md` | Closed PROP-001 and PROP-002; incremented run counters | Both proposals were applied in this run |
| 2026-04-05 | FIX-006 | `04_TASK_EFFICIENCY_GUIDE.md` | Added "How Scheduled Tasks Are Triggered" section with hooks config example | Guides mentioned scheduled tasks but never explained how they are actually triggered |
| 2026-04-05 | FIX-005 | `06_SELFIMPROVE_TEMPLATE.md` | Added "File" column to Applied Fixes and Archived Fixes tables | Resolved PROP-002: aligns template with Guide 05 and the actual IMPROVEMENTS.md format |
| 2026-04-05 | FIX-004 | `03_MEMORY_AND_PROFILE.md` | Added cross-link from Hypothesis System section to Guide 05 Part 4 | Resolved PROP-001: readers of Guide 03 now know the full hypothesis lifecycle is in Guide 05 |
| 2026-04-05 | FIX-003 | `03_MEMORY_AND_PROFILE.md` | Added "Memory File Format" section showing MEMORY.md index and individual file format | Gap: guide described memory files but never showed what they look like |
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
[]
```

*(No proposals currently pending. PROP-001 and PROP-002 were applied as FIX-004 and FIX-005 on 2026-04-05.)*

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
