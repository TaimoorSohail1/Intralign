# Recommendation / Resolution Paths Reconciliation Decision 001

**Type:** Architecture reconciliation review & owner decision (ratified)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Subject:** Resolution of **AMB-1** (`RELEASE_1_ARCHITECTURE_CONSISTENCY_AUDIT_001.md` / `_002.md`).
**Decision:** **Option A ratified** (owner). Possible Resolution Paths are a **user-facing presentation pattern over multiple Recommendations**, **not** a first-class Release 1 reasoning construct.

> Scope: resolve **only** the Finding ↔ Recommendation ↔ Possible Resolution Paths relationship. No other architecture change. No doctrine, governance, execution, or new objects.

---

## 1. The ambiguity (AMB-1)

Two competing interpretations co-existed in the stack:

- **Interpretation 1 (multiple Recommendations per Finding):**
  ```text
  Finding ├─ Recommendation A ├─ Recommendation B └─ Recommendation C
  ```
- **Interpretation 2 (Resolution Paths beneath one Recommendation):**
  ```text
  Finding └─ Recommendation ├─ Resolution Path A ├─ Resolution Path B └─ Resolution Path C
  ```

Both were present, creating AMB-1.

---

## 2. Analysis

**Recommendation already owns** rationale, finding attribution, affected CAF dimensions, expected impact, explainability, lifecycle, supersession, prioritization, and user accept/reject behavior.

**Resolution Paths own no unique reasoning responsibility** — no independent lifecycle, attribution, rationale, explainability, prioritization, supersession, or assessment influence. Their only purpose is **presenting alternative approaches** to the user.

**Architectural principle:** a first-class object should exist **only when it owns unique domain behavior.** Resolution Paths do not — they are a **grouping/presentation mechanism** for alternative Recommendations. They therefore **do not satisfy the requirements of a standalone Release 1 reasoning object.**

**Evaluation (both options):** against ontology clarity, object/lifecycle/explainability/supersession ownership, data-model/API/testing/UI complexity, and Release 1 implementation simplicity — **Option A is simpler and clearer on every axis**, because it avoids creating an object that owns no behavior, and it aligns with what the stack already says (Finding System Spec §F and Coupling Spec §5 already model **multiple Recommendations per Finding**).

---

## 3. Decision — Option A (ratified)

**Possible Resolution Paths are a user-facing presentation pattern. They are not a first-class Release 1 reasoning construct.**

**Canonical Release 1 model:**
```text
Finding ├─ Recommendation A ├─ Recommendation B └─ Recommendation C
```
Recommendations remain the **sole canonical advisory objects**.

A UI **may** render:
```text
Finding
  OSLO Recommended → Recommendation A
  Possible Resolution Paths → Recommendation B, Recommendation C
  Selected Path → (the Recommendation the user selected)
```
…**without** introducing a new domain object.

---

## 4. Consequences of ratification

- **Recommendation remains authoritative** — the sole advisory object.
- **Resolution Paths become presentation-only** — a UI/view concept derived from the multiple Recommendations associated with a Finding.
- **Resolution Paths retired as a modeled construct** — `resolution_paths[]`, `is_recommended`, `is_selected` are **removed** as modeled Recommendation substructures.
- **User-facing experience preserved** — **OSLO Recommended**, **Possible Resolution Paths**, **Selected Path** remain, but as **UI presentation states derived from Recommendations**, not persisted domain-model constructs.
- **No new object introduced** — no Data Model entity, State lifecycle, Event, API resource, or Recommendation sub-object is required.

**Derivation of the UI states (no new persisted fields):**
- **Possible Resolution Paths** = the UI grouping of the multiple Recommendations for a Finding.
- **OSLO Recommended** = the Recommendation OSLO presents as primary (derived from prioritization, Recommendation System Spec §7).
- **Selected Path** = the Recommendation the user has selected/accepted (derived from the Recommendation lifecycle, §8).

*(If a persisted "primary recommendation" marker is ever wanted, that is a separate additive Recommendation-field decision — not required by this decision and not introduced here.)*

---

## 5. Follow-up changes (applied with this decision)

1. **Retired** `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` (banner-marked; retained for history).
2. **Removed** the Resolution Paths modeled substructure from `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` §4; replaced with the UI-presentation note (above).
3. **Resolved** the related backlog: Recommendation System Spec §11b (alternative-paths) is now satisfied by *multiple Recommendations per Finding*; the resolution-path-specific reconciliation/integration direction (`CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md`, already superseded) is closed.
4. **Preserved** the user-facing terminology as **UI language only** (Possible Resolution Paths / OSLO Recommended / Selected Path).
5. **UI direction:** render **Possible Resolution Paths by deriving from multiple Recommendations** associated with a Finding (no new object). *(UI Spec carries no resolution-path entity to remove; apply this derivation when the recommendations surface is detailed.)*
6. **API direction:** expose **Recommendations only**; no top-level or sub-resource Resolution Path endpoints. *(API Contract carries no resolution-path resource to remove.)*

**Untouched:** the Future-Architecture Resolution Candidate (governance) and all Governance Domain models remain isolated and unmodified. Findings remain descriptive; Recommendations advisory; assessment changes only via reanalysis.

---

## 6. Reconciliation-backlog effect

| Item | Effect of Decision A |
|---|---|
| **AMB-1** | **Resolved** — Option A ratified (multiple Recommendations per Finding; paths are UI-only) |
| Resolution-path Data Model v1.2 application | **Withdrawn** — no `resolution_paths` field; no new entity |
| RS-R5 (finding cardinality) / RS-R6 (affected-dimension cardinality) | **Independent of this decision** — they concern Recommendation↔Finding attribution generally; remain as the existing reconciliation backlog (not resolution-path-specific) |
| RS-R1/R2/R3/R4/R7 (recommendation type/lifecycle/fields) | **Unaffected** — remain in the Recommendation reconciliation backlog |

---

## Owner Decision

**Decision A — Ratified.** Possible Resolution Paths are a presentation/view over multiple Recommendations and are **not** a first-class Release 1 reasoning construct.

*Rationale:* preserves architectural simplicity, ontology clarity, and Recommendation ownership of lifecycle/explainability/supersession, while preserving the desired user experience — and aligns with the stack's existing multiple-Recommendations-per-Finding model.

---

*This decision resolves AMB-1 by ratifying Option A. It retires Resolution Paths as a modeled construct, preserves the user-facing experience as derived UI states, introduces no new object/lifecycle/event/API resource, and leaves Future Architecture untouched.*

**Recommendation / Resolution Paths Reconciliation Decision complete.**
