# Independent Judgment: Getting an Answer Instead of Your Own View Reflected Back

> Claude is disposed to agree with you, and you are constantly telling it what you think without meaning to. Every framing, every "I have some concerns", every question phrased as *would this work?* moves the answer toward the one you already hold. This guide is about the prompts and protocols that get you a judgment Claude reached on its own — and about how much independence those protocols actually buy, which is less than it feels like.

> **Companion guides:** [Guide 26](./26_CONTEXT_SCOPING.md) is the closest neighbour and the boundary matters. Guide 26 covers contamination from the *environment* — Claude knows something your reader will not, so the defect never surfaces. This guide covers contamination from *you* — Claude knows what you think, and converges on it. Guide 26 owns the artefact-review workflow (deny-lists, staged copies, the blind → in-context → reconcile passes); this guide owns why your own input biases an answer and what to do about it, in review and in ordinary conversation alike. [Guide 02](./02_PROMPTING_BASICS.md) covers instruction quality. [Guide 20](./20_INTERACTIVE_PROMPTING.md) covers session mechanics. [Guide 04](./04_MEMORY_AND_PROFILE.md) matters here too: a saved preference is a standing opinion Claude reads before it answers.

> **Giving this guide to Claude:**
> "Read 27_INDEPENDENT_JUDGMENT.md. I want an independent read on [decision / document / plan] and I have already formed a view. Set up the protocol — tell me what to withhold, what to ask for, and in what order."

---

## The Problem, Stated Precisely

Two separate things go wrong and they need different fixes.

| # | Mechanism | What it looks like | Fix |
|---|---|---|---|
| 1 | **Anchoring** | You state or imply a view. Claude's answer lands near it. You read the agreement as corroboration. | Withhold the view until Claude has committed. |
| 2 | **Agreement pressure** | You ask Claude to evaluate *your* proposal. It grades your work rather than solving the problem, and grades generously. | Change the task: ask for the answer, not a verdict on yours. |

They compound. Ask "I'm planning to do X, would that work?" and you have done both at once: anchored on X, and set the task to *assess X* rather than *find the best approach*. The reply will be a qualified yes with two improvements attached. That reply is nearly content-free, and it is the single most common shape of exchange people mistake for validation.

**The tell that you have done it:** your prompt contains your answer. If Claude can extract a proposal from your message, you are asking for a grade.

---

## What Leaks, and How Much

Withholding your conclusion is not the same as withholding your view. Most leaks are structural rather than stated.

| What you say | What Claude infers |
|---|---|
| "I've read it and have some observations." | Findings exist and are findable. Raises the hit rate on invented ones. |
| "What's wrong with this?" | Something is wrong. Finding nothing is a failed answer. |
| "Is this any good?" | A verdict is wanted. Severity gets flattened into a thumbs. |
| "I think the risk is in section 3." | Section 3 gets the scrutiny; sections 1, 2 and 4 get skimmed. |
| "We already decided on X, but review the doc." | X is out of scope for criticism, including where the doc's problems come from X. |
| "Review this before it goes to the client." | Stakes are high; the audience is external. **This one is useful and should stay.** |

The last row is the distinction to hold on to. Context about *stakes and audience* calibrates severity and belongs in the prompt. Context about *your conclusions* biases the finding and does not. Guide 26's failure mode 1 applies here as sharply as anywhere: strip too much and you get a generic review of a document Claude does not understand the purpose of.

**Existence priming is the underrated one.** A reviewer told that problems exist will produce problems. Say nothing about whether you have read the thing. "Review this document; it goes to a regulator on Friday" is complete. Adding "I spotted a few issues but want your read first" costs you the independence you were trying to buy, in the very sentence where you were trying to buy it.

### The neutral ask

Cheap and worth making the default. Instead of a single directional question, require both directions and a hostile one:

> "What does this do well that must survive editing, what does it do badly, and where would a motivated critic attack it?"

Three lenses in one prompt, none of them leading. The first clause is doing real work: without it, a review has no way to report that something is fine, so everything gets framed as a deficiency.

---

## Ask for the Artefact, Not a Verdict

This is the everyday fix and it costs nothing. Rather than presenting your answer for evaluation, present the problem and ask for answers.

| Instead of | Ask |
|---|---|
| "I'm thinking of doing X. Would that work?" | "I need to achieve [goal] under [constraints]. Propose two or three approaches, rank them, and give the failure mode of each." |
| "Is this the right structure for the doc?" | "Here's the audience and what they need to decide. What structure serves that? Then tell me what my current structure costs." |
| "Does this rule make sense in my CLAUDE.md?" | "Here's the behaviour I keep having to correct. Write the rule." |
| "I think we should use approach A over B." | "Here are the constraints. Which of A or B, and what would change the answer?" |

Then reveal. Once Claude's proposal is on the table, compare:

> "Here's what I was planning: [your approach]. Where does it sit against what you proposed? Name anything mine handles better and anything it misses. If yours is better, say so plainly."

You lose nothing by ordering it this way. You still get your idea evaluated. You just get it evaluated against something rather than against nothing, and by a Claude that had to think before it knew what you wanted to hear.

**When to skip this.** Most conversation. Routine work. Anything where you want help executing a decision that is already made and not up for debate — asking for three alternative approaches to a settled question wastes a round trip and invites Claude to relitigate it. The protocol is for decisions that are still open and expensive to get wrong.

---

## Commit, Then Reveal

For anything where you have a formed view and want a real second opinion, the ordering has to be enforced rather than intended.

**1. Claude commits in writing, before you say anything.** Not "let me hear your take first" — an actual artefact: a file, or a message that names findings with locations and severities. A verbal answer in an open conversation is cheap to walk back and the walk-back is invisible. A written list has to be visibly contradicted.

**2. You reveal.** Your findings, your view, in full.

**3. You reconcile.** Covered below.

The commitment step is where people cut the corner, and cutting it dissolves the whole protocol, because a Claude that has not committed will not disagree — it will incorporate. Requiring locations and severities is part of the commitment: a finding pinned to a section and rated *Material* is much harder to quietly soften than "yes, the structure could be tighter".

### A reusable review prompt

Keep this as a file or a skill ([Guide 03](./03_SKILLS.md)) rather than retyping it. Retyping is how your current mood about the document gets into the brief.

```markdown
Review the attached document. Do not ask me questions before starting.
I will not tell you my own view until you are done.

Three passes, different lenses. Do not let a later pass soften an earlier one.
1. Does it do what it claims? Argument, evidence, internal consistency, gaps.
2. Will the intended reader act on it? Structure, clarity, what they will misread.
3. Hostile read: where would a motivated critic attack, and would they land a hit?

Audience and stakes: [fill in — this calibrates severity and is not a leak]

Per finding, give:
- Location (section, and which sentence)
- What is wrong
- Severity: Blocker (do not send) / Material (fix first) / Minor / Nit
- Confidence: high / medium / low
- What evidence would make you drop this finding

Close with:
- The two things you would fix first
- One thing the document does well that should survive editing
- Verified clean: what you checked and found correct

Do not pad with findings that would not change the outcome.
Write this to [path] before we discuss anything.
```

**The "what would make you drop this" line is the highest-value one.** It converts an opinion into a testable claim. At reconcile time you are then checking evidence rather than negotiating between two verdicts, which is what turns a disagreement into a resolvable question. It also exposes findings that have no test behind them, which are the ones worth discarding.

---

## Blinded Reconciliation

Guide 26's reconcile pass has the main session arbitrate between a blind report and an in-context one, keeping blind findings the context explains. Everything there still applies. This guide adds one rule to it.

**The arbiter must not know which list is yours.** In the usual setup it does: the reconcile happens in the session where you stated your view, so authorship is obvious and the finding you argued for gets deference. Fix it in two moves, both cheap:

1. **Run the reconcile in a fresh session.** Not the one that produced either list.
2. **Anonymise and shuffle.** Label them A and B. Do not say which is which. Do not mention that one is human and one is Claude — that alone shifts the treatment.

Then ask symmetrically:

> "Two independent reviews of the attached document, A and B. I am not telling you where either came from. Match findings by location in the document, not by number. For each: keep / drop / needs checking, with the reason. Where they conflict, say which you trust and why — do not average them. Then list anything neither caught."

That last clause earns its place surprisingly often. Two reviewers converging on the same six findings both missed the seventh, and an arbiter looking only at the union will never look for it.

**On findings the context explains:** keep Guide 26's rule. If the blind list flagged something your project knowledge dissolves, it stays, marked as explained. Your reader is blind too.

---

## False Independence

This is the part that changes what you should conclude, and it is the reason a two-reviewer setup can leave you more confident and no better informed.

**Two Claude instances are not two opinions.** They share weights, training, and priors. When they agree, the agreement is largely *correlated error*: they are wrong in the same places for the same reasons. Running the same prompt twice and getting the same answer tells you the answer is stable, not that it is right, and stability is very easy to mistake for corroboration once you have two documents in front of you saying the same thing.

Independence levers, ordered by how much they actually buy:

| Lever | Independence gained | Notes |
|---|---|---|
| Same prompt, second run | Almost none | Confirms stability only. Do not read agreement as evidence. |
| Different lens, persona, or rubric | Some, and it is cheap | The reviewers are looking for different things, so they can miss differently. Best value per token. |
| Different model or model tier | More | Different priors and failure modes. Worth it for high-stakes calls. |
| A human who is not you | Most | Still the gold standard. The protocols here are what you use when a human is not available, not a replacement for one. |

Two practical consequences.

**Do not count votes; read reasons.** Three agreeing reviewers with the same lens are one reviewer. A finding that survives *because a skeptic tried to refute it and failed* is worth more than a finding three instances happened to list. When you want adversarial pressure, prompt for refutation explicitly and give the refuter a bias toward finding the claim unsupported.

**A subagent briefed after you spoke is not blind.** Guide 26 covers the subagent trap on the file-access side: a subagent inherits CLAUDE.md and can read the whole folder. There is a second channel on this side. If Claude writes the subagent's brief *after* hearing your view, your framing gets encoded into that brief — the subagent is uninformed about the project and perfectly informed about your opinion, which is the worst of both. Two defences: write the brief before you say anything, or keep it as a fixed file you reuse verbatim. If Claude drafts a brief for you, read it for your own fingerprints before it runs.

**And memory leaks too.** A saved preference or a past correction ([Guide 04](./04_MEMORY_AND_PROFILE.md)) is a standing statement of your view that loads before the conversation starts. Mostly that is the point. But if you are asking for an independent read on a question your memory files have an opinion about, the blind pass is not blind, and no deny-list in the prompt changes what already loaded.

---

## Making It Standing

The temptation is a CLAUDE.md line saying "be objective" or "don't just agree with me". It does very little, for the reason [Guide 02](./02_PROMPTING_BASICS.md) gives in Mistake 3: it describes a disposition, not a behaviour, so Claude has to infer what to actually do. It also tends to produce theatre — a token disagreement offered to satisfy the rule.

Standing rules that specify a behaviour work better:

```markdown
When I propose an approach, state the strongest objection to it before
saying whether you agree, and say whether that objection is fatal.

When I ask whether something will work, answer the underlying question
first — what would actually work — then assess my version against that.

If I ask you to review something and tell you I have already formed a
view, do not ask what it is. Review it, then ask.
```

Each of these names an action, and the third is the load-bearing one: it makes Claude decline the leak rather than relying on you never offering it. Note the honest limit — these are requests, not boundaries, the same limitation Guide 26 names for deny-lists. They raise the floor; they do not guarantee the behaviour. The protocol steps above (a written commitment, a fresh session, anonymised lists) are what actually enforce anything, because they change what Claude *can* see rather than what it is asked to ignore.

Put the review protocol in a skill rather than in CLAUDE.md. It applies to one workflow, not every interaction, and a skill can carry the whole prompt including the finding schema.

---

## Anti-Patterns

**"I have some thoughts but you go first."** Feels neutral, is not. It tells Claude that findings exist, which is most of what it needed to manufacture some.

**Treating agreement between two Claude runs as corroboration.** Correlated error reads exactly like consensus and is the most confidence-inflating mistake in this guide.

**Reconciling in the contaminated session.** The arbiter knows which findings are yours and defers to them. The whole comparison is then a formality.

**Blinding everything.** Context is usually right. Guide 26's table on when a blind pass is worth it applies unchanged; this guide adds no reason to blind more often, only to blind more honestly.

**Asking for a critique when you needed a decision.** Guide 26 makes this point about prompts; it holds for reviews too. "Tell me what's weak about my plan" returns a list of weaknesses. If you want the better plan, ask for the plan.

**A standing "be objective" rule, and nothing else.** Unfalsifiable, unenforceable, and it makes the setup feel handled.

---

## Checklist

Before asking for a judgment you intend to rely on:

- [ ] Check whether your prompt contains your answer — if it does, you are asking for a grade
- [ ] Say nothing about having read it, or about findings existing
- [ ] Keep the stakes and audience in the prompt; keep your conclusions out
- [ ] Ask for the artefact (approaches, findings, the plan), not a verdict on yours
- [ ] Require a written commitment — locations, severities, confidence — before you reveal anything
- [ ] Require "what would make you drop this" per finding, so reconciling checks evidence rather than opinions
- [ ] Ask for what the thing does well, not only what is wrong
- [ ] Vary the lens between reviewers rather than repeating the prompt; a second identical run buys nothing
- [ ] Reconcile in a fresh session, with the two lists anonymised and shuffled
- [ ] Ask what neither review caught
- [ ] Check whether memory or a saved preference already states the view you are trying to withhold
- [ ] Before trusting a subagent's independence, check its brief for your fingerprints
- [ ] Read reasons, not vote counts
