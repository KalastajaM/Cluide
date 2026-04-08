# IMPROVEMENTS.md
> Maintained by the assistant. Updated at the end of every run (Step 9D).
> LESSONS.md is the append-only history log. This file is the live state.

---

## Run Counter

```
runs_total: 0
runs_since_last_refactor: 0
last_refactor_date: —
last_self_review_date: —
```

---

## Pending Proposals

*None.*

---

<!-- Template for new proposals:
### PROP-NNNN — [Short title]
- **Status:** PENDING | APPROVED | REJECTED
- **Raised:** YYYY-MM-DD
- **Type:** schema | run-procedure | output-template | profile | connector | other
- **Rationale:** [Why this change would improve the assistant]
- **Confidence:** LOW | MEDIUM | HIGH
- **Proposed change:** [Specific edit — be precise enough to apply without ambiguity]
- **Risk:** [What could go wrong if applied]
-->

---

## Applied Fixes

| Date | ID | Title | Type | Details |
|------|----|-------|------|---------|

---

## Scheduled Tasks

| Task ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| `business-assistant` | Daily business assistant (this task) | ✅ Enabled | |
| `friday-weekly-plan` | Friday weekly planner | ✅ Enabled | |
| `urgent-scan` | Mid-day urgent scan | ✅ Enabled | Output: ACTIONS_URGENT.html |
| `weekly-maintenance` | Monday profile/knowledge/PA cleanup | ✅ Enabled | Output: MAINTENANCE_REPORT.md |

---

## Known Issues

*No known issues.*

---

## Digest Senders

Automated/notification senders confirmed to be collapsed under Step 3A-1.

| Sender / Domain | Type | Added |
|-----------------|------|-------|
| *none yet — populate from first run with digest traffic* | | |

---

## Refactor Trigger Status

| Trigger | Threshold | Current | Status |
|---------|-----------|---------|--------|
| runs_since_last_refactor | ≥ 25 | 0 | OK |
| Open PAs | > 8 | 0 | OK |
| TASK.md line count | > 600 | — | OK |
| Repeated resolution failures | ≥ 3 same PA | 0 | OK |
