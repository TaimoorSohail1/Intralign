# Release 1 Event Model Specification v1

**Type:** Implementation artifact — the authoritative Release 1 event architecture (events, triggers, recompute, ordering, idempotency, dispatch)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Aligned with:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_DATA_STATE_RECONCILIATION_AUDIT.md` · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`

> Active Release 1 only. **No Governance Domain concepts** (no Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding), no Agent Governance, Execution Intelligence, Future Architecture, or Release 2. This document defines **what causes state transitions**. It does not define schema (Data Model), API design, UI, or governance behavior.
>
> **State vocabulary note.** This spec uses the **State Model** lifecycle names (the lifecycle authority). Where it touches a field still under reconciliation, it cites the backlog ID from `RELEASE_1_DATA_STATE_RECONCILIATION_AUDIT.md` (R-1…R-7).

---

## 1. Purpose

The Event Model is the **third leg** of the Release 1 lifecycle backbone:

- **Data Model → what exists** (entities, fields, relationships).
- **State Model → what state it can be in** (lifecycles, transitions, supersession).
- **Event Model → what causes state transitions** (the events, their triggers, and the deterministic recompute they drive).

It is an implementation artifact. It defines the event envelope, taxonomy, per-domain events with producers/consumers/resulting transitions, the deterministic recompute rules, and ordering/idempotency/dispatch semantics — so the event-driven, replayable behavior the two analysis horizons depend on is unambiguous.

---

## 2. Event Principles

- **Event-driven** — every state transition in the State Model is caused by exactly one event; nothing transitions on a timer except explicit expiry events.
- **Deterministic** — the same event applied to the same object state always yields the same transition and recompute (§15).
- **Replayable** — replaying the ordered event log reconstructs all current state and supersession chains.
- **Traceable** — every event carries its actor, source, and the object it acts on; every state change is attributable to an `event_id`.
- **Idempotent** — re-delivering an event produces no additional effect (§17).
- **Append-only** — the event log is immutable; corrections are new events, never edits. This is the runtime expression of the State Model's supersession-over-mutation principle.

---

## 3. Event Taxonomy

| Category | Purpose | Drives |
|---|---|---|
| **Project Events** | project lifecycle | Project state machine |
| **Artifact Events** | synthesized-artifact changes | Deep Analysis recompute |
| **Context Events** | evidence / context-item changes | Fast & Deep recompute |
| **Analysis Events** | Fast/Deep pass execution | AnalysisRun + Project states; emit all downstream |
| **Confidence Events** | confidence/CAF state creation & supersession | Confidence/CAF lifecycles |
| **Finding Events** | finding lifecycle | Finding state machine |
| **Recommendation Events** | recommendation lifecycle | Recommendation state machine |
| **Notification Events** | awareness lifecycle | Notification state machine (no analysis) |
| **Collaboration Events** | comments, mentions, shares | Notifications; may produce evidence |
| **Reporting Events** | report generation/publication | Report state machine |

All categories are scoped to a single workspace + project (except workspace-level Notification/Collaboration which carry both ids).

---

## 4. Event Envelope

Canonical structure for every event (implementation-oriented; field types owned by Data Model):

| Field | Meaning |
|---|---|
| `event_id` | Globally unique id; idempotency key |
| `event_type` | e.g. `deep_analysis_completed` |
| `timestamp` | Event-time (UTC) of occurrence |
| `workspace_id` | Owning workspace (tenancy boundary) |
| `project_id` | Owning project (nullable only for pure workspace events) |
| `actor` | `{type: user\|system, id}` — who/what caused it |
| `source` | Originating component or trigger (e.g. `chat`, `editor`, `scheduler`, `analysis_engine`) |
| `payload` | Type-specific body (ids of affected objects, run refs, etc.) |
| `causation_id` | (optional) `event_id` that caused this event — for chains |
| `correlation_id` | (optional) groups all events of one analysis cycle |

`event_id` + `event_type` together make every event idempotent and replayable; `causation_id`/`correlation_id` make a recompute cycle reconstructable end-to-end.

---

## 5. Project Events

| Event | Producer | Consumers | Resulting transition |
|---|---|---|---|
| `project_created` | User (surface) | Analysis scheduler, Notification | Project → **Draft** |
| `project_updated` | User | Knowledge Layer | none (metadata); may emit no recompute |
| `project_archived` | User | All project consumers | Project → **Archived** (terminal) |

`project_created` arms the Fast Analysis trigger (fires once first analyzable input exists, §15).

---

## 6. Artifact Events

| Event | Producer | Recompute implication |
|---|---|---|
| `artifact_created` | User / chat / editor | First analyzable artifact may satisfy the Fast Analysis precondition; thereafter qualifies for Deep Analysis |
| `artifact_updated` | User / chat / editor | **Substantive** update → qualifies for Deep Analysis (coalesced); trivial edits do not (§15) |
| `artifact_version_created` | Knowledge Layer | Append to ArtifactVersion chain; carries the substantive-change signal that Deep Analysis evaluates |

Artifact events never directly mutate Findings/Recommendations — they trigger an AnalysisRun, which does.

---

## 7. Context Events

| Event | Producer | Impact on analysis |
|---|---|---|
| `evidence_added` | User / ingestion | New evidence → Fast precondition (if first input) or Deep Analysis trigger |
| `context_item_added` | Context Plane (extraction) | Fast-horizon items feed orientation; deep-horizon items feed Deep Analysis |
| `context_item_updated` | Context Plane | Substantive change → Deep Analysis trigger (coalesced) |

Context events are the primary "new information" signal; per the active loop, only new action/evidence changes assessment.

---

## 8. Analysis Events  *(critical)*

| Event | Producer | Consumers | Resulting transition |
|---|---|---|---|
| `fast_analysis_requested` | Scheduler (on first input) | Analysis engine | AnalysisRun(fast) → **Queued**; Project → **Orientation Running** |
| `fast_analysis_started` | Analysis engine | — | AnalysisRun → **Running** |
| `fast_analysis_completed` | Analysis engine | Confidence, Finding, Recommendation, Notification | AnalysisRun → **Completed**; Project → **Orientation Complete**; emits `confidence_created`, initial `finding_created`*, `recommendation_created`* |
| `deep_analysis_requested` | Scheduler (on qualifying event) | Analysis engine | AnalysisRun(deep) → **Queued**; Project → **Deep Analysis Running** |
| `deep_analysis_started` | Analysis engine | — | AnalysisRun → **Running** |
| `deep_analysis_completed` | Analysis engine | Confidence, Finding, Recommendation, Notification | AnalysisRun → **Completed**; Project → **Deep Analysis Complete**; emits `confidence_recalculated`, Expanded `finding_created`*, Expanded `recommendation_created`*, and `*_superseded` as needed |
| `analysis_failed` | Analysis engine | Scheduler, Notification | AnalysisRun → **Failed**; Project reverts to last completed state; may emit retry `*_requested` (§17) |
| `analysis_cancelled` | User / system | Scheduler | AnalysisRun → **Cancelled** (cites **R-6**) |
| `analysis_superseded` | Scheduler | — | prior Completed AnalysisRun → **Superseded** when a newer run Completes |

\* downstream finding/recommendation events are emitted by the completing run, carrying `first_seen_run_id`.

---

## 9. Confidence Events

| Event | Producer | Resulting transition |
|---|---|---|
| `confidence_created` | Fast run completion | new ConfidenceState → **Current**; (no prior to supersede on first run) |
| `confidence_recalculated` | Deep run completion | new ConfidenceState → **Current** |
| `confidence_superseded` | emitted with recalculation | prior ConfidenceState → **Superseded** via `supersedes_confidence_state_id` |

Each completing run emits exactly one create/recalculate + (if a prior exists) one supersede — **supporting Confidence Recalculation** as a first-class event. CAF state changes mirror this (a `caf_state_created` / `caf_state_superseded` pair per run; CAF meaning unchanged).

---

## 10. Finding Events

| Event | Producer | Resulting transition |
|---|---|---|
| `finding_created` | Analysis run | Finding → **Detected** (deep run ⇒ Expanded Finding, `first_seen_run_id`=this run) |
| `finding_updated` | User / run | Detected→Acknowledged→Addressed (per actor) |
| `finding_closed` | User / run | Finding → **Closed** |
| `finding_reopened` | Run (new evidence) | Closed → **Reopened** |
| `finding_superseded` | Deep run | Finding → **Superseded** (cites **R-1**: requires the `superseded` value) |

**Supports Expanded Findings:** a `deep_analysis_completed` fans out into Expanded `finding_created` events. Findings remain descriptive — events change a finding's status, never its prescriptive nature.

---

## 11. Recommendation Events

| Event | Producer | Resulting transition |
|---|---|---|
| `recommendation_created` | Analysis run | Recommendation → **Generated** (deep ⇒ Expanded, `first_seen_run_id`) |
| `recommendation_accepted` | User | Generated/**Deferred** → **Accepted** |
| `recommendation_rejected` | User | Generated/**Deferred** → **Rejected** |
| `recommendation_deferred` 〔RS-R3 / Data Model v1.2〕 | User | Generated → **Deferred** (postponed; remains valid) |
| `recommendation_implemented` | User action + evidence | Accepted → **Implemented** |
| `recommendation_superseded` | Deep run | → **Superseded** (retained) |

**Supports Expanded Recommendations.** Recommendations remain advisory — accept/reject/implement are user choices surfaced as events; the recommendation never self-executes.

---

## 12. Notification Events

| Event | Producer | Resulting transition |
|---|---|---|
| `notification_created` | Source-object change | Notification → **Created** |
| `notification_viewed` | User | → **Viewed** |
| `notification_dismissed` | User | → **Dismissed** |
| `notification_expired` | Scheduler (aging) | → **Expired** (cites **R-3**) |

**Clarification:** notifications never drive analysis. A notification event has **zero** recompute consumers and never alters a Finding or Recommendation — it only surfaces awareness.

---

## 13. Collaboration Events

| Event | Producer | Effect |
|---|---|---|
| `comment_created` | User | Stateless thread entry; may emit `notification_created` for mentioned/owner users |
| `mention_created` | User (within comment) | emits `notification_created` to mentioned user |
| `artifact_shared` | User | SharedArtifact → **Shared** (cites **R-5** for status); emits `notification_created` |
| `share_revoked` | User | SharedArtifact → **Revoked** |
| `share_expired` | Scheduler | SharedArtifact → **Expired** |

Release 1 only (private/public-link + workspace visibility; view/comment permission). A collaboration event that introduces new evidence (e.g., a comment captured as context) may *separately* emit a Context Event that qualifies for Deep Analysis — the collaboration event itself does not.

---

## 14. Reporting Events

| Event | Producer | Resulting transition |
|---|---|---|
| `report_generated` | User / system | Report → **Draft**; new ReportSnapshot |
| `report_published` | User | Report → **Published** (cites **R-4** for status) |
| `report_superseded` | Newer publish | prior Report → **Superseded** (snapshot chain retained) |
| `report_archived` | User | Report → **Archived** |

---

## 14a. Clarification Event (information-capture — DL-089)

Clarification is **conversational information-capture**, not a modeled object (per `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1` §122). A user's answer to an OSLO clarification is captured as a **project-information change** (like an artifact edit / evidence add) and feeds the next reanalysis; it changes no assessment by itself.

| Event | Producer | Resulting transition |
|---|---|---|
| `clarification_answer_captured` | User | Project-information change recorded (Attested authorship) → marks analysis stale and **feeds the next Deep Analysis**. Payload `{answer_text, prompt_ref?, context_ref?}`. **No** Clarification object/lifecycle/disposition is created. |

*(Optional presentation-only `clarification_prompt_shown` — awareness that OSLO raised a prompt; **zero** recompute consumers — may be added if the surface needs it; otherwise the stale/pending analysis state suffices.)*

---

## 15. Recompute Rules  *(critical)*

Deterministic event→recompute mapping. **No-change → no-recompute:** an event that does not change evidence, artifacts, or context produces no run.

### Fast Analysis
Triggered by `project_created` **followed by** the first analyzable `artifact_created` / `evidence_added`.
**Rule:** emit `fast_analysis_requested` **iff** the project has **no completed fast run** AND ≥1 analyzable input. Exactly once per project.

### Deep Analysis
Triggered by: `fast_analysis_completed` (auto first deep pass); substantive `artifact_updated` / `artifact_version_created`; `context_item_added/updated`; `recommendation_implemented` (fix produced new evidence); `clarification_answer_captured` (DL-089); collaboration-derived Context Events; `manual` request.
**Rule:** on a qualifying event, **if no deep run is Running** for the project → emit `deep_analysis_requested`; **if one is Running** → set "deep pending" and **coalesce** subsequent qualifying events into a single next request (debounce window = calibration, §19). Trivial edits do not qualify.

### Confidence Recalculation
**Rule:** every `*_analysis_completed` emits `confidence_created` (first) or `confidence_recalculated` + `confidence_superseded` (subsequent). No standalone confidence recompute exists.

### Finding Expansion
**Rule:** a `deep_analysis_completed` evaluates understanding and emits Expanded `finding_created` (new findings, `first_seen_run_id`=this run) and `finding_updated`/`finding_superseded` for existing ones. Fast runs emit initial `finding_created` only.

### Recommendation Expansion
**Rule:** a `deep_analysis_completed` emits `recommendation_created` for new/updated findings and `recommendation_superseded` for replaced ones. Always tied to a Finding.

---

## 16. Event Ordering

- **Per-object ordering is total.** Events for a single object (`project_id`+entity id) are processed in `timestamp`, then `event_id`, order. A handler must not apply an event that is causally older than the object's current state (stale events are dropped — see idempotency).
- **Cross-object ordering is causal, not global.** Ordering is guaranteed only along `causation_id` chains; unrelated objects may process concurrently.
- **Sequencing within a run:** a completing run's fan-out is ordered `confidence_* → finding_* → recommendation_* → notification_*` (the §18 flow), sharing one `correlation_id`.
- **Duplicate handling:** duplicates (same `event_id`) are detected and ignored (§17); out-of-order non-duplicates for the same object are reordered by (`timestamp`,`event_id`) before application.

---

## 17. Idempotency Rules

- **Duplicate events:** processing is keyed on `event_id`; a second delivery is a no-op. Handlers record the last-applied `event_id` per object.
- **Replay:** replaying the ordered log from genesis reproduces identical current state and supersession chains (deterministic, §2). Replay must not emit external side effects (notifications/emails) — those are suppressed in replay mode.
- **Retry:** a failed delivery is retried with the **same** `event_id` (safe — idempotent). A failed **analysis run** does **not** retry in place; the scheduler emits a **new** `*_analysis_requested` (new run, linked `previous_run_id`), preserving the failed run. Retry bound = calibration (§19).
- **Effect idempotency:** state transitions are defined as "set to target state," not "increment," so re-application converges to the same state.

---

## 18. Event Flow Diagrams

**Orientation Flow**
```text
project_created
  → artifact_created / evidence_added        (first analyzable input)
  → fast_analysis_requested  → fast_analysis_started → fast_analysis_completed
       ├─ confidence_created                 (Initial Confidence — Current)
       ├─ finding_created × N                (Initial Findings — Detected)
       ├─ recommendation_created × M         (Initial Recommendations — Generated)
       └─ notification_created               (orientation ready)
  Project: Draft → Orientation Running → Orientation Complete
```

**Deep Analysis Flow**
```text
artifact_updated (substantive)               [coalesced if a deep run is running]
  → deep_analysis_requested → deep_analysis_started → deep_analysis_completed
       ├─ confidence_recalculated + confidence_superseded   (Confidence Recalculation)
       ├─ finding_created × k        (Expanded Findings, first_seen = this run)
       ├─ finding_superseded × j     (replaced findings)
       ├─ recommendation_created × p (Expanded Recommendations)
       ├─ recommendation_superseded × q
       └─ notification_created
  Project: Deep Analysis Running → Deep Analysis Complete
  (user acts → recommendation_implemented → new evidence → next deep cycle)
```

---

## 19. Open Questions  *(unresolved — not solved here)*

1. **Coalescing / debounce window** for Deep Analysis (timing) — calibration/ops.
2. **Retry bound + backoff** for failed runs and failed deliveries — calibration.
3. **"Substantive change" threshold** — what makes an `artifact_updated` qualify vs trivial — needs a rule from the analysis engine.
4. **Transport guarantees** — at-least-once vs exactly-once delivery, ordering buffer size — infra choice (this spec assumes at-least-once + idempotent handlers).
5. **Replay side-effect suppression** boundary — which effects are external vs internal.
6. **Concurrent deep runs** — single-active+coalesce assumed; parallelism is an implementation choice.
7. **Event retention** vs supersession/GDPR — owned by Data Model/ops.
8. Data/State reconciliation items **R-1, R-2, R-4, R-5, R-6** must land before the cited fields are persisted.

*Recorded for the API/NFR/operational specs and calibration track; not solved here.*

---

## 20. Validation

- Active Release 1 only — ✅
- No Governance concepts — ✅
- Supports Fast Analysis Pass — ✅ (§8, §15, §18)
- Supports Deep Analysis Pass — ✅ (§8, §15, §18)
- Supports Confidence Recalculation — ✅ (§9, §15)
- Supports Expanded Findings — ✅ (§10, §15)
- Supports Expanded Recommendations — ✅ (§11, §15)
- Supports Replayability — ✅ (§2, §17)
- Supports Event Ordering — ✅ (§16)
- Supports Idempotency — ✅ (§17)
- No Future Architecture introduced — ✅

**Release 1 Event Model Specification complete.**
