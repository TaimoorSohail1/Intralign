# Resolution Candidate Model v1

**Document:** RESOLUTION_CANDIDATE_MODEL_V1.md
**Status:** Specification of the Resolution Candidate Model — **the first Governance Domain object**
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `MODEL_LINEAGE_INDEX_V1.md`
**Date:** 2026-05-31

> **Architecture V1 classification (added by the Architecture V1 Simplification Refactor):** **Future Architecture — Outcome Orchestration / Agent Governance.** This model is **preserved and specified in full** and is **not part of the active Architecture V1 (Planning Intelligence) system**; it is deferred for later activation. This classification is additive — **no model content below is changed, deprecated, or invalidated.** See `ARCHITECTURE_V1_REFACTOR_REPORT.md`.

> **Scope.** This document defines the **Resolution Candidate Model** — what a Resolution Candidate is, why it exists, how it relates to Findings, Recommendations, CAF, Reliability, Outcome Confidence, and Governance, how it behaves, and how it supports human validation. It establishes the **first governance object** in the OSLO architecture. It does **not** define review workflows, notification behavior, governance processes, approval workflows, user interfaces, disposition logic, recommendation logic, scoring formulas, or truth-promotion mechanisms. Those are future Governance Domain capabilities, defined elsewhere.
>
> **Position in the architecture.** The Model Lineage Index identifies the Governance Domain as an emerging area and names the Resolution Candidate as a candidate future model. This document begins specifying that domain by formalizing its first object; it does not modify the Index or any Understanding Domain model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The eight upstream models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Resolution Candidate Model**: the first governance object — a proposed resolution to a Finding, surfaced for human evaluation.

This document defines:

- what a Resolution Candidate is;
- why Resolution Candidates exist;
- how Resolution Candidates relate to Findings;
- how Resolution Candidates relate to Recommendations;
- how Resolution Candidates relate to Governance;
- how Resolution Candidates behave;
- how Resolution Candidates support human validation.

It is a conceptual and behavioral model. It defines no workflow, no governance process, no notification, and no formula.

---

## 2. Resolution Candidate Overview

**A Resolution Candidate is a proposed resolution to a Finding.** It **is not a Finding** and **is not a Recommendation**; it **represents a possible way a Finding may be resolved.** *(Resolution Candidate Position #1)*

**Resolution Candidates are governance objects.** They **exist to support validation, clarification, review, and decision-making**, and they **are not assessment objects.** *(Resolution Candidate Position #3)* This makes the Resolution Candidate a new *category* of object: distinct from the descriptive assessment objects (such as Findings) and from the prescriptive Recommendation object — it is the first object whose purpose is governance.

**Resolution Candidates are proposals; they are not truth.** They **do not become truth merely because they exist.** *(Resolution Candidate Position #5)* A candidate is a possibility put forward for consideration, nothing more.

**Resolution Candidates require human evaluation.** Human evaluation remains **external to this model**; this model only establishes that candidates exist *for* evaluation. *(Resolution Candidate Position #6)* The Resolution Candidate is the object that makes a Finding's possible resolution explicit and available to a human; it does not perform, simulate, or pre-empt that human judgment.

**Generated from assessment context.** Resolution Candidates are generated from assessment context — which may include Findings, Evidence, Inference, CAF, Reliability, and Outcome Confidence — which they **consume, not create.** *(Resolution Candidate Position #2)*

---

## 3. Relationship To Findings

- **Findings remain descriptive observations.** A Finding states what was observed about understanding.
- **Resolution Candidates are proposed resolutions.** A candidate proposes a possible way the Finding may be resolved.
- **Resolution Candidates operate on Findings.**
- **Resolution Candidates do not replace Findings.**
- **Resolution Candidates do not become Findings.**

**Multiplicity.** **Multiple Resolution Candidates may exist for a single Finding** — a Finding may have **more than one plausible resolution**, and OSLO may **surface multiple candidates simultaneously.** *(Resolution Candidate Position #4)*

**Non-alteration.** **Resolution Candidates do not directly alter Findings.** *(Resolution Candidate Position #8)* A candidate is a proposal; **acceptance and subsequent action may eventually alter a Finding** — the candidate itself never does. This preserves the Finding Model: a Finding changes only as understanding changes, never because a proposal was put forward about it.

---

## 4. Relationship To Recommendations

Resolution Candidates and Recommendations are **distinct objects** that must not be conflated:

- **Recommendations** suggest actions intended to **improve understanding**; they are **improvement-oriented** and prescriptive, and they live in the Understanding Domain.
- **Resolution Candidates** propose **possible resolutions to Findings** for human evaluation; they are **governance-oriented**, and they live in the Governance Domain.

Both consume assessment context, both relate to Findings, and both influence assessment only through action — but their purpose differs. A Recommendation answers *"what should the user do to improve understanding?"* A Resolution Candidate answers *"here is a plausible way this Finding could be resolved — for human evaluation."* One drives improvement; the other surfaces a proposal for governed resolution. They are different objects with different orientations, and neither replaces the other.

---

## 5. Relationship To CAF

CAF remains the assessment layer.

- **Resolution Candidates may be informed by CAF.** CAF can be part of the assessment context that shapes a candidate.
- **Resolution Candidates do not alter CAF.** *(Resolution Candidate Position #9)*

**CAF changes only when understanding changes.** A Resolution Candidate, being a proposal, changes nothing in CAF; only accepted actions and the resulting evidence changes may affect assessment (Section 9).

---

## 6. Relationship To Reliability

Reliability remains the supportability layer.

- **Resolution Candidates may be informed by Reliability.**
- **Resolution Candidates do not alter Reliability.** *(Resolution Candidate Position #9)*

A candidate can take into account how trustworthy the assessment is, but it neither determines nor changes Reliability, which moves only on its own inputs and only following action.

---

## 7. Relationship To Outcome Confidence

Outcome Confidence remains the confidence layer.

- **Resolution Candidates may be informed by Confidence.**
- **Resolution Candidates do not alter Confidence.** *(Resolution Candidate Position #9)*

A candidate can be informed by how confident OSLO is, but changes none of the consolidation that produces Confidence and none of its value.

---

## 8. Relationship To Governance

**Resolution Candidates are the first governance object.** *(Resolution Candidate Position #12)* They **establish a mechanism through which proposed resolutions may later be reviewed, validated, accepted, rejected, or promoted through governance processes.**

**This document does not define those processes.** Review, validation, disposition, routing, and truth promotion are future Governance Domain capabilities (Section 14). The Resolution Candidate establishes only the *object* those future processes will act upon — the explicit, evaluable proposal that gives governance something to govern. It is **the bridge between Understanding and Governed Understanding** (Section 9).

---

## 9. Resolution Candidate Philosophy

Two domains ask two different questions:

- The **Understanding Domain** answers: *"What do we understand?"*
- The **Governance Domain** answers: *"What are we willing to accept as true?"*

**Resolution Candidates represent the transition between those two questions.** Understanding produces Findings about reality; governance decides what to accept about them. The Resolution Candidate is the object that carries a Finding from the first question toward the second — making a possible resolution explicit so that a human, and later a governance process, can evaluate it.

The conceptual relationship:

```text
Finding
  ↓
Resolution Candidate
  ↓
Human Evaluation
  ↓
Future Governance Processes
```

**Resolution Candidates exist to support governed resolution of understanding.** They are the first step out of pure assessment and into governance: assessment surfaces a Finding, a Resolution Candidate proposes how it might be resolved, and human evaluation — supported by future governance processes — decides. Nothing in this chain alters understanding on its own; as in the Understanding Domain, only action and resulting evidence change assessment.

---

## 10. Resolution Candidate Lifecycle Model

**Resolution Candidates are event-driven.** *(Resolution Candidate Position #11)* A candidate exists in relation to the Finding and assessment context that produced it, and it moves when those move.

**Lifecycle concepts.** A Resolution Candidate may **appear, change, withdraw, supersede one another, or disappear** as understanding changes:

- **generation** — a candidate is generated when a Finding and its assessment context admit a plausible resolution worth surfacing;
- **change** — a candidate changes when its Finding or assessment context changes;
- **withdrawal** — a candidate withdraws when its basis no longer holds;
- **supersession** — one candidate may supersede another as a more plausible resolution emerges;
- **evaluation outcome** — a candidate may be **accepted, rejected, superseded, withdrawn, or remain unresolved** *(Resolution Candidate Position #7)*. These are **conceptual outcomes**; the evaluation that produces them is external to this model (Section 2), and **no workflow implementation is defined.**

**Event-driven, not time-driven.** Candidates **do not change merely because time passes** *(Resolution Candidate Position #11)*. A candidate moves only as its Finding and assessment context change — inheriting the event-driven discipline of the whole architecture.

Consistent with the requirement to remain conceptual, this model defines the lifecycle *concepts* and does **not** prescribe implementation-specific states.

---

## 11. Resolution Candidate Explanation Model

**Resolution Candidates are explainable.** *(Resolution Candidate Position #10)* Every candidate should be traceable to its basis:

```text
Finding
  ↓
Assessment Context
  ↓
Resolution Candidate
```

An explanation of a Resolution Candidate should identify:

- **the originating Finding** — the Finding the candidate proposes to resolve;
- **the relevant assessment context** — the Evidence, Inference, CAF, Reliability, and/or Outcome Confidence that informed it;
- **the rationale for candidate generation** — why this resolution is plausible given that Finding and context.

**Candidates should never appear disconnected from their basis.** A Resolution Candidate that cannot be traced to a Finding and its assessment context would violate this model. As elsewhere in the architecture, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring by which a candidate is produced.

---

## 12. Resolution Candidate Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no workflow and no formula.

### Example A — a candidate exists for evaluation
- **Finding:** Ambiguous KPI definition.
- **Resolution Candidate:** Interpretation A.
- **Result:** the candidate **exists for evaluation** — a possible resolution of the ambiguous-KPI Finding is made explicit and available for human evaluation. It is a proposal, not truth, and it alters nothing on its own.

### Example B — multiple plausible resolutions
- **State:** one Finding generates multiple Resolution Candidates.
- **Result:** **multiple plausible resolutions exist simultaneously** (Section 3, Position #4). OSLO surfaces them together; the model affirms their coexistence without deciding among them.

### Example C — a candidate responds to context
- **State:** assessment context changes.
- **Result:** the **Resolution Candidate changes.** Candidates are event-driven (Section 10): a shift in the Finding or its context can change, withdraw, or supersede a candidate.

### Example D — a candidate is rejected
- **State:** a Resolution Candidate is rejected.
- **Result:** the **Finding remains; assessment remains unchanged.** Rejection is a conceptual evaluation outcome; because nothing was acted upon, no evidence entered the loop, so CAF, Reliability, and Confidence are untouched. The Finding still stands, available for other candidates.

### Example E — a candidate is accepted and acted upon
- **State:** a Resolution Candidate is accepted and acted upon; evidence changes.
- **Result:** the **Finding may change; CAF may change; Confidence may change.** The candidate influenced assessment **only through action**: acceptance led to action, action produced new evidence, and the assessment chain re-ran. The candidate itself altered nothing — the action did (Sections 5–7, Position #9). (Per the Finding and Recommendation models, such change is possible but not guaranteed.)

---

## 13. Preserved Model Principles

The Resolution Candidate Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Resolution Candidate Model preserves it |
|---|---|
| Findings are descriptive observations | Findings remain descriptive; candidates are proposals, not observations (§3) |
| Findings change only as understanding changes | Candidates never directly alter Findings; only action does (§3) |
| Recommendations are prescriptive, improvement-oriented | Recommendations remain prescriptive; candidates are governance-oriented and distinct (§4) |
| CAF assesses understanding integrity | Candidates may be informed by CAF but never alter it (§5) |
| Reliability is independent supportability | Candidates may be informed by Reliability but never alter it (§6) |
| Confidence derives from CAF and Reliability | Candidates may be informed by Confidence but never alter it (§7) |
| MRI / Overlay are the visualization and attention layers | Candidates define no visualization or attention behavior; they consume assessment context only (§2) |
| Assessment moves only on its real inputs via action | Candidates influence assessment only through accepted action and resulting evidence (§9, §12) |
| Event-driven and explainable across the architecture | Candidates are event-driven and explainable to their basis (§10, §11) |

Findings **remain descriptive**; Recommendations **remain prescriptive**; Resolution Candidates **remain governance objects**; and Resolution Candidates **must not redefine** the assessment models.

---

## 14. Future Evolution

Future versions may add:

- review workflows;
- governance routing;
- reviewer assignment;
- escalation;
- prioritization;
- disposition integration;
- truth-promotion integration.

These are future capabilities. This document defines the **Resolution Candidate Model only** — the first governance object, its lifecycle concepts, its explanation, and its relationships, at the conceptual level. The governance *processes* that will review, route, assign, escalate, prioritize, dispose of, or promote candidates are defined elsewhere, not here. So too are notification behavior, user interfaces, and any scoring.

---

## 15. Summary

A Resolution Candidate is a proposed resolution to a Finding — the first governance object in OSLO's architecture. It is not a Finding and not a Recommendation; it is a new category of object whose purpose is governance, surfacing a possible way a Finding may be resolved so that a human can evaluate it. It is generated from assessment context (Findings, Evidence, Inference, CAF, Reliability, Confidence) which it consumes but does not create, and it is a proposal — never truth merely by existing.

Resolution Candidates operate on Findings without replacing, becoming, or directly altering them; multiple plausible candidates may exist for one Finding at once. They may be informed by CAF, Reliability, and Confidence but alter none of them — only accepted action and resulting evidence change assessment. They are event-driven (appear, change, withdraw, supersede, disappear as understanding changes) and explainable, always traceable to an originating Finding, its assessment context, and a rationale. Their conceptual outcomes — accepted, rejected, superseded, withdrawn, or unresolved — arise from human evaluation, which this model establishes the need for but leaves external.

Resolution Candidates are the bridge between Understanding and Governed Understanding: the transition from *"what do we understand?"* to *"what are we willing to accept as true?"* This document opens the Governance Domain by defining its first object; it defines no governance process, workflow, notification, disposition, truth promotion, UI, or formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Proposed resolution to a Finding; not a Finding, not a Recommendation | §2, §3 |
| #2 | Generated from assessment context; consume, not create | §2 |
| #3 | Governance objects, not assessment objects | §2, §8 |
| #4 | Multiple candidates may exist for one Finding | §3 |
| #5 | Proposals, not truth | §2 |
| #6 | Require human evaluation; evaluation external to the model | §2, §9 |
| #7 | Accepted/rejected/superseded/withdrawn/unresolved; conceptual outcomes | §10 |
| #8 | Do not directly alter Findings; acceptance + action may | §3 |
| #9 | Do not directly alter CAF, Reliability, or Confidence | §5, §6, §7 |
| #10 | Explainable; traceable Finding → Assessment Context → Resolution Candidate | §11 |
| #11 | Event-driven; appear/change/withdraw/supersede/disappear; not by time | §10 |
| #12 | Exist within the Governance Domain; bridge Understanding → Governed Understanding | §8, §9 |

All twelve founder positions are represented.

**Required behavior examples:** A (candidate exists for evaluation), B (multiple plausible resolutions), C (event-driven change), D (rejected — Finding remains, assessment unchanged), E (accepted and acted upon — evidence changes, Finding/CAF/Confidence may change) — all included and explained conceptually (§12).

**Exclusion checklist**
- Resolution Candidates are distinct from Findings — confirmed (§2, §3).
- Resolution Candidates are distinct from Recommendations — confirmed (§4).
- Resolution Candidates are governance objects — confirmed (§2, §8).
- Resolution Candidates are proposals, not truth — confirmed (§2).
- Resolution Candidates require human evaluation — confirmed (§2, §9).
- Do not directly alter Findings — confirmed (§3).
- Do not directly alter CAF — confirmed (§5).
- Do not directly alter Reliability — confirmed (§6).
- Do not directly alter Confidence — confirmed (§7).
- Explainable — confirmed (§11).
- Event-driven — confirmed (§10).
- No workflow implementation — confirmed (§10, §14).
- No governance process implementation — confirmed (§8, §14).
- No notification behavior — confirmed (§14).
- No scoring formulas — confirmed.
- All nine indexed documents unmodified — confirmed (consumed only).

*Resolution Candidate Model v1 complete. Formalizes the founder-approved positions; defines the Resolution Candidate as OSLO's first governance object — a proposed, explainable, event-driven resolution to a Finding that requires human evaluation, alters nothing on its own, and bridges Understanding and Governed Understanding. Defines the model only — not governance processes, workflows, notification, disposition, truth promotion, UI, or formulas. Subject to governance review before adoption.*
