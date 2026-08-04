# Self-Improvement Log — [TASK NAME]

> Managed by the task. Read every run (in the "Read State" step). Updated every run (in the "Self-Improvement" step).
> The human can respond to proposals by annotating them directly here or in the task's output file with [APPROVED], [REJECTED], or [MODIFY: ...].

---

## Counters

```json
{
  "total_runs": 0,
  "runs_since_last_refactor": 0,
  "refactor_threshold": 25,
  "last_refactor_date": null,
  "next_refactor_due_at_run": 25
}
```

*Adjust `refactor_threshold` based on run frequency. For daily runs: 25–30. For weekly runs: 10–15.*

---

## Noise Filters

*Domain-specific patterns that are always noise. Collapse these to a count in the run log rather than processing individually. Add a new entry after observing 5+ structurally identical instances over multiple runs, or when the human confirms an item is noise.*

| Pattern / Sender | Description | Added |
|-----------------|-------------|-------|
| *(example)* | *(e.g. "Weekly digest from X — always identical structure, no actionable content")* | YYYY-MM-DD |

**Still process individually if:** the item deviates from its typical pattern, matches a tracked keyword or active project, or would qualify as actionable.

---

## Applied Fixes

*(Auto-applied fixes, newest first. Archive to "Archived Fixes" when this list exceeds 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|
| *(none yet)* | | | | |

---

## Archived Fixes

*(Rotated out of Applied Fixes when the table exceeds 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|
| *(none yet)* | | | | |

---

## Pending Proposals

*(Larger changes awaiting human input. Human responds by annotating here or in the task output file.)*

```json
[
  {
    "id": "PROP-001",
    "proposed": "YYYY-MM-DD",
    "title": "Short description of the change",
    "rationale": "Why this would improve the task's output or efficiency",
    "change": "Exactly what would change — which file, which step, what wording",
    "confidence": "HIGH | MEDIUM | LOW",
    "status": "PENDING | APPROVED | REJECTED | MODIFIED"
  }
]
```

*(No proposals currently pending.)*

---

## Known Issues

*(Unresolved limitations or bugs observed in operation.)*

| ID | Description | First observed | Status |
|----|-------------|----------------|--------|
| *(none yet)* | | | |

---

## Improvement Ideas Backlog

*(Low-priority ideas not yet ready to propose. Add here to avoid losing them.)*

- *(none yet)*


> **Note:** The canonical self-improvement instructions live in TASK.md Step 6. Do not duplicate them here.
