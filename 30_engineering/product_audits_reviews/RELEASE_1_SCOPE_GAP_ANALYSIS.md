# Release 1 Scope Gap Analysis

**Type:** Gap analysis — does current documentation cover everything the Release 1 user journey requires?
**Date:** 2026-05-31
**Reviewed:** `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` (+ `_V1`) · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md` · `OSLO_RELEASE_1_MASTER_SPEC.md` · `03_architecture/*` · `02_product/user_experience/*`, `plg/*`
**Companion to:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md`

> **Method & boundary.** For each capability in the canonical user journey (Intent → Context Plane → Knowledge Layer → Fast Analysis Pass → 60-Second Orientation → Deep Analysis Pass → Confidence Recalculation → Expanded Findings → Expanded Recommendations → Expanded Understanding), this analysis asks whether the documentation needed to **build** it exists. **It does not design any artifact** — it only identifies whether each is required and why, and recommends the next artifact. No capability, model, initiative, or scope is created or changed.

---

## 1. User-journey capability coverage (conceptual level)

| Journey stage | Documented at capability level? | Source |
|---|---|---|
| Intent / intake | ✅ Yes | Master Spec §15A/§15B; Matrix V2 (EI, PF) |
| Context Plane — Fast/Deep Extraction, enrichment, claim/assumption/relationship discovery | ✅ Yes | Baseline (Context Plane); Matrix V1 (Active V1 rows); Initiatives V1 I3 |
| Knowledge Layer — storage, retrieval, versioning, relationship graph | ✅ Yes (conceptual) | Baseline (Knowledge Layer); Master Spec §18 (object model) |
| Fast Analysis Pass → 60-Second Orientation | ✅ Yes | Master Spec §5; Matrix V2 AE-01; Initiatives V2 I7 |
| Deep Analysis Pass → Confidence Recalc / Expanded Findings / Recommendations | ✅ Yes | Master Spec §6; Matrix V2 AE-02; Initiatives V2 I8; Baseline (Planning Intelligence) |
| Understanding Domain models (CAF…Recommendation) | ✅ Yes | the 8 model specs; Matrix V2 |
| Notification, Collaboration & Sharing, Reporting | ✅ Yes | Master Spec §9/§16; Matrix V2; `02_product/*` |

**Conclusion:** every Release 1 user-journey capability is documented **at the capability/conceptual level.** No journey stage is undefined conceptually. The gaps are in the **cross-cutting implementation artifacts** required to build them, below.

---

## 2. Implementation-artifact gaps

### Gap A — Data Model
- **Description:** The Master Spec §18 ("Object Model & Data Architecture") defines a **conceptual** object model (~19 objects) and lineage, but there is **no implementable, field-level data model / schema** for the active Release 1 scope — in particular for the **Knowledge Layer** (canonical storage, **versioning**, **relationship graph**) and the Context Plane's discovered claims/assumptions/relationships. Existing concrete data-model material (`raw/notion` Knowledge Layer Data Model, schemas) belongs to the older/future 7-layer architecture, not the active scope.
- **Severity:** **High.** The Knowledge Layer (storage/retrieval/versioning/relationship graph) and persistence cannot be built without it; it underpins the whole journey.
- **Recommended next artifact:** a **Release 1 Data Model Specification** (entities, fields, relationships, versioning, relationship-graph model) aligned to the Master Spec §18 object model and the active scope.

### Gap B — State Models
- **Description:** Lifecycle **concepts** exist in the model specs (Finding, Recommendation, Confidence history, Notification; the two analysis-pass horizons), and an older `03_architecture/runtime_architecture/08_state_logic_state_machines.md` exists — but there is **no consolidated set of state machines for the active Release 1 objects and flows** (e.g., Finding lifecycle, Recommendation lifecycle, analysis-pass states: orientation → deep-analysis → expanded, confidence-recalculation triggers, event-driven recompute states).
- **Severity:** **Medium-High.** Event-driven recompute, the two-horizon analysis flow, and object lifecycles need defined states to implement reliably (this is also the "event-driven Deep Pass semantics undefined" risk in the dependency graph).
- **Recommended next artifact:** a **Release 1 State Model Specification** (object + analysis-flow state machines for the active scope), reconciling/superseding the older `08_state_logic_state_machines.md` where it predates the active architecture.

### Gap C — API Contracts
- **Description:** There is **no API / service-interface contract** for the active Release 1 product. (Existing "contract" documents are governance/terminology or the future 7-layer consumption contracts — not Release 1 product APIs.) Interfaces among Context Plane, Knowledge Layer, Planning Intelligence, the Understanding models, Notification, Collaboration, and the surfaces are undefined at the contract level.
- **Severity:** **High.** Front-end/back-end and inter-service development needs defined contracts; the 60-second orientation + deep-analysis flow crosses several services.
- **Recommended next artifact:** a **Release 1 API / Service Contract Specification** (the interfaces the active components expose and consume).

### Gap D — UI Specification
- **Description:** Wireframes exist (`02_product/user_experience/01_product_shell_layout`, `03_outcome_space_workspace`, `04_core_navigation_information_architecture`, `06_interaction_rules`; `02_product/plg/02_plg_60_second_flow_wireframes`), and the Master Spec §15 defines screen-level UX — but there is **no single consolidated "UI Specification"** (the onboarding path lists it as "when created"). The wireframes are dispersed and not unified into one buildable spec.
- **Severity:** **High.** It is a named required-onboarding document and blocks coherent front-end delivery of the orientation, MRI, overlays, workspace, collaboration, and reporting surfaces.
- **Recommended next artifact:** a **consolidated UI Specification** unifying the existing wireframes + Master Spec §15 screen architecture for the active Release 1 surfaces.

### Gap E — Testing Strategy
- **Description:** Acceptance criteria exist per capability (Master Spec §16; ~59 acceptance references in Matrix V2) and there are risk/open-questions docs (`05_execution/implementation_tracking/*`), but there is **no consolidated Release 1 Testing Strategy** — no test approach for the two analysis horizons (e.g., the §20 *Time-to-First-MRI < 60s* target, deep-analysis recompute correctness), no acceptance-test-to-capability mapping, no determinism/replay test plan for the analysis passes.
- **Severity:** **Medium.** Needed to verify Release 1 success criteria (esp. the 60-second and deep-analysis outcomes) but does not block initial build.
- **Recommended next artifact:** a **Release 1 Testing Strategy** (acceptance-test mapping to §16 criteria, the 60-second metric, deep-analysis/recompute and determinism tests).

---

## 3. Related (non-artifact) gaps — already recorded, noted for completeness

Not artifact types, but blockers the journey depends on (already captured in `OSLO_CAPABILITY_MATRIX_V2.md` §22 and the Dependency Graph — **not re-designed here**):

- **CAF scoring method & CAF→Confidence formula undefined** (calibration). High — pivots the analysis. *(Calibration artifact, owner-owned.)*
- **Event-driven Deep Analysis recompute semantics undefined.** High — underlies the Deep Analysis Pass (overlaps Gap B).
- **Notification object / external-reviewer identity** — relevant to Collaboration (M3); lower priority for the core analysis journey.

---

## 4. Severity summary & recommended artifact order

| Gap | Severity | Recommended next artifact |
|---|---|---|
| A — Data Model | **High** | Release 1 Data Model Specification |
| C — API Contracts | **High** | Release 1 API / Service Contract Specification |
| D — UI Specification | **High** | Consolidated Release 1 UI Specification |
| B — State Models | **Medium-High** | Release 1 State Model Specification |
| E — Testing Strategy | **Medium** | Release 1 Testing Strategy |

Recommended order: **Data Model → State Models → API Contracts → UI Specification → Testing Strategy** (data and state underpin contracts; contracts + UI enable build; testing verifies). These five are the documentation required to take Release 1 from *defined* to *buildable*; **none is designed here** — each is identified as required, with rationale.

---

## Final Verification

- **Governance remains Future Architecture** — confirmed (no governance reclassified active; the 5 governance models stay Future; Collaboration's "CAF Review Requests" is a feature, not the governance Review Request Model).
- **Deep Analysis remains Active Release 1** — confirmed (canonical scope §3/§4/§7; gap analysis treats it as active).
- **No new capabilities introduced** — confirmed (capabilities cited from existing sources only; gaps are *artifacts*, not capabilities).
- **No scope changes made** — confirmed (scope mirrors the founder-approved In/Out lists).
- **Canonical scope successfully consolidated** — confirmed (`OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` is the single governing scope source; this analysis identifies the buildability gaps beneath it).

**Release 1 canonical scope established.**
