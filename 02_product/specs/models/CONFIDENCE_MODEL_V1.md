# Confidence Model v1

**Document:** CONFIDENCE_MODEL_V1.md
**Status:** Specification of the Outcome Confidence Model (founder-approved positions formalized)
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md`
**Representation vocabulary:** `OSLO_RELEASE_1_MASTER_SPEC.md` §3 (confidence state vocabulary).
**Date:** 2026-05-31

> **Scope.** This document defines the **Confidence Model** — what Outcome Confidence is, what it represents, how it relates to CAF and Reliability, how it is derived, how it behaves, and how it explains itself. It does **not** define MRI visualization or implementation, CAF overlays, recommendation generation, environmental-signal processing, calibration formulas, numeric thresholds, weights, percentages, or UI design. Those belong to separate documents. CAF qualitative levels (High / Moderate / Medium / Low) are used as the founder uses them; they correspond to OSLO's canonical confidence states (Master Spec §3) without any threshold being fixed here.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment and Scoring models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's model of **Outcome Confidence**: the summarized signal of how much trust should be placed in OSLO's current understanding of project reality.

This document defines:

- what Outcome Confidence is;
- what Outcome Confidence represents;
- how Outcome Confidence relates to CAF;
- how Outcome Confidence relates to Reliability;
- how Outcome Confidence is derived;
- how Outcome Confidence behaves conceptually;
- how Outcome Confidence explains itself.

It is a conceptual and behavioral model, not a calibration. It introduces no formula, weight, threshold, or percentage.

---

## 2. Outcome Confidence Overview

**Outcome Confidence represents OSLO's overall confidence in project understanding.** *(Founder Positions #1, #6)*

It is a single, summarized signal that answers one question: *how confident should we be in our current understanding of project reality?* Where CAF assesses understanding across three independent dimensions, Outcome Confidence consolidates that assessment — qualified by how trustworthy the assessment itself is — into one signal a person can act on.

Outcome Confidence is derived from two things, and only two things: *(Founder Positions #4, #6)*

1. **CAF Assessment** — the strength of understanding.
2. **Assessment Reliability** — the degree of trust that should be placed in that assessment.

**CAF determines the strength of understanding. Reliability determines the degree of trust that should be placed in that assessment.** *(Founder Position #6)* Outcome Confidence combines both.

---

## 3. Relationship To CAF

**Outcome Confidence is derived from CAF.** CAF provides the dimensional assessment; Outcome Confidence provides the summarized signal. *(Founder Position #2)*

CAF and Confidence are **distinct**. CAF remains the primary intelligence and assessment layer; **Confidence is a consumer of CAF.** Confidence adds no new assessment of project reality — it summarizes the assessment CAF has already produced and qualifies it by reliability. It does not feed back into CAF, and it never overrides a CAF dimension.

**Conceptual flow.** Outcome Confidence sits at the end of OSLO's assessment chain:

```text
Evidence
  ↓
Inference
  ↓
Findings
  ↓
Impact Assessment
  ↓
CAF
  ↓
Clarity
Alignment
Feasibility
        +
Reliability
  ↓
Outcome Confidence
```

The three CAF dimensions and the assessment's reliability are the inputs to Confidence; Confidence is their consolidated output. Everything upstream of CAF (evidence, inference, findings, impact assessment) reaches Confidence only through CAF, as established in the CAF models.

---

## 4. Relationship To Reliability

**Outcome Confidence is qualified by assessment reliability.** Strong CAF assessments with weak reliability produce lower confidence than equally strong CAF assessments with high reliability. *(Founder Position #3)*

Two principles govern this relationship:

- **Reliability does not replace CAF; Reliability qualifies CAF.** Reliability never changes a dimension's assessed strength. It changes how much trust the summarized signal places in that strength. CAF answers *how strong is our understanding?*; Reliability answers *how trustworthy is the assessment?*
- **CAF may remain unchanged while Confidence changes.** Because Confidence depends on reliability as well as CAF, Confidence can move when reliability moves, even if every CAF dimension is identical. In particular, **Confidence may increase even when CAF remains unchanged, if reliability improves** — for example, as coverage broadens and the same understanding becomes more completely assessable.

This is the mechanism by which a high CAF assessment over a narrow, incompletely assessed surface yields a more cautious confidence signal than the same CAF assessment over a well-covered surface.

---

## 5. Confidence Philosophy

Outcome Confidence answers: **"How confident should we be in our current understanding of project reality?"**

It sits alongside two narrower questions answered upstream:

- **CAF answers:** *"How strong is our understanding?"*
- **Reliability answers:** *"How trustworthy is the assessment?"*

**Outcome Confidence combines both.**

**Outcome Confidence is not:**

- project success probability;
- project health;
- execution readiness;
- outcome prediction.

**Outcome Confidence is confidence in understanding.** It speaks only to whether the understanding on which decisions are being made can be trusted — inheriting the CAF Assessment Model's commitment that the signal claims neither certainty nor truth, only justified integrity given what OSLO currently knows. A project may be healthy or troubled, likely or unlikely to succeed, for reasons entirely outside the confidence OSLO holds in its understanding; Outcome Confidence makes no claim about those.

---

## 6. Confidence Determination Model

Outcome Confidence is determined by two inputs: *(Founder Positions #4, #6)*

**Input 1 — CAF Assessment**, derived from the three independent CAF dimensions:

- Clarity
- Alignment
- Feasibility

**Input 2 — Assessment Reliability**, derived from:

- Coverage
- Evidence availability
- Assessability of project understanding

The determination proceeds in two conceptual movements:

1. **Consolidate the CAF Assessment.** The three dimensions are combined into a single understanding-strength signal under the constrained-aggregation principles of Section 7 — reflecting strengths and weaknesses together, without simple averaging and without weakest-link domination.
2. **Qualify by reliability.** The consolidated strength is qualified by Assessment Reliability (Section 8): the more completely and evidentially the assessment could be made, the more fully the consolidated strength is expressed in the confidence signal; the less reliable the assessment, the more the signal is held back.

The result is the summarized Outcome Confidence signal. This document fixes the *structure* of the determination (two inputs; consolidate-then-qualify) and the *properties* it must satisfy; it fixes no arithmetic, weight, or threshold — those are calibration and lie outside this model.

---

## 7. Constrained Aggregation Principles

Outcome Confidence is a **constrained aggregation** of the CAF dimensions. *(Founder Position #5)* The aggregation must:

- **reflect strengths** — strong dimensions contribute positively to the signal;
- **reflect weaknesses** — weak dimensions materially constrain the signal;
- **avoid simple averaging** — the signal is not a mean that lets a strong dimension silently offset a weak one;
- **avoid weakest-link domination** — a single weak dimension does not, by default, collapse the entire signal to its level.

Two balancing rules make this precise: *(Founder Position #5)*

- **No single dimension should be ignored.** Every dimension participates; none is dropped from the signal.
- **No single dimension should completely dominate confidence by default.** Neither the strongest nor the weakest dimension is permitted, by default, to determine the signal alone.

The intent is a signal that **summarizes overall project understanding while respecting meaningful weaknesses in any CAF dimension.** A genuinely weak dimension must be felt in the confidence signal; it must not be averaged away. Equally, one weak dimension among strengths must constrain confidence without erasing the contribution of the strengths. The aggregation lives deliberately between an average and a minimum.

---

## 8. Reliability Qualification

Reliability is the trust qualifier applied to the consolidated CAF strength. It is derived from Coverage, Evidence availability, and Assessability of project understanding (Section 6), consistent with the CAF Scoring Model, where coverage governs the reliability qualifier on each dimension.

Principles:

- **Reliability qualifies, never replaces.** A reliability change re-qualifies how much of the CAF strength is expressed in Confidence; it never alters a CAF dimension.
- **Same CAF, different reliability, different Confidence.** Identical CAF dimensions can yield different Outcome Confidence depending on reliability:

```text
High CAF
Low Reliability
  ↓
Moderate Confidence
```

```text
High CAF
High Reliability
  ↓
High Confidence
```

- **Confidence can rise on reliability alone.** Because reliability is an input, improving reliability — broader coverage, more available evidence, a more fully assessable understanding — can raise Confidence even while CAF is unchanged.

Reliability therefore expresses the difference between *strong understanding we can fully vouch for* and *strong understanding we can only partly see*.

---

## 9. Confidence Behavior Examples

These examples are conceptual illustrations of the model's expected behavior. They introduce no formula; the qualitative levels are used as the founder uses them.

### Example A — strong and reliable
- **CAF:** Clarity High · Alignment High · Feasibility High
- **Reliability:** High
- **Result:** **High Confidence**
- **Why:** All three dimensions are strong and the assessment is fully trustworthy. There is no weakness to constrain the signal and no reliability shortfall to hold it back, so the consolidated strength is expressed in full.

### Example B — strong but weakly assessed
- **CAF:** Clarity High · Alignment High · Feasibility High
- **Reliability:** Low
- **Result:** **Moderate Confidence**
- **Why:** The CAF assessment is identical to Example A, yet the assessment itself is weakly supported — coverage is thin, evidence is limited, or the understanding is only partly assessable. Reliability qualifies the strong CAF downward: OSLO cannot fully vouch for an assessment it could only partly make. This is the case where CAF is high but Confidence is held to Moderate. *(Founder Position #3)*

### Example C — a material weakness among strengths
- **CAF:** Clarity High · Alignment High · Feasibility Low
- **Reliability:** High
- **Result:** **Medium Confidence**
- **Why:** Two dimensions are strong and one is materially weak, under a trustworthy assessment. Constrained aggregation requires the strong dimensions to contribute positively while the weak Feasibility dimension materially constrains the signal — neither dominating by default. The result reflects both: clearly above weak, clearly below strong. *(Founder Positions #5, #7)*

**On Examples B and C together:** they reach a middle-range signal by different routes. In B, strong understanding is held back by *low trust in the assessment*. In C, a *genuine weakness in understanding* constrains an otherwise trustworthy assessment. The model distinguishes these causes even where the summarized level is similar — which is why the explanation model (Section 10) always names the cause.

---

## 10. Confidence Explanation Model

Outcome Confidence is explainable by construction. Because it is a consumer of CAF qualified by reliability, its explanation is composed of:

- **CAF basis** — the three dimension assessments and how each participated: which dimensions contributed positively as strengths, and which constrained the signal as weaknesses. No dimension is omitted from the explanation, mirroring the rule that none is ignored in the aggregation.
- **Reliability basis** — the assessment reliability that qualified the consolidated strength, traceable to coverage, evidence availability, and assessability. The explanation states whether reliability raised, held, or constrained the expression of CAF strength.
- **Cause of the current level** — whether the signal sits where it does primarily because of a CAF weakness, a reliability shortfall, or both (the distinction drawn in Section 9).
- **Change attribution** — what last moved the signal. Because CAF is event-driven (it changes only when evidence or findings change) and reliability changes only when coverage, evidence availability, or assessability change, every change in Outcome Confidence is attributable to a CAF change, a reliability change, or both. The explanation can therefore always answer *"why did Confidence move — did our understanding change, or did our trust in the assessment change?"*

An explanation of Outcome Confidence never reduces to a number or a formula; it reduces to its **basis** — the CAF dimensions and the reliability that account for the signal and its last movement — faithful to the epistemology inherited from the CAF models: the signal is justified by what OSLO currently knows, not asserted as truth.

---

## 11. Preserved CAF Principles

The Confidence Model consumes CAF without altering it. The CAF Assessment and Scoring models remain authoritative; Confidence preserves their principles:

| CAF principle | How Confidence preserves it |
|---|---|
| CAF assesses integrity of understanding, not outcome | Confidence is confidence *in understanding*, explicitly not success probability, health, readiness, or prediction (§5) |
| Three independent dimensions | The dimensions enter Confidence independently; none is ignored and none dominates by default (§7) |
| No certainty, no truth | Confidence claims justified trust in understanding, not certainty or truth (§5, §10) |
| Event-driven | Confidence changes only when CAF changes or reliability changes — never with time alone (§10) |
| Evidence and findings are the only CAF forces | Confidence introduces no new force; it summarizes CAF and qualifies by reliability (§3) |
| Coverage governs reliability | Assessment Reliability derives from coverage, evidence availability, and assessability (§6, §8) |
| CAF is the assessment layer | Confidence is a downstream consumer of CAF, never a replacement (§3) |

---

## 12. Future Evolution

Consistent with the boundaries of the CAF models, the following are explicitly out of scope here:

- **Environmental signals.** Future OSLO versions may admit environmental signals into CAF; this model concerns Confidence as derived from CAF and Reliability in Release 1 only.
- **Representation and calibration.** The numeric expression of Outcome Confidence, its state-band boundaries, and the arithmetic of constrained aggregation and reliability qualification are calibration, owned elsewhere; this model fixes only structure, properties, and behavior.
- **Consumers of Confidence.** MRI visualization and implementation, CAF overlays, recommendation generation, and UI design consume Outcome Confidence but are defined in their own documents. This model defines the signal, not its surfaces.

---

## 13. Summary

Outcome Confidence is OSLO's summarized signal of how much trust to place in its current understanding of project reality. It is derived from exactly two inputs — the CAF Assessment (the strength of understanding, across Clarity, Alignment, and Feasibility) and Assessment Reliability (the trustworthiness of that assessment, from coverage, evidence availability, and assessability). CAF determines strength; Reliability determines trust; Confidence combines them.

The combination is a constrained aggregation that reflects both strengths and weaknesses without simple averaging and without weakest-link domination — no dimension ignored, none dominating by default — and the consolidated strength is then qualified by reliability, so that strong understanding that is only partly assessable yields a more cautious signal than the same understanding fully assessed. Because reliability is an input, Confidence can change even when CAF does not.

Confidence is confidence in understanding — not success probability, not health, not readiness, not prediction. It consumes CAF without altering it, it is explainable by its CAF-and-reliability basis, and it changes only when CAF or reliability changes. This document defines that model; it does not define Confidence's calibration or its surfaces.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Confidence = overall confidence in project understanding | §2, §5 |
| #2 | Derived from CAF; CAF dimensional, Confidence summarized | §3 |
| #3 | Qualified by reliability; strong CAF + weak reliability → lower confidence | §4, §8, §9 (Ex. B) |
| #4 | Determined by CAF Assessment + Assessment Reliability; their sub-inputs | §6 |
| #5 | Constrained aggregation; none ignored, none dominates by default | §7 |
| #6 | CAF = strength, Reliability = trust; Confidence combines both | §2, §6 |
| #7 | Behavioral example (High/High/Low → Medium) | §9 (Ex. C) |

All founder positions are represented.

**Required behavior examples:** Example A (→ High), Example B (→ Moderate), Example C (→ Medium) included and explained conceptually (§9).

**Exclusion checklist**
- Confidence remains derived from CAF and Reliability — confirmed (§2, §6).
- Confidence is not project success probability — confirmed (§5).
- Confidence is not project health (nor readiness/prediction) — confirmed (§5).
- No scoring formulas — confirmed.
- No weights — confirmed.
- No thresholds — confirmed.
- No percentages — confirmed.
- No MRI implementation details — confirmed (§12).
- No recommendation logic — confirmed (§12).
- CAF Assessment and Scoring models unmodified — confirmed (consumed only).

*Confidence Model v1 complete. Formalizes the founder-approved confidence positions; derives Outcome Confidence from CAF and Reliability as a constrained, reliability-qualified, explainable signal. Defines the model only — not calibration, surfaces, or future environmental-signal logic. Subject to governance review before adoption.*
