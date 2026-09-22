# Task: Audit CLAUDE.md

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/audit-claude-md.md`
> **Source guides:** `01_PROJECT_INSTRUCTIONS.md`, `16_BEST_PRACTICES.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

The stable filename audits **project instructions**, not the presence of a Claude file on every platform. Select the effective policy and adapter chain before Step 1: `CLAUDE.md` for Claude-only, `AGENTS.md` plus overrides/ancestors for Codex, shared policy plus adapters for dual-platform, and project instructions plus policy sources for ChatGPT. Run Steps 2–5 against that selection. A thin adapter is healthy when it loads the shared policy; do not flag it for lacking copied identity/style sections.

For a repository policy, required content follows its purpose: scope, conventions, verification and action boundaries. Identity and timezone are required only where the work depends on them. Treat 30 lines as a small-policy heuristic, not a hard failing threshold; check the current native loader limit separately (Guide 35 §9). Check source revision, import/read fallback, contradictory overrides and a fresh-session policy question. Unread app fields or untested loaders are unverified, not “missing CLAUDE.md.”

## Purpose
Review an existing `CLAUDE.md` against best-practice criteria: every line should change behaviour, the file should be short, and it should cover identity, style, and critical rules — nothing else. Flags dead rules, missing sections, over-length, and common mistakes.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Locate and read the file

Resolve the native policy as described above. The shell block and missing-file message below are **Claude-only**. On Codex inspect `AGENTS.md` and its effective overrides; on ChatGPT inspect project instructions and policy sources. A missing Claude file alone never stops an OpenAI audit.

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

**Structure — required where relevant to the selected policy:**
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

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

Then ask:
> "Would you like me to apply fixes? I can rewrite the file, remove specific lines, or just show you what I'd change. Or we can work through it together."

### Step 4 — Apply fixes

Based on the user's choice:

**Option A — Rewrite:** produce a clean version applying all fixes, show the diff, ask for approval, then write.

**Option B — Targeted fix:** for each flagged issue, show the specific change (old → new) and apply after confirmation.

**Option C — Review together:** walk through each issue one at a time, let the user decide what to keep, change, or remove.

After changes, re-count lines, retain necessary rules, check the native loader limit and report the fresh-session result.

### Step 5 — Confirm

Tell the user:
- How many issues were found and fixed
- Final line count
- "Re-run this audit whenever `CLAUDE.md` feels cluttered, or after a period of frequent updates."

## Cross-section consistency

Check that broad default-deny language does not accidentally block actions explicitly permitted elsewhere; one-time and standing approvals keep their stated scope across handoffs. Missing company or project context should block dependent claims, not every useful draft. Look for explicit assumptions, unresolved questions and task-specific permission gates. Check that archive, output and memory rules allow authorised recovery, preservation of returned records and explicit corrections with provenance.

<!-- harvested: 2026-09-22 from a generic executive-support framework review; design review, not production validation -->
