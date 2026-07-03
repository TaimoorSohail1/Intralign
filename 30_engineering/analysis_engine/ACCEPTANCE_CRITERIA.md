# Acceptance Criteria

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** Testing Strategy · NFR · State/Event Models · Engine. Tags: `canonical` / `derived` / `proposal` / `TBD`. Each criterion is testable (Given/When/Then style).

> Quantitative thresholds that are undefined upstream are marked `TBD – Owner Decision Required`; the test is scaffolded but its numeric pass/fail is deferred.

## A. Fast Pass latency
- **AC-L1** `canonical` — Given an in-envelope project, When a Fast run completes, Then Time-to-First-MRI is **< 60s** (NFR §3). *(Percentile + envelope size = `TBD`.)*
- **AC-L2** `derived` — Given queue load, When measuring, Then queue-time and compute-time are reported separately (NFR §18).
- **AC-L3** `proposal` — Given an oversized input (> ceiling), When submitted, Then it is accepted but routed Deep-only with a "large project" message (no Fast-budget breach).

## B. Fast Pass outputs
- **AC-F1** `canonical` — When a Fast run completes, Then exactly one `CAFState` and one `ConfidenceState` exist for the run.
- **AC-F2** `canonical` — Then initial `Finding`s exist with `status=detected` and each has ≥1 `evidence_link`.
- **AC-F3** `canonical` — Then initial `Recommendation`s exist with `status=generated`, each referencing a `finding_id`.
- **AC-F4** `canonical` — Then the orientation is labelled non-final and Project = `oriented`.
- **AC-F5** `canonical` — Then Confidence is reliability-qualified (no bare value).

## C. Deep Pass outputs
- **AC-D1** `canonical` — When a Deep run completes, Then a new `ConfidenceState` supersedes the prior (`supersedes_confidence_state_id` set; prior retained).
- **AC-D2** `canonical` — Then Expanded `Finding`s exist with `first_seen_run_id` = the deep run.
- **AC-D3** `canonical` — Then Expanded `Recommendation`s exist for new/updated findings.
- **AC-D4** `canonical` — Then any superseded finding/recommendation/confidence is **retained, not deleted**.
- **AC-D5** `canonical` — Then Project = `analyzed`; the deep pass performed **no governance** (no acceptance/disposition records exist).

## D. Determinism
- **AC-DET1** `canonical` — Given identical inputs + pinned model config, When a pass re-runs, Then governable outputs (finding-type set, recommendation set, confidence band, reliability qualifier) are **bounded-equivalent**. *(Tolerance = `TBD`.)*
- **AC-DET2** `canonical` — Given identical understanding, When re-triggered, Then no new state is fabricated (no-change → no-recompute).

## E. Replay
- **AC-R1** `canonical` — Given the event log, When replayed into a clean store, Then reconstructed state is identical to original (modulo suppressed side effects).
- **AC-R2** `canonical` — Then the AnalysisRun, confidence, and finding/recommendation supersession chains rebuild exactly.
- **AC-R3** `canonical` — Given duplicate/out-of-order events, When replayed, Then dedupe + reorder yields the same state.

## F. Traceability
- **AC-T1** `canonical` — For every Finding, Then its basis (evidence/claim + producing run) is resolvable without recomputation.
- **AC-T2** `canonical` — For every Recommendation, Then `finding_id` + `first_seen_run_id` resolve.
- **AC-T3** `canonical` — For every ConfidenceState, Then `analysis_run_id` + (where applicable) `supersedes_confidence_state_id` resolve.
- **AC-T4** `canonical` — Every claim/finding carries a resolvable source span.

## G. LLM validation
- **AC-V1** `proposal` — Given any LLM output, When parsed, Then it conforms to the fixed schema or is rejected and retried (bound = `TBD`).
- **AC-V2** `canonical` — Then enum-valued fields validate against `analysis_enums`; unknown values are rejected.
- **AC-V3** `canonical` — Then no LLM output introduces a formula/weight/percentage/threshold or a bare confidence value.

## H. Rule/LLM boundary
- **AC-B1** `derived` — Then deterministic stages (0,1,5-emission,8; mechanics of 7) produce identical output across runs on identical input.
- **AC-B2** `canonical` — Then no Finding contains prescriptive content; no Recommendation is auto-applied.
- **AC-B3** `proposal` — Then intrinsic Clarity detections (vagueness/missing-units/coverage-gap) are produced by rules and are reproducible.

## I. UX behavior
- **AC-U1** `canonical` — Then the 60-Second Orientation displays the "not final / Deep Analysis in progress" banner.
- **AC-U2** `canonical` — Then entity states display only Data Model v1.1 enum values; actions are enabled only on legal source states.
- **AC-U3** `canonical` — Then screens refresh in place on the mapped events (no manual reload); superseded items shown, not deleted.
- **AC-U4** `canonical` — Then Alignment/Feasibility reliability is shown as preliminary in Fast.

## J. Scope compliance
- **AC-S1** `canonical` — Then no Governance/Accepted-Understanding/Agent-Governance/Execution/Actuation/Orchestration concept appears anywhere in the workflow.
- **AC-S2** `canonical` — Then no new entity, state, event, or capability beyond the Data/State/Event models exists.
- **AC-S3** `canonical` — Then Fast output is never presented or stored as final understanding.

## K. Failure handling
- **AC-FAIL1** `canonical` — Given an analysis failure, When it occurs, Then run = `failed`, Project reverts to last completed state, prior outputs intact.
- **AC-FAIL2** `canonical` — Given a retry, Then a **new** AnalysisRun is created (`previous_run_id`); the failed run is retained.
- **AC-FAIL3** `canonical` — Given a cancel on `queued`/`running`, Then run = `cancelled`, no partial commit.
- **AC-FAIL4** `canonical` — Given any publication, Then it is atomic (all outputs or none).
- **AC-FAIL5** `proposal` — Given a global-skeleton failure (Fast S2), Then the run degrades to isolation-only with reduced reliability rather than failing.
