# Best Practices: Writing CLAUDE.md for a Personal Assistant

*Last reviewed: April 2026*

CLAUDE.md is the always-loaded instruction file that shapes every interaction. It is the difference between an assistant that constantly needs re-explaining and one that just gets it. This document covers what to put in it, how to structure it, and what to avoid.

---

## What CLAUDE.md Is For

CLAUDE.md loads into every conversation automatically. It answers the question: "Before I do anything, what do I need to know about this person and how they want to work?" It is not a task list and not a knowledge base — it is the standing operating contract between you and the assistant.

The key principle: **every line should change behaviour.** If removing a line wouldn't change how the assistant acts, cut it.

---

## Core Sections

### 1. User Identity

Give the assistant a confident mental model of who it is serving. Include:

- Name and location (city + country)
- Language(s) spoken and language of preference for assistant responses
- Timezone — critical for scheduling, deadlines, and timestamping
- Relevant roles (e.g., "Director at X company", "manages affairs for elderly parent")

**Example:**
```markdown
# About [User]
- Software engineer, based in Singapore
- Timezone: Asia/Singapore (SGT, UTC+8)
- Respond in English always
- Works across US, EU, and APAC teams — flag when a message is likely to reach
  someone outside business hours
```

What makes this effective: it is specific enough to resolve edge cases — the assistant knows to flag time-zone considerations when scheduling, and responds in English even if the user pastes content in another language.

### 2. Communication Style

Tell the assistant exactly how to format and phrase responses. The default Claude style — bullet points, headers, emojis, verbose summaries — is rarely what a regular user actually wants. Be explicit.

**What to cover:**
- Prose vs. bullet points (and when each is acceptable)
- Length/verbosity preference
- Emoji use
- Whether to ask clarifying questions or just proceed

**Example:**
```markdown
# Communication Style
- Be direct and practical, no fluff
- No bullet points or headers for conversational replies — prose only
- No emojis unless asked
```

**Why this matters:** Without these instructions, the assistant defaults to structured outputs with bullets and bold text for almost everything, including casual answers. Most people find this exhausting to read over time.

### Writing Style: A Separate File

Format preferences (prose vs. bullets, emoji use) belong in CLAUDE.md because they apply to every response. Language quality rules are different — they are longer, more nuanced, and benefit from independent maintenance. Put them in a dedicated file, e.g. `writing-style.md`, and load it with a read instruction in CLAUDE.md.

A writing style file typically contains:
- Banned words and phrases that produce generic AI-sounding output ("leverage", "delve into", "it's worth noting", "importantly")
- Sentence structure preferences — e.g. short sentences, active voice, no padding phrases
- Prose vs. list rules — when bullets are acceptable vs. when they fragment ideas that flow better as prose

This keeps the writing style evolvable: you can add new patterns as you notice them without touching the core identity and rules file. The read instruction is one line in CLAUDE.md:

```
Read `writing-style.md` at the start of every session.
```

Keep the file under 60 lines. If it grows beyond that, you are likely cataloguing individual violations rather than capturing the underlying principle.

### 3. Critical Rules (the safety boundary)

This is the most important section. Clearly state what the assistant must never do without explicit confirmation. For a personal assistant with access to email, calendar, and files, the rule is almost always:

**Never take real-world actions autonomously.**

Write this section as a hard rule, not a preference. Use "NEVER" intentionally — it signals a constraint, not a style suggestion.

**Example:**
```markdown
# Critical Rules
- NEVER send emails, create calendar events, or take real-world actions autonomously
- Always propose drafts and wait for explicit confirmation before anything is sent
- When drafting messages in a second language, produce polished text appropriate in form
  (formal, friendly, etc.) for the recipient — ready to send as-is
```

The third point shows a useful pattern: pair the constraint ("never send autonomously") with a positive counterpart ("but do produce a complete, polished draft so the user can send it instantly"). This gives the assistant something concrete to do rather than just a prohibition.

---

## Layering: CLAUDE.md vs. Task-Level Instructions

CLAUDE.md contains standing rules that apply to every interaction. Task-specific instructions (how to run a weekly project status digest, how to track client contracts) belong in dedicated task files like `TASK.md`, which the assistant reads on demand.

The right question for each rule: "Does this apply to every single conversation, regardless of what I'm doing?" If yes → CLAUDE.md. If it's specific to a workflow → the relevant task file.

**Keep CLAUDE.md short.** Aim for under 30 lines. If it grows beyond that, you are likely adding task-specific instructions that belong elsewhere.

---

## File Access Tiers

Not all files in a project warrant the same access. Four tiers cover most cases:

- **Auto-read:** files Claude loads at the start of every session — personal profile, writing style, active context. List these as explicit read instructions in CLAUDE.md.
- **Reference-only:** folders Claude knows about but reads on demand — knowledge bases, output archives, templates. Name them in CLAUDE.md so Claude knows where to look, but don't auto-load them.
- **Read-only:** files Claude can read but must not modify — master data, shared reference files, historical records. State this explicitly in CLAUDE.md: "The `masterdata/` folder is read-only — never edit files in it."
- **Ignored:** files Claude should not read. Use `.claudeignore` for this in Claude Code. In Claude.ai or Cowork, or when the directory structure should be self-documenting, use a name prefix: `[IGNORE]` for folders to skip entirely, `[ARCHIVE]` for old versions stored for reference. The two approaches are complementary — `.claudeignore` handles patterns, name prefixes communicate intent visibly in the folder tree.

The token cost of auto-reading compounds across every session. Keep the auto-read tier small. Everything else earns its place by being referenced in a task, not by being loaded by default.

---


## Cross-Reference Consistency Rules (Project CLAUDE.md)

When a project has multiple linked artifacts — risk registers, action trackers, dependency registers, decision logs — add explicit rules that tell Claude what to check whenever any one of them changes. Without this, Claude will update the register you mention and leave the others stale.

Write the rule as a checklist tied to the ID type:

```markdown
**Cross-reference consistency:** Whenever an action, dependency, or risk is added or changed:
- New Risk → check for a linked Dependency and an Action tracking mitigation; link both ways.
- New Dependency → check whether it drives an existing Risk; link if so.
- New Action → record its source (Risk/Dependency/Decision) and ensure the source references it back.
```

This pattern applies any time a project manages two or more linked registers. The PMO_TEMPLATE shows a full implementation. For a simple personal project with one tracker, skip this — it's only needed when orphaned IDs are a real failure mode.

---

## What NOT to Put in CLAUDE.md

- **Lists of capabilities** ("you can use Gmail, Calendar, etc.") — the assistant discovers tools from its environment
- **Workflow steps** — these belong in task files
- **Information about the user's projects or contacts** — these belong in profile files
- **Rules that rarely apply** — do not clutter standing instructions with edge cases that come up once a month

---

## Maintenance

CLAUDE.md should evolve. When you correct the assistant on a behaviour repeatedly, that correction belongs in CLAUDE.md. Common triggers for updating it:

- The assistant keeps doing something you don't like (add a rule)
- You keep explaining the same context at the start of sessions (add it to the identity section)
- A rule has never mattered (remove it — dead rules dilute the live ones)

A good CLAUDE.md is a living document that reflects a few months of real use, not a first draft from day one.

---

## Quick Reference: Anatomy of a Good CLAUDE.md

```
# About [User]
[Who they are, where, timezone, language preference]

# Communication Style
[Format, verbosity, tone preferences]

# Critical Rules
[What the assistant may never do; what it should always do instead]
```

That is usually enough. Add sections only when you have a real behavioural problem they solve.

---

## Real-World Example

Below is a complete, working CLAUDE.md for a personal setup. It is intentionally short — 18 lines of real content — and every line changes behaviour.

```markdown
# About User
- Dutch, based in Helsinki, Finland
- Timezone: Europe/Helsinki (EET UTC+2 / EEST UTC+3 in summer)
- Always respond in English, even if I write in Finnish or paste Finnish content
- Uses Gmail (firstname.lastname@gmail.com) and Google Calendar

# Communication Style
- Be direct and practical — no fluff, no filler
- Prose for conversational replies; only use bullet points or headers when the
  content genuinely calls for it (e.g. a list of tasks, a structured document)
- No emojis unless I use them first
- Don't ask clarifying questions for every task — make a reasonable assumption
  and proceed; flag the assumption briefly if it matters

# Critical Rules
- NEVER send emails, create calendar events, or take any real-world action autonomously
- Always draft first and wait for my explicit confirmation before anything is sent or saved
- When drafting Finnish messages, produce polished text appropriate for the
  recipient (formal or casual) — ready to send as-is
```

**Why this works:**
- The timezone entry ensures scheduling suggestions are in Helsinki time, not UTC.
- "Always respond in English" resolves the ambiguity of a Dutch person in Finland who reads Finnish but prefers English responses.
- The "make a reasonable assumption" instruction prevents the assistant from stalling on every slightly ambiguous request.
- The Finnish message rule pairs the "don't act autonomously" constraint with a clear positive: produce something I can send immediately.

**Giving this to Claude:**
> "Read 01_CLAUDE_MD.md and help me write my own CLAUDE.md. Ask me the key questions you need answered."

Claude will walk you through identity, style, and rules — and produce a draft in the format above.

**Faster alternative:** `tasks/setup-claude-md.md` does this end-to-end without reading the guide first. `tasks/audit-claude-md.md` reviews an existing CLAUDE.md against this guide's checklist.

---

## Second Example: Developer Setup

For comparison — a CLAUDE.md for a software engineer who uses Claude for code review, meeting prep, and async communication. Same three sections, different rules.

```markdown
# About Alex
- Software engineer, based in Toronto (EST, UTC-5)
- Works primarily in Python and TypeScript
- Timezone: America/Toronto
- Respond in English always

# Communication Style
- Technical responses are fine — don't simplify unless I ask
- Be concise; avoid restating what I just said
- No emojis
- If I ask for a code review, give direct feedback — don't soften problems

# Critical Rules
- NEVER commit, push, or run destructive commands autonomously
- For anything that modifies files or runs code: show the command and wait for confirmation
- When I paste code, assume it is from my codebase unless I say otherwise
```

**What is different here:**
- The critical rule is about code operations, not email. The pattern is the same — "never act autonomously, show first" — but adapted to the domain.
- "Don't simplify" is the opposite of what many users want, but correct for someone who works technically and finds over-explained answers slow.
- "Assume it is from my codebase" avoids Claude treating every code snippet as a standalone hypothetical with invented context.

The two examples show the same three-section structure applied to different contexts. The sections do not change; the content inside them reflects real use.
