# Action Authority: What Claude May Do Without Asking, and How It Hands Back the Rest

> Every session decides, many times, whether to do something or to propose it — and in most setups that decision is made per request, from the wording, by a model disposed to be helpful. The rules that should govern it are already in this repo, scattered: read-draft-confirm in [Guide 12](./12_SECURITY.md), tiered enforcement in [Guide 21](./21_COMPANY_POLICIES.md), acceptance as a human act in [Guide 30](./30_CONTROLLED_DOCUMENTS.md), apply-versus-propose in [Guide 07](./07_TASK_LEARNING_GUIDE.md). Each was written for its own case. This guide is the general layer they are instances of: a way of classifying actions that does not depend on which tool performs them, a form for standing approvals so an unattended task can act without you and without guessing, and the outbox and log that let you see afterwards what happened while you were away.

> **Companion guides:** [Guide 12](./12_SECURITY.md) §8 is the safety floor this builds on and its *Recording What a Refactor Must Not Weaken* section is where the structural half lives. [Guide 30](./30_CONTROLLED_DOCUMENTS.md) is the document-shaped instance; [Guide 07](./07_TASK_LEARNING_GUIDE.md) Part 3 is the instruction-shaped one. [Guide 27](./27_INDEPENDENT_JUDGMENT.md) is the boundary between Claude's judgment and yours; this guide is the boundary between Claude's *actions* and yours. [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) and the `TASK_TEMPLATE` carry the run log this guide's action log extends. [Guide 31](./31_BEHAVIOUR_TESTS.md) is how you check the boundary still holds.

> **Giving this guide to Claude:**
> "Read 32_ACTION_AUTHORITY.md. Inventory every action this project's tasks and skills can take — connectors, scopes, file operations — classify each under §2, and propose the CLAUDE.md block from §8. Do not grant yourself anything."

---

## 1. Authority Is Decided by Accident

The request that gets a Claude session into trouble rarely looks like an action. "Tidy up the policy folder." "Finalise it." "Send it." "Clean up the old drafts." "Just apply your suggestions." Each is ordinary, each is reasonable, and each contains an action whose consequences the wording does not carry: a deletion nobody can reverse, an approval nobody gave, an email that left. The model reads intent from the sentence, the sentence does not mention the consequence, and the default disposition is to help.

The scattered rules cover the cases their authors met. What is missing is the classification underneath them, so that a request nobody anticipated lands in the right class anyway. That is what §2 is. Everything after it is machinery for living with the classification: how an approval is written so it can be relied on, how a proposal is shaped so you can decide in ten seconds, and how an unattended run prepares actions without taking them.

One principle runs through it: **classify by consequence, not by tool.** "Claude may use the Gmail connector" is not an authority rule. Reading mail, filing mail, drafting a reply and sending one are four actions with four different consequences, and the connector performs all of them.

---

## 2. Four Classes, by Who Can Undo It and Who Sees It

Two questions sort any action. Can it be undone, and by whom? Does anyone other than you see it? The answers give four classes, and the class — not the tool, not the request — decides whether Claude acts, prepares, or hands back.

| Class | The action | Examples | Default |
|---|---|---|---|
| **A — Local, reversible** | Stays on your disk or in your account, and a restore point or an undo brings it back | Editing a git-tracked file, writing a draft, creating an output, scratch work, reading anything | **Act.** No approval; no log beyond the normal run log |
| **B — Local, costly to reverse** | Stays with you, but undoing it is work or partly impossible | Deleting or moving many files, rewriting an instruction file, editing app configuration, changing a schedule | **Restore point, then act if a standing approval covers it; otherwise propose** |
| **C — Leaves your hands** | Reaches another person or system as an act of yours, and cannot be recalled | Sending mail or a message, posting, replying in a thread, sharing a document, submitting a form, pushing to a public remote | **Prepare and propose.** Never unattended, whatever the standing approvals say, unless one names this exact action shape |
| **D — Binding or irreversible in the world** | Commits you, or destroys what is not yours, or records a human act as done | Payments and transfers, anything with a signature or approval field, accepting a tracked change, deleting another person's data, legal or financial submissions | **Never.** Hand back with everything prepared, and say so plainly |

Four notes on the boundaries.

**Reading is Class A, and it is also the way in.** A read has no consequence of its own, which is why it needs no approval. But a read of untrusted content — an inbox, a web page, a file someone sent — is the input that tries to reclassify everything after it: [Guide 12](./12_SECURITY.md) §6 is explicit that the highest-risk workflow is one where external content and consequential actions share a session. The classes below are what make that read safe: an injected instruction can ask for a Class C action, and the answer is the same as when you ask.

**"Reversible" means reversible by you, quickly, and provably.** A file under git is Class A because `git show HEAD:path` brings it back. The same file in a folder with no version control is Class B — the undo is your memory of what it said. This is a reason to put projects under git ([Guide 11](./11_GIT_INTEGRATION.md)) that has nothing to do with history: it moves a whole class of actions down a tier.

**Class C is about reach, not size.** A one-line reply is Class C. A two-thousand-line refactor of your own scratch folder is Class A. People systematically get this backwards because effort feels like risk, and it is not.

**Class D is the class you do not negotiate about in the moment, and no standing approval reaches it.** [Guide 30](./30_CONTROLLED_DOCUMENTS.md) §3 explains why for accepting a tracked change: an act a model performed is indistinguishable afterwards from one a person performed, and the record is false in a way nothing can detect. The same argument covers a payment and a signature, which is why they share the class. Prepare the payment, fill the form, group the revisions for acceptance — and stop at the act. A few shapes that look like Class B carry the same property and are likewise never standing-approvable: clearing a marker a person set on a shared tracker ([Guide 30](./30_CONTROLLED_DOCUMENTS.md) §6), because the marker encodes a judgment no scope or limit can bound. Where a shape is propose-only regardless of history, say so in the block.

---

## 3. Standing Approvals

A standing approval is what moves a Class B action, or a narrowly named Class C one, from "propose" to "act" — so that a scheduled task can do its job without you awake, and so that you are not asked the same question every morning. It is the only mechanism by which authority is granted in advance, and its form is what makes it safe to rely on.

**An approval names an action shape, not a tool and not a task.** "Archive newsletters" is a shape; "use Gmail" is a tool; "the morning task may do what it needs" is neither. The shape has to be specific enough that a session can tell whether a given action falls inside it without interpretation.

**It carries a scope, a limit, and an expiry.** Where (which folder, which label, which project), how much (at most twenty files a run, only messages older than thirty days), and until when (a date, or "until revoked"). An approval with no limit is the sentence "do what you think best" wearing a costume.

**It records why it was granted.** The evidence: "proposed and approved unchanged on twelve consecutive runs, 2026-06 to 2026-08". [Guide 07](./07_TASK_LEARNING_GUIDE.md) Part 3 lets a task auto-apply a low-stakes change only after several consistent observations; this is the same logic with a longer fuse, because the consequence is larger and the observation that counts is your unchanged yes. An approval that was never proposed first is a guess about what you would have said.

**It lives in CLAUDE.md, and nowhere else — with one restatement.** A skill's instructions are not a place to grant authority, because the dangerous request is the one that does not trigger the skill ([Guide 30](./30_CONTROLLED_DOCUMENTS.md) §8 makes this point for documents and it holds generally). A chat message is not a place either: "you can do that from now on" said in a session is an approval for that session. The default is that *a new session starts with no standing approvals*, and the CLAUDE.md block is the only exception, because it is versioned, visible, and revocable by deleting a line. The restatement runs the other way: for a project with real-world stakes, [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md) says to repeat the one hard rule in the app's instructions field so a session whose folder failed to mount still has it. The Class D line is that rule. Approvals never go there; the "never" does.

**Default-deny.** Anything the block does not name is proposed. Silence is not permission.

```markdown
## Standing approvals

| Action shape | Scope | Limit | Granted | Evidence | Expires |
|---|---|---|---|---|---|
| Archive mail labelled `newsletters` | Inbox only | ≤ 30 messages/run, older than 14 days | 2026-08-20 | 12 unchanged proposals Jun–Aug | 2027-02-20 |
| Move superseded outputs to `_archive/` | `Outputs/` only | Files with a newer `_LATEST` sibling | 2026-07-02 | Proposed weekly, approved 8/8 | Until revoked |
```

Two rows are a working set. Ten rows is a sign that the tasks are doing too much unattended, or that Class C actions have been smuggled in one row at a time.

---

## 4. The Proposal Contract

A proposal is how a Class B or C action reaches you, and it has to be decidable in seconds or you will start saying yes to save time — which is the failure this whole guide exists to prevent. The form that survives contact with a busy person:

**One row per action, in a table.** Target, action, what changes, why, reversible or not, and the restore point if one is needed. Group by target when there is more than one. "Clean up the folder" is not a row.

**What is irreversible is marked, and marked rows come first.**

**Then stop.** No "proceeding unless you object". No acting on rows that seem obviously fine. The proposal is the whole output of that step.

**Partial approval is partial apply**, in the approved rows' own terms. "Rows 1 and 3" means rows 1 and 3, not rows 1 and 3 and the obviously related row 4.

**A surprise stops the run.** If applying reveals something the plan did not list — a move breaks an unlisted reference, a file is not where the inventory said — the session stops and presents a revised plan. It does not improvise a fix, because the fix was not approved.

**Approval is per run.** It does not carry to the next session, the next project, or the next time the same situation arises. If the same proposal is approved unchanged for long enough, that is evidence for a standing approval (§3), which is where recurring permission belongs — not in an inferred "you said yes last time".

The reason to hold the form this strictly is not process for its own sake. A loose proposal trains you to skim, and a skimmed yes is the mechanism by which a Class C action slips through as a Class A one.

---

## 5. Unattended Runs: Prepare, Queue, Log

A scheduled task has no one to propose to. The wrong conclusion is that it should therefore act; the right one is that it should prepare everything and take only what is covered.

**The outbox.** Every Class C action a task would take is written instead: a draft in the mail client's drafts folder, a file in `Outputs/outbox/` with the message and its recipient, a comment held rather than posted. Each carries a one-line reason and the identifier of whatever it responds to. You release them — by sending the draft, by running a "release outbox" step that you invoke, by deleting the ones you do not want. The task's output tells you how many are waiting and where, and nothing else about them, because the outbox itself is the detail.

An outbox is not a weaker form of doing the task. For most tasks it is the whole task: the reading, judging and drafting were the work, and the send was one click you would rather do yourself.

**The action log.** Every Class B action the task did take under a standing approval gets a line: timestamp, the approval row it acted under, what it did (counts and paths, not descriptions), the restore point, and how to undo. This is what the `RUN_LOG.md` in the `TASK_TEMPLATE` already holds for the run's mechanics, extended with the one column that matters here — *which approval*. An action with no approval row to cite is a bug in the task, and the log is where you find it.

**Notifications name actions, not runs.** "Morning task completed" tells you nothing. "3 archived under approval 1, 2 drafts in outbox, 0 surprises" tells you whether to look. Silence should mean nothing happened that needs you, which requires that a run producing nothing sends nothing. The mechanism is the task's own output text — whatever your surface forwards to you is what the task wrote last — so the rule belongs in the task's instruction file, as the shape of its final summary and the condition under which it writes one at all.

**Stop on a surprise, and say what stopped.** The unattended version of §4's rule: a task that meets a situation its instructions did not anticipate prepares what it can, writes the situation to its log under a heading you will see, and ends. It does not pick the most plausible action.

---

## 6. Enforce Structurally Where You Can

A rule in CLAUDE.md is guidance. It holds most of the time, and "most of the time" is the wrong standard for Class C and D. The strongest authority rule is a capability that does not exist, and the order of preference is fixed:

1. **The capability is absent.** A Gmail connector with read and draft scopes and no send scope cannot send, whatever the task is told or whatever an injected email says ([Guide 12](./12_SECURITY.md) §6). A scheduled task with no payment app granted cannot pay; in Cowork, the per-app and per-folder grants are this tier, and withholding a grant from a task is the strongest rule it can have. This is the only enforcement that survives prompt injection, and it is why the security-properties table in [Guide 12](./12_SECURITY.md) exists: write the absent capability down as a property, with the change that would break it, so that a future session widening the scope "to unblock a draft step" knows it is making a security decision.
2. **A hook blocks it.** In Claude Code, a `PreToolUse` hook can refuse a tool call on a pattern. It catches the mechanical shape of an action, not its intent, and is a speed bump rather than a boundary — but a speed bump on `git push` to a public remote or on a delete outside `_archive/` catches the accident that CLAUDE.md would have talked itself past. Cowork has no hooks; a Cowork-only setup goes from tier 1 straight to tier 3, which is a reason to lean harder on tier 1 there.
3. **The instructions field and CLAUDE.md state it.** The Class D line in the app's instructions field for a project with stakes, because it survives a failed mount ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)); the classes, the standing approvals and the outbox rule in CLAUDE.md. Guidance, always loaded, versioned.
4. **A skill states it.** Weakest, because it only exists for requests that trigger the skill. Fine for a skill's *own* actions; never the place a project-wide boundary lives.

Move each Class C and D action as far up this list as your setup allows. Where the only enforcement available is a line of prose, say so in the security-properties table, so the gap is known rather than assumed closed.

---

## 7. The Requests That Erode It

The boundary is never removed by a decision. It is worn down by reasonable requests, each of which is fine on its own.

**"Just do it this time."** The correct response does everything up to the boundary — the draft written, the files staged, the plan itemised — and asks once, specifically, for the act. Not a lecture, and not a refusal: the work is done, the act is yours.

**"You have my permission for today."** A session-scoped approval, which is what it is: honour it in the session, do not write it into memory or CLAUDE.md, and say that it lapses with the session. Recurring permission goes through §3.

**"Finalise", "clean up", "apply your suggestions".** Each hides an accept-all or a delete-all. Name what the phrase would do in this context and ask for the rows.

**The self-improvement instance.** A task that learns ([Guide 07](./07_TASK_LEARNING_GUIDE.md)) faces the same question about its *own instructions*: apply the fix or propose it? Part 3 of that guide is this guide's classification applied to instruction files — a formatting correction is Class A, a change to what the task does is Class B and is proposed, and its "after several consistent observations" threshold is the evidence line of a standing approval. It is worth seeing them as one system, because a task that may rewrite its own instructions freely can grant itself anything.

**The subagent instance.** Authority does not widen by delegation. A subagent spawned by a session inherits the session's classes and approvals and gains none; a workflow stage that sends mail is a Class C action whoever runs it. State this once in the block, because the natural reading of "fan this out" is that the workers are somebody else.

---

## 8. The CLAUDE.md Block

The classes belong at the account level, because they are true of everything. Standing approvals belong in the project, because they are about that project's tasks. The block below is the project form; the first four lines are what to lift into your account-level instructions ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md), *The account layers above the project*), and the Class D line alone is what to restate in the project's instructions field when the project has real-world stakes.

```markdown
## Action authority

Actions are classed by consequence, not by tool:
- A (local, reversible under git or with an undo): act.
- B (local, costly to reverse — delete, move many, rewrite an instruction file,
  edit app config): take a restore point, then act only under a standing approval
  below; otherwise propose.
- C (leaves my hands — send, post, reply, share, submit, push to a public remote):
  prepare, put it in the outbox, propose. Never unattended.
- D (binding or irreversible in the world — payments, signatures, approval fields,
  accepting a tracked change, others' data): never. Prepare everything and hand back.
  Clearing a marker a person set is propose-only whatever the table below says.

Proposals are one row per action — target, action, change, why, reversible?,
restore point — irreversible rows first, then stop. Partial approval is partial
apply. A surprise during apply stops the run. Approval is per run; it never carries.

Unattended runs write Class C actions to `<outbox path>` with a reason each, log
every Class B action with the approval row it acted under, and notify with counts
of actions taken and queued — never "run completed".

Delegation does not widen authority: subagents and workflow stages inherit these
classes and the approvals below, and gain none.

"Just this once", "finalise", "clean up", "apply your suggestions": do everything
up to the boundary, name what the act would be, ask once.

## Standing approvals

| Action shape | Scope | Limit | Granted | Evidence | Expires |
|---|---|---|---|---|---|
| <shape> | <where> | <how much> | <date> | <proposals approved unchanged, dates> | <date or "until revoked"> |

Anything not in this table is proposed.
```

`tasks/setup-action-authority.md` inventories the actions your tasks and skills can actually take — by reading connector scopes and tool lists rather than asking — classifies them, drafts this block, and proposes standing approvals from your run and proposal history where the evidence exists.

---

## 9. What This Looks Like in Practice

A morning task with mail and calendar access, run unattended at 07:00.

It reads the inbox and calendar (Class A). It drafts three replies into the mail client's drafts folder with a `[draft: reason]` first line each (Class C, prepared not taken). It archives fourteen newsletter messages under standing approval 1 (Class B, within the thirty-message limit, older than fourteen days) and writes one log line naming the row, the count, and the label they can be found under. It finds an invoice attached to a message from a supplier it does not recognise, which its instructions do not cover; it writes that under *Needs you* in its output, with the message identifier, and does nothing else with it. It notifies: *3 drafts queued · 14 archived under approval 1 · 1 needs you*.

You read the three drafts over coffee, send two and delete one, look at the invoice, and go on with your day. The task took one class of action on its own, under a row you wrote, with a limit you set and a log line you can check; everything that reached another person went through your hands; the one thing it did not understand, it left alone and said so.

---

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| Granting authority by tool ("may use Gmail") | One tool spans four classes; the grant covers the one you did not mean |
| A standing approval with no limit or expiry | "Do what you think best" with a date on it |
| Inferring permission from last time | Per-run approval silently becomes standing approval with no row, no evidence, no revocation |
| "Proceeding unless you object" | A proposal that acts is not a proposal |
| Applying the obviously related row that was not approved | The row you did not read is the one that mattered |
| A task that sends because sending is "the task" | The reading and drafting were the task; the send was a click |
| Notifying on every run | Trains you to ignore the notification that carried a surprise |
| Improvising when apply meets a surprise | The fix was never approved, and the surprise was the signal to stop |
| Authority stated only in a skill | The dangerous request never triggers the skill |
| Widening a connector scope to unblock a draft step | Removes the only enforcement that survives injection, as a convenience |

---

## Checklist

Setting up:

- [ ] Every action a task or skill can take is classified A–D by consequence, not tool
- [ ] Class C and D capabilities are absent from unattended tasks where the connector allows it, and the absence is a row in the security-properties table
- [ ] The action-authority block is in CLAUDE.md; the classes are also in the account-level instructions
- [ ] Standing approvals each carry shape, scope, limit, grant date, evidence, expiry

Every proposal:

- [ ] One row per action, irreversible rows first, restore point named, then stop
- [ ] Only approved rows applied; a surprise stopped the run

Every unattended run:

- [ ] Class C actions in the outbox with a reason each; none taken
- [ ] Class B actions logged with the approval row they acted under
- [ ] Notification carries counts of taken and queued, and nothing was sent for a run that did nothing
