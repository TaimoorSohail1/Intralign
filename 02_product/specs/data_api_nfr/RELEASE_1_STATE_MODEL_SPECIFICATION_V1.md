# Release 1 State Model Specification v1

**Type:** Implementation artifact — the authoritative Release 1 lifecycle & state-behavior specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Aligned with:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`

> **Scope guardrails.** Active Release 1 only. **No Governance Domain concepts** (no Resolution Candidate, Review Request Model, Disposition, Governance, Accepted Understanding), no Agent Governance, Execution Intelligence, Future Architecture, or Release 2. This document defines **lifecycle behavior, state transitions, recomputation, supersession, and event-triggered state changes**. It does **not** define database schema (the Data Model owns that), API, UI, or governance behavior.
>
> **Authority note.** This is the **lifecycle authority**. Where a state name here differs from an enum value in `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md`, this document governs the *behavior* and the Data Model's enum should be reconciled to it (see the post-document "Recommended Data Model updates"). Each state machine below includes a **Data-Model mapping**.

---

## 1. Purpose

This document defines **how Release 1 objects behave over time**: their lifecycle states, the events that transition them, how analysis recomputes, and how history is preserved through supersession. It is an **implementation artifact**, not doctrine. It is the **lifecycle authority** and the **behavior authority** for Release 1, and it **complements the Data Model**: the Data Model defines *what is stored* (entities, fields, relationships); this document defines *how those entities move between states and when*. The conceptual models (Finding, Recommendation, Notification, CAF, Confidence) define *meaning*; this document does not redefine them — it specifies their Release 1 runtime behavior.

---

## 2. State Modeling Principles

- **Event-driven** — every state change is caused by an event (creation, evidence/artifact change, run completion, user action); no transition occurs on the passage of time alone (except explicit expiry).
- **Replayable** — state history is reconstructable from supersession chains and per-run snapshots.
- **Deterministic** — given the same object state and the same event, the resulting transition is always the same (§15 rules).
- **Traceable** — every transition is attributable to a triggering event/run.
- **Append-friendly** — new states/runs are appended; prior states are retained.
- **Supersession over mutation** — history-bearing objects (runs, CAF/Confidence states, findings, recommendations, reports) are superseded via pointers, never destructively overwritten.
- **Explainable** — current state + its supersession chain explain "what is true now and what changed."

---

## 3. State Model Inventory

| Object | Purpose of its state machine | Lifecycle Owner | Release 1 Status |
|---|---|---|---|
| **Project** | Track a project from draft through orientation and deep analysis to archive | Workspace/User | ✅ Active |
| **Analysis Run** | Track a Fast/Deep analysis pass execution | Project | ✅ Active |
| **CAF State** | Current/superseded/historical CAF per run | Analysis Run | ✅ Active |
| **Confidence State** | Current/superseded/historical confidence per run | Analysis Run | ✅ Active |
| **Finding** | Lifecycle of an observation about understanding | Project | ✅ Active |
| **Recommendation** | Lifecycle of an advisory improvement | Project | ✅ Active |
| **Notification** | Awareness lifecycle | Workspace | ✅ Active |
| **Report** | Report draft → publish → supersede → archive | Project | ✅ Active |
| **Shared Artifact** | Share link lifecycle | Workspace | ✅ Active |

---

## 4. Project Lifecycle

**States:** `Draft → Orientation Running → Orientation Complete → Deep Analysis Running → Deep Analysis Complete → Archived`
*(Deep Analysis Running ↔ Deep Analysis Complete may cycle as event-driven deep runs recur.)*

| State | Entry criteria | Exit criteria |
|---|---|---|
| **Draft** | Project created; no analyzable input yet | First analyzable input (evidence/synthesized artifact) present |
| **Orientation Running** | Fast Analysis Pass started | Fast run completes (or fails) |
| **Orientation Complete** | Fast run completed; 60-Second Orientation produced | First Deep Analysis Pass starts |
| **Deep Analysis Running** | A Deep Analysis Pass is active | Deep run completes (or fails) |
| **Deep Analysis Complete** | A Deep run completed | A new qualifying event starts another Deep run; or project is archived |
| **Archived** | User archives the project | (terminal in R1) |

**Allowed transitions:** Draft→Orientation Running; Orientation Running→Orientation Complete; Orientation Complete→Deep Analysis Running; Deep Analysis Running→Deep Analysis Complete; Deep Analysis Complete→Deep Analysis Running (recurring deep analysis); {Orientation Complete, Deep Analysis Complete}→Archived.
**Invalid transitions (examples):** Draft→Deep Analysis Running (must orient first); Draft→Archived only if never analyzed is allowed but Archived is terminal; Archived→any (no un-archive in R1); Orientation Running→Deep Analysis Running (orientation must complete first).
**Failure:** Orientation Running→(fail)→Draft (retry re-orients); Deep Analysis Running→(fail)→Deep Analysis Complete of the prior run (last good state) — see §17.
**Data-Model mapping:** `Project.lifecycle_state`: Draft=`created`, Orientation Running=`orienting`, Orientation Complete=`oriented`, Deep Analysis Running=`deep_analyzing`, Deep Analysis Complete=`analyzed`, Archived=`archived`. *(Recommend renaming the enum to the state names — see post-doc.)*

---

## 5. Analysis Run Lifecycle

**States:** `Queued → Running → Completed`, plus `Failed`, `Cancelled`, `Superseded`.

| State | Meaning |
|---|---|
| **Queued** | Run created and waiting to execute |
| **Running** | Executing |
| **Completed** | Finished successfully; produced CAFState + ConfidenceState + findings/recs |
| **Failed** | Errored before completion (retained) |
| **Cancelled** | Cancelled before completion (retained) |
| **Superseded** | A newer Completed run for the project has replaced this one as current (retained) |

**Allowed transitions:** Queued→Running; Running→Completed; {Queued,Running}→Failed; {Queued,Running}→Cancelled; Completed→Superseded.
**Invalid (examples):** Completed→Running (immutable once completed); Superseded→Completed; Failed→Running (retry creates a **new** run).
**Retry behavior:** a Failed/Cancelled run is **not** restarted in place; a **new** AnalysisRun is queued, linked via `previous_run_id`. The failed run is preserved.
**Replacement behavior:** when a new run Completes, the previously-current Completed run for that project transitions to **Superseded**; the newest Completed run is "current."
**Historical preservation:** Failed, Cancelled, and Superseded runs are all retained (replay/audit).
**Data-Model mapping:** `AnalysisRun.run_status` (queued/running/completed/failed/superseded) — **aligned.**

---

## 6. Fast Analysis Pass Behavior

**The 60-Second Orientation lifecycle.** Project: Draft→Orientation Running→Orientation Complete; AnalysisRun(`run_type=fast_analysis_pass`): Queued→Running→Completed (target ≤ 60s).

- **Inputs:** Project; Evidence; synthesized Artifacts/ArtifactVersions; **fast-horizon** ContextItems (Fast Extraction).
- **Outputs (required):** **Initial Confidence** (a new ConfidenceState), **Initial Findings**, **Initial Recommendations** — plus CAFState and an MRI snapshot.
- **Behavior:** runs once per project on first analyzable input; optimized for speed; communicates confidence maturity.
- **Clarification:** **Fast Analysis is not final understanding.** It produces an *orientation*; the Deep Analysis Pass continues after it. Project does not terminate at Orientation Complete.

---

## 7. Deep Analysis Pass Behavior

**Deep Analysis lifecycle.** Project: Orientation Complete→Deep Analysis Running→Deep Analysis Complete (recurring on events); AnalysisRun(`run_type=deep_analysis_pass`): Queued→Running→Completed.

**Additional work performed:** additional claim discovery; context enrichment; assumption expansion; relationship expansion; **contradiction discovery**; confidence refinement; finding expansion; recommendation expansion. (Deep-horizon ContextItems are produced with `extraction_horizon=deep`.)

- **Outputs (required):** **Confidence Recalculation** (a new ConfidenceState superseding the prior), **Expanded Findings** (new Findings with `first_seen_run_id` = this deep run), **Expanded Recommendations** (new Recommendations from new/updated findings).
- **Clarifications:** **Deep Analysis improves understanding. Deep Analysis performs no governance** — it does not accept, govern, or create Accepted Understanding; it only expands and refines understanding.

---

## 8. Confidence State Lifecycle

**Concepts:** **Current Confidence** (the latest ConfidenceState, pointed to by `Project.current_confidence_state_id`), **Superseded Confidence** (a prior ConfidenceState replaced by a newer one), **Historical Confidence** (the full supersession chain).

- **Creation:** every Completed AnalysisRun produces exactly one new ConfidenceState.
- **Replacement:** the new ConfidenceState sets `supersedes_confidence_state_id` → the prior current; the prior becomes Superseded; the project's current pointer advances.
- **Preservation:** superseded states are retained — confidence history is the chain.
- **Evolution across runs:** Fast run → C1 (current). First deep run → C2 (supersedes C1). Each subsequent deep run → C3, C4 … each superseding the prior. The chain is the confidence trend/history.

---

## 9. CAF State Lifecycle

**Concepts:** **Current CAF** (latest CAFState), **Superseded CAF** (replaced), **Historical CAF** (chain). Same lifecycle pattern as Confidence: each Completed run produces a CAFState; the latest is current; prior CAFStates are retained.

This is **state lifecycle only** — it does **not redefine CAF**. The meaning of Clarity/Alignment/Feasibility and how they are assessed/scored remains owned by the CAF Assessment and CAF Scoring models; here we only track which CAFState is current vs superseded vs historical.

---

## 10. Finding Lifecycle

**States:** `Detected → Acknowledged → Addressed → Closed`, plus `Superseded` and `Reopened`.

| State | Meaning |
|---|---|
| **Detected** | Surfaced by an analysis run |
| **Acknowledged** | A user has seen/accepted it as real |
| **Addressed** | Work has been done that targets it (edit, fix, evidence) |
| **Closed** | Resolved — no longer an open concern |
| **Reopened** | A Closed finding returns to active (new evidence shows it again) |
| **Superseded** | A run determines this finding no longer holds / is replaced (retained) |

**Allowed transitions:** Detected→Acknowledged; Acknowledged→Addressed; Addressed→Closed; Closed→Reopened; {Detected,Acknowledged,Addressed}→Superseded; Reopened→Acknowledged/Addressed.
**Invalid (examples):** Detected→Closed (must be addressed first); Closed→Addressed (use Reopened); Superseded→any active (a superseded finding is terminal; a *new* finding may replace it).
**Clarification:** **Findings remain descriptive** — a Finding's state describes the status of an observation; it never prescribes action.
**Data-Model mapping:** `Finding.status` currently (detected/validated/recommended/addressed/resolved/reopened). Mapping: Detected=`detected`, Acknowledged≈`validated`, Addressed=`addressed`, Closed=`resolved`, Reopened=`reopened`, **Superseded = new value required.** *(Conflict — see post-doc.)*

---

## 11. Recommendation Lifecycle

**States:** `Generated → Accepted → Rejected → Deferred → Implemented`, plus `Superseded`. 〔`Deferred` added per Recommendation Reconciliation Ratification Decision 001 (RS-R3) / Data Model v1.2〕

| State | Meaning |
|---|---|
| **Generated** | Produced by an analysis run for a Finding |
| **Accepted** | User accepts the recommendation |
| **Rejected** | User rejects it |
| **Deferred** 〔RS-R3〕 | User postpones it; the recommendation remains valid (Recommendation Model Position #12) |
| **Implemented** | Acted upon / applied |
| **Superseded** | Replaced by a newer recommendation (retained) |

**Transition rules:** Generated→{Accepted, Rejected, **Deferred**}; **Deferred→{Accepted, Rejected}**; Accepted→Implemented; {Generated, Accepted, **Deferred**}→Superseded; (Rejected is terminal unless superseded).
**Replacement behavior:** a Deep run may supersede a Generated/Accepted/Deferred recommendation with an expanded one; the prior is retained as Superseded.
**Invalid (examples):** Rejected→Implemented; Implemented→Generated; Superseded→Accepted.
**Clarification:** **Recommendations remain advisory** — Accept/Reject/Defer/Implement are user choices; the recommendation never acts on its own. Only user action + resulting evidence changes understanding.
**Data-Model mapping (v1.2):** `Recommendation.status` = `{generated, accepted, rejected, deferred, implemented, superseded}` — **aligned** (no `presented`/`completed` states; RS-R2/RS-R4). Maps 1:1 to the states above.

---

## 12. Notification Lifecycle

**States:** `Created → Viewed → Dismissed`, plus `Expired`.

| State | Meaning |
|---|---|
| **Created** | Surfaced by a source-object change |
| **Viewed** | The target saw it |
| **Dismissed** | The target dismissed it |
| **Expired** | Aged out (retained as awareness history) |

**Allowed transitions:** Created→Viewed; Viewed→Dismissed; Created→Dismissed (dismiss unread); {Created,Viewed}→Expired.
**Invalid (examples):** Dismissed→Viewed; Expired→Viewed.
**Clarification:** **Notification state changes do not alter Findings or Recommendations.** A Notification only surfaces awareness; dismissing or expiring it changes nothing about the object it referenced.
**Data-Model mapping:** `Notification.state` currently (created/viewed/dismissed/acted_upon/historical). Mapping: Created=`created`, Viewed=`viewed`, Dismissed=`dismissed`, **Expired ≈ `historical`** (recommend rename/alias); `acted_upon` is not used by this state machine. *(Minor conflict — see post-doc.)*

---

## 13. Report Lifecycle

**States:** `Draft → Published → Superseded → Archived` (with version history via ReportSnapshot).

| State | Meaning |
|---|---|
| **Draft** | Being generated; not yet a current snapshot |
| **Published** | Current snapshot is live/shareable |
| **Superseded** | A newer published snapshot replaced this one (retained) |
| **Archived** | Retired |

**Allowed transitions:** Draft→Published; Published→Superseded (new snapshot); Published→Archived; Superseded→Archived.
**Version history:** each publish creates a new `ReportSnapshot` (version chain); superseded snapshots are retained.
**Data-Model mapping:** the Data Model models `Report` + versioned `ReportSnapshot` but **has no `Report.status` field.** *(Recommend adding — see post-doc.)*

---

## 14. Shared Artifact Lifecycle

**States:** `Created → Shared → Viewed → Revoked` (plus `Expired`).

| State | Meaning |
|---|---|
| **Created** | Share object created |
| **Shared** | Link active and distributable |
| **Viewed** | Accessed by a recipient |
| **Revoked** | Access revoked by an owner |
| **Expired** | Passed `expires_at` |

**Allowed transitions:** Created→Shared; Shared→Viewed; {Shared,Viewed}→Revoked; {Shared,Viewed}→Expired.
**Invalid (examples):** Revoked→Viewed; Expired→Shared.
**Data-Model mapping:** the Data Model models `SharedArtifact` with `created_at`/`expires_at`/`revoked_at` but **no explicit `status` field.** *(Recommend adding — see post-doc.)* Release 1 only — no external-governance concepts.

---

## 15. Recompute Rules

Deterministic event→trigger rules. **Event-driven:** an event that does not change evidence, artifacts, or findings produces **no** recompute (no-change → no-recompute).

### Fast Analysis
- **Triggers:** project creation followed by first analyzable input; initial artifact/evidence ingestion; the first "major" analyzable artifact.
- **Rule (deterministic):** Fast Analysis runs **exactly once per project**, when the project has **no completed fast run** AND has at least one analyzable input. Re-orientation is not triggered by later changes (those trigger Deep Analysis).

### Deep Analysis
- **Triggers (examples):** orientation completion (auto first deep pass); substantial context changes; major artifact update; suggested-fix applied; chat-generated edit; collaboration event that produces new evidence; manual request.
- **Rule (deterministic):** on a qualifying event, **if no Deep run is currently Running** for the project, queue a new Deep run; **if one is Running**, mark the project "deep-recompute pending" and **coalesce** rapid events into a single next run (debounce/cooldown window — value is calibration, §19). Trivial/non-substantive edits do not qualify.

### Confidence Recalculation
- **Rule:** occurs as part of **every Completed run** — each Completed run emits a new ConfidenceState superseding the current (§8). There is no standalone confidence recompute.

### Finding Expansion
- **Rule:** a Completed **Deep** run evaluates current understanding and **appends new Findings** (`first_seen_run_id` = this run), re-evaluates existing Findings (status may advance or Supersede). Fast runs produce initial Findings only.

### Recommendation Expansion
- **Rule:** a Completed Deep run **generates new Recommendations** for new/updated Findings and may Supersede prior recommendations. Recommendations are always tied to a Finding.

---

## 16. Supersession Model

History is preserved by **supersession chains; no destructive mutation.**

| Object | Supersession mechanism |
|---|---|
| **Analysis Runs** | `previous_run_id` chain; the prior current Completed run → `Superseded` when a newer run Completes; all retained |
| **CAF States** | new CAFState per run; prior retained as historical/superseded |
| **Confidence States** | `supersedes_confidence_state_id` chain; prior → Superseded; retained |
| **Findings** | a finding may transition to `Superseded`; a new finding may replace it; both retained |
| **Recommendations** | `Superseded` state; prior retained |
| **Reports** | `ReportSnapshot` version chain; superseded snapshots retained |

**Principle:** the current state of any object is the head of its chain; the chain *is* the history. Nothing is deleted to change state (subject to retention policy — §19).

---

## 17. Failure & Recovery Model

- **Failure:** an analysis run that errors transitions Queued/Running→**Failed** (retained). The project reverts to its **last completed state** (a failed first orientation → project stays `Draft`; a failed deep run → project stays at `Deep Analysis Complete` of the prior run).
- **Retries:** a Failed run is not restarted in place; a **new** AnalysisRun is queued (linked via `previous_run_id`). **[decision]** Release 1 = bounded retry then surface failure status; the retry policy count is calibration (§19).
- **Cancellation:** Queued/Running→**Cancelled** (user or system); a new run may be queued later.
- **Restart / recovery:** on system restart, a run left `Running` with no progress is marked **Failed** (idempotent completion means a re-run is safe); recompute rules (§15) re-trigger as needed. **[decision]** Release 1 favors fail-and-retry over mid-run resume.
- **Invariant:** failures never corrupt prior state — the last Completed run and its CAF/Confidence/Findings remain current until a new run Completes.

---

## 18. Lifecycle Interaction Diagram

```text
Project: Draft
   │  (first analyzable input → Fast Analysis)
   ▼
Project: Orientation Running ── AnalysisRun(fast): Queued→Running→Completed
   ▼
Project: Orientation Complete ──► Outputs: Initial Confidence (C1) · Initial Findings · Initial Recommendations · MRI
   │  (auto first Deep Analysis; later: events → Deep Analysis)
   ▼
Project: Deep Analysis Running ── AnalysisRun(deep): Queued→Running→Completed
   ▼
Project: Deep Analysis Complete ──► Confidence Recalculation (C2 supersedes C1)
                                  ──► Expanded Findings   (first_seen = this deep run)
                                  ──► Expanded Recommendations
   │  (new qualifying event → another Deep run: cycle back to Deep Analysis Running)
   ▼
(eventually) Project: Archived
```
Each cycle preserves history via supersession (§16); the user acts on recommendations, producing new evidence that drives the next Deep run.

---

## 19. Open Questions (unresolved — not solved here)

1. **Debounce / cooldown window** for Deep Analysis coalescing (timing values) — calibration/ops.
2. **Retry policy** (max attempts, backoff) for failed runs — calibration.
3. **Re-orientation** — modeled as once-only; whether a project can be re-oriented (vs only deep-reanalyzed) is deferred.
4. **Run concurrency** — single-active Deep run + coalesce is assumed; multi-worker parallel deep analysis is an implementation choice.
5. **In-flight recovery semantics** — fail-and-retry vs mid-run resume (idempotency boundary).
6. **Finding "Acknowledged" actor** — user-only vs system auto-acknowledge.
7. **Report auto-supersession** — what event publishes/supersedes a report (manual vs run-driven).
8. **Retention/deletion** interaction with supersession (GDPR) — owned by Data Model/ops (§16 caveat).

*These are recorded for the Event Model, calibration, and ops specs to resolve; not solved here.*

---

## 20. Validation

- Active Release 1 only — ✅
- No Governance concepts — ✅
- Supports Fast Analysis Pass — ✅ (§5, §6; AnalysisRun fast lifecycle → orientation)
- Supports Deep Analysis Pass — ✅ (§5, §7; recurring deep lifecycle)
- Supports Confidence Recalculation — ✅ (§8; new ConfidenceState per run, supersession chain)
- Supports Expanded Findings — ✅ (§10, §15; deep run appends findings)
- Supports Expanded Recommendations — ✅ (§11, §15; deep run generates recs)
- Supports Replayability — ✅ (§16 supersession chains + per-run snapshots)
- Supports Supersession — ✅ (§16)
- Supports Reporting — ✅ (§13)
- Supports Collaboration — ✅ (§12 notifications, §14 shared artifacts; comments are stateless threads)
- Event-driven — ✅ (§2, §15; no-change → no-recompute)
- No Future Architecture introduced — ✅

**Release 1 State Model Specification complete.**
