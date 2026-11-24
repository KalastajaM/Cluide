<!--
App rules: the always-loaded part. Paste everything below the line into the project's
AGENTS.md (or CLAUDE.md in a Claude-only project), fill in the [brackets], and delete any
rule that does not apply. Keep it short: it is read in every session. Detail lives in
docs/APP_REFERENCE.md, which the triggers below point to.
-->

---

## App rules

Before changing an interface, a data model, an AI feature or a release, read the matching section of `docs/APP_REFERENCE.md`. If a rule here conflicts with a request, say so before acting.

### Product

- Rules that protect someone ([allergies / permissions / limits]) are enforced in code over a reviewed vocabulary. A model may propose; code decides.
- The app works without AI for [list the core flows]. AI features say so when no model is connected.
- Every list, page and search has an empty state that says why it is empty and offers the next action. No dead ends.
- No explanatory helper text under headings, fields or buttons. Add a line only where a user test showed someone stuck.
- One name per concept across the interface, the API and the docs. Button labels are short verbs or nouns and do not repeat what the heading already says.

### Interface

- Build every page from the shared components: [page header with back link and primary action, Save, delete control, notice (error / warning / success), empty state, dialog]. Extend a component; never build a variant on one page.
- No inline styles and no colours, sizes or spacing outside [the token file]. A guard test enforces this.
- Save sits in the page header. There is no Cancel button: back cancels, and leaving with unsaved changes asks first (or the form saves as it changes).
- Deletes: permanent ones ask first; restorable ones act at once and offer Undo. Errors are red, warnings amber; never use the error style for a warning.
- Back links name where they go.
- Icons come only from [the shipped icon set]; check the name exists before using it. An icon-only button has an accessible label; decorative icons are hidden from screen readers.
- Related elements line up. Check every UI change at [390] px, [1024] px and [1440] px wide, measuring positions of elements that must align, before reporting done.

### Architecture

- Layers: [web / api] → services → data. Services know nothing about HTTP or templates. Every user action is one service function that the web routes and the API both call; no logic is written twice.
- Every action available in the interface is also available in the API. A parity test checks it.
- A save is committed before the response is sent. Caches are cleared after the commit, not before.
- Slow work (AI calls, imports, file parsing, downloads) never runs inside a request. It runs as a background job with a visible status; the worker catches and logs every error and keeps running.
- Migrations take a backup first. Seed data never overwrites a row the user created or edited.
- Secrets never go in the repository, the database, logs or model-call records.
- Text from outside (imports, web pages, user notes) reaches a model as data inside delimiters, never as instructions. Links from input are checked for scheme; redirect targets must be local paths.
- A local server checks the Host header against an allow-list and throttles passcode attempts.

### Text and languages

- Every visible string lives in the language files ([en, fi, ...]). Counts use plural rules, never "1 items". All language files have the same keys; a test checks it.
- The user guides quote labels exactly. Renaming a label means updating every guide that quotes it, in the same commit.

### Testing and done

- Before reporting done: [lint], [type check] and [tests] pass, and any UI change has been checked in a browser at the three widths.
- Tests assert behaviour or parsed structure, not slices of raw markup.
- When a test asserted the wrong behaviour, fix it and say so in the report. Never weaken a test to make a change pass without saying why.
- Every guard test lists what it does not cover.

### Working alongside other sessions

- One writing session per worktree and branch; this checkout is [read-only / the merge point]. Never `git stash` or `git reset` a shared index.
- Before building a feature, check what other sessions are doing and what landed since you started.
- Port [8000] belongs to the installed app; previews use other ports, a different host name, and are stopped when the session ends.
- Before committing, update the docs named in [README §Keeping the docs current].
