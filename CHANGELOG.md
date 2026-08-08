# Changelog

Cluide is versioned by content event, not on a calendar: a tag marks guides being added, a reading track being restructured, or the consumed surface changing. Minor for additions and restructures, patch for corrections.

The **consumed surface** — dimension numbers in `tasks/analyze-project-reference.md`, filenames in `tasks/`, and guide numbers — is append-only. Entries below note explicitly when it grows.

## [Unreleased]

### Added

- **`git-guru` skill.** Full-lifecycle git and GitHub management: a diagnose-first loop
  (never advise from memory), a three-regime environment model (Cowork device mounts /
  cloud container / plain local) with the mount lock mechanics documented, judgment-based
  autonomy with explicit safety tiers (working-tree-destroying operations always propose
  first; pushed-history rewrites only for approved secret remediation), repo-resident
  profiles (`## Git` section per repo, template included), an added-lines-only secrets and
  personal-data scan before commits toward public or unverified remotes, and a handover
  format for commands the user must run (self-labelling output, validated against live
  state). Skills are not part of the consumed surface; nothing renumbered.

- **Guide 27 — Independent Judgment.** A guide on getting a judgment Claude reached on its own,
  rather than your own view reflected back. It separates the two mechanisms that cause it —
  anchoring (you state a view, the answer lands near it) and agreement pressure (you ask Claude to
  grade your proposal, so it grades rather than solves) — and covers what actually leaks, asking for
  the artefact instead of a verdict on yours, the commit-then-reveal protocol, blinded
  reconciliation in a fresh session, and false independence: two instances of the same model
  agreeing is correlated error, not corroboration.
  Guide 26 already owned blind review passes, so the boundary is stated in both companion blocks —
  26 covers context leaking from the *environment*, 27 covers your own view leaking from *you*.
  Pointers added from guides 02, 13 and 20, each of which cited 26 without a route to this material.
- **The consumed surface grew.** Guide number `27` is new. Dimension 13 in
  `tasks/analyze-project-reference.md` widened to `guides 20, 26, 27` and was renamed to
  "Interactive prompting, context scoping & independent judgment". Nothing was renumbered, removed,
  or reused.
- **`review-protocol` skill.** Ships the protocol Guide 27 recommends putting in a skill: stakes and
  audience in the brief with the operator's conclusions kept out, findings written to a file before
  the operator speaks, the finding schema (location, severity, confidence, and the evidence that
  would make Claude drop the finding), and anonymised reconciliation of two independent reviews in a
  fresh session. Guide 27 and Guide 26 now name it instead of describing an asset the repo did not
  ship, and dimension 13 names it as the fix.

### Changed

- **Cluide now follows Guide 27 itself.** A compliance pass found the guide set teaching, in its own
  worked prompts and tasks, several of the things Guide 27 identifies as failures. `16_BEST_PRACTICES.md`
  presented the self-review as a free win and offered "ask Claude to show its reasoning" as an
  alternative to verification; `tasks/analyze-project.md` — the task that administers the dimension 13
  check — presented its findings in chat and iterated until the operator was satisfied, with nothing
  written first and no record of what was argued away; and no finding schema anywhere in the repo
  carried a confidence or a drop-test.
  Fixed across guides 01, 02, 07, 13, 16, 17 and 26, the six `audit-*` tasks, `analyze-project`,
  `tune-instruction-layers`, `review-tasks`, `setup-self-improving-task`, the `ai-assistant-setup`,
  `cowork-optimizer` and `policies-validator` skills, the task, assistant and PMO templates, and
  `CHEATSHEET.md`. The auto-apply gates in both self-improvement templates now require a change to be
  mechanically checkable rather than "clearly correct", which also resolves the contradiction where
  the refactor step was told to remove steps the apply rule forbade it to touch.
  Full findings, with locations and severities, in `development/REVIEW_G27_2026-08-06.md`.
- **Merge gate check 1** compares the branch diff against the scope written into the branch's first
  commit message, rather than against the session's recollection of it.
- **`CLUIDE_IMPROVEMENT_PLAN.md` gained a *Revised in review* section** — findings dropped or
  re-prioritised after the draft was presented, with the evidence that moved them. The consumed
  surface did not change: no dimension number, `tasks/` filename, or guide number was touched.

---

## [1.0.1] — 2026-08-05

### Fixed

- **The `security-review` session cleanup script no longer kills MCP servers.** Its "kill zombie
  Claude processes" step matched every MCP server the desktop app spawns, and read instantaneous
  `%cpu` as a liveness signal — an idle stdio MCP server sits at 0.0% CPU as its *healthy* state.
  A deployed copy SIGTERM'd an entire MCP fleet three times a day. The kill step is removed rather
  than repaired: no `ps`-based signal separates idle-healthy from stuck, and the failure mode is
  worse than the problem. The transcript scrub is removed too — it required storing a credential
  pattern, in plaintext, in order to remove that credential. Phase 5b now installs a maintenance
  script, records that it is not wired to a hook event despite the `hook-` filename, requires any
  schedule to be written beside the install step, and adds a drift check against the reference.
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
