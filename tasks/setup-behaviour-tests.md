# Task: Setup Behaviour Tests

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-behaviour-tests.md`
> **Source guide:** `31_BEHAVIOUR_TESTS.md` (see also `27_INDEPENDENT_JUDGMENT.md` for grading judgement, `26_CONTEXT_SCOPING.md` for why tests run in a fresh session)

## Purpose

Build a small behaviour-test suite for a project — or for an account-level setup — so that the rules and skills worth protecting can be re-checked after an instruction edit, a model launch, a new skill, or on a quarterly drift run. The suite is a folder of cases, each a prompt plus checkable graders, in the shape Guide 31 §3 describes. The task interviews for what earns a case, writes the first cases, runs them once by hand in a fresh session to establish the baseline, and installs the CLAUDE.md block that ties future edits to a test run.

Use it when a project has rules or skills that would be embarrassing to lose silently, when a model launch has just happened and nobody knows what changed, when a new skill has been added beside older ones, or when `analyze-project.md` dimension 23 reports no behaviour tests for a project that carries standing rules or scheduled tasks.

This task is distinct from `audit-skill.md` and `audit-claude-md.md`: those read a definition and judge it; this runs the behaviour and records what happened. Both are needed and neither replaces the other.

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons rather than plain text.

### Step 0 — Preconditions and runner

Confirm the project folder is mounted and writable, and that you can read its `CLAUDE.md`, skills, task definitions, and (if present) the account-level instructions the user pastes in.

Establish which runner the user has, because it shapes Step 5:

- **Cowork only** — cases are run by hand in a fresh session. This is a complete method, not a fallback; say so.
- **Claude Code** — cases can be scripted with `claude -p --output-format json`. Confirm in the user's build that print mode loads the project's `CLAUDE.md` and skills the way an interactive session does (Guide 31 §4 says why this needs checking) before promising a scripted run.
- **`claude plugin eval` available** — early access as of September 2026, enabled per organisation. Check with `claude plugin eval --help`; if the command reports early access, say so and fall back to the previous option. Do not build the suite around a runner the user cannot execute.

### Step 1 — Inventory what could be protected (read-only)

Read, and list without judging yet:

1. Every standing rule in `CLAUDE.md` and in the account-level instructions, one line each.
2. Every skill in the project and every account skill the project relies on, with its trigger description.
3. Every scheduled task, with the actions it may take (its connectors and scopes — Guide 32 §2 classes if the project has an action-authority block).
4. Any rule that lives in a skill rather than in `CLAUDE.md` (Guide 30 §8 and Guide 32 §6 both flag these as weak; they are also the ones most worth testing).

Present the list. Do not propose cases yet — the user has to say what matters.

### Step 2 — Interview: what earns a case

Ask, in this order:

1. **Which of these would be embarrassing or costly to lose silently?** Point at the inventory; take the user's picks. Guide 31 §2 is the filter: a case is a claim that a failure matters. If the user cannot name the failure, the item does not get a case yet.
2. **For each pick, what is the sentence you actually type?** Not a description of the request — the request. For a rule, ask for the request that would violate it if the rule were absent (the one that does not mention the rule). For a skill, ask for the phrasing that should trigger it *and* the neighbouring phrasing that should not.
3. **For each scheduled task picked, is there a fixture?** A frozen input — an exported sample, a fixture folder — that the task can run against. If not, the task case waits until one exists; never point a case at live data. Offer to build the fixture as a separate step.
4. **Which model is the baseline?** The one the project runs on today. Results are recorded against it.

Stop once the user has named ten to thirty cases' worth. More than thirty is a sign the filter in question 1 was not applied; say so.

### Step 3 — Draft the cases (read-only until approved)

For each pick, draft the case in Guide 31 §3's shape and show them all before writing anything:

```
tests/behaviour/<case-name>/
  prompt.md      ← frontmatter: name, protects (rule or failure + date), tags, runs: 3
                   body: the exact request
  graders/
    <grader>.md  ← frontmatter: type (regex | tool_used | tool_order | file_exists | llm)
                   and its fields; body: the pattern or the criteria
```

Rules for the draft:

- **Every positive trigger case has a negative neighbour.** Draft them as pairs and name them as pairs (`x-triggers`, `x-stays-quiet`).
- **Mechanical graders first.** A regex on the output, a tool call count, a file's existence. Reach for an `llm` grader only where the rule has no mechanical shadow, and then write its criteria as observations to make, not verdicts to reach (Guide 31 §6). Show the user which graders are `llm` and why each could not be mechanical.
- **`protects:` is filled for every case** — the rule it guards or the failure it was written against, with a date. A case without one is not drafted.
- **Task cases name their fixture path** and the fixture lives under `tests/behaviour/fixtures/`, not in the project's data folders.

Present the full draft as a table: case, kind (trigger / rule / task), prompt, graders, protects. Then **stop and wait** for approval, row by row if the user prefers.

### Step 4 — Write the suite

Create `tests/behaviour/` with the approved cases, a `README.md`, an empty `RESULTS.md`, and `fixtures/` if any task case needs one.

The `README.md` states: what the suite protects (one line per case, the `protects:` field), when it was last run and on which model, the four triggers for running it (Guide 31 §5), and which runner the project uses. Keep it under a page; it is read before every run.

`RESULTS.md` is append-only: one block per run with date, model, runner, and a line per case with its pass rate (n of 3) and a note on any failure. Never overwritten.

### Step 5 — Run the baseline

Run every case three times on the baseline model, by the runner established in Step 0:

- **By hand:** tell the user to open a **fresh** session in the project — not this one — paste each prompt, and report back what came out. The first pass is one run per case; any case that is marginal or fails gets its three runs (Guide 31 §4).
- **Scripted:** run the loop with the model pinned (`--model`), collect the JSON output.

Grading splits by grader type. **Mechanical graders** — regex, tool counts, file existence — may be applied by this session to whatever came back; they cannot be biased by having drafted the case. **`llm` graders and any judgement call** are not applied by this session: it drafted the criteria and knows what a pass looks like (Guide 27). Hand those to the user, or to a fresh session given only the output and the grader file. Record the pass rate per case.

Append the baseline block to `RESULTS.md`.

A case that fails at baseline is a finding, not a bad test: either the setup does not do what the user believed (report it, with Guide 31 §7's table to sort it) or the case's prompt or grader is wrong (fix the case *only* with the user's agreement and say so in the results block). Do not edit a case to make the baseline pass.

### Step 6 — Install the CLAUDE.md block

Add Guide 31 §10's block to the project's `CLAUDE.md`, with the paths filled in. Add `tests/behaviour/` to the file map. A new hard rule in CLAUDE.md is one of Guide 25's update triggers, so check the app-side fields the same session; usually nothing there changes, and the mirror block records that it was checked.

If the project has a `.gitignore`, confirm `tests/behaviour/` is tracked and `fixtures/` contains nothing that should not be — a fixture built from a real mailbox export is personal data, and belongs in the ignore list with a bootstrap stub (Guide 11 and `setup-bootstrap-folder.md`).

## Output

An inventory of protectable rules, skills and tasks (Step 1); an approved case table (Step 3); the suite under `tests/behaviour/` with `README.md`, `RESULTS.md` and any fixtures (Step 4); a recorded baseline run with pass rates per case (Step 5); and the CLAUDE.md block installed (Step 6).

## Constraints

- Read-only until the Step 3 table is approved.
- Never point a case at live data. A task case with no fixture is not written.
- Baseline runs happen in a fresh session or a pinned scripted runner, never in this one. Mechanical graders may be applied here; `llm` graders and judgement calls go to the user or a fresh session.
- Never edit a case to make a run pass. A baseline failure is reported; a case is corrected only with the user's agreement and a note in `RESULTS.md`.
- Do not build the suite around a runner the user has not confirmed works in their build.
- Keep the suite small. Over thirty cases is a finding about the filter, not a bigger suite.
