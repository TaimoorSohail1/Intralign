# Accepted Understanding Model v1

**Document:** ACCEPTED_UNDERSTANDING_MODEL_V1.md
**Status:** Specification of the Accepted Understanding Model — **the output of Governance**
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `REVIEW_REQUEST_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `AUTHORITY_PLANE_MODEL_V1.md` · `MODEL_LINEAGE_INDEX_V1.md`
**Date:** 2026-05-31

> **Architecture V1 classification (added by the Architecture V1 Simplification Refactor):** **Future Architecture — Outcome Orchestration / Agent Governance.** This model is **preserved and specified in full** and is **not part of the active Architecture V1 (Planning Intelligence) system**; it is deferred for later activation. This classification is additive — **no model content below is changed, deprecated, or invalidated.** See `ARCHITECTURE_V1_REFACTOR_REPORT.md`.

> **Scope.** This document formalizes the architectural endpoint currently produced by Governance. It defines what Accepted Understanding is, why it exists, how it differs from Understanding, Findings, and Dispositions, how it relates to Governance, and how it relates to future Knowledge Layer concepts. It remains **conceptual**. It does **not** define truth-promotion algorithms, canonical knowledge management, knowledge-graph implementation, storage models, governance workflows, review workflows, scoring formulas, notification behavior, user interfaces, or automation behavior. Those are future capabilities, defined elsewhere.
>
> **Position in the architecture.** The Governance Model produces acceptance; Accepted Understanding is the durable object that acceptance produces. It is the final output of the Governance Domain chain and the bridge to future Knowledge Layer concepts (which this document does not define). It does not modify the Model Lineage Index or any other model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The thirteen referenced models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Accepted Understanding Model**: the durable object that Governance produces when understanding is accepted.

This document defines:

- what Accepted Understanding is;
- why it exists;
- how it differs from Understanding;
- how it differs from Findings;
- how it differs from Dispositions;
- how it relates to Governance;
- how it relates to future Knowledge Layer concepts.

It is a conceptual model. It defines no truth-promotion algorithm, no knowledge-layer mechanism, no storage model, no workflow, and no formula.

---

## 2. Accepted Understanding Overview

**Accepted Understanding is the output of Governance.** Governance governs acceptance; **Accepted Understanding is what Governance produces.** *(Accepted Understanding Position #1)*

It is a distinct state, separated from every object that precedes it:

- **Accepted Understanding is not Understanding.** Understanding is **assessed**; Accepted Understanding is **governed**. These are **different states.** *(Position #2)* The Understanding Domain produces assessed understanding; Governance produces accepted understanding. The same project reality can be well assessed yet not accepted, or accepted yet still being reassessed.
- **Accepted Understanding is not a Finding** *(Position #3)*, **not a Resolution Candidate** *(Position #4)*, **not a Review Request** *(Position #5)*, **not a Disposition** *(Position #6)*, and **not Governance** *(Position #7)*. It is informed by these objects but is none of them.

**It is the result of acceptance, not the act.** Governance **performs** acceptance; Accepted Understanding **is the result** of acceptance *(Position #7)*. Where a Disposition records the outcome of an evaluation, Accepted Understanding is **the governed understanding that exists after governance** *(Position #6)* — the durable object that holds what governance has accepted.

**Why it exists.** Accepted Understanding exists because **governance outcomes must have a durable object.** Without it, governance would conclude with nothing durable to point to as "the understanding we have accepted."

---

## 3. Relationship To Findings

- **Findings remain descriptive observations.**
- **Accepted Understanding may be informed by Findings.**
- **Accepted Understanding does not replace Findings.**
- **Accepted Understanding does not alter Findings directly.**

A Finding records what was observed about understanding; Accepted Understanding records what has been governed as accepted. The former is descriptive and remains untouched; the latter is governed and durable. A Finding changes only as understanding changes — never because understanding was accepted.

---

## 4. Relationship To Resolution Candidates

- **Resolution Candidates remain proposals.**
- **Accepted Understanding consumes the outcomes of governance over proposals.**
- **Accepted Understanding is not a proposal.** *(Position #4)*

A Resolution Candidate proposes a possible resolution; Accepted Understanding is the governed result that may follow once such a proposal has been evaluated and governed. The proposal remains a proposal; Accepted Understanding is not.

---

## 5. Relationship To Review Requests

- **Review Requests remain requests for evaluation.**
- **Accepted Understanding is not a request.** *(Position #5)*

A Review Request asks for evaluation; Accepted Understanding is the governed understanding that may exist far downstream of that request, after evaluation and governance. The request and the accepted result are different objects at different points in the chain.

---

## 6. Relationship To Dispositions

- **Dispositions remain recorded outcomes.**
- **Accepted Understanding is based upon governance outcomes informed by Dispositions.**
- **Accepted Understanding does not replace Dispositions.**

A Disposition is the durable record of an evaluation's outcome; Governance operates on that record; Accepted Understanding is the governed understanding that results. The Disposition records *what was decided about a proposal*; Accepted Understanding holds *what understanding is now accepted*. The two coexist — the Disposition is retained as part of the record, and Accepted Understanding stands distinct from it.

---

## 7. Relationship To Governance

- **Governance performs acceptance.**
- **Accepted Understanding is produced by Governance.**
- **Governance and Accepted Understanding must remain distinct.**

Governance is the act and the layer of acceptance; Accepted Understanding is the object that act produces. Conflating them would lose the distinction between *governing* (a responsibility exercised on human judgment) and *the governed result* (a durable object). Governance changes; Accepted Understanding is what stands as accepted at any point — each is its own thing.

---

## 8. Relationship To CAF

- **CAF assesses understanding** (integrity).
- **Accepted Understanding is governed understanding.**
- **Accepted Understanding does not alter CAF.** *(Position #10)*

CAF assesses; Accepted Understanding is the governed result of accepting (or not) what was assessed. Accepted Understanding may be informed by CAF, but it neither performs CAF nor changes it; assessment changes only through evidence and understanding changes (Section 11).

---

## 9. Relationship To Reliability

- **Reliability assesses supportability.**
- **Accepted Understanding does not alter Reliability.** *(Position #10)*

Reliability tells how trustworthy an assessment is; acceptance does not change that supportability. Accepted Understanding neither determines nor alters Reliability.

---

## 10. Relationship To Outcome Confidence

- **Confidence summarizes trust in understanding.**
- **Accepted Understanding does not alter Confidence.** *(Position #10)*

Confidence summarizes how much to trust the understanding; that an understanding is accepted does not change the consolidation that produces Confidence or its value. Acceptance and confidence are distinct: understanding may be accepted at any confidence, and high confidence is not itself acceptance.

---

## 11. Accepted Understanding Philosophy

Three questions sit in sequence across the architecture:

- The **Understanding Domain** answers: *"What do we understand?"*
- The **Governance Domain** answers: *"What are we willing to accept?"*
- **Accepted Understanding** answers: *"What understanding has been accepted?"*

**Understanding and Accepted Understanding are distinct.** A project may be:

- understood but not accepted;
- accepted and later reconsidered;
- accepted and later superseded.

These cases show that acceptance is its own state, separable from understanding and never permanent. **Accepted Understanding exists because governance outcomes must have a durable object** — something that endures as "the understanding we have accepted," that can be traced, reconsidered, and superseded while keeping history.

**Conceptual relationship.** Accepted Understanding is the final output of Governance and the bridge onward:

```text
Understanding Domain
  ↓
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
Governance
  ↓
Accepted Understanding
  ↓
Future Knowledge Layer Concepts
```

**Accepted Understanding is the bridge between Governance and future Knowledge Layer concepts.** *(Position #13)* This document does not define those concepts; it defines only the bridge — the durable, governed object that future Knowledge Layer work would consume. As throughout the architecture, Accepted Understanding changes understanding through nothing on its own; only action and resulting evidence change assessment.

---

## 12. Accepted Understanding Lifecycle Model

**Accepted Understanding is event-driven.** *(Position #12)* It exists in relation to its governance context and moves when that context changes.

**Lifecycle concepts.** Accepted Understanding may move through:

- **establishment** — an accepted-understanding object is established when Governance accepts understanding;
- **change** — it changes when its governance context changes;
- **reconsideration** — an established acceptance may be reconsidered; **acceptance is not permanence**, and **governed understanding may later change** *(Position #8)*;
- **supersession** — one accepted understanding may supersede another;
- **historical retention** — a reconsidered or superseded accepted understanding is **retained as history**.

These are **lifecycle concepts only**; this model does **not** prescribe implementation-specific states, and **no workflow implementation is defined.**

**History is preserved.** **Accepted Understanding preserves history. Historical accepted understanding remains part of governance history.** *(Position #9)* Reconsideration and supersession produce a new current accepted understanding while the prior one is retained — consistent with the Disposition, Governance, and Finding models. This keeps the governed record truthful and auditable.

**Event-driven, not time-driven.** **It changes when governance context changes; it does not change merely because time passes.** *(Position #12)* It inherits the event-driven discipline of the entire architecture.

---

## 13. Accepted Understanding Explanation Model

**Accepted Understanding is explainable.** *(Position #11)* Every accepted-understanding object should be traceable to its basis:

```text
Finding
  ↓
Resolution Candidate
  ↓
Review Request
  ↓
Disposition
  ↓
Governance
  ↓
Accepted Understanding
```

An explanation of an Accepted Understanding object should identify:

- **the originating Finding** — the Finding ultimately at issue;
- **the relevant Resolution Candidate(s)** — the proposed resolution(s) concerned;
- **the Review Request** — the request whose evaluation contributed;
- **the Disposition(s)** — the recorded evaluation outcome(s) Governance operated on;
- **the Governance rationale** — why the understanding was accepted;
- **the Accepted Understanding outcome** — what was accepted.

**Accepted Understanding should never appear disconnected from its basis.** An accepted understanding that cannot be traced through Governance, a Disposition, a Review Request, and a Resolution Candidate to a Finding would violate this model. As elsewhere, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring by which acceptance is produced.

---

## 14. Accepted Understanding Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no workflow and no formula.

### Example A — understanding accepted
- **State:** Governance accepts understanding.
- **Result:** **Accepted Understanding is established.** The durable, governed object now exists, traceable back through Governance and its prior governance objects to an originating Finding. It is the result of acceptance, not the act of accepting.

### Example B — acceptance declined
- **State:** Governance declines acceptance.
- **Result:** **Accepted Understanding is not established.** Because Governance did not accept, no accepted-understanding object is produced; the underlying Finding and its assessment remain, simply not accepted (Sections 2, 7).

### Example C — accepted understanding reconsidered
- **State:** an established Accepted Understanding is reconsidered.
- **Result:** **history is preserved.** Acceptance is not permanence (Position #8); reconsideration produces a new current state while the prior accepted understanding is retained as governance history (Section 12, Position #9).

### Example D — acceptance moves independently of assessment
- **State:** CAF remains unchanged; Accepted Understanding changes.
- **Result:** **acceptance and assessment remain separate.** Because Accepted Understanding is governed and CAF is assessed, the accepted state can change while CAF stays fixed — the clearest demonstration that acceptance is a distinct state from assessment (Sections 2, 8).

### Example E — accepted understanding leads to action
- **State:** Accepted Understanding leads to action; evidence changes.
- **Result:** **CAF may change.** Accepted Understanding influenced assessment **only through action**: the accepted understanding led to action, action produced new evidence, and the assessment chain re-ran. Accepted Understanding itself altered nothing — the action did (Section 8). (Such change is possible but not guaranteed.)

---

## 15. Preserved Model Principles

The Accepted Understanding Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Accepted Understanding Model preserves it |
|---|---|
| CAF assesses understanding integrity | Accepted Understanding is governed, not assessed; it may be informed by CAF but never alters it (§8) |
| Reliability assesses supportability | Accepted Understanding never alters Reliability (§9) |
| Confidence summarizes trust | Accepted Understanding never alters Confidence; confidence is not acceptance (§10) |
| Findings are descriptive observations | Findings remain descriptive; Accepted Understanding neither replaces nor alters them (§3) |
| Recommendations are prescriptive | Recommendations remain prescriptive; Accepted Understanding is a governed result and distinct |
| Resolution Candidates are proposals | Accepted Understanding is not a proposal; it consumes governed outcomes over proposals (§4) |
| Review Requests request evaluation | Accepted Understanding is not a request (§5) |
| Dispositions record outcomes; preserve history | Accepted Understanding is based on dispositions without replacing them; it preserves history (§6, §12) |
| Governance governs acceptance | Governance performs acceptance; Accepted Understanding is its result, kept distinct (§7) |
| Assessment moves only on its inputs via action | Accepted Understanding changes assessment through nothing; only action and evidence can (§8–§10, §14) |
| Event-driven and explainable across the architecture | Accepted Understanding is event-driven and explainable to its basis (§12, §13) |

**Assessment remains separate from acceptance.** **Governance remains separate from accepted understanding.** **Accepted Understanding remains distinct from future knowledge-layer concepts.** Accepted Understanding **must not redefine** the assessment or governance models.

---

## 16. Future Evolution

Future versions may add:

- truth-promotion models;
- canonical knowledge models;
- knowledge-layer models;
- governance-to-knowledge transitions;
- audit models.

These are future capabilities. This document defines **Accepted Understanding only** — the governed object Governance produces, its relationships, lifecycle concepts, and explanation, at the conceptual level. Truth promotion, canonical knowledge management, knowledge-layer mechanisms, governance-to-knowledge transitions, and audit — along with storage, workflows, notification, user interfaces, automation, and any scoring — are defined elsewhere, not here. Accepted Understanding is the **bridge** to those concepts, not their definition.

---

## 17. Summary

Accepted Understanding is the output of Governance — the durable, governed object that exists after understanding has been accepted. It is a distinct state: not Understanding (which is assessed, not governed), not a Finding, not a Resolution Candidate, not a Review Request, not a Disposition, and not Governance itself. It is the *result* of acceptance, not the act; it exists because governance outcomes must have a durable object to stand as "the understanding we have accepted."

Accepted Understanding may be informed by Findings, consumes governed outcomes over Resolution Candidates, and is based upon Governance outcomes informed by Dispositions — without replacing any of them. It may be informed by CAF, Reliability, and Confidence but alters none of them; assessment changes only through evidence and understanding changes, so acceptance can move while assessment stays fixed. It is event-driven (established, changed, reconsidered, superseded, retained as history as governance context changes), preserves history, and is explainable, always traceable through Governance, a Disposition, a Review Request, and a Resolution Candidate to an originating Finding. Acceptance is not permanence: accepted understanding may later be reconsidered or superseded, with prior states retained.

Accepted Understanding is the final output of Governance and the bridge between Governance and future Knowledge Layer concepts. This document defines that object and that bridge only; it defines no truth-promotion algorithm, canonical knowledge model, knowledge-layer mechanism, storage, governance or review workflow, notification, UI, automation, or formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | Output of Governance; what Governance produces | §2 |
| #2 | Not Understanding; assessed vs governed; different states | §2 |
| #3 | Not a Finding; may be informed by, does not replace, Findings | §2, §3 |
| #4 | Not a Resolution Candidate; not a proposal | §2, §4 |
| #5 | Not a Review Request; not a request | §2, §5 |
| #6 | Not a Disposition; the governed understanding after governance | §2, §6 |
| #7 | Not Governance; the result of acceptance, not the act | §2, §7 |
| #8 | May be reconsidered; acceptance is not permanence | §12 |
| #9 | Preserves history; historical accepted understanding retained | §12 |
| #10 | Does not directly alter CAF, Reliability, or Confidence | §8, §9, §10 |
| #11 | Explainable; traceable Finding → … → Governance → Accepted Understanding | §13 |
| #12 | Event-driven; changes on governance context, not time | §12 |
| #13 | Bridge between Governance and future Knowledge Layer concepts | §11 |

All thirteen founder positions are represented.

**Required behavior examples:** A (understanding accepted — established), B (acceptance declined — not established), C (reconsidered — history preserved), D (CAF unchanged, Accepted Understanding changes — acceptance and assessment separate), E (leads to action — evidence changes, CAF may change) — all included and explained conceptually (§14).

**Exclusion checklist**
- Distinct from Understanding — confirmed (§2).
- Distinct from Findings — confirmed (§2, §3).
- Distinct from Resolution Candidates — confirmed (§2, §4).
- Distinct from Review Requests — confirmed (§2, §5).
- Distinct from Dispositions — confirmed (§2, §6).
- Distinct from Governance — confirmed (§2, §7).
- Does not directly alter CAF — confirmed (§8).
- Does not directly alter Reliability — confirmed (§9).
- Does not directly alter Confidence — confirmed (§10).
- Explainable — confirmed (§13).
- Event-driven — confirmed (§12).
- Preserves history — confirmed (§12, Ex. C).
- Bridges Governance and future Knowledge Layer concepts — confirmed (§11, §16).
- No workflow implementation — confirmed (§12, §16).
- No truth-promotion implementation — confirmed (§16).
- No scoring formulas — confirmed.
- All thirteen referenced documents unmodified — confirmed (consumed only).

*Accepted Understanding Model v1 complete. Formalizes the founder-approved positions; defines Accepted Understanding as the durable, governed output of Governance — distinct from Understanding, Findings, Resolution Candidates, Review Requests, Dispositions, and Governance itself — that alters no assessment signal, is event-driven and explainable, preserves history, may be reconsidered, and bridges Governance and future Knowledge Layer concepts. Defines the object and the bridge only — not truth promotion, canonical knowledge, knowledge-layer mechanisms, storage, workflows, notification, UI, automation, or formulas. Subject to governance review before adoption.*
