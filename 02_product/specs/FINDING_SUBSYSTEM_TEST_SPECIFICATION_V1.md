# Finding Subsystem Test Specification v1

**Type:** Testing & validation artifact (implements; creates no behavior)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — validates, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · Finding Model · CAF Scoring v2 · Reliability v2 · Confidence v2 · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · `RECOMMENDATION_SUBSYSTEM_TEST_SPECIFICATION_V1.md` · Data Model v1.2 · State Model · Event Model · Architecture Audit 001/002 · `FINDING_PRESENTATION_SPECIFICATION_V1.md`.

> **Validates doctrine; creates none.** No new doctrine, Finding behavior, lifecycle states, finding types, scoring/severity algorithms, recommendation behavior, governance, execution, or automation. Determinism tolerance for any generated content is **"Deferred to Determinism Calibration Note."** Conformance is **structural**, never a pass-rate.

---

## 1. Purpose

Authoritative Release 1 test reference for the **Finding subsystem**. It validates that Findings behave exactly as the architecture defines: **descriptive, evidence-based, explainable** objects that contribute to CAF **only via Impact Assessment**, **never** influence Reliability, **never** directly modify Confidence, give rise to (but are never altered by) Recommendations, and carry **no** governance/execution semantics.

## 2. Scope

**Tested:** Finding definition, representation, attribution, type taxonomy, affected-dimension attribution, the Impact-Assessment relationship, lifecycle, supersession/history, explainability, the Finding↔Recommendation relationship, the CAF boundary, Reliability/Confidence isolation, governance/execution isolation, replay/history, and presentation alignment.

**Out of scope:** recommendation behavior (except relationship validation); CAF scoring arithmetic; reliability determination; confidence synthesis; governance; execution; agents; automation; numeric calibration (Deferred).

## 3. Subsystem Under Test

```text
Evidence / Context ─▶ FINDING (descriptive) ─▶ Impact Assessment ─▶ CAF ─▶ (+Reliability) ─▶ Confidence
                              └─▶ Recommendation (originates from the Finding)
```

- **Findings influence CAF only through Impact Assessment.**
- **Findings never influence Reliability** (Reliability derives from Coverage/Evidence Availability/Assessability, independent of findings — RR-2).
- **Findings never directly influence Confidence** (reach it only through CAF — FND-4).

## 4. Test Categories

| Category | Validates | Source |
|---|---|---|
| Representation (§5) | required fields | Finding §B; Data v1.2 §11 |
| Attribution (§6) | evidence/context/dimensions; no orphans | FND-5/FND-6 |
| Type taxonomy (§7) | canonical 7 types only | FND-6; Finding §B |
| Impact Assessment (§8) | contribution via IA; type-not-coefficient | FND-2/FND-9 |
| Lifecycle (§9) | states/transitions | FND §C; State §10 |
| Supersession & History (§10) | append-only | FND-8; §E |
| Explainability (§11) | no opaque finding | FND-7; §D |
| Recommendation relationship (§12) | recs from findings; no feedback | FND-10; Coupling |
| CAF boundary (§13) | no direct CAF write | FND-2 |
| Reliability/Confidence isolation (§14) | no influence | FND-3/FND-4; RR-2 |
| Negative / Governance isolation (§15) | no governance/execution | FND-12 |
| Replay / History (§16) | reconstructable | FND-8; Engine §16 |
| Presentation alignment (§17) | matches Finding Presentation Spec | FPRS-* |

---

## 5. Finding Representation Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **REP-T1** | Required fields present | `finding_id`, `finding_type`, `affected_dimensions`, `status`, `evidence_links`, `rationale` present | any required field missing |
| **REP-T2** | Title/summary present (if used) | human-readable title/summary renders | unreadable/absent where required |
| **REP-T3** | Severity representation (if present) | qualitative `severity ∈ {critical, moderate, warning}`; **no numeric score** | a numeric severity score appears |
| **REP-T4** | Supersession references | `supersedes_finding_id`/chain reconstructable | chain absent/broken |
| **REP-T5** | No invented fields | only canonical Data Model v1.2 Finding fields exist | a non-canonical field exists |

## 6. Finding Attribution Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **ATT-T1** | Source evidence present | every finding has ≥1 `evidence_links` | unattributed finding (FND-5) |
| **ATT-T2** | Supporting context present | producing run (`first_seen_run_id`) + context resolvable | context missing |
| **ATT-T3** | Affected dimensions declared | `affected_dimensions ⊆ {clarity, alignment, feasibility}`, ≥1 | dimensions undeclared (FND-6) |
| **ATT-T4** | No orphan findings | every finding traces to evidence + run | orphan exists |
| **ATT-T5** | Attribution survives supersession | superseded finding retains its basis | basis lost on supersede |

## 7. Finding Type Taxonomy Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **TYP-T1** | Canonical types only | `finding_type ∈ {missing_information, ambiguity, assumption, inference, conflict, constraint, coverage_gap}` | a non-canonical `finding_type` value exists |
| **TYP-T2** | "dependency issue" mapped | represented as `constraint`/`coverage_gap` (+ Feasibility dimension), not a new type | a `dependency` type value exists |
| **TYP-T3** | "feasibility/alignment/clarity concern" mapped | expressed via `affected_dimensions`, not as types | a dimension-concern type value exists |
| **TYP-T4** | Type is a label | type does not set CAF effect magnitude/locality | type used as a coefficient (FND-9) |

## 8. Impact Assessment Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **IA-T1** | IA required for CAF contribution | a finding contributes to CAF only via its Impact Assessment | direct CAF contribution without IA (FND-2) |
| **IA-T2** | Type-not-coefficient | two same-type findings with different IA → different contribution | magnitude set by type (FND-9) |
| **IA-T3** | Affected dimensions control locality | contribution confined to IA-declared dimensions | contribution to a non-affected dimension |
| **IA-T4** | IA controls contribution | re-assessing IA changes the dimension without the finding changing | finding forced to change, or no effect |
| **IA-T5** | No direct CAF change | finding never writes a CAF value | finding sets CAF (FND-2) |
| **IA-T6** | IA explainable | IA basis (significance/scope/evidence-support — qualitative) reconstructable | opaque IA |

*(No formulas, scoring, or magnitudes beyond canonical qualitative severity.)*

## 9. Lifecycle Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **LIFE-T1** | Legal path | detected→acknowledged→addressed→closed | legal step blocked |
| **LIFE-T2** | Reopen | closed→reopened | reopen unsupported |
| **LIFE-T3** | Supersede | {detected,acknowledged,addressed}→superseded (retained) | overwrite/loss |
| **LIFE-T4** | Forbidden transitions | detected→closed, superseded→active → blocked | illegal transition allowed |
| **LIFE-T5** | No hidden/governance states | status ∈ the 6 canonical only | any extra/governance state exists |

## 10. Supersession and History Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **SUP-T1** | Supersede, not overwrite | new finding supersedes; prior retained | prior overwritten/deleted (FND-8) |
| **SUP-T2** | Superseded retained | superseded findings remain in history | superseded finding deleted |
| **SUP-T3** | Chain reconstructable | supersession chain rebuilds | chain not reconstructable |
| **SUP-T4** | Reopened behavior | closed→reopened restores to active; history intact | reopen loses history |
| **SUP-T5** | Closed retained | closed findings retained in history | closed finding deleted |

## 11. Explainability Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **EXP-T1** | Why identified | rationale reconstructable | missing rationale |
| **EXP-T2** | Source evidence | `evidence_links` resolvable | unresolvable evidence |
| **EXP-T3** | Supporting context | producing run/artifact reachable | missing context |
| **EXP-T4** | Affected dimensions | shown | missing |
| **EXP-T5** | Impact Assessment basis | qualitative IA summary reachable | opaque |
| **EXP-T6** | Related recommendations | reachable from the finding | not linked |
| **EXP-T7** | Supersession history | reachable where applicable | missing |
| **EXP-T8** | No opaque finding | every required component available | any opaque finding (FND-7) |

## 12. Finding → Recommendation Relationship Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **REL-T1** | Recommendations originate from findings | every recommendation traces to a finding | rec without finding (REC-1) |
| **REL-T2** | One finding → many recommendations | multiple recs may attach to one finding | model forbids >1 |
| **REL-T3** | Recommendation lifecycle doesn't alter finding | accept/defer/implement/supersede of a rec writes nothing to the finding | rec mutates finding (FND-10) |
| **REL-T4** | Coupling on finding change | finding state change drives rec coupling per the Coupling Spec | coupling not applied (RFC-*) |
| **REL-T5** | Rec actions don't close findings | implementing a recommendation does **not** directly close/weaken the finding | rec directly closes the finding |
| **REL-T6** | Only reanalysis resolves | finding weakened/removed/closed **only** via reanalysis | finding resolved without reanalysis |

## 13. CAF Boundary Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **CAF-T1** | CAF via IA only | findings contribute to CAF only through Impact Assessment | direct CAF contribution (FND-2) |
| **CAF-T2** | No direct CAF modify | no finding writes a CAF dimension | finding modifies CAF |
| **CAF-T3** | Descriptive, not a score | finding presence is descriptive; no intrinsic score | finding carries a CAF score |
| **CAF-T4** | Type-not-coefficient | (cross-ref IA-T2) | type sets CAF effect |
| **CAF-T5** | No direct Confidence change | no finding changes Outcome Confidence directly | finding writes confidence |

## 14. Reliability / Confidence Isolation Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **ISO-T1** | Findings never influence Reliability | adding/removing findings does **not** move reliability | reliability moved by a finding (RR-2/FND-3) |
| **ISO-T2** | Findings never directly modify Confidence | confidence unchanged except via CAF/Reliability change | finding writes confidence (FND-4) |
| **ISO-T3** | Confidence change path | confidence moves only when CAF or Reliability changes | confidence moves with no CAF/Reliability change |
| **ISO-T4** | Reliability source | reliability derives only from Coverage/Evidence Availability/Assessability | reliability derived from findings |

## 15. Negative / Governance Isolation Tests *(hard gate — must FAIL if present)*

| ID | Objective | Failure |
|---|---|---|
| **NEG-T1** | No **Resolution Candidate** in the active Finding subsystem | any reference/application |
| **NEG-T2** | No **Clarification Candidate** | any reference |
| **NEG-T3** | No **Accepted Understanding** | any reference |
| **NEG-T4** | No **Disposition** | any reference |
| **NEG-T5** | No **Review Request** | any reference |
| **NEG-T6** | No **Governance state** on a Finding | any governance state exists |
| **NEG-T7** | No **Agent action** | any autonomous agent affordance |
| **NEG-T8** | No **Execution workflow** | any execution/automation on a Finding (FND-12) |

## 16. Replay and History Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **RPL-T1** | Finding states reconstruct | replay rebuilds finding states exactly | divergence |
| **RPL-T2** | Status transitions reconstruct | transition history exact | divergence |
| **RPL-T3** | Supersession chains reconstruct | chains exact | divergence |
| **RPL-T4** | Source evidence references reconstruct | `evidence_links` exact | loss |
| **RPL-T5** | Impact Assessment links reconstruct | IA links exact | loss |
| **RPL-T6** | Recommendation links reconstruct | finding↔rec links exact | loss |

## 17. Presentation Alignment Tests

| ID | Objective | Expected | Failure |
|---|---|---|---|
| **PA-T1** | Cards descriptive | finding cards present observations, not actions | a finding card frames an action/command (FPRS-1) |
| **PA-T2** | Recommendations nested under findings | recs render beneath their finding | rec not finding-anchored (FPRS-2) |
| **PA-T3** | Possible Resolution Paths presentation-only | rendered as grouped Recommendations; no object/field | a resolution-path object/field surfaces (FPRS-6) |
| **PA-T4** | Findings ≠ recommendations | findings never appear as recommendations | conflation |
| **PA-T5** | No direct-assessment implication | UI never implies a finding modifies CAF/Confidence | such implication present (FPRS-4/FPRS-5) |

## 18. Fixture Requirements

Fixture **classes** required later (no content created here): ambiguity · missing-information · assumption · inference · conflict · constraint · coverage-gap · superseded-finding · reopened-finding · finding-with-multiple-recommendations. Fixtures must be deterministic and configuration-pinned (see the Finding Fixture Library Spec, future).

## 19. Conformance Requirements

The subsystem is **certified** when **all** hold (objective, structural, **non-numeric**):
- **FST-C1.** Representation/Attribution/Type/IA suites pass (§5–§8) — every finding attributed, typed canonically, contributing to CAF only via IA.
- **FST-C2.** Lifecycle/Supersession/History pass (§9–§10) — canonical states, append-only, reconstructable.
- **FST-C3.** Explainability passes (§11) — **no opaque finding**.
- **FST-C4.** Recommendation-relationship passes (§12) — recs from findings, no feedback, resolution only via reanalysis.
- **FST-C5.** CAF-boundary + Reliability/Confidence-isolation pass (§13–§14) — **no direct CAF/Confidence write; no Reliability influence**.
- **FST-C6.** **All Negative/Governance-isolation tests (§15) pass** (hard gate) — no governance/execution/retired/future artifact.
- **FST-C7.** Replay/History (§16) and Presentation-alignment (§17) pass.
- **FST-C8.** Any **opaque finding, unattributed finding, governance leakage, direct CAF/Confidence modification, Reliability influence, non-canonical type, or resolution-without-reanalysis** **fails conformance** regardless of other results.

## 20. Deferred Items

Deferred (not asserted with numeric criteria): fixture **content**; scoring/calibration values; **severity algorithms**; Impact-Assessment **magnitudes**; recommendation effectiveness analytics; UI implementation; determinism **tolerance** for generated finding content (Determinism Calibration Note).

---

*This specification validates the Release 1 Finding subsystem: descriptive, evidence-attributed, canonically-typed, explainable, append-only findings that contribute to CAF only via Impact Assessment, never influence Reliability, never directly modify Confidence, give rise to (but are never altered by) Recommendations, and carry no governance/execution semantics. It changes no model or behavior and defers only numeric calibration and fixture content.*

**Finding Subsystem Test Specification v1 complete.**
