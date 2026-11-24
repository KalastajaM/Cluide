# App Rules: Starting Rules for an App Built Over Many Sessions

> Rules for an app that other people will use, built with an assistant doing most of the typing. They come from the fixes three such projects kept making: a household planner built over about 40 sessions (the case in [Guide 36](../../36_MULTI_SESSION_APPS.md)), a budgeting app with over a thousand commits and an 819-line policy file, and a document archive taken to a public release. The fixes include the same correction given page by page, review findings that were one-line fixes early and risky ones late, AI features that drifted, and private material that reached a public history. Written down on day one, each rule replaces a class of later prompts.

## What is in this folder

| File | Goes to | Loaded |
|---|---|---|
| `APP_POLICY.md` | Pasted into the project's `AGENTS.md` (or `CLAUDE.md` in a Claude-only project) as an *App rules* section | Every session, so it stays short |
| `APP_REFERENCE.md` | Copied to `docs/APP_REFERENCE.md` | On demand: `APP_POLICY.md` names when to read each section |

This split follows the reference-companion pattern in [Guide 01](../../01_PROJECT_INSTRUCTIONS.md#when-the-policy-cannot-be-short-the-reference-companion): the short rules load every session, the tables and reasons only when the work needs them.

## How to use it

1. **Before the first screen,** copy both files into the new project and fill in every `[bracket]`: the language files, the token file, the icon set, the three widths, the ports, the check commands.
2. **Delete what does not apply.** A rule for an app without AI, a local server or a second language is noise in every session. An app with one user and one device is a helper app: use [Guide 22](../../22_HELPER_APPS.md) instead.
3. **Build the guard tests the rules name** (inline styles, language-file parity, layering, interface/API parity) before the second screen, so the rules are enforced rather than remembered.
4. **Build the shared components** the *Interface* rules list before the second page.
5. **Schedule the validation passes** in `APP_REFERENCE.md` §5 as milestones in the plan.
6. **Add a line when a correction repeats.** If you give the same instruction a second time, it belongs in `APP_POLICY.md` or, better, in a component or a test.

## What these rules are not

They are not a style guide or a stack choice. They name what to decide and what to enforce, not which framework, colours or fonts to use. Bracketed values are examples from these projects; replace them with yours.

They are also not complete. They cover what went wrong in three projects. Treat them as a floor, and add the rules your own projects earn.

## Giving this to an assistant

> "We are starting [app]. Copy `templates/APP_RULES/APP_POLICY.md` into our `AGENTS.md` and `APP_REFERENCE.md` into `docs/`. Interview me to fill in every bracket and to decide which rules do not apply, then list the guard tests and shared components the rules require, as the first milestone."
