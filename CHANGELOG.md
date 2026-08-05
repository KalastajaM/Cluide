# Changelog

Cluide is versioned by content event, not on a calendar: a tag marks guides being added, a reading track being restructured, or the consumed surface changing. Minor for additions and restructures, patch for corrections.

The **consumed surface** — dimension numbers in `tasks/analyze-project-reference.md`, filenames in `tasks/`, and guide numbers — is append-only. Entries below note explicitly when it grows.

## [Unreleased]

### Fixed

- **Merge-gate check 3 no longer fails on clean `main`.** It asserted byte-identity for every guide
  and index across the root and the bundled skill mirror, without the `00_INDEX.md` exception that
  `CONTRIBUTING.md`, the pull request template and `review-tasks.md` all carry. Every guide-adding
  branch failed it.
- **The root-contents rule in `CLAUDE.md`** omitted `CHANGELOG.md` and `.github/`, so read literally
  it sent the changelog to `development/`.
- **Five derived counts removed** from `README.md`, `00_INDEX.md` and `ai-assistant-setup`, against
  the repo's own rule against writing them down.
- **`ai-assistant-setup` pointed at guide 08** for task layout, sending installed users to a stub.
- **The `00_INDEX.md` link-stripping exception was applied incompletely** — three links to unbundled
  root assets survived in the skill copy. `review-tasks.md` now records the exception's real scope.
- **`template-exporter` gained the edge cases** `audit-skill.md` requires.

### Changed

- **`tasks/README.md`** now accepts `## Hard rules` in place of `Output` + `Constraints`, and carves
  out `audit-*` tasks. The old rule was met by four of twenty-seven task files.
- **Merge-gate check 5 is marked maintainer-only.** It points at a private companion project that no
  clone has; the project is no longer named.

The consumed surface did not grow: no guide number, `tasks/` filename or dimension number was added,
renumbered or reused.

## [1.0.0] — 2026-08-04

First release. A complete operational framework for building, running, and improving a persistent AI assistant with Claude.

This release establishes the consumed surface: the numbered guides, the filenames in `tasks/`, and the dimension numbers in `tasks/analyze-project-reference.md`. Everything after this may add to that surface and may not renumber it.

### What's included

- **26 numbered guides** plus a quickstart and an index with reading tracks, covering the lifecycle from a first `CLAUDE.md` through skills, memory, MCP servers, scheduled automation, self-improving tasks, cost control, security, multi-project setups, and context scoping.
- **27 runnable tasks** in `tasks/` — `setup-*` tasks that interview and build, `audit-*` tasks that inspect read-only and then apply approved fixes, and structural-change tasks that move things and rewire every reference in the same unit of work.
- **8 installable skills** in `skills/`, from an interactive setup coach with every guide bundled, to a whole-project analyzer, a phased security audit, and a company-policy guardrail.
- **4 copy-paste templates** in `templates/` for a project, a scheduled task, a full personal assistant, and a PMO initiative.
- **Contributor documentation** in `.github/`. `CONTRIBUTING.md` covers the conventions that are invisible in a diff and cause most reworked pull requests: the byte-identical bundled guide copies under `skills/*/references/` (with a runnable check), the append-only consumed surface, the rule against writing down derived counts, and `development/` as the home for anything that does not ship. `SECURITY.md` scopes reporting to what this repository actually risks — instructions an agent will read and act on, rather than a CVE surface — and routes it through GitHub private advisories so that no email address is published. Plus a Contributor Covenant 2.1 code of conduct, a pull request template mirroring the merge gate in `CLAUDE.md`, and issue forms for corrections, patterns, and questions.

### Notable in the run-up to this release

- **Guides 23–26 added** — multi-project setups, project folder structure, project instruction layers, and context scoping.
- **A guide-set coverage check** (`review-tasks.md` step 4c) that fails loudly when a guide lands without a scoring dimension, a task never enters the mapping table, or the three statements of the guide range disagree. It caught a real regression during the final review pass.
- **The consumed-surface contract** making dimension numbers, task filenames, and guide numbers append-only, so anything citing them by number keeps meaning what it meant.
- **Guide 08 merged into Guide 07 Part 9**, its number retained as a stable address rather than reused.
- **The analysis engine widened.** Dimension 11 additionally checks for content that is gitignored but not claudeignored, and points at the new `audit-file-hygiene` task. Dimension 4 covers all three memory layers. Dimension 20 scores the app-side project fields, falling back to *requires operator input* only when the state file is genuinely unreachable.
- **`.claudeignore` excludes the bundled guide copies.** They are byte-identical build artifacts of the skills, so loading them alongside the root guides doubled the context cost and made every search return each hit twice. Skill-specific reference files stay loadable, and `review-tasks.md` reads the copies with shell commands, which `.claudeignore` does not affect.
- **Non-shipping files moved into a gitignored `development/` folder** — review notes, dated review passes, planning docs, editor configs, and the `_to_delete/` staging area. The repo root now holds only what a reader of the published guides would open, and a new working file needs the right home rather than a new ignore rule.
- **A full external review pass** applied across the guides, tasks, skills, and templates.

### Corrections landed just before tagging

These are recorded because they are the kind of error a reader would otherwise inherit, not because they existed publicly — nothing before this tag was released.

- **The app-side project fields are readable, and three files said they were not.** Guide 25 described a Cowork project's description and instructions fields as invisible to every audit, and dimension 20 of the analysis engine instructed sessions not to score them. Both fields are stored verbatim in the desktop app's own state file (`spaces.json`), reachable through the Filesystem MCP server. Guide 25 now covers the path, the schema, the absent-vs-empty trap, the freshness check, and why it is a read path and not a write path. The layer table separates *versioned* from *auditable* — the fields are the latter but not the former, and conflating the two is what produced the wrong claim.
- **`allowed-tools` was documented in Guide 03 and absent from every task that writes or audits a skill.** `setup-skill.md` offers the allowlist whenever an interview answer names a hard prohibition; `audit-skill.md` flags any skill whose constraints say NEVER but whose frontmatter does not enforce it; dimension 3 checks the same. A prohibition that maps onto a tool should be enforced, not merely written down.
- **`audit-memory.md` could only see one of the three memory layers.** It scanned `.auto-memory/` and reported "no memory system found" on setups using native memory or profile files. It now detects all three, flags the native 200-line / 25KB auto-load cap as a hard limit rather than a style preference, and checks the Guide 04 rule that scheduled tasks must not depend on native memory.
- **The bundled `00_INDEX.md` had been re-synced verbatim from the root copy**, restoring six links to `templates/`, `tasks/` and `skills/` — assets that do not ship inside the skill package and therefore resolve nowhere once it is installed. The links are stripped again, and `review-tasks.md` records this file as the one deliberate exception to byte-identity so the next sync does not silently undo it.
- **`CLAUDE.md` pointed at a file no clone contains.** The file-hygiene paragraph ends with "See `development/README.md`", but `development/` is gitignored as a whole, so that reference resolved for the maintainer and for nobody else. The paragraph is now marked optional, with a note explaining why the target is absent and stating that anyone who cloned Cluide to use the guides rather than change them can delete it.
- **Three stale references to Guide 08** after its merge into Guide 07 Part 9, in `analyze-project-reference.md`, `skills/ai-assistant-setup/SKILL.md`, and `templates/AI-ASSISTANT_TEMPLATE/README.md`.
- **Three tasks added** to close guides that had no runnable procedure: `tune-instruction-layers.md` (Guide 25), `relocate-project.md` (Guides 11 and 24 — the three layers that record absolute paths and break silently on a move, and why a streaming sync folder destroys git repositories), and `audit-file-hygiene.md` (clutter, plus trees that are gitignored but still loading as context).
- **`review-tasks.md` step 4a asserts byte-identity** between bundled guide copies and their root originals, instead of a line-count heuristic that could pass on a small edit to a large guide.
