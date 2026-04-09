# Development and Execution: Using Claude Code and Cowork Together

> Two Claude tools, two distinct roles. Claude Code is where you build and maintain your assistant — editing task files, debugging problems, managing git. Cowork (or any conversational Claude interface) is where you run it — executing tasks, processing emails, doing the actual work. Keeping these roles separate is one of the most useful things you can do for the long-term health of your setup.

---

## The Two Roles

| Role | Tool | What you do here |
|------|------|-----------------|
| **Development** | Claude Code | Edit TASK.md, SKILL.md, CLAUDE.md. Debug failing runs. Add new features. Review and apply IMPROVEMENTS.md proposals. Manage git. Run the guide-improvement task. |
| **Execution** | Cowork (conversational Claude) | Run your daily tasks. Process emails. Draft messages. Use skills. Let tasks run and read the output. |

The key principle: **do not mix the roles in a single session.** When you open Cowork to check your emails, you are not also editing your email skill. When you open Claude Code to fix a bug, you are not also running your actual tasks.

Keeping the roles separate prevents a class of errors where mid-session edits interact with a running task, or where you accidentally trigger a live task while debugging it.

---

## Architecture: Files That Work in Both Tools

The setup that works well for both tools has two structural rules: **definition files and state files for a task live in the same place**, and **Claude's config folder is separate from your project folders**.

`~/.claude/` is Claude's config folder — like `.vscode/` or `.git/`. Two locations inside it are for your content; everything else is internal:

```
~/.claude/
├── CLAUDE.md                    # Your instructions — read every session
├── settings.json                # Internal — do not edit
├── skills/
│   └── gmail-task-manager/
│       └── SKILL.md             # Definition — edited in Claude Code, used in Cowork
├── projects/                    # Internal — do not edit
└── sessions/                    # Internal — do not edit
```

Tasks, profiles, and knowledge live in a project folder of your choosing — not inside `~/.claude/`:

```
MyAssistant/                     # Any folder you choose
├── email-digest/
│   ├── TASK.md                  # Definition — edited in Claude Code
│   ├── IMPROVEMENTS.md          # State — written by Cowork, read and edited in Claude Code
│   ├── LAST_RUN.md              # State — written by Cowork, read in Claude Code
│   └── RUN_LOG.md               # State — written by Cowork
├── Profile/                     # Optional — cross-session context
└── Knowledge/                   # Optional — domain knowledge

.auto-memory/
├── MEMORY.md                    # State — read by Cowork, updated by Cowork
└── *.md                         # State — individual memory files
```

**Definition files** (TASK.md, SKILL.md, CLAUDE.md) are edited in Claude Code and read by Cowork. They should be stable between runs — Cowork reads them but does not modify them.

**State files** (IMPROVEMENTS.md, LAST_RUN.md, RUN_LOG.md, profile files, memory files) are written by Cowork and read by both tools. Claude Code reads them to understand what happened; Cowork updates them every run.

### The shared folder approach

If both tools point to the same directory on disk (or the same cloud-synced folder), edits you make in Claude Code are immediately available to Cowork on the next session — no explicit deployment step needed. This is the simplest setup.

### The git approach

If you use git, the typical flow is:
1. Edit in Claude Code on a feature branch
2. Commit and merge to main
3. Cowork runs from main (either via a pull step in the task, or via a shared folder that is already on main)

The git approach adds a deployment step but gives you the rollback and history benefits described in [Guide 09](./09_GIT_INTEGRATION.md).

### What to avoid

**Hardcoded paths.** If TASK.md says `Read /Users/username/tasks/email-digest/LAST_RUN.md`, it will break if the folder moves or if another user tries to use your setup. Use relative paths from the task folder wherever possible.

**Settings.json in shared files.** Each tool has its own `settings.json` (Claude Code's is at `~/.claude/settings.json`; Cowork has its own). Do not try to share this file — it contains tool-specific configuration. Keep them separate.

---

## Development Workflow: Adding or Changing Something

When you want to add a new skill, update a task, or make a CLAUDE.md change:

**1. Open Claude Code.**
All editing happens here. Claude Code has the file editing tools, git, and the ability to read and reason about your entire setup at once.

**2. Edit the relevant file.**
For a new skill: create the SKILL.md in the skills folder. For a task change: edit TASK.md or TASK_REFERENCE.md. For a behaviour change: edit CLAUDE.md.

Use the guides as reference material directly in Claude Code:
> "Read 02_SKILLS.md and create a new skill for [what you want]. Follow all the best practices in the guide."

**3. Review before using it in Cowork.**
In Claude Code, read the file you just created or edited. Ask Claude to check it:
> "Read this SKILL.md and tell me: will the description trigger reliably? Are there missing edge cases? Is the output format specific enough?"

For tasks, ask for a dry-run analysis:
> "Read TASK.md and LAST_RUN.md. Walk me through what this task would do if it ran right now — without actually running it."

**4. Commit to git** (if you are using git).
See [Guide 09 — Git Integration](./09_GIT_INTEGRATION.md) for commit conventions.

**5. Switch to Cowork for the first live run.**
The first real run of a new or changed skill is always in Cowork. Watch the output carefully. If it looks right, you are done. If something is off, go back to Claude Code to diagnose and fix.

---

## Debugging: When Something Breaks in Cowork

The diagnostic loop always starts in Claude Code, not in Cowork. Cowork is for running; Claude Code is for understanding and fixing.

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

### Step 5: Add a guard if the bug was silent

If the bug ran for multiple sessions before you noticed — producing subtly wrong output that you only caught later — add a validation step to the task so it cannot happen again silently:

> "Add a self-check step to TASK.md: before writing outputs, verify that [the condition that was violated]. If the check fails, write a WARNING line at the top of LAST_RUN.md and stop the run."

---

## Reviewing and Applying IMPROVEMENTS.md Proposals

The self-improvement system (Guide 05) generates proposals in IMPROVEMENTS.md that wait for your input. This review loop is naturally a Claude Code task, not a Cowork task.

**The pattern:**

1. Open Claude Code periodically (weekly, or after a few runs)
2. Read IMPROVEMENTS.md
3. For each pending proposal: review the rationale and the proposed change
4. Tell Claude Code what to do:
   > "Read IMPROVEMENTS.md. For PROP-001, apply the change. For PROP-002, reject it — the current behaviour is intentional. For PROP-003, modify it: instead of [X], do [Y]."
5. Claude Code makes the edits, you review the diff, commit
6. Cowork picks up the changes on the next run

This keeps the review thoughtful (Claude Code has the full file context and your explicit direction) and keeps Cowork focused on execution.

---

## New Features: Development Checklist

When building something new — a skill, a task, a profile update — use this checklist in Claude Code before taking it live in Cowork:

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
- Make any needed edits to TASK.md, SKILL.md, or CLAUDE.md
- Commit changes
- Run the guide-improvement task if guides need updating

**In Claude Code (as needed, on demand):**
- Debug a broken run
- Build a new skill or task
- Audit a skill for the [Guide 04](./04_TASK_EFFICIENCY_GUIDE.md) efficiency checklist

---

## Giving This to Claude

**To debug a problem using Claude Code:**
> "The email-digest task produced wrong output on the last run. Read LAST_RUN.md and TASK.md and tell me what caused it and what to fix."

**To review improvement proposals:**
> "Read guide-improvement/IMPROVEMENTS.md and my tasks/[task-name]/IMPROVEMENTS.md. For each pending proposal, summarise what it does and ask me to approve, reject, or modify."

**To build a new skill ready for Cowork:**
> "Read 02_SKILLS.md and 08_MCP_SERVERS.md. Create a new skill for [what you want]. Before finishing, run through the new features checklist in 10_DEV_EXECUTION_WORKFLOW.md and confirm each item."
