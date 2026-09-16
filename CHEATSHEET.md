# Claude and ChatGPT — Quick Reference

> One-page reference for the most common patterns. Keep this open while building.
> For the full explanation behind any section, see the linked guide.

---

## What Should I Build?

| You want to... | Build | Guide |
|---|---|---|
| An assistant follows standing rules | Shared policy + native entry point | [01](./01_PROJECT_INSTRUCTIONS.md) |
| Run the same task repeatedly when you ask | Skill | [03](./03_SKILLS.md) |
| Run something automatically on a schedule | Scheduled Task | [18 Stage 4](./18_END_TO_END_WALKTHROUGH.md) + `tasks/setup-scheduled-task.md` |
| An assistant retains context between sessions | Memory | [04](./04_MEMORY_AND_PROFILE.md) |
| A task that learns and improves over time | Task + IMPROVEMENTS.md | [07](./07_TASK_LEARNING_GUIDE.md) |
| Answer a one-off question | Chat | — |
| Coordinate tasks that share data | Orchestrator | [09](./09_MULTI_TASK_ORCHESTRATION.md) |
| Track and control task costs | Run metrics | [10](./10_COST_PERFORMANCE.md) |
| Build everything from scratch, step by step | Full walkthrough | [18](./18_END_TO_END_WALKTHROUGH.md) |
| Make task or skill output look good | Guide 19 | [19](./19_OUTPUT_FORMATTING.md) |
| Control what a session is allowed to see | Context scoping | [26](./26_CONTEXT_SCOPING.md) |
| Get a second opinion you can actually rely on | Review protocol | [27](./27_INDEPENDENT_JUDGMENT.md) + `review-protocol` skill |
| Route delegated work to the right model tier | Dispatch policy | [09](./09_MULTI_TASK_ORCHESTRATION.md) + `dispatch` skill |
| Keep a repo healthy and get changes onto GitHub | Git management | [11](./11_GIT_INTEGRATION.md) + `git-guru` skill |

---

## Shared Policy Skeleton

**File location:** root `AGENTS.md` for the shared pattern; `CLAUDE.md` imports it for Claude Code. App-source projects need a bootstrap. Keep the starter short; length targets are design guidance, not universal product limits. See Guides 01 and 35.

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
- [Rule 1 that overrides default behaviour]
- [Rule 2]
- [Rule 3 — max 5 total]
```

✅ Every line should change the assistant's behaviour
❌ Keep long workflow steps and reference material outside standing instructions; retain the project purpose and a short file map.

---

## SKILL.md Skeleton

**Native locations:** Claude Code `.claude/skills/`; Codex `.agents/skills/`. Keep source workflows portable; install only through the selected surface’s route (Guide 03). ~500 lines is an authoring guideline, not a permission or loading guarantee.

````markdown
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
3. [Third step — identify the required operation and bind the actual tool exposed by this host]
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
````

---

## IMPROVEMENTS.md Skeleton

**File location:** Inside your task folder · **Guide:** [07 Part 9](./07_TASK_LEARNING_GUIDE.md)

> Use the canonical [IMPROVEMENTS.md template](./templates/TASK_TEMPLATE/IMPROVEMENTS.md). It owns the counters, noise filters, proposals, and applied-fix history; do not maintain another inline copy.

**Responding to a PROP:** Tell your assistant "Apply PROP-001", "Reject PROP-001 — [reason]", or "Modify PROP-001: instead of X, do Y."

---

## File Naming Conventions

| File | Purpose |
|---|---|
| `TASK.md` | Main task instructions — edit in a repository-capable session or text editor |
| `TASK_REFERENCE.md` | Static reference data (too large for TASK.md, rarely changes) |
| `LAST_RUN.md` | Output/log from the most recent task run (some templates use `LAST_RUN.txt` — pick one name per project) |
| `RUN_LOG.md` | Running history of all runs |
| `IMPROVEMENTS.md` | Self-improvement proposals and confirmed knowledge |
| `PROFILE_SUMMARY.md` | Compact profile (≤50 lines) — read every run |
| `PROFILE_[topic].md` | Detailed profile section — read only when updating |
| `MEMORY.md` | Auto-memory index — read when explicitly requested by the shared policy; verify access on each surface |

---

## Token Cost Quick Reference

These are rough planning examples, not measured usage for your model. Use actual runtime usage where available; otherwise label the estimate. See Guide 10 for API pricing versus subscription limits.

| File size | Approx. tokens | Notes |
|---|---|---|
| 20 lines | ~300 t | short-policy example |
| 50 lines | ~600 t | PROFILE_SUMMARY.md limit |
| 150 lines | ~2,000 t | Good max for any always-loaded file |
| 500 lines | ~6,000 t | Split this into reference + active sections |
| 1,500 lines | ~18,000 t | Only load on demand |

**Rule:** Explicitly decide what each session or run reads. A file link does not guarantee loading; verify native discovery or request the read. Large repeated inputs increase work even when token metrics are unavailable.

---

## Examples of Tool Operations

| Operation | Illustrative names, not portable identifiers |
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

**Important:** Use the exact tool name in your SKILL.md workflow steps. If you write "check the calendar" without naming the tool, the assistant may select the wrong integration; resolve actual names from the connected runtime.

---

## Run Metrics Block (append to RUN_LOG.md)

**Guide:** [10](./10_COST_PERFORMANCE.md)

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

**Guide:** [09](./09_MULTI_TASK_ORCHESTRATION.md)

```
shared/
├── SCHEMA.md                         ← documents data contracts
├── email_digest_2026-04-10.json      ← written by email task
└── calendar_2026-04-10.json          ← written by calendar task
```

**Rules:** each task owns its own files · always check freshness before reading · choose one scheduler owner per job and use a verified duplicate-run guard; staggering alone is not mutual exclusion · keep shared files under 100 lines.

---

## Useful Prompts for Either Assistant

**Set up project instructions:**
> "Read 01_PROJECT_INSTRUCTIONS.md and help me write shared project instructions and the native entry points I need. Ask me what you need to know."

**Create a new skill:**
> "Read 03_SKILLS.md and create a skill for [what you want]. Follow the guide's best practices."

**Audit a task for efficiency:**
> "Read 06_TASK_EFFICIENCY_GUIDE.md and audit [task name] TASK.md for token efficiency."

**Add self-improvement to a task:**
> "Read 07_TASK_LEARNING_GUIDE.md (including Part 9), then add the improvements system to my [task name] task."

**Review and apply improvement proposals:**
> "Read my IMPROVEMENTS.md. For each pending proposal, explain it and ask me to approve, reject, or modify."

**Get an independent read on something you already have a view about:**
> "Read 27_INDEPENDENT_JUDGMENT.md. Review [file] and write the findings to a file before I say anything — location, what is wrong, severity, confidence, and what evidence would make you drop each one. Say what it does well too. I'll give you my own read afterwards."

**Use Plan Mode before making changes:**
> "Read [file] and plan how to [change]. Don’t make any edits yet. Use a native plan mode if this surface provides one."

**Debug something broken:**
> "Read LAST_RUN.md and TASK.md for [task name]. The last run had [problem]. What caused it and what should I change?"

**Format task output as a styled HTML report:**
> "Read 19_OUTPUT_FORMATTING.md and generate a self-contained HTML report for the output of my [task name]. Use the skeleton from the guide as the base layout."

---

## Quick Checklist: Before Going Live with a New Skill or Task

- [ ] Description mentions natural trigger phrases users actually say
- [ ] Output format shows an exact example (not just a description)
- [ ] At least 3 edge cases are handled explicitly
- [ ] Every MCP tool used is named exactly in the workflow steps
- [ ] If it writes files, the format and size limit are defined
- [ ] First run won't take any irreversible action without confirmation

## Switching Platforms

Read [Guide 35](./35_DUAL_PLATFORM_PROJECTS.md). Share the policy and task definitions; keep native memory, connector grants and scheduler registrations separate. Record the branch/revision, pending work, checks and output location at handoff. Refresh uploaded sources explicitly. Mark untested surfaces honestly.
