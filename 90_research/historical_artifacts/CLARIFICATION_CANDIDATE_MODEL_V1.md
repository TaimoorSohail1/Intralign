# Clarification Candidate Model v1 — RETIRED

> **📦 ARCHIVED 2026-06-04 — historical.** Superseded by `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md (Resolution Paths substructure)`. Moved to `04_research/historical_artifacts/` to keep the active tree clean; content preserved for history and does **not** govern implementation.

> ## ⛔ RETIRED / SUPERSEDED — founder decision (2026-05-31)
> **Per founder decision, the Clarification Candidate is NOT a first-class persisted Release 1 object.** "Resolution Paths" are instead modeled as a **Recommendation substructure** (`Recommendation → resolution_paths[]`), not as a standalone domain object.
> - This document is **NOT registered as an active domain object** and **NOT** added to the active model lineage. It is **retained for reference only** (history preserved; not deleted).
> - **Superseded by:** `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` and `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` §4 (resolution_paths).
> - **No** ClarificationCandidate entity / lifecycle / events / endpoints / UI pages / fixtures / governance model are created.
> - The Future-Architecture `RESOLUTION_CANDIDATE_MODEL_V1.md` (governance object) remains **untouched** and is **not reclassified**.
> - The accompanying `CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md` is likewise **superseded** and is no longer the implementation direction.
>
> *The content below is preserved as the historical proposal only; it does not govern Release 1 implementation.*

**Type:** Implementation/conceptual model — **RETIRED proposal** (superseded; not an active object)
**Status:** **RETIRED / superseded — not an active domain object** · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** Recommendation Model v1 · Finding Model · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · CAF Scoring v2 · Reliability v2 · Confidence v2 · State/Data Models.
**Revision:** 2026-05-31 — clarified as a **persisted** Active Release 1 object with user-facing label **"Resolution Path"**, and added **recommended-path vs user-selected-path** semantics (§2a). Cross-document changes (Data/State/Event/API/UI/Recommendation/Testing) are specified in `CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md` (ready-to-apply, pending owner ratification). The Future-Architecture Resolution Candidate model is **not** modified.

> **Naming note.** "**Clarification Candidate**" is a **new, distinct active-Architecture-V1 object**, deliberately named to **avoid collision** with the existing `RESOLUTION_CANDIDATE_MODEL_V1.md`, which is a **Future-Architecture *Governance* object** ("the first Governance Domain object"). The two are **different objects**: the Resolution Candidate (governance/future) is **untouched** by this document; the Clarification Candidate (active/non-governance) is defined here. "Clarification" is used in the broad sense of *clarifying/resolving the understanding gap a finding represents* — it spans all finding-resolution paths (§5), not only Clarity.
>
> **Persistence & user-facing label.** The Clarification Candidate is a **persisted Active Release 1 object** (a Data Model entity — see `CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md`). Its **user-facing label is "Resolution Path"**; "Clarification Candidate" is the internal/model name. UI surfaces a finding's candidates as **"Possible Resolution Paths."**
>
> **Scope guards.** Active Release 1 only. **No Governance, Accepted Understanding, Resolution Candidate (governance), Disposition, Review, Approval, Agent Governance, Autonomous execution, Actuation, scoring, formulas, thresholds, weighting, or probability.** Clarification Candidates change **no** CAF/Reliability/Confidence signal directly; only **user action → reanalysis** does.

---

## 1. Purpose

Define the **Clarification Candidate**: a **possible way a finding could be resolved**, surfaced so the user can consider it. Clarification Candidates populate the **option space** that recommendations draw from and that user action ultimately acts upon — closing the understanding-improvement loop **without** any governance, approval, or truth-promotion semantics.

This document defines: what a Clarification Candidate is; how it differs from a Finding and a Recommendation; its types; its lifecycle; its traceability; the user-interaction boundary; how it feeds recommendations and reanalysis; and its explicit exclusions.

---

## 2. What a Clarification Candidate Is

> **A Clarification Candidate is a proposed, non-advisory possibility for resolving a Finding** — a candidate resolution path. It enumerates *a way the finding could be resolved*, without advising that it be taken and without deciding, approving, or governing anything.

- It is an **understanding-improvement option object** — **not** an assessment object and **not** a governance object.
- **Multiple Clarification Candidates may exist for one Finding** — the set of plausible resolution paths (the "alternative paths" of `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` §5).
- It is **optional and advisory-neutral**: it states a possibility; it neither commands nor recommends (recommending is the Recommendation's job, §4).
- It **influences understanding only indirectly** — via a recommendation and/or user action that produces information change and reanalysis. It **never** modifies CAF/Reliability/Confidence directly.

---

## 2a. Persistence, User-Facing Label, and Recommended vs Selected Path

- **Persisted Active Release 1 object.** A Clarification Candidate is **persisted** (a Data Model entity with identity), not an ephemeral display item. Its lifecycle, links, and supersession history are stored and reconstructable.
- **User-facing label: "Resolution Path."** Internally the object is the *Clarification Candidate*; to users it is presented as a **Resolution Path**, and a finding's set of candidates is presented as **"Possible Resolution Paths."**
- **One finding → many Resolution Paths.** A single Finding may have **multiple** Clarification Candidates (the plausible resolution paths). They **coexist** as parallel valid options (coupling spec §5); none is "the answer" by default.
- **OSLO's recommended path.** A **Recommendation may identify exactly one** of a finding's Clarification Candidates as **OSLO's recommended path** (an advisory `is_recommended` marker set via the recommendation). At most one candidate per finding is marked recommended at a time; this is **advice, not a decision**.
- **User-selected path (may differ).** The **user may select any** Resolution Path — **including one different from OSLO's recommended path** (a `is_selected` marker set by the user). OSLO's recommendation never constrains the user's choice; **recommended ≠ selected**, and the two may diverge.
- **Still advisory-neutral and non-governance.** Marking recommended (OSLO) or selecting (user) is **not** an approval, decision, or governance act, and **changes no CAF/Reliability/Confidence signal**. Only the user's subsequent **action → information change → reanalysis** can move assessment.
- **Still distinct from the Resolution Candidate.** This persisted Release 1 *Resolution Path* object is **not** the Future-Architecture governance Resolution Candidate (which remains untouched).

---

## 3. How a Clarification Candidate Differs From a Finding

| | Finding | Clarification Candidate |
|---|---|---|
| **Nature** | **Descriptive** — states *what is wrong/uncertain* in the understanding | **Possibility** — states *a way that could be resolved* |
| **Direction** | Identifies a gap/conflict/assumption/etc. | Proposes a resolution path for such a finding |
| **Cardinality** | The observed condition | **One-or-more** candidates may address one finding |
| **Role in loop** | The problem to be improved | An option for improving it |
| **Governance** | None (descriptive) | None (explicitly excluded) |

A Finding **describes**; a Clarification Candidate **proposes a possibility** to resolve that description. A Clarification Candidate **always traces to ≥1 Finding** (§7) and cannot exist without one.

---

## 4. How a Clarification Candidate Differs From a Recommendation

| | Recommendation | Clarification Candidate |
|---|---|---|
| **Nature** | **Advisory / prescriptive** — OSLO's *suggested action* ("do this") | **Non-advisory possibility** — *"this could resolve it"* |
| **Stance** | OSLO advocates a path | OSLO enumerates a path without advocating |
| **Relationship** | A recommendation may **advise pursuing** a specific Clarification Candidate | A Clarification Candidate may **give rise to** a recommendation |
| **Selection** | OSLO's suggestion | The space the suggestion selects from |
| **Action** | Suggests an action; only the user acts | Suggests a possibility; only the user acts |

**Key distinction:** a **Recommendation is OSLO's advice**; a **Clarification Candidate is the neutral possibility space that advice draws from.** They are complementary, not redundant: candidates enumerate *what could resolve the finding*; the recommendation expresses *which OSLO suggests*. (This realizes the Recommendation System Spec §11b "alternative paths" concept as a first-class object.)

---

## 5. Clarification Candidate Types 〔proposal — taxonomy reconciliation〕

Types describe the **kind of resolution path** a candidate represents, aligned to the Finding taxonomy. *(Proposed; reconciliation with the Finding/Recommendation taxonomies required before canonical adoption — §13.)*

- **Clarification** — resolve an ambiguity by making meaning precise.
- **Definition** — resolve missing/undefined terms or targets.
- **Information Provision** — resolve missing information by supplying it.
- **Assumption Validation** — resolve an assumption by confirming/sourcing it.
- **Conflict Reconciliation** — resolve a conflict between elements.
- **Constraint Resolution** — resolve a limiting constraint affecting feasibility.
- **Dependency Resolution** — resolve a dependency affecting feasibility.
- **Coverage Improvement** — resolve a coverage gap by extending the plan/evidence.

These mirror the finding types they address; they introduce **no scoring** and **no ordering** (ordering/selection is out of scope, §14).

---

## 6. Clarification Candidate Lifecycle

States (active, non-governance — **no approval/disposition/decision semantics**):

| State | Meaning |
|---|---|
| **Identified** | OSLO surfaces a candidate resolution path for a finding |
| **Surfaced** | Presented to the user for consideration (a UI surfacing, not a status decision) |
| **Selected** | The user chooses to pursue this candidate (a user choice, **not** an approval) |
| **Dismissed** | The user sets this candidate aside (a user choice, not a rejection-with-authority) |
| **Acted Upon** | The user has acted in the direction of this candidate (action produces information change) |
| **Resolved** | The finding this candidate addressed was **weakened or removed** via reanalysis (success, measured downstream like recommendations) |
| **Superseded** | Replaced by a newer candidate; **retained**, never deleted |

**Transitions.** Identified → Surfaced → {Selected, Dismissed}; Selected → Acted Upon → Resolved; any active state → Superseded. **Append-only** — candidates are superseded (retained), never overwritten; a dismissed/superseded candidate is **not resurrected** (a new candidate may be identified). **Selected/Dismissed are user choices, never governance decisions; Resolved is a downstream reanalysis outcome, not an approval.**

---

## 7. Traceability

- Every Clarification Candidate **traces to ≥1 Finding** (it cannot exist unattributed; mirrors REC-1/RFC-1).
- A Clarification Candidate exposes, at all times: its **source finding(s)**, its **type**, its **rationale** (why it could resolve the finding, inherited from the finding context), its **current lifecycle state**, any **recommendation(s)** that advise pursuing it, and its **supersession history**.
- Coupling to finding state changes follows `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md`: when a source finding is superseded/closed/removed and the candidate traces only to it, the candidate is **superseded**; weakening alone does not supersede it; reopening yields a **new** candidate (no resurrection).
- A Clarification Candidate **must never become opaque** — its basis is always reconstructable.

---

## 8. User Interaction Boundary

- **The user may** consider, **select**, **dismiss**, or **defer** a Clarification Candidate, and **act** on a selected one. **Only the user acts.**
- **OSLO may** identify, surface, explain, and **advise** (via recommendations) among candidates. **OSLO never** selects, acts, approves, decides, validates, governs, or auto-applies a candidate.
- **No assessment change occurs from interaction itself.** Selecting, dismissing, or deferring a candidate changes **no** CAF/Reliability/Confidence signal; only the user's **action → information change → reanalysis** can (and only through reanalysis).
- This boundary is **human-in-the-loop**, identical in spirit to the Recommendation System's: OSLO proposes possibilities and advises; the user decides and acts.

---

## 9. How Clarification Candidates Feed Recommendations & Reanalysis

```text
Finding ─▶ Clarification Candidate(s) ─▶ Recommendation (advises pursuing a candidate)
                                       ─▶ User selects + acts on a candidate
                                              ─▶ Information Change ─▶ Reanalysis ─▶ Finding weakened/removed ─▶ CAF/Confidence may improve (via reanalysis only)
```

- **Feeds recommendations:** Clarification Candidates are the **option space** recommendations draw from; a recommendation **advises pursuing a specific candidate** (or is generated from one). Multiple candidates may underlie the alternative recommendations for one finding (§11b realized).
- **Feeds reanalysis (indirectly):** when the user **acts** on a selected candidate, the action produces **information change**, which the **existing event/reanalysis loop** turns into reanalysis (triggers are defined in the Event Model, **not here**). Reanalysis may weaken/remove the finding, after which CAF — and consequently Confidence — may improve **through reanalysis, never directly.**
- **Success** is measured downstream (finding weakened/removed), exactly as for recommendations (Recommendation System Spec §11). Identifying or selecting a candidate is **not** success.

---

## 10. Explicit Exclusions (Governance / Accepted Understanding)

The Clarification Candidate is **explicitly NOT** a governance object. It does **not** involve, and must not introduce:
- **Governance** — no review, approval, decision authority, or governance process.
- **Accepted Understanding** — no truth-promotion, ratification of understanding, or "accepted" state.
- **Resolution Candidate (governance), Disposition, Review Request** — no governance-object semantics; the Clarification Candidate is a distinct, active, non-governance object.
- **Agent Governance / Autonomous execution / Actuation** — no autonomous selection, action, or application.
- **Scoring / ranking / formulas / thresholds / probability** — candidates are enumerated possibilities, not scored or ordered here.

A Clarification Candidate **resolves nothing by itself** and **decides nothing**; it is a neutral possibility the **user** may act on. Anything resembling governance, approval, or truth-acceptance belongs to the deferred Governance Domain (Future Architecture — including the governance Resolution Candidate) and is **out of scope** for this active model.

---

## 11. Integrity Rules

*Structurally testable; each consistent with existing doctrine; none introduces governance.*

- **CC-1.** A Clarification Candidate must trace to **≥1 active Finding**, or be **superseded** (never unattributed, never deleted).
- **CC-2.** A Clarification Candidate is **not a governance object** — no approval/disposition/decision/accepted-understanding semantics.
- **CC-3.** A Clarification Candidate **never directly modifies CAF, Reliability, or Confidence** (only user action → reanalysis does).
- **CC-4.** A Clarification Candidate is **advisory-neutral and optional** — only the **user** selects/acts; OSLO never selects, acts, approves, or governs.
- **CC-5.** Clarification Candidates are **append-only** — superseded (retained), never overwritten or resurrected.
- **CC-6.** A Clarification Candidate must remain **explainable** (source findings, type, rationale, state, linked recommendations, supersession history); never opaque.
- **CC-7.** A Clarification Candidate is **distinct** from a Finding (descriptive) and a Recommendation (advisory): it is a **non-advisory possibility**.
- **CC-8.** Clarification Candidate behavior under finding state-change follows `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` (coupling, not governance).
- **CC-9.** No scoring, ranking, ordering, or selection among candidates is introduced (Deferred, §14).
- **CC-10.** A Clarification Candidate is **distinct from the Future-Architecture governance Resolution Candidate** and introduces none of its governance semantics (naming note).

---

## 12. Conformance Requirements

Structural (**no percentages, thresholds, or pass-rate language**) — a conforming implementation MUST:
- **C-1.** Persist ≥1 finding reference per candidate; supersede (never delete) a candidate that loses all active source findings (CC-1/CC-5).
- **C-2.** Provide only user-initiated selection/dismissal/deferral/action; expose no path by which OSLO selects, acts on, approves, or governs a candidate (CC-2/CC-4).
- **C-3.** Guarantee no candidate operation alters CAF/Reliability/Confidence (CC-3).
- **C-4.** Keep candidates explainable with full basis; no opaque candidate (CC-6).
- **C-5.** Link candidates to the recommendations that advise them and to the finding(s) they address (CC-7; §7/§9).
- **C-6.** Apply finding-coupling per the coupling spec (CC-8).
- **C-7.** Introduce no scoring/ranking/selection among candidates (CC-9).

Conformance is **all-or-nothing on these rules**; any governance/approval semantics, any direct assessment change, any autonomous action, or any opaque/unattributed candidate **fails conformance**.

---

## 13. Reconciliation Notes (proposal — owner ratification)

| ID | Item | Action |
|---|---|---|
| **CC-R1** | **New object introduction** — Clarification Candidate added to the active Release 1 object set | **Proposal** — on ratification, register in the active object inventory / `MODEL_LINEAGE_INDEX_V1.md` (Active Understanding/Improvement domain). **Not applied here.** |
| **CC-R2** | **Type taxonomy** (§5) | **Proposal** — reconcile with Finding/Recommendation taxonomies (cf. RS-R1) before canonical adoption. |
| **CC-R3** | **Multi-finding attribution** (§3/§7) | Depends on Data Model reconciliation (cf. RS-R5: `finding_id` → `finding_references`). **Proposal.** |
| **CC-R4** | **Naming distinctness** | Affirms Clarification Candidate (active) ≠ Resolution Candidate (Future/governance); no reclassification of, or change to, the governance Resolution Candidate. |

**Governance posture:** this document **introduces a new active object under a new name** and **does not** modify, reclassify, or supersede the governance Resolution Candidate or any other canonical artifact; it edits neither v1 models nor the Model Lineage Index, and awaits owner ratification for registration.

---

## 14. Deferred Items

Explicitly **Deferred** (out of scope for this active model):
- **Ranking / selection / scoring** among candidates (no ordering of resolution paths).
- **Mutual-exclusivity** modeling among candidates (default: coexist until the finding resolves — coupling spec §5).
- **Candidate generation heuristics** (how candidates are produced) — engine/calibration concern.
- **Effectiveness analytics** over candidate outcomes.
- **All Governance Domain capabilities** (review, disposition, governance, accepted understanding, truth promotion, governance Resolution Candidate) — Future Architecture, not here.

Future work must conform to this model and the layers above it, introducing no governance/scoring/automation/execution into Release 1.

---

*This document defines the Clarification Candidate — an active, non-governance Release 1 object: a neutral possibility for resolving a finding that feeds recommendations and (via user action → reanalysis) understanding improvement. It is distinct from Findings (descriptive), Recommendations (advisory), and the Future-Architecture governance Resolution Candidate. It introduces no governance/accepted-understanding/scoring/automation, modifies no canonical artifact, and awaits owner ratification for registration.*

**Clarification Candidate Model v1 complete.**
