---
name: backlog
description: >
  Portable project backlog manager. Use this skill whenever the user wants to review, prioritize, or add to the project backlog — including requests like "/backlog", "/backlog groom", "add this to the backlog", "what should we work on next", "let's review the backlog", "backlog session", or "what's in the backlog". Also triggers when the user brings a new idea or improvement suggestion and wants it tracked. The skill handles initialization automatically if no backlog files exist yet.
---

# Backlog Management

A lightweight, portable backlog system. Each project has two files: `BACKLOG.md` (the living idea list) and `DECISIONS.md` (the architectural decision log). This skill defines how to run sessions against those files.

## Core Responsibilities

- Load and normalize `BACKLOG.md` and `DECISIONS.md` at the start of every session
- Orient the user: counts, blocked items, dependency readiness, and conflicts
- Check new ideas against past decisions before adding them
- Propose a prioritized pick order and confirm the user's selection
- Write all outcomes back to files before ending the session
- Guard against re-litigating closed decisions

## File Formats

### BACKLOG.md — item format

```markdown
## BL-001 — Short descriptive title

**Status:** open | in-progress | blocked | closed | rejected
**Category:** feature | improvement | fix | architecture | ops
**Tags:** optional, free-form
**Dependencies:** BL-004 (reason — must ship first)
**Conflicts-with:** BL-007 (reason — mutually exclusive approaches)
**Added:** YYYY-MM-DD

One paragraph: what the idea is and why it matters.
```

Required fields: `Status`, `Category`, `Added`. All others are optional, filled in as needed.

Closed/rejected items collapse to a single line at the bottom under `## Closed`:
```
- BL-001 — Title [closed YYYY-MM-DD → DEC-001]
```

### DECISIONS.md — decision format

```markdown
## DEC-001 — Title of the decision

**Date:** YYYY-MM-DD
**Related:** BL-001, BL-003
**Decision:** implemented | rejected | deferred | superseded
**Rationale:** Why — the reasoning that must not be forgotten
**Trade-offs:** What was given up or left open
```

Entries are append-only. If a past decision is ever reversed, add a new entry referencing the old DEC-NNN rather than editing it.

---

## Session Modes

### Standard session (`/backlog`)

Run these steps in order:

**1. Load state.** Read `BACKLOG.md` and `DECISIONS.md` from the project root (Read tool). If either file is missing, follow the Initialization section below first.

**2. Normalize any manual additions.** If `BACKLOG.md` contains raw notes or unnormalized text (no `## BL-NNN` heading, missing required fields), normalize them into proper format before proceeding. Assign the next available ID.

**3. Orient.** Show a concise summary:
- Open items grouped by category, with counts
- Any items with `Status: blocked` and what's blocking them
- Any items whose dependencies just became satisfiable (all `Dependencies` items are now closed)
- Items with unresolved `Conflicts-with` tags

Example orient output:

```
**Backlog — 8 open items**

| Category     | Count |
|--------------|-------|
| feature      | 4     |
| improvement  | 2     |
| architecture | 1     |
| fix          | 1     |

**Blocked:** BL-003 (waiting on BL-001 — auth must ship first)
**Ready (deps met):** BL-005 (BL-001 now closed)
**Conflict:** BL-006 ↔ BL-007 (mutually exclusive approaches — must resolve before picking either)
```

**4. New item intake.** If the user has brought new ideas (in this message or earlier in the conversation), before adding them: check each against `DECISIONS.md` for conflicts with past decisions. If a proposed item overlaps with a rejected decision, flag it and explain the prior reasoning before asking whether to add anyway.

**5. Prioritization.** Propose a prioritized ordering of open items with brief reasoning (value, dependencies, risk, effort). The user adjusts. Lead with your recommendation — don't just list items.

**6. Pick work.** The user selects item(s) to act on next. Before confirming, check:
- Does the item have unresolved `Dependencies`? Flag if so.
- Does the item have active `Conflicts-with`? Flag if so — both items can't be "next".
Items with unresolved conflicts or unsatisfied dependencies are blocked from being picked until cleared.

**7. Write outcomes.** Update `BACKLOG.md` with any status changes, new items, or field updates (Edit tool). For any item that is closed or rejected, collapse it to a one-liner and append a corresponding entry to `DECISIONS.md` (Edit tool).

---

### Grooming session (`/backlog groom`)

Same as standard, but insert a **full architecture review** between Orient and Prioritization:

- **Redundancy check**: Identify items that overlap significantly or duplicate each other. Propose merging or replacing.
- **Hidden conflicts**: Look for items that haven't been tagged `Conflicts-with` but would pull the architecture in incompatible directions if both were implemented. Tag them.
- **Obsolescence check**: Are any items superseded by work already done, or by other backlog items that make them irrelevant? Flag for closing.
- **Dependency chains**: Trace all dependency chains. Flag cycles. Identify bottlenecks (items that many others depend on) and surface them for prioritization.
- **Architecture coherence**: Step back and read all open items as a set. Do they form a coherent direction? Is there drift between categories (e.g., features pulling away from a stated architectural goal)? Surface observations.

After the review, present findings before prioritizing. The user may want to resolve some findings before picking work.

---

### Adding items interactively (outside a session)

When the user says "add this to the backlog" or similar during any session:

1. Assign the next available `BL-NNN` ID (Read tool — scan current max from `BACKLOG.md`).
2. Check the proposed item against `DECISIONS.md` before writing — if it conflicts with a past decision, flag it first.
3. Write the item to `BACKLOG.md` in proper format (Edit tool), asking for any missing required fields if they're not obvious from context.

---

## Initialization

When `BACKLOG.md` doesn't exist in the project root:

1. Create `BACKLOG.md` with this skeleton (Write tool):

```markdown
# Backlog

Items are tracked as BL-NNN. Closed items collapse to one-liners at the bottom. See DECISIONS.md for architectural decision log.

## Open

## Closed
```

2. Create `DECISIONS.md` with this skeleton (Write tool):

```markdown
# Architectural Decisions

Entries are append-only. Each decision records what was decided and why, so future sessions don't re-litigate closed questions.
```

3. Scan the project for any existing idea files: `IMPROVEMENTS.md`, `TODO.md`, `IDEAS.md`, `NOTES.md`, or similar. If found, offer to import them as draft items — the user reviews each one before it gets a BL-NNN ID.

4. After initialization, proceed with a standard session.

---

## Constraints

> Claude writes to `BACKLOG.md` and `DECISIONS.md` but does not commit to git. Committing is the user's responsibility — the files belong in git.

---

## Tone & Format

Output should be concise and structured with markdown headers, tables, and lists. Avoid prose-heavy summaries — a table of counts is better than a paragraph describing them. No emoji unless the user uses them. When the backlog has no open items, say so in one sentence rather than showing empty sections.

---

## Edge Cases

- **BACKLOG.md is not in the project root:** Use it wherever it is and note the location at the top of the orient summary. Do not move it.
- **DECISIONS.md is missing but BACKLOG.md exists:** Create `DECISIONS.md` with the standard skeleton (Write tool) and continue — do not trigger full re-initialization.
- **More than 20 open items:** In the orient summary, show counts by category only. Do not list all items individually — offer to show a specific category on request.
- **User adds an item mid-session without an explicit command:** Treat it as "Adding items interactively." Assign an ID, check decisions, write it, and continue the session.
- **Proposed item conflicts with a past decision:** Present the prior decision verbatim (Rationale + Trade-offs) before asking whether to add anyway. Do not add silently.

---

## Key Principles

**DECISIONS.md is the memory.** Claude reads it at the start of every session. Its purpose is to prevent re-proposing ideas that were already deliberated — the single biggest source of wasted refactoring in AI-assisted projects. A good entry in DECISIONS.md is worth more than a well-written BACKLOG.md item.

**Conflicts block selection.** An item tagged `Conflicts-with: BL-007` cannot both be "next". The conflict must be resolved (one item closed/rejected, or the conflict tag removed with explanation) before either can be picked.

**Dependencies block selection too.** An item with unsatisfied `Dependencies` is not available to pick. Surface these as blocked in the Orient step.

**The backlog belongs in git.** `BACKLOG.md` and `DECISIONS.md` are design artifacts — commit them. They are not personal data and should not be gitignored.

**No Claude memory needed.** `BACKLOG.md` and `DECISIONS.md` are the persistence layer. Do not write backlog state to Claude's persistent memory.

**This skill is project-agnostic.** Nothing in it assumes a specific project, language, or domain. The skill works identically in any project that has the two files.

---

## Example Interaction

**User:** `/backlog` — also I've been thinking we should add dark mode

**Assistant:**

> **Backlog — 5 open items**
>
> | Category    | Count |
> |-------------|-------|
> | feature     | 3     |
> | improvement | 1     |
> | fix         | 1     |
>
> **Blocked:** BL-003 (waiting on BL-001)
> **Ready:** BL-002 (BL-001 now closed)
> No unresolved conflicts.
>
> **New idea — dark mode:** Checking past decisions... DEC-002 deferred this as "post-MVP, revisit when design system is stable." Still want to add it?

**User:** Yeah, add it — design system is done now.

**Assistant:**

> Added as **BL-006 — Dark mode support** (feature, open, 2026-04-11).
>
> **Proposed priority:**
> 1. BL-002 — API rate limiting *(unblocked, high risk if skipped)*
> 2. BL-005 — Export to CSV *(low effort, high user value)*
> 3. BL-006 — Dark mode *(new, design system now ready)*
> 4. BL-004 — Onboarding flow *(depends on BL-002)*
>
> Which item do you want to take next?

**User:** BL-002.

**Assistant:**

> BL-002 updated to `in-progress`. BACKLOG.md written.
