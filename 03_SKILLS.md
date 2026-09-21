# Best Practices: Designing Skills for a Personal Assistant

A skill is a SKILL.md file (plus optional supporting files) that tells the assistant how to perform a specific, recurring type of task — producing formatted meeting notes, triaging support tickets, drafting client status updates, and so on. Good skills make the assistant dramatically more reliable at the things you do repeatedly. This document explains how to write them well.

---

## Why Skills Exist

Without a skill, the assistant has to figure out your preferences from scratch every time. With a skill, it consults a set of instructions that captures: what to do, how to format it, what to avoid, what tools to use, and how to handle edge cases. The skill is the accumulated wisdom of everything you would otherwise have to re-explain.

---

## Install the Same Workflow on Each Surface

Keep the workflow, input contract and output format portable; install and test its native entry point separately. A folder in Cluide's `skills/` distribution directory is source material until the host discovers or installs it.

| Surface | Native route | Metadata and limits |
|---|---|---|
| Claude Code | Project `.claude/skills/<name>/SKILL.md` or personal `~/.claude/skills/<name>/SKILL.md` | Claude frontmatter extensions apply only here; inspect their documented semantics before using them |
| Codex | Repository `.agents/skills/<name>/SKILL.md` or personal `~/.agents/skills/<name>/SKILL.md` | Required `name` and `description`; optional `agents/openai.yaml` for host metadata and invocation policy |
| ChatGPT / conversational Claude | Use the skill or plugin installation surface available to the account | If installation is unavailable, supply the workflow as a source and invoke it explicitly; do not call that automatic discovery |

Minimal migration: copy the common body into a native skill folder, keep only supported metadata, replace tool-specific steps with capability checks, and run one positive trigger, one neighbouring non-trigger and one unavailable-tool case. Keep a single authored workflow when distributing to both; generate or compare installed copies to avoid independent edits.

Tool dependencies and instructions are not permission grants. Claude `allowed-tools`, hook names and model fields must not be copied into OpenAI metadata as if they enforce the same controls. Inspect the active tool inventory and use [Guide 12](./12_SECURITY.md) for enforcement. Missing tools should produce an explicit limitation or a draft that the user can use.

Checked 2026-09-14: [Claude skills](https://code.claude.com/docs/en/skills), [OpenAI skill discovery and metadata](https://learn.chatgpt.com/docs/build-skills). These checks establish the documented paths, not a live run of every bundled skill.

---

## The Anatomy of a Skill

A skill lives in a folder and requires at minimum a single file:

```
my-skill/
└── SKILL.md          (required)
```

For more complex skills, you can add:

```
my-skill/
├── SKILL.md
├── references/       (detailed docs the skill reads on demand)
├── scripts/          (reusable Python/bash scripts called by the skill)
└── assets/           (templates, icons, fonts)
```

**`references/`** — detailed content the skill needs occasionally but not every activation (schemas, full format specs, domain guides). SKILL.md references these by name; the assistant loads them only when needed. Keep SKILL.md itself under ~500 lines and offload the rest here.

**`scripts/`** — Python or shell scripts the skill can execute when the host exposes an appropriate execution tool. Good for fixed-format artifact generation, data transformation, or any repeatable computation that doesn't need the assistant to reason about it.

**Context note (Claude-specific exclusion example):** Files in `references/` and `scripts/` are not loaded into Claude's context automatically — the host initially discovers metadata and loads the skill body when invoked. To discourage Claude from loading them even when exploring the project, add the patterns to `.claudeignore` — but note that `.claudeignore` support varies by product and version; treat it as hygiene, not a security boundary, and pair it with `permissions.deny` rules for genuinely sensitive files (see [Guide 12](./12_SECURITY.md)). See [Guide 11 — Git Integration](./11_GIT_INTEGRATION.md) for `.claudeignore` setup.

The SKILL.md file has two parts: a YAML frontmatter block, and the instruction body.

---

## The Frontmatter: Name and Description

```yaml
---
name: my-skill-name
description: >
  What this skill does and when to use it. (The triggering mechanism.)
---
```

**The description field is the most important part of any skill.** It is how the assistant decides whether to consult the skill at all. A vague description = a skill that never triggers. A precise description = a skill that activates exactly when it should.

**Write the description to be slightly "pushy".** It should name:
1. What the skill does
2. The specific phrases or situations that should trigger it — including casual and implicit phrasings

**Weak description (undertriggers):**
```yaml
description: Helps the user write client update emails.
```

**Strong description (triggers reliably):**
```yaml
description: >
  Produces formatted client status updates and project progress emails. Trigger
  this skill whenever the user wants to send a client an update, check-in, or
  summary — even casual phrasings like "shoot the client a note", "update Sarah
  on where we are", or "write something for the weekly status". Use when the user
  gives bullet points, a rough summary, or just describes the situation. Always
  confirm the desired tone (brief/formal vs. conversational) unless it's already
  clear from context.
```

The second version lists the implicit triggers ("shoot the client a note") and tells the assistant what to do proactively (confirm tone). This prevents a common failure mode where the assistant processes the request itself rather than consulting the skill.

**The description field has a hard length cap.** A save/install path was observed rejecting a description over 1024 characters (encountered 2026-09-21 with a maintenance-routing skill — the author had to shorten it by hand after the save failed). The limit applies to the full `description:` value, not the line count in the YAML block. Being "pushy" (above) and staying under the cap pull the same direction: a description long enough to risk the cap is usually cramming detail that belongs in the skill body instead. Aim for well under it — a few hundred characters covers most skills — and check the actual character count before installing rather than finding the limit at save time.

**Claude Code optional frontmatter fields.** Beyond `name` and `description`, Claude Code supports native extensions. Two of them control tools. `allowed-tools` pre-approves tools for the invoking turn — a read-only reporting skill lists just `Read` and `Grep`, and nothing else is pre-approved. `disallowed-tools` goes further: it removes those tools from Claude's available pool while the skill is active, which is what you want for an autonomous or background skill that must never call something — `AskUserQuestion` in an unattended loop, for instance. An allowlist of pre-approved tools does not remove other tools; `disallowed-tools` is the restriction, with the documented invocation lifetime. Test the effect in Claude Code. Neither field grants equivalent enforcement in OpenAI; see [Guide 12](./12_SECURITY.md).

Other Claude Code fields worth knowing: `paths` takes glob patterns and auto-activates the skill only when you're working with matching files; `context: fork` runs the skill in a forked subagent context, with `agent` choosing the subagent type and `background: false` waiting for the result; `when_to_use` adds trigger context appended to the description; `model` and `effort` override which model and effort level the skill runs at. The full field list is on [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills).

**After editing a skill:** check that the installed host sees the new revision. Codex documents automatic discovery and recommends restarting if a change does not appear. For Claude Code use the reload controls documented by your installed version or a fresh session; this guide does not require an unverified `/reload-skills` command.

**Skills in Cowork:** Cowork loads the skills enabled for your account under Customize, and does not read the Claude Code CLI's `~/.claude` directory on your machine — a skill that exists only there has to be added in Customize before Cowork can use it. Cowork can also record a skill and save skills Claude proposes during a conversation, so a skill can start life there rather than in a file you write by hand.

---

## The Skill Body

The body is markdown instructions the assistant reads when the skill activates. A good body covers:

### 1. Core Responsibilities (3–6 bullet points)

What the skill is fundamentally responsible for. Keep this short — it orients the assistant before it reads the details.

### 2. Workflow / Steps

The procedural heart of the skill. Use numbered steps for sequential actions, use a table for decision logic. Be concrete:

- Name the tools to call (`gmail_create_draft`, `gcal_create_event`, etc.)
- Specify what to ask the user at each stage — for bounded choices, use the host's available and permitted question dialog when appropriate, or one concise text question. Approval requests must follow the native tool's policy; do not assume a choice dialog accepts approvals. `AskUserQuestion` is the Claude example, not a universal tool (see [Guide 20](./20_INTERACTIVE_PROMPTING.md))
- Say what to do when a step fails

### 3. Output Format

If the skill produces a structured output (a task list, a briefing document, a formatted report), show exactly what it should look like. Include a code block example. Ambiguity in output format leads to inconsistency across sessions.

### 4. What the Assistant Can and Cannot Do

If there is a constraint (e.g., "the assistant can create email drafts but cannot send them"), state it clearly in the skill. This prevents the assistant from either overstepping or under-delivering:

```
> This workflow is draft-only. Use a draft-creation tool if available; otherwise return the draft text. Do not send it. Tool availability and permission are separate checks.
> The user sends from Gmail.
```

### 5. Tone and Format Rules

How should this skill's output be written? Formal or casual? Emoji use? Language? If it differs from the canonical policy's defaults, state the narrower workflow rule explicitly.

### 6. Edge Cases

A few "what if" clauses that resolve common ambiguities. Examples:
- "If the email is in a foreign language, read it and present the task summary in the user's preferred language"
- "If there are 15+ unread emails, focus on the 10 most urgent"
- "If tone materially affects the result and is not clear from context, ask a brief question using the available native dialog or text; offer Formal, Casual, or Match original when helpful."

### 7. Example Interaction

One concrete example showing a realistic input and the ideal output. This is the fastest way to convey expectations. It also serves as a sanity check when you're editing the skill — if the example looks wrong, the skill's instructions are wrong.

---

## Progressive Disclosure: Keeping Skills Lean

**Progressive disclosure is the core skill-design principle** — Anthropic names it as such in their Agent Skills engineering post ([anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)): the description is always in context, SKILL.md loads on activation, and reference files load only when a step needs them. Each layer costs tokens only when it earns them.

Aim for under 500 lines in SKILL.md. If you need more:

- Move detailed reference content to a `references/` subfolder
- Reference those files from SKILL.md with a clear note: "For full schema, see references/schemas.md"
- Put reusable scripts in `scripts/` — the assistant can execute them without reading every line into context

The goal is that reading SKILL.md takes <60 seconds and the assistant is ready to go. Long skills that dump everything into one file are harder to follow and slower to load. In Claude Code, use `/skill-doctor` only if the installed version exposes it, and verify its counters and configuration against that version. In Codex or ChatGPT, inspect the available skill/usage controls instead. If per-skill usage is unavailable, record that limitation and compare representative runs; do not invent counters or apply Claude settings to OpenAI.

---

## Memory Within a Skill

If your skill needs to remember things between sessions (shopping habits, snoozed tasks, important contacts), be explicit about what to store and the format:

```markdown
## Memory & Continuity
Use memory to track:
- Snoozed tasks: "Snoozed: [task] — due [date]"
- High-priority senders: "High-priority sender: name@email.com"
- Recurring preferences: "User prefers [brand] at [store]"
```

Without explicit memory instructions, the skill will re-learn the same things from scratch every session.

---

## Common Skill Mistakes

**Vague description:** The skill never triggers, or triggers for things it shouldn't. Fix: rewrite the description with concrete phrases the user would actually type.

**Missing output format:** The skill produces different layouts every session. Fix: include an explicit format example with a code block.

**No edge case handling:** The skill breaks on anything slightly unusual. Fix: add 3–5 "if X, do Y" clauses for the most common deviations.

**Overlong SKILL.md:** The skill is slow to activate and hard to maintain. Fix: move reference material to a `references/` subfolder.

**Omitting tool names:** The skill says "check the calendar" without naming `gcal_list_events`. The assistant may use a different approach each time. Fix: name the exact tools. Not sure what tools are available in your setup? See [Guide 05 — MCP Servers](./05_MCP_SERVERS.md) for how to discover them.

---

<a id="skill-vs-claudemd-vs-task-file"></a>

## Skill vs. Shared Policy vs. Task File

| What | Where |
|------|-------|
| Standing preferences (language, tone, safety rules) | Shared policy and its native entry point (Guide 01) |
| Recurring user-triggered actions (meeting notes, status updates, document drafts) | Skill |
| Automated scheduled workflows (daily digest, contract expiry checks) | Task file (TASK.md) — see [Guide 06](./06_TASK_EFFICIENCY_GUIDE.md) and [Guide 07](./07_TASK_LEARNING_GUIDE.md) |

When in doubt: if the user asks for it ad hoc and it needs consistent, detailed behaviour → skill. If it runs on a schedule without the user asking → task file.

---

## Packaging a Project as a Plugin

A single skill lives in one `SKILL.md`. When a *whole project setup* proves itself — its scaffolding, its slash commands, and the skills that maintain it — you can package the entire thing as an installable plugin, so a fresh copy is one install away. This is the natural endpoint of Guide 16's "build for reuse and sharing": the unit you share is no longer one action, it is a project-in-a-box.

The Claude plugin packaging example below bundles four things. For OpenAI, package through its documented plugin mechanism; this manifest and slash-command layout are not a portable installer. The authored scaffold should retain shared `AGENTS.md` policy and thin native adapters.

```
my-project.plugin/
  .claude-plugin/
    plugin.json        ← manifest: name, version, description, keywords
  templates/           ← the empty project scaffold, copied into a new folder
    AGENTS.md          ← shared policy
    CLAUDE.md          ← Claude adapter
    <trackers, profile, dashboard, starting folders…>
  commands/            ← slash commands (setup, rebuild-dashboard, …)
  skills/
    <skill-name>/
      SKILL.md         ← the skill that operates the project day-to-day
      references/
```

- **`templates/`** holds the empty project structure — shared policy, native adapters, the trackers, the starting folders — that a `setup` command copies into place.
- **`commands/`** are the runnable entry points: one to scaffold a new project from the templates, one to regenerate a derived view (e.g. a dashboard) from the trackers.
- **`skills/`** are the maintenance workflows that keep the project consistent across sessions.

Everything operates on local files inside the scaffolded project — no remote dependencies — so an installed plugin and the project it creates stay self-contained.

Reach for this only when the unit of reuse is an entire project. For a single recurring action, a plain skill (above) is still the right unit; a plugin is the wrapper you add once that one skill has grown a scaffold, its own commands, and a structure worth reproducing.

---

## Real-World Examples

Four skills that illustrate different patterns. None of them ships in this repo's `skills/` folder — they are described here to illustrate the patterns, not to be installed. For the skills Cluide does ship, see `00_INDEX.md`.

---

### gmail-task-manager — A skill with clear triage logic

**What it does:** Scans Gmail for unread emails, extracts actionable items, and presents them as a prioritised task list. Can draft replies, create calendar events, and snooze tasks.

**Key design choices:**
- **Description lists implicit triggers** — "what's pending?", "catch me up", "any follow-ups?" — so the skill activates from natural phrasing, not just a precise command.
- **Scanning strategy is explicit** — specific Gmail search queries (`is:unread newer_than:7d`) are written into the workflow, not left to the assistant to figure out.
- **Output format is shown with an example** — the 🔴🟡🟢 priority structure is defined once and reused every run.
- **"the assistant can create drafts but cannot send"** — the constraint is stated clearly, with native permissions enforcing the boundary where required.
- **Edge cases are named** — too many emails (15+), Finnish-language emails, long threads — each has a defined handling rule.

**What makes the description work:**

```yaml
description: >
  Scans Gmail for actions, tasks, and follow-ups and turns them into a clear,
  prioritised task list. Trigger this skill whenever the user asks to check their
  email for things to do, wants to know what needs their attention, asks
  "what do I need to action?", "any tasks in my email?", "what's pending?",
  "check my inbox", "any follow-ups?", "what emails need a reply?",
  "catch me up on my emails", or any similar request related to managing
  email-based actions.
```

This is a strong description: it names the implicit trigger phrases, is specific about the task, and uses "trigger this skill" explicitly.

---

### grocery-list-assistant — A skill that learns over time

**What it does:** Builds shopping lists for the user's regular supermarkets, learns from habits, suggests items proactively, and can email the finished list to the user.

**Key design choices:**
- **Memory is built into the skill** — the skill maintains a running model of staples, brand preferences, and run-out items using explicit project memory files (Guide 04), or native memory when that is the intended store.
- **Proactive suggestion on session start** — the skill doesn't wait to be told what to add; it surfaces what you probably need based on past behaviour.
- **Output format is grouped by store section** — produce/dairy/bread etc. — which mirrors how a real store is laid out.
- **Recipe-based ingredient extraction** — "I want to make risotto" maps to a specific ingredient list, cross-checked against likely in-stock items.

**The grocery skill is a good model for any skill that benefits from cross-session learning** — the memory structure (staples, brand preferences, run-outs, avoided items) can be adapted to other domains.

---

### finnish-message-assistant — A skill for structured output variants

**What it does:** Writes Finnish messages, emails, and texts. Produces two tone variants by default (formal and casual) with notes on the differences.

**Key design choices:**
- **Input-agnostic** — handles English text, bullet points, or a situation description. The skill normalises inputs before producing output.
- **Always two versions** — unless tone is already specified. This is baked in as a default, not something the user has to ask for each time.
- **Format is shown as an example** — the formal/casual pair, subject lines, and "key differences" note are all illustrated with a concrete worked example.
- **SMS/WhatsApp has separate rules** — shorter, no openers, no formal variant unless asked. Named explicitly because the user texts in Finnish regularly.

---

### backlog — A skill where files replace memory

**What it does:** Manages a project backlog across sessions using two files: `BACKLOG.md` (living idea list) and `DECISIONS.md` (architectural decision log). Runs standard sessions (`/backlog`) and grooming sessions (`/backlog groom`), handles initialization automatically, and guards against re-litigating closed decisions.

**Where to use it:** Any project where you want to track ideas, improvements, and architecture decisions across assistant sessions — regardless of language or domain. Install the skill through the native route and verify that it reads the two files from the intended project.

**Key design choices:**
- **Files are the persistence layer, not native memory** — `DECISIONS.md` plays the role that memory would in other skills. The skill explicitly states that native memory should not be used, so state never ends up in two places.
- **Two session modes with different scopes** — the standard session runs a focused orient → prioritize → pick → write loop; the grooming session inserts a full architecture review. Separating them prevents grooming overhead from slowing down everyday sessions.
- **Conflicts and dependencies block selection** — items with unresolved `Conflicts-with` or unsatisfied `Dependencies` cannot be picked. This is enforced as a rule, not a suggestion.
- **Constraint is explicit** — "the assistant writes the files but does not commit." The user commits. Stating this prevents the assistant from attempting git operations.
- **Orient output format is shown** — a concrete table + flagged-items block, so the expected layout is checkable across sessions.

**The backlog skill is a good model for any skill where the data outlives the conversation** — the pattern of "two files, one for state and one for decisions" can be adapted to support tickets, product specs, hiring pipelines, or any domain where you need both a working list and an immutable audit trail.

---

## Giving This to an Assistant

> "Read 03_SKILLS.md and create a skill for [what you want]. Follow all the best practices in the guide — strong description, workflow steps, output format example, and at least 3 edge cases."

**Faster alternative:** `tasks/setup-skill.md` interviews you and generates a complete skill without reading the guide first. `tasks/audit-skill.md` reviews an existing skill against this guide's checklist.
