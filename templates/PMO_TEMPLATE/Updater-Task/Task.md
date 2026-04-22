# Update Task: Cross-reference audit for PMO registers

**Purpose:** Keep the four programme registers and the knowledge base internally consistent — no orphaned IDs, no missing back-links, no legacy ID formats. Run this after a heavy editing session, or on a regular cadence (e.g. weekly).

This task operationalises the **Cross-reference consistency** rules already prescribed in `CLAUDE.md`. Nothing new is being enforced — the task just makes the audit explicit and repeatable.

---

## Files in scope

| File | Role |
|---|---|
| `PMO/Risk_Register.md` | Risks (`R-##`) |
| `PMO/Dependency_Register.md` | Dependencies (`D-##`) |
| `PMO/Action_Tracker.md` | Actions (`ACT-<Cat>-##` where `Cat` ∈ P/C/F/O/D/PJ) |
| `PMO/Decision_Tracker.md` | Decisions (`DEC-##`) |
| `PMO/Knowledge_Base.md` | Knowledge-base sections (`KB §#`) |

**Do not touch** anything under a folder whose name starts with `[ARCHIVE]`. **Do not modify** `Charter/Initiative_Charter.md` or `PMO/Guardrails.md` unless the user explicitly asks.

---

## Step 1 — Read the files in full

Read all five files listed above before making any changes. You need the complete picture of every ID, every cross-reference, and every anchor target before you can decide what's consistent and what isn't.

---

## Step 2 — Check bidirectional links

For every cross-reference, confirm the link exists on **both** sides:

- **Risk ↔ Action:** every `R-##` that lists a mitigating `ACT-##` must appear as the source in that action's entry, and vice versa.
- **Risk ↔ Dependency:** every `R-##` that cites a driving `D-##` must appear in that dependency's "linked risks" field, and vice versa.
- **Dependency ↔ Action:** every `D-##` that lists a tracking `ACT-##` must appear as the source in that action's entry, and vice versa.
- **Decision ↔ Action / Risk:** every `DEC-##` that closes or changes the status of a linked item must reference that item, and the item must reference the decision back.
- **KB ↔ Register entry:** every `KB §#` reference on a risk, dependency, action, or decision must point to a real section in `Knowledge_Base.md`.

Flag every case where one side links and the other does not.

---

## Step 3 — Check every anchor target exists

For every `R-##`, `D-##`, `ACT-<Cat>-##`, `DEC-##`, and `KB §#` reference found anywhere in the five files, confirm the target entry actually exists. Flag any reference that points to a non-existent ID.

---

## Step 4 — Check ID-format compliance

Confirm all IDs follow the standard format:

- Risks: `R-##` (e.g. `R-01`)
- Dependencies: `D-##`
- Actions: `ACT-<Cat>-##` with `Cat` ∈ P / C / F / O / D / PJ (e.g. `ACT-PJ-03`, `ACT-F-12`)
- Decisions: `DEC-##`
- KB sections: `KB §#`

Flag any legacy or one-off formats (e.g. bare `A-2`, `S-1`, `PM-2`, or actions without a category letter). These must be migrated to the standard format.

---

## Step 5 — Report, then fix

Before editing, produce a short report of all findings from Steps 2–4, grouped by file. Let the user confirm scope if any of the fixes look material (e.g. an ID migration that changes many references).

Then apply the corrections. When you touch a file:

- Add the missing back-link, fix the broken target, or rewrite the non-standard ID.
- Keep the actual **content** of entries unchanged unless the fix requires it — this is a consistency audit, not a rewrite.

---

## Step 6 — Bump revs and log

For every file you modified:

- Update the `**Last updated:**` header (bump the rev number and set today's date).
- Append a short change-log entry at the bottom describing what was fixed and why (e.g. "Added missing R-04 → ACT-F-02 back-link; migrated legacy `A-3` references to `ACT-PJ-03`").

---

## Notes

- This task does **not** update HTML render files — the template ships Markdown only. If you add HTML views later, extend this task with MD→HTML sync steps.
- If a fix reveals a missing Risk, Dependency, or Action that the registers genuinely don't yet track (not just a broken link), surface it in the report and ask the user before creating a new entry — that's a scope change, not an audit fix.
