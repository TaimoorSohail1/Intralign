# DL-072 — Wave B exit-gate pass (with conditions) + Phase IV/Wave C authorization

- **Date:** 2026-06-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** DL-044 (per-wave exit-gate / authorization); DL-068 (Wave B authorization + conditions); the Wave B exit-gate review (RB-024); PR #39 (Wave B, merged to `main`) and PR #46 (Phase IV / Wave C, in review). Owner ratification via the Founder Console, 2026-06-18.
- **Layer:** Delivery governance (DL-044 wave gate). No doctrine/constitution change.

## Decision
1. **Wave B (Understanding) PASSES the DL-044 exit gate — with conditions.** Synthesis (IC-WS-SYNTH), Infer/Finding (IC-WB-INFER), and Evaluate/CAF-Confidence (IC-WB-EVAL) are delivered and merged green to `main` (#39): epistemic invariants enforced by negatives (Derived-never-Attested, one-producer, CHR-append-on-recompute); DL-062 CAF-first-class / Reliability-non-collapse / CONF-06 honored; the Gate-3 cost-accounting defect was fixed before merge (commit `2b0fc56` — token-usage shape-robust + pydantic-ai pinned), restoring DL-048 accounting / DL-069 Condition 2; the DL-059→DL-069 governance retarget landed.
2. **Authorize Phase IV / Wave C (Advise)** to proceed (PR #46), building on Wave B — subject to the binding conditions below and CI fully green.

## Binding conditions (verified gaps — must land in/by Wave C)
1. **Unarchive (DL-058) — NOT built in Wave B.** `code/backend/responsibilities/retain/archival.py` on `main` still declares "an explicit unarchive is OUT of scope in R1." DL-068 Condition 3 folded unarchive into Wave B; it was not delivered. **Build it in Wave C or a dedicated near-term slice** (new reversal event type + path). Tracked as **RB-025**.
2. **DL-062 decomposability negative test — missing.** The evaluate negatives cover Confidence-isn't-health, Reliability non-collapse, CONF-06, and a non-empty `basis`, but **no test asserts CAF drivers stay individually inspectable** ("no opaque rollup"), which DL-062 Condition 1 explicitly requires as a QA negative test. **Add it.** Tracked as **RB-026**.
3. **<60s Time-to-First-MRI (DL-046) — unproven on the live internal-Gemma model.** CI uses recorded fixtures; the G8 latency line (p50 ≤ 25s / p95 ≤ 50s, < 60s ceiling) has not been measured against a live Gemma Fast-Pass. **Run and record it before Phase IV exit** — this also clears the DL-070 (Phase 1 sign-off) latency condition.

## Process note
Wave C (#46) was opened **before** this exit-gate review ran. Going forward, the DL-044 cadence should run the wave exit gate **before** the next wave's PR opens, so authorization precedes build. (Recurring "engineering ahead of the per-wave gate" pattern.)

## Supersedes / Amends
Exercises the DL-044 per-wave gate; consumes DL-068's Wave B authorization. Closes **RB-024** (this review). Opens **RB-025** (unarchive) and **RB-026** (decomposability test). No canonical content superseded.

## Provenance
Founder Console Decide log; ratified by Idris 2026-06-18. Landed under the DL-065 number-at-merge records discipline.
