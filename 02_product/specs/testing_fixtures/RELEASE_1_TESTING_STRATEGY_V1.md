# Release 1 Testing Strategy v1

**Type:** Release 1 Testing Strategy Specification
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded exclusively in:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` · `RELEASE_1_UI_SPECIFICATION_V1.md` · `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md`

> **Scope guardrails.** Active Release 1 only. **No new architecture, entities, states, events, capabilities, workflows, or future scope.** Testing **validates** behavior defined by the specifications; it never **redefines** it. The State Model is the lifecycle authority, the Event Model the event authority, the API Contract the interface authority, the UI Spec the UI authority, and the NFR Spec the performance authority. The **only** approved numeric performance threshold is the **60-second Time-to-First-MRI**; all other performance targets are tested as **`TBD – Owner Decision Required`** (no thresholds invented).
>
> *Filename note: the NFR spec is cited by its actual repo name, `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md`.*

---

## 1. Purpose

Testing exists to give **confidence in the implementation** of Release 1: that behavior matches the specs, that user outcomes (orientation, expanded understanding, improvement) actually occur, and that changes don't silently break what works.

- **Confidence in implementation** — every spec'd behavior has at least one executable check.
- **Verification of behavior** — commands cause the sanctioned transitions and emit the defined events; nothing more, nothing less.
- **Prevention of regression** — a maintained suite gates releases so fixed behavior stays fixed.
- **Validation of user outcomes** — the 60-Second Orientation, Deep Analysis expansion, and the find→recommend→improve loop are validated end to end, not just unit-wise.

---

## 2. Testing Philosophy

- **Event-driven verification** — behavior is asserted as *command → transition → emitted event → persistence → (notification) → UI refresh*, matching the Event Model.
- **Deterministic outcomes** — same input + same state ⇒ same output and same transition (§6); flakiness is treated as a defect.
- **Replayability** — replaying the event log reconstructs identical state; tests exercise this (§7).
- **Tenant isolation** — every cross-workspace access path is a negative test (§12).
- **Traceability** — every test traces to a capability/spec clause (§4); no orphan tests, no untested clauses.
- **User-centric validation** — acceptance suites are framed around the Canonical Scope journey and real outcomes, not internal mechanics.

**Explicit principle:** *Testing validates the system behavior defined by the specifications and does not redefine behavior.* Where a spec is `TBD`, the test asserts the **structural** behavior and marks the quantitative bound `TBD – Owner Decision Required` rather than inventing one.

---

## 3. Test Pyramid

| Level | Purpose | Coverage | Examples |
|---|---|---|---|
| **Unit** | Validate isolated logic | enum/state validators, transition guards, payload builders, supersession-pointer logic | "acknowledge is rejected unless status=`detected`"; "new ConfidenceState sets `supersedes_confidence_state_id`" |
| **Integration** | Validate components together | persistence ↔ analysis engine ↔ event bus | "completing a run writes CAFState+ConfidenceState and emits the fan-out in order" |
| **API Contract** | Validate the interface | request/response schema, status codes, auth, idempotency | "`POST /findings/{id}:acknowledge` on a `closed` finding → `409`" |
| **Workflow** | Validate multi-step journeys | the Canonical Scope sequence across services | "create → evidence → fast run → orientation → deep run → expanded findings" |
| **System** | Validate the whole deployed stack | end-to-end incl. UI + events | "user creates project and sees orientation within budget" |
| **Acceptance** | Validate spec'd outcomes (§5) | capability acceptance criteria (Matrix §16) | Suites A–I |
| **Performance** | Validate approved NFRs (§14) | Time-to-First-MRI; others TBD | "TtFMRI < 60s for in-envelope project" |
| **Security** | Validate boundaries (§13) | authN/authZ, isolation, exposure | "Workspace A token cannot read B's project" |
| **Regression** | Prevent backsliding (§15) | critical-path + previously-fixed defects | smoke suite on every release candidate |

---

## 4. Traceability Model

Every test traces along the backbone so coverage is auditable:

```text
Capability (Matrix V2)
  → Entity (Data Model v1.1)
     → State (State Model)
        → Event (Event Model)
           → API (API Contract)
              → UI (UI Spec)
                 → Test Case(s)
```

**Framework:** a traceability matrix keyed by capability ID maps each capability to its entity, the State Model lifecycle(s) it touches, the Event(s) it emits, the API endpoint(s), the UI screen(s), and the test case IDs that cover them. Acceptance gate: **no capability without a test; no test without a spec clause.** Example row — *"Acknowledge Finding"* → `Finding` → `detected→acknowledged` → `finding_updated` → `POST /findings/{id}:acknowledge` → Findings Workspace → `TC-F-ACK-01..n`.

---

## 5. Release 1 Acceptance Suites

### Suite A — Project Lifecycle
Validate: project **creation** (`created`); **analysis initiation** (fast run → `orienting`); **orientation** (`oriented`); **deep analysis** (`deep_analyzing → analyzed`, recurring); **completion/archival** (`archived`, terminal). Assert illegal jumps rejected (e.g., `created → deep_analyzing`).

### Suite B — Fast Analysis Pass
Validate: **run creation** (`run_type=fast_analysis_pass`, `queued`); **state transitions** `queued→running→completed`; **confidence generation** (one initial `ConfidenceState`); **findings generation** (initial `detected` findings); **recommendations generation** (initial `generated` recs). Assert events `fast_analysis_requested→started→completed` + fan-out.

### Suite C — 60-Second Orientation
Validate: **Time-to-First-MRI** (< 60s, in-envelope — §14); **confidence display** (value+band+reliability); **findings display** (top by severity); **recommendation display** (tied to findings). **Must explicitly test that Fast Analysis is NOT the final analysis state** — assert the project is `oriented` (not terminal), the "Deep Analysis in progress" banner condition holds, and a deep run is queued/expected.

### Suite D — Deep Analysis Pass
Validate: **confidence recalculation** (new `ConfidenceState` superseding prior; `confidence_recalculated`+`confidence_superseded`); **expanded findings** (`first_seen_run_id` = deep run); **expanded recommendations**; **supersession chains** (superseded findings/recs/confidence retained, not deleted).

### Suite E — Findings Lifecycle
Validate **every** Finding transition per State Model §10: `detected→acknowledged→addressed→closed`, `closed→reopened`, `{detected,acknowledged,addressed}→superseded`. Assert invalid transitions rejected (`detected→closed`, `superseded→*`). State Model is authority.

### Suite F — Recommendation Lifecycle
Validate **every** Recommendation transition per State Model §11: `generated→accepted`, `generated→rejected`, `accepted→implemented`, `{generated,accepted}→superseded`. Assert invalid transitions rejected (`rejected→implemented`). State Model is authority.

### Suite G — Notifications
Validate: **creation** (`created`); **display**; **viewing** (`viewed`); **dismissal** (`dismissed`); **expiration** (`expired`). Assert notifications **never trigger analysis** and have no analysis consumers. **In-product only — no external channels** (no email/SMS/Slack test paths exist).

### Suite H — Collaboration
Validate: **comments** (threaded on artifact/version/finding/project); **mentions** (→ `notification_created`); **shared artifacts** (`created→shared→viewed→revoked/expired`); **permissions** (view vs comment enforced).

### Suite I — Reporting
Validate: **report generation** (`draft` + snapshot); **snapshots** (pinned to `generated_from_run_id`); **exports** (pdf/html/json); **version history** (append-only chain); status `draft→published→superseded→archived`.

---

## 6. Determinism Test Strategy

Dedicated suite asserting **same input ⇒ same output**. With fixed inputs and a fixed model/config (and any stochasticity seeded/pinned per the engine's determinism contract), re-running the same pass on the same project state must yield equivalent results:

- **Fast Analysis** — same evidence/artifacts ⇒ same CAFState, ConfidenceState band, and the same set of initial findings/recommendations.
- **Deep Analysis** — same inputs ⇒ same expanded findings/recommendations and the same recalculated confidence.
- **Findings / Recommendations** — same analysis ⇒ same items (stable identity/type/severity).
- **Confidence** — same inputs ⇒ same value/band/qualifier.

**Examples:** run Fast twice on a frozen fixture → assert identical finding-type set and confidence band; replay a deep run → assert identical expanded-finding count and supersession links. Non-determinism is a defect (or an explicitly-documented tolerance owned by the engine spec, not invented here).

---

## 7. Replayability Test Strategy

Validate that replaying the ordered event log reconstructs state exactly (Event Model §17, set-to-state):

- **Historical replay** — replay genesis→now ⇒ identical current state; external side effects suppressed.
- **AnalysisRun reconstruction** — run chain (`previous_run_id`) and statuses rebuild identically.
- **Confidence reconstruction** — `supersedes_confidence_state_id` chain rebuilds the same trend.
- **Finding reconstruction** — finding statuses + supersession rebuild identically.
- **Recommendation reconstruction** — same, including superseded items.

**Methodology:** snapshot state → replay event log into a clean store → diff reconstructed vs original (must be empty, modulo suppressed side effects). Also test duplicate/out-of-order delivery → dedupe + reorder yields the same state.

---

## 8. Event Model Validation

Validate **every** event. For each event class assert the full chain:

```text
Event → State Transition → Persistence → (Notification) → UI Refresh
```

| Event class | Assertion |
|---|---|
| Project (`project_created/updated/archived`) | correct `lifecycle_state`; persisted; UI badge |
| Artifact/Context (`artifact_*`, `evidence_added`, `context_item_*`) | recompute trigger fires per §15 rules; persisted |
| Analysis (`*_analysis_requested/started/completed`, `analysis_failed/cancelled/superseded`) | run status; fan-out ordered; UI progress |
| Confidence (`confidence_created/recalculated/superseded`) | ConfidenceState + supersession; UI chip |
| Finding (`finding_created/updated/closed/reopened/superseded`) | status; persisted; UI row + maybe notification |
| Recommendation (`recommendation_created/accepted/rejected/implemented/superseded`) | status; persisted; UI row |
| Notification (`notification_created/viewed/dismissed/expired`) | state; **no analysis consumer**; UI center |
| Collaboration (`comment_created/mention_created/artifact_shared/share_revoked/share_expired`) | persistence; notification; UI |
| Reporting (`report_generated/published/superseded/archived`) | Report status; snapshot; UI |

**Methodology:** emit/trigger each event in a controlled fixture; assert (a) the exact target state, (b) the persisted row, (c) notification creation iff specified, (d) the UI region updates (§20 of UI). Assert **no new event types** appear and idempotency on `event_id`.

---

## 9. State Transition Validation

Validate every state machine exhaustively (legal + illegal), State Model as authority:

| Entity | Legal transitions asserted | Illegal transitions rejected |
|---|---|---|
| **Project** | created→orienting→oriented→deep_analyzing→analyzed (↺), →archived | created→deep_analyzing; archived→* |
| **AnalysisRun** | queued→running→completed; →failed/cancelled; completed→superseded | completed→running; superseded→* |
| **Finding** | detected→acknowledged→addressed→closed; closed→reopened; →superseded | detected→closed; superseded→* |
| **Recommendation** | generated→accepted→implemented; generated→rejected; →superseded | rejected→implemented; implemented→generated |
| **Notification** | created→viewed→dismissed; →expired | dismissed→viewed; expired→viewed |
| **Comment** | created (+reply thread) | n/a (no lifecycle states) |
| **SharedArtifact** | created→shared→viewed→revoked/expired | revoked→shared; expired→shared |
| **Report** | draft→published→superseded→archived | published→draft |

Coverage target: **every edge in each State Model diagram has a passing legal-path test and a rejected illegal-path test.**

---

## 10. API Contract Validation

Validate per the API Contract: **request schema** (required fields, enum validation, reject-unknown), **response schema** (resource + emitted-event names), **authorization** (role gates), **error handling**, **status codes** (400/401/403/404/409/422/429/500). **Negative testing is required**: malformed bodies → 400; missing/invalid token → 401; forbidden role/share scope → 403; cross-workspace → 404; illegal transition → 409; constraint violation (free-tier limit, bad permission_level) → 422; rate/limit → 429. Assert idempotency-key replay returns the original result with no duplicate resource/event.

---

## 11. UI Validation Strategy

Validate per the UI Spec (authority): **screen rendering** (13 screens + embedded views), **state visibility** (labels = v1.1 enums, §15), **action enablement** (buttons enabled only on legal source state — prevents the `409` path), **error messaging** (mapped to API error model, UI §17), **empty states** (per screen). Specifically assert the **60-Second Orientation "not final / Deep Analysis in progress" banner**, event-driven in-place refresh (UI §20), and that no UI state exists outside the model enums.

---

## 12. Tenant Isolation Testing

Validate **Workspace A cannot access Workspace B** across every path:

- **Direct access attempts** — A's token requesting B's `project_id`/`finding_id`/etc. → `404` (existence not leaked).
- **API access** — every list/get is filtered by caller `workspace_id`; no parameter injection bypasses it.
- **Shared-artifact boundaries** — a share grants only the single `shared_object_id` at its `permission_level`, only while `shared`/`viewed`; `revoked`/`expired` → `403`/`404`; comment-permission cannot escalate to edit.
- **Report boundaries** — a shared report exposes only that snapshot, not the project or sibling reports.

Isolation tests are mandatory negative tests on every tenant-scoped resource.

---

## 13. Security Testing (Release 1 only)

Validate: **authentication** (valid/invalid/expired token → 200/401), **authorization** (role-gated commands; member cannot archive/revoke beyond rights → 403), **permissions** (view vs comment), **session handling** (token lifecycle/expiry), **data-exposure prevention** (404 hides cross-tenant existence; no secret/PII leakage in responses or logs; input validation rejects injection-shaped payloads). **No future/enterprise features** (no SSO, no compliance-framework tests); rate-limit enforcement (`429`) included.

---

## 14. Performance Testing

Validate **only approved NFRs.**

### Time-to-First-MRI (the one approved threshold)
- **Requirement:** < **60 seconds** for a project within the supported-size envelope.
- **Methodology:** seeded in-envelope fixtures; measure from `fast_analysis_requested` (or project-create + first input) to MRI/orientation available; report distribution (p50/p95) and queue-time vs compute-time separately (NFR §18).
- **Pass/fail:** in-envelope runs meet < 60s at the agreed percentile (percentile itself is `TBD – Owner Decision Required`); **out-of-envelope inputs are excluded** until the envelope is set.

### All other performance targets
**`TBD – Owner Decision Required`** — Deep Analysis latency, API latencies, event throughput/lag, reporting/notification latency, scalability limits. Tests are **scaffolded** (harness + metrics in place) but assert structure only; numeric pass/fail is added when owners set values (NFR §20). **No thresholds invented.**

---

## 15. Regression Testing Strategy

- **Release gates** — the acceptance suites (A–I) + determinism + replay + isolation + the 60s test must pass for a release candidate to proceed.
- **Automated regression suites** — full suite on every candidate; run in CI on merge to the release branch.
- **Smoke tests** — fast critical-path subset (create → fast run → orientation; finding acknowledge; deep run → expansion) on every build.
- **Critical-path protection** — the Canonical Scope journey and tenant isolation are designated non-negotiable; any failure blocks release. Every fixed defect adds a regression test.

---

## 16. Test Data Strategy

Synthetic, versioned fixtures (no real customer data):

- **Synthetic projects** — deterministic, fixture-pinned for determinism/replay.
- **Small projects** — minimal evidence; fast-path and envelope baseline.
- **Medium projects** — multi-artifact; exercise expansion and pagination.
- **Ambiguity-heavy projects** — rich in ambiguity/assumption findings (exercise CAF Clarity).
- **Contradiction-heavy projects** — designed to trigger conflict findings + contradiction discovery in Deep Analysis.
- **Deep Analysis datasets** — fixtures that reliably produce expanded findings/recommendations and confidence recalculation across multiple deep runs (for supersession/replay).

Fixtures are frozen and checksum-pinned so determinism tests are stable.

---

## 17. Environment Strategy

| Environment | Purpose |
|---|---|
| **Local** | unit + fast integration; developer inner loop; mocked event transport |
| **Integration** | cross-service integration, API contract, event-bus, determinism/replay against real services |
| **Staging** | full system + acceptance + isolation + the 60s performance test; production-like; release-candidate gate |
| **Production validation** | post-deploy smoke + synthetic monitoring (no real-tenant data mutation); confirms health, not feature testing |

Tenant data never crosses environments (mirrors isolation requirement).

---

## 18. Test Reporting

- **Execution reporting** — pass/fail/skipped per suite + traceability coverage (capabilities covered vs total).
- **Defect reporting** — severity, the spec clause violated, reproduction, linked test.
- **Pass/fail reporting** — per release gate (§19), with the 60s distribution surfaced explicitly.
- **Release readiness reporting** — a single go/no-go view aggregating gate status, open criticals, and outstanding `TBD` performance items (flagged, not blocking unless owner-designated).

---

## 19. Release Readiness Criteria

Release 1 ships only when **all** hold:

- **Acceptance suites A–I** pass.
- **Security** tests pass (authN/authZ, permissions, exposure).
- **Determinism** suite passes (same input ⇒ same output).
- **Replayability** suite passes (log replay reconstructs state).
- **Tenant isolation** passes (no cross-workspace access on any path).
- **Time-to-First-MRI** < 60s for in-envelope projects at the agreed percentile.
- **Regression/smoke** green; zero open critical defects.

Outstanding `TBD` performance targets are **reported** but gate release only where an owner has designated them release-blocking.

---

## 20. Open Questions (captured, not resolved)

1. **Determinism tolerance** — is analysis bit-exact, or is a bounded semantic-equivalence tolerance allowed? (Owned by the analysis-engine contract.)
2. **Approved percentile** for the 60s target (p50/p95?) — owner/NFR.
3. **Size envelope** defining "in-envelope" for the 60s test — owner/NFR (§14 dependency).
4. **Event transport** under test (websocket/SSE/poll) — affects UI-refresh test harness.
5. **Performance pass/fail thresholds** for all non-60s targets — owner/NFR §20.
6. **Replay side-effect-suppression** boundary — which effects are internal vs external.
7. **Load/soak** scope and capacity targets — pending scalability limits.

---

## Validation

- No new architecture introduced — ✅
- No new entities introduced — ✅
- No new states introduced — ✅
- No new events introduced — ✅
- No governance concepts introduced — ✅
- No future architecture introduced — ✅
- State Model used as lifecycle authority — ✅ (§5E/F, §9)
- Event Model used as event authority — ✅ (§8)
- API Contract used as interface authority — ✅ (§10)
- UI Specification used as UI authority — ✅ (§11)
- NFR Specification used as performance authority — ✅ (§14; only 60s numeric, rest TBD)
- Release 1 only — ✅

**Release 1 Testing Strategy complete.**
