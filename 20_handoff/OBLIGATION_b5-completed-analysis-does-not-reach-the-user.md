# OBLIGATION — B5: a completed analysis does not reach the user

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit; filed 2026-09-01 on discovering that criterion **N-1** fails with no obligation object behind it
**Invariants violated:** ⚠️ NOT YET DETERMINED — the GT acceptance register lives on the design line. **Escalated, not guessed.** Owner or dev lead to fill the GT ids before this row is accepted. N-1 is a named criterion in the production-gating subset; whether it also binds a GT id is the open question.

## 1 · What was measured

A read that had **finished computing** did not arrive at the surface. The audit recorded the client stalled **≥158 seconds** on an analysis the backend had completed.

`MEASURED-BY:` 2026-08-29 staging fitness audit, recorded in `R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b Tier 3 as criterion **N-1 · a completed analysis reaches the user — ⚠️ FAILS**.

⚠️ **The duration is a floor, not a measurement.** 158s is where observation stopped, not where the stall ended. Nothing has established whether the read eventually arrived, arrived on refresh, or never arrived at all. That distinction changes what the fix is, and it has not been made.

## 2 · Why this gates production

Tier 3 of the subset asks one thing: **can the user complete the core loop.** A product whose central act is "read your plan" fails at its own premise if the read completes and the user never sees it.

It is also the most corrosive failure mode available to this product. Every other defect in the subset shows the user something wrong; this one shows them nothing while the system believes it succeeded. A user cannot distinguish "still thinking" from "finished and lost", so the honest-read doctrine has no surface to be honest on. The system's internal state and the user's evidence disagree, and only the system knows.

## 3 · Current state

**No obligation object existed for this defect until now.** B1, B2 and B3 were filed from the same audit; B5 was not. It has been failing its criterion, in a subset the owner ruled as this sprint's bar, with nothing in the generated queue to carry it.

⚠️ **It is not covered by the shared identity cause.** B1, B2 and B3 trace to findings having no stable identity across re-analyses, fixed in #249. **B5 is a delivery failure, not an identity failure** — the analysis was correct and complete and did not arrive. Nothing in #249's remediation report addresses transport, polling, or terminal-state signalling. Closing B1–B3 will not close this.

⚠️ **Cause unknown.** Whether this is polling, a terminal-state signal never emitted, a socket dropped, a client state machine with no exit, or an upstream timeout has not been established. This obligation does not assert a cause.

## 4 · DONE CONDITION

All five, on the deployed build, each reported with the command or observation that produced it:

1. **The stall is characterized before it is fixed.** Reproduce and record what actually happens after the observed window: does the read arrive late, arrive on refresh, or never arrive. A fix aimed at an uncharacterized stall cannot be shown to have addressed it.
2. **The cause is named, not inferred.** State the mechanism with the evidence that identifies it — a log line, a network trace, a state dump. "Likely polling" is not a cause.
3. **RED proof.** The failure is reproduced on the deployed build with the timing recorded, before the fix.
4. **GREEN proof, with a bound.** After the fix, a completed analysis reaches the surface within a stated ceiling, measured across repeated runs rather than once. The ceiling is named in this row before the measurement, not chosen after it.
5. **The failure path exists.** When delivery does fail, the user sees a stated failure rather than an indefinite wait. This is criterion **N-4**, which the subset records as ⚠️ partial; a fix that makes the happy path fast while leaving the unhappy path silent does not close this row.

## 5 · Out of scope, filed as a pointer

**N-4 · every round-trip has a failure path** is recorded in the subset as partial, on the evidence of a raw `Failed to fetch` reaching the surface (audit finding R8). §4.5 above requires N-4's behaviour for *this* path only. The general criterion has no obligation object of its own and still needs one.
