# Dual-Platform Projects: One Project, Claude and ChatGPT

> A project worked on from two assistants has two sets of entry points and one set of intentions. Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`, and a Claude project and a ChatGPT project each have instruction fields that the other never sees. Left alone, this produces three failures:
> - two instruction files that start as copies and drift into disagreement;
> - a skill or hook that one assistant honours and the other has never heard of;
> - a scheduled job that runs twice because it was set up on both sides.
>
> This guide is the structure that prevents all three: one shared policy, thin native adapters, a written list of what does not translate, and a check on each surface before anyone calls it working.

> **Companion guides:**
> - [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md) owns the instruction layers this guide doubles, and [Guide 01](./01_CLAUDE_MD.md) owns the body of the Claude adapter.
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

In this guide, *dual-platform* means at least one Claude surface and at least one OpenAI surface. Claude Code plus Cowork is two surfaces of one platform: they share `CLAUDE.md`, and [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers that split. A *surface* is the product a session actually runs in: Claude Code, conversational Claude or Cowork, a ChatGPT project, or Codex. File access, tools and loaders depend on the surface, not on which model answers.

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

The shared file uses the name Codex discovers natively. Claude Code does not read `AGENTS.md` itself, but it resolves imports, and its own documentation recommends exactly this adapter. Codex documents no import syntax, so the reverse arrangement would leave Codex holding a pointer and no rules (§9). A symlink from `CLAUDE.md` to `AGENTS.md` also works for Claude Code, but it leaves no room for the fallback line or for Claude-only rules.

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
- **The fallback line is load-bearing.** Not every Claude surface resolves imports; a conversational session reading a folder may treat `@AGENTS.md` as plain text. The explicit "read `AGENTS.md`" sentence is what reaches those sessions.
- **Respect the smaller limit.** Both products load the shared file, so the stricter project-instruction size limit in §9 caps it. Long reference material goes into files the policy points to, using [Guide 01](./01_CLAUDE_MD.md)'s companion-file pattern.
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
- **Uploaded sources are copies.** A project that works from uploaded files sees the revision that was uploaded, not the repository. A merge does not refresh it. Record the uploaded revision (a commit hash or a date) in the mirror, and replace the uploads explicitly after every policy change.
- **Mirror per platform.** Keep Guide 25's mirror block, with one entry per platform and a last-verified date on each. A mirror that says "fields verified" without naming a platform is the ambiguity this rule removes.
- **Record only what was applied.** Proposed field text is a draft, not configuration. It enters the mirror after someone has pasted it and confirmed that.

---

## 6. Capabilities Do Not Translate

Both vendors have mechanisms in most of the same categories: skills, hooks, permission controls, ignore rules, subagents, MCP connections, schedulers. They are not the same mechanisms, and they rarely share a file format or a location. Record each capability the project relies on in a capability-gap list on the setup page, with one of three outcomes:

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

**Native memory stays native.** Each product's memory holds what that product learned, and neither reads the other's. Anything both assistants must know goes into files: `.auto-memory/`, profile files, or the shared policy ([Guide 04](./04_MEMORY_AND_PROFILE.md)). Treat native memory as a per-platform cache. When one memory genuinely needs to cross over, [Guide 34](./34_IMPORTING_FROM_OTHER_ASSISTANTS.md) is the tool.

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

Untested is an honest result. "Works on both" while one surface is untested is not. Re-run the check after every change to the shared policy, the adapter or an app-side field, and after every refresh of uploaded sources. A passing check verifies that surface on that day, not the product in general. [Guide 31](./31_BEHAVIOUR_TESTS.md) turns the check into a case with graders, run on each surface with results recorded per product.

---

## 9. Platform Facts

Checked on 2026-09-14 against official documentation. A row marked *re-verify* could not be confirmed cleanly on that date, so read the source before relying on its detail. This is the only section of the guide that goes stale. `tasks/setup-dual-platform.md` Step 0 re-checks the rows a project relies on each time it runs, and `tasks/review-platform-changes.md` re-checks the whole section.

| Fact | Claude | OpenAI | Sources |
|---|---|---|---|
| Native instruction file | Claude Code reads `CLAUDE.md` at the managed, user, project and local levels. It does not read `AGENTS.md`; its documentation recommends a `CLAUDE.md` that imports `AGENTS.md`, or a symlink | Codex reads `AGENTS.md`, or `AGENTS.override.md` in its place where one exists: first in Codex home, then in each directory from the project root down to the working directory. Fallback filenames are configurable | [Claude Code memory](https://code.claude.com/docs/en/memory); [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Nested files | Ancestor-directory files load before the working directory's file; `CLAUDE.local.md` loads after `CLAUDE.md` at each level | Files are concatenated from the root down, and files closer to the working directory take precedence | As above |
| Imports | `@path`, relative to the importing file, recursing up to four hops | No import syntax documented. Treat `AGENTS.md` as having to carry its own text. This is inferred from the documentation's silence and an open feature request, not stated by the vendor | As above; [openai/codex#28739](https://github.com/openai/codex/issues/28739) |
| Size limit | No combined limit stated on the page checked; [Guide 01](./01_CLAUDE_MD.md)'s length target applies | Combined project instructions stop at `project_doc_max_bytes`, 32 KiB by default | [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Seeing what loaded | `/memory` lists the instruction files; `/context` shows what actually loaded | Not checked. Use the fresh-session question (§8) | [Claude Code memory](https://code.claude.com/docs/en/memory) |
| Configuration | `.claude/settings.json` and hooks ([Guide 12](./12_SECURITY.md)) | `~/.codex/config.toml`, with project overrides in `.codex/config.toml`. MCP servers go under `mcp_servers`. `sandbox_mode` is `read-only`, `workspace-write` or `danger-full-access`, alongside the supported `approval_policy` settings; `on-request` is the interactive example and `untrusted` is retired | [Codex config reference](https://learn.chatgpt.com/docs/config-file/config-reference); [approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) |
| Skills | `SKILL.md` folders in `.claude/skills/` (project) or `~/.claude/skills/` (personal). Anthropic describes the format as the Agent Skills open standard, with Claude-specific extensions | `SKILL.md` folders with required `name` and `description` frontmatter; repository skills in `.agents/skills`. User skills are in `~/.agents/skills`; optional OpenAI metadata lives in `agents/openai.yaml` | [Claude Code skills](https://code.claude.com/docs/en/skills); [Codex skills](https://learn.chatgpt.com/docs/build-skills) |
| Scheduled runs | Cowork scheduled tasks ([Guide 06](./06_TASK_EFFICIENCY_GUIDE.md)) | OpenAI Scheduled supports local desktop and web execution. Local-file tasks need the computer on and app running; web tasks use uploaded/connected inputs. CLI/IDE prepare workflows but do not provide the Scheduled management interface | [OpenAI scheduled tasks](https://learn.chatgpt.com/docs/automations) |
| Conversational projects | Cowork projects hold a description, instructions, local folders, links, linked claude.ai knowledge and project memory, and live on one computer. The page checked does not say a folder's `CLAUDE.md` loads as the project's instructions, so bootstrap it ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md), pattern 1) | ChatGPT source projects hold instructions and uploaded/connected context, without direct laptop-folder access. Local projects are a separate access mode. Record source revision and refresh uploaded policy explicitly; do not infer native `AGENTS.md` loading from an upload | [Cowork projects](https://claude.com/docs/cowork/guide/projects); [Projects and sources](https://learn.chatgpt.com/docs/projects) |

---

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
