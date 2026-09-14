# Template: PMO Initiative — Shared Assistant Workspace

Start with `PLATFORM_SETUP.md`: choose Claude or OpenAI and verify source access. `AGENTS.md`
is shared policy; `CLAUDE.md` is its thin Claude adapter. ChatGPT needs the explicit project-source
bootstrap; Codex uses the repository workspace. No surface is verified merely by copying files.


This template sets up a assistant-supported project workspace for managing a **PMO project**. It includes a AGENTS.md with project rules, a project guide, an initiative charter, and a full PMO register suite (risks, actions, dependencies, decisions, and a knowledge base).

The template is a shared project folder. Configure the chosen surface and verify instruction loading using `PLATFORM_SETUP.md` before relying on its rules.

> **Companion guides:** [09 Multi-Task Orchestration](../../09_MULTI_TASK_ORCHESTRATION.md) · [11 Git Integration](../../11_GIT_INTEGRATION.md) · [12 Security](../../12_SECURITY.md)

---

## What you'll need

- A project folder or a dated set of uploaded project sources
- Access to the selected Claude or OpenAI surface and the tools needed for the task
- Basic familiarity with Markdown files
- Placeholder values for your initiative (see "How to customize" below)

---

## What's included

```
PMO_TEMPLATE/
├── AGENTS.md                          ← assistant project instructions (rules + routing)
├── project.md                         ← App-side description/instructions text (Guide 25 fields — paste into the app)
├── PROJECT_GUIDE.md                   ← Folder map: what every file is, what to update
├── Charter/
│   └── Initiative_Charter.md          ← Initiative charter (scope, objectives, team, KPIs)
├── Financial Model/
│   └── Model_Summary.md              ← assistant-readable summary of the financial model
├── Project Plan/
│   └── Project_Plan.md               ← Project plan (scope, milestones, timeline)
├── Data/                              ← Raw data exports (do not modify)
├── Incoming/                          ← Intake queue for material arriving outside chat (delete if unused)
├── PMO/
│   ├── Guardrails.md                  ← Policy: PMO validation guardrails
│   ├── Knowledge_Base.md              ← Running knowledge base / institutional memory
│   ├── Risk_Register.md               ← Risk register (rated + linked to dependencies)
│   ├── Action_Tracker.md              ← Open action items (non-milestone tasks)
│   ├── Dependency_Register.md         ← Internal + external programme dependencies
│   └── Decision_Tracker.md            ← All programme decisions, with rationale
└── Updater-Task/
    └── Task.md                        ← Runnable cross-reference audit across the registers
```

---

## How to customize

Replace every `[PLACEHOLDER: ...]` value with your own content. The table below lists the main placeholders:

| Placeholder | What to fill in | Example |
|---|---|---|
| `[PLACEHOLDER: Company Name]` | Your company or organisation | Northstar Inc |
| `[PLACEHOLDER: Initiative ID]` | Your initiative reference number or code | INI-07 |
| `[PLACEHOLDER: Initiative Name]` | Short name for the initiative | Project Apex |
| `[PLACEHOLDER: Initiative Owner Name]` | Full name of the initiative owner | Alex Jordan |
| `[PLACEHOLDER: Team Member 1/2/3]` | Internal team members | Sam Lee, Jordan Park |
| `[PLACEHOLDER: External Consultant Name]` | External advisor or support resource | Robin Clarke |
---

## How to use it

1. Copy this folder to the chosen workspace; follow `PLATFORM_SETUP.md` for ChatGPT source uploads.
2. Replace all `[PLACEHOLDER: ...]` values across all files.
3. Fill in the Charter with your actual initiative scope, team, KPIs, and financial figures.
4. Clear or reset the PMO registers (Risk, Action, Dependency, Decision) — the current entries are illustrative examples. Keep the schema and format.
5. Add your own risks, actions, and dependencies as you work.
6. Configure the bootstrap and run a fresh-session check for `AGENTS.md` and `PROJECT_GUIDE.md` on every selected surface.
7. **Guardrails:** read `PMO/Guardrails.md` as project policy. Optional native skill packaging is product-specific: use Cluide’s `tasks/setup-skill.md`, preserve the domain checks, and test discovery on the chosen surface. Copying a policy file alone does not prove a skill is valid or loaded.
8. **(Optional) Run the Updater-Task periodically:** After a heavy editing session — or on a cadence (e.g. weekly) — open `Updater-Task/Task.md` with your assistant and follow its steps. It audits cross-references across the four registers + KB, fixes what it can, and appends a change-log entry.

---

## Conventions

- **`[ARCHIVE]` folders** — any folder whose name starts with `[ARCHIVE]` (e.g. `[ARCHIVE] Previous Plans/`) is a read-only backup. The assistant is instructed never to read from or write to them (see `AGENTS.md`). Use this prefix when you retire old material but want to keep it on disk.
- **`_LATEST` filename suffix (optional)** — when a file starts going through versioned iterations (common for the project plan), rename the active copy to `<name>_LATEST.md` and move older revisions into an `[ARCHIVE]` subfolder. Don't adopt this until versioning actually starts — the unsuffixed name shipped with the template is fine while there's only one.
- **Register ID format** — `R-##` (risks), `D-##` (dependencies), `ACT-<Cat>-##` (actions, where `Cat` is one of P/C/F/O/D/PJ), `DEC-##` (decisions), `KB §#` (knowledge-base sections). Don't mix in legacy prefixes — the Updater-Task will flag them.

---

## Notes
- The `Knowledge_Base.md` is intentionally blank in the template — populate it as your project progresses.
- If you generate HTML versions of the registers (`.html` files), treat them as optional view-only renderings of the Markdown files — none ship with the template.
- Two folder names contain spaces (`Financial Model/`, `Project Plan/`) — quote them in shell commands (e.g. `ls "Financial Model/"`).
- If your governance framework has fewer or more gate stages than the five (Gate 1–Gate 5) shown here, adjust all references throughout.
