# R2 Slice 3 — Reanalysis Engine + First-Run Freeze/Unlock — Build Design

**Status:** DRAFT — awaiting slice sign-off · **Date:** 2026-08-06 · **Scope:** the event-driven batch reanalysis engine, the read-freshness (STALE) contract, and the first-run freeze/unlock latch.
**Source tags:** `[CAP#1]` = `OSLO_BACKEND_CAPABILITIES.md` cap #1 · `[LAT-*]` = the ingestion-latency instructions · `[AUDIT-*]` = the underspecification audit (§4.3 R2-RE-1…8, §3 landmines DL-L*) · `[PROTO:line]` = `oslo-prototype-r2.html`.

---

## 1. Locked decisions

| # | Decision | Source |
|---|----------|--------|
| D1 | Reanalysis is **event-driven and BATCHED, not per-fix.** Plan-affecting acts enqueue change-events; a debounced/consolidated/cooled-down pass resolves the whole batch and steps integrity **once**. | `[CAP#1]` |
| D2 | **Only reanalysis changes the assessment** (bands / issues / integrity / pillar levels). A manual act only enqueues. The honesty backbone. | `[CAP#1]`; `[AUDIT-4.3]` |
| D3 | Between a change and the next pass the assessment is **STALE = "based on previous analysis"** — an explicitly labelled Pending-Analysis state. | `[CAP#1]`; `[AUDIT R2-RE-5]` |
| D4 | **Two-pass:** Fast Pass ≤60s P95 / ~45s target on the critical path (hard gate, time-to-first-read only, never completeness); Deep Pass off-path + **supersedes**. First-run is **Fast-Pass-only**. | `[LAT-Rec0/L1/E5]` |
| D5 | **Fast Pass emits all 3 pillar initial values** — Viability(CAF), Grounding(all-inferred at t0), Adaptability-v1(coverage) — plus outcomes + primary-confirm-ready. Not CAF alone. | `[LAT-L1a]` |
| D6 | Per-run token caps + **degrade-to-fit** (partial orientation, `Provisional`, defer remainder to Deep) — never a hang. Free Fast=150k/Deep=600k; Basic 300k/1M. | `[LAT-L2/E4]` |
| D7 | **First-run unlock is LATCHED.** `freezeOn = firstRun && confirmCount<2 && !_everUnlocked`; once 2 calls are first reached, `_everUnlocked` sets and the freeze never re-engages if `confirmCount` later dips. | `[PROTO]`; `[AUDIT R2-RE-3]` |
| D8 | The **activation event is immutable** (append-only): the live freeze *gate* may re-lock pre-latch, but the activation *event*, once emitted, is never rewritten by a withdraw. | `[AUDIT DL-L9]` |
| D9 | The freeze is **presentation-only.** The read API must never withhold the read based on `confirmCount`. | `[AUDIT DL-L4]` |
| D10 | Attributed **"your read moved"** durable notification only when the land was **delayed** or the user was **away**; immediate + on-read → transient flash only (`IMMEDIATE_THRESHOLD`). | `[PROTO]`; `[AUDIT R2-RE-5]` |

---

## 2. State Model

**Freeze / unlock (per-user × per-project, durable — R2-RE-3 requires persistence, not the proto's reset-on-reload `firstRun`):**
```
FROZEN     firstRun ∧ confirmCount<2 ∧ ¬everUnlocked        (workspace blurred/pacing gate)
   │  confirmCount reaches 2 (first time)  → set everUnlocked=true  [LATCH]
   ▼
UNLOCKED   everUnlocked ∧ firstRun                            (latched; withdraw cannot re-freeze)
   │  firstRun cleared (onboarding fully done, persistence)
   ▼
NORMAL     ¬firstRun                                          (freeze construct retired)
```
Pre-latch only, a withdraw that drops `confirmCount` below 2 re-enters FROZEN; post-latch it does not. The activation *event* is unaffected in both cases (D8).

**Read-freshness (per-project, orthogonal to freeze):**
```
FRESH → (a plan-affecting act enqueues) → STALE  [labelled — D3]
STALE → (debounce/cooldown fires OR "Reanalyze now") → REANALYZING
REANALYZING → (_completeReanalysis lands, integrity steps once) → FRESH
```
New acts during REANALYZING re-enter STALE for the next batch. Empty queue → `no-change → no-reanalysis` (idempotent).

---

## 3. Data / Object model
- **`ReanalysisPass`** — `{ pass_id, project_id, kind:fast|deep, trigger:intake|batch|explicit|deep-supersede, consolidated_event_ids[], state:queued|running|complete|degraded, prev_integrity{via,grd,ada,min}, new_integrity{…}, settled_issue_ids[], superseded_finding_ids[], token_budget, tokens_used, degraded, provisional, started_at, landed_at }`.
- **Batch queue / consolidation key** — change-event `{ event_id, project_id, issue_key, act_kind, pillar_hint, ts }`. **Consolidation key = `project_id`** (single-active-per-project; all pending acts coalesce into one pass). Window controls `debounce`/`cooldown`/`max-age` are **R2-RE-1 placeholders** (§8). Reuses R1's coalesced-recompute backbone.
- **`ReadFreshness`** — `{ project_id, state:fresh|stale|reanalyzing, pending_count, last_act_ts, based_on_pass_id }`. First-class per R2-RE-5.
- **`FirstRun/unlock state`** (durable, per-user × per-project) — `{ first_run, confirm_count, ever_unlocked, activation_event_id (immutable once set) }`. `confirm_count` is a real server metric (which acts increment, decrement-on-withdraw, durability — R2-RE-4).
- **`ReadMovedNotification`** — `{ project_id, rose[] (pillar→band deltas), settled[] (cause), band, seen, created_at, linger }`.

---

## 4. Event Model
**Acts that ENQUEUE (never resolve directly):** `confirm`, `flag`, `apply-fix`/`fixFromFlag`, `answer-clarify`, `route-response`, `edit`, `add-checkpoint`. Each sets the item `addressed` (recorded, Undo-able, does not move the read) + `_scheduleReanalysis()`.
**Lifecycle:** act → `addressed`, `ReadFreshness→STALE`, arm/refresh debounce → debounce elapses (or explicit "Reanalyze now") → `_runReanalysis` (guard `_pendingCount>0`, single-active) → `_completeReanalysis` resolves each item + **recomputes `min(via,grd,ada)` once** + emits pillar/band events → `FRESH`.
**Fast/Deep:** `intake` → FastPass (critical path, L1a) lands the read; then enqueue DeepPass off-path → `deep-supersede` refines all three pillars via append-only supersession. First-run: no DeepPass on critical path. Over-cap → `degrade` → `Provisional`.
**"Read moved" notification:** fires inside `_completeReanalysis` iff `anyPillar||bandMoved`. Transient always fires; **durable `ReadMovedNotification`** created only when `!(immediate && present)` (`immediate = now−_lastResolveTs ≤ IMMEDIATE_THRESHOLD`, `present = view==='read'`). Self-clears after `READMOVED_LINGER` once seen.

---

## 5. Honesty invariants (testable)
- **I1 only-reanalysis-resolves** — no terminal `you`/`fixed`/integrity move outside `_completeReanalysis`.
- **I2 unlock-latched** — after `confirmCount` first hits 2, a withdraw below 2 leaves `freezeOn()===false`; `everUnlocked` monotonic.
- **I3 activation-event-immutable** — withdraw decrements the live count but never deletes/rewrites the activation event.
- **I4 stale-labelled** — `pending_count>0` ⇒ STALE, and egress surfaces (export/share/roll-up) show "based on previous analysis"; export re-reads first.
- **I5 degrade-not-hang** — over-cap returns a `Provisional` Fast-Pass read <60s; no run exceeds its cap.
- **I6 fast-pass-emits-3-pillars** — Fast-Pass output has non-null V/G/A initial values.
- **I7 freeze-presentation-only** — read API returns full read regardless of `confirmCount`.
- **I8 integrity-steps-once-per-batch** — N acts → exactly one integrity step.

---

## 6. FE↔BE integration bindings

| FE surface / trigger | Direction | BE contract |
|---|---|---|
| confirm/flag/route/fix/answer button | Write | `POST /acts` → `addressed`, enqueue, STALE; never returns a new band |
| "recorded · pending reanalysis"; Undo | Read/Write | `ReadFreshness.state`, `pending_count`; `DELETE /acts/{id}` (undoPending) |
| "Reanalyze now" | Write | `POST /reanalysis:run` (bypass debounce) |
| band "updating…" + pillar/band flash | Event | `reanalysis.landed` → `prev/new_integrity`, `rose[]`, `settled[]` |
| "your read moved" durable banner | Read/Event | `GET /notifications?type=read_moved` (delayed/away only) |
| first-run frozen workspace | Read | `GET /workspace` → `first_run`, `confirm_count`, `ever_unlocked`; freeze client-side |
| unlock reveal | Event | `activation.unlocked` (once, on latch) |
| first read render | Read | Fast-Pass output = L1a (7 artifacts + outcomes + 3 pillars) |
| Deep Pass supersession | Event | `reanalysis.superseded` (append-only) |

---

## 7. R1 reuse vs net-new
**Reuse (recompute backbone — audit §6):** event-driven coalesced recompute, single-active-per-project, `no-change→no-reanalysis`, append-only supersession/history; attestation-ledger primitives back `addressed→resolved`.
**Net-new:** the **seconds-scale grounding-act batch window** (R1 only scoped hours-scale Deep coalescing — R2-RE-1); the **Fast/Deep choice on the batch** (R2-RE-2 / R1 gap G7); the **freeze/unlock latch** (durable first_run/confirm_count/ever_unlocked, one-way-door — R2-RE-3/4); the **causal attributed "your read moved" notification** (R2-RE-5/G8).

---

## 8. Open items / placeholders
- **R2-RE-1 [owner+spec]** exact debounce/cooldown/max-age numbers — proto stubs (1500/900/5000/16000 ms) are illustrative; treat as tuning config, not literals.
- **R2-RE-2/G7 [owner]** Fast-vs-Deep on the grounding-act batch (Fast tier / Deep tier / scoped-incremental?).
- **R2-RE-4 [spec]** `confirmCount` server-metric (which acts count, decrement-on-withdraw, durability).
- **R2-RE-5 [owner]** STALE ambient-vs-egress ruling (main read ambient vs egress labelled).
- **R2-RE-7 [spec]** post-stage-model "next best move" as a computed contract.

---

## 9. Acceptance criteria
1. Fast-Pass first read **<60s P95** on a 10-page doc; the read does not `await` the Deep Pass; first-run triggers no Deep Pass on the critical path.
2. Fast Pass **emits all 3 pillar initial values** + outcomes + confirm-ready primary; any null pillar on first read fails.
3. **Batch coalesces:** N acts in one window → exactly one ReanalysisPass and one integrity step.
4. **Only reanalysis resolves:** an act flips the item to `addressed` and moves neither band nor integrity; the move happens solely in `_completeReanalysis`.
5. **STALE labelled:** while `pending_count>0`, every egress surface renders "based on previous analysis"; export re-reads first.
6. **Unlock latched:** reaching `confirmCount=2` sets `ever_unlocked`; a later withdraw below 2 leaves the workspace unlocked.
7. **Activation-event immutable:** that withdraw decrements the live count but does not delete/rewrite the activation event.
8. **Degrade-not-hang:** a doc 3× the Free budget returns a `Provisional` Fast-Pass read <60s; no run exceeds its cap.
9. **Causal notification:** a delayed/away land creates a durable "your read moved" banner naming pillars-that-rose + the settled cause; an immediate on-read land shows only a transient flash.
10. **Freeze presentation-only:** the read API returns the full read irrespective of `confirmCount`.

*Grounded against cap #1, the two-pass latency contract + L1a, §4.3 R2-RE register, and the prototype. The two owner decisions this slice cannot self-resolve: R2-RE-1 (window numbers) and R2-RE-2/G7 (Fast-vs-Deep batch).*
