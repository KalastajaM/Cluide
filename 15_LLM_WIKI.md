# LLM Wiki: Building a Personal Knowledge Base

*Last reviewed: April 2026*

> Most people use LLMs for Q&A — ask a question, get an answer, lose it to chat history. The LLM wiki pattern is different: the LLM incrementally builds and maintains a persistent, structured knowledge base that gets richer with every source you add and every question you ask. Nothing is re-derived from scratch. Knowledge compounds.

> **Companion guides:** [Guide 11](./11_GIT_INTEGRATION.md) covers git — a wiki is just a folder of markdown files, and versioning it costs nothing. [Guide 14](./14_PERSONAL_DATA_LAYER.md) covers personal data — wikis and data layers are complementary, not alternatives. [Guide 04](./04_MEMORY_AND_PROFILE.md) covers `.auto-memory/` — which serves a different purpose (see below).

> **Giving this guide to Claude:**
> "Read 15_LLM_WIKI.md and help me set up an LLM wiki for [topic]. Ask me what sources I have and what I want to be able to query."
>
> **Faster alternative:** `tasks/setup-wiki.md` interviews you and creates the full wiki structure and schema without reading the guide first.

---

## The Core Idea

Standard RAG (NotebookLM, ChatGPT file uploads, most document Q&A tools) retrieves relevant chunks at query time and generates an answer from scratch. Ask something that requires synthesising five documents and the LLM has to find and piece together the fragments every time. Nothing accumulates.

The wiki pattern inverts this. When you add a new source, the LLM reads it, extracts key information, and integrates it into existing markdown pages — updating entities, revising summaries, flagging contradictions, strengthening the synthesis. Knowledge is compiled once and kept current. By the time you ask a question, the cross-references are already there. The contradictions have already been noted. The synthesis already reflects everything you've read.

The wiki is a **persistent, compounding artifact**. You rarely write it yourself — Claude writes and maintains all of it. Your job is sourcing, exploration, and asking the right questions. Claude does the summarising, cross-referencing, filing, and bookkeeping.

A useful mental model: Obsidian is the IDE; Claude is the programmer; the wiki is the codebase.

---

## Do You Need This Guide?

| If you want to... | Use |
|---|---|
| Claude to remember your preferences, corrections, and working style | `.auto-memory/` → [Guide 04](./04_MEMORY_AND_PROFILE.md) |
| Claude to remember facts about ongoing projects and contacts | `.auto-memory/` → [Guide 04](./04_MEMORY_AND_PROFILE.md) |
| Build a knowledge base about a subject domain (threat intel, research, competitors) | **LLM Wiki — this guide** |
| Have synthesised answers waiting before you ask the question | **LLM Wiki — this guide** |
| Compound knowledge across many sources over weeks or months | **LLM Wiki — this guide** |

If you're unsure: start with Guide 04. Come back here when you have a domain you want to research deeply over time.

---

## How This Differs from `.auto-memory/`

`.auto-memory/` is about **you** — your working style, your preferences, your project context. It helps Claude collaborate with you more effectively across sessions.

An LLM wiki is about **a subject domain** — a topic you're researching, a competitive landscape, a threat intelligence area, a book you're reading. It accumulates knowledge about that domain, not about you.

They complement each other: `.auto-memory/` shapes how Claude works with you; the wiki is what you're building together.

---

## Architecture

Every LLM wiki has three layers:

**Raw sources** — your curated collection of input documents. Articles, papers, PDFs, data files, images. These are immutable — Claude reads from them but never modifies them. This is your source of truth. Store them in a `sources/` folder.

**The wiki** — a directory of Claude-maintained markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. Claude owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; Claude writes it. Store it in a `wiki/` folder.

**The schema** — a `CLAUDE.md` file (or `SCHEMA.md` if you prefer to keep it separate) that tells Claude how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or running a health-check. This is the key configuration file — it's what makes Claude a disciplined wiki maintainer rather than a generic chatbot. You and Claude co-evolve this over time as you figure out what works for your domain.

A minimal directory layout:

```
my-wiki/
├── CLAUDE.md          ← schema and instructions for Claude
├── sources/           ← raw inputs, immutable
│   ├── article-1.md
│   └── report-2.pdf
├── wiki/              ← Claude-maintained pages
│   ├── index.md       ← catalog of all pages
│   ├── log.md         ← append-only history
│   ├── overview.md    ← evolving synthesis
│   └── entities/      ← one page per entity, concept, actor, etc.
│       └── ...
```

---

## The Three Operations

### Ingest

You drop a new source into `sources/` and ask Claude to process it. A typical flow:

1. Claude reads the source and discusses key takeaways with you
2. Claude writes a summary page in `wiki/`
3. Claude updates `wiki/index.md` with a new entry
4. Claude updates relevant entity and concept pages across the wiki
5. Claude appends an entry to `wiki/log.md`

A single source might touch 10–15 wiki pages. You can stay closely involved — reading summaries, checking updates, guiding emphasis — or batch-ingest with less supervision. Document the workflow you prefer in `CLAUDE.md` so it's consistent across sessions.

**Prompt to start an ingest:**
> "Read 15_LLM_WIKI.md, then ingest `sources/[filename]` into the wiki. Follow the schema in CLAUDE.md. Talk me through the key takeaways before making any changes."

### Query

You ask questions against the wiki rather than against raw sources. Claude reads `wiki/index.md` to find relevant pages, reads those pages, and synthesises an answer with citations.

The critical insight: **good answers should be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. Tell Claude to save the answer as a wiki page when the result is worth keeping.

**Prompt for a query:**
> "Search the wiki and answer: [question]. If the answer is a useful synthesis that isn't already captured, save it as a new wiki page."

### Lint

Periodically ask Claude to health-check the wiki. Look for:

- Contradictions between pages
- Stale claims that newer sources have superseded
- Orphan pages with no inbound links
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that could be filled with a web search

Claude is good at surfacing new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

**Prompt for a lint pass:**
> "Read 15_LLM_WIKI.md and run a lint pass on the wiki. Check for contradictions, orphan pages, missing cross-references, and stale claims. Give me a prioritised list of issues and suggested fixes before making any changes."

---

## Index and Log

Two files help Claude (and you) navigate the wiki as it grows.

**`wiki/index.md`** is content-oriented — a catalog of every page, each with a link, a one-line summary, and optional metadata (date added, source count). Organised by category (entities, concepts, summaries, queries, etc.). Claude updates it on every ingest. When answering a query, Claude reads the index first to find relevant pages, then drills into them. This works well at moderate scale — around 100 sources and hundreds of pages — without needing embedding-based search infrastructure.

**`wiki/log.md`** is chronological — an append-only record of what happened and when: ingests, queries, lint passes. Use a consistent prefix for each entry so the log is scannable:

```
## [2026-04-08] ingest | Threat report: APT-X Q1 2026
## [2026-04-09] query  | Comparison: APT-X vs APT-Y TTPs
## [2026-04-10] lint   | Pass 3 — 2 contradictions resolved
```

This makes the log parseable with simple tools and gives Claude a clear picture of what's been done recently when starting a new session.

---

## Writing a Schema (CLAUDE.md)

The schema is what separates a disciplined wiki from a pile of markdown files. It tells Claude:

- What page types exist and what each one contains
- How pages are named and linked
- What to do on ingest, query, and lint
- What frontmatter (if any) to add to pages
- Any domain-specific conventions

A minimal starting schema for a research wiki:

```markdown
# Wiki Schema

## Page types
- `wiki/overview.md` — evolving synthesis of everything ingested so far. Update after every ingest.
- `wiki/entities/[name].md` — one page per named entity (person, organisation, tool, concept). Create when first mentioned; update as more sources arrive.
- `wiki/sources/[slug].md` — summary of a single raw source. Create on ingest; never modify after.
- `wiki/queries/[slug].md` — saved answer to a query. Create when the answer is worth keeping.
- `wiki/index.md` — catalog. Update on every ingest or new page.
- `wiki/log.md` — append-only. Add one entry per operation.

## Naming conventions
- File names: lowercase, hyphens, no spaces. E.g. `apt-lazarus.md`, `supply-chain-attacks.md`.
- Internal links: use relative markdown links. E.g. `[Lazarus Group](../entities/apt-lazarus.md)`.

## On ingest
1. Read the source.
2. Discuss key takeaways with the user.
3. Create `wiki/sources/[slug].md`.
4. Update `wiki/overview.md`.
5. Update or create relevant entity pages.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`.

## On query
1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesise an answer with citations.
4. Ask the user if the answer should be saved as a `wiki/queries/` page.

## On lint
1. Read all pages.
2. Check for contradictions, orphans, missing links, stale claims.
3. Report issues to user before making any changes.
```

Start here and evolve it as you learn what your domain needs.

---

## Practical Applications

Some uses that fit naturally with this setup:

**Threat intelligence** — sources are advisories, CVE reports, vendor blogs, MITRE ATT&CK updates. Entity pages cover threat actors, TTPs, tooling, affected sectors. The overview tracks the evolving threat landscape. Lint catches when a TTP has been attributed to a new actor or a tool has been updated. Query saves comparison tables of actor capabilities directly back into the wiki.

**Research deep-dives** — reading papers or reports over weeks. Each paper becomes a source; entity pages cover authors, methods, datasets, findings. The synthesis tracks how the evidence is building. Useful for literature reviews or due diligence.

**Competitive analysis** — sources are product announcements, job postings, pricing pages, customer reviews. Entity pages cover competitors, features, pricing models. The overview tracks positioning. Lint flags when a competitor has shipped something that updates a claim.

**Book companion** — file each chapter as you read. Entity pages for characters, places, themes, events. By the end you have a rich cross-referenced companion. Think fan wikis built automatically as you go.

---

## Tooling Tips

**Obsidian** works well as a reader alongside Claude. Claude edits the files; you browse the results in Obsidian — following links, checking the graph view, reading updated pages. Install the **Obsidian Web Clipper** browser extension to convert web articles to markdown for your `sources/` folder quickly.

**Obsidian's graph view** shows the shape of the wiki — which pages are hubs, which are orphans. Useful for spotting gaps the lint pass might miss visually.

**Marp** is a markdown-based slide format with an Obsidian plugin. Useful if you want Claude to generate a presentation from wiki content.

**Dataview** (Obsidian plugin) runs queries over page frontmatter. If Claude adds YAML frontmatter to pages (tags, dates, source counts), Dataview can generate dynamic tables and dashboards.

**Search at scale**: at small scale the `index.md` approach is sufficient. As the wiki grows into hundreds of pages, consider [qmd](https://github.com/tobi/qmd) — a local search engine for markdown with hybrid BM25/vector search that has both a CLI (Claude can shell out to it) and an MCP server.

---

## Querying Large Wikis (100+ Pages)

The `index.md` approach works well up to roughly 100–150 pages. Beyond that, reading the full index every query becomes expensive and slow. Here's how to scale.

### Tiered Index

Add a `wiki/categories.md` file that groups pages by domain area:

```markdown
# Categories

## Threat Actors (23 pages)
See: entities/threat-actors section in index.md

## Tools & Malware (18 pages)
See: entities/tools section in index.md

## TTPs (31 pages)
See: entities/ttps section in index.md

## Source Summaries (45 pages)
See: sources/ section in index.md
```

Claude reads `categories.md` first (5–10 lines), identifies the relevant category, then reads only that slice of `index.md`. This cuts index-reading cost by 70–80% for focused queries.

### Pagination

When a query matches many pages, don't read them all. Read the top 5–10 most relevant pages (by recency or link count) and synthesise from those. If the answer feels incomplete, read the next batch. State this in the schema:

```markdown
## On query (large wiki)
1. Read `wiki/categories.md` to identify relevant categories.
2. Read the matching section of `wiki/index.md`.
3. Select the 5–10 most relevant pages (prefer recently updated, highly linked).
4. Synthesise an answer. If incomplete, read up to 5 more pages.
5. Always cite which pages were consulted.
```

### When to Switch to qmd

**Rule of thumb:** if you have 150+ entity pages or find yourself waiting noticeably for index-based queries, add qmd.

**CLI usage** (Claude can shell out to this):
```bash
qmd search "lateral movement techniques" --top 10 --path wiki/
```

**MCP server config** (add to `settings.json`):
```json
"qmd": {
  "command": "qmd",
  "args": ["serve", "--path", "/path/to/wiki"]
}
```

With the MCP server running, Claude can call `qmd_search` directly instead of reading the index. The hybrid BM25/vector search handles disambiguation and fuzzy matching that index scanning misses.

### Structured Queries with Dataview

For "list all X where Y" questions (e.g., "all threat actors targeting healthcare"), consider Dataview (Obsidian plugin) over having Claude read pages. If Claude adds YAML frontmatter to entity pages:

```yaml
---
type: threat-actor
sectors: [healthcare, finance]
first_seen: 2025-03
---
```

Then Dataview can answer structured queries instantly without Claude reading dozens of pages. Claude writes the Dataview query; Obsidian runs it.

### Anti-patterns

- **Reading all pages to answer a narrow question.** Always filter through index or categories first.
- **Reading the full index when a category filter would suffice.** Use the tiered approach.
- **Skipping citations.** At scale, knowing which 5 of 200 pages informed an answer matters more, not less.

---

## Git Integration

The wiki is just a folder of markdown files — version it with git and you get the full pre/post-run commit pattern from [Guide 11](./11_GIT_INTEGRATION.md) for free.

`wiki/log.md` is append-only, which produces an unusually clean git history: each commit adds exactly one entry, so `git log` on that file reads like a timeline of the wiki's evolution. `git diff HEAD~1 HEAD -- wiki/` shows exactly what a single ingest changed across all pages — useful for reviewing Claude's work before pushing.

Track the `wiki/` folder. Track `CLAUDE.md`. Do not track anything in `sources/` that contains sensitive data.

---

## What Good Looks Like

A mature wiki after a few months of regular use:

```
wiki/
├── index.md              ← 80 entries, organised by category
├── log.md                ← 40 entries: 30 ingests, 7 queries saved, 3 lint passes
├── overview.md           ← 5 pages, updated 12 times
├── entities/             ← 35 actor/tool/concept pages, cross-linked
├── sources/              ← 30 source summaries
└── queries/              ← 7 saved analyses and comparisons
```

The git log on `wiki/log.md` shows the exact date of every ingest, every saved query, every lint pass. You can `git diff` any two points in time and see how the synthesis evolved.

---

## Anti-Patterns

**Using the wiki as a dump of raw sources.** The wiki layer is for synthesis, not storage. If Claude copies source text verbatim into wiki pages without summarising, cross-referencing, or integrating, you have a mirror of `sources/` with extra steps. The value comes from the transformation — distill, connect, and compress.

**One massive file instead of topic pages.** A single `wiki/everything.md` defeats the purpose. Claude can't selectively read relevant pages on query; every question loads the entire wiki into context. Split by entity, concept, or source — many small pages with links between them.

**Skipping the schema.** Without a `CLAUDE.md` defining page types, naming conventions, and workflows, Claude improvises. Pages drift in structure across sessions: some have frontmatter, some don't; naming varies; the ingest workflow changes. The schema is cheap to write and prevents entropy.

**Ingesting without deduplication.** Adding the same source twice (or two versions of the same report) creates contradictions and bloat. Before ingesting, check `wiki/log.md` and `wiki/index.md` for the source. If it's already there, update rather than re-ingest. Add a dedup check to your schema's ingest workflow.

**Treating the wiki as append-only.** Wikis need pruning. Sources get superseded, entities merge, early summaries become stale as better sources arrive. The lint operation exists for this reason — run it regularly and let Claude remove or consolidate pages that no longer earn their keep.

**Confusing wiki with auto-memory.** `.auto-memory/` stores facts about you — preferences, corrections, project context. It updates implicitly during normal conversation and shapes how Claude collaborates with you. A wiki stores domain knowledge — it updates explicitly through ingest/query/lint operations and compounds research about a subject. Mixing the two (putting research into memory, or preferences into wiki pages) weakens both.

---

## Starting a New Wiki

Share this with Claude and say:

> "Read 15_LLM_WIKI.md. I want to build a wiki about [topic]. My sources will be [describe what you have]. Help me set up the directory structure and write an initial CLAUDE.md schema. Ask me questions to understand the domain before writing anything."

Claude will ask about your domain, your sources, and what you want to be able to query — then build the scaffold to match.
