# Contributing to Cluide

Cluide is a guide set, not a codebase. There is no build, no test suite, and no runtime — the deliverable is a body of interlocking documentation plus the tasks, skills, and templates that install it. That shapes what a good contribution looks like: the bar is whether a change makes the set more correct, more coherent, or more runnable, not whether it compiles.

Read `CLAUDE.md` before opening a pull request. It is the operating contract for this repository, and everything below is downstream of it.

---

## What fits

**Corrections.** A guide that describes a tool behaviour inaccurately, a task step that no longer works, a stale model name or price, a broken cross-reference, a claim that was true once and quietly stopped being true. These are the most valuable contributions and the easiest to accept.

**Patterns from real use.** If you run a Claude assistant and have a pattern that works in production and Cluide does not teach, describe it with the evidence: what problem it solves, how long you have run it, what it replaced. Cluide prefers one pattern proven across two independent setups to five plausible ideas.

**New guides.** The bar is high, and a new guide is a structural change rather than an addition — see *Adding a guide* below. Open an issue first and get agreement on the number and scope before writing.

**What does not fit.** Tips lists, prompt collections, links to other resources, and reformatting passes. Cluide is opinionated by design; a change that makes it more neutral or more comprehensive at the cost of being decisive is usually a step backwards.

---

## The workflow

Cluide is trunk-based. Work happens on a short-lived branch, merged into `main` by pull request, branch deleted on merge. There is no `develop` branch and no release branch, deliberately — `CLAUDE.md` explains why. `main` is always the current, self-consistent guide set.

```bash
git checkout -b short-descriptive-name
# make the change
git commit
git push -u origin short-descriptive-name
gh pr create
```

Every pull request is squash-merged, so `main` only ever gains complete units of work. Write the change as one whole unit: a half-applied sweep is a stop however clean the diff looks, because `main` is public and a partial guide set is what a stranger clones.

---

## The rules that actually catch people

Four conventions cause almost every rejected or reworked pull request. None of them are obvious from reading a diff.

### 1. The bundled guide copies must stay byte-identical

`skills/ai-assistant-setup/references/` contains copies of the numbered guides so the skill works when installed standalone. Some copies also live under `skills/cowork-optimizer/references/` and `skills/policies-validator/references/`. **Always edit the root guide, then mirror the change.** Verify before pushing:

```bash
for f in skills/*/references/[0-9][0-9]_*.md; do
  b=$(basename "$f"); [ -f "$b" ] && { diff -q "$b" "$f" >/dev/null || echo "DIFFERS: $f"; }
done
```

The one permitted exception is `00_INDEX.md`, whose bundled copy drops repo-relative links that do not resolve inside an installed skill.

### 2. The consumed surface is append-only

Guide numbers, filenames under `tasks/`, and the dimension numbers in `tasks/analyze-project-reference.md` are consumed by downstream projects that Cluide cannot see. They may be added, never renumbered, and a retired number is never reused. Guide `08` is a pointer stub rather than a deleted file for exactly this reason. A pull request that renumbers anything is a stop, not a judgement call.

### 3. Never write down a derived count

Do not state how many guides, tasks, skills, or dimensions exist — not in a guide, not in a README, not in a task file. A copied count goes stale silently: nothing breaks, no link check fails, it is simply wrong, and it stays wrong for months. Refer to the set instead ("the dimension set defined in `tasks/analyze-project-reference.md`") and let the reader look.

### 4. Anything that does not ship goes in `development/`

The repository root holds only what a reader of the published guide would open. Review notes, planning docs, scratch output, and editor configs live under `development/`, which is gitignored as a whole — so a new working file needs no new ignore rule, it just needs the right home. Before adding a file at the root, ask whether it ships.

---

## Adding a guide

A new guide is registered in more places than is obvious, and partial registration is this repository's known drift mode. A guide that exists but is not registered everywhere looks fine in review and is invisible to half the tooling.

Run `tasks/review-tasks.md` step 4c, which asserts guide-set coverage mechanically and names what is missing. Then confirm by hand that every `.md` citing the previous guide's number also cites the new one, and that the root and bundled copies are byte-identical.

---

## Style

Match the prose around you. The guides are written as connected argument, not bullet lists — a bullet list is for things that are genuinely list-like, and a table is for things with parallel structure. Em dashes are fine; this repository uses them.

State the reasoning, not just the rule. Most of Cluide's value is in the *why*, because a reader who understands why a convention exists can adapt it, and one who only knows the rule cannot. Where a recommendation has a real cost, name the cost.

Prefer concrete examples over abstract description, and invented ones over real ones. Do not put personal data, employer names, internal project codenames, or real colleague names into examples, even in a template placeholder. Use the established fake names already in the repository.

---

## Changelog

Add an entry under `## [Unreleased]` in `CHANGELOG.md` describing what changed and why. If your change grows the consumed surface — a new guide number, a new `tasks/` filename, a new dimension — say so explicitly in the entry.

Releases are content events rather than a calendar. Do not propose a version bump in a pull request; the maintainer tags when guides are added, a reading track restructures, or the consumed surface changes.

---

## Questions

Open an issue. For anything about how to *use* Cluide rather than change it, start with `00_QUICKSTART.md` and `17_TROUBLESHOOTING.md` — between them they cover most of what gets asked.
