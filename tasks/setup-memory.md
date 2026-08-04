# Task: Setup Memory

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-memory.md`
> **Source guides:** `04_MEMORY_AND_PROFILE.md`, `14_PERSONAL_DATA_LAYER.md`

## Purpose
Set up a persistent memory system so Claude remembers key facts, preferences, and projects across sessions. Creates the `.auto-memory/` folder structure and populates it with an initial set of memory files based on a user interview.

This is the recommended memory system for deliberate, cross-session memory. It survives context resets and works in scheduled tasks — unlike native Claude memory.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Check current state

```bash
ls .auto-memory/MEMORY.md 2>/dev/null && echo "exists" || echo "missing"
ls CLAUDE.md 2>/dev/null && echo "claude-md-exists" || echo "no-claude-md"
```

- If `.auto-memory/MEMORY.md` exists: read it and the existing memory files. Tell the user "A memory system already exists with N entries. I'll review and fill any gaps." Skip the interview questions already answered; ask only what's missing.
- If missing: proceed to Step 2.

### Step 2 — Interview the user

Explain first:
> "I'm going to ask you a few questions to populate your memory system. These facts will be loaded at the start of every Claude session so you don't have to re-explain them. Keep answers brief — 1–3 sentences each is ideal."

Ask the following. Skip any the user doesn't want to answer.

**Identity (user memory):**
> 1. What's your name and where are you based?
> 2. What's your timezone?
> 3. What language do you prefer for Claude's responses?
> 4. What are your main tools (email, calendar, project management, etc.)?
> 5. What's your role / what kind of work do you do?

**Preferences (feedback memory):**
> 6. Any strong preferences for how Claude should respond — format, length, tone?
> 7. Any corrections you've had to make repeatedly that Claude keeps forgetting?

**Active projects (project memory):**
> 8. What are your 1–3 most active projects right now? For each: what is it, what's the current status, and is there anything Claude should flag or track?

**Reference pointers (reference memory):**
> 9. Is there anything important stored somewhere specific — a file, a folder, a system — that Claude should know to look at? (e.g. "contracts are in ~/Documents/Clients/")

After collecting answers: "Thanks — I'll create your memory files now."

### Step 3 — Create the memory files

1. Create the `.auto-memory/` directory if it doesn't exist.

2. For each piece of information, create a separate markdown file using this format:

```markdown
[Memory content — 2–5 sentences. Direct facts, no padding.]
[updated: YYYY-MM]
```

File naming:
- User identity → `user-identity.md`
- Communication preferences → `feedback-communication.md`
- Each active project → `project-[slug].md`
- Reference pointers → `reference-[slug].md`
- Any correction → `feedback-[slug].md`

3. Create `.auto-memory/MEMORY.md` as the index:

```markdown
# Memory Index

- [user-identity](./user-identity.md) — Who the user is, timezone, language preference
- [feedback-communication](./feedback-communication.md) — Response format and style preferences
...
```

Keep each index line under ~100 characters. Max 30 entries total.

### Step 4 — Wire memory into CLAUDE.md

Check if `CLAUDE.md` exists.

- If yes: check if it already contains a line like `Read .auto-memory/MEMORY.md`. If not, add it to a `## Memory` section or append to the top-level list.
- If no: tell the user "You don't have a CLAUDE.md yet. Run `tasks/setup-claude-md.md` to create one — it will include the memory loading instruction."

The line to add to `CLAUDE.md`:
```markdown
## Memory
- Read `.auto-memory/MEMORY.md` at the start of every session.
```

### Step 5 — Confirm

Tell the user:
- How many memory files were created
- What's in the index
- "Going forward, Claude will load these facts at the start of every session. To add a memory: ask Claude to save it. To update: ask Claude to update the relevant file. To remove: ask Claude to delete the file and its index entry."
- "Keep the index under 30 entries. If it grows beyond that, consolidate or remove stale entries."
