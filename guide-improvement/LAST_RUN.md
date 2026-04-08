# Guide Improvement — Run 4
**Date:** 2026-04-08
**External projects analysed:** AI-Assistant, VCP8 - Business Suite

---

## Direct Fixes Applied

| File | Fix |
|------|-----|
| `00_INDEX.md` | FIX-008: `claude-assistant-setup/` → `ai-assistant-setup/` in skill install instructions |
| `skills/ai-assistant-setup/references/00_INDEX.md` | FIX-008 (mirror): same fix in bundled copy |

---

## Proposals Pending Review

**PROP-003 — Add LESSONS.md as optional companion file for complex tasks**
_From AI-Assistant analysis (34+ runs, 35+ entries)._
Guide 05 and TASK_TEMPLATE cover IMPROVEMENTS.md for structured proposals and fixes, but don't mention a separate chronological mistakes log. The AI-Assistant uses `LESSONS.md` as an append-only record of _why_ changes were made — each applied proposal is logged here before being applied. This keeps IMPROVEMENTS.md focused on current state while LESSONS.md preserves the reasoning history. Suggested addition: a short section in Guide 05 and a placeholder file in TASK_TEMPLATE describing LESSONS.md as an optional companion for tasks where audit trail matters.

**PROP-004 — Add Guide 12 to ai-assistant-setup skill references**
Guide 12 (`12_LLM_WIKI.md`) exists in the repo but is not bundled in the skill. The skill description currently says "All 11 guides" which is accurate (01–11 are bundled), but a user who installs the skill and asks about LLM wikis won't have access to it. Proposal: copy `12_LLM_WIKI.md` into `skills/ai-assistant-setup/references/` and update the description to "All 12 guides".

---

## Unvalidated Learnings

- **ISSUES_LOG.md pattern** (from AI-Assistant): a separate production issues log (connector errors, logic issues, missed items) kept per task, distinct from IMPROVEMENTS.md. Used across 3 of 4 tasks in a mature 34-run setup. Useful for connector-heavy tasks. Not general enough to add to guides yet — needs evidence from a second independent project. Added to backlog.

- **Maintenance meta-task** (from AI-Assistant): a dedicated scheduled task that reviews and proposes improvements for the other tasks. Powerful pattern for complex multi-task setups. Single project evidence, advanced use case only. Added to backlog.

---

## External Project Analysis

**AI-Assistant** — mature setup, 34+ runs. Most patterns already covered in guides (TASK_REFERENCE.md, pre-run snapshot, dedup guard, two-pass triage, Python scripts for output generation). Two novel patterns surfaced: LESSONS.md (→ PROP-003) and ISSUES_LOG.md (→ backlog).

**VCP8 - Business Suite** — CLAUDE.md only, no task or skill files. Content closely matches the PMO_TEMPLATE just added — confirms the template reflects real usage accurately. No new patterns to surface.

---

## Live Setup Notes

No CLAUDE.md or memory files at user home level — consistent with prior runs.
