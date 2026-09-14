# Working on Cluide with Claude and ChatGPT

This page configures **this documentation project** for both platforms. The guide now separates shared principles from surface-specific routes. Existing Claude hooks and agent definitions remain explicitly Claude-specific. Verify the relevant route in your own runtime before relying on it.

## Shared instructions, separate entry points

`AGENTS.md` owns the repository rules, guide map, file hygiene, and merge gate. Edit shared policy there. `CLAUDE.md` imports that file for Claude Code and includes an explicit read fallback for interfaces that do not resolve imports. No shared rule should need two edits.

| Surface | Setup |
|---|---|
| Codex working in the repository | Open this folder as the project, or start the CLI from its root. Codex discovers the root `AGENTS.md`; check for user-level or nested overrides if behavior differs. |
| Claude Code working in the repository | Open this folder. The root `CLAUDE.md` imports `AGENTS.md`. |
| ChatGPT project using uploaded or connected sources | Supply `AGENTS.md`, `00_INDEX.md`, and the guides needed for the work as sources. Put the bootstrap below in project instructions. A GitHub merge does not refresh uploaded copies. |
| Conversational Claude / Cowork | Make the repository files available through the supported project or folder interface and use the bootstrap below. Explicitly read `AGENTS.md` when file imports are not supported. |

OpenAI documents [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [ChatGPT project sources and instructions](https://learn.chatgpt.com/docs/projects). Anthropic documents [CLAUDE.md imports](https://code.claude.com/docs/en/memory). Checked 2026-09-13. File access and tools depend on the selected surface, not merely on which model answers.

## App-side bootstrap

Suggested description:

> Cluide: guides, tasks, skills, and templates for persistent AI assistants, covering Claude and ChatGPT, including dual-platform project design.

Suggested project instructions for either conversational platform:

> Before working on Cluide, read the supplied AGENTS.md as the shared repository policy, then the relevant guides from 00_INDEX.md. If those sources are unavailable, report what is missing before making repository changes. Distinguish Claude, ChatGPT, and Codex capabilities; use only tools available in this session. Treat templates as reference material until asked to instantiate them. Report whether changes were saved to the repository or only drafted in chat.

These texts are ready to apply; their presence here does not configure an app. Record the platform, date, and actual field values after applying them. Retain historical mirrors until the corresponding live fields are verified.

## Check a new session

Ask: “Which project instruction files did you load? Where should review notes go, what is the merge gate, and which parts of the guide are still Claude-specific?”

The answer should identify `AGENTS.md`, `development/`, the shared merge gate, and which native mechanisms remain platform-specific. In Claude Code, check `/memory` to confirm the imported file. For an uploaded-source project, also check the source revision; replace stale uploads explicitly. A successful answer verifies that session, not every product or future session.

## Keeping the project dual-platform

Keep shared rules in `AGENTS.md` and platform adapters small. Preserve the public guide numbers and task filenames. Keep platform-native settings, credentials, memory, and scheduled jobs separate; a shared Markdown file does not synchronize them. When switching assistants, hand off the branch, commit, changed files, verification results, and outstanding work. Use separate branches/worktrees for simultaneous changes and reconcile through Git.

When extending the guide, explain the common principle first, then give separately verified platform steps. Identify unsupported or untested capabilities explicitly. Update dependent tasks, templates, skill bundles, and audit criteria with each complete content change.
