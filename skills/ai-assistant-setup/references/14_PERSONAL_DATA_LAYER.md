# Connecting Claude to Your Personal Data

> Five patterns for getting personal data — investments, finances, transactions — into Claude tasks without exposing raw files, building fragile pipelines, or paying excessive token costs.

> **Companion guides:** [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) covers token efficiency — Python data feeders (Pattern 1) are one of the highest-leverage efficiency moves you can make. [Guide 07](./07_TASK_LEARNING_GUIDE.md) covers self-improvement — once your data layer is stable, the task can start learning from it. [Guide 11](./11_GIT_INTEGRATION.md) covers git tracking — your JSON data files are prime candidates for pre-run snapshots.

> **Use this when:** you want Claude to reason about personal data (portfolio performance, spending patterns, bank transactions) but the data lives in apps that have no API, in raw files too large to paste in directly, or in formats Claude can't parse without help.

> **Giving this guide to Claude:**
> "Read 14_PERSONAL_DATA_LAYER.md and help me set up a data layer for [my investment tracker / personal finance workflow / etc.]. Ask me what data sources I have and recommend which patterns apply."

---

## Do You Need This Guide Yet?

This is an advanced guide requiring Python scripts, browser JavaScript, or multi-step pipelines. Come back here when:
- You want Claude to reason about data in a web app with no API
- You have local files too large or raw to paste into Claude directly
- A task needs computed values (P&L, totals, averages) rather than raw records

If you just want Claude to remember things about you, that's [Guide 04 — Memory](./04_MEMORY_AND_PROFILE.md).

---

## The Core Problem

Claude is good at reasoning over data but not at raw data ingestion. A 500-row transactions JSON file costs thousands of tokens and gives Claude more noise than signal. A screenshot of your bank app is unreadable without a vision model in the pipeline. A live web app has no way to hand data to Claude at all.

The solution is a thin data layer that transforms raw personal data into compact, Claude-readable context:

```
Raw data source  →  [data layer]  →  Compact context  →  Claude task
(JSON / web app / screenshot)        (table / summary / structured JSON)
```

Three questions determine which pattern to use:

1. **Where does the data come from?** — local files, a web app, or images
2. **How often does it change?** — static reference data vs. daily transactions
3. **What does Claude actually need to reason over?** — computed summaries vs. raw records

---

## 1. Python Scripts as Data Feeders

**When to use this:** Data lives in local files (JSON, CSV). You need computed values — P&L, totals, ratios, averages — not raw records. The same computation runs every time Claude needs the data.

**The pattern:** Write a script that reads raw data, computes what Claude needs, and prints a compact summary to stdout. The task file tells Claude to run the script and use its output as context — never the raw file.

### Example: investment portfolio advisor

`investments.json` holds raw positions (ISIN, quantity, purchase price). A companion script reads it, computes P&L per position, and prints an ASCII table. Claude reads the table output as its context for writing an advice report.

```
Script: portfolio_advisor.py
Input:  investments.json  (positions: ISIN, quantity, buy_price, current_price)
Output: ASCII table to stdout — one row per position: ticker, qty, buy, now, P&L, P&L%
Usage:  python3 portfolio_advisor.py
```

Example output (what Claude actually reads):

```
Portfolio summary — 2026-04-06
═══════════════════════════════════════════════════════════
Ticker        Qty    Buy      Now      P&L        P&L%
───────────────────────────────────────────────────────────
MSCI World     50    92.00    98.40   +320.00     +7.0%
STOXX 600      30   110.00   118.50   +255.00     +7.7%
Tech Fund       8   250.00   297.50   +380.00    +19.0%
───────────────────────────────────────────────────────────
TOTAL                                 +955.00    +10.5%
═══════════════════════════════════════════════════════════
```

How the task file references the script:

```markdown
## Step 1: Load portfolio data
Run: `python3 scripts/portfolio_advisor.py`
Use the printed table as your context for the analysis below.
Do not read investments.json directly.
```

**Design rules:**

- Scripts own the data transformation; Claude owns the reasoning. Never mix the two.
- Output should be human-readable and Claude-readable simultaneously. ASCII tables work for both.
- Keep output under ~80 lines to stay token-efficient (see [Guide 06 §Core Principle](./06_TASK_EFFICIENCY_GUIDE.md)).
- Print a timestamp in the header so Claude knows how current the data is.
- If the script fails, Claude should log the failure and stop. It should not attempt to read the raw file directly — that would bypass all the effort to keep context compact.

---

## 2. JSON as Your Personal Database

**When to use this:** You need a persistent, structured store of personal data that both you and Claude can read and update. Your data sets are small (hundreds of records, not millions). You want git-trackable history of every change.

**Why JSON over a real database:**

- No setup, no running server, no schema migrations
- Human-readable — you can spot errors with a text editor
- Git-trackable — every change has history and is reversible (see [Guide 11](./11_GIT_INTEGRATION.md))
- Claude can read, update, and query it directly
- Works as both the input to Pattern 1 scripts and the output of Pattern 3 and 4 extraction pipelines

**5 design rules:**

1. **Flat structures over nested ones.** A list of transaction objects with flat fields is easier to query than nested account → month → transaction hierarchies. Claude reads linearly; deep nesting makes it harder to reason over.

2. **Use stable IDs as keys.** ISINs for securities, account IDs for accounts, ISO dates for time-series. Avoid sequence numbers that can shift. Stable keys make merges and updates safe.

3. **Separate master data from transactions.** Keep slowly-changing reference data (security names, account names, budget categories) in one file; append-only transaction records in another. This keeps each file focused and avoids redundancy.

4. **Store what happened, not what was computed.** Raw purchase price, quantity, and date belong in the data store. P&L does not — that is computed at query time by the script. Storing computed values creates drift when inputs change.

5. **Include a `last_updated` field at the root.** Claude and you both need to know how fresh the data is.

**Recommended file layout:**

```
data/
  securities_master.json      ← static: ISIN → name, currency, asset class
  portfolio_positions.json    ← slow-changing: current holdings per ISIN
  transactions.json           ← append-only: buy/sell/dividend records
  budget_categories.json      ← static: envelope → monthly target
  goodbudget_balances.json    ← refreshed by Pattern 3 (browser extraction)
  bank_transactions_raw.json  ← refreshed by Pattern 4 (vision ingestion)
```

Example `portfolio_positions.json` structure:

```json
{
  "last_updated": "2026-04-06",
  "positions": {
    "IE00B3RBWM25": {
      "name": "Vanguard FTSE All-World ETF",
      "currency": "USD",
      "quantity": 50,
      "avg_buy_price": 92.00
    },
    "LU0274208692": {
      "name": "X-Trackers STOXX Europe 600",
      "currency": "EUR",
      "quantity": 30,
      "avg_buy_price": 110.00
    }
  }
}
```

**Anti-pattern:** storing raw API or browser responses directly as your database. These tend to be deeply nested, have volatile keys, and contain many extraneous fields. Extract and normalize into your own schema instead.

---

## 3. Browser JavaScript Extraction

**When to use this:** The data you need is in a web application that has no API and no export feature. The data is visible in the browser. You want structured JSON out of it without manual copy-paste.

**The pattern in four steps:**

1. Open the web app in a browser and navigate to the page with the data
2. Open the developer console (Cmd+Option+J on Mac, F12 on Windows)
3. Paste the extraction script and press Enter — it copies structured JSON to your clipboard
4. Paste the clipboard contents into the appropriate data file

```
Script: extract_goodbudget.js  (run in browser console at goodbudget.com)
Target: envelope balances and account balances
Output: JSON copied to clipboard
Save to: data/goodbudget_balances.json
```

Example extraction script:

```javascript
// Run in browser console on GoodBudget accounts page
const envelopes = [];
document.querySelectorAll('.envelope-row').forEach(row => {
  envelopes.push({
    name: row.querySelector('.envelope-name')?.textContent.trim(),
    balance: parseFloat(
      row.querySelector('.balance')?.textContent.replace(/[^0-9.-]/g, '') || '0'
    )
  });
});

const result = {
  extracted_at: new Date().toISOString().slice(0, 10),
  envelopes: envelopes
};

copy(JSON.stringify(result, null, 2));
console.log(`Extracted ${envelopes.length} envelopes. JSON copied to clipboard.`);
```

What the task file says about the manual refresh step:

```markdown
## Refresh GoodBudget balances (manual, ~2 minutes)
When: before running a spending analysis, or weekly
Steps:
  1. Open goodbudget.com in Chrome, navigate to Accounts
  2. Open console (Cmd+Option+J), paste contents of scripts/extract_goodbudget.js
  3. Press Enter — JSON is copied to clipboard
  4. Open data/goodbudget_balances.json and replace the contents
  5. Run the spending analysis task as normal
```

**Practical notes:**

- Browser JS is fragile to UI changes. When the script stops working, inspect the page element and update the CSS selector — a 5-minute fix when you know what to look for.
- Always include `extracted_at` in the output so the data file is self-documenting.
- The `copy()` function works in Chrome and Edge developer consoles. In Firefox, use `console.log(JSON.stringify(result, null, 2))` and copy manually.
- This is an intentionally manual step. The value is structured, normalized data that Claude can reliably read, not zero human effort.

**When not to use this:** If the app has an official API or CSV export, use that instead. Browser JS extraction is a workaround for apps with no better option.

---

## 4. Claude Vision for Data Ingestion

**When to use this:** Data is only accessible as images — bank app screenshots, statements you photographed, scanned PDFs. Manual transcription would be tedious and error-prone. You want structured JSON out.

**The pattern:** A Python script sends screenshots to the Claude API (vision), asks Claude to return structured JSON, and saves the result to a data file. This is typically one step in a larger pipeline, not a standalone workflow.

```
Script: extract_transactions.py
Input:  screenshots/  directory of bank app screenshots (PNG/JPG)
Output: data/bank_transactions_raw.json
Usage:  python3 scripts/extract_transactions.py
Requires: ANTHROPIC_API_KEY set in environment
Cost:   ~$0.01 per screenshot
```

Core script structure:

```python
import anthropic
import base64
import json
from pathlib import Path
from datetime import date

client = anthropic.Anthropic()

def extract_from_screenshot(image_path: Path) -> list[dict]:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Extract all transactions from this bank screenshot. "
                        "Return a JSON array only, no other text. "
                        "Each object must have: date (YYYY-MM-DD), "
                        "description (string), amount (number, negative = debit), "
                        "currency (3-letter code)."
                    )
                }
            ]
        }]
    )
    return json.loads(response.content[0].text)


screenshots = sorted(Path("screenshots").glob("*.png"))
all_transactions = []
for path in screenshots:
    print(f"Processing {path.name}...")
    all_transactions.extend(extract_from_screenshot(path))

output = {
    "extracted_at": str(date.today()),
    "source": "vision extraction",
    "transactions": all_transactions
}
Path("data/bank_transactions_raw.json").write_text(
    json.dumps(output, indent=2)
)
print(f"Extracted {len(all_transactions)} transactions from {len(screenshots)} screenshots.")
```

For SDK setup and API key configuration, see the `claude-api` skill.

**Design rules:**

- The prompt must be precise about the output schema. Ask for exactly the fields you need; vague prompts produce inconsistent JSON structures.
- Include "Return a JSON array only, no other text" — otherwise Claude may wrap the result in a prose explanation.
- Name the output file `_raw` and run a separate normalization/validation step before merging into your main data store.
- Batch all screenshots from the same time period into one script run to minimize API calls.
- Add `screenshots/` to `.gitignore` — they are large and may contain sensitive financial data.

**On accuracy:** Claude Vision is generally reliable for structured data in clean bank app screenshots, but errors happen with unusual formatting or low-contrast images. Spot-check a sample of extracted transactions against the originals before merging into your data store.

---

## 5. Multi-Step Instruction Files

**When to use this:** A workflow has three or more distinct phases with different inputs, outputs, and tools. The full workflow is too complex to fit in one TASK.md without it becoming unreadable. Some steps may be optional, or need to be re-run independently.

**The pattern:** One master instruction file per workflow. One instruction file per step. Each step file is self-contained: purpose, inputs, command, expected outputs. The master file sequences them and handles branching.

**Directory layout:**

```
tasks/bank-import/
  TASK.md                          ← master: orchestrates all steps
  steps/
    01_take_screenshots.md         ← manual: capture bank app screens
    02_extract_transactions.md     ← automated: run vision extraction
    03_review_and_normalize.md     ← Claude: validate and clean raw data
    04_import_to_goodbudget.md     ← manual: browser JS import
```

Example step file (`02_extract_transactions.md`):

```markdown
# Step 2: Extract Transactions from Screenshots

## Purpose
Convert bank screenshots into structured JSON using the Claude vision API.

## Inputs
- `screenshots/` directory: PNG files captured in Step 1
- `scripts/extract_transactions.py`
- `ANTHROPIC_API_KEY` set in environment

## Command
python3 scripts/extract_transactions.py

## Expected output
- `data/bank_transactions_raw.json` created or updated
- Console: "Extracted N transactions from M screenshots."

## On failure
1. Check ANTHROPIC_API_KEY is set: `echo $ANTHROPIC_API_KEY`
2. Verify screenshots directory is not empty
3. Check PNG files open correctly (not corrupted)
Retry once. If still failing, log the error and continue Step 3
using the previous raw file if one exists.
```

Example master `TASK.md`:

```markdown
# Bank Import Workflow

## Steps
1. Take screenshots (manual) → steps/01_take_screenshots.md
2. Extract transactions (script) → steps/02_extract_transactions.md
3. Review and normalize (Claude) → steps/03_review_and_normalize.md
4. Import to GoodBudget (manual) → steps/04_import_to_goodbudget.md

## Partial runs
To re-run extraction only (e.g., screenshots changed): start at Step 2.
To re-run from normalization (extraction already done): start at Step 3.
```

**Design rules:**

- Each step file must be self-contained. Claude should be able to run step 3 without reading steps 1 and 2.
- Steps must have explicit outputs — a file created, a console message, a named dataset. No ambiguous "done" states.
- Keep the master file short. It is an index and a sequencer, not a procedure manual. Details belong in step files.
- Number steps with leading zeros (01, 02) so they sort correctly in directory listings.
- Distinguish manual from automated steps in the master file — this makes it clear where human action is required.

Cross-reference: Step files follow the same principles as TASK.md in [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md): load only what is needed, state outputs explicitly, keep each file under ~200 lines.

---

## Putting It Together

Here is how all five patterns combine in a complete personal finance data layer.

### Weekly portfolio and spending analysis

**Data collection** (runs before each analysis):

| Data source | Pattern | Output file |
|-------------|---------|-------------|
| Bank app screenshots | 4 — Vision ingestion | `bank_transactions_raw.json` |
| GoodBudget web app | 3 — Browser JS extraction | `goodbudget_balances.json` |
| `investments.json` | 2 — JSON database | (maintained continuously) |

**Analysis** (Claude reads script output, not raw files):

| Analysis | Pattern | What Claude produces |
|----------|---------|----------------------|
| `portfolio_advisor.py` | 1 — Python feeder | Advice report (HTML) |
| `spending_summary.py` | 1 — Python feeder | Monthly envelope review (Markdown) |

**Orchestration:** 4-step TASK.md + step files (Pattern 5)

**What Claude reads vs. never reads:**

```
Claude reads:    script output tables (~200 tokens each)
                 compact JSON summaries (~100 tokens)

Claude never:    raw transactions JSON (500+ rows = thousands of tokens)
reads:           GoodBudget's full page DOM
                 bank screenshot images directly
```

**The compounding benefit:** once the data layer is set up, adding a new analysis (e.g., a tax year-to-date summary) means writing one new Python script and one new task step. The data is already there in normalized JSON.

### Maintenance expectations

| Pattern | Stability | What breaks and when |
|---------|-----------|---------------------|
| Browser JS (Pattern 3) | Low | App UI changes — check monthly, fix selectors in 5 min |
| Vision extraction (Pattern 4) | High | Rarely breaks; spot-check after model updates |
| JSON schemas (Pattern 2) | High | Add fields as needed; old fields are harmless to leave |
| Python scripts (Pattern 1) | Medium | Update when the output format needs to change for a new analysis |

---

## Anti-Patterns

**Pasting raw CSV or JSON into prompts.** A 500-row bank export costs thousands of tokens and gives Claude noise, not signal. Use a Python script (Pattern 1) to compute the 50 tokens Claude actually needs.

**Feeding data without a schema.** If Claude has to guess what columns mean — is "amount" gross or net? is the date DD/MM or MM/DD? — it will guess wrong silently. Always define the schema explicitly in your extraction prompt or script header.

**Computing values in Claude instead of in scripts.** Asking Claude to compute P&L from raw prices every run wastes tokens and introduces inconsistency. Deterministic computations belong in Python, run once.

**Storing computed values in your JSON database.** P&L, averages, and category totals belong in script output, not data files. When inputs change, stored computed values drift silently. Store raw facts; compute on demand.

**Storing PII in memory files or CLAUDE.md.** Bank account numbers, national ID numbers, and full addresses do not belong in files that persist across sessions or get committed to git. Keep sensitive identifiers in local data files listed in `.gitignore`.

**Hardcoding absolute paths.** `~/Documents/Finance/data.json` breaks when you move machines or share the project. Use paths relative to the project root, or resolve them in scripts via `Path(__file__).parent`.

**Running data scripts without validating output.** A vision extraction script that returns malformed JSON will silently corrupt your data store. Add a validation step — check that required fields exist and types are correct — before writing to disk.

**Using Vision when text or API alternatives exist.** Vision extraction is slower, costlier, and less reliable than CSV export or API calls. Only use Pattern 4 when no text-based alternative exists.

**Extraction scripts without timestamps.** Any data file without `last_updated` or `extracted_at` will eventually cause confusion about freshness. Always include a date in the output.

**One giant task file for a multi-step workflow.** A 400-line TASK.md covering four phases is hard to read, hard to run partially, and expensive to load. Split it using Pattern 5.

**Automating everything at once.** Start with the manual version of browser extraction (Pattern 3). Only automate when the manual step is genuinely painful. Premature automation adds fragility without adding value.

---

## Quick Reference

| Situation | Pattern |
|-----------|---------|
| Data in local JSON/CSV, need computed values | 1 — Python script feeder |
| Need a persistent, structured personal data store | 2 — JSON as database |
| Data visible in a web app with no API | 3 — Browser JS extraction |
| Data only accessible as screenshots or images | 4 — Claude Vision ingestion |
| Workflow has 3+ distinct phases with different inputs | 5 — Multi-step instruction files |

---

> **Giving this guide to Claude:**
> "Read 14_PERSONAL_DATA_LAYER.md and help me build a data layer for [describe your use case]. Ask me what data sources I have and which patterns apply."
