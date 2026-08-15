# Task: Audit File Hygiene

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-file-hygiene.md`
> **Source guides:** 11 (Git Integration — ignore rules), 24 (Project Folder Structure — archive conventions).

## Purpose

Find and clear the clutter a project accumulates: OS junk, editor and lock files, zero-byte strays, duplicate families, superseded outputs, and large trees that are gitignored but still loading as context. Archiving is the default; deletion is the exception.

Where `setup-ignore-hygiene.md` writes the *rules* (`.gitignore`, `.claudeignore`), this sweeps what is actually on disk. The two are complementary and a project usually needs both: rules stop the next mess, this clears the current one.

Run it when a project has grown messy, before archiving or handing over a project, or when sessions feel slower than the project's real content justifies.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 0 — Preconditions

- The target is mounted. If not, stop and ask for it.
- Read the target's own `CLAUDE.md` and `README` first. **A file that looks like junk may be intentional** — a deliberate empty placeholder, a `.bak` the project keeps on purpose, a sample fixture with a misleading name. Local rules win; when in doubt, flag rather than clear.

### Step 1 — Scan by category (read-only)

Record each hit's relative path, size, and category:

```bash
find . -name '.DS_Store' -o -name 'Thumbs.db' -o -name 'desktop.ini'      # OS junk
find . -name '~$*' -o -name '*.tmp' -o -name '*.swp' -o -name '*.bak'     # editor / lock / temp
find . -type f -empty                                                      # zero-byte
find . \( -name '* copy*' -o -name '*([0-9])*' -o -name '*_v[0-9]*' \)    # duplicate families
find . -name '*.lock' -o -name 'index.lock' -o -name 'HEAD.lock'           # stale git locks
```

Then two categories the patterns above miss:

- **Superseded outputs** — generated reports, exports, and run artifacts plausibly past their useful life.
- **Large ignored-but-loaded trees** — see Check 4, the one worth running even on a project that looks tidy.

**Never open, copy, or echo the contents of anything that looks like a secret.** Flag by location only.

### Step 2 — Run the checklist

#### Check 1: Resolve duplicate families

For each family (`foo copy.docx`, `foo (1).pdf`, `final_v3_FINAL.xlsx`), identify which file is canonical — the newest, or the one referenced elsewhere — and which are redundant.

Where cheap, confirm byte-identity (`md5`/`shasum`) rather than trusting the name. **A name pattern is not evidence of identical content**, and two files that merely share a stem are not a duplicate family.

#### Check 2: Judge superseded outputs conservatively

Default old outputs to **archive**, never delete. Treat something as stale only if it is clearly superseded *and* nothing references it — grep for the filename before proposing anything.

#### Check 3: Zero-byte and lock files

- Zero-byte files: distinguish intentional placeholders (`.gitkeep`, a stub with a documented purpose) from strays.
- Stale git locks with no process holding them: these block commits and are safe to clear — but they signal something else went wrong (a crashed process, a sync daemon fighting git — see `relocate-project.md`). Report the cause alongside the file.

#### Check 4: Ignored but still loaded

The check that catches what the others miss. A large tree can be correctly gitignored and still load into every session, because `.gitignore` and `.claudeignore` are different lists serving different purposes.

```bash
# Anything sizeable that git ignores — then ask whether .claudeignore covers it too
git status --ignored --porcelain | grep '^!!' | cut -c4- | xargs -I{} du -sh {} 2>/dev/null | sort -rh | head -20
```

Flag any large gitignored path — backup folders, `_to_delete/`, vendored trees, duplicate exports — that `.claudeignore` does **not** cover. Flag duplicated content specifically: a second copy of files that already exist elsewhere in the project is pure context cost with no upside.

Recommend `setup-ignore-hygiene.md` for the rule change; this task proposes the sweep.

#### Check 5: Ignore-rule asymmetry

Look for a rule covering one artifact but not its near-identical sibling — `REVIEW_*.md` ignored while `PROJECT_REVIEW.md` is tracked, one export folder ignored and the next one not. These are almost always oversights rather than decisions, but confirm before proposing: sometimes one really is meant to ship.

#### Check 6: Never touch

Exclude from every proposal, without exception: `.git/` internals, `.env`, credentials, tokens, keys, anything secret-looking, memory and profile files, raw source data marked do-not-modify, and anything whose purpose is unclear. When unsure, leave it and flag it.

### Step 3 — Present findings and the change plan

A table, grouped by category: path, size, category, proposed action (`archive` / `delete` / `add to .claudeignore` / `leave — flagged`), and a one-line reason.

Default every row to **archive** (move to `_archive/` inside the target). Reserve `delete` for truly worthless, regenerable files — `.DS_Store`, stale locks — and even then it needs explicit per-file approval, never a blanket yes.

State the totals: how many files, how much disk, how much context the ignored-but-loaded findings would free.

Then state what you checked and found legitimate — the folders that look like clutter and are not, the
duplicates that turned out to differ, the large files that earn their size. A project with a clean tree
should read as clean rather than as an empty table.

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

Then **stop and wait.**

### Step 4 — Take a restore point, then apply

This step moves files in bulk and may delete some, so take a way back first: a git commit or tag when the project is under version control, otherwise a dated zip of just the affected folders stored outside the working tree. Confirm it exists before the first move. Retire it once Step 5 verifies the result.

Apply only approved rows. Create `_archive/` if needed. For `.claudeignore` additions, show the diff before writing.

If a file turns out to be referenced somewhere after all, stop and re-present rather than moving it anyway.

### Step 5 — Verify

Confirm nothing referenced was moved (grep the project for the names of archived files), the project's own tasks and skills still resolve, and any `.claudeignore` change is syntactically valid. Report what moved, what was deleted, and what was left flagged.

## Output

A categorised findings table (Step 3), an approved change plan, and a post-apply confirmation listing what moved, what was deleted, and what was deliberately left alone.

## Constraints

- Read-only until Step 3 is approved.
- **Restore point before the first move.** No bulk archive or delete without a way back (Step 4).
- **Archive by default; deletion needs explicit per-file approval.** Never a blanket delete, and never a cross-project sweep applied without a per-project plan.
- Never edit file *contents* — this task moves and removes only. Content problems belong to the relevant `audit-*` task.
- Never open or echo anything that looks like a secret; report location only.
- Respect the target's own `CLAUDE.md`; an intentional-looking oddity is a flag, not a fix.
- Confirm byte-identity before calling two files duplicates.
