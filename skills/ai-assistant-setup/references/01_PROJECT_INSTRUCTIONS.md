# Best Practices: Writing Shared Instructions, AGENTS.md and CLAUDE.md

Standing instructions shape how an assistant works across tasks. This guide covers their content and structure, then shows how that contract reaches Claude, ChatGPT projects and Codex. `CLAUDE.md` is the Claude entry point, not a universal loader. The former filename is retained as a compatibility page.

---

<a id="what-claudemd-is-for"></a>

## What Project Instructions Are For

Standing instructions answer: "Before I do anything, what do I need to know about this project or person?" They are an operating contract, not a task list or a knowledge base. **Every line should change behaviour.** If removing a line would not change an action or answer, cut it.

For a dual-platform repository, keep shared rules in root `AGENTS.md`; make `CLAUDE.md` a thin adapter containing `@AGENTS.md` plus an explicit instruction to read it if imports are not resolved. Keep Claude-only configuration outside the shared rules. This repository demonstrates the arrangement; [Guide 35](./35_DUAL_PLATFORM_PROJECTS.md) explains the ownership and migration rules.

| Surface | Where the contract reaches the assistant | Check before relying on it |
|---|---|---|
| Claude Code | Native `CLAUDE.md` files and their imports; current versions also read `AGENTS.md` natively when no `CLAUDE.md` exists ([Guide 35 §9](./35_DUAL_PLATFORM_PROJECTS.md#9-platform-facts)) | Inspect the loaded files, including parent and local instructions |
| Cowork / conversational Claude | Project instructions bootstrap the accessible policy source | Confirm the connected folder or uploaded revision was actually read |
| Codex repository session | Native `AGENTS.md` discovery; `AGENTS.override.md` can supersede it at a level | Start in the intended workspace and inspect overrides along the instruction chain |
| ChatGPT uploaded-source project | Project instructions plus uploaded or connected policy source | Record source revision; a repository edit does not refresh an upload |

Do not treat an `@` import as Codex syntax or an uploaded instruction file as proof of automatic loading. Put the full shared contract in `AGENTS.md`, with explicit read pointers for longer references. After changing rules, start a fresh session on each supported surface and test a behaviour that depends on them. Record missing sources as missing, not as permission to guess.

Documentation checked 2026-09-14: [Claude instruction loading](https://code.claude.com/docs/en/memory), [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [ChatGPT projects and sources](https://learn.chatgpt.com/docs/projects). The detailed product facts are maintained in [Guide 35 §9](./35_DUAL_PLATFORM_PROJECTS.md#9-platform-facts).

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

Tell the assistant exactly how to format and phrase responses. Model defaults and user preferences differ; test the style you want rather than assuming a default. Be explicit.

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

**Why this matters:** A concrete format preference is easier to test than "write naturally". Check a short conversational answer and a structured artifact so the rule fits both.

### Writing Style: A Separate File

Format preferences (prose vs. bullets, emoji use) belong in the canonical policy: `AGENTS.md` for the shared setup, or `CLAUDE.md` for a Claude-only setup. Language quality rules are different — longer, more nuanced, and benefiting from independent maintenance. Put them in a dedicated file, e.g. `writing-style.md`, and load it with a read instruction in that canonical policy.

A writing style file typically contains:
- Banned words and phrases that produce generic AI-sounding output ("leverage", "delve into", "it's worth noting", "importantly")
- Sentence structure preferences — e.g. short sentences, active voice, no padding phrases
- Prose vs. list rules — when bullets are acceptable vs. when they fragment ideas that flow better as prose

This keeps the writing style evolvable — add new patterns as you notice them without changing the policy or native adapter. The read instruction is one line:

```
Read `writing-style.md` at the start of every session.
```

Keep the file under 60 lines. If it grows beyond that, you are likely cataloguing individual violations rather than capturing the underlying principle.

### 3. Critical Rules (the safety boundary)

State the scope of action authority: what the assistant may do now, what has standing approval, and what requires a new decision. [Guide 32](./32_ACTION_AUTHORITY.md) provides the consequence classes and proposal contract. The draft-only example below is one conservative personal policy, not a requirement to reconfirm every reversible edit.

Write this section as a hard rule, not a preference. Use "NEVER" intentionally — it signals a constraint, not a style suggestion.

**Example:**
```markdown
# Critical Rules
- NEVER send emails, create calendar events, or take real-world actions autonomously
- Always propose drafts and wait for explicit confirmation before anything is sent
- When drafting messages in a second language, produce polished text appropriate in form
  (formal, friendly, etc.) for the recipient — ready to send as-is
```

The third point shows a useful pattern: pair each constraint with a positive counterpart. "Never send autonomously" + "produce a polished draft ready to send" gives the assistant something concrete to do rather than just a prohibition.

A rule about judgment has to name a behaviour, the same as a rule about actions. "Be objective", "push back", "don't just agree with me" describe a disposition, so the assistant has to infer what to actually do, and the usual result is a token disagreement offered to satisfy the rule. Write the action instead: *state the strongest objection before saying whether you agree*, or *when I ask whether something will work, answer what would actually work first, then assess my version against it*. [Guide 27](./27_INDEPENDENT_JUDGMENT.md) has the full set and the honest limit on what a standing rule can buy.

For data projects, add an epistemic rule alongside the action rules: if the project holds both records you observed and records a script derived (predictions, scores, candidates), state that derived records are hypotheses and must never be presented as confirmed facts — and that the distinction stays explicit in every answer. See [Guide 14 §2, rule 7](./14_PERSONAL_DATA_LAYER.md).

---

<a id="layering-claudemd-vs-task-level-instructions"></a>

## Layering: Standing Rules vs. Task-Level Instructions

The canonical instruction file (`AGENTS.md` in the shared pattern, `CLAUDE.md` in a Claude-only project) contains standing rules within its scope. Task-specific instructions (how to run a weekly status digest, how to track contracts) belong in dedicated task files, which the assistant reads on demand.

The test for each rule: "Does this apply to every conversation, regardless of what I'm doing?" If yes, the canonical policy. If it is specific to a workflow, the relevant task file.

**Keep the canonical policy short.** Aim for under 30 lines for a personal policy. If it grows beyond that, check for task-specific instructions that belong elsewhere. Project policies carrying cross-reference checklists may legitimately run longer. In a shared setup, keep `CLAUDE.md` as the thin adapter; do not move shared rules into it to meet an `AGENTS.md` length target.

---

## File Access Tiers

These tiers describe project policy. Enforce sensitive boundaries with the actual runtime or connector permissions in [Guide 12](./12_SECURITY.md); neither a filename nor a prose rule denies access. In the examples below, put shared read instructions in `AGENTS.md` for dual-platform repositories, or in the project instructions for uploaded-source use.

Not every file in a project warrants the same access. Four tiers cover most cases:

- **Auto-read:** files the policy asks the assistant to read at session start — personal profile, writing style, active context. List these as explicit read instructions in the canonical policy.
- **Reference-only:** folders the assistant can access but reads on demand — knowledge bases, output archives, templates. Name them in the canonical policy so the assistant knows where to look, but don't auto-load them.
- **Read-only:** files the assistant can read but must not modify — master data, shared reference files, historical records. State this explicitly in the canonical policy: "The `masterdata/` folder is read-only — never edit files in it."
- **Excluded from context:** files the assistant should skip. Use the current surface's supported context controls or omit them from uploaded sources. Claude-specific ignore settings and visible `[IGNORE]` or `[ARCHIVE]` prefixes can communicate selection intent, but are not access controls. Protect sensitive files with actual runtime or connector permissions (see [Guide 12](./12_SECURITY.md)); do not assume another platform reads Claude configuration.

The token cost of auto-reading compounds across every session. Keep the auto-read tier small. Everything else earns its place by being referenced in a task, not by being loaded by default.

---


<a id="cross-reference-consistency-rules-project-claudemd"></a>

## Cross-Reference Consistency Rules

When a project has multiple linked artifacts — risk registers, action trackers, dependency registers, decision logs — add explicit rules telling the assistant what to check whenever any one changes. Without this, the assistant updates the register you mention and leaves the others stale.

Write the rule as a checklist tied to the ID type:

```markdown
**Cross-reference consistency:** Whenever an action, dependency, or risk is added or changed:
- New Risk → check for a linked Dependency and an Action tracking mitigation; link both ways.
- New Dependency → check whether it drives an existing Risk; link if so.
- New Action → record its source (Risk/Dependency/Decision) and ensure the source references it back.
```

This pattern applies whenever a project manages two or more linked registers. The PMO_TEMPLATE (`templates/PMO_TEMPLATE/`) shows a full implementation. For a simple project with one tracker, skip this — it is only needed when orphaned IDs are a real failure mode.

---

<a id="what-not-to-put-in-claudemd"></a>

## What Not to Put in Standing Instructions

- **Lists of capabilities** ("you can use Gmail, Calendar, etc.") — the assistant discovers available tools from its environment. This is different from an identity fact like the example's "Uses Gmail (address) and Google Calendar" — identity facts that change behaviour are fine.
- **Workflow steps** — these belong in task files
- **Information about the user's projects or contacts** — these belong in profile files
- **Rules that rarely apply** — do not clutter standing instructions with edge cases that come up once a month

---

<a id="when-claudemd-cannot-be-short-the-reference-companion"></a>

## When the Policy Cannot Be Short: the Reference Companion

The section above removes what does not belong. It does not help with the harder case: rules that
genuinely belong in the canonical policy, apply rarely, and are expensive to get wrong. "Never cite a section
number from memory — use the verified map" is not clutter, and deleting it is not an option, but it
earns its always-loaded cost only in the sessions that cite one.

Split the file rather than choosing between a bloated policy and a missing rule. Standing rules and
the working set stay in `AGENTS.md` for a shared setup; situational material moves to
`PROJECT_REFERENCE.md` beside it. A Claude-only setup may retain `CLAUDE.md` and
`CLAUDE_REFERENCE.md`.
The parent keeps a pointer at the exact place the rule would have been, naming the trigger rather
than the topic:

> **Before citing any section number, read `PROJECT_REFERENCE.md` § Citation Map.** Do not cite from
> memory.

The pointer is what makes this work. A companion file with no triggers in the parent is a file nobody
opens, and a trigger written as "see the reference file for more detail" is one nobody acts on. Write
the condition under which reading is mandatory.

This is the project layer of progressive disclosure ([Guide 02](./02_PROMPTING_BASICS.md) §
Progressive disclosure) — the same split as `SKILL.md` → `references/` and `TASK.md` →
`TASK_REFERENCE.md`. Use it where a project is genuinely complex: a long-running case file, a
regulated domain, a codebase with real invariants. Do not use it to avoid pruning. A policy that is
long because nobody maintained it needs the *Maintenance* section below, not a second file.

---

## Maintenance

The canonical policy should evolve. When you repeatedly correct a shared behaviour, update `AGENTS.md` in a dual-platform setup, or `CLAUDE.md` in a Claude-only setup. Keep product-specific changes in their native adapter or setup section, then reload or refresh each supported surface. Common triggers:

- The assistant keeps doing something you don't like (add a rule)
- You keep explaining the same context at the start of sessions (add it to the identity section)
- A rule has never mattered (remove it — dead rules dilute the live ones)

A good canonical policy is a living document that reflects a few months of real use, not a first draft from day one.

---

<a id="quick-reference-anatomy-of-a-good-claudemd"></a>

## Quick Reference: Anatomy of a Good Project Policy

```
# About [User]
[Who they are, where, timezone, language preference]

# Communication Style
[Format, verbosity, tone preferences]

# Critical Rules
[What the assistant may never do; what it should always do instead]
```

That is usually enough. Add sections only when they solve a real behavioural problem.

---

## Real-World Example

Below is a personal policy example. Put its shared content in `AGENTS.md` for a dual-platform setup, or `CLAUDE.md` for Claude-only use. It is intentionally short — 18 lines of real content — and every line changes behaviour.

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

**Giving this to an assistant:**
> "Read 01_PROJECT_INSTRUCTIONS.md and help me write my canonical policy and native entry point for my chosen surface. Ask me the key questions you need answered."

The assistant will walk you through identity, style, and rules — and produce a draft in the format above.

**Faster alternative:** `tasks/setup-claude-md.md` does this end-to-end without reading the guide first. `tasks/audit-claude-md.md` reviews the existing instruction setup against this guide's checklist.

---

## Second Example: Developer Setup

For comparison — a canonical policy for a software engineer using an assistant for code review, meeting prep and async communication. Apply the same shared-policy/native-adapter placement rule. Same three sections, different rules.

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
- When I ask for a code review, state the strongest objection to the code before saying whether it looks fine

# Critical Rules
- NEVER commit, push, or run destructive commands autonomously
- For anything that modifies files or runs code: show the command and wait for confirmation
- When I paste code, assume it is from my codebase unless I say otherwise
```

**What is different here:**
- The critical rule is about code operations, not email. The pattern is the same — "never act autonomously, show first" — but adapted to the domain.
- "Don't simplify" is the opposite of what many users want, but correct for someone who works technically and finds over-explained answers slow.
- "Assume it is from my codebase" avoids the assistant treating every code snippet as a standalone hypothetical with invented context.

Both examples use the same three-section structure. The sections stay fixed; the content inside reflects real use.
