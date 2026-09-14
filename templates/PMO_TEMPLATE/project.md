# Project: [PLACEHOLDER: Initiative Name — e.g. "Project Apex"]

## Purpose

This project workspace supports a structured, assistant-supported programme to deliver [PLACEHOLDER: brief description of the initiative — e.g. "a new operational capability within the organisation"]. It provides the assistant with the full context, rules, and registers needed to act as an embedded PMO assistant throughout the initiative lifecycle.

## Project overview

| Field | Value |
|---|---|
| Initiative ID | [PLACEHOLDER: Initiative ID — e.g. "PMO-07"] |
| Initiative name | [PLACEHOLDER: Initiative Name] |
| Owner | [PLACEHOLDER: Initiative Owner Name] |
| Sponsor | [PLACEHOLDER: Workstream Sponsor Name] |
| Governance model | [PLACEHOLDER: Governance Framework — e.g. "Stage-Gate (Gate 1–Gate 5)"] |
| Current gate | [PLACEHOLDER: Current Gate — e.g. "Gate 1: Concept"] |
| Delivery approach | [PLACEHOLDER: Delivery Approach — e.g. "Phased delivery across 4 workstreams"] |

## Tasks in this project

This project has no pre-configured scheduled tasks — it is a **context-loaded workspace** rather than an automated task runner. The assistant operates interactively, guided by the AGENTS.md project rules, and performs PMO, analytical, and documentation tasks on request.

Suggested tasks to add to this project as your initiative matures:

- **Weekly register review** — prompt the assistant to review and update Risk, Action, and Dependency registers based on meeting notes or new information.
- **Financial model update** — prompt the assistant to update Model_Summary.md when the Excel model changes.
- **Steerco pack prep** — prompt the assistant to compile a Steerco/steering committee slide deck from current register status.
- **Action tracker triage** — prompt the assistant to review overdue or blocked actions and propose next steps.
- **Knowledge base capture** — after key meetings, prompt the assistant to extract and log new insights into Knowledge_Base.md.

## Shared context

The following files provide the assistant with standing context for every conversation in this project:

- `AGENTS.md` — project rules, routing logic, and update triggers
- `PROJECT_GUIDE.md` — folder map, file purposes, and read/write permissions
- `Charter/Initiative_Charter.md` — initiative scope, team, KPIs, and financials (read-only)
- `PMO/Guardrails.md` — PMO validation skill; validates every recommendation against the charter

## App bootstrap

Use `PLATFORM_SETUP.md` for the selected product and record its applied fields and source revision there. This overview is source material, not proof that any app settings were applied.
