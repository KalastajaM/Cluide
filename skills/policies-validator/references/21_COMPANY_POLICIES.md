# Company Policies Guide: Embedding Existing Policies as Guardrails

*Last reviewed: April 2026*

> How to make Claude honour your organisation's existing policies — AI use policy, Code of Conduct, data classification, and similar — without copying the policy content into Cluide. Policies stay where they already live; Cluide holds only the pointers and the enforcement logic.

> **Companion guides:** [Guide 03](./03_SKILLS.md) covers skill design — the `policies-validator` skill follows its conventions. [Guide 05](./05_MCP_SERVERS.md) covers MCP server setup, needed when policies live in SharePoint or Confluence. [Guide 12](./12_SECURITY.md) covers operational security; this guide covers *policy* enforcement.

> **Giving this guide to Claude:**
> "Read 21_COMPANY_POLICIES.md and help me wire up the company policies I care about."
>
> **Faster alternative:** `tasks/setup-policies.md` runs the full interview, classifies each policy, and generates the skill end-to-end without reading the guide first.

---

## 1. Why This Pattern

Most organisations already publish the policies that should shape Claude's behaviour — AI use policy, Claude-specific guidelines, Code of Conduct, data / information classification, export control, acceptable use. These are authoritative documents owned by legal, security, or HR. They change on their own schedule, have formal approval workflows, and are sometimes confidential to the organisation.

The problem: Claude does not automatically know about any of this. Without explicit wiring, a skill will happily help draft a customer email that breaches tone guidelines, a task will happily process data classified above what it should touch, and a chat session will happily cite sources the policy prohibits.

The goal of this pattern:

- Claude's output conforms to policy automatically — no human has to remember to check
- Policy *content* stays in its authoritative location (SharePoint, Confluence, or a private local folder) — Cluide contains only pointers
- The enforcement strength scales with the policy: a data classification rule blocks hard, a style-guide nudges softly
- When a policy changes, updating the source document is enough — nothing in Cluide has to change

**Why not just put the policies in `CLAUDE.md`?**

- CLAUDE.md is loaded into every session, which inflates context
- Copies drift from the authoritative source — and it is not obvious which copy is current
- Cluide is designed to be shareable. Pasting confidential policies into it defeats that
- CLAUDE.md has no enforcement mechanism — it is advisory. Policies often need a stronger surface

---

## 2. The Separation Principle

Three layers, cleanly separated:

| Layer | Contains | Lives where | Shareable? |
|---|---|---|---|
| **Cluide** | Generic framework — guides, templates, skill scaffolding | This repo | Yes |
| **Policy content** | The actual policy text (AI use, Code of Conduct, classification…) | Outside Cluide — central folder or external system | No (org-confidential) |
| **The bridge** | A skill and one CLAUDE.md line that reference the policy content by path / URL | Inside the project (`.claude/skills/`, `CLAUDE.md`) | Yes — only pointers, no policy text |

The bridge is the interesting layer. It is what lets a generic, shareable framework produce org-specific guardrails.

**Golden rule:** the Cluide repo must contain zero characters of policy text. If you can paste a file from the repo into a public forum without a compliance review, the separation is intact.

---

## 3. Where Policies Live — Two Storage Patterns

### Pattern A — Central user-level folder

A single folder on your machine, outside any git-tracked project, holds the policies in Markdown form:

```
~/CompanyPolicies/
  index.md                      # lists all policies + tier + version date
  ai-use.md
  claude-guidelines.md
  code-of-conduct.md
  data-classification.md
  acceptable-use.md
```

Every project's `policies-validator` skill references these via absolute paths.

**Pros:**
- One source of truth across all your Claude projects
- Updating a policy once is enough
- Never accidentally committed — the folder is not part of any repo
- Works offline

**Cons:**
- Machine-local — does not help colleagues without the same folder
- You are responsible for keeping it in sync with the authoritative source
- Risk of staleness if you forget to update after a policy is revised

**File hygiene:**
- Keep the folder outside any git-tracked directory (simplest)
- If it must live inside a repo for any reason, add the folder to both `.gitignore` **and** `.claudeignore` — see [Guide 11](./11_GIT_INTEGRATION.md)

**Best for:** individual users whose policies change infrequently, or air-gapped / offline work.

### Pattern B — External systems via MCP

Policies stay where they already live — SharePoint, Confluence, an internal intranet page — and the skill fetches them at runtime via MCP tools.

```
Skill → MCP tool (getConfluencePage / sharepoint_search) → live policy
```

**Pros:**
- Always the authoritative version
- Access-controlled — reading the policy requires the same permissions as normal access
- Team-wide — everyone pointing the skill at the same URLs gets the same current text
- Leaves an audit trail if the MCP server logs reads

**Cons:**
- Depends on the MCP server being configured and online
- Network round-trip on every consultation (can be mitigated by caching within a session)
- Harder to test offline

**File hygiene:** nothing to worry about — no local copies exist.

**Best for:** organisations where policies are already published in SharePoint / Confluence, where updates are frequent, or where team-wide consistency matters.

### Picking between them

| Question | Lean A (local folder) | Lean B (MCP) |
|---|---|---|
| How often do policies change? | Rarely (annually) | Often (quarterly or more) |
| Is this for you alone or a team? | Solo | Team |
| Are the authoritative docs already in SharePoint / Confluence? | No | Yes |
| Do you work offline regularly? | Yes | No |
| Do you need an audit trail of policy reads? | No | Yes |

You can mix: keep stable policies (Code of Conduct, classification scheme) locally and fetch volatile ones (current AI use guidance) via MCP.

---

## 4. Tiered Enforcement Model

Not every policy deserves the same treatment. A data classification rule should stop a mistake from happening; a style guide should shape tone. Classify each policy into one of three tiers at setup time.

| Tier | Enforcement | Typical policies | Skill behaviour |
|---|---|---|---|
| **T1 — Hard block** | Refuse the action, escalate | Data classification, export control, information security, legal constraints | Pre-action check. On violation: stop, emit `🛑 POLICY BLOCK`, point to the policy and owner. Do not produce the requested output. |
| **T2 — Required check** | Validate and surface the result | AI use policy, Claude-specific guidelines, Code of Conduct | Pre-response checklist. Emit `⚠️ POLICY ALERT` when the response drifts, or `✅ POLICY ALIGNED` when it passes. |
| **T3 — Soft guidance** | Load into context; apply judgment | Style guides, preferred vendors, tone guidelines, branding rules | Content is loaded into context; Claude applies it while drafting. No required output block. |

### Worked example — T1 (Hard block)

**Policy:** Data classification scheme says "Confidential" data must not be sent to external AI services.

**User prompt:** "Here's the customer export — summarise it for me."

**Skill behaviour:** Reads the classification policy. Detects that the pasted content contains fields flagged as Confidential. Halts before producing a summary.

**Output:**

```
🛑 POLICY BLOCK — Data Classification
The pasted content contains fields classified Confidential (customer email,
internal ID). The Data Classification Policy prohibits sending Confidential
data to this assistant.

Policy: ~/CompanyPolicies/data-classification.md §3.2
Owner:  Information Security team — infosec@example.com

What to do next: re-run with the export redacted to Public/Internal only,
or route the request through an approved internal tool.
```

### Worked example — T2 (Required check)

**Policy:** AI use policy requires that any externally-shared draft be labelled as AI-assisted and reviewed by the author.

**User prompt:** "Draft a reply to this customer email."

**Skill behaviour:** Drafts the reply. Runs the AI-use checklist. Notices the draft has no "AI-assisted" marker.

**Output:**

```
[Draft email here]

⚠️ POLICY ALERT — AI Use
Policy: ~/CompanyPolicies/ai-use.md §4 (AI-assisted content labelling)
Issue:  Draft is intended for external use but is not labelled as AI-assisted.
Fix:    Before sending, add the AI-assistance disclosure required by §4,
        and confirm you have reviewed the content.
```

Or, on a passing response:

```
[Draft email here]

✅ POLICY ALIGNED — AI use policy checks passed (labelling, review step noted).
```

### Worked example — T3 (Soft guidance)

**Policy:** Brand style guide specifies voice ("direct, not formal") and banned phrases.

**User prompt:** "Draft a blog post about our product launch."

**Skill behaviour:** Loads the style guide into context. Produces a draft that follows it.

**Output:** The blog post itself — no block, no alert. The policy shaped the output silently.

### How to pick a tier

- If a violation causes legal, security, or compliance exposure → **T1**
- If a violation is embarrassing but recoverable, or requires an author action before use → **T2**
- If the policy is about *how* rather than *whether* → **T3**

When in doubt, a policy can start at T2 and move to T1 later if experience shows violations are happening.

---

## 5. Implementation Pattern

The pattern has three integration points. All three are needed; skipping any one weakens enforcement.

### 5.1 The skill — `policies-validator`

The active component. A single skill, installed once per user (or per project), containing:

- A **Policy Registry** table with every policy, its tier, and its location
- The **Validation Protocol** — what to do before each response, tier by tier
- The **Output Formats** — the block templates for POLICY BLOCK / POLICY ALERT / POLICY ALIGNED

The structure mirrors the existing PMO Guardrails skill at `templates/PMO_TEMPLATE/PMO/Guardrails.md` — specifically the pre-response checklist pattern in sections 11 (lines 128–152) of that file. That skill has been in production use; `policies-validator` generalises it from one initiative charter to a registry of company policies.

A generic, ready-to-install version is bundled at `skills/policies-validator/SKILL.md`.

### 5.2 The CLAUDE.md line

One line in the project's `CLAUDE.md` tells Claude to consult the skill on every turn:

```markdown
## Company policies
Before responding, consult the `policies-validator` skill. T1 violations must
block; T2 issues must be surfaced; T3 guidance should shape the response.
```

Keep it short — the skill itself holds the detail.

### 5.3 Task references

For scheduled tasks, declare policy coupling at the top of the task file:

```markdown
> **Policies applied:** ai-use (T2), data-classification (T1)
```

This makes the dependency visible when someone maintains the task — they know which policies gate the task's behaviour without having to trace through the skill.

---

## 6. File Hygiene

**Policy content must never land in the Cluide repo.** The skill uses placeholder paths and MCP queries; the paths are filled in per-machine at setup time.

Checks:

- **Before committing any change to Cluide:** grep the repo for company names, internal URLs, and policy IDs. Zero matches expected.
- **If policies are stored locally inside a git-tracked folder:** add the folder to `.gitignore` and `.claudeignore`. See [Guide 11](./11_GIT_INTEGRATION.md).
- **If policies are fetched via MCP:** nothing to ignore — but confirm the MCP server's authentication flow does not log credentials into session transcripts. See [Guide 12](./12_SECURITY.md).

**The skill itself** (`skills/policies-validator/SKILL.md`) is Cluide-safe by design: it contains only `[PLACEHOLDER: ...]` markers where policy names, paths, and owners go. The filled-in version lives in `~/.claude/skills/policies-validator/SKILL.md` on each user's machine (or in `.claude/skills/` per project), not in the repo.

---

## 7. Verification

After running `tasks/setup-policies.md`, test the wiring with three prompts:

| Test | Expected outcome |
|---|---|
| Ask something benign ("What's the weather pattern called when warm air sits above cold air?") | `✅ POLICY ALIGNED` (or no block at all if you only configured T1/T3) |
| Ask something that exercises a T2 policy (e.g. "draft an external email" when the AI use policy requires labelling) | `⚠️ POLICY ALERT` with a reference to the AI use policy |
| Ask something that violates a T1 policy (e.g. paste mock data flagged Confidential) | `🛑 POLICY BLOCK` with refusal and escalation path |

A T3 policy should silently shape tone — test by asking for a draft and checking that the output follows the style guide without any visible block.

---

## 8. Maintenance

- **When a policy is revised:** update the source (the local file or the SharePoint / Confluence page). No change to Cluide. No change to the skill. The next Claude turn sees the new text.
- **When a new policy is introduced:** re-run `tasks/setup-policies.md`. It will pick up the existing registry, ask about the new policy, and append it.
- **When a policy is retired:** remove its row from the Policy Registry in the skill. Leaving stale entries causes broken-link behaviour and noisy false alerts.
- **Periodic audit (quarterly suggested):** for each entry in the Policy Registry, confirm the path resolves or the MCP query returns a result. Flag broken references. Confirm the tier is still appropriate.

---

## 9. Related Guides

- [Guide 01](./01_CLAUDE_MD.md) — where the one-line CLAUDE.md reference lives
- [Guide 03](./03_SKILLS.md) — skill design conventions; `policies-validator` follows them
- [Guide 05](./05_MCP_SERVERS.md) — needed for Pattern B (policies fetched via MCP)
- [Guide 11](./11_GIT_INTEGRATION.md) — `.gitignore` / `.claudeignore` hygiene
- [Guide 12](./12_SECURITY.md) — operational security, prompt injection defence (relevant when policies are loaded from external systems)
- [Guide 14](./14_PERSONAL_DATA_LAYER.md) — the same separation principle applied to personal rather than policy data
