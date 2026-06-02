# Fast Pass vs Deep Pass — Comparison

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** Planning Intelligence §16–§20 · Analysis Engine §7–§10 · State/Event Models · NFR. Tags: `canonical` / `derived` / `proposal` / `TBD`.

> Both passes execute the same reasoning (Planning Intelligence) and produce the same object types; they differ in horizon, latency, completeness, and reliability. Fast = orientation (not final). Deep = expansion (no governance).

| Aspect | Fast Pass | Deep Pass | Tag |
|---|---|---|---|
| Purpose | 60-Second Orientation | Improve/expand understanding | canonical |
| Horizon | fast (shallow) | deep (enriched) | canonical |
| `run_type` | `fast_analysis_pass` | `deep_analysis_pass` | canonical |
| Trigger | once per project, first analyzable input | qualifying event, coalesced, single-active | canonical |
| Project transition | `created → orienting → oriented` | `deep_analyzing → analyzed` (recurs) | canonical |
| Latency target | **< 60s Time-to-First-MRI** | **TBD – Owner Decision Required** | canonical / TBD |
| Execution mode | synchronous-feel, bounded | asynchronous, coalesced | canonical |
| Claim scope | bounded salient subset (~50–100) | fuller set (~350–850 est.) | proposal / TBD |
| Context window | single context (≤ envelope, no capacity chunking) | parallel chunking carrying global map | proposal |
| CAF coverage | Clarity full; Alignment/Feasibility preliminary | all three fully relational | derived |
| Reliability | lower (esp. Alignment/Feasibility) | higher (fuller Coverage/Evidence/Assessability) | canonical |
| Confidence | initial `ConfidenceState` | recalculated (supersedes prior) | canonical |
| Findings | initial `detected` | expanded (`first_seen_run_id`=deep) + supersession | canonical |
| Recommendations | initial `generated` | expanded + supersession | canonical |
| Conflict discovery | shallow only | signature activity (relational) | canonical |
| Governance | none | none (expansion only) | canonical |
| Finality | **explicitly NOT final** | latest understanding (still superseded by later runs) | canonical |
| Completion event | `fast_analysis_completed` | `deep_analysis_completed` | canonical |
| Fan-out (ordered) | confidence_created → finding_created → recommendation_created → notification_created | confidence_recalculated+superseded → finding_created/superseded → recommendation_created/superseded → notification_created | canonical |
| Failure effect | Project reverts to `created` | Project stays at prior `analyzed`/`oriented` | canonical |
| History | n/a (first) | prior superseded, retained (never deleted) | canonical |

**Shared invariants (canonical):** event-driven; deterministic w.r.t. understanding; replayable; traceable to basis; findings descriptive; recommendations advisory; confidence derived from CAF + Reliability; supersession over deletion; user decides.

**Key distinction to preserve (canonical):** Fast output must be surfaced as orientation-in-progress ("Deep Analysis to follow"), never as final understanding. Deep is where the relational, highest-value findings (contradictions, infeasibility, misalignment) are competently evaluated.
