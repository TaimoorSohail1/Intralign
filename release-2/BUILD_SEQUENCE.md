# R2 Build Sequence

Dependency-ordered plan for building the nine R2 slices. The ordering follows the data dependencies in each slice's "R1 reuse vs net-new" and cross-references, not calendar convenience. Slice 9 is the exception: its **integration map is read first** (it is the contract every surface builds against), while its **test suite closes last** (it can only be fully green once the surfaces exist).

**The spine that constrains all ordering:** only reanalysis resolves. Every act enqueues; a batched re-read is the sole writer of a band/issue/integrity move. So the integrity engine (what a read *is*) and the reanalysis engine (the only thing that *moves* a read) are the two foundations; everything else is a surface or a side channel over them.

---

## Phase 0 — Establish the contract (before any surface work)

- **Adopt Slice 9 §2 (FE↔BE Integration Map) as the build contract.** Every dynamic surface must have a row: `{Reads, Written-by (act), Changed-by (event)}`. A surface not in the map is not shippable. New surfaces amend the map first.
- **Stand up the `_S10` → GT-01…GT-44 harness skeleton** (Slice 9 §3; GT-34…GT-44 = the DL-209/Slice 10 twins) in CI as pending/allowed-red, so guards go green slice-by-slice rather than all at the end.
- **Apply the Phase-A prototype corrections** (below) so the reference implementation matches canon before it is used as the oracle.

---

## Phase A — Foundation (parallel pair)

These two have no dependency on any other slice and everything depends on them. Build together.

### Slice 1 — Outcome-Integrity Engine  ·  `slices/01-integrity-engine.md`
The three-pillar engine (Viability × Grounding × Adaptability), weakest-gates `min()`, computed from the single exposure-gated issue layer. This is what a "read" *is*.
- **Depends on:** nothing (foundation). Reuses R1 CAF/Reliability + grounding/provenance primitives.
- **Delivers to everyone:** the `Issue` object, `Pillar`, `Integrity{level,limitingPillar,decomposition}`, the false-confidence issue type, the exposure queue.
- **Owner-open blockers:** band cutpoints `[c1..c4]`; load-bearing denominators; checkpoint-needed target; the three interior band labels. (All tuning config — build the mechanism, keep numbers in config.)

### Slice 3 — Reanalysis Engine + First-Run Freeze/Unlock  ·  `slices/03-reanalysis-freeze-unlock.md`
The event-driven batched reanalysis engine, the STALE freshness contract, the Fast/Deep two-pass (Fast ≤60s P95), and the latched first-run freeze/unlock.
- **Depends on:** Slice 1's `Integrity` (it recomputes `min()`); otherwise foundation. Reuses R1 coalesced-recompute backbone.
- **Delivers to everyone:** `POST /acts` (enqueue), `_completeReanalysis` (the sole resolver), `ReadFreshness`, the freeze/unlock latch, the "your read moved" notification, the Fast-Pass L1a output contract.
- **Owner-open blockers:** debounce/cooldown/max-age window numbers (R2-RE-1); Fast-vs-Deep on the grounding-act batch (R2-RE-2); `confirmCount` server-metric spec (R2-RE-4); STALE ambient-vs-egress ruling (R2-RE-5).

> **Why paired:** Slice 1 defines the read; Slice 3 is the only thing allowed to change it. Neither is useful without the other, and both are prerequisites to every later slice. Build and integrate them together, then freeze the `only-reanalysis-resolves` invariant (`GT-10`, pinned) before proceeding.

---

## Phase B — Core lifecycle

### Slice 2 — Issue Lifecycle & Grounding Acts  ·  `slices/02-issue-lifecycle-grounding-acts.md`
The item lifecycle (Inferred → Settling → Resolved / the two "acted-on-not-closed" forks), the grounding acts (confirm/flag/fix/route/answer/withdraw), the append-only attestation ledger + BASIS enum.
- **Depends on:** Slice 1 (`Issue` object), Slice 3 (act→enqueue→reanalysis→resolve). Reuses R1 attestation primitives + apply-fix + StakeholderResponse seam.
- **Delivers to later slices:** the `grounding_act` stream (consumed by S6 route-as-act, S8 funnel), the attestation ledger, the "Acted on · not yet closed" folder, `groundMitigated`/`fixFromFlag`.
- **Owner-open blockers:** `answered`-basis strength; reviewer-reject → flag authority; withdraw→reanalysis; `groundMitigated` ledger shape.

---

## Phase B+ — Load-bearing sensitivity & issue classification (DL-209)

### Slice 10 — Load-Bearing Sensitivity + Issue-Classification Engine  ·  `slices/10-load-bearing-sensitivity-engine.md`
The L0 dependency graph, the deterministic L1 sensitivity engine (structural pre-filter → two-sided counterfactual span, uncertainty/runway-aware), the thin L2 calibration gate (global threshold at launch, dormant segmentation), the static L3 classification table (finding-type → pillar + acts; retires the hand-set `primaryMove`), and the optional offline L4 feedback loop. This is what makes an issue *an issue* (load-bearing) and derives *how it closes* (verify/build/decide).
- **Depends on:** Slice 1 (the `Integrity` function it recomputes under counterfactuals; the `Issue`/exposure objects) and Slice 2 (the derived resolution affordance replaces the authored one). Extends both; freeze `onlyVerifyMovesGrounding` (GT-35, pinned) with them.
- **Delivers to everyone:** the load-bearing gate (`isLoadBearing`), the sensitivity/exposure ordering, and the derived issue-card primary act (a pinned no-write projection of the model).
- **Build note:** ship **L0→L3 with a conservative global `LB_THRESHOLD`** (the ratified launch policy) — deterministic and defensible day one; **L4 + domain segmentation are v2**, snapping onto L2 without touching the invariants.
- **Owner-open blockers:** the `LB_THRESHOLD` launch value + asymmetric-loss/floor params (resolved by the §7 **calibration procedure** — shadow-run → owner boundary review → lock → telemetry-confirm); the L0 classifier-validation track; L4 holdout design. None blocks the mechanism.

> **Why after Slice 2:** the sensitivity engine decides which issues are load-bearing and the classification decides how each closes — both operate over the `Issue` object (Slice 1) and drive the resolution affordance (Slice 2). It cannot precede its inputs, and every read surface downstream consumes its `loadBearing`/`exposureRank`/`primaryAct` output.

---

## Phase C — Read surfaces (the funnel)

### Slice 5 — Multi-Outcome Read & Deferred Disclosure  ·  `slices/05-multi-outcome-deferred-disclosure.md`
Reading >1 outcome from an intake brief, primary/secondary ranking with explainable rationale, the held-pool/deferred-disclosure state machine, post-activation disclosure.
- **Depends on:** Slice 3 (Fast-Pass emits primary + secondaries), Slice 1 (integrity per outcome), Slice 2 (confirm-outcome as an act). **Hands optimization to Slice 4's gate.**
- **Owner-open blockers:** engagement threshold for disclosure; rationale-generation contract + low-confidence fallback; secondary-detection confidence floor; cross-session persistence of disclosure/dismissal.

### Slice 4 — Freemium: Entitlement, Commitment Gate, Outcome-Unit, Archive  ·  `slices/04-freemium-entitlement-commitment-gate.md`
The tier/entitlement model (Free = 1 active outcome), the ENFORCE commitment gate (block → named capability + price → real checkout → grant), Outcome-as-metered-unit, reversible archive, the intent-signal stream.
- **Depends on:** Slice 5 routes multi-outcome optimization into this gate; otherwise self-contained. **Reuses (re-aligned) R1 422/checkout canon — not superseded.**
- **Build note:** enforcement is **ENFORCE**, not observe (DL-202/DR-3 reverse the audit's original "observe" — see the slice's central correction). The prototype already implements the reversed model.
- **Owner-open blockers:** Pro price ($79 provisional); exact envelope numbers; checkout provider; subscription lifecycle (deferred).

> **Why 5 before/with 4:** Slice 5 produces the captured-but-held secondaries and the disclosure moment that *drives traffic into* the gate. Slice 4 is the gate. Build 5's read + disclosure first (or in parallel), then 4's gate is the thing disclosure routes to. Either can ship its non-shared parts independently; the seam is `_discloseOutcomes → vmOutcomeCap → _payGate`.

---

## Phase D — Collaboration & output

### Slice 6 — Collaboration: Reviewer Round-Trip, Roll-up, Grounding Map, Share  ·  `slices/06-collaboration-reviewer-rollup-share.md`
The hard-enforced scoped external reviewer, the read-only roll-up + grounding-map projections, the revocable view-only share snapshot, the role model, the k-factor invite.
- **Depends on:** Slice 2 (attestation ledger + route-as-act; reviewer answer enqueues like the user's own call), Slice 1 (integrity for roll-up). Reuses R1 sharing/comment/notification canon.
- **Keystone within the slice:** the external reviewer is a **hard-enforced scope (403 on anything else)** — an access-control guarantee, not display-only. Roll-up/grounding-map are **pinned no-write** projections.
- **Owner-open blockers:** owner-vs-delegate role/access matrix (display-only this release); recipient-tailoring enum; scope-token shape/revocation; viewAudit retention.

### Slice 7 — Reports & Export / Hand-off  ·  `slices/07-reports-export-handoff.md`
Four reports (1 authored + 3 generated projections), real export (PDF w/ D153 disclaimer, PM-tool hand-off, copy), export reanalyzes-if-pending, Basic-gated scheduling with a free send-now.
- **Depends on:** Slice 1/2/3 (a generated report is a projection of the committed read; export forces one consolidated re-read when pending, via Slice 3). Reuses R1 Report/ReportSnapshot.
- **Build note:** export is a **real flow, not a stub** (supersedes capability #10's stale "stubbed toasts" wording); never maturity-gated, shows an honest readiness signal.
- **Owner-open blockers:** which PM tools ship first (Asana first suggested); recipient-tailoring enum; report names; readiness-signal threshold.

---

## Phase E — Telemetry (side channels)

### Slice 8 — Feedback, Survey & Funnel Telemetry  ·  `slices/08-feedback-survey-telemetry.md`
Feedback ticketing, the PMF/readiness survey + trigger/targeting + timing A/B, the durable funnel event stream.
- **Depends on:** Slice 2 (`grounding_act` stream → funnel milestones), Slice 3 (activation = the unlock). Reuses R1 telemetry envelope/pipeline.
- **Structurally forbidden from changing the read:** feedback + survey live in an isolated store with **no write grant** to plan/finding/attestation/History; free-text is sanitized at egress. Both are pinned negatives.
- **Prototype correction owed:** `_isActivated()` = `confirmCount>=1` is stale vs **DR-6 (Activated = 2nd grounding act, the unlock)** — this slice builds to DR-6.
- **Owner-open blockers:** which tracker (Linear/Jira/internal); readiness-gate statistics (cohort/window/min-N); retention/consent for free text; intent-vs-History exemption confirmation.

---

## Continuous — the keystone

### Slice 9 — Doctrine Guardrails as Tests + FE↔BE Integration Map  ·  `slices/09-doctrine-guardrails-integration-map.md`
Read first (Phase 0), close last. The integration map is the standing contract; the GT-01…GT-44 register (incl. the DL-209/Slice 10 twins) + the `_S10` guards' server twins go green slice-by-slice and must all be green — with the pinned negatives red-if-violated forever — before R2 ships.
- **Depends on:** all slices (it binds and proves them). Ships no new capability.

---

## Phase-A prototype corrections (apply before using the prototype as oracle)

These are small, known deltas where the reference prototype currently deviates from ratified canon. Each slice doc flags its own; consolidated here:

1. **5-step bands.** Prototype ships a 4-step scale (`Very Low·Low·Moderate·Sound`); canon is **5-step Fragile→Weak→Developing→Solid→Sound** (DL-195 §6). (Slice 1)
2. **Foundation-first tie-break.** Prototype's `_gate()` tie-breaks Grounding-first `{grd:0,via:1,ada:2}`; canon is **Viability→Grounding→Adaptability** `{via:0,grd:1,ada:2}` (DL-195 §6). (Slice 1)
3. **Viability from weakness reduction, not a fix count.** Retire the prototype's `_fixedCount()>=2 → +1` bump (Slice 1 L10).
4. **Bands normalize to plan size.** Replace the DevNorth-fixture absolute cutoffs (`/6`, `/4`, `>=3`) with size-normalized fractions (Slice 1 L9).
5. **False-confidence issue layer.** Pillars currently read from hardcoded fixture counts, not the DL-196/197 issue layer (`ISS-FC-<art>`). Build the real issue layer (Slice 1 L6/L7).
6. **Activation = 2nd act.** `_isActivated()` = `confirmCount>=1` is stale vs **DR-6** (Activated = 2nd grounding act / the unlock) (Slice 8 FB-G7/DR-6).

Items 3–5 are the substantive engine build (Slice 1 / the State-1 Phase-A plan in `canon/audits/R2_STATE1_BUILD_PLAN.md`); items 1, 2, 6 are small edits.

---

## Owner-open decisions (non-blocking to design; gate copy/launch/tuning)

Every `[owner]`/`[spec]` item across the nine slices is consolidated in `BACKLOG.md` → **Owner-Open Decisions**. None is architectural; all can be ratified in a batch in parallel with the build. Build the mechanism, keep the value in config.
