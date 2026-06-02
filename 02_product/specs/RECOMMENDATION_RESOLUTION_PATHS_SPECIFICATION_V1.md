# Recommendation Resolution Paths Specification v1 — RETIRED

> ## ⛔ RETIRED — AMB-1 reconciliation, Decision A ratified (2026-05-31)
> **Resolution Paths are NOT a modeled construct.** Per `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md` (Option A), "Possible Resolution Paths" are a **UI presentation pattern over multiple Recommendations associated with the same Finding**, not an embedded Recommendation substructure and not a domain object.
> - **Do not implement** `resolution_paths[]`, `is_recommended`, or `is_selected` as modeled fields.
> - **Canonical model:** `Finding → Recommendation A · B · C` (multiple Recommendations per Finding). See `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` §4 (UI presentation pattern) and §11b (resolved).
> - **User-facing terminology preserved** as derived UI states: **Possible Resolution Paths · OSLO Recommended · Selected Path.**
> - Retained for history only; the content below no longer governs implementation. Future-Architecture Resolution Candidate remains untouched.

**Type:** Implementation specification — **RETIRED** (was: Resolution Paths as an embedded Recommendation substructure)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · Recommendation Model v1 · Finding Model · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` · CAF Scoring v2 · Reliability v2 · Confidence v2 · State/Data/Event Models.
**Supersedes (as implementation direction):** `CLARIFICATION_CANDIDATE_MODEL_V1.md` (retired) · `CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md` (superseded).

> **Founder decision (2026-05-31).** Release 1 supports the UX of showing **multiple possible paths under a recommendation**, modeled as **`Recommendation → resolution_paths[]`** — **not** as `Finding → ClarificationCandidate → Recommendation`. Resolution Paths are an **embedded substructure of a Recommendation**, keeping Tier 1 / Tier 2 simpler.
>
> **This spec creates NO standalone domain object.** No ClarificationCandidate entity, lifecycle, events, top-level endpoints, UI object pages, fixture category, or governance model. **No new Data Model entity, no new State Model lifecycle, no new Event Model events.** The Future-Architecture `RESOLUTION_CANDIDATE_MODEL_V1.md` (governance) is **untouched and not reclassified.** Release 1 remains **human-in-the-loop**; nothing here modifies CAF/Reliability/Confidence directly.

---

## 1. Purpose

Define **Resolution Paths**: the advisory **options embedded within a Recommendation** that present the user with multiple possible ways to act on that recommendation. A recommendation may offer several paths; OSLO may mark one as recommended; the user may select any (including a non-recommended one). Resolution Paths exist to support the "possible paths" UX **without** introducing a standalone object.

---

## 2. What a Resolution Path Is

> **A Resolution Path is an advisory option, embedded in a Recommendation, for how the user might act on that recommendation.**

- **Substructure, not object.** A Resolution Path has **no independent identity, lifecycle, events, or endpoints**; it lives **inside** its Recommendation and shares the Recommendation's lifecycle (§8 of the Recommendation System Spec) and its supersession/history.
- **Advisory option, not a command.** It proposes a way to act; it neither commands nor decides.
- **Multiple per recommendation.** A Recommendation may contain **several** Resolution Paths (the possible ways to act on it).
- **Non-governance, non-assessment.** A Resolution Path is **not** a governance object and **not** an assessment object; it changes **no** CAF/Reliability/Confidence signal.

---

## 3. Structure (embedded in Recommendation)

`Recommendation.resolution_paths[]` — an ordered list; each element:

| Field | Meaning |
|---|---|
| `path_id` | identifier, **scoped within the recommendation** (not a global entity id) |
| `label` | the path's own user-facing name (the collection is surfaced to users as **"Possible Resolution Paths"**) |
| `description` | what the path entails |
| `rationale` | why this path could address the recommendation's finding(s) |
| `related_findings` | the finding(s) it addresses (a subset of the recommendation's `finding_references`) |
| `affected_caf_dimensions` | the CAF dimension(s) it is expected to improve (declared, never computed) |
| `is_recommended` | OSLO may mark **one** path per recommendation as recommended (advisory) |
| `is_selected` | the user may select **any** path (incl. non-recommended); may differ from `is_recommended` |

Constraints: **at most one** path per recommendation has `is_recommended = true`; `is_selected` is the user's choice and **independent** of `is_recommended`; a recommendation may have **zero or more** paths (zero = a single implicit action).

---

## 4. Recommended vs Selected Path

- **OSLO's recommended path** (`is_recommended`) is **advice** — OSLO's suggested way to act, surfaced visibly. It is **not** a decision, approval, or command.
- **The user's selected path** (`is_selected`) is the user's choice; the user **may select a different path** than OSLO's recommended one. **Recommended path ≠ selected path.**
- **Neither marking changes assessment.** Marking recommended (OSLO) or selecting (user) changes **no** CAF/Reliability/Confidence. **Only the user's action → information change → reanalysis** can move assessment (Recommendation System Spec §11).

**Canonical user-facing labels (terminology normalization).** Internal identifiers are unchanged; their **user-facing labels** are:

| Internal identifier | User-facing label |
|---|---|
| `resolution_paths[]` (collection) | **Possible Resolution Paths** |
| `is_recommended` | **OSLO Recommended** |
| `is_selected` | **Selected Path** |

These are the **only** approved user-facing labels; variants ("Resolution Path/Paths", "Recommended Path", "Suggested Path", "Selected Resolution Path", "Active Path", "Chosen Path") are not used in user-facing surfaces.

---

## 5. Lifecycle (reuses Recommendation lifecycle — no new states)

Resolution Paths have **no lifecycle of their own**. They are carried by the Recommendation and follow the **existing Recommendation lifecycle** (Generated · Presented · Accepted · Rejected · Deferred · Completed · Superseded; Recommendation System Spec §8):
- Selecting a path is a user interaction with the recommendation (it may inform the recommendation's progression, e.g., toward Accepted/Completed) — it introduces **no path-level state machine**.
- When the recommendation is **superseded** (e.g., via finding coupling, `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md`), its embedded paths are superseded **with it** (retained in the recommendation's history; append-only).
- No path is independently created, retired, or resurrected; paths exist only as the recommendation's content at each version.

---

## 6. Explainability & Traceability

- Each Resolution Path is **explainable**: `label`, `description`, `rationale`, `related_findings`, `affected_caf_dimensions`, and its `is_recommended`/`is_selected` flags are all available as part of the recommendation's explanation (Recommendation System Spec §9).
- Paths trace to the recommendation's findings (a path's `related_findings` ⊆ the recommendation's `finding_references`).
- No opaque path: a recommendation's paths are always reconstructable from the recommendation.

---

## 7. Boundaries (explicit exclusions)

This spec **does not** create, and Release 1 **must not** introduce:
- a **ClarificationCandidate** (or Resolution Path) **entity, lifecycle, events, API endpoints, UI object pages, fixture category, or governance model**;
- any **Governance, Accepted Understanding, Disposition, Review Request, Resolution Candidate (governance)** semantics;
- any **autonomous selection/action**, scoring/ranking among paths, formulas, thresholds, weighting, or probability;
- any **direct CAF/Reliability/Confidence modification**.
The **Future-Architecture Resolution Candidate** and all Governance Domain models remain **untouched**.

---

## 8. Cross-Document Implementation Direction (recommendation-scoped only)

- **Data Model:** **No new entity.** If persistence is needed, add `resolution_paths` as an **additive field on the `Recommendation` entity only** (an embedded list with the §3 fields). No `ClarificationCandidate` table.
- **State Model:** **No new lifecycle.** Use the **existing Recommendation lifecycle** only.
- **Event Model:** **No new ClarificationCandidate events.** If events are needed, they are **recommendation-scoped** only — e.g., a `recommendation_updated`/recommendation-scoped "path selected" carried within the recommendation's existing events — **not** standalone candidate events.
- **API:** Expose Resolution Paths **through the Recommendation payload** or **recommendation-scoped sub-resources** (e.g., `GET /recommendations/{rid}` includes `resolution_paths[]`; `POST /recommendations/{rid}/resolution-paths/{path_id}:select` for user selection). **Do NOT create top-level Resolution Path endpoints** unless later ratified.
- **UI:** Show **"Possible Resolution Paths"** under a recommendation; visually mark the **"OSLO Recommended"** path; **allow the user to select a different path** (the chosen one shown as **"Selected Path"**). No standalone object page.
- **Testing/Fixtures:** Add tests for multiple paths, recommended path, selected = recommended, alternate (non-recommended) selection, no-assessment-change on selection, and supersession-with-recommendation — as **recommendation tests/fixtures**, **not** a new ClarificationCandidate fixture category.

---

## 9. Integrity Rules

- **RP-1.** A Resolution Path exists **only** inside a Recommendation; it has no standalone identity, lifecycle, events, or endpoints.
- **RP-2.** A Recommendation may contain **multiple** Resolution Paths; **at most one** is `is_recommended`.
- **RP-3.** The user may select **any** path; `is_selected` is independent of `is_recommended` (**recommended ≠ selected**).
- **RP-4.** Marking/selecting a path changes **no** CAF/Reliability/Confidence; only user action → reanalysis does.
- **RP-5.** Resolution Paths are **advisory options, not commands**; only the user acts.
- **RP-6.** Resolution Paths reuse the **Recommendation lifecycle**; they introduce **no new state machine**.
- **RP-7.** Each path is **explainable** and traces to the recommendation's finding(s).
- **RP-8.** No governance/Accepted-Understanding/Resolution-Candidate semantics; Future Architecture untouched.

---

## 10. Conformance Requirements

Structural (**no percentages/thresholds/pass-rate language**) — a conforming implementation MUST:
- **C-1.** Model Resolution Paths as an **embedded list on the Recommendation**, with the §3 fields; persist no standalone candidate entity (RP-1).
- **C-2.** Enforce **at most one** `is_recommended` path per recommendation; allow the user to set `is_selected` on **any** path independently (RP-2/RP-3).
- **C-3.** Guarantee selection/recommendation marking alters **no** CAF/Reliability/Confidence (RP-4).
- **C-4.** Provide only **user-initiated** path selection; expose no OSLO-acts/auto-select path (RP-5).
- **C-5.** Surface paths via **recommendation payloads / recommendation-scoped endpoints** only — **no** top-level Resolution Path endpoints (§8).
- **C-6.** Keep paths explainable and finding-traceable; supersede paths with their recommendation (RP-6/RP-7).
- **C-7.** Introduce no governance/scoring/automation/new-object (RP-8).

---

## 11. Deferred Items

- **Ranking/scoring/selection-arithmetic** among paths — Deferred.
- **Path persistence specifics** (exact storage shape on Recommendation) — additive Data Model field, owner-ratified.
- **Recommendation-scoped event shape** for "path selected" — to be defined within the existing Event Model, recommendation-scoped, not as candidate events.
- **All Governance Domain capabilities** — Future Architecture, out of scope.

---

*This specification defines Resolution Paths as an advisory, embedded **substructure of a Recommendation** (`Recommendation → resolution_paths[]`), realizing the multiple-paths UX without any standalone object, lifecycle, events, endpoints, fixtures, or governance. It introduces no new domain object, no new lifecycle, and no new events; touches no Governance/Future-Architecture model; keeps Release 1 human-in-the-loop; and modifies no CAF/Reliability/Confidence behavior. It supersedes the retired Clarification Candidate model and its integration spec as the implementation direction.*

**Recommendation Resolution Paths Specification v1 complete.**
