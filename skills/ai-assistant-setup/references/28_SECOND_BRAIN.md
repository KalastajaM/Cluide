# Second Brain: A Personal Knowledge Layer Claude Can Read

> A second brain is the layer above your projects: the notes, clippings, decisions and reference material that belong to your working life rather than to any one piece of work. The classic advice for building one — capture everything, organise it into buckets, distil as you read, review weekly — was written for a reader who cannot search their own filing cabinet. Claude can. This guide covers what survives that change, what stops being worth the effort, and how to build the layer so it stays useful instead of becoming an archive nobody opens.

> **Companion guides:** [Guide 15](./15_LLM_WIKI.md) is the closest neighbour and the boundary is the point. Guide 15 builds a wiki *about a subject* — one domain, deliberately curated, where every new source enriches existing pages. This guide covers the layer *about your work* — many domains, mostly uncurated, where the job is triage rather than synthesis. Most people need both, and mixing them ruins both. [Guide 04](./04_MEMORY_AND_PROFILE.md) is the third neighbour: memory holds facts about *you* that Claude needs in order to behave correctly, not material you want to consult. [Guide 24](./24_PROJECT_FOLDER_STRUCTURE.md) is the layout *inside* one project; this is the layer above them, and its `incoming/` folder is a per-project intake queue rather than the inbox described here. [Guide 23](./23_MULTI_PROJECT_SETUPS.md) decides when knowledge earns its own project. [Guide 14](./14_PERSONAL_DATA_LAYER.md) covers structured personal data, which does not belong in notes at all.

> **Giving this guide to Claude:**
> "Read 28_SECOND_BRAIN.md. Here is what I currently keep and where [describe it]. Tell me whether a second brain layer is worth building for me, and if so, what the four homes and the index should look like."
>
> **Faster alternative:** `tasks/setup-second-brain.md` applies the objection test first, then interviews you and builds or repairs the layer without reading the guide first.

---

## First, the Objection

Most second brains die. They die the same way: capture is frictionless and enjoyable, triage is neither, so the inbox grows, the ratio of unread to read gets embarrassing, and consulting the thing stops being worth the guilt. The literature calls the underlying error the collector's fallacy — the feeling of having saved something standing in for the work of having understood it.

An LLM does not fix this. It makes the first half cheaper and leaves the second half exactly where it was. Worse, Claude can now read your email, your drive, your repos and your project folders directly, which removes one of the original reasons for a curated middle layer: you no longer need a personal copy of a document in order to search it.

So the test is narrower than the usual advice implies. A second brain earns its keep when it holds something no source system holds:

- **Your synthesis of material that lives somewhere else.** The three paragraphs of "what this 90-page regulation actually means for us" that exist nowhere but in your head.
- **Decisions and their reasons.** Source systems record what was decided. They rarely record why, what was rejected, and what would change the answer.
- **Material whose source is unreliable or unsearchable.** Things you read once on a site that will be gone, conversations, things people told you.
- **Cross-cutting connections.** The link between what a supplier said in March and a clause you signed in June, which no single system can see.

If what you are about to save is none of these — if it is a document that will still be searchable in its own system next year — a link and a sentence is the right note, and the full copy is clutter. Read the rest of this guide with that filter on.

---

## What Changes When Claude Is the Reader

The standard second-brain methods are retrieval aids designed for a human with no search. Four of them change materially once an LLM reads your notes.

**Tags and taxonomies matter much less.** Their job was to let you find a note whose title you had forgotten. Claude greps. A carefully maintained tag vocabulary costs you discipline on every note and buys back something a search already does. Keep tags only where they encode something not present in the text — status, confidentiality, review date. Drop the topical ones.

**Distillation shifts from a speed aid to a context aid.** Progressive summarisation — the layered bolding and highlighting that lets you re-read a long note in ten seconds — solves a problem Claude does not have. What distillation still buys is real but different: a 200-word synthesis costs a fraction of the context of the 12-page source, and a note that states a conclusion cannot be misread the way raw material can. You distil to make loading cheap and meaning unambiguous, not to make re-reading fast.

**You can capture rawer than the classic advice allows.** Because distillation is cheap on demand, the instruction to process each item as you save it is no longer the only safe path. This is a genuine relaxation, and it is also a trap: rawer capture makes the collector's fallacy easier, not harder. The compensation is that the inbox rule has to get *stricter*, not looser. See below.

**Format beats features.** Notes in Notion, Roam or an app database are effectively invisible to Claude unless a connector exposes them, and connectors return search results rather than a browsable tree. Plain markdown files in a folder Claude can mount are readable, greppable, diffable and version-controllable. Obsidian is a good choice precisely because it is a viewer over markdown on disk rather than a database. If you take one structural decision from this guide, take that one.

What does *not* change: atomic notes still beat long ones, links still beat isolation, and an inbox that never empties is still a failure rather than a backlog.

---

## The Four Homes

The useful part of PARA is not the acronym, it is the sorting question: *what makes this note stop being relevant?* Four different answers, four homes.

```
second-brain/
├── index.md          ← the map: what lives where, what changed recently
├── inbox/            ← unsorted, everything lands here, must be emptied
├── projects/         ← tied to something with an end date
├── areas/            ← ongoing responsibilities with no end date
├── resources/        ← reference material, no owner, might be useful
└── archive/          ← finished or dormant, kept for the record
```

**`projects/`** — notes attached to something you are actively trying to finish. The apartment sale, the migration, the certification. A project note stops being relevant when the project ends, at which point the whole folder moves to `archive/`. This is the folder with the highest turnover and the shortest useful life per note.

**`areas/`** — responsibilities you maintain indefinitely: your finances, your health records, a property you own, a domain you are the expert on at work. Area notes are never "done" and rarely archived; they are revised. If you find yourself writing the same kind of note repeatedly under different project names, it is an area.

**`resources/`** — material with no owner and no deadline that you expect to want again. Reading notes, technique writeups, a summary of a law, a supplier comparison. This is the folder that grows without limit and needs the most aggressive pruning, because everything that fails the sorting question elsewhere ends up here by default.

**`archive/`** — everything above, once dormant. The point of archiving rather than deleting is that Claude can still search it on request while it stays out of the way of everything routine. Archive by moving the folder intact; do not flatten it.

Two rules make this hold together. First, **the home is decided by relevance decay, not by topic.** A note about tax rules is a `resources/` note; a note about *your* 2026 tax return is a `projects/` note; a note about how you handle tax every year is an `areas/` note. Same topic, three homes, because they die at different times. Second, **when in doubt it goes to `resources/`**, and the weekly review moves it if it was wrong. Hesitating over placement is the friction that kills the habit.

If your notes span work you would not want in the same place — a client's material and your own, say — that is a signal for separate roots rather than separate top-level folders. [Guide 23](./23_MULTI_PROJECT_SETUPS.md) covers the split.

---

## Capture and the Inbox

Everything new lands in `inbox/` as a file. No sorting at capture time, no decision about which home, no required format. The only thing capture must produce is a file with enough context to be triaged later — which in practice means a title, the source, the date, and why you saved it.

```markdown
---
captured: 2026-08-12
source: https://example.com/article
why: possible answer to the retention question in the migration
---

[paste, link, or two lines of your own]
```

That `why` line is the highest-value field in the whole system and the one most often skipped. Without it, triage a fortnight later cannot distinguish "this mattered" from "this looked interesting", and the default becomes keeping everything. With it, most items can be resolved in seconds — the question it was saved for has since been answered, so the note is deleted rather than filed.

Practical capture routes: a browser clipper writing markdown into `inbox/`, a plain text file you append to during the day, meeting notes dumped verbatim, or asking Claude to write the note for you at the end of a session ("save what we concluded about X to the inbox, with the reasoning"). The last one is underused and produces the best notes in the system, because the synthesis has already happened.

**The one rule: the inbox is emptied, not managed.** An inbox with permanent residents is not an inbox, it is a `resources/` folder with a misleading name — and once it becomes one, capture stops feeling free and the habit decays. Empty it on a fixed cadence (weekly is enough for most people) and accept deletion as the most common outcome. If you cannot empty it weekly, you are capturing too much; tighten the filter from the first section rather than extending the cadence.

A project folder can have an intake folder of its own (Guide 24 calls it `incoming/`, and the emptying rule there is this one). The two are not interchangeable. Anything landing in a project's `incoming/` is already known to belong to that project, so triage only picks a folder; anything landing here has no home yet, and triage may well decide it should not have one. Give them different names and the ambiguity disappears.

---

## Triage and Distillation

Triage is the weekly pass over `inbox/`. For each item, exactly one of four outcomes:

| Outcome | When |
|---|---|
| **Delete** | The question it was saved for is answered or gone. Should be the most common. |
| **File as-is** | Already short, already clear, already the note you want. Move it. |
| **Distil, then file** | Worth keeping, but the value is buried in bulk. Write the synthesis, keep the link, discard or archive the raw material. |
| **Act, then delete** | It was a task wearing a note's clothing. Put it where tasks live and remove it from here. |

That last row catches a common leak: second brains fill with disguised to-dos, and a note that is really an action will neither be done nor be useful as knowledge.

Distillation is the step to hand to Claude, and it is worth being specific about what you are asking for, because the default output is a summary and a summary is not what you want. A summary compresses what the source says. A distilled note states what you concluded, what it applies to, and what would change your mind — which is the thing your source cannot provide and the thing you will actually want back.

> "Read the file in inbox/ and write a distilled note for resources/. State the conclusion first in one paragraph. Then: what it applies to and what it does not, anything the source asserts without evidence, and what would change the conclusion. Keep the source link. Do not summarise the structure of the original. Under 300 words unless the material genuinely needs more."

**One idea per note.** Not for purity — because a note about two things is filed under one of them and lost to the other, and because loading a 3,000-word omnibus note to answer a narrow question wastes most of what it costs. Split at the point where you would need a new heading.

---

## Making It Findable

The index is the part that makes the difference between a second brain and a folder of files, and it is the part most often missing.

`index.md` is a map, not a table of contents. It holds: what each home currently contains in a sentence, the ten or fifteen notes that get consulted most, anything in flight, and a short recent-changes list. It should be small enough that reading it is never a decision — under a hundred lines. When Claude starts a session against your notes, this is the file it should read first, and it should be able to tell from the index alone which two or three files to open next. That is progressive disclosure applied to your own knowledge: the index is always affordable, everything else loads only when a question reaches it. [Guide 02](./02_PROMPTING_BASICS.md) covers the principle; [Guide 03](./03_SKILLS.md) covers the same structure inside a skill.

Beyond the index, three conventions carry most of the retrieval weight:

**Filenames that state the content.** `2026-03-vat-treatment-of-intra-eu-services.md` beats `vat-notes-3.md`. Claude reads filenames before it reads files, and a directory listing of good filenames is often enough to answer the question without opening anything. Date-prefix notes whose relevance is time-bound; do not date-prefix reference notes.

**Frontmatter for what the text does not say.** Status, review date, confidence, source, whether something is superseded. Not topic tags. A `superseded_by:` field is worth more than any tag you will ever write, because contradiction between old and new notes is the failure mode that actually damages answers.

**Links where a link changes an answer.** Cross-linking everything to everything produces a graph that looks impressive and helps nobody. Link when reading note A without note B would produce a wrong conclusion. Those links are the ones worth traversing, and they let Claude follow a thread across three notes instead of loading the folder.

---

## Getting Work Out of It

The point of the layer is output, and the honest measure of whether it is working is how often it appears in real work rather than how large it has grown.

Three patterns cover most of it. **Ask against the notes, not against the world** — "based on what is in `areas/property/`, what do I still owe on the renovation and what did I decide about the roof?" — where the value is that the answer is grounded in your record rather than in general knowledge. **Draft from the notes** — a document, a message, a position paper assembled from material you already distilled, which is the case where the up-front distillation pays for itself most visibly. **Resurface deliberately**: ask Claude what in `resources/` bears on the thing you are currently working on. Old notes do not resurface by themselves, and the graph view that promises serendipity mostly delivers a pretty picture.

The habit worth building is the return leg. When a session produces a conclusion you will want again, it goes back into the layer as a note before the session ends. A second brain that only ever receives clippings and never receives your own conclusions is missing its best material.

---

## The Weekly Review

Thirty minutes, fixed slot, and it is the difference between a system and a pile. Most of it can be handed to Claude; the judgment calls cannot.

Claude does the mechanical pass: list what is in `inbox/`, flag notes in `projects/` whose project looks finished, find notes not touched in a year, find pairs of notes that appear to cover the same thing, find claims that contradict each other, and list any note whose `review:` date has passed. Ask for it as a report, not as edits.

> "Weekly review of second-brain/. Report only, no changes. 1) Everything in inbox/ with its `why` line. 2) Notes in projects/ that look complete or abandoned. 3) Notes untouched for 12+ months in areas/ and resources/. 4) Probable duplicates or overlapping pairs. 5) Direct contradictions between notes. 6) Anything past its review date. Rank sections 3–5 by how much damage a wrong answer from them would do."

You do the deciding: empty the inbox, archive what is finished, resolve contradictions (which means editing the wrong note, not keeping both), and delete. **Pruning is not optional and it is not tidiness.** An outdated note is worse than a missing one, because Claude will use it, and it will read as authoritative because you wrote it. The single most valuable habit in the whole system is editing or deleting the note that has quietly become wrong.

Guide 15's lint pass is the same instinct applied to a curated domain wiki, and if you run both layers you can run the two passes together.

---

## Which Layer Does This Belong To?

| It is... | Home | Guide |
|---|---|---|
| A fact Claude needs in order to behave correctly (your role, your preferences, a standing constraint) | Memory / profile | [04](./04_MEMORY_AND_PROFILE.md) |
| Synthesised knowledge about one subject, deliberately curated, where sources enrich existing pages | Domain wiki | [15](./15_LLM_WIKI.md) |
| A note about your work, your decisions, or something you read | Second brain | this guide |
| Structured data with values that change (holdings, transactions, measurements) | Data layer, behind a feeder script | [14](./14_PERSONAL_DATA_LAYER.md) |
| A working file belonging to one active piece of work | That project's folder | [24](./24_PROJECT_FOLDER_STRUCTURE.md) |
| Material that arrived outside a chat and belongs to one project, not yet filed | That project's `incoming/`, briefly | [24](./24_PROJECT_FOLDER_STRUCTURE.md) |
| Knowledge several projects consume and none owns | Its own project | [23](./23_MULTI_PROJECT_SETUPS.md) |

The two boundaries that get violated most: putting facts about yourself into the notes layer, where nothing reads them at the moment they are needed, and letting the second brain accumulate structured data as prose, where it goes stale invisibly and cannot be computed with.

---

## Anti-Patterns

**A perpetually full inbox.** The defining failure. Fix the capture filter, not the review cadence.

**Capturing what a source system already holds.** A copy of a document that remains searchable where it lives is a maintenance liability with no upside. Save the link and your reading of it.

**Elaborate tag taxonomies.** Discipline spent on every note to buy something grep already does. Keep status and lifecycle tags; drop topical ones.

**Notes in an app Claude cannot read.** The most consequential structural mistake, and the most expensive to reverse once you have a thousand notes. Markdown on disk.

**Append-only.** A layer that never deletes converges on an archive whose average note is wrong. Prune weekly and resolve contradictions by editing, not by keeping both versions.

**Organising instead of using.** Restructuring folders feels productive and generates no output. If the layer has not fed into a real deliverable in a month, the problem is not the structure.

**Merging the second brain and the domain wiki.** Guide 15's pattern depends on curation and a schema; this layer depends on triage and tolerating mess. Run both if you need both, in separate roots.

**Second brain as to-do list.** Tasks that live in notes are neither done nor useful. Route them out during triage.

---

## Checklist

Setting the layer up:

- [ ] Plain markdown in a folder Claude can mount — not an app database
- [ ] Four homes plus `inbox/`, sorted by when a note stops being relevant
- [ ] `index.md` under a hundred lines, read first in any session against the notes
- [ ] Capture template with `captured`, `source`, and `why`
- [ ] A fixed weekly slot for review, in the calendar

Keeping it alive:

- [ ] Inbox emptied every week, deletion the most common outcome
- [ ] Distilled notes state a conclusion and what would change it, not a summary of the source
- [ ] One idea per note; split at the point you would add a heading
- [ ] Links only where reading one note without the other gives a wrong answer
- [ ] `superseded_by:` set whenever a note replaces an earlier one
- [ ] Contradictions resolved by editing the wrong note, never by keeping both
- [ ] Conclusions from real sessions written back into the layer before the session ends
- [ ] Finished projects archived as whole folders
- [ ] If nothing from the layer has reached a deliverable in a month, ask whether it should exist
