# Release 1 NFR Acceptance Matrix

**Type:** Engineering quick-reference — acceptance criteria for every Release 1 NFR
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Companion to:** `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md`

> Each NFR with its acceptance criteria and decision owner. `TBD-OD` = TBD – Owner Decision Required (value not yet approved; not invented). "Eng" = engineering-verifiable now; "Owner" = needs a target before it can be accepted; "Owner+Eng" = owner sets the value, engineering verifies.

| Requirement | Category | Acceptance Criteria | Owner |
|---|---|---|---|
| Time-to-First-MRI (Fast Analysis) | Performance | p? Time-to-First-MRI **< 60 s** for projects within the supported-size envelope | Owner+Eng (60s approved; envelope TBD-OD) |
| Fast Analysis size envelope | Performance | Defined max project size for which 60s holds; oversized inputs gated/queued | Owner |
| Fast Analysis acceptable range | Performance | Approved p50/p95 within 60s ceiling | Owner |
| Fast Analysis timeout + retry | Reliability | Timeout → `failed`; new run on retry (not in-place); prior state intact | Owner+Eng (bound TBD-OD) |
| Deep Analysis completion target | Performance | Approved completion band (TBD-OD); run reaches `completed` within it | Owner |
| Deep Analysis cancellation | Reliability | `:cancel` from queued/running → `cancelled`, no partial commit | Eng |
| Deep recompute coalescing | Performance | Single active deep run/project; rapid events coalesced; debounce window applied | Owner+Eng (window TBD-OD) |
| Confidence Recalculation | Performance/Correctness | Each completed run yields a new `ConfidenceState` superseding prior | Eng |
| Expanded Findings / Recommendations | Correctness | Deep run appends items with `first_seen_run_id` = that run | Eng |
| UX interaction latencies (create/save/upload/load) | Performance | Meet approved targets | Owner (TBD-OD) |
| API read/write latency | Performance | Meet approved per-class targets | Owner (TBD-OD) |
| Analysis API ack time | Performance | `:fast`/`:deep`/`:cancel` return run state within approved ack target | Owner (TBD-OD) |
| Event delivery semantics | Event processing | At-least-once delivery; consumers idempotent on `event_id` | Eng |
| Event ordering | Event processing | Total per-object; causal cross-object; run fan-out ordered | Eng |
| Event replay | Event processing | Log replay reproduces identical state; side effects suppressed | Eng |
| Event throughput / delivery lag | Event processing | Meet approved throughput + lag p95 | Owner (TBD-OD) |
| Scalability per dimension | Scalability | Sustain approved limits (workspaces/projects/artifacts/…) | Owner (TBD-OD) |
| Free-tier single active project | Scalability/Cost | >1 active project rejected (`422`) | Eng |
| Retention / pruning / hard-delete | Data growth | Approved retention applied; deletes honored (incl. GDPR) — no governance policy | Owner (TBD-OD) |
| Availability SLO | Reliability | Meet approved availability target | Owner (TBD-OD) |
| Recovery (RTO/RPO) | Reliability | Restore within approved RTO/RPO via backup + event replay | Owner (TBD-OD) |
| Analysis failure non-corruption | Reliability | Failure leaves last completed state current; history preserved | Eng |
| Authentication | Security | Valid bearer token required; invalid → `401` | Eng |
| Authorization | Security | Role-gated commands enforced; violation → `403` | Eng |
| Workspace isolation | Security/Tenancy | Every op filtered by `workspace_id`; cross-tenant → `404` | Eng |
| Shared-artifact protection | Security | Scope + permission_level + status/expiry enforced; revoked/expired denied | Eng |
| Input validation | Security | Enums validated; unknown fields rejected; size limits enforced | Owner+Eng (limits TBD-OD) |
| Rate limiting | Security/Cost | Limits enforced (`429`+`Retry-After`); incl. fix daily cap | Owner+Eng (thresholds TBD-OD) |
| Secrets handling | Security | No client-exposed secrets; server-side management | Eng |
| Auditability | Security/Observability | State changes emit immutable events + telemetry; history reconstructable | Eng |
| Observability (logs/metrics/traces) | Observability | Run/API/event metrics + correlation tracing present; alert thresholds set | Owner+Eng (thresholds TBD-OD) |
| Backups/deployment/env separation | Operational | Backups scheduled; envs separated; versioned releases | Owner+Eng (RPO/cadence TBD-OD) |
| Accessibility baseline | Accessibility | Keyboard, screen-reader, color-independence, focus per UI §18 | Eng |
| Accessibility conformance level | Accessibility | Meet approved WCAG tier | Owner (TBD-OD) |
| Browser/device matrix | Accessibility | Support approved matrix | Owner (TBD-OD) |
| Responsive behavior | Accessibility | Reflow without loss of function; mobile read-optimized | Eng |
| Reporting performance | Performance | Generation/retrieval/export within approved targets | Owner (TBD-OD) |
| Notification performance | Performance | Creation/visibility within approved targets; in-product only | Owner+Eng (targets TBD-OD) |
| AI cost budgets (overall + per pass) | Cost | Stay within approved budgets; per-tier limits enforced | Owner (TBD-OD) |
| Storage cost | Cost | Within approved budget (driven by retention) | Owner (TBD-OD) |

*All `TBD-OD` items are enumerated in §20 of the NFR spec. Engineering-verifiable ("Eng") items can be accepted at build time; owner items gate SLA sign-off.*
