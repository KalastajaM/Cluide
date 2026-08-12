# Agent Starter Pack — model-pinned subagents for Claude Code

> Four subagent definitions with the model tier pinned in frontmatter, so routing is structural
> rather than re-decided per prompt. Companion to the `dispatch` skill (`skills/dispatch/`),
> which carries the routing policy itself; these files are the Claude Code binding for it.
> Claude Code only — Cowork sessions don't persist agent definition files; there the dispatch
> skill routes via per-spawn model parameters instead.

---

## What's in this folder

| File | Agent | Model | Effort | Role |
|---|---|---|---|---|
| `scout.md` | scout | haiku | low | Bulk reading, searching, extraction, classification. Read-only. |
| `builder.md` | builder | sonnet | (default) | Implementing well-specified changes and drafts. |
| `verifier.md` | verifier | opus | high | Adversarial checking of other agents' output. Read-only, cannot spawn. |
| `researcher.md` | researcher | sonnet | (default) | Web research legwork; returns findings with sources. |

## Install

For all your projects (recommended):

```bash
cp scout.md builder.md verifier.md researcher.md ~/.claude/agents/
```

For one project only: copy into that project's `.claude/agents/` instead. Project-level
definitions override user-level ones with the same name. Verify with `/agents` in a session.

## Recommended session setup

Run orchestrating sessions on `opus`, per the dispatch policy. Where a task has a distinct
plan-then-execute shape, `opusplan` (set via `/model opusplan`) plans on Opus and executes on
Sonnet automatically — the same split without any dispatching at all.

Optionally add this stanza to `~/.claude/CLAUDE.md` (or a project's) to reinforce the stance:

```markdown
## Delegation
When a task splits into independent or mechanical parts, plan and review here but dispatch the
parts to subagents — scout for bulk reading/extraction, builder for specified changes,
researcher for web legwork, verifier for checking — in parallel where independent. Subtask
prompts must be self-contained. Have workers return summaries and file paths, not full content.
Do small subtasks inline; dispatching has overhead.
```

## Notes

- **Don't set `CLAUDE_CODE_SUBAGENT_MODEL`** alongside this pack: the environment variable
  overrides every agent's frontmatter, so it would flatten the tiers you just installed.
- The dispatching model can still override any agent's model per invocation; the frontmatter is
  the default, not a cage.
- The escalation ladder (cheap → verify → one tier up on failure) and the routing table live in
  the `dispatch` skill; keep the two in sync if you edit either.
- Frontmatter fields used here (`model`, `effort`, `tools`) are documented at
  [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents).
