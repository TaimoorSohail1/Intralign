# Release 1 Confidence Fixture Library Specification

**Type:** Fixture-framework artifact (defines the canonical fixture library; creates no fixture data)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md` · `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` · `RELEASE_1_CONFIDENCE_SUBSYSTEM_TEST_SPECIFICATION.md`
**Stack position:** `OUTCOME_CONFIDENCE_STACK_INDEX.md` (validation support for L4).
**Revision:** 2026-05-31 — owner-ratified refinement applied per `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_REVIEW_001.md`: added the **Fixture Minimality** principle (§3, Rec 1) and **Fixture Composition** + Primary/Secondary Purpose (§5, Rec 2). Recs 3 (FC-9) and 4 (FC-10) **rejected** — no new conformance rule added; FC-2/FC-3/FC-4 unchanged.

> **Non-negotiable.** This document defines the **canonical fixture framework** — categories, structure, requirements, governance, lifecycle, and traceability. It creates **no** doctrine, calibration, formulas, thresholds, weights, probabilities, implementation code, **actual fixture data**, or test results. Expectations are **structural**, never numeric. Whenever a choice arises between adding a concept and preserving doctrine, **doctrine is preserved.**

---

## 1. Purpose

A fixture library exists to provide **repeatable, deterministic validation inputs** for the CAF → Reliability → Confidence subsystem. Fixtures let the test specification (`RELEASE_1_CONFIDENCE_SUBSYSTEM_TEST_SPECIFICATION.md`) exercise doctrine the same way every time, on the same controlled inputs, so behavior is verifiable and regressions are detectable.

**Fixtures exist to validate doctrine. Fixtures do not define doctrine.** A fixture is an input scenario plus the **structural** behavior the doctrine/models require of it — never a source of new meaning, calibration, or values.

---

## 2. Scope

**In scope:** the framework for —
- **CAF fixtures** (ambiguity, assumption, conflict, feasibility scenarios),
- **Reliability fixtures** (coverage, evidence, assessability scenarios),
- **Confidence fixtures** (consolidation/qualification scenarios),
- **Fast/Deep fixtures** (provisional → supersede, rise/fall),
- **Replay fixtures** (reconstruction scenarios),
- **Determinism fixtures** (stable, pinned inputs).

**Out of scope:** production data, customer projects, calibration values, tolerance/threshold values, implementation/storage formats, and actual fixture content (Section 15).

---

## 3. Fixture Philosophy

- **A fixture is a controlled project-understanding scenario** — a deliberately shaped set of inputs (intent, artifacts, evidence, context) that places understanding in a known condition.
- **Fixtures represent understanding conditions**, not finished projects: an "ambiguous-KPI" fixture exists to create an ambiguity condition, not to model a real product.
- **Fixtures are not intended to represent real projects perfectly** — realism is sacrificed for **control and repeatability**.
- **Fixtures exist to exercise doctrine** — each is built to make a specific doctrinal behavior observable (e.g., a conflict fixture exists to drive Alignment-reduction and a Deep-pass confidence decrease).

**Fixture Minimality (principle).** 〔ratified — Review 001, Rec 1〕 A fixture should contain **only** the information required to exercise its intended doctrinal behavior. **Single-behavior fixtures are preferred.** Composite fixtures are permitted **only when the interaction itself is the behavior being tested** (see §5 *Fixture Composition*). Authors avoid unrelated complexity that would obscure attribution, explainability, determinism, replayability, or traceability. *(This is an authoring **principle**, not a conformance gate; minimality is not adjudicated numerically.)*

---

## 4. Fixture Taxonomy

Top-level categories (illustrative scenario names only — **no fixture data created**):

### Ambiguity Fixtures *(exercise Clarity)*
Ambiguous ownership · ambiguous KPI · ambiguous timeline · ambiguous success criteria.

### Assumption Fixtures *(exercise the dimension an assumption underpins)*
Hidden assumption · invalid assumption · assumption chain · unsupported assumption.

### Conflict Fixtures *(exercise Alignment; drive Deep-pass decreases)*
Goal conflict · scope conflict · schedule conflict · resource conflict.

### Feasibility Fixtures *(exercise Feasibility)*
Resource shortage · timeline infeasibility · dependency infeasibility · capability infeasibility.

### Reliability Fixtures *(exercise Coverage / Evidence Availability / Assessability)*
Low coverage · high coverage · evidence-rich · evidence-poor · assessability-constrained.

### Deep Analysis Fixtures *(exercise Fast→Deep supersession & discovery)*
Hidden contradiction discovered · hidden dependency discovered · hidden feasibility issue discovered.

---

## 5. Fixture Structure

Every fixture MUST contain the following components. Expectations are **structural only — no numeric expectations**:

| Component | Definition |
|---|---|
| **Fixture ID** | Stable unique identifier. |
| **Fixture Name** | Human-readable scenario name. |
| **Fixture Category** | One of the Section 4 categories. |
| **Primary Purpose** 〔ratified — Review 001, Rec 2〕 | The **single** doctrinal behavior the fixture primarily exists to exercise. |
| **Secondary Purposes** *(optional)* 〔ratified — Review 001, Rec 2〕 | Additional behaviors a composite fixture also exercises (may be empty). |
| **Input Artifacts** | The controlled understanding inputs (intent/artifacts/evidence/context) — *described structurally; actual data deferred*. |
| **Expected CAF Behavior** | Which dimension(s) are affected and in which direction (strengthen/weaken/stable), and via which finding(s)/Impact Assessment — **no indices/values**. |
| **Expected Reliability Behavior** | How Coverage/Evidence Availability/Assessability are positioned and the qualifier direction (e.g., "low coverage → constrained reliability") — **no values**. |
| **Expected Confidence Behavior** | The structural outcome of consolidate-then-qualify (e.g., "material weakness constrains the band"; "reliability holds expression back without collapse") — **no bands-as-numbers**. |
| **Expected Explainability Behavior** | Which basis components must be reconstructable (CAF basis, reliability basis, contributing findings, impact assessments, change attribution). |
| **Expected History Behavior** | Whether and how supersession occurs; what must be retained. |
| **Expected Fast/Deep Behavior** | The fixture's behavior across Fast vs Deep (e.g., "Deep discovers the contradiction; confidence decreases; Fast state retained"). |

A fixture missing any required component is **non-conformant** (Section 14).

### Fixture Composition 〔ratified — Review 001, Rec 2〕

A fixture **may** exercise multiple behaviors. When it does:
- exactly **one** behavior is its **Primary Purpose**; additional behaviors **may** be recorded as **Secondary Purposes** (optional);
- **attribution, explainability, and traceability must remain intact** — a composite fixture must **never** make it impossible to determine **why** a model state changed;
- composition is used **only where the interaction is the behavior under test** (per §3 *Fixture Minimality*).

Composite fixtures introduce **no new conformance rule**: the existing **FC-2 (traceable), FC-3 (deterministic), and FC-4 (explainable / no opaque fixture)** apply **equally** to composite fixtures. A composite fixture that obscures attribution or explainability **fails FC-4**.

---

## 6. Fixture Quality Requirements

Fixtures MUST be:
- **deterministic** — identical inputs under a pinned configuration yield equivalent governable outputs;
- **reproducible** — runnable repeatedly with the same result;
- **explainable** — permit full basis reconstruction (Section 12);
- **traceable** — mapped to doctrine/calibration/model rules/tests (Section 7);
- **doctrine-valid** — consistent with the authoritative meaning/calibration/models (never contradicting them).

Fixtures MUST NOT:
- depend on **UI**;
- depend on **implementation details** (storage formats, engine internals);
- depend on **calibration values** (band boundaries, tolerances, magnitudes).

---

## 7. Fixture Traceability

Every fixture MUST map, **bidirectionally**, to:
- **Doctrine** — the meaning principle(s) it exercises (Decision/Interpretation/Leadership 001).
- **Calibration** — the calibration principle/invariant(s) it depends on (Calibration Decision 001; INV-1/2/3).
- **Model rules** — the specific Integrity Rules it validates (CR-* / RR-* / IR-*).
- **Test cases** — the test IDs that consume it (CAF-T*, REL-T*, CONF-T*, INV-T*, FD-T*, HIST-T*, REPLAY-T*, EXPL-T*, DET-T*).

**Bidirectional** means: from a fixture one can reach the rules/tests it serves, **and** from any rule/test one can reach the fixtures that exercise it. No fixture may be untraceable; no validated rule may lack a covering fixture.

---

## 8. Fixture Lifecycle

States (using lifecycle concepts; no workflow implementation):

| State | Behavior |
|---|---|
| **Draft** | Authored, not yet reviewed; not used in certification. |
| **Approved** | Reviewed and accepted as doctrine-valid and traceable; eligible to activate. |
| **Active** | In the certification suite; changes create a **new baseline** (Section 11). |
| **Deprecated** | Superseded by a better fixture; retained, not used for new certification; references preserved. |
| **Retired** | No longer used; **retained in history** (append-only; never deleted), for replay/audit of past runs. |

Transitions are **append-only** (a fixture is superseded/retired, not overwritten), mirroring the subsystem's supersession discipline.

---

## 9. Fixture Governance

- **Who may create fixtures.** Any contributor may author a **Draft**.
- **Who may modify fixtures.** Only via governance review; an **Active** fixture is not edited in place — a change produces a **new versioned fixture** (new baseline) and supersedes the prior.
- **How fixture changes are reviewed.** Through the repository governance lifecycle (Backlog → Proposal → Review → Decision → Change → Changelog); review confirms **doctrine-validity, traceability, determinism, and explainability** before Approval/Activation. No layer self-ratifies; the owner ratifies.
- **How versioning works.** Each fixture carries a version; supersession links versions; history is retained. *(No workflow/tooling implementation defined here.)*

---

## 10. Canonical Release 1 Fixture Families

| Family | Purpose | Primary model exercised | Primary test areas |
|---|---|---|---|
| **Ambiguity** | Create Clarity-reducing conditions | CAF Scoring v2 (Clarity) | CAF-T3/T4/T8; EXPL-T1 |
| **Assumption** | Exercise unsupported/invalid assumptions | CAF Scoring v2 (affected dimension) | CAF-T3/T5; EXPL-T4/T5 |
| **Conflict** | Drive Alignment reduction & Deep-pass decreases | CAF Scoring v2 (Alignment) + Confidence v2 | FD-T4/T5; CONF-T5; INV-T1 |
| **Feasibility** | Create Feasibility-reducing conditions | CAF Scoring v2 (Feasibility) | CAF-T3; CONF-T1 |
| **Reliability — Coverage** | Vary breadth of observable surface | Reliability v2 (Coverage) | REL-T1/T6; CONF-T4 |
| **Reliability — Evidence** | Vary evidence availability | Reliability v2 (Evidence Availability) | REL-T2/T6 |
| **Reliability — Assessability** | Exercise gating & non-collapse | Reliability v2 (Assessability) | REL-T3/T5; INV-T3 |
| **Confidence consolidation** | Exercise consolidate-then-qualify (strength + weakness mix) | Confidence v2 | CONF-T1/T2/T4 |
| **Fast/Deep** | Provisional → supersede; rise & fall | All three v2 models | FD-T1…T6; HIST-T*; REPLAY-T* |
| **Replay/Determinism** | Stable, pinned inputs for reconstruction | All three v2 models | REPLAY-T1…T6; DET-T1…T3 |

*(Families correspond to the §4 taxonomy plus the cross-cutting consolidation/replay families the test spec requires.)*

---

## 11. Determinism Support

- **Why fixtures must remain stable.** Determinism tests assert that identical inputs under a pinned configuration yield **equivalent governable outputs**; if the fixture inputs drift, the test cannot distinguish a real regression from a fixture change.
- **Why determinism testing depends on fixture stability.** A determinism/regression result is only meaningful relative to a **fixed input baseline** — the fixture is that baseline.
- **Why fixture modifications create new baselines.** Changing an **Active** fixture changes the baseline; the change is a **new versioned fixture** and a **new baseline**, never an in-place edit — so prior results remain interpretable and a baseline update is not mistaken for a regression.
- **Tolerance.** The bounded-equivalence **tolerance value is not defined here** — "Deferred to Determinism Calibration Note" (Section 15).

---

## 12. Explainability Support

Every fixture MUST permit full reconstruction of:
- **CAF basis** — dimension assessments + contributing findings + impact assessments;
- **Reliability basis** — coverage/evidence/assessability + independence statement;
- **Confidence basis** — CAF basis + reliability basis + cause-of-level;
- **Change attribution** — what moved a state (CAF and/or reliability change);
- **Supersession history** — the chain a fixture run produces.

**No opaque fixture is allowed** — a fixture whose expected behavior cannot be explained to basis is non-conformant. (Supports EXPL-T1…T7.)

---

## 13. Fast vs Deep Support

Required fixture families to validate Fast/Deep behavior:
- **Confidence increases** — a Fast→Deep fixture where Deep resolves ambiguity / adds coverage (drives FD-T3).
- **Confidence decreases** — a Fast→Deep fixture where Deep discovers a contradiction lowering CAF (drives FD-T4).
- **Deeper understanding** — Deep-analysis fixtures that demonstrably enrich the understanding (Deep Analysis Fixtures, §4).
- **Contradiction discovery** — conflict fixtures whose contradiction is hidden at Fast horizon and surfaced at Deep.
- **Supersession** — fixtures producing a Fast state then a Deep state that supersedes it (drives FD-T2/T6; HIST-T*).

These families must collectively demonstrate the doctrine principle: **confidence may decrease as understanding improves** — a Deep-pass decrease is **discovery, not deterioration**, with the prior (higher) state retained in history.

---

## 14. Conformance Requirements

Structural conformance (**no percentages, no thresholds**) — the fixture library conforms when:
- **FC-1.** **Every fixture is classified** into a Section 4 category.
- **FC-2.** **Every fixture is traceable** bidirectionally to doctrine/calibration/model rules/tests (Section 7).
- **FC-3.** **Every fixture is deterministic** and configuration-pinned (Section 6/11).
- **FC-4.** **Every fixture is explainable** — full basis reconstructable; no opaque fixture (Section 12).
- **FC-5.** **Every fixture carries all required structure** (Section 5 components).
- **FC-6.** **Every fixture is doctrine-valid** — consistent with, and contradicting none of, the authoritative layers.
- **FC-7.** **Coverage:** every Integrity Rule and cross-model invariant the test spec validates has **at least one** covering fixture (no uncovered rule).
- **FC-8.** **Lifecycle integrity:** changes to Active fixtures occur as new versions/baselines (append-only); nothing overwritten.

---

## 15. Deferred Items

Explicitly **deferred** (not created or assumed here):
- **Actual fixture data** — the concrete inputs and expected-output content → fixture authoring (post-approval).
- **Calibration values** — band/scale boundaries, magnitudes → the v2 calibration appendices.
- **Tolerance values** — bounded-equivalence/determinism bound → **Determinism Calibration Note**.
- **Implementation formats** — file/storage/encoding formats for fixtures → implementation.

These deferrals affect **content and numeric bounds only**; the **framework** (structure, governance, lifecycle, traceability, conformance) is defined and enforceable now.

---

*This document defines the canonical Release 1 fixture framework for validating the CAF → Reliability → Confidence subsystem. It creates no doctrine, calibration, or fixture data, introduces no numerics, and defers all content and tolerance values. It is the authoritative reference for how Confidence-subsystem fixtures are categorized, structured, governed, and traced.*

**Release 1 Confidence Fixture Library Specification complete.**
