---
type: llm
---
Pass if the improved prompt guards against adding the same transactions twice (idempotence, a last-imported marker, or a check before writing). Fail if re-running it could double-enter transactions.
