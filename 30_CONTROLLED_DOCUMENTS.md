# Controlled Documents: Review, Comment, and Approval on Files That Have Owners

> Most of what Claude writes is yours to accept or throw away. Some of it isn't. A policy with a named owner, a contract someone else drafted, a document that carries a version number and an approval date — these are files where *who changed what, and who signed off* is part of the content. Claude's default behaviour on a file is to produce a better version of it, and on this class of document that default is wrong. This guide is the set of rules that makes Claude a reviewer rather than an author, and the document-management scaffolding that keeps the result auditable.

> **Companion guides:** [Guide 27](./27_INDEPENDENT_JUDGMENT.md) is the general form of the boundary in §3 — where Claude's judgment stops and yours starts. [Guide 21](./21_COMPANY_POLICIES.md) covers turning existing policies into guardrails Claude applies; this guide covers maintaining the policy documents themselves. [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) has the definitions-versus-generated-outputs principle that §5 applies to registers. [Guide 12](./12_SECURITY.md) covers the hard stops that hold regardless. [Guide 19](./19_OUTPUT_FORMATTING.md) is for documents you are producing rather than reviewing.

> **Giving this guide to Claude:**
> "Read 30_CONTROLLED_DOCUMENTS.md. My project has documents with owners and approvals in it. Run §1 on the folder and tell me which files are controlled documents and which are drafts, then propose the CLAUDE.md block from §8 for my setup."

**This applies well beyond compliance work.** An ISO or SOC 2 document set is the clearest case, but so are board minutes, contracts under negotiation, a shared research protocol, a family estate document that several people comment on, and any document where a person other than you owns the text. The examples below lean on management-system documents because that is where the conventions are most developed, not because the pattern is confined there.

---

## 1. Which Kind of Document Is This?

The whole guide turns on one distinction, and it is worth making explicitly rather than by feel.

| | Draft | Controlled document |
|---|---|---|
| Who owns the text | You, or Claude on your behalf | A named person, possibly not you |
| What a change is | An improvement | A proposal that someone must accept |
| What "done" means | It reads well | Someone approved it, on a date, at a version |
| Right Claude behaviour | Rewrite it | Propose, comment, and stop |
| Right failure mode | Too timid | Too helpful |

**The test:** if a change to this file could later be mistaken for something a person decided, it is a controlled document. That covers anything with an approver field, anything circulated for comment, anything referenced by an identifier elsewhere, and anything a third party will read as evidence of what was agreed.

**State it in the project, not per request.** The classification belongs in CLAUDE.md as a rule about paths — `03 - Policies/**` is controlled, `drafts/**` is not — because a per-request instruction only protects the requests you remembered to protect. §8 has the block.

---

## 2. Review: No Silent Edits

The rule is short: **Claude never changes an existing controlled document invisibly.** Every change goes in as a tracked change under a distinct author name, paired with a comment saying why. The reviewer then audits in Word's revision pane, which is where they already work, rather than diffing files or trusting a summary of what Claude says it did.

Two review paths follow from this, and they are worth naming separately because people confuse them.

**Someone else has commented, and you want the comments actioned.** Ask Claude to read the comments and tracked changes back to you, or to action specific ones — "apply the owner's comment on section 3". Claude's own edit is itself a tracked change with an explanatory comment. This gives you a chain: their comment, Claude's change, Claude's reason, your decision.

**You want Claude to review the document itself.** Ask against a named standard and a named clause — "review this against ISO/IEC 27001 cl. 6.1.3", "check this contract's liability section against the term sheet". Findings land as tracked-change edits plus comments, the same as above. Scope the request narrowly ([Guide 26](./26_CONTEXT_SCOPING.md)): a request to review a document against a whole standard produces a sweep that is long, shallow, and mostly restatement, while a request against two named controls produces findings you can act on. If you want breadth, run several narrow passes rather than one wide one.

**Author identity is not cosmetic.** Redline under a name that is obviously not a person — "Claude", not your own initials. Six months later, the revision pane is the only record of which suggestions came from a model, and that distinction matters when someone asks how a clause got there.

**Comments carry the reason, the change carries the text.** A tracked change with no comment is an assertion; the reviewer has to reconstruct why. Prefix Claude's comments consistently (`[Claude] …`) so they can be filtered and, later, cleared as a group.

### What this costs to run

The mechanics are real, not aspirational — but there is one operational trap.

The `docx` skill supports both halves. Tracked changes are `<w:ins>`/`<w:del>` runs with `w:id`, `w:author` and `w:date`; the skill's validator takes `--author` and `--original` and reports any text changed *without* a revision mark around it, which is easy to do by accident and invisible in the accepted view. Comments need six cross-linked files inside the `.docx`, and the skill ships a helper that writes all of them and prints the range markers to place — until those markers are in `document.xml`, the comment exists but is not visible in Word. Always run the validator before handing a redline back; an untracked change inside a document full of tracked ones is worse than no redline at all, because it is invisible precisely where the reviewer has learned to trust the pane.

**The trap:** that toolchain lives where Claude's own environment is, not on your disk. In a Cowork session with a connected folder, most file work should happen in place on your machine — but tracked-change editing of a `.docx` is one of the exceptions. The file has to be brought into Claude's environment, edited there, and written back to the same path. Two consequences follow. Say explicitly that the revised file must be returned to its original path, or you end up with a redlined copy in a chat and the stale original still on disk. And if you edited the document yourself in the meantime, that write should be refused rather than forced — the round trip is the one moment where two copies exist and can diverge.

---

## 3. Acceptance Is a Human Act

**Claude never accepts a tracked change — its own or anyone else's — and never fills an approver or approval-date field on its own initiative.**

This deserves its own section, above the mechanics, because it is the rule most likely to be softened in the moment by an entirely reasonable request. "Clean this up", "finalise it", "just apply your own suggestions" — each of these is asking for an accept-all pass, and each should get the same answer: the revisions stay pending, and Claude says so.

The reason is not process piety. It is that **an AI-accepted change is an approval nobody gave, and after the fact it is indistinguishable from one that someone did give.** A rejected suggestion and an accepted one look identical in the final text. The only place the difference was ever recorded is the act of accepting, and if a model performed that act, the record is false in a way no later audit can detect. The same argument covers the register: Claude does not write *Approved by* or *Approved on*, because those fields are a claim about what a person did.

The compensating move is to make acceptance cheap for you rather than to do it for you. Claude can group revisions so you accept a section at a time, list which ones are mechanical, and say plainly which of its own suggestions it is least confident in. What it does not do is convert your convenience into a signature.

This is the document-shaped instance of [Guide 27](./27_INDEPENDENT_JUDGMENT.md)'s boundary. The general rule there is that Claude should hand you the artefact rather than the verdict. Here the verdict has a physical form — a revision mark that disappears when accepted — which is exactly what makes it dangerous.

---

## 4. Identity in the Filename, State Inside the Document

Version numbers in filenames are the single most common document-management failure, and every set of them ends the same way: `Policy_v3_FINAL_reviewed_v2.docx`, four links pointing at three different files, and nobody sure which one the auditor saw.

The convention that survives contact with reality:

- **A stable filename, forever.** `Access-Control-Policy.docx`, not `Access-Control-Policy-v2.4.docx`. Every link, citation and register row points here and never breaks.
- **A short identifier that outlives the title.** `DOC-042`. Documents get renamed and merged; the identifier is what the evidence file, the register row and the cross-reference in another document all agree on. Titles are not stable enough to carry that load.
- **Version, status, owner, approver and approval date live inside the document**, in a control block at the top, and are mirrored in the register (§5). The filename says *which document*; the content says *which state*.
- **One conditional suffix, removed once.** A `-DRAFT` suffix is the one exception worth allowing, because "is this approved yet" is the question people ask most and a filename answers it for free. It comes off at the same moment the approval is recorded in the register — one rename, done once, after which the link is permanent.

**The control block is a template, not a habit.** Keep the field list — reference, title, owner, approver, version, status, date, classification — in one template file and have Claude copy it. A document set that grew organically will contain three or four different control-table shapes, and a session asked to "add a control block" without a template will invent a fifth.

**Retrofit on touch, never in bulk.** When you introduce or change the control block, the rule is that the missing fields get added *the next time a document is otherwise edited*, not in a standalone migration pass. A bulk retrofit rewrites every file in the set on one date, which destroys the modification history that told you which documents were actually live, produces a review queue nobody will work through, and buys nothing that waiting does not also buy. Put the rule in CLAUDE.md so Claude applies it unprompted when you ask for an unrelated edit.

---

## 5. One Register, and Everything Else Generated From It

A document register answers "which version was approved, and when" without opening any files. The moment there is more than one place that answers it, they disagree — usually within weeks, and always at the moment someone external asks.

**Structure it as one authored source and N generated views.** The source is a plain-text file — Markdown, CSV, whatever your tooling reads — because that is what merges, diffs and greps. The views are whatever people actually want: a spreadsheet tab, a formatted Word register, a derived-path column, a dashboard. A script regenerates all of them from the source in one pass.

**A hand-edit to a generated file is a defect, not a contribution.** State this plainly in CLAUDE.md, because it is not obvious and the failure is silent: someone corrects a status in the spreadsheet, the next sync overwrites it, and the correction is gone with no error anywhere. Claude's rule is to fix the source and re-run, and to revert rather than preserve an edit found in a generated file. This is [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md)'s definitions-versus-outputs separation applied to documents rather than folders.

**Put the invariants in the sync script, not in the guidance.** The rules that matter most are the ones a script can refuse to proceed on:

- A row cannot read `Approved` unless version, approver and approval date are all present. The script exits and names the offending row.
- Every identifier resolves to a file that exists at the path the register claims.
- No identifier is used twice; the next one issued is the highest plus one.

A rule stated in prose is followed until someone is in a hurry. A rule that stops a script is followed always. This is the same argument [Guide 22](./22_HELPER_APPS.md) makes about invariants in a small tool, and a register is a small tool.

**File the approval evidence where the register can point at it.** An email or chat approval is usually sufficient; what matters is that it is stored under a predictable name — identifier and date — so the register row and the evidence are one lookup apart rather than one search apart.

---

## 6. Shared Trackers: Merge by Identifier, Never by Position

Once a spreadsheet or table is edited by both people and Claude, it becomes the highest-risk file in the project. It looks like data, so it invites bulk operations, and it holds judgment, so a bulk operation can destroy work nobody can reconstruct.

Four rules, in the order they prevent damage:

1. **Read the live file first.** Not a cached copy, not what a previous session reported. The row you are about to overwrite may have changed an hour ago.
2. **Merge on the identifier, never on row position.** Clause ID, control ID, document reference. Row order is not stable — anyone who sorts a column has silently re-indexed the file, and a positional merge then writes every value into the wrong row while producing no error at all.
3. **Back up before any structural change**, to a path that is not the working folder.
4. **Verify nothing was silently lost.** Compare row counts and non-empty cell counts before and after. A merge that drops half the annotations reports success just as loudly as one that does not.

**Human markers mean something Claude does not know.** Highlighting, a colour, a flag column: these usually record a human judgment — "walked through this with the owner", "waiting on legal" — that no other field carries. Claude clearing them during a refresh destroys information silently. The rule to state is that Claude does not clear a human marker on its own initiative; if the underlying content changed, it says so and asks, or re-does the work that would justify re-marking.

If you have ever lost data in a shared tracker, write that incident and its date into CLAUDE.md alongside these rules. A safeguard with a story attached survives; a safeguard stated as best practice gets negotiated away by the next session in a hurry.

---

## 7. What This Looks Like in Practice

A worked sequence, showing which rules fire where.

> **You:** "The owner has commented on the Access Control Policy. Read me the comments."
>
> **Claude:** Reads the file, lists four comments with locations and the text each anchors to. No edit made.
>
> **You:** "Action 1, 2 and 4. Skip 3, I disagree with it."
>
> **Claude:** Brings the file into its environment, makes three tracked changes authored `Claude`, each with a `[Claude]` comment giving the reason and referring to the owner's comment number, runs the validator to confirm no untracked text changed, writes the file back to its original path, and reports which three it made and that comment 3 was left alone. Notices the document still carries an old-shape control block and adds the missing Doc Ref row from the template in the same pass — because the document was being touched anyway (§4).
>
> **You:** "Good. Finalise it."
>
> **Claude:** Does not. Says the revisions are pending your acceptance in Word, offers to group them, and notes that once you accept and approve, the register update and the `-DRAFT` rename are one command.
>
> **You:** "Accepted it, the owner approved it today."
>
> **Claude:** Updates the register source row — version, status, approver, date — re-runs the sync so the spreadsheet mirror and the Word register follow, renames the file to drop `-DRAFT`, and tells you where to file the approval email.

The shape to notice: Claude does everything up to the point of judgment, stops cleanly there, and resumes with the mechanical work the moment you supply the judgment.

---

## 8. The CLAUDE.md Block

Controlled-document behaviour has to be standing instruction. It cannot be a skill description alone, because the risky moment is a request that does not mention documents at all — "tidy up the policy folder" — and a skill that has not triggered protects nothing. Paths, not file types: `.docx` in a scratch folder is a draft.

```markdown
## Controlled documents

Controlled documents live under `<paths>`. Anything under `<draft paths>` is a draft
and these rules do not apply.

- Never edit a controlled document silently. Every change is a tracked change
  authored "Claude", paired with a comment starting "[Claude]" giving the reason.
  Run the docx validator afterwards to confirm no text changed outside a revision mark.
- Never accept a tracked change, mine or anyone's. "Finalise" and "clean up" mean
  leave the revisions pending and say so.
- Never write Approved by / Approved on / Approved status. Those record a human act.
- Filenames are stable and carry no version number. Version, status, owner, approver
  and date live in the control block and in the register. A `-DRAFT` suffix comes off
  at the moment approval is recorded.
- When editing or promoting a document whose control block is an old shape, add the
  missing fields from `<template path>` in the same pass. Never as a bulk retrofit.
- The register source is `<path>`. All other register views are generated by
  `<sync command>`. Never hand-edit a generated view; fix the source and re-run.
  An edit found in a generated view is reverted, not preserved.
- Before any structural change to `<tracker>`: read the live file, merge on
  clause/control ID and never on row position, back up to `<backup path>`, then verify
  no rows or annotations were lost. <Incident and date, if you have one.>
- Do not clear human markers (highlighting, flags) on my behalf. Say what changed
  and ask.
```

Keep it this long. This is a case where compression costs more than the tokens save: every line here exists because its absence has a specific, silent failure mode, and a shortened version reads as a preference rather than a boundary.

---

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| "Just apply your suggestions and give me the clean version" | Converts a proposal into an approval nobody gave; unrecoverable afterwards |
| Version numbers in filenames | Guarantees divergence between links, citations and reality |
| Bulk retrofit of a template across a document set | Destroys the modification history that told you which documents were live |
| A register that is also hand-maintained somewhere else | The two disagree within weeks, and you find out from an outsider |
| Correcting a status in the generated spreadsheet | Silently overwritten at the next sync, with no error |
| Merging a tracker on row position | Writes every value into the wrong row and reports success |
| Redlining under your own name | Six months later nobody can tell which clauses a model proposed |
| Reviewing a document "against the standard" | Produces a long shallow sweep; name the clause |
| Leaving the controlled-document rules to a skill | The dangerous request is the one that never mentions documents |

---

## Checklist

Before Claude touches a document set:

- [ ] Controlled and draft paths are named in CLAUDE.md, not decided per request
- [ ] A redline author name is set, and it is obviously not a person
- [ ] The control-block template exists as a file Claude can copy
- [ ] The register source is identified, and every other view is known to be generated

On every review:

- [ ] Changes are tracked, comments carry the reason, nothing edited silently
- [ ] The validator confirms no text changed outside a revision mark
- [ ] The file went back to its original path, and a concurrent edit would have blocked the write
- [ ] Revisions left pending; no accept-all, no approver or date filled in
- [ ] Old-shape control block topped up if the document was being touched anyway

On every register or tracker change:

- [ ] Source edited, views regenerated, no generated file hand-edited
- [ ] Approved rows carry version, approver and date, enforced by the script
- [ ] Live file read first; merged on identifier; backed up; loss check run
- [ ] Human markers left alone
