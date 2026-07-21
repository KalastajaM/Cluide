# 23 — Multi-Project Setups

> How to design and maintain several linked Cowork projects so shared facts stay consistent and each one stays focused. This is the cross-*project* extension of Guide 09 (which handles shared state and ownership across multiple *tasks* inside one assistant).

Most setups start as one project and should stay that way. You reach for multiple projects when a single `CLAUDE.md` and folder start pulling in two directions at once: different purposes, different lifecycles, or data that keeps colliding. This guide covers when that moment has arrived, how to split cleanly when it has, what to do when two independent projects grow an overlap instead, and how to keep linked projects consistent and change them without breaking each other afterward.

## When to split

Prefer one project until it actively hurts. A single project is cheaper to reason about, mount, and audit. Split only when at least one of these is clearly true:

- **Two purposes, one folder.** The project serves two audiences or two jobs that share almost no files, and the `CLAUDE.md` has to context-switch to describe both.
- **Different lifecycles.** One part changes daily while another is a stable archive; one is active work while another is finished and kept for reference.
- **Data that keeps colliding.** The same fact is being restated in several places and drifting, or two workflows keep editing the same file for different reasons.
- **Access boundaries.** Part of the work needs to be mounted, shared, or scoped separately (for example, something you want to share without exposing the rest).

Signs you should **not** split: the folder is merely large but coherent; you only want tidier subfolders (use folder structure, not a new project); the parts are edited together in the same workflow. Splitting has a real cost (cross-project references, extra mounts, and the ownership discipline below), so the collision has to be worth paying for.

The best seam almost always follows a **data owner**: split so that each shared fact ends up with exactly one project that naturally owns it. If you cannot name the owner of a fact after the split, the seam is in the wrong place.

## How to split

Splitting is a move-and-rewire operation, not a copy. The failure modes are all variants of "copied instead of moved" (now two owners) and "moved but did not rewire" (dead references). Work through it in order.

1. **Name the seam and the owner.** State in one sentence what the new project is for, and which shared facts it will own after the split. Everything else stays put. If facts do not cleanly land on one side, stop and re-cut the seam.

2. **Inventory what moves.** List every file, folder, skill, task, memory entry, and `CLAUDE.md` rule that belongs to the new project. Separately list the shared facts that will now cross the boundary; these become entries in the ownership registry (below). Do this before touching anything.

3. **Scaffold the new project.** Create the new folder with its own `CLAUDE.md` (purpose + local rules), a `README`, and a layout consistent with your other projects (see the `PROJECT_TEMPLATE`). If the project is under git and history matters, preserve it (for example with `git subtree split` or `git filter-repo`) rather than starting fresh; if history does not matter, a clean copy of just the moved files is fine.

4. **Move, do not copy.** Move the owned content into the new project. In the old project, replace what you moved with a **pointer** to the new owner, never a duplicate. A duplicated fact is a second owner waiting to drift.

5. **Rewire every reference.** Update all cross-project mentions to point at the new owner. Fix skills, tasks, and paths that referenced the moved files. Check both projects for dead references: the old project pointing at files that left, and the new project pointing back at things that stayed.

6. **Re-scope memory and tasks.** Split memory files along the seam so each project's memory describes only its own facts. A scheduled task that spanned the old project may need to be split or re-pointed; if a task now depends on data owned by the other project, give it an explicit link and a freshness check rather than a silent assumption.

7. **Verify both sides.** Audit each project: no dead references, `CLAUDE.md` matches the folder contents, each shared fact has exactly one owner. Mount both projects together and confirm the cross-project references actually resolve and the workflows still run end to end.

8. **Decommission the old copy.** Archive what was moved (prefer archiving over deleting) and record the split. Do not leave a stale duplicate behind "just in case"; that is the drift you just paid to remove.

Merging projects is the inverse: pick the surviving owner, move content in, collapse the two ownership entries into one, rewire references, and archive the absorbed project.

## When independent projects overlap

Not every multi-project setup comes from a deliberate split. More often you have a project about topic X, later start one about topic Y, and Y turns out to need knowledge that lives in X. The projects converged instead of being carved apart, whether by accident or by design. The same single-owner discipline applies, but now you are retrofitting it onto projects that were never built to link.

Resolve the overlap one of three ways, in order of preference:

1. **Reference the existing owner.** If the shared knowledge is genuinely *about* X and X maintains it well, X stays the owner and Y links to it. Mount X when Y needs it, and add the fact to the ownership registry with X as owner and Y as a referencer. This is the default and the cheapest.
2. **Extract a shared owner.** If the knowledge is common to several projects and not really "about" any one topic (it only lives in X because X came first), move it into a dedicated reference project that both X and Y consume. Guide 15 (LLM Wiki) is that pattern. Reach for this once a second or third project needs the same facts, or when X and Y would otherwise both claim them.
3. **Never duplicate.** Copying X's knowledge into Y feels fast and is exactly what bites you later: two copies, two owners, silent drift. If you catch yourself pasting, stop and take option 1 or 2.

Retrofitting the link:

- **Pick the owner deliberately.** The owner is the project where the fact is most at home: most detailed, most actively maintained, most naturally updated. If neither X nor Y is a good home, that is the signal to extract (option 2).
- **Keep the dependency one-way.** Y depends on X, not each on the other. If X starts depending on Y's copy of the same knowledge, you have a circular dependency; extract the shared part into its own owner and have both reference it.
- **Catch divergence early.** If the knowledge already got copied into both and they have drifted, reconcile to one owner and convert the other to a pointer (see "Keeping linked projects consistent"). Caught early it is a one-line pointer; caught late it is a reconciliation.

## The single-owner principle

Once you have more than one project, the rule that keeps them sane is: **every shared fact has exactly one owning project. Everyone else references it; no one else restates it.** A "shared fact" is anything described in more than one project: a value, a date, a decision, a status, an entity. The owner holds the canonical version, and referencing projects link to it.

This is the same principle Guide 09 applies to multiple tasks sharing state, raised to the project level. When two projects both assert a fact, they will eventually disagree, and you will not know which is right.

## Ownership registry

Track ownership explicitly in one place, a small table in whichever project coordinates the others (or in the owner of the domain). One row per shared fact:

| Fact / topic | Owner | Canonical location | Referencing projects | Last verified | Status |
|---|---|---|---|---|---|

- **Owner** is the single project whose value is authoritative.
- **Canonical location** is the exact file inside the owner that holds it.
- **Referencing projects** are the ones that mention it and must link rather than restate.
- **Last verified** is when the references were last confirmed to match the owner.

The registry is what makes drift detectable: to check consistency, you verify each referencing project still points at the owner and has not grown its own copy.

## Cross-project linking conventions

- **Link to the owner, quote sparingly.** A referencing project should point at the canonical location, not paste the value. If it must show the value inline for readability, mark it as a mirror of the owner and note where the truth lives.
- **Keep pointers durable.** When the owner moves or renames the canonical file, update every referencing pointer in the same change. A pointer to a moved file is a dead reference.
- **Reference across a mount, not a guess.** A project can only read another that is mounted in the same session. If the owner is not mounted, say so and stop; do not act on a remembered value.

## Keeping linked projects consistent

- **Detect drift** by scanning for the same fact stated in more than one project and comparing values, and by checking that each referencing pointer still resolves.
- **Reconcile to the owner.** When a referencing copy disagrees, the owner wins unless the owner is the one that is stale; either way, one value survives and the rest become pointers.
- **Respect each project's own rules.** A project's local `CLAUDE.md` is authoritative for that project. Never silently edit another project's data to enforce consistency; surface the conflict and let the owner decide.
- **Freshness over cleverness.** Prefer an explicit "last verified" date and a periodic recheck to any scheme that assumes references stay correct on their own.

## Changing a linked project without breaking the other

When projects are linked, a change in one can break the other, and the direction decides the risk. Say X consumes from Y: Y owns the knowledge, X references it.

- **Modifying the consumer (X) is safe for the owner (Y) as long as X only reads Y.** A referencing project that never writes into its owner cannot break it. Keep consumption read-only and one-way, and X is free to change without touching Y. The only ways a change to X breaks Y are if X writes into Y's files, or the dependency is secretly circular (Y also reads X). Both are signals to fix the coupling, not to tiptoe around it.
- **Modifying the owner (Y) is the change that breaks consumers.** Y's canonical files and facts are a contract X relies on. Renaming or moving a canonical file, changing a fact's format or meaning, or deleting something referenced will break X.

Treat the consumed set as that contract:

1. **Know the surface.** Write down what each consumer relies on: which files, which facts. The ownership registry already carries this, since the "referencing projects" column tells an owner who depends on it. Anything not in that surface is internal and free to change.
2. **Check impact before changing the surface.** Before you rename, move, reformat, or delete anything in the surface, look up who references it and mount those projects. An empty registry entry is not proof of no dependents; if unsure, grep the linked projects for the path or the fact.
3. **Prefer non-breaking changes.** Add rather than rename. Keep the old canonical location working, or provide the new form alongside the old and migrate consumers before removing it.
4. **When you must break it, fix the dependents in the same change.** Update every referencing pointer as part of the edit, not afterward. A surface change and its rewires are one unit of work.
5. **Verify like a test.** Mount both projects, confirm references resolve, and run the dependent's workflow end to end. This is the cross-project equivalent of running the tests after a change.

## Anti-patterns

- **Duplicating instead of pointing.** The single most common cause of cross-project drift.
- **Splitting mid-workflow.** Cutting a seam through a process that is edited as one unit, so a task now breaks across two projects.
- **Orphaned references.** Moving a file without rewiring the projects that pointed at it.
- **Implicit coupling.** One project quietly depending on another's file with no link and no freshness check.
- **Two owners.** No registry, so two projects both believe they are authoritative.

## Short version

1. Stay in one project until two purposes, two lifecycles, or colliding data force a split.
2. Cut the seam along a data owner: after the split, every shared fact has one clear owner.
3. Split by moving, not copying; leave a pointer behind, never a duplicate.
4. Rewire every reference and check both sides for dead links.
5. When a new project needs knowledge from an existing one, reference the owner or extract a shared project; never copy.
6. Track shared facts in an ownership registry: owner, canonical location, referencers, last verified.
7. Referencing projects link to the owner and never restate its facts.
8. Reconcile drift to the owner; never silently edit another project's data.
9. Before changing what a project owns, check who references it, prefer non-breaking changes, and rewire dependents in the same change. A read-only consumer can never break its owner.
