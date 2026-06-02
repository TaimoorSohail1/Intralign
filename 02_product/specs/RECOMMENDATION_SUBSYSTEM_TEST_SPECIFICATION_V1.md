# Recommendation Subsystem Test Specification v1

**Type:** Testing & validation artifact (implements; creates no behavior)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — validates, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · Recommendation Model v1 · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `FINDING_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md` · `RECOMMENDATION_RECONCILIATION_RATIFICATION_DECISION_001.md` · Data Model v1.2 · State Model · Event Model · CAF Scoring v2 · Reliability v2 · Confidence v2.

> **Validates doctrine; creates none.** No new behavior, lifecycle, object, event, governance, execution, scoring, or probability. Determinism tolerance is **"Deferred to Determinism Calibration Note."** Conformance is **structural**, never a pass-rate. The subsystem under test is the **ratified post-v1.2 Recommendation model** (lifecycle `generated/accepted/rejected/deferred/implemented/superseded`; single `finding_id`; **no** Resolution Path object; AMB-1 resolved).

---

## 1. Purpose

Authoritative test reference for the Recommendation subsystem: attribution, the CAF/Reliability/Confidence boundary, the `deferred` lifecycle, supersession, multiple-recommendations-per-finding, the **derived** presentation labels (OSLO Recommended / Possible Resolution Paths / Selected Path), success-via-reanalysis, and the **negative guarantees** (no resolution-path field/entity, no Clarification Candidate, no Resolution Candidate leakage).

## 2. Scope

**Tested:** Recommendation entity/lifecycle/supersession/attribution, Finding↔Recommendation coupling, presentation derivation, success semantics, and isolation from retired/future concepts.
**Not tested here:** CAF/Reliability/Confidence internals (their own subsystem spec), Finding internals (Finding subsystem spec), UI pixels, and numeric calibration (Deferred).

## 3. Subsystem Under Test

```text
Finding (descriptive) ─< Recommendation (advisory; generated/accepted/rejected/deferred/implemented/superseded)
                              │ derived presentation: OSLO Recommended · Possible Resolution Paths · Selected Path
                              └─ User action → Information change → Reanalysis → Finding weakened/removed (success)
```
Recommendations consume Finding/CAF context; they **never** write CAF/Reliability/Confidence. A Finding may have **many** Recommendations (single `finding_id` each).

## 4. Test Categories

| Category | Validates | Source |
|---|---|---|
| Attribution (§5) | trace to ≥1 Finding | REC-1/REC-8; DMA-6 |
| Boundary (§6) | no direct CAF/Reliability/Confidence write | REC-2/REC-3; C-5/C-6 |
| Lifecycle (§7) | states incl. `deferred` | State §11; Data v1.2 |
| Supersession (§8) | append-only | REC-6/REC-11 |
| Multiplicity (§9) | many recs per finding | Finding §F; AMB-1; Coupling §5 |
| Presentation derivation (§10) | OSLO Recommended / Possible Resolution Paths / Selected Path | Presentation §C/§D; AMB-1 |
| Success (§11) | reanalysis-only | Rec §11; REC-12 |
| Negative / Isolation (§12) | no resolution-path field/entity; no Clarification/Resolution Candidate | DMA-1/2/3 |
| Coupling (§13) | finding state-change | RFC-* |
| Determinism / Replay (§14) | reconstructable | REC-11; Engine §16 |

---

## 5. Attribution Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **ATT-T1** | Every recommendation traces to a Finding | `finding_id` present and resolvable | Unattributed recommendation persists (REC-1/REC-8) |
| **ATT-T2** | Single-finding attribution (v1.2) | exactly one `finding_id`; **no** `finding_references` array | A `finding_references[]` field exists (RS-R5 deferred; DMA-6) |
| **ATT-T3** | Rejection of unattributed creation | create without a finding → rejected | Recommendation created with no finding |
| **ATT-T4** | Attribution survives lifecycle | finding link intact through accept/defer/implement/supersede | Link lost on a transition (REC-8) |

## 6. Boundary Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **BND-T1** | No direct CAF write | accepting/deferring/implementing changes no `CAFState` | A recommendation op alters CAF (REC-2) |
| **BND-T2** | No direct Reliability write | no recommendation op alters reliability | Reliability changed by a recommendation (REC-3) |
| **BND-T3** | No direct Confidence write | no recommendation op alters `ConfidenceState` | Confidence changed by a recommendation (REC-3) |
| **BND-T4** | No execution | no recommendation performs an action autonomously | An action occurs without user (REC-9/REC-10) |

## 7. Lifecycle Tests (incl. `deferred`)

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **LIFE-T1** | Generated → Accepted | legal | rejected/blocked |
| **LIFE-T2** | Generated → Rejected | legal | — |
| **LIFE-T3** | **Generated → Deferred** | legal (postpone; remains valid) 〔RS-R3〕 | `deferred` not supported, or treated as rejection |
| **LIFE-T4** | **Deferred → Accepted / Deferred → Rejected** | legal (re-engage a deferred rec) | deferred is terminal/illegal transition |
| **LIFE-T5** | Accepted → Implemented | legal | — |
| **LIFE-T6** | Any active (incl. Deferred) → Superseded | legal; prior retained | deferred cannot be superseded |
| **LIFE-T7** | Illegal transitions rejected | Rejected→Implemented, Implemented→Generated, Superseded→Accepted → `409`/blocked | illegal transition allowed |
| **LIFE-T8** | No `presented`/`completed` states | status enum = {generated,accepted,rejected,deferred,implemented,superseded} | `presented` or `completed` state exists (RS-R2/RS-R4) |
| **LIFE-T9** | Deferral changes no assessment | deferring alters no CAF/Reliability/Confidence | assessment moved on defer |

## 8. Supersession Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **SUP-T1** | Supersede, not overwrite | new rec supersedes; prior retained (`status=superseded`) | prior overwritten/deleted (REC-6) |
| **SUP-T2** | Append-only state changes | every change appends; no in-place mutation of a prior state | in-place mutation (REC-11) |
| **SUP-T3** | Chain reconstructable | supersession chain rebuilds the recommendation history | chain not reconstructable |
| **SUP-T4** | Deferred rec superseded | a deferred rec can be superseded and is retained | loss of deferred rec on supersession |

## 9. Multiplicity Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **MULTI-T1** | Many recs per finding | one Finding → multiple Recommendations coexist | model forbids >1 rec per finding |
| **MULTI-T2** | Coexistence (parallel options) | alternatives coexist; not mutually exclusive by default | one auto-rejects others (Coupling §5) |
| **MULTI-T3** | Accept one, leave others | user accepts one; others remain Generated/Deferred | accepting one forces others closed |
| **MULTI-T4** | Resolution supersedes alternatives | when the finding resolves, remaining open alternatives → superseded (retained) | alternatives left dangling or deleted |

## 10. Presentation-Derivation Tests

*(These assert the labels are **derived**, with **no persisted** `is_recommended`/`is_selected`/`resolution_paths`.)*

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **PRES-T1** | **OSLO Recommended derived** | the primary recommendation is derived from prioritization (Rec §7); **no** persisted `is_recommended` field | An `is_recommended` field exists, or a score/rank is shown |
| **PRES-T2** | **Possible Resolution Paths derived** | the grouping is the set of multiple Recommendations for the finding; **no** `resolution_paths[]` field/object | A `resolution_paths[]` field/entity exists |
| **PRES-T3** | **Selected Path derived from accepted rec** | "Selected Path" = the user's **accepted** Recommendation (lifecycle); **no** persisted `is_selected` field | An `is_selected` field exists, or Selected ≠ the accepted rec |
| **PRES-T4** | Recommended ≠ Selected allowed | user may accept a non-primary rec; Selected Path differs from OSLO Recommended | system forces selected = recommended |
| **PRES-T5** | No score displayed | OSLO Recommended/ordering shows no number/percentage | a score/rank appears |

## 11. Success Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **SUCC-T1** | Acceptance ≠ success | accepting a rec does not mark success | accept treated as success |
| **SUCC-T2** | Implemented ≠ success | `implemented` alone is not success | implemented shown as resolution |
| **SUCC-T3** | Success via reanalysis | success only when user action → information change → reanalysis weakens/removes the finding | success without reanalysis/finding change (REC-12) |
| **SUCC-T4** | Acted-but-ineffective | acted + reanalyzed but finding unchanged → "acted upon, not effective" (not success) | ineffective action marked success |

## 12. Negative / Isolation Tests *(must FAIL if any are present)*

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **NEG-T1** | **No `resolution_paths[]` field** | the model/schema/payload has no `resolution_paths` | field present (DMA-1) |
| **NEG-T2** | **No `is_recommended`/`is_selected` fields** | absent from model/schema/payload | either field present (DMA-1) |
| **NEG-T3** | **No standalone Resolution Path entity** | no entity/table/lifecycle/event/endpoint for a Resolution Path | any such artifact exists (DMA-1/DMA-9/DMA-10) |
| **NEG-T4** | **No Clarification Candidate** | no ClarificationCandidate entity/event/endpoint/reference in active scope | any reference exists (DMA-2) |
| **NEG-T5** | **No Resolution Candidate leakage** | no governance Resolution Candidate / Accepted Understanding / Disposition / Governance in the active Recommendation model | any such concept referenced/applied (DMA-3) |
| **NEG-T6** | API exposes Recommendations only | no Resolution Path / Clarification Candidate endpoints | such endpoints exist (DMA-10) |

## 13. Coupling Tests (finding state-change)

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **CPL-T1** | Finding superseded/closed/removed | a rec tracing to it is superseded (retained); else re-evaluated | rec deleted or left unattributed (RFC-1/RFC-2) |
| **CPL-T2** | Finding weakened | rec persists (still coupled) | rec superseded on weakening alone (RFC-4) |
| **CPL-T3** | Finding reopened | a **new** rec may be generated; no resurrection of a superseded one | a superseded rec is resurrected (RFC-2) |
| **CPL-T4** | Coupling changes no assessment | coupling transitions write no CAF/Reliability/Confidence | assessment moved by coupling (RFC-3) |

## 14. Determinism / Replay Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **DET-T1** | State-machine determinism | same command on same state → same transition (set-to-state) | nondeterministic transition |
| **DET-T2** | Replay reconstruction | event-log replay rebuilds recommendation states + supersession chains exactly | divergence on replay |
| **DET-T3** | No-op idempotency | re-applying a transition/command converges to the same state | double-advance / duplicate effect |
| **DET-T4** | Event coverage | each transition emits its Event-Model event (`recommendation_created/accepted/rejected/deferred/implemented/superseded`); no extra events | missing/extra event (incl. any resolution-path event) |

*(Determinism tolerance, where applicable to LLM-generated recommendation content, is "Deferred to Determinism Calibration Note"; the state-machine tests above are exact.)*

---

## 15. Conformance Requirements

The subsystem is **certified** when **all** hold (structural — no percentages/thresholds):
- **RC-1.** Attribution (§5), Boundary (§6), Lifecycle incl. `deferred` (§7), Supersession (§8), Multiplicity (§9), Success (§11), and Coupling (§13) suites pass.
- **RC-2.** Presentation-derivation (§10) passes — labels derived, **no** persisted `is_recommended`/`is_selected`/`resolution_paths`.
- **RC-3.** **All Negative/Isolation tests (§12) pass** — i.e., **none** of the forbidden artifacts exist (hard gate).
- **RC-4.** Determinism/Replay (§14) passes (tolerance deferred).
- **RC-5.** Any boundary write (CAF/Reliability/Confidence), unattributed/overwritten recommendation, autonomous action, displayed score, success-without-reanalysis, or forbidden artifact **fails certification** regardless of other results.

## 16. Deferred Items

Deferred (not asserted with numeric criteria here): determinism **tolerance** (Determinism Calibration Note); recommendation **prioritization** numeric realization (none — conceptual only); multi-finding / multi-dimension behavior (RS-R5/RS-R6 deferred — out of scope until ratified); fixture **content** (Recommendation Fixture Library Spec).

---

*This specification validates the ratified Release 1 Recommendation subsystem: finding-attributed, advisory, append-only, with the `deferred` lifecycle, multiple-recommendations-per-finding, derived presentation labels, success only via reanalysis, and hard isolation from resolution-path fields/entities, Clarification Candidate, and Future-Architecture Resolution Candidate. It changes no model or behavior and defers only numeric calibration.*

**Recommendation Subsystem Test Specification v1 complete.**
