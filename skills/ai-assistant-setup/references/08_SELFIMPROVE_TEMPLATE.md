# The Self-Improvement Template

> **Companion guides:** [Guide 07](./07_TASK_LEARNING_GUIDE.md) describes the full learning framework this template implements — read it first to understand why the template is structured the way it is. [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) covers token efficiency — keep always-loaded files compact.

> **Giving this to Claude:**
> "Read 08_SELFIMPROVE_TEMPLATE.md and set up the self-improvement system for my task at [path/to/task-folder/]. Follow the installation steps in the guide."

---

## What This Template Is

Every task that learns over time needs an `IMPROVEMENTS.md` file — a structured log that tracks run history, applied fixes, pending proposals, known issues, and the self-improvement instructions the task follows at runtime.

The template lives at [`templates/TASK_TEMPLATE/IMPROVEMENTS.md`](../templates/TASK_TEMPLATE/IMPROVEMENTS.md). It is ready to copy into any task folder and use from run 1.

---

## What the Template Contains

The template has two parts:

**1. The state sections** — updated every run by the task:
- **Counters** — total runs, runs since last refactor, refactor threshold
- **Noise Filters** — domain-specific patterns to collapse rather than process individually
- **Applied Fixes** — auto-applied changes, newest first (archives when > 10 entries)
- **Archived Fixes** — rotated out of Applied Fixes
- **Pending Proposals** — larger changes awaiting human input, in structured JSON
- **Known Issues** — active bugs or limitations being tracked
- **Improvement Ideas Backlog** — low-priority observations not yet ready to propose

**2. The Self-Improvement Step reference** — instructions the task reads at runtime:
- **A. Feedback Signal Detection** — what signals to look for each run (user corrections, ignored suggestions, operational failures)
- **B. Refactor Trigger Check** — when to run a full structural cleanup
- **C. Auto-apply vs. Propose** — the decision rule for when to act vs. when to ask
- **D. Update IMPROVEMENTS.md** — what to write at the end of every run

---

## Installation

### Step 1: Copy the template

```bash
cp templates/TASK_TEMPLATE/IMPROVEMENTS.md tasks/[task-name]/IMPROVEMENTS.md
```

Or ask Claude:
> "Copy `templates/TASK_TEMPLATE/IMPROVEMENTS.md` into my task folder at [path/], rename it `IMPROVEMENTS.md`, and fill in the task name."

### Step 2: Fill in the task name

Replace `[TASK NAME]` in the title with the actual task name.

### Step 3: Wire it into TASK.md

Add two references in your `TASK.md`:

**In the "Read State" step (near the top of the run procedure):**
```markdown
Read `IMPROVEMENTS.md`. Note `runs_since_last_refactor` — increment it this run.
Act on any proposals marked [APPROVED], [REJECTED], or [MODIFY: ...]. Note fixable known issues.
```

**As the final step before the run log:**
```markdown
Run the Self-Improvement step: follow sections A–D in `IMPROVEMENTS.md`
(Feedback Signal Detection → Refactor Trigger Check → Auto-apply vs. Propose → Update IMPROVEMENTS.md).
```

### Step 4: Adjust the refactor threshold

In the Counters block, set `refactor_threshold` based on how often the task runs:
- Daily runs → 25–30
- Weekly runs → 10–15

### Step 5: Delete the placeholder rows

Remove the `*(example)*` row from Noise Filters and the `PROP-001` placeholder from Pending Proposals before the first run.

---

## Responding to Proposals

When the task generates a proposal, it appears in the Pending Proposals section. Respond by annotating directly in `IMPROVEMENTS.md` or in the task's output file:

- `[APPROVED]` — apply the change as described
- `[REJECTED]` — do not apply; archive the proposal
- `[MODIFY: ...]` — apply with the modification you specify

The task picks up the annotation on the next run and acts on it.

---

## How the Template Connects to Guide 07

Guide 07 describes the full learning framework — what signals to detect, the hypothesis lifecycle, the refactoring system. The template operationalises it: the Self-Improvement Step instructions in section A–D are a condensed, ready-to-run version of the Guide 07 framework.

For most tasks, the template is sufficient. Read Guide 07 when you want to understand the reasoning behind the rules, or when you need to adapt the system for a more complex task.
