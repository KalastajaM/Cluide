# Troubleshooting Guide: When Things Don't Work

*Last reviewed: April 2026*

> Every other guide assumes things go right. This one is for when they don't. Each section is a symptom -- find yours, follow the steps.

> **Companion guides:** [Guide 05 — MCP Servers](./05_MCP_SERVERS.md) for MCP-specific issues. [Guide 06 — Task Efficiency](./06_TASK_EFFICIENCY_GUIDE.md) for slow tasks. [Guide 09 — Multi-Task Orchestration](./09_MULTI_TASK_ORCHESTRATION.md) for task coordination failures. [Guide 10 — Cost and Performance](./10_COST_PERFORMANCE.md) for cost spikes. [Guide 11 — Git Integration](./11_GIT_INTEGRATION.md) for rollback. [Guide 12 — Security](./12_SECURITY.md) for security concerns. [Guide 14 — Personal Data Layer](./14_PERSONAL_DATA_LAYER.md) for data ingestion issues.

> **Quick diagnostic prompt:**
> "Read LAST_RUN.md and TASK.md for [task name]. The problem is [describe it]. What's causing it and what should I change?"

---

## General Debugging Mindset

Before jumping to specific problems, apply this order:

1. **Read the evidence first.** Open `LAST_RUN.md` (if it exists) and read what actually happened. The problem often explains itself here.
2. **Then read the instruction.** Open `TASK.md` or `SKILL.md`. Does the instruction actually say what you think it says? Mismatches between what you intended and what you wrote are the most common cause.
3. **Ask what changed.** Did this work before? What's different now — a file edit, a new MCP server, a different Cowork session?
4. **One thing at a time.** Fix one suspected cause, test, then fix the next. Making three changes at once makes it impossible to know which one worked.

---

## Problem: My Skill Isn't Triggering

**Symptom:** You type a request that should activate your skill, but Claude responds generically without following the skill instructions.

**Most likely causes:**

**1. The description does not match your phrasing**
The `description:` field in SKILL.md frontmatter determines whether Claude activates the skill. If the description says "summarise email threads" but you say "catch me up on my inbox", Claude may not connect them.

*Fix:* Open `SKILL.md` and expand the description. Add the natural phrases you actually use:
```yaml
description: >
  Use this skill when the user wants to catch up on email, summarise their inbox,
  review unread messages, or check what needs a reply.
  Triggers on: "catch me up", "what's in my inbox", "email summary",
  "what do I need to reply to", "summarise my emails".
```

**2. You edited the skill during an active session**
Skill changes only take effect in new sessions. If you edited the file and retried in the same conversation, Claude is still using the old version.

*Fix:* Start a fresh Cowork conversation.

**3. The file is in the wrong location**
The skill must be at `.claude/skills/[skill-name]/SKILL.md`. A common mistake is `.claude/[skill-name]/SKILL.md` (missing the `skills/` subfolder) or a different filename.

*Fix:* Verify the exact path. The folder name must match and the file must be named `SKILL.md`.

**4. The file was saved with a different extension**
On Windows, Notepad may save as `.md.txt`. macOS TextEdit in rich-text mode can add hidden formatting.

*Fix:* Open a terminal and check: `dir .claude\skills\` (Windows) or `ls .claude/skills/` (Mac). Confirm you see `SKILL.md`, not `SKILL.md.txt`.

---

## Problem: Claude Is Ignoring My CLAUDE.md Instructions

**Symptom:** You have rules in `CLAUDE.md` (e.g. "always use bullet points", "respond in English") but Claude does not follow them.

**Most likely causes:**

**1. CLAUDE.md is in the wrong location**
It must be at the root of the project or at `.claude/CLAUDE.md`. Not inside a nested subfolder.

**2. The instruction is too vague**
"Be concise" means different things in different contexts. "Keep responses to 5 bullet points or fewer unless I ask for detail" is specific enough to follow consistently.

*Fix:* Rewrite vague rules as concrete, testable statements. See [Guide 01](./01_CLAUDE_MD.md) for examples.

**3. The instruction conflicts with another instruction**
If CLAUDE.md says "be brief" but your SKILL.md says "include full detail", the more specific instruction (skill) wins. This is correct behavior but can feel like CLAUDE.md is being ignored.

*Fix:* Check if a skill or task instruction is overriding the CLAUDE.md rule you expected to apply.

**4. You're using a skill or tool that loads its own context**
Some skills and scheduled tasks load their own instructions that may not repeat CLAUDE.md's rules. A task that runs autonomously may not have the same standing instructions as a conversational session.

*Fix:* Add critical formatting rules directly to the relevant `TASK.md` or `SKILL.md`, not only to `CLAUDE.md`.

---

## Problem: Memory Isn't Persisting Between Sessions

**Symptom:** Claude forgets something it knew in a previous session -- a preference, a project, a standing fact about you.

**Understand the two memory systems first:**

| System | How it works | Survives context reset? |
|---|---|---|
| **Native Claude memory** | Built-in; Claude writes facts automatically | No -- resets when session context clears |
| **`.auto-memory/` folder** | Explicit markdown files on disk | Yes -- loaded from disk every session |

Native memory is not reliably loaded in autonomous task runs. Scheduled tasks must use the file-based system.

**Most likely causes and fixes:**

**1. You're relying on native memory for tasks**
Native memory is designed for conversational use. Scheduled tasks should use the `.auto-memory/` folder system.

*Fix:* Set up `.auto-memory/` as described in [Guide 04](./04_MEMORY_AND_PROFILE.md) and add this line to your `CLAUDE.md`:
```markdown
- Read `.auto-memory/MEMORY.md` at the start of every session.
```

**2. The MEMORY.md isn't being loaded**
Even with the folder in place, if `CLAUDE.md` doesn't instruct Claude to read it, it won't be loaded automatically.

*Fix:* Check your `CLAUDE.md` contains the line above.

**3. The memory file was written but not in the right format**
Claude reads `MEMORY.md` as an index of pointers. If the file doesn't list the individual memory files, those files won't be read.

*Fix:* Open `.auto-memory/MEMORY.md` and check it lists all your memory files with their paths.

---

## Problem: An MCP Tool Isn't Available or Fails

**Symptom:** Claude says it cannot find a tool, uses the wrong tool, or an MCP-dependent skill fails with an error.

**Most likely causes:**

**1. The MCP server is not running**
Each MCP integration (Gmail, Calendar, Jira, etc.) is a separate server that must be configured and running.

*Fix:* Check that the relevant server is listed and enabled. In Claude Code, check `settings.json` under `mcpServers`. In Cowork, check tool/integration settings.

**2. The tool name in the skill does not match the actual tool name**
If your SKILL.md says `use gmail_get_emails` but the actual tool is `gmail_list_emails`, Claude will fail to use it.

*Fix:* Ask Claude in a fresh session: "What MCP tools do you have available?" Update your skill to use the exact name shown.

**3. The credentials or token have expired**
MCP servers that connect to external services use tokens that expire.

*Fix:* Re-authenticate the MCP server. See [Guide 05](./05_MCP_SERVERS.md#troubleshooting-by-server) for per-server troubleshooting steps.

**4. The server is configured but the wrong permission scope is set**
A Gmail token set to read-only cannot send email. A calendar token set to read-only cannot create events.

*Fix:* Check the scope of the token used by the server. Re-authorize with the correct scope if needed.

---

## Problem: Task Output Has Drifted From What I Expect

**Symptom:** The task used to produce clean, well-formatted output, but over time the format has changed, new sections appeared, or something is consistently wrong.

**Most likely causes:**

**1. A self-improvement proposal changed the format**
If the self-improvement system is active, an applied proposal may have altered the output.

*Fix:* Open `IMPROVEMENTS.md` and look at the "Applied Changes" section. If a recent change altered the format undesirably, tell Claude to revert it:
> "The change applied as PROP-005 produced output I don't like. Revert that change in TASK.md."

**2. The output format in TASK.md is too vague**
If the output format says "produce a clean summary" without showing the exact structure, Claude's interpretation will drift over time.

*Fix:* Replace the description with a concrete code block template:
```markdown
## Output Format
Produce output in exactly this structure:
```
## Summary — [Date]

**Key items:** [number]

1. [Item] — [one-line description]
2. [Item] — [one-line description]

**Action needed:** [Yes/No] — [brief description if yes]
```
```

**3. A new fact in the profile or memory file is being applied incorrectly**
If a task reads a profile file and that file was recently updated, new content may be changing the output.

*Fix:* Open the profile file and check recent updates (look for `[updated:]` timestamps). If an entry looks wrong, correct it directly in the file.

---

## Problem: My Task Is Running Very Slowly

**Symptom:** The task takes much longer than it used to, or stalls mid-run.

**Most likely causes:**

**1. A file it reads has grown too large**
Tasks that accumulate run logs, profile data, or knowledge files without trimming slow down over time.

*Fix:* Run the efficiency audit from [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md):
> "Read 06_TASK_EFFICIENCY_GUIDE.md and run the audit checklist on my [task name] task."

Also check:
- Is `LAST_RUN.md` growing without limit? Add a rule: "Overwrite LAST_RUN.md on each run — do not append."
- Is `RUN_LOG.md` very long? Trim entries older than 30 days.
- Are profile files growing? Archive completed projects and old entries.

**2. The task is reading files it doesn't need**
If TASK.md has instructions like "Read all files in the tasks folder", it is loading everything — not just what it needs for this run.

*Fix:* Rewrite instructions to read only specific named files.

**3. Too many MCP calls in sequence**
Each MCP call takes time. Fetching 50 emails one by one instead of in bulk will be slow.

*Fix:* Consolidate MCP calls. "Fetch the 20 most recent emails in one call, then filter locally" is faster than fetching and checking one at a time.

---

## Problem: I Don't Understand an IMPROVEMENTS.md Proposal

**Symptom:** The task generated a proposal in IMPROVEMENTS.md and you are not sure what it means, whether it is safe, or what it will change.

**What to do:**

Share the proposal with Claude and ask for an explanation:
> "Read my IMPROVEMENTS.md. Explain PROP-003 to me: what would change, why is it being suggested, and what could go wrong if I apply it?"

**Red flags in proposals — don't apply without understanding:**
- Proposals that relax a safety or confirmation rule ("remove the confirmation step before sending")
- Proposals to read new files or use new MCP tools the task didn't use before
- Proposals that change the core purpose of the task
- Proposals with no clear rationale in the "Why" column

**If a proposal looks wrong:**
> "Reject PROP-003 — the current behaviour is intentional. Add a note explaining why so this isn't proposed again."

---

## Problem: Something Broke After I Made a Change

**Symptom:** Everything was working, you made a change to a file, and now something is wrong.

**If you are using git** (recommended):

Find what changed:
```bash
git log --oneline
git diff HEAD~1 HEAD -- tasks/[task-name]/TASK.md
```

Roll back to the previous version:
```bash
git checkout HEAD~1 -- tasks/[task-name]/TASK.md
```

**If you are not using git:**

1. Open the file you changed and try to recall what was there before
2. Ask Claude: "The [file name] I edited now causes [problem]. Here is the current file: [paste it]. What is the most likely cause and how do I fix it?"
3. Make one change at a time, testing between each

**Consider setting up git** -- even for non-developers, it is the single best protection against "I broke something and I don't know what." [Guide 11](./11_GIT_INTEGRATION.md) walks through the setup.

---

## Problem: A Task Run Was Unexpectedly Expensive

**Symptom:** A task that typically costs $0.10-$0.20 per run suddenly costs $0.50+ or more, or your monthly spend has jumped without obvious cause.

**Most likely causes:**

**1. A file the task reads has grown silently**
Profile files, wiki pages, and accumulated run logs grow over time. Each extra kilobyte is more input tokens billed every run.

*Fix:* Check the sizes of all files listed in TASK.md's read instructions. Trim, archive, or summarize anything that has grown beyond what the task actually needs. See [Guide 10](./10_COST_PERFORMANCE.md) for cost estimation tables and budgeting patterns.

**2. The self-improvement system added a new file read**
An applied IMPROVEMENTS.md proposal may have added "also read [file]" to the task, increasing input tokens.

*Fix:* Review recently applied proposals. Revert any that added file reads without clear justification.

**3. You switched from Sonnet to Opus without adjusting scope**
Opus costs roughly 5x more per token than Sonnet. A task designed for Sonnet's pricing may become expensive on Opus.

*Fix:* Either switch back to Sonnet for routine tasks, or reduce the task's input scope to compensate. Use the cost tables in [Guide 10](./10_COST_PERFORMANCE.md) to estimate the difference.

---

## Problem: MCP Server-Specific Failures

**Symptom:** A particular MCP integration (Gmail, Calendar, Jira, etc.) fails consistently while others work fine. Errors may include timeouts, authentication failures, or malformed responses.

**Most likely causes:**

**1. Token or session expiry for that specific service**
Each MCP server authenticates independently. One can expire while others remain valid.

*Fix:* Re-authenticate the failing server only. See the per-server troubleshooting notes in [Guide 05](./05_MCP_SERVERS.md#troubleshooting-by-server) for service-specific steps.

**2. Rate limiting by the upstream API**
Services like Gmail and Microsoft Graph have per-minute and per-day rate limits. A task that fetches too many items in a burst can hit these.

*Fix:* Reduce the number of items fetched per run, add delays between calls, or switch to batch-fetch patterns. See the error handling patterns in [Guide 05](./05_MCP_SERVERS.md#error-handling-patterns).

**3. The server process crashed and did not restart**
MCP servers run as separate processes. A crash may leave the tool unavailable without a visible error until the next call.

*Fix:* Restart the MCP server process. In Claude Code, check `settings.json` under `mcpServers` to confirm the server is still listed, then restart the session.

---

## Problem: Multi-Task Orchestration Breaks Silently

**Symptom:** A downstream task produces wrong, empty, or stale output because an upstream task it depends on failed or ran late.

**Most likely causes:**

**1. Missing freshness check on shared files**
If the downstream task reads a shared file without checking its timestamp, it may consume stale data from a previous day without warning.

*Fix:* Add a freshness check: compare the file's date or `updated_at` field to today. Treat stale data the same as missing data. See [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md#failure-handling) for the three failure modes to handle.

**2. Upstream task ran but wrote partial or malformed output**
The upstream task may have hit an error mid-run and written an incomplete file.

*Fix:* Add schema validation in the downstream task before consuming the input. Check that required fields exist and contain expected types. Log what was wrong and fall back gracefully.

**3. Timing overlap between tasks**
If the upstream task runs at 07:00 and the downstream task also starts at 07:00 (or too soon after), the upstream output may not be ready yet.

*Fix:* Space task schedules with enough buffer. A 10-15 minute gap between dependent tasks is usually sufficient.

---

## Problem: Data Ingestion Script Fails

**Symptom:** A script that imports data into your personal data layer (bank transactions, health data, expense records) fails or produces incomplete output.

**Most likely causes:**

**1. Source format changed**
Banks, apps, and services periodically change their export formats — column names shift, date formats change, new fields appear.

*Fix:* Compare the current export against the schema your ingestion script expects. Update the parsing logic to match the new format. See [Guide 14](./14_PERSONAL_DATA_LAYER.md) for ingestion patterns.

**2. The raw file is too large for a single pass**
A full year of transactions or a large CSV can exceed what Claude processes efficiently in one call.

*Fix:* Split the input into chunks (e.g., one month at a time) or pre-filter to only new records before passing to Claude.

**3. Vision ingestion failed on a screenshot**
Screenshots from mobile apps may be low resolution, cropped, or have overlapping UI elements that confuse extraction.

*Fix:* Retake the screenshot with higher resolution and ensure all relevant data is visible without scrolling. If extraction remains unreliable, switch to a text-based export if the source app offers one.

---

## When to Start Fresh

Sometimes a task or setup has accumulated so many issues that repair takes longer than starting over. Consider starting fresh when:

- Three or more things are wrong at once and the causes are unclear
- The task file has grown beyond 300 lines and the structure is hard to follow
- The IMPROVEMENTS.md shows repeated proposals for conflicting changes
- You've changed so much that LAST_RUN.md no longer reflects actual behaviour

**How to start fresh:**
1. Copy the current broken file to `[TASK.md.backup]` so you can reference it
2. Start from the `TASK_TEMPLATE/` in the templates folder
3. Copy over only the sections you're confident in
4. Let the task run 3–5 times to re-establish a baseline before re-adding complexity

---

## Giving This to Claude

**To diagnose a specific problem:**
> "Read LAST_RUN.md and TASK.md for [task name]. The problem is: [describe it]. What is causing it and what should I change?"

**To audit a task that has slowed down:**
> "Read 06_TASK_EFFICIENCY_GUIDE.md and run the audit checklist on my [task name] task. Tell me what to fix and in what order."

**To investigate a cost spike:**
> "Read 10_COST_PERFORMANCE.md and analyze the token usage of my [task name] task. Which files or steps are consuming the most tokens and how do I reduce them?"

**To debug orchestration failures:**
> "Read 09_MULTI_TASK_ORCHESTRATION.md and check the shared output files for my [task chain]. Are any files missing, stale, or malformed?"

**To review recent changes for the cause of a problem:**
> "Read the current TASK.md and compare it to what you would expect based on LAST_RUN.md. What inconsistencies do you see?"

**To explain an improvement proposal:**
> "Read my IMPROVEMENTS.md and explain each pending proposal in plain language. For each one, tell me what it would change, why it was suggested, and whether you recommend applying it."
