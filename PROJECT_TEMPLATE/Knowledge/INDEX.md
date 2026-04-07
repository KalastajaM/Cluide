# [PROJECT NAME] — Knowledge Index

> Index of all topic knowledge files in this folder.
> Read this file to know what topics exist before deciding which detail file to open.
> Update this index whenever a topic file is created, renamed, or archived.

---

## Active Topics

| File | Topic | Last updated | Status |
|------|-------|--------------|--------|
| `[TOPIC_NAME].md` | [What this topic covers] | [YYYY-MM-DD] | Active |

*No topics yet — create the first one when a topic emerges that warrants its own file.*

---

## Archived Topics

| File | Topic | Archived |
|------|-------|----------|
| *(none yet)* | | |

---

## When to Create a Topic File

Create a new `Knowledge/[TOPIC].md` when:
- A subject has 3+ distinct facts, decisions, or states worth tracking
- You find yourself re-explaining the same context to Claude across sessions
- A project, client, or system warrants its own running record

Use the template below to start a new topic file.

---

## Topic File Template

Copy this into a new `Knowledge/[TOPIC].md` file:

```markdown
# [Topic Name]

> Last updated: [YYYY-MM-DD]

## Summary

[2–3 lines: what this is and why it matters.]

## Current Status

[One-line state: e.g. "In progress", "Blocked on X", "Complete as of YYYY-MM-DD"]

## Key Facts

- [Fact 1 — include date if relevant]
- [Fact 2]

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| [YYYY-MM-DD] | [What was decided] | [Why] |

## Open Questions

- [Question 1]

## History

[Brief chronological notes. Compress older entries. Only keep what's useful for future context.]
```
