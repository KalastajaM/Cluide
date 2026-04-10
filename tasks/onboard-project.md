# Task: Onboard Project

> **Cluide task** — run this to set up a new project end-to-end:
> `Claude, run tasks/onboard-project.md`
> **Source guides:** `01_CLAUDE_MD.md`, `03_MEMORY_AND_PROFILE.md`, `08_MCP_SERVERS.md`, `09_GIT_INTEGRATION.md`, `13_SECURITY.md`

## Purpose
Set up a new project for use with Claude end-to-end — in the right order, without having to know which individual setup tasks to run. Covers: CLAUDE.md, ignore hygiene, git/GitHub, security, and optionally memory and MCP. Can start from a project template if one fits.

This task orchestrates the other setup tasks rather than duplicating their logic. It reads the relevant task files and runs them in sequence.

---

## Instructions

### Step 1 — Understand the project

Ask:
> 1. What is this project? (one sentence)
> 2. Is this a new empty folder, an existing codebase, or something else?
> 3. What will Claude mainly help you with in this project? (e.g. writing code, managing documents, running scheduled tasks, research)
> 4. Will this project use any external tools — email, calendar, GitHub, databases?
> 5. Will it contain sensitive data, credentials, or personal information?

Then ask:
> "Would you like to start from one of the available project templates, or set up from scratch?
>
> **Available templates:**
>
> - **PROJECT_TEMPLATE** — a general-purpose project with `CLAUDE.md`, `Profile/`, and `Knowledge/` pre-structured. Good starting point for any persistent assistant context: document management, research, ongoing projects.
>
> - **AI-ASSISTANT_TEMPLATE** — a complete personal business assistant. Monitors email, Teams, and calendar via Microsoft 365; maintains a live work context profile; delivers daily briefings. Includes four coordinated scheduled tasks out of the box. Good for: setting up a daily work assistant.
>
> - **PMO_TEMPLATE** — a project workspace for managing a programme or migration initiative. Includes a full PMO register suite: risk register, action tracker, dependency register, decision tracker, and knowledge base. Good for: structured project management with linked registers.
>
> - **Start from scratch** — run individual setup tasks tailored to this project. More flexible; takes a few extra minutes."

Based on the answers, recommend a template if one clearly fits, or recommend scratch if none does. Don't force a template.

### Step 2 — Option A: Start from a template

If the user chooses a template:

**For PROJECT_TEMPLATE:**
```bash
cp -r /path/to/Claude-Teacher/templates/PROJECT_TEMPLATE ./
```
Tell the user: "Copy the template folder to your project root, then rename it and fill in the placeholders marked `[placeholder]` in each file. I'll help you do that now."

Read `templates/PROJECT_TEMPLATE/README.md` and walk the user through filling in:
- `CLAUDE.md` — replace placeholders with real identity, style, and rules
- `Profile/PROFILE_SUMMARY.md` — replace with actual project summary
- `Knowledge/` — add any domain knowledge files relevant to the project

Then skip to Step 4 (ignore hygiene) — CLAUDE.md is already handled.

**For AI-ASSISTANT_TEMPLATE:**
Read `templates/AI-ASSISTANT_TEMPLATE/SETUP.md` and walk the user through the setup steps it describes. This template has its own setup procedure — follow it rather than the generic steps below.

After completing the template setup, ask: "Would you also like me to run the security and GitHub setup steps?"

**For PMO_TEMPLATE:**
```bash
cp -r /path/to/Claude-Teacher/templates/PMO_TEMPLATE ./
```
Read `templates/PMO_TEMPLATE/README.md` and walk the user through filling in the initiative-specific placeholders.

Then continue with Steps 4–7 below (ignore hygiene, git, security).

---

### Step 2 — Option B: Start from scratch

If starting from scratch, run Steps 3–7 in order.

---

### Step 3 — CLAUDE.md

Say: "I'll run the CLAUDE.md setup now."

Follow all steps in `tasks/setup-claude-md.md` — interview, draft, review, write.

### Step 4 — Ignore hygiene

Say: "Now I'll check what should be in `.gitignore` and `.claudeignore`."

Follow all steps in `tasks/setup-ignore-hygiene.md` — scan, propose, apply, handle tracked files.

For the enforcement option in that task, recommend:
- If this is a code project: Option A (PostToolUse hook)
- Otherwise: Option B (CLAUDE.md rule)

### Step 5 — Git and GitHub

Ask:
> "Is this project going to be on GitHub? (Yes / No / Already is)"

- **Yes:** follow all steps in `tasks/setup-github.md` — init, create repo, first commit, ongoing sync.
- **Already is:** skip to checking if ongoing sync is set up. If not, offer to add it (Step 8 of `setup-github.md`).
- **No:** run `git init` and make a first local commit. No remote needed.

### Step 6 — Security

Say: "I'll run a quick security check."

Follow Steps 1–3 of `tasks/setup-security.md` — credential scan, permission audit, file hygiene check.

Ask: "Would you like me to also install the PreToolUse hook that blocks dangerous shell commands? (Recommended for projects where Claude runs bash commands.)"

If yes, follow Step 6 Fix A of `tasks/setup-security.md`.

### Step 7 — Optional: Memory

Ask:
> "Would you like to set up a memory system so Claude remembers facts, preferences, and project context across sessions? (Recommended for projects you'll work on regularly.)"

If yes, follow all steps in `tasks/setup-memory.md`.

### Step 8 — Optional: MCP servers

Ask:
> "Does this project need Claude to connect to external tools — email, calendar, GitHub API, filesystem access outside this folder, or a browser?"

If yes, follow Steps 2–4 of `tasks/setup-mcp.md` for the specific servers needed.

### Step 9 — Confirm

Tell the user what was set up:

```
Project Onboarding Complete
────────────────────────────
✓ CLAUDE.md — [N lines]
✓ .gitignore / .claudeignore — [N patterns added]
✓ Git / GitHub — [local only / pushed to github.com/...]
✓ Security — [clean / N issues found and fixed]
[✓ Memory — N memory files created]
[✓ MCP servers — N servers configured]
[✓ Template — started from [template name]]
```

Suggest what to do next based on what the project is:
- Code project: "Consider running `tasks/setup-skill.md` to create skills for tasks you do repeatedly in this project."
- Scheduled tasks project: "Consider running `tasks/setup-scheduled-task.md` to scaffold your first automated task."
- Research/knowledge project: "Consider running `tasks/setup-wiki.md` to create a knowledge base for this topic."
