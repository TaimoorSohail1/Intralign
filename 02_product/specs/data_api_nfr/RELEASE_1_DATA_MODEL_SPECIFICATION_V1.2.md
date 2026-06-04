# Release 1 Data Model Specification v1.2

**Type:** Implementation artifact — the authoritative Release 1 persistence data model (Recommendation reconciliation applied)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Supersedes:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` (v1.1 retained; this is the additive successor)
**Applies:** `RECOMMENDATION_RECONCILIATION_RATIFICATION_DECISION_001.md` (RS-R3, RS-R7) via `DATA_MODEL_V1_2_RECONCILIATION_APPLICATION_SPECIFICATION.md`.

> **v1.2 = v1.1 + this delta (additive only).** The **only** change from v1.1 is to the **`Recommendation` entity** (§12): add the `deferred` status value (RS-R3) and five card fields (RS-R7). **All other sections of v1.1 are inherited unchanged** (Workspace, User, Project, Artifact, Evidence, ContextItem, AnalysisRun, CAFState, ConfidenceState, Finding, Notification, Collaboration, Report, isolation, versioning, traceability, ERD, open questions). **No new entity** is introduced; the **Finding entity is unchanged**.
>
> **Explicitly NOT changed** (ratified rejections/deferrals): `recommendation_type` stays 3 values (RS-R1); **no** `presented`/`completed` status (RS-R2/RS-R4 — terminal stays `implemented`); `finding_id` stays **single** (RS-R5 deferred); `expected_dimension` stays **single** (RS-R6 deferred). **No** `resolution_paths[]`/`is_recommended`/`is_selected` (AMB-1). Future-Architecture Resolution Candidate untouched.

---

## Delta from v1.1 (summary)

| Change | v1.1 | v1.2 | Decision |
|---|---|---|---|
| `Recommendation.status` | `{generated, accepted, rejected, implemented, superseded}` | `{generated, accepted, rejected, **deferred**, implemented, superseded}` | RS-R3 (Ratify) |
| `Recommendation` fields | (no title/description/effort/artifact refs) | **+`title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference`** | RS-R7 (Ratify) |
| Everything else | — | **unchanged** | RS-R1/R2/R4 keep ratified; RS-R5/R6 deferred |

---

## 12. Recommendation Model 〔v1.2 — RS-R3 + RS-R7 applied〕

Persistence representation only — aligned with the Recommendation Model and `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md`. Suggested fixes are a recommendation type. **v1.2:** `status` += `deferred`; five additive card fields added.

| Field | Type | Class | Notes |
|---|---|---|---|
| `recommendation_id` | UUID (PK) | inherited | |
| `project_id` | UUID (FK) | inherited | tenant scope |
| `finding_id` | UUID (FK Finding) | inherited | operates on **one** Finding (single; multi-finding **deferred**, RS-R5) |
| `first_seen_run_id` | UUID (FK AnalysisRun) | inherited | run that produced it (**deep ⇒ Expanded Recommendation**) |
| `recommendation_type` | enum(`improvement`,`validation`,`suggested_fix`) | inherited | **unchanged** (RS-R1); finer 9-type names are **presentation labels only**, not persisted |
| `status` | enum(`generated`,`accepted`,`rejected`,**`deferred`**,`implemented`,`superseded`) | **modified** | **+`deferred`** (RS-R3). No `presented`/`completed` (RS-R2/RS-R4) |
| `title` | string | **new** | short card label (RS-R7) |
| `description` | text | **new** | the proposed action (RS-R7) |
| `rationale` | text | inherited | the explanation/basis (why) |
| `expected_dimension` | enum(`clarity`,`alignment`,`feasibility`, nullable) | inherited | **single** dimension (plural **deferred**, RS-R6) |
| `effort` | enum(`low`,`medium`,`high`) | **new** | qualitative effort estimate (RS-R7) |
| `artifact_reference` | UUID (FK Artifact, nullable) | **new** | artifact the action concerns (RS-R7) |
| `artifact_element_reference` | string/ref (nullable) | **new** | element within the artifact (RS-R7) |
| `supersedes_recommendation_id` | UUID (FK self, nullable) | inherited | supersession chain (append-only) |
| `created_at` / `updated_at` | timestamp | inherited | |

**Status model (v1.2):** `generated → {accepted, rejected, deferred}`; `deferred → {accepted, rejected}`; `accepted → implemented`; any active → `superseded` (State Model §11). **Recommendations remain advisory**; selecting/deferring changes no CAF/Reliability/Confidence.

**Attribution model:** **one Recommendation → one Finding** (`finding_id`, always present). A Finding may have **many** Recommendations (inverse); the UI surfaces these as **"Possible Resolution Paths"** (presentation only — AMB-1; no `resolution_paths` field).

*Suggested-fix application interacts with free-tier daily-fix limits (Monetization) — enforced elsewhere, not modeled here.*

---

## Sections inherited unchanged from v1.1

The following are **inherited verbatim from `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md`** (no change in v1.2): §1 Purpose · §2 Principles · §3 Entity Inventory *(no new entity)* · §4 Relationship Map · §5 Workspace · §6 User · §7 Project · §8 Artifact · §9 Context Plane (Evidence/ContextItem) · §10 Analysis Run (AnalysisRun/CAFState/ConfidenceState) · **§11 Finding Model (unchanged)** · §13 Notification · §14 Collaboration · §15 Reporting · §16 Multi-Tenant Isolation · §17 Versioning · §18 Auditability · §19 ERD · §20 Open Questions.

*(The ERD's `RECOMMENDATION` node gains `status∈{…,deferred,…}` and the five additive fields; no relationship or other entity changes.)*

---

## Validation

- Active Release 1 only — ✅
- Additive only — ✅ (one enum value + five fields on `Recommendation`)
- No new entity — ✅ · **Finding unchanged** — ✅
- `status` includes `deferred`, excludes `presented`/`completed` — ✅ (RS-R3/RS-R2/RS-R4)
- `recommendation_type` = 3 values — ✅ (RS-R1)
- `finding_id` single; `expected_dimension` single — ✅ (RS-R5/RS-R6 deferred)
- No `resolution_paths`/`is_recommended`/`is_selected` — ✅ (AMB-1)
- No governance / Resolution Candidate / Clarification Candidate — ✅
- No CAF/Reliability/Confidence/Finding/Recommendation behavior change — ✅ (additive persistence only)

**Release 1 Data Model Specification v1.2 complete.**
