# Reusable surface checks

These are acceptance fixtures, not runtime certification. Copy the template to an isolated scratch
workspace, fill placeholders with synthetic values, and keep real connectors/schedulers disabled.
For root checks use that workspace; for loading-nested start in its
`tests/behaviour/fixtures/nested/` directory. The fixture is self-contained; preserve its layout.

1. Write expected answers from AGENTS.md and CASES.md before opening the test session.
2. Start a fresh session on each selected surface. For Claude Code retain the adapter; for Codex
   open the fixture workspace at the relevant root/task folder. For Cowork use the connected
   scratch folder and bootstrap; for ChatGPT upload the scratch sources with a manifest/revision
   and paste the bootstrap. Never assume uploaded nested files auto-load.
3. Run each CASES.md prompt independently with the supplied synthetic data. For output-home
   inspect the actual file when write access exists. For text-only sessions grade the draft label.
4. Save prompt, response, tool/action evidence and each grader result under Working/behaviour-runs/.
   Record actual product/version/date/source revision. Do not call a documentation review a pass.
5. Repeat after policy, adapter, bootstrap or uploaded-source changes. Missing capabilities are
   recorded explicitly; a correct stop can pass a missing-tool case but does not verify that tool.

| Surface | Loading | Freshness | Tools | Output | Handoff/duplicates | Evidence |
|---|---|---|---|---|---|---|
| Claude Code | untested | untested | untested | untested | untested | none |
| Cowork | untested | untested | untested | untested | untested | none |
| Codex | untested | untested | untested | untested | untested | none |
| ChatGPT | untested | untested | untested | untested | untested | none |

Fixtures contain no personal data. Runtime result logs belong in ignored Working/ storage;
these source cases ship with the template. A case checks instruction following, not structural
scheduler enforcement: independently test the chosen lock/ledger implementation under races.

<!-- harvested: 2026-09-22 from a generic executive-support framework review; design review, not production validation -->
