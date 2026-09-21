# Best Practices: Memory and Profile Systems

Without memory, every session starts from zero — you re-explain your situation, preferences, and contacts. This guide covers two complementary memory systems: **auto-memory** (lightweight, cross-session facts in `.auto-memory/`) and **profile files** (structured, richly maintained knowledge for scheduled task agents).

---

## Which System Should You Use?

### The four memory layers

Separate **native conversational memory**, **native coding-agent memory**, **explicit project memory**, and **task profiles**. The first two belong to the account or runtime; the last two are files you own and deliberately load. They can serve the same user without being the same store.

| Layer | Owner and use | Verification |
|---|---|---|
| Conversational memory in Claude or ChatGPT | Native account/project settings; useful for preferences and continuity | Inspect the current surface's memory controls; check whether the intended conversation can recall a harmless fact |
| Claude Code or Codex native memory | Runtime-local state, when available | Inspect that runtime's current controls; do not infer paths or availability from the other product |
| Cluide `.auto-memory/` | Explicit Markdown index and topic files in the project | Add a read instruction to the shared policy; test from a fresh session |
| Task profile files | Explicit input to a recurring task | Name them in `TASK.md` and confirm access in the actual scheduled environment |

Cluide's `.auto-memory/` is a convention, not either vendor's native feature. Codex does not gain Claude Code memory by sharing a checkout, and a ChatGPT uploaded source does not update when a local memory file changes.

For scheduled tasks, use explicit, accessible state whose revision and load can be verified. Local tasks can read project files; cloud tasks need uploaded or connected sources and an explicit write-back destination. A file on your laptop is not an available input merely because its path appears in the prompt. Keep one writer per memory topic; the other surface proposes updates or receives a handoff. Conflicts need evidence and dates, not last-writer-wins.

### Claude Code auto memory as of September 2026

Claude Code documents per-project memory under `~/.claude/projects/<project>/memory/`, with a compact `MEMORY.md` index and on-demand topic files. Keep that store separate from shared project memory and exclude private content from distribution. Use its memory controls to inspect what is enabled rather than assuming every environment loads it. [Official memory documentation](https://code.claude.com/docs/en/memory), checked 2026-09-14.

### ChatGPT and Codex continuity

For ChatGPT projects, put durable task facts in an accessible source and retain an authored copy outside chat if they need version history. Record which project and source revision are in use. For Codex, use `AGENTS.md` for standing rules and explicit reads for project memory; native memory is optional continuity, not the acceptance oracle. Verify one fact in a fresh session after updating it. [Projects and sources](https://learn.chatgpt.com/docs/projects) and [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), checked 2026-09-14.

ChatGPT memory and local Codex memory are separate stores: ChatGPT web uses ChatGPT's memory feature, while local Codex clients (Codex CLI and IDE, and local work in the ChatGPT desktop app) keep their own local memory store with independent controls. Local memory is off by default — enable it in the desktop app under Settings > Personalization > Enable memories, or with `[features] memories = true` in `config.toml` — and `/memories` (desktop app and Codex TUI) sets per chat whether that chat can use and contribute to memories. The store lives under `~/.codex/memories/`, so treat it as machine-local state alongside `~/.claude/projects/`. Project-only memory is documented for cloud ChatGPT projects; no per-project memory scope is documented for local projects. [Codex memories](https://learn.chatgpt.com/codex/customization/memories) and, for cloud projects, the help article [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), checked 2026-09-21.

Start with a short index. Add richer profiles when a recurring task needs narrative context. Domain research belongs in [Guide 15's wiki](./15_LLM_WIKI.md), not personal memory.

---

## Two Kinds of Memory

**Auto-memory** stores discrete facts about the user, their preferences, and their projects in small markdown files with a shared index (`MEMORY.md`). General-purpose, designed for facts that change how the assistant behaves in any future conversation. It handles the vast majority of deliberate memory cases: assistant-wide preferences, corrections, project states, and reference pointers.

**Profile files** are richer, domain-specific documents a task agent reads at the start of each run. They capture relationships, project states, hypotheses, and history. Best suited to recurring agents needing deep contextual awareness — for example, a daily email analysis task.

Use auto-memory for assistant-wide preferences and quick facts. Use profile files for narrative depth, tracking over time, or structured relationships.

---

## Auto-Memory: What to Save

Save things that would change how the assistant responds in a future conversation. Four types:

**User memories** — who the person is: role, context, relevant skills, life situation. Example: "Sam is a freelance UX designer, works remotely across multiple time zones, prefers async communication. Has two main long-term clients and takes on smaller projects in between."

**Feedback memories** — corrections and confirmed preferences. The most important type. Every correction should be saved so it never needs to be repeated. Include why: "Always suggest a subject line when drafting emails. Why: user finds writing subject lines more friction than the email body itself."

**Project memories** — ongoing work the assistant should be aware of: "Website redesign proposal for Hartwell Co. — draft sent 2026-02-14, awaiting feedback. Follow up if no response by 2026-03-01." Convert relative dates to absolute when saving — "next Thursday" means nothing in a future session.

**Reference memories** — where to find things: "Active client contracts are tracked in [workspace]/Clients/CONTRACTS.md"

**What not to save:** code patterns, file structures, git history, anything derivable from reading the project, anything only relevant to the current conversation.

---

## Memory File Format

Auto-memory files are small markdown files stored in `.auto-memory/`. There is one index file (`MEMORY.md`) and one file per memory entry. Here is what they look like:

**`.auto-memory/MEMORY.md`** (the index, explicitly loaded by the project bootstrap below):

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

To request explicit loading, add this line to the canonical policy (`AGENTS.md` in a shared repository, `CLAUDE.md` for Claude-only use), then verify it in a fresh session:

```markdown
- Read `.auto-memory/MEMORY.md` at the start of every session.
```

**Keep `MEMORY.md` under 30 entries.** Every entry in the index is loaded into every session — compactness matters just as much here as in profile files.

---

## Profile Files: Structure and Purpose

The profile system divides a person's profile across files by topic. The key insight: you almost never need everything at once — you need a compact summary every time, and the full detail files only when updating them.

**PROFILE_SUMMARY.md** — the only file read every single run. Keep it under 40–50 lines (roughly 600 tokens). It should answer: who is this person, what are their active projects right now, who are the key contacts, and what are the open action items? If it grows beyond this limit, trim or move content to the detail files.

**PROFILE_identity.md** — key people and relationships: family members, colleagues, service contacts, and what the assistant needs to know about each.

**PROFILE_projects.md** — active projects, their status, and what the assistant should track or surface.

**PROFILE_patterns.md** — behavioural patterns, preferences, recurring habits, subscriptions, services.

**PROFILE_hypotheses.md** — things the assistant believes to be true but hasn't confirmed. More on this below.

**PROFILE_archive.md** — completed projects and resolved items worth keeping for historical reference.

---

## Profile Update Discipline

**Use targeted edits, not full rewrites.** When a new fact arrives, update the specific line or section. Only do a full rewrite for structural changes. Targeted edits are faster, less error-prone, and avoid accidentally overwriting still-valid data.

**Timestamp your updates.** Every significant profile edit should include `[updated: YYYY-MM]` so you can see at a glance how fresh the data is. Entries not updated in 3+ months should be flagged as potentially stale.

**Distinguish evidence from confirmed fact.** The assistant will infer things from email patterns and context that may not be correct. Use consistent notation to mark confirmed vs. inferred:
- `[USER]` or `[USER-CONFIRMED]` — manually entered or confirmed by the user; never overwrite
- No tag — inferred by the assistant; may need verification
- `[updated: YYYY-MM]` — recently confirmed accurate

**Never overwrite user annotations.** If the user has annotated their profile with a correction or note, treat it as ground truth that takes precedence over any inference.

---

## The Periodic Knowledge Sweep

Day-to-day memory captures what surfaces run-to-run (see [Guide 07](./07_TASK_LEARNING_GUIDE.md) for the incremental, signal-driven version). Occasionally it is worth a deliberate *bulk* pass over a whole historical corpus — an email or chat archive, a folder of documents, past performance reviews — to mine the latent facts before they are lost. This is the right motion when you are first building a profile, or before a major transition (a job change, a move, taking over a new responsibility) where years of undocumented context suddenly matters.

The sweep is a four-step motion, distinct from incremental learning:

1. **Sweep** — read across the corpus and dump raw findings into one dated file: `Knowledge-Sweep-YYYY-MM.md`. Capture liberally; don't filter yet.
2. **Validate** — check each finding against what's already known. Dedupe, resolve contradictions, flag anything uncertain for the user to confirm.
3. **Merge** — fold the confirmed findings into the master profile / knowledge files using the targeted-edit discipline above. Tag confirmed items `[USER-CONFIRMED]`, leave inferences untagged.
4. **Archive** — move the raw sweep file to an archive once merged. It has done its job; keep it for provenance but don't re-read it every session (that would defeat the lean-summary principle below).

Run it at intervals or before transitions — not every session. The sweep is the bulk-import counterpart to the steady trickle of incremental updates: one mines history, the other keeps up with the present.

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

Facts sometimes conflict — the user moved cities, changed roles, or corrected an earlier assumption. Resolution rules, in order:

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

Some signals are meaningful but not yet confirmed. Rather than ignoring them or committing to a possibly wrong fact, use a hypothesis layer.

A hypothesis captures: what the assistant believes, why, and what evidence would confirm or refute it. Example:

```
H-001: User may be considering raising their day rate
Evidence: Googled "freelance rate calculator" twice; declined a small project citing time constraints
Confidence: LOW
Would confirm: Direct mention of rate change; new proposal sent with higher figure
```

This lets the assistant surface the hypothesis as a proactive suggestion ("I've noticed a few signals you might be re-evaluating your rates -- want me to pull together a market comparison?") rather than ignoring the signal or stating it as fact.

For the full hypothesis lifecycle — how hypotheses are promoted from LOW to CONFIRMED, when to surface them, and when to expire them — see [Guide 07, Part 4](./07_TASK_LEARNING_GUIDE.md#part-4-the-hypothesis-system).

---

## The PROFILE_SUMMARY.md Hard Limit

The summary file is read into every automated run. Every extra line costs context. Enforce a strict size limit (40-50 lines) and trim before every write. Priority order:

1. Who the person is (2–3 lines)
2. Active projects with current status (most important)
3. Key contacts — quick reference, not full detail
4. Open action items with IDs (so the agent knows what it's tracking)
5. User preferences that override defaults

Everything else belongs in the detail files.

---

## Sensitive Information

Store the minimum needed to be useful:

- Health information: store at the category level ("ongoing condition, actively managed") not the clinical detail
- Financial specifics: store the project ("reviewing accountant options for next tax year") not account numbers or exact figures
- Relationship details: note that a contact exists and the role, not sensitive context about the relationship

The test: would you be comfortable if this profile file were accidentally shared? If no, reduce the detail.

---

## Keeping Profile Files Lean

Profile files grow over time. Apply these rules:

- Split any file that exceeds ~150 lines of genuinely useful content
- Archive completed projects rather than leaving them in the active section
- Compress old session logs and history entries to single-line summaries
- Remove hypotheses that have been confirmed (move the fact to the appropriate detail file) or refuted (delete them)

A lean profile stays fast and useful. A 500-line dump of everything the assistant has ever learned is almost as bad as no profile at all.

**System-level target:** keep all auto-read files combined under ~2,000 tokens (~100-150 lines total across everything the assistant loads at session start). The per-file maxima elsewhere in this guide are ceilings, not targets — the combined session-start budget is what governs. Lightweight auto-read files mean the assistant infers context without re-explanation and sessions start immediately useful. When they grow unchecked, token cost compounds across every run and important context gets diluted by stale detail. If you consistently hit context limits early, audit the auto-read set first.

---

## Memory Across Multiple Task Agents

Multiple scheduled task agents (e.g., a daily email digest and a client pipeline tracker) can share the same profile files. The convention that makes this work:

- All agents read `PROFILE_SUMMARY.md` every run
- Agents submit discoveries to the designated profile writer, or acquire the shared destination's atomic claim before reading and updating it. Re-read the current revision after acquisition; a failed claim waits or skips. Do not permit all agents to write freely.
- No agent overwrites `[USER]`-annotated entries
- Each agent has its own session/run log; shared summaries, indexes and detail files still use the same writer/claim protection
- Apply [Guide 09's collision procedure](./09_MULTI_TASK_ORCHESTRATION.md#avoiding-collisions) to manual runs, retries and both platforms. Schedule gaps and separate logs are not exclusion.

The shared profile becomes connective tissue between agents — the user does not have to explain an ongoing client situation to both the email agent and the pipeline tracker. Both already know.

---

## Real-World Auto-Memory Examples

Facts that belong in auto-memory, shown here as illustrative examples. Each is saved as a small markdown file with a pointer in `MEMORY.md`.

**User memory:**
> User is Dutch, lives in Helsinki (timezone: Europe/Helsinki). Prefers English responses always, even when sending content in Finnish. Uses Gmail and Google Calendar as primary tools.

**Feedback memory:**
> Always produce Finnish messages in two versions (formal and casual) unless tone is specified. Why: user regularly needs Finnish communication for both official contexts (banks, authorities) and everyday situations — having both versions ready saves time and avoids asking.

**Project memory (example):**
> Contract renewal decision due 2026-04-30. User is reviewing options; has not yet replied to the supplier's last email (2026-03-15). Flag if no action by 2026-04-01.

**Reference memory:**
> Active shopping list is tracked in the grocery-list-assistant skill memory. Two stores are used: one main supermarket and one for fresh produce.

---

## Giving This to an Assistant

**To set up auto-memory from scratch:**
> "Read 04_MEMORY_AND_PROFILE.md and start setting up my memory system. Ask me what you need to know about me, my projects, and my preferences — then save it in the right format."

**To set up profile files for a scheduled task:**
> "Read 04_MEMORY_AND_PROFILE.md and create the profile file structure for my daily email digest task. The task already has a TASK.md — add the profile files it needs to track context across runs."

**Faster alternative:** `tasks/setup-memory.md` interviews you and creates the full `.auto-memory/` structure without reading the guide first. `tasks/audit-memory.md` reviews an existing memory system for staleness and drift.
