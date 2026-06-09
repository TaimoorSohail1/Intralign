# Notification Model v1

**Document:** NOTIFICATION_MODEL_V1.md
**Status:** Specification of the Notification Model — **a supporting awareness & delivery service**
**Consumes (authoritative, unmodified):** `MODEL_LINEAGE_INDEX_V1.md` · `MODEL_COVERAGE_AUDIT_V1.md` · `AUTHORITY_PLANE_MODEL_V1.md` · `ACCEPTED_UNDERSTANDING_MODEL_V1.md` · `REVIEW_REQUEST_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md`
**Date:** 2026-05-31

> **Scope.** This document defines the **Notification Model** — Notification as a **supporting awareness and delivery service** that surfaces awareness of relevant changes, requests, and events. It does **not** redefine governance, assessment, recommendations, or user action, and it does **not** define routing rules, delivery channels, email/Slack/in-app behavior, assignment algorithms, notification-priority formulas, escalation behavior, workflow implementation, governance behavior, assessment behavior, or recommendation logic. Those are out of scope.
>
> **Position in the architecture.** The Model Lineage Index names Notification as the one remaining future supporting service in the Governance Domain — explicitly "it supports awareness and delivery; it does not define governance judgment, disposition, or acceptance." This document specifies that supporting service at the conceptual level. It does not modify the index or any other model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The eleven referenced documents are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Notification Model**: the supporting service that surfaces awareness of relevant changes, requests, and events across both domains, without performing assessment, governance, or prescription.

This document defines:

- what a Notification is;
- what Notifications do and do not do;
- what may trigger a Notification;
- how Notifications may be targeted (conceptually);
- how Notifications behave and are explained;
- how Notifications support — without belonging to — both domains.

It is a conceptual model. It defines no routing, no delivery channel, no assignment algorithm, no priority formula, and no workflow.

---

## 2. Notification Overview

**A Notification is a supporting service object that surfaces awareness of relevant changes, requests, or events.** It **is not a Finding, not a Recommendation, not a Review Request, not a Disposition, and not Governance.** *(Notification Position #1)* It is a distinct kind of object — a *supporting service object* — whose only purpose is to make a relevant change or event known.

**Notifications support awareness and delivery.** They **do not perform assessment**, **do not perform governance**, and **do not make decisions.** *(Notification Position #2)* A Notification carries awareness; it never evaluates, governs, prescribes, or decides anything.

**Notifications are supporting service objects.** They **do not belong to the primary Understanding Domain lineage** and **do not belong to the primary Governance Domain acceptance chain.** They **support both domains.** *(Notification Position #8)* A Notification is adjacent to the architecture's two domains, serving awareness across them rather than sitting inside either chain.

---

## 3. Relationship To Understanding Domain

The Understanding Domain (assessment → scoring → reliability → confidence → MRI → overlay → finding → recommendation) produces understanding and improvement signals. Notification's relationship to it:

- Notifications may **surface awareness** of relevant changes within the Understanding Domain (for example, a changed Finding or Recommendation).
- Notifications **do not belong to the understanding-improvement loop** and add no node to it.
- Notifications **do not alter** any Understanding-Domain signal or object; they make changes *known*, not *different*.

MRI and Overlays *make understanding observable and manage attention within it*; Notification is a different concern — it surfaces awareness of *changes/events* to people, outside the visualization surface. The two are complementary and distinct: MRI/Overlay show the current picture; Notification announces that something relevant changed.

---

## 4. Relationship To Governance Domain

The Governance Domain (Resolution Candidate → Review Request → Human Evaluation → Disposition → Governance → Accepted Understanding) carries understanding toward acceptance. Notification's relationship to it:

- Notifications may **surface awareness** of relevant governance changes, requests, and events.
- Notifications **do not belong to the acceptance chain** and add no node to it.
- Notifications **do not perform** evaluation, recording, governance, or acceptance, and **do not make decisions** (Section 2).

The index's constraint is preserved exactly: Notification *supports awareness and delivery; it does not define governance judgment, disposition, or acceptance.* It informs the people around the governance chain; it never advances the chain itself.

---

## 5. Relationship To Findings

- **Findings remain descriptive observations** (Finding Model).
- A Notification **may be triggered by a change in a Finding** (Section 11).
- A Notification **does not replace, alter, or become a Finding**; it surfaces awareness that a Finding changed.

A Finding changes only as understanding changes; a Notification about it changes nothing in the Finding.

---

## 6. Relationship To Recommendations

- **Recommendations remain prescriptive** advisory suggestions (Recommendation Model).
- A Notification **may be triggered by a change in a Recommendation**.
- A Notification **does not prescribe.** It surfaces awareness that a Recommendation appeared or changed; the Recommendation remains the prescriptive object. *(This is the distinction Example E illustrates.)*

A Notification never carries a "what to do next"; that remains the Recommendation's role.

---

## 7. Relationship To Review Requests

- **Review Requests request evaluation** (Review Request Model).
- A Notification **may be triggered by the creation or change of a Review Request** — for instance, surfacing awareness to a reviewer that an evaluation has been requested.
- A Notification **does not request or perform evaluation.** It informs that a request exists; the Review Request remains the object that requests evaluation, and human evaluation remains external.

A Notification about a Review Request is awareness *of* the request, not a second request.

---

## 8. Relationship To Dispositions

- **Dispositions record evaluation outcomes** (Disposition Model).
- A Notification **may be triggered by a recorded Disposition** — surfacing awareness to a responsible stakeholder that an outcome was recorded.
- A Notification **does not record outcomes and does not alter a Disposition.** It informs that a Disposition exists; the Disposition remains the durable record. *(This is the distinction Example B illustrates.)*

---

## 9. Relationship To Governance And Accepted Understanding

- **Governance governs acceptance; Accepted Understanding is its durable output** (Governance & Accepted Understanding Models).
- A Notification **may be triggered by a governance outcome or by a change in Accepted Understanding**.
- A Notification **does not govern, does not accept, and does not alter Governance outcomes or Accepted Understanding.** It surfaces awareness that acceptance changed; the governed state is untouched. *(This is the distinction Example C illustrates.)*

A Notification about acceptance is news of the acceptance, never the acceptance itself.

---

## 10. Notification Philosophy

The two domains answer *"what do we understand?"* (Understanding) and *"what are we willing to accept?"* (Governance). Neither, by itself, ensures the right person **knows** that something relevant has changed. **Notification answers a third, supporting question: *"who needs to be made aware that something relevant changed?"***

This is deliberately a **supporting** question, not a primary one. Notification sits beside the two domain chains, not inside them: it consumes their changes and events and turns them into awareness, while changing nothing in either chain. It carries no judgment, no assessment, and no prescription — only awareness. The architecture's invariant holds here as everywhere: **nothing changes understanding or acceptance except action and evidence (Understanding) and human evaluation/governance (Governance); a Notification changes neither — it only makes change known.**

---

## 11. Notification Trigger Model

**Notifications are event-driven.** They **arise from relevant changes or events**, and **do not exist merely because time passes.** *(Notification Position #5)*

A Notification **may be triggered by changes in:** *(Notification Position #3)*

- Findings
- Recommendations
- Resolution Candidates
- Review Requests
- Dispositions
- Governance outcomes
- Accepted Understanding

The trigger is a *relevant change or event* in one of these objects; the Notification is the awareness that follows. This model fixes **what may trigger** a Notification; it does **not** define *which* changes are relevant, how triggers are detected, or any priority among them — those are out of scope (no priority formula, no detection rules).

A Notification **does not directly alter Findings, CAF, Reliability, Confidence, Governance, or Accepted Understanding.** It only surfaces awareness. *(Notification Position #4)*

---

## 12. Notification Targeting Model

**Notifications may target responsible people, roles, reviewers, stakeholders, or system actors.** *(Notification Position #7)*

This model defines **targetability conceptually only** — that a Notification *can be directed at* a responsible party. It does **not** define routing, delivery channels, or assignment logic: how a target is chosen, how a Notification reaches them, or through what medium are all out of scope. Targeting here means only that a Notification has a conceptual addressee; the mechanics of reaching that addressee belong to future, out-of-scope capabilities.

Targeting connects to ownership where it exists (Findings carry ownership; governance context carries ownership information), but this model neither defines nor performs ownership assignment.

---

## 13. Notification Lifecycle Model

**Notifications are event-driven** (Section 11) and have conceptual lifecycle outcomes.

**Lifecycle outcomes.** A Notification may be **dismissed, viewed, acted upon, or become historical.** *(Notification Position #9)* These are **conceptual lifecycle outcomes only**; this model does **not** define workflow implementation, status vocabularies, or the mechanics of dismissal/viewing.

**Awareness history is preserved.** **Notifications preserve awareness history. A delivered or historical Notification remains part of the awareness record.** *(Notification Position #10)* A Notification that has been viewed, dismissed, acted upon, or aged into history is retained as part of the awareness record — consistent with the history-preservation discipline across the architecture (Finding, Disposition, Governance, Accepted Understanding all preserve history).

**Event-driven, not time-driven.** A Notification arises from a relevant change or event and does not appear merely with the passage of time (Section 11). Its lifecycle progresses through awareness events (viewed, dismissed, acted upon), not on a clock.

Note that "**acted upon**" here means the *Notification's* awareness state changed because the recipient engaged with it; the *action* that may change understanding or acceptance occurs through the proper objects (User Action on a Recommendation; Human Evaluation on a Review Request), never through the Notification itself.

---

## 14. Notification Explanation Model

**Notifications are explainable.** *(Notification Position #6)* Every Notification should be **traceable to the object, event, or change that produced it.**

```text
Source object / event / change
  ↓
Notification
```

An explanation of a Notification should identify:

- **the source object** — the Finding, Recommendation, Resolution Candidate, Review Request, Disposition, governance outcome, or Accepted Understanding involved;
- **the triggering event or change** — what relevant change or event occurred;
- **the conceptual target** — the responsible party the awareness is directed at (per Section 12).

A Notification should **never appear disconnected from its basis** — the source object and event that produced it. As elsewhere in the architecture, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring by which a Notification is produced or prioritized.

---

## 15. Notification Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no routing, delivery channel, or formula.

### Example A — a Review Request triggers awareness
- **State:** a Review Request is created; a Notification surfaces awareness to a reviewer.
- **Result:** the Notification **supports awareness; it does not perform evaluation.** The reviewer is made aware that an evaluation has been requested; the evaluation itself remains external, and the Review Request remains the object that requests it (Section 7).

### Example B — a Disposition triggers awareness
- **State:** a Disposition is recorded; a Notification surfaces awareness to a responsible stakeholder.
- **Result:** the Notification **informs; it does not alter governance.** Awareness that an outcome was recorded is delivered; the Disposition and all governance state are untouched (Section 8).

### Example C — Accepted Understanding changes
- **State:** Accepted Understanding changes; a Notification surfaces awareness.
- **Result:** the Notification **does not alter Accepted Understanding.** It announces that the governed state changed; the governed state itself is unchanged by the announcement (Section 9).

### Example D — a Notification is dismissed
- **State:** a Notification is dismissed.
- **Result:** the **Notification's state changes; the underlying object remains unchanged.** Dismissal is a Notification lifecycle outcome (Section 13); the source Finding/Recommendation/governance object is unaffected, and the dismissed Notification is retained in the awareness record (Position #10).

### Example E — a Recommendation changes
- **State:** a Recommendation changes; a Notification surfaces awareness.
- **Result:** the Notification **does not prescribe; the Recommendation remains the prescriptive object.** Awareness that a Recommendation appeared or changed is delivered; the "what to do next" stays with the Recommendation (Section 6).

---

## 16. Preserved Model Principles

The Notification Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Notification Model preserves it |
|---|---|
| Findings are descriptive observations | Notifications may announce Finding changes; they never replace or alter Findings (§5) |
| Recommendations are prescriptive | Recommendations remain the prescriptive object; Notifications do not prescribe (§6) |
| Review Requests request evaluation | Notifications announce a request; they do not request or perform evaluation (§7) |
| Dispositions record outcomes | Notifications announce a recorded outcome; they do not record or alter it (§8) |
| Governance governs; Accepted Understanding is its output | Notifications announce acceptance changes; they do not govern, accept, or alter the governed state (§9) |
| Assessment signals change only via action/evidence | Notifications alter no Finding, CAF, Reliability, or Confidence; they only surface awareness (§5, §11) |
| MRI/Overlay are the visualization/attention surfaces | Notification is a distinct awareness service, not a visualization or attention lens (§3) |
| Event-driven and explainable across the architecture | Notifications are event-driven and explainable to their source (§11, §14) |
| History is preserved | Notifications preserve awareness history (§13) |

Notifications **remain supporting service objects**: they support both domains, belong to neither chain, and **must not redefine** governance, assessment, recommendations, or user action.

---

## 17. Future Evolution

Future versions may add the delivery and management mechanics deliberately excluded here, including:

- routing rules and delivery channels (email, Slack, in-app, and others);
- assignment algorithms and ownership-assignment integration;
- notification priority and escalation;
- batching, digest, and suppression behavior;
- user-interface presentation.

These are future capabilities. This document defines the **Notification Model only** — the supporting awareness object, its triggers, conceptual targetability, lifecycle concepts, and explanation. Routing, channels, assignment, priority, escalation, UI, and any workflow are defined elsewhere, not here.

---

## 18. Summary

A Notification is a supporting service object that surfaces awareness of relevant changes, requests, and events. It is not a Finding, Recommendation, Review Request, Disposition, or Governance; it supports awareness and delivery and performs no assessment, no governance, and no decision. It is a supporting service that sits beside both domains — belonging to neither the Understanding-improvement loop nor the Governance acceptance chain — and serves both.

Notifications are event-driven: they arise from relevant changes in Findings, Recommendations, Resolution Candidates, Review Requests, Dispositions, governance outcomes, or Accepted Understanding, and never merely with the passage of time. They may be targeted, conceptually, at responsible people, roles, reviewers, stakeholders, or system actors — but routing, channels, and assignment are out of scope. They alter none of the assessment signals, governance outcomes, or objects they announce; they only make change known. They have conceptual lifecycle outcomes (dismissed, viewed, acted upon, become historical), preserve awareness history, and are explainable — always traceable to the source object and event that produced them.

This document defines that supporting service only; it defines no routing, delivery channel, assignment algorithm, priority formula, escalation, UI, workflow, governance behavior, assessment behavior, or recommendation logic.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Supporting service object surfacing awareness; not Finding/Recommendation/Review Request/Disposition/Governance | §2 |
| #2 | Supports awareness & delivery; no assessment, governance, or decisions | §2 |
| #3 | May be triggered by changes in the seven listed objects | §11 |
| #4 | Does not directly alter Findings, CAF, Reliability, Confidence, Governance, or Accepted Understanding | §11 (and §5–§9) |
| #5 | Event-driven; arises from changes/events, not time | §11 |
| #6 | Explainable; traceable to the producing object/event/change | §14 |
| #7 | May target people/roles/reviewers/stakeholders/system actors; targetability conceptual only | §12 |
| #8 | Supporting service object; belongs to neither primary chain; supports both | §2, §3, §4 |
| #9 | Conceptual lifecycle outcomes (dismissed/viewed/acted upon/historical) | §13 |
| #10 | Preserves awareness history | §13 |

All ten Notification positions are represented.

**Required behavior examples:** A (Review Request → awareness; no evaluation performed), B (Disposition → awareness; governance unaltered), C (Accepted Understanding change → awareness; unaltered), D (dismissed; underlying object unchanged), E (Recommendation change → awareness; Recommendation remains prescriptive) — all included and explained conceptually (§15).

**Exclusion checklist**
- Notification remains a supporting service object — confirmed (§2, §8).
- Distinct from Finding, Recommendation, Review Request, Disposition, Governance — confirmed (§2, §5–§9).
- Supports awareness and delivery only — confirmed (§2, §10).
- Does not directly alter assessment signals — confirmed (§5, §11).
- Does not directly alter governance outcomes — confirmed (§9, §11).
- Event-driven — confirmed (§11).
- Explainable — confirmed (§14).
- Preserves awareness history — confirmed (§13).
- No routing implementation — confirmed (§12, §17).
- No delivery-channel implementation — confirmed (§12, §17).
- No workflow implementation — confirmed (§13, §17).
- No scoring formulas — confirmed.
- All eleven referenced documents unmodified — confirmed (consumed only).

*Notification Model v1 complete. Formalizes the founder-approved positions; defines Notification as a supporting awareness & delivery service object that surfaces awareness of relevant changes across both domains, belongs to neither primary chain, alters nothing it announces, is event-driven and explainable, preserves awareness history, and is targetable only conceptually. Defines the model only — not routing, delivery channels, assignment, priority, escalation, UI, workflow, governance, assessment, or recommendation logic. Subject to governance review before adoption.*
