# Routing Log

> One line per dispatched subtask, and per decision to keep a subtask inline, appended by the
> session that made it (see the `dispatch` skill). Archetype starts with a log key from the
> skill's routing table (or `inline`), optionally followed by a colon and detail. Corrected is
> the number of worker output items the orchestrator had to fix or discard (`—` for inline).
> This log is the input to routing calibration: during a periodic review, keys with ~10+ rows
> and no escalations or corrections are candidates to demote a tier; keys failing more than ~1 in
> 3 are candidates to promote. Either change is proposed for approval, then recorded in the
> *Dispatch Overrides* section of `CLAUDE.md` (Claude) or the OpenAI routing section of
> `PLATFORM_SETUP.md` — this file is evidence, not policy.
> Archive rows older than ~3 months to `ROUTING_LOG_ARCHIVE.md` if the file grows past ~100 rows.

| Date | Archetype | Tier | Effort | Escalated | Corrected | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-12 | bulk-extract: receipts (example) | [configured model] | low | N | 0 | 34 receipts parsed, spot-check clean — delete this row |
