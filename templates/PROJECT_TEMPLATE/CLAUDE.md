# Claude entry point

@AGENTS.md

`AGENTS.md` beside this file is the shared policy. If this interface does not resolve
imports, read it in full before working. Shared rules live there, not in this adapter; only
Claude-specific sections belong here.

## Dispatch Overrides

*Claude-only and optional — delete this section together with `ROUTING_LOG.md` and the
Delegation section of `AGENTS.md` if nothing in this project is delegated.* Routing exceptions
for the `dispatch` skill; its routing table applies wherever this section is silent.

- Before any task with bulk, parallel or mechanical parts, load the `dispatch` skill — even when
  another skill has already supplied the procedure.
- Default worker tier for work no table row places: [sonnet]. Pass `model` on every spawn of
  an unpinned agent type.
- Never below [opus] for: [content whose errors are expensive here — figures, dates, legal
  terms, anything sent in my name]
- Known-safe on [haiku]: [archetypes the routing log has proven — leave empty until calibration]
- Log dispatches to `ROUTING_LOG.md`.
