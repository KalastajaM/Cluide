---
name: cowork-optimizer
description: >
  Analyze and optimize a Cowork task or project to make it run faster, use fewer tokens, reduce unnecessary steps, and improve overall structure. Use this skill whenever the user shares a Cowork task or project and asks to optimize, improve, speed up, refactor, or reduce Claude usage. Also trigger when the user says things like "make this more efficient", "this task is slow", "can we trim this down", "review my task", or pastes a Cowork task/project definition and asks for feedback.
---
 
# Cowork Optimizer

Analyze a Cowork task or project definition, identify optimization opportunities, present a prioritized plan, get user sign-off, then implement agreed changes.

> This skill applies the patterns from [06_TASK_EFFICIENCY_GUIDE.md](../../06_TASK_EFFICIENCY_GUIDE.md) and [07_TASK_LEARNING_GUIDE.md](../../07_TASK_LEARNING_GUIDE.md). Read those guides if you want to understand the reasoning behind any recommendation.

## Rules

- Always use this skill before making any edits to a Cowork task or project — even if the user just says "take a look at my task."
- Do not silently apply changes beyond what was agreed in Phase 3.
- Flag tradeoffs explicitly — do not silently optimize toward one axis (speed vs. thoroughness).
 
---
 
## Phase 1: Ingest

**If the content is already in the conversation, skip to Phase 2 immediately.**

Otherwise, attempt to locate the task autonomously before asking the user:

```bash
find /sessions -maxdepth 6 -name "TASK.md" 2>/dev/null
```

If one or more TASK.md files are found, present the list and ask which task to audit. If none are found, ask the user to share the task. They can provide:
- The task instructions pasted directly
- A path to the task file (`.task` or `.md`)
- A Cowork project folder path

If files are referenced inside the instructions (e.g., skill files, reference docs, templates), read those too — optimization depends on understanding the full dependency chain.
 
**Read any referenced skill files.** If the task invokes one or more skills (via `/skill-name` or a `skills:` directive), read those SKILL.md files before auditing. A task may be doing manually what a skill already handles better, or may be loading a skill for a narrow use case that doesn't justify the overhead.
 
Also check whether the task folder contains any of these companion files — they're highly informative for the audit:
- `IMPROVEMENTS.md` — tracks applied fixes, pending proposals, and known issues
- `RUN_LOG.md` — reveals which steps fail repeatedly or take long
- `KNOWLEDGE_SUMMARY.md` — indicates whether state is being carried efficiently between runs
 
**If the content is already in the conversation, skip asking and proceed directly to Phase 2.**
 
---
 
## Phase 2: Audit

Analyze the task/project across nine dimensions. For each finding, note: what it is, why it's a problem, and the effort to fix (Low / Medium / High).

**Read `references/audit-dimensions.md` for the full checklist.** The dimensions are ranked by typical ROI:

| Dimension | Focus | Typical ROI |
|---|---|---|
| 2.1 Token & Context Efficiency | Instruction size, always-loaded files, lazy loading | Highest |
| 2.2 External Data Fetching | Two-pass triage, digest collapsing, recency skips | Highest |
| 2.3 Run Flow Efficiency | Fast-path skips, deduplication, conditional regeneration | High |
| 2.4 Edit Efficiency | Targeted edits vs. full read/write | Medium |
| 2.5 Output & Script Offloading | Fixed-format output → scripts | Medium |
| 2.7 Instruction Clarity | Ambiguity, missing criteria, implicit assumptions | Medium |
| 2.8 Structural / Architectural | Task splitting, script candidates, hardcoded values | Low–Medium |
| 2.9 Self-Improvement Infrastructure | IMPROVEMENTS.md, RUN_LOG.md scaffolding | Low (optional) |

Stop when you are confident there are no further significant findings. Dimensions 2.7–2.9 can be skipped if the task is already efficient.

---

## Phase 3: Present the Plan

**If no findings exceed ~500 tokens per run in estimated impact and none are qualitatively significant (clarity, correctness, structural), say so explicitly and stop:** "This task is already well-optimized. No changes recommended." Do not generate a thin list of minor findings just to appear thorough.

Otherwise, produce a structured audit report in the conversation. Format:

**Summary** — one sentence characterizing the main issues and rough token cost estimate if calculable.

Then a prioritized list of findings, highest ROI first. For each:
- **Finding title** (e.g., "Unconditional large file load in step 3")
- What the problem is
- Proposed fix
- Effort: Low / Medium / High
- Impact: token savings estimate, speed improvement, or qualitative benefit
 
**Token estimation guide:**
| Component | Rough cost |
|-----------|------------|
| Task instruction file | ~15 tokens/line |
| Each "read every run" file | ~15 tokens/line |
| Each external API fetch (full) | 200–2,000 tokens |
| Each file write (generated output) | ~15 tokens/line |
| Script execution | ~50 tokens |
 
**Flag tradeoffs explicitly.** If a proposed change trades thoroughness for speed, say so. Let the user decide — don't silently optimize toward one axis.
 
**Scope note:** Self-improvement infrastructure (IMPROVEMENTS.md, RUN_LOG.md, KNOWLEDGE_SUMMARY.md) is valuable but represents a meaningful addition, not just a cleanup. Present it as an optional enhancement, not a required fix, unless the task already has partial scaffolding.
 
End with: "Which of these would you like me to implement? You can say 'all of them', pick specific numbers, or tell me to skip any."
 
---
 
## Phase 4: Implement
 
Once the user confirms which changes to make:
 
1. **Back up before editing.** Preferred: `git add` and commit the current state so there's a clean restore point. If git is not available, copy the file with a `.bak` suffix. Note the backup location in your response.
2. Apply changes one finding at a time.
3. After each non-trivial change, briefly note what you changed and why (one line).
4. Present the final revised task/project.
5. If the task has test prompts or a known test workflow, suggest running it to verify behavior is unchanged.

**To roll back:** restore from git (`git checkout -- <file>`) or copy the `.bak` file back to its original path and delete the modified version.
 
**Apply vs. propose discipline:**
- Apply directly (no further confirmation): clearly correct, low-risk, narrow-scope changes — typos, wrong dates, confirmed facts, adding a named sender to a noise list.
- Flag and ask before applying: anything that affects behavior in a non-obvious way, restructures how information is tracked, modifies core logic, touches 3+ files, or where you're not certain the user would agree.
 
**Do not silently apply changes beyond what was agreed.** If you spot something while implementing that wasn't in the plan, flag it and ask.
 
---
 
## Phase 5: Wrap-up
 
After implementation:
- Summarize what changed vs. what was left alone (and why, if relevant).
- Note the new estimated TASK.md line count and token cost per run if measurably improved.
- Offer to package/export if the user needs to reinstall the task or share it.
- If the frontmatter `description` is vague or seems to trigger unreliably, offer to rewrite it: a good description names concrete user phrases, specific file types, and clear exclusions. Rewriting it is low-effort and can significantly improve how reliably Claude picks up the skill.

---

## Edge Cases

- If the task file is empty or contains only a title: say "This task has no content to audit. Would you like me to help you write it from scratch instead?" and offer to run `tasks/setup-scheduled-task.md`.
- If the task is under 50 lines and already follows Guide 06 patterns: say "This task is already well-optimized. No changes recommended." Do not invent marginal findings.
- If the user provides a Cowork project folder (not a single TASK.md): read all task files in the folder and audit each independently, presenting findings grouped by file.
- If IMPROVEMENTS.md contains stale proposals (>10 pending, none applied): flag this as a finding — the improvement system itself needs maintenance.
- If the task uses MCP tools that are not configured in the current environment: note this in findings but do not treat it as an optimization issue — it's a setup problem, not an efficiency problem.
