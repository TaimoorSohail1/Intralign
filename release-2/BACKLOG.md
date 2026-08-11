# R2 Build Backlog

Nine epics (one per slice) with derived tickets. Each ticket carries: **depends-on**, the **acceptance criteria** it closes (AC-n in the slice doc), the **honesty invariant / `_S10` guard / GT-test** it must satisfy, and any **owner-open blocker**. Build order follows `BUILD_SEQUENCE.md`. Ticket IDs are `R2-S{slice}-{n}`.

Import notes: this is intentionally tracker-agnostic markdown. Epics → epics/labels; tickets → issues. The "Guard/GT" field is the CI assertion that proves the ticket is done; the "AC" field is the human acceptance check in the slice doc.

Legend: 🔒 = **pinned negative** (must stay red-if-violated forever). ⛔ = **owner-open blocker** (mechanism is buildable; a number/choice gates copy/launch). ✦ = net-new (no R1 reuse).

---

## Phase-A · Prototype corrections (pre-build)  ·  epic `R2-PA`
Bring the reference implementation to canon before it is used as the oracle. Source: `BUILD_SEQUENCE.md` → Phase-A corrections; `slices/01`, `slices/08`, `canon/audits/R2_STATE1_BUILD_PLAN.md`.

| ID | Ticket | AC / source | Guard/GT |
|---|---|---|---|
| R2-PA-1 | Replace 4-step band scale with 5-step Fragile→Weak→Developing→Solid→Sound | S1 L8 / DL-195 §6 | `bandsAreWordsNotNumbers`, GT-20 |
| R2-PA-2 | ✅ done-in-oracle 2026-08-08 · foundation-first tie-break `{via:0,grd:1,ada:2}` | S1 L3, AC-2 | `integrityIsWeakestGate`, `integrityTuningFinalized`, GT-19 |
| R2-PA-3 | ✅ done-in-oracle 2026-08-08 · retired the applied-fix-count Viability bump; Viability moves only on real weakness reduction | S1 L10, AC-4 | `integrityTuningFinalized`, GT-11 (via INV-2) |
| R2-PA-4 | ✅ done-in-oracle 2026-08-08 · pillars size-normalized via `bandOf(f)` (`grounded÷ITEMS`, `clear÷UND`, `chk÷needed`); ada ladder now linear | S1 L9, AC-6 | `integrityTuningFinalized`, `pillarLevelsInRange`, GT-13 |
| R2-PA-5 | Build the real DL-196/197 issue layer (`ISS-FC-<art>`) behind the pillars | S1 L6/L7, AC-8 | GT-19, GT-07 |
| R2-PA-6 | `_isActivated()` → DR-6 (2nd grounding act / unlock), retire `confirmCount>=1` | S8 FB-G7 / DR-6 | `unlockLatched`, GT-09 |

---

## Epic 1 · Outcome-Integrity Engine  ·  `slices/01-integrity-engine.md`
The three-pillar read computed from one exposure-gated issue layer. Foundation — build first (Phase A).

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S1-1 | `Issue` object + single exposure-gated issue layer (`{dim,dims,ftype,sec,sev,status,t,rec}`), one queue ranked by outcome-exposure | — | AC-7 | GT-19 | ✦ the resolution unit for all 3 pillars |
| R2-S1-2 | Viability pillar = CAF composite over load-bearing artifacts; movement only from real per-issue weakness reduction | R2-S1-1 | AC-4 | GT-11 | reuse R1 CAF primitives |
| R2-S1-3 | Grounding pillar = grounded ÷ load-bearing + outcome-root cap; `ISS-FC-<art>` false-confidence issue type (one-door) | R2-S1-1 | AC-8 | GT-07 🔒(care-point isolation) | ✦ false-confidence type |
| R2-S1-4 | Adaptability v1 pillar = checkpoint coverage (resolved ÷ needed); checkpoint issues computed, not authored | R2-S1-1 | AC-9 | — | ✦ new peer axis ⛔ checkpoint-needed target |
| R2-S1-5 | Composite `Integrity{level=min, limitingPillar (foundation-first), decomposition}` + moment-in-time pending marker | R2-S1-2,3,4 | AC-1, AC-2, AC-5 | `integrityIsWeakestGate` GT-19, GT-20 | ✦ weakest-gates composite |
| R2-S1-6 | Size-normalization of all denominators; band mapping via config cutpoints `[c1..c4]` | R2-S1-5 | AC-6 | GT-13 | ⛔ cutpoints, load-bearing denominators |
| R2-S1-7 | Care-point isolation guards: Adaptability/Grounding issues never touch `_cafOf`/CAF rows/heat map | R2-S1-3,4 | AC-7 | GT-07 🔒 | pinned negative |

---

## Epic 2 · Issue Lifecycle & Grounding Acts  ·  `slices/02-issue-lifecycle-grounding-acts.md`
The lifecycle, the six acts, the attestation ledger. Phase B.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S2-1 | Lifecycle state machine Inferred→Settling→Resolved with the transition table; **only `_completeReanalysis` resolves** | S1, S3 | AC-2, AC-3 | GT-10 🔒 | the spine |
| R2-S2-2 | Append-only attestation ledger + `BASIS` enum (`documented\|vendor-or-owner-verified\|verified-directly\|answered`) | R2-S2-1 | AC-7 | GT-26 | ✦ `answered` net-new |
| R2-S2-3 | Flag fork: a flag credits Grounding, never firms Viability; statement stays `inferred`; routes to "Acted on · not yet closed" not Resolved | R2-S2-1 | AC-1, AC-8 | `needsFixFork`, GT-11 | INV-3/INV-6 |
| R2-S2-4 | Mitigated fork: a `fixed` (mitigated-ungrounded) item never reads as closed; routes to the same folder with `groundMitigated` | R2-S2-1 | AC-11 | `mitigatedNeedsGrounding`, GT-33 🔒 | INV-9 — the honesty fix |
| R2-S2-5 | Fix firms Viability but never fabricates Grounding; figure stays inference until `groundMitigated` + basis | R2-S2-1 | AC-9 | GT-27 | INV-8 |
| R2-S2-6 | Withdraw-as-new-event across `withdrawItem`/`withdrawRoute`/`groundMitigated` — appends, never erases | R2-S2-1 | AC-4, AC-5 | GT-25 | INV-5 |
| R2-S2-7 | Evidence ≠ comment: comment/@mention can never ground or resolve; structural | R2-S2-1 | AC-6 | GT-12 🔒 | reuse R1 comment obj |
| R2-S2-8 | Route-as-act on the `grounding_act` stream; reviewer answer enqueues like the user's own call | R2-S2-1 | AC-10 | — | feeds S6/S8 |

---

## Epic 3 · Reanalysis Engine + Freeze/Unlock  ·  `slices/03-reanalysis-freeze-unlock.md`
The only writer of a read; the STALE contract; Fast/Deep passes; the freeze latch. Foundation — build with Slice 1 (Phase A).

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S3-1 | Event-driven **batched** reanalysis: acts enqueue (`POST /acts` → `addressed`, STALE); one debounced pass per project resolves the batch and steps integrity **once** | S1 | AC-3, AC-4 | GT-10 🔒, GT-24 | consolidation key = project_id ⛔ window numbers (R2-RE-1) |
| R2-S3-2 | `ReadFreshness` (FRESH/STALE/REANALYZING) first-class; egress surfaces labelled "based on previous analysis" | R2-S3-1 | AC-5 | — | ⛔ ambient-vs-egress (R2-RE-5) |
| R2-S3-3 | Two-pass: Fast Pass ≤60s P95 on the critical path (never awaits Deep); Deep off-path + append-only supersession; first-run Fast-only | R2-S3-1 | AC-1 | — | ✦ seconds-scale batch ⛔ Fast-vs-Deep (R2-RE-2) |
| R2-S3-4 | Fast-Pass output contract (L1a): 7 artifacts + outcomes + **all 3 pillar initial values** + confirm-ready primary | R2-S3-3, S1 | AC-2 | GT-23 | any null pillar fails |
| R2-S3-5 | Per-run token caps + degrade-to-fit (`Provisional`, defer to Deep) — never a hang | R2-S3-3 | AC-8 | — | ⛔ envelope numbers |
| R2-S3-6 | First-run freeze/unlock **latch** (durable `first_run`/`confirm_count`/`ever_unlocked`); freeze is presentation-only | — | AC-6, AC-10 | `unlockLatched`, `freezeFormulaIntact`, GT-04 🔒, GT-18 | ⛔ confirmCount metric spec (R2-RE-4) |
| R2-S3-7 | Activation event immutable (append-only) — withdraw decrements live count, never rewrites the event | R2-S3-6 | AC-7 | GT-09 | DL-L9 |
| R2-S3-8 | Causal attributed "your read moved" durable notification — delayed/away only; immediate+present = transient flash | R2-S3-1 | AC-9 | `readMovedBannerDurable` | ✦ |

---

## Epic 4 · Freemium: Entitlement, Commitment Gate, Outcome-Unit, Archive  ·  `slices/04-freemium-entitlement-commitment-gate.md`
ENFORCE commitment gate, Outcome-as-metered-unit, reversible archive, intent stream. Phase C.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S4-1 | Entitlement/Tier object (Free=1 active outcome:1 plan), `enforcement_mode=enforce`, grants + **never_metered_exemptions[]** first-class | — | AC-9 | `commitmentGatePresent` | reuse R1 tenant/Principal |
| R2-S4-2 | Commitment gate: block → named capability + price → **real hosted checkout** → grant; no silent 422, no silent grant | R2-S4-1 | AC-1, AC-8 | GT-01, INV-6 | ✦ enforce-mode contract ⛔ checkout provider |
| R2-S4-3 | Outcome-as-metered-unit (Workspace→Plan→Outcome); 422 at cap drives the gate | R2-S4-1 | AC-1, AC-2 | — | ✦ reverses R1 "Intend do-not-add" |
| R2-S4-4 | Reversible self-service archive/reactivate; record stays viewable; reactivate guarded when slot full | R2-S4-3 | AC-5, AC-6 | `archiveIsARealFreePath`, GT-03, GT-02 🔒 | DL-L3 |
| R2-S4-5 | Never-metered exemptions enforced: record, reviewer/CRR loop, Viewers — zero `gate_hit` at free | R2-S4-1 | AC-3 | GT-02 🔒 | DL-L2 pinned |
| R2-S4-6 | Gate is capacity-only, never quality: integrity output byte-identical free vs basic | R2-S4-1 | AC-4 | — | INV-3 |
| R2-S4-7 | Intent-signal stream — **every** wall branch emits one row with a distinct `chosen_path` (computable denominator) | R2-S4-2 | AC-7 | `intentCaptureSurfaces`, GT-30 | ✦ fixes the missing-denominator gap |
| R2-S4-8 | Content-metered ingest — over-envelope word count trips `envelope`; many small in-envelope files do not | R2-S4-1 | AC-10 | — | ⛔ ~50k-word Free number |
| R2-S4-9 | Price copy: gate names tier + $29/mo; Pro renders `placeholder` tag | R2-S4-2 | AC-9 | GT-21 (lint) | ⛔ Pro $79 provisional |

---

## Epic 5 · Multi-Outcome Read & Deferred Disclosure  ·  `slices/05-multi-outcome-deferred-disclosure.md`
Read >1 outcome, rank, hold secondaries, disclose post-activation. Phase C.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S5-1 | Multi-outcome NLU at Fast Pass: extract all outcomes, elect primary confirm-ready, seed secondaries `inferred` | S3 | AC-1, AC-5 | `intakeMultiOutcome`, GT-23 | ✦ replaces `_splitOutcomes` heuristic ⛔ detection floor |
| R2-S5-2 | Explainable ranking rationale (`_OC_IMPACT_NOTE`) citing real plan signal — never a template | R2-S5-1 | AC-10 | `intakeMultiOutcome` | ⛔ rationale contract + fallback |
| R2-S5-3 | Held-pool / deferred-disclosure state machine (Rank × Provenance × Disclosure); captured-never-leaked | R2-S5-1 | AC-3, AC-5 | `deferredDisclosure`, GT-22 | HI-1 |
| R2-S5-4 | Primary-only reveal — no secondary in any confirm beat | R2-S5-1 | AC-2 | GT-22 | HI-2 |
| R2-S5-5 | Post-activation disclosure nudge — only when engaged, never in freeze; fire-once, cross-session dismissal | R2-S5-3, S3 | AC-4 | `deferredDisclosure` | ⛔ engagement threshold; ⛔ persistence |
| R2-S5-6 | Disclosure → secondary rows; declaring free, "optimize" routes to the Slice-4 gate; neutral copy (no tier/price) | R2-S5-5, S4 | AC-6, AC-7, AC-9 | GT-21 (lint) | seam to Epic 4 |
| R2-S5-7 | Primary-edit re-reads downstream — re-flags inferred goals/metrics `outcomeStale`; acting clears | R2-S5-1, S3 | AC-8 | `refineReflagsDownstream` | — |

---

## Epic 6 · Collaboration: Reviewer, Roll-up, Grounding Map, Share  ·  `slices/06-collaboration-reviewer-rollup-share.md`
Scoped reviewer, read-only projections, view-only share. Phase D.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S6-1 | Scoped external reviewer — **hard-enforced scope token** granting `{question,source}` only; 403 on anything else | S2 | AC-1 | GT-08 🔒, GT-17 | ✦ access-control, not display ⛔ token shape/TTL |
| R2-S6-2 | Reviewer round-trip: request→deliver→pending→respond→(evidence\|reject→flag)\|withdraw; answer enqueues, resolves on batch, attributed | R2-S6-1, S2 | AC-5, AC-6 | — | reuse R1 StakeholderResponse |
| R2-S6-3 | Collaborator (delegate/PM) sees full read and co-grounds | S2 | AC-2 | — | ⛔ role/access matrix (display-only this release) |
| R2-S6-4 | Roll-up + grounding-map = read-only Disclose projections; **no write path**; every row deep-links | S1 | AC-3 | `ownerDashboardPresent`, GT-14 🔒 | pinned no-write |
| R2-S6-5 | Share = revocable view-only **frozen snapshot**; revoked → 404; live edits don't leak; **never metered** | S1 | AC-4, AC-8 | `sharePanelSimplified`, GT-02 🔒 | reuse R1 SharedArtifact ⛔ viewAudit retention |
| R2-S6-6 | Comment never grounds in the awareness feed; salience-filtered (DL-166) routed-response surfaces, routine quiet | S2 | AC-9, AC-10 | GT-12 🔒 | — |
| R2-S6-7 | k-factor invite = invite-to-own-read; OSLO drafts, user sends; honest "awaiting them" | R2-S6-2 | — | — | ✦ delivery channel |

---

## Epic 7 · Reports & Export / Hand-off  ·  `slices/07-reports-export-handoff.md`
Four reports, real export, scheduling. Phase D.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S7-1 | Four reports — 1 authored (Executive Briefing, editable→immutable memo) + 3 generated projections; a generated report never moves a band | S1, S2 | AC-1, AC-2 | `reportsTabsGenerated`, GT-31 🔒 | reuse R1 Report/ReportSnapshot |
| R2-S7-2 | Real export flow (supersedes "stubbed toasts"): PDF package + PM-tool hand-off + copy | S1 | AC-1 | `exportFlowReal` | ✦ ⛔ which PM tools first |
| R2-S7-3 | Export reanalyzes-if-pending (`_exportGuard` forces one consolidated re-read when pending; else zero recompute) | R2-S7-2, S3 | AC-4 | — | INV-2 |
| R2-S7-4 | Export never maturity-gated; shows honest min-of-three readiness signal ("firms as you confirm more") | R2-S7-2 | AC-5 | GT-28 | ⛔ readiness threshold |
| R2-S7-5 | D153 advisory disclaimer on every package (PDF cover dated to the analysis, memo, done-state) | R2-S7-2 | AC-6 | GT-16 | — |
| R2-S7-6 | PM-tool hand-off pushes **only** the executable plan (task·owner·dates·provenance); no assessment/read crosses | R2-S7-2 | AC-8 | — | ✦ connector auth/mapping/idempotency |
| R2-S7-7 | Free export states "optimized for [primary]" + upgrade path; paid states "all N outcomes" (routes multi-outcome to Slice-4 gate) | R2-S7-2, S4/S5 | AC-7 | — | — |
| R2-S7-8 | Report scheduling: Basic-gated automation, free "send now"; every scheduled send re-reads for currency first | R2-S7-1, S3, S4 | AC-10 | `reportCurrencyDated` | — |
| R2-S7-9 | Sent memo immutable + stale-flagged ("Previous analysis") when the read moves | R2-S7-1 | AC-9 | GT-31 🔒 | — |

---

## Epic 8 · Feedback, Survey & Funnel Telemetry  ·  `slices/08-feedback-survey-telemetry.md`
Side channels that observe the read and are structurally forbidden from changing it. Phase E.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S8-1 | Isolated `feedback_svc` store with **no write grant** to plan/finding/attestation/History; attempted write → permission error | — | AC-1 | GT-06 🔒, `feedbackCapturePresent` | DL-L6 pinned ✦ |
| R2-S8-2 | Feedback ticketing: durable ticket, server-authoritative id, status lifecycle beyond `Filed`, delivered to a real tracker (back-sync) | R2-S8-1 | AC-6 | `defectTicketFormat` | ⛔ which tracker |
| R2-S8-3 | Egress sanitization: free-text redaction/scan; auto-context = allowlisted metadata only (no plan content) | R2-S8-1 | AC-2, AC-3 | GT-05 | DL-L5 ✦ |
| R2-S8-4 | Funnel event stream off one `grounding_act`: `funnel_initiated`(1st act)/`_activated`(2nd act=unlock)/`_engaged`; immutable | S2, S3 | AC-9 | GT-09 | ✦ DR-6 (Activated=2nd act) |
| R2-S8-5 | Survey trigger/targeting engine: eligibility (post-activation+engaged), fire-once, cross-session cooldown, honors dismissal | R2-S8-4 | AC-4 | `surveyTriggerFiresOncePostActivation` | ✦ |
| R2-S8-6 | Readiness/PMF metric: server-computed, non-gating, **never surfaced to the user** | R2-S8-4 | AC-5 | GT-15 🔒 | ⛔ cohort/window/min-N stats |
| R2-S8-7 | Timing A/B: sticky durable per-user variant, immutable for life, stamped on every survey event | R2-S8-5 | AC-8 | GT-32 | ✦ |
| R2-S8-8 | Intent-capture is the **only** side channel that writes History (deliberate narrow exemption); feedback+survey write zero History | R2-S8-1 | AC-10 | GT-29 🔒 | ⛔ confirm exemption |

---

## Epic 9 · Doctrine Guardrails as Tests + FE↔BE Integration Map (keystone)  ·  `slices/09-doctrine-guardrails-integration-map.md`
Read the map first (Phase 0); close the suite last. Binds and proves the other eight.

| ID | Ticket | Depends | AC | Guard/GT | Notes |
|---|---|---|---|---|---|
| R2-S9-1 | Adopt the consolidated FE↔BE Integration Map as the build contract — a surface not in it is not shippable | all | AC (S9 §2) | — | the keystone |
| R2-S9-2 | Port all 59 `_S10` client guards to named **server twins** (shape-check → data/permission check); names preserved | all | AC-9 (S9) | GT-01…GT-33 | L4 |
| R2-S9-3 | Stand up the GT-01…GT-33 register as a CI merge gate; a red suite blocks the build | all | S9 §3 | — | L3 |
| R2-S9-4 | Pin the two negative classes red-if-violated forever: no-write projections + never-metered exemptions | S4,S6,S7,S8 | S9 §3 | 🔒 set | L7 |
| R2-S9-5 | Quarantine owner-open placeholders as `pending()` tests (neither pass nor fail the gate until ratified) | all | S9 §8 | — | L9 |

---

## Owner-Open Decisions (consolidated — non-blocking to design)
Every mechanism is buildable now; these numbers/choices gate copy, launch, or tuning. Ratify in a batch in parallel with the build. Keep each value in config.

| # | Decision | Slice(s) | Blocks |
|---|---|---|---|
| O-1 | ✅ **RESOLVED 2026-08-08** — cutpoints `[.25,.5,.75,1]` (Sound = full completion), size-normalized ratio denominators (DevNorth 6/4/3), checkpoint-needed = **1 per outcome-bearing workstream**, interior labels **Weak·Developing·Solid**. Applied to the oracle (`integrityTuningFinalized`); slice-01 §7 updated. Formal DL to be landed via dl-land (proposed **DL-206**). | S1 | — closed (was: R2-S1-4, R2-S1-6 tuning) |
| O-2 | Reanalysis window numbers (debounce/cooldown/max-age, R2-RE-1) | S3 | R2-S3-1 tuning |
| O-3 | Fast-vs-Deep on the grounding-act batch (R2-RE-2) | S3 | R2-S3-3 policy |
| O-4 | `confirmCount` server-metric spec (which acts count, decrement-on-withdraw, R2-RE-4); STALE ambient-vs-egress (R2-RE-5) | S3 | R2-S3-6, R2-S3-2 |
| O-5 | `answered`-basis strength; reviewer-reject→flag authority; withdraw→reanalysis; `groundMitigated` ledger shape | S2 | R2-S2-2/6/8 semantics |
| O-6 | Pro price ($79 provisional); exact envelope numbers (~50k-word Free, file rails); checkout provider; subscription lifecycle | S4 | R2-S4-8/9 copy/launch |
| O-7 | Disclosure engagement threshold; rationale-generation contract + low-confidence fallback; secondary-detection floor; disclosure/dismissal persistence | S5 | R2-S5-2/5 |
| O-8 | Owner-vs-delegate role/access matrix; recipient-tailoring enum; scope-token shape/TTL/revocation; viewAudit retention/consent | S6 | R2-S6-1/3 |
| O-9 | Which PM tools ship first (Asana suggested); report names; readiness-signal threshold; copy/clipboard serialization | S7 | R2-S7-2/4 launch |
| O-10 | Which feedback tracker (Linear/Jira/internal); readiness-gate statistics (cohort/window/min-N); free-text retention/consent (GDPR); intent-vs-History exemption confirmation | S8 | R2-S8-2/6/8 |

*All items also appear in each slice's §8 "Open items / placeholders" with full context.*

---

## Tier-2 / Basic — Deferred (post-R2)  ·  epic `T2-MO`
**Trigger:** begin when **tier-two (Basic tier) product design starts** (owner Idris, 2026-08-08). Do **not** build into the R2 single-outcome line before then. This is the *integrity architecture across multiple committed outcomes* — distinct from **Epic 5** (which is the R2 multi-outcome *read* + deferred disclosure: extract/rank/hold/disclose). Epic 5 lets OSLO *read* >1 outcome at Free; **T2-MO** lets a project *carry and optimize* N outcomes at Basic, with integrity computed and reconciled across them. Belongs to Basic per freemium doctrine (multi-outcome = capacity gate, DR-7).

**Design of record:** `release-2/oslo-integrity-architecture.md` (Part B). Current single-outcome prototype = the **N=1** slice of this model.

| ID | Ticket | Depends | Notes |
|---|---|---|---|
| T2-MO-1 | Add `outcome` field to every `Issue`; make the current single outcome `Outcome[1]` | Epic 1, Epic 5 | ✦ additive; issue layer already carries `dim/ftype/sev/target` |
| T2-MO-2 | Cascade tree per outcome: Outcome → Goal → SuccessCriterion → KPI (grounded\|inferred per node) | T2-MO-1 | ✦ generalizes the single "intent" tree |
| T2-MO-3 | Per-outcome pillar computation (Grounding/Viability/Adaptability scoped to that outcome's issues) + per-outcome `Integrity(O)=min(pillars)` | T2-MO-1,2 | reuse Epic 1 engine, scoped |
| T2-MO-4 | Project rollup: pillar rollups across outcomes → `Integrity(Project)=min(rollups)≡min over O of Integrity(O)` (associative under `min`) | T2-MO-3 | preserves the weakest-gates invariant at N outcomes |
| T2-MO-5 | **Aggregation policy = primary-gates** (recommended): headline `min` over *committed* outcomes (primary always; secondaries as activated); inferred secondaries shown with own band, don't gate headline | T2-MO-4 | ⛔ owner-ratify vs strict-min / weighted; dovetails with the Slice-4 commitment gate |
| T2-MO-6 | Shared-artifact issue **fan-out**: one issue on a shared artifact (budget/calendar) attributes to every dependent outcome, resolves once (closes for all) | T2-MO-1 | ✦ |
| T2-MO-7 | **Cross-outcome conflict** issue type (`dim:via`, feasibility): two outcomes contend for the same constrained resource; attributes to both; resolves by re-allocation/re-prioritization | T2-MO-1 | ✦ the one issue class that cannot exist at N=1 |
| T2-MO-8 | Proposals + pillars reconcile per outcome: proposals stay optional/band-neutral scoped per outcome; each pillar keeps its cross-outcome rollup + per-outcome drill-down | T2-MO-3 | honesty rule unchanged |

**Prereq DONE (2026-08-08, R2 line):** the owner's invariant — *resolve every open issue → every pillar Sound → integrity Sound, no dead-ends* — was verified + fixed on the R2 prototype. Fixes: reconciled `issueOpen` for 3 dead-end execution issues (`sponsor-deadline`/`catering-owner`/`no-checkpoints`); made the integrity **ceiling** reachable (metrics lever now grounds Intent's inferred lines; held secondary outcome excluded from Viability, owned by the disclosure flow); proposals folded into the read as optional accept/reject rows. Guards: `issuesResolvableNoDeadEnds`, `nextStepToSoundLegible`, `proposalsFoldedIntoRead`, `welcomeBackDigest`.

**Formal ratification:** the primary-gates aggregation (T2-MO-5) and the cross-outcome conflict type (T2-MO-7) warrant a governed **DL** when Tier-2 design opens (via the dl-land procedure) — not minted here.
