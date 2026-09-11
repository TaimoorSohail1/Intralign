# OBLIGATION — B2: a settled finding regressed to open at rank #1, and an open finding vanished

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit — `20_handoff/audits/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md` *(path corrected 2026-09-02: this row cited `release-2/…`, which exists on no ref. B0 cited the same audit correctly.)*
**Invariants violated:** ▶ **RULED 2026-09-02 — `GT-67`** *(settled never regresses on landing)*. Not derived here: `R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b already binds it to this defect by name — *"GT-67 settled never regresses on landing · **B2 — attested work returned as the top task** · ⚠️ FAILS"*. The blank was filled from the record, not from judgement.
*(The field previously read "NOT YET DETERMINED — the GT acceptance register lives on the design line and was not reachable when this obligation was written." That reason expired: `design/release-2.1` is current and reachable.)*

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

**Lifecycle vocabulary for this proof:** `settled` means `addressed` or `resolved`. `routed` is recorded separately and is not settled. `withdraw` is a user act that returns an issue to `open` through re-analysis; it is not a terminal lifecycle state.

1. **Settle a finding, then re-analyse three times.** It stays settled across all three, and does not re-enter the open list under any wording.
2. **No finding leaves the open set without a recorded state transition.** Every departure from the open set enters `addressed`, `routed` or `resolved`, and the transition is visible in History. If a finding vanishes silently, this row does not close regardless of item 1 — that is the unexplained half.
3. **The reworded case specifically:** a finding whose wording changes between runs keeps its identity and its attestation join. Demonstrated, not asserted from unit tests.
4. **The historical orphan repair is scoped** — the affected projects and keys identified, the repair run or explicitly ruled unnecessary with the count that supports it.

   ▶ **RULED 2026-09-02 — owner, date and ticket.** §5 recorded that this repair *"currently has no owner, no date and no ticket"*; that is now closed.
   - **Owner: TaimoorSohail1.** R2.0-5 assigns product/engine defects to him, and he authored the change that stops NEW orphans being created. The repair of the ones already there belongs with it.
   - **Date: after the B-series deployment, not before.** ⚠️ **Repairing before the fix ships re-orphans on the next run** — the change explicitly does not delete already-orphaned attestations, so a repair run against an un-fixed build produces new ones. The dependency is the date; a fixed calendar date that the deploy can miss would be a commitment the apparatus could not keep.
   - **Ticket: this item.** Per R2.0-1 every open subset criterion gets a durable object, and this obligation is B2's. The repair is not split into its own row because it cannot close independently of items 1–3: all four are evidenced on the same deployed build, in the same session.

   ⚠️ **This item can fail on its own.** If the affected keys are identified and the repair is neither run nor ruled unnecessary *with a supporting count*, item 4 is unmet and **B2 does not close**, however items 1–3 read.

## 5 · Notes

Items 1 and 3 are expected to follow from the identity fix. **Item 2 is the one to watch** — nothing in engineering's account explains the silent disappearance, and a done condition that only tests the explained half is how a defect survives its own fix.
