---
name: project-analyzer
description: >
  Analyze another Claude project — Claude Code or Cowork, from a local folder or a GitHub repo —
  against the full Cluide guide set and produce a written improvement plan. Use whenever the user wants
  a whole-project health check or improvement plan for a Claude setup other than the obvious one in
  front of them. Trigger on phrases like "analyze my other Claude project", "review this repo's Claude
  setup against Cluide", "audit my whole assistant setup", "what should I improve in my Claude project",
  "generate an improvement plan for <project>", or "score my project against the Cluide guides".
  Not for optimizing a single Cowork task's efficiency — use the cowork-optimizer skill for that.
---

# Project Analyzer

Analyze another Claude project against the full Cluide guide set and write a single, reviewable
improvement plan (`CLUIDE_IMPROVEMENT_PLAN.md`) into that project. Read-only on the target except for
that one file; it produces a reviewed plan and **stops** — it does not implement changes.

> **This skill is a thin router.** The full procedure lives in `tasks/analyze-project.md` and its
> criteria/template in `tasks/analyze-project-reference.md`. Do not duplicate that logic here — run the
> task and follow it. Keeping a single source of truth avoids the bundled-copy drift that
> `tasks/review-tasks.md` checks for.

## Rules

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons
> instead of plain text.

- This skill must run from a **Cluide checkout** — the analysis criteria reference the root guides
  (`00_INDEX.md` and the numbered guides). If the guides aren't present in the working context, locate
  the Cluide repo, or tell the user to run this from Cluide, and stop.
- Plan-only: never edit the target's `CLAUDE.md`, skills, tasks, settings, or config. The only write is
  `CLUIDE_IMPROVEMENT_PLAN.md` at the target root.
- Never copy secret or credential **values** into the plan — reference their location only.

## What to do

1. Read `tasks/analyze-project.md` and execute it end-to-end (Steps 0–6): locate the target
   (local folder or GitHub repo) → inventory and detect type → clarify intent → analyze against the
   dimensions → draft for review → write the final plan and stop.
2. Use `tasks/analyze-project-reference.md` for the per-dimension criteria, project-type detection
   signals, input handling, and the exact output template.

That's it — the task owns the workflow; this skill just makes it triggerable from natural language.
