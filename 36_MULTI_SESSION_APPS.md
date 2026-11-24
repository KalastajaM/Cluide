# Multi-Session App Builds: When the Tool Outgrows the Helper-App Pattern

> [Guide 22](./22_HELPER_APPS.md) covers the small tool you build for yourself: one user, one machine, a page of shared policy. This guide covers the next stage, when the same way of working produces an app other people use: a second user, a phone client, an AI feature with rules that must hold, a package you hand to friends. At that stage the assistant is still doing most of the typing, but across dozens of sessions, often several at once, and four things go wrong that a human team with branches rarely sees:
> - every session copies the nearest screen, so the interface drifts apart one page at a time;
> - tests pass while the app is wrong for a new user, so "done" stops meaning "usable";
> - AI features inside the app quietly turn one remark into a rule, or blame the wrong cause when they fail;
> - sessions working in the same repository at the same time undo each other's commits.
>
> This guide is the assistant-facing layer for that stage: what to decide before the first screen, what to set up on day one, which validation passes to schedule, and how to run parallel sessions without collisions.

> **Companion guides:**
> - [Guide 22](./22_HELPER_APPS.md) is the stage before this one. Its four patterns (invariant, helper index, verification gates, conventions) still apply and are not repeated here.
> - [Guide 29](./29_SPEC_BEFORE_REBUILD.md) is what to do when an app built this way has already grown without a contract.
> - [Guide 11](./11_GIT_INTEGRATION.md) owns branches, worktrees and the commit recipe for a shared checkout. [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) owns running sessions side by side.
> - [Guide 31](./31_BEHAVIOUR_TESTS.md) tests the assistant's behaviour; §7 here tests the app's behaviour as a user meets it.
> - [Guide 26](./26_CONTEXT_SCOPING.md) and [Guide 27](./27_INDEPENDENT_JUDGMENT.md) explain why the review passes in §7 run in fresh sessions.
> - [Guide 12](./12_SECURITY.md) owns the threat model; §5 and §7 here say when to apply it to the app itself.

> **Giving this guide to an assistant:**
> "Read 36_MULTI_SESSION_APPS.md. I'm about to start [app], which [who uses it, which devices, which AI features]. Before any design, review my spec against §3 and ask me the questions it raises. Then propose the design-system list from §4 and the day-one setup from §5 for this project."

---

## 1. What This Guide Is, and Is Not

This guide is about the collaboration, not the software. It gives no stack advice, no testing framework, no architecture opinions. Each section answers one question: what goes wrong *because an assistant builds the app across many short sessions*, and what prevents it. General engineering practice (CI, design systems, security reviews) appears only where the assistant changes when or why you need it.

The evidence is one project: a local-first household app with a web interface, a phone client over a private network, optional cloud and local AI models, and a distributable desktop package. It was built in four days of November 2026 over about 40 sessions and 177 commits, often with several sessions running at once. The figures quoted below come from that project's commit history and session reports. Treat them as one observed case, not as rates.

---

## 2. When You Have Crossed Over

[Guide 22 §8](./22_HELPER_APPS.md#8-when-to-stop-using-this-guide) lists the signs that a helper app has hit its ceiling. Any one of these means this guide applies as well:

- **More than one person uses it**, even inside one household. Settings, names and defaults now have to make sense to someone who did not write the spec.
- **It runs on more than one device class**, such as a laptop window and a phone. Every screen now has at least two layouts to keep consistent.
- **An AI feature makes decisions that must respect a rule**, such as an allergy, a budget limit or a permission.
- **Someone else installs it.** A package means first-run, empty states and recovery matter.
- **You run more than one writing session at a time** on the same repository.

The last one is the most common trigger and the least visible. Parallel sessions make a build fast (the source project landed 77 commits on one day and 75 on another), and they are where most of its process accidents came from.

---

## 3. Specify Before the First Screen

The sequence that worked: a critical review of the spec with questions, a revised spec, two rounds of wireframes, a technical design, then milestones small enough that one session finishes one. "Start milestone 3b", review, commit, merge was a rhythm that never broke.

The review step paid for itself only because it hunted for specific things. Ask the assistant to find these before any design:

- **What must never depend on the model.** In the source project, allergy enforcement first relied on the model producing canonical ingredient keys. The review pointed out that a model drifts between `garlic`, `garlic_fresh` and `fresh_garlic`, and that compound foods hide allergens. Rules that protect someone belong in deterministic code over a reviewed vocabulary; the model proposes, the code decides.
- **What works with no AI connected.** A capability table (feature, works without AI, works with a local model, needs a cloud model) settles scope arguments early and keeps the app useful when the model is off or slow.
- **Contradictions in deployment.** "Runs on localhost" and "installs on the phone" contradicted each other; the phone needs HTTPS. Resolving it in the spec cost a paragraph.
- **Keys you will need later.** A tenant or household key on every table is one column in version one and a migration across every table later.
- **The first five minutes.** Write first-run and empty states into the spec. The source project's first new-user test found that a user without AI finished setup and then could not get a single suggestion until they typed in their own recipes. That was a design omission, fixed after the fact.

Then draw the screens before the data model is final. Drawing exposed a gap no prose review had found: swapping an ingredient for a safe variant left the old ingredient named in the method steps. Steps had to refer to ingredients, not repeat them, and that changed the schema before any code existed.

---

## 4. Fix the Design System Before the Second Screen

This was the largest source of rework in the source project, and it is specific to assistant builds. A session that builds a new page reads the nearest existing page and copies its structure. With one session that is consistency; with forty sessions it is forty slightly different copies, and drift grows with the number of sessions, not with the size of the app.

The symptoms, from three consistency audits run late in the build:

- Two Save button styles, three header layouts, and title sizes of 28, 34, 40 and 46 px.
- Five different delete behaviours. Some deletes asked first and could be undone; one meal delete removed the record for good on a single tap with no question.
- Warnings shown in the red error style.
- About 360 one-off inline styles, which other sessions kept adding while the cleanup ran.
- The same correction given page by page: "Save in the header, no Cancel, warn on unsaved changes" took seven separate prompts, one per page.

**Decide these before the second screen,** as components, not as guidance:

| Pattern | Decide |
|---|---|
| Page header | Title, back link and primary action in one shared component; the back link names where it goes |
| Save | One button style and position; whether Cancel exists; what happens when you leave with unsaved changes |
| Delete | Confirm when permanent, offer Undo when restorable; one trash control style |
| Feedback | Error, warning and success styles, and which one each case uses |
| Empty states | Every empty list says why it is empty and offers the next action |
| Dialogs and sheets | Widths, where the primary button sits, whether it stays visible while the content scrolls |
| Icons and assets | The icon set you ship; if it is a subset, the list of names that render |

**Make the wrong thing hard to write.** A shared component plus a test that fails on any fixed inline style stopped the drift where written rules had not. The source project added that test after the cleanup; added on day one it would have prevented the cleanup. The same applies to [Guide 22 Pattern D](./22_HELPER_APPS.md#pattern-d--convention-normalisations): a convention the assistant keeps breaking belongs in a guard test or a component, not in a longer list.

**Write a help-text policy.** Sessions add an explanatory line under a heading or button by default. The user then removes it, one prompt at a time; in the source project that happened about a dozen times ("text not needed", "self-explanatory"). One line in the shared policy prevents the whole class: no helper text unless a user test showed someone stuck at that point.

**Alignment and every width are acceptance criteria,** not polish. Related elements share a line, at phone width, at the narrowest desktop width and at full width. Several bugs in the source project lived only at the narrow desktop width (1024 to 1279 px): a shopping-list column 92 px wide, a settings card cut off. A hidden screen-reader label widened the phone page to 621 px. Every test passed throughout. The verification gate in [Guide 22 Pattern C](./22_HELPER_APPS.md#pattern-c--verification-gates) should name all three widths and ask for measured positions, not a glance at a screenshot.

---

## 5. Day-One Repository Setup

Each item below cost minutes on day one and cost a session or more when it was added later.

- **CI that runs lint, types and tests on every push.** The source project had a `make check` target and no CI, so the check ran when someone remembered. With many sessions, "someone" is nobody in particular.
- **Guard tests for the drift you can predict.** Language files with identical keys, import layering between packages, no inline styles. Each caught regressions from other sessions. State what each guard does not cover: the layering test silently skipped three packages, and nobody noticed until a code review read it.
- **A keep-the-docs-current rule in the shared policy.** Name which documents change with which kind of change, and say that user guides quote interface labels exactly. The source project added this on day four; from then on the README and both language versions of the user guide stayed accurate. Link the user guide from inside the app; a guide that exists only in the repository is never found.
- **Reserved ports and preview hygiene.** The installed app's port is never used for a preview server. Browsers do not separate cookies by port, so local servers on one host name overwrite each other's session cookies; give each server its own host name (`localhost` for one, `127.0.0.1` for another, or a per-app `name.localhost` where the browser resolves it) or its own cookie name. Stop preview servers when the session ends. In the source project a preview left running on the real app's port made the installed app show test data, and the user believed it had switched to a demo mode.
- **Demo seed data with invented names,** before the first screenshot, recording or marketing page. A teaser built from real household data was committed; rebuilding it later does not remove the copy from history.
- **Security basics for a local server.** A local web server with no password still needs a host-name allow-list (otherwise any web page the user visits can reach it through DNS rebinding), throttling on any passcode, and a save that is durable before the user is told it succeeded. The source project's late review found all three missing ([§7](#7-validate-in-three-passes)).
- **The worktree rule in the shared policy:** one worktree per writing session ([§9](#9-parallel-sessions-on-one-repository)).

---

## 6. Milestones and the Iteration Loop

[Guide 22 §5](./22_HELPER_APPS.md#5-the-iteration-loop) describes the loop for one feature. At this stage, two additions matter.

**Size a milestone to one session.** The source project's milestones (1, 2, 3a to 3c, 4a to 4c, 5a, 5b, 6a, 6b) each ran as one cycle of "start", review, commit and merge. A milestone that needs two sessions needs a written handoff between them; splitting it in the plan is cheaper.

**One screen and one change per request.** Most of the later prompts were short and specific ("move Save to the header", "remove that sentence"), and they landed in one pass. When you ask for a page to match another, name the reference page. Better still, fix the component (§4) so there is nothing to match.

---

## 7. Validate in Three Passes

Unit and integration tests prove the code does what the session meant. They do not prove a new user can use the app, that forty sessions produced one product, or that the design is safe. Three passes do, and each works best in a fresh session that did not build what it is checking ([Guide 26](./26_CONTEXT_SCOPING.md), [Guide 27](./27_INDEPENDENT_JUDGMENT.md)).

### The new-user pass

"Run the app as a new user and do UX testing" was the most productive prompt of the source project. Each run found problems no test could: dead ends with no button forward, setup text that was wrong, a default flag every user had (so it meant nothing), the wrong choice styled as the primary button, unlabelled icon buttons, a layout that broke at one width.

The method that worked:

1. An empty data folder and the committed code in a clean worktree, so other sessions' unfinished work does not show up as findings.
2. AI switched off for the first run, because that is the path a new user hits first.
3. Every main flow at phone and desktop width, including setup, adding the first item, and the empty states.
4. A report ranked by impact, with what works well listed first so it survives the fixes.
5. Each finding checked against the code before anything is fixed. One "cut-off label" turned out to be the label's real text.

Run it after the first usable milestone, then after each major interface round. A second run after the fixes found a new layer of problems every time.

### The consistency pass

Read every template and measure every page header on a running copy, read-only, then fix in a separate session. Each of the three audits found less than the one before, and the third found regressions caused by fixes in the second: a sentence in the user guide had become false, and a page now scrolled sideways on phones. Run it after every interface round, and expect it to keep finding something while sessions run in parallel.

### The security and architecture pass

An independent review of the code, with separate reviewers for security and for architecture, run on day four of the source project. It found: database commits that ran after the response had been sent (so a failed save was reported as a success), no host-name check on the local server, unthrottled passcode login, a background worker that could die silently, a back link that could redirect off-site, and the missing CI. Most were one-line fixes, and every one was cheaper before data and users depended on the code. Run it at the end of the first real milestone and again before anyone else installs the app.

### Tests that encode the wrong expectation

Several passes found tests asserting wrong behaviour: plural forms checked with the wrong grammar, a test that cut the page at the first closing tag and missed two buttons. Fixing such a test is correct, and the session should say so in its report. A test changed quietly to make a change pass is the false-done of [Guide 22 §7](./22_HELPER_APPS.md#7-anti-patterns) in another form.

---

## 8. AI Features Inside the App

An app with its own AI features repeats, in miniature, the problems Cluide describes for assistants. Five showed up.

**Keep the rule out of the model.** See §3. The model suggests; deterministic code checks every suggestion against the rules and drops what breaks them.

**Feedback over-generalises.** One remark about one dish ("needed more sauce") became a standing instruction in three taste profiles, because each profile was rewritten from the previous profile plus new feedback. Within a week the app would have favoured sauce in everything. This is the summary-of-a-summary drift that [Guide 29's corollary for anything that learns](./29_SPEC_BEFORE_REBUILD.md#the-corollary-for-anything-that-learns) describes for learning logs. The fix: keep a remark with the item it is about, and promote it to a profile only when it recurs across different items, written as a condition ("in sauce-based dishes, make enough sauce").

**Constrained output can break small local models.** Asking a local model for output that must match a strict JSON schema from the first token made one runtime switch off the model's reasoning; the model returned an empty list in seconds. Requiring at least one item made it loop until the timeout. Let a local model reason first, then extract the structured part or convert it in a second, constrained call. Measure before assuming a local model can do a task at all.

**Errors must name the real cause.** The empty list was reported to the user as "no dish fits everyone's food rules", and a slow model as "is the server running?". Each wrong message cost a debugging session. Map each failure to its own message: no output, output dropped by a rule, timeout, unreachable.

**Log outside the transaction you are logging.** Model-call logs were written inside the job's database transaction, so a failed job rolled back its own evidence. Write the log so it survives the failure it describes.

Two more habits made the AI features usable. Route per task: local models for small, frequent tasks, cloud models for the hard ones, with latency, cost and validity recorded per task so the choice rests on data. And check the runtime before blaming the model: in the source project the local runtime had loaded a context window over 150 times larger than the prompts needed, and the machine was deep in swap.

---

## 9. Parallel Sessions on One Repository

Several sessions at once made the source project fast. Running them in one shared checkout caused these, each at least once:

- A commit built from an index read before another session committed silently reverted that session's commit.
- One session reset the shared index between another session's `git add` and `git commit`, so two commits went out without their stylesheet and language-file changes, and a repair commit followed.
- A plain `git stash` swept up every other session's uncommitted work.
- Two sessions built the same feature in parallel; the merge had to choose one and discard the other.

**The rule:** one writing session per worktree, each on its own branch, merged through one place. The shared checkout is for reading. [Guide 11](./11_GIT_INTEGRATION.md#several-sessions-in-one-checkout) has the recipe for when a session has to commit from a shared checkout anyway; the recipe working is not a reason to keep needing it.

**Split work by area, not by size.** Two sessions that touch the same files will collide however small their changes are. Brief each session with the files it owns. Some files are touched by almost every change (the stylesheet, the language files, the shared schemas); split them by feature early, or route all edits to them through one session.

**Check before you start.** Before a session builds a feature, have it check what other sessions are doing and what landed since it started. Duplicate work was the costliest collision because both versions were finished before anyone noticed.

**Report what other sessions will see.** When a session merges, it should say which files other sessions have open and which of their next commits could undo its work, so those sessions can bring their files up to date before they commit.

---

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| Fixing page by page what a component should fix | Each session copies the nearest page, so every fix has to be repeated on every page, and the next new page copies whichever version it finds |
| Helper text by default | Every session adds a line; the user removes them one prompt at a time |
| "Done" with tests green and no look at three widths | The narrow-desktop and phone layouts break while every test passes |
| New-user testing only at the end | The first-run gaps are design omissions; found late, they are rework |
| The security review after users have data | One-line fixes become migrations and apologies |
| A safety rule enforced by the model | Model output drifts; the rule silently stops holding |
| Profiles rewritten from the previous profile | One remark becomes a standing rule within a few rewrites |
| Several writing sessions in one checkout | Commits revert each other's work without any error |
| Two sessions on the same feature | Both finish, one is thrown away |
| A preview server on the installed app's port | The user sees test data in the real app and cannot tell why |
| Screenshots from real data | The copy stays in history after you replace it |

---

## Checklist

Before the first screen:

- [ ] Spec reviewed for what must not depend on the model, the no-AI capability table, deployment contradictions and keys needed later
- [ ] First-run and empty states written into the spec
- [ ] Screens drawn and the data model checked against them

Before the second screen:

- [ ] Shared components for header, Save, delete, feedback styles and empty states
- [ ] Delete policy written: confirm when permanent, Undo when restorable
- [ ] Help-text policy in the shared policy
- [ ] Verification gate names phone, narrow-desktop and full width, with measured alignment

On day one:

- [ ] CI runs lint, types and tests on every push
- [ ] Guard tests for inline styles, language-file parity and layering, each stating what it skips
- [ ] Docs rule in the shared policy; user guide linked from the app
- [ ] Ports reserved; each local server on its own host name or cookie name; previews stopped at session end
- [ ] Demo seed data with invented names
- [ ] Host-name allow-list, passcode throttling, durable save before success
- [ ] One worktree per writing session, written into the shared policy

`templates/APP_RULES/` holds these decisions as a ready-to-fill policy section and an on-demand reference; start from it rather than writing the rules from scratch.

During the build:

- [ ] Milestones sized to one session
- [ ] New-user pass after the first usable milestone and after each interface round
- [ ] Consistency pass after each interface round
- [ ] Security and architecture pass after the first real milestone and before anyone else installs the app
- [ ] AI features: rules in code, feedback scoped to its item, honest error messages, logs that survive failure

---

## Giving This to an Assistant

> "We are building [app] with several sessions over the coming weeks. Read Guide 36 and Guide 22. Review the spec against §3 and ask me the questions it raises, in one list. Then draft the shared-policy additions for §4 and §5 from `templates/APP_RULES/` (design-system patterns, help-text rule, verification widths, docs rule, ports, worktree rule) and show them to me before writing anything. Schedule the three validation passes from §7 as milestones in the plan."
