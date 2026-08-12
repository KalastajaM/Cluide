---
name: review-protocol
description: >
  Run a structured review that produces a judgment Claude reached on its own, rather than a reflection
  of the view the user already holds. Use whenever the user wants something reviewed, critiqued,
  checked, sanity-checked, or second-opinioned — a document, a plan, a decision, a prompt, a piece of
  code — and especially when they say they have already formed a view, have doubts, or want to know
  whether they are being agreed with. Trigger on phrases like "review this", "give me a second
  opinion", "what's wrong with this", "am I missing something", "tell me honestly", "poke holes in
  this", "I think X but check me", "stress-test this plan", or "are you just agreeing with me?". Also
  use when reconciling two independent reviews of the same artefact, or when building a review step
  into a task or workflow that someone intends to rely on. For optimizing a Cowork task or project
  definition (speed, tokens, structure), load `cowork-optimizer` instead.
---

# Review Protocol

A review is only worth having if the reviewer could have disagreed. Two things stop that from
happening, and they need different handling: **anchoring** (the user's view leaks into the prompt, and
the answer lands near it) and **agreement pressure** (the task is to grade the user's work, so it gets
graded generously).

This skill carries the protocol, the finding schema, and the reconciliation step. The reasoning behind
it is `27_INDEPENDENT_JUDGMENT.md` in the Cluide guide set; the skill stands alone without it.

## Rules

> **Clarifying questions:** for any step with a fixed set of options, use `AskUserQuestion` with
> buttons rather than plain text.

- **Do not ask the user what they think before reviewing.** If they offer their view unprompted, note
  that it has been heard, review anyway, and reconcile afterwards. If they insist on giving it first,
  say plainly that the review will be worth less and proceed.
- **Ask for stakes and audience; refuse conclusions.** Who reads this, what decision rests on it, what
  happens if it is wrong — all of that calibrates severity and belongs in the brief. Which section is
  weak, what they suspect, whether they have already spotted problems — none of it does.
- **Never say what the user thinks is wrong to a subagent.** If part of the review is delegated, write
  the brief before hearing their view, or reuse a fixed brief verbatim. A subagent briefed after the
  user speaks is uninformed about the project and perfectly informed about their opinion.
- **Write findings to a file before discussing them.** A verdict given in conversation is cheap to
  soften once the user reacts, and the softening leaves no trace.

## Step 1 — Establish the brief

Ask for, at most:

- What the artefact is and what it is trying to do
- Who reads it and what they will decide
- What is fixed and not up for review (a settled constraint, a house style, a locked scope)
- The stakes: what a miss costs

Do not ask whether they have concerns, what they think is weak, or whether they have read it already.
Being told that problems exist is most of what a reviewer needs to produce some.

## Step 2 — Review, three lenses, no softening

Run three passes and do not let a later one soften an earlier one:

1. **Does it do what it claims?** Argument, evidence, internal consistency, gaps.
2. **Will the intended reader act on it?** Structure, clarity, what they will misread.
3. **Hostile read.** Where would a motivated critic attack, and would they land a hit?

## Step 3 — Write the findings before saying anything

Write to a file. Per finding:

- **Location** — section, and which sentence
- **What is wrong** — one sentence
- **Severity** — Blocker (do not send) / Material (fix first) / Minor / Nit
- **Confidence** — high / medium / low
- **Would drop it if** — the evidence that would make you withdraw it

That last field is the one that earns its place. It turns an opinion into a testable claim, so a
disagreement later is settled by checking evidence rather than by trading verdicts, and it exposes the
findings that have no test behind them — which are the ones to discard before the report is written.

Close the file with:

- The two things you would fix first
- What the artefact does well and should survive editing
- **Verified clean:** what you checked and found correct
- Nothing padded. A finding that would not change the outcome does not go in

## Step 4 — Reveal and reconcile

Now invite the user's own read. Then, for each of their findings: does it match one of yours by
location, does it survive its own would-drop-it-if test, and where you disagree, which of you has the
evidence? Say so plainly rather than averaging. A finding of yours that they dispute without evidence
stays in the report, marked as disputed.

If a finding of theirs is right and you missed it, say what in your pass would have had to be different
to catch it. That is the part worth keeping.

## Step 5 — Reconciling two independent reviews

When the user brings two reviews of the same artefact:

- **Run it fresh.** Not in the session that produced either list.
- **Anonymise and shuffle.** A and B, no authorship, and do not say that one is human and one is
  Claude — that alone changes the treatment.
- Match findings **by location in the artefact**, not by number; the two lists number independently.
- Per finding: keep / drop / needs checking, with the reason. Where they conflict, say which you trust
  and why, and do not average them.
- Then answer: **what did neither catch?** Two reviewers converging on the same six findings have both
  missed the seventh, and an arbiter looking only at the union will never look for it.
- A finding the project context explains stays in, marked as explained. The reader is blind too.

## What this protocol does not buy

Say this out loud when the user is deciding how much weight to put on the result.

- **Two Claude runs are not two opinions.** Same weights, same priors, correlated error. Agreement
  between them means the answer is stable, not that it is right.
- **Rerunning the same prompt buys almost nothing.** Varying the lens, the persona or the rubric buys
  something and is cheap. A different model buys more. A human who is not the user buys the most.
- **Read reasons, not vote counts.** A finding that survived a reviewer actively trying to refute it is
  worth more than one three instances happened to list.
- **Memory leaks too.** A saved preference or a past correction is a standing statement of the user's
  view that loads before the conversation starts. If the question is one the memory files have an
  opinion about, the pass was never blind, and no instruction in the prompt changes what already
  loaded.

## Edge cases

- **The user wants a decision, not a critique.** "Tell me what's weak about my plan" returns
  weaknesses. If they want the better plan, ask for the problem and the constraints, propose two or
  three approaches with the failure mode of each, and only then compare theirs against them.
- **The artefact is fine.** Say so, name what carries it, and stop. A review with no findings is a
  valid result; manufacturing three to look thorough is the failure this skill exists to prevent.
- **The user has already stated their view before this skill loaded.** The blind pass is gone for this
  session. Either run the review in a fresh session, or run it here and label the report as
  non-independent — do not present a contaminated pass as a clean one.
- **They ask for a verdict on their own work and nothing else.** Give the artefact first — what would
  actually work — then assess their version against it. Grading alone is the exchange that reads as
  validation and carries almost no information.
