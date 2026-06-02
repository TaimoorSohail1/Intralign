# CAF Scoring Model v1

**Document:** CAF_SCORING_MODEL_V1.md
**Status:** Specification of the CAF Scoring Model (representation, effect mapping, dimension calculation, explanation)
**Builds on (authoritative):** `CAF_ASSESSMENT_MODEL_V1.md` — the assessment model is not modified by this document.
**Representation grounding:** `OSLO_RELEASE_1_MASTER_SPEC.md` §3, §5 (numeric signal + state bands + reliability).
**Date:** 2026-05-31

> **What this document adds.** The Assessment Model defines *how CAF reasons*; it deliberately excluded scoring. This document defines the **scoring layer that sits on top of that reasoning** — how impact-assessed findings, evidence, and coverage translate into per-dimension CAF scores, how those scores are represented, and how they are explained. Every assessment-model principle is preserved (Section 10).
>
> **What this document deliberately does not fix.** This is a *model*, not a calibration. It defines the **structure, direction, properties, and representation** of CAF scoring. It does **not** assert specific numeric weights, band boundaries, or aggregation arithmetic as canonical — no authoritative source defines them (the scoring methodology is recorded as an open item in `OSLO_CAPABILITY_MATRIX_V2.md` §22, and the Master Spec states exact thresholds "may evolve"). Concrete parameter values are **calibration**, owned by the repository owner and supplied by a separate calibration artifact (Section 11).
>
> **Governance.** Non-canonical specification; adoption subject to governance review. Canonical terminology from the Assessment Model and Master Spec is preserved; scoring-layer terms introduced here are labeled as such and do not redefine assessment concepts.

---

## 1. Purpose

Define the model by which CAF's assessment of understanding integrity becomes a **score** — a represented, explainable signal per dimension. Specifically, this document defines:

- how findings translate into CAF effects;
- how impact assessments influence CAF;
- how coverage influences CAF;
- how dimensions are calculated;
- how CAF scores are represented;
- how CAF explains scores.

It defines these as a coherent scoring model while preserving every principle established in the Assessment Model.

---

## 2. Relationship to the Assessment Model

The scoring model is strictly downstream of, and bounded by, the Assessment Model. The mapping:

| Assessment-model concept | Scoring-model role |
|---|---|
| Integrity of understanding (the thing CAF assesses) | The quantity each dimension **score** represents |
| Three independent dimensions (Clarity, Alignment, Feasibility) | Three independently **calculated** scores |
| Evidence strengthens integrity | The **strengthening contribution** to a dimension score |
| Findings reduce integrity | The **reducing contribution** to a dimension score |
| Impact Assessment (significance, affected dimensions, evidence support, scope) | The **modulator** that determines the magnitude and reach of each finding's reducing contribution |
| Coverage Gap (incomplete evidence surface) | The **reliability qualifier** on a dimension score |
| Event-driven dynamics | Scores **recompute only** on evidence or finding change |
| Confidence is downstream of CAF | CAF scores are an **input to Confidence**, defined elsewhere |

The scoring model introduces no new assessment semantics. It adds only the representation and the mechanics of effect aggregation.

---

## 3. How CAF Scores Are Represented

Each CAF dimension is represented by three coordinated elements:

1. **Integrity index** — a bounded signal expressing the assessed integrity of that dimension of understanding. Per Master Spec §3 and the worked example in §5 (where Clarity, Alignment, and Feasibility are each shown as a bounded number), the index uses the same bounded scale OSLO uses for its confidence signal. The index is an **integrity signal, not a probability and not a percentage of completion** — consistent with the Assessment Model's commitment that CAF claims neither certainty nor truth.
2. **State band** — a qualitative label corresponding to the index (Master Spec §3 defines the band vocabulary: Very Low, Low, Moderate, High, Very High). The band makes the index human-legible without implying false precision.
3. **Reliability qualifier** — a statement of how completely the dimension could be assessed given current coverage (Master Spec §5 illustrates this as a reliability label alongside each dimension, e.g., "High Reliability" / "Low Reliability"). The reliability qualifier is governed by coverage (Section 6).

A dimension score is therefore always a triple: **(integrity index, state band, reliability qualifier)**. A bare number is never a complete CAF score, because a high index under low reliability means something materially different from the same index under high reliability.

**Calibration boundary.** The exact numeric range, the band boundaries, and the reliability bands are calibration, not doctrine. The Master Spec presents its band ranges as examples and states thresholds "may evolve." This document fixes the *representation structure* (index + band + reliability) and defers the *boundary values* to calibration (Section 11).

---

## 4. How Findings Translate Into CAF Effects

A finding becomes a CAF effect only through its Impact Assessment; it never carries an intrinsic score (Assessment Model, Founder Position #9). The translation has fixed **direction and locality** and variable **magnitude**:

- **Direction — always reducing.** A finding contributes a *reducing contribution* to a dimension score. The *presence* of a finding reduces integrity and never raises it (Founder Position #5); however, *resolving* a finding withdraws or lessens its reducing contribution, and so raises the index. A dimension's index therefore rises either when evidence strengthens understanding or when a finding's reducing contribution is removed or lessened — both detailed in Section 7. Resolution is not a new force; it manifests through a change in evidence, a change in findings, or a change in an Impact Assessment.
- **Locality — only the affected dimensions.** A finding contributes to the score of a dimension **only if** that dimension appears in the finding's Impact Assessment as an Affected Dimension. A finding affecting only Clarity produces no contribution to Alignment or Feasibility. A finding may, per its Impact Assessment, affect more than one dimension, in which case it contributes a distinct reducing contribution to each affected dimension. This preserves dimension independence (Founder Position #2): cross-dimension movement occurs only where a finding's own assessment declares it.
- **Magnitude — derived, never intrinsic.** The size of the reducing contribution is determined by the finding's Impact Assessment (Section 5), not by its finding type. The flat taxonomy (Founder Position #13) is preserved: a finding's *type* classifies what kind of observation it is; it does not set the magnitude or the dimension of its effect.

The finding type is thus an input label, not a coefficient. Two findings of the same type may produce very different reducing contributions, and a single type may contribute to different dimensions in different cases, depending entirely on each finding's Impact Assessment.

---

## 5. How Impact Assessments Influence CAF

The Impact Assessment is the **modulator** that converts a finding into a sized, located reducing contribution. Each of its four factors (Assessment Model, Founder Position #10) governs a specific aspect of that contribution:

| Impact Assessment factor | What it governs in scoring |
|---|---|
| **Significance** | The **magnitude** of the reducing contribution — how strongly the finding lowers the affected dimension's integrity index. |
| **Affected CAF Dimensions** | The **locality** — which dimension scores receive a contribution (one or more). |
| **Evidence Support** | The **firmness** of the contribution — how well the finding and the understanding it concerns are evidenced. A finding about understanding that is itself thinly evidenced interacts with the evidence/inference balance (Section 7); a well-evidenced finding contributes a firmly established reduction. |
| **Scope of Impact** | The **breadth** — how much of the dimension's understanding surface the finding affects (localized versus pervasive). |

These four factors jointly determine each finding's reducing contribution to each affected dimension. They are combined by the dimension calculation (Section 8). This document fixes **which factor governs which property**; it does not fix the arithmetic that combines them — that is calibration (Section 11).

Because magnitude flows entirely from Impact Assessment, the Assessment Model's separation of *recording a finding* from *assessing its impact* is preserved in scoring: a finding can exist with no settled effect until its Impact Assessment is performed, and re-assessing impact (e.g., as evidence support changes) changes the score without the finding itself changing.

Inter-finding relationships (root cause, downstream effects) are reasoned in Impact Assessment, not in the taxonomy (Founder Position #13). The scoring model therefore receives whatever consolidated reducing contributions Impact Assessment produces; it does not re-derive relationships from finding types.

---

## 6. How Coverage Influences CAF

Coverage Gap is a finding type (Assessment Model §8.1, type 7): understanding cannot be fully assessed because the relevant evidence surface is incomplete. Coverage influences scoring along **two distinct channels**:

1. **As a reducing contribution.** Like any finding, an impact-assessed Coverage Gap contributes a reducing contribution to its affected dimension(s) — an incompletely evidenced surface lowers the assessable integrity of that dimension.
2. **As the reliability qualifier.** Distinctively, coverage also governs the **reliability** element of the dimension score (Section 3). Where coverage is strong, the dimension's integrity index is a reliable assessment; where coverage is weak, the same index is provisional. Coverage thus answers *"how completely could this dimension be assessed?"* — separate from *"how high is the assessed integrity?"*

This dual role keeps two questions from being conflated: a dimension can show a high integrity index under low reliability (high integrity over the *part* of reality OSLO can currently see) — precisely the situation the Master Spec's reliability signaling (§5) exists to surface. Coverage is the bridge between the Assessment Model's Coverage Gap finding type and the score's reliability qualifier.

---

## 7. How Evidence Strengthens CAF

A dimension's integrity index can rise by **two paths**, and they are not competing mechanisms:

- **Strengthened understanding** — evidence that supports the dimension contributes positively to its integrity index.
- **Reduced negative impact** — a finding affecting the dimension is resolved, removed, downgraded, or narrowed in scope, withdrawing or lessening its reducing contribution.

Both paths raise the index, and both reduce to the two — and only two — fundamental forces of CAF determination: **evidence (the strengthening force) and findings (the reducing force)**. No third force is introduced.

**The strengthening path (evidence).** Its role in scoring mirrors its role in the Assessment Model (Founder Positions #5, #6, #8):

- **Strengthening contribution.** Evidence that supports a dimension's understanding contributes positively to that dimension's integrity index. Evidence is defined by its contribution to understanding, not by its source or container; any trusted source contributes (Founder Position #8).
- **Evidence/inference balance.** A dimension whose understanding rests heavily on inference carries lower integrity than one resting on validated evidence (Founder Position #6). As inferences are validated by evidence, the strengthening contribution rises and the dimension's index increases. Inference is never scored as a dimension (Founder Position #7); it influences the index only through (a) the findings it contributes and (b) the evidence/inference balance reflected in the strengthening contribution.

**The resolution path (finding change).** Users most often improve understanding through actions they experience as *resolving issues* rather than *adding evidence* — resolving findings, clarifying ambiguities, validating assumptions, confirming inferred understanding, responding to CAF Review Requests, or editing project artifacts. In scoring terms these raise the index because they **remove or lessen a reducing contribution**. Specifically, a dimension's index increases when:

1. New evidence is introduced.
2. An existing finding is resolved, removed, downgraded, or narrowed in scope.
3. Inferred understanding is validated.
4. An ambiguity is clarified.
5. An assumption is confirmed or replaced by evidence.

Each of these remains consistent with the Assessment Model because it manifests through **a change in evidence, a change in findings, or a change in an Impact Assessment** — never through a new force. Validating an inference or confirming an assumption introduces evidence and thereby downgrades or removes the corresponding finding; clarifying an ambiguity removes the ambiguity finding; narrowing a finding's scope lessens its reducing contribution via re-assessed impact. The user's experience ("I resolved an issue") and the model's mechanics ("a reducing contribution was withdrawn, or a strengthening contribution was added") are two descriptions of the same events.

**Two valid paths to higher CAF.** Finding resolution and evidence strengthening are not alternatives in tension; finding resolution is *typically achieved through* evidence changes or impact-assessment changes, and both paths terminate in the same place.

```text
Evidence
  ↓
Finding Resolution
  ↓
Reduced Negative Impact
  ↓
Higher CAF
```

```text
Evidence
  ↓
Strengthened Understanding
  ↓
Higher CAF
```

- **Interaction, not addition in isolation.** Neither evidence nor findings determines a dimension alone (Founder Position #5). The dimension index is the resolved result of strengthening contributions and reducing contributions together; this document fixes that both forces participate and their directions, and defers their combination arithmetic to calibration.

---

## 8. How Dimensions Are Calculated

Each dimension — Clarity, Alignment, Feasibility — is calculated **independently** from the strengthening contributions (evidence) and reducing contributions (impact-assessed findings) assigned to it. The calculation is defined here by the **properties it must satisfy**, not by a fixed formula (which is calibration, Section 11):

1. **Independence.** A dimension's index is a function only of the contributions assigned to that dimension. A finding or evidence item affects another dimension only if its own assessment assigns it there (Founder Position #2).
2. **Directional monotonicity.** Adding or strengthening evidence for a dimension does not decrease its index; adding or increasing the impact of a finding affecting a dimension does not increase its index (Founder Position #5).
3. **Interaction.** The index resolves strengthening and reducing contributions together; neither alone fixes it (Founder Position #5).
4. **Boundedness.** The index stays within the represented range (Section 3).
5. **Reliability-qualified.** The index is always paired with the reliability derived from coverage (Section 6); the calculation never emits a bare index.
6. **Event-driven determinism.** The index is recomputed only when the evidence or findings assigned to the dimension change, and never merely with the passage of time (Founder Position #4). Given identical evidence and identical impact-assessed findings, the calculation yields the identical score.

The **method** that satisfies these properties — how individual contributions are aggregated into the index — is the scoring calibration. This document constrains that method to the six properties above; it does not select among the methods that satisfy them.

CAF as a whole is the set of the three independently calculated dimension scores. There is no separate "overall CAF number" defined here; consolidation across dimensions, and any further consolidation into Confidence, belongs to the downstream Confidence model (Section 9, and Master Spec §3).

---

## 9. How CAF Explains Scores

Every dimension score is explainable by construction, satisfying OSLO's requirement that the signal be traceable to its basis. A score's explanation is composed of, for the dimension in question:

- **Strengthening basis** — the evidence contributing positively to the dimension's index (the dimension's "drivers").
- **Reducing basis** — the impact-assessed findings contributing negatively, each carried with its finding type and the Impact Assessment that sized and located it (the dimension's "reducers"). The finding type is shown as a label; the magnitude is shown as coming from the Impact Assessment, preserving Founder Position #9.
- **Reliability basis** — the coverage state governing the reliability qualifier (Section 6), making explicit how completely the dimension could be assessed.
- **Change attribution.** Because scoring is event-driven (Section 8, property 6), any change to a dimension score is attributable to the specific evidence change or finding change that triggered it. An explanation can therefore always answer *"what changed, and why did the score move?"* by naming the triggering event.

An explanation never reduces to a formula trace, because this model does not fix the formula. It reduces to the **basis**: the evidence, the impact-assessed findings, and the coverage that together account for the score and its last movement. This keeps explanation faithful to the Assessment Model's epistemology — a score is justified by what OSLO currently knows, not asserted as truth.

---

## 10. Preserved Assessment-Model Principles

The scoring model preserves every Assessment-Model principle:

| # | Assessment principle | How scoring preserves it |
|---|---|---|
| 1 | CAF assesses integrity of understanding, not outcome | The index represents integrity of understanding; never outcome likelihood |
| 2 | Three independent dimensions; a finding may affect several | Dimensions calculated independently (§8.1); a finding contributes only to its assessed dimensions (§4) |
| 3 | No certainty, no truth; supportable integrity | Index is an integrity signal, not a probability or truth claim (§3) |
| 4 | Event-driven; no time decay | Scores recompute only on evidence/finding change (§8.6); change is event-attributable (§9) |
| 5 | Evidence × findings; neither alone | Strengthening and reducing contributions resolved together (§7, §8.3) |
| 6 | Inference lowers integrity; validation raises it | Evidence/inference balance governs the strengthening contribution (§7) |
| 7 | Inference is not a dimension | Inference is never scored as a dimension; it acts via findings and the evidence balance (§7) |
| 8 | Evidence defined by contribution, not source | Any trusted source contributes a strengthening contribution (§7) |
| 9 | Findings not inherently impactful | Magnitude derives from Impact Assessment, never from the finding itself (§4, §5) |
| 10 | Impact Assessment factors determine influence | The four factors govern magnitude, locality, firmness, breadth (§5) |
| 11 | Findings are inputs; dimensions are targets; by type not dimension | Type is an input label; effect location comes from Impact Assessment (§4, §5) |
| 12 | Seven canonical finding types | Used as input labels in the reducing basis; not as coefficients (§4, §9) |
| 13 | Flat taxonomy; relationships via Impact Assessment | Scoring consumes consolidated impact contributions; it does not re-derive relationships from type (§5) |

---

## 11. Calibration Boundary

The following are **calibration**, not defined by this model, and require owner approval and (where applicable) data-driven tuning:

- The numeric range and exact band boundaries of the integrity index and state bands (Master Spec presents its bands as examples that "may evolve").
- The reliability bands attached to coverage states.
- The arithmetic that aggregates strengthening and reducing contributions into a dimension index (any method satisfying the six properties of Section 8).
- The arithmetic by which Impact Assessment factors size a reducing contribution (Section 5 fixes *which factor governs which property*, not the magnitudes).

These are deliberately externalized so that calibration can change without altering the model. A separate calibration artifact, adopted under governance, supplies them.

---

## 12. Future Evolution

Consistent with the Assessment Model's boundary:

- **Environmental signals.** Future OSLO versions may admit environmental signals as a further strengthening or reducing force; Release 1 scoring is driven by evidence and findings only (Founder Position #4).
- **Impact Assessment extensions.** If Impact Assessment later adds Assessment Confidence or Root Cause Relationships (Assessment Model §12), the scoring model would receive them as additional modulators of the reducing contribution and of the reliability qualifier, without change to the representation or to dimension independence.

No Confidence definition, MRI implementation, UI visualization, or recommendation logic is defined here; CAF scores are an input to those, which are specified separately.

---

## 13. Summary

The CAF Scoring Model places a representation and an effect-aggregation layer on top of the CAF Assessment Model without altering its reasoning. Each dimension is scored independently as a triple — an integrity index, a state band, and a coverage-governed reliability qualifier. Evidence supplies the only strengthening contribution; impact-assessed findings supply directed, located, magnitude-from-impact reducing contributions; coverage both reduces integrity and qualifies reliability. Dimensions are calculated to satisfy fixed properties — independence, monotonicity, interaction, boundedness, reliability-qualification, and event-driven determinism — while the specific aggregation arithmetic, band boundaries, and factor magnitudes are externalized as owner-owned calibration. Every score is explainable by its basis: the evidence, the impact-assessed findings, and the coverage that account for it and its last change. CAF scores are then consumed by Confidence, which this document references but does not define.

This document defines how CAF is scored. It does not redefine how CAF reasons, and it does not fix the calibration of the scoring.

---

## Validation

**Required deliverables covered**

| Requested | Defined in |
|---|---|
| How findings translate into CAF effects | §4 |
| How impact assessments influence CAF | §5 |
| How coverage influences CAF | §6 |
| How dimensions are calculated | §8 |
| How CAF scores are represented | §3 |
| How CAF explains scores | §9 |

**Assessment-model preservation:** all 13 principles preserved (§10).

**Boundary checklist**
- Assessment model unmodified — confirmed (this document only consumes it).
- No fabricated canonical weights, band boundaries, or aggregation arithmetic — confirmed (externalized as calibration, §11).
- Representation grounded in Master Spec §3/§5, not invented — confirmed.
- Confidence referenced only as a downstream consumer, not defined — confirmed.
- No MRI implementation, UI visualization, or recommendation logic — confirmed.

*CAF Scoring Model v1 complete. Builds on the Assessment Model without modifying it; defines the scoring model's structure, representation, and explanation while deferring numeric calibration to a separate owner-approved artifact. Subject to governance review before adoption.*
