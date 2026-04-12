# Guide 19: Output Formatting — Markdown & HTML

*Last reviewed: April 2026*

> How to make generated output look good — whether Claude is producing a Markdown summary or a full HTML report.
> Covers Markdown basics with Claude-specific tips, and a practical HTML layout pattern for polished, self-contained reports.

> **Companion guides:** [Guide 02](./02_PROMPTING_BASICS.md) covers how to prompt Claude to use a specific output format. [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) explains when to script fixed-format artifact generation instead of having Claude compose it fresh each run.

> **Giving this guide to Claude:**
> "Read 19_OUTPUT_FORMATTING.md and help me format the output of my [task/skill] as [Markdown / a styled HTML report]."

---

## Why Formatting Matters

A task that produces a wall of unformatted text is a task nobody reads. A small amount of structure — clear headings, a summary table, status colours — turns output from something that requires effort to parse into something that communicates at a glance.

This guide covers two formats:
- **Markdown** — best for output read in Claude's chat UI, GitHub, or a Markdown editor
- **HTML** — best for standalone reports, dashboards, or anything that needs custom styling or status colours

---

## Part 1 — Markdown

### What Markdown Is

Markdown is a lightweight text format that renders as formatted content in most modern tools. You write plain text with simple syntax (e.g. `## Heading`, `**bold**`, `- bullet`) and the tool renders it visually. Claude uses Markdown natively in its responses.

### Where Markdown Renders (and Where It Doesn't)

Before using Markdown in task output, check whether the output will actually be rendered:

| Context | Renders? |
|---------|---------|
| Claude chat UI | ✓ Yes |
| GitHub (README, issues, PRs) | ✓ Yes |
| VS Code (preview mode) | ✓ Yes |
| Obsidian, Notion, Bear | ✓ Yes |
| Plain terminal / `cat` output | ✗ No — you see raw syntax |
| Piped to another script | ✗ No — treat as plain text |
| Plain text email | ✗ No — use plain prose or HTML |

**Rule:** if the output will be read in a rendered environment, use Markdown. If it's piped to a tool or sent as plain text, strip Markdown or avoid it entirely.

### Claude-Specific Tips

**Ask for specific elements, not just "use Markdown"**

Vague: *"Format the output as Markdown."*
Better: *"Format the output as Markdown. Start with a one-sentence summary in bold. Use `## Section` headers to separate topics. Present key metrics in a table. Use `> blockquote` for important callouts."*

The more specific you are about which elements to use, the more consistent the output will be across runs.

**Useful elements to request explicitly:**

| Element | Syntax | Good for |
|---------|--------|----------|
| Section header | `## Heading` | Separating topics |
| Bold key term | `**term**` | Drawing attention to a value |
| Table | `\| col \| col \|` | Structured comparisons, metrics |
| Blockquote callout | `> note` | Summaries, warnings, highlights |
| Task list | `- [ ] item` | Action items |
| Code block | ` ``` ` | Commands, file paths, code |
| Horizontal rule | `---` | Separating sections visually |

**Include an example in your prompt**

The single most effective way to get consistent Markdown output is to show Claude an example of what you want:

```
Format the output like this:

## Summary
[2–3 sentences]

| Metric | Value |
|--------|-------|
| [name] | [value] |

## Actions
- [ ] [action item]
```

This works because Claude pattern-matches from examples better than it follows abstract instructions.

**When to skip Markdown entirely**

- Output will be processed by a script (use JSON or plain text instead)
- Output goes into a plain text email body
- Output is very short (1–3 lines) — prose is cleaner than formatted structure
- You're generating content for a system that doesn't support Markdown rendering

---

## Part 2 — HTML

### When HTML Beats Markdown

Use HTML when:
- The output needs **status colours** (green/amber/red at a glance)
- The output is a **standalone report** someone opens in a browser
- You want **card-based layout** with multiple sections side by side
- The output is long enough that **a table of contents** would help
- You want the file to look polished without requiring a Markdown renderer

### The Self-Contained File Pattern

The most practical HTML output pattern for Claude-generated reports is a **single `.html` file with all CSS embedded**. No external stylesheets, no frameworks, no dependencies. The file works offline, can be emailed or shared as an attachment, and opens correctly anywhere.

Ask Claude to produce output in this format:

```
Generate a self-contained HTML file with embedded CSS.
No external stylesheets, no CDN links, no JavaScript frameworks.
All styles should be inside a <style> tag in the <head>.
```

### Design Hints

These patterns produce clean, readable reports without over-engineering:

**Typography**
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem;
    background: #f9f9f9;
}
```
`max-width: 720px` keeps lines readable. `-apple-system` gives native fonts on Mac/iOS with a clean Windows fallback. `line-height: 1.6` prevents the wall-of-text feel.

> **Note:** In the skeleton below, `max-width` and `margin: 0 auto` are applied to a `.container` wrapper div rather than directly to `body`. This lets the `background` on `body` fill the full viewport width. Use the skeleton's structure when you want a coloured page background.

**CSS variables for theming**
```css
:root {
    --accent: #2563eb;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
    --card-bg: #ffffff;
    --border: #e5e7eb;
}
```
Define colours once. Changing the theme means editing four lines, not hunting through the whole file.

**Card layout for sections**
```css
.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
```
Cards create visual separation between sections without heavy borders or colour backgrounds.

**Status badges**
```css
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green  { background: #dcfce7; color: #166534; }
.badge-amber  { background: #fef9c3; color: #854d0e; }
.badge-red    { background: #fee2e2; color: #991b1b; }
```
Use these for at-a-glance status on rows, cards, or metrics.

### Prompting Claude for HTML Output

A reusable prompt snippet to paste into a task or skill:

```
Generate a self-contained HTML report file with the following:
- All CSS embedded in a <style> tag — no external links
- A clean sans-serif font, max-width 720px, centred
- Section cards with a light border and padding
- A summary card at the top with key metrics in a two-column grid
- Status badges (green/amber/red) for any status fields
- A <title> and <h1> matching the report name
- Semantic HTML (use <section>, <header>, <table> where appropriate)
```

Adjust the bullet points to match your specific report structure.

### Minimal Styled HTML Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Title</title>
    <style>
        :root {
            --accent: #2563eb;
            --success: #16a34a;
            --warning: #d97706;
            --danger:  #dc2626;
            --card-bg: #ffffff;
            --border:  #e5e7eb;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #1a1a1a;
            background: #f4f4f5;
            padding: 2rem;
        }
        .container { max-width: 720px; margin: 0 auto; }
        h1 { font-size: 1.5rem; margin-bottom: 0.25rem; }
        .meta { color: #6b7280; font-size: 0.9rem; margin-bottom: 2rem; }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
        }
        .card h2 { font-size: 1rem; color: #374151; margin-bottom: 1rem; }
        .metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .metric-value { font-size: 1.5rem; font-weight: 700; }
        .metric-label { font-size: 0.8rem; color: #6b7280; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        th { text-align: left; padding: 0.5rem; background: #f9fafb; border-bottom: 1px solid var(--border); }
        td { padding: 0.5rem; border-bottom: 1px solid #f3f4f6; }
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-green  { background: #dcfce7; color: #166534; }
        .badge-amber  { background: #fef9c3; color: #854d0e; }
        .badge-red    { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
<div class="container">
    <h1>Report Title</h1>
    <p class="meta">Generated {{DATE}}</p> <!-- Replace with actual generated date -->

    <div class="card">
        <h2>Summary</h2>
        <div class="metrics">
            <div>
                <div class="metric-value">42</div>
                <div class="metric-label">Items processed</div>
            </div>
            <div>
                <div class="metric-value">3</div>
                <div class="metric-label">Actions needed</div>
            </div>
        </div>
    </div>

    <div class="card">
        <h2>Details</h2>
        <table>
            <thead>
                <tr><th>Item</th><th>Status</th><th>Notes</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>Example item</td>
                    <td><span class="badge badge-green">Done</span></td>
                    <td>No action needed</td>
                </tr>
                <tr>
                    <td>Another item</td>
                    <td><span class="badge badge-amber">Review</span></td>
                    <td>Check before Friday</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
```

Copy this skeleton into a task's `TASK_REFERENCE.md` or a skill's reference section as the output template. Claude can then populate the data fields without redesigning the layout each run.

---

## Anti-Patterns to Avoid

**Markdown in non-rendering contexts.** Output piped to a script, written to a plain text email, or printed to a terminal that doesn't render Markdown will show raw `**bold**` and `## headers`. Check where output lands before using Markdown.

**Vague format instructions.** "Use nice formatting" produces inconsistent results. Name the specific elements you want: table, badge, card, blockquote. Show an example.

**`<br>` soup HTML.** Using `<br><br>` for spacing instead of CSS `margin` or structural elements (`<section>`, `<p>`) produces fragile, unreadable markup. Use structural HTML and let CSS handle spacing.

**External CSS frameworks for one-off reports.** Pulling in Bootstrap or Tailwind via a CDN adds a network dependency, increases file weight, and requires knowing the framework's class names. For a self-contained report, 50 lines of embedded CSS does everything you need.

**Composing the HTML layout fresh every run.** If the report structure doesn't change between runs — only the data does — store the skeleton in `TASK_REFERENCE.md` and have Claude fill in values, not redesign the page. See [Guide 06 §Script fixed-format artifact generation](./06_TASK_EFFICIENCY_GUIDE.md).

**Mixing Markdown and raw HTML without a reason.** GitHub's Markdown renderer, for example, strips block-level HTML (like `<div>` or `<table>`) placed inside Markdown lists or blockquotes — the HTML appears as raw text instead of rendering. Stick to one format per output file.
