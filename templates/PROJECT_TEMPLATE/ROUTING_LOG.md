# Routing Log

> One line per dispatched subtask, appended by the session that dispatched it (see the
> `dispatch` skill). This log is the input to routing calibration: during a periodic review,
> archetypes that never escalate are candidates to demote a tier; archetypes escalating more
> than ~1 in 3 are candidates to promote. Either change is proposed for approval, then recorded
> in the Dispatch Overrides section of `CLAUDE.md` — this file is evidence, not policy.
> Archive rows older than ~3 months to `ROUTING_LOG_ARCHIVE.md` if the file grows past ~100 rows.

| Date | Archetype | Tier | Effort | Escalated | Outcome |
|---|---|---|---|---|---|
| 2026-08-12 | bulk-extract (example) | haiku | low | N | 34 receipts parsed, spot-check clean — delete this row |
