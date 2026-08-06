# Task: Review Tasks Against Guides

> **Cluide maintenance task** — run this whenever guides in this project are updated.
> `Claude, run tasks/review-tasks.md`

## Purpose
Detect which guides have changed since each task was last reviewed, then check whether the affected tasks need updating to stay in sync. Also runs structural drift checks: the bundled guide copies in `skills/ai-assistant-setup/references/` against the root guides, the canonical IMPROVEMENTS template against its one marked inline copy, and guide-set coverage (every guide scored or explicitly not scored, every task in the mapping table, the advertised guide range correct). Keeps the tasks/ collection accurate as the Cluide guides evolve.

> **Complementary task:** this keeps the framework in sync when a *guide* changes. Its inverse,
> `tasks/harvest-from-projects.md`, goes the other way — it harvests proven patterns from your *live
> projects* back into the guides, tasks, templates, and skills. Run them together as a quarterly
> health check.

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
| `setup-self-improving-task.md` | `07_TASK_LEARNING_GUIDE.md` (incl. Part 9) |
| `setup-wiki.md` | `15_LLM_WIKI.md` |
| `setup-bootstrap-folder.md` | `11_GIT_INTEGRATION.md` |
| `audit-claude-md.md` | `01_CLAUDE_MD.md`, `16_BEST_PRACTICES.md` |
| `audit-task-efficiency.md` | `06_TASK_EFFICIENCY_GUIDE.md` |
| `audit-memory.md` | `04_MEMORY_AND_PROFILE.md` |
| `setup-skill.md` | `03_SKILLS.md` |
| `audit-skill.md` | `03_SKILLS.md`, `02_PROMPTING_BASICS.md` |
| `setup-scheduled-task.md` | `06_TASK_EFFICIENCY_GUIDE.md`, `07_TASK_LEARNING_GUIDE.md` (incl. Part 9) |
| `setup-orchestration.md` | `09_MULTI_TASK_ORCHESTRATION.md` |
| `audit-cost.md` | `10_COST_PERFORMANCE.md` |
| `onboard-project.md` | `01_CLAUDE_MD.md`, `04_MEMORY_AND_PROFILE.md`, `05_MCP_SERVERS.md`, `11_GIT_INTEGRATION.md`, `12_SECURITY.md` |
| `setup-data-layer.md` | `14_PERSONAL_DATA_LAYER.md` |
| `setup-policies.md` | `21_COMPANY_POLICIES.md`, `03_SKILLS.md`, `05_MCP_SERVERS.md` |
| `reorganize-project.md` | `24_PROJECT_FOLDER_STRUCTURE.md` |
| `relocate-project.md` | `11_GIT_INTEGRATION.md`, `24_PROJECT_FOLDER_STRUCTURE.md` |
| `audit-file-hygiene.md` | `11_GIT_INTEGRATION.md`, `24_PROJECT_FOLDER_STRUCTURE.md` |
| `tune-instruction-layers.md` | `25_PROJECT_INSTRUCTION_LAYERS.md`, `01_CLAUDE_MD.md` |
| `analyze-project.md` (+ `analyze-project-reference.md`) | All guides (`01`–`27`) — its dimension criteria summarise the full set; review after any guide change |

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

### Step 4 — Structural drift checks (run every time, regardless of git history)

#### 4a. Bundled guide copies in `skills/*/references/`

Several skills bundle copies of the root guides (`ai-assistant-setup`, `cowork-optimizer`, `policies-validator`, …). They drift silently when a root guide is edited. For every `skills/*/references/*.md` file that has a matching root guide:

1. Assert byte-identity against the root counterpart:
   ```bash
   for f in skills/*/references/*.md; do
     base=$(basename "$f"); root="./$base"
     [ -f "$root" ] && { diff -q "$root" "$f" >/dev/null || echo "DRIFTED: $f"; }
   done
   ```
   (Reference files with no matching root guide — `audit-dimensions.md`, `output-formats.md` — are skill-specific; the `[ -f ]` test skips them.)
2. **One deliberate exception:** `skills/ai-assistant-setup/references/00_INDEX.md` is a *variant*, not a copy — links to `templates/`, `tasks/` and `skills/` are stripped because those assets do not ship inside the skill package. It must therefore differ. The stripping covers `templates/`, `tasks/` and `skills/` links **and** the root-level `README.md` and `CHEATSHEET.md`, none of which ship inside the skill package. Confirm the diff is confined to that link-stripping and nothing else; a content change that reached the root index but not this copy is real drift wearing the exception as cover.
3. Flag every other drifted copy: "`[file]` is out of sync with the root guide — re-copy it." Re-copying is the fix; never patch a bundled copy by hand, or the next diff passes while the two say different things.

This is why `.claudeignore` excludes the numbered copies: they are build artifacts of the skill, and the shell commands here read them regardless.

Also flag reference files with no root counterpart (stale, predates a renumbering) and root guides missing from `references/` that the skill claims to bundle.

#### 4b. IMPROVEMENTS template canonicality

The IMPROVEMENTS template must exist in **exactly one canonical place** — `templates/TASK_TEMPLATE/IMPROVEMENTS.md` — plus one clearly marked inline copy in `tasks/setup-self-improving-task.md` (Step 3, for portability).

1. Search for other embedded IMPROVEMENTS templates:
   ```bash
   grep -rl "Self-Improvement Log\|Improvements Log" tasks/ templates/ skills/ *.md --include="*.md"
   ```
2. Verify the inline copy in `setup-self-improving-task.md` still matches the canonical template section-for-section (Counters including `last_refactor_date` / `next_refactor_due_at_run`, Noise Filters columns, Applied/Archived Fixes, Pending Proposals, Known Issues, Ideas Backlog, the closing "instructions live in TASK.md" note).
3. Flag: any third copy elsewhere, or any mismatch between the canonical template and the marked inline copy.

#### 4c. Guide-set coverage

The checks above compare copies against copies. This one checks that the *set* is complete — it is what
catches a new guide landing without ever being wired into the audit engine or the mapping table.

Run all three assertions:

1. **Every guide is either scored or explicitly not scored.** For each root `NN_*.md`, confirm its number
   is cited by a dimension heading in `analyze-project-reference.md`, or that the guide appears in the
   "not scored" list at the end of the dimension section with a reason. A guide in neither place is the
   failure this check exists for.
   ```bash
   for g in [0-9][0-9]_*.md; do n=${g:0:2}
     grep -qE "guides? [0-9, ]*\b$n\b" tasks/analyze-project-reference.md \
       || grep -q "$g" <(sed -n '/^### Guides not scored/,/^---/p' tasks/analyze-project-reference.md) \
       || echo "UNSCORED: $g"
   done
   ```
2. **Every task appears in the mapping table above.** A task absent from it is never reviewed against its
   guide, however often this task runs.
   ```bash
   for t in tasks/*.md; do b=$(basename "$t")
     case "$b" in README.md|review-tasks.md|harvest-from-projects.md|analyze-project-reference.md) continue;; esac
     grep -q "$b" tasks/review-tasks.md || echo "NOT IN MAPPING TABLE: $b"
   done
   ```
3. **The advertised range matches reality.** The highest `NN_` guide on disk must equal the range stated in
   the `analyze-project.md` mapping row above, in `analyze-project.md` itself, and in `00_INDEX.md`. Three
   places say it; all three must agree.

Flag each failure with the specific file and the missing wiring. These are one-line fixes individually, and
the check is cheap enough to run every time.

### Step 5 — Present findings

```
Task Review Results
───────────────────
Reviewed: N tasks (based on N changed guides)

Issues found:

[task file]:
  ⚠ [issue type]: [description]
  ⚠ [issue type]: [description]

[task file]: ✓ No issues — still in sync with [guide]

Structural drift:
  ⚠ [references/ file or template]: [description, or "✓ no drift detected"]

Total: N issues across N tasks
```

Ask:
> "Would you like me to apply fixes? I can update each task to match the current guide content. I'll show you the changes before writing."

### Step 6 — Apply fixes

For each flagged issue, show the specific change (old → new) and ask for approval before writing.

After applying: note the fix with a comment at the bottom of the task file:
```markdown
<!-- last reviewed: YYYY-MM-DD against [guide file] -->
```

This comment is invisible in rendered markdown but lets the next review see when the task was last checked.

### Step 7 — Confirm

Tell the user:
- Which tasks were reviewed
- Which had issues and what was fixed
- Which were clean
- Whether the bundled reference copies, the IMPROVEMENTS template, and the guide-set coverage checks passed
- "Run this task again after the next guide update, or quarterly as a health check."

<!-- last reviewed: 2026-08-04 — added step 4c guide-set coverage -->
