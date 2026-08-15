# Outputs

Finished deliverables — documents, decks, PDFs, exports, reports — generated *from* the project's
source files. They live here and not at the root, because they are regenerable and must never be
confused with the sources they came from.

Two consequences of that separation, worth stating in `CLAUDE.md` if they matter here:

- **Regeneration is safe in this folder and nowhere else.** Rebuilding an output overwrites a file
  here only. If a source ever ends up in this folder, that guarantee is gone.
- **Cleanup can treat this folder as one batch.** Because outputs are regenerable by construction,
  a tidy-up pass can propose archiving the contents in one go rather than asking file by file. It
  still proposes: "regenerable by construction" is a statement about where a file was put, and a
  signed PDF that came back from someone else does not become regenerable by landing here.

While there is one copy of a deliverable, give it a plain name. Once it starts going through
versioned iterations, mark the active one `_LATEST` and move older revisions to `_archive/`; use
`YYYYMMDD` in the name for point-in-time snapshots.
