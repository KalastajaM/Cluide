# Dispatch — behaviour cases

Cases for the `dispatch` skill in the shape of Guide 31 §3: each folder holds the prompt as it
would actually be typed and checkable graders. They test behaviour, not the text of `SKILL.md`.

| Case | Protects | Written against |
|---|---|---|
| `loads-alongside-playbook` | The skill loads next to a playbook skill that matches the same task | 2026-08-12: a sweep loaded the maintenance playbook only and never made a routing decision |
| `tier-question` | Positive neighbour: a question about the tier of delegated work loads the skill | Pairs with `stays-quiet-session-model` |
| `explicit-model-per-spawn` | Every spawn names its tier; no forks for bulk work; the fan-out is batched | 2026-09-23 review: a spawn of an unpinned type without `model` inherits the session's (top) tier |
| `inline-floor` | A task that reduces to one scripted check is done inline, not delegated | The inline floor, §1 |
| `stays-quiet-session-model` | Negative neighbour: a request to change the session's own model does not load the skill | The description's exclusion |

**How to run.** In a fresh session — never the session that edited the skill (Guides 26, 27) —
opened on a *throwaway clone* of Cluide with the skill installed: one prompt asks for fixes, and
a behaviour test never edits a live checkout. Paste `prompt.md`'s body, then check each grader
against the reply and the tool calls. Record results below per surface and model; an unrun case
is **untested**, not passing.

**What `loads-alongside-playbook` tests depends on the setup.** In a Cluide clone the root
`CLAUDE.md` carries the load hook, so the case tests the hook. To test the bare trigger race —
the skill description alone against a playbook — run it where a matching playbook skill is
installed (for example `maintenance-dispatcher` with its maintenance project mounted) and no
hook is present, and record which setup you used.

**Scripted runners.** `claude plugin eval` runs each case in a throwaway workspace with only the
plugin loaded (Guide 31 §4), so these cases need the Cluide tree supplied through each case's
`case.yaml` setup before that runner can grade them. Not yet written; hand runs only.

| Date | Surface | Model | Skill revision | Result |
|---|---|---|---|---|
| — | — | — | — | untested |
