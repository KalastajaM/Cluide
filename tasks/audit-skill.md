# Task: Audit Skill

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/audit-skill.md`
> **Source guides:** `03_SKILLS.md`, `02_PROMPTING_BASICS.md`

## Purpose
Review an existing skill against the Guide 03 quality checklist: reliable triggering, complete workflow, explicit output format, named tools, and edge case coverage. Returns a prioritised list of issues and applies fixes after approval.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Identify the skill to audit

Ask: "Which skill should I audit? Provide the skill name or path (e.g. `client-status-update` or `~/.claude/skills/client-status-update/SKILL.md`)."

Read the `SKILL.md`. Also check if a `references/` subfolder exists and how large `SKILL.md` is.

Report:
```
Skill: [name]
Location: [path]
Lines: N
References folder: [exists with N files / missing]
```

### Step 2 — Run the audit checklist

#### Check 1: Description quality (most important)

The description controls whether the skill triggers. Evaluate:

- [ ] Names what the skill does (not just a title)
- [ ] Lists specific trigger phrases — including casual, implicit phrasings
- [ ] Uses "trigger this skill" explicitly (helps Claude match intent)
- [ ] Covers at least 3–5 example user phrasings
- [ ] Says what to do proactively when input is ambiguous (e.g. "confirm tone unless clear")
- [ ] Not so broad it triggers for unrelated requests

Flag weak descriptions with: "A user saying '[phrase]' would not trigger this skill with the current description."

#### Check 2: Workflow completeness

- [ ] Steps are numbered and sequential
- [ ] Each step that uses an MCP tool names the exact tool (e.g. `gmail_create_draft`, not "check email")
- [ ] Each step that needs user input specifies what to ask
- [ ] Each step that can fail has a fallback or graceful skip
- [ ] No step is so vague Claude would interpret it differently each session

#### Check 3: Output format

- [ ] An explicit output format is defined
- [ ] A code block example is included showing exactly what the output should look like
- [ ] Headers, bullet style, and field names are specified — not left to Claude's discretion

#### Check 4: Constraints

- [ ] Hard limits are stated with "NEVER" (e.g. "NEVER send — always draft")
- [ ] Each prohibition has a positive counterpart (what to do instead)
- [ ] Any prohibition that maps onto a tool is **enforced** by an `allowed-tools` allowlist in the frontmatter, not left to prose

On the last point: `allowed-tools` lists the only tools the skill may use, so anything omitted is unavailable rather than discouraged. There is no deny-list field. Flag with: "This skill says NEVER [X] but has no `allowed-tools` line — a session under pressure can still do it. Add `allowed-tools: [list]` to make the constraint real." Do not flag a general-purpose skill that legitimately needs the full toolset; the finding is for skills whose own constraints describe a restriction the frontmatter doesn't implement (Guide 03 optional frontmatter, Guide 12).

#### Check 5: Edge cases

- [ ] At least 3 edge cases are named
- [ ] Each edge case has a specific handling rule (not "use your judgment")
- [ ] The most common failure modes for this skill type are covered

#### Check 6: Size and progressive disclosure

- [ ] SKILL.md is under 500 lines
- [ ] If over 500 lines: detailed reference content is moved (or should be moved) to `references/`
- [ ] `references/` files are named from SKILL.md — not silently expected

#### Check 7: Memory (if applicable)

If the skill involves recurring context (contacts, preferences, past decisions):
- [ ] Memory section is present with explicit format for what to store
- [ ] Without it: the skill re-learns the same things every session

### Step 3 — Present findings

```
Skill Audit: [name]
───────────────────
Size: N lines [✓ under 500 / ⚠ consider splitting]

Issues found (prioritised by impact):

CRITICAL (skill may not trigger reliably):
  ✗ Description: [specific problem] — "[current text]"
    Suggested: [improved version]

HIGH (inconsistent output or broken steps):
  ⚠ [Check N]: [description]

MEDIUM (edge cases, memory):
  ⚠ [Check N]: [description]

LOW / OPTIONAL:
  ℹ [Check N]: [description]

Passing:
  ✓ [Check N]: [description]

Overall: [N issues — critical/high/medium/low breakdown]
```

**Finding discipline.** For anything that rests on judgement rather than on a file being present or
absent, carry a **confidence** (high / medium / low) and a **would-drop-it-if** line naming the evidence
that would make you withdraw the finding. A finding with no answer to that question is an opinion — leave
it out rather than padding the report with it. When the user pushes back, check the finding against its
would-drop-it-if line instead of trading verdicts (`27_INDEPENDENT_JUDGMENT.md`).

**Real-world example** — what an audit finding looks like with specific, actionable detail:

```
Skill Audit: client-email-drafter
──────────────────────────────────
Size: 85 lines ✓ under 500

Issues found (prioritised by impact):

CRITICAL (skill may not trigger reliably):
  ✗ Description: Only says "Draft client emails" — no trigger phrases listed.
    Current: "Draft professional emails to clients."
    Suggested: "Draft professional emails to clients. Trigger when the user says
    'write an email to [client]', 'draft a reply to [name]', 'help me respond to
    this email', or 'client email'. Also trigger when the user pastes an email
    and asks to reply or follow up."

HIGH (inconsistent output or broken steps):
  ⚠ Check 2 (Workflow): Step 3 says "send the email" but uses no tool name.
    Fix: Replace with "Call `gmail_create_draft` with the composed email.
    NEVER call `gmail_send_email` — always draft, never send."

MEDIUM (edge cases, memory):
  ⚠ Check 5 (Edge cases): Only 1 edge case listed. Missing:
    - If the client name is ambiguous (multiple contacts with similar names)
    - If the user wants to reply to a thread vs. start a new email

Passing:
  ✓ Check 3 (Output format): Clear email template with subject, greeting, body, sign-off
  ✓ Check 4 (Constraints): "NEVER send" rule present with positive counterpart

Overall: 3 issues — 1 critical, 1 high, 1 medium
```

Ask:
> "Would you like me to apply fixes? Options:
> - (A) Rewrite the description (highest impact — do this first)
> - (B) Fix workflow steps and tool names
> - (C) Add/improve output format example
> - (D) Add edge cases
> - (E) All of the above
> - (F) Walk through each issue together"

### Step 4 — Apply fixes

**Description rewrite:** Show the old description and the proposed new version side by side. The new version should be longer and more explicit. Apply after approval.

**Workflow fixes:** For each step missing a tool name, propose the specific tool. For each step missing a fallback, propose one. Show each change and apply after approval.

**Output format:** If missing, ask: "Can you show me an example of what the ideal output looks like?" Use that to write the format block. If the user can't provide one, generate a plausible example and ask them to correct it.

**Edge cases:** Propose 3 edge cases based on the skill's domain. The user approves, rejects, or modifies each.

### Step 5 — Confirm

Tell the user:
- Issues found and fixed
- Final line count
- The trigger phrases now in the description
- "Test it: start a new Claude session and use one of the trigger phrases. If it still doesn't activate, the description needs stronger phrasing."
