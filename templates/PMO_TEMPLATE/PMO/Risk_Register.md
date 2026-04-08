# [PLACEHOLDER: Initiative Name] – Risk Register

**Owner:** [PLACEHOLDER: Initiative Owner Name] | **Sponsor:** [PLACEHOLDER: Workstream Sponsor Name]
**Last updated:** [PLACEHOLDER: YYYY-MM-DD] (rev 1 — initial template)
**Purpose:** Central, maintained register of risks to the [PLACEHOLDER: Legacy Product Name] → [PLACEHOLDER: Cloud Platform Name] migration programme. For narrative context and supporting evidence behind each risk, see `Knowledge_Base.md` and `Migrations/Product_Dependencies.md`. For programme-level dependencies that underpin these risks, see `Dependency_Register.md` — risk entries reference dependency IDs (D-xx) where applicable.

---

## Summary

| ID | Category | Risk | Likelihood | Impact | Status | Steerco |
|---|---|---|---|---|---|---|
| [R-01](#r-01) | Product | [PLACEHOLDER: Risk title — e.g. "Feature gap blocks enterprise migration"] | M | M | 🔴 Open | ⭐ Key |
| [R-02](#r-02) | Product | [PLACEHOLDER: Risk title — e.g. "Non-migratable accounts — air-gap / compliance constraints"] | H | H | 🔴 Open | ⭐ Key |
| [R-03](#r-03) | Commercial | [PLACEHOLDER: Risk title — e.g. "Specific segment churn not modelled"] | M | M | 🔴 Open | ⭐ Key |
| [R-04](#r-04) | Commercial | [PLACEHOLDER: Risk title — e.g. "Partner resistance — self-interest in legacy revenue"] | M | M | 🔴 Open | ⭐ Key |
| [R-05](#r-05) | Commercial | [PLACEHOLDER: Risk title — e.g. "Customer deferral — competing IT projects"] | H | M | 🟡 Monitoring | |
| [R-06](#r-06) | Financial | [PLACEHOLDER: Risk title — e.g. "Price increase delay"] | L | H | 🟡 Monitoring | |
| [R-07](#r-07) | Commercial | [PLACEHOLDER: Risk title — e.g. "Non-migratable base unquantified — GRR/NRR target set incorrectly"] | H | H | 🔴 Open | ⭐ Key |
| [R-08](#r-08) | Operational | [PLACEHOLDER: Risk title — e.g. "Sales incentive misalignment — no reward for conversion"] | H | H | 🔴 Open | ⭐ Key |
| [R-09](#r-09) | Operational | [PLACEHOLDER: Risk title — e.g. "Migration team capacity and geographic coverage gaps"] | H | H | 🔴 Open | ⭐ Key |
| [R-10](#r-10) | Financial | [PLACEHOLDER: Risk title — e.g. "Financial model reliability — data quality / assumption uncertainty"] | H | M | 🔴 Open | ⭐ Key |

---

## Rating scale

**Likelihood:** H = High (likely or already occurring) / M = Medium / L = Low
**Impact:** H = High (material effect on GRR/NRR target or programme outcome) / M = Medium / L = Low
**Status:** 🔴 Open / 🟡 Monitoring / 🟢 Mitigated / ⚫ Closed

**Update cadence:** Review at each programme milestone or when field intelligence changes a rating. Likelihood or impact moving to H must be escalated to [PLACEHOLDER: Initiative Owner Name] (Owner) and [PLACEHOLDER: Workstream Sponsor Name] (Sponsor).

---

## Product Risks

---

### R-01

**Category:** Product | **Likelihood:** M | **Impact:** M | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe the product risk. Example: "Elements lacks enterprise-grade RBAC. Accounts with multi-site admin requirements cannot migrate until asset grouping and policy delegation features are delivered in 2027."]

**Mitigation / Response:**
[PLACEHOLDER: Describe mitigation. Example: "Do not commit to migrating accounts with full RBAC requirements without disclosing the 2027 roadmap dependency. Qualify upfront whether the simpler SSO capability alone satisfies the customer's use case."]

**Linked dependencies:** [PLACEHOLDER: List linked D-xx dependency IDs from Dependency_Register.md — e.g. "[D-01](Dependency_Register.md#d-01)"]

---

### R-02

**Category:** Product | **Likelihood:** H | **Impact:** H | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe the non-migratable accounts risk. Example: "Fully air-gapped environments cannot connect to the cloud platform regardless of configuration. The extent of semi-air-gapped environments that could use a connector solution is not yet quantified."]

**Mitigation / Response:**
[PLACEHOLDER: Describe mitigation. Example: "Map air-gapped vs semi-air-gapped accounts. Communicate connector capabilities to affected segments. Adjust GRR/NRR denominator once non-migratable base is quantified."]

**Linked dependencies:** [PLACEHOLDER: e.g. "[D-02](Dependency_Register.md#d-02)"]

---

## Commercial Risks

---

### R-03

**Category:** Commercial | **Likelihood:** M | **Impact:** M | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe a segment-specific churn risk not captured in the financial model. Example: "EDU/GOV customers subject to tender cycles may churn at a materially higher rate than modelled. This segment's churn behaviour has not been stress-tested in the financial model."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Add EDU/GOV uplifted churn scenario to financial model. Qualify accounts in this segment early."]

**Linked dependencies:** [PLACEHOLDER: D-xx reference if applicable, or "None"]

---

### R-04

**Category:** Commercial | **Likelihood:** M | **Impact:** M | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Describe partner resistance risk. Example: "Some resellers sell on-prem hosting as a separate revenue stream and will resist migration to protect it. This affects a subset of high-touch partners."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Win-win-win approach: lower total spend for customer, partner recovers revenue via cloud ARR and margin, company retains ARR at a better multiple."]

**Linked dependencies:** [PLACEHOLDER: D-xx or "None"]

---

### R-05

**Category:** Commercial | **Likelihood:** H | **Impact:** M | **Status:** 🟡 Monitoring | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Describe customer deferral risk. Example: "Customers defer migration due to competing IT projects or budget cycles, causing slippage against conversion targets."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Increase urgency through price increase lever; proactive engagement by migration team with accounts showing deferral signals."]

**Linked dependencies:** [PLACEHOLDER: D-xx or "None"]

---

### R-07

**Category:** Commercial | **Likelihood:** H | **Impact:** H | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe the unquantified non-migratable base risk. Example: "Without estimating the non-migratable base (air-gapped, compliance-prohibited), GRR/NRR targets may be set against the wrong denominator, creating a false picture of programme performance."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Complete account mapping exercise. Do not finalize GRR/NRR targets until this base is quantified."]

**Linked dependencies:** [PLACEHOLDER: D-xx or "None"]

---

## Financial Risks

---

### R-06

**Category:** Financial | **Likelihood:** L | **Impact:** H | **Status:** 🟡 Monitoring | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Describe price increase delay risk. Example: "If the planned price increase is delayed beyond the target date, the primary 'stick' lever is removed, reducing urgency for customers and partners to migrate."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Maintain price increase as confirmed commitment; escalate immediately if commercial leadership signals delay."]

**Linked dependencies:** [PLACEHOLDER: e.g. "[D-05](Dependency_Register.md#d-05)"]

---

### R-10

**Category:** Financial | **Likelihood:** H | **Impact:** M | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe financial model reliability risk. Example: "Source data contains anomalies (credit notes, inactive accounts) that may distort ACV figures. Model assumptions have not been stress-tested against large-account concentration or segment-specific scenarios."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Clean data anomalies in source. Add customer concentration and segment stress-test scenarios to the model. Document all assumptions explicitly."]

**Linked dependencies:** [PLACEHOLDER: D-xx or "None"]

---

## Operational Risks

---

### R-08

**Category:** Operational | **Likelihood:** H | **Impact:** H | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe incentive misalignment risk. Example: "Sales compensation plans do not reward on-prem to cloud conversion. Local sales teams in non-migration-team-covered markets have no incentive to drive migrations."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Update sales incentive plan so that conversion counts as net new ARR. Extend migration team coverage or appoint local TSMs/SEs to drive conversions in uncovered markets."]

**Linked dependencies:** [PLACEHOLDER: e.g. "[D-04](Dependency_Register.md#d-04)"]

---

### R-09

**Category:** Operational | **Likelihood:** H | **Impact:** H | **Status:** 🔴 Open | **Owner:** [PLACEHOLDER: Risk Owner] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Risk:** ⭐ Yes

**Description:**
[PLACEHOLDER: Describe migration team capacity risk. Example: "The migration team is currently sized and structured for DACH and Japan only. Finland and other markets require local involvement. Without expanding coverage, the tech-touch volume cannot be handled at scale."]

**Mitigation / Response:**
[PLACEHOLDER: Mitigation — e.g. "Review operating model at AG3. Plan handoff of migration execution to local sales teams for tech-touch accounts."]

**Linked dependencies:** [PLACEHOLDER: D-xx or "None"]

---

## Change Log

| Rev | Date | Change |
|---|---|---|
| 1 | [PLACEHOLDER: YYYY-MM-DD] | Initial register created from template |
