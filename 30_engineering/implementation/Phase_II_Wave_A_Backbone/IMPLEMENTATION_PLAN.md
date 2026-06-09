# Phase II — Wave A: Backbone (Perceive · Retain · Recompute)

**Sequence:** After Phase I. The spine every later phase depends on. · **Status:** Not started · **Owner gate:** required before Phase III.
**Contracts:** `IC/QA/OBS-WA-00R`, `IC/QA/OBS-WA-001`, `IC/QA/OBS-WA-002` (`03_architecture/contracts/WAVE_A_*`).

## Goal
Build the ingestion → canonical-retention → recompute spine: artifacts come in (integrity-gated), become attested canonical records, and a recompute can re-run the pipeline appending history. This is the foundation the understanding/advisory/disclose waves all sit on.

## Scope & build order (within the phase)
1. **`IC-WA-00R` — Recompute & Stale Backbone (Act/Adapt)** — build **first**: recompute triggers; re-run Retain→Infer→Evaluate→Advise; **append a `CognitionHistoryRecord` per emission, never overwrite**; last-known-good on failure.
2. **`IC-WA-001` — Artifact Intake (Perceive)** — integrity-gated admission (no Authority step); upload ≠ canonical; provenance; idempotency; Promotion-Candidate → Attested handoff to Retain; user-acceptance capture input for Wave U.
3. **`IC-WA-002` — Canonical Knowledge Retention (Retain)** — `AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`; Canonical = Attested; persistence ≠ canonicalization; append-only.

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The contracts below are authoritative — if a plan and a contract differ, the **contract wins**.

### Phase-specific (Wave A — build 00R → 001 → 002)
- **Contracts:** `03_architecture/contracts/WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` · `…/WAVE_A_CONTRACT_PACKAGE_001_ARTIFACT_INTAKE.md` · `…/WAVE_A_CONTRACT_PACKAGE_002_CANONICAL_KNOWLEDGE_RETENTION.md`
- **Conformance (must pass review):** `03_architecture/contracts/WAVE_A_CONTRACT_PACKAGE_001_ARTIFACT_INTAKE_CONFORMANCE_REVIEW.md` · `…/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md`
- **Ownership map:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1.md`
- **Inventory:** `03_architecture/contracts/RELEASE_1_CONTRACT_INVENTORY_V1.md`
- **Analysis modes (this backbone powers Fast/Deep):** `02_product/specs/data_api_nfr/RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` (00R recompute = the **Deep Pass** continuous-expansion engine; intake feeds the **Fast Pass** orientation) · `02_product/specs/data_api_nfr/RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` (the **< 60s** Fast-Pass budget the backbone must not block)

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
Phase I (stores, schema, CI).

## Expected outcomes (definition of done)
- ✅ **Observability:** each governed output emits its events and **appends a Cognition History Record**, with **two-axis replay** hooks present and validated per the OBS contract (a phase is not done until its outputs are observable — functional success ≠ observed success).
- ✅ An artifact can be ingested; it is **not** canonical on upload; provenance + identity recorded.
- ✅ A promotion candidate is handed to Retain and stored as an **Attested Assertion** (attributed + re-derivable).
- ✅ Re-ingesting the same artifact is **idempotent** (no duplicate canonical record).
- ✅ A recompute **appends** a new `CognitionHistoryRecord`; the prior record is unchanged and still queryable (history is append-only).
- ✅ A forced recompute failure leaves the last-known-good projection intact (no canonical loss).
- ✅ Negative tests prove: a Derived value **cannot** be written to the canonical store as Attested; a recompute **cannot** overwrite a CHR.

- ✅ **Analysis-mode support (explicit):** the 00R recompute backbone supports **Deep Pass** async / event-triggered re-analysis (coalesced; last-known-good on failure) **and** does not block the **Fast Pass** < 60s orientation budget.

## Invariants enforced
Canonical = Attested; persistence ≠ canonicalization; **recompute appends, never overwrites**; one producer per output; no Authority.

## Testing focus
Object + Behavior layers: object existence/ownership/lifecycle (Retain); event generation + recompute behavior (00R). **Negative tests are the heart of this phase** — they protect the epistemic boundary.

## Exit gate (owner-approved before Phase III)
Ingest → attested retention → recompute-appends demonstrated end to end, with the append-only and no-Derived-as-Attested invariants proven by passing negative tests.


---

## DL-047 scope additions (ratified 2026-06-04)
- **Claim Extraction (Perceive):** extract admitted evidence into **evidence-attested assertions** (source-attributed, re-derivable) for Retain — Perceive does this; it performs **no** Derived cognition. DoD: extraction produces correctly-typed, source-attributed assertions; negative test rejects Perceive emitting a Finding/assessment.
- **CRR response intake:** a submitted stakeholder response is admitted as **new evidence** and triggers Deep Pass (00R). Source: `WAVE_A_CONTRACT_PACKAGE_001` DL-047 Additions.
