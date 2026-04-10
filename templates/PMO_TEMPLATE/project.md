# Cowork Project: [PLACEHOLDER: Initiative Name — e.g. "Legacy-to-Cloud Migration Initiative"]

## Purpose

This project workspace supports a structured, Claude-assisted programme to migrate customers from a legacy on-premises product to a cloud platform. It provides Claude with the full context, rules, and registers needed to act as an embedded PMO assistant throughout the initiative lifecycle.

## Project overview

| Field | Value |
|---|---|
| Initiative ID | [PLACEHOLDER: Initiative ID — e.g. "VCI-12"] |
| Initiative name | [PLACEHOLDER: Initiative Name] |
| Owner | [PLACEHOLDER: Initiative Owner Name] |
| Sponsor | [PLACEHOLDER: Workstream Sponsor Name] |
| Governance model | [PLACEHOLDER: Governance Framework — e.g. "Stage-Gate (AG1–AG5)"] |
| Current gate | [PLACEHOLDER: Current Gate — e.g. "AG1: Initiative Idea"] |
| Legacy product | [PLACEHOLDER: Legacy Product Name] |
| Cloud target | [PLACEHOLDER: Cloud Platform Name] |

## Tasks in this project

This project has no pre-configured Cowork tasks — it is a **context-loaded workspace** rather than an automated task runner. Claude operates interactively, guided by the CLAUDE.md project rules, and performs PMO, analytical, and documentation tasks on request.

Suggested tasks to add to this project as your initiative matures:

- **Weekly register review** — prompt Claude to review and update Risk, Action, and Dependency registers based on meeting notes or new information.
- **Financial model update** — prompt Claude to update Model_Summary.md when the Excel model changes.
- **Steerco pack prep** — prompt Claude to compile a Steerco/steering committee slide deck from current register status.
- **Action tracker triage** — prompt Claude to review overdue or blocked actions and propose next steps.
- **Knowledge base capture** — after key meetings, prompt Claude to extract and log new insights into Knowledge_Base.md.

## Shared context

The following files provide Claude with standing context for every conversation in this project:

- `CLAUDE.md` — project rules, routing logic, and update triggers
- `PROJECT_GUIDE.md` — folder map, file purposes, and read/write permissions
- `Charter/Initiative_Charter.md` — initiative scope, team, KPIs, and financials (read-only)
- `PMO/Guardrails.md` — PMO validation skill; validates every recommendation against the charter
