<!--
Thanks for contributing to Cluide. Please read .github/CONTRIBUTING.md first —
the four conventions in "The rules that actually catch people" cause almost
every reworked pull request, and none of them are visible in a diff.
-->

## What this changes

<!-- One or two sentences. What is different after this merges, and why. -->

## Why

<!--
For a correction: what was wrong, and how you know.
For a new pattern: where it comes from, how long you have run it, what it replaced.
For anything larger: link the issue where the scope was agreed.
-->

---

## Checks

- [ ] **Whole unit.** This is a complete change, not one batch of a larger sweep. Someone cloning `main` after this merges gets a self-consistent guide set.
- [ ] **Bundled copies mirrored.** If a numbered guide changed, the copies under `skills/*/references/` were updated too and `diff -q` reports them identical. (`00_INDEX.md` is the one permitted exception.)
- [ ] **Consumed surface unchanged or only added to.** No guide number, `tasks/` filename, or dimension number was renumbered, removed, or reused.
- [ ] **No derived counts.** This change does not state how many guides, tasks, skills, or dimensions exist.
- [ ] **Nothing non-shipping at the root.** Working files, notes, and scratch output went into `development/`.
- [ ] **No personal or proprietary data.** No real names, employer names, internal codenames, addresses, credentials, or real colleagues — in prose, examples, or placeholders.
- [ ] **The title is the changelog entry.** Do not edit `CHANGELOG.md` here. It is written at tag time from the squashed commit subjects, so this title has to carry its own scope — and name what was added if the consumed surface grew.

<!-- Adding or renaming a guide? Run tasks/review-tasks.md step 4c and paste what it reported. -->

---

<!--
This will be squash-merged, so the PR title becomes the commit subject on main.
Write it as the commit message you want to keep.
-->
