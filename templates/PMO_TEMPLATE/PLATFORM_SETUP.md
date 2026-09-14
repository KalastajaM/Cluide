# Platform setup

Choose the actual surface before setup: Claude Code, Cowork, Codex with repository
access, or ChatGPT with project sources. Files copied here configure no accounts or jobs.

## Source loading

- **Claude Code:** keep `CLAUDE.md` beside `AGENTS.md`; the adapter imports the shared policy.
- **Cowork:** connect the intended folder and paste the bootstrap below into project instructions;
  verify access to that folder rather than assuming imports are resolved.
- **Codex:** open this repository as the workspace. Start at its root to load root `AGENTS.md`.
  For nested tasks, start in the task folder or explicitly read its `AGENTS.md` before work.
- **ChatGPT:** create a project, add `AGENTS.md`, this page, the file map and required task/source
  files as project sources, then paste the bootstrap into project instructions. Keep relative
  folder paths in a source manifest when uploaded filenames are ambiguous. Supply required
  nested `AGENTS.md` files explicitly. An upload is a snapshot, not a repository connection.

Bootstrap to customize and paste:

> Read the supplied `AGENTS.md` in full first, then the file map and instructions for the
> requested task. State which required sources are missing and the source revision you can
> actually see. Use only available tools. Pause dependent work if source freshness cannot
> be established. Follow the project's hardest safety rule: [paste exact rule]. State whether
> outputs were saved to the connected project or are drafts for me to apply.

## Applied settings and sources

Keep one row per surface; drafts remain untested until someone applies and checks them.
Replace uploaded sources after policy/source changes and record the new revision here.

| Surface | Folder or uploaded manifest | Source revision | Instructions applied/date | Fresh-session result |
|---|---|---|---|---|
| Claude Code | [folder] | [commit/date] | adapter, untested | untested |
| Cowork | [folder] | [commit/date] | draft, not applied | untested |
| Codex | [workspace] | [commit/date] | shared file, untested | untested |
| ChatGPT | [source manifest] | [commit/date uploaded] | draft, not applied | untested |

Mirror the exact applied instructions and any description separately for each selected surface.
Do not assume every app offers the same fields. Keep native memory, credentials, connector grants,
app settings and session history in each product's own storage; do not commit or copy them.
Shared profile files are ordinary project data, not native memory synchronization.

## Tools and dispatch

Inventory required tools before the first run. Record capability, surface, available tool,
permission/enforcement, official source/date and test evidence. Use **verified**, **no verified
counterpart**, or **untested**. A prose rule is not an enforced permission boundary.
If a required connector or script runtime is missing, stop that step and identify the missing
capability; offer a supplied export or a draft only if it preserves the task's requirements.
Never invent connector names, model identifiers or cross-vendor configuration paths.

**Claude-only optional routing:** if the installed dispatch skill and host allow delegation,
configure its sonnet/opus/haiku tiers there. The agent starter pack is Claude Code only.
**OpenAI routing:** retain the configured model and follow the host's available delegation
controls. No Claude-to-OpenAI model mapping is supplied.

## Recurring jobs and concurrent work

Copying a task does not register or transfer it. Complete this table before enabling any job.
Keep native registration IDs in a local, ignored operations record if sensitive.

| Stable job ID | Task file | Active owning surface | IANA timezone | Native registration ID/location | Duplicate guard | Last verification |
|---|---|---|---|---|---|---|
| [project/job] | [path] | none yet | [Area/City] | not registered | [atomic lock + completed run key] | untested |

Use a run key of stable job ID plus scheduled time slot. Before state/output writes, verify the
owner and acquire a shared atomic lock, then check the completed-run ledger. An existing lock or
completed key means stop without duplicating work. A timestamp check alone is not a lock.
If separate machines cannot share an atomic claim, allow only the owning runner to execute and
verify old registrations are removed before activation. Do not pretend this template enforces a
lock: implement and test the chosen mechanism before unattended use.

To migrate, inventory both schedulers; stop the old owner, prepare the new job without enabling
duplicate execution, test a supervised run, delete the old registration, record the transfer and
activate the new owner. On failure keep both inactive until ownership is resolved.
Keep one writer per shared file set; hand off branch/commit, changed files, test results, pending
work and unsaved drafts. Overlapping tasks must serialize shared-state writes.

## Acceptance check and official references

Start a fresh session on each selected surface. Ask which instruction files loaded, where outputs
go, what actions need approval, what source revision is visible, and what happens when a tool is
missing or a job already ran. Compare to the written policies before marking that surface verified.
Use the reusable cases in Cluide's `templates/PROJECT_TEMPLATE/tests/behaviour/` as fixtures.
All surfaces in this unused template are **untested**; documentation checks are not runtime tests.

Instruction/source mechanics checked 2026-09-14: [Claude Code memory](https://code.claude.com/docs/en/memory),
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[ChatGPT projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).
Recheck current scheduler and connector documentation for the surface you actually deploy.
