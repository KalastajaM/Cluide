# prompt-improver — behaviour cases

Cases in the shape of Guide 31 §3: each folder holds the prompt as it would actually be typed and
checkable graders. They test behaviour, not the text of `SKILL.md`. All inputs are invented; no
case uses anyone's real prompt or data.

| Case | Protects | Written against |
|---|---|---|
| `leave-alone-sufficient` | A sufficient short prompt comes back unchanged, with the reason | The do-no-harm gate: improving weak prompts must not damage good ones |
| `implicit-ask` | Pasted material with no verb gets a named task and deliverable | Implicit-ask failure mode |
| `anchored-review` | A review prompt is stripped of the user's conclusion and existence claims | Guide 27: anchoring and existence priming |
| `missing-input-branch` | An unattended task gains a missing-input branch and a duplicate guard | Unattended-run failure modes |
| `code-fence-in-prompt` | A prompt containing a fence is wrapped in a longer fence | Copy-ready output breaks on nested fences |
| `secret-in-prompt` | A credential in the prompt is not repeated back | Unusual-input rule |
| `from-scratch-code-review` | A drafted prompt has a done-state and placeholders, not invented values | Writing-from-scratch section |
| `skill-description-trigger` | A rewritten description has triggers, an exclusion and stays under 1024 characters | Skill-description reference |
| `improve-prompt-fires` | Positive trigger on a casual phrasing that never says "prompt improver" | Pairs with the two negative cases |
| `review-plan-stays-quiet` | Negative neighbour: reviewing a plan that is not a prompt does not load the skill | The description's exclusion |
| `task-cost-stays-quiet` | Negative neighbour: making a task cheaper does not load the skill | The description's exclusion |

**How to run.** In a fresh session with the skill installed — never the session that edited the
skill (Guides 26, 27) — paste `prompt.md`'s body, then check each grader against the reply and the
tool calls. Run each case three times and record the pass rate; a case at two of three is a
finding. An unrun case is **untested**, not passing. The graders name Claude transcript evidence
(skill loads, tool calls), so the suite is Claude-only as written.

**Grading.** Binary graders saturate on this skill: earlier versions scored full marks on cases
that a blinded rubric separated clearly. For a version comparison, also score each output 0–2 on
restraint (nothing added that the prompt did not need), diagnosis (the real gap named), standalone
(runs in a fresh session), format (copy-ready block, rationale tied to weaknesses) and preserved
constraints (nothing from the original silently dropped), with judges who do not know which
version produced which output. Keep a few hand-graded outputs to check the judges against.

| Date | Surface | Model | Skill revision | Result |
|---|---|---|---|---|
| 2026-11-08 | Claude cloud session; workers followed `SKILL.md` from a file, so triggering was not exercised | sonnet workers, three opus judges, blinded | 6.0.0 against the previous version | Seven content cases (all except `skill-description-trigger` and the three trigger cases), 2 runs each, below the three-run protocol, so treat as provisional: every grader passed in every 6.0.0 run. Rubric over ten cases plus three maintainer-only cases not shipped here: 6.0.0 higher on seven, equal on two, lower by 0.15 points (of 12) on one; one case regressed in the first round and was fixed and re-run before release. Largest gain `anchored-review` (8.8 → 11.0 of 12), which version 5 failed. Trigger cases and `skill-description-trigger`: **untested** |
