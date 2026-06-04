# Release 1 UI Specification v1

**Type:** Implementation artifact — the authoritative Release 1 UI specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded exclusively in:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md`

> **Scope guardrails.** Active Release 1 only. **No Governance Domain concepts, Future Architecture, Agent Governance, or Execution Intelligence.** This spec introduces **no new capabilities, workflows, entities, or lifecycle states** — it presents the architecture already defined. All entity states shown are the Data Model v1.1 / State Model enums verbatim; all refresh triggers are Event Model events; all data flows are API contract endpoints.

**The UI exists to make one journey obvious:**

```text
Intent → Context Collection → Fast Analysis Pass → 60-Second Orientation
→ Deep Analysis Pass → Confidence Recalculation → Expanded Findings → Expanded Recommendations
→ Improved Understanding
```

Internal architectural complexity (Context Plane, Knowledge Layer, Planning Intelligence, run chains) is **not** surfaced as such; the user sees projects, confidence, findings, recommendations, and reports.

---

## 1. UX Principles

- **Clarity over complexity** — present understanding, not architecture; one primary action per screen state.
- **Explainability** — every confidence value, finding, and recommendation can be traced to its basis (evidence/context/run) on demand.
- **Progressive disclosure** — orientation first (60s), depth on request; advanced detail (run history, supersession chains) behind expanders.
- **Confidence transparency** — confidence and its CAF drivers are always visible and always reliability-qualified; never a bare number without its qualifier.
- **Finding-centric workflow** — findings are the governable unit the user acts on; the UI is organized around moving findings through their lifecycle.
- **Recommendation-centric improvement** — recommendations are the prescriptive path; accepting/implementing them is the core improvement loop.
- **Event-driven refresh** — screens update from Event Model events (§20); the user never manually "re-runs analysis" to see new state.

---

## 2. Information Architecture

Primary navigation (persistent left rail / mobile drawer):

```text
OSLO
├── Projects            (default landing; list + create)
│     └── Project Workspace
│            ├── Orientation / Analysis
│            ├── Findings
│            ├── Recommendations
│            ├── Reports
│            └── Activity (comments)
├── Findings            (cross-project, current project context)
├── Recommendations     (cross-project, current project context)
├── Reports
├── Shared Artifacts
└── Notifications       (badge count)
User menu → Settings
```

Hierarchy: **Workspace → Project → (Artifacts, Analysis/Confidence, Findings → Recommendations, Reports, Comments)**. Findings/Recommendations/Reports/Shared/Notifications are top-level entries that resolve within the active project (or workspace, for Shared/Notifications) — mirroring the API resource scoping (§4 of the contract).

---

## 3. Screen Inventory

| # | Screen | One-line purpose |
|---|---|---|
| 1 | **Dashboard** | Entry: active project(s), latest confidence, attention items |
| 2 | **Project Creation** | Create a project and add first intent/evidence |
| 3 | **Project Workspace** | Hub for one project: artifacts, analysis, findings, recs, activity |
| 4 | **Artifact Editor** | View/edit a planning artifact + its versions |
| 5 | **Analysis Progress** | Async run status (fast/deep) while running |
| 6 | **60-Second Orientation** | First understanding: confidence, CAF, top findings/recs |
| 7 | **Deep Analysis Results** | Expanded findings/recs + recalculated confidence |
| 8 | **Findings Workspace** | Triage/act on findings across their lifecycle |
| 9 | **Recommendation Workspace** | Accept/reject/implement recommendations |
| 10 | **Report Viewer** | View/version/export reports |
| 11 | **Shared Artifact Viewer** | Scoped read (view/comment) of a shared object |
| 12 | **Notification Center** | Awareness feed |
| 13 | **User Settings** | Profile, workspace basics |

These 13 cover the full Canonical Scope journey; no additional screens are introduced.

---

## 4. Dashboard

- **Purpose:** orient the user on landing — what project is active, how confident OSLO is, and what needs attention.
- **Displayed information:** active project card(s) with `lifecycle_state` badge and current `ConfidenceState` (value + band + reliability qualifier); counts of open findings (by severity) and pending recommendations; recent notifications.
- **Primary actions:** Open project · Create project · View notifications.
- **Empty state:** no projects → single prominent "Create your first project" CTA + one-line description of the journey.
- **Loading state:** skeleton cards for project + confidence (§16).
- **Error state:** if dashboard data fails, inline retry banner (API error model §17); partial data renders what loaded.
- **Mobile:** single-column stacked cards; confidence and attention counts prioritized above the fold.

Data: `GET /projects`, `GET /projects/{pid}/confidence`, `GET /notifications`.

---

## 5. Project Creation Experience

- **User flow:** Create → name (optional) → add initial intent/evidence → system auto-triggers Fast Analysis → lands on Analysis Progress → 60-Second Orientation.
- **Fields:** `title` (optional — OSLO may infer), `description` (optional), initial intent/evidence (free text or upload; maps to `Evidence.source_type`).
- **Validation:** free-tier active-project limit (one active project) → `422` surfaced as "Archive your current project to start a new one"; evidence size limits (TBD).
- **Save behavior:** `POST /projects` (→ `Project.lifecycle_state=created`), then `POST /projects/{pid}/evidence`. First analyzable input arms Fast Analysis; the client calls `POST /projects/{pid}/analysis-runs:fast` (or the server auto-requests per Event Model §15).
- **API interactions:** `project_created`, `evidence_added`, `fast_analysis_requested` events observed.
- **Resulting transitions:** `created → orienting` (Project) on fast run start.

---

## 6. Project Workspace

- **Layout:** persistent project header (title, `lifecycle_state` badge, current confidence chip) + left sub-nav (Orientation/Analysis · Findings · Recommendations · Reports · Activity) + main content + right context panel (explainability/evidence).
- **Sections:** Orientation/Analysis (screens 5–7), Findings (9), Recommendations (10), Reports (13), Activity (comments §14).
- **Artifact access:** artifacts listed with `artifact_type` and `state`; open → Artifact Editor (screen 4).
- **Analysis controls:** "Run Deep Analysis" (manual `:deep`) when project is `oriented`/`analyzed`; runs are otherwise event-driven. Cancel available while `queued`/`running`.
- **Confidence visibility:** current confidence chip always in header; click → Confidence Experience (§11).
- **Finding visibility:** open-findings summary by severity; click → Findings Workspace.
- **Recommendation visibility:** pending-recommendations summary; click → Recommendation Workspace.
- **Activity visibility:** recent comments/mentions in the Activity tab.

Data: `GET /projects/{pid}` (+ artifacts, findings, recommendations, confidence, comments).

---

## 7. 60-Second Orientation Screen  *(critical)*

The payoff of the Fast Analysis Pass. Renders as soon as the fast run completes.

- **Displayed confidence:** the initial `ConfidenceState` — `outcome_confidence_value` + `confidence_band` + `reliability_qualifier`, presented as a single transparent confidence statement.
- **CAF visibility:** the three first-class dimensions from `CAFState` — Clarity, Alignment, Feasibility — each with its index and per-dimension reliability qualifier. No other dimensions are shown (CAF model is authoritative; none invented).
- **Top findings:** highest-severity initial `Finding`s (status `detected`), with type and affected dimension(s).
- **Top recommendations:** initial `Recommendation`s (status `generated`) tied to those findings.
- **Evidence summary:** count/sources of `Evidence` and key fast-horizon `ContextItem`s that fed orientation.
- **Analysis status:** a persistent banner — **"This is your 60-Second Orientation, not final analysis. Deep Analysis is in progress."** — reflecting that Project is `oriented` and a deep run is queued/running.
- **User actions:** acknowledge a finding, accept/reject a recommendation, open explainability, add more evidence, or run/await Deep Analysis.
- **Explainability behavior:** each item expands to show its basis (linked evidence/context + producing run) from stored lineage — no recomputation.

**Explicitly stated on-screen:** this is **not** final analysis; **Deep Analysis remains in progress.**

Data: `GET /analysis-runs/{rid}?include=caf_state,confidence_state,mri_snapshot`, `GET .../findings?status=detected`, `GET .../recommendations?status=generated`.

---

## 8. Deep Analysis Experience

- **Progress indicators:** Analysis Progress (screen 5) shows the deep run `queued → running`; non-blocking — the user keeps working while it runs.
- **Expanded findings:** on `deep_analysis_completed`, new `Finding`s (`first_seen_run_id` = this deep run) appear flagged "New from Deep Analysis."
- **Expanded recommendations:** new `Recommendation`s similarly flagged.
- **Confidence recalculation:** the header confidence chip updates to the new `ConfidenceState`; a "recalculated" indicator links to the change vs the superseded value.
- **Analysis history / run history:** a timeline of `AnalysisRun`s (fast → deep → deep…) with `run_type`, `run_status`, timestamps; selecting a run shows its CAF/confidence/findings snapshot (replay).
- **Refresh behavior / event-driven updates:** the screen subscribes to deep-analysis events and updates in place (§20) — no manual reload.

Data: `GET /projects/{pid}/analysis-runs`, `GET .../findings?first_seen_run_id=`, `GET /projects/{pid}/confidence?history=true`.

---

## 9. Findings Workspace

- **Finding lifecycle visibility:** each finding shows its State Model status — **Detected · Acknowledged · Addressed · Closed · Reopened · Superseded** (Data Model v1.1 enum).
- **Filters:** by `status`, `finding_type` (the 7-type taxonomy), `severity` (critical/moderate/warning), `first_seen_run_id` (e.g., "new from deep run").
- **Sorting:** by severity, recency (`last_updated_run_id`), or lifecycle status.
- **Grouping:** by affected CAF dimension, by severity, or by artifact location.
- **Acknowledge / Address / Close / Reopen:** action buttons mapped to `:acknowledge`/`:address`/`:close`/`:reopen`, each enabled **only** when the source state is legal (Detected→Acknowledge, Acknowledged→Address, Addressed→Close, Closed→Reopen); illegal actions hidden/disabled (mirrors API `409`).
- **Supersession visibility:** `superseded` findings shown in a collapsed "Superseded" group with a link to the superseding finding/run; never deleted.
- **Traceability / evidence linkage:** each finding expands to its `evidence_links` (evidence/context items) and producing run — the explainability path.

Findings are **descriptive** — the UI presents them as observations, never as actions taken.

Data: `GET /projects/{pid}/findings`, finding `:verb` commands.

---

## 10. Recommendation Workspace

- **Recommendation lifecycle visibility:** status shown as **Generated · Accepted · Rejected · Implemented · Superseded** (v1.1 enum).
- **Accept / Reject / Implement:** buttons mapped to `:accept`/`:reject`/`:implement`, enabled only on legal source states (Generated→Accept/Reject, Accepted→Implement).
- **Supersede:** `superseded` recommendations shown collapsed with link to the replacement; produced by deep runs, not a user action.
- **Finding linkage:** every recommendation shows its parent `Finding` (and that finding's status).
- **Confidence linkage:** shows which CAF dimension it's expected to improve (`expected_dimension`) and, after implementation + next run, the confidence movement.
- **Explainability:** expands to `rationale` and the basis (finding + evidence + run).

Recommendations are **advisory** — the UI frames accept/implement as user choices; nothing auto-applies.

Data: `GET /projects/{pid}/recommendations` (or per-finding), recommendation `:verb` commands.

---

## 11. Confidence Experience

- **Confidence display:** current `ConfidenceState` — value, `confidence_band`, `reliability_qualifier` — as a transparent statement.
- **Confidence history:** the supersession chain (`supersedes_confidence_state_id`) as an ordered timeline.
- **Confidence recalculation visibility:** each entry maps to the `AnalysisRun` that produced it (fast vs deep), so the user sees confidence evolve fast → deep → deep.
- **Trend visualization:** a simple line/step trend across runs (no invented metrics — points are stored `outcome_confidence_value`s, each reliability-qualified).
- **Driver breakdown:** the three CAF dimensions (Clarity/Alignment/Feasibility) with their indices and reliability qualifiers from `CAFState`.
- **Evidence drilldown:** from a driver → the findings affecting that dimension → their evidence/context.

**No new scoring dimensions** — only the existing CAF and Confidence models are displayed.

Data: `GET /projects/{pid}/confidence?history=true`, `GET /analysis-runs/{rid}/caf-state`.

---

## 12. Notifications

- **Notification center:** workspace-scoped feed of `Notification`s, newest first, with an unread badge.
- **States shown:** **Created (unread) · Viewed · Dismissed · Expired** (v1.1 enum) — `:view` and `:dismiss` actions; expired items shown in a collapsed history group.
- **Presentation behavior:** each notice shows its `source_object_type`/`event_type` and links to the source (finding/recommendation/run/comment/share). Notifications **never** trigger analysis.
- **Refresh behavior:** updates on `notification_created`/`viewed`/`dismissed`/`expired` events (§20).
- **No delivery-channel concepts** — **no email, SMS, or Slack.** Release 1 notifications are in-product awareness only.

Data: `GET /notifications`, `POST /notifications/{nid}:view|:dismiss`.

---

## 13. Reporting Experience

- **Report creation:** "Generate Report" → choose `report_type` (executive_summary / charter_report / mri_export / analytics) and `format` (pdf/html/json) → `POST /projects/{pid}/reports` (→ `draft`).
- **Report viewing:** Report Viewer renders the current `ReportSnapshot`.
- **Report history / versions:** the `ReportSnapshot` version chain, each pinned to the `AnalysisRun` it reflects (replay-accurate).
- **Published state:** "Publish" → `published` (with `published_snapshot_id`); publishing a newer snapshot moves the prior report to `superseded`.
- **Archived state:** "Archive" → `archived`.
- **Export UX:** download the snapshot in its `format`; share via the sharing flow (§14).

States shown: **Draft · Published · Superseded · Archived** (v1.1 enum).

Data: `GET /projects/{pid}/reports`, `GET /reports/{rid}/snapshots`, report `:verb` commands.

---

## 14. Collaboration Experience

- **Comments / replies:** threaded comments on artifacts, artifact versions, findings, or the project (`target_type`); reply inline.
- **Mentions:** @-mention workspace users in a comment → generates a notification to the mentioned user.
- **Shared artifacts:** share a project/artifact/MRI snapshot/report via a link with `visibility` (private_link/public_link/workspace) and `permission_level`.
- **View vs comment permissions:** **view** = read-only; **comment** = read + comment. (Only these two R1 levels; no others.)
- **Sharing UX:** create link → shows status **Created · Shared · Viewed · Revoked · Expired** (v1.1 enum); revoke disables access; optional expiry.

Uses existing R1 collaboration capabilities only (Comment/Mention/SharedArtifact).

Data: `GET/POST /projects/{pid}/comments`, `POST /shares`, `POST /shares/{sid}:revoke`.

---

## 15. State Presentation Rules

All labels map 1:1 to State Model / Data Model v1.1 enums; the UI shows no state the models don't define.

| Entity | Visible states (label) | Transition behavior in UI |
|---|---|---|
| **Project** | Draft · Orienting · Oriented · Deep Analyzing · Analyzed · Archived | badge follows `lifecycle_state`; archive is terminal |
| **AnalysisRun** | Queued · Running · Completed · Failed · Cancelled · Superseded | progress UI for queued/running; terminal states final; cancel only while queued/running |
| **Finding** | Detected · Acknowledged · Addressed · Closed · Reopened · Superseded | action buttons enabled only on legal source state; superseded collapsed |
| **Recommendation** | Generated · Accepted · Rejected · Implemented · Superseded | accept/reject from generated; implement from accepted; superseded collapsed |
| **Notification** | Created (unread) · Viewed · Dismissed · Expired | view/dismiss actions; expired in history |
| **Report** | Draft · Published · Superseded · Archived | publish from draft; archive from published/superseded |
| **SharedArtifact** | Created · Shared · Viewed · Revoked · Expired | revoke from shared/viewed; revoked/expired deny access |

Illegal transitions are never offered (prevents the API `409` path).

---

## 16. Loading States

- **Fast Analysis loading:** Analysis Progress with a "Building your 60-Second Orientation" indicator; target < 60s (Master Spec §20). If exceeded, show continued-progress messaging (no fake completion).
- **Deep Analysis loading:** non-blocking inline indicator on the analysis area + run-history "running" row; user keeps working.
- **Report generation loading:** spinner on the report card until `draft` snapshot ready.
- **Refresh loading:** subtle in-place update indicators on event-driven refresh (no full-page reload).
- **Empty states:** per screen (no projects, no findings yet, no recommendations yet, no reports, no notifications) — each with a one-line explanation tied to the journey.
- **Skeleton states:** cards/lists render skeletons while initial data loads.

---

## 17. Error States

Aligned to the API Contract error model (§9):

| Condition | UI behavior |
|---|---|
| **Validation (400/422)** | inline field errors; e.g., free-tier limit → archive-prompt |
| **Unauthenticated (401)** | redirect to sign-in |
| **Permission (403)** | "You don't have access" with role/share context; hide unavailable actions |
| **Not found (404)** | "Not found or outside your workspace" (isolation-respecting) |
| **Conflict (409)** | "This item changed — refresh" (illegal transition); auto-refresh the item |
| **Rate limited (429)** | show `Retry-After`; for free-tier fix cap, explain the daily limit |
| **Server (500)** | non-destructive error banner + retry |
| **Analysis failure (`analysis_failed`)** | run row shows Failed; offer "Retry analysis" (creates a new run); prior state preserved |
| **Timeouts** | retry affordance; never lose unsaved edits |

Retry UX uses the same `Idempotency-Key` contract (safe retries).

---

## 18. Accessibility (Release 1 level)

- **Keyboard navigation:** all primary actions and nav reachable/operable by keyboard; logical tab order.
- **Screen reader support:** semantic landmarks, labeled controls, ARIA live regions for event-driven updates (e.g., "Deep Analysis complete, confidence updated").
- **Color independence:** confidence bands, severities, and states conveyed by label/icon + color, never color alone.
- **Focus management:** focus moves predictably on navigation, modal open/close, and async completion.
- **Responsive behavior:** content reflows to small viewports without loss of function (§19).

---

## 19. Mobile & Responsive

- **Supported experiences:** dashboard, viewing orientation/confidence/findings/recommendations, acting on findings/recommendations (acknowledge/accept/etc.), notifications, report viewing, shared-artifact viewing.
- **Unsupported (read-optimized) on small screens:** heavy artifact editing and complex report authoring are de-prioritized (view-first; full editing is a desktop/tablet experience).
- **Responsive priorities:** confidence + attention items first; single-column stacking; touch-sized actions.
- **Tablet:** near-desktop layout (two-pane workspace) where width allows.

---

## 20. UI / Event Integration

The UI subscribes to Event Model events and updates the relevant screen region in place (no manual refresh). Mapping:

| Event | Screen update |
|---|---|
| `fast_analysis_started` / `_completed` | Analysis Progress → 60-Second Orientation renders (confidence/CAF/findings/recs) |
| `deep_analysis_started` / `_completed` | inline progress → Deep Analysis results; header confidence chip updates |
| `analysis_failed` | run row → Failed; retry affordance (§17) |
| `analysis_cancelled` | run row → Cancelled |
| `confidence_recalculated` / `confidence_superseded` | confidence chip + Confidence Experience timeline update |
| `finding_created` | Findings Workspace prepends (flagged "new from deep" if deep run) |
| `finding_updated` / `_closed` / `_reopened` / `_superseded` | finding row status updates in place |
| `recommendation_created` | Recommendation Workspace prepends |
| `recommendation_accepted` / `_rejected` / `_implemented` / `_superseded` | rec row status updates |
| `comment_created` / `mention_created` | Activity tab + notification badge |
| `notification_created` / `_viewed` / `_dismissed` / `_expired` | Notification Center + badge |
| `report_generated` / `_published` / `_superseded` / `_archived` | Reports list + Report Viewer status |

**Refresh behavior:** event-driven in-place updates are the default; an explicit manual refresh is available as a fallback. Replayed/duplicate events are deduped (idempotent UI updates — set-to-state, matching the API/Event contract).

---

## Validation

- No Governance concepts — ✅
- No Future Architecture — ✅
- No new capabilities — ✅
- No new workflows — ✅ (single journey only)
- Fast Analysis supported — ✅ (§5, §7)
- Deep Analysis supported — ✅ (§8)
- 60-Second Orientation supported — ✅ (§7, with "not final" banner)
- Confidence Recalculation supported — ✅ (§8, §11)
- Expanded Findings supported — ✅ (§8, §9)
- Expanded Recommendations supported — ✅ (§8, §10)
- State Model alignment preserved — ✅ (§15; enums verbatim)
- Event Model alignment preserved — ✅ (§20; no new events)
- API Contract alignment preserved — ✅ (every data flow = a contract endpoint)

**Release 1 UI Specification complete.**
