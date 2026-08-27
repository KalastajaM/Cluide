# Specify Before You Rebuild: Turning a Grown Artefact Into One With a Stated Contract

> Anything built by asking Claude for one thing at a time eventually reaches a state where each new change costs more than the last, and the fixes start protecting each other. At that point another fix is the wrong move. This guide is the manoeuvre for that point: write down what the thing must do, keep the running version as the only evidence you have about whether the new one is right, and stay honest about which parts of that evidence are wrong.

> **Companion guides:** [Guide 22](./22_HELPER_APPS.md) covers a small self-built tool while it is still healthy — invariants, a helper index, verification gates. This guide is what to do when those stop holding. [Guide 13](./13_DEV_EXECUTION_WORKFLOW.md) is the day-to-day loop this interrupts. [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) and the `dispatch` skill run the audit fan-out; [Guide 26](./26_CONTEXT_SCOPING.md) scopes each pass and [Guide 27](./27_INDEPENDENT_JUDGMENT.md) is how you get the spec checked without hearing your own view back. [Guide 07](./07_TASK_LEARNING_GUIDE.md) has the same pathology inside a task's learning log. [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) is where most of the prevention in §5 actually lives.

> **Giving this guide to Claude:**
> "Read 29_SPEC_BEFORE_REBUILD.md. [Artefact] has grown ad hoc and I am deciding whether to keep patching it or respecify it. Run §1 first and tell me which trigger signals are actually present, with counts."

**This is not only about code.** A CLAUDE.md that accreted over a year, a set of skills with overlapping triggers, a scheduled task whose improvements log outgrew the task itself — all of these are artefacts whose behaviour is defined only by their current implementation, and all of them reach the same wall. The examples below alternate deliberately.

---

## 1. The Trigger: Compensating Machinery

Do not run this on a hunch that something feels messy. The signal is **compensating machinery**: work the artefact does to protect itself from its own design, which would have no reason to exist if the design were right.

| Signal | What it looks like in a tool | What it looks like in an assistant setup |
|---|---|---|
| Repair shipped as a feature | A "fix links" button users are told to press | A rule whose job is to undo what another rule causes |
| One rule, *n* implementations | The same date parsing in four files | The same convention stated in CLAUDE.md, two skills and a task |
| A fix that took several attempts across several surfaces | One bug chased through three screens | The same correction given four times in four sessions |
| An invariant documented but unenforced | "callers must sort first" in a comment | "always check X before Y" with nothing that makes skipping it visible |
| Volume grows, confidence does not | More tests, same fear of changing it | More rules, same rate of correction |

**Count them from history, do not argue from taste.** `git log`, the improvements log, your own corrections. The output of this step is a number per class — *twelve incidents trace to this one gap, six to that one* — because that number is the only honest argument for spending the rebuild, and because a class you cannot count is usually a preference rather than a defect.

**When not to do this.** The artefact is small enough to rewrite in an afternoon: rewrite it. The defects are independent rather than tracing to two or three shared roots: fix them. You want it different rather than correct: that is a redesign, and it does not need an oracle or a spec of the old thing. This manoeuvre is expensive, and its whole value is in cases where the expense is smaller than continuing.

---

## 2. Audit Before You Specify

The specification is written **from the artefact**, not from memory or from what you meant to build. That means an audit first, and the audit has its own rules.

**Orthogonal dimensions, shallow before deep.** Passes that overlap produce agreement that means nothing (see [Guide 27](./27_INDEPENDENT_JUDGMENT.md) on correlated error). A workable spread: an inventory of what exists, a structural pass on what depends on what, a history pass on what broke and how often, a data-safety pass on where information can be silently lost — and only then deep extraction of the rules that turned out to matter. The deep passes are targeted by what the shallow ones found; running them first wastes the expensive tier on the wrong subject.

**Every load-bearing claim is verified first-hand.** A claim that arrived through a summary of a summary is not evidence. If a subagent reports that a rule exists in three places, the synthesis step opens all three. This is the single most common way a confident spec turns out to be describing a system nobody has.

**Findings are logged, not fixed.** This is the rule people break, and it costs the most. You are about to make the current version your measuring stick (§6); repairing it mid-audit moves the stick while you are measuring against it. There is a second reason that matters more in practice: a session that starts fixing stops auditing, and comes back with three fixes and half a map.

**Dispatch.** This is a natural fan-out — see [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) and the `dispatch` skill. Inventory, counting and mechanical sweeps go to the cheap tier; the rule extraction and the synthesis that turns findings into a spec do not. Scope each pass with [Guide 26](./26_CONTEXT_SCOPING.md) so a pass looking for duplication is not also reading your opinion of the design.

---

## 3. Write It Normative

**Declare which kind of document it is, in the first paragraph.** A descriptive spec ("here is what it does") is an inventory: accurate, and useless to build against, because it faithfully reproduces the defects. A normative spec ("here is what it must do") is buildable and immediately disagrees with the thing on disk. Every disagreement is then either a defect you are choosing to correct, or a behaviour nobody wrote down — and both need resolving.

**Mark every divergence inline, at the rule it contradicts**, with three fields and nothing else:

```markdown
> ⚠️ **DIVERGES FROM v1** — what the current version does, why that is wrong,
> what the new version must do instead.
```

Inline placement is not cosmetic. A separate defect list gets read once; a marker sitting under the rule it contradicts is read by whoever implements that rule, at the moment they would otherwise reproduce the defect. These markers also become load-bearing later: §6 uses them to decide which disagreements between old and new are expected.

**The completeness test:** someone can build the new version from the spec **without reading the old one**. Apply it rule by rule. A rule you can only understand by opening the source is not specified yet, and the gap is usually where the interesting behaviour lives.

**For a non-code artefact** the same shape holds. The spec of an assistant setup states the behaviours the setup must produce, which surface owns each one, and what must never happen — not the current text of the files. "Corrections to figures are made in the owning project and referenced elsewhere" is a rule. "CLAUDE.md line 34 says to check the tracker" is an inventory entry.

---

## 4. Decide in the Open

A spec that hides its decisions gets relitigated every time someone reads it. Give each one four fields:

| Field | Why |
|---|---|
| **Statement** | One line, in the imperative |
| **Status** — Locked or Recommended | Locked is not up for debate during the build; Recommended is a default that may be revisited at a named point |
| **Cost** | What the decision demands in discipline, work, or capability given up. A decision with no stated cost has not been examined |
| **What would reopen it** | The condition under which the decision becomes wrong |

Three habits sit on top of that, and all three are worth stealing:

**Promotion is forced by usage.** If three other sections already assume a Recommended decision, it is not recommended, it is Locked and mislabelled. Sweep for this before you call the spec finished: either promote the decision or remove the assumptions, but do not ship a document that quietly depends on a choice it says is optional.

**When the choice is genuinely open, fix the criteria now and the choice later.** Record the constraints the eventual pick must satisfy, the shortlist, and the milestone at which it gets decided. That is a real decision — it forecloses everything outside the constraints — and it stops the open question from blocking work that does not depend on it.

**Keep a settled-questions ledger, and close it.** Every question the first draft raised, with the date it was settled, the answer, and a pointer to the section where the answer now lives. The spec is not finished while the ledger has open entries. This is the cheapest possible guard against the failure where the answers were reached in conversation and exist nowhere afterwards.

---

## 5. State What Must Be True

### Prevention beats detection, and the ratio is the argument

A rule is a **check**: it catches the mistake after it has been made, and it fails silently when attention or context runs short. Structure is a **schema**: it makes the mistake unconstructible. The rebuild is worth doing to the extent it converts the first into the second.

| Failure | As a check | As structure |
|---|---|---|
| Personal data reaches a public repo | "Do not commit personal data" | One gitignored folder that everything non-shipping lives in, so there is no ignore rule to forget ([Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md)) |
| Two projects state the same figure differently | "Remember project X owns this" | One owner, and a pointer everywhere else ([Guide 23](./23_MULTI_PROJECT_SETUPS.md)) |
| A skill triggers on the wrong kind of request | "Only use this for real estate matters" | A description whose trigger set cannot match the other kind ([Guide 03](./03_SKILLS.md)) |
| A task writes a figure it should have computed | "Always recompute from source" | A template with no field to paste one into |
| A session acts on a stale copy | "Check freshness first" | Nothing is copied; the only reachable form is the live one |

Then build the table that justifies the whole exercise:

| Failure class | Incidents | Mechanism in the new version | Level |
|---|---|---|---|
| … | count from §1 | … | structure / check |

**The ratio is the finding.** If most classes are still prevented by a check, the rebuild is a rewrite of the same design and will regrow the same machinery. That is a reason to go back to §3, not a reason to start building.

### The corollary for anything that learns

A learning log ([Guide 07](./07_TASK_LEARNING_GUIDE.md)) accumulates one rule per incident. Left alone long enough it becomes a defect-driven specification in prose: it records what went wrong rather than what must be true, it is over-fitted to its own history, and it is hostile to any redesign because nobody can tell which entries still matter. Distil it periodically — restate the accumulated fixes as the handful of properties they are instances of, keep the properties, archive the instances. A rule that is a past incident restated is the thing to drop.

---

## 6. Prove It

### The old version is the oracle — keep it running

The single most valuable asset in a rebuild is the thing you are replacing, because it is the only available answer key. Run both on the same real inputs and reconcile. **Do not delete or disable the old version until the reconciliation is done**, and resist the pull to "just start clean": clean means no evidence.

### It is knowingly wrong, so reconcile three ways

| Verdict | Meaning | Action |
|---|---|---|
| **Match** | Both agree | Nothing |
| **Expected divergence** | They disagree at a point the manifest names | Assert the difference matches that entry's predicate |
| **Unexplained divergence** | They disagree anywhere else | **Stop.** Either the new version is wrong, or the old one has a behaviour nobody wrote down |

The third row is the entire point. A two-way diff cannot express "we expected this one", so it degrades into a list somebody eyeballs, and eyeballing is where the real defects get filed as noise.

**The manifest is a file, not prose.** The divergence markers from §3 are for humans; a reconciliation needs entries something can compare against — an id, the marker it comes from, the predicate (an exact expected value where computable, a direction otherwise), and every downstream surface the divergence reaches. That last field is what makes the check strict: a difference on a surface no entry names is Unexplained even when its cause is obvious elsewhere.

**Divergences split two ways.** One is *data-shaped* — the old version holds bad entries — and is neutralised at source by repairing the old data before comparing, after which everything downstream simply matches. The other is *behaviour-shaped* — the old version computes or decides differently from clean inputs — and cannot be fixed at source, so it must be enumerated.

**Tolerance is zero and stays zero.** Small unexplained differences get investigated one at a time and promoted to manifest entries with exact predicates. None is waved through as "probably rounding" or "close enough". This rule exists because explaining away a near-match is the default behaviour of both people and models under time pressure, and because the near-misses are where the interesting defects hide.

### Fixtures are computed before the new version exists

Write the scenarios down first — the awkward, several-things-at-once cases — with their expected results **derived by hand from the spec**, before there is an implementation to ask. Otherwise the expected values get read back out of the new version, and the check proves only that the new version is deterministic.

State the tie-break in the fixture file itself: if a generated result contradicts a hand-computed one, either the implementation is wrong or the fixture is, and the disagreement is settled on paper before either is changed.

### Check the whole output, not the part you touched

The most expensive defects keep the output *self-consistent while wrong* — one quantity converted in one place and displayed in another, a figure that is wrong identically everywhere. Per-surface checks pass straight over that class. Capture every derived surface at once, and keep at least one end-to-end check that crosses several surfaces in a single run, because nothing smaller can see it.

### Run it where the failure is visible

A green check proves nothing if it ran in the one configuration where the failure cannot appear. The canonical example is a date bug that passes in UTC and fails everywhere else, but the general form is broader: a locale, a timezone, an empty folder, a first run with no history, a session with a different set of connectors. Pick the configurations that make each class visible and run all of them.

### When there is no oracle

Sometimes the old version cannot be run side by side, or was never deterministic enough to compare — most assistant setups are in this position for anything subjective. Say so in the spec rather than pretending. Two substitutes, and they are weaker: hand-computed fixtures carry the whole load, so write more of them; and where output is judgement rather than a value, run the same inputs through both and have a third session compare the results blind, per [Guide 27](./27_INDEPENDENT_JUDGMENT.md).

---

## 7. Sequence It

Milestones are defined by **exit criteria, not dates** — a milestone is done when something demonstrable is true, and "we spent two weeks on it" is not that.

Two ordering rules earn their place:

**Put the first reconciliation run as early as it can possibly go.** It is the earliest hard evidence that the rebuild is on track, and every milestone after it is cheaper for having it. A plan that leaves reconciliation until the end has no feedback until the point where feedback is unaffordable.

**Everything is re-earned.** Nothing carries into the new version because it exists. Each feature, rule, skill or file is either specified in §3 or it does not come across. This is where most of the size reduction comes from, and it is much easier to enforce as a default than as a series of individual deletions.

---

## 8. Keep the Spec Honest

A specification nobody trusts is ignored; one that is trusted while quietly wrong is worse than none. Make its checkable claims checkable:

- **Every cross-reference resolves.** A reference to a section that no longer exists means the document is lying about itself, and it is the first symptom of a spec that has drifted.
- **Every count the document states about itself is asserted mechanically.** "Eleven cross-cutting rules", "83 markers", "the four homes" — these are exactly the claims that drift through an otherwise clean edit, because nobody re-counts while changing something else.

Both are a few lines of script, and they belong in whatever gate the project already runs. This applies to any document set with internal structure, not only to a rebuild spec; Cluide runs the same two checks on itself.

---

## 9. Worked Example: Respecifying an Assistant Setup

A setup grown over a year: one CLAUDE.md, eleven skills, four scheduled tasks. The complaint is that Claude behaves inconsistently and the fixes have stopped working.

**§1 — trigger.** Two skills whose descriptions both match "draft a message"; a CLAUDE.md rule added to suppress a behaviour a different rule causes; the same convention stated in CLAUDE.md, in two skills and in a task; eight corrections in the last month, five of them the same correction. That is compensating machinery, and it is counted rather than felt.

**§2 — audit.** One pass inventories every standing rule with the file it lives in. One counts corrections from conversation history by type. One maps which skills can trigger on the same request. Nothing is fixed; the eight findings go in a list.

**§3 — spec.** Normative: the behaviours the setup must produce, which surface owns each, what must never happen. Where the current setup does something wrong — a skill that fires on the wrong requests, a rule that contradicts another — that is marked inline with what it does, why it is wrong, and what must happen instead.

**§4 — decisions.** *Skills own workflows, CLAUDE.md owns standing behaviour* — Locked, cost: some duplication of context inside skills. *Memory holds preferences, not project facts* — Locked, reopens if project memory stops being available.

**§5 — prevention.** Of the five recurring corrections, three become structure: the overlapping skills merge so the ambiguous trigger cannot occur; the thrice-stated convention gets one owner and two pointers; the figure that kept going stale is never copied. Two stay checks, and that is written down as a known weakness rather than hidden.

**§6 — proof.** Ten representative prompts, run through the old setup and the new one. Six matched. Three are expected divergences — the manifest names them, each pointing at the marker that predicted it. One is unexplained, which stops the rollout until it is understood; it turns out to be a rule nobody knew was firing.

**§7 — sequence.** M0 the new CLAUDE.md, M1 the merged skills, M2 the first ten-prompt reconciliation, M3 the tasks. The reconciliation lands third, not last.

---

## Anti-Patterns

**Fixing during the audit.** Destroys the measurement and ends the audit. Log it.

**Deleting the old version before the reconciliation.** Throws away the only answer key you will ever have, usually in the name of a clean start.

**Reading expected values back from the new implementation.** Tests that the new thing is deterministic, and nothing else.

**A prose list of expected divergences.** Nothing can compare against it, so the comparison becomes eyeballing and the real defects get filed as noise.

**Waving through a near-match.** "Probably rounding" is the sentence this guide exists to prevent. Tolerance is zero.

**A descriptive spec presented as a design.** Faithfully reproduces every defect, and the fidelity reads as rigour.

**Rebuilding on aesthetics.** With no incident count, "this is a mess" is a preference, and the rebuild will regrow the same machinery around slightly different code.

**Calling the spec finished with open questions in it.** The answers then get made up independently, at implementation time, by whoever hits each one.

**Carrying something across because it exists.** Everything is re-earned, or the new version is the old version with better formatting.

---

## Checklist

Before deciding to respecify:

- [ ] Compensating machinery identified, with an incident count per class from history
- [ ] Checked that the defects trace to a few shared roots rather than being independent
- [ ] Confirmed the artefact is too big to simply rewrite, and this is correctness rather than taste

While specifying:

- [ ] Audit passes are orthogonal, shallow before deep, every load-bearing claim verified first-hand
- [ ] Findings logged, nothing fixed
- [ ] The document declares itself normative in its first paragraph
- [ ] Every divergence marked inline with what it does, why it is wrong, what must happen
- [ ] Someone could build from the spec without reading the old version
- [ ] Every decision carries status, cost, and what would reopen it
- [ ] No Recommended decision that other sections already assume
- [ ] The settled-questions ledger is empty before the spec is called finished

Before trusting the result:

- [ ] The old version still runs, and reconciliation is three-way, not a diff
- [ ] Expected divergences live in a machine-readable manifest naming every surface each reaches
- [ ] Tolerance is zero; every near-match investigated and given an exact predicate
- [ ] Fixtures hand-computed from the spec before the new version existed
- [ ] Checks capture every derived surface, not the one that changed
- [ ] Run in the configurations where each failure class is visible
- [ ] The prevented-versus-checked ratio justifies having rebuilt at all
- [ ] Cross-references resolve and self-claimed counts are asserted
