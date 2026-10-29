# Dual-Platform Projects: One Project, More Than One Assistant

> A project worked on from two assistants has two sets of entry points and one set of intentions. Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`, and a Claude project and a ChatGPT project each have instruction fields that the other never sees. Left alone, this produces three failures:
> - two instruction files that start as copies and drift into disagreement;
> - a skill or hook that one assistant honours and the other has never heard of;
> - a scheduled job that runs twice because it was set up on both sides.
>
> This guide is the structure that prevents all three: one shared policy, thin native adapters, a written list of what does not translate, and a check on each surface before anyone calls it working.

> **Companion guides:**
> - [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md) owns the instruction layers this guide doubles, and [Guide 01](./01_PROJECT_INSTRUCTIONS.md) owns shared policy content and native entry points.
> - [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) says where shared and local files live.
> - [Guide 23](./23_MULTI_PROJECT_SETUPS.md)'s single-owner rule is applied here across platforms instead of across projects.
> - [Guide 11](./11_GIT_INTEGRATION.md) owns the branches, worktrees and commits that carry a handoff. [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) owns shared state and collision-free scheduling.
> - [Guide 12](./12_SECURITY.md) §3 and [Guide 32](./32_ACTION_AUTHORITY.md) are why a prose rule is not an enforcement mechanism.
> - [Guide 26](./26_CONTEXT_SCOPING.md) owns the fresh session the verification needs, and [Guide 31](./31_BEHAVIOUR_TESTS.md) turns that check into a case.
> - [Guide 34](./34_IMPORTING_FROM_OTHER_ASSISTANTS.md) is the one-way move, which this guide is not.
>
> `tasks/setup-dual-platform.md` runs this guide against a project.

---

## 1. What This Guide Is, and Is Not

This guide is about coexistence, not migration. [Guide 34](./34_IMPORTING_FROM_OTHER_ASSISTANTS.md) moves a setup from one assistant to another and leaves the old one behind. This guide keeps one project running on both, indefinitely. Indefinitely is what makes it hard: every rule change must reach both assistants, and a release on either side can break the arrangement.

Two rules keep the guide durable, and they are the rules for anyone editing it later:

- **Principle before product.** Every section states what must hold whichever assistant is working, and names product mechanisms only as examples.
- **Product facts live in §9 and nowhere else.** That covers which file a product discovers, whether it resolves imports, its size limits, and where its skills and schedules live. Each row carries its source and the date it was checked. A sentence elsewhere that would need re-verifying after a vendor release is in the wrong section.

In this guide, *dual-platform* means at least one Claude surface plus at least one surface from another vendor: OpenAI, or since October 2026 Google, whose routes in §9 are documented but not yet tested. A project on three vendors follows the same structure, with every per-platform rule applied once more. Claude Code plus Cowork is two surfaces of one platform: they can use the same authored policy through different entry points, and [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers that split. A *surface* is the product a session actually runs in: Claude Code, conversational Claude or Cowork, a ChatGPT project, Codex, Antigravity, Jules, or a Gemini app notebook. File access, tools and loaders depend on the surface, not on which model answers.

---

## 2. When a Second Platform Is Worth It

A second platform has a running cost. Every supported surface is one more place a rule change has to be verified, every capability used on one side needs an answer on the other, and every switch between assistants needs a handoff. It is worth that cost when:

- different people on the project use different assistants, and the project cannot choose for them;
- the work genuinely splits by surface, such as repository work in Codex and scheduled file tasks in Cowork, and both sides must follow the same rules;
- you want the project to survive a change of assistant, and are prepared to verify both sides rather than assume them.

It is not worth it when the second assistant is consulted occasionally for one kind of question. Give that assistant the shared policy as a source and stop there. A project that claims two platforms and verifies only one is worse than a project that honestly supports one.

---

## 3. Four Homes

Everything a dual-platform project holds belongs in exactly one of four homes.

| Home | Holds | Lives in | Shared |
|---|---|---|---|
| **Shared policy** | Purpose, conventions, file hygiene, approval rules, hard safety rules, workflow gates: anything true whichever assistant is working | One instruction file at the project root (`AGENTS.md` in the pattern in §4) | Yes. Versioned, one copy |
| **Native adapter** | The line that loads the shared policy, a fallback telling the session to read it where loading does not happen, and nothing else it can avoid | Each product's own entry file (`CLAUDE.md` for Claude) | Versioned, read by one product |
| **Platform-specific rules** | How one product's mechanism is used: a hook, a skill location, a sandbox setting, a scheduler | A section of the adapter or of the setup page labelled with the product name. Never unlabelled in the shared file | Versioned, labelled |
| **Platform-local state** | Credentials, app settings, native memory, scheduler registrations, connector grants, session history | Wherever each product keeps them | **No.** The setup page records where each one lives; nothing in the repository synchronises them |

Two tests sort anything that is not obvious:

- **For a rule:** if the other assistant followed this sentence literally, would it do the right thing? If yes, it is shared policy. If it only works with a mechanism the other assistant lacks, it goes in the adapter or the platform-specific section.
- **For state:** would copying a file move it? A memory entry, a registered schedule or an OAuth grant does not move when anything is copied. It is platform-local, and treating it as shared is how a job runs twice or a permission gets assumed.

[Guide 23](./23_MULTI_PROJECT_SETUPS.md)'s single-owner principle applies across the four homes just as it applies across projects: every rule has one home. The one sanctioned duplicate is still [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)'s, a hard safety rule restated in an app-side instructions field. The difference is that there is now one such field per platform.

---

## 4. One Shared File, Thin Adapters

The pattern: the shared policy is `AGENTS.md` at the project root, and `CLAUDE.md` is an adapter that imports it.

The shared file uses the name Codex discovers natively. Current Claude Code can also read `AGENTS.md` itself, but not on every version or deployment (§9), so the adapter stays the recommendation. It works on every Claude Code version and deployment; it gives Claude-only rules a place beside the import; Claude Code's documentation says keeping the import never makes it read `AGENTS.md` twice; and under the default setting a `CLAUDE.md` or `CLAUDE.local.md` in the tree switches native `AGENTS.md` reading off anyway. Codex documents no import syntax, so the reverse arrangement would leave Codex holding a pointer and no rules (§9). A symlink from `CLAUDE.md` to `AGENTS.md` also works for Claude Code, but it leaves no room for the fallback line or for Claude-only rules.

A minimal adapter:

```markdown
# <Project> — Claude Entry Point

@AGENTS.md

`AGENTS.md` is the shared project policy. If this interface does not resolve imports,
read `AGENTS.md` in full before working. Do not restate shared rules here.

## Claude-only
<only rules that depend on a Claude mechanism: hooks, skill allowlists, scheduled-task conventions>
```

Cluide's own root `CLAUDE.md` is this adapter in practice.

Four rules for the pair:

- **Move rules; never copy them.** A rule enters the shared file in the same edit that removes it from the adapter. Two copies agree only on the day they are made.
- **The fallback line is load-bearing.** Not every Claude surface resolves imports; a conversational session reading a folder may treat `@AGENTS.md` as plain text. The explicit "read `AGENTS.md`" sentence is what reaches those sessions. It supplements the import rather than replacing it: in Claude Code a prose pointer alone is followed only if Claude decides to open the file (§9). One observed session, not documented behaviour and not a fresh-session check (§8): in a Cowork cloud task linked to a local folder on 2026-09-21, the folder's `CLAUDE.md` reached the session but its `@AGENTS.md` import was not expanded, and `AGENTS.md` had to be read explicitly.
- **Respect the smaller limit.** Every product loads the shared file, so the strictest project-instruction size limit in §9 caps it. Long reference material goes into files the policy points to, using [Guide 01](./01_PROJECT_INSTRUCTIONS.md)'s companion-file pattern.
- **Keep product names out of the shared file.** No model name, tool name or path that belongs to one product. The shared file says "use the configured model", and routing lives in the adapter. Never translate a model name from one vendor into a guessed equivalent from another.

Nested instruction files get the same treatment one folder at a time. The products discover nested files differently (§9), so check that a nested rule reaches each of them before relying on it.

---

## 5. App-Side Layers on Each Platform

[Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)'s layers exist on every platform, but not in the same form. Each project product has an instructions field that reaches the session before any file is read. No product versions those fields. A conversational project may not read the repository at all, and may work from uploaded copies instead.

- **Bootstrap each side separately.** Each platform's instructions field gets its own short bootstrap:
  - read the shared policy first;
  - report which sources are missing before making changes;
  - distinguish the products' capabilities, and use only the tools this session has;
  - say whether changes were saved to the project or only drafted in chat.

  One text can often serve both (Cluide's `PLATFORM_SETUP.md` gives one), but it is pasted and mirrored once per platform.
- **Local projects read folders, and only one is discovered.** A ChatGPT local project works on folders on the computer rather than uploads, but instruction files are discovered only from its primary folder (§9). Make the repository the primary folder, and treat discovery in a ChatGPT Work chat as untested until a fresh-session check (§8) has run there.
- **Uploaded sources are copies.** A project that works from uploaded files sees the revision that was uploaded, not the repository. A merge does not refresh it. Record the uploaded revision (a commit hash or a date) in the mirror, and replace the uploads explicitly after every policy change.
- **Uploaded skills are copies too.** The Gemini app (documented, untested) creates a skill from an uploaded `SKILL.md` folder (§9). Like an uploaded source, it does not follow the repository: record the revision you uploaded and replace it after a change.
- **Mirror per platform.** Keep Guide 25's mirror block, with one entry per platform and a last-verified date on each. A mirror that says "fields verified" without naming a platform is the ambiguity this rule removes.
- **Record only what was applied.** Proposed field text is a draft, not configuration. It enters the mirror after someone has pasted it and confirmed that.

---

## 6. Capabilities Do Not Translate

Compare the capability a workflow needs, not just the feature name: reusable instructions, lifecycle actions, access controls, context selection, delegation, tool connections and scheduling. They are not the same mechanisms, and they rarely share a file format or a location. Record each capability the project relies on in a capability-gap list on the setup page, with one of three outcomes:

| Outcome | Means | Records |
|---|---|---|
| **Verified counterpart** | The other product has a mechanism that does the same job, and it has been checked as the project uses it | Its name, official source, date, and the check that was run |
| **No verified counterpart** | No counterpart has been established for this project | What the other side does instead: a prose rule, nothing, or the work stays on the first platform |
| **Untested** | A counterpart may exist, but nobody has checked | Who will check it, or that nobody will. It is a valid state, but it is not the same as verified |

The list prevents two errors.

**Path conversion.** Copying the contents of `.claude/` into the other product's configuration directory, or inventing an ignore file for it, produces files in a format nothing reads. The other product's configuration has its own keys (§9). Skills are the near-exception: both products read `SKILL.md` folders, but from different locations and with different optional fields. Even a skill that would load on both is listed as untested until it has run on both. Every counterpart comes from the other product's documentation, never from analogy.

**Prose standing in for enforcement.** A hook that blocks a command, or an allowlist that removes a tool, is structural ([Guide 12](./12_SECURITY.md) §3). The same sentence in the shared policy is only a request. When one side enforces something and the other only instructs, the list says so. [Guide 32](./32_ACTION_AUTHORITY.md)'s classes then decide whether the unenforced side may do that work at all. And `.claudeignore` is context hygiene rather than a security boundary ([Guide 12](./12_SECURITY.md) §7), on either platform.

---

## 7. State, Schedules and Handoffs

**Native memory stays native.** Each product's memory holds what that product learned, and neither reads the other's. Anything both assistants must know goes into files: `.auto-memory/`, profile files, or the shared policy ([Guide 04](./04_MEMORY_AND_PROFILE.md)). OpenAI itself keeps two stores that do not share: ChatGPT memory, and a separate local Codex memory in `~/.codex/memories/`, off by default ([Codex memories](https://learn.chatgpt.com/codex/customization/memories)). Treat native memory as a per-platform cache. When one memory genuinely needs to cross over, [Guide 34](./34_IMPORTING_FROM_OTHER_ASSISTANTS.md) is the tool.

**One owner per recurring job.** Every scheduled or recurring job has exactly one owning platform, a timezone, and a stable identity (its name and the task file it runs), recorded in an owner table on the setup page. Copying a `TASK.md` does not move a registration. To move a job:

1. Inventory the old registration, pause it, and confirm no run is in flight. Preserve the last accepted state and stable deduplication key.
2. Configure the new registration inactive, or test the new task manually with outbound effects disabled. Verify inputs, output and state once before recurring execution.
3. Delete the old registration, then activate the new owner; never leave both schedules active. Pause is a transfer step, not the final retirement state ([Guide 33](./33_RETIRING_AND_LEAVING.md)).
4. Record the new owner, registration identity, timezone, source revision, date and controlled-run result in the owner table. If verification fails, keep the new owner inactive and explicitly restore the previous one only after checking that no run overlaps.

Find a job registered on both platforms by inventory, not by noticing duplicate output. Run deduplication inside the task itself ([Guide 06](./06_TASK_EFFICIENCY_GUIDE.md)) is the backstop, not the control.

**One writer, or separate branches.** When both assistants can write the same files, pick one of two arrangements: one named writer per set of files at a time, or each assistant working on its own branch or worktree, reconciled through git ([Guide 11](./11_GIT_INTEGRATION.md)). The failure is two sessions writing to one checkout at once. Which product each session runs has nothing to do with it.

**A handoff record.** When work switches assistants partway through, pass on:

- the branch and last commit;
- the changed files;
- the verification that was run, and its result;
- outstanding work;
- anything drafted but not saved.

No assistant has another's session history, so the record is the only memory of the handoff. Keep it in the commit message or pull request, or wherever [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) puts working notes.

---

## 8. Verifying Each Surface

A structure that looks right on disk is not verified until a session on each surface has loaded it. For each supported surface:

1. Start a fresh session: one that has not seen the setup work ([Guide 26](./26_CONTEXT_SCOPING.md)).
2. Ask a check question whose answer depends on the shared policy having loaded. For example: which instruction files did you load, where do working notes go, what must you never do, and which parts of this project are platform-specific?
3. Compare the answer against an expected answer written before the session started.
4. Record the result for that surface as **verified** (date, plus the product version if one is shown), **failed** (what differed), or **untested**.

Untested is an honest result. "Works on both" while one surface is untested is not. Re-run the check after every change to the shared policy, the adapter or an app-side field, and after every refresh of uploaded sources. A passing check verifies that surface on that day, not the product in general. [Guide 31](./31_BEHAVIOUR_TESTS.md) turns the check into a case with graders, run on each surface with results recorded per product. `tasks/audit-dual-platform.md` covers the mechanical half of this on a shorter cycle — do the referenced files, sibling folders and scheduler rows still resolve — without repeating the full fresh-session interview; run it more often than the check above, and run the full check whenever it finds something structural.

---

## 9. Platform Facts

Checked on 2026-09-21 against official documentation, except: the Claude cells of the *Native instruction file*, *Size limit* and *Seeing what loaded* rows, which were re-checked on 2026-10-02; the Claude cell of the *Direct API parameters* row and the Cowork *Conversational projects* cell, re-checked on 2026-10-29; and the Claude *Nested files* cell, last checked on 2026-09-14. A row marked *re-verify* could not be confirmed cleanly on the date that applies to it, so read the source before relying on its detail. This table is the reference for dated platform facts; examples elsewhere depend on these facts and must be reviewed when a row changes. `tasks/setup-dual-platform.md` Step 0 re-checks the rows a project relies on each time it runs, and `tasks/review-platform-changes.md` re-checks the whole section.

| Fact | Claude | OpenAI | Sources |
|---|---|---|---|
| Native instruction file | Claude Code reads `CLAUDE.md` at the managed, user, project and local levels. Since v2.1.277 it also reads `AGENTS.md` natively. Under the default `/config` "Project instructions" value, `claude-md-or-agents-md`, it does so only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it; a user `~/.claude/CLAUDE.md`, managed `CLAUDE.md` or `.claude/rules/` does not suppress it. The other values are `claude-md-and-agents-md`, `claude-md` and `managed-only`. Native reading is not available before v2.1.277, with the built-in `agents-md` plugin disabled, or, in some cases, in the first session after upgrading from v2.1.276 or earlier; before v2.1.281 it was also unavailable on Amazon Bedrock, Vertex, Foundry, LLM gateways and with telemetry disabled. There, import it from `CLAUDE.md`. Claude Code also reads `.claude/AGENTS.md`, but not `AGENTS.local.md`, `AGENTS.override.md` or anything under `.agents/`: a Codex override does not reach Claude. On an existing `CLAUDE.md` containing `@AGENTS.md`: "Keeping the import never makes Claude read AGENTS.md twice". A `CLAUDE.md` that only asks in words to read `AGENTS.md` works only if Claude decides to open the file | Codex reads `AGENTS.md`, or `AGENTS.override.md` in its place where one exists: first in Codex home, then in each directory from the project root down to the working directory. Fallback filenames are configurable | [Claude Code memory](https://code.claude.com/docs/en/memory), [AGENTS.md section](https://code.claude.com/docs/en/memory#agents-md); [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Nested files | Ancestor-directory files load before the working directory's file; `CLAUDE.local.md` loads after `CLAUDE.md` at each level | Files are concatenated from the root down, and files closer to the working directory take precedence | As above |
| Imports | `@path`, relative to the importing file, recursing up to four hops | No import syntax documented. Treat `AGENTS.md` as having to carry its own text. This is inferred from the documentation's silence and an open feature request, not stated by the vendor | As above; [openai/codex#28739](https://github.com/openai/codex/issues/28739) |
| Size limit | A `CLAUDE.md` of up to 4 MiB loads in full; a larger one is skipped. Subdirectory `CLAUDE.md` files and path-scoped rules have a smaller per-file limit, and since v2.1.309 a nested file over it loads only its start. Claude Code warns at startup and in `/status` when one instruction file is over the recommended length, and at session start when files that are each within that length add up past a combined limit; the page gives no figure for either. [Guide 01](./01_PROJECT_INSTRUCTIONS.md)'s length target applies | Combined project instructions stop at `project_doc_max_bytes`, 32 KiB by default | [Claude Code memory](https://code.claude.com/docs/en/memory#my-claude-md-is-too-large); [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Seeing what loaded | `/memory` lists the instruction files; `/context` shows what actually loaded. An imported `AGENTS.md` shows there as usual. Since v2.1.280, `/memory` lists a natively read `AGENTS.md` as well; on earlier versions neither `/memory` nor `/context` listed it, so ask Claude what its project instructions say. An interactive session also prints "no CLAUDE.md found; AGENTS.md loaded: <path>". `InstructionsLoaded` hooks fire for it only when it is imported | Not checked. Use the fresh-session question (§8) | [Claude Code memory](https://code.claude.com/docs/en/memory#agents-md) |
| Configuration | `.claude/settings.json` and hooks ([Guide 12](./12_SECURITY.md)) | `~/.codex/config.toml`, with project overrides in `.codex/config.toml`, which Codex loads only when you trust the project. MCP servers go under `mcp_servers`. `sandbox_mode` is `read-only`, `workspace-write` or `danger-full-access`. `approval_policy` is `on-request`, `never` or a `granular` table (`sandbox_approval`, `rules`, `mcp_elicitations`, `request_permissions`, `skill_approval`); `untrusted` and `on-failure` are no longer supported. `default_permissions` takes `:read-only`, `:workspace`, `:danger-full-access` or a custom `[permissions.<name>]` profile, and should not be combined with `sandbox_mode` or `[sandbox_workspace_write]`. `approvals_reviewer` is `user` (default) or `auto_review`. The desktop app, CLI and IDE also offer permission modes: Ask for approval, Approve for me, Full access, or Custom via `config.toml` | [Codex config reference](https://learn.chatgpt.com/docs/config-file/config-reference); [permission modes](https://learn.chatgpt.com/codex/permission-modes) |
| Skills | `SKILL.md` folders in `.claude/skills/` (project) or `~/.claude/skills/` (personal). Anthropic describes the format as the Agent Skills open standard, with Claude-specific extensions. Since v2.1.275, skills and plugins enabled on the claude.ai account sync into Claude Code sessions signed in with it (opt out with `syncClaudeAiSkills: false` or `syncClaudeAiPlugins: false`); synced skills are downloaded from the account, not read from local files | `SKILL.md` folders with required `name` and `description` frontmatter; repository skills in `.agents/skills`. User skills are in `~/.agents/skills`; optional OpenAI metadata lives in `agents/openai.yaml`. In ChatGPT, type `@` to select a skill; in Codex CLI or IDE, run `/skills` or type `$`. Description limits differ: the Agent Skills specification caps `description` at 1024 characters, Claude Code truncates description plus `when_to_use` at 1,536 characters in its skill listing, and Codex gives the initial skill list at most 2% of the context window (8,000 characters when unknown), shortening descriptions first. Stay within 1024 so one `SKILL.md` installs everywhere | [Claude Code skills](https://code.claude.com/docs/en/skills); [Claude Code changelog](https://code.claude.com/docs/en/changelog) (v2.1.275); [Codex skills](https://learn.chatgpt.com/docs/build-skills); [Agent Skills specification](https://agentskills.io/specification) |
| Scheduled runs | Cowork scheduled tasks ([Guide 06](./06_TASK_EFFICIENCY_GUIDE.md)) | The ChatGPT feature is Scheduled tasks (sidebar page: Scheduled). Scheduled tasks run in ChatGPT; Codex automations run in Codex. A task created in a project cannot access uploaded files or files stored in that project. In the desktop app, keep the computer on and the app running when a task needs local files; runs happen in the project directory or an isolated worktree, unattended with the default sandbox settings and `approval_policy = "never"` where organisational policy permits. On web and mobile, eligible plans can also run tasks from supported app events (Plus or higher). Scheduled tasks can use plugins and skills. Whether the CLI or IDE offer schedule management is not documented | [ChatGPT scheduled tasks (help)](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt); [Codex automations](https://learn.chatgpt.com/codex/automations) |
| Conversational projects | Cowork projects hold a description, instructions, local folders, links, linked claude.ai knowledge and project memory. New Cowork projects are saved to the Claude account and open on other devices; the desktop app also moves folder-based projects into the account, while their folders and files stay on the computer. On Team and Enterprise without the unified experience, a folder-based project stays on that computer. The Cowork docs projects page still says projects are not synced; the support article is the later source. The page checked does not say a folder's `CLAUDE.md` loads as the project's instructions, so bootstrap it ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md), pattern 1) | Cloud ChatGPT projects hold files, instructions, connected apps and project-only memory, without direct laptop-folder access. Record source revision and refresh uploaded policy explicitly; do not infer native `AGENTS.md` loading from an upload. Local projects are a separate access mode for files on the computer: in the ChatGPT desktop app, Edit project → Add folder attaches more folders, and Make primary picks one. New chats start in the primary folder, and Codex discovers `AGENTS.md`, skills and `config.toml` only there; secondary folders can be searched, read and edited but are not discovered. Remote projects support one folder. Discovery is documented for Codex; whether a ChatGPT Work chat in the same local project gets it is untested | [Cowork projects](https://claude.com/docs/cowork/guide/projects); [Organize tasks with projects](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork); [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans); [ChatGPT projects (cloud)](https://help.openai.com/en/articles/10169521-projects-in-chatgpt); [Projects, including local projects](https://learn.chatgpt.com/codex/projects) |
| Direct API parameters | Anthropic Messages is post-prefill and adaptive-thinking on current models. Assistant message prefilling returns a 400 on Sonnet 4.6, Opus 4.6 and later — use structured outputs (`output_config.format`) or a system-prompt instruction instead. Manual `budget_tokens` thinking is deprecated on Opus 4.6 and Sonnet 4.6 and returns a 400 on Sonnet 5, Opus 4.7 and later — use `thinking: {type: "adaptive"}` with `output_config.effort`. Haiku 4.5 and pre-4.6 models still take `budget_tokens`. Opus 5.5 (`claude-opus-5-5`) goes further: thinking is always on, so `thinking: {type: "disabled"}` or a manual budget returns a 400, as does forced tool use (`tool_choice` `any` or a named tool), and its default effort is `medium` where Opus 5's was `high`. Sonnet 5.5 (`claude-sonnet-5-5`) also rejects forced tool use and returns a 400 for a non-default `temperature`, `top_p` or `top_k`; its lowest thinking setting is `between_tools`, which turns off up-front thinking at `high` effort or below. On the Claude API and Google Cloud neither accepts the `computer_20251124` computer-use tool. On both, the short notes written between tool calls arrive as `thinking` blocks, not `text`, so an application streaming text goes quiet between tool calls. Haiku 5.5 (`claude-haiku-5-5`, 2026-10-07) is not a drop-in for Haiku 4.5: manual `budget_tokens`, `temperature`, `top_p`, `top_k`, assistant prefill and `computer_20250124` can each return a 400. API version 2026-10-21 removes `temperature`, `top_p` and `top_k` for every model (a 400 if sent) and shipped with new major SDK versions that send it by default and carry breaking changes, so upgrading the SDK moves client code to it: re-test before upgrading | Not checked on this date. The OpenAI Responses API has its own parameters; neither thinking controls nor prefill behaviour transfer by renaming fields | [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide), [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [What's new in Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5), [Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [API release notes](https://platform.claude.com/docs/en/release-notes/overview), [deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) |


### Google (Gemini): the third platform

Checked on 2026-10-15 against Google's official documentation. No Google surface has had a fresh-session check (§8), so every row here is documented, not verified; a project relying on one records its own check. Google's coding tools read the same `AGENTS.md` and `.agents/skills/` that Codex reads, which is why the shared-policy pattern carries over unchanged. The differences that matter are the limits and which surface reads which file.

| Fact | Google | Sources |
|---|---|---|
| Surfaces | **Antigravity** (app, CLI `agy`, IDE, IDE extensions, SDK) is the repository agent. **Jules** is a cloud coding agent that works on a GitHub repository and is labelled experimental. The **Gemini app** (web, mobile, desktop) is the conversational surface. **Gemini CLI** stopped serving Google AI Pro, Ultra and free individual users on 18 June 2026 and remains available through paid Gemini and Gemini Enterprise Agent Platform API keys and Gemini Code Assist Standard or Enterprise licences: treat it as a legacy surface | [Gemini CLI to Antigravity CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli); [Jules](https://jules.google/docs/) |
| Native instruction file | Antigravity reads `AGENTS.md` or `GEMINI.md` natively in any directory, plus `.agents/rules/*.md`. Which wins when `AGENTS.md` and `GEMINI.md` sit in the same directory is not documented, so keep only `AGENTS.md`. Jules reads `AGENTS.md` from the repository root; nested files are not documented. Gemini CLI reads `GEMINI.md` unless `context.fileName` in its `settings.json` lists `AGENTS.md` | [Antigravity rules](https://antigravity.google/docs/rules); [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md) |
| Nested files | Antigravity walks up from the file being read or edited to the workspace root and loads rules at each level. Rules accumulate, and the more specific directory wins a conflict | [Antigravity rules](https://antigravity.google/docs/rules) |
| Imports | Antigravity inlines `@[label](path)` before its size checks. Its rules page says a bare `@filename` is only rewritten to a path, while its app changelog (v2.11.0, 2026-08-26) says `@path/to/file` now inlines: *re-verify*. Gemini CLI imports `@file.md`. Import rules differ per product and Codex has none, so the shared file carries its own text rather than depending on an import | As above; [Antigravity changelog](https://antigravity.google/docs/changelog) |
| Size limit | Antigravity truncates any single rule file over 24,000 bytes, measured after includes are expanded. All always-on and global rules share a 20,000-token budget; over it, the largest files are demoted to pointers read on demand | [Antigravity rules](https://antigravity.google/docs/rules) |
| Seeing what loaded | Gemini CLI: `/memory show`. Antigravity: not documented on the rules page; ask the session which rule files it loaded | As above |
| Configuration | Antigravity keeps MCP servers in `~/.gemini/config/mcp_config.json` and `.agents/mcp_config.json`, hooks in `~/.gemini/config/hooks.json` and `.agents/hooks.json`, and resolves permission rules Deny > Ask > Allow. Unconfigured MCP tools run in Ask mode | [MCP](https://antigravity.google/docs/mcp); [hooks](https://antigravity.google/docs/hooks); [permissions](https://antigravity.google/docs/permissions) |
| Skills | Antigravity: a folder holding `SKILL.md`, `description` required, `name` optional (defaults to the folder name). Workspace skills live in `.agents/skills/`, the same path Codex uses. The global path differs by surface: `~/.gemini/config/skills/` for the app and IDE, `~/.gemini/antigravity-cli/skills/` for the CLI. The Gemini app replaces Gems with skills from November 2026 on personal accounts, and creates one from an uploaded `SKILL.md` file or a folder or `.zip` holding one; skills are not yet available on work or school accounts | [Antigravity skills](https://antigravity.google/docs/skills); [Gems to skills](https://support.google.com/gemini/answer/18560919); [Create skills](https://support.google.com/gemini/answer/17094296) |
| Scheduled runs | Gemini app: up to 10 active scheduled actions, with Keep Activity on. Jules: scheduled tasks (daily, weekly); its scheduled-tasks page says a task cannot be edited, while its 2026-01-26 changelog entry adds Edit, Pause and Resume, so *re-verify* | [Gemini schedules](https://support.google.com/gemini/answer/16316416); [Jules scheduled tasks](https://jules.google/docs/scheduled-tasks/); [Jules changelog](https://jules.google/docs/changelog/) |
| Conversational projects | Gemini app notebooks hold custom instructions and uploaded files and sync with NotebookLM; no access to folders on the computer is documented. Treat a notebook like a cloud ChatGPT project: bootstrap the policy in its instructions, upload it, record the revision. Launched in April 2026 for Google AI Ultra, Pro and Plus subscribers on the web, with mobile and free users to follow; not available on Workspace, Education or under-18 accounts | [Notebooks in Gemini](https://blog.google/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/) |
| Models and plans | Gemini 4 Argon is in the Gemini app on Google AI Pro and Ultra, but in Antigravity only on Ultra and Enterprise, and not in the Antigravity IDE on any plan. On Pro, Antigravity offers Gemini 3.8 Flash and, on a non-trial subscription, Claude Sonnet 5.5 and Opus 5.5. Jules is included in Google AI Pro, for personal (@gmail.com) accounts, with higher limits than the free tier | [Gemini release notes](https://gemini.google/release-notes/); [Antigravity models](https://antigravity.google/docs/models); [Jules limits](https://jules.google/docs/usage-limits/) |
| Direct API | The Gemini API's managed Antigravity agent loads `.agents/AGENTS.md` (not a root `AGENTS.md`) and discovers `.agents/skills/`; `system_instruction` and `AGENTS.md` are additive. `gemini-4-argon` is not on the free tier; at the Standard tier it costs $2/$10 per million input/output tokens through 30 November 2026, then $4/$20 | [Managed agents](https://ai.google.dev/gemini-api/docs/custom-agents); [pricing](https://ai.google.dev/gemini-api/docs/pricing) |

---

### Counterparts and gaps to carry into setup

Documentation checks below are dated 2026-09-21. They establish a native route, not a live verification of this project. “No verified counterpart” means that equivalence has not been established, not that a vendor can never offer it.

| Need | Claude route | ChatGPT / Codex route | Gap or fallback |
|---|---|---|---|
| Shared rules | Claude Code reads `AGENTS.md` natively or through the adapter import; app projects bootstrap it | Codex reads `AGENTS.md` (in a local project, from the primary folder only); cloud projects use instructions plus accessible policy | No documented Codex `@` import equivalent. Put required rules in the native instruction chain or require an explicit source read. |
| Lifecycle actions and tool checks | Claude Code hooks in native settings | Codex `hooks.json` or inline `[hooks]` in active config layers; review and trust changed hooks | Same event names do not prove identical coverage. Hosted tools and subsequent `write_stdin` input are outside Codex's pre-tool check described by the source. Keep sandbox and grants as separate controls. |
| Browser and desktop operation | Claude in Chrome; Cowork computer use | OpenAI browser and Computer Use on supported surfaces | An API browser or cloud session is not control of local apps. If tools are absent, use a connector/export for data or a screenshot for review; report interactive verification as untested. |
| Scripted behaviour tests | `claude -p` | `codex exec`; source-only chats can run fixture prompts manually | Native loader, skill and tool behaviour must be checked separately. A CLI test does not verify the chat product. |
| Context exclusion | `.claudeignore` only where supported; explicit scoped reads | Explicit source selection and native access controls | No verified direct `.claudeignore` counterpart. Neither a prose exclusion nor a Git ignore pattern is a read-denial mechanism. |
| Account-native state | Claude memory, registrations and artifact grants | ChatGPT memory, separate local Codex memory, registrations and native delivery tools | No shared native store or automatic grant transfer. Shared files, explicit refresh and one scheduler owner are the portable route. The full Claude artifact lifecycle has no verified equivalent here. |
| Model routing and skill extensions | Claude model identifiers, native frontmatter and agent definitions | Available OpenAI models and supported skill/agent metadata | No model-name or optional-field equivalence. Keep the configured model unless an authorized supported alternative is selected. |

Sources for the additional routes: [Codex hooks](https://learn.chatgpt.com/docs/hooks), [OpenAI browser](https://learn.chatgpt.com/docs/browser), [OpenAI Computer Use](https://learn.chatgpt.com/docs/computer-use), [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode). Instruction, skill, memory/source and schedule sources are in the table above. Confirm availability in the target account before installation.

**Google routes for the same needs** (checked 2026-10-15, documented, untested):

| Need | Google route | Gap or fallback |
|---|---|---|
| Shared rules | Antigravity and Jules read `AGENTS.md` natively; a Gemini app notebook bootstraps it in its instructions | No `AGENTS.override.md` equivalent is documented. A `GEMINI.md` beside `AGENTS.md` has undocumented precedence, so keep only `AGENTS.md` |
| Lifecycle actions and tool checks | Antigravity `hooks.json` and permission rules | Same event names do not prove identical coverage; test the tool paths the project uses |
| Skills | `.agents/skills/` in Antigravity, the same folder Codex reads | Global paths differ per Antigravity surface; a Gemini app skill is an uploaded copy |
| Schedules | Gemini app scheduled actions; Jules scheduled tasks | One scheduler owner per job (§7); Jules editing behaviour needs re-verifying |
| Model routing | The configured Gemini model | No model-name equivalence with Claude or OpenAI tiers |

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| Two full instruction files kept "in sync" by hand | They agree on the day they are copied and diverge at the next edit made in a hurry |
| Converting `.claude/` paths into lookalike paths for the other product | Produces configuration nothing reads, and a setup page that claims support it does not have |
| A hook's guarantee restated as a sentence in the shared policy | One side enforces, the other is asked. The difference is invisible until the unenforced side acts |
| Registering the same scheduled job on both platforms | Duplicate runs, duplicate outputs, and sometimes duplicate outbound actions |
| Treating native memory as shared | Each assistant acts on facts the other never learned, and nothing records which |
| Translating model names between vendors | A guessed identifier fails at best and routes work to the wrong tier at worst |
| Uploading the policy to a conversational project and never replacing it | The project follows last month's rules while the repository has moved on |
| Declaring a surface supported without a fresh-session check | The one surface nobody checked is where the loader, the limit or the fallback fails |
| Product facts scattered through the prose | Every vendor release makes some sentence wrong, and nothing says which one |

---

## Checklist

- [ ] Surfaces the project supports are named; "dual-platform" means one Claude surface plus at least one OpenAI or Google surface
- [ ] Shared policy in one root file; each rule has one home among the four
- [ ] Claude adapter imports the shared file, carries the read fallback, restates nothing
- [ ] Shared file within the smaller product's size limit, and free of product-specific model, tool and path names
- [ ] Each platform's instructions field bootstraps to the shared policy; mirrored per platform with dates
- [ ] Uploaded-source revision recorded where a project works from copies
- [ ] Capability-gap list: every one-platform mechanism is verified, has no counterpart, or is untested
- [ ] Native memory, credentials, settings and registrations kept platform-local, with their locations on the setup page
- [ ] Owner table: every recurring job has one platform, a timezone and a stable identity
- [ ] One writer per file set, or separate branches or worktrees; a handoff record at every switch
- [ ] Fresh-session check recorded per surface as verified, failed or untested
- [ ] Every §9 fact the project relies on re-checked, with its source and date

---

## Giving This to an Assistant

> "This project should work from both Claude and ChatGPT or Codex. Read Guide 35, then run `tasks/setup-dual-platform.md`: inventory what binds the project to one platform, sort every rule into the four homes, list what does not translate, and show me the plan before changing anything. Mark any platform fact you could not verify, and any surface you could not test."
