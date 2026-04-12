# Guide 20: Interactive Prompting — Claude Code Features & Patterns

*Last reviewed: April 2026*

> Claude Code has interactive features that go beyond writing instructions well. This guide covers the tools and patterns that shape *how you work with Claude in a session* — file references, plan mode, question dialogs, and keeping the context window clean.

> **Companion guides:** [Guide 02](./02_PROMPTING_BASICS.md) covers instruction quality — context, task, constraints, and output format. [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers Claude Code vs. Cowork — when to use each. This guide covers what to do *during* a Claude Code session.

> **Giving this guide to Claude:**
> "Read 20_INTERACTIVE_PROMPTING.md and apply the patterns here to help me set up / improve / debug [my workflow / this task / this skill]."

---

## `@` File References

When you mention a file in a message using `@filepath`, Claude reads the file before responding. This is faster and more accurate than describing the file's contents.

**Without `@` reference:**
> "I have a config file in the auth module — it sets up the JWT token lifetime. Can you make the timeout configurable?"

Claude has to guess where the file is, what it contains, and what "configurable" means in context.

**With `@` reference:**
> "Read `@src/auth/config.ts` and make the JWT timeout configurable via an environment variable."

Claude opens the file, sees the exact structure, and makes a targeted edit.

### When to use it

| Situation | Use `@` reference? |
|---|---|
| You want Claude to edit a specific file | Yes — always |
| You want Claude to follow an existing pattern | Yes — point to the example file |
| You're asking a general question not tied to a file | No |
| You're describing a problem but don't know which file | No — ask Claude to find it first |

### Where `@` references work

- Chat messages
- CLAUDE.md (e.g. `@docs/style-guide.md` to import shared rules)
- Skill descriptions and task instructions

---

## AskUserQuestion: Input Types and Options

When Claude needs a decision from you mid-task, it uses the `AskUserQuestion` tool to present a structured choice rather than a wall of prose. Understanding the options helps you write skills and tasks that make good use of it.

### Input types

**`single_select`** (default) — one choice only. Use when options are mutually exclusive.

> "Which environment should I deploy to?"
> - Staging
> - Production

**`multi_select`** — multiple choices allowed. Use when options aren't mutually exclusive.

> "Which checks should I run before committing?"
> - Run tests
> - Run linter
> - Check types
> - Verify build

Set `multiSelect: true` in the question definition.

### Option fields

Each option has two useful fields beyond the label:

**`description`** — a short explanation shown alongside the option. Useful when the label alone is ambiguous.

```yaml
options:
  - label: "Soft delete"
    description: "Set a deleted_at timestamp. Row stays in the database."
  - label: "Hard delete"
    description: "Remove the row permanently. Cannot be undone."
```

**`preview`** — Markdown or HTML rendered when the option is focused. Use for code comparisons or visual mockups.

```yaml
options:
  - label: "Option A"
    preview: |
      ```typescript
      // Uses a factory function
      const client = createClient({ timeout: 5000 })
      ```
  - label: "Option B"
    preview: |
      ```typescript
      // Uses a class constructor
      const client = new Client({ timeout: 5000 })
      ```
```

This lets you compare two code patterns side by side before choosing.

### Header field

The `header` field (max 12 characters) appears as a chip/tag above the question. Keep it short and descriptive: `"Environment"`, `"Auth method"`, `"Output fmt"`.

### What NOT to include as an option

Don't add an "Other" option — it's always provided automatically as a free-text fallback. Adding it explicitly creates a duplicate.

### Limits

- 1–4 questions per call
- 2–4 options per question (plus the automatic "Other")

---

## Plan Mode as a Workflow Pattern

Plan mode separates *understanding the problem* from *solving it*. When Claude is in plan mode, it reads files and asks questions without making any changes. You review the plan, adjust it if needed, then approve it.

### What it prevents

The most common cause of wasted effort is Claude solving the wrong problem — implementing X when you meant Y, or touching the wrong files. Plan mode forces a checkpoint before code is written.

### When to use it

| Situation | Use plan mode? |
|---|---|
| Adding a feature across multiple files | Yes |
| Fixing a bug with an unclear root cause | Yes | 
| A one-line change in a known location | No |
| You're not sure what approach to take | Yes — let Claude propose one |

### How to trigger it

Ask Claude to plan before acting:

> "Before you make any changes, read the relevant files and tell me your approach."

Or explicitly:

> "Enter plan mode and propose how you'd implement X. Don't write any code yet."

In Claude Code, plan mode is also available as a built-in mode — Claude will read files, run searches, and ask clarifying questions, then present a plan for your approval before doing anything irreversible.

---

## In-Session Prompting Patterns

### The interview pattern

For large or ambiguous features, ask Claude to interview you before starting:

> "Before you implement anything, ask me the questions you need answered to do this well. I'll answer them, then you can proceed."

This surfaces assumptions you didn't know you were making. Claude will ask things like: "Should this work for unauthenticated users?", "Is there an existing error format I should match?", "Do you want this to be reversible?" — questions you'd otherwise discover mid-implementation.

### Explore → Plan → Implement → Verify

For non-trivial tasks, four phases produce better results than jumping straight to implementation:

1. **Explore** — Claude reads relevant files, searches the codebase, understands existing patterns
2. **Plan** — Claude proposes an approach; you review and adjust
3. **Implement** — Claude writes the code
4. **Verify** — Claude (or you) confirms the result against the original requirement

You can enforce this explicitly:

> "First, explore how auth is currently handled in this codebase. Then propose an approach. Don't implement until I approve the plan."

### Point to existing patterns

Describing what you want is weaker than showing it:

**Weak:**
> "Add error handling that follows the project's style."

**Strong:**
> "Add error handling following the pattern in `@src/api/users.ts`. Match the structure exactly — same error types, same logging call, same response shape."

When Claude can see a real example, it replicates it precisely. When it's working from a description, it invents something plausible.

### Include verification criteria

Tell Claude what "done" looks like. This gives it a stopping condition and makes it easier to check its own work.

**Without criteria:**
> "Add rate limiting to the API."

**With criteria:**
> "Add rate limiting to the API. Done when: (1) the test in `tests/test_rate_limit.py` passes, (2) requests over the limit return HTTP 429, (3) the limit resets after 60 seconds."

Claude will check these conditions before declaring the task complete.

---

## CLAUDE.md Structural Tips

These tips extend [Guide 01](./01_CLAUDE_MD.md) with structural features that affect how instructions load and get used.

### `@` imports for modular CLAUDE.md files

A CLAUDE.md file can import other files using the same `@filepath` syntax:

```markdown
# My Assistant

@docs/style-guide.md
@docs/project-conventions.md

## Standing instructions
...
```

Use this to:
- Share common rules across multiple projects without copy-pasting
- Keep the root CLAUDE.md short while pulling in detailed references only when needed
- Maintain a single source of truth for conventions used across repos

### Length discipline

A long CLAUDE.md file causes instructions to be ignored. The more rules you add, the less reliably any single rule is followed.

**Signs your CLAUDE.md is too long:**
- You've added rules to fix behaviour that was already in the file
- You're repeating the same point in different words
- You have rules that only apply to one specific task or skill

**What to do:**
- Move task-specific rules to the relevant `SKILL.md` or `TASK.md`
- Remove rules that describe Claude's default behaviour (they're redundant)
- Merge rules that say the same thing

Aim for a CLAUDE.md that takes under two minutes to read.

### Emphasis markers

For rules that are genuinely critical — where a single mistake causes real damage — use emphasis:

```markdown
IMPORTANT: Never commit changes to the `production` branch directly. Always use a pull request.

YOU MUST read the existing test file before adding new tests — do not create a second test file.
```

Use these sparingly. If everything is `IMPORTANT`, nothing is.

---

## Context Hygiene

Claude's context window holds the full conversation. As a session grows, earlier content competes with newer content for attention — and older instructions can subtly influence responses in ways you don't expect.

### Use `/clear` between unrelated tasks

When you finish one task and start a completely different one, clear the context:

```
/clear
```

This prevents the first task's files, decisions, and constraints from leaking into the second. It's especially important when switching between different areas of the codebase.

### Use subagents for research-heavy subtasks

When Claude needs to explore a large codebase, search many files, or fetch external documentation, that work fills the context window with results you may not need to keep.

Instead of doing it all in the main conversation:

> "Use a subagent to find all the places in the codebase that call the `sendEmail` function. Report back with just the file paths and line numbers."

The subagent does the exploration in a separate context, then returns a concise summary. Your main context window stays clean.

### When context is near its limit

Signs you're approaching the limit: responses start omitting details they'd normally include, or Claude seems to "forget" instructions from earlier in the session.

What to do:
1. Summarise what's been completed: "Summarise the changes made so far in 5 bullet points."
2. Save that summary somewhere (a file, a note)
3. Run `/clear`
4. Start a new session, pasting the summary as context

---

## Applying These Patterns

**To make better use of file references:**
> "Read 20_INTERACTIVE_PROMPTING.md. Then look at my recent messages and identify places where I described a file instead of referencing it with `@`. Show me the pattern."

**To improve a skill that asks questions:**
> "Read 20_INTERACTIVE_PROMPTING.md. Then read my [skill name] skill. Does the AskUserQuestion call use descriptions and previews effectively? Improve it."

**To set up a clean workflow for a new feature:**
> "Read 20_INTERACTIVE_PROMPTING.md. I want to implement [feature]. Use the interview pattern first — ask me what you need to know, then propose a plan before writing any code."
