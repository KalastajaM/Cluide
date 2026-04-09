# Troubleshooting Guide: When Things Don't Work

> Every other guide in this collection assumes things go right. This one is for when they don't. Each section is a symptom — find yours, follow the steps.

> **Companion guides:** [Guide 04 — Task Efficiency](./04_TASK_EFFICIENCY_GUIDE.md) for slow tasks. [Guide 13 — Security](./13_SECURITY.md) for security concerns. [Guide 09 — Git Integration](./09_GIT_INTEGRATION.md) for rollback.

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

**1. The description doesn't match your phrasing**
The `description:` field in SKILL.md frontmatter is what Claude uses to decide whether to activate the skill. If your description says "summarise email threads" but you say "catch me up on my inbox", Claude may not connect them.

*Fix:* Open `SKILL.md` and expand the description. Add the natural phrases you actually use:
```yaml
description: >
  Use this skill when the user wants to catch up on email, summarise their inbox,
  review unread messages, or check what needs a reply.
  Triggers on: "catch me up", "what's in my inbox", "email summary",
  "what do I need to reply to", "summarise my emails".
```

**2. You're in an existing session when you made the change**
Skill changes only take effect in new Cowork sessions. If you edited the file and then tried again in the same conversation, Claude is still using the old version.

*Fix:* Start a fresh Cowork conversation.

**3. The file is in the wrong location**
The skill must be at `.claude/skills/[skill-name]/SKILL.md`. A common mistake is putting it at `.claude/[skill-name]/SKILL.md` (missing the `skills/` subfolder) or naming the file differently.

*Fix:* Verify the exact path. The folder name must match and the file must be named `SKILL.md`.

**4. The file was saved with a different extension**
On Windows, Notepad may save as `.md.txt`. macOS TextEdit in rich text mode can add hidden formatting.

*Fix:* Open a terminal and check: `dir .claude\skills\` (Windows) or `ls ~/.claude/skills/` (Mac). Make sure you see `SKILL.md`, not `SKILL.md.txt`.

---

## Problem: Claude Is Ignoring My CLAUDE.md Instructions

**Symptom:** You have rules in `CLAUDE.md` (e.g. "always use bullet points", "respond in English") but Claude isn't following them.

**Most likely causes:**

**1. CLAUDE.md is in the wrong location**
It must be at `.claude/CLAUDE.md` — at the root level of the `.claude` folder. Not inside a project subfolder.

**2. The instruction is too vague**
"Be concise" means different things in different contexts. "Keep responses to 5 bullet points or fewer unless I ask for detail" is specific enough to follow consistently.

*Fix:* Rewrite vague rules as concrete, testable statements. See [Guide 01](./01_CLAUDE_MD.md) for examples.

**3. The instruction conflicts with another instruction**
If CLAUDE.md says "be brief" but your SKILL.md says "include full detail", the more specific instruction (skill) wins. This is correct behaviour — but can feel like CLAUDE.md is being ignored.

*Fix:* Check if a skill or task instruction is overriding the CLAUDE.md rule you expected to apply.

**4. You're using a skill or tool that loads its own context**
Some skills and scheduled tasks load their own instructions that may not repeat CLAUDE.md's rules. A task that runs autonomously may not have the same standing instructions as a conversational session.

*Fix:* Add critical formatting rules directly to the relevant `TASK.md` or `SKILL.md`, not only to `CLAUDE.md`.

---

## Problem: Memory Isn't Persisting Between Sessions

**Symptom:** Claude forgets something it knew in a previous session — a preference you corrected, a project you mentioned, a standing fact about you.

**Understand the two memory systems first:**

| System | How it works | Survives context reset? |
|---|---|---|
| **Native Claude memory** | Built-in; Claude writes facts automatically | No — resets when session context clears |
| **`.auto-memory/` folder** | Explicit markdown files on disk | Yes — loaded from disk every session |

If you are relying on native memory for a scheduled task, this will fail — native memory is not reliably loaded in autonomous task runs.

**Most likely causes and fixes:**

**1. You're relying on native memory for tasks**
Native memory is designed for conversational use. Scheduled tasks should use the `.auto-memory/` folder system.

*Fix:* Set up `.auto-memory/` as described in [Guide 03](./03_MEMORY_AND_PROFILE.md) and add this line to your `CLAUDE.md`:
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

**Symptom:** Claude says it can't find a tool, uses the wrong tool, or an MCP-dependent skill fails with an error.

**Most likely causes:**

**1. The MCP server isn't running**
Each MCP integration (Gmail, Teams, Outlook, etc.) is a server that must be configured and running.

*Fix:* Open your MCP settings and check that the relevant server is listed and enabled. In Cowork, this is in the tool/integration settings. In Claude Code, check `settings.json` under `mcpServers`.

**2. The tool name in the skill doesn't match the actual tool name**
If your SKILL.md says `use gmail_get_emails` but the actual tool is named `gmail_list_emails`, Claude will fail to use it.

*Fix:* Ask Claude in a fresh session: "What MCP tools do you have available?" This lists all active tools with their exact names. Update your skill to use the exact name shown.

**3. The credentials or token have expired**
MCP servers that connect to external services (Gmail, Microsoft 365, Jira) use tokens that expire.

*Fix:* Re-authenticate the MCP server. In most cases this means going back to the setup/install step for that server and re-connecting your account. See [Guide 08](./08_MCP_SERVERS.md) for server-specific notes.

**4. The server is configured but the wrong permission scope is set**
A Gmail token set to read-only cannot send email. A calendar token set to read-only cannot create events.

*Fix:* Check the scope of the token used by the server. Re-authorise with the correct scope if needed.

---

## Problem: Task Output Has Drifted From What I Expect

**Symptom:** The task used to produce clean, well-formatted output, but over time the format has changed, new sections appeared, or something is consistently wrong.

**Most likely causes:**

**1. An IMPROVEMENTS.md proposal was applied that changed the format**
If the self-improvement system is active, it may have applied a change that altered the output.

*Fix:* Open `IMPROVEMENTS.md` and look at the "Applied Changes" section. If a recent change altered the format undesirably, tell Claude to revert it:
> "The change applied as PROP-005 produced output I don't like. Revert that change in TASK.md."

**2. The output format section in TASK.md is too vague**
If your output format says "produce a clean summary" without showing the exact structure, Claude's interpretation will drift over time.

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

**Symptom:** The task takes much longer to complete than it used to, or seems to stall.

**Most likely causes:**

**1. A file it reads has grown too large**
Tasks that accumulate run logs, profile data, or knowledge files without trimming will eventually slow down.

*Fix:* Run the efficiency audit from [Guide 04](./04_TASK_EFFICIENCY_GUIDE.md):
> "Read 04_TASK_EFFICIENCY_GUIDE.md and run the audit checklist on my [task name] task."

Also check:
- Is `LAST_RUN.md` growing without limit? Add a rule: "Overwrite LAST_RUN.md on each run — do not append."
- Is `RUN_LOG.md` very long? Trim entries older than 30 days.
- Are profile files growing? Archive completed projects and old entries.

**2. The task is reading files it doesn't need**
If TASK.md has instructions like "Read all files in the tasks folder", it is loading everything — not just what it needs for this run.

*Fix:* Rewrite instructions to read only specific named files.

**3. Too many MCP calls in sequence**
Each MCP call (read an email, check a calendar event) takes time. If the task reads 50 emails one by one instead of fetching in bulk, it will be slow.

*Fix:* Consolidate MCP calls. For example, "Fetch the 20 most recent emails in one call, then filter locally" is faster than "Fetch email, check, fetch next email, check..."

---

## Problem: I Don't Understand an IMPROVEMENTS.md Proposal

**Symptom:** The task has generated a proposal in IMPROVEMENTS.md but you're not sure what it means, whether it's safe to apply, or what it will change.

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

**Consider setting up git** — even for non-developers, it is the single best protection against "I broke something and I don't know what." [Guide 09](./09_GIT_INTEGRATION.md) walks through the setup.

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
> "Read LAST_RUN.md and TASK.md for [task name]. The problem is: [describe it]. What's causing it and what should I change?"

**To audit a task that has slowed down:**
> "Read 04_TASK_EFFICIENCY_GUIDE.md and run the audit checklist on my [task name] task. Tell me what to fix and in what order."

**To review recent changes for the cause of a problem:**
> "Read the current TASK.md and compare it to what you'd expect based on LAST_RUN.md. What inconsistencies do you see?"

**To explain an improvement proposal:**
> "Read my IMPROVEMENTS.md and explain each pending proposal in plain language. For each one, tell me what it would change, why it was suggested, and whether you recommend applying it."
