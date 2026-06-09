# Authority-Plane Model v1 (Product Governance — formerly Governance Model)

**Document:** AUTHORITY_PLANE_MODEL_V1.md *(renamed from `GOVERNANCE_MODEL_V1.md` per DL-053 to disambiguate)*
**Status:** Specification of the Authority-Plane Model — **OSLO's product Authority-Plane (the Governance Domain's acceptance layer)**

> **Disambiguation (DL-053):** "Governance" in this document means OSLO's **product Authority-Plane Governance**
> (the product governing its own outputs — expose/suppress/authorize a finding), **specified but INACTIVE in R1**.
> It is **not** Build-Governance (CI/deploy/QA gates) or Repository Governance (Framework 001 / DL- ratification).
> See `00_owner/CANONICAL_GLOSSARY.md` § Disambiguation Register.
**Consumes (authoritative, unmodified):** `CAF_ASSESSMENT_MODEL_V1.md` · `CAF_SCORING_MODEL_V1.md` · `RELIABILITY_MODEL_V1.md` · `CONFIDENCE_MODEL_V1.md` · `MRI_MODEL_V1.md` · `OVERLAY_MODEL_V1.md` · `FINDING_MODEL_V1.md` · `RECOMMENDATION_MODEL_V1.md` · `RESOLUTION_CANDIDATE_MODEL_V1.md` · `REVIEW_REQUEST_MODEL_V1.md` · `DISPOSITION_MODEL_V1.md` · `MODEL_LINEAGE_INDEX_V1.md`
**Date:** 2026-05-31

> **Architecture V1 classification (added by the Architecture V1 Simplification Refactor):** **Future Architecture — Outcome Orchestration / Agent Governance.** This model is **preserved and specified in full** and is **not part of the active Architecture V1 (Planning Intelligence) system**; it is deferred for later activation. This classification is additive — **no model content below is changed, deprecated, or invalidated.** See `ARCHITECTURE_V1_REFACTOR_REPORT.md`.

> **Scope.** This document defines the **Governance Model** — what Governance is, why it exists, how it relates to Understanding and to Findings, Resolution Candidates, Review Requests, Dispositions, CAF, Reliability, and Outcome Confidence, and how it relates to accepted understanding. It establishes Governance as the layer responsible for the **controlled acceptance of understanding**. It does **not** define governance workflows, approval workflows, reviewer-assignment algorithms, routing logic, notification behavior, escalation mechanisms, truth-promotion algorithms, user interfaces, automation rules, or scoring formulas. Those are future Governance Domain capabilities, defined elsewhere.
>
> **Position in the architecture.** The Governance Domain has been built up through the Resolution Candidate (proposed resolutions), the Review Request (requests for evaluation), and the Disposition (recorded outcomes). The Governance Model is the layer those objects serve: it governs the **acceptance** of understanding. This document does not modify the Model Lineage Index or any other model.
>
> **Governance.** Non-canonical specification formalizing founder-approved positions; adoption subject to governance review. The twelve referenced models are consumed, not modified. Canonical terminology is preserved.

---

## 1. Purpose

Define, as a coherent specification, OSLO's **Governance Model**: the domain layer responsible for determining what understanding may be accepted.

This document defines:

- what Governance is;
- why Governance exists;
- how Governance relates to Understanding;
- how Governance relates to Findings;
- how Governance relates to Resolution Candidates;
- how Governance relates to Review Requests;
- how Governance relates to Dispositions;
- how Governance relates to accepted understanding.

It establishes Governance as the layer responsible for the controlled acceptance of understanding. It is a conceptual model: it defines no workflow, no authority mechanism, no truth-promotion algorithm, and no formula.

---

## 2. Governance Overview

**Governance is a domain, not a workflow.** It **exists to determine what understanding may be accepted.** Governance **does not create understanding** — understanding is created by the Understanding Domain. *(Governance Position #1)*

**Governance exists because assessment alone is insufficient for acceptance.** **Assessment may identify understanding; Governance determines whether understanding may be accepted.** *(Governance Position #2)* Knowing *what* is understood, *how strongly*, and *how trustworthily* — the work of the Understanding Domain — does not by itself establish that the understanding is accepted. Acceptance is a separate act, and Governance is the layer responsible for it.

**Governance is responsible for acceptance, not for assessment.** *(Governance Position #11)* **Assessment and acceptance are separate responsibilities.** The Understanding Domain assesses; the Governance Domain accepts. This separation is the central commitment of the model.

**Governance depends upon human judgment.** It **may be informed by assessments**, but it **is not performed by assessments.** *(Governance Position #7)* No assessment signal — not CAF, not Reliability, not Confidence — performs governance; governance is a human responsibility that those signals may inform.

**Governance consumes understanding; it does not create it.** Governance consumes Findings, Resolution Candidates, Review Requests, and Dispositions. *(Governance Position #6)*

---

## 3. Relationship To Findings

- **Findings remain descriptive observations.**
- **Governance consumes Findings.**
- **Governance does not create Findings.**
- **Governance does not alter Findings directly.**

Governance reads the Findings the Understanding Domain produced; it neither authors them nor changes them. A Finding changes only as understanding changes.

---

## 4. Relationship To Resolution Candidates

- **Resolution Candidates remain proposals.**
- **Governance consumes Resolution Candidates.**
- **Governance does not create Resolution Candidates.**

Governance weighs the proposed resolutions surfaced for it; it does not propose them. The Resolution Candidate remains a proposal regardless of what Governance accepts.

---

## 5. Relationship To Review Requests

- **Review Requests remain requests for evaluation.**
- **Governance consumes Review Requests.**
- **Governance does not create Review Requests.**

Governance operates in a context shaped by the requests for evaluation that preceded it; it does not issue those requests. The Review Request remains the asking; Governance is concerned with acceptance, downstream of the evaluation a request set in motion.

---

## 6. Relationship To Dispositions

- **Dispositions remain recorded outcomes.**
- **Governance consumes Dispositions.**
- **Governance does not replace Dispositions.**
- **Dispositions provide the durable basis on which Governance operates.**

The Disposition is the record of an evaluation's outcome; Governance stands on that durable record. Governance does not overwrite or substitute for a Disposition — it consumes the recorded outcome and governs acceptance on its basis. Where a Disposition preserves the *outcome of an evaluation*, Governance addresses *whether the understanding is accepted* in light of it.

---

## 7. Relationship To CAF

- **CAF assesses understanding** (integrity).
- **Governance governs acceptance.** *(Governance Position #3)*
- **Governance may be informed by CAF.**
- **Governance does not alter CAF.** *(Governance Position #8)*

CAF and Governance are distinct: one assesses the integrity of understanding, the other governs whether understanding is accepted. Governance may take CAF into account, but it neither performs CAF nor changes it; assessment changes only through evidence and understanding changes (Section 10).

---

## 8. Relationship To Reliability

- **Reliability assesses supportability.**
- **Governance governs acceptance.** *(Governance Position #4)*
- **Governance may be informed by Reliability.**
- **Governance does not alter Reliability.** *(Governance Position #8)*

Reliability tells Governance how trustworthy an assessment is; Governance may weigh that, but it neither determines nor changes Reliability.

---

## 9. Relationship To Outcome Confidence

- **Confidence summarizes trust in understanding.**
- **Governance governs acceptance.** *(Governance Position #5)*
- **Governance may be informed by Confidence.**
- **Governance does not alter Confidence.** *(Governance Position #8)*

Confidence summarizes how much to trust the understanding; Governance may be informed by it but changes none of the consolidation that produces it and none of its value. Notably, a high confidence signal does not itself constitute acceptance — acceptance remains a separate, governed act.

---

## 10. Governance Philosophy

Two domains ask two different questions:

- The **Understanding Domain** answers: *"What do we understand?"*
- The **Governance Domain** answers: *"What are we willing to accept?"*

**Understanding and acceptance are not the same thing.** A project may be:

- well understood but not accepted;
- accepted but later reconsidered;
- poorly understood and not accepted.

**Governance exists because understanding alone does not establish acceptance.** These cases show that the two can diverge in every direction — strong understanding need not be accepted, an acceptance can be revisited, and absence of understanding need not force a decision either way. Governance is the layer that holds the second question apart from the first.

**Conceptual relationship.** Governance is the layer that stands between understanding and accepted understanding:

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
```

**Governance bridges Understanding and Accepted Understanding.** *(Governance Position #12)* It is the final layer of the Governance Domain chain — consuming Findings, proposed resolutions, requests, and recorded outcomes, and, on a basis of human judgment, governing whether understanding is accepted. As throughout the architecture, Governance changes understanding through nothing on its own; only action and resulting evidence change assessment.

---

## 11. Governance Lifecycle Model

**Governance is event-driven.** *(Governance Position #10)* A governance outcome exists in relation to its governance context — the Findings, Resolution Candidates, Review Requests, and Dispositions that precede it — and it moves when that context changes.

**Lifecycle concepts.** Governance may move through:

- **establishment** — an acceptance outcome is established on the basis of its governance context;
- **change** — a governance outcome changes when its governance context changes;
- **reconsideration** — an established acceptance may be reconsidered (an *accepted but later reconsidered* case, Section 10);
- **supersession** — one governance outcome may supersede another;
- **historical retention** — a superseded or reconsidered governance outcome is **retained as history**, not erased.

These are **lifecycle concepts only**; this model does **not** prescribe implementation-specific states, and **no workflow implementation is defined.**

**History is preserved.** Consistent with the Disposition Model and the Finding Model, governance outcomes retain history: reconsideration and supersession produce a new current outcome while the prior one is retained, keeping the governance record truthful and auditable.

**Event-driven, not time-driven.** **Governance changes when governance context changes; it does not change merely because time passes.** *(Governance Position #10)* It inherits the event-driven discipline of the entire architecture.

---

## 12. Governance Explanation Model

**Governance is explainable.** *(Governance Position #9)* Every governance outcome should be traceable to its basis:

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
```

An explanation of a governance outcome should identify:

- **the originating Finding** — the Finding ultimately at issue;
- **the relevant Resolution Candidate(s)** — the proposed resolution(s) concerned;
- **the Review Request** — the request whose evaluation contributed to the outcome;
- **the Disposition(s)** — the recorded evaluation outcome(s) on which Governance operated;
- **the governance rationale** — why understanding was or was not accepted;
- **the accepted understanding outcome** — what acceptance state resulted.

**Governance should never appear disconnected from its basis.** A governance outcome that cannot be traced through a Disposition, Review Request, and Resolution Candidate to a Finding would violate this model. As elsewhere, the explanation reduces to a *basis*, not a formula; the model remains conceptual and defines no scoring by which acceptance is produced.

---

## 13. Governance Behavior Examples

These examples illustrate the model's expected behavior conceptually. They introduce no workflow and no formula.

### Example A — understanding accepted
- **Chain:** Finding → Resolution Candidate → Review Request → Disposition → Governance.
- **Result:** **understanding accepted.** Governance, on the basis of the recorded disposition and human judgment, governs the understanding as accepted. It consumed the prior governance objects; it created none of them.

### Example B — acceptance declined
- **State:** Governance declines acceptance.
- **Result:** **understanding remains unaccepted.** Declining is a governance outcome; the underlying understanding (the Finding, its assessment) is untouched — it simply has not been accepted. Assessment and acceptance remain separate (Section 2).

### Example C — a governance outcome changes
- **State:** a governance outcome changes (for example, an accepted understanding is reconsidered).
- **Result:** **prior governance is retained as history** (Section 11). The new outcome becomes current while the prior outcome remains part of the governance record.

### Example D — acceptance moves independently of assessment
- **State:** CAF remains unchanged; Governance changes.
- **Result:** **acceptance changes independently from assessment.** Because Governance governs acceptance and not assessment, an acceptance outcome can move while CAF stays fixed — the clearest demonstration that the two responsibilities are separate (Sections 2, 7).

### Example E — accepted understanding leads to action
- **State:** accepted understanding leads to action; evidence changes.
- **Result:** **CAF may change.** Governance influenced assessment **only through action**: acceptance led to action, action produced new evidence, and the assessment chain re-ran. Governance itself altered nothing — the action did (Section 8). (Such change is possible but not guaranteed.)

---

## 14. Preserved Model Principles

The Governance Model consumes the upstream models and preserves their principles without redefining them:

| Upstream principle | How the Governance Model preserves it |
|---|---|
| CAF assesses understanding integrity | Governance may be informed by CAF but governs acceptance, not assessment; never alters CAF (§7) |
| Reliability assesses supportability | Governance may be informed by Reliability but never alters it (§8) |
| Confidence summarizes trust | Governance may be informed by Confidence but never alters it; confidence is not acceptance (§9) |
| Findings are descriptive observations | Governance consumes Findings; it neither creates nor alters them (§3) |
| Recommendations are prescriptive | Recommendations remain prescriptive; Governance is acceptance-oriented and distinct (§14 below) |
| Resolution Candidates are proposals | Governance consumes proposals without creating them or making them accepted by default (§4) |
| Review Requests request evaluation | Governance consumes requests; it does not issue them (§5) |
| Dispositions record outcomes; preserve history | Governance stands on Dispositions without replacing them; governance outcomes preserve history (§6, §11) |
| Assessment moves only on its inputs via action | Governance changes assessment through nothing; only action and evidence can (§7–§9, §13) |
| Event-driven and explainable across the architecture | Governance is event-driven and explainable to its basis (§11, §12) |

**Assessment remains separate from acceptance.** Findings **remain descriptive**; Recommendations **remain prescriptive**; Governance **remains acceptance-oriented**; and Governance **must not redefine** the assessment models.

---

## 15. Future Evolution

Future versions may add:

- authority models;
- policy models;
- truth-promotion models;
- audit models;
- delegation models;
- governance automation.

These are future capabilities. This document defines **Governance only** — the acceptance layer of the Governance Domain, its relationships, lifecycle concepts, and explanation, at the conceptual level. Authority, policy, truth promotion, audit, delegation, and automation — along with workflows, routing, notification, escalation, user interfaces, and any scoring — are defined elsewhere, not here.

---

## 16. Summary

Governance is a domain, not a workflow — the layer responsible for the controlled acceptance of understanding. It exists because assessment alone is insufficient for acceptance: the Understanding Domain identifies and assesses understanding, but determining whether that understanding may be accepted is a separate responsibility, and Governance holds it. Governance depends upon human judgment; it may be informed by assessments but is never performed by them.

Governance is distinct from CAF, Reliability, and Outcome Confidence — each assesses some facet of understanding, while Governance governs acceptance. It consumes the Governance Domain's objects — Findings, Resolution Candidates, Review Requests, and Dispositions — without creating any of them, and it stands on Dispositions as its durable basis. It alters none of the assessment signals, nor the Findings; assessment changes only through evidence and understanding changes, so acceptance can move independently of assessment. Governance is event-driven and explainable, always traceable through a Disposition, Review Request, and Resolution Candidate to an originating Finding, and it preserves history when outcomes are reconsidered or superseded.

Governance bridges Understanding and Accepted Understanding — the layer that stands between what we understand and what we are willing to accept. This document defines that layer only; it defines no authority model, workflow, policy, truth-promotion algorithm, audit, delegation, automation, routing, notification, UI, or formula.

---

## Validation

**Founder position coverage**

| Position | Subject | Represented in |
|---|---|---|
| #1 | A domain, not a workflow; determines acceptable understanding; does not create understanding | §2 |
| #2 | Exists because assessment alone is insufficient for acceptance | §2 |
| #3 | Distinct from CAF; CAF assesses, Governance governs acceptance | §7 |
| #4 | Distinct from Reliability | §8 |
| #5 | Distinct from Outcome Confidence | §9 |
| #6 | Consumes Findings, Resolution Candidates, Review Requests, Dispositions; does not create understanding | §2, §3–§6 |
| #7 | Depends on human judgment; informed by, not performed by, assessments | §2 |
| #8 | Does not directly alter CAF, Reliability, or Confidence | §7, §8, §9 |
| #9 | Explainable; traceable Finding → Resolution Candidate → Review Request → Disposition → Governance | §12 |
| #10 | Event-driven; changes on governance context, not time | §11 |
| #11 | Responsible for acceptance, not assessment; separate responsibilities | §2 |
| #12 | Bridges Understanding and Accepted Understanding | §10 |

All twelve founder positions are represented.

**Required behavior examples:** A (understanding accepted), B (acceptance declined — understanding remains unaccepted), C (governance outcome changes — prior retained as history), D (CAF unchanged, Governance changes — acceptance independent of assessment), E (accepted understanding leads to action — evidence changes, CAF may change) — all included and explained conceptually (§13).

**Exclusion checklist**
- Governance distinct from assessment — confirmed (§2, §11).
- Governance distinct from CAF — confirmed (§7).
- Governance distinct from Reliability — confirmed (§8).
- Governance distinct from Confidence — confirmed (§9).
- Governance consumes but does not create understanding — confirmed (§2–§6).
- Governance depends on human judgment — confirmed (§2).
- Does not directly alter CAF — confirmed (§7).
- Does not directly alter Reliability — confirmed (§8).
- Does not directly alter Confidence — confirmed (§9).
- Explainable — confirmed (§12).
- Event-driven — confirmed (§11).
- Bridges Understanding and Accepted Understanding — confirmed (§10).
- No workflow implementation — confirmed (§11, §15).
- No truth-promotion implementation — confirmed (§9, §15).
- No scoring formulas — confirmed.
- All twelve referenced documents unmodified — confirmed (consumed only).

*Governance Model v1 complete. Formalizes the founder-approved positions; defines Governance as the acceptance layer — a domain (not a workflow) that consumes Findings, Resolution Candidates, Review Requests, and Dispositions, depends on human judgment, alters no assessment signal, is event-driven and explainable, preserves history, and bridges Understanding and Accepted Understanding. Defines the model only — not authority, policy, truth promotion, audit, delegation, automation, workflow, routing, notification, UI, or formulas. Subject to governance review before adoption.*
