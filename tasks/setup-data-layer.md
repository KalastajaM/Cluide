# Task: Setup Data Layer

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-data-layer.md`
> **Source guide:** `14_PERSONAL_DATA_LAYER.md`

## Purpose
Help the user connect personal data — investments, finances, transactions, or any data living in local files or web apps — to Claude tasks in a token-efficient way. Recommends the right pattern(s) for the use case and sets up the initial structure.

The core idea: Claude should read *computed summaries*, not raw data files. A Python script transforms raw data into what Claude actually needs — keeping context compact and reasoning accurate.

---

## Instructions

### Step 1 — Understand the use case

Ask:
> 1. What data do you want Claude to reason about? (e.g. investment portfolio, bank transactions, budget envelopes, project status, inventory)
> 2. Where does the data currently live? Choose all that apply:
>    - Local files (JSON, CSV, Excel)
>    - A web app with no API or export (e.g. GoodBudget, a proprietary tool)
>    - Screenshots or scanned documents
>    - Already structured but too large to paste in directly
>    - Something else — describe it
> 3. How often does the data change? (real-time / daily / weekly / rarely)
> 4. What do you want Claude to *do* with the data? (e.g. analyse trends, give advice, track changes, answer questions, update records)

Based on answers, recommend one or more patterns from the table below and explain why:

| Pattern | Best for |
|---------|---------|
| 1 — Python script feeder | Data in local files; need computed values (totals, ratios, P&L) not raw records |
| 2 — JSON database | Persistent structured store Claude can read and update; small dataset; want git history |
| 3 — Browser JS extraction | Data visible in a web app with no API; want structured JSON out without copy-paste |
| 4 — Vision ingestion | Data only accessible as screenshots or scanned documents |
| 5 — Multi-step instruction file | Workflow with 3+ distinct phases (collect → process → analyse) |

Say: "Based on what you described, I recommend [Pattern N] because [reason]. Would you like to set that up?"

### Step 2 — Set up Pattern 1: Python script feeder

*Use when: data is in local JSON/CSV files and Claude needs computed values, not raw records.*

Ask:
> - What is the raw data file? (path and format)
> - What computed values does Claude need? (e.g. P&L per position, total spend by category, days since last update)
> - What should the output look like? (table, summary paragraph, JSON — "ASCII table" is a good default)

Create the `scripts/` directory if it doesn't exist.

Write `scripts/[name]_feeder.py`:

```python
#!/usr/bin/env python3
"""
[name]_feeder.py — data feeder script
Reads [raw data file], computes [what], and prints a compact summary to stdout.
Claude reads this output as context — never the raw file directly.
"""
import json
from pathlib import Path
from datetime import date

DATA_FILE = Path("[path to raw data file]")

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def summarise(data):
    # TODO: implement computation
    # Return a list of rows or a summary string
    pass

def main():
    data = load_data()
    summary = summarise(data)
    print(f"[Data name] summary — {date.today()}")
    print("=" * 60)
    # Print summary as ASCII table or structured text
    print(summary)

if __name__ == "__main__":
    main()
```

Tell the user: "Fill in the `summarise()` function with the computation. The goal is: run this script, get ~50–80 lines of output that contain everything Claude needs and nothing it doesn't."

Add to the relevant `TASK.md` or create a new task step:
```markdown
## Step N — Load [data name]
Run: `python3 scripts/[name]_feeder.py`
Use the printed output as context. Do not read [raw file] directly.
If the script fails, log the error and stop — do not attempt to read the raw file.
```

### Step 3 — Set up Pattern 2: JSON database

*Use when: you need a persistent, structured personal data store that Claude can read and update across runs.*

Ask:
> - What entities does the database track? (e.g. portfolio positions, transactions, contacts, budget categories)
> - What are the key fields for each entity?
> - What's the natural ID for each entity? (e.g. ISIN for securities, account ID, date for time-series)

Create the `data/` directory.

For each entity type, create a starter JSON file:

```json
{
  "last_updated": "[YYYY-MM-DD]",
  "[entity_plural]": {}
}
```

Write a `data/README.md` listing each file, its purpose, and its schema. Tell the user:
- Keep master data (names, categories) separate from transactions (append-only records)
- Store raw facts (purchase price, quantity) — not computed values (P&L, averages)
- Always update `last_updated` when writing

Add `data/` to `.claudeignore` if the files contain personal data that shouldn't auto-load as context.

### Step 4 — Set up Pattern 3: Browser JS extraction

*Use when: data is visible in a web app with no API. Requires Chrome developer console.*

Ask:
> - Which web app? (URL and what page the data is on)
> - What data elements do you need? (describe what's visible on the page)
> - Where should the extracted JSON be saved?

Write `scripts/extract_[name].js`:

```javascript
// extract_[name].js
// Run in Chrome developer console on [URL]
// Output is copied to clipboard as JSON

const items = [];
// TODO: update selectors to match the actual page structure
document.querySelectorAll('[data-selector]').forEach(el => {
  items.push({
    name: el.querySelector('.name')?.textContent.trim(),
    value: el.querySelector('.value')?.textContent.trim(),
  });
});

const result = {
  extracted_at: new Date().toISOString().slice(0, 10),
  source: '[web app name]',
  items: items
};

copy(JSON.stringify(result, null, 2));
console.log(`Extracted ${items.length} items. JSON copied to clipboard.`);
```

Write `data/[name]_extraction.md` with the manual refresh procedure:

```markdown
# [Name] Data Refresh

Run when: [before analysis / weekly / when data changes]
Time: ~2 minutes

Steps:
1. Open [URL] in Chrome, navigate to [page]
2. Open console (Cmd+Option+J on Mac, F12 on Windows)
3. Paste the contents of `scripts/extract_[name].js`
4. Press Enter — JSON is copied to clipboard
5. Open `data/[name].json` and replace the contents with the clipboard

Note: update the CSS selectors in the script if the page layout changes.
```

### Step 5 — Set up Pattern 4: Vision ingestion

*Use when: data is only available as screenshots or scanned documents.*

Ask:
> - What are the screenshots of? (bank app, statements, invoices — describe the layout)
> - What fields should be extracted? (date, amount, description, etc.)
> - Where should screenshots go, and where should extracted data be saved?

Create `screenshots/` and `data/` directories.

Add `screenshots/` to `.gitignore` — screenshots are large and may contain sensitive data.

Write `scripts/extract_[name].py`:

```python
#!/usr/bin/env python3
"""
extract_[name].py — vision-based data extraction
Sends screenshots to the Claude API and extracts structured JSON.
Requires: ANTHROPIC_API_KEY environment variable
Cost: ~$0.01 per screenshot
"""
import anthropic
import base64
import json
from pathlib import Path
from datetime import date

client = anthropic.Anthropic()

SCHEMA_DESCRIPTION = (
    "Extract all [entity] from this [screenshot type]. "
    "Return a JSON array only, no other text. "
    "Each object must have: [field1] ([type]), [field2] ([type]), ..."
)

def extract(image_path: Path) -> list[dict]:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": SCHEMA_DESCRIPTION}
        ]}]
    )
    return json.loads(response.content[0].text)

screenshots = sorted(Path("screenshots").glob("*.png"))
all_items = []
for path in screenshots:
    print(f"Processing {path.name}...")
    all_items.extend(extract(path))

output = {"extracted_at": str(date.today()), "source": "vision extraction", "items": all_items}
Path("data/[name]_raw.json").write_text(json.dumps(output, indent=2))
print(f"Extracted {len(all_items)} items from {len(screenshots)} screenshots.")
```

Fill in the schema description and field names based on what the user described. Tell the user: "Update `SCHEMA_DESCRIPTION` to match exactly what fields you need — precise prompts produce consistent JSON."

### Step 6 — Set up Pattern 5: Multi-step instruction file

*Use when: the workflow has 3+ distinct phases that need different inputs, tools, or can be re-run independently.*

Ask: "How many phases does this workflow have, and what does each one do?"

Create:
```
tasks/[workflow-name]/
  TASK.md                    ← master: sequences the steps
  steps/
    01_[phase-name].md
    02_[phase-name].md
    ...
```

For each step file, use the structure:
```markdown
# Step N: [Phase Name]

## Purpose
[What this step does and why it's separate.]

## Inputs
- [Input 1: source and format]
- [Input 2]

## Command / Instructions
[Exact command or Claude instructions]

## Expected output
- [Output file created or updated]
- [Console confirmation message]

## On failure
[What to check and retry. What to skip if unrecoverable.]
```

Master `TASK.md`:
```markdown
# [Workflow Name]

## Steps
[N]. [Phase name] ([manual/script/Claude]) → steps/0N_[name].md
...

## Partial runs
To re-run from step N: [instruction]
```

### Step 7 — Confirm

Tell the user:
- Which patterns were set up and where the files are
- What still needs manual work (filling in selectors, implementing the computation function, taking the first screenshots)
- Any files added to `.gitignore` or `.claudeignore`
- "Once the scripts are working, add a step to the relevant task that runs the script and uses its output — never the raw file directly."
