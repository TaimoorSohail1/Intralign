# DTM-0005 — Recompute & stale backbone (the 00R spine)

**Status:** Not started · **Module:** DTM-0005 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R** · **Depends:** DTM-0004

## Goal / observable behavior

A valid trigger (promotion · knowledge-changing modification · clarification answered ·
information-changing user action · explicit/auto reanalysis) moves a project's cognition
state `Current → Stale → Reanalyzing → Current'`, re-runs the registered chain
`Retain → Infer → Evaluate → Advise` as a **durable LangGraph run**, replaces the live
Derived projection, and appends one CHR per emission via DTM-0004. On chain failure:
state → `Failed`, **last-known-good live projection retained**, history uncorrupted.

## Source docs / constraints

- The whole of `WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` — IC A3 (required), **A4 (forbidden — enforce in tests)**, A7 states, A10 invariants; QA B2/B3/B4.
- DL-046: 00R is the **Deep Pass** engine — async, coalesced, must not block Fast Pass.
- ADR-0002: ALL graph wiring in `backend/orchestration/` (registry/runner/checkpointer); domain logic in responsibilities. A node is thin.
- Trigger detection belongs to Perceive; orchestration coordination to Act/Adapt (contract A1).

## Locked decisions

- Chain stages are **injected via a stage registry**: Phase II-A registers explicit no-op placeholders for Infer/Evaluate/Advise (each returns input unchanged, marked `WAVE_B_PLACEHOLDER`/`WAVE_C_PLACEHOLDER`). Backbone produces no cognition itself (A4.3).
- State machine + trigger types in `responsibilities/adapt/` (recompute discipline) + stale detection in `responsibilities/perceive/`; graph topology `orchestration/graphs/deep_pass.py`; durable checkpointer wired (Supabase Postgres) per `orchestration/checkpointer.py` stub.
- Coalescing: triggers arriving while `Reanalyzing` mark the run stale-again; one queued follow-up max (no unbounded queue) — exact semantics from contract A3/§0 (coalesced).
- States as enum: `analyzing | current | stale | reanalyzing | failed` (contract A3.6).
- Events emitted to an internal dispatcher seam only (transport TBD — open NFR); full observability contract is DTM-0006.

## Owned files

- `backend/orchestration/**` (implement stubs: checkpointer, runner, registry, state, graphs/deep_pass.py), `backend/responsibilities/{adapt,perceive}/**`, `tests/{positive,negative}/{orchestration,adapt,perceive}/**`.
- Read-only: `retain/` (consume DTM-0004 repo as-is), migrations, api/.

## Packages / refactors

- `langgraph-checkpoint-postgres` approved if the pinned langgraph version needs it (stop-and-ask otherwise). No refactors.

## Implementation instructions (TDD)

1. Red first against QA-WA-00R: B2.1–B2.5 positives; B3.1–B3.5 negatives (assessment-without-recompute impossible; CHR overwrite rejected; intake alone changes nothing; backbone emits no cognition of its own; no Derived→Attested write path).
2. Green: state machine → trigger validation → graph topology → durable run via checkpointer → last-known-good handling.
3. Replace each `NotImplementedError` stub in `orchestration/` — do not change its public seam without EM approval.

## Test plan

- Positive: each valid trigger → full transition cycle; CHR appended per emission; resume-after-interrupt (kill mid-run, resume from checkpoint); coalescing under burst triggers.
- Negative: B3 set, invalid trigger rejected, failure path retains last-known-good and appends nothing partial.
- Failure classification awareness: any Critical-class behavior (B4) = test must exist proving impossibility.

## Done criteria

- All QA-WA-00R B2+B3 mapped to named tests (traceability list in worker report); durable resume demonstrated; PR cites `IC-WA-00R`; gates green.

## Worker report

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_
