# DL-070 — Ratify the Phase 1 "Prove Understanding" falsifiable exit gate (P-4 / DL-059 realization)

- **Date:** 2026-06-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** DL-059 (the P-4 directive: Phase 1 "Prove Understanding" must have a falsifiable, owner-authored pass/fail gate); the drafted gate harness `00_owner/build_governance/PHASE_1_PROVE_UNDERSTANDING_EXIT_GATE_V1.md`; owner ratification via the Founder Console, 2026-06-18.
- **Layer:** Implementation Spec / Delivery governance (Phase 1 sign-off gate), in `00_owner/build_governance/` — owner-ratified build policy that binds engineering. No doctrine/constitution change.

## Decision
Ratify the **Phase 1 "Prove Understanding" Falsifiable Exit Gate (V1)** as canon, fixing the four owner-only values that previously left the criterion unfalsifiable (DL-059's P-4 gap):
1. **Corpus pass rate (G7 + §1 aggregate): > 90%** (Master Spec §20 baseline). Structural conditions G1–G6 and G9 remain at 100%.
2. **Evaluation corpus size: N ≥ 20** in-envelope, version-pinned projects spanning the three R1 intake modes (Upload / Describe / Template, DL-056).
3. **Time-to-First-MRI (G8): p50 ≤ 25s / p95 ≤ 50s** under the ratified **< 60s** ceiling, at the **Tier-1 envelope** (DL-046 register A2 + A1).
4. **Determinism (D1): deferred to the Phase 2 "Prove Improvement" gate** (tolerance band remains owner-open; not part of Phase 1).

The single pass/fail line: Phase 1 PASSES iff a Fast Pass satisfies every Required Condition for > 90% of the pinned corpus with zero FAIL-Trigger occurrences; no partial sign-off.

## Conditions / Resulting actions
1. The gate file flips to **Ratified (DL-070)**; this record + CHG-100 are the traceability.
2. **Kashif (mkashifse)** (a) **validates G8 latency against a live internal-Gemma Fast-Pass run** (local-inference latency is unproven against p95 ≤ 50s per DL-069), then (b) **pins the revised Phase 1 sign-off date** to this gate. If local inference cannot meet p95 ≤ 50s, that is a fast-follow amendment to value #3 — not a pre-emptive relaxation.
3. Engineering authors the realizing evaluation harness (metrics + pinned corpus fixtures) against this gate; the gate text is canon, the harness is engineering realization.

## Supersedes / Amends
Resolves the DL-059 Condition-1 deliverable (the gate text itself). The prior "DL-060" proposal/ratification-stub drafts are **void** (retired by DL-066) and are not part of canon. Supersedes nothing else.

## Provenance
Founder Console Decide log; ratified by Idris 2026-06-18. Realizes DL-059. Landed under the DL-065 number-at-merge records discipline.
