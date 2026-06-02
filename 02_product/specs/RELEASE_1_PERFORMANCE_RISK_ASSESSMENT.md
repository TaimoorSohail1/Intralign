# Release 1 Performance Risk Assessment

**Type:** Risk assessment following the Release 1 Performance & NFR Specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Inputs:** `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` · `RELEASE_1_NFR_ACCEPTANCE_MATRIX.md` · API/State/Event/Data v1.1/UI specs · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md`

> Assesses Release 1's principal NFR risks with mitigations. Read-only; introduces no new architecture, capability, or value.

## 1. Fast Analysis risk — **High**

The 60-second Time-to-First-MRI is the product's core promise and the only approved target, but it has **no supported-project-size envelope** — so for large inputs the promise is unbounded and likely to break. Queue-time under load is a hidden contributor that can erode the budget even when compute is fast.
**Mitigation:** owner-set the **size envelope** (top priority); gate/queue oversized inputs with honest messaging; prioritize fast runs in the queue; monitor Time-to-First-MRI broken out by project size and by queue-time vs compute-time; autoscale workers.

## 2. Deep Analysis risk — **Medium-High**

No completion target, timeout, or debounce window is defined, so queueing, coalescing, and "still working" UX can't be tuned, and cost can drift (it's the expensive pass). Because Deep is non-blocking, the *reliability* impact is contained (prior understanding stays intact), but *cost* and *UX-latency* exposure is real.
**Mitigation:** owner-set a Deep completion band + timeout + debounce/cooldown; rely on single-active-deep-run + event coalescing (already specified) to bound re-analysis; keep the UI non-blocking; surface run history so users see progress.

## 3. API risk — **Low-Medium**

API correctness is well-specified (commands→transitions→events, idempotency, error model); the gap is purely **undefined latency targets** per class. The async ack-vs-execution distinction is correctly drawn, so analysis time won't masquerade as API latency.
**Mitigation:** owner-set per-class latency targets; ship sensible defaults + monitoring meanwhile; keep idempotency-key-safe retries; paginate all list reads (already default 25).

## 4. Event-processing risk — **Medium**

Guarantees are firm (at-least-once, idempotent, ordered, replayable), but **throughput, delivery-lag, and the client transport** are undefined. Risk is stale UI or double-handling under load, and unbounded lag without a target.
**Mitigation:** keep consumers idempotent (`event_id` dedupe); enforce per-object ordering by (`timestamp`,`event_id`); choose a transport (SSE/websocket/poll) and set a delivery-lag p95; add a dead-letter path + event-lag monitoring.

## 5. Cost risk — **High**

AI inference dominates cost and **no budgets are approved** (overall or per pass), which is an existential unit-economics risk on the free tier. In-product-only notifications keep delivery cost near zero (a positive), but Deep runs and history growth are the exposure.
**Mitigation:** owner-set per-tier AI budgets; lean on existing controls (single-active-project free tier, daily suggested-fix cap, single-active-deep-run + coalescing); meter AI spend per run/tier; consider depth/size caps tied to the §1 size envelope.

## 6. Scalability risk — **Medium**

All per-dimension capacity limits are TBD, so provisioning is guesswork and load behavior is unknown. Append-only history means read paths slow as data grows.
**Mitigation:** owner-set per-dimension limits; load-test once targets exist; paginate + index hot read paths (findings/recommendations/runs); plan cold-history archival (ties to retention, §7 below).

## 7. Operational risk — **Medium**

Availability SLO, RTO/RPO, and **retention/pruning** are undefined. Retention is the sharpest: explainability/replayability require keeping history, but storage/cost bound it — and hard-delete (GDPR) must be honored. (This is a storage/cost decision, **not** a governance policy.)
**Mitigation:** owner-set availability + RTO/RPO and a retention/pruning/hard-delete policy; implement backups + event replay for recovery; environment separation; feature-flag deferred surfaces (`delivered`/`verified`).

---

## Mitigation Priority (recommended owner-decision order)

1. **Fast Analysis size envelope** (R-1) — unblocks the core SLA, cost caps, and load testing.
2. **AI cost budgets per tier/pass** (R-3/Cost) — unit-economics gate.
3. **Deep Analysis target + debounce window** (R-2) — tuning + UX.
4. **Retention/pruning/hard-delete policy** (R-4/Operational) — storage/cost + GDPR.
5. **Availability SLO + RTO/RPO** (R-7).
6. **API/event latency targets + event transport** (R-2/R-5).
7. **Scalability limits** (R-6) — then load test.

---

## Summary

| Area | Risk | Primary driver |
|---|---|---|
| Fast Analysis | **High** | No size envelope for the 60s promise |
| Cost | **High** | No AI budgets; Deep + history exposure |
| Deep Analysis | **Medium-High** | No latency target/debounce window |
| Event processing | **Medium** | Throughput/lag/transport undefined |
| Scalability | **Medium** | Capacity limits TBD; append-only growth |
| Operational | **Medium** | SLO/RTO/RPO + retention TBD |
| API | **Low-Medium** | Latency targets TBD (correctness solid) |

The architecture's **qualitative** guarantees (idempotency, ordering, supersession, isolation, non-corrupting failure) are sound and engineering-verifiable now. The risk is concentrated in **undefined quantitative targets** — every High/Medium item resolves to an owner decision, not a design flaw. Setting the §20 values (size envelope and cost budgets first) converts these from open risks into testable acceptance criteria.

**Release 1 Performance & NFR Specification complete.**
