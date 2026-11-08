# Improving system prompts and API prompts

Prompts that run programmatically: system prompts for products, templates with variables, agent instructions. These run thousands of times unattended, so reliability and edge-case behavior matter more than elegance, and there is no follow-up turn to repair a misunderstanding.

## Common failure modes

- **No structure.** Long undifferentiated prose. Use XML tags or Markdown headers to separate role, context, task, constraints, examples, and output format so instructions don't blur together.
- **Untyped variables.** Template slots like {{input}} with no statement of what the variable contains, its format, or what to do when it is empty or malformed.
- **No output contract.** If downstream code parses the response, the prompt must pin the exact output format (JSON schema, tags, delimiters) and forbid extra prose. Include a literal example of a valid output.
- **Edge cases unhandled.** What should the model do with off-topic input, empty input, adversarial input, or a task it cannot complete? Silence here produces improvisation in production.
- **Untrusted input mixed with instructions.** User messages, retrieved documents, emails and web pages pasted into a template can contain text that reads as instructions. Put each in its own delimited block (XML tags work well), say once that content inside those blocks is data to work on, never instructions to follow, and keep the actual instructions outside them.
- **Format enforced by prose when the host can enforce it.** If the API offers structured output (a JSON schema, a response format, tool definitions), use it and keep the prompt's format section for meaning, not syntax. Prose is the fallback where no such feature exists.
- **Conflicting or stale instructions.** Grown-by-accretion prompts accumulate contradictions. Diff instructions against each other and against the examples; examples win in practice, so wrong examples are worse than no examples.

## Patterns that help

- Few-shot examples covering the normal case plus one or two edge cases. Match example formatting exactly to the demanded output format.
- Positive framing for behavior rules, with the reason attached, so the model generalizes to unlisted cases.
- Critical constraints restated near the end of long prompts.
- For classification or extraction: enumerate the label set exhaustively and give a fallback label.
- Consider prompt caching boundaries: put stable content first, variable content last.
- Keep a small regression set: a dozen real inputs, including the edge cases above, with the expected output or a checkable property of it. Rerun it whenever the prompt or the model changes; a prompt edit that fixes one case often breaks another.
