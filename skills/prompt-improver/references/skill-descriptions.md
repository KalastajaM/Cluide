# Improving skill descriptions and SKILL.md files

The frontmatter description is the triggering mechanism: it is always in context, and the agent decides from it alone whether to consult the skill. The body only loads after triggering. So description problems are triggering problems, and body problems are execution problems; diagnose which one the user actually has.

## Description failure modes

- **Undertriggering (the common case).** Descriptions that only say what the skill does, not when to use it. Agents err toward not consulting skills, so descriptions should be a little pushy: use "trigger this skill whenever..." phrasing and list concrete user phrases, contexts, and file types that should trigger it, including casual phrasings that don't name the skill. The description can also carry proactive defaults the skill should apply on activation ("always confirm tone unless it's clear from context").
- **"When to use" information in the body.** Useless there; it is only read after the triggering decision is made. Move it all into the description.
- **Overtriggering by keyword.** Descriptions that match on a broad keyword ("email", "data") fire in adjacent contexts. Add explicit "do NOT use for X" boundaries against near-miss cases.
- **Overlap with a sibling skill.** Two installed skills whose descriptions both claim "review this" or "optimize my instructions" race for the same request, and the loser goes quiet without any error. Check the descriptions of skills likely to be installed alongside, and put a reciprocal exclusion in each ("do NOT use to review a document that is not a prompt"). Name the job being excluded; a skill name only helps where that skill is known to exist.
- **Too long, or not parseable.** The open standard caps `description` at 1024 characters, and some install paths reject a longer one at save time; other hosts truncate the skill listing or shorten descriptions to fit a budget. A description long enough to risk the cap is usually carrying detail that belongs in the body. Stay at or under 1024, aim for a few hundred characters, and count before installing. A plain one-line value containing ": " breaks strict YAML parsers: use a folded `>` block or quote it.
- **Simple-task blindness.** Agents skip skills for tasks they can handle directly, regardless of description. If the skill's value is on simple-looking tasks, the description must say why the direct approach falls short.

## Body failure modes

- **Everything in one file.** Keep SKILL.md under ~500 lines; push domain detail into references/ with clear pointers on when to read each.
- **Missing output format.** Without an exact example the skill produces a different layout every session. Show the format in a code block with headers and field names; one filled example beats a paragraph of description.
- **Vague tool references.** "Check the calendar" without naming the exact tool or query means a different approach every run. Name tools, search queries, and file paths literally.
- **No edge-case clauses.** Skills break on slightly unusual input. Three to five "if X, do Y" clauses for the most common deviations (too many items, wrong language, missing data) fix most of it.
- **Rigid MUSTs instead of reasons.** All-caps rules overfit; explaining why a step matters lets the model handle unlisted cases. Treat ALWAYS/NEVER as a yellow flag — except hard safety boundaries (never send, never commit autonomously), which should stay explicit. Tool-restriction frontmatter is host-specific: the open standard marks `allowed-tools` experimental, Claude Code documents `allowed-tools` (pre-approves) and `disallowed-tools` (removes) with its own semantics, and other hosts ignore both. Treat prose as the only portable enforcement and put structural controls in the host's own settings or skill fields where the skill will actually run.
- **Narrow examples treated as spec.** Examples anchored to one case make the skill useless outside it. Pick examples that span the input space.
- **Repeated work not bundled.** If every invocation would write the same helper script, ship it in scripts/ instead.

## Improving a description: quick procedure

1. Collect realistic should-trigger and should-not-trigger user queries, favoring near-misses over obvious cases. Pair every positive case with the nearest request that should not fire it, including the requests a sibling skill owns: a new description that steals an old skill's trigger fails both at once, which is exactly the signal to look for. Run each case more than once; a case that passes two runs out of three is on the edge.
2. Rewrite: what it does, then explicit trigger contexts and phrases, then exclusions.
3. Read the result aloud as if telling a colleague when to use the skill; if the way the user naturally asks for the task isn't covered, add that phrasing.
4. Where tooling is available, run the host's description optimizer against the query set rather than hand-tuning.

## One format, several hosts

`SKILL.md` is an open standard, developed by Anthropic and released publicly, and implemented by
several assistants, including Claude, OpenAI's ChatGPT and Codex, and Google's Antigravity. A
skill written to the common core (`name` and `description` frontmatter, a Markdown body, optional
`references/`, `scripts/` and `assets/` folders) installs on any of them. Deltas worth knowing
when improving a description, as documented in late 2026 (recheck the host's own documentation):

- The standard limits `name` to 64 lowercase letters, digits and hyphens, matching the folder
  name. Claude also rejects the reserved words "claude" and "anthropic" in it, so a portable
  skill obeys both.
- Some hosts treat `name` as optional and default it to the folder name. Set it anyway.
- Host-specific files and fields (OpenAI's optional `agents/openai.yaml`, Claude Code's extra
  frontmatter such as `when_to_use` or tool restrictions) are ignored elsewhere. Nothing in a
  portable description should depend on them.

Install routes differ entirely and are not interchangeable; that is a packaging concern, not a
description concern.
