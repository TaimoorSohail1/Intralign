# CAF Scoring Model v2

**Type:** Implementation-model artifact (L4 realization) — realizes CAF doctrine + calibration; creates none
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — must implement, must not modify):** CAF Assessment Model · CAF Scoring Model v1 · `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md` · `CONFIDENCE_MODEL_V2.md`
**Realizes / consistent with (not modified):** Reliability Model · Planning Intelligence · Analysis Engine · Data Model v1.1 · State/Event Models. **Stack position:** `OUTCOME_CONFIDENCE_STACK_INDEX.md` (L4).

> **Non-negotiable.** This document **realizes** approved CAF doctrine and calibration as an operational model. It does **not** redefine Clarity, Alignment, Feasibility, Outcome Confidence, or Reliability; introduces **no** new dimensions, findings, entities, states, events, probability, prediction, project-health, governance, or executive-decision concepts; and introduces **no arithmetic, formulas, thresholds, percentages, weighting, or scoring equations.** Where evidence is insufficient it states **"Deferred to future calibration."** Whenever a choice arises between adding a concept and preserving doctrine, **doctrine is preserved.**

---

## 1. Purpose

CAF Scoring Model v2 specifies, at the **model level**, how CAF expresses the **integrity of project understanding** across its three dimensions: what strength and weakness mean, how findings (via Impact Assessment) shape each dimension, how CAF evolves, supersedes, explains itself, preserves history, behaves across Fast/Deep, and **supports** (but is never altered by) Confidence. It is the authoritative implementation/testing reference for CAF behavior.

---

## 2. Scope

**In scope:** the conceptual operating model for the `CAFState` — per-dimension representation, strength/weakness semantics, Impact-Assessment realization, finding contribution, evolution, explanation, history, Fast/Deep behavior, integrity rules, the CAF→Confidence interface, and conformance.

**Out of scope (Deferred to future calibration / owned elsewhere):** the numeric index range, band boundaries, the magnitude arithmetic of a finding's reducing contribution, Reliability's overall determination (owned by the Reliability Model), Confidence synthesis (owned by Confidence Model v2), severity numerics, UI, governance, and any probability/outcome construct. **CAF dimensions and Confidence/Reliability meaning are consumed, not defined here.**

---

## 3. Model Relationships

```text
Evidence ─▶ Inference ─▶ Findings ─▶ Impact Assessment
                                        │  (modulates each finding's reducing contribution)
                                        ▼
                        CAF (three independent, co-equal dimensions)
                        ├─ Clarity      (integrity index · band · reliability qualifier)
                        ├─ Alignment    (integrity index · band · reliability qualifier)
                        └─ Feasibility  (integrity index · band · reliability qualifier)
                                        │  (CAF provides dimension assessments — does NOT consolidate)
                                        ▼
                        Confidence Model v2  (consolidate-then-qualify)
```

CAF is produced **per analysis run** (`CAFState`). Findings reach CAF **only through Impact Assessment**; they never touch Confidence directly. CAF **provides** the three dimension assessments to Confidence and is **never altered by** Confidence or Reliability (no feedback). Entities/fields are the existing Data Model v1.1 ones — **none new**.

---

## 4. CAF Representation

Each dimension is represented as a **triple** (realizing CAF Scoring v1 §3), never a bare number:

1. **Integrity index** — a bounded integrity signal for that dimension (an **integrity signal, not a probability or percentage of completion**). Subordinate to the band.
2. **State band** — a qualitative label (**Very Low · Low · Moderate · High · Very High**; Master Spec §3) — the primary human-legible expression.
3. **Reliability qualifier** — how **completely the dimension could be assessed** given current coverage (per-dimension; CAF Scoring v1 §3).

A `CAFState` carries this triple for **each** of Clarity, Alignment, Feasibility. **A bare index is never a complete CAF score** (a high index under low reliability means something materially different from the same index under high reliability). The **numeric range and band boundaries are Deferred to future calibration** (Section 16).

*(Note: the per-dimension reliability qualifier here is the coverage-governed completeness of that dimension's assessment. The **overall Assessment Reliability** that qualifies Outcome Confidence is determined independently by the **Reliability Model** and is not owned by CAF.)*

---

## 5. CAF Strength Semantics

Strength is the **assessed integrity** of a dimension — described as qualitative regions, **no thresholds or percentages**; boundaries **Deferred to future calibration**. Grounded in the dimension definitions (CAF Assessment §3) and the finding-reduces-integrity principle (CAF Scoring v1 §4):

**Clarity** — integrity of how clearly project reality is understood.
- *Weak:* pervasive ambiguity and/or missing information; claims ill-formed or admitting multiple material readings.
- *Moderate:* substantially clearer, but notable unclarity remains.
- *Strong:* claims precise, well-formed, and unambiguous, with little unresolved unclarity.

**Alignment** — integrity of coherence between project elements and intended outcomes.
- *Weak:* significant conflicts among elements and/or drift from intent.
- *Moderate:* broadly coherent, with some unresolved misalignment.
- *Strong:* elements coherent with the intent and with one another.

**Feasibility** — integrity of the understanding that intended outcomes are realistically achievable.
- *Weak:* significant constraints and/or coverage gaps undermining achievability.
- *Moderate:* achievable understanding, with notable constraints or gaps remaining.
- *Strong:* no material constraint or gap is left unaddressed; the plan, as understood, is plausibly achievable.

*Strength is a statement about the **integrity of understanding**, never about project quality, health, or outcome (CAF Assessment §2).*

---

## 6. CAF Weakness Semantics

Weakness in a dimension is the presence of a finding's **reducing contribution** to that dimension (CAF Scoring v1 §4). As model concepts — **no quantification**:

- **Weakness** — any reducing contribution present on the dimension; the dimension's integrity is lowered to some degree.
- **Meaningful weakness** — a reducing contribution large enough to **materially lower** the dimension's assessed integrity (driven by the finding's Impact Assessment, not its type).
- **Material weakness** — a meaningful weakness **significant and/or pervasive enough that it must be felt** in the consolidated confidence signal — i.e., it is the kind of weakness constrained aggregation may not average away (Confidence Model v2 §5/§7 consumes this notion).

**Why some weaknesses constrain understanding more than others.** The constraining force of a weakness is governed by its **Impact Assessment** — chiefly **significance** (how strongly it lowers integrity) and **scope** (how much of the dimension's surface it affects) — **not** by the finding's type. A localized, low-significance ambiguity constrains far less than a pervasive, high-significance conflict, even though both are "findings." **This is conceptual; the magnitude that separates weakness / meaningful / material is Deferred to future calibration.**

*This model is the authoritative source for "material weakness"; Confidence Model v2 consumes the term without redefining it.*

---

## 7. Impact Assessment Model

The Impact Assessment is the **modulator** that turns a finding into a **sized, located, firm** reducing contribution (realizing CAF Scoring v1 §5). Its factors govern CAF as follows — **no formula**:

| Impact Assessment factor | What it governs in CAF |
|---|---|
| **Significance** | The **magnitude** of the reducing contribution — how strongly the finding lowers the affected dimension's integrity. |
| **Affected CAF Dimensions** | The **locality** — which dimension(s) receive a contribution (one or more). |
| **Evidence Support** | The **firmness** — how well-established the contribution is (a thinly-evidenced finding contributes a less firm reduction than a well-evidenced one). |
| **Scope of Impact** | The **breadth** — how much of the dimension's surface is affected (localized vs pervasive). |

These four factors **jointly** determine each finding's contribution to each affected dimension. **Which factor governs which property is fixed here; the arithmetic that combines them is Deferred to future calibration.** Because magnitude flows entirely from Impact Assessment, **recording a finding is separate from assessing its impact**: a finding may exist with no settled effect until its Impact Assessment is performed, and re-assessing impact changes the dimension without the finding itself changing.

---

## 8. Finding Contribution Model

Realizes CAF Scoring v1 §4 — **direction and locality fixed, magnitude derived**:

- **Why findings reduce integrity.** A finding is an observation of a gap, conflict, assumption, or limitation in understanding; its **presence reduces** the affected dimension's integrity and **never raises** it. *Resolving* a finding **withdraws or lessens** its reducing contribution, which is how a dimension's integrity rises (the other way being evidence that strengthens understanding).
- **How findings contribute.** Each finding contributes a **reducing contribution** to **each dimension named in its Impact Assessment**, sized by that Impact Assessment.
- **Why finding type does not determine contribution.** Finding **type is a label**, not a coefficient or weight. Two findings of the same type may contribute very differently, and one type may affect different dimensions in different cases — entirely per each finding's Impact Assessment.
- **Why contribution must be local to affected dimensions.** A finding contributes to a dimension **only if** that dimension appears as an Affected Dimension in its Impact Assessment. This **preserves dimension independence** (CAF Assessment §3): cross-dimension movement occurs only where a finding's own assessment declares it.

---

## 9. CAF Evolution Model

CAF changes only on **evidence or finding change** (event-driven; CAF Scoring v1 §2 "scores recompute only on evidence or finding change"):

- **Strengthening CAF** — evidence strengthens the understanding, and/or a finding's reducing contribution is **removed or lessened** (resolution, or a reduced Impact Assessment).
- **Weakening CAF** — a **new or worsened** finding adds/increases a reducing contribution, and/or an Impact Assessment grows in significance/scope.
- **Stable CAF** — **no change**, because neither evidence nor findings (nor their Impact Assessments) changed.

**Legitimate CAF movement** is exactly movement caused by an evidence change or a finding/Impact-Assessment change — and **nothing else**. CAF does **not** move on the passage of time, on Confidence, or on Reliability.

---

## 10. CAF Explanation Model

Every `CAFState` MUST, by construction, make these explanation components **available** (realizing CAF Scoring v1 §3 + the Explainability Invariant inherited from the stack):

1. **Dimension assessments** — the triple (index · band · reliability qualifier) for **each** of Clarity, Alignment, Feasibility; none omitted.
2. **Contributing findings** — the findings contributing a reducing contribution to each dimension.
3. **Impact assessments** — for each contributing finding, the Impact Assessment that sized and located its contribution (significance · affected dimensions · evidence support · scope).
4. **Supersession context** — the prior `CAFState` this one superseded (if any) and **what changed** (which evidence or finding moved which dimension) — change attribution.

A CAF assessment for which any required component cannot be produced is **non-conformant** (Section 13). Explanation **reduces to basis** — the findings, impact assessments, and evidence that account for each dimension — **never to a formula**.

---

## 11. CAF History Model

Using existing State Model concepts (State Model §9 CAF lifecycle; Data Model v1.1 `CAFState` per run) — **no new states**:

- **Current CAF assessment** — the latest `CAFState` for the project; the assessment in effect now.
- **Superseded CAF assessment** — a prior `CAFState` replaced by a newer one; **retained**, never deleted.
- **Historical CAF assessment** — any `CAFState` in the chain; the chain **is** the CAF history.

**Interpretation:** the chain is read as the **evolution of understanding integrity over time**, each link attributable to an evidence or finding change (Section 9). History is **append-only via supersession**; it is a record of how understanding's integrity matured, never a project-health timeline.

---

## 12. Fast vs Deep CAF

Using existing doctrine (Planning Intelligence §16–§18; Analysis Engine §9/§10) — `run_type` distinguishes runs; **no new concepts, no governance**:

- **Fast Analysis CAF** — an **initial** `CAFState` over the shallow fast-horizon understanding. **Clarity** is substantially assessable; **Alignment** and **Feasibility** are **preliminary** and typically carry a **lower per-dimension reliability qualifier**, because relational evaluation is deferred to Deep.
- **Deep Analysis CAF** — a **reassessed** `CAFState` over the enriched understanding, which **supersedes** the Fast CAF.
- **Why Deep CAF may strengthen** — deeper analysis can resolve ambiguity, validate assumptions, and broaden coverage, **withdrawing/lessening** reducing contributions and raising dimensions.
- **Why Deep CAF may weaken** — deeper analysis can **surface previously-hidden findings** (deeper assumptions, contradictions) whose Impact Assessment adds reducing contributions, **lowering** dimensions even though the project did not worsen.
- **Why Deep CAF supersedes Fast CAF** — Deep produces a **fuller, better-supported** assessment; supersession preserves the Fast CAF in history (Section 11). This underwrites the downstream principle that **confidence may decrease as understanding improves** (Confidence Model v2 §11).

---

## 13. CAF Integrity Rules

*Authoritative testing reference. Each realizes existing doctrine; none is new doctrine.*

**Dimensions**
- CR-1. CAF consists of **exactly** Clarity, Alignment, Feasibility. No new dimension.
- CR-2. Dimensions are **independent** — one dimension's integrity does not, by structure, determine another's.
- CR-3. Dimensions are **co-equal** — no hierarchy, no ordering, **no weighting**.

**Findings & Impact Assessment**
- CR-4. Finding **type is never a coefficient or weight**; it is a label only.
- CR-5. A finding contributes **only to its Affected Dimensions** (Impact Assessment), never to others.
- CR-6. A finding's **direction is always reducing**; integrity rises only via evidence strengthening or via removal/lessening of a reducing contribution.
- CR-7. A finding's **magnitude derives from its Impact Assessment**, never from its type.
- CR-8. Recording a finding is **separate** from assessing its impact; impact may be (re)assessed without the finding changing.

**Evolution**
- CR-9. CAF **recomputes only** on an evidence change or a finding/Impact-Assessment change. No time-based, Confidence-based, or Reliability-based movement.

**Boundaries**
- CR-10. **Reliability does not alter CAF** (it is determined independently and qualifies Confidence, not CAF).
- CR-11. **Confidence does not feed back into CAF** and never alters a dimension.
- CR-12. CAF is an **integrity** signal — never probability, prediction, project-health, or readiness.

**Explainability & history**
- CR-13. Every `CAFState` MUST be **explainable** through dimension assessments, contributing findings, impact assessments, and supersession context.
- CR-14. A new `CAFState` MUST **supersede** (not overwrite) the prior; superseded states MUST be **retained**; the chain MUST reconstruct CAF history.

---

## 14. Relationship To Confidence

- **What CAF provides:** the **three independent, co-equal dimension assessments** (each a triple) that Confidence consolidates. CAF is the **primary assessment layer**.
- **What CAF does not provide:** CAF does **not** consolidate the dimensions into one signal, does **not** determine overall Assessment Reliability, and does **not** produce Outcome Confidence — those are owned by Confidence Model v2 and the Reliability Model respectively.
- **Why Confidence consumes CAF:** Outcome Confidence is **derived from CAF** (qualified by Reliability) via consolidate-then-qualify; everything upstream of CAF (evidence, inference, findings, impact assessment) reaches Confidence **only through CAF**.
- **Why Confidence cannot modify CAF:** Confidence is a **downstream consumer**; it never overrides a dimension and never feeds back. The boundary is one-directional: **CAF → Confidence**, never the reverse.

*No new doctrine — this restates the consume-not-alter relationship the stack already fixes.*

---

## 15. Conformance Requirements

A conforming implementation MUST satisfy **all** CAF Integrity Rules (Section 13) and, additionally:

- **C-1.** Produce one `CAFState` per completed analysis run, carrying the triple for **each** of the three dimensions.
- **C-2.** Apply each finding's reducing contribution **only** to its Impact-Assessment-declared dimensions, sized by Impact Assessment (not type).
- **C-3.** Recompute CAF **only** on an evidence or finding/Impact-Assessment change (testable against CR-9).
- **C-4.** Keep dimensions independently calculated; a change confined to one dimension's findings MUST NOT move another dimension (testable against CR-2/CR-5).
- **C-5.** Surface the full explanation (dimension assessments + contributing findings + impact assessments + supersession context) without recomputation (lineage stored).
- **C-6.** Set the supersession pointer on each reassessment and retain prior `CAFState`s.
- **C-7.** Reject (as a defect) any `CAFState` that is unexplainable, that lets finding type act as a coefficient, that moves a dimension without a valid cause, or that is altered by Reliability or Confidence.
- **C-8.** Provide the three dimension assessments to Confidence Model v2 **without** itself consolidating or qualifying them.

These map directly to the Testing Strategy's CAF, determinism, replay, and traceability suites.

---

## 16. Open Items Deferred To Future Calibration

The following are **Deferred to future calibration** — this model fixes their *structure and constraints*, not their values:

- **Integrity index range and band boundaries** (Sections 4–5). *Deferred.*
- **Magnitude of a finding's reducing contribution** — the arithmetic combining significance / evidence support / scope (Section 7), preserving CR-4/CR-7. *Deferred.*
- **Weakness gradation boundaries** — what separates weakness / meaningful / material weakness (Section 6). *Deferred.*
- **Per-dimension reliability-qualifier boundaries** (coverage-governed; Section 4). *Deferred (and the overall Assessment Reliability is owned by the Reliability Model).*
- **Severity numerics** — severity meaning is owned by the Calibration doctrine; numeric basis. *Deferred.*

None of these may, when resolved, alter the CAF doctrine (independence, co-equality, no weighting, type-not-coefficient, locality, reducing-direction) or any higher-layer meaning/calibration. Confidence and Reliability remain **consumers/independent** per the stack.

---

*CAF Scoring Model v2 realizes the approved CAF doctrine and calibration as an operational model. It redefines nothing above it, introduces no arithmetic/thresholds/weights/probability/new doctrine, creates no new dimensions/findings/entities/states/events, and defers all numeric calibration. It is the implementation/testing reference for CAF behavior in Release 1.*

**CAF Scoring Model v2 complete.**
