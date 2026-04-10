# Claude Assistant — Quick Reference Cheat Sheet

*Last reviewed: April 2026*

> One-page reference for the most common patterns. Keep this open while building.
> For the full explanation behind any section, see the linked guide.

---

## What Should I Build?

| You want to... | Build | Guide |
|---|---|---|
| Claude always responds a certain way | CLAUDE.md | [01](./01_CLAUDE_MD.md) |
| Run the same task repeatedly when you ask | Skill | [02](./02_SKILLS.md) |
| Run something automatically on a schedule | Scheduled Task | [04](./04_TASK_EFFICIENCY_GUIDE.md) |
| Claude remembers things between sessions | Memory | [03](./03_MEMORY_AND_PROFILE.md) |
| A task that learns and improves over time | Task + IMPROVEMENTS.md | [05](./05_TASK_LEARNING_GUIDE.md) |
| Answer a one-off question | Chat | — |
| Coordinate tasks that share data | Orchestrator | [16](./16_MULTI_TASK_ORCHESTRATION.md) |
| Track and control task costs | Run metrics | [17](./17_COST_PERFORMANCE.md) |

---

## CLAUDE.md Skeleton

**File location:** `.claude/CLAUDE.md` · **Max length:** ~30 lines

```markdown
## Who I Am
- I am [name], [role] at [organisation]
- Based in [city], timezone [e.g. Europe/Helsinki]
- [1–2 lines of relevant context: industry, main tools, languages]

## How I Work
- [Communication preference: e.g. concise / detailed / bullet points]
- [Drafting preference: e.g. produce directly / ask first]
- [Decision preference: e.g. give me options / recommend one]

## Standing Rules
- [Rule 1 that overrides Claude's default behaviour]
- [Rule 2]
- [Rule 3 — max 5 total]
```

✅ Every line should change Claude's behaviour
❌ Don't include: capability lists, project info, workflow steps, file paths

---

## SKILL.md Skeleton

**File location:** `.claude/skills/[skill-name]/SKILL.md` · **Max length:** ~500 lines

```markdown
---
name: your-skill-name
description: >
  Use this skill when the user [describes the situation clearly].
  Triggers on phrases like "[phrase 1]", "[phrase 2]", "[phrase 3]".
  Also applies when the user [alternative trigger scenario].
---

## Purpose
[1–2 sentences: what this skill does and why it exists]

## Workflow
1. [First step — be specific about what to read/check]
2. [Second step]
3. [Third step — name the MCP tool if one is used, e.g. use gmail_list_emails]
4. [Final step — produce the output]

## Output Format
[Paste an exact example of what the output should look like]
```example
## Subject: [subject]

**Summary:** [2-3 sentences]

**Actions needed:**
- [ ] [action 1]
- [ ] [action 2]
```

## Edge Cases
- If [condition], then [what to do differently]
- If [condition], then [what to do differently]
- If no [data/input] is available, [fallback behaviour]

## Examples
> User: "[typical trigger phrase]"
> Skill produces: [brief description of expected output]
```

---

## IMPROVEMENTS.md Skeleton

**File location:** Inside your task folder · **Guide:** [06](./06_SELFIMPROVE_TEMPLATE.md)

```markdown
# Improvements Log — [Task Name]

## Pending Proposals

| ID | What | Why | Status |
|----|------|-----|--------|
| PROP-001 | [proposed change] | [observed reason] | PENDING |

## Applied Changes

| ID | What | Applied | Result |
|----|------|---------|--------|
| — | — | — | — |

## Confirmed Knowledge

- [Fact confirmed after 3+ runs]
- [User preference confirmed]

## Hypotheses

| ID | Belief | Confidence | Evidence |
|----|--------|-----------|---------|
| H-001 | [what the task believes] | LOW/MEDIUM/HIGH | [what led to this] |
```

**Responding to a PROP:** Tell Claude "Apply PROP-001", "Reject PROP-001 — [reason]", or "Modify PROP-001: instead of X, do Y."

---

## File Naming Conventions

| File | Purpose |
|---|---|
| `TASK.md` | Main task instructions — edit in Claude Code or text editor |
| `TASK_REFERENCE.md` | Static reference data (too large for TASK.md, rarely changes) |
| `LAST_RUN.md` | Output/log from the most recent task run |
| `RUN_LOG.md` | Running history of all runs |
| `IMPROVEMENTS.md` | Self-improvement proposals and confirmed knowledge |
| `PROFILE_SUMMARY.md` | Compact profile (≤50 lines) — read every run |
| `PROFILE_[topic].md` | Detailed profile section — read only when updating |
| `MEMORY.md` | Auto-memory index — loaded every session if referenced in CLAUDE.md |

---

## Token Cost Quick Reference

| File size | Approx. tokens | Notes |
|---|---|---|
| 20 lines | ~300 t | CLAUDE.md target |
| 50 lines | ~600 t | PROFILE_SUMMARY.md limit |
| 150 lines | ~2,000 t | Good max for any always-loaded file |
| 500 lines | ~6,000 t | Split this into reference + active sections |
| 1,500 lines | ~18,000 t | Only load on demand |

**Rule:** Files in CLAUDE.md load every session. Files in TASK.md load every run. Large always-loaded files slow down every interaction and raise cost.

---

## Common MCP Tool Names

| Tool | Typical name in skills |
|---|---|
| Read Gmail inbox | `gmail_list_emails` |
| Send Gmail | `gmail_send_email` |
| Read Outlook mail | `outlook_email_search` |
| Read Outlook calendar | `outlook_calendar_search` |
| Read Teams messages | `chat_message_search` |
| Search SharePoint | `sharepoint_search` |
| Read/write local files | `read_file`, `write_file`, `list_directory` |
| Browse a web page | `navigate`, `get_page_text` |
| Search the web | `web_search` |
| Jira issue | `getJiraIssue`, `createJiraIssue` |
| Confluence page | `getConfluencePage`, `createConfluencePage` |

**Important:** Use the exact tool name in your SKILL.md workflow steps. If you write "check the calendar" without naming the tool, Claude may not know which integration to use.

---

## Run Metrics Block (append to RUN_LOG.md)

**Guide:** [17](./17_COST_PERFORMANCE.md)

```markdown
## [2026-04-10] Run #47

**Duration:** ~3 min
**Tokens (est.):** ~8K input, ~2K output
**API calls:** 12 (gmail_search: 1, gmail_read: 8, gcal_list: 1, write_file: 2)
**Notes:** Normal run. 8 emails processed, 2 action items found.
```

Add as the final step in TASK.md. Archive entries after 30 runs.

---

## Shared State Convention (Multi-Task)

**Guide:** [16](./16_MULTI_TASK_ORCHESTRATION.md)

```
shared/
├── SCHEMA.md                         ← documents data contracts
├── email_digest_2026-04-10.json      ← written by email task
└── calendar_2026-04-10.json          ← written by calendar task
```

**Rules:** each task owns its own files · always check freshness before reading · stagger schedules by 10+ minutes · keep shared files under 100 lines.

---

## Useful Prompts to Give Claude

**Set up or improve your CLAUDE.md:**
> "Read 01_CLAUDE_MD.md and help me write my CLAUDE.md. Ask me what you need to know."

**Create a new skill:**
> "Read 02_SKILLS.md and create a skill for [what you want]. Follow the guide's best practices."

**Audit a task for efficiency:**
> "Read 04_TASK_EFFICIENCY_GUIDE.md and audit [task name] TASK.md for token efficiency."

**Add self-improvement to a task:**
> "Read 05_TASK_LEARNING_GUIDE.md and 06_SELFIMPROVE_TEMPLATE.md, then add the improvements system to my [task name] task."

**Review and apply improvement proposals:**
> "Read my IMPROVEMENTS.md. For each pending proposal, explain it and ask me to approve, reject, or modify."

**Use Plan Mode before making changes:**
> "Enter plan mode. Read [file] and plan how to [change]. Don't make any edits yet."

**Debug something broken:**
> "Read LAST_RUN.md and TASK.md for [task name]. The last run had [problem]. What caused it and what should I change?"

---

## Quick Checklist: Before Going Live with a New Skill or Task

- [ ] Description mentions natural trigger phrases users actually say
- [ ] Output format shows an exact example (not just a description)
- [ ] At least 3 edge cases are handled explicitly
- [ ] Every MCP tool used is named exactly in the workflow steps
- [ ] If it writes files, the format and size limit are defined
- [ ] First run won't take any irreversible action without confirmation
