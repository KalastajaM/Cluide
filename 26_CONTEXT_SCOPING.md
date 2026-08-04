# Context Scoping and Prompt Construction

> Every prompt makes a decision about what Claude is allowed to see. Most of the time that decision is made by accident — whatever happened to be in the session, whatever files the folder contains. This guide is about making it deliberately: when withholding context produces a *better* judgment, not just a cheaper one, and how to build a prompt in one session that you run in another.

> **Companion guides:** [Guide 02](./02_PROMPTING_BASICS.md) covers instruction quality — context, task, constraints, output format. This guide covers the layer above it: which session gets which context. [Guide 20](./20_INTERACTIVE_PROMPTING.md) covers the session mechanics (`/clear`, `@` references, plan mode). [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) covers subagents as a parallel-work tool. [Guide 04](./04_MEMORY_AND_PROFILE.md) covers memory, which is context that loads whether you want it or not.

> **Giving this guide to Claude:**
> "Read 26_CONTEXT_SCOPING.md. I need to review [deliverable] before it goes to [audience] / build a one-shot prompt for [high-stakes task]. Help me scope what the reviewing session should and should not see."

---

## Three Ways Context Goes Wrong

| # | Failure | What happens | Usual fix |
|---|---|---|---|
| 1 | **Too little** | Claude fills gaps with plausible invention. Generic output that doesn't fit your situation. | Add context. [Guide 02](./02_PROMPTING_BASICS.md). |
| 2 | **Too much** | Instructions compete for attention. Rules get dropped. Cost rises. | Trim. [Guide 02](./02_PROMPTING_BASICS.md) on context engineering, [Guide 06 — Task Efficiency](./06_TASK_EFFICIENCY_GUIDE.md). |
| 3 | **Wrong kind** | Claude resolves an ambiguity the real reader cannot resolve, so the defect never surfaces at all. | Withhold. This guide. |

Failures 1 and 2 are well covered elsewhere. Failure 3 is the one nobody plans for, because it does not look like a failure. The output is confident, coherent, and wrong in a way you cannot see from inside.

**A concrete case.** You ask Claude to review the onboarding doc for a new hire. Claude has the whole repo in context. The doc says "run the usual setup script." Claude knows which script, sees no problem, reports the doc as clear. The new hire, who has none of that context, is stuck on line one.

The same mechanism bites every time an output leaves the environment that produced it: a proposal to a client, a spec handed to a contractor, a contract sent to a counterparty, a guide published for strangers, an API doc. The reviewer's context is precisely what makes them unable to review it.

**The principle:** context that explains a defect prevents you from seeing it.

---

## What Each Isolation Lever Actually Isolates

Three levers, and they are not interchangeable. Each hides something different and leaks something different.

| Lever | Hides | Still leaks | Cost |
|---|---|---|---|
| **Fresh session** (`/clear`, new chat) | Everything said earlier in the conversation | CLAUDE.md, project instructions, memory, the whole folder | No token cost; you lose the working state. |
| **Subagent** (Agent tool) | Nothing by default — see below | CLAUDE.md, project instructions, folder read access, whatever you put in the brief | One agent's tokens. Returns whatever its brief asks for. |
| **Staged copy** (artefact alone in a scratch directory) | Every project file, because they are not there to read | Nothing on the filesystem side. CLAUDE.md still loads. | A copy step. The only lever that is enforced rather than requested. |
| **Saved prompt file** | The reasoning, negotiation, and dead ends that produced the instruction | Only what you wrote into the prompt | A design session up front. Reusable after. |

### The subagent trap

A subagent is **not blind by default.** It inherits CLAUDE.md and project instructions, and it can read every file in the folder. "Delegate this to a subagent for fresh eyes" gets you nothing on its own — you have handed the same context to a different instance.

Blindness has to be constructed. The brief needs an explicit deny-list naming what is off limits:

```markdown
THE ONLY FILE IN YOUR BRIEF: [path to the artefact]

DENY-LIST — do not open, search for, or reason from any of these:
- Any other file in this folder or on any mounted device folder
- Any CLAUDE.md, project instructions, or project memory
- [prior analyses, trackers, source material — name yours]
- Web search
If you find yourself wanting one of them, that is itself a finding:
note what you needed and why, then continue.

Before your findings, list every file you actually opened.
```

Two of those lines do specific work. **"That is itself a finding"** turns the reviewer reaching for context into a signal: the artefact does not stand alone. **"List every file you actually opened"** is the audit trail — see below for why you need one.

### A deny-list is an instruction, not a boundary

This is the limit of the technique, and it matters more than the technique.

A deny-list asks the subagent not to read something. Nothing stops it. A subagent that opens CLAUDE.md anyway will not announce it, and its findings will silently carry context you thought you had excluded — which is failure mode 3, one level up, in the very tool you reached for to prevent it.

Three responses, in increasing order of strength:

1. **Ask for the file list.** Require the reviewer to open its report with every file it read. Cheap, and it makes most violations visible. It does not make them impossible: a model can produce an inaccurate list as easily as an inaccurate finding. Treat it as a smoke detector, not a lock.
2. **Check the findings for leaked knowledge.** If a blind reviewer references a fact that appears nowhere in the artefact, it did not come from the artefact. This is the check that actually catches things.
3. **Stage a copy.** Copy the artefact alone into a scratch directory outside the project and point the reviewer at that path. Now the project files are not merely forbidden, they are absent. CLAUDE.md still loads, so this is not perfect isolation, but the filesystem half is enforced rather than requested.

Use the deny-list alone for routine reviews. Stage a copy when the finding actually matters — before something leaves for a client, a counterparty, or the public. It costs one `cp`.

### Choosing a lever

- The reader will not have your context → **subagent with a deny-list**, plus a staged copy if the stakes justify it.
- The instruction is worth reusing, or the stakes are high enough that you want to review the instruction itself before running it → **saved prompt file.**
- You are just switching topics → **fresh session.** This is hygiene, not scoping.

---

## The Blind Pass

The pattern in full: **blind → in context → reconcile.** Run the first two without the third and the blind pass mostly generates noise you then throw away.

### Pass 1 — Blind

A subagent whose brief is the artefact and nothing else. Its job is the fresh read: does this stand on its own, is it internally coherent, what would a hostile reader attack? 

Specify the finding schema *in the brief*, filled in, not described. The subagent's returned text is the report, so whatever shape you did not ask for is a shape you will not get.

### Pass 2 — In context

The main session, with everything: project files, memory, source material, prior decisions. Run the substantive checklist. This is the pass that catches factual errors, contradictions with the underlying record, and anything requiring domain knowledge.

### Pass 3 — Reconcile

The main session does the merge — it is the only one holding both reports, and its job here is arbitration, not review. Inputs: the blind report and the in-context findings. Findings are matched by *location in the artefact*, not by number, because the two passes number independently.

The rule that makes it work: where the blind pass flagged something the context explains, **keep the finding** and mark it `Explained by context`, stating the explanation. Do not delete it. The external reader is blind too, so a finding that only your project file dissolves is still a real weakness in the artefact.

Where the two passes disagree on substance, say which you trust and why. Do not average them.

**A reconciled entry, filled in** (the example is self-referential: it comes from reviewing an early draft of this very deny-list pattern, so do not go hunting for the "four files"):

```markdown
### F-04 · Material · § "Scope" · Explained by context
**Blind pass.** "the four files listed above" — the reader has no four files.
The deny-list block reads as a copy-paste that will not fit their case.
**In context.** True: that phrasing is a leftover from the project this
pattern came from, where there genuinely were four documents.
**Kept because.** Every reader outside that project hits the same wall.
The context explains where it came from, not why it should stay.
**Fix.** Replace with "the files listed above" and bracket the
project-specific nouns as slots.
```

That is the shape of a finding the context dissolved and you kept anyway. If your reconciled report has none of these, either the artefact is unusually self-contained or the reconcile pass quietly deleted them.

### When to use it

| Situation | Blind pass? |
|---|---|
| Output goes to someone outside your context — client, counterparty, regulator, new hire, the public | Yes |
| Documentation, onboarding material, a published guide | Yes |
| A deliverable you have iterated on for weeks and can no longer read freshly | Yes |
| Code inside its own codebase, where local convention is the point | No — context is the standard here |
| Anything cheap to fix after the fact | No — not worth the tokens |

### Controlling the noise

A blind reviewer will flag things that are fine. Three instructions keep the report usable:

1. **A severity scale with a floor**, defined by what you should do about it: **Blocker** (do not send) · **Material** (send only after fixing) · **Minor** · **Nit**. Require all Nits grouped into one entry rather than one section each.
2. **Anti-padding.** "Do not pad the report with findings that would not change the outcome." Absent that instruction, reports tend to run long, because volume reads as effort.
3. **A `Verified clean` section.** List what was checked and found correct. Without it, an empty finding list is indistinguishable from a check that never ran.

### When the artefact is too big

If the deliverable will not fit one reviewer, split by document or by section rather than summarising it first — a summary is context of the wrong kind, generated by exactly the session you were trying to exclude. Give each reviewer a whole, self-contained piece and reconcile across them.

---

## Build the Prompt in One Session, Run It in Another

For a task that is high stakes and roughly one-shot, the prompt is worth treating as its own deliverable.

### Stage 1 — Design session

Bring the mess. Constraints, prior mistakes, things that must not be touched and why, what the output has to look like, who reads it. Ask Claude to interview you, then produce the prompt as a standalone file.

A prompt-review skill can do this if you have one installed ([Guide 03](./03_SKILLS.md) covers skills); otherwise use the fallback prompt below:

> "I need to write a prompt for [task]. Before drafting, ask me the questions you need answered to write it well. Then produce the prompt as a standalone file I can run in a clean session — it must work for someone who was not part of this conversation."

That last clause is the whole test.

### Stage 1b — Critique is not the prompt

Here is the step that gets skipped. A prompt-engineering pass returns a *critique*: what is vague, what is missing, which constraint is unstated, what the output schema should include. That is advice, not a prompt. If you stop there you have a list of improvements you now have to apply yourself, by hand, under exactly the conditions that produced the weak prompt in the first place.

Ask for the finished prompt explicitly:

> "Now write the prompt itself, incorporating everything above. Output the complete prompt as a single block I can copy and run, not a description of what it should contain."

Two things to watch:

- **The critique stays behind.** The reasoning that produced the prompt is context for you, not for the run session. Only the prompt travels. If the final block says "as discussed above" or "per the constraint we identified", it is not standalone yet.
- **Check what silently dropped.** A prompt rebuilt from a critique tends to lose constraints that were in your original but outside the critique's field of view. Diff the new prompt against your original requirements, not against the critique.

### Stage 2 — Run session

Run the prompt clean. **Not in the session that wrote it** — that session still remembers every clarification you made while writing, including the reasoning you deliberately left out of the final text. You would be testing the conversation, not the prompt.

### Stage 3 — Keep it

The prompt is now a file. Save it, version it, and edit it when a run disappoints. Expect to run it more than once: the first run is usually what tells you what the prompt failed to say.

### When it is done

Not when it is long. When someone who was not in the design session could run it and get what you wanted. Length is a symptom, not the goal — good long prompts are long because nearly every line encodes a decision someone actually made. A prompt that is long without that is just failure mode 2.

### When not to bother

Routine work, anything cheap to redo, anything you will iterate on interactively anyway. The two-stage workflow costs a session. It pays off when the output is expensive to get wrong and you get roughly one attempt.

---

## Anatomy of a One-Shot Prompt

A skeleton, as slots. Fill each with real decisions from your case; do not keep the generic phrasing.

```markdown
# [What this run produces]

## Role and stake
Who Claude is acting as, what expertise applies, who the audience is, and what
happens if this is wrong. One paragraph. This calibrates severity judgments.

## Scope
Exactly which artefacts are in scope. How to resolve which version is current
(highest version number, most recent mtime, a named file). What to ignore
(lock files, drafts, archives).
Require the run to open by listing the files and timestamps it actually read.
If an on-disk copy looks stale or a file is open in another app, say so rather
than guessing.
(This header is self-reported, so it catches honest mistakes, not dishonest
ones. Spot-check it against the folder when the stakes are high.)

## Hard rules
Each rule gets three things: the rule, the reason, and the price of breaking it.
Then a sanctioned way to challenge it.

  Example shape:
  "Never do X. Reason: it converts A into B, costing roughly [amount / harm].
   If you believe X is nonetheless required, report it as a finding with the
   consequence priced in. Do not silently do it."

Rules without reasons get followed literally in cases they were not meant for,
or quietly dropped. Rules without an escape hatch force a choice between
obedience and undisclosed violation.

## Method
The passes, in order, and what each one may see.
For any blind pass: the explicit deny-list, plus the file-list requirement.
For the reconcile pass: the keep-and-mark rule.

## Dimensions to check
The things to check, as named categories rather than prose. One line each.
This is the part that is entirely domain-specific.

## Known traps
Places this exact work has gone wrong before. Specific, not general.
"Section numbers in this file are frequently misremembered: the correct ones
are X, Y, Z" beats "be careful with citations."
This is where the corrections you have saved in memory (Guide 04) earn their
keep — pointed at the exact spot rather than stated as a general principle.

## Verification of external claims
Which claims must be checked against a primary source, and where.
Require the source to be quoted, and require anything unconfirmed to be marked
UNVERIFIED rather than dropped. Silent omission hides the boundary of what
Claude actually knows.

## Output
The exact file path and format.
The finding schema, shown as a filled-in example, not described:

  ### F-03 · [Severity] · [Location] ↔ [Other location]
  **Finding.** What is wrong, in one or two sentences.
  **Where.** File, section, which sentence.
  **Why it matters.** The consequence, concretely.
  **Basis.** Source, quoted, with a link.
  **Proposed fix.** The replacement text.
  **Pass.** Blind / in context / both.
  **Confidence.** High / medium / low, with the reason.

Severity levels, defined by what the reader should do:
Blocker (do not send) · Material (send only after fixing) · Minor · Nit.

## Closing sections
- **Verified clean** — what was checked and found correct, listed explicitly,
  so silence is never ambiguous.
- **Open questions** — phrased as decisions for a human to make, not hedges.
- **Verdict** — one line.

## Discipline
Distinguish throughout between what the artefact says, what the project file
says, and what Claude concludes.
Do not pad with findings that would not change the outcome.
Where you do not know, say so.
```

Two of these slots do most of the work. **Rules that carry their price** are what let Claude reason at the edges instead of guessing which way to fail. **Verified clean** is what makes the report trustworthy, because it converts silence from ambiguous to meaningful.

---

## Anti-Patterns

**"Use a subagent for fresh eyes."** Without a deny-list this is theatre — the subagent reads CLAUDE.md like everyone else. With only a deny-list it is a request, not a boundary; stage a copy when it matters.

**Discarding blind findings the context explains.** The most common way to waste the pattern. Those findings are the deliverable, not the noise.

**Blind-passing everything.** Context is usually the right answer. Reserve this for output that leaves your context.

**Generic prompt skeletons, filled in generically.** A prompt built from the template above with no real decisions in it is unlikely to beat three clear sentences. The structure is a place to put specifics, not a substitute for having them.

---

## Checklist

Before a high-stakes run:

- [ ] Decide explicitly what this session should and should not see — do not let the folder decide
- [ ] If the output leaves your context, plan a blind pass
- [ ] Write the blind brief with an explicit deny-list, and require it to report which files it opened
- [ ] Stage a copy of the artefact outside the project if the finding actually matters
- [ ] Include the reconcile rule: keep blind findings the context explains, marked
- [ ] Give every hard rule a reason, a price, and a sanctioned way to challenge it
- [ ] Require a provenance header: which files, which versions, which timestamps
- [ ] Show the output schema as a filled-in example
- [ ] Require `Verified clean`, open questions as decisions, and a one-line verdict
- [ ] Add an anti-padding instruction
- [ ] Ask the design session for the finished prompt as a copyable block, not a critique
- [ ] Check the finished prompt is standalone — no "as discussed above", no dropped constraints
- [ ] Run the prompt in a clean session, then save it as a versioned file
