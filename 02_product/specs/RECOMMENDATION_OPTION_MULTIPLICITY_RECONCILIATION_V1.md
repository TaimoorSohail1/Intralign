# Recommendation Option Multiplicity Reconciliation v1

**Type:** Architecture reconciliation (ratified) — authoritative resolution of **AMB-1**
**Status:** Active Release 1 · **Date:** 2026-05-31
**Resolves:** AMB-1 (`RELEASE_1_ARCHITECTURE_CONSISTENCY_AUDIT_001.md` / `_002.md`).
**Companion / consolidates:** `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md` (the owner decision; same ratified outcome). This document is the audit-named, authoritative reconciliation record; the two are consistent and non-conflicting.

> Scope: resolve **only** the Finding ↔ Recommendation ↔ Possible Resolution Paths multiplicity. No doctrine, no governance, no execution, no new objects.

---

## 1. Ratified Decision

**Possible Resolution Paths are NOT a first-class reasoning object in Release 1.** They are a **user-facing presentation pattern over multiple Recommendations associated with the same Finding.**

**Canonical model:**
```text
Finding
  → Recommendation A
  → Recommendation B
  → Recommendation C
```
A UI may render those Recommendations using the labels **OSLO Recommended · Possible Resolution Paths · Selected Path** — but these are **presentation labels only**.

---

## 2. Required Conclusions

1. **Recommendation remains the canonical advisory object** — it owns rationale, finding attribution, affected CAF dimensions, expected impact, explainability, lifecycle, supersession, and prioritization.
2. **Possible Resolution Paths are a view/grouping of Recommendations** — the UI grouping of the multiple Recommendations for a Finding; they own no reasoning, lifecycle, attribution, or assessment influence.
3. **`resolution_paths[]`, `is_recommended`, and `is_selected` are removed as modeled substructure fields.** *(Applied — Recommendation System Spec §4.)*
4. **No Resolution Path entity, lifecycle, event, or API resource is created.** The API exposes **Recommendations only**.
5. **Future-Architecture Resolution Candidate (governance) remains untouched** and is not reclassified.
6. **Recommendation System Spec updated accordingly.** *(Applied — §4 rewritten as a UI presentation pattern; §11b marked resolved; Revision 3.)*
7. **`RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` retired/superseded.** *(Applied — retirement banner.)*
8. **Resolution Paths v1.2 application work removed from the reconciliation backlog** — no `resolution_paths` Data Model field, no State/Event/API/UI resolution-path application; that work is **withdrawn**.
9. **Desired UX preserved as a UI rendering pattern** — **OSLO Recommended** (the primary Recommendation, derived from prioritization §7), **Possible Resolution Paths** (the grouped Recommendations for a Finding), **Selected Path** (the Recommendation the user accepted, derived from lifecycle §8). All **derived, not persisted**.

---

## 3. Application Status

| Conclusion | Status |
|---|---|
| 3 — remove modeled fields | ✅ Applied (Recommendation System Spec §4) |
| 6 — update Recommendation System Spec | ✅ Applied (§4 + §11b + Revision 3) |
| 7 — retire Resolution Paths Spec | ✅ Applied (retirement banner) |
| 8 — withdraw v1.2 application | ✅ Recorded (backlog item withdrawn) |
| 1, 2, 4, 5, 9 | ✅ Established by this decision |

No further edits to canonical Data/State/Event/API/UI artifacts are required (none ever contained `resolution_paths` — confirmed in Audit 002). UI/API specs simply render/expose **Recommendations**; the three labels are applied at the UI layer when the recommendations surface is detailed.

---

## 4. Reconciliation-Backlog Effect

| Item | Effect |
|---|---|
| **AMB-1** | **Resolved** (this decision) |
| Resolution-Path Data Model v1.2 + State/Event/API/UI application | **Withdrawn** — not needed |
| Recommendation System Spec §11b (alternative paths) | **Resolved** — alternatives = multiple Recommendations |
| RS-R5 / RS-R6 (Recommendation↔Finding cardinality) | **Independent** — remain in the Recommendation reconciliation backlog (not resolution-path-specific) |
| RS-R1/R2/R3/R4/R7 (recommendation type/lifecycle/fields) | **Unaffected** — remain in backlog |

---

## 5. Validation

- **No ontology expansion** — ✅ (no concept added; an over-modeled one removed)
- **No new object** — ✅ (no Resolution Path entity)
- **No new lifecycle** — ✅ (Recommendation lifecycle only)
- **No new event** — ✅ (no resolution-path events)
- **No CAF/Reliability/Confidence behavior changes** — ✅ (selection = accepting a Recommendation; assessment changes only via reanalysis)
- **No governance / Future-Architecture leakage** — ✅ (Resolution Candidate and Governance Domain untouched)

---

*This reconciliation resolves AMB-1 by ratifying that Possible Resolution Paths are a UI presentation pattern over multiple Recommendations per Finding — not a modeled construct. Recommendation remains the sole advisory object; the resolution-path substructure and its spec are retired; the v1.2 application is withdrawn; the UX is preserved as derived UI labels; and Future Architecture is untouched. Consistent with, and consolidating, `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md`.*

**Recommendation Option Multiplicity Reconciliation v1 complete.**
