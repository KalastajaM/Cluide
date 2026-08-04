# Task: Audit Memory

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-memory.md`
> **Source guide:** `04_MEMORY_AND_PROFILE.md`

## Purpose
Review the project's memory for stale entries, missing index pointers, duplicates, and entries that belong in `CLAUDE.md` instead. Keeps memory lean and current so it stays useful as sessions accumulate.

Guide 04 describes three layers — **native memory**, the `.auto-memory/` folder, and **profile files**. All three use the same `MEMORY.md`-index-plus-topic-files shape, so the checks below apply to whichever the project actually uses. Audit every layer present, not just `.auto-memory/`.

Target: index under 30 entries, each memory file under ~10 lines, no entries older than 6 months without a freshness check.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Find which layers are in use

Check all three before concluding anything is missing:

```bash
# Layer 1 — .auto-memory/ folder (the explicit pattern)
ls .auto-memory/MEMORY.md 2>/dev/null && echo "auto-memory: exists" || echo "auto-memory: missing"
ls .auto-memory/*.md 2>/dev/null | wc -l

# Layer 2 — native memory (default location, or wherever autoMemoryDirectory points)
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null | head
grep -rs "autoMemoryDirectory\|autoMemoryEnabled" .claude/settings.json ~/.claude/settings.json 2>/dev/null

# Layer 3 — profile files
ls Profile/PROFILE_SUMMARY.md */PROFILE_SUMMARY.md 2>/dev/null
```

- **No layer found anywhere:** say "No memory system found. Run `tasks/setup-memory.md` to create one." Stop here.
- **Any layer found:** read its index and topic files and audit it. Never report "no memory system" on the absence of `.auto-memory/` alone — native memory is on by default and holds the same kind of content.
- **Native memory redirected into the project** (`autoMemoryDirectory` set): audit it as a folder like any other, and note that it is git-trackable and readable by scheduled tasks in that configuration.

Report:
```
Memory layers in use: [native | .auto-memory/ | profile files]
  Index entries: N
  Memory files on disk: N
  Index vs files: [match / N orphans / N missing pointers]
```

### Step 2 — Run the audit checklist

Run every check against each layer found in Step 1.

#### Check 1: Index size

Count entries in `MEMORY.md`. Target: ≤ 30 entries.
- Over 30: flag which entries are lowest-value candidates for consolidation or removal.
- For native memory specifically, there is a hard reason for the limit: only the first 200 lines / 25KB of `MEMORY.md` auto-load into a session. Anything past that is invisible. If the index exceeds it, flag as HIGH — those entries are not merely low-value, they are silently not loading.

#### Check 2: Orphaned files

Memory files with no pointer in `MEMORY.md` — they are loaded by nobody.
Flag each orphan.

#### Check 3: Broken pointers

Entries in `MEMORY.md` pointing to files that don't exist.
Flag each broken pointer.

#### Check 4: Staleness

For each memory file, check for a `[updated: YYYY-MM]` timestamp.

- Missing timestamp: flag as "unknown freshness"
- Timestamp older than 6 months: flag as "potentially stale — verify"
- Project memories with past dates (deadlines, events): flag as "likely expired"

#### Check 5: Duplicates

Look for memory files that cover the same topic — e.g., two files about communication preferences, or two about the same project.

Flag pairs with: "These may overlap: [file A] and [file B] — consider merging."

#### Check 6: Wrong location

Memory files should contain facts, preferences, corrections, and pointers — not standing rules or workflow instructions.

Flag any entry that looks like:
- A rule that should be in `CLAUDE.md` (e.g. "always respond in English")
- A task step or workflow description
- A code pattern or architecture note (derivable from the codebase)

#### Check 7: Content quality

For each memory file:
- Longer than ~10 lines: suggest trimming — memory should be compact facts, not narratives
- Relative dates ("next Thursday", "in a few weeks"): flag — these become meaningless; should be absolute dates

#### Check 8: Right layer for the job

Guide 04's rule: **scheduled tasks must not depend on native memory.** It is built for interactive sessions and is not reliably available to autonomous runs — a task that relies on it works some runs and forgets everything on others, which reads as a task bug rather than a memory bug.

- Any scheduled task in this project that expects remembered context, with no `.auto-memory/` or profile file it explicitly loads: flag as HIGH.
- Native memory redirected into the project via `autoMemoryDirectory`: not a finding — that puts it on disk where a task can read it. Note the configuration so the next audit doesn't re-flag it.
- The reverse case is also worth a note: heavy profile machinery built for purely interactive use, where native memory would have done the job with no files to maintain.

### Step 3 — Present findings

```
Memory Audit
────────────
Index: N entries [✓ under 30 / ⚠ over 30]
Files: N on disk [✓ matches index / ⚠ N orphans / ⚠ N broken pointers]

Issues found:

STALENESS:
  ⚠ [file]: [updated: YYYY-MM — N months ago] — verify still accurate
  ✗ [file]: no timestamp

STRUCTURE:
  ⚠ [file]: orphaned (no index pointer)
  ✗ [file]: broken pointer in index (file missing)

DUPLICATES:
  ⚠ [file-a] + [file-b]: possible overlap on [topic]

WRONG LOCATION:
  ⚠ [file]: looks like a CLAUDE.md rule, not a memory fact

CONTENT:
  ⚠ [file]: N lines — consider trimming

No issues: [files that passed all checks]

Overall: [Clean / N issues]
```

Ask:
> "Would you like me to fix these? Options:
> - (A) Fix structural issues (orphans, broken pointers, merge duplicates)
> - (B) Trim or consolidate oversized files
> - (C) Move misplaced rules to CLAUDE.md
> - (D) All of the above
> - (E) Walk through each issue together"

### Step 4 — Apply fixes

**Orphaned files:** ask whether to add a pointer to the index or delete the file.

**Broken pointers:** ask whether to remove the pointer or recreate the missing file.

**Duplicates:** read both files, produce a merged version, show the user, ask for approval before writing.

**Misplaced rules:** show the line, propose where it should go (CLAUDE.md section), apply after confirmation. Remove from memory file.

**Stale entries:** show the content, ask: "Is this still accurate? If yes, I'll update the timestamp. If no, tell me what's changed and I'll update the content."

**Trim:** for files over 10 lines, produce a condensed version preserving all distinct facts. Show before/after and apply after confirmation.

### Step 5 — Confirm

Tell the user:
- Issues found and fixed
- Final index count
- "Re-run this audit every few months, or when the memory system starts feeling slow or out-of-date."
