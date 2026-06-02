# CAF Assessment Model v1

**Document:** CAF_ASSESSMENT_MODEL_V1.md
**Status:** Specification of founder-approved CAF positions (assessment model)
**Scope:** Defines the **CAF Assessment Model**. It does **not** define the CAF Scoring Model.
**Authoritative source:** The thirteen founder-approved CAF positions, formalized here without reinterpretation, extension, or substitution.
**Date:** 2026-05-31

> **Boundary of this document.** This specification defines *how CAF reasons about the integrity of project understanding*. It deliberately excludes numerical scoring, weighting, formulas, thresholds, percentages, confidence calculations, UI visualization, MRI implementation, and recommendation logic. Those belong to future documents. Where Confidence appears, it appears only as a downstream consumer of CAF and is not defined here.
>
> **Governance.** This document formalizes founder-approved positions; adoption as canonical content remains subject to governance review. Canonical terminology is preserved throughout.

---

## 1. Purpose

CAF is OSLO's model for evaluating the **integrity of project understanding**.

CAF does not measure outcome success. CAF measures the integrity of the understanding upon which outcome success depends. *(Founder Position #1)*

The purpose of this specification is to define, as a coherent and professional model:

- what CAF is;
- what CAF assesses;
- how CAF reasons;
- how evidence contributes to understanding;
- how findings contribute to assessment;
- how impact assessments contribute to CAF.

This document is an **assessment model**. It establishes the conceptual machinery by which CAF arrives at an assessment of understanding integrity. It does not establish how that assessment is quantified.

---

## 2. CAF Overview

CAF is the mechanism through which OSLO assesses whether its current understanding of project reality can be trusted.

Project understanding is the interpretation OSLO holds of project reality at a given moment. That understanding is never guaranteed to be complete or correct; it is supported, to varying degrees, by the evidence available to OSLO and qualified by the findings OSLO has observed. CAF assesses the **integrity** of that understanding — the degree to which the understanding is justified by what OSLO currently knows.

CAF is therefore a statement about understanding, not about the project's eventual result. A project may ultimately succeed or fail for reasons outside the integrity of its understanding; CAF speaks only to whether the understanding on which decisions are being made is sound given the available evidence and known findings.

---

## 3. CAF Dimensions

CAF consists of three dimensions: **Clarity**, **Alignment**, and **Feasibility**. *(Founder Position #2)*

Each dimension is an independent **assessment target** — a distinct facet of the integrity of project understanding:

- **Clarity** — the integrity of how clearly project reality is currently understood.
- **Alignment** — the integrity of the coherence between project elements and intended outcomes.
- **Feasibility** — the integrity of the understanding regarding whether intended outcomes are realistically achievable.

Two structural properties govern the dimensions:

1. **The dimensions are independent.** No dimension depends on another. The integrity of one facet of understanding does not, by structure, determine the integrity of another. *(Founder Position #2)*
2. **A finding may impact one or more dimensions simultaneously.** The dimensions are independent as assessment targets, but a single observation about understanding may bear on several of them at once. *(Founder Position #2)*

The dimensions are targets of assessment, not categories of input. The relationship between inputs (findings) and targets (dimensions) is defined in Sections 7–9.

---

## 4. CAF Assessment Philosophy

CAF represents an **assessment of the integrity of current project understanding** based on the evidence available to OSLO and the findings OSLO has observed. *(Founder Position #3)*

Three epistemological commitments define this philosophy:

**CAF does not claim certainty.** An assessment of integrity is not a claim that the understanding is certain.

**CAF does not claim truth.** CAF does not assert that the understanding is correct; it assesses whether the understanding is *justified* by what OSLO currently knows.

**CAF reflects supportable integrity.** CAF reflects the integrity of understanding that can be supported by the evidence currently available to OSLO. As that evidence changes, the supportable integrity — and therefore the assessment — may change. *(Founder Position #3)*

**Determination.** CAF is determined by the interaction between available evidence and known findings. Evidence strengthens confidence in the integrity of project understanding; findings reduce confidence in the integrity of project understanding. **Neither evidence nor findings alone is sufficient to determine CAF** — the assessment arises from their interaction, not from either in isolation. *(Founder Position #5)*

**Dynamics.** CAF is **event-driven**. CAF changes when available evidence changes or when findings change. CAF does not change merely because time passes. *(Founder Position #4)* In Release 1, CAF is driven by evidence and findings only. Future versions of OSLO may incorporate environmental signals that affect CAF, but those are outside the scope of this model (see Section 12).

---

## 5. Evidence Model

**Evidence is any information that contributes to OSLO's understanding of project reality.** *(Founder Position #8)*

Evidence may originate from many sources, including:

- project artifacts;
- stakeholder communications;
- meeting transcripts;
- comments;
- review responses;
- execution signals;
- other trusted sources.

**Artifacts are a source of evidence, not the definition of evidence.** *(Founder Position #8)* Evidence is defined by its contribution to understanding, not by the form or container in which it arrives. Any trusted information that informs OSLO's interpretation of project reality is evidence, regardless of origin.

**Role in assessment.** Evidence strengthens confidence in the integrity of project understanding. *(Founder Position #5)* The more an understanding is supported by validated evidence, the higher its integrity. Evidence is the strengthening force in the determination of CAF; it does not act alone, but in interaction with findings.

---

## 6. Inference Model

**Inference is not a CAF dimension. Inference is a characteristic of understanding.** *(Founder Position #7)*

Understanding may be supported by evidence, or it may be synthesized — inferred — where direct evidence is absent. Inference describes *how* a piece of understanding came to be held, not *what facet* of understanding it concerns.

**Evidence-supported versus inference-supported understanding.** CAF assessments are influenced by the balance between evidence-supported understanding and inference-supported understanding. Understanding that relies heavily on inference has **lower integrity** than understanding supported by validated evidence. As inferences are validated through evidence, understanding integrity increases. *(Founder Position #6)*

**How inference enters assessment.** Because inference is a characteristic of understanding rather than a dimension, it influences CAF indirectly: inference may **contribute findings** that impact Clarity, Alignment, Feasibility, or multiple dimensions, depending on the nature of the understanding being inferred. *(Founder Position #7)* Inference is therefore never assessed directly as a dimension; it is expressed through findings, and those findings are assessed for their impact.

---

## 7. Finding Model

**A finding is an observation about project understanding that is relevant to the assessment of understanding integrity.** *(Founder Position #9)*

A finding records something OSLO has observed about the understanding it holds — for example, that a piece of understanding is absent, ambiguous, or in conflict with another. A finding is an **assessment input**.

Two principles govern findings:

**Findings do not inherently determine CAF impact.** *(Founder Position #9)* The existence of a finding does not, by itself, dictate how — or how much — it influences the assessment. The influence of a finding is established only through a separate Impact Assessment (Section 9), which evaluates the finding's significance, context, evidence support, and affected dimensions.

**Findings are the reducing force.** Findings reduce confidence in the integrity of project understanding. *(Founder Position #5)* They act in interaction with evidence; neither is sufficient alone.

**Findings are categorized by finding type, not by CAF dimension.** *(Founder Position #11)* CAF dimensions are assessment targets; finding types are assessment inputs. A finding of a given type may impact one or more CAF dimensions. The taxonomy of finding types is defined in Section 8.

---

## 8. Canonical Finding Taxonomy

The CAF finding taxonomy organizes findings by **finding type**. Finding types are peer categories; the taxonomy is **flat**. *(Founder Positions #11, #13)*

### 8.1 Canonical finding types

The initial CAF finding taxonomy consists of seven finding types: *(Founder Position #12)*

1. **Missing Information** — required understanding is absent.
2. **Ambiguity** — understanding supports multiple plausible interpretations.
3. **Assumption** — understanding depends on something not yet validated.
4. **Inference** — understanding was synthesized rather than directly evidenced.
5. **Conflict** — two or more elements cannot simultaneously be true.
6. **Constraint** — a limitation threatens the viability of understanding.
7. **Coverage Gap** — understanding cannot be fully assessed because the relevant evidence surface is incomplete.

### 8.2 Flat taxonomy

The CAF finding taxonomy is **flat**. Finding types are peer categories. *(Founder Position #13)*

Relationships between findings — including root-cause relationships and downstream effects — are **not** expressed through the structure of the taxonomy. They are evaluated through Impact Assessment, not through taxonomy hierarchy. *(Founder Position #13)* The taxonomy classifies *what kind* of observation a finding is; it does not encode how findings relate to one another.

### 8.3 Finding type to dimension relationship

A finding may impact one or more CAF dimensions. *(Founder Position #11)* The finding type does not predetermine which dimension is affected; the affected dimensions are established during Impact Assessment (Section 9). For example, an Inference-type finding may bear on Clarity, on Alignment, on Feasibility, or on several at once, depending on the nature of the understanding being inferred (Section 6).

---

## 9. Impact Assessment Model

A finding's influence on CAF is established through **Impact Assessment**, which is separate from the recording of the finding itself. *(Founder Position #9)*

Impact Assessment evaluates four factors: *(Founder Position #10)*

1. **Significance** — the importance of the finding to the integrity of project understanding.
2. **Affected CAF Dimensions** — which of Clarity, Alignment, and Feasibility the finding bears upon (one or more).
3. **Evidence Support** — the degree to which the finding, and the understanding it concerns, is supported by evidence.
4. **Scope of Impact** — the breadth of understanding the finding affects.

Together, these factors determine **how findings influence the assessment of understanding integrity.** *(Founder Position #10)* Impact Assessment is the bridge between an observed finding and its contribution to CAF: it is where significance, context, evidence support, and affected dimensions are weighed in judgment — not in formula.

Impact Assessment is also where inter-finding relationships are evaluated. Because the taxonomy is flat (Section 8.2), root-cause and downstream relationships between findings are reasoned about here rather than encoded structurally.

**Future extensions.** Impact Assessment may, in future versions, also include Assessment Confidence and Root Cause Relationships. *(Founder Position #10)* These are noted as planned extensions and are not part of this model (see Section 12).

---

## 10. CAF Assessment Pipeline

CAF is determined through a directed reasoning pipeline. Each stage feeds the next; the pipeline expresses how raw information becomes an assessment of understanding integrity, and how that assessment is, in turn, consumed downstream.

```text
Evidence
  ↓
Inference
  ↓
Finding
  ↓
Impact Assessment
  ↓
CAF
  ↓
Confidence
```

Reading the pipeline:

- **Evidence** is information contributing to OSLO's understanding of project reality (Section 5).
- **Inference** is the characteristic of understanding that arises where understanding is synthesized rather than directly evidenced (Section 6). Inference does not bypass the pipeline; it contributes findings.
- **Finding** is an observation about understanding relevant to integrity (Section 7), classified by a flat taxonomy of finding types (Section 8).
- **Impact Assessment** evaluates each finding's significance, affected dimensions, evidence support, and scope (Section 9), establishing how the finding influences the assessment.
- **CAF** is the resulting assessment of the integrity of project understanding across the three independent dimensions (Sections 3–4), determined by the interaction of evidence and findings.
- **Confidence** is a **downstream consumer** of CAF. It is named here only to position CAF within OSLO's larger reasoning chain. Confidence is defined in a separate document and is not specified, calculated, or otherwise elaborated here.

The pipeline is **event-driven** end to end: it advances when evidence changes or findings change, and not merely with the passage of time (Section 4, Founder Position #4).

---

## 11. Assessment Principles

The following principles summarize the commitments that govern any CAF assessment under this model. They are restatements of the founder positions, consolidated for reference.

1. **CAF assesses integrity of understanding, not outcome success.** *(P#1)*
2. **CAF has three independent dimensions** — Clarity, Alignment, Feasibility — each an assessment target. *(P#2)*
3. **A single finding may impact multiple dimensions.** *(P#2, P#11)*
4. **CAF claims neither certainty nor truth**; it reflects supportable integrity given current evidence. *(P#3)*
5. **CAF is event-driven**; it changes only when evidence or findings change. *(P#4)*
6. **CAF is determined by the interaction of evidence and findings**; neither alone is sufficient. *(P#5)*
7. **Evidence strengthens, findings reduce** the assessed integrity of understanding. *(P#5)*
8. **Inference lowers integrity relative to validated evidence**; validating inferences raises it. *(P#6)*
9. **Inference is a characteristic of understanding, not a dimension**; it acts through findings. *(P#7)*
10. **Evidence is defined by contribution to understanding**, not by source or container. *(P#8)*
11. **Findings are inputs; dimensions are targets.** Findings are categorized by type, not by dimension. *(P#11)*
12. **Findings do not inherently determine impact**; impact is established by separate assessment. *(P#9, P#10)*
13. **The taxonomy is flat**; finding relationships are reasoned in Impact Assessment, not encoded in structure. *(P#13)*

---

## 12. Future Evolution

The following are explicitly noted as outside Release 1 and outside this assessment model. They are recorded to mark the model's boundary, not to define future behavior:

- **Environmental signals.** Future versions of OSLO may incorporate environmental signals that affect CAF. Release 1 CAF is driven by evidence and findings only. *(Founder Position #4)*
- **Impact Assessment extensions.** Future extensions of Impact Assessment may include **Assessment Confidence** and **Root Cause Relationships**. *(Founder Position #10)*

No scoring model, weighting scheme, threshold, calculation, confidence definition, UI visualization, MRI implementation, or recommendation logic is defined or implied by this document. Each belongs to a separate, future specification.

---

## 13. Summary

CAF is OSLO's model for assessing the integrity of project understanding — the soundness of the interpretation on which outcome success depends, not the outcome itself. It assesses that integrity across three independent dimensions, Clarity, Alignment, and Feasibility, each a target of assessment rather than a category of input.

CAF reasons from evidence and findings. Evidence — any information that contributes to understanding, from any trusted source — strengthens assessed integrity. Findings — observations about understanding, classified by a flat taxonomy of seven finding types — reduce it. Inference is a characteristic of understanding, not a dimension; it lowers integrity until validated and influences CAF through the findings it contributes. Neither evidence nor findings determines CAF alone; the assessment emerges from their interaction, and it changes only when they change.

A finding does not by itself determine its influence. Influence is established through Impact Assessment, which weighs significance, affected dimensions, evidence support, and scope — and which is also where relationships between findings are reasoned about, since the taxonomy itself is flat. The resulting assessment, CAF, is then consumed downstream by Confidence, which this document references but does not define.

This is an assessment model: it defines how CAF reasons. It does not define how CAF is scored.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | CAF Purpose (integrity, not outcome) | §1, §2, §11(1) |
| #2 | CAF Structure (3 independent dimensions; multi-dimension findings) | §3, §11(2,3) |
| #3 | CAF Epistemology (no certainty/truth; supportable integrity) | §4, §11(4) |
| #4 | CAF Dynamics (event-driven; no time decay; future environmental signals) | §4, §10, §12 |
| #5 | CAF Determination (evidence × findings; neither alone) | §4, §5, §7, §11(6,7) |
| #6 | Evidence vs Inference (inference lowers integrity; validation raises it) | §6, §11(8) |
| #7 | Inference (characteristic, not dimension; acts via findings) | §6, §8.3, §11(9) |
| #8 | Evidence (definition; sources; artifacts ≠ definition) | §5, §11(10) |
| #9 | Findings (definition; not inherently impactful) | §7, §9, §11(12) |
| #10 | Impact Assessment (4 factors; future extensions) | §9, §12 |
| #11 | Finding Taxonomy Structure (by type, not dimension; targets vs inputs) | §7, §8, §11(11) |
| #12 | Canonical Finding Types (7 types + definitions) | §8.1 |
| #13 | Flat Taxonomy (peer types; relationships via Impact Assessment) | §8.2, §9, §11(13) |

All thirteen founder positions are represented.

**Exclusion checklist**

- No numerical scoring — confirmed.
- No weighting — confirmed.
- No thresholds — confirmed.
- No percentages — confirmed.
- No confidence-calculation logic — confirmed (Confidence referenced only as a downstream consumer, §10).
- No formulas — confirmed.
- No UI / visualization / MRI implementation details — confirmed.
- No recommendation logic — confirmed.

*CAF Assessment Model v1 complete. Formalizes the founder-approved positions without reinterpretation or extension. Defines the assessment model only; the scoring model is out of scope. Subject to governance review before adoption.*
