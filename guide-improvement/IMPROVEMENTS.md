# Guide Improvement Log — Claude Teacher

> Managed by the guide-improvement task. Read at the start of every run (Step 1). Updated at the end of every run (Step 9).
> Respond to proposals by annotating them [APPROVED], [REJECTED], or [MODIFY: ...] directly in this file.

---

## Counters

```json
{
  "total_runs": 5,
  "runs_since_last_refactor": 5,
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
| 2026-04-08 | FIX-020 | Multiple guides + TASK.md | Expert review: 14 fixes across all guides — hardcoded paths, LAST_RUN.md contradiction, Chrome MCP update, scheduling, memory clarification, Plan Mode, subagents, computer use, project-level MCP settings, scripts/ explanation, .claudeignore link, Guide 07 header, Guide 12 bundled in skill | Full expert audit pass |
| 2026-04-08 | FIX-010 | `00_INDEX.md` + `skills/ai-assistant-setup/references/00_INDEX.md` | "All 11 guides" → "All 12 guides" | Guide 12 (12_LLM_WIKI.md) now bundled in skill references (PROP-004) |
| 2026-04-08 | FIX-009 | `05_TASK_LEARNING_GUIDE.md`, `templates/TASK_TEMPLATE/LESSONS.md`, `templates/TASK_TEMPLATE/README.md` | Added LESSONS.md as optional companion file: new section in Guide 05 Part 6, placeholder file in TASK_TEMPLATE, README updated | PROP-003: preserves reasoning history separate from IMPROVEMENTS.md for complex long-running tasks |
| 2026-04-08 | FIX-008 | `00_INDEX.md` + `skills/ai-assistant-setup/references/00_INDEX.md` | `claude-assistant-setup/` → `ai-assistant-setup/` in skill install instructions (both copies) | Wrong folder name — actual skill folder and .skill file are named `ai-assistant-setup` |
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

*(No proposals currently pending. PROP-003 and PROP-004 were applied on 2026-04-08.)*

---

## Known Issues

*(Unresolved limitations or bugs observed in operation.)*

| ID | Description | First observed | Status |
|----|-------------|----------------|--------|
| ISS-001 | TASK.md contains hardcoded session path (`/sessions/busy-exciting-hypatia/`) which differs per session. | 2026-03-26 | RESOLVED — FIX-020 replaced with relative paths |

---

## Improvement Backlog

*(Unvalidated learnings and low-priority ideas. Each entry notes what evidence would promote it to a proposal.)*

- **Skills-first setup path (2 observations):** Setup shows skills active but no CLAUDE.md or auto-memory across two runs. Most appear to be third-party platform plugins. *Promote to proposal if:* a third observation confirms user-created skills active without CLAUDE.md/memory, or user reports the ordering advice was unhelpful.

- **ISSUES_LOG.md pattern (1 observation, AI-Assistant):** A separate production issues log per task (connector errors, logic issues, missed items), distinct from IMPROVEMENTS.md Known Issues. Useful for connector-heavy tasks. *Promote to proposal if:* observed in a second independent project.

- **Maintenance meta-task (1 observation, AI-Assistant):** A dedicated scheduled task for reviewing and proposing improvements to other tasks. Powerful for setups with 3+ tasks. *Promote to proposal if:* user mentions wanting this pattern, or observed in a second project with multi-task setup.
