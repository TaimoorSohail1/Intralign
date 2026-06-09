# Recommendation System Specification v1 — Governance Review

**Type:** Governance review (evaluate only — no rewrite, no new doctrine, no implementation detail)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Subject:** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md`
**Reviewed against:** Outcome Confidence Doctrine/Interpretation/Leadership/Calibration 001 · CAF Assessment · CAF Scoring v2 · Reliability v2 · Confidence v2 · Recommendation Model v1 · State Model · Data Model v1.1 · Confidence Subsystem Test Spec · Confidence Fixture Library.

> Evaluation only. No doctrine, implementation, execution, agents, automation, governance workflow, scoring, formulas, weighting, probability, or calibration arithmetic is introduced.

---

## A. Executive Assessment

**Ready with Minor Revisions.**

The specification is **doctrinally sound and well-bounded**: recommendations are advisory, human-in-the-loop, and influence CAF/Reliability/Confidence **only** through user action → reanalysis, with strong boundary rules. The one substantive issue is **incomplete Data Model reconciliation** — the spec adds recommendation **attributes and cardinalities** that diverge from the ratified Data Model v1.1 entity but are **not** captured in §13a. Adding those reconciliation items (and two small success/coupling clarifications) is **additive, not a redesign**.

---

## B. Findings

| # | Area | Finding | Disposition |
|---|---|---|---|
| F-1 | **Stack consistency** | Aligns with Recommendation Model (advisory; improves understanding via action), CAF/Confidence boundaries, and active-loop doctrine. No meaning drift in CAF/Reliability/Confidence; no hidden confidence-domain doctrine. | **Accept** |
| F-2 | **Boundary integrity** | REC-2/3/9/10 + C-5/6/7 robustly prevent direct CAF/Reliability/Confidence modification, actions, agents, and execution. | **Accept** |
| F-3 | **Type taxonomy** (9 vs ratified 3) | Correctly flagged (RS-R1) as proposal with a mapping; not silently adopted. | **Backlog** (RS-R1) |
| F-4 | **Lifecycle states** | Coherent; `Presented`/`Deferred`/`Completed` correctly flagged proposal (RS-R2/3/4). `Presented` is the weakest as a *persisted status* (it is a UI/notification concern per R-2). | **Accept with Modification** (keep Presented proposal-only; see C) |
| F-5 | **Data Model field reconciliation** | **Gap.** §4 introduces field/cardinality divergences from the ratified Data Model v1.1 `Recommendation` entity that §13a does **not** capture (see F-5a/b/c). | **Accept with Modification** → add RS-R5/R6/R7 |
| F-5a | finding cardinality | §1/§6/REC-1 allow **one-or-more** findings (`finding_references`), but Data Model v1.1 `Recommendation.finding_id` is **single**. | **Backlog** (new RS-R5) |
| F-5b | affected-dimension cardinality | §4 declares **affected CAF dimension(s)** (plural), but Data Model v1.1 `Recommendation.expected_dimension` is **single**. | **Backlog** (new RS-R6) |
| F-5c | new fields | §4 adds `title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference` — not in the ratified `Recommendation` entity. | **Backlog** (new RS-R7) |
| F-6 | **Success model (§11)** | Sound and doctrinally faithful, but has minor unstated cases: "acted-but-finding-not-weakened" (ineffective action) and "completed-but-no-information-change-→-no-reanalysis." | **Accept with Modification** (add a one-line acknowledgement; no model change) |
| F-7 | **Finding↔recommendation coupling** | **Gap.** The spec does not define what happens to a recommendation when its **source finding is superseded/closed/removed** — yet finding resolution is the success condition. | **Backlog** (required before Resolution Candidate; see D) |
| F-8 | **Alternative paths** | Recommendation Model Example C affirms **multiple valid recommendations per finding**; the spec models one-rec-to-many-findings but not many-recs-to-one-finding coexistence vs supersession. | **Backlog** (see D) |
| F-9 | **Explainability/traceability** | §9 + REC-5/8 + C-1/2 prevent opacity; attribution, rationale, finding traceability, supersession history all required. Sufficient. | **Accept** |
| F-10 | **Prioritization (§7)** | Conceptual ordering only; explicitly defers combination; no scoring/weighting/calibration leakage. The numbered 1–4 list slightly implies precedence but is framed as "considerations, not algorithm." | **Accept** |
| F-11 | **Testing readiness** | REC-1…12 + C-1…8 + explainability/supersession structure map cleanly to a future Recommendation Test Spec / Fixture family without redesign. | **Accept** |
| F-12 | **Reliability in §3 flow** | The flow diagram omits Reliability (shows CAF→Confidence); REC-3 covers it, but the diagram could note reanalysis also moves Reliability. Cosmetic. | **Accept** (optional note) |

---

## C. Reconciliation Review

| Item | Subject | Recommendation | Rationale |
|---|---|---|---|
| **RS-R1** | 9-type taxonomy vs ratified 3 | **Retain as Proposal** | Diverges from ratified `recommendation_type`; the 9 may be adopted as a finer taxonomy or kept as display sub-types — owner reconciliation, not unilateral. |
| **RS-R2** | `Presented` status | **Retain as Proposal** (lean: model as non-status UI event) | R-2 explicitly **removed** `presented` from the status enum as a UI concern; re-adding it as a persisted status reverses a ratified decision. Prefer modeling "presented" as a UI/notification event, not a lifecycle status. |
| **RS-R3** | `Deferred` status | **Ratify (advance)** | **Doctrinally supported** — Recommendation Model Position #12 explicitly lists "deferred" as a valid outcome. Low-risk additive status; the strongest candidate to ratify. |
| **RS-R4** | `Completed` vs `implemented` | **Retain as Proposal** (lean: keep `implemented`) | Pure naming reconciliation; recommend adopting the ratified `implemented` to avoid churn, with "Completed" as optional display, and folding the reanalysis-verified notion into the Success Model (§11) rather than a new state. |
| **RS-R5** *(new)* | finding cardinality single→multiple | **Retain as Proposal** | Requires a Data Model v1.1 change (`finding_id` → `finding_references`); genuine and currently unflagged. |
| **RS-R6** *(new)* | affected-dimension cardinality single→multiple | **Retain as Proposal** | `expected_dimension` (single) → `affected_caf_dimensions` (plural); reconcile with Data Model. |
| **RS-R7** *(new)* | new fields (title/description/effort/artifact refs) | **Retain as Proposal** | Additive `Recommendation` fields; ratify via Data Model reconciliation. |

**Net:** of the seven, **RS-R3 is recommended to advance to ratification**; the rest **retain as proposal** pending Data/Recommendation Model reconciliation. **None recommended for removal.** Three new items (RS-R5/6/7) are required to make §13a complete.

---

## D. Missing Areas (genuinely required before Resolution Candidate modeling begins)

1. **Finding↔recommendation lifecycle coupling (required).** Define what happens to a recommendation when its **source finding** is superseded, closed, reopened, or removed (e.g., does the recommendation auto-supersede when its sole source finding is resolved?). Because **finding resolution is the success condition** (§11) and Resolution Candidate modeling builds directly on finding/recommendation resolution, this coupling must be modeled first. *(Gap — F-7.)*

2. **Multiple recommendations per finding / alternative paths (required).** Recommendation Model Example C affirms multiple valid improvement paths for one finding. The spec must state how **co-existing recommendations for the same finding** relate (parallel valid options vs supersession) before Resolution Candidate (which selects among resolution paths). *(Gap — F-8.)*

3. **Reanalysis-trigger cross-reference (minor).** The success model depends on action → reanalysis; the **trigger** already exists in the Event Model (`recommendation_implemented`/evidence-change → deep analysis), but the spec should **cross-reference** it so the success loop is closed end-to-end. *(Not a redesign; a citation.)*

*No other gaps are deemed genuinely required before Resolution Candidate modeling. Scoring, ranking, automation, and effectiveness analytics remain correctly Deferred (§14) and are not prerequisites.*

---

## E. Ratification Recommendation

**Apply Revisions Then Ratify.**

The specification is fundamentally sound and well-bounded; it does **not** require significant revision. Before ratification, apply this **minor, additive** set (no redesign, no new doctrine):

1. **Complete §13a** with **RS-R5 (finding cardinality), RS-R6 (affected-dimension cardinality), RS-R7 (new fields)** so the Data Model reconciliation surface is fully disclosed.
2. **Advance RS-R3 (`Deferred`)** toward ratification (doctrinally supported); keep RS-R1/R2/R4 as proposals with the leanings in §C.
3. **Add a one-line acknowledgement** to §11 of the "acted-but-finding-unchanged" and "completed-without-information-change" cases (no model change).
4. **Add two backlog items** for the required gaps: **finding↔recommendation coupling** and **alternative-paths coexistence** (D-1, D-2), to be modeled before Resolution Candidate.
5. *(Optional)* note Reliability in the §3 flow; cross-reference the Event-Model reanalysis trigger.

With items 1–4 applied, the specification is **ratifiable** and provides a sufficient, testable foundation for a future Recommendation Test Specification and Recommendation Fixture Library without redesign.

---

*Governance review only. The subject document was not modified. Recommendations are for owner ratification under the governance lifecycle; RS-R5/R6/R7 and the D-gaps are proposed backlog additions, not applied here.*

**Recommendation System Specification v1 governance review complete.**
