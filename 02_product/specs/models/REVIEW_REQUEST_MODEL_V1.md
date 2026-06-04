# Review Request Model v1

**Document:** REVIEW_REQUEST_MODEL_V1.md
**Status:** Specification of the Review Request Model — **a Governance Domain object**
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `MODEL_LINEAGE_INDEX_V1.md`
**Date:** 2026-05-31

> **Architecture V1 classification (added by the Architecture V1 Simplification Refactor):** **Future Architecture — Outcome Orchestration / Agent Governance.** This model is **preserved and specified in full** and is **not part of the active Architecture V1 (Planning Intelligence) system**; it is deferred for later activation. This classification is additive — **no model content below is changed, deprecated, or invalidated.** See `ARCHITECTURE_V1_REFACTOR_REPORT.md`.

> **Scope.** This document defines the **Review Request Model** — what a Review Request is, why it exists, how it relates to Resolution Candidates, Findings, Recommendations, CAF, Reliability, Outcome Confidence, and Governance, and how it supports human evaluation. It establishes the mechanism through which proposed resolutions are presented for evaluation. It does **not** define notification behavior, reviewer-assignment algorithms, governance workflows, approval workflows, escalation logic, disposition logic, user interfaces, routing rules, prioritization rules, or scoring formulas. Those are future Governance Domain capabilities, defined elsewhere.
>
> **Position in the architecture.** The Resolution Candidate Model opened the Governance Domain by defining its first object. The Review Request is the next Governance Domain object: it requests evaluation of a Resolution Candidate. This document does not modify the Model Lineage Index or any other model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The ten referenced models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Review Request Model**: the governance object that requests evaluation of a Resolution Candidate.

This document defines:

- what a Review Request is;
- why Review Requests exist;
- how Review Requests relate to Resolution Candidates;
- how Review Requests relate to Findings;
- how Review Requests relate to Governance;
- how Review Requests support human evaluation.

It establishes the mechanism through which proposed resolutions are presented for evaluation. It is a conceptual and behavioral model: it defines no workflow, no routing, no notification, no disposition, and no formula.

---

## 2. Review Request Overview

**A Review Request is a governance object that requests evaluation of a Resolution Candidate.** It **is not a Resolution Candidate**, **not a Finding**, and **not a Recommendation.** *(Review Request Position #1)* It is a distinct governance object whose sole purpose is to bring a proposed resolution forward for human evaluation.

**Review Requests exist to facilitate human evaluation.** They **do not perform evaluation**, **do not make decisions** — they **request evaluation.** *(Review Request Position #3)* The Review Request is the asking, never the answering.

**Review Requests are requests, not decisions.** **The existence of a Review Request does not imply approval, rejection, acceptance, or truth.** *(Review Request Position #5)* That a resolution has been put forward for evaluation says nothing about how — or whether — it will be evaluated.

**Generated from governance context.** Review Requests are generated from governance context — which may include Findings, Resolution Candidates, Assessment Context, and Ownership information — which they **consume, not create.** *(Review Request Position #2)*

**Human evaluation is external.** Human evaluation **remains external to this model**; this model **establishes the request for evaluation** and **does not define how evaluation occurs.** *(Review Request Position #6)*

---

## 3. Relationship To Findings

- **Findings remain descriptive observations.**
- **Review Requests may originate from Findings through Resolution Candidates.** A Review Request does not arise directly from a Finding; it arises from a Resolution Candidate, which in turn proposes a resolution to a Finding.
- **Review Requests do not replace Findings.**
- **Review Requests do not alter Findings.** *(Review Request Position #8)*

The Finding remains untouched by the existence of a Review Request, exactly as it remained untouched by the Resolution Candidate. A Finding changes only as understanding changes.

---

## 4. Relationship To Resolution Candidates

Resolution Candidates and Review Requests are adjacent governance objects with distinct jobs:

- **Resolution Candidates propose possible resolutions.**
- **Review Requests request evaluation of those proposals.**

The division of labor:

- **Resolution Candidates answer:** *"What could resolve this?"*
- **Review Requests answer:** *"Who should evaluate this?"*

**Review Requests consume Resolution Candidates; they do not create them.** *(Review Request Position #4)* **A Review Request may reference one or more Resolution Candidates.** Because a single Finding may generate multiple Resolution Candidates, a Review Request may request evaluation of **one or many** candidates at once. *(Review Request Position #4)*

**Non-alteration.** **Review Requests do not directly alter Resolution Candidates.** *(Review Request Position #8)* A Review Request requests that a candidate be evaluated; it does not change the candidate. As with Findings, only subsequent evaluation and resulting action can lead to change.

---

## 5. Relationship To Recommendations

Recommendations and Review Requests are distinct objects:

- **Recommendations** suggest improvement actions; they are **prescriptive** and live in the Understanding Domain.
- **Review Requests** request evaluation of proposed resolutions; they are **governance-oriented** and live in the Governance Domain.

A Recommendation answers *"what should the user do to improve understanding?"* A Review Request answers *"who should evaluate this proposed resolution?"* One drives improvement; the other brings a proposal forward for governed evaluation. **They are distinct objects** and neither replaces the other.

---

## 6. Relationship To CAF

CAF remains the assessment layer.

- **Review Requests may be informed by CAF.** CAF can be part of the governance context that shapes a request.
- **Review Requests do not alter CAF.** *(Review Request Position #9)*

A Review Request, being a request for evaluation, changes nothing in CAF; assessment changes only through evidence and understanding changes (Section 10).

---

## 7. Relationship To Reliability

Reliability remains the supportability layer.

- **Review Requests may be informed by Reliability.**
- **Review Requests do not alter Reliability.** *(Review Request Position #9)*

A request can take into account how trustworthy an assessment is, but it neither determines nor changes Reliability.

---

## 8. Relationship To Outcome Confidence

Outcome Confidence remains the confidence layer.

- **Review Requests may be informed by Confidence.**
- **Review Requests do not alter Confidence.** *(Review Request Position #9)*

A request can be informed by how confident OSLO is, but changes none of the consolidation that produces Confidence and none of its value.

---

## 9. Relationship To Governance

**Review Requests are governance objects.** They **establish a mechanism through which Resolution Candidates are brought forward for evaluation.**

**This document does not define** evaluation processes, governance decisions, dispositions, or truth promotion. Those belong to future models. The Review Request establishes only the *object* that asks for evaluation — the explicit, traceable request that future governance processes will act upon. It is **the bridge between Proposed Resolution and Human Evaluation** (Section 10).

---

## 10. Review Request Philosophy

Two domains ask two different questions:

- The **Understanding Domain** answers: *"What do we understand?"*
- The **Governance Domain** answers: *"What are we willing to accept as true?"*

**Review Requests exist because proposed resolutions require evaluation before they can influence governed understanding.** A Resolution Candidate makes a resolution explicit; but a proposal does not become accepted merely by existing. Something must carry it to a human for evaluation — that something is the Review Request.

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
Future Governance Processes
```

**Review Requests request evaluation; they do not perform evaluation.** They are the step between a proposed resolution and the human judgment that will weigh it. As throughout the architecture, nothing here changes understanding on its own; only action and resulting evidence change assessment.

---

## 11. Review Request Lifecycle Model

**Review Requests are event-driven.** *(Review Request Position #11)* A request exists in relation to the governance context — the Finding, Resolution Candidate(s), and assessment/ownership context — that produced it, and it moves when those move.

**Lifecycle concepts.** A Review Request may **appear, change, withdraw, supersede one another, or close** as governance context changes:

- **creation** — a request is created when a Resolution Candidate (or candidates) is brought forward for evaluation;
- **change** — a request changes when its governance context changes;
- **withdrawal** — a request withdraws when its basis no longer holds;
- **supersession** — one request may supersede another as the governance context evolves;
- **fulfillment** — a request is fulfilled when the evaluation it requested has occurred (the evaluation itself being external to this model);
- **closure** — a request closes when it is no longer open.

These map to the conceptual outcomes that a Review Request **may be fulfilled, withdrawn, superseded, closed, or remain open** *(Review Request Position #7)*. These are **conceptual outcomes**; **no workflow implementation is defined.**

**Event-driven, not time-driven.** Requests **do not change merely because time passes** *(Review Request Position #11)*. A request moves only as its governance context changes — inheriting the event-driven discipline of the architecture.

Consistent with the requirement to remain conceptual, this model defines the lifecycle *concepts* and does **not** prescribe implementation-specific states.

---

## 12. Review Request Explanation Model

**Review Requests are explainable.** *(Review Request Position #10)* Every request should be traceable to its basis:

```text
Finding
  ↓
Resolution Candidate
  ↓
Review Request
```

An explanation of a Review Request should identify:

- **the originating Finding** — the Finding ultimately at issue;
- **the relevant Resolution Candidate(s)** — the proposed resolution(s) the request asks to be evaluated;
- **the governance context** — the assessment and ownership context that informed the request;
- **the rationale for the evaluation request** — why this proposal warrants evaluation now.

**Requests should never appear disconnected from their basis.** A Review Request that cannot be traced through a Resolution Candidate to a Finding would violate this model. As elsewhere, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring or routing by which a request is produced or directed.

---

## 13. Review Request Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no workflow, routing, or formula.

### Example A — a request exists for evaluation
- **Finding:** Missing KPI ownership.
- **Resolution Candidate:** Assign KPI ownership to the Sponsor.
- **Review Request:** Evaluate the proposed ownership assignment.
- **Result:** the request **exists for evaluation** — the proposed resolution is brought forward so a human can evaluate it. The request is not a decision; it implies no approval, rejection, or truth (Section 2).

### Example B — multiple proposals in one request
- **State:** one Finding produces multiple Resolution Candidates; the Review Request references all of them.
- **Result:** **multiple proposals are presented for evaluation** together (Section 4, Position #4). The request consumes several candidates without creating or altering any.

### Example C — a request responds to context
- **State:** governance context changes.
- **Result:** the **Review Request changes.** Requests are event-driven (Section 11): a shift in the Finding, the candidate(s), or the governance context can change, withdraw, or supersede a request.

### Example D — a request is withdrawn
- **State:** the Review Request is withdrawn.
- **Result:** **no decision occurs; assessment remains unchanged.** Withdrawal is a conceptual lifecycle outcome; because no evaluation concluded and no action followed, no evidence entered the loop, so CAF, Reliability, and Confidence are untouched. The Finding and the Resolution Candidate(s) remain as they were.

### Example E — a request is fulfilled
- **State:** the Review Request is fulfilled through human evaluation.
- **Result:** **evaluation occurs** (externally to this model), and **subsequent governance processes may continue.** This model establishes that the request was fulfilled; it **does not define** the evaluation or what follows it. Any assessment change that eventually results would, as always, come only through action and resulting evidence — not from the request itself.

---

## 14. Preserved Model Principles

The Review Request Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Review Request Model preserves it |
|---|---|
| Findings are descriptive observations | Findings remain descriptive; requests neither replace nor alter them (§3) |
| Recommendations are prescriptive | Recommendations remain prescriptive; requests are governance-oriented and distinct (§5) |
| Resolution Candidates are proposals, not truth | Requests consume candidates without making them truth; a request implies no acceptance (§2, §4) |
| Resolution Candidates require human evaluation | Requests facilitate that evaluation; they request it, never perform it (§2, §10) |
| CAF assesses understanding integrity | Requests may be informed by CAF but never alter it (§6) |
| Reliability is independent supportability | Requests may be informed by Reliability but never alter it (§7) |
| Confidence derives from CAF and Reliability | Requests may be informed by Confidence but never alter it (§8) |
| Assessment moves only on its real inputs via action | Requests change assessment through nothing; only evaluation-driven action and evidence can (§6–§8, §13) |
| Event-driven and explainable across the architecture | Requests are event-driven and explainable to their basis (§11, §12) |

Findings **remain descriptive**; Recommendations **remain prescriptive**; Resolution Candidates **remain proposals**; Review Requests **remain evaluation requests**; and Review Requests **must not redefine** the assessment models.

---

## 15. Future Evolution

Future versions may add:

- reviewer assignment;
- routing mechanisms;
- notifications;
- escalation;
- prioritization;
- disposition integration;
- governance integration.

These are future capabilities. This document defines the **Review Request Model only** — the governance object that requests evaluation, its lifecycle concepts, its explanation, and its relationships, at the conceptual level. Reviewer assignment, routing, notification, escalation, prioritization, disposition, and broader governance integration — along with user interfaces and any scoring — are defined elsewhere, not here.

---

## 16. Summary

A Review Request is a governance object that requests evaluation of a Resolution Candidate. It is not a Resolution Candidate, not a Finding, and not a Recommendation; it is the mechanism through which a proposed resolution is presented for human evaluation. It is generated from governance context — Findings, Resolution Candidates, assessment context, and ownership information — which it consumes but does not create, and it is a request, not a decision: its existence implies no approval, rejection, acceptance, or truth.

Review Requests consume Resolution Candidates and may reference one or many of them; they answer *"who should evaluate this?"* where Resolution Candidates answer *"what could resolve this?"* They neither perform evaluation nor make decisions — human evaluation remains external to this model. They may be informed by CAF, Reliability, and Confidence but alter none of them, nor do they alter Findings or Resolution Candidates; assessment changes only through evidence and understanding changes. They are event-driven (appear, change, withdraw, supersede, close as governance context changes) and explainable, always traceable through a Resolution Candidate to an originating Finding.

Review Requests are the bridge between Proposed Resolution and Human Evaluation — the step where a proposal is carried forward to be weighed. This document defines that object only; it defines no evaluation process, governance decision, disposition, truth promotion, reviewer assignment, routing, notification, UI, or formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Governance object requesting evaluation of a Resolution Candidate; not a Candidate/Finding/Recommendation | §2 |
| #2 | Generated from governance context; consume, not create | §2 |
| #3 | Facilitate human evaluation; do not perform or decide; request evaluation | §2 |
| #4 | May reference one or more Resolution Candidates | §4 |
| #5 | Requests, not decisions; imply no approval/rejection/acceptance/truth | §2 |
| #6 | Human evaluation external; establish the request, not how evaluation occurs | §2, §10 |
| #7 | Fulfilled/withdrawn/superseded/closed/open; conceptual outcomes | §11 |
| #8 | Do not directly alter Resolution Candidates or Findings | §3, §4 |
| #9 | Do not directly alter CAF, Reliability, or Confidence | §6, §7, §8 |
| #10 | Explainable; traceable Finding → Resolution Candidate → Review Request | §12 |
| #11 | Event-driven; appear/change/withdraw/supersede/close; not by time | §11 |
| #12 | Exist within the Governance Domain; bridge Proposed Resolution → Human Evaluation | §9, §10 |

All twelve founder positions are represented.

**Required behavior examples:** A (request exists for evaluation), B (multiple proposals in one request), C (event-driven change), D (withdrawn — no decision, assessment unchanged), E (fulfilled — evaluation occurs externally, subsequent governance not defined here) — all included and explained conceptually (§13).

**Exclusion checklist**
- Distinct from Findings — confirmed (§2, §3).
- Distinct from Resolution Candidates — confirmed (§2, §4).
- Distinct from Recommendations — confirmed (§5).
- Governance objects — confirmed (§2, §9).
- Request evaluation — confirmed (§2, §10).
- Do not perform evaluation — confirmed (§2, §10).
- Do not make decisions — confirmed (§2).
- Do not directly alter Findings — confirmed (§3).
- Do not directly alter CAF — confirmed (§6).
- Do not directly alter Reliability — confirmed (§7).
- Do not directly alter Confidence — confirmed (§8).
- Explainable — confirmed (§12).
- Event-driven — confirmed (§11).
- No workflow implementation — confirmed (§11, §15).
- No routing implementation — confirmed (§12, §15).
- No notification behavior — confirmed (§15).
- No disposition logic — confirmed (§9, §15).
- No scoring formulas — confirmed.
- All ten referenced documents unmodified — confirmed (consumed only).

*Review Request Model v1 complete. Formalizes the founder-approved positions; defines the Review Request as a governance object that requests — never performs — evaluation of one or more Resolution Candidates, alters nothing on its own, is event-driven and explainable to its basis, and bridges Proposed Resolution and Human Evaluation. Defines the model only — not evaluation, governance processes, disposition, truth promotion, reviewer assignment, routing, notification, UI, or formulas. Subject to governance review before adoption.*
