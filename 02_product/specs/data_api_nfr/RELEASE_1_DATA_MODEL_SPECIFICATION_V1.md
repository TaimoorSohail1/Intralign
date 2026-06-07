# Release 1 Data Model Specification v1

> **⚠ SUPERSEDED (KIA-5, 2026-06-05) — build to `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (current canonical).** v1 → v1.1 → v1.2; v1.2 has the reconciliations applied. Retained for history.

**Type:** Implementation artifact — ~~authoritative~~ **superseded** Release 1 persistence data model
**Status:** **Historical — superseded by v1.2** · **Date:** 2026-05-31
**Aligned with:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md` · `OSLO_RELEASE_1_MASTER_SPEC.md` §18 (object model)

> **Scope guardrails.** Active Release 1 only. **No Governance Domain entities** (no Resolution Candidate, Review Request, Disposition, Governance, or Accepted Understanding), no Agent Governance, no Execution Intelligence, no Future Architecture, no Release 2. This is an **implementation artifact, not doctrine** — it defines persistence entities and resolves ambiguity with explicit modeling decisions (marked **[decision]**). It models the Master Spec §18 object model's **active** subset and the Canonical Scope flow: Fast Analysis Pass → 60-Second Orientation → Deep Analysis Pass → Confidence Recalculation → Expanded Findings → Expanded Recommendations.

---

## 1. Purpose

This document is the **authoritative source for Release 1 persistence entities**. It is an **implementation artifact**, not doctrine and not conceptual architecture — the conceptual models (CAF Assessment, Finding, Recommendation, Notification, etc.) define *meaning*; this document defines *what is stored, with what fields and relationships*, so engineering can build persistence, the Knowledge Layer, and the analysis flow. Where the conceptual sources leave an implementation choice open, this document makes an explicit **[decision]** for Release 1.

---

## 2. Data Modeling Principles

- **Event-driven** — entities are created/updated in response to events (evidence change, edit, run completion), not on a clock; `AnalysisRun.trigger_source` records the cause.
- **Versioned** — Artifacts, Analyses, and Reports keep version chains; nothing mutates in place where history matters.
- **Traceable** — every Finding/Recommendation links to the evidence, context, and analysis run that produced it (lineage, §18).
- **Replayable** — append-friendly version chains + per-run snapshots allow reconstructing any prior state.
- **Tenant isolated** — every tenant-scoped row carries `workspace_id`; isolation is enforced at that boundary (§16).
- **Explainable** — assessment snapshots and lineage links allow any signal to be explained from stored data.
- **Append-friendly** — supersession via pointers (`supersedes_*`, `previous_run_id`) rather than destructive updates for history-bearing entities.
- **Analysis-history preserving** — each AnalysisRun and its ConfidenceState/CAFState are retained, so confidence and findings history survive recalculation.

---

## 3. Entity Inventory

| Entity | Purpose | Lifecycle Owner | Active R1 | Notes |
|---|---|---|---|---|
| **Workspace** | Tenant root | Workspace owner | ✅ | Tenancy boundary |
| **User** | Person in a workspace | Workspace | ✅ | Single-workspace in R1 **[decision]** |
| **Project** | Primary operating object | User (in workspace) | ✅ | One active project on free tier |
| **Artifact** | A planning artifact | Project | ✅ | Intent/Context/Scope/Req/WBS/Resources/Schedule/Exec-Summary |
| **ArtifactVersion** | Version of an artifact | Artifact | ✅ | Version history + replay |
| **Evidence** | Raw input contributing to understanding | Project | ✅ | text/doc/structured/imported |
| **ContextItem** | Extracted/enriched context unit | Project | ✅ | claim/assumption/relationship; fast/deep horizon |
| **AnalysisRun** | A Fast or Deep analysis pass execution | Project | ✅ | Core of the analysis flow |
| **CAFState** | Per-run CAF dimension snapshot | AnalysisRun | ✅ | Clarity/Alignment/Feasibility |
| **ConfidenceState** | Per-run Outcome Confidence snapshot | AnalysisRun | ✅ | Confidence history / recalculation |
| **Finding** | An observation about understanding | Project | ✅ | persistence of Finding Model |
| **Recommendation** | Prescriptive improvement (incl. suggested fix) | Project | ✅ | operates on a Finding |
| **Notification** | Awareness of a relevant change | Workspace | ✅ | persistence only; no routing |
| **Comment** | Collaboration comment/reply | Project | ✅ | threaded |
| **Mention** | @-mention within a comment | Comment | ✅ | |
| **SharedArtifact** (Share Link) | A share of a project/artifact/MRI/report | Workspace | ✅ | permission levels |
| **Report** | A report definition | Project | ✅ | exec summary / charter / export |
| **ReportSnapshot** | Versioned report instance | Report | ✅ | versioned reporting |
| **MRISnapshot** *(derived)* | Visualization snapshot of understanding | AnalysisRun | ✅ | derived; recomputed per run |
| **CAFOverlay** *(derived)* | Finding mapped to an artifact location | Finding | ✅ | derived |
| **ChatSession** | OSLO Chat session (M3) | Project | ✅ | lightly modeled in R1 |
| **TelemetryEvent** | Product/operational event | Workspace | ✅ | append-only; operational |

*No governance entities are present. CAF Review Requests are handled as a collaboration capability and are not a separate persistence entity in this model (collaboration is Comment/Mention/SharedArtifact).* **[decision]**

---

## 4. Core Relationship Map

```text
Workspace
  └─< User
  └─< Project
        ├─< Artifact ─< ArtifactVersion
        ├─< Evidence ─< ContextItem
        ├─< AnalysisRun
        │      ├─ 1:1 CAFState
        │      ├─ 1:1 ConfidenceState
        │      ├─< Finding ─< Recommendation
        │      └─ 0:1 MRISnapshot
        ├─< Comment ─< Mention
        ├─< Report ─< ReportSnapshot
        └─< ChatSession
Workspace
  └─< Notification        (references a source object: Finding/Recommendation/AnalysisRun/Comment/Share)
  └─< SharedArtifact       (references Project/Artifact/MRISnapshot/Report)
Finding ─< CAFOverlay (→ Artifact location)
AnalysisRun.previous_run_id → AnalysisRun   (fast → deep → deep chain)
```

---

## 5. Workspace Model

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | UUID (PK) | Tenant root |
| `name` | string | |
| `owner_user_id` | UUID (FK User) | Workspace owner |
| `tier` | enum(`free`,`paid`) | Free-tier limits per Monetization |
| `status` | enum(`active`,`suspended`) | |
| `created_at` / `updated_at` | timestamp | |

---

## 6. User Model

| Field | Type | Notes |
|---|---|---|
| `user_id` | UUID (PK) | |
| `workspace_id` | UUID (FK Workspace) | **[decision]** single workspace per user in R1 (multi-workspace = future) |
| `email` | string (unique) | |
| `display_name` | string | |
| `role` | enum(`owner`,`admin`,`member`) | R1 roles; **no external-reviewer role** (governance/future) |
| `status` | enum(`invited`,`active`,`deactivated`) | Alpha invitation → activation |
| `created_at` / `updated_at` | timestamp | |

---

## 7. Project Model

| Field | Type | Notes |
|---|---|---|
| `project_id` | UUID (PK) | Primary operating object |
| `workspace_id` | UUID (FK) | Tenant scope |
| `created_by_user_id` | UUID (FK User) | |
| `title` | string (nullable) | OSLO may infer; naming optional |
| `description` | text (nullable) | |
| `lifecycle_state` | enum(`created`,`orienting`,`oriented`,`deep_analyzing`,`analyzed`,`archived`) | **[decision]** mirrors the analysis flow (orientation → deep) |
| `current_confidence_state_id` | UUID (FK ConfidenceState, nullable) | latest confidence |
| `created_at` / `updated_at` | timestamp | |

**Ownership rules.** A Project belongs to exactly one `workspace_id` and is created by one `created_by_user_id`. Access is governed by workspace membership and shares (§16). Free tier permits one active (non-archived) Project per workspace **[decision]**.

---

## 8. Artifact Model

**Artifact**

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `artifact_type` | enum(`intent_charter`,`context`,`scope`,`requirements`,`wbs`,`resource_plan`,`schedule`,`executive_summary`) | the supported artifact types |
| `current_version_id` | UUID (FK ArtifactVersion) | pointer to head version |
| `state` | enum(`generated`,`modified`,`reviewed`,`validated`,`evolving`) | artifact lifecycle (PS-04) |
| `created_at` / `updated_at` | timestamp | |

**ArtifactVersion** (append-only; supports version history + replay)

| Field | Type | Notes |
|---|---|---|
| `artifact_version_id` | UUID (PK) | |
| `artifact_id` | UUID (FK) | |
| `version_number` | int (monotonic per artifact) | |
| `content` | json/text | artifact body (sections) |
| `authored_by_kind` | enum(`system_synthesis`,`user_edit`,`assisted_edit`) | provenance of the version |
| `authored_by_user_id` | UUID (nullable) | when user/assisted |
| `supersedes_version_id` | UUID (FK, nullable) | prior version |
| `created_at` | timestamp | |

---

## 9. Context Plane Data Model

**Evidence**

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `source_type` | enum(`free_text`,`uploaded_document`,`structured_input`,`imported_content`) | |
| `content_ref` | text / blob-ref | inline or storage reference |
| `provenance` | json | source attribution, origin, capture time |
| `created_at` | timestamp | |

**ContextItem** (extracted/enriched; supports Fast/Deep Extraction, claim/assumption/relationship discovery)

| Field | Type | Notes |
|---|---|---|
| `context_item_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `evidence_id` | UUID (FK, nullable) | derived-from evidence |
| `item_type` | enum(`claim`,`assumption`,`relationship`,`entity`,`metric`,`interpretation`) | claim/assumption/relationship discovery |
| `extraction_horizon` | enum(`fast`,`deep`) | **fast = orientation; deep = enrichment** |
| `produced_by_run_id` | UUID (FK AnalysisRun) | which run produced it |
| `content` | json | |
| `source_attribution` | json | provenance |
| `created_at` | timestamp | |

*No governance concepts. Context is raw/enriched understanding input only.*

---

## 10. Analysis Run Model

**AnalysisRun** — the execution record of a **Fast** or **Deep** analysis pass. Central to the flow.

| Field | Type | Notes |
|---|---|---|
| `analysis_run_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `run_type` | enum(`fast_analysis_pass`,`deep_analysis_pass`) | the two horizons |
| `run_status` | enum(`queued`,`running`,`completed`,`failed`,`superseded`) | |
| `trigger_source` | enum(`project_created`,`evidence_added`,`artifact_edited`,`fix_applied`,`chat_interaction`,`collaboration_event`,`manual`) | event-driven cause |
| `previous_run_id` | UUID (FK AnalysisRun, nullable) | chains fast→deep and deep→deep |
| `started_at` / `completed_at` | timestamp | `completed_at` nullable until done |

**Multiple runs per project.** The first run is a `fast_analysis_pass` (produces the 60-Second Orientation). One or more `deep_analysis_pass` runs follow, each triggered by an event, each linked via `previous_run_id`. Each run produces exactly one `CAFState` and one `ConfidenceState`, and creates/updates `Finding`s and `Recommendation`s. This is how **Confidence Recalculation**, **Expanded Findings**, and **Expanded Recommendations** are recorded: a deep run yields a new ConfidenceState (recalculation) and adds findings/recommendations whose `first_seen_run_id` is that deep run (expansion).

**CAFState** (1:1 per run)

| Field | Type | Notes |
|---|---|---|
| `caf_state_id` | UUID (PK) | |
| `analysis_run_id` | UUID (FK) | |
| `project_id` | UUID (FK) | denormalized for query/isolation |
| `clarity_index` / `alignment_index` / `feasibility_index` | numeric | values produced by scoring (range = calibration; see §20) |
| `clarity_reliability` / `alignment_reliability` / `feasibility_reliability` | enum/qualifier | per-dimension reliability qualifier |
| `created_at` | timestamp | |

**ConfidenceState** (1:1 per run; chained = history)

| Field | Type | Notes |
|---|---|---|
| `confidence_state_id` | UUID (PK) | |
| `analysis_run_id` | UUID (FK) | |
| `project_id` | UUID (FK) | |
| `outcome_confidence_value` | numeric | summarized signal (range = calibration) |
| `confidence_band` | enum(`very_low`,`low`,`moderate`,`high`,`very_high`) | |
| `reliability_qualifier` | enum/value | overall reliability |
| `supersedes_confidence_state_id` | UUID (FK, nullable) | prior confidence (recalculation chain) |
| `created_at` | timestamp | |

---

## 11. Finding Model

Persistence representation only — aligned with the Finding Model doctrine; **not a redefinition**.

| Field | Type | Notes |
|---|---|---|
| `finding_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `first_seen_run_id` | UUID (FK AnalysisRun) | run that first produced it (**deep ⇒ Expanded Finding**) |
| `last_updated_run_id` | UUID (FK AnalysisRun) | run that last touched it |
| `finding_type` | enum(`missing_information`,`ambiguity`,`assumption`,`inference`,`conflict`,`constraint`,`coverage_gap`) | flat taxonomy |
| `affected_dimensions` | array(enum(`clarity`,`alignment`,`feasibility`)) | one or more |
| `severity` | enum(`critical`,`moderate`,`warning`) | |
| `status` | enum(`detected`,`validated`,`recommended`,`addressed`,`resolved`,`reopened`) | issue lifecycle |
| `artifact_id` / `artifact_version_id` | UUID (FK, nullable) | location |
| `evidence_links` | array(UUID) | evidence/context_item ids (traceability) |
| `created_at` / `updated_at` / `resolved_at` | timestamp | history preserved on resolution |

---

## 12. Recommendation Model

Persistence representation only — aligned with the Recommendation Model; suggested fixes are a recommendation type.

| Field | Type | Notes |
|---|---|---|
| `recommendation_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `finding_id` | UUID (FK Finding) | operates on a Finding |
| `first_seen_run_id` | UUID (FK AnalysisRun) | run that produced it (**deep ⇒ Expanded Recommendation**) |
| `recommendation_type` | enum(`improvement`,`validation`,`suggested_fix`) | |
| `status` | enum(`generated`,`presented`,`accepted`,`modified`,`rejected`,`applied`,`verified`) | incl. Generated/Accepted/Rejected |
| `rationale` | text | the explanation/basis |
| `expected_dimension` | enum(`clarity`,`alignment`,`feasibility`, nullable) | which dimension improves |
| `created_at` / `updated_at` | timestamp | |

*Suggested-fix application interacts with free-tier daily-fix limits (Monetization) — that limit is enforced elsewhere and is not modeled here.*

---

## 13. Notification Model

Persistence representation only. **No routing, delivery, or workflow logic** (those are out of scope of this model and of the Notification Model).

| Field | Type | Notes |
|---|---|---|
| `notification_id` | UUID (PK) | |
| `workspace_id` | UUID (FK) | |
| `project_id` | UUID (FK, nullable) | |
| `source_object_type` | enum(`finding`,`recommendation`,`analysis_run`,`comment`,`shared_artifact`) | what changed |
| `source_object_id` | UUID | |
| `event_type` | enum(`created`,`changed`,`resolved`,`completed`,`mentioned`,`shared`) | the triggering event |
| `target_user_id` | UUID (FK User) | conceptual addressee only |
| `state` | enum(`created`,`viewed`,`dismissed`,`acted_upon`,`historical`) | lifecycle outcomes |
| `created_at` / `viewed_at` / `dismissed_at` | timestamp | awareness history preserved |

---

## 14. Collaboration Model

**Comment**

| Field | Type | Notes |
|---|---|---|
| `comment_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `author_user_id` | UUID (FK User) | |
| `target_type` | enum(`artifact`,`artifact_version`,`finding`,`project`) | |
| `target_id` | UUID | |
| `parent_comment_id` | UUID (FK, nullable) | replies |
| `body` | text | |
| `created_at` / `updated_at` | timestamp | activity preserved |

**Mention**

| Field | Type | Notes |
|---|---|---|
| `mention_id` | UUID (PK) | |
| `comment_id` | UUID (FK) | |
| `mentioned_user_id` | UUID (FK User) | |

**SharedArtifact** (Share Link)

| Field | Type | Notes |
|---|---|---|
| `share_id` | UUID (PK) | |
| `workspace_id` | UUID (FK) | |
| `shared_object_type` | enum(`project`,`artifact`,`mri_snapshot`,`report`) | |
| `shared_object_id` | UUID | |
| `visibility` | enum(`private_link`,`public_link`,`workspace`) | |
| `permission_level` | enum(`view`,`comment`) | **[decision]** R1 levels = view/comment (fuller enumeration = open, §20) |
| `created_by_user_id` | UUID (FK) | |
| `created_at` / `expires_at` / `revoked_at` | timestamp | expiry/revocation nullable |

---

## 15. Reporting Model

**Report**

| Field | Type | Notes |
|---|---|---|
| `report_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `report_type` | enum(`executive_summary`,`charter_report`,`mri_export`,`analytics`) | exec summary is a report type |
| `current_snapshot_id` | UUID (FK ReportSnapshot) | head |
| `created_at` / `updated_at` | timestamp | |

**ReportSnapshot** (versioned reporting)

| Field | Type | Notes |
|---|---|---|
| `report_snapshot_id` | UUID (PK) | |
| `report_id` | UUID (FK) | |
| `version_number` | int (monotonic) | |
| `generated_from_run_id` | UUID (FK AnalysisRun) | the analysis state it reflects (replay) |
| `format` | enum(`pdf`,`html`,`json`) | |
| `content_ref` | text/blob-ref | |
| `created_at` | timestamp | |

---

## 16. Multi-Tenant Isolation Model

- **Workspace is the tenant boundary.** Every tenant-scoped entity carries `workspace_id` (denormalized onto Project-children for isolation and query efficiency) **[decision]**.
- **Access scoping:** a User accesses entities in their `workspace_id`; Project access additionally respects ownership/membership; cross-tenant access is only via a `SharedArtifact` with an explicit `permission_level`.
- **Isolation enforcement:** all reads/writes are filtered by `workspace_id`; share links grant scoped, revocable, optionally-expiring access to a single shared object.
- **No governance/posture/tenancy-policy concepts** — Release 1 tenancy is workspace + ownership + share scope only.

---

## 17. Versioning Strategy

- **Artifact versioning:** `ArtifactVersion` append-only chain (`version_number`, `supersedes_version_id`); `Artifact.current_version_id` points to head. Full history retained.
- **Analysis versioning:** each `AnalysisRun` is immutable once `completed`; `previous_run_id` chains runs; per-run `CAFState`/`ConfidenceState` snapshots are retained (confidence/findings history). Recalculation = a new run + new states, never an in-place overwrite.
- **Report versioning:** `ReportSnapshot` append-only chain per `Report`, each pinned to the `AnalysisRun` it reflects.
- **Replayability:** any prior project state is reconstructable from the artifact-version, analysis-run, and report-snapshot chains plus the evidence/context that fed them.

---

## 18. Auditability & Traceability

Lineage is stored end to end:

```text
Evidence ─< ContextItem ─(produced_by_run)→ AnalysisRun
AnalysisRun ─< Finding ─< Recommendation
Finding.evidence_links → Evidence / ContextItem
ConfidenceState.supersedes → ConfidenceState   (confidence history)
ReportSnapshot.generated_from_run → AnalysisRun
```

Every Finding traces to its evidence and producing run; every Recommendation traces to its Finding and run; every confidence value traces to its run and prior value. This supports explainability ("why is this finding/score here, and what changed?") directly from stored relationships — no recomputation required for explanation.

---

## 19. Entity Relationship Diagram (text)

```text
WORKSPACE (workspace_id PK)
  1───< USER (user_id PK, workspace_id FK)
  1───< PROJECT (project_id PK, workspace_id FK, created_by_user_id FK)
  1───< NOTIFICATION (notification_id PK, workspace_id FK, target_user_id FK,
                       source_object_type/id)
  1───< SHARED_ARTIFACT (share_id PK, workspace_id FK, shared_object_type/id, permission_level)
  1───< TELEMETRY_EVENT (event_id PK, workspace_id FK)

PROJECT
  1───< ARTIFACT (artifact_id PK, project_id FK, current_version_id FK)
  │        1───< ARTIFACT_VERSION (artifact_version_id PK, artifact_id FK, version_number,
  │                                supersedes_version_id FK)
  1───< EVIDENCE (evidence_id PK, project_id FK)
  │        1───< CONTEXT_ITEM (context_item_id PK, project_id FK, evidence_id FK,
  │                            extraction_horizon, produced_by_run_id FK)
  1───< ANALYSIS_RUN (analysis_run_id PK, project_id FK, run_type, run_status,
  │        │          trigger_source, previous_run_id FK)
  │        ├─1:1─ CAF_STATE (caf_state_id PK, analysis_run_id FK)
  │        ├─1:1─ CONFIDENCE_STATE (confidence_state_id PK, analysis_run_id FK,
  │        │                        supersedes_confidence_state_id FK)
  │        └─0:1─ MRI_SNAPSHOT (mri_snapshot_id PK, analysis_run_id FK)
  1───< FINDING (finding_id PK, project_id FK, first_seen_run_id FK, finding_type,
  │        │     severity, status, evidence_links[])
  │        ├─< RECOMMENDATION (recommendation_id PK, finding_id FK, status, recommendation_type)
  │        └─< CAF_OVERLAY (overlay_id PK, finding_id FK, artifact_version_id FK)
  1───< COMMENT (comment_id PK, project_id FK, parent_comment_id FK)
  │        └─< MENTION (mention_id PK, comment_id FK, mentioned_user_id FK)
  1───< REPORT (report_id PK, project_id FK, current_snapshot_id FK)
  │        └─< REPORT_SNAPSHOT (report_snapshot_id PK, report_id FK, generated_from_run_id FK)
  1───< CHAT_SESSION (chat_session_id PK, project_id FK)
```

---

## 20. Open Questions (unresolved — not solved here)

1. **CAF / Confidence value ranges.** `*_index` and `outcome_confidence_value` numeric ranges and band thresholds are **calibration** (owner-owned; Matrix §22 g1). The model stores values; calibration sets the scale.
2. **Permission-level enumeration.** R1 uses `view`/`comment` **[decision]**; a fuller enumeration (and any external-collaborator identity for public shares) is unresolved (Matrix §22 g7).
3. **User ↔ Workspace cardinality.** Modeled single-workspace per user for R1 **[decision]**; multi-workspace membership is deferred.
4. **MRI persistence.** `MRISnapshot` is modeled as persisted-per-run; whether MRI is stored or recomputed on read is an implementation choice.
5. **Retention / deletion (GDPR).** Retention and hard-delete policy for Evidence, ArtifactVersion, AnalysisRun history is unresolved (Master Spec §22 g12).
6. **AnalysisRun concurrency / debounce.** Rapid triggers vs run queuing/cooldown belong to the State Model spec; not resolved here.
7. **TelemetryEvent schema.** Event payload schema is operational and defined elsewhere.

*These are recorded for the State Model, API, and calibration specs to resolve; this document does not solve them.*

---

## Validation

- Active Release 1 only — ✅
- No Governance Domain entities — ✅ (no Resolution Candidate / Review Request / Disposition / Governance / Accepted Understanding)
- Supports Fast Analysis Pass — ✅ (`AnalysisRun.run_type = fast_analysis_pass` → orientation)
- Supports Deep Analysis Pass — ✅ (`AnalysisRun.run_type = deep_analysis_pass`, chained via `previous_run_id`)
- Supports Confidence Recalculation — ✅ (`ConfidenceState` per run, `supersedes_confidence_state_id` chain)
- Supports Expanded Findings — ✅ (`Finding.first_seen_run_id` = a deep run)
- Supports Expanded Recommendations — ✅ (`Recommendation.first_seen_run_id` = a deep run)
- Supports Multi-Tenant Isolation — ✅ (`workspace_id` on all tenant entities; share-scoped access)
- Supports Replayability — ✅ (artifact-version, analysis-run, report-snapshot chains + per-run snapshots)
- Supports Reporting — ✅ (`Report` / `ReportSnapshot`, pinned to runs)
- Supports Collaboration — ✅ (`Comment` / `Mention` / `SharedArtifact`)
- No Future Architecture concepts introduced — ✅

**Release 1 Data Model Specification complete.**
