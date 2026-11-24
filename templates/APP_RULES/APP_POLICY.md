<!--
App rules: the always-loaded part. Paste everything below the line into the project's
AGENTS.md (or CLAUDE.md in a Claude-only project), fill in the [brackets], and delete any
rule that does not apply. Keep it short: it is read in every session. Detail lives in
docs/APP_REFERENCE.md, which the triggers below point to.
-->

---

## App rules

Work in the order set out in `docs/APP_REFERENCE.md` §1. Before changing an interface, a data model, an AI feature, tests or a release, read the matching section of that file. If a rule here conflicts with a request, say so before acting. This section holds rules, not status: migration progress and feature notes go in `docs/`, and this file stays under [24] KB.

### Build order

- Phases run in order, each closed by its gate: spec, design, foundation, milestones, release. No screen is coded before its design is chosen, and no second screen is built before the shared components and guard tests exist.
- The spec maps every input to the outputs it changes; an input that changes nothing is not built. For each thing the user creates, the spec says whether it can be saved, deleted, exported, imported, shared, reported or printed.
- One design direction is chosen before code, with the hard cases drawn (longest language, long names, empty, error, phone, dark). The handoff to the builder is defined and tested on one screen first.
- Owner feedback is sorted before fixing: a one-off is fixed in place; a pattern (anything that could recur on another page) is fixed in the component or rule, applied app-wide, and added here. A correction given twice is a rule.
- A procedure handed to the owner has been run once, as written, with the expected output of each step.

### Product

- Rules that protect someone ([allergies / permissions / limits]) are enforced in code over a reviewed vocabulary. A model may propose; code decides.
- The app works without AI for [list the core flows]. AI features say so when no model is connected.
- Every list, page and search has an empty state that says why it is empty and offers the next action. No dead ends.
- Never show a state you have no evidence for: a failed load is an error with Retry, not "nothing here" or a zero; an unknown verdict says unknown, not green.
- No explanatory helper text under headings, fields or buttons. Add a line only where a user test showed someone stuck, and prefer a disclosure that remembers its state.
- One name per concept across the interface, the API and the docs, kept in [docs/terminology.md]. Button labels are short, in sentence case, and do not repeat what the heading already says.

### Interface

- Build every page from the shared components: [page header with back link and primary action, Save, delete control, notice (error / warning / success), empty state, dialog, form controls]. Extend a component; never build a variant on one page, and never leave a native control unstyled.
- No inline styles and no colours, sizes or spacing outside [the token file]. A guard test enforces this.
- Save sits in the page header. There is no Cancel button: back cancels, and leaving with unsaved changes asks first (or the form saves as it changes).
- Deletes: permanent ones ask first; restorable ones act at once and offer Undo. Errors are red, warnings amber; never use the error style for a warning.
- Back links name where they go.
- Several possible answers use checkboxes, never a "both" option. A question that applies only under an answer is indented under it and hidden until chosen. Controls in one panel share one width.
- One primary button per action row; related buttons share a row, left-aligned. An open menu's button shows as selected.
- Icons come only from [the shipped icon set]; check the name exists before using it. An icon-only button has an accessible label; decorative icons are hidden from screen readers.
- Text never leaves its box, and related elements line up. Check every UI change with long seeded content at the widths, zoom levels, themes and languages in `docs/APP_REFERENCE.md` §2, measuring positions, before reporting done.

### Architecture

- Layers: [web / api] → services → data. Services know nothing about HTTP or templates. Every user action is one service function that the web routes and the API both call; no logic is written twice.
- Every action available in the interface is also available in the API. A parity test checks it.
- Logic never reads the clock or generates ids; callers pass `now` and the id source in. Money and other exact quantities are stored and summed as integers in their smallest unit.
- A save is committed before the response is sent. Caches are cleared after the commit, not before.
- Slow work (AI calls, imports, file parsing, downloads) never runs inside a request. It runs as a background job with a visible status; the worker catches and logs every error and keeps running.
- Anything that writes user files goes through one write layer with undo; a runtime guard in the tests fails any write from elsewhere.
- Applied migrations are never edited. Migrations take a backup first. The app refuses a database stamped by another build. Seed data never overwrites a row the user created or edited.
- Secrets never go in the repository, the database, logs or model-call records.
- Text from outside (imports, web pages, user notes) reaches a model as data inside delimiters, never as instructions. Links from input are checked for scheme; redirect targets must be local paths.
- A local server binds to loopback, checks Host and Origin against an allow-list, and throttles passcode attempts.

### Text and languages

- Every visible string lives in the language files ([en, fi, ...]). Counts use plural rules, never "1 items". All language files have the same keys; a test checks it.
- Number and date format follow the user's region setting, not the interface language.
- The user guides quote labels exactly. Renaming a label means updating every guide that quotes it, in the same commit.

### Testing and done

- Before reporting done: [lint], [type check] and [tests] pass, and any UI change has been checked in a browser as above.
- Tests assert behaviour or parsed structure, not slices of raw markup or CSS.
- Tests contain no hard-coded dates and no timing assertions; CI runs in [two] timezones and on every target OS.
- Allow-lists in guard tests may only shrink; the test pins their size.
- When a test asserted the wrong behaviour, fix it and say so in the report. Never weaken a test to make a change pass without saying why.

### Working alongside other sessions

- One writing session per worktree and branch; this checkout is [read-only / the merge point]. Never `git stash` or `git reset` a shared index.
- Before building a feature, check what other sessions are doing and what landed since you started. Before pushing to a PR branch, check the PR is still open.
- The owner runs the app from a separate worktree of merged main via [scripts/run-latest]; no session works there. Port [8000] belongs to it; previews use other ports and a different host name, and are stopped when the session ends.
- Backlog entries are typed ([bug / feature / decision / debt]), one idea each. A settled decision records the options rejected and what would reopen it; do not re-propose a rejected option.
- Before committing, update the docs named in [README §Keeping the docs current].
