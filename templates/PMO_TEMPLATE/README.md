# Template: PMO Initiative — Claude Workspace

This template sets up a Claude-assisted project workspace for managing a **PMO project**. It includes a CLAUDE.md with project rules, a project guide, an initiative charter, and a full PMO register suite (risks, actions, dependencies, decisions, and a knowledge base).

The template is structured as a Cowork project folder. When customized and dropped into a Cowork workspace, Claude will automatically load and apply all project rules and context.

> **Companion guides:** [09 Multi-Task Orchestration](../../09_MULTI_TASK_ORCHESTRATION.md) · [11 Git Integration](../../11_GIT_INTEGRATION.md) · [12 Security](../../12_SECURITY.md)

---

## What you'll need

- A Cowork workspace folder (or any folder you use with Claude)
- Access to Claude (via Claude.ai, Cowork, or Claude Code)
- Basic familiarity with Markdown files
- Placeholder values for your initiative (see "How to customize" below)

---

## What's included

```
PMO_TEMPLATE/
├── CLAUDE.md                          ← Claude project instructions (rules + routing)
├── PROJECT_GUIDE.md                   ← Folder map: what every file is, what to update
├── Charter/
│   └── Initiative_Charter.md          ← Initiative charter (scope, objectives, team, KPIs)
├── FinancialModel/
│   └── Model_Summary.md              ← Claude-readable summary of the financial model
├── ProjectPlan/
│   └── Project_Plan.md               ← Project plan (scope, milestones, timeline)
├── Data/                              ← Raw data exports (do not modify)
└── PMO/
    ├── Guardrails.md                  ← Claude skill: PMO validation guardrails
    ├── Knowledge_Base.md              ← Running knowledge base / institutional memory
    ├── Risk_Register.md               ← Risk register (rated + linked to dependencies)
    ├── Action_Tracker.md              ← Open action items (non-milestone tasks)
    ├── Dependency_Register.md         ← Internal + external programme dependencies
    └── Decision_Tracker.md            ← All programme decisions, with rationale
```

---

## How to customize

Replace every `[PLACEHOLDER: ...]` value with your own content. The table below lists each one:

| Placeholder | What to fill in | Example |
|---|---|---|
| `[PLACEHOLDER: Company Name]` | Your company or organisation | Northstar Inc |
| `[PLACEHOLDER: Initiative ID]` | Your initiative reference number or code | VCI-12 |
| `[PLACEHOLDER: Initiative Name]` | Short name for the initiative | Project Apex |
| `[PLACEHOLDER: Initiative Owner Name]` | Full name of the initiative owner | Alex Jordan |
| `[PLACEHOLDER: Team Member 1/2/3]` | Internal team members | Sam Lee, Jordan Park |
| `[PLACEHOLDER: External Consultant Name]` | External advisor or support resource | Robin Clarke |
---

## How to use it

1. Copy this entire folder into the workspace folder you use with Claude (Cowork, Claude Code working directory, etc.).
2. Replace all `[PLACEHOLDER: ...]` values across all files.
3. Fill in the Charter with your actual initiative scope, team, KPIs, and financial figures.
4. Clear or reset the PMO registers (Risk, Action, Dependency, Decision) — the current entries are illustrative examples. Keep the schema and format.
5. Add your own risks, actions, and dependencies as you work.
6. Claude will read `CLAUDE.md` and `PROJECT_GUIDE.md` automatically and apply all project rules in every conversation.
7. **(Optional) Install the Guardrails skill:** To have Claude automatically validate recommendations against the charter, copy `PMO/Guardrails.md` to `.claude/skills/pmo-guardrails/SKILL.md`.

---

## Notes
- The `Knowledge_Base.md` is intentionally blank in the template — populate it as your project progresses.
- The HTML versions of registers (`.html` files) are optional view-only renderings. You can generate them from the Markdown files, or omit them.
- If your governance framework has fewer or more gate stages than the five (AG1–AG5) shown here, adjust all references throughout.
