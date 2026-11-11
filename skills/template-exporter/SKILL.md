---
name: template-exporter
description: >
  Use this skill whenever the user wants to turn an existing AI-assistant setup into a reusable,
  shareable template: a chat system prompt or custom instructions, a scheduled or automated task,
  a multi-task project, or a skill, from Claude, ChatGPT/Codex or Gemini. Trigger on "turn this
  into a template", "create a template I can share", "make this reusable", "export this as a
  template", "I want to share this setup with someone", or "create a template for
  [task/project/skill/chat]", and when a conversation holds a full task, project or skill
  definition the user seems to want to preserve or share. Do NOT use it for the word "template"
  alone: a Word or PowerPoint template (.dotx, .potx) belongs to the docx/pptx skills, and a
  scaffold or starter kit built from scratch is not an export. The object here is an existing
  setup being made shareable.
---

# Template Exporter

Turns an existing assistant setup (chat system prompt, assistant task, assistant project, or skill) into a clean, shareable template — stripped of personal, business and identifying content, with annotated placeholders and two audiences served: a human guide (`README.md`) and a setup prompt any assistant can run (`SETUP.md`).

**This folder is self-contained.** Everything the skill needs is here: this file, `references/output-formats.md` (file layout per template type) and `scripts/check_template.py` (leak scan and packaging, Python 3 standard library only). It reads no other repository, guide or mounted folder, so the folder can be copied, zipped and installed on its own.

---

## Step 0: Identify Source and Target Platforms

Before touching content, establish two things from context (ask only if unclear):

- **Source platform** — where the setup runs today: Claude (chat projects, Cowork, Claude Code), ChatGPT or Codex, Gemini (app, Antigravity), or the API.
- **Target platforms** — where the recipient will use it. Default to the source platform only. Add others only when the user asks; a template that claims to work everywhere but was written for one platform fails silently on the others.

Platform-native pieces must stay labelled with the platform they belong to: a Claude Code hook, a `CLAUDE.md` file, Codex `agents/openai.yaml` metadata, an Antigravity `hooks.json`. Do not translate one platform's mechanism into another's by analogy; where a target has no documented counterpart, say so in the README as a gap.

Install routes change often. Use `references/output-formats.md` § Platform install routes as a starting point, and check the platform's current documentation before writing install steps when you can. Never state that an app-side setting (a project instructions field, a scheduled task registration) has been applied: the template can only describe it.

---

## Step 1: Determine the Template Type

> **Clarifying questions:** for any step with a fixed set of options, use the session's multiple-choice question tool when it has one; otherwise ask one concise question in chat.

Identify which type to export. Use context first; ask only if ambiguous.

| Type | Signals |
|------|---------|
| **Chat system prompt** | A system prompt, persona, custom instructions, or instruction block for a chat |
| **Assistant task** | A single task definition, step list, or automation workflow, scheduled or on demand |
| **Assistant project** | A project with instructions plus several tasks, shared context files or a folder structure |
| **Skill** | A `SKILL.md` file or a skill folder |

If ambiguous, offer: `Chat system prompt` / `Assistant task` / `Assistant project` / `Skill`. If several apply, ask whether to export one combined template or one per type.

---

## Step 2: Build the Identifier List, Then Sanitize

**If the source material is already in the conversation, start immediately — do not ask the user to re-share it.**

### 2a. Identifier list

Before editing, write down every identifying string you can find or that the user gives you: the author's name and usernames, email domains, employer and client names, product and system names, project codenames, people's names, street or city names tied to the author. Ask the user once: "Anything else that identifies you or your organisation that I should scrub?" Save the list as `identifiers.txt` **next to** the template folder, never inside it — it is a list of exactly what must not ship. Step 7 scans against it.

### 2b. Leave runtime state behind

A template is a definition, not a snapshot. Do not copy: run logs and outputs (`RUN_LOG.md`, `IMPROVEMENTS.md`, `*.log`), memory files and memory exports, session history, `.env` files, local settings (`settings.local.json` and similar), connector or OAuth grants, scheduler registration IDs, `.git/` folders, OS clutter (`.DS_Store`, `Thumbs.db`). An **empty** state file that the setup needs in order to start (a blank tracker with headers only) may be included as a starting definition; the checker accepts such a file (at MEDIUM) when it holds no real dates or run counters.

### 2c. Sanitization rules — all mandatory

Replace each item with a placeholder in the one format this skill uses everywhere (see Step 3):

- **Personal identifiers** — names, usernames, email addresses, phone numbers.
- **Business identifiers** — company, client, product and internal system names, project codenames.
- **Credentials and secrets** — API keys, passwords, tokens, URLs carrying credentials. Report each one to the user **by location, never by value**.
- **Specific dates and deadlines.**
- **Data and metrics** — real numbers, KPIs, budgets, account figures.
- **File paths** — absolute paths (`/Users/…`, `/home/…`, `C:\Users\…`) and references to sibling projects or mounted folders the recipient will not have.
- **Locale-specific content** — when tightly tied to one region or language, mark it as something to localise.

Preserve the **structure, logic and intent** of the original. Do not simplify or restructure unless something is non-portable by nature, and then say what you changed and why.

---

## Step 3: Placeholders and Sample Content

Use one placeholder format in **every** file, including `SETUP.md`:

```
[PLACEHOLDER: short description — EXAMPLE: "Acme Corp"]
```

Reuse the identical description text for the same value everywhere it appears, so the recipient (and `SETUP.md`) fills it once. Samples must be **fictional and generic** — never derived from the original content.

Sample vocabulary:
- Companies: Acme Corp, Northstar Inc, Riverstone Labs, Skyline Co
- People: Alex, Jordan, Sam, Morgan
- Projects: Project Phoenix, Initiative Delta, Campaign Aurora
- Dates: 2030-Q3, 2030-01-15
- Metrics: 85%, €50,000, 1,200 units
- Emails and domains: `alex@example.com` (the `example.com`/`.org`/`.net` domains are reserved for documentation)
- Paths: `/path/to/your/project`

---

## Step 4: Structure the Output

Read `references/output-formats.md` before writing files: it gives the exact layout per type and the per-platform install wording. The general pattern:

```
template-[name]/
├── README.md              ← Human guide
├── SETUP.md               ← Setup prompt for an assistant
└── [type-specific files]  ← The template content itself
```

---

## Step 5: Write the Human Guide (README.md)

For a person who receives the template and wants to use it:

1. **What this is** — one sentence on the template's purpose.
2. **Platforms** — which platforms it was built and tested on, which are documented-only, and any known gaps.
3. **What you'll need** — accounts, plans, tools, MCP servers or connectors, browser extensions, other skills. For each dependency say how to tell it is connected.
4. **How to customise** — a table of every distinct placeholder: description, example, where it appears.
5. **How to use it** — step-by-step install for each target platform, plus a manual route (paste the files as sources) where native installation is unavailable.
6. **Notes** — caveats, optional parts, what was deliberately left out (runtime state, credentials), version or source date.

Plain Markdown. Write for a non-technical reader unless the source signals otherwise.

---

## Step 6: Write the Setup Prompt (SETUP.md)

`SETUP.md` is a prompt the recipient gives to their assistant to fill in the template interactively. Structure:

```markdown
# Setup Prompt

Paste everything below the line into a new chat with your assistant (Claude, ChatGPT or Gemini)
to set up [template name]. [If the template is large: attach the files of this template folder
to the same message.]

**Before you start:** [list required tools, connectors or skills, and how to check each is connected —
or "No special tools needed."]

---

You are helping me set up a template. Follow these steps:

1. Read the template content below [and the attached files].
2. Find every marker that starts with "[PLACEHOLDER:" (a description, then an EXAMPLE, then "]").
   Markers with the same description are one value. List them, then ask me for the values — several at a time is
   fine. Offer the example when I am unsure.
3. Do not proceed until every value is collected. Do not invent values.
4. Return each completed file in full, under its file name, with every marker replaced.
5. Then repeat the install steps from README.md for my platform. You cannot apply app settings
   or register scheduled tasks yourself unless you have a tool for it; say which steps I must do.

[Template content inline here. For templates over ~300 lines, omit it and rely on attachments.]
```

Do not use any other marker style; one format is what lets step 2 of the prompt find every value.

---

## Step 7: Check and Package

Run the bundled checker from this skill's folder:

```bash
python3 <this-skill-folder>/scripts/check_template.py template-[name] --identifiers identifiers.txt --zip
```

It scans every file for likely secrets (reported by location only), email addresses outside reserved example domains, personal absolute paths, the strings in `identifiers.txt`, runtime-state files from Step 2b, placeholders missing an example, placeholders the README does not mention, and leftover `<<<…>>>` markers. It exits non-zero on any HIGH finding. With `--zip` and no HIGH findings it writes `template-[name].zip` beside the folder and verifies the archive.

Fix every HIGH finding and rerun. Review each MEDIUM finding and either fix it or tell the user why it stays.

**If Python is unavailable**, do the same by hand: `grep -rniE` over the folder for each identifier, for `@`, `/Users/`, `/home/`, `C:\\Users`, `sk-`, `ghp_`, `xox`, `AKIA`, `AIza` and `PRIVATE KEY`; then `zip -r template-[name].zip template-[name]/` and `unzip -l template-[name].zip`.

---

## Step 8: Deliver

- **Chat or cloud-session surfaces:** send the ZIP with the session's file-delivery tool (whatever tool the session offers for giving the user a file).
- **Local CLI (Claude Code, Codex CLI, Antigravity):** write the folder and ZIP under the current working directory and report the full path.

Never ship or send `identifiers.txt`. Tell the user it exists beside the folder and can be deleted.

---

## Quality Checklist

Before delivering, verify:
- [ ] `check_template.py` reports no HIGH findings (or the manual grep is clean)
- [ ] Every placeholder uses the single format and has an example
- [ ] README's customise table covers every distinct placeholder
- [ ] README names tested versus documented-only platforms, and every dependency
- [ ] No runtime state, credentials or memory content in the folder
- [ ] Platform-native files are labelled with their platform
- [ ] `unzip -l` shows all expected files and nothing else
- [ ] Structure and logic of the original are preserved

## Edge Cases

**The source contains a secret, a token or a credential.** Stop and say so by location, never by value.
A template is made to be shared, so a credential that survives export is published, not merely copied.
Replace it with a labelled placeholder and note in the README that the recipient supplies their own.
If it was a live credential, tell the user it is now in this conversation and suggest rotating it.

**The source points at files or projects the recipient will not have.** Absolute paths, sibling-project
references and mounted-folder assumptions all break silently on the other machine. Convert each one to
a placeholder with an example value, and list them in the README's customisation table. A pointer
that resolves only for the author is worse than no pointer, because it reads as working.

**The source depends on an MCP server, a connector, a browser extension or another skill.** The
structure exports cleanly and then does nothing. State the dependency in `SETUP.md` as a precondition,
with what to install and how to tell it is connected, rather than leaving the recipient to discover it
at the first failure. Do not bundle another author's skill unless its licence allows it; name it instead.

**The source is already partly sanitized or is already a template.** Keep pre-existing placeholders,
converting them to the single format, and tell the user which were already there. If nothing needed
sanitizing, say so rather than implying a scrub happened.

**The source is very large (over ~400 lines).** Ask: `Split into multi-file template` /
`Export as single file`. Either way, `SETUP.md` relies on attachments rather than inline content.

**The source mixes platforms** (for example a shared `AGENTS.md` with a `CLAUDE.md` adapter, or one
skill folder with Claude and Codex metadata). Keep every platform's files, keep relative imports
working, and keep the shared file carrying its own text. Do not collapse them into one platform's format.

**There is no reusable structure to extract.** Some things are one-offs: a single conversation, a
one-time analysis, a document with no pattern behind it. Say so and stop, rather than producing a
template whose only content is placeholders. Ask what the recipient is meant to *do* with it; if that
has no answer, there is no template here.

**The user wants to share something personal rather than something structural.** A finished document,
a filled-in tracker, a real dataset. That is a file to send, not a template to export. Offer the file
and say why the template path adds nothing.
