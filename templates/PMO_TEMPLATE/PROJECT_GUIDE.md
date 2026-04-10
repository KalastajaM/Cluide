# [PLACEHOLDER: Initiative ID] – [PLACEHOLDER: Initiative Name]: Project Guide

## Quick reference: What do you need to do?

| Task | Where to look | Where to update |
|---|---|---|
| Understand the project scope & goals | `Charter/Initiative_Charter.md` | ❌ Do not modify |
| Check project constraints & boundaries | `PMO/Guardrails.md` | ❌ Do not modify unless explicitly asked |
| Look up or record project knowledge/insights | `PMO/Knowledge_Base.md` | ✅ Append new insights here |
| View or update the programme risk register | `PMO/Risk_Register.md` | ✅ Update when risk status, likelihood, or impact changes |
| Track open clarification, investigation, and decision actions | `PMO/Action_Tracker.md` | ✅ Update when actions are opened, progressed, or closed |
| Record or review programme decisions | `PMO/Decision_Tracker.md` | ✅ Update when decisions are made, revised, or superseded |
| Track programme-level dependencies (internal & external) | `PMO/Dependency_Register.md` | ✅ Update when dependency status, target date, or priority changes |
| Understand the financial model | `FinancialModel/Model_Summary.md` | ✅ Update when the Excel model changes |
| Work with the financial model itself | `FinancialModel/[PLACEHOLDER: Financial Model Filename].xlsx` | ✅ Main financial model |
| Access raw source data | `Data/*.csv` (or equivalent) | ❌ Raw source data — do not modify |
| View or build the project plan | `ProjectPlan/` | ✅ Work in progress |

---

## Folder-by-folder breakdown

### `Charter/`
The initiative charter. This is **fixed and static** — do not modify it unless the user explicitly asks you to. Use it to understand the original mandate, scope, and objectives of the project.

### `PMO/`
Home for programme management artefacts: registers, the knowledge base, and guardrails.

- **`PMO/Guardrails.md`** — Defined guardrails for the project, derived from the charter. **Do not modify** unless explicitly instructed.
- **`PMO/Knowledge_Base.md`** — The central knowledge base. Any new insight, finding, decision, or relevant piece of information should be captured here. When in doubt about where to record something, put it here.
- **`PMO/Dependency_Register.md`** — Programme-level register of internal and external dependencies. **Update** when a dependency's status, target date, or priority changes. The Risk Register references dependency IDs (D-xx) where a missed dependency drives a risk. Do not duplicate dependency tracking in the KB or Risk Register — link to this file instead.
- **`PMO/Risk_Register.md`** — Programme risk register. Update when risk status, likelihood, or impact changes.
- **`PMO/Action_Tracker.md`** — Open clarification, investigation, and decision actions.
- **`PMO/Decision_Tracker.md`** — Programme decision register. Update whenever a decision is made, revised, or superseded.

### `FinancialModel/`
- **`[PLACEHOLDER: Financial Model Filename].xlsx`** — the official financial model. This is the primary source of truth for financial figures.
- **`Model_Summary.md`** — a Claude-generated description of the model. **Must be updated** whenever the Excel model is updated.

### `Data/` (or equivalent data folder)
Raw data exports and a normalized file used as input for the financial model.

- **Raw exports** — source data, do not modify.
- **Normalized data file** — the processed version that feeds into the financial model. Update this when a new export is brought in.

### `ProjectPlan/`
Home for the project plan. Update `Project_Plan.md` (or equivalent) whenever scope, timeline, or milestones change.
