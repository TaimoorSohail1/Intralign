# Deep-task plan — Wave C exit-gate conditions (DL-072 carry-overs)

**Status:** DRAFT (planning only) · **Gated on:** owner ratification of the Wave C exit-gate review
(`00_owner/decisions/WAVE_C_EXIT_GATE_REVIEW_DRAFT.md`, recommended *Accepted with Conditions*) +
DL-044 cadence. **Coding does not begin until the owner ratifies.**

Discharges the three binding conditions carried from **DL-072** so Phase V / Wave U can be
authorized. One fresh worker per slice; EM review → fix → verify → approve between slices; each
branches from fresh `main`; one canon/PR in flight at a time. **Latency is Slice 0 and is a
GO / NO-GO** — nothing else builds until it passes.

## Sequence (risk-first)

| # | Slice | Condition | Effort | Gate behaviour |
|---|---|---|---|---|
| **0** | **Live-Gemma <60s Time-to-First-MRI proof** | DL-072 C3 · DL-046 · DL-070 | S (measure, no build) | **GO / NO-GO.** Fail → STOP + escalate; do not build Slices 1–2 on a failing latency floor. |
| 1 | CAF driver-decomposability negative test | DL-072 C2 · RB-026 · DL-062 C1 | S (test-only) | Standard EM review. |
| 2 | Unarchive (reversal event type + derive path) | DL-072 C1 · RB-025 · DL-058 | M (build + tests) | Standard EM review; owner nod on the LDM vocab edit (see escalation E1). |

On all three green → reconcile the Phase IV plan status + record the cadence guard → return to the
owner for Wave C exit ratification → **Phase V / Wave U authorized.**

---

## Slice 0 — Live-Gemma latency proof  *(GO / NO-GO)*

**Why first.** It is the only open condition that can surface a real architecture/performance
problem; it has been deferred across two gates; and it also clears the **DL-070** Phase 1
("Prove Understanding") latency sign-off. Build nothing else until it passes.

**Outcome.** A recorded measurement of Time-to-First-MRI against a **live internal-Gemma
Fast-Pass** (not recorded fixtures), on the owner-confirmed envelope, evaluated against the
**ratified <60s ceiling**.

**Envelope (owner-confirmed, OPEN_TBD A1).** Tier-1 / Free: **~20 artifacts · ~50k words · 1
active run**. This is where the <60s gate is guaranteed; larger projects degrade gracefully, not
rejected — so they are out of scope for this pass/fail.

**Method.**
- Promote the scaffolded gate `code/tests/positive/evaluate/test_b2_performance_gate.py` from a
  fixture-ceiling check to an **env-gated live-model run** (Supabase up, live Gemma at the seam,
  no recorded fixtures), reusing the `time_to_first_mri_ms` already on the `ai_spend_recorded`
  event (`test_b2_ai_spend_recorded_carries_time_to_first_mri_latency`).
- Run N≥30 Fast-Pass executions at the envelope ceiling; record **p50 / p95 / max** and the full
  distribution; attach the run log + Grafana/Tempo trace IDs.

**Pass / fail.**
- **Ratified gate (hard):** every run's Time-to-First-MRI **< 60s** (Master Spec §20/M1). Any
  breach at/under the Tier-1 envelope = **NO-GO**.
- **Reported, not gating:** p50 / p95 against the *proposed* DL-046 targets (p50 ≤ 25s /
  p95 ≤ 50s). These are **owner-TBD (OPEN_TBD A2)** — record them, do **not** auto-pass/fail on
  them. See escalation E2.

**On NO-GO.** Stop the slice. File an engineering finding (where the budget is spent — retrieval /
synthesis / Gemma inference), recommend remediation, and escalate to the owner before any further
Wave C/Phase V work. Do not "fix by assumption."

**Done.** Live measurement recorded + attached to the exit-gate review; <60s holds across the run
at the Tier-1 envelope; DL-070 latency condition cross-referenced as cleared.

---

## Slice 1 — CAF driver-decomposability negative test  *(RB-026 / DL-062 C1)*

**Outcome.** A QA **negative** test proving the confidence basis keeps CAF drivers **individually
inspectable** — an opaque rollup is rejected. Closes the one DL-062 Condition 1 gap (the evaluate
negatives today cover Reliability-non-collapse, cost/perf, producer-boundary, recompute/invariants,
but not driver decomposability).

**Spec anchor (DL-062 C1, verbatim intent).** "Drivers folded into a CAF dimension (esp.
assumption stability, interpretation stability) and the Reliability sub-axes MUST remain
individually inspectable in the confidence basis/explanation; an opaque Clarity rollup is
non-conformant (QA negative test required)." Doctrine 06: uncertainty must remain structurally
inspectable.

**Scope.** Add `code/tests/negative/evaluate/test_b3_caf_decomposability.py`:
- **Negative:** a Confidence whose basis exposes only a single rolled-up Clarity scalar (no
  per-driver / per-sub-axis breakdown) is **rejected** as non-conformant.
- **Positive companion (if not already covered):** a conformant Confidence exposes each CAF
  contributor + Reliability sub-axis in `basis`/explanation, individually addressable.
- No production change expected (evaluate already emits decomposed CAF); if a gap is found, that is
  itself a finding → escalate, do not silently widen scope.

**Done.** Test green in CI (offline + live); ruff + gate-4 + gate-5 green; no baseline regression.

---

## Slice 2 — Unarchive  *(RB-025 / DL-058)*

**Outcome.** Archive becomes **reversible in R1** (DL-058; UP-3 affirmed), append-only, destroying
nothing — discharging the DL-068 Cond 3 / DL-072 Cond 1 gap. `archival.py` today states unarchive
is out of scope because no `unarchived` event type exists in the LDM §2.5 vocabulary; this slice
adds it.

**Build.**
- **LDM §2.5 vocab:** add `unarchived` to the `History Record.event_type` enum
  (`30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` §2.5). **See escalation E1.**
- **Derive path:** extend the derived-status read (`is_archived`) so the **latest** of
  `archived` / `unarchived` wins — symmetric with the existing archived-derivation; no status
  column, no schema mutation, no row deletion (mirrors the archival append-only pattern).
- **Responsibility:** add `unarchive_assertion(...)` to
  `code/backend/responsibilities/retain/archival.py` — appends ONE `history_record`
  (`event_type='unarchived'`) + emits the reversal event(s) (e.g. `knowledge_unarchived` +
  `knowledge_mutation_recorded`); the `attested_assertion` row stays intact and in the version
  chain. Remove the "out of scope" docstring.

**Tests.**
- **Positive:** archive → unarchive → `is_archived` false; both history entries present and
  ordered; prior versions byte-intact; a re-archive after unarchive flips status back (latest
  wins). Emission appends a CHR; recompute appends, never overwrites.
- **Negative:** unarchive destroys/mutates no row (append-only invariant); unarchive of a
  non-existent assertion raises `AssertionNotFoundError`; status is never read from a column
  (derived-only). Preserve advisory-only / no-execution boundary (DL-047).

**Done.** Positive + negative green (offline + live); ruff + gate-4 + gate-5 green; observability
events + two-axis replay present for the reversal; no baseline regression.

---

## Test strategy (all slices)

- Recorded-fixture CI for AI text (ADR-0004) — **except Slice 0**, which is an explicit
  **env-gated live-Gemma** run (that is the point of the proof).
- ruff + gate-4 (contract) + gate-5 + the live A→B→C e2e green; the current Wave C baseline
  (live 587 / 0) must not regress.
- Determinism per the existing tiers; emission record-exact; recompute ≥90% set overlap.

## Manual checks (EM / owner)

- **Slice 0:** EM watches one live Fast-Pass at the envelope; confirms the Grafana/Tempo trace and
  the recorded p50/p95/max; owner reviews the distribution against §20 / DL-046.
- **Slice 2:** live — admit → archive → unarchive → status flips back, both history rows persist,
  prior CHRs byte-intact; grep/AST — retain exposes no destroy/execute surface.

## Escalations  *(Anti-Assumption Build Protocol — do not infer; escalate)*

- **E1 — LDM §2.5 vocab edit authority.** Adding `unarchived` to the contracted event_type enum
  touches a runtime model. DL-058 ratifies the *intent* (unarchive in R1); engineering authors the
  *realization*. **Confirm with the owner** whether the enum edit lands as engineering authorship
  or needs an explicit nod before merge — do not assume.
- **E2 — p50/p95 thresholds (OPEN_TBD A2).** Proposed (p50 ≤ 25s / p95 ≤ 50s), owner-to-confirm.
  Slice 0 reports them; the **only** ratified pass/fail is the <60s ceiling. Owner sets the
  distribution pass/fail if/when desired.
- **E3 — Paid-tier latency envelope (OPEN_TBD A1).** TBD. This slice proves only the Tier-1 (Free)
  envelope; paid-tier latency proofs are out of scope until the owner parameterizes them.

## Done = conditions discharged

Slice 0 GO recorded (<60s live, Tier-1 envelope) · RB-026 decomposability negative green ·
RB-025 unarchive built + tested green · Phase IV plan status reconciled · cadence guard recorded.
→ Return to owner for **Wave C exit ratification → Phase V / Wave U authorization.**
