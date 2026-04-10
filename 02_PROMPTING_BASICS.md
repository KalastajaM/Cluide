# Prompting Basics: Writing Instructions That Work

*Last reviewed: April 2026*

> The quality of Claude's output is determined almost entirely by the quality of the instructions it receives. This guide is about writing better instructions — whether in CLAUDE.md, a skill, a task, or a chat message.

> **Companion guides:** [Guide 01 — CLAUDE.md](./01_CLAUDE_MD.md) for applying these principles to your standing instructions. [Guide 03 — Skills](./03_SKILLS.md) for skill descriptions and trigger phrases.

> **Giving this guide to Claude:**
> "Read 02_PROMPTING_BASICS.md and help me improve my [CLAUDE.md / SKILL.md / task instructions]. Read the file I want to improve and apply the principles from the guide."

---

## The Anatomy of a Good Instruction

Every strong instruction has four parts. You don't always need all four, but knowing what's missing explains why output is off.

**1. Context** — who, what, why
What Claude needs to know about the situation to produce a relevant response. Without this, Claude fills in the gaps with generic assumptions.

> Weak: *"Write a summary."*
> Strong: *"You are summarising a security incident report for a non-technical manager. The audience has no IT background. Focus on business impact, not technical details."*

**2. Task** — what to produce
The specific output Claude should create. Be precise — "analyse" can mean anything; "list the top 3 risks and recommend one mitigation per risk" is specific.

> Weak: *"Analyse the email."*
> Strong: *"Read the email and identify: (a) any action item addressed to me, (b) any deadline mentioned, (c) the sender's tone. Then draft a brief reply acknowledging receipt."*

**3. Constraints** — what not to do, limits, format rules
What Claude should avoid, the length target, the format, the tone. Constraints are as important as the task itself — they prevent the default responses that don't fit your needs.

> Weak: *"Keep it professional."*
> Strong: *"Keep the response under 5 sentences. Do not use bullet points. Do not start with 'Certainly' or 'Of course'. Match the formality level of the original message."*

**4. Output format** — exactly what it should look like
Show a template or example of the expected output. This single addition more than anything else produces consistent results.

> Weak: *"Produce a structured summary."*
> Strong: Show an exact template (see the section below).

---

## Show an Example, Not a Description

Descriptions of what you want are weaker than examples of what you want. Claude learns from the shape of a real output far faster than from abstract instruction.

**Instead of:**
> "Produce a concise action-oriented email summary."

**Do this:**
````markdown
## Output Format
Produce the output in exactly this structure:

```
## Email Summary — [Date]

**From:** [sender name]
**Subject:** [subject line]

**In brief:** [1 sentence: what this email is about]

**Action needed:** [Yes/No]
**If yes:** [What, by when, from whom]

**Context:** [1–2 sentences of background if relevant, otherwise omit]
```
````

When Claude sees the exact structure, headers, and field names you expect, it produces the same shape every time. When it only reads a description, it invents a structure each run.

---

## Specify What NOT to Do

Negative constraints are just as useful as positive ones. If you've corrected Claude on the same thing three times, it belongs in your instructions as a "not" rule.

**Common negatives worth including:**

| Unwanted behaviour | Instruction to prevent it |
|---|---|
| Starts responses with "Certainly!" / "Of course!" | "Do not start responses with affirmations like 'Certainly', 'Of course', or 'Absolutely'." |
| Adds unnecessary disclaimers | "Do not add disclaimers or caveats unless I ask for them." |
| Produces walls of text | "Use bullet points and headers for any response longer than 3 sentences." |
| Rephrases instead of edits | "When I ask you to edit text, change what needs changing — do not rewrite the whole thing." |
| Over-explains simple tasks | "For routine requests, produce the output directly without explaining your approach." |
| Invents information | "If you don't have enough information to answer accurately, ask me rather than guessing." |

These belong in your `CLAUDE.md` if they apply to all interactions, or in `SKILL.md` if they apply to one specific workflow.

---

## Use Explicit Output Formats

Three levels of format specificity, from weakest to strongest:

**Level 1 — No format (weakest):** "Write a report."
Claude invents the structure, length, and style. Different every time.

**Level 2 — Description:** "Write a concise report with a summary and action items."
Better, but "concise" is subjective and "action items" is ambiguous.

**Level 3 — Template (strongest):** Show the exact structure with field names, headers, and one filled example.
````markdown
Produce output in this exact format:

```
## Weekly Status — [Week of DATE]

**Overall:** [Red / Amber / Green] — [one sentence why]

**Completed this week:**
- [Item]
- [Item]

**Blocked / at risk:**
- [Item] — [what the block is]

**Next week:**
- [Item]
```
````

Use Level 3 for anything that runs repeatedly — skills, tasks, any instruction you've set up in CLAUDE.md. Reserve Level 2 for one-off chat requests.

---

## Writing Skill Descriptions: Triggers, Not Titles

The `description:` field in a SKILL.md file is not a title. It is a **trigger pattern** — the set of phrases and situations that tell Claude "activate this skill now."

Most skill descriptions that fail are too short and too formal.

**Weak description (too short, too formal):**
```yaml
description: Email summarisation and action tracking skill.
```
This will only trigger if the user literally says something very close to those words.

**Strong description (natural phrases, multiple triggers):**
```yaml
description: >
  Use this skill when the user wants to review their email, check what needs
  a reply, get a summary of their inbox, or identify action items from messages.
  Also triggers when the user says things like: "what's in my inbox",
  "catch me up on email", "what do I need to reply to", "any urgent emails?",
  "check my messages", or "summarise my emails from today".
```

**The test:** Read your description aloud as if you were telling a colleague when to use this skill. Does it cover the way you naturally ask for it? If you say "can you check my inbox?" but the description only mentions "summarise emails", it may not trigger.

---

## Debugging a Bad Prompt

When output is consistently wrong, use this process:

**Step 1: Strip it down.**
Remove all constraints and special instructions. Run the bare minimum: context + task only. Does Claude produce the right kind of output (even if imperfect)?

If yes → the constraints were the problem. Add them back one at a time.
If no → the task description itself is unclear. Rewrite it.

**Step 2: Add back one constraint at a time.**
Each constraint you add should make the output better. If adding a constraint makes things worse, that constraint is either wrong or contradicts something else.

**Step 3: Look for contradictions.**
Common contradictions:
- "Be brief" + "Include all relevant details" → Claude will flip between interpretations
- "Always suggest options" + "Give me one recommendation" → Claude won't know which to follow
- "Respond formally" in CLAUDE.md + "Use casual language" in skill → skill wins, but inconsistently

Pick one. Remove the other.

**Step 4: Check if you're describing the result, not the process.**
"Analyse carefully and think through the implications" describes the process. "List the top 3 risks in order of likelihood with one mitigation each" describes the result. The second is always better.

---

## Common Mistakes and Fixes

### Mistake 1: Too Vague

| Instead of | Write |
|---|---|
| "Be helpful" | "When the user asks for [X], do [Y] in [Z] format" |
| "Summarise this" | "Summarise in 3 bullet points, each under 15 words" |
| "Keep it professional" | "Match the formality of the original; no slang, no emoji" |
| "Be concise" | "Maximum 5 sentences unless the user asks for more" |

---

### Mistake 2: Everything in CLAUDE.md

CLAUDE.md should contain only rules that apply to **every interaction**. Workflow steps, output templates, and task-specific rules belong in `SKILL.md` or `TASK.md`.

**In CLAUDE.md:**
- Communication style, tone, language
- Standing rules that override Claude's defaults
- Who you are (2–3 lines)

**In SKILL.md:**
- Workflow steps for that specific skill
- Output format template
- Edge cases for that skill

**In TASK.md:**
- Full workflow for the scheduled task
- All task-specific rules and logic
- Run state tracking instructions

---

### Mistake 3: Describing Intent, Not Behaviour

Instructions that describe what you want Claude to achieve (rather than what to do) produce inconsistent results because Claude has to infer the behaviour.

| Describes intent | Describes behaviour |
|---|---|
| "Understand context before responding" | "Read the last 3 messages before answering, then summarise the situation in one sentence before proceeding" |
| "Be thorough" | "Check each item against the criteria in section 3 before moving to the next" |
| "Stay on topic" | "If the user asks about [X] while we are working on [Y], acknowledge it and return to [Y]: 'Noted — I'll come back to that after we finish [Y].'" |

---

### Mistake 4: Forgetting the Output Format

If you don't specify a format, Claude will pick one. The one it picks will be:
- Different each run
- Not quite what you expected
- Hard to use downstream (e.g. in another task or a template)

**Always add an output format section** to skills and tasks. For chat, describe the format in your request.

---

## Applying These Principles to Your Setup

**To improve CLAUDE.md:**
> "Read 02_PROMPTING_BASICS.md and then read my current CLAUDE.md. For each rule, tell me whether it's specific enough to change Claude's behaviour reliably. Rewrite any that are too vague."

**To improve a skill description:**
> "Read 02_PROMPTING_BASICS.md and then read my [skill-name] SKILL.md. Is the description strong enough to trigger reliably? Rewrite it using the guidance in the prompting guide."

**To add an output format to a skill or task:**
> "Read my [task name] TASK.md. The output format section is too vague. Look at the last 3 entries in LAST_RUN.md to see what the output actually looks like, then write a proper output format template to match it."
