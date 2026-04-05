# Best Practices: Designing Skills for a Personal Assistant

A skill is a SKILL.md file (plus optional supporting files) that tells the assistant how to perform a specific, recurring type of task — producing formatted meeting notes, triaging support tickets, drafting client status updates, and so on. Good skills make the assistant dramatically more reliable at the things you do repeatedly. This document explains how to write them well.

---

## Why Skills Exist

Without a skill, the assistant has to figure out your preferences from scratch every time. With a skill, it consults a set of instructions that captures: what to do, how to format it, what to avoid, what tools to use, and how to handle edge cases. The skill is the accumulated wisdom of everything you would otherwise have to re-explain.

---

## The Anatomy of a Skill

A skill lives in a folder and requires at minimum a single file:

```
my-skill/
└── SKILL.md          (required)
```

For more complex skills, you can add:

```
my-skill/
├── SKILL.md
└── references/       (detailed docs the skill reads on demand)
└── scripts/          (reusable Python/bash scripts)
└── assets/           (templates, icons, fonts)
```

The SKILL.md file has two parts: a YAML frontmatter block, and the instruction body.

---

## The Frontmatter: Name and Description

```yaml
---
name: my-skill-name
description: >
  What this skill does and when to use it. (The triggering mechanism.)
---
```

**The description field is the most important part of any skill.** It is how the assistant decides whether to consult the skill at all. A vague description = a skill that never triggers. A precise description = a skill that activates exactly when it should.

**Write the description to be slightly "pushy".** It should name:
1. What the skill does
2. The specific phrases or situations that should trigger it — including casual and implicit phrasings

**Weak description (undertriggers):**
```yaml
description: Helps the user write client update emails.
```

**Strong description (triggers reliably):**
```yaml
description: >
  Produces formatted client status updates and project progress emails. Trigger
  this skill whenever the user wants to send a client an update, check-in, or
  summary — even casual phrasings like "shoot the client a note", "update Sarah
  on where we are", or "write something for the weekly status". Use when the user
  gives bullet points, a rough summary, or just describes the situation. Always
  confirm the desired tone (brief/formal vs. conversational) unless it's already
  clear from context.
```

The second version lists the implicit triggers ("shoot the client a note") and tells the assistant what to do proactively (confirm tone). This prevents a common failure mode where the assistant processes the request itself rather than consulting the skill.

---

## The Skill Body

The body is markdown instructions the assistant reads when the skill activates. A good body covers:

### 1. Core Responsibilities (3–6 bullet points)

What the skill is fundamentally responsible for. Keep this short — it orients the assistant before it reads the details.

### 2. Workflow / Steps

The procedural heart of the skill. Use numbered steps for sequential actions, use a table for decision logic. Be concrete:

- Name the tools to call (`gmail_create_draft`, `gcal_create_event`, etc.)
- Specify what to ask the user at each stage
- Say what to do when a step fails

### 3. Output Format

If the skill produces a structured output (a task list, a briefing document, a formatted report), show exactly what it should look like. Include a code block example. Ambiguity in output format leads to inconsistency across sessions.

### 4. What the Assistant Can and Cannot Do

If there is a constraint (e.g., "Claude can create email drafts but cannot send them"), state it clearly in the skill. This prevents the assistant from either overstepping or under-delivering:

```
> Note: Claude can create drafts but cannot send emails directly.
> The user sends from Gmail.
```

### 5. Tone and Format Rules

How should this skill's output be written? Formal or casual? Emoji use? Language? If different from the global CLAUDE.md rules, say so explicitly.

### 6. Edge Cases

A few "what if" clauses that resolve common ambiguities. Examples:
- "If the email is in a foreign language, read it and present the task summary in the user's preferred language"
- "If there are 15+ unread emails, focus on the 10 most urgent"
- "If the user doesn't specify a tone, offer two variants: formal and friendly"

### 7. Example Interaction

One concrete example showing a realistic input and the ideal output. This is the fastest way to convey expectations. It also serves as a sanity check when you're editing the skill — if the example looks wrong, the skill's instructions are wrong.

---

## Progressive Disclosure: Keeping Skills Lean

Aim for under 500 lines in SKILL.md. If you need more:

- Move detailed reference content to a `references/` subfolder
- Reference those files from SKILL.md with a clear note: "For full schema, see references/schemas.md"
- Put reusable scripts in `scripts/` — the assistant can execute them without reading every line into context

The goal is that reading SKILL.md takes <60 seconds and the assistant is ready to go. Long skills that dump everything into one file are harder to follow and slower to load.

---

## Memory Within a Skill

If your skill needs to remember things between sessions (shopping habits, snoozed tasks, important contacts), be explicit about what to store and the format:

```markdown
## Memory & Continuity
Use memory to track:
- Snoozed tasks: "Snoozed: [task] — due [date]"
- High-priority senders: "High-priority sender: name@email.com"
- Recurring preferences: "User prefers [brand] at [store]"
```

Without explicit memory instructions, the skill will re-learn the same things from scratch every session.

---

## Common Skill Mistakes

**Vague description:** The skill never triggers, or triggers for things it shouldn't. Fix: rewrite the description with concrete phrases the user would actually type.

**Missing output format:** The skill produces different layouts every session. Fix: include an explicit format example with a code block.

**No edge case handling:** The skill breaks on anything slightly unusual. Fix: add 3–5 "if X, do Y" clauses for the most common deviations.

**Overlong SKILL.md:** The skill is slow to activate and hard to maintain. Fix: move reference material to a `references/` subfolder.

**Omitting tool names:** The skill says "check the calendar" without naming `gcal_list_events`. The assistant may use a different approach each time. Fix: name the exact tools. Not sure what tools are available in your setup? See [Guide 08 — MCP Servers](./08_MCP_SERVERS.md) for how to discover them.

---

## Skill vs. CLAUDE.md vs. Task File

| What | Where |
|------|-------|
| Universal preferences (language, tone, safety rules) | CLAUDE.md |
| Recurring user-triggered actions (meeting notes, status updates, document drafts) | Skill |
| Automated scheduled workflows (daily digest, contract expiry checks) | Task file (TASK.md) — see guides 04 and 05 |

When in doubt: if the user asks for it ad hoc and it needs consistent, detailed behaviour → skill. If it runs on a schedule without the user asking → task file.

---

## Real-World Examples

Three working skills from a personal setup. Each illustrates a different pattern.

---

### gmail-task-manager — A skill with clear triage logic

**What it does:** Scans Gmail for unread emails, extracts actionable items, and presents them as a prioritised task list. Can draft replies, create calendar events, and snooze tasks.

**Key design choices:**
- **Description lists implicit triggers** — "what's pending?", "catch me up", "any follow-ups?" — so the skill activates from natural phrasing, not just a precise command.
- **Scanning strategy is explicit** — specific Gmail search queries (`is:unread newer_than:7d`) are written into the workflow, not left to Claude to figure out.
- **Output format is shown with an example** — the 🔴🟡🟢 priority structure is defined once and reused every run.
- **"Claude can create drafts but cannot send"** — the constraint is stated clearly, so Claude never oversteps.
- **Edge cases are named** — too many emails (15+), Finnish-language emails, long threads — each has a defined handling rule.

**What makes the description work:**

```yaml
description: >
  Scans Gmail for actions, tasks, and follow-ups and turns them into a clear,
  prioritised task list. Trigger this skill whenever the user asks to check their
  email for things to do, wants to know what needs their attention, asks
  "what do I need to action?", "any tasks in my email?", "what's pending?",
  "check my inbox", "any follow-ups?", "what emails need a reply?",
  "catch me up on my emails", or any similar request related to managing
  email-based actions.
```

This is a strong description: it names the implicit trigger phrases, is specific about the task, and uses "trigger this skill" explicitly.

---

### grocery-list-assistant — A skill that learns over time

**What it does:** Builds shopping lists for Finnish supermarkets (Prisma, K-Citymarket), learns from habits, suggests items proactively, and can email the finished list to the user.

**Key design choices:**
- **Memory is built into the skill** — the skill maintains a running model of staples, brand preferences, and run-out items using Claude's persistent memory.
- **Proactive suggestion on session start** — the skill doesn't wait to be told what to add; it surfaces what you probably need based on past behaviour.
- **Output format is grouped by store section** — produce/dairy/bread etc. — which mirrors how a real store is laid out.
- **Recipe-based ingredient extraction** — "I want to make risotto" maps to a specific ingredient list, cross-checked against likely in-stock items.

**The grocery skill is a good model for any skill that benefits from cross-session learning** — the memory structure (staples, brand preferences, run-outs, avoided items) can be adapted to other domains.

---

### finnish-message-assistant — A skill for structured output variants

**What it does:** Writes Finnish messages, emails, and texts. Produces two tone variants by default (formal and casual) with notes on the differences.

**Key design choices:**
- **Input-agnostic** — handles English text, bullet points, or a situation description. The skill normalises inputs before producing output.
- **Always two versions** — unless tone is already specified. This is baked in as a default, not something the user has to ask for each time.
- **Format is shown as an example** — the formal/casual pair, subject lines, and "key differences" note are all illustrated with a concrete worked example.
- **SMS/WhatsApp has separate rules** — shorter, no openers, no formal variant unless asked. Named explicitly because the user texts in Finnish regularly.

**Giving this to Claude:**
> "Read 02_SKILLS.md and create a skill for [what you want]. Follow all the best practices in the guide — strong description, workflow steps, output format example, and at least 3 edge cases."
