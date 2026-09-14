# Development and Execution: Working Across Claude and OpenAI

> Separate changing the assistant from using it. Claude Code and Codex can maintain repository definitions; Cowork, ChatGPT and coding-agent sessions can execute workflows when they have the required sources and tools. Assign roles by capability, not by brand.

> **See also:** [Guide 20 — Interactive Prompting](./20_INTERACTIVE_PROMPTING.md) for Claude Code session features: `@` file references, plan mode, AskUserQuestion input types, and context hygiene.

---

## The Two Roles

| Role | Suitable surface | What happens here |
|---|---|---|
| Development | Claude Code, Codex, or a file-capable assistant with a reviewable editor | Edit policy, tasks and skills; inspect failures; validate fixtures; review and commit changes |
| Execution | Cowork, ChatGPT, Claude Code or Codex with the required access | Read stable definitions, process authorized inputs and save outputs/state |
| Uploaded-source execution | ChatGPT or conversational Claude project | Work from a recorded source revision; return deliverables or write through an authorized connector |

Separate development and execution sessions when testing a changed workflow. Do not edit the definition under a live run. A fresh execution session proves that the saved instructions work without the author's conversation context. An uploaded-source session additionally needs refreshed sources before that test.

---

## Architecture: Files That Work in Both Tools

Use one authored definition set and explicit state ownership. Native configuration stays outside that contract.

```text
project/
├── AGENTS.md                    # Shared policy
├── CLAUDE.md                    # Claude adapter
├── PLATFORM_SETUP.md            # Capabilities, source revisions, scheduler owner
├── skills/                      # Authored workflow sources; install per surface
├── tasks/email-digest/
│   ├── TASK.md                  # Stable definition during a run
│   ├── IMPROVEMENTS.md          # Proposed/applied changes with evidence
│   ├── LAST_RUN.md              # State owned by one execution path
│   └── RUN_LOG.md
└── .auto-memory/                # Explicit project memory, private when personal
```

### The shared folder approach

Two local tools can read the same project, but only one writes a given state file at a time. New sessions must load updated policy. Sharing a folder does not share native memory, installed skills, app grants or schedule registrations.

### The git approach

Develop on a branch or worktree, review the diff, validate fixtures and merge the complete change. Execution then uses a known revision. Do not pull into a checkout while a live run is writing it. Record the branch, commit, changed files, validation and outstanding work in a handoff.

### What to avoid

Do not run both platforms' schedules against the same job. Keep one scheduler owner and migrate it under [Guide 35](./35_DUAL_PLATFORM_PROJECTS.md#7-state-schedules-and-handoffs). Do not treat a ChatGPT upload as a shared folder: refresh the source revision and explicitly deliver accepted changes back to the authored project. Never copy native settings or credentials from `.claude/` into a guessed OpenAI path.

---

## Development Workflow: Adding or Changing Something

When you want to add a new skill, update a task, or make a CLAUDE.md change:

**1. Open the development surface.**
Use Claude Code, Codex or another authorized file-capable editor in the intended repository. Check the branch and instruction files before editing.

**2. Edit the relevant file.**
For a new skill: create the SKILL.md in the skills folder. For a task change: edit TASK.md or TASK_REFERENCE.md. For a shared behaviour change: edit `AGENTS.md`; keep product-specific behaviour in its native adapter.

Use the guides as reference material directly in Claude Code:
> "Read 03_SKILLS.md and create a new skill for [what you want]. Follow all the best practices in the guide."

**3. Review before using it in Cowork.**
Start a new Claude Code session for this rather than continuing in the one that wrote the file — the writing session already believes the file is right, and it will defend rather than assess ([Guide 27](./27_INDEPENDENT_JUDGMENT.md)). Ask neutrally:
> "Read this SKILL.md. What does it do well that must survive editing, what does it do badly, and where would it fail in real use? Cover the description's trigger reliability, edge cases and output format. If a part is fine, say so."

For tasks, ask for a dry-run analysis:
> "Read TASK.md and LAST_RUN.md. Walk me through what this task would do if it ran right now — without actually running it."

**4. Commit to git** (if you are using git).
See [Guide 11 — Git Integration](./11_GIT_INTEGRATION.md) for commit conventions.

**5. Test on the intended execution surface.**
Use a fresh session and fixtures first, then an authorized live run. Record results separately for Claude and OpenAI; passing in Codex does not prove that a ChatGPT project can reach the same inputs. If something fails, return to the development session with the evidence.

---

## If You Only Use Cowork (No Claude Code)

Claude Code is the recommended tool for development work — but it is optional. If you work entirely within Cowork, the same workflows are available, just with a different toolset.

### Editing Files

Your task and skill files are plain markdown text files. You can edit them in any text editor:
- **Windows:** Notepad, Notepad++, or VS Code
- **Mac:** TextEdit (in plain text mode), VS Code, or BBEdit

Or — ask Claude in a fresh Cowork conversation to make the edit for you:

> "Read my TASK.md at `[path to file]` and add a rule that when the output contains more than 5 action items, flag the top 3 as priorities. Show me the change before writing it."

Claude will propose the edit and ask you to confirm before writing. This gives you the review step even without Claude Code's diff view.

### Testing

After editing, open a **new Cowork conversation** (not the one you used for editing) and run the skill or task. Mixing editing and testing in the same session creates confusion because Claude is holding both the "editing Claude" and "execution Claude" context at once.

### Debugging

When something breaks, open a new Cowork conversation and share the relevant files:

> "Here is my LAST_RUN.md: [paste contents]. Here is my TASK.md: [paste contents]. The problem is [describe it]. What caused it and what should I change in TASK.md to fix it?"

You can diagnose and fix entirely through Cowork this way. For the most effective debugging, follow the same order as the Claude Code workflow: read evidence → identify cause → fix → test.

### Reviewing IMPROVEMENTS.md

Open a new Cowork conversation and share the proposals:

> "Here is my IMPROVEMENTS.md: [paste contents]. For each pending proposal, explain what it does and ask me whether to apply it, reject it, or modify it."

Work through them one at a time. Claude will make the change in the TASK.md once you confirm.

### What You Miss Without Claude Code

Cowork has plan mode and subagents of its own, so the main thing you give up by staying out of Claude Code is **git integration** — rollback, history, pre-run snapshots ([Guide 11](./11_GIT_INTEGRATION.md)). You can work effectively without it, but it is worth setting up even if you are not a developer: it is the single best protection against "I broke something and don't know what".

---

## Debugging: When Something Breaks in Cowork

The example below uses Claude Code to diagnose a Cowork run. The same evidence-first loop works in Codex; use the actual execution surface for the final check.

### Step 1: Read the evidence in Claude Code

Open Claude Code and read the relevant state files:

```
Read tasks/[task-name]/LAST_RUN.md
Read tasks/[task-name]/IMPROVEMENTS.md
```

Ask:
> "Read LAST_RUN.md and TASK.md for the email-digest task. The last run produced [describe the problem]. What in TASK.md could have caused this?"

Claude Code can compare TASK.md against LAST_RUN.md and reason about what went wrong — something Cowork is not well-positioned to do mid-session.

### Step 2: Check what changed recently

If the problem appeared after a recent change, git is your fastest diagnostic:

```bash
git log --oneline -- tasks/[task-name]/
git diff HEAD~1 HEAD -- tasks/[task-name]/TASK.md
```

This shows exactly what was different in the run that broke versus the run before it.

If you are not using git, compare the current TASK.md against the last time you remember it working. Even a mental diff of "what did I change?" is useful.

### Step 3: Fix in Claude Code

Once you know the cause, edit the file in Claude Code. Do not edit task files directly in Cowork during a debugging session — you want a clean, deliberate fix, not a mid-conversation edit that may be inconsistent.

Common fixes:
- **Wrong output format:** add or tighten the output format section in TASK.md
- **Missed edge case:** add a handling rule to the appropriate section
- **Stale data in profile file:** use Claude Code to read and update the specific profile entry
- **IMPROVEMENTS.md proposal causing unexpected behaviour:** review the proposal in Claude Code, determine whether to revert or adjust

### Step 4: Test the fix in Claude Code before re-running in Cowork

After fixing, do a quick review:
> "Read the updated TASK.md. Walk me through what will happen differently on the next run compared to the run that broke."

If the reasoning sounds right, commit and let Cowork run it.

**If the fix changes figures or output the task has produced before**, do not compare the next run
against your memory of the last one. Keep the last known-good output and compare against it — and
treat the comparison as three-way rather than as a diff: things that match, differences you
predicted and can state in advance, and differences you cannot explain. Only the third kind stops
the rollout, and it stops it every time: an unexplained difference is either a defect in the fix or
a behaviour of the old version that nobody had written down, and both need resolving before the
number is trusted. [Guide 29](./29_SPEC_BEFORE_REBUILD.md) covers the full form of this, including
what to do when the old version can no longer be run at all.

### Step 5: Add a guard if the bug was silent

If the bug ran for multiple sessions before you noticed — producing subtly wrong output that you only caught later — add a validation step to the task so it cannot happen again silently:

> "Add a self-check step to TASK.md: before writing outputs, verify that [the condition that was violated]. If the check fails, write a WARNING line at the top of LAST_RUN.md and stop the run."

---

## Reviewing and Applying IMPROVEMENTS.md Proposals

The self-improvement system (Guide 07) generates proposals in IMPROVEMENTS.md that wait for your input. Use a development session with the accepted files and evidence; Claude Code and Codex are both suitable. The numbered example below uses Claude Code.

**The pattern:**

1. Open Claude Code periodically (weekly, or after a few runs)
2. Read IMPROVEMENTS.md
3. For each pending proposal: review the rationale and the proposed change
4. Tell Claude Code what to do:
   > "Read IMPROVEMENTS.md. For PROP-001, apply the change. For PROP-002, reject it — the current behaviour is intentional. For PROP-003, modify it: instead of [X], do [Y]."
5. Claude Code makes the edits, you review the diff, commit
6. Cowork picks up the changes on the next run

This separates review from execution and leaves a diff and validation record.

The proposals were written by Claude, so asking Claude whether to apply them is not an independent check — the reviewer and the author share their priors about what a good change looks like. Ask what would go wrong if you applied it, and what would have to be true for the proposal to be a mistake, rather than for a recommendation ([Guide 27](./27_INDEPENDENT_JUDGMENT.md)).

---

## Plan Mode: Review Before Executing

For any change that is structural, multi-file, or hard to undo — ask Claude to plan before editing. This separates the "figure out what to do" step from the "do it" step.

**How it works:**
1. Ask Claude to plan only — no edits yet (use Shift+Tab to toggle plan mode, or state it in your prompt)
2. Claude reads relevant files and describes the proposed changes
3. You review and approve, reject, or amend the plan
4. Claude executes only what was approved

**When to use Plan Mode:**
- Adding a new feature to a task or skill (multi-step, multiple files)
- Restructuring a TASK.md or SKILL.md
- Making changes whose impact is non-obvious
- Any time you want to review before Claude acts, not after

**When to skip it:**
- Single-line fixes, typo corrections, adding one entry to a table
- Changes you'd be happy to just undo if they're wrong

**Prompt to activate:**
> "Plan how to [change] in [file]. Don't make any edits yet — I'll review first."

---

## Subagents: Parallel Work in Claude Code

Claude Code can spawn **subagents** — parallel Claude instances that work on focused subtasks and report back. Subagents are dispatched via the Agent tool (named the Task tool in older Claude Code versions) and can read, search, and reason about files independently.

**When to use subagents:**
- You need to explore multiple files or areas in parallel
- A task has multiple independent subtasks that can run concurrently
- You want research or analysis done without blocking the main session

**Example:**
> "Launch two subagents in parallel: one to read all TASK.md files and summarise their run procedures, another to read all SKILL.md files and summarise their triggers."

**Important:** Subagents are best used for read-heavy exploration and analysis. For file edits, use the main session to keep changes coordinated and reviewable.

**Subagents are not isolated by default.** A subagent inherits CLAUDE.md, project instructions, and read access to the whole folder. If you are using one for a deliberately uninformed review rather than for parallelism, it needs an explicit deny-list — see [Guide 26](./26_CONTEXT_SCOPING.md). A deny-list only governs what the subagent may read; if you briefed it after stating your own view, your framing is already inside the brief ([Guide 27](./27_INDEPENDENT_JUDGMENT.md)).

---

## New Features: Development Checklist

When building something new — a skill, task or profile update — use this checklist in the development surface before taking it live on the selected execution surface:

- [ ] **Description triggers correctly** — read the skill/task description aloud. Would it trigger from a casual, implicit phrasing, or only from an exact command?
- [ ] **Output format is explicit** — is there a code block showing exactly what the output should look like? Ambiguous format = inconsistent output.
- [ ] **Edge cases are handled** — are there at least 3 "what if" clauses for the most common deviations?
- [ ] **Tools are named** — does every step that calls an MCP tool name the tool explicitly?
- [ ] **State management is defined** — if the skill or task writes to a file, is the write format and size limit defined?
- [ ] **First-run is safe** — on the very first run in Cowork, will this skill/task do anything irreversible? If yes, add a confirmation gate for run 1.

---

## The Maintenance Rhythm

A sustainable rhythm for this two-tool workflow:

**In Cowork (daily / as needed):**
- Run tasks, use skills
- Provide corrections when output is wrong — these corrections become learning signals for the self-improvement system

**In Claude Code (weekly or after problems):**
- Review LAST_RUN.md for the previous week's runs
- Review IMPROVEMENTS.md for pending proposals and apply/reject them
- Make any needed edits to TASK.md, SKILL.md, CLAUDE.md, or hooks in settings.json
- Commit changes
- Run the guide-improvement task if guides need updating

**In Claude Code (as needed, on demand):**
- Debug a broken run
- Build a new skill or task
- Audit a skill for the [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) efficiency checklist

---

## Giving This to an Assistant

**To debug a problem using Claude Code:**
> "The email-digest task produced wrong output on the last run. Read LAST_RUN.md and TASK.md and tell me what caused it and what to fix."

**To review improvement proposals:**
> "Read guide-improvement/IMPROVEMENTS.md and my tasks/[task-name]/IMPROVEMENTS.md. For each pending proposal, summarise what it does and ask me to approve, reject, or modify."

**To build a new skill ready for Cowork:**
> "Read 03_SKILLS.md and 05_MCP_SERVERS.md. Create a new skill for [what you want]. Before finishing, run through the new features checklist in 13_DEV_EXECUTION_WORKFLOW.md and confirm each item."
