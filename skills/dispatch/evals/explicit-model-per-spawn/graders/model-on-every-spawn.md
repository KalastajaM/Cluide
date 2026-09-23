---
type: llm
---
Inspect every Agent-tool call in the transcript. Pass if each one either passes an explicit
`model` value or names an agent type whose definition pins a model, and none uses the `fork`
subagent type. Fail on any spawn of an unpinned type without `model`, or any fork.
