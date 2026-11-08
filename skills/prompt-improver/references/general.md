# Improving everyday prompts

Prompts a person types or pastes into a chat interface. The audience is a capable model in an interactive setting, so the prompt can rely on follow-up turns existing, but a good prompt gets the right answer in one shot.

## Common failure modes

- **Underspecified deliverable.** "Write something about X" leaves format, length, audience, and tone to chance. Fix by naming all four when they matter.
- **Missing context the user has but the model doesn't.** Who is this for, what has already been tried, what constraints exist. The user forgets the model can't see their situation.
- **Multiple asks fused into one sentence.** Split into an ordered list of steps or separate the primary ask from the nice-to-haves.
- **Quality adjectives instead of quality criteria.** "Make it engaging and professional" gives the model nothing to aim at. Replace with observable properties: reading level, structure, what to include or exclude, an example of the desired register.
- **The ask is implicit.** The prompt is mostly pasted material (a data table, an error log, a document, a narrative account, a bare status update) with no verb attached, leaving the instruction to be inferred from the surrounding context or the session title. The model then picks between summarising, diagnosing, filing and advising, and it will not always pick the intended one. Fix by naming the verb and the deliverable, even in one clause; the pasted material itself usually needs no change.
- **No branch for missing or unfindable input.** The prompt names a file, figure or fact and says nothing about what to do if it is not there. The failure mode is not a refusal, it is a confident plausible substitute that reads like a finding. Add the branch explicitly: say so and stop, rather than infer a value.
- **The user's own figures treated as fact.** When a prompt asserts numbers, dates or names that will be carried into the output, an error in the prompt becomes an error in the document. Where a source for them exists, instruct the model to recompute or re-read from that source and flag any mismatch instead of accepting the prompt's version.
- **The prompt carries its own answer.** Common in prompts that ask for a review, an evaluation or a decision. "I'm planning X, would that work?" anchors the reply on X and turns the task into grading X, which comes back as a qualified yes. "Find the problems in this" or "I spotted a few issues" tells the model problems exist, so it produces some. Fix by asking for the artefact rather than a verdict ("propose two or three approaches, rank them, give each one's failure mode"), and by dropping the user's conclusions while keeping stakes and audience ("it goes to a regulator on Friday" calibrates severity and should stay). A neutral replacement for "what's wrong with this": "what does this do well that must survive editing, what does it do badly, and where would a motivated critic attack it?". Skip this when the decision is already made and the prompt only asks for help carrying it out.

## Patterns that help

- State role or perspective only when it changes the answer ("as a tax advisor reviewing this for red flags").
- Put reference material first, the ask last. Context stated upfront (audience, purpose, constraints) steers generation; the same note added afterwards reads as a correction.
- State scope boundaries explicitly: "update section 3, leave everything else unchanged" prevents the model's tendency to improve things it wasn't asked to touch.
- For revision tasks, include the original and say what to preserve, not just what to change.
- Ask for reasoning or a plan first only when the task is genuinely hard; for simple tasks it adds noise.
- Write for a reader who cannot see the conversation the prompt came from. If it will be pasted into a fresh chat, run as a task, or handed to someone else, then "the documents", "the usual format" and "as we discussed" resolve to nothing. Name the files, state the format, restate the constraint.
- Define the done-state, not only the task. "Ready to send to the counterparty" or "passes review without further edits" lets the model derive checks the prompt never listed; "review this" leaves it guessing when to stop.

## High-stakes one-shot prompts

When the output is expensive to get wrong and the prompt runs roughly once, in a fresh session, a few additions pay for themselves. Use them only then: on a routine prompt they are padding.

- **Rules carry reason, cost and an escape route.** "Never do X. Reason: it turns A into B. If you believe X is nonetheless required, report it as a finding with the consequence stated; do not silently do it." A rule without a reason is applied literally where it was not meant; a rule without a sanctioned way to challenge it forces a choice between obedience and a quiet violation.
- **Provenance first.** The run opens by listing the files, versions and dates it actually read, so a stale copy or a missed file shows before the findings do.
- **External claims checked against a named primary source,** with anything unconfirmed marked UNVERIFIED rather than dropped. Silent omission hides the edge of what the run knows.
- **The output schema as a filled example,** not a description.
- **Closing sections that make silence meaningful:** "Verified clean" (what was checked and found correct), open questions phrased as decisions for a person, and a one-line verdict.
- **An anti-padding line:** no findings that would not change the outcome.

A skeleton filled with generic phrasing is unlikely to beat three clear sentences. The structure is a place to put real decisions, not a substitute for them.
