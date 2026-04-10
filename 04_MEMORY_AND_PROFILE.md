# Best Practices: Memory and Profile Systems

*Last reviewed: April 2026*

A personal assistant is only as good as its memory. Without memory, every session starts from zero — you re-explain your situation, your preferences, who your contacts are. This document covers two complementary memory systems: the **auto-memory** system (lightweight, cross-session key-value facts) and the **profile file system** (structured, richly maintained knowledge about a person's life and projects).

---

## Which System Should You Use?

### Native Claude Memory vs. `.auto-memory/`

There are three memory layers available. Understanding when each applies prevents a common frustration: expecting memory to persist when the system you're relying on doesn't survive between sessions.

| Dimension | Native Claude Memory | `.auto-memory/` folder | Profile files |
|---|---|---|---|
| Setup required | None — always active | Create folder + MEMORY.md + one CLAUDE.md line | Create profile folder structure |
| Where it lives | `~/.claude/projects/[hash]/memory/MEMORY.md` | Your project folder on disk | Your task folder on disk |
| Survives context reset? | **No** — clears when session context resets | **Yes** — read from disk each session | **Yes** — read explicitly each run |
| Works in scheduled tasks? | **Not reliably** | **Yes** — explicitly loaded | **Yes** — explicitly loaded |
| Multiple files? | No — single file | Yes — one file per topic | Yes — one file per profile domain |
| Best for | Chat assistant use, corrections in conversations | Cross-session facts, preferences, projects | Scheduled task agents needing deep context |

**The critical rule for scheduled tasks: always use `.auto-memory/` or profile files, not native memory.** Native memory is not reliably available to autonomous task runs — it is designed for interactive sessions. A task that depends on native memory may behave correctly some runs and forget everything on others.

**If you are just getting started:** let native memory work by default for your conversational use. Add `.auto-memory/` when you want structured, reliable memory. Add profile files only when a scheduled task clearly needs them — after auto-memory is already in place.

The two systems can coexist: native memory for your interactive chat assistant, `.auto-memory/` for your tasks and projects. They do not conflict.

**Note:** This guide covers memory *about you* — your preferences, projects, and working style. If you want to build a knowledge base *about a subject domain* (research, threat intelligence, competitive analysis), that's a different system: see [Guide 15 — LLM Wiki](./15_LLM_WIKI.md).

---

**Use auto-memory** (the `.auto-memory/` folder) for the vast majority of deliberate memory cases. It handles assistant-wide preferences, corrections, project states, and reference pointers.

**Use profile files** only when you have a scheduled task agent that requires deep, structured knowledge about a person: full relationship maps, historical project tracking, hypotheses about behaviour. This is a more advanced pattern, typically added after auto-memory is already in place.

---

## Two Kinds of Memory

**Auto-memory** is the simpler system. It stores discrete facts about the user, their preferences, and their projects in small markdown files with a shared index (`MEMORY.md`). It is general-purpose and designed for facts that would change how the assistant behaves in any future conversation.

**Profile files** are richer, domain-specific documents that a task agent reads at the start of each run. They capture not just facts but relationships, project states, hypotheses, and history. They are best suited to a recurring agent that needs deep contextual awareness — for example, a daily email analysis task.

Use auto-memory for assistant-wide preferences and quick facts. Use profile files for anything that requires narrative depth, tracking over time, or structured relationships.

---

## Auto-Memory: What to Save

Save things that would change how the assistant responds in a future conversation if it knew them. The four types:

**User memories** — who the person is: role, context, relevant skills, life situation. Example: "Sam is a freelance UX designer, works remotely across multiple time zones, prefers async communication. Has two main long-term clients and takes on smaller projects in between."

**Feedback memories** — corrections and confirmed preferences. This is the most important type. Every time you correct the assistant on something, that correction should be saved so it does not need to be made again. Include why: "Always suggest a subject line when drafting emails. Why: user finds writing subject lines more friction than the email body itself."

**Project memories** — ongoing work the assistant should be aware of: "Website redesign proposal for Hartwell Co. — draft sent 2026-02-14, awaiting feedback. Follow up if no response by 2026-03-01." Convert relative dates to absolute when saving — "next Thursday" means nothing in a future session.

**Reference memories** — where to find things: "Active client contracts are tracked in [workspace]/Clients/CONTRACTS.md"

**What not to save:** code patterns, file structures, git history, anything derivable from reading the project, anything only relevant to the current conversation.

---

## Memory File Format

Auto-memory files are small markdown files stored in `.auto-memory/`. There is one index file (`MEMORY.md`) and one file per memory entry. Here is what they look like:

**`.auto-memory/MEMORY.md`** (the index — Claude reads this every session):

```markdown
# Memory Index

- [user-identity](./user-identity.md) — Who the user is, timezone, language preferences
- [feedback-email-format](./feedback-email-format.md) — How to format email drafts
- [project-lease-2026](./project-lease-2026.md) — Lease renewal tracking
- [reference-contracts](./reference-contracts.md) — Where contracts are stored
```

**Individual memory file** (e.g., `.auto-memory/user-identity.md`):

```markdown
User is Dutch, lives in Helsinki (timezone: Europe/Helsinki).
Prefers English responses always, even when sending content in Finnish.
Uses Gmail (firstname.lastname@gmail.com) and Google Calendar as primary tools.
[updated: 2026-01]
```

To ensure Claude loads your memory index at the start of each session, add this line to your `CLAUDE.md`:

```markdown
- Read `.auto-memory/MEMORY.md` at the start of every session.
```

**Keep `MEMORY.md` under 30 entries.** Every entry in the index is loaded into every session — compactness matters just as much here as in profile files.

---

## Profile Files: Structure and Purpose

The profile file system divides a person's profile across several files by topic. The key insight is that you almost never need everything at once — you need a compact summary every time, and the full detail files only when you are updating them.

**PROFILE_SUMMARY.md** — the only file read every single run. Keep it under 40–50 lines (roughly 600 tokens). It should answer: who is this person, what are their active projects right now, who are the key contacts, and what are the open action items? If it grows beyond this limit, trim or move content to the detail files.

**PROFILE_identity.md** — key people and relationships: family members, colleagues, service contacts, and what the assistant needs to know about each.

**PROFILE_projects.md** — active projects, their status, and what the assistant should track or surface.

**PROFILE_patterns.md** — behavioural patterns, preferences, recurring habits, subscriptions, services.

**PROFILE_hypotheses.md** — things the assistant believes to be true but hasn't confirmed. More on this below.

**PROFILE_archive.md** — completed projects and resolved items worth keeping for historical reference.

---

## Profile Update Discipline

**Use targeted edits, not full rewrites.** When a new fact arrives, use search + edit to update the specific line or section. Only do a full rewrite when making structural changes. This is faster, less error-prone, and avoids accidentally overwriting still-valid data.

**Timestamp your updates.** Every significant profile edit should include `[updated: YYYY-MM]` so you can see at a glance how fresh the data is. Entries not updated in 3+ months should be flagged as potentially stale.

**Distinguish evidence from confirmed fact.** The assistant will infer things from email patterns and browsing that may not be correct. Use a consistent notation to mark what is confirmed vs. inferred:
- `[USER]` or `[USER-CONFIRMED]` — manually entered or confirmed by the user; never overwrite
- No tag — inferred by the assistant; may need verification
- `[updated: YYYY-MM]` — recently confirmed accurate

**Never overwrite user annotations.** If the user has annotated their profile with a correction or note, treat it as ground truth that takes precedence over any inference.

---

## Decision Tree: Update vs. Create

When a new fact arrives, follow this flow:

```
New fact arrives
  ├─ Does a memory file for this topic already exist?
  │   ├─ YES → Is the new fact a refinement or a contradiction?
  │   │   ├─ REFINEMENT → Edit the existing file (targeted edit, not rewrite)
  │   │   └─ CONTRADICTION → See "Contradiction Resolution" below
  │   └─ NO → Create a new file, add a one-line pointer to MEMORY.md
  │
  └─ Maintenance checks (apply periodically):
      ├─ Two files cover overlapping topics? → Merge into one, remove the redundant file
      ├─ One file exceeds ~40 lines of distinct subtopics? → Split by subtopic
      └─ Entry not updated in 3+ months? → Verify it's still accurate or archive it
```

**When to merge:** if you notice two memory files that both cover the same person, project, or preference — combine them into the more descriptive one and delete the other. Update the MEMORY.md index.

**When to split:** if a single file has grown to cover multiple unrelated subtopics (e.g., a "user-work" file that now covers both the user's role and three separate projects), split into focused files. Each file should have a clear, single topic.

---

## Contradiction Resolution

Facts sometimes conflict — the user moved cities, changed roles, or corrected an earlier assumption. Follow these rules in order:

1. **`[USER]`-tagged entries always win.** If the existing entry is marked `[USER]` or `[USER-CONFIRMED]`, it was explicitly provided by the user. Never overwrite it based on inference alone — ask the user first.

2. **More recent wins, unless the older entry is user-confirmed.** If both entries are inferred (no `[USER]` tag), the more recent observation takes precedence. Update the file and add an `[updated: YYYY-MM]` tag.

3. **When uncertain, keep both and flag.** If you cannot determine which fact is correct — for example, two plausible but conflicting inferences — do not silently pick one. Add both with a `[CONFLICTING]` tag and surface the conflict to the user at the next opportunity.

**Example — user moved cities:**

The memory file says `Lives in Amsterdam (timezone: Europe/Amsterdam) [updated: 2025-06]`. A new email signature shows a Helsinki address.

- The existing entry has no `[USER]` tag → it's inferred, not user-confirmed
- The new signal is more recent → update the file:

```markdown
Lives in Helsinki (timezone: Europe/Helsinki) [updated: 2026-04]
Previously: Amsterdam (until ~2025)
```

**Example — ambiguous conflict:**

Memory says "Prefers formal tone in Finnish emails." A recent email draft from the user uses casual Finnish. This could mean the preference changed, or it could be context-specific.

- Add: `[CONFLICTING] Recent email used casual Finnish — confirm if tone preference has changed`
- Surface to the user next session: "I noticed you used casual Finnish in a recent draft — should I update your preference, or was that specific to that message?"

---

## The Hypothesis System

Some signals are meaningful but not yet confirmed. Rather than either ignoring them or committing to a fact that may be wrong, use a hypothesis layer.

A hypothesis captures: what the assistant believes, why it believes it, and what evidence would confirm or refute it. Example:

```
H-001: User may be considering raising their day rate
Evidence: Googled "freelance rate calculator" twice; declined a small project citing time constraints
Confidence: LOW
Would confirm: Direct mention of rate change; new proposal sent with higher figure
```

This lets the assistant surface the hypothesis as a proactive suggestion ("I've noticed a few signals you might be re-evaluating your rates — want me to pull together a market comparison?") rather than either ignoring the signal or stating it as fact.

For the full hypothesis lifecycle — how hypotheses are promoted from LOW to CONFIRMED, when to surface them, and when to expire them — see [Guide 07, Part 4](./07_TASK_LEARNING_GUIDE.md#part-4-the-hypothesis-system).

---

## The PROFILE_SUMMARY.md Hard Limit

The summary file is read into every automated run. Every extra line has a cost in context. Enforce a strict size limit (40–50 lines) and trim before every write. The priority order for what to include:

1. Who the person is (2–3 lines)
2. Active projects with current status (most important)
3. Key contacts — quick reference, not full detail
4. Open action items with IDs (so the agent knows what it's tracking)
5. User preferences that override defaults

Everything else belongs in the detail files.

---

## Sensitive Information

Not everything should be stored in a profile. As a rule, store the minimum needed to be useful. Specifically:

- Health information: store at the category level ("ongoing condition, actively managed") not the clinical detail
- Financial specifics: store the project ("reviewing accountant options for next tax year") not account numbers or exact figures
- Relationship details: note that a contact exists and the role, not sensitive context about the relationship

The test: would you be comfortable if this profile file were accidentally shared? If no, reduce the detail.

---

## Keeping Profile Files Lean

Profile files grow over time and become slow to read and hard to maintain. Apply these rules:

- Split any file that exceeds ~150 lines of genuinely useful content
- Archive completed projects rather than leaving them in the active section
- Compress old session logs and history entries to single-line summaries
- Remove hypotheses that have been confirmed (move the fact to the appropriate detail file) or refuted (delete them)

A profile system that is kept lean stays fast and useful. A profile that becomes a 500-line dump of everything the assistant has ever learned is almost as bad as no profile at all.

---

## Memory Across Multiple Task Agents

If you run more than one scheduled task agent (e.g., a daily email digest agent and a client pipeline tracker), they can share the same profile files. The convention that makes this work:

- All agents read `PROFILE_SUMMARY.md` every run
- All agents update the relevant detail file when they discover new information
- No agent overwrites `[USER]`-annotated entries
- Each agent has its own session/run log so their histories don't collide

The shared profile becomes the connective tissue between agents — the user does not have to explain an ongoing client situation to the email agent and separately to the pipeline tracker. Both of them know.

---

## Real-World Auto-Memory Examples

Here are the kinds of facts that belong in auto-memory, drawn from a working personal assistant setup. Each would be saved as a small markdown file with a pointer in `MEMORY.md`.

**User memory:**
> User is Dutch, lives in Helsinki (timezone: Europe/Helsinki). Prefers English responses always, even when sending content in Finnish. Uses Gmail and Google Calendar as primary tools.

**Feedback memory:**
> Always produce Finnish messages in two versions (formal and casual) unless tone is specified. Why: user regularly needs Finnish communication for both official contexts (banks, authorities) and everyday situations — having both versions ready saves time and avoids asking.

**Project memory (example):**
> Apartment lease renewal due 2026-04-30. User is reviewing options; has not yet replied to landlord's last email (2026-03-15). Flag if no action by 2026-04-01.

**Reference memory:**
> Active shopping list is tracked in the grocery-list-assistant skill memory. Finnish supermarkets used: Prisma (main) and K-Citymarket (fish/fresh produce).

---

## Giving This to Claude

**To set up auto-memory from scratch:**
> "Read 04_MEMORY_AND_PROFILE.md and start setting up my memory system. Ask me what you need to know about me, my projects, and my preferences — then save it in the right format."

**To set up profile files for a scheduled task:**
> "Read 04_MEMORY_AND_PROFILE.md and create the profile file structure for my daily email digest task. The task already has a TASK.md — add the profile files it needs to track context across runs."

**Faster alternative:** `tasks/setup-memory.md` interviews you and creates the full `.auto-memory/` structure without reading the guide first. `tasks/audit-memory.md` reviews an existing memory system for staleness and drift.
