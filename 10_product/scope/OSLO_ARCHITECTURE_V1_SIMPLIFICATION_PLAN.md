# OSLO Architecture v1 Simplification Plan

**Document:** OSLO_ARCHITECTURE_V1_SIMPLIFICATION_PLAN.md
**Type:** Read-only architecture simplification plan (classification & recommendation only)
**Reviewed (authoritative, unmodified):** the full model set (CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation · Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding · Notification) · `MODEL_LINEAGE_INDEX_V1.md` · `MODEL_COVERAGE_AUDIT_V1.md`
**Date:** 2026-05-31

> **Nature of this document.** This is a **read-only plan**. It **deletes no file**, **modifies no model document**, and **does not modify the Model Lineage Index**. It classifies the existing models for a simplified, planning-stage **Architecture v1**, explains why the Governance Domain is deferred, and **recommends** (without making) the index updates that would reflect the simplification. Every governance model remains **specified and preserved** as future scope; nothing is removed.

---

## 1. Purpose

Simplify **Architecture v1** for the **planning-stage product** by removing the first-class **Governance Domain** models from the *active* v1 architecture, while **preserving them intact** as future **Outcome Orchestration / agent-governance** scope.

The simplification is a **re-classification**, not a deletion or a redesign: the same fourteen specified models remain on disk and unchanged; this plan only re-frames which of them constitute the *active* planning-stage architecture and which are deferred.

---

## 2. Rationale — Why Governance Is Deferred

**Planning-stage OSLO is an understanding-improvement system, not yet a governed execution/orchestration system.**

The active value loop of planning-stage OSLO is: *assess understanding → make it observable → surface what's weak → suggest improvements → the user acts → new evidence → re-assess.* In that loop the **user retains authority**; OSLO recommends, the user decides, and only **action and evidence** change understanding.

The **Governance Domain** (Resolution Candidate → Review Request → Human Evaluation → Disposition → Governance → Accepted Understanding) implements something different and later: the **controlled acceptance of understanding** — proposing resolutions, requesting evaluation, recording outcomes, governing acceptance, and producing durable *accepted* (governed) understanding. That machinery — validation, review, disposition, acceptance, the promotion of understanding toward governed/accepted status — is the substrate of **governed execution and Outcome Orchestration / agent governance**, not of a planning-stage understanding tool.

Deferring governance is consistent with the product's own framing: the Release 1 scope is understanding, improvement, sharing, and conversion, with **Execution Intelligence, Operational Confidence, Portfolio/Program Intelligence, Agent Governance, and Autonomous Project Management explicitly out of scope** ("OSLO recommends. Users decide."). The Governance Domain is the home of exactly those deferred concerns.

**Key structural fact that makes deferral safe:** the Understanding Domain loop is **self-contained and closed**. It closes through *User Action → Evidence* without ever entering the governance chain. Removing governance from active v1 therefore leaves a **complete, closed system** — no active transition becomes unowned, because the governance chain was always an *additional downstream*, never a link the understanding loop depended on.

---

## 3. Classification

Every model/document classified into the four buckets.

| Document | Bucket | Notes |
|---|---|---|
| CAF Assessment | **Active Architecture v1** | Assessment foundation |
| CAF Scoring | **Active Architecture v1** | Representation/scoring of CAF |
| Reliability | **Active Architecture v1** | Supportability of the assessment |
| Confidence | **Active Architecture v1** | Summarized trust signal |
| MRI | **Active Architecture v1** | Visualization of understanding |
| Overlay | **Active Architecture v1** | Attention management |
| Finding | **Active Architecture v1** | The governable, actionable object |
| Recommendation | **Active Architecture v1** | Prescriptive improvement suggestion |
| Notification | **Supporting Service** | Awareness service; active-object triggers operative (see §5) |
| Resolution Candidate | **Future Scope** | Governance entry object → Outcome Orchestration / agent governance |
| Review Request | **Future Scope** | Evaluation request → governed acceptance |
| Disposition | **Future Scope** | Evaluation-outcome record → governed acceptance |
| Governance | **Future Scope** | Acceptance layer → governed execution |
| Accepted Understanding | **Future Scope** | Governed output → Outcome Orchestration endpoint |
| Model Lineage Index | **Archive / Reference** | Navigational map; *recommended for update* (see §9), not archived |
| Model Coverage Audit | **Archive / Reference** | Retained analysis artifact |
| Terminology Audit / Decision 001 / Workbook 001 | **Archive / Reference** | Retained decision-support artifacts |
| This plan | **Archive / Reference** | Read-only planning artifact |

*No document is deleted. "Archive / Reference" means retained-for-reference, not removed.*

---

## 4. Active Architecture v1 (the understanding-improvement system)

The eight Understanding Domain models constitute Active Architecture v1, forming the closed understanding-improvement loop:

```text
Evidence → Inference → Finding → Impact Assessment → CAF → Reliability → Outcome Confidence
   → MRI → Overlay → Recommendation → [User Action: external] → Evidence
```

This is the complete active system: it assesses understanding (CAF Assessment, CAF Scoring), qualifies it (Reliability), summarizes it (Confidence), makes it observable and navigable (MRI, Overlay), captures the actionable object (Finding), and prescribes improvement (Recommendation) — closing through user action. **It requires none of the Governance Domain models to be complete.** The descriptive/prescriptive boundary (seven descriptive + one prescriptive) is entirely contained within Active v1.

---

## 5. Supporting Service — Notification

Notification remains the one **Supporting Service** in Active v1: it surfaces awareness of relevant changes across the active system **without belonging to the loop** and **without altering anything it announces**.

**Trigger scope under the simplification (no model change required):** the Notification Model conceptually lists triggers including governance objects (Review Request, Disposition, Governance outcomes, Accepted Understanding). Under Architecture v1, only the **active-object triggers are operative** — changes in **Findings** and **Recommendations**. Notification's **governance-object triggers are deferred** alongside the Governance Domain and become operative when governance does. This is a *scoping observation*, not an edit: the Notification Model already defines all triggers conceptually; planning-stage v1 simply exercises the active subset.

---

## 6. Future Scope — Governance Domain (Outcome Orchestration / Agent Governance)

The five Governance Domain models are reclassified as **Future Scope**, preserved exactly as written:

```text
Finding → Resolution Candidate → Review Request → Human Evaluation (external)
   → Disposition → Governance → Accepted Understanding → [deferred Knowledge Layer]
```

These models specify **governed acceptance** — the controlled path by which understanding becomes *accepted/governed*. That capability belongs to **Outcome Orchestration and agent governance**, where governed execution, validation, and acceptance authority become first-class. They are **not deleted, not modified, and not deprecated** — they are **deferred**: complete, specified, and ready to re-activate when OSLO moves from a planning-stage understanding system to a governed orchestration system.

**What carries forward unchanged when governance re-activates:** the understanding-domain hand-off point (Finding), the external Human Evaluation step, the history-preservation and explainability invariants, and the bridge to the deferred Knowledge Layer. Nothing about the active system blocks their return.

---

## 7. Reference / Archive

The navigational and analysis documents (Model Lineage Index, Model Coverage Audit, Terminology Audit, Decision 001, Workbook 001, and this plan) are **retained for reference**. **No archiving or deletion is required or recommended.** The Model Lineage Index is the one Reference document that should be **updated** to reflect the active/future split (§9) — updated in place, not archived.

---

## 8. Impact of the Simplification

- **Active surface shrinks from 14 to 9 models** (8 Understanding + Notification), simplifying the planning-stage architecture a contributor must hold in mind.
- **No active transition becomes unowned** — the understanding loop was always closed independently of governance (§2).
- **No capability is lost** — governance is deferred, not removed; all five models remain specified and re-activatable.
- **The descriptive/prescriptive boundary is unaffected** — it lives entirely in Active v1.
- **Notification narrows to active triggers** — its governance triggers go dormant with governance (§5), with no model edit needed.
- **The deferred Knowledge Layer frontier is unchanged** — still beyond Accepted Understanding, still undefined; the simplification simply means the *path to it* (governance) is future scope too.
- **Terminology decisions are de-risked for v1** — the open "Accepted/Acceptance," "Governed vs Accepted Understanding," and "Outcome" collisions (per the Decision/Workbook artifacts) all sit in the **deferred** Governance Domain or at the governance endpoint; only the comparatively low-risk Understanding-Domain usages remain active, so the founder terminology decisions are no longer on the v1 critical path.

---

## 9. Recommended Index Updates (exact — *do not make them in this plan*)

The following are the precise updates that **would** bring `MODEL_LINEAGE_INDEX_V1.md` into line with this simplification. **This plan recommends them; it does not apply them.** Each is a re-framing only — no model behavior, lineage, or boundary changes.

1. **§2 Architectural Overview.** Reframe from "two fully-specified domains + supporting service" to: **Active Architecture v1 = the eight Understanding Domain models + the Notification supporting service**; the **Governance Domain is reclassified as Future Scope (Outcome Orchestration / agent governance)**, specified but not part of active v1.
2. **§5 Model Responsibility Matrix.** Keep all rows (delete nothing); **add a status marker per row** — `Active v1` (the 8), `Supporting Service` (Notification), `Future Scope` (the 5 governance models). Update the grouping note accordingly.
3. **§7 Governance Domain Overview.** Re-title/re-frame from an *active, fully-specified* domain to **"Governance Domain — Future Scope (deferred)."** Keep the governance lineage chain and the Human Evaluation external note **verbatim**; only change the framing sentence(s) that present it as active.
4. **§8 Future Model Expansion Areas.** Move the five "Specified Governance Domain Models" under a heading such as **"Future Scope — Governance Domain (Outcome Orchestration / Agent Governance)"**, retaining their per-model purpose lines and "Specified" tags (they remain specified, just deferred). Keep "Specified Supporting Services → Notification." Keep the "Future Expansion Areas / deferred Knowledge Layer" note.
5. **§9 Architectural Principles.** Keep the Understanding and Notification principles as **Active v1**; mark the seven Governance Domain principles as **Future Scope** (no wording change to the principles themselves).
6. **§10 Summary.** Reframe to: Active Architecture v1 = 9 models (8 Understanding + Notification); 5 Governance Domain models deferred to Future Scope (Outcome Orchestration / agent governance); fourteen models remain specified; the deferred Knowledge Layer remains the frontier.
7. **Validation.** Update tables/checklist to assert the **Active v1 (9) vs Future Scope (5)** split, that governance is **specified-but-deferred** (not active, not deleted), that no model was modified, and that no document was archived or removed.

*Recommendation only. No edit above has been performed.*

---

## 10. Preservation Guarantees

- **No file deleted** — all fourteen model documents and all reference documents remain on disk.
- **No model document modified** — the Governance Domain models are reclassified, not edited; they remain specified verbatim.
- **No index modified by this plan** — §9 lists recommended index edits; none is applied here.
- **No doctrine introduced, no architecture redesigned** — this is a classification of existing, unchanged models.
- **Governance is deferred, not deprecated** — fully re-activatable as Outcome Orchestration / agent governance.

---

## 11. Verification

- **Read-only plan produced** — confirmed (classification + rationale + recommendations only).
- **No file deleted** — confirmed.
- **No model document modified** — confirmed.
- **Model Lineage Index not modified** — confirmed (edits are recommended in §9, not made).
- **Active Architecture v1 = CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, Overlay, Finding, Recommendation** — confirmed (§3, §4).
- **Supporting Service = Notification** — confirmed (§3, §5).
- **Future Scope = Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding** — confirmed (§3, §6).
- **Governance deferral rationale stated** (planning-stage OSLO is an understanding-improvement system, not yet a governed execution/orchestration system) — confirmed (§2).
- **Exact index updates recommended but not made** — confirmed (§9).

*OSLO Architecture v1 Simplification Plan complete. A read-only re-classification deferring the five Governance Domain models to Future Scope (Outcome Orchestration / agent governance) while preserving them intact, leaving Active Architecture v1 as the eight Understanding Domain models plus the Notification supporting service. No file deleted, no model modified, no index modified; index updates recommended only.*
