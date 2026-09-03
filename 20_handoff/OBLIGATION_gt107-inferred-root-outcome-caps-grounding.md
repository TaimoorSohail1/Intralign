# OBLIGATION — GT-107: an inferred root outcome caps Grounding — untested

**Status:** OPEN
**Fix:** HamzaSohailCodes *(assigned by owner 2026-09-02 — checks & infrastructure lane)*
**Accepts:** idris-manley
**Class:** R2.0 production blocker · production-gating subset, Tier 1 (honesty of the read)
**Raised:** `20_handoff/R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md` §4b — state: **untested**
**Criterion:** **GT-107** — *an inferred root outcome caps Grounding*. Subset state: **untested.**
**Invariants:** registered. ⚠️ **Twin state unknown** — inside `GT-58…GT-118`, the 61 with no server twin.

## 1 · What was measured

**Nothing.** GT-107 is the only Tier 1 criterion in the production-gating subset with no verdict — every
other row in that tier is either passing or attached to a named defect.

**CONTROL:** the same table records GT-10, GT-26, GT-33 and GT-20 as passing and GT-67, GT-61·GT-93 as
failing, so the blank against GT-107 is an unexercised check rather than an unreported one.

## 2 · Why this is blocking for production

**Tier 1 is "a user acts on something false."** GT-107 is the cap that stops the product reporting strong
Grounding on a plan whose *root outcome* is still OSLO's inference rather than the user's evidence.

Without it, the failure is silent and it is the worst-shaped failure this product can have: a user reads a
healthy Grounding number, believes their plan is evidenced, and acts on it — while the thing everything
else hangs from was never confirmed by anyone. **Only verify moves Grounding** is the doctrine; a cap that
is never exercised is a doctrine with no demonstrated mechanism.

⚠️ It is adjacent to **B3**, where Grounding's numerator fell to 0 after two attestations. **Adjacent, not
identical** — B3 is about the counter moving wrongly, GT-107 is about a ceiling that should hold. Do not
let one close the other.

## 3 · Cause and current state

Not applicable — never exercised. **Do not assume it passes** because the surrounding Tier 1 criteria do;
the neighbouring rows test different mechanisms.

⚠️ Inside `GT-58…GT-118`, so no server twin exists and no regression would be caught even if a manual run
passes today.

## 4 · DONE CONDITION

On the deployed build, each result reported with the command or observation that produced it:

1. **The cap is observed holding.** A plan whose root outcome is inferred cannot report Grounding above
   the cap, whatever else is grounded — measured by grounding every non-root item and reading the number.
2. **The cap is observed lifting.** Verify the root outcome and show Grounding is then free to rise.
   ⚠️ **Both directions, or the check cannot fail** — a cap that never lifts and a number that never rose
   are indistinguishable from a broken read.
3. **The cap is disclosed to the user**, not merely applied. A ceiling the user cannot see reads as the
   product simply scoring them low.
4. **A pinned-negative twin exists** that goes red when the cap is removed, per §4.1.
5. **A build identity is cited** alongside the result (see the N-5 obligation).

## 5 · Notes

★ **Cheap to run and it is Tier 1** — the highest-stakes tier in the subset, and the only unmeasured row in
it. Sequence it with GT-106·GT-110; both are execution rather than fixes, and both can be done before B0's
deployment lands.

⚠️ **If it fails, it is a same-day escalation.** A Tier 1 honesty cap that does not hold is not a backlog
item — it is the class of defect the production-gating subset exists to catch.
