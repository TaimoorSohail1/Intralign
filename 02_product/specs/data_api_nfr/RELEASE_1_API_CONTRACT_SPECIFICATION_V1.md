# Release 1 API Contract Specification v1

**Type:** Implementation artifact — the authoritative Release 1 API & service-contract specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded exclusively in:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`

> **Scope guardrails.** Active Release 1 only. **No Governance Domain concepts, Future Architecture, Execution Intelligence, Agent Governance, or Autonomous Actions.** This spec introduces **no new entities, lifecycle states, or capabilities** — it exposes the existing architecture only. All resource names, enums, and events are used **exactly** as defined by the Data Model v1.1, State Model, and Event Model. Where a value is not yet defined upstream (e.g., latency targets), it is marked **TBD** — no benchmarks are invented.
>
> *Filename note: the Capability Matrix and Implementation Plan are cited by their actual repo names (`OSLO_CAPABILITY_MATRIX_V2.md`, `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`).*

The API exposes exactly one workflow and introduces no alternatives:

```text
Intent → Context Plane → Knowledge Layer → Planning Intelligence
→ Fast Analysis Pass → 60-Second Orientation
→ Deep Analysis Pass → Confidence Recalculation → Expanded Findings → Expanded Recommendations
```

---

## 1. Purpose

The API is the **command/query surface** over the Release 1 architecture. It exists so clients (web app, integrations) can drive and read the single understanding-improvement loop without bypassing it.

- **Relationship to the Data Model (v1.1):** API resources are the Data Model entities; request/response schemas use Data Model fields and enums verbatim. The API never persists anything the Data Model does not define.
- **Relationship to the State Model:** state-changing endpoints are **commands** that cause exactly the transitions the State Model defines; the API exposes no transition the State Model does not sanction.
- **Relationship to the Event Model:** every successful command **emits the Event Model event(s)** for that transition; the API does not invent events, and recompute is event-driven (§7, §8, §10).

The API is a thin contract over Data + State + Event — it adds interface, not architecture.

---

## 2. Architectural Style

- **REST**, resource-oriented, **JSON** request/response bodies, UTF-8.
- **Asynchronous analysis execution** — analysis is never synchronous; starting an analysis returns an `AnalysisRun` in `queued` and the client observes progress via polling (§11) or notifications.
- **Event-driven recomputation** — clients do not orchestrate recompute; they emit intent (add evidence, edit artifact) and the engine triggers runs per the Event Model recompute rules (§15 of the Event Model).

**Three interaction types:**

| Type | Definition | API form | Example |
|---|---|---|---|
| **Command** | A request that creates or changes state | `POST`/`PATCH`/`DELETE` on a resource or sub-action | `POST /projects`, `POST /analysis-runs:fast` |
| **Query** | A side-effect-free read | `GET` | `GET /projects/{id}/findings` |
| **Event** | A fact emitted *by the system* when state changes (not called by clients) | published to consumers (webhook/stream — transport TBD) | `deep_analysis_completed` |

Commands **emit** events; queries never do. Clients consume events but cannot publish them.

---

## 3. Authentication

- **User authentication:** bearer token (session/JWT) identifies the `user_id`. (Release 1 only — **SSO and enterprise auth are out of scope** and not designed here.)
- **Workspace scoping:** every authenticated request resolves to the caller's single `workspace_id` (Data Model §6 `User.workspace_id`, single-workspace per user in R1). All resource access is implicitly scoped to that workspace.
- **Tenant isolation:** the server filters every read/write by `workspace_id` (Data Model §16). A token for workspace A can never address resources in workspace B; the only cross-workspace path is a valid `SharedArtifact` (§12).

Roles (`owner`/`admin`/`member`, Data Model §6) gate privileged commands (e.g., archive project, revoke share). No external-reviewer role exists (governance/future — excluded).

---

## 4. Core Resource Inventory

Resources use **Data Model v1.1 names exactly**:

| Resource | Path root | Owner scope |
|---|---|---|
| Workspace | `/workspace` | tenant root (self) |
| User | `/users` | workspace |
| Project | `/projects` | workspace |
| Artifact | `/projects/{pid}/artifacts` | project |
| ArtifactVersion | `/artifacts/{aid}/versions` | artifact |
| Evidence | `/projects/{pid}/evidence` | project |
| ContextItem | `/projects/{pid}/context-items` | project (read-mostly; produced by runs) |
| AnalysisRun | `/projects/{pid}/analysis-runs` | project |
| CAFState | `/analysis-runs/{rid}/caf-state` | run (1:1) |
| ConfidenceState | `/analysis-runs/{rid}/confidence-state` | run (1:1) |
| Finding | `/projects/{pid}/findings` | project |
| Recommendation | `/findings/{fid}/recommendations` | finding |
| Notification | `/notifications` | workspace |
| Comment | `/projects/{pid}/comments` | project |
| Mention | `/comments/{cid}/mentions` | comment |
| SharedArtifact | `/shares` | workspace |
| Report | `/projects/{pid}/reports` | project |
| ReportSnapshot | `/reports/{rid}/snapshots` | report |

*(MRISnapshot and CAFOverlay are derived read resources, exposed under their AnalysisRun/Finding parents; ChatSession and TelemetryEvent are not part of the R1 public contract.)*

---

## 5. Command Endpoints

All commands: require auth (§3), are workspace-scoped, accept an `Idempotency-Key` header (§10), return the affected resource + the emitted event name(s). Transitions and events cite the State Model (SM) and Event Model (EM).

### Projects

| Command | Method + Endpoint | Request (key fields) | Response | Validation | Transition (SM) | Emits (EM) |
|---|---|---|---|---|---|---|
| Create Project | `POST /projects` | `{title?, description?}` | `Project` (`lifecycle_state=created`) | within free-tier active-project limit | — → **created** | `project_created` |
| Update Project | `PATCH /projects/{pid}` | `{title?, description?}` | `Project` | project not archived | none (metadata) | `project_updated` |
| Archive Project | `POST /projects/{pid}:archive` | — | `Project` (`archived`) | role owner/admin; not already archived | any → **archived** (terminal) | `project_archived` |

### Artifacts

| Command | Method + Endpoint | Request | Response | Validation | Transition | Emits |
|---|---|---|---|---|---|---|
| Create Artifact | `POST /projects/{pid}/artifacts` | `{artifact_type, content}` | `Artifact` + head `ArtifactVersion` | `artifact_type` ∈ Data Model enum | artifact `state=generated` | `artifact_created` (may satisfy Fast precondition) |
| Update Artifact | `PATCH /artifacts/{aid}` | `{state?}` | `Artifact` | valid artifact `state` value | artifact `state` transition | `artifact_updated` |
| Create Artifact Version | `POST /artifacts/{aid}/versions` | `{content, authored_by_kind}` | `ArtifactVersion` (new head) | monotonic `version_number`; `authored_by_kind` valid | append version chain | `artifact_version_created` (substantive ⇒ Deep trigger) |

### Evidence

| Command | Method + Endpoint | Request | Response | Validation | Transition | Emits |
|---|---|---|---|---|---|---|
| Add Evidence | `POST /projects/{pid}/evidence` | `{source_type, content_ref, provenance?}` | `Evidence` | `source_type` valid; project not archived | — | `evidence_added` (Fast precondition / Deep trigger) |
| Update Evidence | `PATCH /evidence/{eid}` | `{provenance?, content_ref?}` | `Evidence` | own-workspace | — | `evidence_added` (re-extraction) *(no separate update event in EM; treated as a context change)* |
| Remove Evidence | `DELETE /evidence/{eid}` | — | `204` | role member+; subject to retention policy (TBD, Data §20.5) | — | `evidence_added` superseding signal *(soft-remove; see §10)* |

### Analysis

| Command | Method + Endpoint | Request | Response | Validation | Transition (SM) | Emits (EM) |
|---|---|---|---|---|---|---|
| Start Fast Analysis | `POST /projects/{pid}/analysis-runs:fast` | — | `AnalysisRun` (`run_type=fast_analysis_pass`, `run_status=queued`) | project has ≥1 analyzable input AND no completed fast run (EM §15) | Project → **orienting**; run → **queued** | `fast_analysis_requested` |
| Start Deep Analysis | `POST /projects/{pid}/analysis-runs:deep` | `{trigger_source=manual}` | `AnalysisRun` (`deep_analysis_pass`, `queued`) | project `oriented`/`analyzed`; no deep run currently `running` (else coalesced) | Project → **deep_analyzing**; run → **queued** | `deep_analysis_requested` |
| Cancel Analysis | `POST /analysis-runs/{rid}:cancel` | — | `AnalysisRun` (`cancelled`) | run in `queued`/`running` | run → **cancelled** | `analysis_cancelled` |

### Findings

| Command | Method + Endpoint | Request | Response | Validation | Transition (SM §10) | Emits (EM §10) |
|---|---|---|---|---|---|---|
| Acknowledge Finding | `POST /findings/{fid}:acknowledge` | — | `Finding` (`acknowledged`) | status `detected` | detected → **acknowledged** | `finding_updated` |
| Address Finding | `POST /findings/{fid}:address` | — | `Finding` (`addressed`) | status `acknowledged` | acknowledged → **addressed** | `finding_updated` |
| Reopen Finding | `POST /findings/{fid}:reopen` | — | `Finding` (`reopened`) | status `closed` | closed → **reopened** | `finding_reopened` |

*(`finding_created`/`finding_closed`/`finding_superseded` are engine-produced via analysis runs, not direct client commands — §7. `Close` may be surfaced as `POST /findings/{fid}:close` from `addressed`, emitting `finding_closed`.)*

### Recommendations

| Command | Method + Endpoint | Request | Response | Validation | Transition (SM §11) | Emits (EM §11) |
|---|---|---|---|---|---|---|
| Accept Recommendation | `POST /recommendations/{rid}:accept` | — | `Recommendation` (`accepted`) | status `generated` | generated → **accepted** | `recommendation_accepted` |
| Reject Recommendation | `POST /recommendations/{rid}:reject` | — | `Recommendation` (`rejected`) | status `generated` | generated → **rejected** | `recommendation_rejected` |
| Defer Recommendation 〔RS-R3 / Data Model v1.2〕 | `POST /recommendations/{rid}:defer` | — | `Recommendation` (`deferred`) | status `generated` | generated → **deferred** | `recommendation_deferred` |
| Implement Recommendation | `POST /recommendations/{rid}:implement` | — | `Recommendation` (`implemented`) | status `accepted` | accepted → **implemented** | `recommendation_implemented` (→ new evidence ⇒ Deep trigger) |

### Collaboration

| Command | Method + Endpoint | Request | Response | Validation | Emits |
|---|---|---|---|---|---|
| Create Comment | `POST /projects/{pid}/comments` | `{target_type, target_id, body}` | `Comment` | `target_type` valid; target in workspace | `comment_created` (+`notification_created` to owner) |
| Reply To Comment | `POST /comments/{cid}/replies` | `{body}` | `Comment` (`parent_comment_id=cid`) | parent exists | `comment_created` |
| Mention User | (within comment body) `POST .../comments` w/ mentions | `{body, mentions:[user_id]}` | `Comment` + `Mention[]` | mentioned users in workspace | `mention_created` (+`notification_created`) |

### Sharing

| Command | Method + Endpoint | Request | Response | Validation | Transition (SM §14) | Emits (EM §13) |
|---|---|---|---|---|---|---|
| Create Share Link | `POST /shares` | `{shared_object_type, shared_object_id, visibility, permission_level, expires_at?}` | `SharedArtifact` (`shared`) | object in workspace; `permission_level` ∈ {view,comment} | created → **shared** | `artifact_shared` (+`notification_created`) |
| Revoke Share Link | `POST /shares/{sid}:revoke` | — | `SharedArtifact` (`revoked`) | role owner/admin or creator; status `shared`/`viewed` | → **revoked** | `share_revoked` |

### Reporting

| Command | Method + Endpoint | Request | Response | Validation | Transition (SM §13) | Emits (EM §14) |
|---|---|---|---|---|---|---|
| Generate Report | `POST /projects/{pid}/reports` | `{report_type, generated_from_run_id?, format}` | `Report` (`draft`) + `ReportSnapshot` | `report_type`/`format` valid; run belongs to project | → **draft** | `report_generated` |
| Publish Report | `POST /reports/{rid}:publish` | — | `Report` (`published`) | status `draft`; has snapshot | draft → **published** | `report_published` |
| Archive Report | `POST /reports/{rid}:archive` | — | `Report` (`archived`) | status `published`/`superseded` | → **archived** | `report_archived` |

---

## 6. Query Endpoints

All queries: workspace-scoped, support cursor pagination (`?cursor=&limit=` , default `limit=25`, max `100`), return `{data:[...], next_cursor}`. Filters listed per endpoint.

| Query | Endpoint | Parameters / Filters | Response |
|---|---|---|---|
| Get Project | `GET /projects/{pid}` | — | `Project` (incl. `lifecycle_state`, `current_confidence_state_id`) |
| List Projects | `GET /projects` | `?lifecycle_state=&cursor=&limit=` | `Project[]` |
| Get Analysis Run | `GET /analysis-runs/{rid}` | `?include=caf_state,confidence_state,mri_snapshot` | `AnalysisRun` (+ optional embeds) |
| List Analysis Runs | `GET /projects/{pid}/analysis-runs` | `?run_type=&run_status=&cursor=` | `AnalysisRun[]` (newest first) |
| Get Findings | `GET /projects/{pid}/findings` | `?status=&finding_type=&severity=&run_id=&first_seen_run_id=` | `Finding[]` |
| Get Recommendations | `GET /projects/{pid}/recommendations` *(or `/findings/{fid}/recommendations`)* | `?status=&recommendation_type=&finding_id=` | `Recommendation[]` |
| Get Confidence | `GET /projects/{pid}/confidence` | `?history=true` (returns supersession chain) | `ConfidenceState` (current) or chain |
| Get Notifications | `GET /notifications` | `?state=&project_id=&cursor=` | `Notification[]` |
| Get Reports | `GET /projects/{pid}/reports` | `?status=&report_type=` | `Report[]` (+ `current_snapshot_id`) |
| Get Shared Artifacts | `GET /shares` | `?status=&shared_object_type=` | `SharedArtifact[]` |
| Get Comments | `GET /projects/{pid}/comments` | `?target_type=&target_id=&parent_comment_id=` | `Comment[]` (threaded) |

Reads honor tenant isolation (§12); a shared-link reader sees only the shared object at its `permission_level`.

---

## 7. Analysis Contracts  *(critical)*

### Fast Analysis Pass

- **Inputs:** `project_id`; current Evidence + synthesized Artifacts/ArtifactVersions; fast-horizon ContextItems (Context Plane fast extraction).
- **Outputs:** one `AnalysisRun(fast_analysis_pass, completed)` → exactly one `CAFState`, one `ConfidenceState` (**Initial Confidence**), initial `Finding[]`, initial `Recommendation[]`, one `MRISnapshot`.
- **Expected states:** run `queued → running → completed`; Project `orienting → oriented` (State Model §6).
- **Expected events:** `fast_analysis_requested → fast_analysis_started → fast_analysis_completed`, then `confidence_created`, `finding_created`×N, `recommendation_created`×M, `notification_created` (Event Model §8/§18).
- **Latency target:** Time-to-First-MRI **< 60 seconds** (Canonical Scope / Master Spec §20 M1). Supported-project-size envelope for that target = **TBD** (not defined upstream; Data §20.1 / readiness audit D9).
- **Clarification:** Fast Analysis is **orientation, not final understanding.**

### Deep Analysis Pass

- **Inputs:** `project_id`; full Evidence/Artifacts; deep-horizon ContextItems (enrichment); prior run via `previous_run_id`.
- **Outputs:** one `AnalysisRun(deep_analysis_pass, completed)` → new `CAFState`, new `ConfidenceState` (**Confidence Recalculation**, supersedes prior), **Expanded Findings** (`first_seen_run_id`=this run), **Expanded Recommendations**, plus `*_superseded` where applicable.
- **Expected states:** run `queued → running → completed`; Project `deep_analyzing → analyzed` (recurring on events) (State Model §7).
- **Expected events:** `deep_analysis_requested → deep_analysis_started → deep_analysis_completed`, then `confidence_recalculated`+`confidence_superseded`, `finding_created`(expanded)/`finding_superseded`, `recommendation_created`(expanded)/`recommendation_superseded`, `notification_created`.
- **Latency target:** **TBD** (no quantified Deep Analysis latency target defined upstream; readiness audit D9). Not invented here.
- **Clarification:** Deep Analysis **improves understanding and performs no governance.**

**Explicitly contracted:**
- **Confidence Recalculation** = each completed run emits a new `ConfidenceState`; deep runs emit `confidence_recalculated`+`confidence_superseded`; readable via `GET /projects/{pid}/confidence?history=true`.
- **Expanded Findings** = `Finding`s whose `first_seen_run_id` is a deep run; readable via `GET .../findings?first_seen_run_id={deep_rid}`.
- **Expanded Recommendations** = `Recommendation`s with `first_seen_run_id` = a deep run; readable via the recommendations query.

---

## 8. Event Publication Contracts

Events are **produced by the system**, named per the Event Model. Envelope (Event Model §4): `event_id, event_type, timestamp, workspace_id, project_id, actor, source, payload, causation_id?, correlation_id?`. All events are **idempotent on `event_id`** (consumers dedupe; §10). Transport (webhook/stream) = TBD.

| Event | Producer | Consumers | Payload (key ids) | Idempotency |
|---|---|---|---|---|
| `project_created` | Project cmd | scheduler, notification | `project_id` | dedupe `event_id` |
| `artifact_created` | Artifact cmd | analysis scheduler | `artifact_id`, `version_id` | dedupe |
| `artifact_updated` | Artifact cmd | analysis scheduler | `artifact_id` | dedupe |
| `evidence_added` | Evidence cmd | context plane, scheduler | `evidence_id` | dedupe |
| `analysis_started`* | analysis engine | clients (polling), telemetry | `analysis_run_id`, `run_type` | dedupe |
| `analysis_completed`* | analysis engine | confidence/finding/recommendation, notification | `analysis_run_id`, `run_type` | dedupe; fan-out under one `correlation_id` |
| `analysis_failed` | analysis engine | scheduler, notification | `analysis_run_id`, `error_code` | dedupe; retry = new run |
| `analysis_cancelled` | cancel cmd / system | scheduler | `analysis_run_id` | dedupe |
| `finding_detected`** | analysis run | UI, notification | `finding_id`, `first_seen_run_id` | dedupe |
| `finding_acknowledged`** | acknowledge cmd | UI | `finding_id` | dedupe; set-to-state |
| `finding_addressed`** | address cmd | UI | `finding_id` | dedupe |
| `finding_closed` | close cmd / run | UI, notification | `finding_id` | dedupe |
| `finding_reopened` | run (new evidence) | UI, notification | `finding_id` | dedupe |
| `finding_superseded` | deep run | UI | `finding_id`, `superseded_by?` | dedupe |
| `recommendation_generated`** | analysis run | UI, notification | `recommendation_id`, `finding_id` | dedupe |
| `recommendation_accepted` | accept cmd | UI | `recommendation_id` | dedupe |
| `recommendation_deferred` 〔RS-R3〕 | defer cmd | UI | `recommendation_id` | dedupe |
| `recommendation_rejected` | reject cmd | UI | `recommendation_id` | dedupe |
| `recommendation_implemented` | implement cmd | scheduler (Deep trigger) | `recommendation_id` | dedupe |
| `recommendation_superseded` | deep run | UI | `recommendation_id` | dedupe |
| `comment_created` | comment cmd | notification | `comment_id`, `target_id` | dedupe |
| `mention_created` | mention cmd | notification | `mention_id`, `mentioned_user_id` | dedupe |
| `notification_created` | source-object change | notification surface | `notification_id`, `source_object_id` | dedupe; **never drives analysis** |
| `report_generated` | generate cmd | UI | `report_id`, `report_snapshot_id` | dedupe |

\* `analysis_started`/`analysis_completed` are the run-type-qualified events `fast_analysis_started`/`fast_analysis_completed`/`deep_analysis_started`/`deep_analysis_completed` (Event Model §8); listed here in the prompt's generic form.
\*\* Per the Event Model, finding/recommendation status changes are carried by the canonical `finding_created`/`finding_updated` and `recommendation_created` events with the resulting status in the payload. The granular names (`finding_detected/acknowledged/addressed`, `recommendation_generated`) are documented here as **status-specific facets** of those canonical events — **no new event types are introduced** beyond the Event Model.

---

## 9. Error Contracts

Standard error body:
```json
{ "error": { "code": "string", "message": "string", "details": [], "request_id": "uuid" } }
```

| HTTP | Code | When |
|---|---|---|
| 400 | `bad_request` | malformed JSON / missing required field |
| 401 | `unauthenticated` | missing/invalid token |
| 403 | `forbidden` | authenticated but not permitted (role/tenant/share scope) |
| 404 | `not_found` | resource absent or outside caller's workspace (isolation hides existence) |
| 409 | `conflict` | invalid state transition (e.g., acknowledge a non-`detected` finding; cancel a `completed` run) |
| 422 | `unprocessable_entity` | semantically invalid (e.g., free-tier active-project limit exceeded; `permission_level` not in {view,comment}) |
| 429 | `rate_limited` | rate/quota exceeded (incl. free-tier suggested-fix daily limit); includes `Retry-After` |
| 500 | `internal_error` | unexpected server fault |

Example 409:
```json
{ "error": { "code": "conflict", "message": "Finding f_123 is not in 'detected'; cannot acknowledge.", "details":[{"current_status":"addressed"}], "request_id":"..." } }
```

---

## 10. Idempotency

Aligned with Event Model §17.

- **Create behavior:** mutating commands accept an `Idempotency-Key` header; a repeated key returns the original result (no duplicate resource/event). Keys retained for a bounded window (TBD).
- **Retry behavior:** safe to retry any command with the same `Idempotency-Key`. A failed **analysis** is **not** retried in place — a new `AnalysisRun` is created (linked `previous_run_id`); the failed run is retained.
- **Event replay behavior:** consumers dedupe on `event_id`; replaying the event log reproduces identical state (set-to-state transitions). Replay suppresses external side effects (no re-notification).
- **Duplicate submission handling:** transitions are defined as "set to target state," so re-applying a command/event converges to the same state (no double-advance). Status commands on an already-target state return `200` (no-op) or `409` if the source state no longer matches.

---

## 11. Async Job Model

`AnalysisRun` is the async job. Lifecycle (Data Model §10 / State Model §5): `queued → running → completed`, plus `failed`, `cancelled`, `superseded`.

- **Creation:** `POST .../analysis-runs:fast|:deep` → `201` with run in `queued`; emits `*_analysis_requested`.
- **Polling:** `GET /analysis-runs/{rid}` returns current `run_status`; clients poll until terminal, or subscribe to `*_analysis_started/completed/failed`.
- **Completion:** engine sets `completed`, emits `*_analysis_completed` + fan-out (confidence/findings/recommendations). Prior current run → `superseded` (emits `analysis_superseded`).
- **Cancellation:** `POST /analysis-runs/{rid}:cancel` from `queued`/`running` → `cancelled`; emits `analysis_cancelled`. Terminal and retained.
- **Failure/recovery:** engine sets `failed` (emits `analysis_failed`); Project reverts to last completed state; retry = new run.

Terminal states: `completed`, `failed`, `cancelled`, `superseded`. No in-place restart.

---

## 12. Tenant Isolation

Per Data Model §16:

- **`workspace_id` boundary:** every resource carries/derives `workspace_id`; the server injects the caller's workspace into every query predicate. Cross-workspace reads/writes are impossible via the primary API.
- **Query constraints:** list/get endpoints implicitly filter by `workspace_id`; a resource in another workspace returns `404` (existence not leaked).
- **Sharing exception:** the **only** cross-workspace/anonymous access is via a valid `SharedArtifact` — scoped to one `shared_object_id`, at `permission_level` (view/comment), honoring `status` (`shared`/`viewed` only; `revoked`/`expired` → `403`/`404`) and `expires_at`.
- **No enterprise policy concepts** (no posture, tenancy policy, external-reviewer identity).

---

## 13. Performance Targets

| Surface | Target |
|---|---|
| Fast Analysis (Time-to-First-MRI) | **< 60 s** (Master Spec §20 / M1) |
| Fast Analysis supported-size envelope | **TBD** (undefined upstream — Data §20.1) |
| Deep Analysis latency | **TBD** (no upstream target) |
| API response (reads/commands, non-analysis) | **TBD** (no upstream SLO) |
| Notification surfacing | **TBD** |
| Report generation | **TBD** |

No benchmarks invented. TBD items are owned by a forthcoming Performance/NFR specification (readiness audit D9).

---

## 14. Security Considerations

Release 1 only:

- **Authorization:** role-gated commands (owner/admin/member); least-privilege defaults.
- **Tenant isolation:** §12 (`workspace_id` on every operation).
- **Share-link access:** scoped, revocable, optionally-expiring; `permission_level` enforced; revoked/expired links denied.
- **Input validation:** all enums validated against Data Model; reject unknown fields; size limits on `content_ref`/`body` (limits TBD).
- **Rate limiting:** per-user/per-workspace limits incl. free-tier suggested-fix daily cap (`429` + `Retry-After`).
- **Auditability:** state-changing commands emit events (immutable log) and write `TelemetryEvent`s; supersession chains preserve history.

**No compliance frameworks introduced** (SOC 2 / GDPR posture are referenced by the Master Spec security baseline but are not designed here).

---

## 15. API Versioning Strategy

- **v1:** all endpoints under `/v1`. Reconciled Data Model v1.1 enums are the v1 contract vocabulary.
- **Future compatibility:** additive changes (new optional fields, new enum values such as a future `delivered` notification state or `verified` recommendation sub-flag) ship within `v1` and must be tolerated by clients (ignore-unknown). Breaking changes (removing/renaming a field or enum value) require `/v2`.
- **Deprecation:** deprecated fields are marked in responses (`Deprecation`/`Sunset` headers) and documented in the endpoint catalog for ≥1 minor cycle before removal. Keep simple — no parallel long-lived majors in R1.

---

## Validation

- No Governance Domain concepts — ✅
- No Future Architecture concepts — ✅
- No Agent Governance — ✅
- No Execution Intelligence — ✅
- No new entities — ✅ (resources = Data Model v1.1 entities)
- No new states — ✅ (enums used verbatim)
- No new capabilities — ✅ (exposes existing workflow only)
- Fast Analysis supported — ✅ (§5, §7)
- Deep Analysis supported — ✅ (§5, §7)
- Confidence Recalculation supported — ✅ (§7, §8)
- Expanded Findings supported — ✅ (§7, §8)
- Expanded Recommendations supported — ✅ (§7, §8)
- Event Model alignment preserved — ✅ (§8; no new event types)
- Data Model alignment preserved — ✅ (§4; v1.1 names/enums)
- State Model alignment preserved — ✅ (§5, §11; sanctioned transitions only)

**Release 1 API Contract Specification complete.**
