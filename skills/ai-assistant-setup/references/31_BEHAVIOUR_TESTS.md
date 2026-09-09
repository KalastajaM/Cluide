# Behaviour Tests: Checking That the Setup Still Does What You Built

> Every audit task in this repo reads a file and judges it. None of them asks the only question that matters: when you type the sentence you actually type, does the thing you built still happen? A CLAUDE.md rule can be perfectly written and silently stop holding — because a model changed, because a new skill now wins the trigger, because account memory accumulated a fact that reframes the request. Nothing in the file moved, so no audit notices. This guide is about testing behaviour rather than text: what a case looks like, how to run one, when to run the set, and what a failure means.

> **Companion guides:** [Guide 29](./29_SPEC_BEFORE_REBUILD.md) proves a *rebuild* against the old version as an oracle; this guide is the standing version of that proof, run against the setup you already have. [Guide 27](./27_INDEPENDENT_JUDGMENT.md) is why a model grading a model needs care (§6). [Guide 26](./26_CONTEXT_SCOPING.md) is why a test runs in a fresh session and never in the one you edited from. [Guide 07](./07_TASK_LEARNING_GUIDE.md) catches behaviour drift *inside* a scheduled task from its own feedback signals; this guide catches it from outside, on demand. [Guide 03](./03_SKILLS.md) and [Guide 01](./01_CLAUDE_MD.md) are what the tests protect. `tasks/review-platform-changes.md` checks whether Cluide's *guides* still match the platform; `tasks/setup-behaviour-tests.md` builds the suite that checks whether *your setup* does.

> **Giving this guide to Claude:**
> "Read 31_BEHAVIOUR_TESTS.md. List the rules in my CLAUDE.md and the skills in this project that would be embarrassing to lose silently, then propose a case for each in the §3 shape. Do not run anything yet."

---

## 1. Why the Audits Are Not Enough

An audit is a review of a definition. `audit-skill.md` reads a SKILL.md and judges whether its description would trigger; `audit-claude-md.md` reads CLAUDE.md and judges whether its rules are dead or over-long. Both are useful and both share a blind spot: they assume that a well-written definition produces the behaviour it describes. That was true the day you wrote it. It stops being true without any file changing, and there are four ways it stops.

**The model moved.** A model launch changes what a given instruction produces — longer or shorter replies, a different reading of "concise", a different threshold for asking versus acting. Anthropic's own [model migration guidance](https://platform.claude.com/docs/en/models/opus-5/migration-guide) for API users says to re-test prompt parsing, tool-use loops and refusal handling on each new model; there is no equivalent page for a Claude Code or Cowork setup, which is why this one exists.

**The platform moved.** A permission mode changes its default, a hook event gains a field, account memory starts loading into a surface where it did not before. Your instruction is the same; the surroundings it executes in are not.

**You moved.** The most common one. You added a skill last month whose description overlaps an older one, and now the older skill loses the trigger race for the phrasing you always used ([Guide 29](./29_SPEC_BEFORE_REBUILD.md) counts this as compensating machinery). You added an account-level rule that interacts with a project rule. You wrote a memory note that now reframes a class of requests. Every one of these was a deliberate change to something else, with a side effect on the thing you did not touch.

**Context accumulated.** Account memory, auto memory and the project's own memory files grow. A fact that is true and correctly stored can still change how a request is read — a stored preference for brevity, applied to a task that needed the long form.

None of these leaves a trace in the file an audit reads. The only way to see them is to run the behaviour and look. That is a test, and the rest of this guide is how to make one cheap enough to actually run.

---

## 2. What Earns a Test

Not everything. A personal setup needs a small suite, on the order of ten to thirty cases, and every case must be able to say what failure it protects against. Three classes earn a place:

**Trigger tests.** Does the skill fire on the phrasings you actually use, and stay quiet on the neighbours that should not fire it? The second half is the one people skip and the one that catches the trigger-race problem: a new skill that steals "draft a message" from an older one fails the older skill's positive case and the new skill's negative case at the same time, which is exactly the signature you want. In Claude Code, `/skill-doctor` (where your build has it) lists each skill's recent usage and warns on skills never invoked; a skill that has not fired in weeks is either unneeded or losing the trigger race, and either way is a candidate for a case.

**Rule tests.** Does a standing rule hold under a request that does not mention it? The dangerous request never names the rule: "tidy this up" against a controlled document ([Guide 30](./30_CONTROLLED_DOCUMENTS.md)), "send it" against a rule that says draft only, a request for an email against a rule about punctuation. Test the rule with the request that would violate it if the rule were absent, not with a request that restates the rule.

**Task tests.** A scheduled task run against a frozen input produces output of the expected shape — the sections present, the counts plausible, the actions it took within the ones it is allowed ([Guide 32](./32_ACTION_AUTHORITY.md)). Frozen means frozen: a fixture folder or an exported sample, never the live mailbox. Two reasons, and they are different from each other: a test pointed at live data can act on it, and live data changes under you, so a failure cannot be reproduced.

What does not earn a test: style preferences that cost nothing when they slip, anything you would not notice or mind, and rules you added speculatively and have never seen violated. A test is a claim that a failure matters. If you cannot name the failure, you do not need the test yet.

---

## 3. A Case Is a Prompt and Its Graders

Borrow the shape from the platform. As of September 2026, Claude Code's `claude plugin eval` (early access, enabled per organisation — the command exists and says so when it is not enabled) defines a case as a folder holding a `prompt.md` and a `graders/` directory. The layout and field names below are the ones that tool used at the time of writing; adopt the shape regardless, because it separates the input from the judgement and makes both greppable, and nothing in this guide depends on the names surviving. The suite is the same suite whichever runner executes it (§4).

The suite is a home [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) does not list. It holds definitions (the cases) and input data (the fixtures) that must never be read as project data, so it gets its own root and a line in the file map.

```
tests/behaviour/
  README.md                          ← what the suite protects, when it was last run, pass rates
  no-send-without-approval/
    prompt.md                        ← frontmatter: name, tags, runs; body: the request
    graders/
      no-send-tool.md                ← type: tool_used, tool: <send tool>, min: 0, max: 0
      draft-exists.md                ← type: file_exists (or a regex on the reply)
  finnish-draft-triggers/
    prompt.md
    graders/
      skill-fired.md
  finnish-draft-stays-quiet/         ← the negative case, always paired with the positive
    prompt.md
    graders/
      skill-did-not-fire.md
```

**The prompt is the sentence you would actually type.** Not a description of it. "Draft a reply to Anna saying Thursday works" is a test; "test whether the Finnish drafting skill triggers on a reply request" is a request for the model to grade itself, and it will.

**Graders are checkable or they are not graders.** The platform's grader types are a good taxonomy whether or not you use the tool: a `regex` on the last message or on a produced file, `tool_used` with a minimum and maximum count (a "must not call" is `min: 0, max: 0`), `tool_order`, `file_exists` over what the run created, and `llm` with written criteria for what cannot be expressed mechanically. Prefer them in that order. "Contains no em dash" is a regex. "Did not call the send tool" is a count. "Sounds like me" is an llm grader, and §6 is about why it is the weakest of the set.

**A case records why it exists.** One line in the frontmatter or the README: the date and the failure it was written against, or the rule it protects. [Guide 30](./30_CONTROLLED_DOCUMENTS.md) makes the same point about safeguards — a case with a story survives the next tidy-up; a case that reads as best practice gets pruned by someone in a hurry.

---

## 4. Three Ways to Run One

The suite is the same whichever way you run it. Pick by what you have.

**By hand, in a fresh session.** The floor, and the only option for a Cowork-only setup. Open a new session in the project — new, never the one you just edited in, because that session already holds your intent and will grade itself kindly ([Guide 27](./27_INDEPENDENT_JUDGMENT.md); [Guide 26](./26_CONTEXT_SCOPING.md) on what a fresh session does and does not clear) — paste the prompt, check each grader against what came back, record pass or fail in the suite README with the date and the model. A run of ten cases takes a quarter of an hour; the three-run rule below triples that, which is why the first baseline pass is one run per case and the repeats are reserved for the cases that were marginal and for regression runs on a rule you changed. This is not a lesser method; it is the same test with a slower runner.

**Scripted, with `claude -p`.** Claude Code's [print mode](https://code.claude.com/docs/en/headless) runs a single prompt and exits, and `--output-format json` gives a parseable result; `--json-schema` forces a structured verdict you can assert on, and `--model` pins the model so a failure is attributable. As documented at the time of writing, print mode without `--bare` runs hooks and loads MCP servers; check in your own build that it also loads the project's CLAUDE.md and skills the way an interactive session does, because that is the whole point and the documentation is not explicit about it. A [`Stop` hook](https://code.claude.com/docs/en/hooks) receives the final reply as `last_assistant_message` and can fail the run on a pattern. A shell loop over the case folders, a regex per grader, a line per case in a results file — that is the whole harness, and it should stay that small.

**With `claude plugin eval`.** Where it is enabled, it runs each case in a throwaway workspace with only the plugin under test loaded, several times by default, with an optional baseline arm that runs the same prompt without the plugin and reports the delta. That last feature is the one hand-running cannot cheaply reproduce, and it answers the question "does this skill actually change anything" more honestly than reading the skill does. It is early access at the time of writing, so treat its presence as something to check, not assume; what it asks for is the case-folder shape above, so a suite written that way is ready if it arrives.

**Whichever runner: one run proves little.** Trigger behaviour in particular is probabilistic at the margin. Run a case three times before calling it passed or failed, and record the pass rate rather than a single verdict. A trigger case at two of three is a finding — the description is on the edge, and the next model will push it over.

---

## 5. When to Run the Suite

Four triggers, and not "every session".

**After you change a rule or a description.** The regression run. You edited the phrasing of a CLAUDE.md rule or a skill description; run the cases that touch it and the negative cases of its neighbours. This is also the moment to update the case if the change was deliberate — a test that encodes the old behaviour after you changed the rule on purpose is a spec that has fallen behind, and [Guide 29](./29_SPEC_BEFORE_REBUILD.md)'s rule applies: change the statement first, then the artefact, then check one against the other.

**After a model launch, or when a model changes underneath a task.** The full suite, once, with the results recorded against the model name. `PreModelSwitch` and `PostModelSwitch` hooks fire in-session when the model changes and can log it, but a scheduled task that silently picked up a new default model has no such moment; the results file is how you notice.

**After adding a skill.** Every existing trigger test, positive and negative. New skills are the most common cause of an old skill going quiet, and nobody thinks to test the old one.

**Periodically, as drift detection.** Quarterly is enough for a personal setup. This is the run that catches the platform and context sources from §1 — the ones you did not cause and would otherwise discover from a wrong email.

---

## 6. Grading Judgement Without Grading Yourself

Where a grader has to be an `llm` grader — the reply reads as yours, the summary picks the right items — two traps are waiting.

**The judge is not independent.** A model grading a model shares its dispositions, and [Guide 27](./27_INDEPENDENT_JUDGMENT.md) is blunt about what two agreeing runs are worth: correlated error, not corroboration. Majority voting across several judge runs — which is what the platform's own `llm` grader did at the time of writing — helps with noise and not with shared bias. Mitigate by writing criteria a person could apply mechanically ("names the three deadlines in the fixture", "contains no sentence beginning 'I hope this finds you'") and by keeping a handful of hand-graded reference outputs the llm grader is periodically checked against.

**The criteria leak the answer.** A grader that says "check that the reply refuses to send" tells the judge what a pass looks like, and the judge will find it. Write criteria as observations to make, not verdicts to reach — the finding-schema discipline from [Guide 26](./26_CONTEXT_SCOPING.md): what to look for, where, and what evidence would fail it.

The stronger move is to need fewer llm graders. Most rules that feel like judgement have a mechanical shadow: a tool that must not be called, a file that must exist, a string that must not appear. Test the shadow.

---

## 7. What a Failure Means

A failed case is a fact, not yet a diagnosis. Sort it into one of four before touching anything.

| Failure looks like | It probably is | What to do |
|---|---|---|
| Fails on the new model, passed on the old, no file changed | A model change | Fix the instruction so it holds on the model you run, not the one you wrote it for. Waiting is not a fix. Pinning the task's model buys time and should be recorded as a decision with an expiry |
| Fails on both models after a recent edit elsewhere | Your own accretion — a trigger race, a rule interaction | Find the competing rule or skill; the fix is usually in the *other* file |
| Fails intermittently at a stable rate | A marginal description or an under-specified rule | Sharpen it until the rate is 3 of 3, or accept the rate in writing |
| Fails because the platform moved | A platform change | Record it in the suite README with the date; rewrite the case or the rule |

**A test that fails after a model launch is a fact about the model, and the fix belongs in your instructions.** The instinct is to wait for the model to settle, or to file it as a platform problem. Neither changes what your setup does tomorrow morning.

---

## 8. Keeping the Suite Honest

A suite rots in the same two directions a CLAUDE.md does: cases nobody remembers the reason for, and cases that encode a rule you already changed.

- **A case that cannot say what it protects is pruned**, the same as a rule ([Guide 16](./16_BEST_PRACTICES.md)).
- **A deleted rule takes its cases with it.** In the same commit.
- **A changed rule changes its cases first** — never a test edited to match whatever the setup did today.
- **The results file is history, not state.** Append, with date and model; never overwrite. The pattern across runs is what tells you whether a failure is new.
- **Size stays small.** If the suite passes thirty cases, ask what each is for. A suite that takes an hour to run by hand will not be run.

---

## 9. Worked Example

A setup with three things worth protecting: an account-level rule that outgoing emails contain no em dashes; a skill that drafts messages in a second language and must trigger on "draft a reply to …" but not on "summarise this thread"; and a scheduled morning task that reads a mailbox and must draft but never send.

Six cases: two for the rule (an email request that says nothing about punctuation, once in each language, regex on the output), two for the skill (the positive phrasing, the negative phrasing, a `tool_used`-style check on whether the skill loaded, or by hand a look at whether its output format appeared), two for the task (the fixture mailbox run through the task's instruction file, `tool_used` on the send tool at zero, `file_exists` on the draft folder).

Run by hand in a fresh session the first time, one run per case — ten minutes. Five pass cleanly; the negative skill case is marginal, so it gets its three runs and fails two of them, because "summarise this thread and draft a short reply" is in the fixture and is a legitimately ambiguous request. That is a finding about the fixture, not the skill; the case is split into a clean negative and an ambiguous one whose expected outcome is "asks". The README records the date, the model, and the split.

After the next model launch, the full six again. The em-dash rule now fails one of three in the second language. The fix is one line in the account instructions, made specific about that language; the case that caught it gets the date added to its frontmatter.

---

## 10. The CLAUDE.md Block

Short, because most of this is a procedure and lives in the suite's README rather than in standing instruction. What belongs in CLAUDE.md is the rule that changes to protected things come with a test run.

```markdown
## Behaviour tests

The suite lives in `tests/behaviour/`. Each case is a `prompt.md` plus `graders/`,
and its frontmatter names the failure or rule it protects.

- After editing a CLAUDE.md rule or a skill description, run the cases that touch
  it and the negative cases of neighbouring skills. Report pass rates, not verdicts.
- Run tests in a fresh session, never in the one the edit was made in.
- Test inputs are fixtures under `tests/behaviour/fixtures/`. Never point a test at
  live data.
- Append results to `tests/behaviour/RESULTS.md` with date and model. Never overwrite.
- A failing case is a finding to report, not a test to edit. Editing a case to match
  current behaviour needs the rule changed first and said so.
```

`tasks/setup-behaviour-tests.md` interviews you for the rules and skills worth protecting, writes the first cases in this shape, and runs them once by hand to establish the baseline.

---

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| Testing in the session you edited from | That session holds your intent and grades itself kindly; the test passes and the fresh session fails |
| A prompt that describes the test instead of making the request | The model is told what a pass looks like and produces one |
| Only positive trigger cases | The trigger race is invisible until a neighbour's negative case fails |
| Pointing a task test at the live mailbox | The test can act; and the fixture changes under you so failures are not reproducible |
| One run, one verdict | Marginal triggers pass by luck and fail on the next model |
| An llm grader for something a regex could check | Weakest grader used where the strongest was available |
| Editing the case until it passes | Encodes today's behaviour as the spec; the rule you wanted is gone and nothing says so |
| A suite of a hundred cases | Will not be run; a suite that is not run protects nothing |
| Waiting for the model to "settle" after a failure | Your setup does the wrong thing tomorrow regardless |

---

## Checklist

Before the first run:

- [ ] Each case names the failure or rule it protects, with a date
- [ ] Every positive trigger case has a negative neighbour
- [ ] Task cases run against fixtures, and the fixtures are under the suite, not in the project's data
- [ ] Graders are mechanical wherever the rule has a mechanical shadow

Every run:

- [ ] Fresh session, or a scripted runner with the model pinned
- [ ] Three runs for every marginal case and every regression run; pass rate recorded, not a single verdict
- [ ] Results appended with date and model

On a failure:

- [ ] Sorted into model, accretion, marginal, or platform before any file is edited
- [ ] The fix is in the instruction, not in the case, unless the rule was changed on purpose and the change is written down first
