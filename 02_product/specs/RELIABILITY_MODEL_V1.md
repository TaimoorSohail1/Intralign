# Reliability Model v1

**Document:** RELIABILITY_MODEL_V1.md
**Status:** Specification of the Assessment Reliability Model (founder-approved positions formalized)
**Related (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md`
**Date:** 2026-05-31

> **Scope.** This document defines the **Reliability Model** — what Assessment Reliability is, what it represents, how it differs from CAF, how it contributes to Outcome Confidence, what influences it, how it behaves, and how it explains itself. It does **not** define CAF scoring calibration, Confidence scoring calibration, MRI implementation, UI behavior, recommendation logic, or environmental-signal processing. Qualitative levels (High / Moderate / Low) are used as the founder uses them; no numeric threshold, weight, or percentage is fixed here.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment, CAF Scoring, and Confidence models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's model of **Assessment Reliability**: the measure of how trustworthy a CAF assessment is, given the observable evidence available to OSLO.

This document defines:

- what Assessment Reliability is;
- what Assessment Reliability represents;
- how Reliability differs from CAF;
- how Reliability contributes to Outcome Confidence;
- what influences Reliability;
- how Reliability behaves conceptually;
- how Reliability explains itself.

It is a conceptual and behavioral model. It introduces no formula, weight, threshold, or percentage.

---

## 2. Reliability Overview

**Assessment Reliability represents the degree to which project understanding can be confidently assessed given the observable evidence available to OSLO.** *(Reliability Position #1)*

Equivalently, **Assessment Reliability represents the degree to which the current CAF assessment is supported by observable project evidence.** *(Reliability Position #6)* It measures the *supportability of the assessment* — not the quality of the project, and not the quality of OSLO. *(Reliability Position #6)*

Two readings of the same idea make the concept precise:

- A CAF assessment can be strong. Reliability asks a different question: *how much observable evidence stands behind that assessment?*
- Reliability does not judge whether the project is good or bad, nor whether OSLO is performing well or poorly. It judges only whether the evidence available to OSLO is sufficient to *support* the assessment OSLO has made.

Reliability is therefore a statement about the **assessment**, expressed independently of how strong that assessment is.

---

## 3. Relationship To CAF

**Reliability is distinct from CAF.** *(Reliability Position #2)*

- **CAF measures the integrity of understanding** — how strong the understanding is.
- **Reliability measures the trustworthiness of the assessment itself** — how well that understanding's assessment is supported by observable evidence.

CAF evaluates **integrity**; Reliability evaluates **supportability**. Because these are different questions, a project may exhibit, without contradiction:

- **High CAF, Low Reliability** — understanding appears strong, but little observable evidence supports the assessment; or
- **Moderate CAF, High Reliability** — understanding is more modest, but the assessment is well supported by observable evidence.

Neither combination is inconsistent. Integrity and supportability are independent properties of the same assessment.

---

## 4. Relationship To Outcome Confidence

Outcome Confidence consumes two inputs: **(1) CAF and (2) Reliability** (Confidence Model §6).

Within that relationship, Reliability plays a specific, bounded role:

- **Reliability qualifies CAF.** It adjusts how much trust should be placed in the CAF assessment.
- **Reliability does not replace CAF.** It never substitutes for the dimensional assessment.
- **Reliability does not summarize CAF.** Summarizing CAF into a single signal is the work of Outcome Confidence, not of Reliability.
- **Reliability influences trust in CAF.** Its entire contribution to Outcome Confidence is to express how trustworthy the CAF assessment is.

Reliability is thus a **supporting assessment layer between CAF and Outcome Confidence**: CAF produces the dimensional assessment, Reliability qualifies its trustworthiness, and Outcome Confidence consumes both.

---

## 5. Reliability Philosophy

Three questions sit in sequence across OSLO's assessment chain:

- **CAF answers:** *"How strong is the current understanding?"*
- **Reliability answers:** *"How trustworthy is the current assessment?"*
- **Outcome Confidence answers:** *"How confident should we be in our understanding?"*

Reliability is the middle question — a **supporting assessment layer between CAF and Outcome Confidence.**

What Reliability is **not**:

- It is **not a measure of project quality.** A well-run project with little documented evidence may carry low reliability; a troubled project richly evidenced may carry high reliability.
- It is **not a measure of OSLO's quality.** Reliability does not grade OSLO's reasoning; it reports the supportability of the assessment given what is observable.

Reliability evaluates one thing only: the **supportability of the assessment** by observable project evidence.

---

## 6. Reliability Determination Model

**Assessment Reliability is influenced by three inputs:** *(Reliability Position #3)*

1. **Coverage**
2. **Evidence Availability**
3. **Assessability**

Two determination principles govern the model: *(Reliability Position #4)*

- **Reliability is determined independently from CAF.** It is not derived from the CAF dimensions. It is computed from the conditions of the observable evidence surface, not from the strength of understanding.
- **Reliability is not directly influenced by findings.** Findings influence CAF. Coverage, Evidence Availability, and Assessability influence Reliability. Reliability reads the *conditions* of the evidence surface directly; it does not read the findings derived from it.

**Independence from CAF in practice.** Because Reliability draws on different inputs than CAF, **Reliability may change even when CAF remains unchanged.** *(Reliability Position #5)* Additional observable evidence may raise reliability — the assessment becomes better supported — without changing the assessed integrity of understanding. This is the mechanism behind Example C (Section 10).

**Consistency note (not a redefinition).** The CAF models treat an incomplete evidence surface in their own terms (a Coverage Gap is a CAF finding that reduces a dimension). Reliability does not contradict this: the *same underlying condition* — an incomplete or thinly evidenced surface — is read by CAF as a finding affecting integrity, and by Reliability as reduced Coverage / Evidence Availability affecting supportability. The two layers observe the same reality through different lenses; Reliability is computed from the surface conditions, not from the findings, exactly as Position #4 requires.

The model fixes the three inputs and the two determination principles. It fixes no arithmetic by which the inputs combine — that is calibration, outside this model.

---

## 7. Coverage

**Coverage** is the breadth of the observable evidence surface — the degree to which the relevant aspects of project reality have observable evidence available to OSLO.

- High coverage means the assessment was made across a broad, well-observed surface: most of what matters could be seen.
- Low coverage means significant portions of the relevant surface were not observable: the assessment was made over a partial view.

Coverage answers: *how much of the relevant project reality could the assessment actually draw upon?* It is the breadth condition of reliability. Broadening coverage — bringing previously unobserved aspects into view — raises reliability.

---

## 8. Evidence Availability

**Evidence Availability** is the presence and accessibility of observable evidence supporting the assessment — whether evidence that bears on the understanding actually exists and is available to OSLO.

- High evidence availability means the understanding is backed by observable evidence that OSLO can draw upon.
- Low evidence availability means the understanding rests on little observable evidence, even where the surface is nominally in view.

Evidence Availability answers: *how much observable evidence actually stands behind the assessment?* Where coverage concerns breadth of the surface, Evidence Availability concerns the presence of supporting evidence within it. Adding observable evidence raises reliability (Section 10, Example C).

---

## 9. Assessability

**Assessability** is the degree to which project understanding can be confidently assessed — whether the understanding is in a state that can be evaluated against observable evidence at all.

- High assessability means the understanding is expressed in a way that can be examined and supported or challenged by evidence.
- Low assessability means the understanding cannot be fully evaluated — not because evidence is absent, but because the understanding itself is not in an assessable state.

Assessability answers: *can the understanding be confidently assessed in the first place?* It is the condition that determines whether Coverage and Evidence Availability can even be brought to bear. Low assessability constrains reliability regardless of how much evidence might otherwise be available.

---

## 10. Reliability Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no formula; qualitative levels are used as the founder uses them.

### Example A — strong understanding, well supported
- **CAF:** High / High / High
- **Coverage:** High · **Evidence Availability:** High · **Assessability:** High
- **Expected Reliability:** **High**
- **Why:** The assessment was made across a broad surface (high coverage), backed by ample observable evidence (high evidence availability), over understanding that could be confidently evaluated (high assessability). The CAF assessment is fully supportable, so reliability is High. CAF strength and reliability happen to coincide here, but each is established on its own basis.

### Example B — strong understanding, thinly supported
- **CAF:** High / High / High
- **Coverage:** Low · **Evidence Availability:** Low · **Assessability:** Low
- **Expected Reliability:** **Low**
- **Why:** Strong *apparent* understanding exists, but insufficient observable evidence supports the assessment. The surface was narrow, little evidence was available, and the understanding was hard to assess. CAF is identical to Example A, yet reliability is Low — because reliability measures supportability, not integrity. This is the canonical High-CAF / Low-Reliability case. *(Reliability Positions #2, #6, #7)*

### Example C — CAF unchanged, reliability rises
- **CAF:** unchanged
- **Change:** additional observable evidence is added; **Coverage increases**
- **Expected result:** **Reliability improves while CAF remains unchanged.**
- **Why:** New observable evidence broadens coverage and raises evidence availability, so the *same* CAF assessment is now better supported. The assessed integrity of understanding has not changed — the understanding is no stronger — but OSLO can now more fully stand behind the assessment it already held. Reliability rises on its own inputs, independently of CAF. *(Reliability Positions #4, #5)*

---

## 11. Reliability Explanation Model

Assessment Reliability is explainable by construction. Its explanation is composed of:

- **Coverage basis** — how broad the observable evidence surface was for the assessment (Section 7).
- **Evidence Availability basis** — how much observable evidence stood behind the assessment (Section 8).
- **Assessability basis** — the degree to which the understanding could be confidently assessed at all (Section 9).
- **Independence statement** — the explanation makes clear that reliability was determined from these surface conditions, not from CAF and not from findings. It never attributes a reliability level to the strength of understanding or to any finding.
- **Change attribution** — what last moved reliability. Because reliability is determined from Coverage, Evidence Availability, and Assessability, every change in reliability is attributable to a change in one or more of those three — for example, new evidence broadening coverage. The explanation can therefore always answer *"why did reliability move — and note that CAF need not have moved with it."*

An explanation of reliability never reduces to a number or a formula; it reduces to its **basis** — the coverage, evidence availability, and assessability that account for the level and its last change. This keeps reliability faithful to its definition: a statement about the supportability of the assessment, expressed independently of the assessment's strength.

---

## 12. Future Evolution

Consistent with the boundaries of the related models, the following are explicitly out of scope here:

- **Environmental signals.** Future OSLO versions may admit environmental signals; this model concerns Reliability as determined by Coverage, Evidence Availability, and Assessability in Release 1 only.
- **Calibration.** The numeric expression of Reliability, any band boundaries, and the arithmetic combining its three inputs are calibration, owned elsewhere; this model fixes only structure, inputs, and behavior.
- **Consumers of Reliability.** Outcome Confidence consumes Reliability (Confidence Model); MRI visualization and implementation, UI behavior, and recommendation logic consume it further but are defined in their own documents. This model defines the supporting assessment, not its surfaces.

---

## 13. Summary

Assessment Reliability is OSLO's measure of how trustworthy a CAF assessment is, given the observable evidence available to OSLO. Where CAF measures the integrity of understanding, Reliability measures the supportability of the assessment — not the quality of the project and not the quality of OSLO. The two are distinct and independent: a project may show high CAF with low reliability, or moderate CAF with high reliability, without contradiction.

Reliability is determined independently from CAF, from three inputs — Coverage (the breadth of the observable evidence surface), Evidence Availability (the presence of supporting evidence), and Assessability (whether the understanding can be confidently assessed at all). It is not directly influenced by findings; findings influence CAF, while these three surface conditions influence Reliability. Because its inputs differ from CAF's, Reliability can change while CAF stays fixed — additional evidence can make an unchanged assessment better supported.

In the assessment chain, Reliability is the supporting layer between CAF and Outcome Confidence: it qualifies CAF — adjusting trust in the assessment — without replacing or summarizing it, and Outcome Confidence consumes both. Every reliability level is explainable by its coverage, evidence-availability, and assessability basis, and by what last changed it. This document defines that model; it does not define reliability's calibration or its surfaces.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Reliability = degree understanding can be confidently assessed given observable evidence | §2 |
| #2 | Distinct from CAF; integrity vs trustworthiness of the assessment | §3, §5 |
| #3 | Influenced by Coverage, Evidence Availability, Assessability | §6, §7, §8, §9 |
| #4 | Determined independently from CAF; not directly influenced by findings | §6, §11 |
| #5 | May change while CAF is unchanged; added evidence raises reliability, not integrity | §6, §10 (Ex. C) |
| #6 | Supportability of the assessment; not project quality, not OSLO quality | §2, §5 |
| #7 | Behavioral example (High CAF, Low Coverage/Evidence/Assessability → Low Reliability) | §10 (Ex. B) |

All founder positions are represented.

**Required behavior examples:** Example A (→ High), Example B (→ Low), Example C (reliability rises while CAF unchanged) included and explained conceptually (§10).

**Exclusion checklist**
- Reliability remains distinct from CAF — confirmed (§3).
- Reliability remains distinct from Confidence — confirmed (§4: it qualifies, does not replace or summarize).
- Findings do not directly determine Reliability — confirmed (§6, §11).
- Reliability may change while CAF remains unchanged — confirmed (§6, §10 Ex. C).
- No scoring formulas — confirmed.
- No weights — confirmed.
- No thresholds — confirmed.
- No percentages — confirmed.
- No MRI implementation details — confirmed (§12).
- No recommendation logic — confirmed (§12).
- CAF Assessment, CAF Scoring, and Confidence models unmodified — confirmed (consumed only).

*Reliability Model v1 complete. Formalizes the founder-approved reliability positions; defines Assessment Reliability as the supportability of the CAF assessment, determined independently from CAF by Coverage, Evidence Availability, and Assessability, and consumed by Outcome Confidence. Defines the model only — not calibration, surfaces, or future environmental-signal logic. Subject to governance review before adoption.*
