# Setup Prompt

Paste this prompt into a Claude conversation to set up the **Product Migration Initiative** workspace automatically.

---

You are being given a template to set up. Follow these steps exactly:

1. Read all template files provided in this message (they are pasted below, separated by `---FILE:---` markers).
2. For each `<<<PLACEHOLDER: ...>>>` you encounter, ask the user for the value. Collect ALL values before making any substitutions.
3. Once all values are collected, substitute every placeholder with the provided value across all files.
4. Output each completed file, clearly labelled, ready to save.

Start by listing every unique placeholder you found, grouped by file, and ask the user to provide values for each.

---

## Template files

---FILE: CLAUDE.md---

# Project Instructions: <<<PLACEHOLDER: Initiative ID — e.g. "VCP #8">>> – <<<PLACEHOLDER: Initiative Name — e.g. "Legacy-to-Cloud Migration">>>

## Before starting any task
Read `PROJECT_GUIDE.md` in this folder. It maps every folder and file in the project, tells you what is read-only vs. updatable, and is the authoritative guide for navigating this project.

## Rules — always apply these

**Archives:** Never read from or write to any folder whose name starts with `[ARCHIVE]`. Those are backups containing outdated information.

**Protected files:** Do not modify `Charter/Initiative_Charter.md` or `PMO/Guardrails.md` unless the user explicitly instructs you to.

**Financial model:** Whenever the financial model Excel is updated, also update `FinancialModel/Model_Summary.md`.


**Knowledge base:** Capture new insights, decisions, and findings in `PMO/Knowledge_Base.md`. This is the project's institutional memory — when in doubt about where to record something, put it here.

**Project plan:** Whenever project scope, timeline, milestones, or delivery approach changes, update `ProjectPlan/Project_Plan.md`.

**Action tracker:** Whenever new actions, owners, or due dates are identified or resolved, update `PMO/Action_Tracker.md`.

**Risk register:** Whenever new risks are identified or existing risks change in status, likelihood, or impact, update `PMO/Risk_Register.md`.

**Dependency register:** Whenever new dependencies between workstreams, teams, or systems are identified or resolved, update `PMO/Dependency_Register.md`.

---FILE: PROJECT_GUIDE.md---

# <<<PLACEHOLDER: Initiative ID>>> – <<<PLACEHOLDER: Initiative Name>>>: Project Guide

## Quick reference: What do you need to do?

| Task | Where to look | Where to update |
|---|---|---|
| Understand the project scope & goals | `Charter/Initiative_Charter.md` | ❌ Do not modify |
| Check project constraints & boundaries | `PMO/Guardrails.md` | ❌ Do not modify unless explicitly asked |
| Look up or record project knowledge/insights | `PMO/Knowledge_Base.md` | ✅ Append new insights here |
| View or update the programme risk register | `PMO/Risk_Register.md` | ✅ Update when risk status, likelihood, or impact changes |
| Track programme-level dependencies | `PMO/Dependency_Register.md` | ✅ Update when dependency status, target date, or priority changes |
| Understand the financial model | `FinancialModel/Model_Summary.md` | ✅ Update when the Excel model changes |

| Track open clarification, investigation, and decision actions | `PMO/Action_Tracker.md` | ✅ Update when actions are opened, progressed, or closed |
| Record or review programme decisions | `PMO/Decision_Tracker.md` | ✅ Update when decisions are made, revised, or superseded |

---FILE: Charter/Initiative_Charter.md---

# Initiative: <<<PLACEHOLDER: Initiative Name>>>

## Context

### Where We Are
- On-prem ACV is **<<<PLACEHOLDER: Starting ACV — e.g. "€10.1M">>>** at the start of <<<PLACEHOLDER: Initiative Start Year>>>, expected to fall to **<<<PLACEHOLDER: Target ACV End-of-Year>>>** by end of year
  - Budget assumes <<<PLACEHOLDER: Churn ACV>>> churn and <<<PLACEHOLDER: Migration Target ACV>>> conversion to <<<PLACEHOLDER: Cloud Platform Name>>>
- Gross margin is <<<PLACEHOLDER: Gross Margin % — e.g. "~85%">>>; Direct OpEx is <<<PLACEHOLDER: OpEx description — e.g. "small (minor R&D and some sales)">>>
- On-prem business is **non-core**; declining at approximately <<<PLACEHOLDER: Annual Churn Rate — e.g. "25%">>>
- Generates good cash flow; can provide ARR upside by migrating customers to cloud

### Key Decisions Already Made
- EOL announced **<<<PLACEHOLDER: EOL Date — Global>>>** (<<<PLACEHOLDER: Region with different EOL — e.g. "Japan">>>: <<<PLACEHOLDER: EOL Date — Region>>>; pursuing more aggressive approach)
- Maintaining <<<PLACEHOLDER: Legacy Product Name>>> blocks <<<PLACEHOLDER: Technical blocker description — e.g. "endpoint agent architecture changes">>> in the <<<PLACEHOLDER: Cloud Platform Name>>> portfolio
- <<<PLACEHOLDER: Migration Team Name>>> set up in **<<<PLACEHOLDER: Migration Team Start Date — e.g. "August 2025">>>** to do controlled migration directly with Resellers and Customers
  - Migrations are technically fast (though manual)
  - Customers need 3–6 months (governmental up to 9 months) for planning & execution
- Price increase (stick) of **<<<PLACEHOLDER: Price Increase % Range — e.g. "50%–100%">>>** planned for <<<PLACEHOLDER: Price Increase Date>>>

---

## Objectives

- **Net Revenue Retention** (targets <<<PLACEHOLDER: GRR Target>>> GRR / <<<PLACEHOLDER: NRR Target>>> NRR – to be confirmed) leading prioritization of conversion and/or upsell efforts
- Migrate <<<PLACEHOLDER: Legacy Product Name>>> on-prem business to cloud via **high-touch motion** through top <<<PLACEHOLDER: Top N Partners>>> partners
  - <<<PLACEHOLDER: High-Touch Baseline Date>>>: <<<PLACEHOLDER: High-Touch ACV>>> ACV; ~<<<PLACEHOLDER: High-Touch Customer Count>>> customers; avg <<<PLACEHOLDER: High-Touch Avg ACV>>> ACV
- Migrate <<<PLACEHOLDER: Legacy Product Name>>> on-prem business to cloud via **tech-touch motion** through rest of the resellers
  - <<<PLACEHOLDER: Tech-Touch Baseline Date>>>: <<<PLACEHOLDER: Tech-Touch ACV>>> ACV; ~<<<PLACEHOLDER: Tech-Touch Customer Count>>> customers; avg <<<PLACEHOLDER: Tech-Touch Avg ACV>>> ACV
- Reduce renewal churn; milk the remainder for as long as worth the opportunity cost

---

## Future State & Deliverables

- No active <<<PLACEHOLDER: Legacy Product Name>>> customers by end of <<<PLACEHOLDER: Final EOL Year>>>
- Optimized & lean support model for long-tail support extensions (if chosen)

---

## Team

| Role | Name |
|---|---|
| Workstream Sponsor | <<<PLACEHOLDER: Workstream Sponsor Name — e.g. "Morgan Smith">>> |
| Initiative Owner | <<<PLACEHOLDER: Initiative Owner Name — e.g. "Alex Jordan">>> |
| Internal Team | <<<PLACEHOLDER: Internal Team Members — e.g. "Sam Lee, Jordan Park, Casey Kim">>> |
| External Support | <<<PLACEHOLDER: External Consultant Name — e.g. "Robin Clarke">>> |

---

## Risks & Mitigants

| Risk | Mitigant |
|---|---|
| <<<PLACEHOLDER: Risk 1 — e.g. "Delay to EOL — may create technical blockers">>> | <<<PLACEHOLDER: Mitigant 1>>> |
| <<<PLACEHOLDER: Risk 2 — e.g. "Partner resistance — self-interest in legacy revenue">>> | <<<PLACEHOLDER: Mitigant 2>>> |
| <<<PLACEHOLDER: Risk 3 — e.g. "Non-migratable base unquantified">>> | <<<PLACEHOLDER: Mitigant 3>>> |
| <<<PLACEHOLDER: Risk 4 — e.g. "Incentive misalignment across sales team">>> | <<<PLACEHOLDER: Mitigant 4>>> |

---

## High-Level Implementation Steps

### Step 1 – Current State Assessment
- Collect feedback from <<<PLACEHOLDER: Migration Team Name>>> & other stakeholders on current state and ongoing activities
- Formalize a parallel <<<PLACEHOLDER: Legacy Product Name>>> & <<<PLACEHOLDER: Cloud Platform Name>>> usage policy
- Map non-migratable accounts; communicate cloud capability workarounds

### Step 2 – Finalize Migration Pack
- Plan the price increases (amount, upside, communication plan)
- Include carrot and stick offers in migration deck; Translations to <<<PLACEHOLDER: Required languages — e.g. "Finnish, Japanese, German, French">>>
- Business case calculator showing the full comparison of On-Prem vs Cloud
- Productize training, webinars, and trial configurations as scalable self-serve motion

### Step 3 – Redesign Organizational/Operational Plan
- Define who will drive migrations technically and who will do renewals per country
- Decide on the <<<PLACEHOLDER: Sales Incentive Program>>> structure to ensure incentives drive the right behaviour
- Plan and decide on potential extended support to extend revenue stream and reduce churn

### Step 4 – Partner Action Plans
- Build partner-specific action plans for the **top <<<PLACEHOLDER: Top N Partners>>> resellers**
- Leverage the <<<PLACEHOLDER: Year>>> <<<PLACEHOLDER: Partner Program Name>>> change: on-prem ACV no longer counts toward partner KPIs — use actively as a conversion incentive

---

## KPIs

| KPI | Target |
|---|---|
| Converted ACV% (by segment) | <<<PLACEHOLDER: Converted ACV % Target — e.g. "TBD (to be set at Business Case stage)">>> |
| # Customers remaining with <<<PLACEHOLDER: Legacy Product Name>>> (by segment) | <<<PLACEHOLDER: Remaining Customer Count Target>>> |
| Cost of R&D for <<<PLACEHOLDER: Legacy Product Name>>> | <<<PLACEHOLDER: R&D Cost Target — e.g. "€0">>> |
| Cost of Support for <<<PLACEHOLDER: Legacy Product Name>>> | <<<PLACEHOLDER: Support Cost Target — e.g. "€0">>> |

---

## Financial Benefit & Costs

### Financial Benefit
- Successful conversion of ACV at SaaS multiple (<<<PLACEHOLDER: SaaS Valuation Multiple — e.g. "3x">>>) vs. on-prem (<<<PLACEHOLDER: On-Prem Multiple — e.g. "0.8x">>>) represents a significant valuation uplift. Full business case to be developed at Business Case stage.

### One-Time Costs
- <<<PLACEHOLDER: One-time cost items — e.g. "Translations of migration materials">>>

### Running Costs
- <<<PLACEHOLDER: Running cost items — e.g. "Inside sales team; product maintenance until EOL">>>

---

## Current Planning Calculations

| Period | ACT <<<PLACEHOLDER: Year-2>>> | ACT <<<PLACEHOLDER: Year-1>>> | BUD <<<PLACEHOLDER: Current Year>>> |
|---|---|---|---|
| **<<<PLACEHOLDER: Legacy Product Name>>>** | <<<PLACEHOLDER: ACV Year-2>>> | <<<PLACEHOLDER: ACV Year-1>>> | <<<PLACEHOLDER: ACV Budget Year>>> |
| Migration | – | <<<PLACEHOLDER: Migration Year-1>>> | <<<PLACEHOLDER: Migration Budget>>> |
| Churn | – | <<<PLACEHOLDER: Churn Year-1>>> | <<<PLACEHOLDER: Churn Budget>>> |

---

## Governance – Phase

**Current Phase:** <<<PLACEHOLDER: Current Gate Phase — e.g. "Initiative Idea">>>

| Gate | Phase | Status |
|---|---|---|
| AG1 | Initiative Idea | <<<PLACEHOLDER: AG1 Status — e.g. "✅ In Progress">>> |
| AG2 | Business Case | <<<PLACEHOLDER: AG2 Status — e.g. "⬜ Pending">>> |
| AG3 | Implementation Plan | <<<PLACEHOLDER: AG3 Status>>> |
| AG4 | Execute | <<<PLACEHOLDER: AG4 Status>>> |
| AG5 | Full Benefits | <<<PLACEHOLDER: AG5 Status>>> |

---FILE END---

> **Note for very large files (PMO registers, Guardrails):** After collecting all placeholder values above, the user should pass those files as attachments or paste them separately. Apply the same substitutions to those files using the values already collected.
