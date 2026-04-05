# Guide Improvement Review — Run 2

**Date:** 2026-04-01
**Runs since last refactor:** 2 / 6

---

## Direct Fixes Applied

- `05_TASK_LEARNING_GUIDE.md` — Applied Fixes template table header: "What changed" → "What was changed"; added missing "File" column to match Guide 06 template and actual IMPROVEMENTS.md (FIX-002)

---

## Proposals Pending Review

- **PROP-001** — Add cross-link in Guide 03 to Guide 05's hypothesis lifecycle. Guide 03 introduces hypotheses with a simple inline format but doesn't reference Guide 05's full treatment (confidence stages, lifecycle, surfacing criteria, expiry). One sentence pointing from Guide 03 to Guide 05 Part 4 would close this gap.

- **PROP-002** — Align Applied Fixes table in Guide 06 template to include a "File" column. Guide 05 was fixed this run (FIX-002); Guide 06 still lacks the column. Low priority.

---

## Unvalidated Learnings

- **Skills-first setup (run 2):** Still 11 skills installed, still no CLAUDE.md or auto-memory. However, most skills appear to be platform plugins (docx, pdf, pptx, xlsx, etc.) — not user-created. Pattern may reflect plugin installation rather than deliberate ordering choice. *Promote to proposal if:* third observation confirms user-created skills active without CLAUDE.md/memory, or user reports the guide's recommended ordering was unhelpful.

---

## Live Setup Notes

- 11 skills installed (up from ~3 in run 1). Several carry LICENSE.txt files indicating third-party/platform origin. User-created skills appear to be: finnish-message-assistant, grocery-list-assistant.
- No CLAUDE.md and no auto-memory files; both remain absent as of run 2.
- All skill descriptions are well-formed; strong trigger language consistent with Guide 02 recommendations.
- All cross-references between guides verified intact. Formatting consistent across all 8 guide files.
- Hypothesis format differs between Guide 03 (inline "H-001" notation) and Guide 05 (structured "[HYPOTHESIS]" prefix with lifecycle fields) — no cross-link between them. Captured as PROP-001.
