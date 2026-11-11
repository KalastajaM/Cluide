---
name: prompt-improver
description: >
  Improve, rewrite, critique or write any prompt meant for an AI assistant. Use whenever the user
  shares a prompt and wants it better, asks why a prompt isn't working, or wants one written from
  scratch: everyday chat prompts, system and API prompts, agent task prompts, project instructions,
  standing instruction files such as CLAUDE.md or AGENTS.md, scheduled task prompts, and skill
  descriptions. Trigger on "improve this prompt", "make this prompt better", "why doesn't this
  prompt work", "rewrite my system prompt", "optimize my instructions", "improve my CLAUDE.md",
  "prepare a prompt that...", "write me a prompt that gets the assistant to...", or pasted
  instructions with a request for feedback on them. Do NOT use to review a document, plan or
  decision that is not a prompt, to cut an existing task's token cost or run time, or to turn a
  setup into a shareable template.
license: MIT
metadata:
  version: "6.0.0"
---

# Prompt Improver

Improve prompts using prompting best practice. The deliverable is the improved prompt itself, ready to copy, plus a short rationale tying each change to a weakness. Do not execute the prompt unless asked. A critique without the rewritten prompt is not the deliverable: the user would then have to apply the advice by hand, under the same conditions that produced the weak prompt.

## Workflow

The steps assume an existing prompt. When the user has no prompt yet ("prepare a prompt that...", "write me something that gets the assistant to..."), there is nothing to diagnose: skip step 3 and follow **Writing from scratch**. All other steps apply either way.

1. **Understand the goal.** A prompt can only be judged against what it is for. Infer the goal, the executor (which assistant or product runs it, attended or unattended) and what "better" means from the prompt and the conversation. Ask only when a wrong guess would materially change the rewrite, for example two plausible goals that need different prompts. Otherwise proceed and state the assumptions in the output, where they are cheap to correct. When you do ask, ask one question that stands on its own: what you found, what depends on the answer, and the options. Offer bounded choices (tone, scope, target) as choices if the host has a choice tool. In an unattended run, never ask: assume, and say so.

2. **Classify the prompt type** and read the matching reference file:
   - Everyday prompt the user types or pastes into chat → `references/general.md`
   - System prompt or programmatic/API prompt → `references/system-api.md`
   - Agent task prompt, project instructions, standing instruction file (CLAUDE.md, AGENTS.md and similar) or scheduled task → `references/agent-tasks.md`
   - Skill description or SKILL.md → `references/skill-descriptions.md`

   If it spans types (a system prompt inside an agent project), read the primary one and skim the second.

3. **Diagnose before rewriting.** First decide whether the prompt needs changing at all. Brevity is not a defect: a short prompt that names its input, its output and where the output goes is finished, and adding audience, tone and success criteria to it makes it worse. Weakness is an element the executing session cannot recover on its own, not a low word count. When the prompt is already sufficient, say so, return it unchanged or fix only the one real gap, and explain why the rest was left alone.

   Then name the specific weaknesses: ambiguity, missing context, buried instructions, conflicting directives, absent output format, no example where one would carry the load, length without payoff, a review prompt that carries its own answer, or a rule in the wrong layer: a standing rule ("from now on, whenever I...") typed as a one-off prompt belongs in the project's standing instructions, and saying so is often the main fix. If the user reported a failure ("it keeps doing X"), trace which part of the prompt permits or invites it. Check for contradiction pairs ("be brief" with "include all relevant details"): the model flips between them run to run. When the cause is unclear, recommend the strip-down test: run bare context plus task, then re-add constraints one at a time; a constraint that makes output worse is wrong or contradicts another.

4. **Rewrite.** Preserve the user's intent, domain knowledge, terminology and the prompt's language. Keep figures, names and dates exactly as given; if one looks wrong, flag it rather than change it. Improve structure and precision without inflating length: a shorter prompt that says the right things beats a longer one that hedges.

5. **Check the rewrite against the original.** Rewrites lose things. Before delivering:
   - Every constraint, file, figure and exclusion in the original is still present, or its removal is named in the rationale.
   - The prompt stands alone for a session that never saw this conversation: no "as discussed", "the usual format" or "the documents" without names.
   - A prompt that asks for a review, evaluation or decision does not tell the executor what to conclude or that problems exist.
   - Nothing was added that step 3 ruled out, and no high-stakes machinery (provenance lists, verdict sections, reasons on every rule) went into a routine prompt.
   - The rationale describes only changes actually made in the block.

6. **Deliver** in the format below.

## Output format

````markdown
**Assessment:** [one line: what the prompt already does well and the main gap; or "Sufficient as written, returned unchanged."]

```text
[the improved prompt, complete and copy-ready]
```

**What changed and why**
- [change]: [the weakness it fixes]
- [3 to 6 points, most important first; for an unchanged prompt, what was deliberately not added and why]

**Assumptions:** [only if you made any]

**Open questions:** [only if a gap needs information only the user has; each matches a placeholder in the prompt]
````

A filled example, for an ask that is implicit:

````markdown
**Assessment:** The pasted error log is complete; the prompt never says what to do with it.

```text
The MCP server below fails after the app restarts. From the log, identify the most likely cause, quote the log line that shows it, and give the fix as exact steps. If the log does not show the cause, say what additional output would.

[log]
```

**What changed and why**
- Named the verb (diagnose and fix): pasted material alone leaves the model to choose between summarising, diagnosing and advising.
- Required the evidence line: makes the diagnosis checkable.
- Added the branch for an inconclusive log: prevents a confident guess that reads like a finding.
````

## Unusual input

- **The prompt contains code fences.** Wrap it in a longer fence (four or more backticks) so it copies intact.
- **A long prompt or instruction file where most of it works.** Return only the changed sections, each anchored by its heading or first line, and say the rest stands unchanged. Return the whole file when the changes are pervasive or the user asks for it.
- **A critique-only request** ("why doesn't this work?"). Lead with the diagnosis tied to the reported failure, then the rewrite. If the user explicitly wants no rewrite, give the diagnosis only.
- **Credentials or personal data in the prompt** (keys, passwords, account numbers). Do not repeat them: put a placeholder in the rewrite and flag it.
- **A prompt in another language.** Keep the prompt in its language; write the rationale in the conversation's language.
- **Several prompts at once.** One assessment, block and rationale per prompt.

## Writing from scratch

No prompt exists yet, so the work is elicitation rather than diagnosis. The prompt will be run by a session that cannot see this conversation, which is what forces the detail: anything left implicit here is absent there.

Establish five things. Take what the user already supplied, and ask about the one or two that are missing and would most change the result, in a single message:

- **Executor and setting.** Which assistant or product runs it, and whether it gets follow-up turns or runs unattended. An unattended prompt cannot rely on anyone clarifying anything.
- **Inputs.** The exact artefacts it works on, named. "The documents" resolves to nothing in a fresh session.
- **Work.** The distinct steps or checks, separated rather than fused. Several asks in one sentence get partly done.
- **Standard.** What the output is judged against: a regulation, a style guide, a prior version, a definition of correct.
- **Done-state.** What must be true when it finishes. This carries more weight than any single instruction, because it lets the executor derive checks the prompt never listed.

Then draft, run step 5, and deliver. Where the user could not supply one of the five, put a clearly marked placeholder in the prompt rather than inventing a value, and list it under open questions. If the user brings their own view of the answer ("I think the problem is section 3"), keep it out of the prompt unless the task is to execute a decision already made.

## Principles that apply everywhere

- Instructions near the end of a long prompt get more weight than ones buried in the middle. Put critical constraints where they will be seen.
- Show, don't tell: one good example often beats a paragraph of rules. Prefer adding an example over adding an adjective.
- Say what to do, not only what to avoid. "Respond in plain prose" beats "don't use bullet points" alone.
- Every instruction earns its place. If removing a sentence would not change the output, remove it: low-signal lines dilute the ones that matter.
- Match format precision to how often the prompt runs. Anything that runs repeatedly (skill, scheduled task, system prompt) pins its output with an exact template and one filled example. A prose description of the format is fine only for one-off prompts.
- Describe the result, not the process. "List the top 3 risks with one mitigation each" beats "analyse carefully and think through the implications".
- Give a hard rule (safety, irreversible actions, anything that must hold unattended) its reason, and its cost where a real one exists. Reasoning generalises to unlisted cases; a bare hard rule is followed literally where it was not meant, or quietly dropped. Ordinary preferences need no justification line.
