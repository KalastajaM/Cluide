# Improving agent task prompts

Agent task prompts, project instructions, standing instruction files, and scheduled task prompts. These drive an agent with tools, files, and long autonomous runs. Often nobody is watching when they execute, so the prompt must stand alone.

The three layers below exist on every assistant that runs projects; only the filenames and field names differ.

| Layer | What it is | Examples |
|---|---|---|
| Standing instruction file in the folder | Loaded at the start of every session in the project | `AGENTS.md`, `CLAUDE.md` (often a thin file importing a shared `AGENTS.md`), `GEMINI.md` |
| App-side field injected before any file is read | Typed into the product, not stored in the folder | a project's instructions field in a chat or desktop app |
| On-demand workflow file | Read only when one workflow runs | task file, skill file |

Diagnose the layer, not the product. A rule in the wrong layer fails the same way on every assistant.

## Common failure modes

- **Assumes conversation context that won't exist.** Scheduled tasks and new sessions start fresh. Every run needs the full picture inside the prompt: what to do, where files live, what the output should look like, where it should go.
- **No definition of done.** Agents with tools will keep working or stop early without a crisp completion criterion. State the deliverable, its destination, and what "finished" means.
- **Ambiguity that forces a blocking question.** In unattended runs a clarifying question stalls the task for hours. For each judgment call the agent might face, either decide it in the prompt or explicitly delegate it ("if X is ambiguous, choose conservatively and note the assumption").
- **Missing safety boundary.** An agent with email, calendar, payment, or commit access needs the hard rule stated: never send, pay, file, commit, or delete without explicit confirmation — draft first. Write it as an explicit NEVER and pair it with a positive counterpart ("produce a polished draft ready to send"); a prohibition alone leaves the agent nothing to do instead. This is the one place all-caps rules belong. Destructive edits that never leave the machine belong on the same list: a find-and-replace, a bulk rename, or a sweep across "the documents" is irreversible in practice and is usually issued without naming the files it will touch, so require the file list and the exact replacements first, applied only on approval.
- **Tool and connector assumptions.** Naming a connector that isn't attached, or not saying which source is authoritative when two disagree.
- **Scope creep invited by vague verbs.** "Look into", "clean up", "handle" produce wildly variable effort. Bound the work: how deep, how many, what to skip.
- **A pointer prompt that carries nothing.** "Read tasks/x.md and follow its instructions exactly" is a sound way to keep one source of truth, but the pointed-to file can be edited independently of the trigger, so anything living only there is not actually protected. Three things must stay in the trigger prompt itself: the safety boundary, what to do when the file, folder or mount is not reachable, and what a finished run looks like. A pointer with no path, no output destination and no fallback is the weakest shape a recurring task can have.
- **Instructions that grow without a cap.** A prompt loaded on every run is a recurring cost, and long instruction files get followed less reliably. Keep the run procedure to roughly 200–250 lines and move schemas, full templates, and error procedures to a reference file read on demand. Any state file the prompt re-reads every run needs a hard size cap and a trim rule, or it compounds forever.

## Patterns that help

- Structure as: context, task, step outline (only if order matters), output spec, edge case handling.
- Pin the output spec with an exact template — headers, field names, one filled example — not a description. If the format is identical every run and only the data changes, have the prompt run a script that renders the artifact instead of composing it fresh each time.
- For recurring tasks: state what changes between runs and what stays fixed; instruct the task to be idempotent (safe to re-run).
- Specify the quiet case. A recurring task needs a bounded output for a run with nothing to report ("one line: clean, N known flags"), or every run produces a full report and the reader stops distinguishing the ones that matter. This is separate from capping state files: it caps what the run says, not what it stores. A suppression list of settled findings the task must not re-raise does the same job for alert fatigue.
- Attach the cost to a hard guardrail where a real one exists. "Never write the ledger; a duplicate entry double-counts the month and takes hours to unwind" holds under ambiguity in a way that "never write the ledger" alone does not, because an unattended run has no way to reconstruct why the rule was there. Pair it with a sanctioned way to challenge the rule: report a case where it seems wrong as a finding, never act on it silently.
- For unattended runs that would otherwise act: prepare, queue, log. The run prepares the action (the draft, the edit list, the payment details), puts it where a person will approve it, and logs what it did and did not do. The person acts; the run never does.
- Name concrete paths, channels, calendars, and file names rather than descriptions of them.
- For interactive tasks: bounded choices (tone, scope, approve/reject) should be presented as button options where the host offers them; reserve open questions for genuinely open-ended input.

## Where an instruction belongs

Every rule should have exactly one home; duplicated rules drift apart silently. When improving a prompt in one layer, check whether some of its content belongs in another — moving a rule is often the real fix. This is also the repair path after a bad run: the fix for a mistake is a rule written at the layer that will still be loaded next time, not a correction typed into the session where it happened. If a prompt shows the same correction being made repeatedly, the correction belongs upstream.

- **The standing instruction file** holds rules that apply to every session in the project: identity, communication style, hard safety rules, folder conventions. Every line should change behavior; if removing it would change nothing, cut it. Growth past a two-minute read usually means task-specific rules have leaked in — move them to the task or skill file they belong to.
- **The app-side project instructions field** is injected before any file is read, but is invisible to git and to any audit of the folder. Keep it to what must hold from the first token: a bootstrap pointer ("read the project's instruction file in full before doing anything else", naming it), verification that the required folders or sources are actually available, a restated hard safety rule, and session posture (language, draft-only mode). The safety-rule restatement is the only sanctioned duplication — it must hold even in a session where the folder never connects.
- **Task and skill files** hold the workflow steps, output templates, and edge cases for that one workflow, read on demand.
