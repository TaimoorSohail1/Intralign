# R2 Slice 8 — Feedback, Survey & Funnel Telemetry — Build Design

*Grill artifact · 2026-08-06 · DRAFT — awaiting sign-off. Derived from capabilities #15/#17/#18; audit §4.5 (FB-G1…FB-G13) + landmines DL-L5/DL-L6; DR-6 (Activated = 2nd grounding act) + DL-162 (funnel telemetry); the prototype feedback/survey/telemetry surfaces.*

**Scope:** three side-channel telemetry capabilities that observe the read but are **structurally forbidden from changing it** — feedback **ticketing**, the PMF/readiness **survey + trigger/targeting engine + timing A/B**, and the durable **funnel event stream**. Almost entirely net-new; the one large reuse target is the R1 telemetry envelope/pipeline.
**Correction this design lands (FB-G7/DR-6):** the prototype's `_isActivated()` returns `confirmCount>=1` (DL-173 "first act") — ratified **DR-6 supersedes this to the 2nd grounding act (the unlock)**. This design builds to DR-6.

## 1. Locked decisions
| # | Decision | Source |
|---|---|---|
| L1 | Feedback + survey live in an **isolated store with no write credentials** to plan/finding/attestation/History. Structural, asserted by test. | DL-L6; FB-G4 |
| L2 | Free-text passes a **redaction/scan at the feedback-service egress**; auto-context is an **allowlist of metadata only**. "No plan content leaves" is a mechanism. | DL-L5; FB-G3 |
| L3 | A filed item is a **durable ticket** with **server-authoritative id** and a **status lifecycle beyond `Filed`**; delivered to a real tracker. | cap #17; FB-G1/G2 |
| L4 | Defect tickets capture **reproduction context** = view/route + sanitized state, **never plan content**. | cap #17; DL-L5 |
| L5 | **Activated = 2nd grounding act (unlock); Engaged = an act past unlock.** From one `grounding_act` stream, not the freeze. | DR-6; DL-162 |
| L6 | The readiness metric (PMF ~40%-"very disappointed" bar) is **server-computed, non-gating, NEVER surfaced to the user.** | cap #18 |
| L7 | Survey is **triggered**: post-activation + engaged, **fire-once-per-user, cross-session cooldown, honors dismissal**. | cap #18; FB-G7/G8 |
| L8 | The timing A/B (`immediate`/`delayed`) uses a **sticky, durable per-user variant assignment** stamped on every survey event. | cap #18; FB-G9 |
| L9 | Feedback/survey **never `pushHist`**; **intent-capture (`_recordIntent`) is a deliberate, narrow History exemption** (recommended, §8). | audit §4.5; proto |
| L10 | Funnel events are a **durable event stream** feeding the readiness gate, intent signals (#16), and feedback/survey. | cap #15; DL-162 |

## 2. State Model
**Ticket lifecycle** (server-owned; supersedes proto's single `status:'Filed'`): `Filed → Triaged → {Accepted|Duplicate|Won't-fix} → In-progress → Resolved → Closed`. Triage adds de-dup/component/priority (FB-G12); work states back-sync to OSLO for the "Filed this session" echo (FB-G2).
**Survey-eligibility** (per user, cross-session — proto's single-session booleans become durable): `Ineligible → Eligible → Nudged → {Answered|Dismissed}` (both terminal — never re-nag). `Ineligible→Eligible`: `activated(≥2 acts) && engaged && !answered && !dismissed && cooldown-elapsed`. Dismissal honored cross-session forever.
**A/B assignment:** `Unassigned → Assigned{immediate|delayed}` — sticky at first eligibility eval, immutable for the user's lifetime; governs the engagement threshold + stamped on the response.

## 3. Data / Object model
- **Ticket** (isolated store) `{id(DEF/ENH/NOTE-####, server-authoritative), category{defect,enhancement,other}, title, body(post-egress-sanitized), status, priority(from impact), component, dedup_key, defect_only:{expected, impact{blocking,slowing,minor}, repro_context}, created_at, tracker_ref}`. `repro_context` = **allowlisted metadata only**: `{where, view, role, grounded_x, total_y, first_run_flag, ts}` — no plan content.
- **SurveyResponse** (isolated store) `{id, user, pmf{very,somewhat,not}, csat 1..5, open_text(post-egress-sanitized), trigger_variant{immediate,delayed}, cohort, created_at}`.
- **TelemetryEvent** (durable stream on the R1 envelope) `{envelope:{event_name, id, is_internal, ts, session, props}, kind{activation,engagement,experiment,intent,feedback,survey}}`. Funnel milestones off one `grounding_act` stream: `funnel_initiated`(1st act), `funnel_activated`(2nd act — unlock), `funnel_engaged`(act past unlock). **Immutable once emitted** (DL-L9).
- **The isolated store boundary:** feedback + survey persist in a `feedback_svc` datastore with a principal that has **no write grant** to plan/finding/attestation/History schemas; auto-context is assembled client-side from view/role/counts. This is the architectural form of DL-L6 (not "the handler happens not to call `pushHist`").

## 4. Event Model
**Feedback: filed → sanitize → deliver** — `submitFeedback()` → `feedback_svc.file(ticket)` (isolated store, mints id) → **egress sanitizer** (redaction/scan on free-text + allowlist-validate auto-context; reject/redact on plan-content match) → deliver to tracker (field-map, auth, retry, idempotent on `dedup_key`; status back-syncs) → emit `feedback_filed` (no free-text in the event).
**Survey: trigger-eligible → nudge → response** — on read render, server evaluates eligibility; if `Eligible`, `_surveyNudgeHTML()` renders the fire-once nudge inline → `openSurveyFromNudge`/`dismissSurveyNudge` (durable dismissal) → `submitSurvey()` → `feedback_svc.saveResponse` → egress-sanitize → emit `survey_responded {pmf,csat,variant}`. **The read is untouched.** A windowed job recomputes the readiness metric (internal only).
**Funnel:** each grounding act emits `grounding_act`; the pipeline derives `funnel_initiated/_activated/_engaged` (L5). `_recordIntent` emits `intent_signal {vm,tier(internal),ctx,chosen_path}` **and** (per L9 exemption) a History entry — the only side channel that does so.

## 5. Honesty invariants (testable)
| # | Invariant | Test |
|---|---|---|
| H1 | Feedback/survey **structurally cannot** write to read/band/issues/History | `feedback_svc` principal has zero grants; attempted write → permission error |
| H2 | Free-text **sanitized at egress** | inject a defect body with a known plan figure → redacted before the tracker call |
| H3 | Auto-context **metadata-only** | `repro_context` keys ⊆ allowlist; no artifact/statement/figure text |
| H4 | Readiness metric **non-gating + never rendered** | no read/band/entitlement path consumes the PMF metric; no FE surface renders it |
| H5 | Nudge fires **only post-activation+engaged, once, honoring dismissal** | pre-activation eligibility false; after dismissal → never eligible cross-session |
| H6 | Activation event **survives withdraw** | emit activation, withdraw below threshold → live freeze may re-lock; the activation event persists (DL-L9) |

## 6. FE↔BE integration bindings
| FE surface | Trigger | BE contract | Type |
|---|---|---|---|
| Feedback door | `feedbackDoorHTML`/`submitFeedback` | `POST feedback_svc/tickets` → sanitize → tracker; mints server id | Write+Event |
| "Filed this session" list | `_FEEDBACK_LOG` echo | `GET feedback_svc/tickets?session` (status back-sync) | Read |
| Defect auto-context | `_fbContext`/`_fbCtxLine` | client-assembled allowlist metadata; no plan read | Write(metadata) |
| Survey door | `surveyDoorHTML`/`submitSurvey` | `POST feedback_svc/survey` → sanitize; stamps variant | Write+Event |
| Survey nudge (fire-once) | `_surveyNudgeHTML`/`_surveyTriggerEligible` | `GET funnel/eligibility` (durable per-user state) | Read |
| Nudge open/dismiss | `openSurveyFromNudge`/`dismissSurveyNudge` | `POST funnel/nudge:{opened\|dismissed}` (persist) | Write |
| A/B assignment | `_SURVEY_TRIGGER_AB` | `GET experiments/assign(survey_timing)` sticky | Read+Event |
| Grounding-act emitters | `confirmCount++` in `itemAct`/`routeTo`/confirm-outcome | `POST telemetry/grounding_act` → funnel milestones | Event |
| Intent walls | `_recordIntent` | `POST telemetry/intent_signal` (+ History, L9) | Event |

## 7. R1 reuse vs net-new
**Reuse (§6/§7):** the **telemetry event envelope + pipeline** — typed envelope, `is_internal`, dual-write to `analytics_events`, PostHog/ClickHouse, internal-account exclusion, identity stitching (in `OSLO_RELEASE_1_OBSERVABILITY…`). Slice 8's events ride this envelope; do not re-spec it.
**Net-new:** feedback/survey **events not in the R1 taxonomy** (`grounding_act`, `funnel_*`, `intent_signal`, `feedback_filed`, `survey_responded`); the **egress sanitization boundary** (DL-L5); the **readiness computation** (PMF → ~40% gate over cohort/window/min-N — FB-G5); the **trigger/targeting engine** + **A/B assignment service** (FB-G8/G9); the **isolated store + credential boundary** (DL-L6).

## 8. Open items / placeholders
- **[OWNER]** which tracker (Linear/Jira/internal queue) — field mapping, auth, retry, status back-sync (FB-G2).
- **[OWNER+SPEC]** readiness gate parameters: cohort, rolling window, min-N before the ~40% bar is read (FB-G5). The bar is ratified; the statistics are not.
- **[OWNER]** intent-vs-History exemption (L9). Recommended: "side channels never touch the read" holds absolutely for feedback+survey; intent-capture is a deliberate narrow exemption (writes History + its own intent stream ONLY, never plan/finding/band) — an intent moment is an in-product event the user *should* see narrated. Confirm + encode as the exemption test.
- **[SPEC]** retention/consent for free text (GDPR erasure — FB-G13).
- **[SPEC]** de-dup/triage fields (`dedup_key`, component, priority-from-impact — FB-G12).

## 9. Acceptance criteria
1. A feedback submit **cannot alter any band/issue/History** — `feedback_svc` has no write grant; an attempted write fails.
2. Free-text containing plan content is **redacted at egress** before the tracker call.
3. Auto-context is **metadata-only** — `repro_context` keys ⊆ allowlist; no plan text.
4. The survey nudge fires **only post-activation (2nd act) + engaged, once per user, honoring dismissal** cross-session; pre-activation eligibility always false.
5. The readiness metric is **never rendered to the user** and no read/band/entitlement path consumes it.
6. A ticket gets a **server-authoritative unique id** and moves through **states beyond `Filed`**, with tracker status back-synced.
7. **Activation events are immutable** — a withdraw below threshold re-locks the live freeze but leaves the activation event intact.
8. The **A/B variant is sticky per user** and stamped on every survey event.
9. **Funnel milestones derive from the `grounding_act` stream** — Activated = 2nd act, not `score_viewed` or the freeze.
10. **Intent-capture is the only side channel that writes History**; feedback + survey produce zero History entries.

*Builds on Slice 2's `grounding_act` stream and the DR-6 activation ruling; hands its invariants to Slice 9. Two prototype corrections: `_isActivated()` = confirmCount>=1 is stale vs DR-6 (2nd act); `_recordIntent` `pushHist` is the deliberate narrow exemption (owner to confirm).*
