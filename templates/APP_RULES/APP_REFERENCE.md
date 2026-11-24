<!--
App rules: the on-demand part. Copy to docs/APP_REFERENCE.md in the project. APP_POLICY.md
(in AGENTS.md) points here before interface, data, AI, testing and release work. Delete
sections the app will never need; fill in the [brackets].
-->

# App Reference

The detail behind the app rules in `AGENTS.md`. §1 is the order of work; the other sections are read before the kind of work they name. Each rule says why it exists, so a session can tell when it applies. The reasons come from apps built mostly by an assistant: a household planner, a budgeting app, a document archive, and a regulatory checklist tool built in one long chat.

---

## 1. Build sequence

Read at the start of the project and whenever a phase ends. Most of the late tweaking in the source projects came from doing the work out of order: screens coded before there was a design, a design drawn before the spec said what the app keeps and exports, and a design system extracted from the code after the pages had drifted apart. Each phase ends with a gate. Do not start the next phase until the gate passes.

| Phase | Produce | Gate |
|---|---|---|
| 0. Spec | A critically reviewed spec, the input-output map, the data lifecycle, languages and terms, first-run and empty states | The owner has answered the review's questions in one list; every input maps to an output |
| 1. Design | One chosen direction, drawn for every main screen and state; tokens and a component list; a tested handoff | The owner has picked one direction; one screen has been built from the handoff alone |
| 2. Foundation | Tokens, shared components, guard tests, the run script, the CI matrix, a seed generator for long and demo content | The first screen uses only shared components and passes the visual verification in §2 |
| 3. Milestones | One milestone per session, each closed with a feedback round | The validation passes in §6 that fall due at this milestone |
| 4. Release | §7 | The release checklist in §7 |

### Phase 0: settle what goes in and what comes out

- **Input-output map.** List every question or field the user fills in and the outputs each one changes. An input that changes nothing is dropped before it is built. In the checklist tool the owner had to ask, after the screens existed, whether every parameter actually mattered.
- **Choice model.** For each question, record whether it takes one answer or several, and which questions only apply under a given answer. This decides the controls (§2) before anyone draws them. The checklist tool spent four feedback messages turning radio groups with a "both" option into checkboxes and nesting follow-up questions under their parent.
- **Data lifecycle.** For each thing the user creates, decide yes or no for: save, rename, delete, duplicate, export, import, share, report, print and copy. Decided late, each one arrives as its own request. The checklist tool gained saving, deleting, export and import, a full report, print and cost totals over eight separate messages.
- **Languages and terms.** Name the languages. Decide whether official or domain terms stay in their original language in the other versions, and fix the exact spelling and abbreviation of each one. The checklist tool's English version mixed in the original legal terms ("Doorlenen makes you an uitlener"), which took its own round to clean up.
- **Rules with sources.** When the output rests on rules from documents (law, policy, a standard), encode each rule once with its source. Generate the verdict and its explanation from that one rule, so they cannot disagree. In the checklist tool two sessions gave opposite verdicts on the same question, and the owner had to check the tool's own source notes to find out which held.
- **First run and empty states** are part of the spec, not polish.

### Phase 1: one design, before code

- **Mockups come before the first coded screen.** The household planner got its mockups a day after its first web interface was built, from a prompt that called its interface "very simple right now". The budgeting app went through three complete redesigns in four months, each starting from scratch, and had its design system extracted from the code afterwards. Every redesign meant another round of porting and alignment fixes.
- **Explore once, then choose.** Compare directions during the design phase, pick one, and remove the alternatives and the toggles that switched between them. After that, change the design only by refining the system, or by a planned redesign (§2 Redesigns).
- **Draw the hard cases.** Draw the longest language, long names, empty and full lists, errors, phone and desktop, and light and dark. A mockup that only shows the happy path leaves those decisions to whichever session meets them first.
- **The output is a system, not pictures:** tokens, a component list with every state (default, hover, focus, selected, disabled), and which control answers which kind of question.
- **Decide the handoff before designing,** and test it. Settle what the builder receives (a token file, component specs, a map from each mockup screen to a route), then build one screen from it before the design is called done. The owner asked "how do I give this to the builder?" in three separate design sessions.

### Phase 2: the foundation before the second screen

Build the tokens, the shared components listed in the policy, the guard tests (§5), the run script (§8), the CI matrix and a seed generator. The generator has two modes: long and extreme content for checks, and invented demo data for screenshots. The first screen is assembled only from shared components. A later screen that needs something new extends a component rather than building its own.

### Phase 3: milestones and feedback rounds

- **One milestone per session,** closed with tests, the visual verification, the user guide and changelog, and any validation pass that falls due.
- **Feedback comes in rounds.** The owner tries the build and sends one numbered list, each item naming the page and the element. The session sorts the items before fixing anything. A one-off is fixed where it is. A pattern is anything that could happen on another page: an alignment, a button style, a control choice, a helper line. A pattern is fixed in the component or the rule, applied across the app, and added to the policy. The report says which items were patterns.
- **A correction given twice is a rule.** In the checklist tool, seven of thirty messages asked for layout fixes: alignment, control widths, button colours, button rows, selected states, and where helper text sits. Each would have been one line in the interface rules.
- **"Is it ready?" is answered with the gate,** not an impression: which checks ran, which passed, and what was not checked.

---

## 2. Interface patterns

Read before any change to a page, dialog, form or layout.

### Page structure

| Pattern | Rule | Why |
|---|---|---|
| Page header | One component: back link, title, optional subtitle, primary action on the title's line. Every page title has the same size | Pages built separately drift into several header layouts and title sizes |
| Back link | Names the destination ("Recipe: Lentil soup", "Settings"), never just "Back". On a page reachable from several places, it goes back where the user came from | "Back" alone hides where the user will land |
| Shell | Header and navigation stay put; content scrolls. Where a page is split into columns, each column scrolls on its own unless the content belongs together. Nothing moves or flashes when a scroll reaches its end ([`overscroll-behavior: none`] or the platform equivalent) | Bouncing headers and shifting sidebars read as bugs, especially inside a desktop wrapper |
| Wide and narrow | Decide per screen what the phone layout drops or moves. A navigation element shown in the sidebar on wide screens is not repeated as chips in the content | One project removed three such duplicates after the fact: a shortcut, a separate manage item, a second settings button |
| Navigation entries | No shortcut to something one click away elsewhere. Management actions (add, reorder, manage) sit as icons beside the list they act on, not as separate menu items | Each extra entry is one more thing to learn and keep consistent |
| Repeated views | Every view that shows the same kind of item (a file, a record) uses one panel skeleton with one agreed block order | One app showed the same item with a different block order in three views, and one view lacked a block |
| Card grids | Cards in a row share grid rows (CSS subgrid or equivalent), so titles, figures and actions line up across cards whatever their content | Long names and extra details pushed one card's key figure away from its neighbours' |
| Action rows | Buttons that belong together sit on one row, left-aligned with the content above, and wrap as a group only when they do not fit. One primary (filled) button per row; the others share the secondary style | "Why are some buttons blue and some not?", and one download button that sat beside a line of text instead of its siblings |
| Menus and panels | The button whose menu or panel is open shows as selected. A note that belongs to a row of buttons stays under that row, not under whatever panel opens | Both came up in one feedback round: an open menu that looked unselected, and a privacy note pushed below a submenu |
| Long forms | On a long form or settings panel, the bar with the title, language and main actions stays visible while the content scrolls | The owner asked for it after scrolling away from the actions |

### Forms, controls and saving

| Pattern | Rule | Why |
|---|---|---|
| Save | Same button, same size, same place on every form: in the header, on the title's line | Two Save styles appeared within days when each page chose its own |
| Cancel | None. Back cancels. Leaving with unsaved changes asks first | A Cancel beside Back is two ways to do one thing |
| Autosave | Settings-like pages that change one value at a time save on change and say so briefly; long forms save explicitly | A new-user test flagged one section saving on tap beside another that needed a Save button |
| Native controls | Global low-specificity defaults style every input, select and button, so an unwrapped control still matches. Compare a new control's background, border, radius and height with a neighbour | A bare native select beside styled controls was flagged by the owner, and fixed in a dedicated consistency pass |
| Choice questions | A question that can take several answers uses checkboxes, never a radio group with a "both" or "mix" option. One answer from a few options uses radios or a segmented control; from many, a select | The same correction (radios to checkboxes, "both" removed) was given for eight questions over three feedback rounds |
| Follow-up questions | A question that applies only under one answer is indented under that answer and hidden until it is chosen | Flat lists repeated the same follow-up for each case and wasted space; nesting was asked for in four rounds |
| Control widths | Selects, text boxes and other controls in one panel share one width, and none is wider than the panel | A select sized to its longest option overflowed the panel its text boxes fitted |
| Selection controls | One taxonomy: tabs switch sections, segmented buttons switch views of the same data, chips narrow a list. Each has fixed accessibility semantics (`aria-selected` for tabs, `aria-pressed` for toggles) | Each pattern carries different keyboard and screen-reader behaviour; choosing by what changes keeps that behaviour predictable |
| Field rows | Fields side by side share the input line; a longer label or an "(optional)" note never pushes one box lower. Keep the label text in one inline element | One misaligned box was enough for the user to make alignment a standing rule for every form |
| Text areas | A resizable text area never overlaps what follows it; default height fits its expected content | Resizing pushed text areas over the next field |
| Required fields | Marked, with an inline message on the field when missing | A page-level error for one missing field sends the user hunting |
| Preferences | A user preference (units, temperature scale, number format, language) applies everywhere it is relevant, including derived views such as totals and lists | A shopping list in the recipe's units instead of the household's was a repeated fix |
| Scope questions | Do not ask "this item or all of them?" on every action when a setting can answer it once | A per-action scope dialog was added and removed again the next day once the setting existed |
| Double submits | Every submit is guarded against a second press while the first is in flight, and every way of closing an overlay (button, Escape, backdrop, navigation) goes through the same guard | One app created real duplicate records from double submits, and Escape silently dropped a half-finished form |

### Text and numbers in layouts

- **Short content in a fixed-height card or row is centred vertically,** not pinned to the top.
- **Text never leaves its box.** Running text wraps; a one-line control truncates with an ellipsis and shows the full text in a tooltip; flex and grid children get `min-width: 0` so they can shrink.
- **Figures never truncate.** Amounts and other figures shrink to fit, down to a minimum size, through named roles (hero, summary, table, inline). The sign and the unit are never clipped.
- **Long translations** are checked in the tightest layouts (summary cards, table headers, buttons). Long compounds in some languages and a currency symbol placed after the number broke fits that worked in English.
- **Charts** that fit their axis to the data say so in a caption (scale, start, end, change) and offer a zero-based view. Every chart has a table or CSV alternative.

### Destructive actions

| Kind of delete | Ask first? | Undo? |
|---|---|---|
| Restorable (moves to trash, recently deleted) | No | Yes, a message with Undo |
| Permanent (no copy kept) | Yes, naming what is lost | No |
| Quick to redo (remove a tag, a chip, a row from a list) | No | Optional |

A trash or "recently deleted" view says when items go for good ([after 30 days]) instead of offering a manual empty. One trash control style everywhere. For an app that manages the user's own files, "never delete" is a product invariant: deletes move to a trash folder, with a short written list of exceptions.

### Feedback and states

- **Notices:** error (red) when something failed, warning (amber) when something needs attention but worked, success (brief, then gone). Never the error style for a warning.
- **Failed loads** show an error with Retry, never the empty state. A failed query once displayed "nothing here yet" and a zero total; a regression test now reproduces that case.
- **Unknown is a state.** A verdict with too little data behind it ("on track", a green badge) shows a muted "too early to tell" instead. One review found six silently wrong figures, including a goal shown on track with too little data.
- **Empty states:** say why it is empty in the user's terms and offer the action that fills it. A filter that matches nothing offers to loosen the filter.
- **Loading and background work:** show status for anything over a second; say what is happening and, for AI work, which model.
- **Counts:** counters in navigation update after every change that affects them, without a reload.
- **Explanations:** when a page needs one, put it behind a disclosure that remembers whether the user opened it, rather than a line that is always there.

### Dialogs, menus and pickers

- A dialog is as narrow as its content allows; its primary button stays visible while the content scrolls.
- A popover, menu or tooltip renders in the top layer and stays inside the viewport; it never opens under another menu or the sidebar.
- On wide screens, a picker is centred in the content area beside the sidebar, not in the whole window.
- Reordering uses a drag handle on each row, not up and down buttons.
- A clickable title replaces a separate Edit button where the action is obvious.

### Icons, text and accessibility

- Icon-only buttons only for universally understood actions (close, delete, share, add). Anything else gets a text label, at least on phones.
- Icon and text in one control are vertically centred on each other. A row of icon actions is one grouped control.
- Decorative icons are hidden from screen readers; meaningful ones (a favourite heart, a warning) are not.
- Screen-reader-only text must not widen the layout; check horizontal scroll at phone width.
- Touch targets are at least [44] px on phones.
- Labels use sentence case. The button that opens something, the title of what opens, and the empty state that leads there use the same words.

### Themes

Design dark tokens together with the light ones; a dark theme derived afterwards produced unreadable text. Offer light, dark and automatic as soon as the app has a settings page.

### Visual verification

For every UI change:

1. Seed long content: long unbroken names, long translations, large and negative numbers, empty and full lists.
2. Open the page at [320], [390], [768], [1024], [1299] and [1440] px, at 100% and 200% zoom, in light and dark, and in every supported language. Two of those widths (one just under a breakpoint, one very narrow) found layout breaks the common sizes missed.
3. Run [the overflow script], which flags any element whose content escapes its box, and measure (for example with `getBoundingClientRect`) the elements that must line up. A screenshot is evidence; a glance is not.
4. Fix any older violation you meet on the page in the same change.

### Debugging a layout bug

Before changing anything, list every element that could produce what the screenshot shows, and rule each one out against the screenshot (exact label text, sign, shape, which card). Write the reasoning down, then fix the one that remains. A fix applied to the wrong element costs a second round and often a regression.

### Redesigns

- Port the new design screen by screen behind a temporary style switch that uses the same components. Never build a second interface tree.
- Brief the builder that the existing app wins on features only: layout and arrangement follow the design. Compare each screen visually with the design before merging; a first pass that only restyled the old arrangement had to be redone.
- From the moment the new look exists, new features are built in it only.
- When the old look is removed, fold its styles away and compare the computed style of every element across screens, themes, widths and hover and focus states, before and after.

---

## 3. Architecture and data

Read before changing the data model, a service, background jobs or storage.

### Structure

- **One service function per user action.** If the same sequence ("save the meal, then queue the AI job") appears in two routes, it belongs in the service layer. Duplicates drift.
- **API parity.** Each interface action has an API endpoint; a test lists both and fails on a gap. Input schemas can generate the CLI flags, help text and AI tool schemas from one definition.
- **Pages never compute or save directly.** A lint rule forbids pages from doing arithmetic on domain values or writing to storage. Retrofitting this boundary into a grown app took one project 14 pull requests in three days.
- **Logic returns codes, not text.** The service layer returns error and status codes; the interface turns them into words in the user's language.
- **Commit the generated API schema** (OpenAPI or equivalent) and the typed client generated from it, and fail CI when they drift from the code.
- **Schedule a structural pass** after roughly the first hundred commits: split large modules by area, one job runner, explicit wiring, no private imports across modules, a layering test. Splitting by area also reduces collisions between parallel sessions.

### Values, time and identity

- **No clock or id generation inside logic.** `now` and the id generator are required parameters, and a lint rule forbids reading the clock in the core. Removing the defaults in one project found three callers silently using wall time.
- **Exact arithmetic.** Money is stored and summed as integers in the smallest unit. Floating-point balances drifted while display rounding hid it; a property test now pins exactness.
- **Dates** are ISO strings (`YYYY-MM-DD`) compared as strings. Never derive a calendar date from a UTC timestamp, and count whole days on the calendar, not by dividing milliseconds.
- **Conventions at the boundary.** A sign or unit convention (expenses negative, amounts in cents) is enforced where data is written, and a runtime invariant check (for example, money in equals money out plus balance) runs in the app and shows its result.
- **A value computed in one unit and shown in another** has an assertion between the two; self-consistent wrong figures pass every local check.
- **Stable identity for files.** Metadata about the user's files is keyed by a stable file identity, not by path alone, so a rename made outside the app reconnects. Do not trust creation or modification times on a synced drive.
- **Locale-specific logic** (country rules, language-specific parsing) lives in packs with golden test corpora before the first public release, not inline in the core.

### Transactions, concurrency and state

- **Commit before responding.** Check how your framework orders dependency cleanup and the response. A redirect must never reach the browser before the data it shows is committed.
- **Caches** are invalidated after the commit. A cache shared between threads has a lock.
- **Request handlers.** Blocking work (database, file parsing) never runs where it blocks every other request; in an async framework, use synchronous handlers or a thread pool for it.
- **Background jobs.** The worker catches every exception per job, logs it, and continues. A job's result and its "done" marker are written in one transaction, so a retry cannot repeat side effects.
- **Async work belongs to the context that started it.** Capture the session, document or account when the work starts; when it finishes in a different one, fail instead of writing. Refuse writes while a load or a wizard holds the state. One review reproduced data written into the wrong budget at an Undo boundary.
- **Optimistic writes** are registered while in flight and flushed or warned about when the page unloads.
- **One lock for every process.** The CLI and the server share one lock file that records who holds it. Undo, restore and other bulk operations are refused while a batch job runs, and the database is never swapped under a running job.
- **One copy of the app per data folder.** Two installs on one folder means two databases that diverge. For a second machine, move the data folder and use one machine at a time.

### Storage and files

- **One write layer** for anything that touches the user's files: each change is a plan, a journal entry and an undo record. Undo is tested for the side data too (tags, notes, records), not only the file move; that is where undo bugs recurred.
- **Files** are written to a temporary name and renamed, then the directory is synced, so a crash or a sync service never sees half a file. Never put a live database inside a cloud-synced folder. Store media as files, not database blobs.
- **A store split across files** (a database plus a settings file) is resumable: an operation that a crash cut off between the two is finished at the next start.
- **File-based saves in a local-first app** write the before-state and the intended after-state to a journal first, then roll forward or stop on a mismatch, with a version check that shows conflicts to the user.
- **Derived data** (a search index, a cache) can be rebuilt from its source and holds no copy it does not need.
- **Migrations** take a backup first and are tested on a copy of real-shaped data. An applied migration is never edited (CI checks a hash); fix it with a new one. Migration ids are unique across forks, and the app refuses a database stamped by a different build instead of migrating it.
- **Seed and reference data** are loaded by an idempotent step that never overwrites user-created or user-edited rows, and records the version it loaded.
- **Static assets** are addressed by content hash or version, so the browser never runs an old script against a new page.
- **Versions.** One source for the app version; everything else reads it. Where copies cannot be avoided (manifests, issue templates), the release checklist lists every one.

### Performance

Measure on a synthetic large dataset ([50,000 items]) from the start, kept as a test fixture generator. One project found an index update that scanned everything per file, so moving 300 files took 16 seconds; another needed row virtualisation and lazily loaded screens. The app's own file watcher must ignore the changes the app makes.

### Security and privacy

- **Secrets** live in the environment or the operating system's keychain. Never returned by any endpoint, never logged.
- **Local server:** bind to loopback; check Host, Origin and `Sec-Fetch-Site`; require an app token on the API so only the app's own interface and CLI can call it; throttle passcode attempts.
- **Untrusted input.** URLs: allow `http` and `https` only. Redirect targets: local paths only, rejecting `//` and `/\` forms. Downloads: a total time limit, a size limit, and private-address checks on the address actually connected to.
- **Parsers and importers** are hardened against hostile files: limits on archive expansion and size, a marker so a file that crashes the reader is not retried at every start, and validation of any backup, database or settings file before a restore. Never hand HTML or SVG from the user's data to the operating system's "open".
- **Data that leaves the machine** (to an AI model, a lookup service) goes only on the user's action, after a preview of exactly what will be sent, and never from excluded folders. Say so in `SECURITY.md`, so a leak path counts as a vulnerability.
- **Responses with personal or financial data** are not cached by the browser, and tokens in URLs are removed from logs and referrers.

---

## 4. AI features

Read before adding or changing anything that calls a model.

- **The model proposes, code decides.** Every model output that touches a rule is checked by code; failing items are dropped with a reason.
- **Prompts are versioned files** (`<task>.v<N>`), and each model call records the version, model, latency, cost and whether the output validated.
- **Feedback stays where it belongs.** A remark about one item stays with that item. Summaries and profiles are rebuilt from the underlying records each time, not from the previous summary, and a remark reaches a profile only when it recurs across different items, written as a condition.
- **Local models.** Do not force strict structured output from the first token; let the model answer, then extract or convert. Measure each task before routing it to a local model. Check the runtime (context size, memory) before judging the model.
- **Routing per task.** Small, frequent tasks to small or local models; tasks where a mistake is costly to the strongest. Record the choice and its evidence.
- **Errors name the cause.** No output, output rejected by a rule, timeout and unreachable are four different messages.
- **Logs survive failure.** Model-call records are written outside the job's transaction.
- **AI tools inside the app** call the same service functions as the interface, with the same clock and id parameters; one budgeting app found its AI forecast tool silently using wall time.

---

## 5. Testing

Read before adding tests or changing what a test checks.

### Guards

- **Guard tests** worth having from day one: no inline styles, identical keys in every language file, import layering between packages, interface/API parity, no secrets in tracked files, explicit text encoding on every file open. Each lists what it skips.
- **Enforce a write rule twice:** a static test that reads the source, and a runtime guard (in Python, `sys.addaudithook`) that fails any test in which code outside the allowed module writes, renames or removes a file. The runtime guard cannot be hidden by a broad `except`. Exceptions are listed with a reason, and a test that legitimately writes declares it with a marker.
- **Ratchets only tighten.** An allow-list of known violations has a test that pins its size, so it can shrink but never grow.
- **Make the stricter lint rule an error** and fix what it finds; switching one project's hook-dependency rule to an error found a real stale-closure bug.
- **A type checker on the risky core** (domain logic, storage) is worth it even where the rest of the code stays untyped.

### Kinds of tests

- **Parsers** get a corpus of real inputs in each supported language, checked into the repository, with the expected result per line.
- **Domain logic** gets property tests (for example with fast-check or Hypothesis) and golden whole-output scenarios, with a coverage threshold on the core.
- **Learning or summarising logic** gets a test that the incremental result equals a full recomputation.
- **Storage adapters** (local file, browser storage, server) all run one shared contract suite.
- **Undo** is tested for every kind of data an action touches.
- **End-to-end tests** start early, in the first month, not after the app has grown. They wait on state (the save response, the reload, the dialog's open class), not on the page looking done, and the app offers an injectable delay so races can be reproduced on purpose.
- **Documents with counts and cross-references** (a spec, a reference) get a test that keeps the counts honest.
- **Replacing a core** (a rewrite, a new engine behind the same app) gets a read-only comparison harness before anything switches over. Both sides read the same data with the clock pinned (a `--now` option) and are compared to the cent. Every difference is classified against a written list of expected differences, and core defects and unexplained differences are reported first. The budgeting app's engine replacement ran this way through several reruns without touching live data.

### Reliability

- **Behaviour, not markup.** Parse the HTML and find the element; never cut the page at the first closing tag or match raw CSS text.
- **No hard-coded dates.** A test that hard-coded a date became a time bomb that would fail on its own a few weeks later. Use a fixed clock passed in.
- **No timing assertions.** Count events instead; timing checks fail on busy CI runners.
- **Isolation.** Each test gets its own data folder and no fixed port, so the suite can run in parallel.
- **Run under load.** Run the full suite with parallel workers regularly; some tests only fail when others run beside them. Keep a known-flaky list as backlog debt, not as retries.
- **Matrix.** CI runs on every target operating system and in at least two timezones from day one. Running only on one OS in UTC hid a whole class of date bugs and Windows path and encoding bugs.

---

## 6. Validation passes

Read when a milestone finishes. Each runs in a fresh session that did not build the work, read-only first, findings ranked by impact and checked against the code before fixing.

| Pass | When | Method |
|---|---|---|
| New user | After the first usable milestone, then after each interface round | Empty data folder, committed code in a clean worktree, AI off for the first run, every main flow at phone and desktop width |
| Consistency | After each interface round | Read every template; measure headers, buttons and title sizes on a running copy; list every place a shared pattern is not used |
| Security and architecture | After the first real milestone, and before anyone else installs the app | Separate reviewers for security and for architecture; each finding confirmed in the code |
| Feature gap | Once, before 1.0 | Compare with comparable products; record each gap as wanted, rejected (with the reason) or deferred |

- **Say what a pass did not check.** A review report has a coverage table and a "not verified" list. An assistant's walk-through is a heuristic review, not a user study; its recommendations are proposals until the owner has tried them.
- **Review reports are dated records.** Do not edit the findings afterwards; add a status block at the top as items close. Where a report and the code disagree, the code wins.
- **Fix a broad review serially.** Before fixing, recheck every finding against the latest main, after other sessions have landed. Land the fixes as a stack of small pull requests in order.

---

## 7. Release and publishing

Read before building a package, publishing the repository, or handing the app to someone else.

### Before the first public commit

- **Decide on day one whether the assistant's instructions and plans are public.** If not, ignore `CLAUDE.md`, `AGENTS.md` and the planning documents from the first commit. One project removed them from tracking later; they stay in its history.
- **Keep a private working repository and publish a squashed export** to the public one. The export is a dry run by default, excludes paths through an export-ignore list, fails on any match in a deny-pattern list (personal names, accounts, paths, which grows with every new one), and refuses an author email that is not a no-reply address. A pre-push hook blocks pushing the private history to the public remote. Releasing is a human step.
- **Order the switch-over.** Rename the private repository and repoint every clone before creating the public one, so no redirect sends a push to the wrong place. Turn on secret scanning and push protection.
- **Licences.** Keep copyleft dependencies out of the core (behind an optional extra, documented in `docs/licensing.md`). Bundle fonts locally with their licence note and never fetch them at runtime. Put the licence in every package manifest, not only `LICENSE`.

### Repository settings

- **A settings checklist file** ([docs/github-settings.md]): description, topics, social preview, private vulnerability reporting, dependency alerts and updates, discussions, branch protection.
- **Branch protection requires one aggregate CI job** that passes when every job that ran passed. Jobs filtered by path would otherwise skip and block the merge.
- **CI hygiene:** cancel superseded runs per pull request, read-only token permissions, actions pinned to a commit hash with a version comment, installs from the frozen lockfile.
- **Dependencies:** grouped weekly updates with documented major-version holds, a weekly audit workflow at high severity, and no forced audit fixes.
- **A pull-request template** with a "no personal data in code, tests, docs or screenshots" box, and a "not negotiable" security block in `CONTRIBUTING.md`.

### Each release

- Screenshots, recordings and marketing material come from seeded demo data with invented names, never from a copy of real data. A script stages the demo data and takes the screenshots, and is rerun after each interface round.
- The user guide ships with the app and is reachable from inside it; the technical reference is a separate document. If the app bundles the docs, CI runs when they change.
- The release commit changes the version in every place the checklist lists. The changelog's Unreleased entries become the version's section with a summary on top, no entry reworded or dropped, and a new empty Unreleased section.
- First run on a clean machine (or a fresh data folder) is tested, including setup, the empty states and the no-AI path.
- The installed app does not share a port or data folder with development servers.

---

## 8. Working with the assistant

Read when setting up the project, and when the way of working changes.

- **The owner's copy runs from its own worktree** of merged main, updated by one script ([scripts/run-latest]) that fetches, installs only when the lockfile changed, rebuilds only when the commit changed, and starts the app. One owner ran the app from the checkout builders were rebuilding and saw an old interface against a new backend.
- **One launcher.** A single documented command starts the development app, and it assumes neither one operating-system user nor a package-manager service.
- **Check the pull request is still open before pushing to its branch.** Commits pushed after a squash merge never reach main.
- **Unattended work** (overnight, while the owner is away) is a stack of small pull requests with a note to merge them in order. Items that need the owner's decision go on a side branch that can be skipped, and the report lists what was deliberately not built. Cluide's Guide 11 covers landing a stack.
- **Plan first for named risky paths:** [the domain core, the server, migrations, storage, any change across several files]. Typos, translations and documentation edits need no plan.
- **The backlog is typed** (`[bug]`, `[feature]`, `[decision]`, `[debt]`, `[check]`), one idea per entry. Closed entries move to a closed file; a "won't fix" says what would reopen it. Search the closed file before adding an entry.
- **Decisions record the options rejected** and the condition that would reopen them. Rejected features are not proposed again.
- **Memory notes** are written as a rule with a dated reason and a line on how to apply it, so a later session can tell whether it still holds.
- **The policy file holds rules, not status.** One project's policy grew 2.6 times in five weeks to 50 KB, past the size one assistant loads by default, and almost half of it was a migration changelog. Keep status in `docs/`, keep a size budget, prune when a rule is enforced by a test, and give each rule the incident it came from so it can be retired.
- **Feedback rounds.** The owner tries the app and sends one batch of feedback; the session sorts it into one-offs and patterns (§1, Phase 3), fixes it, then updates the user guide and changelog in the same round.
- **A procedure handed to the owner has been run.** Steps the owner will run (a migration, a re-vendor, a restore) are executed once, as written, by the session that wrote them. They list the full sequence with the expected output of each step. One re-vendor procedure failed at its first command because of wrong argument syntax, and the owner had to ask for the full sequence.
