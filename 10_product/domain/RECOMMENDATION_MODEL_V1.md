# Recommendation Model v1

**Document:** RECOMMENDATION_MODEL_V1.md
**Status:** Specification of the Recommendation Model (founder-approved positions formalized)
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md`
**Date:** 2026-05-31

> **Scope.** This document defines the **Recommendation Model** — what a Recommendation is, how it relates to Findings and to CAF / Reliability / Outcome Confidence, how it behaves, how it supports improvement, and how it relates to user action. It does **not** define workflow implementation, UI implementation, recommendation ranking algorithms, recommendation scoring formulas, machine-learning models, automation behavior, autonomous execution, or notification behavior. Qualitative usage follows the related models; no algorithm or formula is fixed here.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, Overlay, and Finding models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Recommendation Model**: the prescriptive, advisory layer that suggests how to improve project understanding by acting on Findings.

This document defines:

- what a Recommendation is;
- how Recommendations relate to Findings;
- how Recommendations relate to CAF;
- how Recommendations relate to Reliability;
- how Recommendations relate to Outcome Confidence;
- how Recommendations behave;
- how Recommendations support improvement;
- how Recommendations relate to user action.

It is a conceptual and behavioral model. It defines no workflow, no UI, no ranking, no formula, and no automation.

---

## 2. Recommendation Overview

**A Recommendation is a prescriptive suggestion intended to improve project understanding.** *(Recommendation Position #1)* Recommendations are **advisory guidance**; they are **not assessments**. Where the assessment layers describe and evaluate understanding, a Recommendation *suggests how to improve it*.

**Recommendations prioritize improvement of understanding.** *(Recommendation Position #8)* They do **not** primarily optimize task completion, schedule completion, or resource utilization. Their primary purpose is improving understanding — consistent with OSLO's orientation toward understanding over activity.

**Recommendations are advisory; users retain authority over action.** *(Recommendation Position #11)* A Recommendation does not override user judgment. Accordingly, a Recommendation **may be accepted, rejected, deferred, or ignored**, and **these outcomes do not invalidate the Recommendation** — they represent **user choice**. *(Recommendation Position #12)* A rejected or ignored Recommendation was no less valid for not being taken.

---

## 3. Relationship To Findings

Findings remain the actionable object. The Recommendation's relationship to them is precise:

- **Recommendations operate on Findings.** *(Recommendation Position #2)* The Finding is the actionable object; a Recommendation addresses a Finding.
- **Recommendations do not replace Findings.**
- **Recommendations do not modify Findings.**
- **Recommendations provide suggested paths for addressing Findings.**

**Multiplicity and alternatives.** **Multiple Recommendations may exist for a single Finding** *(Recommendation Position #6)* — a Finding may have more than one valid improvement path. **Recommendations may differ while targeting the same Finding**, representing **alternative approaches** to improving understanding. *(Recommendation Position #7)* The model affirms that more than one valid path may exist for the same Finding; how (or whether) such alternatives are ordered is a future concern (Section 12) and is not defined here.

The Finding Model establishes that *Recommendations operate on Findings, not directly on CAF*; this model is the counterpart from the Recommendation side.

---

## 4. Relationship To CAF

CAF remains the assessment layer.

- **Recommendations consume CAF context.** CAF is part of the assessment context a Recommendation is generated from (Section 7).
- **Recommendations do not assess CAF.**
- **Recommendations do not modify CAF directly.**

A Recommendation operates on the Finding, not on CAF; **CAF provides assessment context**, the Finding provides the actionable object. *(Recommendation Position #2)* Any change to CAF that follows a Recommendation occurs only through user action (Section 7), never by the Recommendation itself.

---

## 5. Relationship To Reliability

Reliability remains the supportability layer.

- **Recommendations may be informed by Reliability.** Reliability can be part of the assessment context that shapes a Recommendation.
- **Recommendations do not modify Reliability directly.**

A Recommendation can take into account how trustworthy the assessment is, but it neither determines nor changes Reliability. Reliability moves only on its own inputs (Coverage, Evidence Availability, Assessability), and only following user action.

---

## 6. Relationship To Outcome Confidence

Outcome Confidence remains the confidence layer.

- **Recommendations may be informed by Confidence.** The summarized confidence signal can be part of the context that shapes a Recommendation.
- **Recommendations do not modify Confidence directly.**

A Recommendation can be informed by how confident OSLO is, but it performs none of the consolidation that produces Confidence and changes none of its value directly.

---

## 7. Recommendation Philosophy

**Recommendations sit between understanding and action.** They are generated from assessment context and point toward the action that can improve understanding.

**Generated from assessment context.** **Recommendations are generated from assessment context**, which **may include Findings, CAF, Reliability, and Outcome Confidence.** **Recommendations consume assessment context; they do not create it.** *(Recommendation Position #3)* The Recommendation is downstream of all assessment; it reads the assessed picture and suggests a path, adding no assessment of its own.

**Improvement happens through action, not through the Recommendation.** **Recommendations do not alter understanding; user action alters understanding.** A Recommendation **influences understanding only indirectly, through actions taken in response to it.** *(Recommendation Position #4)* Likewise, **Recommendations may influence CAF, Reliability, and Outcome Confidence only through user action; Recommendations themselves do not alter assessment signals.** *(Recommendation Position #9)*

**The improvement loop.** The conceptual chain in which Recommendations sit closes the loop:

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
Finding Attention
  ↓
Recommendation
  ↓
User Action
  ↓
Evidence
```

**Recommendations close the improvement loop.** They are **the mechanism by which understanding may improve** — but the mechanism completes only when a user acts. The loop returns to Evidence: a user acts on a Recommendation, that action produces new evidence, and the assessment chain re-runs. The Recommendation is the hinge between *understanding* (everything above it) and *action* (everything that follows), and it is action — not the Recommendation — that re-enters the loop as evidence.

---

## 8. Recommendation Lifecycle Model

**Recommendations are event-driven.** *(Recommendation Position #5)* A Recommendation exists in relation to the assessment context that produced it, and it moves when that context moves.

**Lifecycle concepts.** A Recommendation may **appear, change, retire, or reappear** as Findings and assessment context change:

- **generation** — a Recommendation is generated when a Finding and its assessment context call for a suggested improvement path;
- **change** — a Recommendation changes when its Finding or assessment context changes;
- **retirement** — a Recommendation retires when its basis no longer holds (for example, when its Finding is resolved);
- **reappearance** — a retired Recommendation may reappear if its basis returns.

**Event-driven, not time-driven.** **Recommendations do not change merely because time passes.** A Recommendation moves only when its underlying Findings and assessment context change — inheriting the event-driven discipline of the entire chain.

Consistent with the requirement to remain conceptual, this model defines the lifecycle *concepts* and **does not prescribe implementation-specific states**; a precise status vocabulary is left to a future, owner-approved definition.

---

## 9. Recommendation Explanation Model

**Recommendations are explainable.** *(Recommendation Position #10)* Every Recommendation should be traceable to its basis:

```text
Finding
  ↓
Assessment Context
  ↓
Recommendation
```

An explanation of a Recommendation should identify:

- **the originating Finding** — the actionable object the Recommendation addresses;
- **the relevant assessment context** — the CAF, Reliability, and/or Outcome Confidence context that shaped it;
- **the rationale** — why this Recommendation follows from that Finding and context.

**Recommendations should never appear disconnected from their basis.** A Recommendation that cannot be traced back to a Finding and its assessment context would violate this model. As with the upstream layers, this explanation reduces to a *basis*, not to a formula; the model remains conceptual and defines no scoring or ranking by which a Recommendation is produced or ordered.

---

## 10. Recommendation Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no algorithm, ranking, or formula.

### Example A — a Recommendation addresses a Finding
- **Finding:** Missing KPI.
- **Recommendation:** Define a measurable KPI.
- **Result:** the Recommendation **operates on the Finding** — it provides a suggested path for addressing that Finding (Section 3). It is prescriptive ("define a KPI"), in contrast to the descriptive Finding ("a required KPI is missing").

### Example B — a Recommendation responds to context
- **State:** the Finding remains unchanged; the assessment context changes.
- **Result:** the **Recommendation changes.** Recommendations respond to context (Section 7): even with the Finding fixed, a shift in CAF, Reliability, or Confidence context can change the suggested path. This is event-driven behavior (Section 8).

### Example C — alternative improvement paths
- **State:** one Finding produces multiple Recommendations.
- **Result:** **multiple valid improvement paths** exist for the same Finding (Sections 3, Positions #6–#7). The model affirms their validity without ordering them.

### Example D — a Recommendation is ignored
- **State:** the user ignores the Recommendation.
- **Result:** the **Recommendation remains advisory**; the user's choice does not invalidate it (Position #12). **Assessment remains unchanged until understanding changes** — because nothing was acted upon, no new evidence entered the loop, so CAF, Reliability, and Confidence are untouched.

### Example E — a Recommendation is acted upon
- **State:** the user acts on the Recommendation; evidence changes; the Finding resolves.
- **Result:** **CAF may change; Confidence may change.** The Recommendation influenced assessment **only through action**: the user's action produced new evidence, which resolved the Finding and re-ran the assessment chain (Sections 7, 9). The Recommendation itself altered nothing — the action did. (Per the Finding Model, CAF change is possible but not guaranteed.)

---

## 11. Preserved Model Principles

The Recommendation Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Recommendation Model preserves it |
|---|---|
| CAF assesses understanding integrity | Recommendations consume CAF context; they do not assess or modify CAF (§4) |
| Reliability measures supportability, independent of findings | Recommendations may be informed by Reliability but never modify it (§5) |
| Confidence derives from CAF and Reliability | Recommendations may be informed by Confidence but never modify it (§6) |
| MRI is the descriptive visualization layer | Recommendations are surfaced after MRI/Overlay attention; this model defines no visualization (§7) |
| Overlays manage attention; descriptive | Finding Attention precedes Recommendation in the chain; this model defines no overlay behavior (§7) |
| Findings are the actionable object; descriptive | Recommendations operate on Findings without replacing or modifying them (§3) |
| Findings descriptive vs Recommendations prescriptive | Findings remain descriptive; Recommendations remain prescriptive (§2, §3) |
| Event-driven across the chain | Recommendations change only as Findings/context change, never on time alone (§8) |
| Assessment signals move only on their real inputs | Recommendations move assessment only via user action that changes those inputs (§7, §9) |

Recommendations **must remain prescriptive**; Findings **must remain descriptive**; and Recommendations **must not redefine** CAF, Reliability, Confidence, MRI, Overlays, or Findings.

---

## 12. Future Evolution

Future versions may add:

- recommendation prioritization;
- recommendation ranking;
- recommendation confidence;
- recommendation bundling;
- recommendation automation;
- recommendation learning;
- recommendation personalization.

These are future capabilities. This document defines the **Recommendation Model only** — the prescriptive, advisory, event-driven, explainable suggestion at the conceptual level. Prioritization and ranking algorithms, recommendation-confidence scoring, bundling, automation and autonomous execution, learning and personalization, along with workflow, UI, and notification behavior, are defined elsewhere, not here.

---

## 13. Summary

A Recommendation is a prescriptive, advisory suggestion intended to improve project understanding. It is not an assessment; it operates on Findings — the actionable object — and not directly on CAF, which provides only assessment context. Recommendations are generated from assessment context (Findings, CAF, Reliability, and Outcome Confidence), which they consume rather than create, and they prioritize the improvement of understanding over task, schedule, or resource optimization.

A Recommendation alters nothing on its own: user action alters understanding, and a Recommendation influences CAF, Reliability, and Outcome Confidence only through the action taken in response to it. Recommendations are event-driven — they appear, change, retire, and reappear as Findings and context change, never on the passage of time — and explainable, always traceable to an originating Finding, its assessment context, and a rationale. They are advisory: users retain authority and may accept, reject, defer, or ignore a Recommendation without invalidating it.

In the conceptual chain, Recommendations close the improvement loop — the hinge between understanding and action, where a user's action becomes new evidence and the assessment chain re-runs. This document defines that model; it does not define workflow, UI, ranking, scoring, automation, autonomous execution, or notification behavior.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Prescriptive suggestion to improve understanding; advisory; not an assessment | §2 |
| #2 | Operate on Findings, not directly on CAF; Findings actionable, CAF context | §3, §4 |
| #3 | Generated from assessment context; consume, not create context | §7 |
| #4 | Do not alter understanding; user action does; indirect influence | §7 |
| #5 | Event-driven; appear/change/retire/reappear; not by time | §8 |
| #6 | Multiple Recommendations may exist for a single Finding | §3 |
| #7 | May differ targeting the same Finding; alternative approaches | §3 |
| #8 | Prioritize improvement of understanding, not task/schedule/resource | §2 |
| #9 | Influence CAF/Reliability/Confidence only through user action | §7 |
| #10 | Explainable; traceable Finding → Assessment Context → Recommendation | §9 |
| #11 | Advisory; users retain authority; do not override judgment | §2 |
| #12 | May be accepted/rejected/deferred/ignored; outcomes are user choice | §2 |

All twelve founder positions are represented.

**Required behavior examples:** A (operates on a Missing-KPI Finding), B (responds to context change), C (multiple improvement paths), D (ignored — remains advisory, assessment unchanged), E (acted upon — evidence changes, Finding resolves, CAF/Confidence may change) — all included and explained conceptually (§10).

**Exclusion checklist**
- Recommendations are prescriptive — confirmed (§2, §3).
- Recommendations operate on Findings — confirmed (§3).
- Recommendations do not operate directly on CAF — confirmed (§4).
- Recommendations are generated from assessment context — confirmed (§7).
- Recommendations are event-driven — confirmed (§8).
- Recommendations are explainable — confirmed (§9).
- Recommendations are advisory; users retain authority — confirmed (§2).
- May be accepted, rejected, deferred, or ignored — confirmed (§2, Ex. D).
- Influence CAF/Reliability/Confidence only through action — confirmed (§7, §9, Ex. E).
- No workflow implementation details — confirmed (named out-of-scope, §12).
- No UI implementation details — confirmed (§12).
- No ranking algorithms — confirmed (§3, §9, §12).
- No scoring formulas — confirmed.
- No automation / autonomous execution behavior — confirmed (§12).
- All seven upstream models unmodified — confirmed (consumed only).

*Recommendation Model v1 complete. Formalizes the founder-approved recommendation positions; defines the Recommendation as a prescriptive, advisory, event-driven, explainable suggestion that operates on Findings, is generated from assessment context, and influences CAF, Reliability, and Outcome Confidence only through user action — closing the improvement loop. Defines the model only — not workflow, UI, ranking, scoring, automation, or notification behavior. Subject to governance review before adoption.*
