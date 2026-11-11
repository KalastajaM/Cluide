# Task: Setup Company Policies

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Run tasks/setup-policies.md`
> **Source guide:** `21_COMPANY_POLICIES.md` (see also `03_SKILLS.md`, `05_MCP_SERVERS.md`)

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

Install the validator through the selected surface's skill route: Codex project `.agents/skills/policies-validator/SKILL.md`, Claude project/personal skill location, or an explicitly invoked task/source where native installation is unavailable. Before using the Claude commands below, select that branch; on Codex inspect/create the `.agents/skills` folder instead and validate metadata using `setup-skill.md`. For ChatGPT, supply the policy pointers and validator workflow as sources, plus an instruction to invoke it before relevant work; do not claim automatic skill loading.

Inspect actual exposed connector names/scopes rather than searching Claude settings for an OpenAI connection. Tier 1 means a verified structural block only when tool grants or runtime controls enforce it; otherwise report the enforcement gap and keep the affected action on a verified surface. Put the shared policy reference in the selected instruction target and record fresh-session checks. Never copy policy text or credentials into the distributable project.

## Purpose
Wire existing company policies (AI use policy, Code of Conduct, data classification, Claude guidelines, and similar) into a Claude project as runtime guardrails — without copying any policy content into the project or into Cluide. Interviews the user, classifies each policy into an enforcement tier, fills in the `policies-validator` skill, and adds the one-line reference to `CLAUDE.md`.

Runs read-only checks first. Does not move or modify policy source files.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Confirm the skill is available

Check whether the `policies-validator` skill is already installed. The skill is its whole folder, not `SKILL.md` alone: it links the guides bundled under its `references/`, so the check tests each of those files (keep the list in step with `skills/policies-validator/`):

```bash
# Claude-only locations; on Codex check .agents/skills/policies-validator instead
check_skill() {
  d=$1
  [ -d "$d" ] || { echo "$d: missing"; return; }
  miss=""
  for f in SKILL.md references/12_SECURITY.md references/21_COMPANY_POLICIES.md; do
    [ -f "$d/$f" ] || miss="${miss:+$miss, }$f"
  done
  if [ -z "$miss" ]; then echo "$d: installed"; else echo "$d: incomplete (missing: $miss)"; fi
}
check_skill ~/.claude/skills/policies-validator
check_skill .claude/skills/policies-validator
```

A location that reports `installed` is ready: go on to Step 2. A location that reports `incomplete` is not: reinstall the complete folder there, per the skill folder layout in Guide 03 (*The Anatomy of a Skill*). Add the missing files from the Cluide repo (if present locally) without overwriting what is already installed, because an installed `SKILL.md` may hold a Policy Registry from an earlier run:

```bash
# Claude personal-scope branch; use .claude/skills for the project-level install
src=path/to/Cluide/skills/policies-validator
dest=~/.claude/skills/policies-validator
( cd "$src" && find . -type f ) | while IFS= read -r f; do
  [ -e "$dest/$f" ] || { mkdir -p "$(dirname "$dest/$f")" && cp "$src/$f" "$dest/$f"; }
done
```

Then re-run `check_skill` and continue only once it reports `installed`.

If both locations report `missing`, copy the skill from the Cluide repo (if present locally):

```bash
# User-level (applies across all projects)
# Claude personal-scope branch only
mkdir -p ~/.claude/skills
cp -r path/to/Cluide/skills/policies-validator ~/.claude/skills/

# Project-level (this project only)
mkdir -p .claude/skills
cp -r path/to/Cluide/skills/policies-validator .claude/skills/
```

Copy the whole folder, not `SKILL.md` alone: the skill links its bundled `references/` (including the security guidance its prompt-injection rule defers to), and a `SKILL.md`-only install leaves those links dangling.

Ask the user whether they want the skill installed user-level (applies to all projects) or project-level (just this one). Default to user-level — policies are usually org-wide.

### Step 2 — Check for an existing Policy Registry

Read the installed `SKILL.md` and look at the Policy Registry table (§1). If it has real entries (non-placeholder rows), tell the user:

> "You already have N policies configured: [list names]. Do you want to add new ones, re-classify existing ones, or start fresh?"

Use the available question tool, or ask in chat: `Add new` / `Re-classify` / `Start fresh` / `Cancel`.

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

Use the available question tool, or ask in chat: `Local file` / `SharePoint` / `Confluence` / `Other URL` / `Skip for now`.

For **Local file**: ask for the absolute path.
For **SharePoint / Confluence**: ask for the URL or page ID.
For **Other URL**: capture the URL and note it may require manual fetching.
For **Skip for now**: record as `[TBD]` — the skill will still run but will emit a `POLICY ALERT` flagging the missing reference.

#### 3.3 — Which tier for each?

Before asking, show the tier definitions:

> **T1 — Stop and escalate.** Violation causes legal, security, or compliance exposure. The skill will refuse to produce output and escalate. Examples: data classification, export control. It cannot stop data the user has already pasted or uploaded — that needs a control outside the assistant (Guide 21 §1, *What a policy line cannot stop*).
>
> **T2 — Required check.** Violation is surface-level but should be flagged. The skill drafts the response then attaches an alert or an aligned confirmation. Examples: AI use policy, Code of Conduct.
>
> **T3 — Soft guidance.** The policy shapes how Claude writes. No visible alert; the policy just influences output. Examples: style guides, preferred vendors.

For each policy, use the available question tool, or ask in chat: `T1 — Stop and escalate` / `T2 — Required check` / `T3 — Soft guidance`.

For each policy classified T1, ask one follow-up: "What stops this breach before it reaches the assistant — DLP, an admin setting, an approved internal tool, training, or nothing yet?" Record the answer, or `none`, for the skill's *Upstream controls* table. If the answer is `none`, tell the user once that the skill will catch the breach only after the data has been sent, and that the gap belongs with the policy owner.

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

Check whether the relevant MCP server is configured. Do not search `settings.json` for it: `tasks/setup-mcp.md` Step 1 records that file as holding permissions, hooks and env, not `mcpServers`. Use that step's method instead:

```bash
# Claude Code: registered servers across all scopes
command -v claude >/dev/null 2>&1 && claude mcp list | grep -i "confluence\|sharepoint\|atlassian" \
  || echo "no match, or claude CLI not available — check the session's tool listing"
```

Then check the session's own tool listing — "What MCP tools do you currently have access to? List them by server." If neither shows the server, warn the user (if you could run neither check, say the configuration is unverified rather than missing):

> "⚠ You chose [SharePoint / Confluence] as the location for [policy name], but the corresponding MCP server doesn't appear to be configured. Options:
> - Configure the MCP server first (see Guide 05) and re-run this task
> - Fall back to a local copy of the policy
> - Proceed anyway (the skill will emit a POLICY ALERT when the policy can't be loaded)"

Use the available question tool, or ask in chat: `Configure MCP first` / `Use local copy` / `Proceed anyway`.

**4.3 — Tier sanity check:**

For each policy, cross-check the tier assignment against the policy name and purpose:

- If a policy name contains "classification", "export", "security", "confidential", "legal" → lean T1. Flag if user chose T3.
- If a policy name contains "conduct", "AI use", "acceptable use" → lean T2. Flag if user chose T3.
- If a policy name contains "style", "brand", "tone", "voice" → lean T3. Flag if user chose T1.

When a flag fires, ask:

> "You classified '[policy name]' as [tier]. Based on the name it looks more like [suggested tier]. Keep [tier] or switch?"

Do not override the user's choice silently.

### Step 5 — Generate

Edit the installed native skill selected above (Codex: `.agents/skills/policies-validator/SKILL.md`; Claude: either `~/.claude/skills/policies-validator/SKILL.md` or `.claude/skills/policies-validator/SKILL.md`):

**5.1 — Policy Registry (§1):** replace placeholder rows with collected entries. Use this row format:

```markdown
| 1 | Policy name | T1/T2/T3 | filepath or "MCP: [tool + arg]" | One-line purpose |
```

**5.1a — Upstream controls (§2):** fill the *Upstream controls* table with one row per T1 policy and the answer collected in Step 3.3. Write `none` where the user named nothing; do not leave it blank or invent a control.

**5.2 — Escalation Path (§5):** fill in the contact table with collected answers. Leave rows the user did not provide as `[not specified — ask the skill maintainer]`.

**5.3 — Policy Loading Notes (§6):** for each policy in the registry, add a loading instruction:

- Local file: `Read ~/CompanyPolicies/ai-use.md` (use absolute path)
- MCP: `Use mcp__...__getConfluencePage with pageId 12345` or `Use mcp__...__sharepoint_search with query "AI Use Policy"`

Preserve the rest of the skill (tier definitions, validation protocol, output formats, edge cases) unchanged.

### Step 6 — Wire into CLAUDE.md

Select the native policy target from the runtime route. The following project/user checks are Claude-only; Codex uses its effective `AGENTS.md` chain, and ChatGPT uses project instructions/source.

```bash
ls CLAUDE.md 2>/dev/null && echo "project-claude-md (root)"
ls .claude/CLAUDE.md 2>/dev/null && echo "project-claude-md (.claude/)"
ls ~/.claude/CLAUDE.md 2>/dev/null && echo "user-claude-md"
```

Ask the user where to add the policy reference. Use the available question tool, or ask in chat: `Project CLAUDE.md` / `User CLAUDE.md` / `Both` / `Skip`.

Append to the chosen file(s). If a project has a `CLAUDE.md` at the root and one under `.claude/`, append to the one that already holds the project's rules rather than creating a second:

```markdown

## Company policies
Before responding, consult the `policies-validator` skill. T1 violations must
block; T2 issues must be surfaced; T3 guidance should shape the response.
```

If the chosen file already contains a "Company policies" section, show the existing content and ask whether to replace it or leave it.

### Step 7 — Task coupling (optional)

Ask:

> "Do any of your existing tasks depend on these policies? For example, a task that drafts external emails depends on the AI use policy. Tagging them makes the dependency visible to anyone maintaining the task later."

Use the available question tool, or ask in chat: `Yes — let me list them` / `No` / `Skip`.

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
  Use mock data only — pasting real classified data is itself the breach.
  Expected: 🛑 POLICY BLOCK — response halted, policy cited, and for a
  breach in the input, a plain statement that the content was already sent.
```

Ask the user to run the three prompts in a fresh session and report back whether the output matched expectations.

### Step 9 — Summary

Print:

```
Policies wired: N
  T1 (stop and escalate): [count]  (upstream control: none for [count])
  T2 (required check):    [count]
  T3 (soft guidance):     [count]

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

## Output

- The `policies-validator` skill installed as a complete folder at the chosen location, user-level or project-level on Claude, `.agents/skills/` on Codex.
- The installed `SKILL.md` filled in: the Policy Registry (§1), the Escalation Path (§5) and the Policy Loading Notes (§6).
- A `## Company policies` reference in the chosen policy file.
- Optionally, a `Policies applied` line under the title of each task the user names.
- Three generated test prompts and the Step 9 summary of policies wired by tier, install path and files updated.

## Constraints

- Read-only checks come first; collect all interview answers before writing anything.
- Never copy policy text or credentials into the project or into Cluide; the registry holds pointers only, and policy source files are never moved or modified.
- Install the whole `policies-validator` folder; an `incomplete` install is repaired without overwriting the installed `SKILL.md`.
- Preserve the rest of the skill (tier definitions, validation protocol, output formats, edge cases) unchanged, and append to an existing registry rather than overwriting it.
- Never override the user's tier choice silently; flag a mismatch and ask. A tier 1 block counts as enforced only where tool grants or runtime controls enforce it.
- Confirm before editing a task file or replacing an existing "Company policies" section, and flag every `[TBD]` or missing reference at the end.
