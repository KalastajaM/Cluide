# Task: Setup LLM Wiki

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-wiki.md`
> **Source guide:** `12_LLM_WIKI.md`

## Purpose
Create a persistent, Claude-maintained knowledge base (LLM wiki) for a topic. Unlike chat Q&A, the wiki compiles and cross-references knowledge permanently — each new source enriches the whole structure rather than disappearing into chat history.

The wiki has three layers: raw sources (immutable), wiki pages (Claude-maintained), and a schema (CLAUDE.md that governs how Claude maintains it).

---

## Instructions

### Step 1 — Interview the user

Ask:
> 1. What topic is this wiki for? (one sentence)
> 2. What sources will you add? (articles, PDFs, research papers, web pages, data exports — describe what you have)
> 3. What do you want to be able to query? What questions should the wiki answer?
> 4. What are the key entities in this domain? (e.g. for a competitive analysis: competitors, products, features; for threat intel: threat actors, TTPs, tools)
> 5. Where should the wiki live? (provide a folder path, e.g. `~/Documents/my-wiki/` or `./wiki/`)

After collecting answers: "Thanks — I'll create the structure now."

### Step 2 — Create the directory structure

```
[wiki-root]/
├── CLAUDE.md          ← schema: how Claude maintains this wiki
├── sources/           ← raw inputs, immutable
└── wiki/
    ├── index.md       ← catalog of all pages
    ├── log.md         ← append-only history
    ├── overview.md    ← evolving synthesis
    └── entities/      ← one page per entity/concept/actor
```

Create all directories. Create placeholder files for `index.md`, `log.md`, and `overview.md`.

### Step 3 — Write the CLAUDE.md schema

Tailor the schema to the user's domain based on the interview answers. Use this structure:

```markdown
# [Topic] Wiki — Schema

## Purpose
[One sentence description from Step 1]

## Page types

- `wiki/overview.md` — evolving synthesis of everything ingested. Update after every ingest. Keep under 3 pages.
- `wiki/entities/[name].md` — one page per [entity type from interview]. Create when first mentioned; update as more sources arrive.
- `wiki/sources/[slug].md` — summary of a single raw source. Create on ingest; never modify after.
- `wiki/queries/[slug].md` — saved answer to a query. Create when the answer is worth keeping.
- `wiki/index.md` — catalog. Update on every ingest or new page.
- `wiki/log.md` — append-only. One entry per operation.

## Naming conventions
- File names: lowercase, hyphens, no spaces. E.g. `[example-entity].md`
- Internal links: use relative markdown links

## On ingest
1. Read the source.
2. Discuss key takeaways with the user.
3. Create `wiki/sources/[slug].md`.
4. Update `wiki/overview.md`.
5. Update or create relevant entity pages.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | [source title]`

## On query
1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesise an answer with citations (link to wiki pages, not raw sources).
4. Ask if the answer should be saved as a `wiki/queries/[slug].md` page.

## On lint
1. Read all pages.
2. Check for: contradictions, orphan pages (no inbound links), stale claims, missing cross-references, important concepts lacking their own page.
3. Report issues to user before making any changes.

## Source handling
- Raw sources live in `sources/` — never modify them.
- When ingesting a source already in `sources/`, check `wiki/index.md` first — it may already be processed.
```

Adapt the entity types and log prefix format to the user's domain.

### Step 4 — Initialise the index and log

Write `wiki/index.md`:
```markdown
# Wiki Index

*[N entries — updated [date]]*

## Overview
- [overview.md](./overview.md) — Evolving synthesis of all ingested sources

## Entities
*(none yet — added as sources are ingested)*

## Sources
*(none yet)*

## Queries
*(none yet)*
```

Write `wiki/log.md`:
```markdown
# Wiki Log

*Append-only. One entry per operation.*

## [YYYY-MM-DD] setup | Wiki created for [topic]
```

Write `wiki/overview.md`:
```markdown
# Overview: [Topic]

*Last updated: [date] — [N] sources ingested*

No sources ingested yet. This overview will evolve as sources are added.
```

### Step 5 — Add to .gitignore if needed

Ask:
> "Should I add `sources/` to `.gitignore`? Raw sources often contain sensitive or large files."

If yes, add `[wiki-root]/sources/` to `.gitignore`.

### Step 6 — Explain how to use it

Tell the user:

**To ingest a source:**
> "Drop a file into `sources/`, then say: 'Ingest `sources/[filename]` into the wiki. Follow the schema in CLAUDE.md. Talk me through the key takeaways before making any changes.'"

**To query the wiki:**
> "Say: 'Search the wiki and answer: [question]. If the answer is a useful synthesis, save it as a wiki page.'"

**To run a lint pass:**
> "Say: 'Run a lint pass on the wiki. Check for contradictions, orphan pages, missing cross-references, and stale claims.'"

**To evolve the schema:**
> "As you ingest sources, you'll discover domain-specific conventions that should be added to `CLAUDE.md`. Update it together with Claude as the wiki grows."

### Step 7 — Confirm

Tell the user:
- The wiki root path
- The directory structure that was created
- "The wiki is ready. Add your first source to `sources/` and ingest it to start building."
