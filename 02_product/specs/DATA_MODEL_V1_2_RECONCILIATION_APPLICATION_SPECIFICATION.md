# Data Model v1.2 Reconciliation Application Specification

**Type:** Implementation application specification (applies ratified decisions; not a review, not a new ratification)
**Status:** Proposed Release 1 · **Date:** 2026-05-31
**Applies (ratified only):** `RECOMMENDATION_RECONCILIATION_RATIFICATION_DECISION_001.md` · Recommendation System Spec v1 · Coupling Spec v1 · Finding System Spec v1 · Recommendation/Finding Presentation Specs v1 · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md` · Architecture Audit 001/002.
**Preserves (unmodified):** CAF Scoring v2 · Reliability v2 · Confidence v2 · Finding Model · Recommendation Model · State/Event Model semantics.

> **Authoritative delta.** This document is the canonical **Data Model v1.2** reconciliation delta (v1.2 = v1.1 + §B/§C) plus the State/Event/API application. It **applies only ratified decisions**: **RS-R3 (add `deferred`)** and **RS-R7 (add card fields)**. RS-R1/R2/R4 keep the ratified model; RS-R5/R6 are deferred. **No** new entity, behavior, doctrine, governance, execution, automation, scoring, or probability. **No Resolution Path / Clarification Candidate** entity/field/object/lifecycle/event/endpoint is added. **Resolution Candidate (Future Architecture) is not referenced or modified.** RS-R decisions are not reopened.

---

## A. Executive Summary

- **Purpose:** align Data Model, State Model, Event Model, and API with the ratified Recommendation architecture.
- **Scope:** **additive only** — one enum value (`deferred`) and five fields on the `Recommendation` entity; one new event; one new API command; payload field exposure. Nothing else changes.
- **Implementation impact:** **low / backward-compatible.** No entity is created; no Finding change; no CAF/Reliability/Confidence/behavior change; no Resolution Path artifacts.

---

## B. Data Model v1.2 Changes

### Change 1 — `Recommendation.status` += `deferred` (RS-R3)
- **Current (v1.1):** `status ∈ {generated, accepted, rejected, implemented, superseded}` (5).
- **New (v1.2):** `status ∈ {generated, accepted, rejected, deferred, implemented, superseded}` (6).
- **Rationale:** Ratification Decision 001 RS-R3 (Ratify) — doctrinally supported (Recommendation Model Position #12).

### Change 2 — Additive `Recommendation` fields (RS-R7)
- **Current (v1.1):** `recommendation_id, project_id, finding_id, first_seen_run_id, recommendation_type, status, rationale, expected_dimension, created_at, updated_at`.
- **New (v1.2):** add **`title`**, **`description`**, **`effort`** (`low|medium|high`), **`artifact_reference`** (nullable), **`artifact_element_reference`** (nullable).
- **Rationale:** Ratification Decision 001 RS-R7 (Ratify) — required for the recommendation card (Recommendation Presentation Spec §E); additive, no behavior change.

### Explicitly NOT changed (ratified rejections / deferrals)
- `recommendation_type` **unchanged** = `{improvement, validation, suggested_fix}` (RS-R1 Reject; 9 = presentation labels only).
- **No** `presented` status (RS-R2 Reject) and **no** `completed` status (RS-R4 — terminal stays `implemented`; "Completed" is a UI display synonym).
- `finding_id` **stays single** (RS-R5 Defer); **no** `finding_references`.
- `expected_dimension` **stays single** (RS-R6 Defer); **no** plural `affected_caf_dimensions`.
- **No** `resolution_paths[]`, `is_recommended`, `is_selected` (AMB-1 — paths are presentation-only).

**Verdict:** **Data Model v1.2 required** (additive: +1 enum value, +5 fields). v1.1 otherwise preserved.

---

## C. Recommendation Entity Specification (canonical, Release 1 / v1.2)

| Field | Type | Cardinality | Class |
|---|---|---|---|
| `recommendation_id` | UUID (PK) | 1 | inherited |
| `project_id` | UUID (FK) | 1 | inherited |
| `finding_id` | UUID (FK Finding) | **1 (single)** | inherited *(multi deferred, RS-R5)* |
| `first_seen_run_id` | UUID (FK AnalysisRun) | 1 | inherited |
| `recommendation_type` | enum(`improvement`,`validation`,`suggested_fix`) | 1 | inherited *(unchanged, RS-R1)* |
| `status` | enum(`generated`,`accepted`,`rejected`,`deferred`,`implemented`,`superseded`) | 1 | **modified** *(+`deferred`, RS-R3)* |
| `rationale` | text | 1 | inherited |
| `expected_dimension` | enum(`clarity`,`alignment`,`feasibility`) | **1 (single)**, nullable | inherited *(plural deferred, RS-R6)* |
| `title` | string | 1 | **new** *(RS-R7)* |
| `description` | text | 1 | **new** *(RS-R7)* |
| `effort` | enum(`low`,`medium`,`high`) | 1 | **new** *(RS-R7)* |
| `artifact_reference` | UUID (FK Artifact) | 0..1 | **new** *(RS-R7)* |
| `artifact_element_reference` | string/ref | 0..1 | **new** *(RS-R7)* |
| `supersedes_recommendation_id` | UUID (FK self) | 0..1 | inherited *(supersession chain)* |
| `created_at` / `updated_at` | timestamp | 1 | inherited |

- **Status model:** generated → accepted/rejected/deferred; accepted → implemented; any active → superseded (§E).
- **Attribution model:** **one Recommendation → one Finding** (`finding_id`), always present (REC-1). A Finding may have **many** Recommendations (inverse), surfaced as "Possible Resolution Paths" (presentation).
- **Distinctions:** *new* = title/description/effort/artifact refs; *modified* = status (+deferred); *inherited* = all others.

---

## D. Finding Entity Impact

**None.** No Finding entity change is required by the ratified decisions (RS-R5/R6 deferred keep the Recommendation single-finding/single-dimension, so the `Finding` entity is untouched). **Explicitly: the Finding entity is unchanged in v1.2.**

---

## E. State Model Application

**Recommendation lifecycle (v1.2):** `generated · accepted · rejected · deferred · implemented · superseded`.

- **Retained:** generated, accepted, rejected, implemented, superseded.
- **Newly ratified:** **`deferred`** (RS-R3).
- **Removed:** none (`presented`/`completed` were never ratified states).
- **Renamed:** none (terminal action = `implemented`; "Completed" is display only).
- **Transitions (additive):** `generated → {accepted, rejected, deferred}`; `deferred → {accepted, rejected}`; `accepted → implemented`; any active → `superseded`. Append-only supersession unchanged.
- **No new lifecycle behavior** — only the additive `deferred` state. Finding lifecycle unchanged.

---

## F. Event Model Application

- **Added (minimum):** **`recommendation_deferred`** — emitted when a user defers a recommendation; sets `status = deferred`.
- **Unaffected (existing):** `recommendation_created/accepted/rejected/implemented/superseded` and all finding/analysis/confidence events.
- **Not added:** no `recommendation_presented` event (surfacing is UI-only); **no Resolution Path events; no Clarification Candidate events; no new event category.**

---

## G. API Contract Impact

- **Recommendation payload:** expose new fields (`title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference`) and the `deferred` status value.
- **Endpoint addition:** **`POST /recommendations/{rid}:defer`** → `deferred`; emits `recommendation_deferred`.
- **Finding payload:** **no change** (Finding entity unchanged).
- **Removals:** none.
- **Not added:** **no Resolution Path endpoints/sub-resources; no Clarification Candidate endpoints.** API exposes **Recommendations only** (AMB-1).

---

## H. Presentation Layer Impact

**No changes required.** The presentation specs were authored anticipating these decisions:
- Recommendation Presentation Spec §G already accommodates **`deferred`** as a visible state; §E already uses **`title`/`description`/`effort`/type**; "Possible Resolution Paths" is already a presentation grouping of multiple Recommendations.
- Finding Presentation Spec is unaffected (Finding entity unchanged).
**Explicitly: no edits to either presentation spec are required by this application pass.**

---

## I. Migration Impact

*(No DB scripts, storage design, or implementation detail.)*
- **Backward compatibility:** **fully additive** — new fields are nullable/defaulted; `deferred` is a new enum value that does not affect existing recommendations; `implemented` retained.
- **Migration requirements:** none breaking. Existing recommendations remain valid; new fields default empty/null until populated.
- **Versioning:** **Data Model v1.2** is an additive successor to v1.1 (this delta governs); API changes are additive **within `/v1`** (no `/v2` needed). State/Event additions are additive.

---

## J. Final Canonical Release 1 Model

**Unchanged in structure** by this pass (additive only):
```text
Finding (descriptive)
  → Recommendation (advisory; +deferred state, +card fields)
     → User Action (only the user acts)
        → Information Change → Reanalysis → Finding weakened/removed → CAF/Confidence may improve (via reanalysis only)
```
A Finding may have **multiple Recommendations**, surfaced as **Possible Resolution Paths** (presentation). Assessment changes only via reanalysis. No structural change; only the additive Recommendation fields/state.

---

## K. Conformance Requirements

A conforming implementation MUST (objective, structurally testable, **non-numeric**):
- **DMA-1.** **No Resolution Path entity/field/object/lifecycle/event/endpoint exists** (no `resolution_paths[]`/`is_recommended`/`is_selected`).
- **DMA-2.** **No Clarification Candidate entity/event/endpoint exists.**
- **DMA-3.** **No Resolution Candidate / governance** concept is referenced or applied in the active model.
- **DMA-4.** `Recommendation.status` includes **`deferred`** and **excludes `presented` and `completed`** (terminal = `implemented`).
- **DMA-5.** `Recommendation.recommendation_type` is exactly `{improvement, validation, suggested_fix}`.
- **DMA-6.** `Recommendation.finding_id` is **single** and **always present** (attribution explainable); no `finding_references` array.
- **DMA-7.** `Recommendation.expected_dimension` is **single**; no plural dimension array.
- **DMA-8.** The new fields (`title`, `description`, `effort∈{low,medium,high}`, `artifact_reference`, `artifact_element_reference`) exist and are additive.
- **DMA-9.** A `recommendation_deferred` event exists; **no** `presented`/Resolution-Path/Clarification-Candidate events exist.
- **DMA-10.** API exposes **Recommendations only**; `:defer` exists; **no** Resolution Path/Clarification Candidate endpoints.
- **DMA-11.** Recommendation remains **advisory**; selection/deferral changes **no** CAF/Reliability/Confidence.
- **DMA-12.** The **Finding entity is unchanged**; no Finding behavior changed.

Conformance is **all-or-nothing**; any Resolution Path/Clarification Candidate/governance artifact, any non-ratified status, any multi-finding/multi-dimension field, or any assessment-behavior change **fails conformance**.

---

## Deliverables (summary)

1. **Data Model v1.2** — +`deferred` status; +`title`/`description`/`effort`/`artifact_reference`/`artifact_element_reference` (§B/§C).
2. **State Model** — +`deferred` state + transitions (§E).
3. **Event Model** — +`recommendation_deferred` (§F).
4. **API** — +fields/`deferred` in payloads; +`:defer` command (§G).
5. **Migration** — additive, backward-compatible; v1.2 successor; additive within `/v1` (§I).
6. **Conformance** — DMA-1…DMA-12 (§K).

---

## Final Validation Checklist

- No Resolution Path entity introduced — ✅
- No Clarification Candidate entity introduced — ✅
- No governance concepts introduced — ✅
- No execution concepts introduced — ✅
- No CAF behavior changed — ✅
- No Reliability behavior changed — ✅
- No Confidence behavior changed — ✅
- No Finding behavior changed — ✅
- No Recommendation behavior changed — ✅ (additive state/fields only; advisory unchanged)

---

*This application specification brings the canonical Release 1 stack into alignment with the ratified Recommendation decisions: Data Model v1.2 (additive `deferred` status + five card fields), the additive `deferred` state, the `recommendation_deferred` event, and additive API exposure. It introduces no entity, behavior, governance, execution, scoring, Resolution Path, or Clarification Candidate; leaves Findings and CAF/Reliability/Confidence untouched; and does not reopen RS-R or AMB-1. v1.2 = v1.1 + this delta.*

**Data Model v1.2 Reconciliation Application Specification complete.**
