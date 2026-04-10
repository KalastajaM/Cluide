# Task: Audit CLAUDE.md

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-claude-md.md`
> **Source guides:** `01_CLAUDE_MD.md`, `07_BEST_PRACTICES.md`

## Purpose
Review an existing `CLAUDE.md` against best-practice criteria: every line should change behaviour, the file should be short, and it should cover identity, style, and critical rules — nothing else. Flags dead rules, missing sections, over-length, and common mistakes.

---

## Instructions

### Step 1 — Locate and read the file

```bash
ls CLAUDE.md 2>/dev/null && echo "found" || echo "missing"
```

- If missing: say "No `CLAUDE.md` found. Run `tasks/setup-claude-md.md` to create one." Stop here.
- If found: read the file and count the lines of real content (exclude blank lines and comments).

### Step 2 — Run the audit checklist

Evaluate each criterion. For each, mark ✓ (pass), ⚠ (concern), or ✗ (fail):

**Length:**
- [ ] Under 30 lines of real content — longer files dilute the effective rules
- [ ] No section exceeds what's needed — no padding or filler

**Structure — required sections:**
- [ ] Has an identity section (who the user is, timezone, language preference)
- [ ] Has a communication style section (format, verbosity, tone, emoji)
- [ ] Has a critical rules section (what Claude must never do + positive counterpart)

**Content quality:**
- [ ] Every line changes behaviour — no line that, if removed, would make no difference
- [ ] No capability lists ("you can use Gmail, Calendar…") — Claude discovers tools itself
- [ ] No workflow steps — those belong in task files
- [ ] No project or contact information — that belongs in profile/memory files
- [ ] Critical rules use strong language ("NEVER", not "try to avoid")
- [ ] Critical rules have a positive counterpart ("NEVER send; always draft first")

**Freshness:**
- [ ] No rules that contradict current actual behaviour (stale rules)
- [ ] No rules for edge cases that come up less than once a month
- [ ] Timezone is explicit (not just "local time")

**Project CLAUDE.md extras (if applicable):**
- [ ] Cross-reference rules are present if the project has linked registers/trackers
- [ ] Project description is one sentence, not a paragraph

### Step 3 — Present findings

Format the report as:

```
CLAUDE.md Audit
───────────────
Length: N lines of real content [✓ under 30 / ⚠ over 30 — consider trimming]

Required sections:
  [✓/✗] Identity
  [✓/✗] Communication style
  [✓/✗] Critical rules

Issues found:
  ⚠ Line N: "[quote]" — [reason this is a problem]
  ✗ Missing: [what's missing and why it matters]
  ✓ [section]: looks good

Overall: [Clean / N issues to address]
```

Then ask:
> "Would you like me to apply fixes? I can rewrite the file, remove specific lines, or just show you what I'd change. Or we can work through it together."

### Step 4 — Apply fixes

Based on the user's choice:

**Option A — Rewrite:** produce a clean version applying all fixes, show the diff, ask for approval, then write.

**Option B — Targeted fix:** for each flagged issue, show the specific change (old → new) and apply after confirmation.

**Option C — Review together:** walk through each issue one at a time, let the user decide what to keep, change, or remove.

After any changes, re-count lines and confirm the file is under 30 lines of real content.

### Step 5 — Confirm

Tell the user:
- How many issues were found and fixed
- Final line count
- "Re-run this audit whenever `CLAUDE.md` feels cluttered, or after a period of frequent updates."
