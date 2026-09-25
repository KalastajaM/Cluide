# Task: Audit Memory

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/audit-memory.md`
> **Source guide:** `04_MEMORY_AND_PROFILE.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

Inventory shared file memory/profile files, each surface's exposed native memory, and ChatGPT project-source revisions separately. On OpenAI, ChatGPT memory and the local Codex memory store (`~/.codex/memories/`, off by default, enabled per chat with `/memories`) are separate stores; audit each on its own. A missing Claude native-memory path is N/A on OpenAI. Apply size/freshness/duplication checks to the relevant layer; do not infer native-memory contents from repository files. Validate explicit state loading in scheduled runs and record inaccessible native memory as unverified. Check one writer or branch isolation for shared state, and verify source refresh/recall separately on each supported surface.

## Purpose
Review the project's memory for stale entries, missing index pointers, duplicates, and entries that belong in `CLAUDE.md` instead. Keeps memory lean and current so it stays useful as sessions accumulate.

Guide 04 describes three on-disk layers — **native memory**, the `.auto-memory/` folder, and **profile files**. All three use the same `MEMORY.md`-index-plus-topic-files shape, so the checks below apply to whichever the project actually uses. Audit every layer present, not just `.auto-memory/`. The fourth layer in Guide 04's table, the account memory behind claude.ai and Cowork, lives in the cloud and cannot be audited from the filesystem — it appears here only in Check 8.

Target: index under 30 entries, each memory file under ~10 lines, no entries older than 6 months without a freshness check.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Find which layers are in use

Check all applicable layers before concluding anything is missing. Use the shared folder/profile checks below with a filesystem; inspect ChatGPT/native memory through exposed controls or operator-provided evidence (local Codex memory, where enabled, is under `~/.codex/memories/`). The Layer 2 shell commands are **Claude Code only**.

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

- **No layer found after all applicable layers were inspected** (unread native memory is unverified, not absent): say "No memory system found. Run `tasks/setup-memory.md` to create one." Stop here.
- **Any layer found:** read its index and topic files and audit it. Never report "no memory system" on the absence of `.auto-memory/` alone — native-memory availability and defaults depend on the actual surface.
- **Claude Code native memory redirected into the project** (`autoMemoryDirectory` set): audit it as a folder like any other, and note that it is git-trackable and readable by scheduled tasks in that configuration.

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
- For Claude Code file-native memory only, re-check the current documented loader limit before scoring. The historical limit used here is: only the first 200 lines / 25KB of `MEMORY.md` auto-load into a session. Anything past that is invisible. If the index exceeds it, flag as HIGH — those entries are not merely low-value, they are silently not loading.

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

Also flag confirmation without a user source, edit timestamps presented as verification dates,
recency used as the only conflict resolver, and rules that prevent explicit user corrections.
Expect provenance for superseded facts and separation of hypotheses from decisions. Check that
sensitive memory stays within its permitted boundary and valuable ignored state has a recovery route.

#### Check 8: Right layer for the job

Guide 04's rule: **scheduled tasks must not depend on native memory or on the account-level memory behind claude.ai and Cowork.** Neither is verified for autonomous runs — a task that relies on one may work some runs and forget everything on others, which reads as a task bug rather than a memory bug. The rule is conservative pending a test, so report the dependency as unverified rather than as known-broken.

- Any scheduled task in this project that expects remembered context, with no `.auto-memory/` or profile file it explicitly loads: flag as HIGH.
- Any reliance on the **Cowork project memory store or the account memory** (Settings → Memory) for something a scheduled task needs: flag, and ask whether it has actually been tested in a scheduled run. Untested is the same as unknown here — if it has not been tested, the fact belongs in a file the task loads explicitly.
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

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

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

<!-- harvested: 2026-09-22 from a generic executive-support framework review; design review, not production validation -->
