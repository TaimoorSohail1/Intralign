# OBLIGATION — B1: the finding set changes across re-analyses of an unedited plan

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit — `release-2/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md`
**Invariants violated:** ⚠️ NOT YET DETERMINED — the GT acceptance register lives on the design line and was not reachable when this obligation was written. **Escalated, not guessed.** Owner or dev lead to fill the GT ids before this row is accepted.

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
