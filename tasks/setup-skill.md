# Task: Setup Skill

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-skill.md`
> **Source guide:** `03_SKILLS.md`

## Purpose
Create a well-structured skill by interviewing the user and generating a `SKILL.md` that triggers reliably, follows a consistent workflow, and handles edge cases. Follows the conventions in Guide 03.

The most important part of any skill is the description — it controls whether the skill triggers at all.

---

## Instructions

### Step 1 — Interview the user

Ask the following questions. Collect all answers before writing anything.

**What the skill does:**
> 1. What task should this skill handle? Describe it in one sentence.
> 2. When should it trigger? What would you say to Claude to kick it off? Give me 3–5 example phrases — including casual ones.
> 3. What does the ideal output look like? (Paste an example, describe a format, or say "I'm not sure yet".)

**Inputs and context:**
> 4. What information do you typically have when you need this skill? (e.g. a rough draft, bullet points, a situation description, a URL)
> 5. Does it need any MCP tools — email, calendar, GitHub, filesystem? If unsure, describe what the skill needs to *do* and I'll figure out the tools.

**Behaviour:**
> 6. Should the skill ask clarifying questions, or make assumptions and proceed?
> 7. Are there any strong "never do this" rules for this skill? (e.g. "never send, only draft")
> 8. Any edge cases you already know about? (e.g. "sometimes I'm in a hurry and just need the short version")

**Memory (optional):**
> 9. Should the skill remember anything between sessions? (e.g. preferences, recurring contacts, past decisions)

After collecting answers: "Thanks — let me draft your skill."

### Step 2 — Determine the skill name and folder

Derive a kebab-case name from the skill description (e.g. `client-status-update`, `meeting-notes`, `finnish-message`).

Ask: "I'll create this as `[name]/SKILL.md`. Does that name work?"

Check if the skill folder already exists:
```bash
ls ~/.claude/skills/[name]/ 2>/dev/null && echo "exists" || echo "new"
```

If it exists, read the existing `SKILL.md` and tell the user. Ask whether to overwrite or improve it.

### Step 3 — Draft the SKILL.md

Write using the full structure below. Every section must be present — don't skip any.

```markdown
---
name: [name]
description: >
  [What the skill does and when to trigger it. Be "pushy" — list:
   1. What it does
   2. Specific trigger phrases including casual ones
   3. What to do proactively if unclear (e.g. "confirm tone unless already clear")
   Aim for 4–8 lines. Vague descriptions cause the skill to never trigger.]
---

## Purpose
[2–3 sentences: what this skill is responsible for and why it exists.]

## Core Responsibilities
- [Bullet 1]
- [Bullet 2]
- [Bullet 3 — keep to 3–6 items]

## Workflow
[Numbered steps. For each step that uses an MCP tool, name the exact tool.
For each step that needs user input, specify what to ask.
For each step that can fail, specify the fallback.]

1. [Step]
2. [Step]
...

## Output Format
[Show exactly what the output should look like using a code block example.
Include headers, bullet style, field names. Ambiguity here = inconsistent output.]

```
[example output]
```

## Constraints
[What the skill can and cannot do. Use "NEVER" for hard limits.
Always pair a prohibition with a positive: "NEVER send — always create a draft the user reviews."]

## Tone and Format Rules
[How this skill's output should be written. Override CLAUDE.md rules only if needed for this skill.]

## Edge Cases
- If [situation]: [handling]
- If [situation]: [handling]
- If [situation]: [handling]
[At least 3 edge cases. These prevent the skill from breaking on anything slightly unusual.]

[## Memory (include only if the skill needs cross-session memory)]
[## Use memory to track:]
[- Item: format]
```

**Real-world example** — a completed SKILL.md for a meeting notes skill:

```markdown
---
name: meeting-notes
description: >
  Summarize meeting notes into a structured format with action items.
  Trigger when the user says "summarize this meeting", "meeting notes",
  "what were the action items", "write up the meeting", or pastes
  raw meeting notes or a transcript. Also trigger when the user says
  "clean up these notes" and the content looks like a meeting.
---

## Purpose
Turn raw meeting notes or transcripts into a clean summary with decisions,
action items, and follow-ups. Saves 10–15 minutes of post-meeting cleanup.

## Core Responsibilities
- Extract key decisions made
- Identify action items with owners and deadlines
- Summarize discussion points concisely
- Flag unresolved questions

## Workflow
1. Read the provided notes or transcript
2. Identify participants from the content
3. Extract and organize into the output format below
4. If any action item lacks an owner, ask: "Who owns [action]?"

## Output Format
```
## Meeting: [topic or title]
**Date:** [date] · **Participants:** [names]

### Decisions
- [Decision 1]
- [Decision 2]

### Action Items
- [ ] [Action] — @[owner], due [date]
- [ ] [Action] — @[owner], due [date]

### Key Discussion Points
- [Point 1: 1–2 sentences]
- [Point 2: 1–2 sentences]

### Open Questions
- [Question needing follow-up]
```

## Constraints
- NEVER invent decisions or actions not present in the source
- If the notes are too vague to extract actions, say so rather than guessing

## Edge Cases
- If no clear action items exist: include "No action items identified" rather than omitting the section
- If the input is a partial transcript (mid-conversation): note "Partial transcript — summary may be incomplete"
- If participants aren't named: use "Participant 1", "Participant 2" and ask the user to fill in names
```

### Step 4 — Review with the user

Show the draft and ask:
> "Does this look right? Pay particular attention to:
> - The description — does it include all the phrases you'd actually say?
> - The output format — does the example match what you want?
> - The edge cases — anything missing?"

Make requested changes.

### Step 5 — Write the file

```bash
mkdir -p ~/.claude/skills/[name]
```

Write the approved content to `~/.claude/skills/[name]/SKILL.md`.

If the skill needs a `references/` subfolder (for schemas, detailed specs, domain content that shouldn't load every activation), create it and note: "Add any detailed reference files here — name them from SKILL.md with 'See references/[file]'."

### Step 6 — Confirm

Tell the user:
- Where the skill was written
- The trigger phrases in the description
- "Test it: start a new Claude session and use one of the trigger phrases. If it doesn't activate, the description may need stronger phrasing — re-run this task or edit the description directly."
- "To audit the skill later: run `tasks/audit-skill.md`."
