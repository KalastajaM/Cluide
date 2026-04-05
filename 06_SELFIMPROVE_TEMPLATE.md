# Self-Improvement Log — [TASK NAME]

> Managed by the task. Read every run (in the "Read State" step). Updated every run (in the "Self-Improvement" step).
> The human can respond to proposals by annotating them directly here or in the task's output file with [APPROVED], [REJECTED], or [MODIFY: ...].

> **This is a template.** Copy it into your task folder and rename it `IMPROVEMENTS.md`. See [Guide 05](./05_TASK_LEARNING_GUIDE.md) for the full learning framework this template implements.

> **Giving this to Claude:**
> "Copy 06_SELFIMPROVE_TEMPLATE.md into my task folder at [path/], rename it IMPROVEMENTS.md, fill in the task name, and add the two references to TASK.md described in the 'How to use this template' section."

---

## How to use this template

1. Copy this file into your task folder and rename it (e.g. `IMPROVEMENTS.md`).
2. Reference it in your TASK.md as follows — add to the "Read State" step and the end-of-run step.
3. Replace `[TASK NAME]` above and fill in the `noise_filters` section with any domain-specific noise patterns.
4. Delete this "How to use" section once configured.

**Add to your TASK.md "Read State" step:**
> Read `IMPROVEMENTS.md`. Note `runs_since_last_refactor` — increment it this run. Act on any proposals marked [APPROVED], [REJECTED], or [MODIFY]. Note fixable known issues.

**Add to your TASK.md as a final step before appending the run log:**
> Run the Self-Improvement step: detect feedback signals, check refactor triggers, apply or propose fixes, then write the updated `IMPROVEMENTS.md`.

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

| Date | ID | What was changed | Why |
|------|----|-----------------|-----|
| *(none yet)* | | | |

---

## Archived Fixes

*(Rotated out of Applied Fixes when the table exceeds 10 entries.)*

| Date | ID | What was changed | Why |
|------|----|-----------------|-----|
| *(none yet)* | | | |

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

---

## Self-Improvement Step — Reference Instructions

Include these instructions in your TASK.md as the final step before writing the run log.

### A. Feedback Signal Detection (every run)

**From the human:**
- Did the human correct something in an output file or tell you something was wrong? → Extract the lesson, apply or propose a fix.
- Did the human resolve an item unusually fast? → Priority classification was correct; reinforce for similar cases.
- Did an item sit open 14+ days with no action? → Priority may be too high, or action/context was unclear.
- Did the human skip or ignore a proposal for 2+ runs? → Archive it as "not a priority".

**Operational self-observation:**
- Did any search or lookup return 0 results when it should have found something? → The query may need updating.
- Did the task miss something that only became apparent later? → Add a detection rule.
- Did the task flag something as urgent that didn't need action? → Recalibrate.
- Is the same section being updated every run with identical content? → Consider a structural improvement.
- Did any file operation fail or produce unexpected output? → Log as a known issue.

### B. Refactor Trigger Check (every run)

| Trigger | Condition | Action |
|---------|-----------|--------|
| Run count | `runs_since_last_refactor` ≥ threshold | Run full refactor this run |
| Output file bloat | Any tracked file > 300 lines | Propose consolidation |
| Stale sections | Any section not updated in 3+ months | Flag in output |
| TASK.md drift | Instructions contradict observed behavior | Auto-fix small drifts, propose larger ones |
| Item accumulation | > 8 open items at once | Review and reprioritize |

**When a refactor runs:**
1. Review all tracked files for stale, duplicate, or contradictory content — consolidate.
2. Review TASK.md for steps that are unclear, never followed, or outdated — propose changes.
3. Review open items for ones that can be closed or merged.
4. Reset `runs_since_last_refactor` to 0.
5. Summarize findings in the task output.

### C. Auto-apply vs. Propose

**Apply automatically (no confirmation needed):**
- The fix is clearly correct and low-risk (typo, wrong date, outdated single entry)
- The fix reverses a known previous error
- The fix is purely additive (adding a missing entry, adding a detection note)
- The scope is a single field or sentence in a single file

**Propose and wait for human input:**
- The change affects behavior in a non-obvious way
- The change restructures how information is tracked
- The change modifies TASK.md's core logic
- The change touches 3+ files or 10+ lines
- Confidence is below HIGH

### D. Update IMPROVEMENTS.md (every run)

After A–C, write the updated file:
- Increment `runs_since_last_refactor` and `total_runs`
- Add any new `applied_fixes` entries (with date and reason)
- Add/update `pending_proposals`
- Add/update `known_issues`
- Rotate Applied Fixes → Archived Fixes if list exceeds 10
- Archive resolved known issues
