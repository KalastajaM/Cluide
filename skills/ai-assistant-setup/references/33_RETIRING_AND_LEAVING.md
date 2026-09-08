# Retiring and Leaving: Ending a Task, a Project, or an Account Without Leaving Live Wires

> This repo is thorough about starting things and almost silent about ending them. [Guide 16](./16_BEST_PRACTICES.md) has one line on retiring a task. [Guide 23](./23_MULTI_PROJECT_SETUPS.md) decommissions a duplicate after a split. [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) says archive rather than delete. `tasks/relocate-project.md` moves a project and is the closest thing to a procedure — and its central insight is the one this guide starts from: a project is not a folder but a set of references to that folder, held in places you do not look at. Stopping a project leaves every one of them live. This guide is the ending as a rewiring operation: retiring a task, retiring a project, and the larger case of leaving an organisation or an account, where the question becomes which parts of your setup were ever yours to take.

> **Companion guides:** [Guide 23](./23_MULTI_PROJECT_SETUPS.md) owns the ownership registry that §3 transfers from. [Guide 04](./04_MEMORY_AND_PROFILE.md) is the source for which memory layer lives where (§5 depends on it). [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)'s mirror block is what makes the app-side fields recoverable at all. [Guide 21](./21_COMPANY_POLICIES.md) is the mechanism by which an employer's policies, including any about what leaves with you, reach a session. [Guide 12](./12_SECURITY.md) §1 covers revoking credentials. [Guide 11](./11_GIT_INTEGRATION.md) is the archive mechanism. `tasks/retire-project.md` runs §2–§4; `tasks/relocate-project.md` is the sibling procedure for a project that continues elsewhere.

> **Giving this guide to Claude:**
> "Read 33_RETIRING_AND_LEAVING.md. I want to retire the project `<name>`. Run the §2 inventory read-only and show me everything that still points at it, grouped by layer, before proposing anything."

---

## 1. Stopping Is Not Ending

A project you have stopped using still has a scheduled task registered against it, which fails quietly on a schedule or, worse, keeps running against stale data and producing output nobody reads. It still holds a row in an ownership registry, so the facts it owned have an owner who will never update them. Other projects still link to it. Memory — every layer [Guide 04](./04_MEMORY_AND_PROFILE.md) lists, plus the per-project store a Cowork project keeps — still describes it in the present tense and shapes how requests are read. Its app-side description still loads into any session that opens it. Connectors it was granted still hold their tokens. Its Claude Code state still sits under a path name.

None of this breaks visibly. That is the problem. A broken reference to a *moved* project fails loudly the first time something follows it; a reference to a *stopped* project resolves fine, to a folder that is simply no longer true. The stale fact propagates, the disabled task gets re-enabled by a well-meaning cleanup, the memory line about an "ongoing" project steers a session six months later.

So the rule: **a project is retired when nothing current points at it, not when you stop opening it.** The inventory in §2 is how you find what points at it; the transfer in §3 is what to do about the facts it owned; the freeze in §4 is the state it ends in.

---

## 2. The Inventory: What Points at It

Read-only, before any decision, and by layer — because the layers a naive search misses are the ones that hurt. This is the same set `tasks/relocate-project.md` sweeps for a move, with three additions a move does not need: memory, credentials, and the ownership registry.

| Layer | Where to look | Why it matters at an ending |
|---|---|---|
| **Other projects** | `grep -rIn "<project name>"` across the projects root, plus the coordinator's registry if you run one ([Guide 23](./23_MULTI_PROJECT_SETUPS.md)) | Cross-project links become dead pointers; a registry row becomes an owner that never updates |
| **Scheduled tasks** | Every task definition and every registration, wherever your surface keeps them — Cowork's task registrations, Claude Code Routines, hooks that fire on a schedule | A disabled task is a stale reference with a switch; someone flips it |
| **Orchestration** | [Guide 09](./09_MULTI_TASK_ORCHESTRATION.md) chains and shared-state files that named this project's task as a stage | The downstream stage waits for a handoff that never comes, or reads a file that stopped updating |
| **Memory** | Account memory (Settings → Memory); the Cowork project's own per-project memory store; Claude Code auto memory; `.auto-memory/` in *other* projects; profile files in tasks | Present-tense lines about a dead project steer future sessions; this is the layer that outlives everything else, and two of its stores are app-side and invisible to a grep |
| **Second brain** | Notes and index entries that link into the project ([Guide 28](./28_SECOND_BRAIN.md)) | The links stay resolvable and stop being true |
| **App-side fields** | The project's description and instructions in the app; its row in `spaces.json` ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)) | The description is injected as identity into any session that opens the project, retired or not |
| **Artifacts** | Published pages and the generators that feed them | A dashboard fed by a retired task renders stale data with no error, indefinitely |
| **Credentials and grants** | Connector authorisations, app grants for computer use, tokens in a keychain or `.env` scoped to this project | A grant nobody uses is a grant nobody watches ([Guide 12](./12_SECURITY.md)) |
| **Claude Code state** | `~/.claude/projects/`: transcripts under a path-derived name, auto memory under a repository-derived one ([Guide 04](./04_MEMORY_AND_PROFILE.md)) — locate them separately | Orphaned under a name nothing resolves; can be collected without warning |
| **Git** | The remote, any open branches, any other repo that submodules or references it | A public remote for a retired project keeps publishing whatever was last pushed |

Classify every hit the way `relocate-project.md` does: a mention in a dated report is history and stays; a mention in a task definition is load-bearing and must go; a mention in another project's CLAUDE.md is a pointer that needs a new target or a removal. The classification is the work; the edits are mechanical afterwards.

---

## 3. Transfer Ownership Before You Touch the Folder

If the project owned any shared fact — a contact list other projects read, a calendar of dates, a canonical figure — then retiring it without naming a successor recreates exactly the drift [Guide 23](./23_MULTI_PROJECT_SETUPS.md) exists to prevent, with the added twist that the stale owner can no longer be asked.

For every fact in its registry rows, one of three outcomes, written down:

- **Transferred** — a named surviving project now owns it, the content has moved there, and every consumer's pointer has been rewired to the new owner. Move, never copy: the retired project keeps a pointer, not a duplicate.
- **Retired with the project** — the fact is no longer needed by anyone. Say so in the registry, with the date, so the next person who goes looking finds a decision rather than a gap.
- **Frozen** — the fact is historical and will not change (the final state of a closed matter, say). It stays in the archived project, the registry marks it frozen and points at the archive, and consumers that needed it as *current* are rewired to whatever replaced it.

Do this before archiving, because the transfer is the only step that needs the retiring project fully readable and mounted alongside its successors. An archived project can be reopened, but by then the consumers have been rewired around a gap and the transfer is a repair rather than a move.

Memory follows the same rule. Lines in *other* projects' memory files that describe this project's facts as current are rewired to the new owner or removed. Entries in account memory that say "currently working on" are removed, and the project's own per-project store is read before the project leaves the app — anything durable and still true in it moves to the successor's folder-bound memory, because that store goes with the project. Account memory is where a dead project lives longest: nothing in it is versioned and no audit runs against it by default. `tasks/audit-memory.md` finds the on-disk lines if you name the project; the app-side stores you search by hand.

---

## 4. The Freeze

What a retired project looks like when it is done. Every item below is a state to reach, and the verification at the end checks the state rather than trusting the steps.

**A `RETIRED.md` at the root**, dated, saying why it was retired, where each owned fact went (the §3 outcomes), what replaced it if anything, and a line stating that nothing current should point here. This file is the thing a future session finds first, and it is what stops the project being resurrected by accident: a folder with a `RETIRED.md` is not a candidate for cleanup, reorganisation, or a fresh audit.

**Git: a final commit, a tag, and a decision about the remote.** Tag `retired-YYYY-MM-DD` on the final commit. If the remote is public, either archive the repository on the host (read-only, still visible) or make it private; a retired public repo that is neither is a page that keeps publishing under your name. Open branches are merged or deleted; there is no "later".

**Scheduled tasks deleted, not disabled.** [Guide 16](./16_BEST_PRACTICES.md) gives the sequence — disable the schedule, archive the task folder to git, then remove it — and the point here is that the last step is the one people skip. A disabled task is the reference most likely to be re-enabled by a cleanup that does not know why it was off. The task folder goes into the archive with the project; the registration is removed. If the task must survive because a successor project needs it, it is moved and re-pointed under `relocate-project.md`'s scheduled-task layer, not left in place.

**Orchestration stages removed.** A chain that named this task as a stage has the stage removed and the downstream stage's dependency rewritten — with a freshness check if it now reads a file the successor produces ([Guide 23](./23_MULTI_PROJECT_SETUPS.md), step 6).

**App-side fields set to retired, then the project leaves the app.** You paste the description as a one-line "Retired YYYY-MM-DD, see RETIRED.md" and empty the instructions field — a session cannot write these fields, it produces the text ([Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md)). The mirror block in CLAUDE.md records both, which is the last time the mirror is updated. Set the fields *before* removing the project from the app's list or moving it to whatever archived state your registry keeps, so that anyone who opens it in the interval is told first. The per-project memory store is read out before this step, because it leaves with the project.

**Grants revoked.** Connector authorisations the project alone used; computer-use grants for apps only its tasks needed; tokens scoped to it rotated or deleted. [Guide 12](./12_SECURITY.md) §1 rotates tokens on a schedule; a credential whose project is gone has no schedule and no one reading its logs, which is a reason to treat it as exposed now rather than at the next rotation.

**The folder archived**, per [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md): moved to the archive location, never deleted, never read from by a live session. Claude Code's state for the project — transcripts and auto memory, located separately as §2 says — is renamed or merged alongside, so the history survives under a name that can be found.

**Verification**, which is the point:

- Re-run the §2 inventory. Every remaining hit is a classified *history* mention. Nothing load-bearing, nothing present-tense.
- Every scheduled-task registration resolves to a project that is not this one.
- The ownership registry has no row naming this project as a current owner.
- Account memory, searched for the project's name, returns nothing in the present tense; the per-project store has been read out.
- The app lists the project as retired or not at all.
- No grant, token or connector authorisation is scoped to it.

Report by layer: what was rewired, what was removed, what was deliberately left as history.

---

## 5. Leaving: What Was Ever Yours to Take

An organisation account, a change of employer, a personal account that accumulated work material, an account you are closing. The retiring procedure runs per project; leaving runs across the whole setup, and its first question is different: not *what points at this* but *which layer does this live in, and who owns that layer*.

| Bound to | What lives there | What that means when you leave |
|---|---|---|
| **The account** | Account memory; each Cowork project's per-project memory store; account-level instruction fields; account-installed skills; Cowork projects' app-side fields; scheduled tasks and Routines; published artifacts; chat and session history; connector authorisations and their tokens | Goes with the account. In an organisation account it belongs to the organisation and may be visible to its administrators; in a personal account it is yours and is lost only if you close it |
| **The folder** | Project folders, `CLAUDE.md`, skills in the project, `.auto-memory/`, profile files, task definitions, outputs, git history | Yours if the disk and the repo are yours; the employer's if they are on employer equipment or in an employer repo |
| **The machine** | Claude Code auto memory under `~/.claude/projects/`, `~/.claude/settings.json`, hooks, agents, `~/.claude.json`, the desktop app's state | Stays on the machine. On employer equipment it leaves with the laptop |

Two things follow from the table that people find out late.

**The app-side fields and the app-side memory stores are the layers you cannot `cp`.** This is the practical reason [Guide 25](./25_PROJECT_INSTRUCTION_LAYERS.md) keeps a versioned mirror of the description and instructions fields in CLAUDE.md, and why `templates/ACCOUNT_INSTRUCTIONS_TEMPLATE.md` exists as a file: at a departure, the mirror is the export. Account memory and a project's per-project store can be read and edited in the app but have no export you should rely on being there; the durable form of what they hold is the `.auto-memory/` and profile files a project keeps on disk ([Guide 04](./04_MEMORY_AND_PROFILE.md)), which is one more argument for keeping the reliable layer the folder-bound one.

**Contamination runs both ways.** A personal account accumulates employer facts — contacts, project names, figures — in memory and in projects; an employer account accumulates personal ones. Leaving means purging each from the other. The employer's policy governs the first direction, and if it is wired in through [Guide 21](./21_COMPANY_POLICIES.md)'s mechanism it will already be telling sessions what may not leave; your own judgement governs the second. Neither purge happens by itself.

The procedure, in the order that keeps it recoverable:

1. **Inventory by layer**, using the table. Every project, every task, every skill, every memory store, every grant: which column is it in, and who owns that column.
2. **Decide per item: keep, transfer, or purge.** Keep means it is yours and stays where it is. Transfer means it moves to a layer you will still have — a project folder to your own disk, a skill from the account to a folder, a Cowork project's fields into its mirror block. Purge means it is theirs and leaves your possession, or it is yours and leaves theirs. Write the decisions down; a departure is a controlled process and a list is what makes it one.
3. **Export what has no file form.** Read the app-side fields into their mirror blocks (for any project whose mirror is stale, this is the last chance). Read account memory and write what is durable and yours into the folder-bound memory of the project it belongs to. Write down which account skills you rely on and where their source lives.
4. **Purge, both directions.** Employer material out of personal memory and projects; personal material out of employer projects and the employer account's memory, where you are permitted to edit it. Search by name, not by feel.
5. **Revoke and rotate.** Every connector authorisation the leaving account granted; every token in a keychain or `.env` that a task under that account used. Then retire the tasks themselves (§4), because a scheduled task that survives an account it no longer has credentials for fails on a schedule forever.
6. **Verify from the other side.** Log in to what remains and search for what should be gone. A purge you have not checked from the receiving end is a purge you believe in.

Do this before the last day, not after. Access ends before you remember the thing you meant to export.

---

## 6. Retiring a Task

The smallest case, and the most common: a task built for a project or a period that has ended.

Disable the schedule first, so nothing runs mid-procedure. Then remove every reference to it — orchestration chains, shared-state files it wrote to, a coordinator's registry. Then the memory it alone relied on: profile files under its folder go with it; lines in the project's `.auto-memory/` that exist only for it are removed. Then credentials it alone held. Then the task folder into `_archive/` with a dated note, and the registration deleted — not left disabled. Then verify that nothing resolves to it and that the project's `CLAUDE.md` file map no longer lists it.

A task whose *purpose* continues but whose *form* has ended — it is being replaced by a better one — is not retired but succeeded: the successor is set up first, run alongside for enough cycles to trust ([Guide 29](./29_SPEC_BEFORE_REBUILD.md) keeps the old version as the oracle), and only then is the old one retired by this procedure.

---

## Anti-Patterns

| Anti-pattern | Why it bites |
|---|---|
| Disabling a scheduled task instead of deleting it | A cleanup re-enables it; a stale reference with a switch |
| Deleting the folder before transferring owned facts | Consumers rewired around a gap; the transfer becomes a repair with the source gone |
| "Keeping a copy just in case" in the old location | The duplicate owner [Guide 23](./23_MULTI_PROJECT_SETUPS.md) just paid to remove |
| Leaving present-tense memory lines about a dead project | Steers sessions for years; account memory has no audit by default |
| Retiring a project whose public remote stays live | Keeps publishing under your name after you stopped looking |
| Treating a departure as copying folders | The account and machine layers do not copy; the mirror block and folder-bound memory were the export |
| Purging only one direction | Employer facts stay in personal memory, or the reverse, and surface in the wrong place later |
| Leaving grants for a project nobody opens | The credential nobody watches is the one to assume exposed |
| Resurrecting a project by reorganising it | A folder with `RETIRED.md` is not a candidate for cleanup |
| Exporting after access ends | It does not |

---

## Checklist

Retiring a project, in order:

- [ ] Inventory (§2) before any decision; every hit classified
- [ ] Ownership outcomes (§3) recorded before the folder is touched
- [ ] Freeze (§4) reached and its verification list passed — the list there is the check; do not shorten it here
- [ ] Nothing was deleted; nothing was left disabled

Leaving:

- [ ] Every item placed in the account / folder / machine column with its owner
- [ ] Keep / transfer / purge decided per item and written down
- [ ] App-side fields in mirror blocks; durable account-memory facts in folder-bound memory
- [ ] Purged in both directions, by search
- [ ] Every authorisation revoked, every token rotated, dependent tasks retired
- [ ] Verified from the remaining side, before access ended
