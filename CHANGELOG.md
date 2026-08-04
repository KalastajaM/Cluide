# Changelog

Cluide is versioned by content event, not on a calendar: a tag marks guides being added, a reading track being restructured, or the consumed surface changing. Minor for additions and restructures, patch for corrections.

The **consumed surface** — dimension numbers in `tasks/analyze-project-reference.md`, filenames in `tasks/`, and guide numbers — is append-only. Entries below note explicitly when it grows.

## [Unreleased]

### Added

- **`tasks/tune-instruction-layers.md`** — reviews a project's three instruction layers (the app-side description and instructions fields plus `CLAUDE.md`) against Guide 25. Reads the live field text, proposes ready-to-paste replacements, and updates the mirror block once you have applied them. Closes the gap where Guide 25 had no runnable task.
- **`tasks/relocate-project.md`** — moves a project, several projects, or a whole projects root, sweeping the three layers that record absolute paths and break silently: the projects, the scheduled tasks, and the desktop app's own configuration. Documents why a streaming sync folder destroys git repositories and makes shell-based audits report clean on files they never read.
- **`tasks/audit-file-hygiene.md`** — sweeps actual clutter (OS junk, lock and temp files, duplicate families, superseded outputs) and the case the ignore-rule tasks miss: a large tree that is correctly gitignored but still loading into every session because `.claudeignore` never got the same entry.

*Surface change: three filenames added to `tasks/`. Nothing renamed or removed.*

### Fixed

- **The app-side project fields are readable, and three files said they were not.** Guide 25 described the description and instructions fields as invisible to every audit, and dimension 20 of the analysis engine instructed sessions not to score them. Both fields are stored verbatim in the desktop app's own state file (`spaces.json`), reachable through the Filesystem MCP server. Guide 25 gains a *Reading the app-side fields* section covering the path, the schema, the absent-vs-empty trap, the freshness check, and why the file is a read path and not a write path. The layer table now separates *versioned* from *auditable* — the fields are the latter but not the former, and conflating the two is what produced the wrong claim.
- **`allowed-tools` was documented in Guide 03 and absent from every task that writes or audits a skill.** `setup-skill.md` now offers the allowlist whenever an interview answer names a hard prohibition, and includes it in the SKILL.md template; `audit-skill.md` flags any skill whose constraints say NEVER but whose frontmatter does not enforce it; dimension 3 checks the same. A prohibition that maps onto a tool should be enforced, not merely written down.
- **`audit-memory.md` could only see one of the three memory layers.** It scanned `.auto-memory/` and reported "no memory system found" on setups using native memory or profile files. It now detects all three, applies its checks to whichever are present, flags the native 200-line / 25KB auto-load cap as a hard limit rather than a style preference, and adds a check for the Guide 04 rule that scheduled tasks must not depend on native memory.
- **The bundled `00_INDEX.md` had been re-synced verbatim from the root copy**, restoring six links to `templates/`, `tasks/` and `skills/` — assets that do not ship inside the skill package and therefore resolve nowhere once it is installed. The links are stripped again, and `review-tasks.md` step 4a now records this file as the one deliberate exception to byte-identity, so the next sync does not silently undo it.
- **Three stale references to Guide 08** after its merge into Guide 07 Part 9, in `analyze-project-reference.md`, `skills/ai-assistant-setup/SKILL.md`, and `templates/AI-ASSISTANT_TEMPLATE/README.md`.

### Changed

- **`review-tasks.md` step 4a asserts byte-identity** (`diff -q`) instead of comparing line counts and spot-checking anything more than 5% apart. The heuristic could pass on a small edit to a large guide.
- **Dimension 11** additionally checks for content that is gitignored but not claudeignored, and points at the new `audit-file-hygiene` task. **Dimension 4** covers all three memory layers. **Dimension 20** now scores the app-side fields, falling back to *requires operator input* only when the state file is genuinely unreachable.
- **`.claudeignore` excludes the bundled guide copies.** They are byte-identical build artifacts of the skills, so loading them alongside the root guides doubled the context cost and made every search return each hit twice. Skill-specific reference files stay loadable, and `review-tasks.md` reads the copies with shell commands, which `.claudeignore` does not affect.
- **Non-shipping files moved into a gitignored `development/` folder** — review notes, dated review passes, planning docs, editor configs, and the `_to_delete/` staging area. The repo root now holds only what a reader of the published guides would open, and a new working file needs the right home rather than a new ignore rule.

## [1.0.0] — 2026-08-04

First tagged release. 26 numbered guides plus a quickstart and index, 25 runnable tasks, 8 installable skills, and 4 copy-paste templates, covering the lifecycle of a Claude assistant from initial setup through scheduled automation, self-improvement, cost control, and security.

The immediate work behind the tag: a full external review pass applied across the guides, tasks, skills and templates; guides 23–26 added (multi-project setups, project folder structure, project instruction layers, context scoping); reading tracks added to the index; Guide 08 merged into Guide 07 Part 9 with its number retained as a stable address; a guide-set coverage check that fails loudly when a guide lands without a scoring dimension; and the consumed-surface contract that makes dimension numbers, task filenames and guide numbers append-only.
## [1.0.0] — 2026-08-04

First release. A complete operational framework for building, running, and improving a persistent AI assistant with Claude.

### What's included

- **26 numbered guides** plus a quickstart and an index with reading tracks, covering the lifecycle from a first `CLAUDE.md` through skills, memory, MCP servers, scheduled automation, self-improving tasks, cost control, security, multi-project setups, and context scoping.
- **27 runnable tasks** in `tasks/` — `setup-*` tasks that interview and build, `audit-*` tasks that inspect read-only and then apply approved fixes, and structural-change tasks that move things and rewire every reference in the same unit of work.
- **8 installable skills** in `skills/`, from an interactive setup coach with every guide bundled, to a whole-project analyzer, a phased security audit, and a company-policy guardrail.
- **4 copy-paste templates** in `templates/` for a project, a scheduled task, a full personal assistant, and a PMO initiative.

### Notable in the run-up to this release

- **Guides 23–26 added** — multi-project setups, project folder structure, project instruction layers, and context scoping.
- **A guide-set coverage check** (`review-tasks.md` step 4c) that fails loudly when a guide lands without a scoring dimension, a task never enters the mapping table, or the three statements of the guide range disagree. It caught a real regression during the final review pass.
- **The consumed-surface contract** making dimension numbers, task filenames, and guide numbers append-only, so anything citing them by number keeps meaning what it meant.
- **Guide 08 merged into Guide 07 Part 9**, its number retained as a stable address rather than reused.
- **A full external review pass** applied across the guides, tasks, skills, and templates.

### Corrections landed just before tagging

These are recorded because they are the kind of error a reader would otherwise inherit, not because they existed publicly — nothing before this tag was released.

- **The app-side project fields are readable, and three files said they were not.** Guide 25 described a Cowork project's description and instructions fields as invisible to every audit, and dimension 20 of the analysis engine instructed sessions not to score them. Both fields are stored verbatim in the desktop app's own state file (`spaces.json`), reachable through the Filesystem MCP server. Guide 25 now covers the path, the schema, the absent-vs-empty trap, the freshness check, and why it is a read path and not a write path. The layer table separates *versioned* from *auditable* — the fields are the latter but not the former, and conflating the two is what produced the wrong claim.
- **`allowed-tools` was documented in Guide 03 and absent from every task that writes or audits a skill.** `setup-skill.md` offers the allowlist whenever an interview answer names a hard prohibition; `audit-skill.md` flags any skill whose constraints say NEVER but whose frontmatter does not enforce it; dimension 3 checks the same. A prohibition that maps onto a tool should be enforced, not merely written down.
- **`audit-memory.md` could only see one of the three memory layers.** It scanned `.auto-memory/` and reported "no memory system found" on setups using native memory or profile files. It now detects all three, flags the native 200-line / 25KB auto-load cap as a hard limit rather than a style preference, and checks the Guide 04 rule that scheduled tasks must not depend on native memory.
- **The bundled `00_INDEX.md` had been re-synced verbatim from the root copy**, restoring six links to `templates/`, `tasks/` and `skills/` — assets that do not ship inside the skill package and therefore resolve nowhere once it is installed. The links are stripped again, and `review-tasks.md` records this file as the one deliberate exception to byte-identity so the next sync does not silently undo it.
- **Three tasks added** to close guides that had no runnable procedure: `tune-instruction-layers.md` (Guide 25), `relocate-project.md` (Guides 11 and 24 — the three layers that record absolute paths and break silently on a move, and why a streaming sync folder destroys git repositories), and `audit-file-hygiene.md` (clutter, plus trees that are gitignored but still loading as context).
- **`review-tasks.md` step 4a asserts byte-identity** between bundled guide copies and their root originals, instead of a line-count heuristic that could pass on a small edit to a large guide.
