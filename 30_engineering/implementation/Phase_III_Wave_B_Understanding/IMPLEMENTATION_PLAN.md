# Phase III — Wave B: Understanding (Infer · Evaluate)

**Sequence:** After Phase II. · **Status:** Not started · **Owner gate:** required before Phase IV.
**Contracts:** `IC/QA/OBS-WB-INFER`, `IC/QA/OBS-WB-EVAL` (`03_architecture/contracts/WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`).

## Goal
Produce OSLO's **understanding** of the canonical record — Findings (Infer), and Issues with Confidence/Reliability/CAF/Outcome Confidence (Evaluate) — all as **Derived** cognition that is recomputable and history-tracked. This is where OSLO starts to *say something* about a project, with calibrated uncertainty.

## Scope & build order
1. **`IC-WB-INFER` — Finding (Infer)** — generate Findings (gap/conflict/risk) from Attested content; one producer; conflicts **surfaced, not resolved**; each Finding is Derived.
2. **`IC-WB-EVAL` — Issue · Confidence · Reliability · CAF · Outcome Confidence (Evaluate)** — assess Findings into Issues; compute Confidence (trust-in-understanding, **never** project health); reliability-qualified; band-semantic per Calibration Defaults.

> **Two analysis modes are an explicit Release 1 requirement (not implicit).** Wave B runs as a **Fast Pass** — latency-bound, delivering Orientation Confidence + initial MRI/findings within the **< 60s Time-to-First-MRI** budget — and a **Deep Pass** — continuous, async, event-triggered expansion (Confidence Recalculation, Expanded Findings/Recommendations), with **progressive confidence** (Orientation → Expanded → Validated). The user never waits for Deep Pass. See the Analysis-modes + Performance-NFR references in the manifest.

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The contract below is authoritative — if a plan and a contract differ, the **contract wins**.

### Phase-specific (Wave B — Infer + Evaluate)
- **Contract:** `03_architecture/contracts/WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`
- **Synthesis Engine contract (DL-047, build with/before Wave B):** `03_architecture/contracts/WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md` (IC/QA/OBS-WS-SYNTH — extraction · synthesis · generation as Derived)
- **Conformance:** `03_architecture/contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (§1 WB-INFER/WB-EVAL)
- **Scoring models (Evaluate):** `02_product/specs/models/CONFIDENCE_MODEL_V2.md` · `…/RELIABILITY_MODEL_V2.md` · `…/CAF_SCORING_MODEL_V2.md`
- **Drift/band config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§2 bands, §3 drift)
- **Fixtures + test specs (Finding):** `02_product/specs/testing_fixtures/FINDING_FIXTURE_LIBRARY_SPECIFICATION_V1.md` · `…/FINDING_SUBSYSTEM_TEST_SPECIFICATION_V1.md`
- **Fixtures + test specs (Confidence/Evaluate):** `02_product/specs/testing_fixtures/RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md` · `…/RELEASE_1_CONFIDENCE_SUBSYSTEM_TEST_SPECIFICATION.md` · `…/RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_REVIEW_001.md`
- **Analysis modes (Fast / Deep — REQUIRED, not implicit):** `02_product/specs/data_api_nfr/RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` · `02_product/specs/FAST_DEEP_WORKFLOW_PACK/FAST_PASS_STAGE_IO_SPEC.md` · `…/DEEP_PASS_STAGE_IO_SPEC.md` · `…/FAST_VS_DEEP_PASS_COMPARISON.md` · `…/ACCEPTANCE_CRITERIA.md`
- **Performance NFR (60s):** `02_product/specs/data_api_nfr/RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` — **Time-to-First-MRI < 60s** (the only owner-approved numeric target; Master Spec §20 / M1)

### Always-required (every phase)
- **Agent rules:** `03_architecture/engineering/starter_kit/AGENTS.md` · `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`
- **Canonical architecture:** `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`
- **Models:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…/RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1.md` · `…/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- **Standards:** `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md`
- **Numeric config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`
- **Ratified scope:** `01_governance/decisions/decision_log.md` (DL-043, DL-044)
- **Testing:** `02_product/specs/testing_fixtures/RELEASE_1_TESTING_STRATEGY_V1.md` · `…/DETERMINISM_CALIBRATION_NOTE_001.md` (test authoring + determinism tiers; pair with each contract's QA section)
- **Observability:** `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` + this wave's **OBS contract** (inside the wave package above — events · audit · two-axis replay · drift/trust signals). Every governed output must emit and be replayable.

## Depends on
Phase II (Attested store + recompute backbone — understanding is recomputed via 00R and appends CHRs).

## Expected outcomes (definition of done)
- ✅ **Observability:** each governed output emits its events and **appends a Cognition History Record**, with **two-axis replay** hooks present and validated per the OBS contract (a phase is not done until its outputs are observable — functional success ≠ observed success).
- ✅ Findings are generated from attested content and stored as **Derived** (never written to the canonical store as Attested).
- ✅ Issues/Confidence/Reliability/CAF/Outcome Confidence compute, each carrying explicit `epistemic_state = derived` and a confidence **band** (0–49/50–74/75–100, with the ±3 edge-guard).
- ✅ Confidence is expressed as **trust in understanding**, reliability-qualified — never as project health/readiness/probability/score (negative tests enforce this).
- ✅ A recompute produces a **new** CHR; comparing two emissions shows confidence/outcome **drift** surfaced at ≥10 pts or a band change (product feature).
- ✅ "Why did confidence change?" is answerable structurally via CHR lineage.
- ✅ Determinism: rule-derived values replay **exactly**; AI-numeric values replay within **±7 pts & same band**.

- ✅ **Fast Pass (explicit):** a first end-to-end pass delivers Orientation Confidence + an initial MRI/findings within the **owner-approved < 60s Time-to-First-MRI** budget; the user is never blocked on Deep Pass.
- ✅ **Deep Pass (explicit):** continuous, async, event-triggered expansion runs after orientation (Confidence Recalculation, Expanded Findings/Recommendations); **progressive confidence stages (Orientation → Expanded → Validated)** are present, observable, and history-tracked.

## Invariants enforced
Cognition is **Derived** and recomputable; confidence ≠ project health; conflicts surfaced not resolved; only-recompute-changes-assessment; one producer per output.

## Testing focus
Behavior layer + determinism tiers: exact replay for rule/formula steps; band-semantic for AI-numeric; semantic for AI-text. Negative tests for the "confidence-as-health" and "Derived-as-Attested" prohibitions.

## Exit gate (owner-approved before Phase IV)
OSLO produces calibrated, Derived understanding with banded confidence and surfaced drift; the determinism tiers hold on replay; uncertainty is explicit, never hidden.


---

## DL-047 scope additions (ratified 2026-06-04)
- **Planning Synthesis + Generation (Infer, Derived):** build `SynthesizedPlanningModel` + generated `PlanningArtifact`s (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) as **Derived** (recomputable, CHR-per-generation, user-editable, never Attested-as-truth).
- **Understanding Evaluation (Evaluate):** seed initial CAF/Confidence from the synthesized model.
- **False-Confidence Detection (CONF-06):** flag high confidence on weak understanding (QA negative required).
- **Understanding State Model / Progressive Disclosure (AE-04/05):** Initial→Partial→Refined→Validated→Mature (extends DL-046 `confidence_stage`).
- DoD: artifacts generated as Derived with CHR + recompute-supersede; negative test rejects a generated artifact written as Attested-truth or changed without recompute. Source: `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING` DL-047 Additions · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1` · `FAST_DEEP_WORKFLOW_PACK/`.
