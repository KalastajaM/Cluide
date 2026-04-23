# Personal Helper Apps Guide: Collaborating with Claude on Small Tools You Build for Yourself

*Last reviewed: April 2026*

> Most of Cluide is about co-work — how Claude drafts your emails, runs your briefings, files your actions. This guide is about an adjacent use-case: the small locally-run tool you build *for yourself* with Claude's help. A budget tracker, a reading log, a data dashboard, a CLI wrapper around an API. Not a product. Not a team deliverable. One user, local data, evolves feature-by-feature over many short sessions.

> **Companion guides:** [Guide 01](./01_CLAUDE_MD.md) covers CLAUDE.md structure — this guide adds four patterns that are specific to helper apps. [Guide 05](./05_MCP_SERVERS.md) covers MCP servers, including Claude Preview and Claude in Chrome which this guide leans on for verification. [Guide 12](./12_SECURITY.md) covers permission hygiene. [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers the build-vs-run split. [Guide 20](./20_INTERACTIVE_PROMPTING.md) covers plan mode, which underpins the iteration loop described here.

> **Giving this guide to Claude:**
> "Read 22_HELPER_APPS.md and help me set up the CLAUDE.md for this helper app — interview me about the app's one invariant, the helpers I already have, and what 'done' looks like for each class of change."

---

## 1. Why This Pattern

Small personal tools have a distinctive shape. There is one user (you), one machine, one dataset, and no deadline. The cost of a bug is annoyance, not revenue. The app will never be deployed, shared, or scaled. You are vibe-coding — improvising features as you notice you want them — and Claude is doing most of the typing.

That shape creates two failure modes Cluide's co-work guides don't directly address:

- **Drift over sessions.** You add a feature this week, forget the conventions next week, and Claude — starting each session cold — reinvents helpers you already wrote, breaks invariants you never wrote down, and introduces a third way of formatting dates. The app slowly rots.
- **False "done".** Claude writes code that compiles, runs the test, reports success, and the UI is visibly broken. Or the data file is silently corrupted. Without a hard verification gate, "done" means "the code ran" — not "the thing works".

This guide is about pushing both failure modes back into the CLAUDE.md layer, where they cost one line each to prevent.

---

## 2. What This Guide Is *Not*

It is not a software-engineering guide. No stack recommendations, no test framework advice, no architecture opinions. Use whatever you want — vanilla JS, Python, a single Bash script. What this guide covers is the *Claude-facing layer*: what to put in CLAUDE.md, how to structure the iteration loop, what MCP tools to use for verification, and how to keep the permission surface tight. Everything here applies whether your helper app is 200 lines or 20,000.

It is also not a guide for anything larger. If the tool grows a second user, an auth system, or a production deployment, stop treating it as a helper app — it needs real engineering discipline, which is outside Cluide's scope entirely.

---

## 3. Four CLAUDE.md Patterns for Helper Apps

These layer on top of the general CLAUDE.md advice in [Guide 01](./01_CLAUDE_MD.md). Each is one short block. Together they prevent the drift and false-done failure modes from Section 1.

### Pattern A — The Domain Invariant

Every helper app has one non-negotiable truth about its data. Money in = money out plus savings. Books read this year + books to read = total books. Sum of time tracked per project = total time tracked. Find yours, state it in one line, and tell Claude to preserve it through every change.

```markdown
## Invariant

`sum(parts) == whole` at all times. Any change that affects the parts or the
whole must recompute both and verify equality before writing to disk.
Never compute this by hand — always call the canonical helper.
```

The invariant is the thing a reviewer would catch in five seconds but Claude will happily introduce a regression for if it isn't written down. One line, one invariant. If you have two, you have two sections. If you have seven, your app is bigger than a helper app.

### Pattern B — The Helper Index

Every helper app accumulates a small library of utility functions that cover 90% of the common cases — a currency formatter, an ID generator, a DOM-escape helper, a toast popup, whatever. The drift failure mode is Claude writing a sixth variant of `formatMoney` in session twelve because it didn't know about the first five.

Fix it with a named list at the top of CLAUDE.md:

```markdown
## Helpers — check these first before writing new code

- `fmt(value, currency)` in `lib/format.js` — all currency display
- `escapeHtml(str)` in `lib/dom.js` — all dynamic HTML
- `newId()` in `lib/id.js` — all new entity IDs
- `toast(msg)` in `lib/ui.js` — all user-visible confirmations
- `readJSON(path)` / `writeJSON(path, obj)` in `lib/storage.js` — all persistence

Before writing a new utility, check whether one of these already covers the need.
```

Keep it to the 5–10 helpers that cover the common paths. Not a full API reference — a *reuse checklist*. Update it whenever you consolidate a new helper.

### Pattern C — Verification Gates

State, per class of change, what "done" requires. Not "run the tests" — specific, observable verification steps tied to the actual MCP tools Claude has.

```markdown
## Verification — before reporting any change as done

- UI / CSS change → take a screenshot via Claude Preview MCP, confirm the
  element looks correct. Code review alone is not enough.
- Data mutation → reload the app, re-read the affected file, confirm the
  invariant from the Invariant section still holds.
- New feature → run the happy path end-to-end in the browser; then try one
  edge case (empty list, long string, negative number).
- Refactor → run the smoke check above and confirm no user-visible change.
```

The point is to deny Claude the move of writing code, noting the code compiles, and reporting success. The gate is a tool call, not a promise.

### Pattern D — Convention Normalisations

The small one-line rules that prevent repeated conversations: sign conventions, ordering rules, string-handling rules, language-parity rules. One line per convention.

```markdown
## Conventions

- Money amounts are stored signed; display with `Math.abs()` and the sign
  applied explicitly. Never render a raw negative string.
- Array order IS display order — there is no separate `order` field.
- Every user-visible string lives in `i18n.js` with both `en` and `fi` keys.
  Never hardcode.
- Never interpolate user data into `innerHTML`. Use `textContent` or
  `escapeHtml()`.
```

Each line is there because you caught the same bug twice and don't want to catch it a third time. When a new convention emerges from a review comment, promote it to this list the same session.

---

## 4. Keep the Permission Surface Tight

`.claude/settings.local.json` is the permission allow-list for this project. For a helper app, it should list the minimum set of tools Claude actually needs to build and verify the app — and nothing else. See [Guide 12](./12_SECURITY.md) for the broader threat model; the helper-app-specific guidance is:

- The run command for your local preview (`python3 -m http.server 8081`, `npm run dev`, whatever) — one entry.
- The MCP tool you use for visual verification (`preview_start`, `preview_screenshot`, or the Claude-in-Chrome equivalents) — only the ones you actually rely on.
- The git/gh commands you use for committing and pushing.
- Nothing else. No broad shell allow. No filesystem wildcards.

A tight allow-list is cheap insurance against Claude deciding, mid-session, to install a dependency, delete a file, or run a script you didn't expect. You will feel a few extra permission prompts early on; you will stop feeling them once the list covers your real workflow.

---

## 5. The Iteration Loop

Helper apps are built feature-by-feature over dozens of short sessions. The loop that works:

1. **You describe the next feature in one sentence.**
2. **Claude drafts a plan as a checklist** — a short `.md` file in a `plans/` folder, with checkbox items, the exact file paths that will change, and inline sketches of the key changes. Plan mode ([Guide 20](./20_INTERACTIVE_PROMPTING.md)) is built for this.
3. **You read the plan, push back on anything off-base, approve.**
4. **Claude executes item by item, committing per logical chunk.** Small commits with conventional messages (`feat(scope): …`, `fix(scope): …`) — cheap to revert.
5. **Verification gate runs** — per Pattern C. Screenshot, reload, smoke check. Claude reports "done" only after the gate passes.
6. **Promote any lesson** — if the review surfaced a new convention, add one line to Pattern D. If a new helper landed, add it to Pattern B.

Step 6 is the drift defence. Without it, the CLAUDE.md and the code diverge, and the app rots. With it, the CLAUDE.md *is* the collaboration memory and stays usable six months in.

---

## 6. Early Hardening

Guardrails are cheap on day 1 and painful to retrofit. Before the app has any real data in it, decide:

- **Unsafe-HTML rule.** If the app renders any dynamic content, ban raw string interpolation into HTML in CLAUDE.md from the start. Retrofitting this once there are fifty `innerHTML` calls is a multi-day sweep.
- **Secret handling.** If the app ever calls an external API, decide where the key lives (env var, local file outside the repo) and write that in CLAUDE.md. Never let the first version hardcode a key "temporarily".
- **Input validation at the boundary.** Any data read from disk, URL, or user input gets validated once at the boundary. Claude will follow this if it is stated; it will not invent it unprompted.
- **Data backup.** If the app writes to local files that matter to you, decide a backup strategy (git commit of the data, periodic copy) before the first real entry goes in.

Four lines in CLAUDE.md. Five minutes on day 1. Many hours not spent later.

---

## 7. Anti-Patterns

- **CLAUDE.md drift.** Rules in CLAUDE.md that no longer match the code. Fix by running [`tasks/audit-claude-md.md`](./tasks/audit-claude-md.md) every few weeks, or whenever the app has had a big reshuffle.
- **Inventing new helpers.** Claude writes a sixth formatter because it didn't check Pattern B. Fix by making the helper index the first thing Claude sees in CLAUDE.md, and by calling out the miss in review so it costs something.
- **Declaring "done" before verification.** The most common false-done. Fix by making Pattern C specific enough that "done" requires a tool call with visible output, not a self-report.
- **Broad permission grants.** "Allow all Bash" because a prompt was annoying. Fix by auditing `.claude/settings.local.json` back down to the real list the moment the session ends.
- **Skipping the plan for "small" changes.** The change is never as small as it looks. A 60-second plan avoids a 20-minute cleanup.
- **Treating this as a product.** The moment you think about sharing it, adding a second user, or deploying it — stop. This guide no longer applies. You are now in real-engineering territory.

---

## 8. When to Stop Using This Guide

Helper apps have a ceiling. Signs you have hit it:

- More than one person uses it.
- It stores data you would be upset to lose and you have no backup story.
- You are adding auth, multi-tenancy, or a server.
- The CLAUDE.md has grown past a page and the patterns here no longer fit.

At that point, the tool has graduated. It needs proper architecture, proper tests, proper deployment — and a collaboration model that goes beyond CLAUDE.md guardrails. Cluide does not cover that. Move the project to your normal engineering setup and keep only the patterns from this guide that still pay rent.

---

## 9. Checklist

Before you consider the helper-app CLAUDE.md "done":

- [ ] One-line invariant written and linked to its canonical helper.
- [ ] Helper index with 5–10 entries, each with a file path.
- [ ] Verification gates per class of change, each tied to a specific MCP tool call.
- [ ] Convention list populated with the rules you have already caught yourself breaking.
- [ ] `.claude/settings.local.json` lists only the tools the workflow actually uses.
- [ ] `plans/` folder exists with the template for a feature plan.
- [ ] Early-hardening rules (HTML escaping, secrets, validation, backup) written *before* the code needs them.

If each of those is in place, the app can survive six months of vibe-coding without rotting.
