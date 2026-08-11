# R2 Slice 5 — Multi-Outcome Read & Deferred Disclosure — Build Design

*Grill artifact · 2026-08-06 · DRAFT — awaiting sign-off. Grounding: capability #16 (freemium/cardinality, multi-outcome NLU); the L1a Fast-Pass output contract; prototype outcome/deferred-disclosure/reveal hooks.*

This slice owns **the moment and the data** for reading more than one outcome from an intake brief, ranking primary vs secondary with an explainable rationale, and disclosing the held secondaries at the right funnel moment. It does **not** own the paywall — the Basic commitment gate (DL-202/DR-7) is Slice 4; this slice produces the captured secondaries and routes the disclosure into that gate.

## 1. Locked decisions
- **LD-5.1** Multi-outcome read is **net-new NLU**; outcome is the metered unit (DL-172). *[RATIFIED — cap #16]*
- **LD-5.2** Both primary and secondaries **captured DURING the Fast Pass** — primary confirm-ready + secondary detection + primary-selection rationale, before the confirm card renders. Data-must-exist-at-Fast-Pass, not Deep-Pass. *[RATIFIED — L1a]*
- **LD-5.3** **Deferred disclosure, funnel-optimized:** the first-run reveal stays **primary-only** to protect activation; secondaries captured-but-**held**, surfaced **post-activation once engaged**. Holding is presentation, not a data gap. *[RATIFIED — owner 2026-08-06]*
- **LD-5.4** Disclosure is an **engagement + multi-outcome upsell moment** ("here's what OSLO also read"), routing optimization into the Basic gate. NOT a first-run mention. *[RATIFIED — owner 2026-08-06]*
- **LD-5.5** **Optimizing secondaries is a Basic capability** (declaring is always free; OSLO optimizing >1 at once is paid). *[RATIFIED — DL-201/202/DR-7]*
- **LD-5.6** **Editing the primary re-reads downstream** — re-flags inferred goals/metrics `outcomeStale`; acting clears it. *[RATIFIED — proto `_grReReadFromOutcome`]*
- **LD-5.7** **Neutral copy** — no tier name/price on disclosure surfaces; only the gate names Basic. *[cap #16]*

## 2. State model
Orthogonal axes per plan:
- **Rank:** `primary` (singleton, the target optimized on Free) vs `secondary`. `_setPrimaryOutcome` enforces singleton.
- **Provenance:** `inferred` (OSLO read) vs `you` (declared) — a `you` secondary is visible immediately; an `inferred` secondary enters the held pool.
- **Disclosure:** `_ocDisclosed` (one-way), `_ocNudgeDismissed` (the "Not now" latch).
- **Held pool** = `!primary && prov==='inferred'`; **Visible secondaries** = `!primary && (_ocDisclosed || prov!=='inferred')`.
**Disclosure-eligibility** (`_ocNudgeEligible`): `engaged AND NOT disclosed AND NOT dismissed AND held-pool non-empty AND NOT frozen`. `engaged = _isEngaged()` (past unlock + ≥1 further act; **note DR-6: activation = 2nd act**). The not-frozen clause is defensive but MUST be asserted independently so a future `_isEngaged` change can't leak a disclosure into the frozen first-run.
**Downstream staleness:** inferred goal/success/kpi items carry `outcomeStale` (true on primary edit, false on any act).

## 3. Data / object model
**Outcome** (item in `intent`, `type:'outcome'`): `id · type · primary(bool, singleton) · text · prov{inferred,you} · rank(derived) · rationale`. Seed: `o1` primary inferred, `o2` secondary inferred (both read during analysis).
**Ranking rationale** (`_OC_IMPACT_NOTE`): a per-plan explainable string tying primary-over-secondary to real plan evidence — model-generated from extracted artifacts, **must cite the actual signal**, never a template.
**Held-pool**: a derived view (`_heldOutcomes()`), not a separate store — no data hidden, only rendering gated.
**Disclosure state**: `_ocDisclosed`/`_ocNudgeDismissed` become durable per-user/plan fields (feed #15) so disclosure fires once and honors cross-session dismissal.

## 4. Event model
1. **Fast-Pass multi-outcome detection + ranking** — extracts all outcomes, elects primary confirm-ready, seeds secondaries `inferred`, produces `_OC_IMPACT_NOTE`; emitted with the confirm card (L1a). Deep Pass may refine, not on the critical path.
2. **Reveal (primary-only)** — `_GR_BEATS` confirm beat binds `_primaryOutcome()` only; confirming sets primary `prov:'you'`, `confirmCount++`.
3. **Disclosure-eligible → nudge** — `_ocDiscloseNudge()` in the right rail ("I also read N more… held until you'd settled in"); post-engagement only, never in freeze.
4. **Disclose** — `_discloseOutcomes()` sets `_ocDisclosed`, opens Intent; secondaries render as "declared, not optimized on Free · make primary · optimize both →"; "optimize both" → `vmOutcomeCap('outcome')` → `_payGate('multiOutcome')` (Basic gate).
5. **Dismiss** — latches; the held note stays in Intent, the rail nudge doesn't re-fire.
6. **User declares own secondary** — `_addOutcome` sets `_ocDisclosed=true`, adds `prov:'you'` secondary, visible at once.
7. **Primary edit → re-flag** — `_grReReadFromOutcome` sets `outcomeStale` on inferred goals/metrics.

## 5. Honesty invariants (testable)
- **HI-1 captured-never-leaked** — while `!_ocDisclosed && held>0`, `_visibleSecondaries().length===0` and the masthead lead shows no "+N more" (guard `deferredDisclosure`).
- **HI-2 primary-only reveal** — no secondary node/text in any `_GR_BEATS` beat.
- **HI-3 disclosure-only-when-engaged** — `_ocNudgeEligible()` ⇒ engaged && !frozen.
- **HI-4 honest count pre-disclosure** — the muted note shows the true `_heldOutcomes().length`.
- **HI-5 rationale explainable not fabricated** — `_OC_IMPACT_NOTE` cites real signal (guard `intakeMultiOutcome`; keyword-split heuristic `_splitOutcomes` retired).
- **HI-6 pre-disclosure every secondary is OSLO's read** — all `prov==='inferred'`.
- **HI-7 declaring free, optimizing gated** — no surface implies declaring costs money; only "optimize" routes to the gate.

## 6. FE↔BE integration bindings
| FE surface | Hook | BE binding |
|---|---|---|
| Reveal confirm card (primary) | `_GR_BEATS`, `_confirmOutcome` | Fast-Pass returns primary confirm-ready + prov; confirm → attestation ledger (#2), activation telemetry (#15) |
| Held-count note (Intent) | `_heldOutcomes()`, `int-obadge held` | read API returns held secondaries `prov:'inferred'`; count exposed, rows suppressed until `_ocDisclosed` |
| Disclosure nudge | `_ocNudgeEligible`/`_ocDiscloseNudge`/`_discloseOutcomes`/`_dismissOcNudge` | engagement signal (`_isEngaged`); disclosure+dismissal persisted per-user/plan, cross-session, fire-once (#15) |
| Post-activation engagement/upsell | `_discloseOutcomes` → secondary rows → `vmOutcomeCap`/`_payGate` | entitlement (Free=1 optimized); DL-202 gate (Slice 4); intent logged (#16 VM-1a) |
| Secondary rows | `_visibleSecondaries`, `_setPrimaryOutcome` | re-election writes primary; "optimize" hits gate; declaring free |
| Primary-edit re-flag | `_grReReadFromOutcome`, `outcomeStale` | event-driven recompute (#1); stale until reanalysis |

## 7. R1 reuse vs net-new
**Reuse:** outcome-as-root grounding (`_rootOutcomeHTML`, Grounding cap at root); Intent artifact + typed statements; reveal/analysis engine; activation/engagement signals; event-driven recompute + stale contract (#1); the commitment-gate primitive (Slice 4).
**Net-new:** multi-outcome NLU + ranking with explainable rationale at Fast-Pass; the deferred-disclosure state machine (held pool, eligibility, post-activation nudge); the primary-edit downstream re-flag. R1 read one outcome; cardinality, holding, and the disclosure moment are all new.

## 8. Open items / placeholders
- **OI-1** engagement threshold for disclosure (independent of the survey A/B?) — owner-TBD.
- **OI-2** rationale-generation contract (model prompt/schema grounding `_OC_IMPACT_NOTE`; low-confidence fallback).
- **OI-3** secondary-detection confidence floor ("second outcome vs goal") — precision bar so weak reads don't inflate the held count.
- **OI-4** cross-session persistence of `_ocDisclosed`/`_ocNudgeDismissed` (in-memory in proto).
- **OI-5** Deep-Pass secondary refinement after disclosure.
- **OI-6** ordering + per-secondary rationale for N>1 held.

## 9. Acceptance criteria
- **AC-1** Fast Pass emits primary confirm-ready + ≥0 secondaries + non-empty `_OC_IMPACT_NOTE` before the confirm card (guard `intakeMultiOutcome`).
- **AC-2** The reveal shows **only the primary**; no secondary in any beat.
- **AC-3** While `!_ocDisclosed` and held>0, no held secondary renders anywhere; lead shows no "+N more" (guard `deferredDisclosure`).
- **AC-4** The nudge fires **only post-engagement** and never during freeze.
- **AC-5** Pre-disclosure the note shows the true held count; every secondary is `prov:'inferred'`.
- **AC-6** Disclosing reveals secondaries as "not optimized on Free" and the "optimize" action routes to the Basic gate.
- **AC-7** Declaring an outcome is free, adds a visible `prov:'you'` secondary, sets `_ocDisclosed`.
- **AC-8** Editing the primary re-flags downstream inferred items `outcomeStale`; acting clears (guard `refineReflagsDownstream`).
- **AC-9** No tier name/price on any disclosure/held/secondary surface.
- **AC-10** `_OC_IMPACT_NOTE` cites real plan signal; `_splitOutcomes` heuristic absent (guard `intakeMultiOutcome`).

*Slice 5 owns the multi-outcome read, the held-pool/deferred-disclosure state machine, and the post-activation disclosure moment; hands optimization to the Slice-4 Basic gate.*
