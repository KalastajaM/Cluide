# Company Policies Guide: Embedding Existing Policies as Guardrails

> How to make either assistant apply your organisation's existing policies — AI use policy, Code of Conduct, data classification, and similar — without copying the policy content into Cluide. Policies stay where they already live; Cluide holds only the pointers and the enforcement logic.

> **Companion guides:** [Guide 03](./03_SKILLS.md) covers skill design — the `policies-validator` skill follows its conventions. [Guide 05](./05_MCP_SERVERS.md) covers MCP server setup, needed when policies live in SharePoint or Confluence. [Guide 12](./12_SECURITY.md) covers operational security; this guide covers *policy* enforcement. [Guide 30](./30_CONTROLLED_DOCUMENTS.md) covers maintaining the policy documents themselves — review, versioning and approval — where this guide covers applying them.

> **Giving this guide to an assistant:**
> "Read 21_COMPANY_POLICIES.md and help me wire up the company policies I care about."
>
> **Faster alternative:** `tasks/setup-policies.md` runs the full interview, classifies each policy, and generates the skill end-to-end without reading the guide first.

---

Shared rules belong in `AGENTS.md` for Codex or a dual-platform repository, with a thin `CLAUDE.md` adapter; app projects bootstrap the same policy through accessible sources. Native skill installation follows Guide 03. Google surfaces (Antigravity and the Gemini app) follow the same principle; their mechanisms are listed in [Guide 35 §9](./35_DUAL_PLATFORM_PROJECTS.md#9-platform-facts), documented and not yet tested.

## 1. Why This Pattern

Most organisations already publish the policies that should shape Claude's behaviour — AI use policy, Claude-specific guidelines, Code of Conduct, data / information classification, export control, acceptable use. These are authoritative documents owned by legal, security, or HR. They change on their own schedule, have formal approval workflows, and are sometimes confidential to the organisation.

The problem: the assistant does not automatically know about any of this. Without explicit wiring, a skill will happily help draft a customer email that breaches tone guidelines, a task will happily process data classified above what it should touch, and a chat session will happily cite sources the policy prohibits.

The goal of this pattern:

- Relevant policies are checked as part of the workflow, with evidence and human review where required
- Policy *content* stays in its authoritative location (SharePoint, Confluence, or a private local folder) — Cluide contains only pointers
- The response scales with the policy: a data classification breach stops the work and escalates, a style guide nudges softly
- The limits are stated plainly: a policy the assistant reads can stop what the assistant does next, never what the user has already sent (see *What a policy line cannot stop*)
- Policy changes flow through a freshness check; uploaded or cached copies must be refreshed before use

**Why not just put the policies in the shared policy?**

- The shared policy is loaded into every session, which inflates context
- Copies drift from the authoritative source — and it is not obvious which copy is current
- Cluide is designed to be shareable. Pasting confidential policies into it defeats that
- The shared policy has no enforcement mechanism — it is advisory. Policies often need a stronger surface

### What a policy line cannot stop

Every mechanism in this guide — the skill, the shared policy line, a project instruction, `CLAUDE.md` or `AGENTS.md` — is text the model reads alongside the user's input. The check runs inside the service that has already received that input. If the policy says "no customer data" and the user pastes a customer file, the assistant can recognise the breach and refuse to go on, but the file has already been sent, processed and, on most surfaces, stored in the conversation. Recognising the data *is* processing it. A policy line reports a breach after the fact; it does not prevent one.

So place each control at the moment it can act:

| Moment | What can stop it | What cannot |
|---|---|---|
| **Before the input leaves the user** (paste, upload, attachment, typed prompt) | Training and redaction habits; data loss prevention, CASB or browser and endpoint controls on the user's device or network; admin settings that disable uploads or restrict which tools may be used; routing sensitive work to an approved internal tool. In Claude Code only, a `UserPromptSubmit` hook (below) | Any skill or instruction the assistant reads |
| **When the assistant reads data** (files, connectors, MCP tools) | Access rights on the source; connector and OAuth scopes; `permissions.deny` rules and `PreToolUse` hooks ([Guide 12](./12_SECURITY.md)) | A policy line asking the assistant not to look |
| **When the assistant produces output or acts** (drafts, sends, writes, calls a tool) | The T1/T2 checks in this guide, backed by permissions and approvals for consequential actions ([Guide 32](./32_ACTION_AUTHORITY.md)) | Nothing further: this is where the skill does real work |

**The one in-product pre-send control: Claude Code's `UserPromptSubmit` hook.** It runs before each prompt is processed and can reject it, in which case the prompt never reaches the model ([hooks reference](https://code.claude.com/docs/en/hooks), checked 2026-11-11). Know its limits before relying on it. It sees the prompt text (pasted text arrives expanded), not files the assistant reads later — those fall to deny rules. A hook that times out lets the prompt through unless it sets `onFailure: "block"`. A blocked prompt still lands in the local transcript and prompt history. And it exists only in Claude Code: the Claude and ChatGPT chat apps have no equivalent, so there the before-send row depends entirely on controls outside the assistant.

For a policy whose breach is the act of sending — data classification, export control, confidentiality — the skill is a backstop and a teaching moment, not the control. Record which upstream control, if any, covers each such policy (the *Upstream controls* table in `policies-validator` §2), so the gap is visible rather than assumed away. Policies, training, access rights and security tooling do the preventing; the assistant's instructions make the policy visible at the point of work.

---

## 2. The Separation Principle

Three layers, cleanly separated:

| Layer | Contains | Lives where | Shareable? |
|---|---|---|---|
| **Cluide** | Generic framework — guides, templates, skill scaffolding | This repo | Yes |
| **Policy content** | The actual policy text (AI use, Code of Conduct, classification…) | Outside Cluide — central folder or external system | No (org-confidential) |
| **The bridge** | A skill and one shared policy line that reference the policy content by path / URL | Inside the project (shared policy plus the native skill location from Guide 03) | Yes — only pointers, no policy text |

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
- One source of truth across all your assistant projects
- Updating a policy once is enough
- Never accidentally committed — the folder is not part of any repo
- Works offline

**Cons:**
- Machine-local — does not help colleagues without the same folder
- You are responsible for keeping it in sync with the authoritative source
- Risk of staleness if you forget to update after a policy is revised

**File hygiene:**
- Keep the folder outside any git-tracked directory (simplest)
- If it must live inside a repo for any reason, add the folder to `.gitignore` **and** add a `Read(...)` deny rule for it in `permissions.deny`, because Claude Code does not enforce `.claudeignore` — see [Guide 11](./11_GIT_INTEGRATION.md) and [Guide 12](./12_SECURITY.md) §7

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
| **T1 — Stop and escalate** | Refuse the action, escalate | Data classification, export control, information security, legal constraints | Pre-action check. On violation: stop, emit `🛑 POLICY BLOCK`, point to the policy and owner. Do not produce the requested output. |
| **T2 — Required check** | Validate and surface the result | AI use policy, Claude-specific guidelines, Code of Conduct | Pre-response checklist. Emit `⚠️ POLICY ALERT` when the response drifts, or `✅ POLICY ALIGNED` when it passes. |
| **T3 — Soft guidance** | Load into context; apply judgment | Style guides, preferred vendors, tone guidelines, branding rules | Content is loaded into context; the assistant applies it while drafting. No required output block. |

**What T1 is and is not.** T1 is best-effort model behaviour, not a technical control: a skill and a shared policy line are the same kind of mechanism — prompt-level instructions the model is asked to follow — and neither can guarantee the stop fires every time. Even when it fires, it acts on what the assistant does next, never on input already sent (see *What a policy line cannot stop* in §1). Permission rules and hooks ([Guide 12](./12_SECURITY.md)) are enforced by the tooling rather than the model, so pair T1 policies with them for reads and actions; for input, the before-send controls in §1 are the only prevention. Compliance readers should not treat T1 as a technical boundary. The output marker keeps its name, `🛑 POLICY BLOCK`, for compatibility with installed skills: it blocks the response, not the data.

The emoji markers (🛑 / ⚠️ / ✅) are intentional signalling — they make policy outcomes scannable at a glance — and are a deliberate exception to any project-level no-emoji conventions.

### Worked example — T1 (Stop and escalate)

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
Owner:  Data Governance team — datagovernance@example.com

The pasted content has already reached this service; this block stops the
summary but cannot undo the send. Report it if the policy requires.

What to do next: re-run with the export redacted to Public/Internal only,
or route the request through an approved internal tool.
```

> **The data has already been sent.** By the time this block fires, the customer export is in the session: the service has received it and the model has read it in order to recognise it. The block stops the summary and tells the user what went wrong — it cannot un-send the paste. Treat a T1 block on input as an incident signal: the user may need to report it under the policy, and the fix is upstream (redaction before pasting, DLP, an approved internal tool), not a better skill. See *What a policy line cannot stop* in §1.

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

## Bind Policy to Each Platform's Actual Controls

Keep policy ownership, source links, revision dates and consequence classes shared. Put native enforcement in the appropriate configuration: Claude Code permissions/hooks, Codex sandbox/approvals, and each conversational product's app grants. A policy-validation skill is an advisory/review mechanism unless an actual permission denies the prohibited action.

For ChatGPT uploaded sources, a new policy version in SharePoint or the repository does not update the uploaded copy. Record the source revision and retrieval date, refresh it before policy-sensitive work, and report when it cannot be verified. For a connector-based read, validate the document's authority and revision rather than trusting the first similarly named result.

Test one permitted and one prohibited fixture on every supported surface. Record the observed enforcement mechanism and result separately; if a control exists only in Claude Code, mark OpenAI's status as untested or unavailable and choose a narrower workflow. Do not describe a prose-only instruction as a hard block. [Guide 12](./12_SECURITY.md) owns the native security procedures and Guide 35 (in the Cluide guide set) the capability-gap record.

---

## 5. Implementation Pattern

The pattern has three integration points. All three are needed; skipping any one weakens enforcement.

### 5.1 The skill — `policies-validator`

The active component. A single skill, installed once per user (or per project), containing:

- A **Policy Registry** table with every policy, its tier, and its location
- The **Validation Protocol** — what to do before each response, tier by tier
- The **Output Formats** — the block templates for POLICY BLOCK / POLICY ALERT / POLICY ALIGNED

The structure mirrors the existing PMO Guardrails skill at `templates/PMO_TEMPLATE/PMO/Guardrails.md` — specifically the pre-response checklist pattern in section 11 of that file. `policies-validator` generalises it from one initiative charter to a registry of company policies.

A generic, ready-to-install version is bundled at `skills/policies-validator/SKILL.md`.

<a id="52-the-claudemd-line"></a>

### 5.2 The Shared Policy Line

One line in the project's shared policy tells the assistant to consult the skill on every turn:

```markdown
## Company policies
Before responding, consult the `policies-validator` skill. T1 violations must
stop the work and escalate; T2 issues must be surfaced; T3 guidance should shape
the response.
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
- **If policies are stored locally inside a git-tracked folder:** add the folder to `.gitignore` and add a `Read(...)` deny rule for it in `permissions.deny` (Claude Code does not enforce `.claudeignore`). See [Guide 11](./11_GIT_INTEGRATION.md) and [Guide 12](./12_SECURITY.md) §7.
- **If policies are fetched via MCP:** nothing to ignore — but confirm the MCP server's authentication flow does not log credentials into session transcripts. See [Guide 12](./12_SECURITY.md).

**The skill itself** (`skills/policies-validator/SKILL.md`) is Cluide-safe by design: it contains only `[PLACEHOLDER: ...]` markers where policy names, paths, and owners go. The filled-in version lives in `~/.claude/skills/policies-validator/SKILL.md` on each user's machine (or in `.claude/skills/` per project), not in the repo.

---

## 7. Verification

After running `tasks/setup-policies.md`, test the wiring with three prompts:

| Test | Expected outcome |
|---|---|
| Ask something benign ("What's the weather pattern called when warm air sits above cold air?") | No policy marker at all — the question touches no policy. (Only expect `✅ POLICY ALIGNED` in setups where a configured T2 policy is actually relevant to the prompt.) |
| Ask something that exercises a T2 policy (e.g. "draft an external email" when the AI use policy requires labelling) | `⚠️ POLICY ALERT` with a reference to the AI use policy |
| Ask something that violates a T1 policy (e.g. paste mock data flagged Confidential — never real data, since pasting it is itself the breach) | `🛑 POLICY BLOCK` with refusal and escalation path |

A T3 policy should silently shape tone — test by asking for a draft and checking that the output follows the style guide without any visible block.

---

## 8. Maintenance

- **When a policy is revised:** update the source (the local file or the SharePoint / Confluence page). No change to Cluide. No change to the skill. The next turn that reads the source sees the new text. An uploaded or cached copy (a ChatGPT project source, a within-session cache) must be refreshed first; see *Bind Policy to Each Platform's Actual Controls*.
- **When a new policy is introduced:** re-run `tasks/setup-policies.md`. It will pick up the existing registry, ask about the new policy, and append it.
- **When a policy is retired:** remove its row from the Policy Registry in the skill. Leaving stale entries causes broken-link behaviour and noisy false alerts.
- **Periodic audit (quarterly suggested):** for each entry in the Policy Registry, confirm the path resolves or the MCP query returns a result. Flag broken references. Confirm the tier is still appropriate.

---

## 9. Related Guides

- Guide 01 (in the Cluide guide set) — where the shared policy reference lives
- [Guide 03](./03_SKILLS.md) — skill design conventions; `policies-validator` follows them
- [Guide 05](./05_MCP_SERVERS.md) — needed for Pattern B (policies fetched via MCP)
- [Guide 11](./11_GIT_INTEGRATION.md) — `.gitignore` / `.claudeignore` hygiene
- [Guide 12](./12_SECURITY.md) — operational security, prompt injection defence (relevant when policies are loaded from external systems)
- [Guide 14](./14_PERSONAL_DATA_LAYER.md) — the same separation principle applied to personal rather than policy data
