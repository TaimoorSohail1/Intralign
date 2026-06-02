# Deep Pass — UX Layout Guidelines

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** UI Specification §8 (Deep Analysis Experience), §9–§11, §20 · State/Event Models · Confidence/Reliability models. Tags: `canonical` / `derived` / `proposal` / `TBD`.

> The Deep Pass UX presents **expanded understanding** — recalculated confidence, expanded findings/recommendations, run history — as a non-blocking, event-driven evolution of the orientation. Expansion improves understanding; it performs no governance.

## Purpose `canonical`
Show the user how understanding deepens over time: new findings/recommendations, recalculated confidence at higher reliability, and the supersession history — without blocking their work.

## Layout regions `derived`
- **Confidence (recalculated)** `canonical` — header chip updates to the new `ConfidenceState`; a "recalculated" indicator links to the change vs the superseded value; Confidence Experience shows the supersession-chain timeline (fast → deep → deep) with reliability rising.
- **Expanded findings** `canonical` — new findings (`first_seen_run_id` = deep run) flagged "New from Deep Analysis"; full Finding lifecycle visible (Detected/Acknowledged/Addressed/Closed/Reopened/Superseded).
- **Expanded recommendations** `canonical` — new recommendations flagged; lifecycle (Generated/Accepted/Rejected/Implemented/Superseded).
- **Run history** `canonical` — timeline of `AnalysisRun`s with `run_type`/`run_status`/timestamps; selecting a run shows its CAF/confidence/findings snapshot (replay).
- **Supersession view** `canonical` — superseded findings/recommendations/confidence shown collapsed with links to replacements; **never deleted**.

## Progress / non-blocking `canonical`
- Inline, non-blocking deep-run indicator (`queued`/`running`); the user keeps working.
- "Run Deep Analysis" (manual) available when project is `oriented`/`analyzed`; cancel available while `queued`/`running`.

## State presentation `canonical`
- Project badge `deep_analyzing` ↔ `analyzed` as runs recur.
- Action enablement mirrors legal source states (acknowledge/address/close/reopen; accept/reject/implement); illegal actions hidden (prevents `409`).

## Event-driven refresh `canonical`
- `deep_analysis_started`/`_completed`, `confidence_recalculated`/`_superseded`, `finding_created`/`_superseded`, `recommendation_created`/`_superseded` update the relevant regions in place (UI §20); ARIA live region announces "Deep Analysis complete, confidence updated."
- `analysis_failed`/`analysis_cancelled` → run row Failed/Cancelled; prior understanding intact.

## Explainability `canonical`
- Expanded findings show both-sides basis for conflicts; recommendations show rationale + finding linkage; confidence movement traces to the run and the superseded value.

## Reliability `canonical`
- Communicate that Alignment/Feasibility reliability has risen vs the Fast orientation; the headline confidence may move up or down while reliability increases — present both honestly.

## Forbidden `canonical`
- No governance/acceptance/disposition UI; no "accept understanding" action; no autonomous apply; no deletion of superseded items; no invented score mechanics.

## Open decisions
- Deep "still working" thresholds, run-history density, supersession-chain visualization, microcopy — **`TBD – Owner Decision Required`** (depend on visual design + Deep latency targets).
