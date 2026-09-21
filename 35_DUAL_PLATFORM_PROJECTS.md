# Dual-Platform Projects: One Project, Claude and ChatGPT

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

In this guide, *dual-platform* means at least one Claude surface and at least one OpenAI surface. Claude Code plus Cowork is two surfaces of one platform: they can use the same authored policy through different entry points, and [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers that split. A *surface* is the product a session actually runs in: Claude Code, conversational Claude or Cowork, a ChatGPT project, or Codex. File access, tools and loaders depend on the surface, not on which model answers.

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
- **Respect the smaller limit.** Both products load the shared file, so the stricter project-instruction size limit in §9 caps it. Long reference material goes into files the policy points to, using [Guide 01](./01_PROJECT_INSTRUCTIONS.md)'s companion-file pattern.
- **Keep product names out of the shared file.** No model name, tool name or path that belongs to one product. The shared file says "use the configured model", and routing lives in the adapter. Never translate a Claude model name into a guessed OpenAI one, or the reverse.

Nested instruction files get the same treatment one folder at a time. The two products discover nested files differently (§9), so check that a nested rule reaches both before relying on it.

---

## 5. App-Side Layers on Each Platform

[Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)'s layers exist on both platforms, but not in the same form. Each project product has an instructions field that reaches the session before any file is read. Neither product versions those fields. A conversational project may not read the repository at all, and may work from uploaded copies instead.

- **Bootstrap each side separately.** Each platform's instructions field gets its own short bootstrap:
  - read the shared policy first;
  - report which sources are missing before making changes;
  - distinguish the products' capabilities, and use only the tools this session has;
  - say whether changes were saved to the project or only drafted in chat.

  One text can often serve both (Cluide's `PLATFORM_SETUP.md` gives one), but it is pasted twice and mirrored twice.
- **Local projects read folders, and only one is discovered.** A ChatGPT local project works on folders on the computer rather than uploads, but instruction files are discovered only from its primary folder (§9). Make the repository the primary folder, and treat discovery in a ChatGPT Work chat as untested until a fresh-session check (§8) has run there.
- **Uploaded sources are copies.** A project that works from uploaded files sees the revision that was uploaded, not the repository. A merge does not refresh it. Record the uploaded revision (a commit hash or a date) in the mirror, and replace the uploads explicitly after every policy change.
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

Neither assistant has the other's session history, so the record is the only memory of the handoff. Keep it in the commit message or pull request, or wherever [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) puts working notes.

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

Checked on 2026-09-21 against official documentation, except the Direct API row, which carries its own date, and the Claude *Nested files* and *Size limit* cells and the Cowork *Conversational projects* cell, which were last checked on 2026-09-14. A row marked *re-verify* could not be confirmed cleanly on that date, so read the source before relying on its detail. This table is the reference for dated platform facts; examples elsewhere depend on these facts and must be reviewed when a row changes. `tasks/setup-dual-platform.md` Step 0 re-checks the rows a project relies on each time it runs, and `tasks/review-platform-changes.md` re-checks the whole section.

| Fact | Claude | OpenAI | Sources |
|---|---|---|---|
| Native instruction file | Claude Code reads `CLAUDE.md` at the managed, user, project and local levels. Since v2.1.277 it also reads `AGENTS.md` natively. Under the default `/config` "Project instructions" value, `claude-md-or-agents-md`, it does so only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it; a user `~/.claude/CLAUDE.md`, managed `CLAUDE.md` or `.claude/rules/` does not suppress it. The other values are `claude-md-and-agents-md`, `claude-md` and `managed-only`. Native reading is not available before v2.1.277, in the first session after install or upgrade, on Amazon Bedrock, Vertex or Foundry, with telemetry disabled, or with `disableAllHooks` / `allowManagedHooksOnly`; there, import it from `CLAUDE.md`. On an existing `CLAUDE.md` containing `@AGENTS.md`: "Keeping the import never makes Claude read AGENTS.md twice". A `CLAUDE.md` that only asks in words to read `AGENTS.md` works only if Claude decides to open the file | Codex reads `AGENTS.md`, or `AGENTS.override.md` in its place where one exists: first in Codex home, then in each directory from the project root down to the working directory. Fallback filenames are configurable | [Claude Code memory](https://code.claude.com/docs/en/memory), [AGENTS.md section](https://code.claude.com/docs/en/memory#agents-md); [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Nested files | Ancestor-directory files load before the working directory's file; `CLAUDE.local.md` loads after `CLAUDE.md` at each level | Files are concatenated from the root down, and files closer to the working directory take precedence | As above |
| Imports | `@path`, relative to the importing file, recursing up to four hops | No import syntax documented. Treat `AGENTS.md` as having to carry its own text. This is inferred from the documentation's silence and an open feature request, not stated by the vendor | As above; [openai/codex#28739](https://github.com/openai/codex/issues/28739) |
| Size limit | No combined limit stated on the page checked; [Guide 01](./01_PROJECT_INSTRUCTIONS.md)'s length target applies | Combined project instructions stop at `project_doc_max_bytes`, 32 KiB by default | [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Seeing what loaded | `/memory` lists the instruction files; `/context` shows what actually loaded. An imported `AGENTS.md` shows there as usual. A natively read `AGENTS.md` is not listed in `/memory` or the `/context` memory files list: look for the line "no CLAUDE.md found; AGENTS.md loaded: <path>", or ask. `InstructionsLoaded` hooks fire for it only when it is imported | Not checked. Use the fresh-session question (§8) | [Claude Code memory](https://code.claude.com/docs/en/memory#agents-md) |
| Configuration | `.claude/settings.json` and hooks ([Guide 12](./12_SECURITY.md)) | `~/.codex/config.toml`, with project overrides in `.codex/config.toml`, which Codex loads only when you trust the project. MCP servers go under `mcp_servers`. `sandbox_mode` is `read-only`, `workspace-write` or `danger-full-access`. `approval_policy` is `on-request`, `never` or a `granular` table (`sandbox_approval`, `rules`, `mcp_elicitations`, `request_permissions`, `skill_approval`); `untrusted` and `on-failure` are no longer supported. `default_permissions` takes `:read-only`, `:workspace`, `:danger-full-access` or a custom `[permissions.<name>]` profile, and should not be combined with `sandbox_mode` or `[sandbox_workspace_write]`. `approvals_reviewer` is `user` (default) or `auto_review`. The desktop app, CLI and IDE also offer permission modes: Ask for approval, Approve for me, Full access, or Custom via `config.toml` | [Codex config reference](https://learn.chatgpt.com/docs/config-file/config-reference); [permission modes](https://learn.chatgpt.com/codex/permission-modes) |
| Skills | `SKILL.md` folders in `.claude/skills/` (project) or `~/.claude/skills/` (personal). Anthropic describes the format as the Agent Skills open standard, with Claude-specific extensions. Since v2.1.275, skills and plugins enabled on the claude.ai account sync into Claude Code sessions signed in with it (opt out with `syncClaudeAiSkills: false` or `syncClaudeAiPlugins: false`); synced skills are downloaded from the account, not read from local files | `SKILL.md` folders with required `name` and `description` frontmatter; repository skills in `.agents/skills`. User skills are in `~/.agents/skills`; optional OpenAI metadata lives in `agents/openai.yaml`. In ChatGPT, type `@` to select a skill; in Codex CLI or IDE, run `/skills` or type `$`. Description limits differ: the Agent Skills specification caps `description` at 1024 characters, Claude Code truncates description plus `when_to_use` at 1,536 characters in its skill listing, and Codex gives the initial skill list at most 2% of the context window (8,000 characters when unknown), shortening descriptions first. Stay within 1024 so one `SKILL.md` installs everywhere | [Claude Code skills](https://code.claude.com/docs/en/skills); [Claude Code changelog](https://code.claude.com/docs/en/changelog) (v2.1.275); [Codex skills](https://learn.chatgpt.com/docs/build-skills); [Agent Skills specification](https://agentskills.io/specification) |
| Scheduled runs | Cowork scheduled tasks ([Guide 06](./06_TASK_EFFICIENCY_GUIDE.md)) | The ChatGPT feature is Scheduled tasks (sidebar page: Scheduled). Scheduled tasks run in ChatGPT; Codex automations run in Codex. A task created in a project cannot access uploaded files or files stored in that project. In the desktop app, keep the computer on and the app running when a task needs local files; runs happen in the project directory or an isolated worktree, unattended with the default sandbox settings and `approval_policy = "never"` where organisational policy permits. On web and mobile, eligible plans can also run tasks from supported app events (Plus or higher). Scheduled tasks can use plugins and skills. Whether the CLI or IDE offer schedule management is not documented | [ChatGPT scheduled tasks (help)](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt); [Codex automations](https://learn.chatgpt.com/codex/automations) |
| Conversational projects | Cowork projects hold a description, instructions, local folders, links, linked claude.ai knowledge and project memory, and live on one computer. The page checked does not say a folder's `CLAUDE.md` loads as the project's instructions, so bootstrap it ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md), pattern 1) | Cloud ChatGPT projects hold files, instructions, connected apps and project-only memory, without direct laptop-folder access. Record source revision and refresh uploaded policy explicitly; do not infer native `AGENTS.md` loading from an upload. Local projects are a separate access mode for files on the computer: in the ChatGPT desktop app, Edit project → Add folder attaches more folders, and Make primary picks one. New chats start in the primary folder, and Codex discovers `AGENTS.md`, skills and `config.toml` only there; secondary folders can be searched, read and edited but are not discovered. Remote projects support one folder. Discovery is documented for Codex; whether a ChatGPT Work chat in the same local project gets it is untested | [Cowork projects](https://claude.com/docs/cowork/guide/projects); [ChatGPT projects (cloud)](https://help.openai.com/en/articles/10169521-projects-in-chatgpt); [Projects, including local projects](https://learn.chatgpt.com/codex/projects) |
| Direct API parameters (checked 2026-09-16) | Anthropic Messages is post-prefill and adaptive-thinking on current models. Assistant message prefilling returns a 400 on Sonnet 4.6, Opus 4.6 and later — use structured outputs (`output_config.format`) or a system-prompt instruction instead. Manual `budget_tokens` thinking is deprecated on Opus 4.6 and Sonnet 4.6 and returns a 400 on Sonnet 5, Opus 4.7 and later — use `thinking: {type: "adaptive"}` with `output_config.effort`. Haiku 4.5 and pre-4.6 models still take `budget_tokens` | Not checked on this date. The OpenAI Responses API has its own parameters; neither thinking controls nor prefill behaviour transfer by renaming fields | [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide), [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |

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

- [ ] Surfaces the project supports are named; "dual-platform" means one Claude and one OpenAI surface at least
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
