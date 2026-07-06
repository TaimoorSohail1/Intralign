# API Contract Endpoint Catalog

**Type:** Engineering quick-reference — complete Release 1 endpoint inventory
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Companion to:** `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md`

> All endpoints under `/v1`, workspace-scoped, JSON. Commands accept `Idempotency-Key`. No new entities/states/capabilities. Sub-action endpoints use the `:verb` convention.

## Commands

| Resource | Endpoint | Method | Purpose |
|---|---|---|---|
| Project | `/projects` | POST | Create project (→ `created`); emits `project_created` |
| Project | `/projects/{pid}` | PATCH | Update project metadata; emits `project_updated` |
| Project | `/projects/{pid}:archive` | POST | Archive project (→ `archived`); emits `project_archived` |
| Artifact | `/projects/{pid}/artifacts` | POST | Create artifact + head version; emits `artifact_created` |
| Artifact | `/artifacts/{aid}` | PATCH | Update artifact state; emits `artifact_updated` |
| ArtifactVersion | `/artifacts/{aid}/versions` | POST | Append new version; emits `artifact_version_created` |
| Evidence | `/projects/{pid}/evidence` | POST | Add evidence; emits `evidence_added` |
| Evidence | `/evidence/{eid}` | PATCH | Update evidence; re-extraction signal |
| Evidence | `/evidence/{eid}` | DELETE | Remove evidence (soft; retention TBD) |
| Clarification | `/projects/{pid}/clarification-answers` | POST | Capture a clarification answer as a **project-information change** (no Clarification object/lifecycle); marks analysis stale; emits `clarification_answer_captured` (DL-089) |
| AnalysisRun | `/projects/{pid}/analysis-runs:fast` | POST | Start Fast Analysis (→ run `queued`); emits `fast_analysis_requested` |
| AnalysisRun | `/projects/{pid}/analysis-runs:deep` | POST | Start Deep Analysis (→ run `queued`); emits `deep_analysis_requested` |
| AnalysisRun | `/analysis-runs/{rid}:cancel` | POST | Cancel run (→ `cancelled`); emits `analysis_cancelled` |
| Finding | `/findings/{fid}:acknowledge` | POST | detected → acknowledged; emits `finding_updated` |
| Finding | `/findings/{fid}:address` | POST | acknowledged → addressed; emits `finding_updated` |
| Finding | `/findings/{fid}:close` | POST | addressed → closed; emits `finding_closed` |
| Finding | `/findings/{fid}:reopen` | POST | closed → reopened; emits `finding_reopened` |
| Recommendation | `/recommendations/{rid}:accept` | POST | generated → accepted; emits `recommendation_accepted` |
| Recommendation | `/recommendations/{rid}:reject` | POST | generated → rejected; emits `recommendation_rejected` |
| Recommendation | `/recommendations/{rid}:implement` | POST | accepted → implemented; emits `recommendation_implemented` |
| Comment | `/projects/{pid}/comments` | POST | Create comment (+mentions); emits `comment_created`/`mention_created` |
| Comment | `/comments/{cid}/replies` | POST | Reply to comment; emits `comment_created` |
| SharedArtifact | `/shares` | POST | Create share link (→ `shared`); emits `artifact_shared` |
| SharedArtifact | `/shares/{sid}:revoke` | POST | Revoke share (→ `revoked`); emits `share_revoked` |
| Report | `/projects/{pid}/reports` | POST | Generate report (→ `draft`); emits `report_generated` |
| Report | `/reports/{rid}:publish` | POST | Publish report (→ `published`); emits `report_published` |
| Report | `/reports/{rid}:archive` | POST | Archive report (→ `archived`); emits `report_archived` |

## Queries

| Resource | Endpoint | Method | Purpose |
|---|---|---|---|
| Workspace | `/workspace` | GET | Current workspace |
| User | `/users` | GET | List workspace users |
| User | `/users/{uid}` | GET | Get user |
| Project | `/projects` | GET | List projects (filter `lifecycle_state`) |
| Project | `/projects/{pid}` | GET | Get project |
| Artifact | `/projects/{pid}/artifacts` | GET | List artifacts |
| Artifact | `/artifacts/{aid}` | GET | Get artifact |
| ArtifactVersion | `/artifacts/{aid}/versions` | GET | List version history |
| Evidence | `/projects/{pid}/evidence` | GET | List evidence |
| ContextItem | `/projects/{pid}/context-items` | GET | List context items (filter `extraction_horizon`,`item_type`) |
| AnalysisRun | `/projects/{pid}/analysis-runs` | GET | List runs (filter `run_type`,`run_status`) |
| AnalysisRun | `/analysis-runs/{rid}` | GET | Get run (poll; `?include=`) |
| CAFState | `/analysis-runs/{rid}/caf-state` | GET | Get per-run CAF snapshot |
| ConfidenceState | `/analysis-runs/{rid}/confidence-state` | GET | Get per-run confidence snapshot |
| ConfidenceState | `/projects/{pid}/confidence` | GET | Current confidence (`?history=true` → chain) |
| Finding | `/projects/{pid}/findings` | GET | List findings (filter `status`,`finding_type`,`severity`,`first_seen_run_id`) |
| Finding | `/findings/{fid}` | GET | Get finding |
| Recommendation | `/projects/{pid}/recommendations` | GET | List recommendations (filter `status`,`type`,`finding_id`) |
| Recommendation | `/findings/{fid}/recommendations` | GET | List recs for a finding |
| MRISnapshot | `/analysis-runs/{rid}/mri-snapshot` | GET | Get MRI snapshot (derived) |
| CAFOverlay | `/findings/{fid}/overlays` | GET | Get finding overlays (derived) |
| Notification | `/notifications` | GET | List notifications (filter `state`,`project_id`) |
| Comment | `/projects/{pid}/comments` | GET | List comments (threaded; filter `target`) |
| Mention | `/comments/{cid}/mentions` | GET | List mentions in a comment |
| SharedArtifact | `/shares` | GET | List shares (filter `status`,`shared_object_type`) |
| SharedArtifact | `/shares/{sid}` | GET | Get share |
| Report | `/projects/{pid}/reports` | GET | List reports (filter `status`,`report_type`) |
| Report | `/reports/{rid}` | GET | Get report |
| ReportSnapshot | `/reports/{rid}/snapshots` | GET | List report snapshots (version history) |

## Notification state commands (awareness only — never drive analysis)

| Resource | Endpoint | Method | Purpose |
|---|---|---|---|
| Notification | `/notifications/{nid}:view` | POST | created → viewed; emits `notification_viewed` |
| Notification | `/notifications/{nid}:dismiss` | POST | → dismissed; emits `notification_dismissed` |

*Catalog reflects `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` exactly. Enums and events are Data Model v1.1 / Event Model verbatim.*
