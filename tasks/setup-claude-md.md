# Task: Setup CLAUDE.md

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/setup-claude-md.md`
> **Source guide:** `01_PROJECT_INSTRUCTIONS.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

The filename is retained for existing callers; this task creates the instruction entry point for the selected surface. Before Step 1 choose the target:

- **Codex local:** inspect ancestor instructions and `AGENTS.override.md` before creating or editing project `AGENTS.md`. Use Steps 2–4 to draft the shared policy; Step 5 writes `AGENTS.md`, not a pointer relying on Claude import syntax. Add nested files only where their scope is needed, then verify from that working directory in a fresh Codex session.
- **Dual-platform:** move shared rules into `AGENTS.md`, retaining one copy. Write `CLAUDE.md` with `@AGENTS.md`, an explicit read fallback for surfaces without imports, and only Claude-specific rules. Follow `setup-dual-platform.md` for the capability list and app mirrors.
- **ChatGPT source project:** draft the policy using Steps 2–4, produce it as a source artifact, and provide this project-instructions bootstrap: “Read the current project policy source before work. Identify missing sources. Use only available tools and say whether an edit was saved or drafted.” Record the supplied source revision and confirmation that the bootstrap was applied; start a fresh project chat and test a rule whose answer is predetermined.
- **Claude-only:** use the `CLAUDE.md` procedure below. Cowork/conversational Claude also needs a confirmed app bootstrap; do not promise auto-loading from the filename alone.

The 30-line draft target is a brevity heuristic for a small personal policy, not grounds to delete required repository safety or workflow rules. Report which policy was actually loaded after the fresh-session check.

## Purpose
Create a well-structured `CLAUDE.md` for this project by interviewing the user and generating a file that changes Claude's behaviour in every session. Follows the conventions in Guide 01.

The key principle: **every line should change behaviour.** If removing a line wouldn't change how Claude acts, it doesn't belong.

This task is designed to be portable. Do not assume any files already exist — check first.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Check current state

Inspect the policy selected above. The shell block and missing-file messages below apply to the **Claude-only branch**; on Codex check `AGENTS.md` and effective overrides, and on ChatGPT inspect the instructions/source inventory.

```bash
ls CLAUDE.md 2>/dev/null && echo "exists" || echo "missing"
```

- If `CLAUDE.md` exists: read it, then tell the user "A CLAUDE.md already exists. I'll review it and suggest improvements rather than starting from scratch." Skip to Step 3.
- If missing: proceed to Step 2.

### Step 2 — Interview the user

Ask the following questions. Collect all answers before writing anything.

**Identity:**
> 1. What's your name and where are you based? (city + country)
> 2. What timezone are you in?
> 3. What language do you prefer for Claude's responses? (even if you write in another language)
> 4. What tools do you use most — email, calendar, GitHub, Slack? Which accounts?

**Communication style:**
> 5. How do you want Claude to format responses — prose, bullet points, or it depends?
> 6. Any strong preferences on length — concise, detailed, or context-dependent?
> 7. Emojis: yes, no, or only when you use them first?
> 8. Should Claude ask clarifying questions, or make a reasonable assumption and proceed?

**Critical rules:**
> 9. What actions should Claude NEVER take without your explicit confirmation? (e.g. sending emails, committing code, making purchases)
> 10. Is there anything Claude should always do? (e.g. "always draft Finnish messages in both formal and casual versions")

**Project-specific (if this is a project CLAUDE.md, not a personal one):**
> 11. What is this project? One sentence.
> 12. Are there any cross-reference rules — linked registers, trackers, or documents that should always be kept in sync?

After collecting answers, say: "Thanks — let me draft your CLAUDE.md."

### Step 3 — Draft the CLAUDE.md

Write the file using the structure below. Keep it **under 30 lines of real content**. Every line must change behaviour.

```markdown
# About [Name]
- [Role or description], based in [city], [country]
- Timezone: [timezone, e.g. Europe/Helsinki (EET UTC+2)]
- [Language preference, e.g. "Always respond in English"]
- [Key tools, e.g. "Uses Gmail (email@example.com) and Google Calendar"]

# Communication Style
- [Verbosity and format preference]
- [Emoji preference]
- [Clarifying questions preference]

# Critical Rules
- NEVER [action] without explicit confirmation
- Always [positive counterpart — what to do instead]
```

Add a `## [Project Name]` section only if this is a project CLAUDE.md with project-specific rules.

Do not add sections for capabilities, tool lists, or things Claude will discover from its environment.

**Real-world example** — a completed CLAUDE.md for a freelance UX designer:

```markdown
# About Emma
- Freelance UX designer, based in Toronto, Canada
- Timezone: America/Toronto (EST UTC-5)
- Always respond in English
- Uses Gmail (emma.designs@gmail.com) and Google Calendar

# Communication Style
- Default to bullet points, not prose
- Keep responses concise — expand only if I ask
- No emojis unless I use them first
- Make a reasonable assumption and proceed — don't ask unless genuinely ambiguous

# Critical Rules
- NEVER send emails — always create a draft I can review
- Always include a subject line suggestion when drafting emails
- When I share a client brief, produce deliverable structure first, then ask before filling in content
```

### Step 4 — Review with the user

Show the draft and ask:
> "Does this look right? Any rules missing, or lines you'd remove? Remember: the goal is short and every line changes behaviour."

Make requested changes.

### Step 5 — Write the file

Write the approved content to the selected native target. Only the Claude-only branch writes its full policy to `CLAUDE.md`; dual-platform writes shared rules to `AGENTS.md` and the thin Claude adapter.

If a `CLAUDE.md` already existed (from Step 1): show a diff of what changed and explain each change briefly.

### Step 6 — Confirm

Tell the user:
- Where the file was written
- How many lines of real content it has
- "Record the fresh-session result for the selected surface. Until it passes, the policy is written but loading remains unverified."
