# Finding Model v1

**Document:** FINDING_MODEL_V1.md
**Status:** Specification of the Finding Model (founder-approved positions formalized)
**Consumes / extends (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md`
**Date:** 2026-05-31

> **Scope.** This document defines the **Finding Model** — what a Finding is as a governable object, how Findings relate to assessment, CAF, Reliability, and Outcome Confidence, how they behave, how they can be resolved, and how they support Recommendations. It does **not** define recommendation logic, workflow behavior, UI implementation, scoring formulas, confidence formulas, reliability formulas, MRI visualization, or overlay behavior. Qualitative usage follows the related models; no numeric value or formula is fixed here.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, and Overlay models are consumed and (for the finding definition) extended, not modified. Canonical terminology is preserved; the flat finding taxonomy defined in `CAF_ASSESSMENT_MODEL_V1.md` is preserved without alteration.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Finding Model**: the Finding as a *governable object* that sits between assessment and action.

This document defines:

- what a Finding is as a governable object;
- how Findings relate to assessment;
- how Findings relate to CAF;
- how Findings relate to Reliability;
- how Findings relate to Outcome Confidence;
- how Findings behave;
- how Findings can be resolved;
- how Findings support Recommendations.

It is a conceptual and behavioral model. It defines no workflow, no UI, and no formula.

---

## 2. Finding Overview

**A Finding is a governable observation about project understanding.** *(Finding Position #1)* This **extends, but does not replace,** the CAF Assessment Model definition — *"a finding is an observation about project understanding that is relevant to the assessment of understanding integrity."* The Finding Model adds the *governable* character: a Finding has lifecycle state, may be resolved, may be grouped, may be related, and may have ownership — while remaining exactly the observation the Assessment Model defines.

**Findings are generated through assessment; Findings are not assessments.** *(Finding Position #2)* CAF is the assessment. A Finding is an **object produced through assessment** — the durable, governable record of an observation the assessment surfaced. The assessment evaluates; the Finding is a thing the evaluation yields.

**Findings are descriptive.** *(Finding Position #12)* A Finding describes something observed about understanding. **Findings do not prescribe actions; Recommendations prescribe actions.** A Finding states *what was observed*; it never states *what to do*.

---

## 3. Relationship To Assessment

A Finding and an assessment are different kinds of thing:

- **CAF is the assessment** — the evaluation of understanding integrity.
- **A Finding is an object produced through that assessment** — not the evaluation itself.

This separation matters for everything downstream: because a Finding is an object rather than an assessment, it can carry state, ownership, relationships, and a history, and it can be acted upon by Recommendations — none of which would be coherent for an assessment value. The assessment produces and updates Findings; Findings never produce or replace the assessment.

---

## 4. Relationship To CAF

CAF assesses understanding integrity. Findings relate to CAF through a single, bounded channel:

- **Findings contribute to CAF through Impact Assessment.** A Finding's influence on CAF is established by its Impact Assessment, as defined in the CAF models — never by the Finding intrinsically.
- **Findings may influence one or more CAF dimensions.** A Finding may impact Clarity, Alignment, Feasibility, or multiple dimensions. *(Finding Position #3)* Which dimensions, and how much, is settled in Impact Assessment, preserving the Assessment Model's flat taxonomy (the Finding's type does not predetermine its dimension or magnitude).
- **Findings do not equal CAF, and do not independently score CAF.** A Finding is not a CAF value and computes nothing about CAF on its own.

**Recommendations and CAF.** **Recommendations operate on Findings, not directly on CAF.** *(Finding Position #10)* CAF provides the *assessment context*; the Finding provides the *actionable object*. This is why the Finding, not the CAF dimension, is the unit a Recommendation addresses.

**Resolution and CAF.** **Resolving a Finding may change CAF, Reliability, and Outcome Confidence — but the relationship is not guaranteed.** *(Finding Position #11)* A resolved Finding may improve CAF, leave CAF unchanged, or expose new Findings. Resolution withdraws or lessens the Finding's contribution (per the CAF Scoring Model), but whether the dimension moves materially depends on the rest of the assessment.

---

## 5. Relationship To Reliability

- **Findings do not directly determine Reliability.** Reliability is determined by Coverage, Evidence Availability, and Assessability (Reliability Model), not by findings.
- **Resolution may *indirectly* affect Reliability.** Resolving a Finding can affect Reliability when the act of resolution adds evidence, improves assessability, or expands coverage — because those are Reliability's actual inputs. The Finding does not change Reliability; the evidence or coverage change that accompanied its resolution does.

This preserves the Reliability Model exactly: Reliability reads the conditions of the evidence surface, not the findings derived from it. A Finding's resolution touches Reliability only by changing those surface conditions.

---

## 6. Relationship To Outcome Confidence

Outcome Confidence consumes CAF and Reliability (Confidence Model).

- **Findings influence Outcome Confidence indirectly** — through their effects on CAF, and in some cases, through resolution-driven changes to Reliability.
- **Findings do not directly determine Outcome Confidence.** There is no path from a Finding to Confidence that does not pass through CAF or Reliability.

A Finding therefore reaches the summarized confidence signal only by way of the assessment layers that Confidence actually consumes.

---

## 7. Finding Philosophy

**Findings sit between assessment and action.** They are the **bridge between understanding and improvement**: assessment produces them, and improvement acts upon them.

The conceptual chain in which Findings sit:

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
Reliability
  ↓
Outcome Confidence
  ↓
MRI
  ↓
Overlay
  ↓
Finding attention
  ↓
Recommendation
  ↓
Action
```

The Finding appears twice in spirit in this chain — first as the observation produced from evidence and inference that feeds Impact Assessment and CAF, and later as the object that, once brought to attention through MRI and Overlays, a Recommendation acts upon to drive action. This dual role is precisely what makes the Finding the bridge: it is both an *input to assessment* and the *actionable object of improvement*. It is descriptive throughout; the prescriptive step (Recommendation → Action) lies beyond the Finding and is defined separately.

---

## 8. Finding Lifecycle Model

**Findings have lifecycle state; Findings are not static observations.** *(Finding Position #6)* A Finding is a governable object whose current state can change over the life of the project.

**Lifecycle concepts.** **Findings may appear, change, resolve, reopen, or disappear as project understanding changes.** *(Finding Position #5)* These are the lifecycle *concepts* the model commits to:

- **Appear** — a Finding comes into being when assessment surfaces a new observation.
- **Change** — a Finding's particulars or assessed impact change as understanding changes.
- **Resolve** — a Finding's current state becomes resolved.
- **Reopen** — a previously resolved Finding returns to an active state.
- **Disappear** — a Finding ceases to be a current observation.

Consistent with Founder Position #6, this model defines the lifecycle *concepts* and deliberately **avoids over-prescribing implementation-specific status values**; the precise status vocabulary is left to a future, owner-approved definition.

**Resolution preserves history.** **Findings may be resolved. Resolving a Finding does not erase history.** *(Finding Position #4)* Resolution changes the *current state* of the Finding while **preserving the record** of the Finding. A resolved Finding remains part of the project's history; resolution is a state transition, not a deletion. This is what allows a resolved Finding to be reopened, and what keeps the understanding timeline truthful.

**Event-driven.** **Findings are event-driven objects.** *(Finding Position #5)* They appear, change, resolve, reopen, or disappear **as project understanding changes**, and **do not change merely because time passes.** This inherits the chain's event-driven discipline: a Finding moves when evidence, findings, or their assessment change — never on the clock alone.

---

## 9. Finding Relationship Model

Findings may be organized — through relationships and through grouping — without their identity or the flat taxonomy being altered.

### 9.1 Relationships

**Findings may be related. Relationships do not alter Finding identity.** *(Finding Position #8)* Relationships may include **root-cause, downstream effect, dependency, similarity, or supporting/contradicting** relationships.

Crucially, **these relationships do not alter the flat finding taxonomy defined in `CAF_ASSESSMENT_MODEL_V1.md`.** The taxonomy classifies *what kind* of observation each Finding is and remains flat; relationships describe how Findings *relate to one another* and are reasoned about separately (consistent with the Assessment Model, where inter-finding relationships are evaluated through Impact Assessment, not encoded in the taxonomy). A related Finding is still its own Finding, of its own type.

### 9.2 Grouping

**Findings may be grouped. Grouping does not change the underlying Findings.** *(Finding Position #7)* **A group is a navigational or explanatory structure, not a replacement for individual Findings.** Grouping organizes Findings for attention and explanation; it neither merges them into a new object nor alters any of them. Removing a group leaves every Finding exactly as it was.

---

## 10. Finding Ownership Model

**Findings may have ownership.** *(Finding Position #9)* Ownership may refer to the **person, role, stakeholder, reviewer, or system actor** responsible for **addressing, validating, reviewing, or clarifying** the Finding.

Ownership is a responsibility relationship, not a causal one: **ownership does not imply the owner caused the Finding.** An owner is who is responsible for *acting on* a Finding, not who is to blame for *its existence*. Ownership, like relationships and grouping, is a governable attribute of the Finding object; it does not change the underlying observation or its assessment.

---

## 11. Finding Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no formula and no workflow.

### Example A — a Finding appears
- **Trigger:** evidence does not support a required element of understanding; a Missing Information Finding appears.
- **Result:** the Finding exists as a **governable object** — an observation with state, available for relationships, grouping, ownership, and (later) resolution. It is descriptive: it records that required understanding is absent, without prescribing a fix.

### Example B — a Finding is resolved by evidence
- **Trigger:** a stakeholder provides evidence that resolves the Finding.
- **Result:** the Finding's **state changes** to resolved; **history remains preserved** (the Finding is not erased); and **CAF may change**, because the resolved Finding's contribution is withdrawn or lessened. Whether CAF moves materially is not guaranteed (Section 4).

### Example C — a Finding is grouped
- **Trigger:** a Finding is grouped with related Findings.
- **Result:** the **group changes navigation and explanation**; the **underlying Findings remain unchanged.** The grouping is a structure over the Findings, not a modification of them (Section 9.2).

### Example D — a Recommendation is generated from a Finding
- **Trigger:** a Recommendation is generated from a Finding.
- **Result:** the **Recommendation operates on the Finding, not directly on CAF.** The Finding is the actionable object; CAF is the assessment context (Section 4). The Recommendation's own logic is defined separately and is out of scope here.

### Example E — resolution without CAF improvement
- **Trigger:** a Finding is resolved, but CAF does not improve.
- **Result:** **resolution does not guarantee CAF improvement.** Resolving the Finding may expose additional Findings, or may reduce the prior impact without changing the dimension materially. The relationship between resolution and CAF is real but not guaranteed (Founder Position #11).

---

## 12. Preserved Model Principles

The Finding Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Finding Model preserves it |
|---|---|
| A finding is an observation relevant to integrity (Assessment Model) | Extended to *governable observation*; the original definition is retained, not replaced (§2) |
| Findings are inputs; impact comes from Impact Assessment | Findings influence CAF only through Impact Assessment; never intrinsically (§4) |
| Flat finding taxonomy | Relationships and grouping never alter the flat taxonomy (§9) |
| Findings reduce; resolution removes the reduction (Scoring Model) | Resolving a Finding withdraws/lessens its contribution; CAF change not guaranteed (§4, §11) |
| Reliability is independent of findings | Findings do not determine Reliability; resolution affects it only via evidence/coverage/assessability (§5) |
| Confidence derives from CAF and Reliability | Findings reach Confidence only indirectly, through CAF and sometimes Reliability (§6) |
| MRI is the descriptive visualization layer | Findings are made visible by MRI; the Finding Model defines no visualization (§7) |
| Overlays manage attention; descriptive, not prescriptive | Findings receive attention through Overlays; the Finding Model defines no overlay behavior (§7) |
| Descriptive vs prescriptive | Findings remain descriptive; Recommendations remain prescriptive (§2, §7) |
| Event-driven across the chain | Findings change only as understanding changes, never on time alone (§8) |

Findings **must remain descriptive**; Recommendations **must remain prescriptive**; and Findings **must not redefine** CAF, Reliability, Confidence, MRI, or Overlays.

---

## 13. Future Evolution

Future versions may add:

- advanced Finding lifecycle states;
- Finding priority models;
- Finding ownership workflows;
- Finding escalation;
- Finding review requests;
- Finding grouping rules;
- root-cause analysis;
- Finding-to-Recommendation generation logic.

These are future capabilities. This document defines the **Finding Model only** — the governable object, its lifecycle concepts, its relationships, grouping, and ownership at the conceptual level. Status vocabularies, priority and escalation models, ownership and review workflows, grouping rules, root-cause analysis, and Recommendation-generation logic are defined elsewhere, not here.

---

## 14. Summary

A Finding is a governable observation about project understanding — the durable, stateful object produced through assessment, extending the CAF Assessment Model's definition without replacing it. Findings are generated through assessment but are not assessments; CAF is the assessment, and a Finding is a thing the assessment yields. Findings are descriptive throughout; they never prescribe.

Findings influence CAF only through Impact Assessment, across one or more dimensions, and never score CAF themselves. They do not directly determine Reliability — Reliability reads coverage, evidence availability, and assessability — though resolving a Finding can affect Reliability indirectly by changing those conditions. They reach Outcome Confidence only indirectly, through CAF and sometimes Reliability. As governable objects, Findings have lifecycle state (appear, change, resolve, reopen, disappear), are event-driven, and preserve history on resolution; they may be related and grouped without altering their identity or the flat taxonomy, and may carry ownership that assigns responsibility without implying causation.

Findings are the bridge between understanding and improvement: assessment produces them, MRI and Overlays bring them to attention, and Recommendations — which operate on Findings, not directly on CAF — turn attention into action. This document defines that model; it does not define recommendation logic, workflows, UI, visualization, overlay behavior, or any scoring formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Governable observation; extends, not replaces, the Assessment Model definition | §2 |
| #2 | Generated through assessment; Findings are not assessments | §2, §3 |
| #3 | May influence one or more CAF dimensions | §4 |
| #4 | May be resolved; resolution preserves history | §8 |
| #5 | Event-driven; appear/change/resolve/reopen/disappear; not by time | §8 |
| #6 | Have lifecycle state; define concepts, avoid over-prescribing status values | §8 |
| #7 | May be grouped; grouping is navigational/explanatory, not a replacement | §9.2 |
| #8 | May be related; relationships do not alter identity or the flat taxonomy | §9.1 |
| #9 | May have ownership; ownership does not imply causation | §10 |
| #10 | Recommendations operate on Findings, not directly on CAF | §4, §7 |
| #11 | Resolution may change CAF/Reliability/Confidence; not guaranteed | §4, §11 (Ex. E) |
| #12 | Findings are descriptive; Recommendations prescribe | §2, §7 |

All twelve founder positions are represented.

**Required behavior examples:** A (Finding appears as a governable object), B (resolved by evidence; state changes, history preserved, CAF may change), C (grouped; navigation/explanation change, Findings unchanged), D (Recommendation operates on the Finding, not CAF), E (resolved but CAF does not improve) — all included and explained conceptually (§11).

**Exclusion checklist**
- Findings are governable observations — confirmed (§2).
- Findings are generated through assessment but are not assessments — confirmed (§2, §3).
- Findings remain descriptive — confirmed (§2, §7, §12).
- Recommendations remain prescriptive — confirmed (§2, §7, §12).
- Recommendations operate on Findings, not directly on CAF — confirmed (§4, Ex. D).
- Findings may influence CAF through Impact Assessment — confirmed (§4).
- Findings do not directly determine Reliability — confirmed (§5).
- Findings do not directly determine Outcome Confidence — confirmed (§6).
- Resolution preserves history — confirmed (§8).
- No recommendation logic — confirmed (§7, §13).
- No workflow implementation details — confirmed (workflows named only as out-of-scope future, §13).
- No UI implementation details — confirmed.
- No scoring formulas — confirmed.
- Flat taxonomy and all six upstream models unmodified — confirmed (consumed/extended only).

*Finding Model v1 complete. Formalizes the founder-approved finding positions; defines the Finding as a governable, event-driven, descriptive object produced through assessment that influences CAF only via Impact Assessment, reaches Reliability and Confidence only indirectly, preserves history on resolution, and serves as the actionable object on which Recommendations operate. Defines the model only — not lifecycle status vocabularies, workflows, UI, or recommendation logic. Subject to governance review before adoption.*
