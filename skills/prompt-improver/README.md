# prompt-improver

Improves, critiques and writes prompts for AI assistants: everyday chat prompts, system and API
prompts, agent task prompts, project instructions, standing instruction files (`AGENTS.md`,
`CLAUDE.md` and similar), scheduled task prompts and skill descriptions. It returns the improved
prompt ready to copy, with a short rationale tying each change to a weakness, and it leaves a
prompt alone when it is already sufficient.

Version 6.0.0 · MIT licence · source: Cluide, `skills/prompt-improver/`. The guidance is condensed
from Cluide Guides 02, 03, 19, 20, 25, 26, 27 and 31; the skill does not need them installed.

## Contents

| Path | Loaded | Purpose |
|---|---|---|
| `SKILL.md` | on trigger | Workflow (goal, classify, diagnose, rewrite, check, deliver), output template, unusual-input rules, writing from scratch. |
| `references/general.md` | on demand | Everyday prompts: failure modes, patterns, high-stakes one-shot prompts. |
| `references/system-api.md` | on demand | System and API prompts: structure, variables, output contracts, untrusted input. |
| `references/agent-tasks.md` | on demand | Agent tasks, project instructions, standing instruction files, scheduled tasks, and which layer a rule belongs in. |
| `references/skill-descriptions.md` | on demand | Skill descriptions and SKILL.md bodies: triggering, overlap, length limits, portability. |
| `evals/` | never at runtime | Behaviour cases in the Guide 31 shape, for whoever maintains the skill. |

## Install

Install the **whole folder**: the workflow reads the reference files.

| Surface | Route |
|---|---|
| Claude (claude.ai / desktop account skills) | Upload `prompt-improver.zip` (this folder, zipped) as a skill. |
| Claude Code | Copy the folder to `~/.claude/skills/prompt-improver/` (personal) or `.claude/skills/prompt-improver/` (project). |
| Codex | Copy the folder to `~/.agents/skills/prompt-improver/` or the repository's `.agents/skills/prompt-improver/`. |
| Antigravity (documented, untested) | Workspace `.agents/skills/prompt-improver/`. |
| Gemini app (documented, untested) | Upload the `.zip` on the Skills page. An upload is a copy: re-upload after each update. |
| ChatGPT | Use the account's skill installation surface where available; otherwise the last row. |
| Hosts without skill install | Supply `SKILL.md` and the `references/` files as sources and ask for the skill explicitly. |

A skill installed on one surface does not appear on the others.

After installing, test three cases in a fresh session: a request that should trigger it
("improve this prompt: summarise the attached contract"), a neighbour that should not ("review
this plan before I send it to the board"), and a prompt that is already sufficient, which should
come back unchanged with the reason.
