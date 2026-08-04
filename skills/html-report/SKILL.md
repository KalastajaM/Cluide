---
name: html-report
description: >
  Generates polished, self-contained HTML reports, briefings, and dashboards from task or
  skill output. Trigger this skill whenever the user wants output as an HTML file or styled
  report — phrases like "make this an HTML report", "generate a dashboard", "style my briefing",
  "turn this summary into something I can open in a browser", or when a task's output format
  calls for status colours, summary metrics, or a shareable standalone page. Also trigger when
  converting an existing Markdown report or run log into HTML. Do NOT trigger for Markdown-only
  output, web app development, or emails.
---

# HTML Report Generator

Produce a single self-contained `.html` file: all CSS embedded, no external stylesheets, no CDN links, no JavaScript frameworks. The file must open correctly offline, from an email attachment, or from any folder.

## Core Responsibilities

- Turn structured data (task output, run logs, summaries, tables) into a clean HTML report
- Reuse the bundled skeleton — never redesign the layout from scratch
- Keep reports readable at a glance: summary metrics first, details in cards below
- Stay dependency-free and self-contained

## Workflow

1. **Get the content.** If the data is already in the conversation, use it. Otherwise ask for the source file(s) and read them.
2. **Load the skeleton.** Read `references/report-skeleton.html`. This is the layout: container, header with title and generated-date, summary card with a metrics grid, detail cards with tables and status badges.
3. **Map the content into the skeleton:**
   - Title and `<title>` → the report name
   - `{{DATE}}` → actual generation date
   - Summary card → 2–4 headline metrics (counts, totals, statuses)
   - One card per logical section; tables for row data; badges (`badge-green` / `badge-amber` / `badge-red`) for any status field
   - Add or remove cards as the content requires — keep the CSS untouched
4. **Write the file.** Single Write call. Default name: `[subject]-report-YYYY-MM-DD.html` next to the source data, unless the user specifies a path.
5. **Confirm.** State the file path and a one-line summary of the sections included.

## Format Rules

- Semantic HTML: `<section>`, `<header>`, `<table>` — no `<br><br>` spacing, no inline styles where a class exists
- Colours only via the CSS variables in the skeleton (`--accent`, `--success`, `--warning`, `--danger`)
- One format per file: no Markdown syntax inside the HTML
- Long reports (5+ sections): add a short linked table of contents after the header

## Recurring Reports

If the same report will be generated repeatedly by a scheduled task (only the data changes, not the layout), recommend once: "Store the skeleton in the task's `TASK_REFERENCE.md` and have the task fill in values — or script the generation entirely (Guide 06)." Do not repeat the recommendation every run.

## Edge Cases

- **Source is Markdown:** convert structure faithfully — `##` → card headings, tables → `<table>`, blockquotes → a highlighted note inside the relevant card.
- **No obvious metrics:** skip the metrics grid; start with a one-paragraph summary card instead.
- **User wants different colours/branding:** change only the `:root` CSS variables; keep the layout.
- **Very short content (a few lines):** say HTML is overkill and offer plain Markdown instead — only proceed if the user confirms.
- **User asks for charts:** simple bar comparisons can be done with styled `<div>` widths; for anything more, note that this skill produces static reports and ask before adding inline SVG.

## Example

> User: "Turn today's run summary into an HTML report."
>
> Output: `digest-report-2026-06-13.html` — header "Email Digest — Daily Report", summary card (42 processed / 3 actions / 0 errors), a card with the actions table (amber badges for pending), and a card with notes. All styles embedded; opens anywhere.
