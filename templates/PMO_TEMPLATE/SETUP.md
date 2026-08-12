# Setup Prompt

Paste this prompt into a Claude conversation to set up the **PMO Project** workspace automatically.

---

You are being given a template to set up. Follow these steps exactly:

1. Read all template files provided in this message (they are pasted below, separated by `---FILE:---` markers).
2. For each `<<<PLACEHOLDER: ...>>>` in the embedded template files below, ask the user for the value. (The files copied from the template folder — `CLAUDE.md`, `PROJECT_GUIDE.md`, `project.md` — use single-bracket `[PLACEHOLDER: ...]` markers instead; customize those in the copies, not here.) Collect ALL values before making any substitutions.
3. Once all values are collected, substitute every placeholder with the provided value across all files.
4. Output each completed file, clearly labelled, ready to save.

Start by listing every unique placeholder you found, grouped by file, and ask the user to provide values for each.

---

## Template files

---FILE: CLAUDE.md and PROJECT_GUIDE.md---

These two files are **not** embedded here. Copy `CLAUDE.md` and `PROJECT_GUIDE.md` from this template folder as-is, then customize the placeholders (`[PLACEHOLDER: ...]`) in the copies using the values collected above. The template files themselves are the single source of truth — do not maintain a second copy of their content in this prompt.

`project.md` is likewise not embedded: it holds the app-side project description/instructions text (the Guide 25 layer). Copy it, customize its `[PLACEHOLDER: ...]` fields with the values collected above, and paste the result into the Cowork project's description/instructions fields in the app.

---FILE: Charter/Initiative_Charter.md---

# Initiative: <<<PLACEHOLDER: Initiative Name — e.g. "Project Apex">>>

## Context

### Where We Are
- <<<PLACEHOLDER: Describe the current state. Example: "The organisation currently operates a manual reporting process that is resource-intensive and error-prone.">>>
- <<<PLACEHOLDER: Describe the key driver or problem. Example: "This creates significant operational risk, with an estimated cost of [amount] per year in rework and corrections.">>>
- <<<PLACEHOLDER: Describe any time pressure or opportunity. Example: "A window of opportunity exists to address this now because a planned system upgrade in Q3 provides a natural integration point.">>>

### Key Decisions Already Made
- <<<PLACEHOLDER: Decision 1 — e.g. "Programme scope formally approved at Gate 1">>>
- <<<PLACEHOLDER: Decision 2 — e.g. "Delivery approach confirmed: phased over three quarters">>>
- <<<PLACEHOLDER: Decision 3 — e.g. "Budget envelope approved by Finance">>>
- <<<PLACEHOLDER: Decision 4 — e.g. "Delivery team established in [Month Year]">>>

---

## Objectives

- <<<PLACEHOLDER: Primary objective — e.g. "Deliver a fully operational reporting solution by end of Q3, within the approved budget and scope">>>
- <<<PLACEHOLDER: Secondary objective — e.g. "Achieve a 20% reduction in manual reporting effort within 6 months of go-live">>>
- <<<PLACEHOLDER: Third objective — e.g. "Ensure adoption across all 8 affected teams by end of year">>>

---

## Future State & Deliverables

- <<<PLACEHOLDER: Describe the target end state. Example: "All 8 teams operating on the new reporting solution by end of year">>>
- <<<PLACEHOLDER: Describe key deliverables. Example: "Documented operating model, trained users, decommissioned legacy tooling, and a validated benefits report">>>

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
| <<<PLACEHOLDER: Risk 1 — e.g. "Scope creep — requirements expand beyond agreed boundaries">>> | <<<PLACEHOLDER: Mitigant 1 — e.g. "Enforce formal change control; Sponsor approval required for any scope change">>> |
| <<<PLACEHOLDER: Risk 2 — e.g. "Key resource unavailability at peak delivery phase">>> | <<<PLACEHOLDER: Mitigant 2 — e.g. "Identify cover arrangements; document specialist knowledge">>> |
| <<<PLACEHOLDER: Risk 3 — e.g. "Stakeholder misalignment across sponsoring teams">>> | <<<PLACEHOLDER: Mitigant 3 — e.g. "Structured alignment session before Gate 2; document agreed positions">>> |
| <<<PLACEHOLDER: Risk 4 — e.g. "Third-party vendor misses critical delivery milestone">>> | <<<PLACEHOLDER: Mitigant 4 — e.g. "Obtain formal delivery schedule; agree escalation triggers">>> |

---

## High-Level Implementation Steps

### Step 1 – Discovery & Current State Assessment
- <<<PLACEHOLDER: Key activity — e.g. "Gather requirements and baseline metrics from key stakeholders">>>
- <<<PLACEHOLDER: Key activity — e.g. "Map current-state process — identify gaps, pain points, and constraints">>>
- <<<PLACEHOLDER: Key activity — e.g. "Quantify the problem and validate the business case assumptions">>>

### Step 2 – Business Case & Planning
- <<<PLACEHOLDER: Key activity — e.g. "Develop and validate the full business case">>>
- <<<PLACEHOLDER: Key activity — e.g. "Define the detailed delivery plan — milestones, dependencies, resourcing">>>
- <<<PLACEHOLDER: Key activity — e.g. "Obtain Gate 2 approval before proceeding to implementation">>>

### Step 3 – Implementation & Execution
- <<<PLACEHOLDER: Key activity — e.g. "Build, test, and pilot the solution with an initial team">>>
- <<<PLACEHOLDER: Key activity — e.g. "Resolve issues from the pilot before full rollout">>>
- <<<PLACEHOLDER: Key activity — e.g. "Execute full rollout and manage change / communications">>>

### Step 4 – Benefits Realisation & Close
- <<<PLACEHOLDER: Key activity — e.g. "Measure outcomes against baseline metrics and KPI targets">>>
- <<<PLACEHOLDER: Key activity — e.g. "Conduct a post-implementation review and document lessons learned">>>
- <<<PLACEHOLDER: Key activity — e.g. "Obtain final gate sign-off on benefits delivery">>>

---

## KPIs

| KPI | Target |
|---|---|
| <<<PLACEHOLDER: KPI 1 — e.g. "% of milestones delivered on time">>> | <<<PLACEHOLDER: Target — e.g. "≥ 90%">>> |
| <<<PLACEHOLDER: KPI 2 — e.g. "Budget variance">>> | <<<PLACEHOLDER: Target — e.g. "≤ 5% overrun">>> |
| <<<PLACEHOLDER: KPI 3 — e.g. "User adoption rate at 3 months post-go-live">>> | <<<PLACEHOLDER: Target — e.g. "≥ 80%">>> |
| <<<PLACEHOLDER: KPI 4 — e.g. "Target benefit delivered">>> | <<<PLACEHOLDER: Target — e.g. "TBD at Business Case stage">>> |

---

## Financial Benefit & Costs

### Financial Benefit
- <<<PLACEHOLDER: Describe expected benefit. Example: "Successful delivery is expected to yield [benefit — e.g. a reduction of £X in annual operating costs]. Full business case to be developed at Gate 2.">>>

### One-Time Costs
- <<<PLACEHOLDER: One-time cost items — e.g. "External advisor fees; tooling setup; training development">>>

### Running Costs
- <<<PLACEHOLDER: Running cost items — e.g. "Ongoing licence fees; internal support team time">>>

---

## Governance – Phase

**Current Phase:** <<<PLACEHOLDER: Current Gate Phase — e.g. "Concept">>>

| Gate | Phase | Status |
|---|---|---|
| Gate 1 | <<<PLACEHOLDER: Gate 1 name>>> | <<<PLACEHOLDER: Gate 1 Status — e.g. "✅ In Progress">>> |
| Gate 2 | Business Case | <<<PLACEHOLDER: Gate 2 Status — e.g. "⬜ Pending">>> |
| Gate 3 | Implementation Plan | <<<PLACEHOLDER: Gate 3 Status>>> |
| Gate 4 | Execute | <<<PLACEHOLDER: Gate 4 Status>>> |
| Gate 5 | <<<PLACEHOLDER: Gate 5 name>>> | <<<PLACEHOLDER: Gate 5 Status>>> |

---FILE END---

> **Note for very large files (PMO registers, Guardrails):** After collecting all placeholder values above, the user should pass those files as attachments or paste them separately. Apply the same substitutions to those files using the values already collected.
