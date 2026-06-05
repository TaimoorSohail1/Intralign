# Release 1 Performance & NFR Specification v1

**Type:** Implementation artifact — the authoritative Release 1 Non-Functional Requirements & Performance specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded exclusively in:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` · `RELEASE_1_UI_SPECIFICATION_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md`

> **Scope guardrails.** Active Release 1 only. **No Governance Domain concepts, Future Architecture, Agent Governance, or Execution Intelligence.** This document defines **quality constraints only** — no new capabilities, entities, workflows, or lifecycle states. **No quantitative target is invented.** The only owner-approved numeric target in the corpus is the **60-second Time-to-First-MRI** (Master Spec §20 / Canonical Scope M1); every other quantitative value is marked **`TBD – Owner Decision Required`** and enumerated in §20.

---

## 1. Performance Philosophy

Release 1 prioritizes, in order:

1. **User-perceived responsiveness** — the product must *feel* fast, anchored by the 60-Second Orientation.
2. **Confidence in results** — outputs are reliability-qualified; correctness/explainability outrank raw speed for Deep Analysis.
3. **Explainability** — every signal traces to its basis from stored lineage (no recomputation), which constrains how aggressively data may be pruned.
4. **Reliability** — analysis failures never corrupt prior state; history is preserved.
5. **Cost efficiency** — AI-call cost is bounded per tier; depth is gated to protect unit economics.

**Fast vs Deep — why different characteristics.** The **Fast Analysis Pass** is latency-bound: it exists to deliver orientation within a hard human-perception budget (60s), so it trades depth for speed (fast-horizon extraction, initial confidence/findings/recommendations). The **Deep Analysis Pass** is throughput/quality-bound: it expands claims, enriches context, discovers contradictions, recalculates confidence, and expands findings/recommendations — work that is inherently longer-running, asynchronous, event-triggered, and coalesced. The two are therefore held to different targets: Fast = a fixed latency ceiling; Deep = a completion-time band (TBD) optimized for quality and cost, not sub-minute response.

---

## 2. User Experience Performance Targets

| Interaction | Expected target | Maximum | Notes |
|---|---|---|---|
| Project Creation (`POST /projects`) | **TBD – Owner Decision Required** | TBD | Synchronous metadata write; should feel instant |
| Artifact Save (`POST /artifacts/{aid}/versions`) | **TBD – Owner Decision Required** | TBD | Append version; excludes any triggered Deep run (async) |
| Evidence Upload (`POST /evidence`) | **TBD – Owner Decision Required** | TBD | Excludes extraction (async); upload-ack only |
| Project Load (`GET /projects/{pid}`) | **TBD – Owner Decision Required** | TBD | Hub read; may aggregate child summaries |
| Findings Load (`GET .../findings`) | **TBD – Owner Decision Required** | TBD | Paginated (default 25) |
| Recommendations Load (`GET .../recommendations`) | **TBD – Owner Decision Required** | TBD | Paginated |

All values pending owner decision; none invented. UI loading/skeleton behavior (UI §16) applies until targets are set.

---

## 3. Fast Analysis Pass Targets  *(critical)*

| Attribute | Value |
|---|---|
| **Orientation target (Time-to-First-MRI)** | **< 60 seconds** *(owner-approved; Master Spec §20 / M1)* |
| Acceptable range | **Proposed defaults (DL-046): p50 ≤ 25s · p95 ≤ 50s · hard ceiling < 60s** — see `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` §4b; owner to confirm |
| Supported-project-size envelope for the 60s target | **Proposed defaults (DL-046): ≤ 20 artifacts / ≤ ~50,000 words / 1 active Fast Pass** — see Calibration Defaults §4b; **conservative placeholders — confirm against target-customer project sizes (highest-priority owner decision, R-1)** |
| Timeout threshold | **TBD – Owner Decision Required** |
| Failure behavior | run → `failed` (Event `analysis_failed`); Project remains `created`/reverts; user offered retry (new run); prior state preserved (State Model §17) |
| Retry behavior | failed fast run is **not** restarted in place — a new `AnalysisRun` is queued, `previous_run_id` linked; retry bound **TBD** |

**Explicitly supports the 60-Second Orientation.** **Dependency:** the 60s target is only meaningful once the **supported-size envelope** is set — without it the promise is unbounded. This is the single highest-priority owner decision (§20, risk R-1).

---

## 4. Deep Analysis Pass Targets

| Attribute | Value |
|---|---|
| Expected completion target | **TBD – Owner Decision Required** (no upstream value) |
| Acceptable range | **TBD – Owner Decision Required** |
| Timeout threshold | **TBD – Owner Decision Required** |
| Cancellation behavior | `:cancel` from `queued`/`running` → `cancelled` (Event `analysis_cancelled`); terminal, retained; no partial-result commit |
| Recomputation expectations | event-triggered + coalesced (Event Model §15); single active deep run per project, rapid events coalesced; debounce window **TBD** |

**Explicitly supports:** **Confidence Recalculation** (each completed run emits a new `ConfidenceState` superseding prior), **Expanded Findings** (`first_seen_run_id` = deep run), **Expanded Recommendations**. No timing numbers invented; quality/correctness take precedence over latency for Deep.

---

## 5. API Performance Targets

| Class | Expected | Maximum | Timeout behavior |
|---|---|---|---|
| Read APIs (`GET`) | **TBD – Owner Decision Required** | TBD | return `408`/`500` per error model; client retry (idempotent) |
| Write APIs (commands) | **TBD – Owner Decision Required** | TBD | idempotency-key-safe retry (API §10) |
| Analysis APIs (`:fast`/`:deep`/`:cancel`) | **ack** target TBD; execution is async (not a request-latency metric) | TBD | request returns `queued` quickly; execution tracked via run lifecycle |
| Reporting APIs (`generate`/`publish`) | **TBD – Owner Decision Required** | TBD | generation may be async if large (snapshot) |
| Notification APIs (`GET`/`:view`/`:dismiss`) | **TBD – Owner Decision Required** | TBD | in-product reads |

Analysis endpoints are **command-acks**, not synchronous compute — their latency target governs enqueue time, not analysis time (which is §3/§4).

---

## 6. Event Processing Targets

Quantitative throughput/latency = **TBD – Owner Decision Required**. The **guarantees** (already fixed by the Event Model, not TBD):

| Concern | Required guarantee |
|---|---|
| Event publication | every successful command emits its Event Model event(s); append-only log |
| Event delivery | **at-least-once** (Event Model assumption); consumers must be idempotent |
| Event ordering | **total per object** (by `timestamp`,`event_id`); **causal across objects** (via `causation_id`); run fan-out ordered confidence→finding→recommendation→notification under one `correlation_id` |
| Event replay | replaying the ordered log reproduces identical state (set-to-state); external side effects suppressed in replay |
| Event recovery | dedupe on `event_id`; stale/duplicate events are no-ops; failed deliveries retried with same `event_id` |

Throughput numbers (events/sec, delivery-lag p95) are owner/NFR decisions; the correctness guarantees above are mandatory regardless of scale.

---

## 7. Scalability Requirements

Per-dimension supported scale = **TBD – Owner Decision Required** (no upstream capacity numbers). Assumptions/constraints that *are* fixed by scope:

| Dimension | Supported scale | Assumptions / constraints |
|---|---|---|
| Workspaces | TBD | tenant boundary; isolation enforced regardless of count |
| Projects | TBD; **free tier = 1 active project/workspace** *(scope decision)* | archived projects retained |
| Artifacts | TBD | 8 fixed `artifact_type`s per project |
| Artifact Versions | TBD | append-only chain; grows with edits (§8) |
| Evidence | TBD | per project; size limits TBD |
| Findings | TBD | grows with deep runs (expansion) |
| Recommendations | TBD | ≤ tied to findings |
| Comments | TBD | threaded per project |
| Reports | TBD | + snapshot chain |
| Shared Artifacts | TBD | per workspace; status-gated |

The only fixed scale constraint is the **free-tier single-active-project** limit; all numeric capacity targets are owner decisions.

---

## 8. Data Growth Requirements

| Source | Growth characteristic | Retention assumption |
|---|---|---|
| Storage | grows with evidence + artifact versions + run history + report snapshots | **TBD – Owner Decision Required** |
| Version growth | append-only `ArtifactVersion` chains (never mutated) | retained for replay; pruning policy **TBD** |
| Analysis history | one `AnalysisRun` + `CAFState` + `ConfidenceState` per run, all retained (supersession) | retained for replay/explainability; pruning **TBD** |
| Report history | append-only `ReportSnapshot` chains | **TBD** |
| Notification growth | one row per surfaced change; `expired` retained as history | **TBD** |

**Tension to resolve (owner):** explainability/replayability require retaining history, but storage/cost bound it. Retention + hard-delete (incl. GDPR) is **TBD – Owner Decision Required** (Data §20.5). **No governance retention policies** introduced — Release 1 retention is a storage/cost decision only.

---

## 9. Reliability Requirements

| Concern | Requirement |
|---|---|
| Availability | **TBD – Owner Decision Required** (no upstream SLO) |
| Recovery | on restart, a `running` run with no progress → `failed` (idempotent re-run safe); recompute re-triggers per rules |
| Failure handling | failures never corrupt prior state; last completed run + its states remain current (State Model §17) |
| Retry behavior | new run on failure (not in-place); bound **TBD** |
| **Fast Analysis failure** | Project stays `created`/reverts; user prompted to retry; orientation not falsely shown |
| **Deep Analysis failure** | Project stays at prior `analyzed`/`oriented`; expanded results simply not added; retry available |
| Report failure | report stays `draft`; no partial publish |
| Notification failure | at-least-once; missing a notification never blocks the underlying action (awareness only) |

Fast and Deep are distinguished: Fast failure blocks first orientation (user-visible, retry-prominent); Deep failure is non-blocking (prior understanding intact).

---

## 10. Security Requirements (Release 1 only)

| Area | Requirement |
|---|---|
| Authentication | bearer token → `user_id`; **no SSO/enterprise auth** (out of scope) |
| Authorization | role-gated commands (owner/admin/member); least privilege |
| Workspace isolation | every operation filtered by `workspace_id` (§11) |
| Shared-artifact protection | scoped to one object at `permission_level` (view/comment); `revoked`/`expired` denied; optional expiry |
| Input validation | enums validated against Data Model v1.1; reject unknown fields; size limits **TBD** |
| Rate limiting | per-user/workspace; incl. free-tier suggested-fix daily cap (`429` + `Retry-After`); thresholds **TBD** |
| Secrets handling | server-side secret management; no secrets client-exposed (mechanism per ops) |
| Auditability | state changes emit immutable events + `TelemetryEvent`; supersession preserves history |

**No compliance frameworks introduced** (SOC 2 / GDPR posture referenced by the security baseline, not designed here).

---

## 11. Multi-Tenant Requirements

Grounded in Data Model §16:

- **`workspace_id` isolation** — every tenant-scoped row carries it (denormalized onto project-children); enforced at the boundary.
- **Query isolation** — server injects caller `workspace_id` into every predicate; cross-workspace rows return `404` (existence not leaked).
- **Sharing exception** — the only cross-tenant/anonymous path is a valid `SharedArtifact`, scoped + `permission_level`-limited + status/expiry-gated.
- **Cross-tenant protections** — no API path addresses another workspace's resources; share tokens grant single-object scope only. No enterprise policy concepts.

---

## 12. Cost Constraints  *(critical)* — **ratified enforcement gate (DL-048)**

AI inference is the dominant cost driver; depth is the lever. **Per DL-048, freemium unit economics is an enforced, tested, observable Release 1 criterion:** the **enforcement mechanism is contracted** on the Fast/Deep engine (Wave B/S, chat/fix caps Wave I) — per-tier token budgets read from config, **per-run over-budget → graceful degradation**, **per-user rollup over-budget → gate**, never silent overspend; a **QA acceptance gate** asserts Free-tier runs stay within budget (negatives: bypass / runaway / silent overspend / wrong-tier routing); and an **`AI Spend Recorded`** event emits tokens + est-cost per run/user/tier/mode/model. The **cap values are tunable config** (Calibration Defaults §4c); the mechanism is non-optional.

| Item | Expectation |
|---|---|
| AI call budget (overall) | **Config (DL-048 / Calibration §4c)** — per-tier monthly rollup (Free: 4M tok/mo ≈ ~$3); enforcement contracted |
| Fast Analysis budget (per run) | **Config — Free 150k tok** (degrade on breach); bounded to protect the 60s/low-cost orientation |
| Deep Analysis budget (per run) | **Config — Free 600k tok** (coalesce/defer on breach); the costlier pass; gated by coalescing + tier |
| Storage cost | **TBD** (driven by retention §8) |
| Notification cost | in-product only → **near-zero external cost**; no email/SMS/Slack spend (no delivery channels in R1) |
| Free-tier constraints | **Config — Balanced ~$3/mo (DL-048):** 1 active project; Deep 2/day single-active+coalesced; 5 fixes/day; 20 chats/day; 500k daily / 4M monthly token budget; nano/mini routing |
| Paid-tier assumptions | higher/relaxed limits — **TBD – Owner Decision Required** (tier-parameterized config rows; Open-TBD E3) |

**Values are owner-set config; the enforcement, QA gate, and `AI Spend Recorded` telemetry are contracted (DL-048).** Cost-control mechanisms: single-active-project (free), suggested-fix daily cap, single-active-deep-run + event coalescing (prevents runaway re-analysis), **tier-keyed cheap-model routing** (the primary lever), per-tier budget gating with graceful degradation. Starting dollar/token figures are estimate-based defaults (Calibration §4c), re-tuned from the contracted cost telemetry.

---

## 13. Observability Requirements

| Capability | Requirement |
|---|---|
| Logging | structured logs for commands, run lifecycle transitions, failures; correlation by `request_id`/`correlation_id` |
| Metrics | run durations (esp. Time-to-First-MRI), queue depth, failure/cancel rates, API latencies, event lag — thresholds TBD |
| Tracing | trace command → emitted events → run → fan-out via `causation_id`/`correlation_id` |
| Analysis monitoring | per-run status, latency vs the 60s target, deep-run completion, coalescing behavior |
| API monitoring | latency/error-rate per endpoint class |
| Event monitoring | publication, delivery lag, dedupe/replay, dead-letter (transport TBD) |
| Failure monitoring | `analysis_failed`/`analysis_cancelled` rates; alert thresholds TBD |

Must support **debugging and replayability** — observability is built around the event log + supersession chains so any state is reconstructable.

---

## 14. Operational Requirements

| Area | Requirement |
|---|---|
| Backups | regular backups of persistence + event log; cadence/RPO **TBD** |
| Recovery | restore from backup + event replay; RTO **TBD** |
| Deployment | standard CI/CD; zero-/low-downtime expectation **TBD** |
| Configuration management | externalized config; no secrets in code |
| Feature flags | gate incomplete surfaces (e.g., deferred `delivered`/`verified`); flag system assumed |
| Environment separation | distinct dev/staging/prod; tenant data never crosses environments |
| Release process | versioned API (`/v1`); additive changes in-version (API §15) |

Mechanisms assumed; specific tooling is an ops decision (not invented here).

---

## 15. Accessibility NFRs (Release 1 scope)

| Area | Requirement |
|---|---|
| Accessibility | keyboard operability, screen-reader semantics + ARIA live regions for event-driven updates, color-independent state encoding, predictable focus (UI §18) |
| Responsiveness | reflow to small viewports without loss of function (UI §19) |
| Supported devices | desktop + tablet full; mobile read-optimized (heavy editing de-prioritized) |
| Supported browsers | current evergreen browsers — **exact matrix TBD – Owner Decision Required** |

Target conformance level (e.g., WCAG tier) = **TBD – Owner Decision Required**; behavioral baseline defined in UI §18.

---

## 16. Reporting Performance

| Operation | Expectation |
|---|---|
| Report generation (`generate` → `draft` snapshot) | **TBD – Owner Decision Required**; may be async for large reports |
| Report retrieval (`GET /reports/{rid}`) | **TBD** |
| Version-history retrieval (`GET /reports/{rid}/snapshots`) | **TBD**; paginated |
| Export (download in `format`) | **TBD**; pdf/html/json |

Snapshots are pinned to runs (replay-accurate); generation cost grows with project size (§7/§8).

---

## 17. Notification Performance

| Operation | Expectation |
|---|---|
| Notification creation (on source change) | **TBD – Owner Decision Required**; should be near-real-time in-product |
| Notification visibility (appears in center) | **TBD**; event-driven (`notification_created`) |
| Refresh | event-driven in-place (UI §20) with manual fallback |

**In-product only — no email/SMS/Slack** assumptions or costs. Notifications never drive analysis.

---

## 18. Analysis Run Performance (by lifecycle state)

Grounded in the `AnalysisRun` lifecycle (Data §10 / State §5):

| State | Performance implication |
|---|---|
| `queued` | time-in-queue counts against the Fast 60s budget; deep queue may coalesce; target queue-time **TBD** |
| `running` | execution time = the §3/§4 targets (Fast < 60s; Deep TBD) |
| `completed` | emits fan-out (confidence/findings/recommendations) — fan-out latency **TBD**, but ordered |
| `failed` | fast emit of `analysis_failed`; prior state intact; retry = new run |
| `cancelled` | prompt termination on `:cancel`; no partial commit |
| `superseded` | bookkeeping transition when a newer run completes; negligible cost; retained |

Queue-time is the hidden contributor to the 60s budget and must be monitored (§13).

---

## 19. Risk Register

| ID | Risk | Category | Impact | Mitigation |
|---|---|---|---|---|
| R-1 | 60s target has no supported-size envelope | Performance | Unbounded promise; missed SLA on large projects | **Owner-set size envelope (top priority)**; gate/queue oversized inputs; monitor TtFMRI by size |
| R-2 | Deep Analysis latency undefined | Performance | Can't tune queueing/coalescing; UX "still working" unbounded | Owner-set Deep band; debounce/cooldown window; non-blocking UI |
| R-3 | AI-call cost per Deep run unbounded | Cost | Unit economics risk, esp. free tier | Coalescing + single-active deep run; per-tier budgets (TBD); fix daily cap |
| R-4 | Data/history growth (append-only) | Data growth | Storage cost + slower reads over time | Retention/pruning policy (TBD); pagination; archive cold history |
| R-5 | Event delivery lag / duplication | Event processing | Stale UI, double-handling | At-least-once + idempotent consumers; ordering by (`timestamp`,`event_id`); dedupe |
| R-6 | Capacity limits undefined | Scalability | Hard to provision; risk under load | Owner-set per-dimension limits; load test once targets exist |
| R-7 | Availability/RTO/RPO undefined | Operational | No reliability bar to design to | Owner-set SLO/RTO/RPO; backups + event replay |
| R-8 | Queue-time erodes 60s budget | Performance | Orientation misses target under load | Monitor queue-time separately; autoscale workers; priority for fast runs |

---

## 20. Open Decisions (no values invented)

**Owner decisions required / TBD values:**

1. **Fast Analysis supported-project-size envelope** (gates the 60s promise) — *highest priority*.
2. Fast Analysis acceptable range (p50/p95) + timeout + retry bound.
3. **Deep Analysis** completion target, range, timeout, debounce/coalesce window.
4. UX interaction targets (§2: create/save/upload/load).
5. API latency targets per class (§5) incl. analysis-ack time.
6. Event throughput / delivery-lag targets + transport choice (§6).
7. Scalability per-dimension limits (§7).
8. **Retention/pruning + hard-delete (incl. GDPR)** policy (§8) — storage/cost decision, *not governance*.
9. Availability SLO + RTO/RPO (§9, §14).
10. Rate-limit + input-size + idempotency-window values (§10).
11. **Cost budgets** — overall + per-pass AI spend; paid-tier limits (§12).
12. Observability alert thresholds (§13).
13. Accessibility conformance level + browser/device matrix (§15).
14. Reporting/notification latency targets (§16, §17).

**Performance / capacity / cost assumptions (explicit, not silent):** in-product notifications ⇒ ~zero external delivery cost; single-active-deep-run + coalescing ⇒ bounded re-analysis cost; append-only history ⇒ growth scales with edits + runs; free tier = 1 active project + daily fix cap. All other quantitative values await owner decision.

---

## Validation

- No Governance concepts — ✅
- No Future Architecture — ✅
- No Agent Governance — ✅
- No new capabilities — ✅
- No new entities — ✅
- No new states — ✅
- Fast Analysis covered — ✅ (§3; 60s target preserved)
- Deep Analysis covered — ✅ (§4)
- Confidence Recalculation covered — ✅ (§4, §18)
- Expanded Findings covered — ✅ (§4)
- Expanded Recommendations covered — ✅ (§4)
- API alignment preserved — ✅ (§5, §18; ack-vs-async distinction)
- State Model alignment preserved — ✅ (§9, §18; lifecycle states verbatim)
- Event Model alignment preserved — ✅ (§6; guarantees, no new events)
- UI alignment preserved — ✅ (§15, §17; event-driven refresh, in-product notifications)
- No quantitative value invented — ✅ (only the owner-approved 60s target is numeric; all else TBD)

**Release 1 Performance & NFR Specification complete.**
