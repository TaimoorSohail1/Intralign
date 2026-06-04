# Recommendation System Specification v1

**Type:** Implementation specification — the authoritative Release 1 recommendation behavior reference
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** Outcome Confidence Doctrine Decision 001 · Interpretation Doctrine 001 · Leadership Doctrine 001 · Calibration Decision 001 · CAF Assessment Model · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` · `CONFIDENCE_MODEL_V2.md` · **Recommendation Model v1** (founder positions).
**Consistent with:** Finding Model · Planning Intelligence · Analysis Engine · Data Model v1.1 · State/Event Models.
**Revision:** 2026-05-31 — additive reconciliation revision per `RECOMMENDATION_SYSTEM_SPECIFICATION_V1_GOVERNANCE_REVIEW.md`: completed §13a (added RS-R5/R6/R7; RS-R3 advanced toward ratification), clarified §11 success cases, added §11a (finding/recommendation coupling backlog) and §11b (alternative-paths backlog), and added the §3 reanalysis/Reliability cross-references. No doctrine, model behavior, lifecycle ratification, or Data Model change applied.
**Revision 2:** 2026-05-31 — founder decision: added **Resolution Paths** as a Recommendation **substructure** (§4 `resolution_paths[]`), realizing §11b without a standalone object. See `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md`. No new entity/lifecycle/events introduced; the retired `CLARIFICATION_CANDIDATE_MODEL_V1.md` is superseded by this approach.
**Revision 3:** 2026-05-31 — **AMB-1 reconciliation, Decision A ratified** (`RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md`): Resolution Paths **retired as a modeled substructure**; §4 now defines **Possible Resolution Paths as a UI presentation pattern over multiple Recommendations** (no `resolution_paths[]`/`is_recommended`/`is_selected` fields). §11b **resolved**. Supersedes Revision 2. No new object/lifecycle/event/API resource.

> **Non-negotiable.** The Recommendation System **does not** create doctrine, modify CAF/Reliability/Confidence, introduce governance decisions, execution agents, autonomous project modification, project-execution capability, probability, scoring formulas, or calibration arithmetic. **Release 1 is human-in-the-loop:** recommendations may **suggest** actions; **only users perform actions**; **CAF and Confidence change only through reanalysis after project information changes.** Where a numeric value would be required, this document states **"Deferred to future calibration."**
>
> **Reconciliation note (read first).** Recommendation Model v1 §8 deliberately **leaves the precise recommendation status vocabulary to a future owner-approved definition** — this document supplies it. Where this specification's **type taxonomy (§4)** or **lifecycle (§8)** extends or diverges from the **ratified** Data Model v1.1 `recommendation_type` / `Recommendation.status` enums (R-2) or State Model §11, those items are tagged **〔proposal — reconciliation required〕** and consolidated in §13a. They are **not** silently adopted as canonical.

---

## 1. Purpose

A **Recommendation** is:

> **A proposed action intended to improve one or more CAF dimensions by addressing the underlying cause of one or more findings.**

Recommendations exist to **help users improve project understanding**. They are the hinge between *understanding* (findings, CAF, reliability, confidence) and *action*: a recommendation suggests an improvement path, the **user acts**, the action produces new project information, reanalysis re-runs, and understanding may improve (Recommendation Model v1 §7). The recommendation itself improves nothing — **only user action does** (Recommendation Position #4/#9).

---

## 2. Scope

**In scope:** recommendation **generation, representation, lifecycle, prioritization, explainability, and supersession** for Release 1.

**Out of scope:** autonomous modification · project execution · agents · governance · probability · scoring formulas · confidence arithmetic. These are excluded by doctrine and are **Deferred** or owned elsewhere (§14).

---

## 3. Model Relationships

```text
Finding ─▶ Recommendation ─▶ User Action ─▶ (new project information) ─▶ Reanalysis ─▶ CAF Improvement ─▶ Confidence Improvement
```

- **Recommendations originate from findings** and propose a path to address a finding's underlying cause.
- **Recommendations influence CAF only through user action and reanalysis.** They **never directly modify CAF or Confidence** (Recommendation Position #9; CAF Scoring v2 CR-11; Confidence v2 IR-6).
- **The loop closes only when a user acts.** Acceptance, rejection, or deferral of a recommendation changes **no** assessment signal by itself; only the resulting **information change + reanalysis** can move CAF, and only a CAF/reliability change can move Confidence.
- **Reliability may also change during reanalysis** — if the user's action changes the observable evidence surface (coverage/evidence/assessability), reanalysis may move Reliability as well as CAF; this too occurs only through reanalysis, never directly from the recommendation.
- **Cross-reference (no triggers defined here).** Recommendation success depends on the **existing event/reanalysis loop**: *User Action → Information Change → Reanalysis* is handled by the **Event Model / reanalysis flow**. **This specification does not define event triggers** (they live in the Event Model).

---

## 4. Recommendation Representation

Required attributes:

**Identity**
- `recommendation_id` — stable unique identifier.
- `title` — short human-readable label.
- `description` — the proposed action.

**Source Attribution**
- `finding_references` — one or more finding IDs (mandatory; §6).
- `artifact_reference` — the artifact the action concerns (if applicable).
- `artifact_element_reference` — the specific element within the artifact (if applicable).

**CAF Attribution**
- `affected_caf_dimensions` — the CAF dimension(s) the action is expected to improve (Clarity / Alignment / Feasibility). **Declared, never computed against CAF.**

**Rationale**
- `rationale` — the explanation for why the recommendation was generated (inherited from its findings; §6).

**Expected Impact**
- `expected_impact` — **structural only** (e.g., "addresses the ambiguity underlying finding F; expected to improve Clarity"). **No indices, magnitudes, or values** — "Deferred to future calibration."

**Effort**
- `effort` — qualitative: **Low · Medium · High** (a user-facing estimate of action cost; not a score).

**Recommendation Type** 〔proposal — finer taxonomy; reconciliation with Data Model v1.1 `recommendation_type` (improvement / validation / suggested_fix) required, §13a〕
- Clarification · Definition · Validation · Alignment · Constraint Resolution · Dependency Resolution · Assumption Resolution · Conflict Resolution · Coverage Improvement.

*These nine types refine the ratified three (improvement / validation / suggested_fix): e.g., Validation maps to `validation`; Clarification/Definition/Alignment/Coverage Improvement refine `improvement`; the Resolution types refine `suggested_fix`/`improvement`. Adoption as canonical requires Recommendation/Data Model reconciliation (§13a).*

**Possible Resolution Paths (UI presentation pattern — NOT a modeled construct)** 〔AMB-1 reconciliation, **Decision A ratified** 2026-05-31 — see `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md`〕
- **Possible Resolution Paths are a user-facing presentation/view over the multiple Recommendations associated with the same Finding** — **not** a Recommendation substructure and **not** a domain object. There is **no** modeled `resolution_paths[]`, `is_recommended`, or `is_selected` field. *(The prior `resolution_paths[]` substructure and `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` are retired.)*
- **Canonical model:** a Finding may have **multiple Recommendations** (A, B, C), each an alternative advisory way to address it (Finding System Spec §F; Coupling Spec §5; §11b). The **Recommendation remains the sole advisory object** and owns rationale, finding attribution, affected CAF dimensions, expected impact, explainability, lifecycle, supersession, and prioritization.
- **UI presentation states (derived, not persisted):**
  - **"Possible Resolution Paths"** — the UI grouping of the multiple Recommendations for a Finding.
  - **"OSLO Recommended"** — the UI label for the Recommendation OSLO presents as primary (derived from prioritization, §7).
  - **"Selected Path"** — the UI label for the Recommendation the user has selected/accepted (derived from the Recommendation lifecycle, §8).
- These presentation states introduce **no** Data Model entity/field, State lifecycle, Event, or API resource; the **API exposes Recommendations only**. Selecting among them is the user accepting a Recommendation; **selection alone changes no CAF/Reliability/Confidence** — only user action → information change → reanalysis can.

---

## 5. Recommendation Semantics

- **Recommendations identify improvement opportunities** — a path to address the cause of one or more findings.
- **Recommendations do not represent commands** — they suggest; they do not direct.
- **Recommendations do not represent certainty** — they are not predictions or guarantees of improvement.
- **Recommendations are advisory** — they may be accepted, rejected, deferred, or ignored, and **these outcomes do not invalidate the recommendation** (Recommendation Position #11/#12). The **user retains authority over action**.

---

## 6. Recommendation Generation Model

- **Recommendations originate from findings.** Every recommendation **must trace to one or more findings** (REC-1).
- **Recommendations inherit rationale from findings** — the recommendation's `rationale` derives from the finding(s) and their Impact Assessment context (consumed, not recomputed).
- **Recommendations are generated after findings exist** — a finding is the precondition for the recommendation that addresses it.
- **No recommendation may exist without finding attribution** — an unattributed recommendation is non-conformant (§12, §13).

Recommendations consume assessment context (findings, CAF, reliability, confidence) — they **create none of it** (Recommendation Model v1 §13).

---

## 7. Recommendation Prioritization Model

Structural prioritization only — **no formulas, scoring, weighting, or thresholds**; **conceptual ordering** of factors, with the resolved order **Deferred to future calibration**:

1. **CAF impact** — the extent to which the action is expected to improve the integrity of understanding (the primary factor; OSLO prioritizes understanding).
2. **Dependency influence** — whether addressing this finding/cause unblocks or affects others.
3. **Confidence influence** — the anticipated downstream effect on Outcome Confidence (via CAF, never directly).
4. **User effort** — the qualitative cost of acting (Low/Medium/High).

This is a **conceptual ordering of considerations**, not a ranking algorithm. How these factors combine into a presented order is **Deferred to future calibration** (and may never introduce probability or scoring arithmetic).

---

## 8. Recommendation Lifecycle

**States:** Generated · Presented · Accepted · Rejected · Deferred · Completed · Superseded.

| State | Meaning | Canonical alignment |
|---|---|---|
| **Generated** | Produced from finding(s); initial state | = ratified `generated` |
| **Presented** | Surfaced to the user | 〔proposal — `presented` was removed from `Recommendation.status` in Data Model v1.1 R-2 as a UI concern; reconciliation required, §13a〕 |
| **Accepted** | User accepts the recommendation | = ratified `accepted` |
| **Rejected** | User rejects it | = ratified `rejected` |
| **Deferred** | User postpones; remains valid | 〔proposal — doctrinally supported (Recommendation Position #12) but absent from the ratified status enum; reconciliation required, §13a〕 |
| **Completed** | The proposed action was carried out by the user | ≈ ratified `implemented` 〔naming reconciliation, §13a〕 |
| **Superseded** | Replaced by a newer recommendation; **retained** | = ratified `superseded` |

**Transitions.** Generated → Presented → {Accepted, Rejected, Deferred}; Accepted → Completed; Deferred → {Presented, Accepted, Rejected}; any active state → Superseded. **Recommendations are append-only — no overwriting.** A change of state sets a new state and retains prior state; a replacement supersedes (retained), never deletes.

*Note: **Completed is not "success"** (see §11) — it records that the action was taken, not that understanding improved.*

---

## 9. Recommendation Explainability Model

Every recommendation MUST expose:
- **source findings** (the finding references it traces to);
- **affected CAF dimensions** (declared);
- **rationale** (inherited from findings);
- **expected impact** (structural);
- **current state** (lifecycle state, §8);
- **supersession history** (the chain it belongs to).

**Recommendations must never become opaque** — a recommendation lacking any required component is non-conformant (§12). Explanation reduces to **basis** (findings + rationale + affected dimensions), never to a number.

---

## 10. Recommendation History Model

- **Current recommendation** — the active recommendation in effect now.
- **Superseded recommendation** — a prior recommendation replaced by a newer one; **retained**, never deleted.
- **Historical recommendation** — any recommendation in the supersession chain.

Behavior is **append-only**: recommendations are superseded, not overwritten; the chain **must be reconstructable** (supporting replay/audit). This mirrors the subsystem-wide supersession discipline (Confidence v2 §10; CAF Scoring v2 §11).

---

## 11. Recommendation Success Model

A recommendation is **successful** only when:

```text
User Action ─▶ Information Change ─▶ Reanalysis ─▶ Finding weakened or removed
```

- **Acceptance alone is not success.** Accepting a recommendation does not, by itself, improve understanding.
- **Completed/Implemented alone is not success.** Marking the action done does not, by itself, improve understanding.
- **Acted but no information change → not yet successful.** If the user acts but **no project information changes**, reanalysis may not occur, and the recommendation is **not yet successful**.
- **Acted and reanalyzed but finding unchanged → acted upon but not effective.** If the user acts and reanalysis occurs but the **source finding is not weakened or removed**, the recommendation was **acted upon but not effective**.
- **Success is measured downstream** — by whether, after the user acts and reanalysis re-runs, the originating finding(s) are **weakened or removed** (and, consequently, the affected CAF dimension(s) may strengthen and Confidence may rise — through reanalysis, never directly).

*(These are clarifications of the single success condition above — **no new lifecycle states** and **no effectiveness analytics** are introduced; effectiveness measurement remains Deferred, §14.)*

This preserves the doctrine that **only action and evidence change assessment**: the recommendation is the hinge; the **action** is what re-enters the loop as evidence.

---

## 11a. Finding / Recommendation Coupling Backlog

**Required future modeling item — to be modeled before Resolution Candidate modeling proceeds.** *(Recorded, not resolved here.)*

The system must define what happens to a recommendation when its **source finding** is:
- **superseded**
- **closed**
- **reopened**
- **removed**
- **weakened**

This specification **does not resolve** the resulting recommendation behavior (e.g., whether a recommendation auto-supersedes when its sole source finding is resolved). It only **records the modeling requirement**, because finding resolution is the recommendation's success condition (§11) and Resolution Candidate modeling builds directly on finding/recommendation resolution.

---

## 11b. Alternative Recommendation Paths — RESOLVED (AMB-1, Decision A)

〔**Resolved 2026-05-31** by `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md`.〕 **Multiple valid ways to address one Finding are modeled as multiple Recommendations** (Finding System Spec §F; Coupling Spec §5). The UI may group them as **"Possible Resolution Paths"** (§4), a presentation pattern — **not** a separate object. Coexistence/supersession of the alternatives follows the Coupling Spec §5 (parallel options; resolving the finding supersedes the remaining open alternatives) and the existing Recommendation lifecycle/supersession. The questions previously recorded here are answered by that model: multiple recommendations are **parallel valid options**; they are **not mutually exclusive by default**; one supersedes another via the normal supersession rules; and a user **may accept one while leaving others open**.

This specification **does not resolve** these; it only **records the modeling requirement**.

---

## 12. Recommendation Integrity Rules

*Formal, structurally testable. Each realizes existing doctrine; none is new doctrine.*

- **REC-1.** Every recommendation **traces to at least one finding**.
- **REC-2.** Recommendations **never directly modify CAF**.
- **REC-3.** Recommendations **never directly modify Confidence** (or Reliability).
- **REC-4.** **Affected CAF dimensions must be declared** on every recommendation.
- **REC-5.** Recommendations **must be explainable** (§9) — no opaque recommendation.
- **REC-6.** Recommendations **may be superseded but never overwritten**; superseded recommendations are retained.
- **REC-7.** Recommendations are **advisory** — accept/reject/defer/ignore are user choices and do not invalidate the recommendation.
- **REC-8.** Recommendations **must remain attributable to findings** throughout their lifecycle.
- **REC-9.** Recommendations **suggest actions only**; **only users perform actions** (no autonomous modification or execution).
- **REC-10.** A recommendation's influence on assessment is **only** via user action → information change → reanalysis (never a direct signal change).
- **REC-11.** Recommendation **state changes are append-only** (no in-place mutation of a prior state).
- **REC-12.** **Completed ≠ success** — success is determined by reanalysis outcome (§11), not by lifecycle state.

---

## 13. Conformance Requirements

Structural (**no percentages, no thresholds, no pass-rate language**) — a conforming implementation MUST:

- **C-1 (traceability).** Persist ≥1 finding reference on every recommendation; reject unattributed recommendations (REC-1/REC-8).
- **C-2 (explainability).** Surface all required explanation components without recomputation (REC-5); no opaque recommendation exists.
- **C-3 (lifecycle integrity).** Permit only the §8 transitions; apply state changes append-only (REC-11).
- **C-4 (supersession integrity).** Supersede (never overwrite) and retain prior recommendations; reconstruct the chain (REC-6).
- **C-5 (CAF boundary).** Guarantee no recommendation operation alters a CAF dimension (REC-2); CAF changes only via reanalysis.
- **C-6 (Confidence boundary).** Guarantee no recommendation operation alters Confidence or Reliability (REC-3).
- **C-7 (human-in-the-loop).** Provide no path by which a recommendation performs an action; actions are user-initiated only (REC-9/REC-10).
- **C-8 (declared dimensions).** Require declared affected CAF dimensions on every recommendation (REC-4).

Conformance is **all-or-nothing on these rules**; any direct CAF/Confidence modification, any opaque or unattributed recommendation, or any autonomous action **fails conformance**.

### 13a. Reconciliation Notes (backlog — owner ratification required)

The following extend or diverge from **ratified** enums and are recorded as **proposals**, not silently adopted:

| ID | Item | Divergence | Action |
|---|---|---|---|
| **RS-R1** | **Recommendation type taxonomy** (9 types, §4) | Ratified Data Model v1.1 `recommendation_type` = {improvement, validation, suggested_fix} (3) | Propose adopting the 9 as a finer taxonomy (mapped under the 3) **or** retaining the 3 with the 9 as display sub-types — reconcile in Recommendation/Data Model |
| **RS-R2** | **`Presented` lifecycle state** (§8) | Data Model v1.1 **R-2 removed** `presented` from `Recommendation.status` as a UI concern | Propose either re-adding `presented` as a status **or** modeling "presented" as a non-status UI/notification event — reconcile with State Model §11 / Data Model v1.1 |
| **RS-R3** | **`Deferred` lifecycle state** (§8) | Doctrinally supported (Recommendation Position #12) but **absent** from ratified `Recommendation.status` | **Advance toward ratification** (doctrinally supported, low-risk additive status) — add `deferred` to the status enum via State Model §11 / Data Model v1.1 reconciliation |
| **RS-R4** | **`Completed` vs `implemented`** (§8) | Ratified terminal action state is `implemented` | Naming reconciliation: adopt one canonical term (note Success Model §11 adds the reanalysis-verified notion the pre-R-2 `verified` once carried) |
| **RS-R5** | **Finding cardinality** (§1/§4/§6) | Spec permits **one-or-more** `finding_references`; ratified Data Model v1.1 `Recommendation.finding_id` is **single** | Record as proposal requiring Data Model reconciliation (`finding_id` → `finding_references`). **Do not resolve here.** |
| **RS-R6** | **Affected-dimension cardinality** (§4) | Spec permits **multiple** `affected_caf_dimensions`; ratified Data Model v1.1 `Recommendation.expected_dimension` is **single** | Record as proposal requiring Data Model reconciliation (`expected_dimension` → `affected_caf_dimensions`). **Do not resolve here.** |
| **RS-R7** | **New recommendation fields** (§4) | Spec introduces `title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference`; ratified Data Model v1.1 `Recommendation` does not currently include all of these | Record as proposal requiring Data Model reconciliation (additive fields). **Do not resolve here.** |

**Ratification posture (per governance review):** **RS-R3** is **advanced toward ratification**; **RS-R1, RS-R2, RS-R4, RS-R5, RS-R6, RS-R7 remain proposals** pending owner / Data Model reconciliation. *Recommendation Model v1 §8 left the precise status vocabulary to a future owner-approved definition; this section routes the differences for that ratification rather than overriding the State/Data models unilaterally.*

---

## 14. Deferred Items

Explicitly **Deferred to future calibration / future releases** (Release 1 does **not** define them):
- **Recommendation scoring** — any numeric score for a recommendation.
- **Recommendation ranking formulas** — the arithmetic realizing the §7 conceptual ordering.
- **Recommendation effort calculation** — any computed effort value (Low/Medium/High remains qualitative).
- **Recommendation automation** — any autonomous generation/application behavior (excluded in R1 by doctrine).
- **Recommendation effectiveness analytics** — measurement of recommendation success rates over time.

Future releases may define these; **Release 1 does not.** Any future definition must conform to this specification and the doctrine/model layers above it, and may not grant recommendations the ability to alter CAF/Confidence directly or to act autonomously.

---

*This document specifies Release 1 recommendation behavior as an implementation reference. It creates no doctrine, modifies no CAF/Reliability/Confidence meaning, introduces no governance, agents, autonomous modification, probability, scoring, or calibration arithmetic, and defers all numeric/automation concerns. Divergences from ratified enums are flagged as reconciliation proposals (§13a), not adopted unilaterally. Recommendations remain advisory; only users act; assessment changes only through reanalysis.*

**Recommendation System Specification v1 complete.**
