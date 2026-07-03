# Recommendation Fixture Library Specification v1

**Type:** Testing support specification (defines the fixture framework; creates no fixture content)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_SUBSYSTEM_TEST_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · Data Model v1.2 · State Model · Event Model · `DETERMINISM_CALIBRATION_NOTE_001.md`.
**Mirrors:** `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md` (style + rigor).

> **Non-negotiable.** This defines the **canonical Recommendation fixture framework** — philosophy, structure, classification, lifecycle, traceability, coverage. It creates **no** recommendation behavior, doctrine, lifecycle definitions, prioritization logic, scoring, calibration, **actual fixture content**, or **numeric tolerances**. Expectations are **structural**, never numeric. **Fixtures validate doctrine; they do not define it.**

---

## 1. Purpose

Recommendation fixtures provide **deterministic, explainable, traceable** validation inputs for the Recommendation subsystem, so the Recommendation Subsystem Test Spec exercises the ratified model the same way every time. Fixtures make recommendation behavior — attribution, lifecycle (incl. `deferred`), supersession, coupling, multiplicity, derived presentation, success-via-reanalysis, and isolation — **repeatably observable**.

## 2. Scope

**In scope:** recommendation generation, attribution, lifecycle, supersession, recommendation/finding coupling, multiplicity, success, and **presentation-derivation** validation.
**Out of scope:** recommendation scoring; prioritization algorithms; calibration; UI implementation; execution behavior; governance behavior; fixture **content** (Deferred §13).

## 3. Fixture Philosophy

- **Determinism** — identical inputs under a pinned configuration yield equivalent governable outputs (§8).
- **Traceability** — every fixture maps bidirectionally to tests/rules/conformance (§7).
- **Explainability** — every fixture permits full basis reconstruction (finding link, rationale, state, supersession).
- **Replayability** — fixture runs reconstruct exactly from the event log.
- **Coverage** — every REC rule, conformance item, lifecycle state, and coupling behavior has a covering fixture (§9).
- **Single-behavior fixtures are preferred** *(ratified principle)* — composite fixtures are permitted **only when the interaction itself is the behavior under test** (§11). Authors avoid unrelated complexity that obscures attribution/explainability/determinism/replay/traceability.

## 4. Fixture Classification

Fixture **families**:
**Attribution · Lifecycle · Supersession · Coupling · Multiple Recommendations · Recommendation Success · Recommendation Presentation · Boundary / Isolation · Replay.**

## 5. Fixture Structure

Every fixture MUST contain (structural — **no numeric expectations**):

| Component | Definition |
|---|---|
| **Fixture ID** | stable unique identifier |
| **Name** | human-readable scenario name |
| **Purpose** | the specific recommendation behavior it exercises (Primary Purpose; see §11) |
| **Source Inputs** | the controlled finding(s)/context that produce the recommendation(s) — *described structurally; content deferred* |
| **Expected Recommendation State** | the recommendation lifecycle state(s) (generated/accepted/rejected/deferred/implemented/superseded) — structural, no scores |
| **Expected Findings Relationship** | the finding(s) the recommendation traces to (single `finding_id`) and coupling behavior |
| **Expected Lifecycle Outcome** | the transition(s) the fixture should drive and their legality |
| **Expected Explainability Outcome** | which basis components must reconstruct (finding link, rationale, state, supersession) |
| **Covered Test Cases** | the Recommendation Subsystem Test IDs it covers (ATT-T*, LIFE-T*, SUP-T*, MULTI-T*, PRES-T*, SUCC-T*, NEG-T*, CPL-T*, DET-T*) |

A fixture missing any required component is **non-conformant** (§12).

## 6. Fixture Lifecycle

`Draft → Approved → Active → Deprecated → Retired` — **append-only**:
- **Draft** authored; not used for certification.
- **Approved** reviewed (doctrine-valid, traceable, deterministic, explainable); eligible to activate.
- **Active** in the certification suite; changes create a **new version/baseline** (§8), never an in-place edit.
- **Deprecated** superseded; retained, not used for new certification.
- **Retired** no longer used; **retained in history** (replay/audit).

Changes to Active fixtures are **new versions** (supersede, not overwrite) — mirroring the subsystem's append-only discipline.

## 7. Fixture Traceability

Every fixture maps **bidirectionally** to:
- **Recommendation subsystem tests** (the test IDs it covers, §5);
- **Recommendation integrity rules** (REC-1…REC-12) and coupling rules (RFC-*);
- **Conformance requirements** (Recommendation Subsystem Test §15 RC-* and DMA-* isolation rules).

From a fixture one can reach the rules/tests it serves, **and** from any rule/test one can reach its covering fixtures. **No fixture is untraceable; no validated rule is uncovered.**

## 8. Fixture Determinism

Aligned with `DETERMINISM_CALIBRATION_NOTE_001.md`:
- Fixtures validate the **governable outputs** for the recommendation domain — **recommendation states, recommendation attribution (finding link), recommendation relationships, and emitted events** — under a **pinned baseline** (configuration × fixture version × model version).
- A fixture change creates a **new baseline**; prior results stay interpretable.
- The recommendation **state machine** is exact; any tolerance for LLM-generated recommendation **content** is **"Deferred to Determinism Calibration Note"** — **no numeric tolerance is defined here.**

## 9. Fixture Coverage Requirements

Coverage MUST exist for:
- **REC-1 … REC-12** (every recommendation integrity rule);
- **all conformance requirements** (RC-1…RC-5; DMA isolation);
- **all lifecycle states** (generated, accepted, rejected, **deferred**, implemented, superseded) and their legal/illegal transitions;
- **all coupling behaviors** (finding superseded/closed/reopened/removed/weakened — RFC-*).

Every Recommendation Subsystem Test (§5–§14 there) has ≥1 covering fixture.

## 10. Recommendation Fixture Families (required classes)

### Attribution Fixtures
single-finding · missing-attribution (must fail) · superseded-attribution.

### Lifecycle Fixtures
generated · accepted · rejected · **deferred** · implemented · superseded.

### Coupling Fixtures
finding-closed · finding-removed · finding-reopened · finding-weakened · finding-superseded.

### Multiple Recommendation Fixtures
parallel-recommendations · selected-recommendation · alternative-recommendations.

### Success Fixtures
accepted-but-not-implemented · implemented-but-ineffective · implemented-and-effective *(success via reanalysis weakening/removing the finding)*.

### Presentation Fixtures *(presentation only — **no persisted fields**)*
OSLO-Recommended (derived from prioritization) · Possible-Resolution-Paths (grouped Recommendations) · Selected-Path (the accepted Recommendation). **No `resolution_paths[]`/`is_recommended`/`is_selected`.**

### Boundary Fixtures
recommendation-cannot-modify-CAF · recommendation-cannot-modify-Reliability · recommendation-cannot-modify-Confidence.

### Isolation Fixtures
no-Resolution-Candidate · no-Clarification-Candidate · no-Governance-objects.

## 11. Composite Fixture Rules

A fixture MAY exercise multiple behaviors. When it does:
- exactly **one Primary Purpose**; additional behaviors **may** be recorded as **Secondary Purposes** (optional);
- **attribution and explainability must remain intact** — a composite fixture must never make it impossible to determine **why** a recommendation state changed;
- composition is used **only where the interaction is the behavior under test** (per §3 single-behavior preference).
Composite fixtures introduce **no new conformance rule**: existing traceability/determinism/explainability conformance applies equally.

## 12. Conformance Requirements

The fixture library conforms when (objective, structural, **no percentages/thresholds**):
- **RFL-C1.** Every fixture is **classified** into a §4/§10 family.
- **RFL-C2.** Every fixture is **traceable** bidirectionally to tests/rules/conformance (§7).
- **RFL-C3.** Every fixture is **deterministic** and baseline-pinned (§8).
- **RFL-C4.** Every fixture is **explainable** — full basis reconstructable; no opaque fixture.
- **RFL-C5.** Every fixture carries all required **structure** (§5).
- **RFL-C6.** Every fixture is **doctrine-valid** — consistent with the ratified Recommendation model (incl. `deferred`; single `finding_id`; **no** resolution-path field/object; no governance).
- **RFL-C7.** **Coverage:** every REC rule, conformance item, lifecycle state, and coupling behavior has ≥1 covering fixture (§9).
- **RFL-C8.** **Lifecycle integrity:** Active-fixture changes are new versions/baselines (append-only); nothing overwritten.

## 13. Deferred Items

Explicitly **deferred** (not created here): fixture **content**; calibration values; **prioritization formulas**; recommendation **effectiveness analytics**; determinism **tolerance** (Determinism Calibration Note); UI implementation.

---

*This document defines the canonical Release 1 Recommendation fixture framework — categorized, structured, governed (append-only), traced, and coverage-complete — for validating the Recommendation subsystem. It creates no recommendation behavior, doctrine, scoring, calibration, or fixture content, introduces no numerics, and mirrors the Confidence Fixture Library Specification in style and rigor.*

**Recommendation Fixture Library Specification v1 complete.**
