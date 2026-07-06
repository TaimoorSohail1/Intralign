# DL-PENDING — Wave C (Advise) exit-gate review + Phase V/Wave U authorization

> **DRAFT for owner ratification.** AI-drafted under Framework 001A (analysis / consistency
> checking / conflict identification / recommendation only). The owner ratifies; AI does not.
> Number-at-merge per DL-065: rename to `00_owner/decisions/records/DL-<NNNN>-wave-c-exit-gate-phase-v-authorization.md`
> on a branch via `python3 tools/dl_records.py next`, regenerate the index, PR → green doc-integrity gate → owner merge. **Never push to main.**

- **Date:** 2026-06-29 · **Status:** DRAFT — recommended disposition **Accepted with Conditions** (owner ratifies) · **Decided by:** Idris (Founder Console) — *pending*
- **Class:** A
- **Source:** DL-044 (per-wave exit-gate / authorization); DL-072 (Wave B exit-gate pass + Wave C authorization, with three binding conditions); PR #46 (Phase IV / Wave C, merged to `main`); deep-tasks DTM-0014 / DTM-0015 (EM-approved 2026-06-18); 2026-06-29 code survey of `code/`.
- **Layer:** Delivery governance (DL-044 wave gate). No doctrine / constitution / responsibility change.

---

## Review (Framework 001A — five outputs)

### Findings

1. **Wave C functional scope is delivered and green on `main`.** `IC-WC-ADVISE` is built in `code/backend/responsibilities/advise/` (`engine.py`, `stage.py`):
   - **DTM-0014** — Recommendation + Clarification Request, each anchored to a Finding/Issue; live A→B→C chain.
   - **DTM-0015** — `SuggestedFix` (REC-04/05) + Validation that **never auto-writes** (DL-047 advisory-only).
   - **Invariants enforced by negative tests** (`code/tests/negative/advise/`): anchoring + Resolution-Path-as-substructure / no standalone Resolution-Path object (`test_c3_anchoring_and_resolution_path.py`); no autonomous fix write (`test_c3_no_autonomous_fix_write.py`, DL-047); one-producer boundary (`test_c3_producer_boundary.py`); CHR-append-on-recompute + history (`test_c3_recompute_and_history.py`).
   - **CI:** ruff clean · gate-4 (contract) PASS · gate-5 PASS · live suite **587 passed / 0 failed** · A→B→C e2e green (per DTM-0015, EM-approved 2026-06-18).
   - Maps to the Phase IV "definition of done" (observability + CHR append + two-axis replay; Recommendation-only-in-Finding-context; Clarification on insufficiency; Resolution Path as substructure).

2. **DL-072 Condition 1 — Unarchive (RB-025, DL-058) — NOT MET.** `code/backend/responsibilities/retain/archival.py` (lines 12–13, 104) on `main` still declares *"an explicit unarchive is OUT of scope in R1 — no `unarchived` event type exists in the LDM §2.5 vocabulary."* DL-068 Condition 3 folded unarchive into Wave B; DL-072 Condition 1 required it to land in/by Wave C. It has not been built.

3. **DL-072 Condition 2 — CAF driver-decomposability negative test (RB-026, DL-062 Cond 1) — NOT MET.** The evaluate negatives (`code/tests/negative/evaluate/`) cover confidence semantics / Reliability-non-collapse, cost & performance, producer boundary, and recompute/invariants — but **no test asserts CAF drivers stay individually inspectable ("no opaque rollup")**, which DL-062 Condition 1 requires as a QA negative. Absent.

4. **DL-072 Condition 3 — live <60s Time-to-First-MRI (DL-046) — NOT MET.** Only a *scaffolded, fixture-based* ceiling test exists (`code/tests/positive/evaluate/test_b2_performance_gate.py`); its own docstring records the envelope value and p50/p95 distribution as owner-TBD. No measurement against a **live internal-Gemma Fast-Pass** has been run or recorded. This condition also gates the open **DL-070** Phase 1 ("Prove Understanding") latency sign-off.

5. **Process / drift.** (a) Wave C PR (#46) opened **before** the Wave B exit gate ran — the recurring "engineering ahead of the per-wave gate" pattern already flagged in the DL-072 process note. (b) Doc drift: `30_engineering/implementation/Phase_IV_Wave_C_Advisory/IMPLEMENTATION_PLAN.md` still reads **"Status: Not started"** despite the merged, candidate-complete build.

### Concerns

1. **Latency is the load-bearing unknown.** It is the only open condition that could surface a *real architecture/performance* problem (live Gemma vs the <60s ceiling), it has been deferred across two gates, and it blocks both this gate and DL-070. Treat it as a go/no-go, run it **first**.
2. **Acceptance ≠ a clean pass.** Two of three DL-072 conditions were explicitly mandated to land *by Wave C*; both are open. Recording a clean "Pass" would mis-state the gate and let governance debt compound into Phase V.
3. **Advisory-only must stay provable.** DL-047 is enforced today (`test_c3_no_autonomous_fix_write.py`); the unarchive build (RB-025) and any Phase V work must preserve append-only / no-destruction and never cross into execution.
4. **Pattern risk.** Building the next wave before the prior gate ratifies erodes the DL-044 cadence; without a cadence guard it will recur at the Wave U gate.

### Dependencies

- **DL-044** (wave-authorization / exit-gate cadence) · **DL-072** (the three carried conditions) · **DL-068 Cond 3** (unarchive origin).
- **DL-058** (archive reversible in R1; UP-3) → RB-025. · **DL-062 Cond 1** (CAF decomposability) → RB-026. · **DL-046** (Fast/Deep + <60s) and **DL-070** (Phase 1 sign-off) → the live latency proof.
- **DL-047 / Positioning §9** (advisory-only) — invariant for unarchive and all downstream waves.
- **Downstream:** Phase V / Wave U (User Acceptance) is blocked on this gate; Phase VI / Wave E (Disclose surfaces) follows Wave U.

### Recommendation

**Accepted with Conditions.** Accept the Wave C (Advise) **functional build** as candidate-complete and green on `main`, and **withhold Phase V / Wave U authorization** until the three carried DL-072 conditions land green on `main`:

1. **RB-025 — Unarchive (DL-058):** add the `unarchived` reversal event type to the LDM §2.5 vocabulary + the derive-status path, append-only (no destruction), with positive and negative tests.
2. **RB-026 — CAF decomposability negative test (DL-062 Cond 1):** assert drivers stay individually inspectable; reject an opaque rollup. Land green.
3. **Live <60s Time-to-First-MRI (DL-046):** measure against a live internal-Gemma Fast-Pass, record p50/p95 vs the ceiling; this also clears the DL-070 latency condition.

Plus two non-blocking housekeeping items: reconcile the Phase IV plan status (drift), and adopt a **gate-before-next-wave-PR** guard so the DL-044 cadence holds at Wave U.

*Alternatives for the owner:* a clean **Accepted** is not available (conditions unmet); **Returned for Revision** is the stricter option if the owner prefers to record no acceptance until all three conditions land.

### Status

**DRAFT — recommended: Accepted with Conditions.** Owner ratification required (Framework 001A — AI may not ratify). Phase V/Wave U authorization is **conditional and not yet effective**.

---

## Decision (recommended wording — owner to ratify)

1. **Wave C (Advise) PASSES the DL-044 exit gate — with conditions.** `IC-WC-ADVISE` (Recommendation + Clarification + SuggestedFix, DTM-0014/0015) is delivered and merged green to `main` (#46), with DL-047 advisory-only and the Wave C invariants enforced by negatives; CI green (gate-4/5, 587/0 live, A→B→C e2e).
2. **Phase V / Wave U (User Acceptance) authorization is WITHHELD** until the three carried DL-072 conditions (RB-025 unarchive, RB-026 decomposability test, live <60s Time-to-First-MRI) land green on `main`. On their landing, Phase V is authorized without a further gate.

## Conditions (blocking for Phase V start)

1. **RB-025 Unarchive built** — reversal event type + derive path, append-only, pos/neg tests on `main`.
2. **RB-026 CAF decomposability negative test** — added and green.
3. **Live-Gemma <60s Time-to-First-MRI** — measured, recorded; clears DL-070 latency condition.
4. **Cadence guard** — run each wave exit gate **before** the next wave's PR opens (DL-072 process note); recommend a doc-integrity/CI check.
5. **Doc reconciliation** — Phase IV plan "Status" updated to reflect the ratified gate result.

## Resulting Actions

1. Owner ratifies this review via the Founder Console; number-at-merge per DL-065 (DL-PENDING → DL-NNNN on a branch; regenerate the records index; PR → green doc-integrity gate → owner merge).
2. Engineering opens a near-term slice for RB-025 + RB-026 and runs the live-Gemma latency measurement (latency first, as a go/no-go).
3. On all three landing green, Phase V / Wave U deep-task plan opens from fresh `main` under DL-044.
4. Update the Phase IV `IMPLEMENTATION_PLAN.md` status; record the cadence guard.

## Supersedes / Amends

None. Exercises the DL-044 wave-authorization gate and discharges the DL-072 carried conditions. No canonical content superseded.

## Provenance

Owner direction 2026-06-29 to draft the Wave C exit-gate review. AI drafted and recommended (Framework 001A — analysis / consistency / conflict identification / recommendation); the owner ratifies. Findings grounded in the 2026-06-29 `code/` survey and DTM-0014/0015. To be numbered at landing under the DL-065 records discipline.
