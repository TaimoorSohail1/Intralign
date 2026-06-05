# Phase V — Wave U: User Acceptance & Reconciliation (additive, non-governance)

**Sequence:** After Phase IV. · **Status:** Not started · **Owner gate:** required before Phase VI.
**Contracts:** `IC/QA/OBS-WU-ACCEPT` (`03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`, Wave U section).

## Goal
Let the **user** accept a recommendation and record that acceptance as a **user-attested plan fact** — then track whether the understanding behind an accepted item later moves (Acceptance-Impact). This is the disposition seam, implemented as **attestation + Derived cognition**, **not** as an Authority/governance engine. OSLO never self-accepts.

## Scope
- **`IC-WU-ACCEPT`** — `UserAcceptanceRecord` (user-attested, **version-pinned** to a `CognitionHistoryRecord`); **plan fact** (a user-attested `AttestedAssertion` — "factual in the plan," not world-truth); `AcceptanceImpactAssessment` (Derived, via Infer+Evaluate). Owners are existing responsibilities (Perceive capture · Retain record · Infer/Evaluate reconcile · Disclose surface) — **no new responsibility, no Authority engine.**

## Depends on
Phase IV (recommendations to accept), Phase II (attested store + version-pinning to CHRs).

## Expected outcomes (definition of done)
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
