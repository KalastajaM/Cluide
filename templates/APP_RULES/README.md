# App Rules: Building an App Over Many Sessions

> An order of work and a set of starting rules for an app that other people will use, built with an assistant doing most of the typing. They come from the fixes four such projects kept making: a household planner built over about 40 sessions (the case in [Guide 36](../../36_MULTI_SESSION_APPS.md)), a budgeting app with over a thousand commits and an 819-line policy file, a document archive taken to a public release, and a regulatory checklist tool built in one 30-message chat. Most of the last-mile tweaking in those projects came from two causes. Work was done out of order: code before a design, a design before the spec, a design system extracted after the pages had drifted. And the same correction was given page by page instead of once, as a rule. The build sequence addresses the first, the rules the second.

## What is in this folder

| File | Goes to | Loaded |
|---|---|---|
| `APP_POLICY.md` | Pasted into the project's `AGENTS.md` (or `CLAUDE.md` in a Claude-only project) as an *App rules* section | Every session, so it stays short |
| `APP_REFERENCE.md` | Copied to `docs/APP_REFERENCE.md` | On demand: §1 at each phase change, the other sections before the work they name |

This split follows the reference-companion pattern in [Guide 01](../../01_PROJECT_INSTRUCTIONS.md#when-the-policy-cannot-be-short-the-reference-companion): the short rules load every session, the tables and reasons only when the work needs them.

## How to use it

The steps follow the phases in `APP_REFERENCE.md` §1.

1. **Before anything else,** copy both files into the new project, fill in every `[bracket]`, and delete what does not apply. A rule for an app without AI, a local server or a second language is noise in every session. An app with one user and one device is a helper app: use [Guide 22](../../22_HELPER_APPS.md) instead.
2. **Spec (phase 0).** Have the spec reviewed critically. Write the input-output map, the choice model for each question, and the data lifecycle (save, delete, export, import, share, report, print). Answer the review's questions in one list.
3. **Design (phase 1).** Get mockups of every main screen and its hard cases, choose one direction, and test the handoff by building one screen from it.
4. **Foundation (phase 2).** Build the tokens, the shared components the *Interface* rules list, and the guard tests the rules name (inline styles, language-file parity, layering, interface/API parity), before the second screen.
5. **Hosting, if the app will serve other people.** Settle the first list in §9 of the reference during the spec, make the deployment its own milestone with the second list, and pass the third before the first outside user.
6. **Milestones (phase 3).** One per session. Send feedback as one numbered list per round, and have the session sort it into one-offs and patterns before fixing. Schedule the validation passes in §6.
7. **Add a line when a correction repeats.** If you give the same instruction a second time, it belongs in `APP_POLICY.md` or, better, in a component or a test.

## What these rules are not

They are not a style guide or a stack choice. They name what to decide and what to enforce, not which framework, colours or fonts to use. Bracketed values are examples from these projects; replace them with yours.

They are also not complete. They cover what went wrong in four projects. Treat them as a floor, and add the rules your own projects earn.

## Giving this to an assistant

> "We are starting [app]. Copy `templates/APP_RULES/APP_POLICY.md` into our `AGENTS.md` and `APP_REFERENCE.md` into `docs/`. Interview me to fill in every bracket and to decide which rules do not apply. Then run phase 0 from §1 of the reference: review my spec critically, and draft the input-output map, the choice model and the data lifecycle, with your questions in one list. Do not start on design or code until I have answered them."
