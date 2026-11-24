<!--
App rules: the on-demand part. Copy to docs/APP_REFERENCE.md in the project. APP_POLICY.md
(in AGENTS.md) points here before interface, data, AI and release work. Delete sections
the app will never need; fill in the [brackets].
-->

# App Reference

The detail behind the app rules in `AGENTS.md`. Each section is read before the kind of work it names. Each rule says why it exists, so a session can tell when it applies.

---

## 1. Interface patterns

Read before any change to a page, dialog, form or layout.

### Page structure

| Pattern | Rule | Why |
|---|---|---|
| Page header | One component: back link, title, optional subtitle, primary action on the title's line. Every page title has the same size | Pages built separately drift into several header layouts and title sizes |
| Back link | Names the destination ("Recipe: Lentil soup", "Settings"), never just "Back". On a page reachable from several places, it goes back where the user came from | "Back" alone hides where the user will land |
| Shell | Header and navigation stay put; content scrolls. Where a page is split into columns, each column scrolls on its own unless the content belongs together. Nothing moves or flashes when a scroll reaches its end ([`overscroll-behavior: none`] or the platform equivalent) | Bouncing headers and shifting sidebars read as bugs, especially inside a desktop wrapper |
| Wide and narrow | Decide per screen what the phone layout drops or moves. A navigation element shown in the sidebar on wide screens is not repeated as chips in the content | One project removed three such duplicates after the fact: a shortcut, a separate manage item, a second settings button |
| Navigation entries | No shortcut to something one click away elsewhere. Management actions (add, reorder, manage) sit as icons beside the list they act on, not as separate menu items | Each extra entry is one more thing to learn and keep consistent |

### Forms and saving

| Pattern | Rule | Why |
|---|---|---|
| Save | Same button, same size, same place on every form: in the header, on the title's line | Two Save styles appeared within days when each page chose its own |
| Cancel | None. Back cancels. Leaving with unsaved changes asks first | A Cancel beside Back is two ways to do one thing |
| Autosave | Settings-like pages that change one value at a time save on change and say so briefly; long forms save explicitly | A new-user test flagged one section saving on tap beside another that needed a Save button |
| Field rows | Fields side by side share the input line; a longer label or an "(optional)" note never pushes one box lower. Keep the label text in one inline element | One misaligned box was enough for the user to make alignment a standing rule for every form |
| Text areas | A resizable text area never overlaps what follows it; default height fits its expected content | Resizing pushed text areas over the next field |
| Required fields | Marked, with an inline message on the field when missing | A page-level error for one missing field sends the user hunting |
| Preferences | A user preference (units, temperature scale, language) applies everywhere it is relevant, including derived views such as totals and lists | A shopping list in the recipe's units instead of the household's was a repeated fix |

### Destructive actions

| Kind of delete | Ask first? | Undo? |
|---|---|---|
| Restorable (moves to trash, recently deleted) | No | Yes, a message with Undo |
| Permanent (no copy kept) | Yes, naming what is lost | No |
| Quick to redo (remove a tag, a chip, a row from a list) | No | Optional |

A trash or "recently deleted" view says when items go for good ([after 30 days]) instead of offering a manual empty. One trash control style everywhere.

### Feedback and states

- **Notices:** error (red) when something failed, warning (amber) when something needs attention but worked, success (brief, then gone). Never the error style for a warning.
- **Empty states:** say why it is empty in the user's terms and offer the action that fills it. A filter that matches nothing offers to loosen the filter.
- **Loading and background work:** show status for anything over a second; say what is happening and, for AI work, which model.
- **Counts:** counters in navigation update after every change that affects them, without a reload.

### Dialogs, menus and pickers

- A dialog is as narrow as its content allows; its primary button stays visible while the content scrolls.
- A popover or menu stays inside the viewport and never opens under another menu or the sidebar.
- On wide screens, a picker is centred in the content area beside the sidebar, not in the whole window.
- Reordering uses a drag handle on each row, not up and down buttons.
- A clickable title replaces a separate Edit button where the action is obvious.

### Icons, text and accessibility

- Icon-only buttons only for universally understood actions (close, delete, share, add). Anything else gets a text label, at least on phones.
- Icon and text in one control are vertically centred on each other.
- Decorative icons are hidden from screen readers; meaningful ones (a favourite heart, a warning) are not.
- Screen-reader-only text must not widen the layout; check horizontal scroll at phone width.
- Touch targets are at least [44] px on phones (a common platform guideline; not one of the source project's fixes).

### Visual verification

For every UI change: open the page at [390], [1024] and [1440] px; measure (for example with `getBoundingClientRect`) the elements that must line up; check that nothing scrolls sideways; check light and dark mode if the app has both. A screenshot is evidence, a glance is not.

---

## 2. Architecture and data

Read before changing the data model, a service, background jobs or storage.

- **One service function per user action.** If the same sequence ("save the meal, then queue the AI job") appears in two routes, it belongs in the service layer. Duplicates drift.
- **API parity.** Each interface action has an API endpoint; a test lists both and fails on a gap. It keeps the app scriptable and keeps logic out of templates.
- **Transactions.** Commit before the response is sent (check how your framework orders dependency cleanup and the response). A redirect must never reach the browser before the data it shows is committed.
- **Caches.** Invalidate after the commit. A cache shared between threads has a lock.
- **Request handlers.** Blocking work (database, file parsing) never runs where it blocks every other request; in an async framework, use synchronous handlers or a thread pool for it.
- **Background jobs.** The worker catches every exception per job, logs it, and continues. A job's result and its "done" marker are written in one transaction, so a retry cannot repeat side effects.
- **Migrations.** Back up the database before upgrading. Test the migration on a copy of real-shaped data.
- **Seed and reference data.** Loaded by an idempotent step that never overwrites user-created or user-edited rows, and records the version it loaded.
- **Files.** Written to a temporary name and renamed, so a crash or a sync service never sees half a file. Never put a live database inside a cloud-synced folder. Store media as files, not database blobs.
- **Static assets.** Addressed by content hash or version, so the browser never runs an old script against a new page.
- **Versions.** One source for the app version; everything else reads it.
- **Secrets.** Environment or the operating system's keychain. Never returned by any endpoint, never logged.
- **Untrusted input.** URLs: allow `http` and `https` only. Redirect targets: local paths only, rejecting `//` and `/\` forms. Downloads: a total time limit, a size limit, and private-address checks on the address actually connected to.

---

## 3. AI features

Read before adding or changing anything that calls a model.

- **The model proposes, code decides.** Every model output that touches a rule is checked by code; failing items are dropped with a reason.
- **Prompts are versioned files** (`<task>.v<N>`), and each model call records the version, model, latency, cost and whether the output validated.
- **Feedback stays where it belongs.** A remark about one item stays with that item. Summaries and profiles are rebuilt from the underlying records each time, not from the previous summary, and a remark reaches a profile only when it recurs across different items, written as a condition.
- **Local models.** Do not force strict structured output from the first token; let the model answer, then extract or convert. Measure each task before routing it to a local model. Check the runtime (context size, memory) before judging the model.
- **Routing per task.** Small, frequent tasks to small or local models; tasks where a mistake is costly to the strongest. Record the choice and its evidence.
- **Errors name the cause.** No output, output rejected by a rule, timeout and unreachable are four different messages.
- **Logs survive failure.** Model-call records are written outside the job's transaction.

---

## 4. Testing

Read before adding tests or changing what a test checks.

- **Guard tests** worth having from day one: no inline styles, identical keys in every language file, import layering between packages, interface/API parity, no secrets in tracked files. Each lists what it skips.
- **Parsers** get a corpus of real inputs in each supported language, checked into the repository, with the expected result per line.
- **Learning or summarising logic** gets a test that the incremental result equals a full recomputation.
- **Behaviour, not markup.** Parse the HTML and find the element; never cut the page at the first closing tag.
- **Isolation.** Each test gets its own data folder and no fixed port, so the suite can run in parallel.

---

## 5. Validation passes

Read when a milestone finishes. Each runs in a fresh session that did not build the work, read-only first, findings ranked by impact and checked against the code before fixing.

| Pass | When | Method |
|---|---|---|
| New user | After the first usable milestone, then after each interface round | Empty data folder, committed code in a clean worktree, AI off for the first run, every main flow at phone and desktop width |
| Consistency | After each interface round | Read every template; measure headers, buttons and title sizes on a running copy; list every place a shared pattern is not used |
| Security and architecture | After the first real milestone, and before anyone else installs the app | Separate reviewers for security and for architecture; each finding confirmed in the code |

---

## 6. Release

Read before building a package or handing the app to someone else.

- Screenshots, recordings and marketing material come from seeded demo data with invented names, never from a copy of real data.
- The user guide ships with the app and is reachable from inside it.
- First run on a clean machine (or a fresh data folder) is tested, including setup, the empty states and the no-AI path.
- The installed app does not share a port or data folder with development servers.
