---
name: [PLACEHOLDER: initiative-slug — e.g. "legacy-to-cloud-guardrails"]
description: >
  Strategic PMO guardrails for the "[PLACEHOLDER: Initiative Name]" workstream under [PLACEHOLDER: Company Name]'s [PLACEHOLDER: Governance Framework — e.g. "stage-gate governance model"]. Use this skill ALWAYS before answering any question, drafting any plan, validating any action, or making any recommendation related to the [PLACEHOLDER: Legacy Product Name] to [PLACEHOLDER: Cloud Platform Name] migration project. Triggers include: migration planning, partner strategy, pricing decisions, churn analysis, EOL timelines, incentives, product gaps, resourcing, KPI tracking, ARR/ACV calculations, segment analysis, customer mapping, migration team activities, and any governance gate review. If the user asks anything about [PLACEHOLDER: Legacy Product Name], [PLACEHOLDER: Cloud Platform Name], on-prem conversion, or this initiative, this skill MUST be consulted first to validate alignment with the initiative charter.
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
| Housing | [PLACEHOLDER: Project Management Platform — e.g. "Amplify / Jira"] |

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
- Optimizes short-term cash at the expense of ARR conversion rates
- Protects [PLACEHOLDER: Legacy Product Name] revenue in a way that delays or complicates migration
- Treats churn as equivalent to conversion — churn does not count as migration success

---

## 4. Financial Baseline & Targets

Refer to the **Current Planning Calculations** and **Financial Benefit & Costs** sections of the Initiative Charter for baseline figures.

**Guardrail**: Flag any scenario or plan that projects current-year migration materially below the conversion target without an explicit explanation of why the target should be revised. Flag plans that assume churn will cover the gap.

---

## 5. Customer Segmentation

Refer to the **Objectives** section of the Initiative Charter for high-touch and tech-touch segment definitions, ACV, and customer counts.

**Guardrail**:
- Do not apply high-touch resources to low-ACV tech-touch accounts without justification (ROI test required)
- Do not apply tech-touch-only approaches to top [PLACEHOLDER: Top N Partners] partners — they require personalized engagement
- Any segmentation change must be validated against the baselines in the Charter

---

## 6. EOL Timeline & Price Increase

Refer to the **Key Decisions Already Made** section of the Initiative Charter for EOL dates and price increase parameters.

**Guardrail**:
- Do not recommend delaying the EOL date without a formal financial feasibility analysis and explicit acknowledgment that delay may create technical blockers in the [PLACEHOLDER: Cloud Platform Name] portfolio
- [PLACEHOLDER: Region with different EOL]-specific plans must be more aggressive than global plans, not less
- The price increase must be treated as a confirmed lever — do not deprioritize or defer it without flagging

---

## 7. Confirmed Decisions (Do Not Revisit Without Escalation)

These decisions are documented in the Initiative Charter under **Key Decisions Already Made** and must be treated as fixed constraints:

- ✅ EOL announced to partners ([PLACEHOLDER: EOL Date — Global] globally; [PLACEHOLDER: EOL Date — Region] for [PLACEHOLDER: Region with different EOL])
- ✅ [PLACEHOLDER: Migration Team Name] operational since [PLACEHOLDER: Migration Team Start Date]
- ✅ Migrations are technically fast but manual; customers need 3–6 months planning (gov: up to 9 months)
- ✅ Price increase of [PLACEHOLDER: Price Increase % Range] planned for [PLACEHOLDER: Price Increase Date]
- ✅ On-prem ACV will **no longer count toward partner KPIs** in [PLACEHOLDER: Year] [PLACEHOLDER: Partner Program Name] — structural conversion incentive to be used actively

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
- GRR/NRR targets must not be finalized until the non-migratable customer base is quantified

---

## 10. Implementation Workstreams

Refer to the **High-Level Implementation Steps** section of the Initiative Charter for the four workstreams.

**Guardrail**: All actions must map to one of the four implementation steps in the Charter. Flag anything that falls outside them as potential scope creep.

---

## 11. PMO Validation Protocol

When this skill is active, apply the following checklist to every response:

### Before answering:
- [ ] Does this action/recommendation align with the strategic objectives? *(Charter: Objectives)*
- [ ] Is it financially consistent with the baseline and targets? *(Charter: Current Planning Calculations)*
- [ ] Does it respect the segmentation model? *(Charter: Objectives – high-touch / tech-touch)*
- [ ] Does it respect EOL dates and the price increase lever? *(Charter: Key Decisions Already Made)*
- [ ] Does it treat confirmed decisions as fixed? *(Section 7 above)*
- [ ] Does it address or acknowledge relevant risks? *(Charter: Risks & Mitigants)*
- [ ] Does it map to one of the four implementation workstreams? *(Charter: High-Level Implementation Steps)*
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

- **ACV**: Annual Contract Value (on-prem subscription revenue)
- **ARR**: Annual Recurring Revenue (cloud subscription revenue)
- **[PLACEHOLDER: Legacy Product Abbreviation — e.g. "BS"]**: [PLACEHOLDER: Legacy Product Name] (on-prem product, going EOL)
- **[PLACEHOLDER: Cloud Platform Abbreviation — e.g. "Elements"]**: [PLACEHOLDER: Cloud Platform Name] (cloud platform; migration target)
- **[PLACEHOLDER: Migration Team Abbreviation — e.g. "ESS"]**: [PLACEHOLDER: Migration Team Name]
- **[PLACEHOLDER: Sales Incentive Abbreviation — e.g. "SIP"]**: [PLACEHOLDER: Sales Incentive Program]
- **[PLACEHOLDER: Partner Program Abbreviation — e.g. "GPP"]**: [PLACEHOLDER: Partner Program Name]
- **GRR**: Gross Revenue Retention
- **NRR**: Net Revenue Retention
- **Top [PLACEHOLDER: Top N Partners]**: The [PLACEHOLDER: Top N Partners] highest-ACV reseller partners ([PLACEHOLDER: High-Touch ACV] ACV as of [PLACEHOLDER: High-Touch Baseline Date])
- [PLACEHOLDER: Add further abbreviations relevant to your initiative]

---

*This skill is the PMO guardrail layer for the [PLACEHOLDER: Initiative Name] workstream. All factual reference data lives in [`../Charter/Initiative_Charter.md`](../Charter/Initiative_Charter.md). All deviations from these guardrails must be escalated to the Initiative Owner ([PLACEHOLDER: Initiative Owner Name]) or Workstream Sponsor ([PLACEHOLDER: Workstream Sponsor Name]).*
