# Task: Review Tasks Against Guides

> **Cluide maintenance task** — run this whenever guides in this project are updated.
> `Claude, run tasks/review-tasks.md`

## Purpose
Detect which guides have changed since each task was last reviewed, then check whether the affected tasks need updating to stay in sync. Keeps the tasks/ collection accurate as the Cluide guides evolve.

---

## Task → Guide mapping

| Task file | Source guides |
|-----------|--------------|
| `setup-claude-md.md` | `01_CLAUDE_MD.md` |
| `setup-memory.md` | `04_MEMORY_AND_PROFILE.md`, `14_PERSONAL_DATA_LAYER.md` |
| `setup-mcp.md` | `05_MCP_SERVERS.md` |
| `setup-security.md` | `12_SECURITY.md` |
| `setup-github.md` | `11_GIT_INTEGRATION.md` |
| `setup-ignore-hygiene.md` | `11_GIT_INTEGRATION.md`, `12_SECURITY.md` |
| `setup-self-improving-task.md` | `07_TASK_LEARNING_GUIDE.md`, `08_SELFIMPROVE_TEMPLATE.md` |
| `setup-wiki.md` | `15_LLM_WIKI.md` |
| `setup-bootstrap-folder.md` | `11_GIT_INTEGRATION.md` |
| `audit-claude-md.md` | `01_CLAUDE_MD.md`, `16_BEST_PRACTICES.md` |
| `audit-task-efficiency.md` | `06_TASK_EFFICIENCY_GUIDE.md` |
| `audit-memory.md` | `04_MEMORY_AND_PROFILE.md` |
| `setup-skill.md` | `03_SKILLS.md` |
| `audit-skill.md` | `03_SKILLS.md`, `02_PROMPTING_BASICS.md` |
| `setup-scheduled-task.md` | `06_TASK_EFFICIENCY_GUIDE.md`, `07_TASK_LEARNING_GUIDE.md`, `08_SELFIMPROVE_TEMPLATE.md` |
| `onboard-project.md` | `01_CLAUDE_MD.md`, `04_MEMORY_AND_PROFILE.md`, `05_MCP_SERVERS.md`, `11_GIT_INTEGRATION.md`, `12_SECURITY.md` |
| `setup-data-layer.md` | `14_PERSONAL_DATA_LAYER.md` |
| `setup-policies.md` | `21_COMPANY_POLICIES.md`, `03_SKILLS.md`, `05_MCP_SERVERS.md` |

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Find recently changed guides

```bash
# Show guide files changed in the last 90 days with dates
git log --since="90 days ago" --name-only --pretty=format:"%ad %s" --date=short -- '*.md' | grep -E "^[0-9]|^[0-9][0-9]_" | sort -u
```

Also ask the user: "Are there any specific guides you just updated that I should focus on?"

Report:
```
Guides changed in the last 90 days:
  [guide file] — last changed [date], commit: [message]
  ...

No recent changes: [guides with no recent commits]
```

### Step 2 — Identify affected tasks

Cross-reference the changed guides with the mapping table above.

Report:
```
Tasks that may need review:
  [task file] — depends on [guide] (changed [date])

Tasks unaffected:
  [task file] — source guides unchanged
```

If no guides changed recently, say: "No guide changes detected in the last 90 days. Run this task after updating a guide, or extend the window with a longer git log range."

### Step 3 — Review each affected task

For each affected task, read both the source guide(s) and the task file side by side.

Check for:
- **Contradictions** — task says X, guide now says Y
- **Missing content** — guide added a new pattern, option, or warning not reflected in the task
- **Outdated steps** — task references something the guide has deprecated or restructured
- **Outdated examples** — code snippets, config formats, or file paths that have changed
- **Missing new options** — e.g. guide added a new hook type or config field the task doesn't offer

For each issue, note:
```
[task file] — [issue type]
  Guide says: "[quote from guide]"
  Task says:  "[quote from task, or 'missing']"
  Suggested fix: [brief description]
```

### Step 4 — Present findings

```
Task Review Results
───────────────────
Reviewed: N tasks (based on N changed guides)

Issues found:

[task file]:
  ⚠ [issue type]: [description]
  ⚠ [issue type]: [description]

[task file]: ✓ No issues — still in sync with [guide]

Total: N issues across N tasks
```

Ask:
> "Would you like me to apply fixes? I can update each task to match the current guide content. I'll show you the changes before writing."

### Step 5 — Apply fixes

For each flagged issue, show the specific change (old → new) and ask for approval before writing.

After applying: note the fix with a comment at the bottom of the task file:
```markdown
<!-- last reviewed: YYYY-MM-DD against [guide file] -->
```

This comment is invisible in rendered markdown but lets the next review see when the task was last checked.

### Step 6 — Confirm

Tell the user:
- Which tasks were reviewed
- Which had issues and what was fixed
- Which were clean
- "Run this task again after the next guide update, or quarterly as a health check."
