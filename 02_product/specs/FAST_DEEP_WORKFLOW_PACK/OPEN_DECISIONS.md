# Open Decisions

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Purpose:** Every unresolved calibration / owner-decision item the Fast/Deep workflow depends on. None are invented here. Each is `TBD – Owner Decision Required` unless marked `proposal` (a recommended starting value pending ratification).

| # | Decision | Status | Proposal (if any) | Affects | Source |
|---|---|---|---|---|---|
| OD-1 | **Model choice / tier** (frontier vs fast tier per stage) | TBD | extraction on fast tier; relational reasoning on frontier (proposal) | latency, cost, determinism | Engine §23 |
| OD-2 | **Ingestion token envelope** (Fast) | TBD | ~20k design point / ~33k hard ceiling (proposal) | 60s budget, cost | NFR §3; pack |
| OD-3 | **Fast claim count bound** | TBD | ~50–100 salient (proposal) | 60s budget | pack |
| OD-4 | **Deep total claim count** (informational) | TBD | ~350–850 estimate (proposal) | Deep latency, cost | pack |
| OD-5 | **LLM per-call output limits** / per-claim token budget | TBD | terse schema; bound per call (proposal) | latency, cost | RULE_LLM §7 |
| OD-6 | **CAF assessed-level scale** (qualitative ↔ numeric) | TBD | — | CAF state, UX | CAF Scoring model |
| OD-7 | **CAF → Confidence synthesis method** | TBD | formula-free; method unspecified | confidence | Confidence model; Matrix §22 g1 |
| OD-8 | **Reliability scale** (High/Moderate/Low ↔ numeric) | TBD | — | reliability qualifier | Reliability §12 |
| OD-9 | **Deep Pass completion target & timeout** | TBD | — | Deep UX, ops | NFR §4 |
| OD-10 | **Debounce / coalescing window** (deep recompute) | TBD | — | recompute, cost | Event §15; NFR |
| OD-11 | **Retry limits / backoff** (LLM call + run) | TBD | bounded retry (proposal) | reliability | Engine §17 |
| OD-12 | **Bounded-equivalence determinism tolerance** | TBD | tolerance over governable outputs (framework only) | determinism tests | Engine §15 |
| OD-13 | **Global-skeleton pattern adoption** | proposal | adopt 2-stage global+local | global semantics, parallelism | pack |
| OD-14 | **Severity assignment basis** (critical/moderate/warning) | TBD | rule heuristic default (proposal) | findings | Finding model |
| OD-15 | **Claim attribute schema** (verbatim_span, normalized_text, modality, support_status, clarity flags, canonical_key, structured_proposition, relationship_links) | proposal | add as ContextItem fields | extraction, dedup, determinism | pack; Data §9 |
| OD-16 | **CAFState attribute additions** (evaluation_completeness, contributing_findings, direction_vs_prior, dimension_coverage) | proposal | add as CAFState fields | CAF UX, traceability | pack; Data §10 |
| OD-17 | **Oversize-input routing policy** (Deep-only/queue) | TBD | route Deep-only with message (proposal) | intake | pack |
| OD-18 | **Event transport** (websocket/SSE/poll) + dead-letter | TBD | — | UI refresh, ordering | Event §19; NFR |
| OD-19 | **Fast/Deep horizon boundary** (what fast defers) | TBD | — | extraction depth | Engine §23; Planning Intel §23 |
| OD-20 | **Performance SLOs** (API/notification/report latency, availability, RTO/RPO) | TBD | — | ops, tests | NFR §5–§17 |
| OD-21 | **Cost budgets** (overall + per-pass AI spend; tier limits) | TBD | — | unit economics | NFR §12 |
| OD-22 | **Notification `delivered` state** | TBD (deferred) | defer until delivery-channel semantics exist | notification lifecycle | Patch-001 |
| OD-23 | **Recommendation `verified` sub-state** | TBD (deferred) | optional `verified_at` flag later | recommendation lifecycle | Data v1.1 §20 |

**Governance note:** all `proposal` items require owner ratification before becoming canonical; all `TBD` items block only the *quantitative* acceptance of their dependent criteria, not the structural build. Resolve OD-2 (envelope) and OD-21 (cost) first — they gate the 60s SLA and unit economics (Performance Risk Assessment).
