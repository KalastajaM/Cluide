# Working on Cluide with Claude, ChatGPT and Gemini

This page configures **this documentation project** for each platform. Google's surfaces were added on 2026-10-15 from documentation only; none has had a fresh-session check yet. The guide now separates shared principles from surface-specific routes. Existing Claude hooks and agent definitions remain explicitly Claude-specific. Verify the relevant route in your own runtime before relying on it.

## Shared instructions, separate entry points

`AGENTS.md` owns the repository rules, guide map, file hygiene, and merge gate. Edit shared policy there. `CLAUDE.md` imports that file for Claude Code and includes an explicit read fallback for interfaces that do not resolve imports. No shared rule should need two edits.

| Surface | Setup |
|---|---|
| Codex working in the repository | Open this folder as the project, or start the CLI from its root. Codex discovers the root `AGENTS.md`; check for user-level or nested overrides if behavior differs. |
| Claude Code working in the repository | Open this folder. The root `CLAUDE.md` imports `AGENTS.md`. Current Claude Code can also read `AGENTS.md` natively, but only where no `CLAUDE.md` exists and not on every version or deployment, so the import is what loads it here (Guide 35 §9). |
| ChatGPT project — local project (filesystem access) | Open this folder as the local project's **primary** folder (Edit project → Add folder, then Make primary). Codex discovers `AGENTS.md`, skills and `config.toml` only from the primary folder; secondary folders are readable but not discovered. That discovery is documented for Codex; whether a ChatGPT Work chat in the same local project gets it is untested, so keep the bootstrap below in project instructions. |
| ChatGPT project — uploaded or connected sources | No native `AGENTS.md` read. Supply `AGENTS.md`, `00_INDEX.md`, and the guides needed for the work as sources. Put the bootstrap below in project instructions. A GitHub merge does not refresh uploaded copies. |
| Antigravity (Google) working in the repository | Open this folder as the workspace. Antigravity reads the root `AGENTS.md` natively; do not add a `GEMINI.md` beside it: their precedence in one directory is not documented. Workspace skills would go in `.agents/skills/`. |
| Jules (Google) | Connect the GitHub repository. Jules reads `AGENTS.md` from the repository root and works on its own clone in a virtual machine. Review whatever it produces through the merge gate in `AGENTS.md`, like any other contributor's change. |
| Gemini app notebook | Upload `AGENTS.md`, `00_INDEX.md` and the guides needed as notebook sources and put the bootstrap below in the notebook's instructions. An upload does not follow the repository; replace it after a merge. |
| Conversational Claude / Cowork | Make the repository files available through the supported project or folder interface and use the bootstrap below. Explicitly read `AGENTS.md` when file imports are not supported. |

OpenAI documents [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [ChatGPT project sources and instructions](https://learn.chatgpt.com/docs/projects) and [projects, including local projects](https://learn.chatgpt.com/codex/projects). Anthropic documents [CLAUDE.md imports and native AGENTS.md reading](https://code.claude.com/docs/en/memory#agents-md). Checked 2026-09-21. Google documents [Antigravity rule files](https://antigravity.google/docs/rules), [Jules and AGENTS.md](https://jules.google/docs/) and [Notebooks in Gemini](https://blog.google/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/), checked 2026-10-15; the dated facts are in Guide 35 §9. File access and tools depend on the selected surface, not merely on which model answers.

## Delegation

OpenAI delegation: retain the configured model unless the user requests a supported alternative. Follow the host's delegation rules.

Google delegation (Antigravity, Jules, Gemini app): the same rule. Retain the configured Gemini model unless the user picks a supported alternative, and never map a Claude tier onto a Gemini model name. Where Antigravity offers Claude models on the user's plan, that choice is the host's model setting, not a Claude dispatch parameter. (Claude-specific delegation routing is in `CLAUDE.md`.)

## Capability Gaps

| Capability | Claude route | OpenAI/Codex route | Google route | Status |
|---|---|---|---|---|
| Permission allowlisting | `.claude/settings.local.json` (`permissions.allow`) | Codex `sandbox_mode` / `approval_policy` in `.codex/config.toml` | Antigravity permission rules, evaluated Deny > Ask > Allow | No verified counterpart — different mechanisms, not checked side by side |
| Security-review hooks | `skills/security-review/references/hook-*.sh` (Claude Code hooks) | `skills/security-review/references/openai-review.md` (separate documented route) | None written; Antigravity has `hooks.json`, but the Claude hook scripts are not a Google route | Verified for Claude and OpenAI — two intentionally separate routes, not a translation of one into the other; no Google route yet |
| Skill loading | `SKILL.md` folders under `.claude/skills/` or project `skills/` | `SKILL.md` folders under `.agents/skills`, optional `agents/openai.yaml` metadata | `SKILL.md` folders under `.agents/skills` (Antigravity, the same folder Codex reads); Gemini app skills by upload | Untested — not yet installed or run on a Codex, ChatGPT or Google surface |
| Model routing | Claude model identifiers (`CLAUDE.md`) | Configured OpenAI model, no name translation (this file) | Configured Gemini model, no name translation (this file) | Verified — kept as separate, unlabelled-model prose rules per vendor |
| Scheduled tasks | Cowork scheduled tasks | ChatGPT scheduled tasks / Codex automations | Gemini app scheduled actions / Jules scheduled tasks | N/A — see Recurring Jobs below |
| Assistant-triggered mid-session folder access | `device_request_folder_access` (Cowork device bridge) — verified 2026-09-21, no task restart needed; see [Guide 23 §"Requesting the mount, on demand"](./23_MULTI_PROJECT_SETUPS.md#requesting-the-mount-on-demand) | Local project "Add folder" is a person-driven UI action | Not documented | Partially verified — Claude route confirmed working; ChatGPT/Codex assistant-triggered equivalent untested; no Google equivalent documented |

## Recurring Jobs

Cluide (the guide repository) has no recurring or scheduled jobs of its own. The scheduler-owner table in Guide 35 §7 applies to *projects built using* these patterns, not to this repository.

## App-side bootstrap

Suggested description:

> Cluide: guides, tasks, skills, and templates for persistent AI assistants, covering Claude, ChatGPT and Gemini, including dual-platform project design.

Suggested project instructions for any conversational platform (a Claude project, a ChatGPT project or a Gemini notebook):

> Before working on Cluide, read the supplied AGENTS.md as the shared repository policy, then the relevant guides from 00_INDEX.md. If those sources are unavailable, report what is missing before making repository changes. Distinguish Claude, ChatGPT, Codex and Gemini capabilities; use only tools available in this session. Treat templates as reference material until asked to instantiate them. Report whether changes were saved to the repository or only drafted in chat.

These texts are ready to apply; their presence here does not configure an app. Record the platform, date, and actual field values after applying them. Retain historical mirrors until the corresponding live fields are verified.

## Fresh-Session Check Results

| Surface | Result | Notes |
|---|---|---|
| Claude Code | Untested | Not yet run against current `AGENTS.md` / `CLAUDE.md` |
| Conversational Claude / Cowork | Untested | A conversational session with filesystem access but no native project binding is not a valid check (Guide 35 §8) |
| ChatGPT project (local) | Untested | Not yet run |
| ChatGPT project (uploaded/connected sources) | Untested | Uploaded-source revision not recorded; unclear whether ever bootstrapped |
| Codex | Untested | Not yet run |
| Antigravity | Untested | Not yet run |
| Jules | Untested | Not yet run |
| Gemini app notebook | Untested | Not yet run |

## Check a new session

Ask: “Which project instruction files did you load? Where should review notes go, what is the merge gate, and which parts of the guide are still Claude-specific?”

The answer should identify `AGENTS.md`, `development/`, the shared merge gate, and which native mechanisms remain platform-specific. In Claude Code, check `/memory` to confirm the imported file. Claude Code v2.1.280 and later also list a natively read `AGENTS.md` in `/memory`; on earlier versions, ask Claude what its project instructions say. For an uploaded-source project, also check the source revision; replace stale uploads explicitly. A successful answer verifies that session, not every product or future session.

## Keeping the project dual-platform

Keep shared rules in `AGENTS.md` and platform adapters small. Preserve the public guide numbers and task filenames. Keep platform-native settings, credentials, memory, and scheduled jobs separate; a shared Markdown file does not synchronize them. When switching assistants, hand off the branch, commit, changed files, verification results, and outstanding work. Use separate branches/worktrees for simultaneous changes and reconcile through Git.

When extending the guide, explain the common principle first, then give separately verified platform steps. Identify unsupported or untested capabilities explicitly. Update dependent tasks, templates, skill bundles, and audit criteria with each complete content change.
