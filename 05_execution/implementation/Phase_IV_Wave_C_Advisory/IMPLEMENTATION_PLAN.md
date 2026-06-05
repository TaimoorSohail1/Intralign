# Phase IV — Wave C: Advisory (Advise)

**Sequence:** After Phase III. · **Status:** Not started · **Owner gate:** required before Phase V.
**Contracts:** `IC/QA/OBS-WC-ADVISE` (`03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`, Wave C section).

## Goal
Generate **advice** — Recommendations and Clarification Requests anchored to Findings/Issues — as governable candidate *responses*. Advise proposes; it never accepts, governs, or executes. This is the layer that turns understanding into "here's what you might do."

## Scope
- **`IC-WC-ADVISE`** — Recommendation (+ Suggested-Action / Candidate-Improvement types) and Clarification Request; each anchored to a Finding/Issue. **Resolution Paths are a presentation-only substructure of a Recommendation — no standalone Resolution-Path object.**

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The contract below is authoritative — if a plan and a contract differ, the **contract wins**.

### Phase-specific (Wave C — Advise)
- **Contract:** `03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md` (**Wave C section**)
- **Conformance:** `03_architecture/contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (§2 WC-ADVISE)
- **Recommendation model:** `02_product/specs/models/RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` (Resolution Paths = substructure, no standalone object)
- **Surface (for shape only):** `02_product/specs/ux/RECOMMENDATION_PANEL_SPECIFICATION_V1.md`
- **Fixtures + test specs (Recommendation):** `02_product/specs/testing_fixtures/RECOMMENDATION_FIXTURE_LIBRARY_SPECIFICATION_V1.md` · `…/RECOMMENDATION_SUBSYSTEM_TEST_SPECIFICATION_V1.md`

### Always-required (every phase)
- **Agent rules:** `03_architecture/engineering/starter_kit/AGENTS.md` · `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`
- **Canonical architecture:** `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`
- **Models:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…/RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1.md` · `…/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- **Standards:** `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md`
- **Numeric config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`
- **Ratified scope:** `01_governance/decisions/decision_log.md` (DL-043, DL-044)
- **Testing:** `02_product/specs/testing_fixtures/RELEASE_1_TESTING_STRATEGY_V1.md` · `…/DETERMINISM_CALIBRATION_NOTE_001.md` (test authoring + determinism tiers; pair with each contract's QA section)

## Depends on
Phase III (Findings/Issues to anchor to) and Phase II (recompute appends CHRs for advisory emissions too).

## Expected outcomes (definition of done)
- ✅ Recommendations are generated **only in the context of a Finding** (Recommendation-only-in-Finding-context invariant), each traceable to its anchor.
- ✅ Clarification Requests generate where understanding is insufficient.
- ✅ Resolution Paths appear as a **substructure** of a Recommendation, **not** as a separate object (negative test rejects a standalone Resolution-Path object).
- ✅ Advise **never** accepts, governs, executes, or self-authorizes (negative tests reject each).
- ✅ Recommendations are **Derived** and recomputable; a recompute appends a new CHR; recommendations never exact-replay (semantic equivalence is the bar).

## Invariants enforced
Only **Advise** generates candidate responses (Authority generates nothing); Recommendation only in Finding context; Resolution-Paths presentation-only; Advise never accepts/governs/executes; cognition Derived + recomputable.

## Testing focus
Governance-adjacent negatives are central here: prove Advise cannot accept/govern/execute and cannot emit a standalone Resolution-Path object. Semantic-equivalence replay for recommendation text.

## Exit gate (owner-approved before Phase V)
OSLO advises with Finding-anchored, governable candidate recommendations and clarifications; the "advise proposes, never disposes" boundary is proven by passing negative tests.
