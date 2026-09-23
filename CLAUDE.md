# Cluide — Claude Entry Point

@AGENTS.md

The imported `AGENTS.md` is the canonical shared repository policy. If this interface does not resolve imports, explicitly read the root `AGENTS.md` before working. Do not duplicate shared rules here.

## Claude-only

### Dispatch Overrides

Claude routing exceptions for work delegated from sessions in this repository — subagents, workflow stages, scheduled tasks. The `dispatch` skill (`skills/dispatch/SKILL.md`) applies wherever this section is silent.

- Before executing any task with bulk, parallel or mechanical parts, load the `dispatch` skill — even when another skill (a maintenance playbook, a review protocol) has already supplied the procedure. Playbooks say what to do; dispatch says which tier does it. Under the inline floor, doing it inline is correct; log it as `inline`.
- Default worker tier: sonnet, replacing the table's haiku rows — only the known-safe list below runs on haiku. Pass `model` on every spawn of an unpinned agent type; an omitted one inherits the session's tier.
- Never below opus for: writing or reviewing guide prose that ships, and review verdicts on guides, skills or templates — publication quality is this repository's whole product.
- Known-safe on haiku: link checks, byte-identity mirror sweeps (`diff -q`), guide-number citation greps, file inventories — anything the merge gate defines mechanically.
- Log dispatches to `development/ROUTING_LOG.md` (gitignored working state: this section is the published example, the log is not).

For conversational Claude setup, see `PLATFORM_SETUP.md`.
