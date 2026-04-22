# Task: Setup Company Policies

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-policies.md`
> **Source guide:** `21_COMPANY_POLICIES.md` (see also `03_SKILLS.md`, `05_MCP_SERVERS.md`)

## Purpose
Wire existing company policies (AI use policy, Code of Conduct, data classification, Claude guidelines, and similar) into a Claude project as runtime guardrails — without copying any policy content into the project or into Cluide. Interviews the user, classifies each policy into an enforcement tier, fills in the `policies-validator` skill, and adds the one-line reference to `CLAUDE.md`.

Runs read-only checks first. Does not move or modify policy source files.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Confirm the skill is available

Check whether the `policies-validator` skill is already installed:

```bash
ls ~/.claude/skills/policies-validator/SKILL.md 2>/dev/null && echo "installed" || echo "missing"
ls .claude/skills/policies-validator/SKILL.md 2>/dev/null && echo "installed-project" || echo "missing-project"
```

If the skill is missing in both locations, copy it from the Cluide repo (if present locally):

```bash
# User-level (applies across all projects)
mkdir -p ~/.claude/skills/policies-validator
cp path/to/Cluide/skills/policies-validator/SKILL.md ~/.claude/skills/policies-validator/SKILL.md
```

Ask the user whether they want the skill installed user-level (applies to all projects) or project-level (just this one). Default to user-level — policies are usually org-wide.

### Step 2 — Check for an existing Policy Registry

Read the installed `SKILL.md` and look at the Policy Registry table (§1). If it has real entries (non-placeholder rows), tell the user:

> "You already have N policies configured: [list names]. Do you want to add new ones, re-classify existing ones, or start fresh?"

Use `AskUserQuestion` with buttons: `Add new` / `Re-classify` / `Start fresh` / `Cancel`.

### Step 3 — Interview the user

Collect all answers before writing anything.

#### 3.1 — Which policies?
> "List the company policies you want Claude to respect. For each one, give me:
> - The name (as it appears in the source document)
> - A one-line summary of what it covers
> - Who owns it in your organisation (team or individual — for escalations)"

Collect as many as the user gives. Common examples to prompt with if they are unsure: AI use policy, Claude-specific guidelines, Code of Conduct, data / information classification, acceptable use, export control, branding / style guide.

#### 3.2 — Where does each live?

For each policy, ask:

> "Where does '[policy name]' live? Options:
> - A local file (e.g. `~/CompanyPolicies/ai-use.md`)
> - A SharePoint page or document
> - A Confluence page
> - An internal intranet URL
> - Somewhere else"

Use `AskUserQuestion` with buttons: `Local file` / `SharePoint` / `Confluence` / `Other URL` / `Skip for now`.

For **Local file**: ask for the absolute path.
For **SharePoint / Confluence**: ask for the URL or page ID.
For **Other URL**: capture the URL and note it may require manual fetching.
For **Skip for now**: record as `[TBD]` — the skill will still run but will emit a `POLICY ALERT` flagging the missing reference.

#### 3.3 — Which tier for each?

Before asking, show the tier definitions:

> **T1 — Hard block.** Violation causes legal, security, or compliance exposure. The skill will refuse to produce output and escalate. Examples: data classification, export control.
>
> **T2 — Required check.** Violation is surface-level but should be flagged. The skill drafts the response then attaches an alert or an aligned confirmation. Examples: AI use policy, Code of Conduct.
>
> **T3 — Soft guidance.** The policy shapes how Claude writes. No visible alert; the policy just influences output. Examples: style guides, preferred vendors.

For each policy, use `AskUserQuestion` with buttons: `T1 — Hard block` / `T2 — Required check` / `T3 — Soft guidance`.

#### 3.4 — Escalation contacts

> "Who should the skill point users to when a policy is unclear or an exception is needed?
> - Overall policy owner (if one person or team owns everything): [name / email]
> - AI-specific contact: [name / email] (leave blank to reuse overall)
> - Information security contact: [name / email]
> - HR / Ethics contact for Code of Conduct: [name / email]
> - Skill maintainer (usually you): [name / email]"

### Step 4 — Validate the answers

Before writing anything, run sanity checks:

**4.1 — File existence (for local-file policies):**
```bash
for file in [collected paths]; do
  ls "$file" 2>/dev/null && echo "ok: $file" || echo "MISSING: $file"
done
```

If any file is missing, ask: "[file] does not exist. Create an empty placeholder, skip, or provide a different path?"

**4.2 — MCP availability (for SharePoint / Confluence policies):**

Check whether the relevant MCP server is configured:

```bash
grep -i "confluence\|sharepoint\|atlassian" ~/.claude/settings.json 2>/dev/null
grep -i "confluence\|sharepoint\|atlassian" .claude/settings.json 2>/dev/null
```

If not found, warn the user:

> "⚠ You chose [SharePoint / Confluence] as the location for [policy name], but the corresponding MCP server doesn't appear to be configured. Options:
> - Configure the MCP server first (see Guide 05) and re-run this task
> - Fall back to a local copy of the policy
> - Proceed anyway (the skill will emit a POLICY ALERT when the policy can't be loaded)"

Use `AskUserQuestion` with buttons: `Configure MCP first` / `Use local copy` / `Proceed anyway`.

**4.3 — Tier sanity check:**

For each policy, cross-check the tier assignment against the policy name and purpose:

- If a policy name contains "classification", "export", "security", "confidential", "legal" → lean T1. Flag if user chose T3.
- If a policy name contains "conduct", "AI use", "acceptable use" → lean T2. Flag if user chose T3.
- If a policy name contains "style", "brand", "tone", "voice" → lean T3. Flag if user chose T1.

When a flag fires, ask:

> "You classified '[policy name]' as [tier]. Based on the name it looks more like [suggested tier]. Keep [tier] or switch?"

Do not override the user's choice silently.

### Step 5 — Generate

Edit the installed `SKILL.md` (either `~/.claude/skills/policies-validator/SKILL.md` or `.claude/skills/policies-validator/SKILL.md`):

**5.1 — Policy Registry (§1):** replace placeholder rows with collected entries. Use this row format:

```markdown
| 1 | Policy name | T1/T2/T3 | filepath or "MCP: [tool + arg]" | One-line purpose |
```

**5.2 — Escalation Path (§5):** fill in the contact table with collected answers. Leave rows the user did not provide as `[not specified — ask the skill maintainer]`.

**5.3 — Policy Loading Notes (§6):** for each policy in the registry, add a loading instruction:

- Local file: `Read ~/CompanyPolicies/ai-use.md` (use absolute path)
- MCP: `Use mcp__...__getConfluencePage with pageId 12345` or `Use mcp__...__sharepoint_search with query "AI Use Policy"`

Preserve the rest of the skill (tier definitions, validation protocol, output formats, edge cases) unchanged.

### Step 6 — Wire into CLAUDE.md

Check for an existing CLAUDE.md in the project and at user level:

```bash
ls .claude/CLAUDE.md 2>/dev/null && echo "project-claude-md"
ls ~/.claude/CLAUDE.md 2>/dev/null && echo "user-claude-md"
```

Ask the user where to add the policy reference. Use `AskUserQuestion` with buttons: `Project CLAUDE.md` / `User CLAUDE.md` / `Both` / `Skip`.

Append to the chosen file(s):

```markdown

## Company policies
Before responding, consult the `policies-validator` skill. T1 violations must
block; T2 issues must be surfaced; T3 guidance should shape the response.
```

If the chosen file already contains a "Company policies" section, show the existing content and ask whether to replace it or leave it.

### Step 7 — Task coupling (optional)

Ask:

> "Do any of your existing tasks depend on these policies? For example, a task that drafts external emails depends on the AI use policy. Tagging them makes the dependency visible to anyone maintaining the task later."

Use `AskUserQuestion` with buttons: `Yes — let me list them` / `No` / `Skip`.

If yes: for each task the user names, read the task file and offer to prepend:

```markdown
> **Policies applied:** [policy-name-1] (T[tier]), [policy-name-2] (T[tier])
```

immediately after the task's title block. Confirm before editing.

### Step 8 — Verify

Suggest three test prompts. Generate them based on the actual policies configured — do not hardcode.

```
Test 1 — benign:
  Ask Claude something neutral (e.g. "summarise this public article URL").
  Expected: ✅ POLICY ALIGNED (if any T2 policies exist) or no block.

Test 2 — T2 adjacent:
  Ask Claude to produce something that exercises a T2 policy.
  Example generated from your policies: [auto-generated based on T2 entries]
  Expected: ⚠️ POLICY ALERT or ✅ POLICY ALIGNED depending on content.

Test 3 — T1 violating:
  Ask Claude to do something a T1 policy prohibits.
  Example generated from your policies: [auto-generated based on T1 entries]
  Expected: 🛑 POLICY BLOCK — response halted, policy cited.
```

Ask the user to run the three prompts in a fresh session and report back whether the output matched expectations.

### Step 9 — Summary

Print:

```
Policies wired: N
  T1 (hard block):       [count]
  T2 (required check):   [count]
  T3 (soft guidance):    [count]

Installed at:  [path to SKILL.md]
CLAUDE.md updated: [path(s)]

When a policy changes:   update the source document (file or SharePoint/Confluence).
                         No change needed here.
When adding a new policy: re-run this task — it will append rather than overwrite.
When retiring a policy:  re-run this task and choose "Re-classify" to remove it.

Audit: re-run quarterly to check for broken references and stale tier assignments.
```

Point the user to:
- `tasks/setup-policies.md` for re-runs
- `21_COMPANY_POLICIES.md` for the full reference
- `skills/policies-validator/SKILL.md` (bundled) if they want to reset to the generic template

**If any policy references were left as `[TBD]` or pointed at missing files**, flag them explicitly:

> "⚠ N policies have unresolved references. The skill will emit POLICY ALERTs for these until they are fixed. Run this task again once the sources are in place."
