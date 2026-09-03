# OBLIGATION — B1: the finding set changes across re-analyses of an unedited plan

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit — `20_handoff/audits/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md` *(path corrected 2026-09-02: this row cited `release-2/…`, which exists on no ref. B0 cited the same audit correctly.)*
**Invariants violated:** ⚠️⚠️ **NONE EXIST — RULED 2026-09-02 as a COVERAGE GAP, not a blank to be filled.**

The original blank said the register *"was not reachable when this obligation was written."* That reason expired — `design/release-2.1` is current and reachable — so the field was re-examined and the answer is worse than *unknown*. **Measured:** `R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b binds a GT id to B2 (`GT-67`) and to B3 (`GT-61 · GT-93`) **by name**, and binds **nothing to B1**. No criterion in the twenty-id production-gating subset would catch *the finding set changing across re-analyses of a plan that was never edited.*

⇒ **This is the third instance of the pattern §3 of that document already names:** *"N-1 and N-4 would each have caught a blocking defect this week. Neither has an entry in the GT register. That is the measure of what 'doctrine-only' leaves uncovered."* N-1 and N-4 were minted in response. B1 was not, and has been carried as a production blocker since 2026-08-29 with nothing that would have caught it.

⚠️ **No id is minted here, deliberately.** R2.0-6 already mints four, and RB-109's range of record is unsettled — minting a fifth inside an obligation row would put a criterion into the subset without passing through the act that governs subset membership. **The gap is recorded; closing it is a separate ruling.** Until then this row's acceptance cannot cite an invariant, and that absence is the finding.

## 1 · What was measured

Three consecutive re-analyses of a plan **that was never edited**, on staging:

| run | findings detected |
|---|---|
| 1 | 24 |
| 2 | 23 |
| 3 | 29 |

The application reported **16 opened / 16 resolved against 3 user acts**. Artifact detail counts moved with them — Intent 5 → 12, Requirements 3 → 13.

## 2 · Why this is blocking for production

A read that returns a different set of findings each time it is asked about the same unchanged plan is not a read. It is a re-derivation presented as an observation, and it breaks the product's central claim — that OSLO reports the maturity of your plan rather than forecasting it. A user who re-reads an untouched plan and sees six new problems appear cannot tell whether their plan changed, the model changed, or nothing changed at all. That is the honesty-first doctrine failing at the surface the whole product rests on.

## 3 · Cause and current state

**Shared cause with B2 and B3:** findings had no stable identity across re-analyses. Every confirmation triggered a full re-read that re-derived the set from scratch, and identity was hashed from generated title/explanation wording.

Engineering has fixed the cause in **PR #249** — `fix(analysis): stabilize issue identity by plan element` (`1fad48d`). Identity is now `graph_node_id + finding_type + structural_target`, and the remediation report records nine sub-concerns resolved, four of them fail-closed.

⚠️ **That fix is verified LOCALLY ONLY, by engineering's own account:** *"The browser verification used the production build locally against the local API and seeded database. Staging is not changed by this branch until the PR is merged and deployed."* No count above has been re-measured where it was observed. The fix is also currently trapped behind the `apps/intralign/` location ruling and a red `doc-integrity` gate on #249.

⚠️ **This obligation's own control was never run.** The audit measured three re-analyses *with* user acts. The flip condition — three re-analyses with **zero** acts — has not been executed, so the pure re-derivation rate is still unknown.

## 4 · DONE CONDITION

All four, on the deployed build carrying the fix, each reported with the command or observation that produced it:

1. **The zero-act control runs first.** Three consecutive re-analyses of an unedited plan with no user acts of any kind. This is the control the original audit lacked; run it before the acted-on sequence so the two are separable.
2. **The finding count is stable across all three runs** of the zero-act control — the same set, by identity, not merely the same total.
3. **The acted-on sequence is re-measured** and the 24 → 23 → 29 movement does not reproduce. Opened/resolved counts reconcile to the number of user acts actually performed.
4. **Artifact detail counts hold** across the sequence — Intent and Requirements do not move on an unedited plan.

A count reported without its command does not close this row.

## 5 · Notes

Closing B1 may dissolve or reshape B2 and B3, which share its cause. Re-measure those independently rather than closing them by inheritance — the audit predicted several findings *may* dissolve, and a prediction is not a measurement.
