# Phase V — Wave U: User Acceptance & Reconciliation (additive, non-governance)

**Sequence:** After Phase IV. · **Status:** Not started · **Owner gate:** required before Phase VI.
**Contracts:** `IC/QA/OBS-WU-ACCEPT` (`03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`, Wave U section).

## Goal
Let the **user** accept a recommendation and record that acceptance as a **user-attested plan fact** — then track whether the understanding behind an accepted item later moves (Acceptance-Impact). This is the disposition seam, implemented as **attestation + Derived cognition**, **not** as an Authority/governance engine. OSLO never self-accepts.

## Scope
- **`IC-WU-ACCEPT`** — `UserAcceptanceRecord` (user-attested, **version-pinned** to a `CognitionHistoryRecord`); **plan fact** (a user-attested `AttestedAssertion` — "factual in the plan," not world-truth); `AcceptanceImpactAssessment` (Derived, via Infer+Evaluate). Owners are existing responsibilities (Perceive capture · Retain record · Infer/Evaluate reconcile · Disclose surface) — **no new responsibility, no Authority engine.**

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The contract below is authoritative — if a plan and a contract differ, the **contract wins**.

### Phase-specific (Wave U — User Acceptance, additive/non-governance)
- **Contract:** `03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md` (**Wave U section**)
- **Conformance:** `03_architecture/contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (§3 WU-ACCEPT)
- **Design basis:** `03_architecture/decisions/USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001.md` · DL-043 constituent G (`01_governance/decisions/decision_log.md`)
- **Acceptance-impact config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§3 acceptance-impact drift)

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
Phase IV (recommendations to accept), Phase II (attested store + version-pinning to CHRs).

## Expected outcomes (definition of done)
- ✅ **Observability:** each governed output emits its events and **appends a Cognition History Record**, with **two-axis replay** hooks present and validated per the OBS contract (a phase is not done until its outputs are observable — functional success ≠ observed success).
- ✅ A user can accept a recommendation; a `UserAcceptanceRecord` is stored, **user-attested** and **version-pinned** to the exact CHR accepted.
- ✅ Acceptance creates a **plan fact** (user-attested) — recorded as fact *in the plan*, distinct from world-truth (OSLO certifies neither).
- ✅ Acceptance is **append-only**; a record cannot be overwritten (negative test) and has no valid form without its version-pin (negative test).
- ✅ When the understanding behind an accepted item drifts (≥10 pts or band change vs the pinned version), an **Acceptance-Impact alert** surfaces ("a decision you confirmed is affected").
- ✅ OSLO **never self-accepts** and a `UserAcceptanceRecord` is **not** a Governance Decision (negative tests enforce both).

## Invariants enforced
User acceptance = attested project history, not truth/governance; version-pinned; append-only; reconciliation is **Derived**; OSLO-level acceptance/approval/execution remains deferred (Outcome Governance, out of R1).

## Testing focus
Object + governance-boundary negatives: reject acceptance-as-world-truth, acceptance-as-Governance-Decision, record overwrite, missing version-pin, OSLO self-acceptance. Acceptance-Impact drift uses the same calibration source as the drift monitor.

## Exit gate (owner-approved before Phase VI)
A user can accept a recommendation into a version-pinned, append-only plan fact; acceptance-impact drift surfaces correctly; the non-governance / never-self-accept boundary is proven by passing negative tests.
