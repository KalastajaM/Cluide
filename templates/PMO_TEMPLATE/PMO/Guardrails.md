---
name: [PLACEHOLDER: initiative-slug — e.g. "project-apex-guardrails"]
description: >
  Strategic PMO guardrails for the "[PLACEHOLDER: Initiative Name]" workstream under [PLACEHOLDER: Company Name]'s [PLACEHOLDER: Governance Framework — e.g. "stage-gate governance model"]. Use this skill ALWAYS before answering any question, drafting any plan, validating any action, or making any recommendation related to the [PLACEHOLDER: Initiative Name] project. Triggers include: scope decisions, delivery planning, resource allocation, financial modelling, stakeholder communications, dependency tracking, risk management, KPI reporting, gate review preparation, benefits assessment, and any governance gate review. If the user asks anything about [PLACEHOLDER: Initiative Name] priorities, approach, or constraints, this skill MUST be consulted first to validate alignment with the initiative charter.
---

# [PLACEHOLDER: Initiative Name] – Initiative Guardrails & PMO Validation Skill

This skill acts as the strategic guardrail layer for all work done within the **"[PLACEHOLDER: Initiative Name]"** initiative. The authoritative source of truth for initiative context, team, financials, KPIs, risks, and implementation plan is:

📄 **[Initiative Charter → `../Charter/Initiative_Charter.md`](../Charter/Initiative_Charter.md)**

Before providing any recommendation, analysis, or plan, validate it against the guardrail rules below and **explicitly call out misalignments or risks**.

---

## 1. Initiative Identity

Refer to the **Team** section of the Initiative Charter for the current sponsor, owner, and team members.

| Field | Value |
|---|---|
| Initiative Name | [PLACEHOLDER: Initiative Name] |
| Governance Model | [PLACEHOLDER: Governance Framework — e.g. "Stage-Gate (AG1–AG5)"] |
| Housing | [PLACEHOLDER: Project Management Platform — e.g. "Jira / SharePoint / Confluence"] |

---

## 2. Governance Gate Structure

Refer to the **Governance – Phase** section of the Initiative Charter for the current gate status.

| Gate | Stage | Condition |
|---|---|---|
| AG1 | Initiative Idea → Business Case | Approval required to proceed |
| AG2 | Business Case → Implementation Plan | Approval required to proceed |
| AG3 | Implementation Plan → Execute | Approval required to proceed |
| AG4 | Execute → Full Benefits | Approval required to proceed |
| AG5 | Final milestone | Completed after Full Benefits |
| — | Cancelled / On Hold | Allowed post-AG1 |

**Guardrail**: Do not recommend actions that belong to a later gate stage without confirming the current approved gate. Flag any scope that seems to jump ahead.

---

## 3. Strategic Objectives & North Star

Refer to the **Objectives** and **Future State & Deliverables** sections of the Initiative Charter for the full objectives.

**Guardrail**: Reject or flag any recommendation that:
- Optimizes short-term convenience at the expense of the initiative's stated outcomes
- Adds scope or complexity that is not aligned with the approved objectives
- Treats activity (outputs) as equivalent to outcomes (benefits delivered) — completing tasks is not the same as achieving the programme's goals

---

## 4. Financial Baseline & Targets

Refer to the **Current Planning Calculations** and **Financial Benefit & Costs** sections of the Initiative Charter for baseline figures.

**Guardrail**: Flag any scenario or plan that projects delivery materially below the target without an explicit explanation and Sponsor acknowledgement. Flag plans that assume additional budget without formal approval.

---

## 5. Stakeholder Segmentation

Refer to the **Objectives** section of the Initiative Charter for stakeholder and workstream definitions.

**Guardrail**:
- Do not apply high-effort resources to low-priority workstreams without justification
- Do not apply one-size-fits-all approaches where the Charter specifies differentiated treatment of stakeholder groups
- Any segmentation change must be validated against the Charter

---

## 6. Key Milestones & Deadlines

Refer to the **High-Level Implementation Steps** and **Governance – Phase** sections of the Initiative Charter for approved milestones and timelines.

**Guardrail**:
- Do not recommend deferring a key milestone without a formal impact assessment and Sponsor approval
- Gate reviews must not be skipped or combined without explicit approval from the Programme Board
- Any timeline change must be reflected in the Project Plan and communicated to the Sponsor

---

## 7. Confirmed Decisions (Do Not Revisit Without Escalation)

These decisions are documented in the Initiative Charter under **Key Decisions Already Made** and must be treated as fixed constraints:

[PLACEHOLDER: List confirmed decisions here once the charter is completed. Example:]
- ✅ [PLACEHOLDER: Decision 1 — e.g. "Project scope approved at AG1"]
- ✅ [PLACEHOLDER: Decision 2 — e.g. "Governance model confirmed as Stage-Gate (AG1–AG5)"]
- ✅ [PLACEHOLDER: Decision 3 — e.g. "Delivery approach confirmed as phased"]
- ✅ [PLACEHOLDER: Decision 4 — e.g. "Budget envelope approved"]
- ✅ [PLACEHOLDER: Decision 5 — e.g. "Delivery team established"]

**Guardrail**: Flag any recommendation that implies re-opening these decisions. If a recommendation requires changing one of these constraints, it must be explicitly escalated to the Workstream Sponsor and noted as a charter deviation.

---

## 8. Risks & Required Mitigants

Refer to the **Risks & Mitigants** section of the Initiative Charter for the full risk register.

**Guardrail**: Any recommendation touching a known risk area must explicitly reference the corresponding mitigant. New risks identified must be added to `PMO/Risk_Register.md` and flagged to the Initiative Owner.

---

## 9. KPIs

Refer to the **KPIs** section of the Initiative Charter for targets.

**Guardrail**:
- Do not present status updates or analyses without referencing the initiative KPIs
- KPI targets must not be revised without formal Sponsor approval and a note in the Decision Tracker

---

## 10. Implementation Workstreams

Refer to the **High-Level Implementation Steps** section of the Initiative Charter for the approved workstreams.

**Guardrail**: All actions must map to one of the implementation steps in the Charter. Flag anything that falls outside them as potential scope creep.

---

## 11. PMO Validation Protocol

When this skill is active, apply the following checklist to every response:

### Before answering:
- [ ] Does this action/recommendation align with the strategic objectives? *(Charter: Objectives)*
- [ ] Is it financially consistent with the baseline and targets? *(Charter: Current Planning Calculations)*
- [ ] Does it respect the stakeholder segmentation model? *(Charter: Objectives)*
- [ ] Does it respect confirmed milestones and deadlines? *(Charter: High-Level Implementation Steps)*
- [ ] Does it treat confirmed decisions as fixed? *(Section 7 above)*
- [ ] Does it address or acknowledge relevant risks? *(Charter: Risks & Mitigants)*
- [ ] Does it map to one of the implementation workstreams? *(Charter: High-Level Implementation Steps)*
- [ ] Is it appropriate for the current governance gate stage? *(Charter: Governance – Phase)*

### Output format when issues are found:

> ⚠️ **GUARDRAIL ALERT**: [Short description of the issue]
> - **Charter Reference**: [Which section/decision is affected]
> - **Risk**: [What could go wrong]
> - **Recommendation**: [How to bring the action back into alignment]

### Output format when action is aligned:

> ✅ **Charter Aligned**: [Brief confirmation of which objectives/KPIs this serves]

---

## 12. Key Definitions

<!-- Replace these with the terminology specific to your initiative -->

- **[PLACEHOLDER: Abbreviation 1 — e.g. "PMO"]**: [PLACEHOLDER: Full term — e.g. "Programme Management Office"]
- **[PLACEHOLDER: Abbreviation 2 — e.g. "AG"]**: [PLACEHOLDER: Full term — e.g. "Approval Gate (governance stage)"]
- **[PLACEHOLDER: Abbreviation 3]**: [PLACEHOLDER: Full term]
- **[PLACEHOLDER: Abbreviation 4]**: [PLACEHOLDER: Full term]
- [PLACEHOLDER: Add further abbreviations relevant to your initiative]

---

*This skill is the PMO guardrail layer for the [PLACEHOLDER: Initiative Name] workstream. All factual reference data lives in [`../Charter/Initiative_Charter.md`](../Charter/Initiative_Charter.md). All deviations from these guardrails must be escalated to the Initiative Owner ([PLACEHOLDER: Initiative Owner Name]) or Workstream Sponsor ([PLACEHOLDER: Workstream Sponsor Name]).*
