# Claude Task Self-Improvement & Continuous Learning Guide

*Last reviewed: April 2026*

> A framework for building tasks that get better over time.
> Integrate the relevant sections into any task's TASK.md or TASK_REFERENCE.md.

> **Companion guides:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) covers token efficiency -- set that up first. [Guide 08](./08_SELFIMPROVE_TEMPLATE.md) is a ready-to-use IMPROVEMENTS.md template that implements the system described here.

> **Giving this guide to Claude:**
> "Read 07_TASK_LEARNING_GUIDE.md and add the self-improvement system to my task at [path/to/TASK.md]. Include signal detection, the apply-vs-propose rules, and set up an IMPROVEMENTS.md file using the template in 08_SELFIMPROVE_TEMPLATE.md."
>
> **Faster alternative:** `tasks/setup-self-improving-task.md` adds the full self-improvement scaffolding to any existing task without reading the guide first.

---

## Why This Matters

A task that runs 50 times and makes the same mistakes as run 1 is an expensive script. A well-designed task becomes measurably more accurate, efficient, and contextually aware with each run -- without manual tuning.

This guide covers the mechanics: what to track, when to act, when to ask, and how to avoid failure modes that cause regression or stagnation.

---

## Part 1: What to Learn and Where to Store It

### Four categories of task knowledge

**1. Facts** -- confirmed information. User has validated it, or evidence is unambiguous.
> Store in: profile/knowledge files. Mark `[confirmed: YYYY-MM]` or `[USER-CONFIRMED]`.

**2. Hypotheses** -- uncertain information being tracked. Some evidence, not yet confirmed.
> Store in: a dedicated hypotheses file or section. Mark confidence level. Confirm or revise over time.

**3. Patterns** -- recurring observations. Not confirmed, but consistent enough to act on tentatively.
> Store in: profile/patterns files. Note observation count and source. Promote to fact when confirmed.

**4. Operational state** -- what has been done, what is pending, what has failed.
> Store in: run log, pending actions, improvements log. Never conflate with knowledge.

### File structure for learning

Suggested files (adapt names to task domain):

```
KNOWLEDGE_SUMMARY.md   ← Compact digest, read every run. Hard limit: ~40 lines.
KNOWLEDGE_detail.md    ← Deep knowledge, read only when updating.
HYPOTHESES.md          ← Uncertain beliefs being tracked.
IMPROVEMENTS.md        ← Run counter, applied fixes, proposals, known issues.
RUN_LOG.md             ← Append-only record of each execution.
```

**KNOWLEDGE_SUMMARY.md** is the critical file. It must stay compact -- if it grows, every future run pays the token cost. Enforce its line cap and trim aggressively. Detail files are cheap because they are only read when needed.

---

## Part 2: Detecting Learning Signals

The task must actively scan for signals each run -- not just execute its primary function.

### User feedback signals (highest quality)

| Signal | What it looks like | What to learn |
|--------|--------------------|---------------|
| Explicit correction | "That's wrong, it should be X" | Apply immediately. Record in improvements log. |
| Annotation on output | [DONE] / [SKIP] / [WRONG] on generated items | Apply the annotation; extract the general rule. |
| Manual edit to state file | User directly edits a file the task manages | Reconcile. If a pattern emerges, update instructions. |
| Repeated rejection | Same type of item rejected 2+ times in a row | That item type is being miscategorized; revise the rule. |
| Quick resolution | Task marked done same day it was raised | Priority calibration was correct; reinforce that pattern. |
| Long delay before resolution | Task sat open 14+ days with no action | Priority may have been too high, or action was unclear. |

### Behavioral signals (medium quality)

| Signal | What it looks like | What to learn |
|--------|--------------------|---------------|
| Implicit confirmation | User acts on a suggestion without comment | The suggestion was correct; reinforce the pattern. |
| Ignored suggestion | Suggestion generated every run, never acted on | Either priority too low, or the suggestion is irrelevant -- investigate after 3 runs. |
| Consistent pattern | Same sender / same type / same outcome across runs | Codify as a rule; do not keep rediscovering it. |

### Operational signals (lower quality, but catches bugs)

| Signal | What it looks like | What to learn |
|--------|--------------------|---------------|
| Query returning 0 | Search expected to find something, found nothing | Query may be wrong; try alternative syntax. |
| File operation failure | Write failed, file not found, etc. | Log as known issue; add error handling. |
| Same profile section updated every run | Repeated minor updates to the same section | Consider a structural improvement (new field, new section). |
| Output growing unbounded | Log, summary, or output file getting longer each run | Add a trim/archive policy. |

### How to scan for signals in practice

Add this to the end of the run procedure (after primary work, before writing the log):

```
Scan for feedback signals:
- Did the user annotate any output files since last run? → Process annotations.
- Did the user make any manual corrections to state files? → Reconcile and extract lesson.
- Are there any items that have been open/unresolved for 14+ days? → Flag and review.
- Did any query or operation fail or produce unexpected output? → Log as known issue.
- Are there recurring patterns (3+ observations) not yet codified as rules? → Propose.
```

---

## Part 3: The Apply vs. Propose Decision

This is the most important judgment a task makes. Applying a change the user did not want erodes trust. Proposing everything creates noise and slows improvement.

### Apply directly (no confirmation needed)

Apply when ALL of the following are true:
- The change is clearly correct with HIGH confidence (unambiguous evidence, or explicit user instruction)
- The change is low-risk (reversible, limited scope, does not affect core behavior)
- The scope is narrow (single field, single sentence, single file)
- The change is purely additive (adding a missing entry, correcting a typo, resolving a known error)

**Examples of auto-apply:**
- Correcting a date that was recorded wrong
- Updating a contact's name after user confirms it
- Marking a task resolved after clear evidence of completion
- Adding a sender to the noise list after 5+ consistent observations

### Propose and wait (put in IMPROVEMENTS.md, report in output)

Propose when ANY of the following are true:
- The change affects behavior in a non-obvious way
- The change restructures how information is tracked
- The change modifies core logic (step order, resolution criteria, priority thresholds)
- The change touches 3+ files or 10+ lines
- Confidence is below HIGH
- The user has not explicitly asked for this change

**Examples that need a proposal:**
- Adding a new step to the run procedure
- Changing how items are prioritized or classified
- Adding a new profile section or data structure
- Any change where you are not 100% sure the user would agree

### The two-run rule for proposals

If a proposal has been in IMPROVEMENTS.md for 2+ runs with no response (not approved, not rejected, not modified), treat it as "not a priority" and archive it. Do not let proposals accumulate indefinitely -- they become noise.

---

## Part 4: The Hypothesis System

Use hypotheses for information that is reasonably confident but unconfirmed. They prevent the task from either ignoring uncertain-but-useful knowledge or treating guesses as facts.

### Format

```
[HYPOTHESIS] Description of the belief.
  Evidence: What observations support this.
  Confidence: LOW | MEDIUM | HIGH | CONFIRMED
  First observed: YYYY-MM
  Last checked: YYYY-MM
```

### Lifecycle

```
Unobserved → [HYPOTHESIS LOW] → [HYPOTHESIS MEDIUM] → [HYPOTHESIS HIGH] → [CONFIRMED]
                                                                    ↓
                                                          [USER-CONFIRMED] (user validates)
```

- **LOW → MEDIUM:** Second independent observation, or one strong observation.
- **MEDIUM → HIGH:** Multiple consistent observations across different contexts.
- **HIGH → CONFIRMED:** User explicitly validates, or unambiguous direct evidence.
- **Downgrade:** Contradicting evidence appears → lower confidence, note the conflict.
- **Expire:** No evidence for 6+ months → add `[POSSIBLY OUTDATED]`.

### When to surface hypotheses

Surface a MEDIUM-confidence hypothesis in the task output when:
- Confirming it would change how you handle a current situation
- It has been MEDIUM for 3+ runs without movement
- You have an opportunity to ask naturally (e.g., related question already in the output)

Do not spam hypotheses. One or two per run maximum.

---

## Part 5: The Refactoring System

Small improvements happen every run. Structural improvements -- rethinking how the task is organized -- should happen on a schedule or when triggered by specific conditions.

### Refactor triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| Run count | N runs since last refactor (set threshold at task creation, e.g. 25) | Schedule full refactor |
| File size | Any always-loaded file > 300 lines | Propose consolidation |
| Stale knowledge | Any section not updated in 3+ months | Flag for review |
| Instruction drift | Task instructions contradict observed behavior | Fix small drifts, propose large ones |
| State accumulation | Pending items / open issues > comfortable threshold | Review and prioritize |
| Repeated failure | Same resolution check failing 5+ runs | Revise the check |

### What a refactor does

A refactor is **structural cleanup, not content change**. It should make the system cleaner -- not change what gets surfaced or how the user is served (unless fixing a known problem).

1. Review all knowledge files -- remove stale, duplicate, or contradictory entries.
2. Review instruction file -- remove steps that are never followed or are now outdated.
3. Review pending/open state -- identify orphaned or obsolete items.
4. Review improvements log -- close resolved issues, archive old applied fixes.
5. Reset the run counter.
6. Summarize what was found and changed.

---

## Part 6: The Improvements Log

Every task should have an IMPROVEMENTS.md (or equivalent) that tracks the task's own evolution. This is read every run. The template below is a simplified reference -- the full production template lives at [`templates/TASK_TEMPLATE/IMPROVEMENTS.md`](./templates/TASK_TEMPLATE/IMPROVEMENTS.md), and [Guide 08](./08_SELFIMPROVE_TEMPLATE.md) explains how to install it.

### Template

```markdown
# Task Improvements Log

## Counters
{
  "total_runs": N,
  "runs_since_last_refactor": N,
  "refactor_threshold": 25
}

## Applied Fixes
*(Newest first. Archive when > 10 entries.)*

| Date | ID | File | What was changed | Why |
|------|----|------|-----------------|-----|
| YYYY-MM-DD | FIX-NNN | `filename.md` | Description | Reason |

## Archived Fixes
*(Older entries rotated out of Applied Fixes.)*

## Pending Proposals
*(Proposals awaiting user input. Archive after 2 ignored runs.)*

| ID | Proposed | Title | Status |
|----|----------|-------|--------|
| PROP-NNN | YYYY-MM-DD | Description | PENDING |

[Full proposal JSON blocks below the table]

## Known Issues
*(Active issues being monitored.)*

| ID | Description | First seen | Status |
|----|-------------|------------|--------|
| ISS-NNN | Description | YYYY-MM-DD | OPEN / MONITORING / ACCEPTED |

## Improvement Backlog
*(Low-priority ideas not ready to propose.)*
- Item 1
- Item 2
```

### ID conventions

- `FIX-NNN` -- applied change (auto-applied, no confirmation needed)
- `PROP-NNN` -- pending proposal (awaiting user input)
- `ISS-NNN` -- known issue being tracked

### Proposal JSON format

```json
{
  "id": "PROP-NNN",
  "proposed": "YYYY-MM-DD",
  "title": "Short description",
  "rationale": "Why this improves the task",
  "change": "Exactly what would change and in which files",
  "confidence": "HIGH | MEDIUM | LOW",
  "status": "PENDING | APPROVED | REJECTED | MODIFIED"
}
```

### Optional companion: LESSONS.md

For tasks with connector dependencies, complex resolution logic, or long operational history, a separate `LESSONS.md` can complement IMPROVEMENTS.md.

**The distinction:** IMPROVEMENTS.md tracks *current state* -- what proposals are pending, what fixes have been applied. LESSONS.md preserves *reasoning history* -- the mistake, the root cause, what the fix was and why that approach was chosen. This matters when a task has run 30+ times: you can see why a connector query was redesigned without trying to reconstruct the context from a table row.

**How it works:**
- Append-only -- never edit existing entries, only prepend new ones.
- When applying an approved proposal, log the reasoning here before making the change.
- When fixing a connector bug or logic error, note the root cause and what signal revealed it.

**Minimal format:**

```markdown
## [YYYY-MM-DD] Short description (FIX-NNN or PROP-NNN)
**What happened:** Brief description of the mistake or situation.
**Root cause:** Why it happened.
**Fix applied:** What changed and why this approach was chosen.
```

**When to add it:** Not needed for simple tasks. Add it when:
- The task has external connector dependencies with known quirks
- You find yourself asking "why did we change this?" after a few months of runs
- IMPROVEMENTS.md Applied Fixes is growing faster than it archives and the *why* is getting lost

---

## Part 7: Learning Principles

### Recency beats volume

A pattern observed once last week is more valuable than one observed 20 times last year. Knowledge files should reflect current state, not historical accumulation. Revise actively -- do not just append.

### Corrections are the strongest signal

When the user explicitly corrects something, that correction outweighs 10 indirect observations. Extract the lesson explicitly: not just "X was wrong" but "when Y, the correct behavior is Z."

### Codify recurring observations

If the same observation appears in 3+ consecutive runs without being codified as a rule, codify it now. Do not keep rediscovering the same pattern.

### Do not regress

Before applying a fix, verify it does not break something already working. "New and improved" should never mean "new and broken."

### Distinguish types of knowledge

Treat confirmed facts, hypotheses, and patterns differently. A hypothesis stated as fact, or a pattern applied as a rule before confirmation, leads to confident wrong behavior -- worse than uncertain correct behavior.

### The profile is not a log

Knowledge files should reflect the current best understanding of the subject, not serve as a changelog. Update old entries rather than appending. The run log is where history lives.

### Compactness compounds

A file 50 lines longer than necessary costs tokens on every future run. Over 50 runs, that is 2,500 extra lines of input. Trim aggressively. Archive ruthlessly. The value of old information decays fast.

---

## Part 8: Anti-Patterns

**Hypothesis fossilization** -- hypotheses that sit at MEDIUM confidence for months without movement. Either surface them for confirmation or downgrade them. Do not let them accumulate.

**Proposal graveyard** -- many pending proposals, none acted on. More than 3-4 pending proposals signals a backlog problem. Archive old ones; make new ones more concrete or smaller-scoped.

**Append-only knowledge** -- adding to knowledge files without revising existing entries. Results in contradictions and stale data alongside current data. Always prefer revision over appending.

**Over-applying** -- auto-applying changes that should have been proposals because they seemed "obviously right." Erodes trust when the user finds unexpected changes. When in doubt, propose.

**Under-applying** -- routing clearly correct, low-risk, single-field fixes through the proposal system. Slows improvement and creates noise. Apply typos, wrong dates, and user-confirmed facts directly.

**Learning without acting** -- noting the same pattern in the backlog run after run without proposing or applying a change. A pattern noted 5 times is overdue for a proposal.

**Noisy output** -- surfacing too many hypotheses, suggestions, and questions in a single run. One or two per category is enough. More than that and the user stops reading.
