# Finding Fixture Library Specification v1

**Type:** Testing support specification (defines the fixture framework; creates no fixture content)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_SUBSYSTEM_TEST_SPECIFICATION_V1.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · CAF Scoring v2 · Reliability v2 · Confidence v2 · Data Model v1.2 · State Model · Event Model · `DETERMINISM_CALIBRATION_NOTE_001.md`.
**Mirrors:** `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md` (rigor, determinism principles, traceability standards).

> **Non-negotiable.** This defines the **canonical Finding fixture framework** — philosophy, structure, classification, lifecycle, traceability, coverage. It creates **no** finding doctrine, behavior, scoring, calibration, lifecycle definitions, type definitions, **actual fixture content**, or **numeric tolerances**. Expectations are **structural**, never numeric. **Findings are descriptive objects; fixtures validate descriptive behavior only. Fixtures validate doctrine; they do not define it.**

---

## 1. Purpose

Finding fixtures provide **deterministic, explainable, traceable, replayable** validation inputs for the Finding subsystem, so the Finding Subsystem Test Spec exercises the ratified model the same way every time. Because **Findings are descriptive**, fixtures validate **descriptive behavior only** — representation, attribution, type, Impact-Assessment relationship, lifecycle, supersession, explainability, the Finding↔Recommendation relationship, and the CAF/Reliability/Confidence boundaries — never prescriptive/action behavior.

## 2. Scope

**In scope:** finding representation · attribution · type validation · lifecycle · supersession · explainability · finding→recommendation relationship · finding→Impact-Assessment · finding→CAF boundary · Reliability isolation · Confidence isolation.
**Out of scope:** recommendation behavior; CAF scoring arithmetic; reliability determination; confidence synthesis; governance; execution; agents; automation; fixture **content** (Deferred §13).

## 3. Fixture Philosophy

- **Determinism** — identical inputs under a pinned configuration yield equivalent governable outputs (§8).
- **Traceability** — every fixture maps bidirectionally to tests/rules/conformance (§7).
- **Explainability** — every fixture permits full basis reconstruction (evidence, rationale, dimensions, IA, history).
- **Replayability** — fixture runs reconstruct exactly from the event log.
- **Coverage** — every FND rule, conformance item, lifecycle state, finding type, supersession, and coupling behavior has a covering fixture (§9).
- **Single-behavior fixtures are preferred** *(ratified principle)* — composite fixtures only where the **interaction itself is the behavior under test** (§11). Authors avoid unrelated complexity that obscures attribution/explainability/determinism/replay/traceability.

## 4. Fixture Classification

Fixture **families**: **Representation · Attribution · Type Taxonomy · Impact Assessment · Lifecycle · Supersession · Explainability · Recommendation Relationship · CAF Boundary · Reliability Isolation · Confidence Isolation · Replay · Governance Isolation.**

## 5. Fixture Structure

Every fixture MUST contain (structural — **no numeric expectations**):

| Component | Definition |
|---|---|
| **Fixture ID** | stable unique identifier |
| **Name** | human-readable scenario name |
| **Purpose** | the specific finding behavior it exercises (Primary Purpose; §11) |
| **Source Inputs** | the controlled evidence/context that produces the finding(s) — *described structurally; content deferred* |
| **Expected Finding State** | finding `finding_type`, `affected_dimensions`, `status`, severity (qualitative) — structural, no scores |
| **Expected Attribution Outcome** | the evidence/context the finding traces to (≥1 `evidence_links`) + producing run |
| **Expected Explainability Outcome** | which basis components must reconstruct (evidence, rationale, dimensions, IA basis, history) |
| **Expected Lifecycle Outcome** | the transition(s) the fixture should drive and their legality |
| **Covered Test Cases** | the Finding Subsystem Test IDs it covers (REP-T*, ATT-T*, TYP-T*, IA-T*, LIFE-T*, SUP-T*, EXP-T*, REL-T*, CAF-T*, ISO-T*, NEG-T*, RPL-T*, PA-T*) |

A fixture missing any required component is **non-conformant** (§12).

## 6. Fixture Lifecycle

`Draft → Approved → Active → Deprecated → Retired` — **append-only; no fixture deletion**:
- **Draft** authored; not used for certification.
- **Approved** reviewed (doctrine-valid, traceable, deterministic, explainable); eligible to activate.
- **Active** in the certification suite; changes create a **new version/baseline** (§8), never an in-place edit.
- **Deprecated** superseded; retained, not used for new certification.
- **Retired** no longer used; **retained in history** (replay/audit).

## 7. Fixture Traceability

Every fixture maps **bidirectionally** to:
- **Finding subsystem tests** (the test IDs it covers, §5);
- **Finding integrity rules** (FND-1…FND-12);
- **Finding conformance requirements** (Finding Subsystem Test §19, FST-C1…C8).

From a fixture one can reach its rules/tests, **and** from any rule/test one can reach its covering fixtures. **No orphan fixtures; no uncovered rule.**

## 8. Fixture Determinism

Aligned with `DETERMINISM_CALIBRATION_NOTE_001.md`:
- Fixtures validate the finding-domain **governable outputs** — **finding state, finding attribution (evidence/dimension links), finding relationships, finding explainability, finding lifecycle** — under a **pinned baseline** (configuration × fixture version × model version).
- A fixture change creates a **new baseline**; prior results remain interpretable.
- The finding **state machine** is exact; any tolerance for LLM-generated finding **content** is **"Deferred to Determinism Calibration Note."** **No tolerances or thresholds are defined here.**

## 9. Fixture Coverage Requirements

Coverage MUST exist for:
- **all FND integrity rules** (FND-1…FND-12);
- **all Finding conformance requirements** (FST-C1…C8);
- **all lifecycle states** (detected, acknowledged, addressed, closed, reopened, superseded) and their legal/illegal transitions;
- **all finding types** (missing_information, ambiguity, assumption, inference, conflict, constraint, coverage_gap);
- **all supersession behaviors**;
- **all finding/recommendation coupling behaviors** (finding superseded/closed/reopened/removed/weakened — RFC-*).

Every Finding Subsystem Test has ≥1 covering fixture.

## 10. Finding Fixture Families (required classes)

### Representation Fixtures
required-fields-present · invalid-field-structure (must fail) · **no invented fields**.

### Attribution Fixtures
evidence-attribution · supporting-context-attribution · affected-CAF-dimension-attribution · missing-attribution (must fail).

### Type Taxonomy Fixtures
one per canonical type (`missing_information`, `ambiguity`, `assumption`, `inference`, `conflict`, `constraint`, `coverage_gap`) · **non-canonical-type (must fail)** · mapped-condition (dependency/feasibility/alignment/clarity → canonical type + dimension).

### Impact Assessment Fixtures
contributes-via-IA · type-is-not-a-coefficient · IA-explainable · no-direct-CAF-change (must fail if direct).

### Lifecycle Fixtures
detected · acknowledged · addressed · closed · reopened · superseded · legal-transitions · illegal-transition (must fail).

### Supersession Fixtures
retained-history · reconstructable-chain · append-only (overwrite must fail).

### Explainability Fixtures
source-evidence · rationale · affected-dimensions · supporting-context · IA-basis · **opaque-finding (must fail)**.

### Recommendation Relationship Fixtures
recommendations-originate-from-finding · one-finding-many-recommendations · recommendation-does-not-alter-finding · resolution-only-via-reanalysis.

### CAF Boundary Fixtures
no-direct-CAF-modification (must fail if present) · contributes-only-via-IA.

### Reliability Isolation Fixtures
finding-does-not-influence-reliability (must fail if it does).

### Confidence Isolation Fixtures
finding-does-not-directly-influence-confidence (must fail if it does).

### Governance Isolation Fixtures
no-Resolution-Candidate · no-Clarification-Candidate · no-Accepted-Understanding · no-Disposition · no-Review-Request · no-Governance-state (each must fail if present).

## 11. Composite Fixture Rules

A fixture MAY exercise multiple behaviors. When it does:
- exactly **one Primary Purpose**; additional behaviors **may** be recorded as **Secondary Purposes** (optional);
- it must **preserve attribution, determinism, explainability, and replayability** — never making it impossible to determine **why** a finding state changed;
- composition is used **only where the interaction is the behavior under test** (per §3).
Composite fixtures introduce **no new conformance rule**; existing traceability/determinism/explainability conformance applies equally.

## 12. Conformance Requirements

The fixture library conforms when (objective, structural, deterministic, **no percentages/thresholds**):
- **FFL-C1.** Every fixture is **classified** into a §4/§10 family.
- **FFL-C2.** Every fixture is **traceable** bidirectionally to tests/rules/conformance (§7) — **no orphan fixture**.
- **FFL-C3.** Every fixture is **deterministic** and baseline-pinned (§8).
- **FFL-C4.** Every fixture is **explainable** — full basis reconstructable; **no opaque finding fixture**.
- **FFL-C5.** Every fixture carries all required **structure** (§5).
- **FFL-C6.** Every fixture is **doctrine-valid** — consistent with the ratified Finding model (canonical 7 types; descriptive; contributes to CAF only via IA; no governance/execution).
- **FFL-C7.** **Coverage:** every FND rule, conformance item, lifecycle state, finding type, supersession, and coupling behavior has ≥1 covering fixture (§9).
- **FFL-C8.** **Lifecycle integrity:** Active-fixture changes are new versions/baselines (append-only); nothing overwritten/deleted.
- **FFL-C9.** Any **opaque finding, unattributed finding, governance leakage, direct CAF modification, Reliability influence, or Confidence influence** in a fixture's expected behavior **fails conformance**.

## 13. Deferred Items

Explicitly **deferred** (not created here): fixture **content**; calibration values; **scoring formulas**; **severity algorithms**; **Impact-Assessment magnitudes**; UI implementation; determinism **tolerance** for generated finding content (Determinism Calibration Note).

---

*This document defines the canonical Release 1 Finding fixture framework — categorized, structured, governed (append-only), traced, and coverage-complete — for validating the descriptive Finding subsystem. It creates no finding doctrine, behavior, scoring, calibration, type/lifecycle definitions, or fixture content, introduces no numerics, and mirrors the Confidence Fixture Library Specification in rigor, determinism, and traceability.*

**Finding Fixture Library Specification v1 complete.**
