---
name: template-exporter
description: Use this skill whenever the user wants to create a reusable template from an existing Claude artifact or setup — including chat system prompts, Cowork tasks, Cowork projects, or skills. Trigger when the user says things like "turn this into a template", "create a template I can share", "make this reusable", "export this as a template", "I want to share this setup with someone", or "create a template for [task/project/skill/chat]". Also trigger when a conversation contains a full Cowork task, project, or skill definition and the user seems to want to preserve or share it. Always use this skill — even if the user just says "template" — when the context involves chat prompts, Cowork configurations, or skill definitions.
---

# Template Exporter

Turns an existing Claude setup (chat system prompt, Cowork task, Cowork project, or skill) into a clean, shareable template — stripped of personal/business/identifying content, with placeholder annotations and dual-audience instructions (human guide + Claude setup prompt).

---

## Step 1: Determine the Template Type

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

Identify which type to export. Use context first; ask only if ambiguous.

| Type | Signals |
|------|---------|
| **Chat system prompt** | User shares a system prompt, persona, or instruction block for a Claude chat |
| **Cowork task** | User shares a task definition, step list, or automation workflow from Cowork |
| **Cowork project** | User shares a project config, folder structure, or multi-task Cowork setup |
| **Skill** | User shares a SKILL.md or skill folder |

If ambiguous, use `AskUserQuestion` with buttons:
> Buttons: `Chat system prompt` / `Cowork task` / `Cowork project` / `Skill`

If multiple types apply, ask the user to confirm or export one per type using `AskUserQuestion`.

---

## Step 2: Extract and Sanitize

**If the source material is already in the conversation, begin sanitizing immediately — do not ask the user to re-share it.**

Apply these sanitization rules — **all are mandatory**:

- **Personal identifiers**: names, usernames, email addresses, phone numbers → replace with `[PLACEHOLDER: e.g. "Your Name"]`
- **Business identifiers**: company names, product names, internal system names, project codenames → replace with `[PLACEHOLDER: e.g. "Company Name"]`
- **Credentials and secrets**: API keys, passwords, tokens, URLs with auth → replace with `[PLACEHOLDER: API key / URL]`
- **Specific dates and deadlines**: replace with `[PLACEHOLDER: e.g. "YYYY-MM-DD"]`
- **Data and metrics**: specific numbers, KPIs, budgets → replace with `[PLACEHOLDER: e.g. "Target metric value"]`
- **File paths**: absolute paths referencing real directories → replace with `[PLACEHOLDER: e.g. "/your/path/here"]`
- **Locale-specific content**: if tightly tied to a region/language, note it as `[PLACEHOLDER: localize for your context]`

Preserve the **structure, logic, and intent** of the original. Do not simplify or restructure unless something is non-portable by nature.

**Edge cases:**

| Situation | Action |
|-----------|--------|
| Source already partially sanitized | Note which placeholders were pre-existing; preserve them as-is |
| Source is already a template | Export as-is; flag to user that sanitization may be minimal |
| Source is very large (>400 lines) | Use `AskUserQuestion`: `Split into multi-file template` / `Export as single file` |

---

## Step 3: Add Sample Content

Where placeholders appear, add a brief inline annotation explaining what belongs there. Format:

```
[PLACEHOLDER: short description — EXAMPLE: "Acme Corp"]
```

Samples must be **fictional and generic** — do not derive them from the original content.

Good sample vocabulary to draw from:
- Companies: Acme Corp, Northstar Inc, Riverstone Labs, Skyline Co
- People: Alex, Jordan, Sam, Morgan
- Projects: Project Phoenix, Initiative Delta, Campaign Aurora
- Dates: 2025-Q3, 2026-01-15
- Metrics: 85%, €50,000, 1,200 units

**Placeholder format — when to use each:**

- `[PLACEHOLDER: ...]` — use in any file the **human will read and edit**: the exported template itself, README.md
- `<<<PLACEHOLDER: ... >>>` — use only inside **SETUP.md**, where Claude needs to collect values interactively

> For templates larger than ~300 lines: break SETUP.md into two steps — collect all placeholder values first, then apply them to the template file passed as an attachment. Do not embed very large templates inline.

---

## Step 4: Structure the Output

See `references/output-formats.md` for the exact file structure per template type. The general pattern is:

```
template-[name]/
├── README.md              ← Human guide
├── SETUP.md               ← Claude setup prompt
└── [type-specific files]  ← The actual template content
```

Type-specific content files:
- **Chat system prompt** → `system-prompt.md`
- **Cowork task** → `task.md`
- **Cowork project** → `project.md` + `tasks/` subfolder with one file per task
- **Skill** → `SKILL.md` + any reference files, preserving the original folder structure

Read `references/output-formats.md` for detailed specs on each type before writing files.

---

## Step 5: Write the Human Guide (README.md)

The README is for a person who receives the template and wants to use it.

Structure:
1. **What this is** — one sentence describing the template's purpose
2. **What you'll need** — prerequisites (e.g. Cowork access, a Claude Pro account)
3. **How to customize** — list every `[PLACEHOLDER: ...]` and what to fill in
4. **How to use it** — step-by-step instructions to deploy (install in Claude.ai, paste into Cowork, etc.)
5. **Notes** — any caveats, optional elements, or versioning info

Keep it plain Markdown. Write for a non-technical reader unless the source content signals otherwise.

---

## Step 6: Write the Claude Setup Prompt (SETUP.md)

The SETUP.md is a prompt that a user can give to Claude to have it automatically instantiate the template.

Structure:
```markdown
# Setup Prompt

Paste this prompt into a Claude conversation to set up [template name] automatically.

---

You are being given a template to set up. Follow these steps:

1. Read the template files provided.
2. For each <<<PLACEHOLDER: ...>>> you encounter, ask the user for the value.
   Collect all values before proceeding.
3. Substitute all placeholders with the provided values.
4. Output the completed [type] ready to use.

[Include the template content inline below this prompt, with <<<PLACEHOLDER>>> markers.
For templates >300 lines, instruct the user to attach the template file instead.]
```

---

## Step 7: Deliver the Output

**In Cowork:** Create the ZIP and use `present_files` to deliver it.
**In Claude Code:** Write all files to disk under the current working directory, then report the full output path to the user.

ZIP command (adjust for your environment):
```bash
zip -r template-[name].zip template-[name]/
```

Verify the archive is intact before delivering:
```bash
unzip -l template-[name].zip
```

---

## Quality Checklist

Before delivering, verify:
- [ ] No real names, companies, or identifiers remain (scan for email patterns, @-mentions, company names identified in Step 2)
- [ ] Every placeholder has a clear label and example value
- [ ] README covers all placeholders in the "How to customize" section
- [ ] SETUP.md uses `<<<PLACEHOLDER>>>` markers; exported template files use `[PLACEHOLDER: ...]`
- [ ] `unzip -l template-[name].zip` shows all expected files
- [ ] Structure and logic of original is fully preserved
