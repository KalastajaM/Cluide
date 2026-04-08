# [PLACEHOLDER: Initiative Name] – Dependency Register

**Owner:** [PLACEHOLDER: Initiative Owner Name] | **Sponsor:** [PLACEHOLDER: Workstream Sponsor Name]
**Last updated:** [PLACEHOLDER: YYYY-MM-DD] (rev 1 — initial template)
**Purpose:** Programme-level register of internal and external dependencies — things the [PLACEHOLDER: Legacy Product Name] → [PLACEHOLDER: Cloud Platform Name] workstream relies on (from R&D, commercial, operational, partner, or external sources) to achieve its objectives. This is the single source of truth for dependency tracking. The Risk Register (`Risk_Register.md`) references dependency IDs (D-xx) where a missed dependency drives a risk. Product-level migration blockers and feature-level open actions are in `Migrations/Product_Dependencies.md`.

---

## Summary

| ID | Description | Type | Priority | Status | Target date | Steerco |
|---|---|---|---|---|---|---|
| [D-01](#d-01) | [PLACEHOLDER: Dependency — e.g. "RBAC / Identity: SSO integration feature"] | Internal | H | 🔴 Open | [PLACEHOLDER: Target date] | ⭐ Key |
| [D-02](#d-02) | [PLACEHOLDER: Dependency — e.g. "RBAC / Delegation: asset grouping and policy delegation"] | Internal | H | 🔴 Open | [PLACEHOLDER: Target date] | ⭐ Key |
| [D-03](#d-03) | [PLACEHOLDER: Dependency — e.g. "Air-gap / connectivity solution"] | Internal | H | 🟡 Monitoring | [PLACEHOLDER: Target date] | ⭐ Key |
| [D-04](#d-04) | [PLACEHOLDER: Dependency — e.g. "Sales incentive plan update — conversion counts as new ARR"] | Internal | H | 🔴 Open | [PLACEHOLDER: Target date] | ⭐ Key |
| [D-05](#d-05) | [PLACEHOLDER: Dependency — e.g. "Price increase execution"] | Internal | H | 🟡 Monitoring | [PLACEHOLDER: Price Increase Date] | ⭐ Key |
| [D-06](#d-06) | [PLACEHOLDER: Dependency — e.g. "Parallel running policy formal documentation"] | Internal | H | 🔴 Open | [PLACEHOLDER: Target date] | ⭐ Key |
| [D-07](#d-07) | [PLACEHOLDER: Dependency — e.g. "CRM data quality for tech-touch motion"] | Internal | M | 🔴 Open | [PLACEHOLDER: Target date] | |
| [D-08](#d-08) | [PLACEHOLDER: Dependency — e.g. "Partner engagement protocol — direct customer access agreement"] | External | M | 🔴 Open | [PLACEHOLDER: Target date] | |
| [D-09](#d-09) | [PLACEHOLDER: Dependency — e.g. "Regulatory cloud prohibition scope clarification"] | External | M | 🟡 Monitoring | Ongoing | |

---

## Rating scale

**Type:** Internal = dependency on your organisation's teams or processes / External = dependency on partners, customers, vendors, or regulatory environment

**Priority:** H = high impact AND/OR low delivery confidence / M = significant friction if missed / L = low impact AND high delivery confidence

**Status:** 🔴 Open (no mitigation in place) / 🟡 Monitoring (in progress, being tracked) / 🟢 Resolved / ⚫ N/A or superseded

**Update cadence:** Review at each programme milestone. Status moving to 🔴, or a target date slipping, must be escalated to [PLACEHOLDER: Initiative Owner Name] (Owner) and [PLACEHOLDER: Workstream Sponsor Name] (Sponsor).

---

## Internal Dependencies

---

### D-01

**Type:** Internal | **Category:** Product – [PLACEHOLDER: e.g. "RBAC / Identity"] | **Priority:** H | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: Team — e.g. "R&D / Product"] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "Cloud platform portal access governed by an enterprise identity provider (e.g. Entra ID / Okta) rather than a separate platform-managed user directory. This is the minimum identity/SSO capability needed for enterprise accounts. Qualification is needed to determine whether this alone satisfies delegation use cases before classifying accounts as fully blocked."]

**Action / next step:**
[PLACEHOLDER: Next step — e.g. "Confirm delivery date. Validate whether this capability alone satisfies delegation requirements raised by key accounts."]

**Linked risks:** [PLACEHOLDER: R-xx reference — e.g. "R-01"]

---

### D-02

**Type:** Internal | **Category:** Product – [PLACEHOLDER: e.g. "RBAC / Delegation"] | **Priority:** H | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: Team] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "Asset grouping and policy delegation to groups. Required for multi-site enterprise accounts where different admins need scoped access to their own device groups and policy sets. Not on roadmap until 2027."]

**Action / next step:**
[PLACEHOLDER: Next step]

**Linked risks:** [PLACEHOLDER: R-xx]

---

### D-03

**Type:** Internal | **Category:** Product – [PLACEHOLDER: e.g. "Connectivity / Air-Gap"] | **Priority:** H | **Status:** 🟡 Monitoring | **Depends on:** [PLACEHOLDER: Team] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "A connector agent or proxy capability that allows semi-air-gapped environments to connect to the cloud platform without full internet exposure. Fully air-gapped environments confirmed non-migratable; this dependency covers the semi-air-gapped segment."]

**Action / next step:**
[PLACEHOLDER: Next step]

**Linked risks:** [PLACEHOLDER: R-xx]

---

### D-04

**Type:** Internal | **Category:** Commercial – [PLACEHOLDER: e.g. "Sales Incentive Plan"] | **Priority:** H | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: Team — e.g. "Commercial / HR"] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "Update to the sales incentive plan so that on-prem to cloud conversion counts as net new ARR for commission purposes. Without this, local sales teams have no financial incentive to drive migrations."]

**Action / next step:**
[PLACEHOLDER: Next step]

**Linked risks:** [PLACEHOLDER: R-xx — e.g. "R-08"]

---

### D-05

**Type:** Internal | **Category:** Commercial – [PLACEHOLDER: e.g. "Price Increase"] | **Priority:** H | **Status:** 🟡 Monitoring | **Depends on:** [PLACEHOLDER: Team — e.g. "Commercial leadership"] | **Target date:** [PLACEHOLDER: Price Increase Date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "Execution of the planned on-prem price increase. This is the primary 'stick' lever to create urgency for customers to migrate. Any delay reduces urgency across the customer base."]

**Action / next step:**
[PLACEHOLDER: Next step — e.g. "Monitor commercial approval timeline. Confirm communication plan."]

**Linked risks:** [PLACEHOLDER: R-xx — e.g. "R-06"]

---

### D-06

**Type:** Internal | **Category:** Operational – [PLACEHOLDER: e.g. "Policy"] | **Priority:** H | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: Team — e.g. "PMO / Legal"] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD] | **Key Dependency:** ⭐ Yes

**Description:**
[PLACEHOLDER: Full description. Example: "Formal documentation of the parallel running policy — the approved window during which customers may run both legacy and cloud products simultaneously. Needed before the migration pack can be finalized and distributed."]

**Action / next step:**
[PLACEHOLDER: Next step]

**Linked risks:** [PLACEHOLDER: R-xx or "None"]

---

### D-07

**Type:** Internal | **Category:** Operational – [PLACEHOLDER: e.g. "Data / CRM"] | **Priority:** M | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: Team — e.g. "Revenue Operations / Sales Excellence"] | **Target date:** [PLACEHOLDER: Target date] | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Full description. Example: "Minimum CRM data fields (account status, product version, renewal date, reseller ID) must be populated and validated before a tech-touch or AI-assisted outreach motion can be launched at scale."]

**Action / next step:**
[PLACEHOLDER: Next step]

**Linked risks:** [PLACEHOLDER: R-xx or "None"]

---

## External Dependencies

---

### D-08

**Type:** External | **Category:** Partner – [PLACEHOLDER: e.g. "Engagement Protocol"] | **Priority:** M | **Status:** 🔴 Open | **Depends on:** [PLACEHOLDER: External party — e.g. "Reseller partners"] | **Target date:** As cases arise | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Full description. Example: "Some reseller contracts require partner consent before the vendor can contact end customers directly. This dependency arises case-by-case and must be managed proactively with the top resellers."]

**Action / next step:**
[PLACEHOLDER: Next step — e.g. "Clarify partner agreement terms for top N resellers. Establish a standard protocol for direct customer contact requests."]

**Linked risks:** [PLACEHOLDER: R-xx or "None"]

---

### D-09

**Type:** External | **Category:** Regulatory – [PLACEHOLDER: e.g. "Cloud Prohibition Scope"] | **Priority:** M | **Status:** 🟡 Monitoring | **Depends on:** [PLACEHOLDER: External party — e.g. "Regulatory authority / Legal"] | **Target date:** Ongoing | **Date added:** [PLACEHOLDER: YYYY-MM-DD]

**Description:**
[PLACEHOLDER: Full description. Example: "Certain regulatory frameworks (e.g. classified data handling requirements) may prohibit specific customer types from moving to public cloud. The scope and size of this population is not yet fully quantified."]

**Action / next step:**
[PLACEHOLDER: Next step — e.g. "Map accounts in regulated sectors. Consult legal on which regulatory prohibitions apply and whether private cloud or connector options provide compliant pathways."]

**Linked risks:** [PLACEHOLDER: R-xx — e.g. "R-07"]

---

## Change Log

| Rev | Date | Change |
|---|---|---|
| 1 | [PLACEHOLDER: YYYY-MM-DD] | Initial register created from template |
