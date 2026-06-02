# Confidence Model v2

**Type:** Implementation-model artifact (L4 realization) — realizes doctrine + calibration; creates none
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — must implement, must not modify):** `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md`
**Realizes / consistent with (not modified):** Confidence Model · CAF Assessment · CAF Scoring · Reliability Models · Planning Intelligence · Analysis Engine · Data Model v1.1 · State/Event Models.
**Stack position:** see `OUTCOME_CONFIDENCE_STACK_INDEX.md` (L4).

> **Non-negotiable.** This document **realizes** approved doctrine and calibration as an operational model. It does **not** redefine Outcome Confidence, CAF, or Reliability; introduces **no** probability, prediction, project-health, governance, executive-decision, or automation concepts; and creates **no** new entities, states, events, or dimensions. It introduces **no arithmetic, thresholds, percentages, or weights** — those remain calibration (Section 14). Where evidence is insufficient, it states **"Deferred to future calibration."** Whenever a choice arises between adding a concept and preserving doctrine, **doctrine is preserved.**

---

## 1. Purpose

Confidence Model v2 specifies, at the **model level**, how Outcome Confidence is **represented, evolved, superseded, explained, and preserved**, how **reliability qualifies** it, and how it **behaves across Fast and Deep Analysis** — all as a faithful realization of the authoritative doctrine and calibration principles. It is the reference an engineer or test author consults to implement confidence behavior **without** having to re-derive meaning.

---

## 2. Scope

**In scope:** the conceptual operating model for the `ConfidenceState` (representation, state semantics, reliability qualification, the consolidate-then-qualify synthesis *framework*, transitions, explanation, history, Fast/Deep behavior, integrity rules, conformance).

**Out of scope (Deferred to future calibration / owned elsewhere):** numeric band boundaries, the synthesis arithmetic, reliability-scale boundaries, the determinism tolerance, severity numerics, UI design, governance, and any probability/outcome-likelihood construct. CAF, Reliability, and the meaning of confidence are **consumed, not defined here.**

---

## 3. Model Relationships

```text
CAFState  ─────────────┐
 (per run; strength)   │
                       ├──▶  Confidence Synthesis (consolidate-then-qualify)  ──▶  ConfidenceState
Reliability  ──────────┘                                                              (per run; the trust signal)
 (per run; supportability,                                                            ├─ confidence_band  (Very Low…Very High)
  Coverage/Evidence/Assessability)                                                    ├─ reliability_qualifier (High/Moderate/Low)
                                                                                      └─ supersedes_confidence_state_id (history)
Findings / Recommendations ──▶ (act on CAF only) ──▶ reach confidence ONLY through CAF
```

A `ConfidenceState` is produced **per analysis run**, from that run's `CAFState` and its reliability. Findings/recommendations influence **CAF**, never confidence directly. Reliability **qualifies** the consolidated CAF strength; it never alters a CAF dimension. (Entities/fields are the existing Data Model v1.1 ones — none new.)

---

## 4. Confidence Representation

A confidence signal is represented as a **triple**, never a bare value (realizing Decision 001 D11 + Calibration §"CAF Treatment"/"Reliability"):

1. **Confidence band** — one of **Very Low · Low · Moderate · High · Very High** (the canonical qualitative state; Calibration CAL-CONF-2 / D12). Primary.
2. **Reliability qualifier** — **High · Moderate · Low** (Calibration CAL-REL-1). Always present.
3. **Basis** — the explanation components (Section 9). Always available.

Any numeric index is **subordinate, supportive, and never a percentage or probability** (Decision 001 D11). A band shown without its reliability qualifier and basis is an **incomplete** representation and is non-conformant (Section 12).

---

## 5. Confidence State Semantics

Each band is a **region in the conceptual space of (consolidated CAF strength × how fully reliability lets that strength be expressed)** — described qualitatively. **No thresholds or percentages**; the precise boundary placement is *Deferred to future calibration* (Section 14). The bands are ordered; the **conceptual distinction between neighbours** is:

| Band | Conceptual character |
|---|---|
| **Very Low** | There is **little or no dependable understanding** to trust — understanding is largely unformed or essentially unsupportable. *(Reached by genuinely weak consolidated CAF — not by low reliability alone; Non-Collapse Invariant.)* |
| **Low** | **Some** trustworthy understanding exists, but **material weaknesses dominate** it — what can be trusted is outweighed by what cannot. |
| **Moderate** | **Strengths and weaknesses are both materially present** — partial, qualified trust; a genuinely mixed understanding in which neither side erases the other. |
| **High** | **Strengths predominate and no weakness materially constrains** the signal — the understanding is broadly dependable, with some residual qualification remaining. |
| **Very High** | **Strong across the dimensions and well-supported**, with **no residual material qualification** — the fullest trust the model expresses. **Still not certainty.** |

**Neighbour distinctions (conceptual, not numeric):**
- **Very Low → Low:** the appearance of *some* genuinely dependable understanding (Low) where there was essentially none (Very Low).
- **Low → Moderate:** weaknesses stop *dominating*; strengths become **materially co-present** rather than outweighed.
- **Moderate → High:** no remaining weakness **materially constrains** the signal; strengths **predominate** rather than merely balance.
- **High → Very High:** the **residual qualification disappears** — all dimensions strong **and** reliability full — leaving the fullest expressible trust (which remains short of certainty).

*The character of each band and each transition is fixed here; exactly where on the scale each boundary falls is calibration.*

---

## 6. Reliability Qualification

Reliability qualifies **how fully the consolidated CAF strength is expressed** as a confidence band (realizing Reliability Model §4 + Calibration "Reliability Treatment" + Non-Collapse Invariant). As qualification concepts:

- **High Reliability** — the assessment rests on a broad, well-evidenced, assessable surface; the consolidated CAF strength is expressed **most fully**, and the signal is **stable** (less likely to move on further evidence).
- **Moderate Reliability** — partial support; the strength is expressed but **with reservation**; the signal is **more open to movement** as evidence accrues.
- **Low Reliability** — thin coverage/evidence, or limited assessability; the strength is **held back** and uncertainty is **preserved** in the signal.

How reliability behaves:
- **Influences expression:** higher reliability lets more of the CAF strength reach the band; lower reliability lets less.
- **Constrains expression:** low reliability **caps how fully** strength is expressed — but **only within bounds**.
- **Preserves uncertainty:** low reliability keeps the signal honest about what is not yet firmly known, rather than overstating trust.
- **Never collapses:** low reliability **alone must never drive the band to Very Low** when consolidated CAF is strong (Non-Collapse Invariant; cf. Confidence Model Example B: High CAF + Low Reliability → Moderate, not the floor).
- **Never replaces or alters CAF:** reliability changes *expression*, never a CAF dimension; and confidence **may move on reliability alone** even when CAF is unchanged.

*No arithmetic; the degree of holding-back is Deferred to future calibration.*

---

## 7. Confidence Synthesis Framework

Realizes the approved **consolidate-then-qualify via constrained aggregation** principle (Calibration CAL-CONF-1; Confidence Model §6/§7) as a **two-movement conceptual process** — **no formula**:

**Movement 1 — Consolidate.** The three **co-equal** CAF dimensions are consolidated into a single **understanding-strength position** that:
- **reflects strengths** (strong dimensions contribute positively),
- **materially reflects weaknesses** (a weak dimension constrains the position),
- **ignores no dimension** (all three participate),
- is **not a simple average** (a strong dimension may not silently offset a weak one) and **not weakest-link domination** (one weak dimension does not collapse the position by default),
- therefore lives **deliberately between an average and a minimum**.

**Movement 2 — Qualify.** Reliability qualifies the consolidated strength (Section 6), governing how fully it is expressed as the **confidence band**, bounded by the Non-Collapse Invariant.

**The result** is the `ConfidenceState` triple (Section 4). **The arithmetic that realizes "between an average and a minimum" and the qualification degree are Deferred to future calibration** — and any such realization **must preserve** the properties above and the integrity rules (Section 12). CAF treatment is **equal standing, no weighting, no hierarchy** (Calibration CAL-CAF-1, unchanged).

---

## 8. Confidence Transition Model

Confidence does not move on its own. As model concepts:

- **Strengthening confidence** — a transition to a higher band (or fuller expression at the same band) caused by **CAF strengthening** (weaknesses addressed; ambiguity/assumption/conflict resolved) and/or **reliability rising** (broader coverage, more evidence, greater assessability).
- **Weakening confidence** — a transition to a lower band caused by **CAF weakening** (new/worsened findings reduce a dimension) and/or **reliability falling**.
- **Stable confidence** — **no transition**, because neither CAF nor reliability has changed.

**Internal interpretation:** every transition is **caused and attributable** — to a CAF change, a reliability change, or both — and **nothing else** (Confidence Stability Invariant). A transition with no CAF/reliability change is **forbidden** and indicates a defect. Direction is realized per Calibration CAL-CONF-3/4/5: findings act through CAF on their affected dimension(s), never by type and never directly on confidence.

---

## 9. Confidence Explanation Model

Every `ConfidenceState` MUST, by construction, make the following explanation components **available** (realizing the Explainability/Attribution Invariant + Confidence Model §10):

1. **Confidence state** — the band + reliability qualifier (the signal itself).
2. **CAF basis** — the contributing CAF dimension assessments and **how each participated** (which strengthened the position, which constrained it). No dimension omitted.
3. **Reliability basis** — the reliability qualifier and its grounding in **Coverage / Evidence Availability / Assessability**; whether reliability raised, held, or constrained expression.
4. **Contributing findings** — the findings (via CAF) that shaped the dimension assessments, and the recommendation history associated with them.
5. **Supersession context** — the prior state this one superseded (if any) and **what changed** — a CAF change, a reliability change, or both (change attribution).

**Cause-of-level** must be expressible: whether the signal sits where it does because of a CAF weakness, a reliability shortfall, or both. A confidence state for which any required component cannot be produced is **non-conformant** (Section 12) — confidence **may never become an opaque signal**. The explanation **reduces to basis, never to a number or formula.**

---

## 10. Confidence History Model

Using existing State Model concepts (State Model §8; Data Model v1.1 `ConfidenceState.supersedes_confidence_state_id`) — **no new states**:

- **Current confidence state** — the latest `ConfidenceState` for the project (pointed to as current); the signal in effect now.
- **Superseded confidence state** — a prior state replaced by a newer one; **retained**, never deleted.
- **Historical confidence state** — any state in the supersession chain; the chain **is** the confidence history.

**Interpretation:** the chain is read as the **evolution of trust in understanding over time** — each link attributable to a CAF and/or reliability change (Section 9). History is **append-only via supersession**; the trend across the chain reflects **understanding maturation**, not a trajectory toward or away from any outcome (Interpretation §10; Leadership §7).

---

## 11. Fast vs Deep Confidence

Using existing doctrine (Decision 001 §7/§8; Interpretation §9; Leadership §8; Planning Intelligence §16–§18) — `run_type` distinguishes the runs; **no new concepts**:

- **Fast Analysis confidence** — the initial `ConfidenceState` from the Fast pass (the 60-Second Orientation). It is **provisional** because the Fast horizon is shallow: understanding is initial and often **lower-reliability**, especially on the relational dimensions. It is **explicitly not final**.
- **Deep Analysis confidence** — a recalculated `ConfidenceState` from a Deep pass that **supersedes** the prior (Section 10). It supersedes because the Deep pass produces a **fuller, better-supported** understanding — typically **higher reliability**.
- **Why Deep confidence may increase** — deeper analysis can strengthen and better-support the understanding (ambiguity resolved, assumptions validated, coverage broadened).
- **Why Deep confidence may decrease** — deeper analysis can **surface previously-hidden findings** (deeper assumptions, contradictions) that reduce CAF, lowering the band even though nothing about the project worsened.

This **preserves the foundational principle: confidence may decrease as understanding improves.** A post-Deep decline is **discovery, not deterioration**; the superseded higher value is retained in history (Section 10), and the new, often higher-reliability value is the more honest signal. **Deep Analysis improves understanding, not certainty.**

---

## 12. Confidence Integrity Rules

*Authoritative implementation/testing reference. Every rule realizes existing doctrine/calibration; none is new doctrine.*

**Representation**
- IR-1. A `ConfidenceState` MUST carry a **band**, a **reliability qualifier**, and an available **basis**. A bare value is non-conformant.
- IR-2. The band MUST be one of Very Low / Low / Moderate / High / Very High; the qualifier one of High / Moderate / Low. No other values.

**Derivation**
- IR-3. Confidence MUST derive **only** from CAF + Reliability (consolidate-then-qualify). No other input may influence it.
- IR-4. Consolidation MUST **not** be a simple average and MUST **not** be weakest-link domination; it MUST reflect strengths and weaknesses and ignore **no** dimension (lives between an average and a minimum).
- IR-5. CAF dimensions MUST be treated with **equal standing** (no weighting, no hierarchy).
- IR-6. Findings/recommendations MUST reach confidence **only through CAF**, never directly.

**Reliability**
- IR-7. Reliability MUST **qualify** expression, never replace or alter a CAF dimension.
- IR-8. **Reliability Non-Collapse:** low reliability **alone** MUST NOT drive the band to **Very Low** when consolidated CAF is strong.
- IR-9. Confidence MAY change on a reliability change alone (CAF unchanged).

**Stability & attribution**
- IR-10. **Confidence Stability:** a `ConfidenceState` MUST NOT differ from its predecessor unless **CAF changed or Reliability changed**. No independent source of movement.
- IR-11. Every transition MUST be **attributable** to a CAF change, a reliability change, or both.

**Explainability**
- IR-12. Every `ConfidenceState` MUST be explainable through **CAF, Reliability, Findings, Recommendation history, and supersession history** (Section 9). Confidence MUST NOT be opaque.
- IR-13. Explanation MUST reduce to **basis**, never to a number or formula.

**History**
- IR-14. A new `ConfidenceState` MUST **supersede** (not overwrite) the prior; superseded states MUST be **retained**.
- IR-15. The supersession chain MUST reconstruct the full confidence history (replayability).

**Meaning boundary**
- IR-16. A `ConfidenceState` MUST NOT be represented or labeled as a **probability, prediction, project-health, readiness, or certainty** signal.
- IR-17. Confidence MUST be presented **with** its reliability qualifier (never the band alone).

---

## 13. Conformance Requirements

A conforming implementation MUST satisfy **all** Integrity Rules (Section 12) and, additionally:

- **C-1.** Produce exactly one `ConfidenceState` per completed analysis run, from that run's CAFState + reliability.
- **C-2.** Carry the reliability qualifier on every state and surface the basis on demand (no recomputation required for explanation — lineage is stored).
- **C-3.** Set the supersession pointer on every recalculation and retain prior states.
- **C-4.** Guarantee that identical CAF + reliability inputs under a pinned configuration yield an **equivalent** band + qualifier (determinism; bounded-equivalence tolerance **Deferred to future calibration**).
- **C-5.** Never emit a band change absent a CAF/reliability change (testable against IR-10).
- **C-6.** Preserve the Fast→Deep supersession behavior, including legitimate **decreases** after Deep Analysis (testable against Section 11).
- **C-7.** Reject (as a defect) any state that is unexplainable, bare, collapsed-by-reliability-alone, or labeled as probability/health/readiness.

These map directly to the Testing Strategy's confidence, determinism, replay, and traceability suites.

---

## 14. Open Items Deferred To Future Calibration

The following are **Deferred to future calibration** — this model fixes their *structure and constraints*, not their values:

- **Band boundaries** — where on the scale each band/neighbour boundary falls (Section 5). *Deferred.*
- **Synthesis arithmetic** — the realization of "between an average and a minimum," preserving IR-4/IR-5. *Deferred.*
- **Reliability qualification degree** — how far low reliability holds expression back, within the Non-Collapse bound (Section 6). *Deferred.*
- **Reliability-scale boundaries** — the High/Moderate/Low boundaries (CAL-REL-1). *Deferred.*
- **Determinism tolerance** — the bounded-equivalence tolerance for C-4 (CAL-DET-1/3). *Deferred.*
- **Confidence index range** (if any subordinate numeric is used) — never a percentage/probability (IR-16). *Deferred.*

None of these may, when resolved, alter the meaning doctrine (L0–L2) or the calibration principles/invariants (L3). Any future probability/outcome-likelihood construct remains a **separate signal** outside this model (Stack Index §7).

---

*Confidence Model v2 realizes the approved Outcome Confidence doctrine and calibration as an operational model. It redefines nothing above it, introduces no arithmetic/thresholds/probability/weights/new doctrine, creates no new entities/states/events/dimensions, and defers all numeric calibration. It is the implementation/testing reference for confidence behavior in Release 1.*

**Confidence Model v2 complete.**
