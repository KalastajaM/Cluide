# Guide Improvement Review — TASK.md

> Periodic review task for the "Claude Teacher" guide collection.
> Scans live setup files and the guides themselves to find improvements.
> Applies unambiguous fixes directly; validates new learnings before adding.

> **Companion files:** `IMPROVEMENTS.md` (state), `LAST_RUN.md` (latest output), `REVIEWED.md` (deduplication log)

---

## Paths

| Item | Path |
|------|------|
| Guide folder | `/sessions/busy-exciting-hypatia/mnt/Claude Teacher/` |
| Task folder | `/sessions/busy-exciting-hypatia/mnt/Claude Teacher/guide-improvement/` |
| Skills folder | `/sessions/busy-exciting-hypatia/mnt/.claude/skills/` |
| CLAUDE.md | `/sessions/busy-exciting-hypatia/mnt/.claude/CLAUDE.md` (may not exist) |
| Memory index | `/sessions/busy-exciting-hypatia/mnt/.auto-memory/MEMORY.md` (may not exist) |

---

## Run Procedure

### Step 1 — Read State

Read `guide-improvement/IMPROVEMENTS.md`.
- Note `total_runs` and `runs_since_last_refactor` — you will increment both at the end.
- Act on any proposals marked [APPROVED], [REJECTED], or [MODIFY: ...].
- Note any fixable known issues.

---

### Step 2 — Scan Guide Files for Internal Issues

Read all guide files in `Claude Teacher/` (files matching `0*_*.md`).

For each file, check for:
- **Broken cross-references** — "See Guide 04" pointing to a wrong filename, or a section that no longer exists.
- **Inconsistencies** — conflicting advice on the same topic across guides.
- **Stale examples** — references to features, workflows, or tools no longer in use.
- **Missing cross-links** — e.g. Guide 02 should reference Guide 04's efficiency tips when discussing scheduled tasks; Guide 03 should reference Guide 05's learning framework.
- **Formatting drift** — headers or structure that don't match the rest of the collection.

**Apply directly** (no confirmation): broken links, typos, clearly wrong factual statements (e.g. wrong filename in an example), duplicate sentences.

**Propose**: any section rewrites, new content, restructuring, or additions longer than ~3 lines.

---

### Step 3 — Scan Live Setup for Signals

Read each SKILL.md in the skills folder. If CLAUDE.md exists, read it. If the memory index exists, read `MEMORY.md` and any memory files it references.

For each file, assess three things:
1. **Gaps** — does it diverge from the guide's recommendations in a way that worked? Note as a potential guide addition.
2. **Missing patterns** — does it do something useful that the guide doesn't cover at all?
3. **Contradictions** — does it contradict guide advice? Determine which is more reliable based on evidence.

Do NOT add every observation to the guide. Apply the validation filter in Step 4 first.

Before scanning, read `REVIEWED.md` and note which source files and findings have already been evaluated. Skip any finding that already has a REVIEWED.md entry — do not re-surface it.

---

### Step 4 — Validate Learning Candidates

Before proposing any "new learning" as a guide addition, apply this filter:

**A. Is there clear, repeated evidence this pattern works?**
Not a one-time setup choice or an experiment that may not have been tested. Look for corroborating signals across multiple files or sessions.

**B. Would this advice be useful to someone setting up from scratch?**
If it's highly specific to this user's workflow or domain, it belongs in their CLAUDE.md — not in a general guide.

**C. Does it contradict existing guide content?**
If yes: which is more reliable? If uncertain, log as an unvalidated hypothesis rather than proposing a change.

Candidates passing all three → propose as guide addition.
Candidates failing any → add to the IMPROVEMENTS.md backlog under "Unvalidated learnings" with a note on what evidence is still needed.

---

### Step 5 — Write Summary Output

Write `guide-improvement/LAST_RUN.md` with:
- Run date and number
- **Direct fixes applied** — each as: `[filename] — description`
- **Proposals pending review** — each as: 1-line summary + ID (e.g. PROP-001)
- **Unvalidated learnings** — what was observed, what evidence would confirm it
- **Live setup notes** — informational observations (gaps, interesting patterns); not prescriptive

Keep this file under 60 lines. It is the human-facing output for this run.

---

### Step 6 — Refactor Check

If `runs_since_last_refactor` ≥ `refactor_threshold` (default: 6):
1. Review all guide files for stale, contradictory, or redundant content — consolidate where possible.
2. Review IMPROVEMENTS.md: archive old proposals (2+ ignored runs), close resolved issues.
3. Check whether any "unvalidated learnings" have now accumulated enough evidence to propose.
4. Reset `runs_since_last_refactor` to 0, update `last_refactor_date`.
5. Note the refactor summary in `LAST_RUN.md`.

---

### Step 7 — Append to REVIEWED.md

For every finding evaluated this run (whether applied, proposed, skipped, or rejected), append one line to `REVIEWED.md`:

```
[YYYY-MM-DD] [source file] [brief description of the finding] — [disposition]
```

This prevents the same finding from being re-surfaced in future runs.

---

### Step 8 — Update IMPROVEMENTS.md

Write the updated `IMPROVEMENTS.md`:
- Increment `total_runs` and `runs_since_last_refactor`
- Add new applied fixes to the Applied Fixes table
- Add new proposals to Pending Proposals
- Update Known Issues
- Archive Applied Fixes if table exceeds 10 entries
- Add unvalidated learnings to the Improvement Backlog with their validation criteria
