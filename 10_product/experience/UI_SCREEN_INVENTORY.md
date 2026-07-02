# UI Screen Inventory

**Type:** Engineering quick-reference — complete Release 1 screen inventory
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Companion to:** `RELEASE_1_UI_SPECIFICATION_V1.md`

> Every Release 1 screen, its purpose, primary user, and the API contract endpoints it consumes. No new screens, capabilities, or workflows beyond the UI spec.

| Screen | Purpose | Primary User | Related APIs |
|---|---|---|---|
| **Dashboard** | Orient on landing: active projects, current confidence, attention items | Any member | `GET /projects`, `GET /projects/{pid}/confidence`, `GET /notifications` |
| **Project Creation** | Create a project; add first intent/evidence; trigger Fast Analysis | Owner/member | `POST /projects`, `POST /projects/{pid}/evidence`, `POST /projects/{pid}/analysis-runs:fast` |
| **Project Workspace** | Hub for one project (artifacts, analysis, findings, recs, activity) | Owner/member | `GET /projects/{pid}` (+ artifacts, findings, recommendations, confidence, comments) |
| **Artifact Editor** | View/edit a planning artifact and its versions | Owner/member | `GET/PATCH /artifacts/{aid}`, `GET/POST /artifacts/{aid}/versions` |
| **Analysis Progress** | Async status while a fast/deep run executes | Owner/member | `GET /analysis-runs/{rid}` (poll), `POST /analysis-runs/{rid}:cancel` |
| **60-Second Orientation** | First understanding: confidence, CAF, top findings/recs (not final) | Owner/member | `GET /analysis-runs/{rid}?include=caf_state,confidence_state,mri_snapshot`, `GET .../findings?status=detected`, `GET .../recommendations?status=generated` |
| **Deep Analysis Results** | Expanded findings/recs + recalculated confidence + run history | Owner/member | `GET /projects/{pid}/analysis-runs`, `GET .../findings?first_seen_run_id=`, `GET /projects/{pid}/confidence?history=true` |
| **Findings Workspace** | Triage and act on findings across their lifecycle | Owner/member | `GET /projects/{pid}/findings`, `POST /findings/{fid}:acknowledge|:address|:close|:reopen` |
| ~~**Recommendation Workspace**~~ · **RETIRED (DL-088)** | Recommendations exist **only** as a contextual **Recommendation Panel opened from a Finding** (Panel Model — no orphan/standalone surface). Actions `POST /recommendations/{rid}:accept\|:reject\|:implement` are invoked from that panel | Owner/member | `GET /findings/{fid}/recommendations` |
| **Report Viewer** | View, version, publish, archive, export reports | Owner/member | `GET /projects/{pid}/reports`, `GET /reports/{rid}/snapshots`, `POST /projects/{pid}/reports`, `POST /reports/{rid}:publish|:archive` |
| **Shared Artifact Viewer** | Scoped read (view/comment) of a shared object | Share recipient (incl. external link) | `GET /shares/{sid}` (scoped), `GET` of shared object at `permission_level` |
| **Notification Center** | In-product awareness feed | Any member | `GET /notifications`, `POST /notifications/{nid}:view|:dismiss` |
| **User Settings** | Profile and workspace basics | Any member | `GET /workspace`, `GET /users/{uid}` |

## Supporting / embedded views (not standalone screens)

| View | Embedded in | Related APIs |
|---|---|---|
| Confidence Experience (history/trend/CAF drivers) | Project Workspace header → expand | `GET /projects/{pid}/confidence?history=true`, `GET /analysis-runs/{rid}/caf-state` |
| Activity / Comments thread | Project Workspace · Findings · Artifacts | `GET/POST /projects/{pid}/comments`, `POST /comments/{cid}/replies` |
| Sharing dialog | Project Workspace · Report Viewer | `POST /shares`, `POST /shares/{sid}:revoke`, `GET /shares` |
| Explainability panel | Findings · Recommendations · Confidence | finding/recommendation reads + `evidence_links` / `rationale` |

*Inventory reflects `RELEASE_1_UI_SPECIFICATION_V1.md` (with **DL-088** corrections). **12 primary screens** + 4 embedded views — #9 Recommendation Workspace **retired** (Panel Model; recommendations live in a contextual Recommendation Panel from a Finding). Findings/History are left-rail center-pane views; command palette deferred to R2. `RELEASE_1_UI_SPECIFICATION_V1.md` to reconcile #9 on next touch. All remaining screens map to API contract endpoints and v1.1 enums.*
