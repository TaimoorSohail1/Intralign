# DL-068 — Wave A sign-off + Wave B authorization

- **Date:** 2026-06-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** `code/docs/deep-tasks/r1-foundation-deep-task/DEVELOPMENT_COMPLETION_REPORT.md` (§8 owner-approval block); DL-044 (wave-authorization gate); Founder Console owner-action `oaq-wavea-signoff`; the 2026-06-17 code survey of `code/`.

## Decision
1. **Accept Phase I (Foundation) + Phase II Wave A as complete** and **sign §8** of the completion report. Evidence: DB-enforced append-only canonical store + CHR lineage; the IC-WA-00R recompute/stale backbone (durable runs, Postgres checkpointer, 5-state machine, coalescing); Perceive (IC-WA-001) and Retain (IC-WA-002); observability + two-axis replay; six-gate CI; ~260 tests incl. invariant-enforcing negatives.
2. **Authorize Wave B** (Understanding) to begin, per DL-044.

## Conditions
1. **psycopg[binary] declared — MET.** Landed on `main` via PR #37 (merge `9d0849d`); the durable PostgresSaver now boots reproducibly on a clean machine/CI. §8 checkbox psycopg = Approve.
2. **ADR-0001 = Ratified (DL-057)** — the monorepo-placement §8 checkbox is satisfied; no action needed.
3. **Unarchive (DL-058) folded into Wave B** — a known, owner-accepted plan-vs-build gap; not a Wave-A blocker.
4. **CI green on `main` — MET.** PR #37 also cleared the Gate 6 advisory (form-data GHSA-hmw2-7cc7-3qxx) via a `form-data ^4.0.6` override; `app-ci` is green on `main`.
5. **Owner-pending TBDs** (e.g., audit-receipt retention, OPEN_TBD C1; paid-tier values) are tracked, not blockers for Wave-A acceptance.

## Wave B scope authorized (per DL-044 / DL-046 / DL-047)
Build order 3-slice, reviewed before the next (mirrors Wave A): Synthesis (IC-WS-SYNTH, with/before) → Infer (IC-WB-INFER) → Evaluate (IC-WB-EVAL). Fold in: the C-2 decomposability negative test (DL-062 — confidence drivers must stay inspectable, no opaque Clarity rollup); unarchive-in-R1 (DL-058); the CAF first-class / Reliability-qualifies model (DL-062); Fast Pass + Deep Pass + <60s Time-to-First-MRI (DL-046). Owner gate required before Phase IV (DL-044). No autonomous production deploy (human-only).

## Supersedes / Amends
None. Exercises the DL-044 wave-authorization gate; closes the `oaq-wavea-signoff` owner action.

## Resulting Actions
1. Owner signs §8 of the completion report (canonical edit — lands alongside / after this record).
2. psycopg[binary] PR — done (PR #37, merge `9d0849d`).
3. Engineering opens the Wave B deep-task plan (Synthesis → Infer → Evaluate) under DL-044; first slice branches from fresh `main`.
4. `oaq-wavea-signoff` clears from the Decide lane on the next monitor run (reconciled as signed).

## Provenance
Founder Console Decide log; owner-action `oaq-wavea-signoff`. Landed via the dl-land workflow (DL-067) under the DL-065 number-at-merge discipline.
