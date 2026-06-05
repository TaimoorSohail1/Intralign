# Phase VI — Wave E: Disclose Surfaces (Presentation)

**Sequence:** Last. · **Status:** Not started · **Owner gate:** required before Release 1 production readiness.
**Contracts:** `IC/QA/OBS-WE-DISCLOSE` (`03_architecture/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md`).

## Goal
Present everything the prior phases produced — **epistemically safely**. Disclose is a **consumer** (presents, never generates); **Render** is its non-cognitive service. Every surface labels uncertainty (Attested/Derived + confidence band + conflict) and shows both current understanding and its history. This is the user-facing layer of Release 1.

## Scope (surfaces, per ratified UX specs)
- **MRI** (umbrella), **Finding Panel** & **Recommendation Panel** (RP-C1: Recommendation Panel only in Finding context), **Issue Cards**, **Project Overview**, **Understanding Companion** (routes via Finding — Option B), **Notification/Awareness**, **History/Timeline**, **Export/Share-out**.

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The contract + UX specs below are authoritative — if a plan and a source differ, the **source wins**.

### Phase-specific (Wave E — Disclose surfaces)
- **Contract:** `03_architecture/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md`
- **Conformance:** `03_architecture/contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (§4 WE-DISCLOSE)
- **UI master:** `02_product/specs/ux/RELEASE_1_UI_SPECIFICATION_V1.md` · `…/UI_SCREEN_INVENTORY.md`
- **Surface specs:** `02_product/specs/ux/` → `MRI_EXPERIENCE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md` · `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1.md` · `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1.md`

### Always-required (every phase)
- **Agent rules:** `03_architecture/engineering/starter_kit/AGENTS.md` · `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`
- **Canonical architecture:** `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`
- **Models:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…/RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1.md` · `…/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- **Standards:** `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md`
- **Numeric config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`
- **Ratified scope:** `01_governance/decisions/decision_log.md` (DL-043, DL-044)

## Depends on
Phases II–V (there is nothing to disclose until the cognition + acceptance records exist).

## Expected outcomes (definition of done)
- ✅ Each surface presents the governed objects it owns and **traces** to its ratified UX spec.
- ✅ Every surface labels **epistemic state** (Attested vs Derived), the **confidence band**, and any **conflict** — Derived is never shown as settled (negative tests enforce; band-edge guard applied).
- ✅ **Recommendation Panel renders only in a Finding context** (RP-C1) — enforced in Disclose (presentation), not duplicated as a cognition rule.
- ✅ Plan facts display as **user-attested** (distinct from evidence-attested and OSLO-self-attested).
- ✅ Both **current foreground** and **history/timeline** are presented; history is append-only in presentation.
- ✅ **Export** packages existing understanding only, carrying epistemic labels; exposure = epistemic-safety labeling (no Authority gate in R1).
- ✅ Disclose **generates nothing** and **changes no assessment** (negative tests); Render performs no cognition.

## Invariants enforced
Disclose presents (consumer, not producer); Render = service; epistemic-safety labeling everywhere; RP-C1; stale-never-current; history append-only; export packages existing understanding only; no Authority.

## Testing focus
Presentation negatives + E2E (Playwright/Cypress): reject Derived-as-settled, overstated confidence, RP-C1 violation, acceptance-by-Disclose, unsourced export. Visual/interaction coverage of the surfaces.

## Exit gate (owner-approved — Release 1 feature-complete)
All surfaces present the cognition chain + acceptance with enforced epistemic-safety labeling and current+history views; Disclose proven to generate nothing and change no assessment. → Release 1 ready for production-readiness review (production deploy remains owner-only).
