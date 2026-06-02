# Reliability Model v2

**Type:** Implementation-model artifact (L4 realization) — realizes Reliability doctrine + calibration; creates none
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits alongside:** `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md`
**Sits below (authoritative — must implement, must not modify):** Reliability Model v1 · `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md`
**Realizes / consistent with (not modified):** CAF Assessment · CAF Scoring · Confidence Models · Planning Intelligence · Analysis Engine · Data Model v1.1 · State/Event Models. **Stack position:** `OUTCOME_CONFIDENCE_STACK_INDEX.md` (L4).

> **Non-negotiable.** This document **realizes** approved Reliability doctrine and calibration as an operational model. It does **not** redefine Outcome Confidence, CAF, Clarity, Alignment, or Feasibility; introduces **no** probability, prediction, project-health, readiness, governance, executive-decision, new-dimension, new-finding, new-entity, new-state, or new-event concepts; and introduces **no formulas, weights, thresholds, percentages, scoring equations, or arithmetic.** Where evidence is insufficient it states **"Deferred to future calibration."** Whenever a choice arises between adding a concept and preserving doctrine, **doctrine is preserved.**

---

## 1. Purpose

Reliability Model v2 specifies, at the **model level**, what **Assessment Reliability** represents, how it is assessed from **Coverage, Evidence Availability, and Assessability**, how it evolves, explains itself, and supersedes, how it **supports** Outcome Confidence, and what it may and may not influence. It is the authoritative implementation/testing reference for Reliability behavior.

---

## 2. Scope

**In scope:** the conceptual operating model for Assessment Reliability — its representation, the High/Moderate/Low semantics, the Coverage / Evidence Availability / Assessability sub-models, the (non-arithmetic) determination framework, evolution, explanation, history, integrity rules, the Reliability→Confidence interface, and conformance.

**Out of scope (Deferred to future calibration / owned elsewhere):** the numeric reliability scale and its boundaries, the arithmetic combining the three inputs, the *degree* to which low reliability holds confidence expression back, Confidence synthesis (Confidence Model v2), CAF scoring (CAF Scoring Model v2), severity, UI, governance, environmental signals (out of Release 1), and any probability/outcome construct. **CAF, Confidence, and their meanings are consumed, not defined here.**

---

## 3. Model Relationships

```text
Observable evidence surface
   ├─ Coverage              (breadth of the surface)
   ├─ Evidence Availability (presence of supporting evidence)
   └─ Assessability         (whether the understanding can be assessed at all)
                 │  (read independently of CAF and of findings)
                 ▼
          Assessment Reliability  (qualitative qualifier: High / Moderate / Low)
                 │  (qualifies — does not replace, summarize, or alter)
                 ▼
   Confidence Model v2:  Confidence = consolidate(CAF) THEN qualify(by Reliability)
```

**Critical relationships preserved (Critical Requirement):**
- **CAF → Confidence** and **Reliability → Confidence** — both feed Confidence.
- **CAF ≠ Reliability** — CAF measures *strength of understanding*; Reliability measures *supportability of the assessment*. Different questions, different inputs.
- **Confidence ≠ Reliability** — Confidence is the consolidated trust signal; Reliability is one qualifying input to it.
- **Reliability qualifies confidence without becoming confidence** — it is a qualifier, never a second confidence score.

Reliability is assessed **per analysis run** and travels with that run's existing states (the per-dimension reliability qualifier on `CAFState`, and the overall `reliability_qualifier` on `ConfidenceState`) — **no new entity, state, or event** is introduced. Findings act on CAF, **never** on Reliability.

---

## 4. Reliability Representation

Assessment Reliability is represented as a **qualitative qualifier** with an available **basis** — never a co-score:

1. **Reliability level** — one of **High · Moderate · Low** (Calibration CAL-REL-1). The qualifier itself.
2. **Basis** — the **Coverage, Evidence Availability, and Assessability** conditions that account for the level (Section 11). Always available.

Reliability is **not** an index parallel to CAF or Confidence, **not** a weighting, and **not** a number to be combined arithmetically with CAF. It is a **statement about the supportability of the assessment**, carried as a qualifier on the per-run states. The **numeric scale and its boundaries are Deferred to future calibration** (Section 16).

---

## 5. Reliability Semantics

Conceptual regions — **no thresholds or percentages**; boundaries **Deferred to future calibration**. Realizing Reliability Model v1 §2/§10:

- **High Reliability** — the assessment was made across a **broad, well-evidenced, and fully assessable** surface; OSLO can **fully vouch** for the assessment it has made. The signal it qualifies is **stable**.
- **Moderate Reliability** — the assessment rests on **partial** support: coverage, evidence, or assessability is meaningful but incomplete; OSLO can vouch for the assessment **with reservation**.
- **Low Reliability** — the assessment rests on a **narrow surface, little available evidence, or limited assessability**; OSLO can **only partly** vouch for it, and uncertainty is **preserved** in what the reliability qualifies.

Reliability describes the **supportability of the assessment** — *not* project quality and *not* OSLO's quality (Reliability Model v1 §5).

---

## 6. Coverage Model

- **What Coverage means.** The **breadth of the observable evidence surface** — the degree to which the relevant aspects of project reality have observable evidence available to OSLO.
- **Poor coverage.** Significant portions of the relevant surface were **not observable**; the assessment was made over a **partial view**.
- **Broad coverage.** **Most of what matters** could be seen; the assessment drew on a wide surface.
- **How Coverage affects Reliability.** Broadening coverage — bringing previously-unobserved aspects into view — **raises** reliability; narrow coverage **lowers** it. Coverage is the **breadth** condition of reliability.

---

## 7. Evidence Availability Model

- **What Evidence Availability means.** The **presence and accessibility of observable evidence** that supports the assessment — whether evidence bearing on the understanding actually exists and is available to OSLO.
- **Limited evidence.** The understanding rests on **little observable evidence**, even where the surface is nominally in view.
- **Abundant evidence.** The understanding is **backed by ample observable evidence** OSLO can draw upon.
- **How Evidence Availability affects Reliability.** Adding available, supporting evidence **raises** reliability; sparse evidence **lowers** it. Where Coverage concerns *breadth of surface*, Evidence Availability concerns the **presence of supporting evidence within it**.

---

## 8. Assessability Model

- **What Assessability means.** The degree to which the **understanding is in a state that can be confidently assessed at all** — whether it can be examined and supported or challenged by evidence.
- **Why it differs from Coverage.** Coverage is about **how much of the surface is observable**; Assessability is about whether the **understanding itself can be evaluated**, independent of how broad the surface is.
- **Why it differs from Evidence Availability.** Evidence Availability is about **whether supporting evidence is present**; Assessability is about whether the understanding is **in a form that evidence can even be brought to bear on**. Evidence can be abundant yet the understanding still not assessable.
- **Why Assessability acts as a constraint.** Assessability **determines whether Coverage and Evidence Availability can be applied at all**. **Low assessability constrains Reliability regardless** of how broad coverage is or how much evidence is available — if the understanding cannot be confidently assessed, neither breadth nor evidence can rescue the reliability of the assessment.

---

## 9. Reliability Determination Framework

Realizes Reliability Model v1 §6 + Calibration "Reliability Treatment" (CAL-REL-2) — **conceptual, no arithmetic**:

- **All three inputs participate; none is ignored.** Reliability is read from **Coverage, Evidence Availability, and Assessability** together.
- **Assessability gates.** **Low assessability constrains reliability regardless** of the other two (Section 8).
- **Read from surface conditions, not from findings.** Reliability is computed from the **conditions of the observable evidence surface**, *not* from the findings derived from it and *not* from CAF (determined **independently**, Reliability Model v1 §6).
- **Non-collapse respected.** Reliability qualifies how fully CAF strength is **expressed** in Confidence, but **must never, by itself, collapse a strong CAF to the lowest confidence state** (Reliability Non-Collapse Invariant; Confidence Model v2 §6/§12). Reliability constrains **expression within bounds**, never to the floor on its own.

**The way the three inputs combine into a level is fixed *in character* here; the arithmetic that produces a specific level is Deferred to future calibration** — and any such realization must preserve the gating role of Assessability and the Non-Collapse Invariant.

---

## 10. Reliability Evolution Model

Reliability changes only when its **surface conditions** change (Reliability Model v1 §6/§10):

- **Increasing Reliability** — coverage **broadens**, supporting **evidence is added/becomes accessible**, or the understanding becomes **more assessable**.
- **Decreasing Reliability** — coverage **narrows**, evidence becomes **less available**, or assessability **falls**.
- **Stable Reliability** — **no change** in Coverage, Evidence Availability, or Assessability.

**Legitimate movement.** Reliability may move **only** because one of its three inputs changed — and it **may move while CAF is unchanged** (added evidence makes the *same* assessment better supported; Reliability Model v1 §5, Example C).

**Prohibited movement.** Reliability **must not** move because **CAF changed**, because a **finding's severity** changed, or because **Confidence** changed. Findings influence CAF; the three surface conditions influence Reliability. Reliability has **no other source of movement**.

---

## 11. Reliability Explanation Model

Every reliability assessment MUST make these explanation components **available** (realizing Reliability Model v1 §11):

1. **Coverage basis** — how broad the observable evidence surface was for the assessment.
2. **Evidence basis** — how much observable supporting evidence stood behind it.
3. **Assessability basis** — the degree to which the understanding could be confidently assessed at all.
4. **Independence statement** — that the level was determined from these **surface conditions, not from CAF and not from findings** (it never attributes a reliability level to the strength of understanding or to any finding).
5. **Supersession context / change attribution** — what last moved reliability (which of Coverage / Evidence Availability / Assessability changed), and that **CAF need not have moved with it**.

A reliability assessment for which any required component cannot be produced is **non-conformant** (Section 13). The explanation **reduces to its basis**, never to a number or formula.

---

## 12. Reliability History Model

Using existing state concepts only — **no new entity, state, or event**. Reliability is assessed **per analysis run** and is carried on that run's existing states (per-dimension on `CAFState`; overall `reliability_qualifier` on `ConfidenceState`):

- **Current reliability assessment** — the reliability carried on the **current** run's states; the supportability in effect now.
- **Superseded reliability assessment** — the reliability carried on a **prior** run's states, replaced when a newer run supersedes; **retained**, never deleted.
- **Historical reliability assessment** — the reliability across the **supersession chain** of those per-run states.

**Interpretation.** Reliability history is read as the **evolution of how well-supported OSLO's assessments have been over time** — each change attributable to a Coverage / Evidence Availability / Assessability change (Section 11). Because reliability can move while CAF does not, the reliability history and the CAF history are **distinct chains** that need not move together.

---

## 13. Reliability Integrity Rules

*Authoritative testing reference. Each realizes existing doctrine; none is new doctrine.*

- RR-1. Reliability derives **only** from **Coverage, Evidence Availability, and Assessability**. No other input.
- RR-2. Reliability is **determined independently of CAF** and is **not directly influenced by findings** (incl. finding severity).
- RR-3. Reliability **never alters CAF** and never alters a CAF dimension.
- RR-4. Reliability **qualifies** Confidence; it **never replaces, summarizes, or substitutes for** Confidence.
- RR-5. Reliability is **not a co-score and not a weighting** — it is a qualifier, not a parallel signal.
- RR-6. **Low Assessability constrains** reliability regardless of Coverage or Evidence Availability.
- RR-7. **Reliability Non-Collapse:** reliability **alone** must never collapse a strong CAF to the **lowest** confidence state.
- RR-8. Reliability **may change while CAF is unchanged**; it **must not** change because CAF, finding severity, or Confidence changed.
- RR-9. Reliability MUST be **explainable** through Coverage, Evidence, Assessability basis + independence statement + change attribution; it MUST NOT be opaque.
- RR-10. A new reliability assessment MUST **supersede** (not overwrite) the prior (via the per-run state chain); superseded reliability MUST be **retained**.

---

## 14. Relationship To Confidence

- **How Reliability supports Confidence.** Confidence is derived from **CAF qualified by Reliability** (consolidate-then-qualify). Reliability provides the **qualification** — governing **how fully the consolidated CAF strength is expressed** in the confidence signal (Confidence Model v2 §6/§7).
- **What Reliability contributes.** A **trust qualifier**: how much the CAF assessment can be vouched for, given the observable surface.
- **What Reliability cannot contribute.** It contributes **no strength assessment** (that is CAF), **no consolidated signal** (that is Confidence), and **no second score**.
- **Why Reliability qualifies confidence.** Because strong understanding that is thinly supported should read more cautiously than the same understanding well supported — qualification is exactly how that caution enters the signal **without** changing CAF.
- **Why Reliability never replaces confidence.** Confidence is the **summary** of CAF qualified by Reliability; Reliability is **one input**, not the summary.
- **Why Reliability never becomes a second confidence score.** Reliability answers a **different question** ("how trustworthy is the assessment?") than Confidence ("how confident should we be in our understanding?"). Treating it as a parallel confidence signal would conflate the two and is **prohibited** (RR-4/RR-5).

---

## 15. Conformance Requirements

A conforming implementation MUST satisfy **all** Reliability Integrity Rules (Section 13) and, additionally:

- **C-1.** Assess reliability **per analysis run** from Coverage / Evidence Availability / Assessability, carried as the qualifier on that run's `CAFState`/`ConfidenceState` (no new entity).
- **C-2.** Surface the reliability **basis** (coverage/evidence/assessability + independence + change attribution) on demand, without recomputation (lineage stored).
- **C-3.** Guarantee reliability **does not move** on a CAF change, a finding/severity change, or a Confidence change (testable against RR-2/RR-8).
- **C-4.** Allow reliability to **move while CAF is unchanged** when a surface condition changes (testable against RR-8 / Example C).
- **C-5.** Enforce **Assessability gating** (RR-6) and **Non-Collapse** (RR-7) — a strong CAF under low reliability MUST NOT yield the lowest confidence state from reliability alone.
- **C-6.** Set the supersession (per-run state) chain and retain prior reliability assessments (RR-10).
- **C-7.** Reject (as a defect) any reliability assessment that is unexplainable, that alters CAF, that acts as a confidence substitute/second score, or that is driven by findings/CAF/Confidence.

These map directly to the Testing Strategy's reliability, determinism, replay, and traceability suites.

---

## 16. Open Items Deferred To Future Calibration

The following are **Deferred to future calibration** — this model fixes their *structure and constraints*, not their values:

- **Reliability scale boundaries** — where the High / Moderate / Low boundaries fall (Sections 4–5). *Deferred.*
- **Determination combination** — the (non-formula) realization combining Coverage / Evidence Availability / Assessability into a level (Section 9), preserving Assessability gating and Non-Collapse. *Deferred.*
- **Qualification degree** — how far low reliability holds confidence expression back, within the Non-Collapse bound (owned jointly with Confidence Model v2 §6). *Deferred.*
- **Input gradation** — what separates poor/broad coverage, limited/abundant evidence, and low/high assessability (Sections 6–8). *Deferred.*
- **Environmental signals** — explicitly **out of Release 1** (Reliability Model v1 §12); any future inclusion requires future doctrine. *Deferred.*

None of these may, when resolved, alter the Reliability doctrine (independence from CAF/findings/confidence; qualifies-not-replaces; Assessability gating; Non-Collapse) or any higher-layer meaning/calibration. CAF and Confidence remain **distinct** from Reliability (Critical Requirement).

---

*Reliability Model v2 realizes the approved Reliability doctrine and calibration as an operational model. It redefines nothing above it, introduces no arithmetic/thresholds/weights/probability/new doctrine, creates no new dimensions/findings/entities/states/events, and defers all numeric calibration. It preserves CAF → Confidence and Reliability → Confidence while keeping CAF ≠ Reliability and Confidence ≠ Reliability — Reliability qualifies confidence without becoming confidence. It is the implementation/testing reference for Reliability behavior in Release 1.*

**Reliability Model v2 complete.**
