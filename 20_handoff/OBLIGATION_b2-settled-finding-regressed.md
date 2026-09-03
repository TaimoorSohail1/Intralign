# OBLIGATION — B2: a settled finding regressed to open at rank #1, and an open finding vanished

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit — `release-2/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md`
**Invariants violated:** ⚠️ NOT YET DETERMINED — the GT acceptance register lives on the design line and was not reachable when this obligation was written. **Escalated, not guessed.** Owner or dev lead to fill the GT ids before this row is accepted.

## 1 · What was measured

On staging, across re-analyses of an unedited plan:

- A finding the user had **settled** returned to **open, at rank #1**, reworded:
  *"No venue dependency is secured…"* → *"Venue dependency is unsecured and unbounded"*
- It returned with **no withdraw** and no visible transition. It simply reappeared as new.
- Separately, an **open finding vanished silently** — no resolution, no withdraw, no trace.
- Both survived a page reload, so this is **server state**, not a rendering artifact.

## 2 · Why this is blocking for production

This is the most direct honesty failure in the R2.0 surface. A user who does the work to settle a finding, and then sees it back at the top of their list under different wording, learns that settling means nothing. A finding that disappears without a withdraw teaches the same lesson from the other direction — that the list is not a record.

It also breaks two ratified doctrines at once: **only-reanalysis-resolves** (a finding must not change state by any other path) and **order-actions-never-truth** (ranking may order what the user does next; it may not restate what is true). A settled item re-entering at rank #1 does both.

## 3 · Cause and current state

**Shared cause with B1 and B3:** identity was hashed from generated wording, so a reworded finding minted a new key and the saved attestation no longer joined to it. The engineering remediation report names this concern directly — *"User confirmation disappears: changed issue key no longer joined to the saved attestation"* — and reports it resolved by the stable semantic key.

Fixed in **PR #249**, commits `1fad48d`, `94dafb1` — `preserve deterministic issue attestations`.

⚠️ **Verified locally only.** No part of the sequence above has been re-run on staging.

⚠️ **The report explicitly excludes historical repair:** *"Already-orphaned attestations from older staging runs are not deleted by this change. If one was orphaned before deployment, it needs a one-time data repair."* That repair currently has no owner, no date and no ticket. It is in scope for this obligation.

⚠️ The **vanishing** finding is not obviously covered by the identity fix. The remediation table addresses reworded findings, artifact movement, duplicate keys and unknown anchors — it does not describe a finding leaving the set without a transition. Treat that as **unexplained until measured**, not as fixed by inheritance.

## 4 · DONE CONDITION

On the deployed build carrying the fix, each result reported with the command or observation that produced it:

1. **Settle a finding, then re-analyse three times.** It stays settled across all three, and does not re-enter the open list under any wording.
2. **No finding leaves the set without a transition.** Every disappearance is a resolve or a withdraw, visible in History. If a finding vanishes silently, this row does not close regardless of item 1 — that is the unexplained half.
3. **The reworded case specifically:** a finding whose wording changes between runs keeps its identity and its attestation join. Demonstrated, not asserted from unit tests.
4. **The historical orphan repair is scoped** — the affected projects and keys identified, the repair run or explicitly ruled unnecessary with the count that supports it.

## 5 · Notes

Items 1 and 3 are expected to follow from the identity fix. **Item 2 is the one to watch** — nothing in engineering's account explains the silent disappearance, and a done condition that only tests the explained half is how a defect survives its own fix.
