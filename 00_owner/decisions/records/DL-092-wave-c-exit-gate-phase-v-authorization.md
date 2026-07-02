# DL-092 — Wave C (Advise) exit-gate pass + Phase V / Wave U authorization

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** DL-044 (per-wave exit-gate / authorization cadence); DL-072 (Wave B exit-gate pass + Phase IV/Wave C authorization, with three binding conditions RB-025 / RB-026 / DL-046-latency); PR #46 (Phase IV / Wave C — Advise, merged to `main`); PR #80 (Wave C exit-gate conditions — commit `2512fe4`, merged `88e0690`); the AI-drafted Wave C exit-gate review (`00_owner/decisions/WAVE_C_EXIT_GATE_REVIEW_DRAFT.md`, 2026-06-29); 2026-07-02 code survey of `code/`. Owner ratification via the Founder Console.
- **Layer:** Delivery governance (DL-044 wave gate). No doctrine / constitution / responsibility change.

---

## Review (Framework 001A — five outputs)

### Findings

1. **Wave C (Advise) functional scope is delivered and green on `main`.** `IC-WC-ADVISE` is built in `code/backend/responsibilities/advise/`: DTM-0014 (Recommendation + Clarification Request, each anchored to a Finding/Issue; live A→B→C chain) and DTM-0015 (`SuggestedFix` + Validation that **never auto-writes**, DL-047 advisory-only). Invariants enforced by negatives in `code/tests/negative/advise/` (anchoring + Resolution-Path-as-substructure; no autonomous fix write; one-producer boundary; CHR-append-on-recompute + history). CI at the Wave C candidate: ruff clean · gate-4/5 PASS · live suite 587/0 · A→B→C e2e green (DTM-0014/0015, EM-approved 2026-06-18).

2. **DL-072 Condition 1 — Unarchive (RB-025, DL-058) — MET.** `code/backend/responsibilities/retain/archival.py` now implements `unarchive_assertion(...)`: it appends an append-only `history_record` reversal entry (`event_type='unarchived'`, LDM §2.5 vocabulary) and emits `knowledge_unarchived` + `knowledge_mutation_recorded`. **No row is mutated** — status is re-derived from history (the latest of `archived` / `unarchived` wins), and unarchiving a non-archived assertion is rejected ("nothing to reverse"). Covered by `code/tests/positive/retain_retention/test_b2_unarchival.py` (+ `test_b2_archival.py`), with the guard behavior asserted via `pytest.raises`. The related OBS-WA-002 escalation was closed (contract + traceability-matrix updated; CI doc-links fixed — commit `a31ffdd`).

3. **DL-072 Condition 2 — CAF driver-decomposability negative test (RB-026, DL-062 Cond 1) — MET.** `code/tests/negative/evaluate/test_b3_caf_decomposability.py` asserts the three CAF drivers stay **individually inspectable** (clarity / alignment / feasibility, each reducing to its own index / band / per-dimension reliability) and **forbids an opaque rollup** — `score`, `rollup`, `composite`, `caf_score`, `clarity_rollup`, `overall` are rejected structurally (`extra='forbid'` → `ValidationError`). This is exactly the QA negative DL-062 Condition 1 mandated.

4. **DL-072 Condition 3 — live <60s Time-to-First-MRI (DL-046) — HARNESS READY; GO MEASUREMENT PENDING (owner-run).** The go/no-go harness `code/scripts/latency_proof/run_latency_proof.py` (+ README) landed via #80. It proves the Fast-Pass Time-to-First-MRI against the ratified <60s ceiling on a **live internal-Gemma** model — the one path CI never exercises (its "live" e2e uses recorded fixtures, zero provider calls). Per its README it **must run in the owner/engineering environment** (live Gemma runtime + local Supabase) and **cannot run in the assistant sandbox**. As of the 2026-07-02 survey, **no `latency_proof_result.json` / GO verdict is committed** — so the *measurement* is not yet on record even though the tooling is complete. (p50/p95 are reported-only; DL-046 targets p50≤25s / p95≤50s are owner-TBD, OPEN_TBD A2 — only the <60s ceiling gates.)

5. **Process / drift.** Phase V / Wave U (#69) was opened **before** this Wave C exit gate ran — the same "engineering ahead of the per-wave gate" pattern flagged in the DL-072 process note. This gate should adopt a cadence guard so the pattern does not recur at the Wave U → Wave E boundary.

### Concerns

1. **Latency is the load-bearing unknown.** It is the only Wave C condition that could surface a *real* architecture/performance problem (live Gemma vs the <60s ceiling), it has now been deferred across two gates, and it gates both this review and the open DL-070 Phase 1 sign-off. It must be run to a recorded **GO** before Phase V authorization is effective — treat it as go/no-go, latency **first**.
2. **Two conditions cleared cleanly; do not let the third slip on assumption.** RB-025 and RB-026 are met and provable on `main`. Recording latency as "done" because the *harness* landed would mis-state the gate (Anti-Assumption): the harness is not the measurement.
3. **Advisory-only must stay provable downstream.** DL-047 is enforced today (`test_c3_no_autonomous_fix_write.py`); the unarchive path and all Phase V work must preserve append-only / no-destruction and never cross into execution.
4. **Cadence risk.** Building the next wave before the prior gate ratifies erodes the DL-044 cadence; without a guard it recurs.

### Dependencies

- **DL-044** (wave gate cadence) · **DL-072** (the three carried conditions) · **DL-068 Cond 3** (unarchive origin).
- **DL-058** (archive reversible in R1; UP-3) → RB-025 (met). · **DL-062 Cond 1** (CAF decomposability) → RB-026 (met). · **DL-046** (Fast/Deep + <60s) and **DL-070** (Phase 1 sign-off) → the live latency GO (pending).
- **DL-047 / Positioning §9** (advisory-only) — invariant for unarchive and all downstream waves.
- **Downstream:** Phase V / Wave U (#69) is blocked on this gate; Phase VI / Wave E (#81) and Release 1 Completion (#82) follow Wave U, one PR to `main` at a time (DL-065).

### Recommendation

**Pass — two of three conditions discharged; Phase V authorization effective on the recorded latency GO.** Accept the Wave C (Advise) build as candidate-complete and green on `main`; record RB-025 (unarchive) and RB-026 (CAF decomposability) as **discharged**; and **authorize Phase V / Wave U** to land — **effective when the owner runs the live-Gemma Time-to-First-MRI proof to a GO verdict and attaches `latency_proof_result.json`** (which also clears the DL-070 latency condition). If a NO-GO is recorded, Phase V authorization does not take effect: file an engineering finding on where the budget is spent and escalate before further work. Plus two non-blocking items: adopt a **gate-before-next-wave-PR** cadence guard, and reconcile any stale Phase IV plan status.

*Alternative for the owner:* if you have **already** run the latency proof to GO in your environment, record that verdict/date inline and this becomes a clean **Pass** with Phase V authorized immediately.

### Status

**Recommended: Pass (conditions 1–2 discharged; latency GO to be recorded).** Owner ratification required — Framework 001A: AI analyzed / checked consistency / recommended; the owner ratifies. Phase V / Wave U authorization is **conditional on the latency GO** and not effective until it is recorded.

---

## Decision (owner ratifies)

1. **Wave C (Advise) PASSES the DL-044 exit gate.** `IC-WC-ADVISE` (Recommendation + Clarification + SuggestedFix, DTM-0014/0015) is delivered and merged green to `main` (#46), with DL-047 advisory-only and the Wave C invariants enforced by negatives.
2. **DL-072 Conditions 1 and 2 are DISCHARGED** on `main` (#80): RB-025 unarchive (append-only reversal event + re-derived status + tests) and RB-026 CAF decomposability negative test (drivers individually inspectable; opaque rollup structurally forbidden).
3. **DL-072 Condition 3 (live <60s Time-to-First-MRI, DL-046) is satisfied by recording a GO** from `code/scripts/latency_proof/run_latency_proof.py` against a live internal-Gemma Fast-Pass. **Latency GO result:** `__________` *(owner to attach `latency_proof_result.json` verdict + date; also clears DL-070's latency condition)*.
4. **Phase V / Wave U (User Acceptance & Reconciliation) is AUTHORIZED**, effective on the Condition-3 GO record. On that record, #69 may merge to `main` (subject to its own code-owner approval + green app-ci); no further wave gate is required to *start* Phase V.

## Conditions (carried into Phase V)

1. **Latency GO recorded** — live-Gemma <60s Time-to-First-MRI, `latency_proof_result.json` attached; NO-GO halts and escalates (Anti-Assumption).
2. **Cadence guard** — run each wave exit gate **before** the next wave's PR opens (DL-072 process note); recommend a doc-integrity/CI check.
3. **Advisory-only preserved** — Phase V keeps append-only / no-destruction; no execution (DL-047).
4. **Doc reconciliation** — any stale Phase IV plan "Status" updated to reflect this ratified result.

## Resulting Actions

1. Owner runs the live-Gemma latency proof (latency first, go/no-go) and records the verdict in Decision §3.
2. On GO: Phase V / Wave U (#69) proceeds to merge — code-owner approval + green app-ci against `main`.
3. Phase VI / Wave E (#81) and Release 1 Completion (#82) re-point to `main` and land one-at-a-time behind their own DL-044 exit-gates (DL-065 — one canon PR in flight; do not collapse the stack).
4. Close RB-025 and RB-026 in the revision backlog against this decision.

## Supersedes / Amends

None. Exercises the DL-044 wave-authorization gate and discharges the DL-072 carried conditions (RB-025, RB-026 met; DL-046-latency on GO record). No canonical content superseded.

## Provenance

Owner direction 2026-07-02 to run the Wave C exit-gate review and authorize Phase V. AI drafted and recommended under Framework 001A (analysis / consistency checking / conflict identification / recommendation) — findings grounded in the 2026-07-02 `code/` survey, #46 (Wave C build), and #80 (conditions); the owner ratifies. Numbered at landing under the DL-065 records discipline.
