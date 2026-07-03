# Release 1 Data Model Specification v1.1

> **⚠ SUPERSEDED (KIA-5, 2026-06-05) — build to `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (current canonical).** Retained for history.

**Type:** Implementation artifact — ~~authoritative~~ **superseded** Release 1 persistence data model (reconciled)
**Status:** **Historical — superseded by v1.2** · **Date:** 2026-05-31
**Supersedes:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` (v1 retained; this is the reconciled successor)
**Reconciliation basis:** `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` (lifecycle authority) · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` (transition authority) · `RELEASE_1_DATA_STATE_RECONCILIATION_AUDIT.md` · `DATA_MODEL_RECONCILIATION_CHANGE_LOG.md` · `DATA_MODEL_RECONCILIATION_PATCH_001.md`
**Aligned with:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md` · `OSLO_RELEASE_1_MASTER_SPEC.md` §18

> **Scope guardrails.** Active Release 1 only. **No Governance Domain entities**, no Agent Governance, Execution Intelligence, Future Architecture, or Release 2. This is an **implementation artifact, not doctrine**.
>
> **v1.1 reconciliation note.** This revision applies the approved reconciliation items **R-1 (Finding), R-2 (Recommendation), R-4 (Notification), R-5 (Report), R-6 (Shared Artifact)** to make the Data Model the persistence authority for the State Model's lifecycles and the Event Model's transitions. **Authority order:** State Model wins for lifecycle definitions; Event Model wins for transition semantics; the Data Model is updated to persist them. Only persistence definitions changed — **no new entities, no new architecture, no governance/future concepts.** Changed sections are marked **〔R-n〕**. See `DATA_MODEL_RECONCILIATION_CHANGE_LOG.md`.

---

## 1. Purpose

This document is the **authoritative source for Release 1 persistence entities**. It is an **implementation artifact**, not doctrine. The conceptual models define *meaning*; this document defines *what is stored, with what fields and relationships*. v1.1 conforms the stored lifecycle enums and adds the missing status fields so persistence exactly mirrors the approved State Model lifecycles and Event Model transitions.

---

## 2. Data Modeling Principles

- **Event-driven** — entities are created/updated in response to events; `AnalysisRun.trigger_source` records the cause.
- **Versioned** — Artifacts, Analyses, and Reports keep version chains.
- **Traceable** — every Finding/Recommendation links to evidence, context, and the producing run (§18).
- **Replayable** — append-friendly chains + per-run snapshots reconstruct any prior state.
- **Tenant isolated** — every tenant-scoped row carries `workspace_id` (§16).
- **Explainable** — assessment snapshots and lineage explain any signal from stored data.
- **Append-friendly** — supersession via pointers, not destructive updates, for history-bearing entities.
- **Analysis-history preserving** — each AnalysisRun and its ConfidenceState/CAFState are retained.

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

*No governance entities. No entities added in v1.1. CAF Review Requests remain a collaboration capability (Comment/Mention/SharedArtifact), not a separate entity.* **[decision]**

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
| `workspace_id` | UUID (FK Workspace) | **[decision]** single workspace per user in R1 |
| `email` | string (unique) | |
| `display_name` | string | |
| `role` | enum(`owner`,`admin`,`member`) | R1 roles; **no external-reviewer role** |
| `status` | enum(`invited`,`active`,`deactivated`) | |
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
| `lifecycle_state` | enum(`created`,`orienting`,`oriented`,`deep_analyzing`,`analyzed`,`archived`) | **[decision]** mirrors the analysis flow; State Model labels Draft/Orientation Running/Orientation Complete/Deep Analysis Running/Deep Analysis Complete/Archived map 1:1 (rename-only; not in this reconciliation batch — see change log note) |
| `current_confidence_state_id` | UUID (FK ConfidenceState, nullable) | latest confidence |
| `created_at` / `updated_at` | timestamp | |

**Ownership rules.** A Project belongs to exactly one `workspace_id`, created by one `created_by_user_id`. Access via workspace membership and shares (§16). Free tier permits one active Project per workspace **[decision]**.

---

## 8. Artifact Model

**Artifact**

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `artifact_type` | enum(`intent_charter`,`context`,`scope`,`requirements`,`wbs`,`resource_plan`,`schedule`,`executive_summary`) | |
| `current_version_id` | UUID (FK ArtifactVersion) | head version |
| `state` | enum(`generated`,`modified`,`reviewed`,`validated`,`evolving`) | artifact lifecycle (PS-04) |
| `created_at` / `updated_at` | timestamp | |

**ArtifactVersion** (append-only)

| Field | Type | Notes |
|---|---|---|
| `artifact_version_id` | UUID (PK) | |
| `artifact_id` | UUID (FK) | |
| `version_number` | int (monotonic per artifact) | |
| `content` | json/text | |
| `authored_by_kind` | enum(`system_synthesis`,`user_edit`,`assisted_edit`) | |
| `authored_by_user_id` | UUID (nullable) | |
| `supersedes_version_id` | UUID (FK, nullable) | |
| `created_at` | timestamp | |

---

## 9. Context Plane Data Model

**Evidence**

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `source_type` | enum(`free_text`,`uploaded_document`,`structured_input`,`imported_content`) | |
| `content_ref` | text / blob-ref | |
| `provenance` | json | |
| `created_at` | timestamp | |

**ContextItem**

| Field | Type | Notes |
|---|---|---|
| `context_item_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `evidence_id` | UUID (FK, nullable) | |
| `item_type` | enum(`claim`,`assumption`,`relationship`,`entity`,`metric`,`interpretation`) | |
| `extraction_horizon` | enum(`fast`,`deep`) | fast = orientation; deep = enrichment |
| `produced_by_run_id` | UUID (FK AnalysisRun) | |
| `content` | json | |
| `source_attribution` | json | |
| `created_at` | timestamp | |

---

## 10. Analysis Run Model

**AnalysisRun** — execution record of a **Fast** or **Deep** pass.

| Field | Type | Notes |
|---|---|---|
| `analysis_run_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `run_type` | enum(`fast_analysis_pass`,`deep_analysis_pass`) | |
| `run_status` | **enum(`queued`,`running`,`completed`,`failed`,`cancelled`,`superseded`)** 〔Patch-001〕 | `cancelled` added to align with State Model §5 and the Event Model `analysis_cancelled` transition (§8). State Model and Event Model unchanged. |
| `trigger_source` | enum(`project_created`,`evidence_added`,`artifact_edited`,`fix_applied`,`chat_interaction`,`collaboration_event`,`manual`) | event-driven cause |
| `previous_run_id` | UUID (FK AnalysisRun, nullable) | chains fast→deep and deep→deep |
| `started_at` / `completed_at` | timestamp | |

**Multiple runs per project.** First run = `fast_analysis_pass` (60-Second Orientation); one or more `deep_analysis_pass` follow. Each run produces exactly one `CAFState` and one `ConfidenceState` and creates/updates Findings/Recommendations. This records **Confidence Recalculation**, **Expanded Findings**, **Expanded Recommendations**.

**CAFState** (1:1 per run)

| Field | Type | Notes |
|---|---|---|
| `caf_state_id` | UUID (PK) | |
| `analysis_run_id` | UUID (FK) | |
| `project_id` | UUID (FK) | denormalized |
| `clarity_index` / `alignment_index` / `feasibility_index` | numeric | range = calibration (§20) |
| `clarity_reliability` / `alignment_reliability` / `feasibility_reliability` | enum/qualifier | |
| `created_at` | timestamp | |

**ConfidenceState** (1:1 per run; chained = history)

| Field | Type | Notes |
|---|---|---|
| `confidence_state_id` | UUID (PK) | |
| `analysis_run_id` | UUID (FK) | |
| `project_id` | UUID (FK) | |
| `outcome_confidence_value` | numeric | range = calibration |
| `confidence_band` | enum(`very_low`,`low`,`moderate`,`high`,`very_high`) | |
| `reliability_qualifier` | enum/value | |
| `supersedes_confidence_state_id` | UUID (FK, nullable) | recalculation chain |
| `created_at` | timestamp | |

---

## 11. Finding Model 〔R-1〕

Persistence representation only — aligned with the Finding Model doctrine; **not a redefinition**. **v1.1:** `status` enum reconciled to the State Model Finding lifecycle.

| Field | Type | Notes |
|---|---|---|
| `finding_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `first_seen_run_id` | UUID (FK AnalysisRun) | run that first produced it (**deep ⇒ Expanded Finding**) |
| `last_updated_run_id` | UUID (FK AnalysisRun) | run that last touched it |
| `finding_type` | enum(`missing_information`,`ambiguity`,`assumption`,`inference`,`conflict`,`constraint`,`coverage_gap`) | flat taxonomy |
| `affected_dimensions` | array(enum(`clarity`,`alignment`,`feasibility`)) | |
| `severity` | enum(`critical`,`moderate`,`warning`) | |
| `status` | **enum(`detected`,`acknowledged`,`addressed`,`closed`,`reopened`,`superseded`)** 〔R-1〕 | reconciled to State Model §10. **Renamed:** `validated`→`acknowledged`, `resolved`→`closed`. **Removed:** `recommended` (the Recommendation link conveys it). **Added:** `superseded`. No additional states. |
| `artifact_id` / `artifact_version_id` | UUID (FK, nullable) | location |
| `evidence_links` | array(UUID) | evidence/context_item ids |
| `created_at` / `updated_at` / `closed_at` 〔R-1〕 | timestamp | `resolved_at` renamed `closed_at`; history preserved on close/supersede |

**Migration considerations 〔R-1〕:** map existing rows `validated→acknowledged`, `resolved→closed`, rename column `resolved_at→closed_at`; for any `recommended` rows, set `status` from the linked Recommendation's existence (→ `acknowledged` if not yet addressed) and rely on the Recommendation FK for "has a recommendation." `superseded` is a new terminal value (no back-mapping needed). Pre-GA: no production data assumed; this is a forward enum definition, not a live migration.

---

## 12. Recommendation Model 〔R-2〕

Persistence representation only — aligned with the Recommendation Model; suggested fixes are a recommendation type. **v1.1:** `status` enum reconciled to the State Model Recommendation lifecycle.

| Field | Type | Notes |
|---|---|---|
| `recommendation_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `finding_id` | UUID (FK Finding) | operates on a Finding |
| `first_seen_run_id` | UUID (FK AnalysisRun) | run that produced it (**deep ⇒ Expanded Recommendation**) |
| `recommendation_type` | enum(`improvement`,`validation`,`suggested_fix`) | |
| `status` | **enum(`generated`,`accepted`,`rejected`,`implemented`,`superseded`)** 〔R-2〕 | reconciled to State Model §11. **Removed:** `presented` (UI/notification concern, not a status), `modified` (an edit produces a new/updated rec, not a status). **Collapsed:** `applied`+`verified`→`implemented`. **Added:** `superseded`. |
| `rationale` | text | |
| `expected_dimension` | enum(`clarity`,`alignment`,`feasibility`, nullable) | |
| `created_at` / `updated_at` | timestamp | |

**Migration impact 〔R-2〕:** `applied→implemented`, `verified→implemented` (an optional `verified_at` timestamp may be added later if a verified sub-state is needed — out of scope here); `presented→generated` (presentation is surfacing, not lifecycle); `modified→accepted` (a modified rec is an accepted one whose content changed). `superseded` is new. Forward enum definition; no live data assumed pre-GA.

---

## 13. Notification Model 〔R-4〕

Persistence representation only. **No routing, delivery, or workflow logic.** **v1.1:** `state` enum reconciled to the State Model Notification lifecycle.

| Field | Type | Notes |
|---|---|---|
| `notification_id` | UUID (PK) | |
| `workspace_id` | UUID (FK) | |
| `project_id` | UUID (FK, nullable) | |
| `source_object_type` | enum(`finding`,`recommendation`,`analysis_run`,`comment`,`shared_artifact`) | |
| `source_object_id` | UUID | |
| `event_type` | enum(`created`,`changed`,`resolved`,`completed`,`mentioned`,`shared`) | triggering source event (unchanged; this is *why* a notification exists, not its lifecycle) |
| `target_user_id` | UUID (FK User) | conceptual addressee only |
| `state` | **enum(`created`,`viewed`,`dismissed`,`expired`)** 〔R-4〕 | reconciled to State Model §12. **Mapped:** `historical`→`expired`. **Deprecated/removed:** `acted_upon` (no lifecycle counterpart; awareness only). |
| `created_at` / `viewed_at` / `dismissed_at` / `expired_at` 〔R-4〕 | timestamp | awareness history preserved; `expired_at` added |

**Mappings & deprecated values 〔R-4〕:** `historical → expired`; `acted_upon` → **deprecated** (drop; the source object's own state records action — a notification never "acts"). **Migration path:** map `acted_upon` rows to `dismissed` (the user engaged then the notice closed) and `historical` to `expired`; forward enum, no live data pre-GA.

> **Discrepancy flagged — `Delivered` (deferred, no behavior invented).** The reconciliation prompt referenced a notification `Delivered` state. The current **State Model §12 does not define `Delivered`** (its lifecycle is Created → Viewed → Dismissed + Expired). Per the governing rules — *State Model wins for lifecycle; State Model must not be modified; do not invent new behavior* — v1.1 does **not** add `delivered` to persistence. **`delivered` is deferred until delivery-channel semantics exist** 〔Patch-001〕: a `delivered` state is only meaningful once Release 1 defines a delivery channel (e.g., push/email/in-app transport) that can confirm receipt; absent that, it has no observable transition. When delivery-channel semantics are introduced, `delivered` must first be added to the State Model via governance, then persisted here. Recorded as an outstanding item (change log "Outstanding" O-2; `DATA_MODEL_RECONCILIATION_PATCH_001.md`).

---

## 14. Collaboration Model 〔R-6 for SharedArtifact〕

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
| `created_at` / `updated_at` | timestamp | |

**Mention**

| Field | Type | Notes |
|---|---|---|
| `mention_id` | UUID (PK) | |
| `comment_id` | UUID (FK) | |
| `mentioned_user_id` | UUID (FK User) | |

**SharedArtifact** (Share Link) — **v1.1:** explicit lifecycle `status` added.

| Field | Type | Notes |
|---|---|---|
| `share_id` | UUID (PK) | |
| `workspace_id` | UUID (FK) | |
| `shared_object_type` | enum(`project`,`artifact`,`mri_snapshot`,`report`) | |
| `shared_object_id` | UUID | |
| `status` | **enum(`created`,`shared`,`viewed`,`revoked`,`expired`)** 〔R-6〕 | reconciled to State Model §14. Lifecycle is now directly queryable rather than inferred from timestamps. |
| `visibility` | enum(`private_link`,`public_link`,`workspace`) | |
| `permission_level` | enum(`view`,`comment`) | **[decision]** R1 levels = view/comment |
| `created_by_user_id` | UUID (FK) | |
| `created_at` / `shared_at` 〔R-6〕 / `first_viewed_at` 〔R-6〕 / `expires_at` / `revoked_at` | timestamp | timestamps retained as **evidence**; `status` is the authoritative lifecycle field |

**Constraints 〔R-6〕:** `status=revoked` requires `revoked_at` set; `status=expired` requires `expires_at` ≤ now; `status` transitions are append-only in intent (no revoked→shared). `expires_at`/`revoked_at` remain nullable evidence fields; `status` is derived-and-stored at transition time (set by the Event Model's `artifact_shared`/`share_revoked`/`share_expired`). Sharing design is unchanged — only lifecycle storage is added.

---

## 15. Reporting Model 〔R-5〕

**Report** — **v1.1:** explicit lifecycle `status` added.

| Field | Type | Notes |
|---|---|---|
| `report_id` | UUID (PK) | |
| `project_id` | UUID (FK) | |
| `report_type` | enum(`executive_summary`,`charter_report`,`mri_export`,`analytics`) | |
| `status` | **enum(`draft`,`published`,`superseded`,`archived`)** 〔R-5〕 | reconciled to State Model §13; set by the Event Model's `report_generated`/`report_published`/`report_superseded`/`report_archived` |
| `current_snapshot_id` | UUID (FK ReportSnapshot) | head |
| `published_snapshot_id` 〔R-5〕 | UUID (FK ReportSnapshot, nullable) | the snapshot live while `status=published` |
| `created_at` / `updated_at` | timestamp | |

**ReportSnapshot** (versioned reporting; unchanged)

| Field | Type | Notes |
|---|---|---|
| `report_snapshot_id` | UUID (PK) | |
| `report_id` | UUID (FK) | |
| `version_number` | int (monotonic) | |
| `generated_from_run_id` | UUID (FK AnalysisRun) | the analysis state it reflects (replay) |
| `format` | enum(`pdf`,`html`,`json`) | |
| `content_ref` | text/blob-ref | |
| `created_at` | timestamp | |

**Constraints & lineage implications 〔R-5〕:** `status` and the `ReportSnapshot` chain are complementary — `status` is the Report's lifecycle; the snapshot chain is its version history. A `published` Report has a non-null `published_snapshot_id`; publishing a newer snapshot moves the prior Report to `superseded` (snapshots retained — supersession over mutation). Reporting design is unchanged; only the status field + published pointer are added.

---

## 16. Multi-Tenant Isolation Model

- **Workspace is the tenant boundary.** Every tenant-scoped entity carries `workspace_id` (denormalized onto Project-children) **[decision]**.
- **Access scoping:** a User accesses entities in their `workspace_id`; Project access respects ownership/membership; cross-tenant access only via a `SharedArtifact` with explicit `permission_level`.
- **Isolation enforcement:** all reads/writes filtered by `workspace_id`; share links grant scoped, revocable, optionally-expiring access. (v1.1 `SharedArtifact.status` makes share liveness explicit, strengthening isolation queries.)
- **No governance/posture/tenancy-policy concepts.**

---

## 17. Versioning Strategy

- **Artifact versioning:** `ArtifactVersion` append-only chain; `Artifact.current_version_id` = head.
- **Analysis versioning:** each `AnalysisRun` immutable once `completed`; `previous_run_id` chains; per-run `CAFState`/`ConfidenceState` retained. Recalculation = new run + new states.
- **Report versioning:** `ReportSnapshot` append-only chain; `Report.status` tracks lifecycle 〔R-5〕.
- **Replayability:** any prior project state reconstructable from artifact-version, analysis-run, and report-snapshot chains plus evidence/context. Reconciled lifecycle enums preserve replay (transitions are set-to-state, idempotent).

---

## 18. Auditability & Traceability

```text
Evidence ─< ContextItem ─(produced_by_run)→ AnalysisRun
AnalysisRun ─< Finding ─< Recommendation
Finding.evidence_links → Evidence / ContextItem
ConfidenceState.supersedes → ConfidenceState   (confidence history)
ReportSnapshot.generated_from_run → AnalysisRun
```

Every Finding traces to its evidence and producing run; every Recommendation to its Finding and run; every confidence value to its run and prior value. Supports explainability directly from stored relationships.

---

## 19. Entity Relationship Diagram (text)

```text
WORKSPACE (workspace_id PK)
  1───< USER (user_id PK, workspace_id FK)
  1───< PROJECT (project_id PK, workspace_id FK, created_by_user_id FK)
  1───< NOTIFICATION (notification_id PK, workspace_id FK, target_user_id FK,
                       source_object_type/id, state∈{created,viewed,dismissed,expired})   〔R-4〕
  1───< SHARED_ARTIFACT (share_id PK, workspace_id FK, shared_object_type/id,
                          status∈{created,shared,viewed,revoked,expired}, permission_level)  〔R-6〕
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
  │        │     severity, status∈{detected,acknowledged,addressed,closed,reopened,superseded},  〔R-1〕
  │        │     evidence_links[])
  │        ├─< RECOMMENDATION (recommendation_id PK, finding_id FK,
  │        │                   status∈{generated,accepted,rejected,implemented,superseded},      〔R-2〕
  │        │                   recommendation_type)
  │        └─< CAF_OVERLAY (overlay_id PK, finding_id FK, artifact_version_id FK)
  1───< COMMENT (comment_id PK, project_id FK, parent_comment_id FK)
  │        └─< MENTION (mention_id PK, comment_id FK, mentioned_user_id FK)
  1───< REPORT (report_id PK, project_id FK, status∈{draft,published,superseded,archived},        〔R-5〕
  │        │    current_snapshot_id FK, published_snapshot_id FK)
  │        └─< REPORT_SNAPSHOT (report_snapshot_id PK, report_id FK, generated_from_run_id FK)
  1───< CHAT_SESSION (chat_session_id PK, project_id FK)
```

---

## 20. Open Questions (unresolved — not solved here)

1. **CAF / Confidence value ranges** — calibration (owner-owned; Matrix §22 g1).
2. **Permission-level enumeration** — R1 uses `view`/`comment` **[decision]**; fuller enumeration unresolved (Matrix §22 g7).
3. **User ↔ Workspace cardinality** — single-workspace per user for R1 **[decision]**.
4. **MRI persistence** — stored-per-run vs recomputed-on-read.
5. **Retention / deletion (GDPR)** — unresolved (Master Spec §22 g12).
6. **AnalysisRun concurrency / debounce** — owned by State/Event Models.
7. **TelemetryEvent schema** — operational, defined elsewhere.
8. **AnalysisRun `cancelled`** — ✅ **resolved in Patch-001** (added to `run_status`, §10).
9. **Notification `Delivered`** — **deferred until delivery-channel semantics exist** 〔Patch-001〕; requires a State Model change first when a delivery channel is defined (see §13 discrepancy note).
10. **Recommendation `verified` sub-state** 〔new〕 — `applied`+`verified` collapsed to `implemented`; if post-implementation verification must be tracked, add a `verified_at` flag (not a lifecycle state) later.

---

## Validation

- Active Release 1 only — ✅
- State Model ↔ Data Model lifecycle alignment — ✅ for Finding, Recommendation, Notification, Report, Shared Artifact, **and AnalysisRun** (R-1, R-2, R-4, R-5, R-6 + Patch-001 `cancelled`). Project enum is rename-only (1:1, behaviorally aligned).
- Event Model transitions remain valid — ✅ for **all** reconciled lifecycles, including `analysis_cancelled` → `run_status=cancelled` (Patch-001).
- No Governance entities introduced — ✅
- No Future Architecture introduced — ✅
- No new domain concepts introduced — ✅ (only enum/field reconciliation; zero new entities)
- Replayability preserved — ✅ (set-to-state transitions; chains intact)
- Event-sourcing assumptions preserved — ✅ (append-only, idempotent, supersession-by-pointer)
- Multi-tenant isolation preserved — ✅ (`workspace_id` unchanged; share liveness now explicit)
- Confidence Recalculation preserved — ✅ (`ConfidenceState` chain unchanged)
- Expanded Findings preserved — ✅ (`first_seen_run_id` unchanged; status now supports `superseded`)
- Expanded Recommendations preserved — ✅ (`first_seen_run_id` unchanged; status now supports `superseded`)

**Release 1 Data Model Specification complete.**
