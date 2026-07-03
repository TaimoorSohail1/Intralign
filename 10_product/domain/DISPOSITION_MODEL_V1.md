# Disposition Model v1

**Document:** DISPOSITION_MODEL_V1.md
**Status:** Specification of the Disposition Model — **a Governance Domain object**
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `REVIEW_REQUEST_MODEL_V1.md` · `MODEL_LINEAGE_INDEX_V1.md`
**Date:** 2026-05-31

> **Architecture V1 classification (added by the Architecture V1 Simplification Refactor):** **Future Architecture — Outcome Orchestration / Agent Governance.** This model is **preserved and specified in full** and is **not part of the active Architecture V1 (Planning Intelligence) system**; it is deferred for later activation. This classification is additive — **no model content below is changed, deprecated, or invalidated.** See `ARCHITECTURE_V1_REFACTOR_REPORT.md`.

> **Scope.** This document defines the **Disposition Model** — what a Disposition is, why Dispositions exist, how they relate to Findings, Resolution Candidates, Review Requests, Recommendations, CAF, Reliability, Outcome Confidence, and Governance, and how they support governed understanding. It establishes the governance object that **records evaluation outcomes**. It does **not** define governance authority, governance workflows, truth promotion, reviewer assignment, routing behavior, notification behavior, escalation logic, approval workflows, user interfaces, or scoring formulas. Those are future Governance Domain capabilities, defined elsewhere.
>
> **Position in the architecture.** The Governance Domain has been opened by the Resolution Candidate Model (proposed resolutions) and the Review Request Model (requests for evaluation). The Disposition is the next Governance Domain object: it records the *outcome* of an evaluation. This document does not modify the Model Lineage Index or any other model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The eleven referenced models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Disposition Model**: the governance object that records the outcome of an evaluation.

This document defines:

- what a Disposition is;
- why Dispositions exist;
- how Dispositions relate to Findings;
- how Dispositions relate to Resolution Candidates;
- how Dispositions relate to Review Requests;
- how Dispositions relate to Governance;
- how Dispositions support governed understanding.

It establishes the governance object that records evaluation outcomes. It is a conceptual and behavioral model: it defines no workflow, no authority, no truth promotion, and no formula.

---

## 2. Disposition Overview

**A Disposition is a governance object that records the outcome of an evaluation.** It **is not a Finding**, **not a Resolution Candidate**, **not a Review Request**, and **not a Recommendation.** *(Disposition Position #1)* It is a distinct governance object whose purpose is to make an evaluation's outcome durable and governable.

**A Disposition is not an evaluation.** It **records evaluation outcomes**; it **does not perform evaluation.** *(Disposition Position #2)* The evaluation happens elsewhere (the human evaluation established by the Review Request Model); the Disposition is the record of what that evaluation concluded.

**A Disposition is not governance authority.** It **records what was decided**; it **does not decide.** *(Disposition Position #3)* A Disposition holds no authority and exercises no judgment — it captures a decision that was made, without being the act of deciding.

**Traceable.** A Disposition **may reference Findings, Resolution Candidates, and Review Requests**, and is **traceable to the governance objects that preceded it.** *(Disposition Position #4)*

---

## 3. Relationship To Findings

- **Findings remain descriptive observations.**
- **Dispositions may reference Findings.**
- **Dispositions do not replace Findings.**
- **Dispositions do not directly alter Findings.** *(Disposition Position #7)*

A Disposition records the outcome of an evaluation that ultimately concerns a Finding; **subsequent actions may alter Findings**, but the Disposition itself never does. The Finding changes only as understanding changes.

---

## 4. Relationship To Resolution Candidates

- **Resolution Candidates remain proposals.**
- **Dispositions may record outcomes related to Resolution Candidates** — for example, recording that a particular candidate was accepted or rejected.
- **Dispositions do not alter Resolution Candidates.**

A Disposition captures *what was decided about* a proposed resolution; it does not change the proposal itself. The Resolution Candidate remains the proposal it was; the Disposition is the durable record of how it was evaluated.

---

## 5. Relationship To Review Requests

- **Review Requests request evaluation.**
- **Dispositions record outcomes of evaluations.**
- **Review Requests precede Dispositions.**
- **Dispositions do not replace Review Requests.**

The two are sequential governance objects: a Review Request asks for evaluation; once human evaluation has occurred, a Disposition records its outcome. The request and the record are distinct objects, and the record does not erase or stand in for the request that preceded it (Section 6).

---

## 6. Relationship To Recommendations

Recommendations and Dispositions are distinct objects:

- **Recommendations** remain prescriptive improvement suggestions — they **suggest**.
- **Dispositions** remain governance records — they **record**.

A Recommendation answers *"what should the user do to improve understanding?"* A Disposition answers *"what was decided about this proposed resolution?"* One suggests an action; the other records an outcome. **They are distinct objects** and neither replaces the other.

---

## 7. Relationship To CAF

CAF remains the assessment layer.

- **Dispositions may be informed by CAF.**
- **Dispositions do not alter CAF.** *(Disposition Position #8)*

A Disposition, being a record of an outcome, changes nothing in CAF; assessment changes only through evidence and understanding changes (Section 11).

---

## 8. Relationship To Reliability

Reliability remains the supportability layer.

- **Dispositions may be informed by Reliability.**
- **Dispositions do not alter Reliability.** *(Disposition Position #8)*

A Disposition can take into account how trustworthy an assessment is, but it neither determines nor changes Reliability.

---

## 9. Relationship To Outcome Confidence

Outcome Confidence remains the confidence layer.

- **Dispositions may be informed by Confidence.**
- **Dispositions do not alter Confidence.** *(Disposition Position #8)*

A Disposition can be informed by how confident OSLO is, but changes none of the consolidation that produces Confidence and none of its value.

---

## 10. Relationship To Governance

**Dispositions are governance objects.** They **provide durable records of evaluation outcomes.**

**This document does not define** authority, truth promotion, governance decisions, or governance policies. Those belong to future Governance Domain models. The Disposition establishes only the *object* that records an outcome — the durable, traceable record that future governance processes (and any audit of them) will rely upon. It does not confer authority, decide anything, or promote anything to truth.

---

## 11. Disposition Philosophy

Two domains ask two different questions:

- The **Understanding Domain** answers: *"What do we understand?"*
- The **Governance Domain** answers: *"What are we willing to accept as true?"*

**Dispositions exist because evaluations require durable recorded outcomes.** A human evaluation that concludes but leaves no record leaves nothing governable behind — **a human evaluation without a disposition leaves no governable record.** The Disposition is the object that captures the outcome so that governance has something durable to stand on.

The conceptual relationship:

```text
Finding
  ↓
Resolution Candidate
  ↓
Review Request
  ↓
Human Evaluation
  ↓
Disposition
  ↓
Future Governance Processes
```

**Disposition records. It does not evaluate. It does not decide. It does not govern.** It is the durable trace at the end of the evaluation step — the bridge between **Human Evaluation** and **Governed Outcome Recording** *(Disposition Position #11)*. As throughout the architecture, the Disposition changes understanding through nothing on its own; only action and resulting evidence change assessment.

---

## 12. Disposition Lifecycle Model

**Dispositions are event-driven.** *(Disposition Position #10)* A Disposition exists in relation to the governance context — the Finding, Resolution Candidate(s), Review Request, and the evaluation it records — and it moves when that context changes.

**Lifecycle concepts.** A Disposition may **appear, change, supersede one another, or become historical** as governance context changes:

- **recording** — a Disposition is recorded when an evaluation's outcome is captured;
- **change** — a Disposition changes when its governance context changes;
- **supersession** — one Disposition may supersede another as a newer outcome is recorded;
- **historical retention** — a superseded Disposition is **retained as history**, not erased.

The conceptual outcomes a Disposition may represent — such as **Accepted, Rejected, Deferred, or Superseded** *(Disposition Position #5)* — are **conceptual outcomes only**; this model does **not** define implementation-specific status values, and **no workflow implementation is defined.**

**History is preserved.** **Dispositions preserve history.** *(Disposition Position #6)* A recorded disposition **remains part of governance history**, and **recording a disposition does not erase prior governance objects.** Supersession produces a new current Disposition while the prior one is retained — exactly as the Finding Model preserves history on resolution. This is what keeps the governance record truthful and auditable.

**Event-driven, not time-driven.** Dispositions **do not change merely because time passes** *(Disposition Position #10)*. A Disposition moves only as its governance context changes — inheriting the event-driven discipline of the architecture.

---

## 13. Disposition Explanation Model

**Dispositions are explainable.** *(Disposition Position #9)* Every Disposition should be traceable to its basis:

```text
Finding
  ↓
Resolution Candidate
  ↓
Review Request
  ↓
Disposition
```

An explanation of a Disposition should identify:

- **the originating Finding** — the Finding ultimately at issue;
- **the relevant Resolution Candidate(s)** — the proposed resolution(s) the outcome concerns;
- **the Review Request** — the request whose evaluation produced this outcome;
- **the governance rationale** — why this outcome was recorded;
- **the recorded outcome** — what was decided (a conceptual outcome, per Section 12).

**Dispositions should never appear disconnected from their basis.** A Disposition that cannot be traced through a Review Request and Resolution Candidate to a Finding would violate this model. As elsewhere, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring by which an outcome is produced.

---

## 14. Disposition Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no workflow and no formula.

### Example A — an outcome is recorded
- **Finding:** Ambiguous KPI Definition.
- **Resolution Candidate:** Interpretation A.
- **Review Request:** Evaluate Interpretation A.
- **Disposition:** Accepted.
- **Result:** the **outcome is recorded.** The Disposition captures that the evaluation of Interpretation A concluded as Accepted. It records; it did not evaluate or decide — it holds the outcome of an evaluation performed elsewhere.

### Example B — outcomes across multiple candidates
- **State:** multiple Resolution Candidates are evaluated; one accepted, the others rejected.
- **Result:** the **Disposition records outcomes** for the evaluated candidates (Section 4). It captures the conclusions without altering any candidate.

### Example C — recording does not alter understanding
- **State:** a Disposition is recorded; the Finding remains unchanged.
- **Result:** **recording does not directly alter understanding.** The outcome is now on the governance record, but CAF, Reliability, Confidence, and the Finding itself are untouched — recording is not action (Sections 3, 7).

### Example D — a Disposition leads to action
- **State:** a Disposition leads to subsequent action; evidence changes; the Finding changes.
- **Result:** **CAF may change.** The Disposition influenced assessment **only through action**: the recorded outcome led to action, action produced new evidence, and the assessment chain re-ran. The Disposition itself altered nothing — the action did (Section 7). (Such change is possible but not guaranteed.)

### Example E — a Disposition is superseded
- **State:** a Disposition is superseded.
- **Result:** **history is preserved; the new disposition becomes current.** The prior Disposition is retained as part of governance history (Section 12, Position #6); supersession records a new current outcome without erasing the old one.

---

## 15. Preserved Model Principles

The Disposition Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Disposition Model preserves it |
|---|---|
| Findings are descriptive observations | Findings remain descriptive; Dispositions neither replace nor alter them (§3) |
| Recommendations are prescriptive | Recommendations remain prescriptive; Dispositions are governance records and distinct (§6) |
| Resolution Candidates are proposals, not truth | Dispositions record outcomes about candidates without altering them or making them truth (§4) |
| Review Requests request, never decide | Review Requests precede Dispositions; the Disposition records the outcome, it does not request or decide (§5) |
| Governance objects do not perform their next step | A Disposition records but does not evaluate, decide, or govern (§2, §11) |
| CAF / Reliability / Confidence change only on their inputs | Dispositions may be informed by them but alter none; change comes only via action and evidence (§7–§9) |
| History is preserved (Finding Model) | Dispositions preserve history; supersession retains prior records (§12) |
| Event-driven and explainable across the architecture | Dispositions are event-driven and explainable to their basis (§12, §13) |

Findings **remain descriptive**; Recommendations **remain prescriptive**; Resolution Candidates **remain proposals**; Review Requests **remain evaluation requests**; Dispositions **remain recorded outcomes**; and Dispositions **must not redefine** the assessment models.

---

## 16. Future Evolution

Future versions may add:

- governance authority integration;
- truth-promotion integration;
- policy integration;
- reviewer attribution;
- audit enhancements;
- escalation integration.

These are future capabilities. This document defines the **Disposition Model only** — the governance object that records evaluation outcomes, its lifecycle concepts, its explanation, and its relationships, at the conceptual level. Authority, truth promotion, policy, reviewer attribution, audit mechanisms, and escalation — along with user interfaces and any scoring — are defined elsewhere, not here.

---

## 17. Summary

A Disposition is a governance object that records the outcome of an evaluation — the durable trace at the end of the evaluation step. It is not a Finding, Resolution Candidate, Review Request, or Recommendation; it is not an evaluation and not governance authority. It records what was decided; it does not perform the evaluation and does not decide. It may reference the Findings, Resolution Candidates, and Review Requests that preceded it, and is always traceable back through them.

Dispositions may represent conceptual outcomes such as Accepted, Rejected, Deferred, or Superseded; they preserve history, so recording or superseding a disposition never erases prior governance objects. They may be informed by CAF, Reliability, and Confidence but alter none of them, nor do they alter Findings or Resolution Candidates; assessment changes only through evidence and understanding changes. They are event-driven (appear, change, supersede, become historical as governance context changes) and explainable, always traceable through a Review Request and Resolution Candidate to an originating Finding.

Dispositions exist because evaluations require durable recorded outcomes: a human evaluation without a disposition leaves no governable record. They are the bridge between Human Evaluation and Governed Outcome Recording — they record, but do not evaluate, decide, or govern. This document defines that object only; it defines no governance authority, workflow, truth promotion, policy, reviewer assignment, routing, notification, UI, or formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Governance object recording an evaluation outcome; not Finding/Candidate/Request/Recommendation | §2 |
| #2 | Not an evaluation; records outcomes, does not perform evaluation | §2 |
| #3 | Not governance authority; records what was decided, does not decide | §2 |
| #4 | May reference Findings, Resolution Candidates, Review Requests; traceable | §2 |
| #5 | Conceptual outcomes (Accepted/Rejected/Deferred/Superseded); no impl status values | §12 |
| #6 | Preserve history; recording does not erase prior governance objects | §12 |
| #7 | Do not directly alter Findings; subsequent actions may | §3 |
| #8 | Do not directly alter CAF, Reliability, or Confidence | §7, §8, §9 |
| #9 | Explainable; traceable Finding → Resolution Candidate → Review Request → Disposition | §13 |
| #10 | Event-driven; appear/change/supersede/become historical; not by time | §12 |
| #11 | Exist within the Governance Domain; bridge Human Evaluation → Governed Outcome Recording | §10, §11 |

All eleven founder positions are represented.

**Required behavior examples:** A (outcome recorded — Accepted), B (outcomes across multiple candidates), C (recording does not alter understanding), D (leads to action — evidence changes, Finding changes, CAF may change), E (superseded — history preserved, new disposition current) — all included and explained conceptually (§14).

**Exclusion checklist**
- Distinct from Findings — confirmed (§2, §3).
- Distinct from Resolution Candidates — confirmed (§2, §4).
- Distinct from Review Requests — confirmed (§2, §5).
- Distinct from Recommendations — confirmed (§6).
- Record outcomes — confirmed (§2).
- Do not perform evaluation — confirmed (§2).
- Do not decide — confirmed (§2, §3).
- Preserve history — confirmed (§12, Ex. E).
- Do not directly alter Findings — confirmed (§3).
- Do not directly alter CAF — confirmed (§7).
- Do not directly alter Reliability — confirmed (§8).
- Do not directly alter Confidence — confirmed (§9).
- Explainable — confirmed (§13).
- Event-driven — confirmed (§12).
- No workflow implementation — confirmed (§12, §16).
- No governance authority implementation — confirmed (§3, §10, §16).
- No truth-promotion implementation — confirmed (§10, §16).
- No scoring formulas — confirmed.
- All eleven referenced documents unmodified — confirmed (consumed only).

*Disposition Model v1 complete. Formalizes the founder-approved positions; defines the Disposition as a governance object that records — never performs — the outcome of an evaluation, references and is traceable to the governance objects that preceded it, preserves history, alters nothing on its own, is event-driven and explainable, and bridges Human Evaluation and Governed Outcome Recording. Defines the model only — not governance authority, workflow, truth promotion, policy, reviewer assignment, routing, notification, UI, or formulas. Subject to governance review before adoption.*
