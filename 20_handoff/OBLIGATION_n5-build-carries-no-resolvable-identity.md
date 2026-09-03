# OBLIGATION — N-5: a build carries no resolvable identity, so no R2.0 measurement can be attributed to what was measured

**Status:** OPEN
**Fix:** HamzaSohailCodes
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-09-01, filed on discovering that the subset criterion whose state reads *"nothing exists"* has no obligation object
**Invariants violated:** ⚠️ NOT YET DETERMINED. N-5 is a named criterion in the production-gating subset; whether an invariant also binds build identity is unread — the acceptance register lives on the design line. **Escalated, not guessed.**

## 1 · What was measured

`R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b Tier 4:

> **N-5** a build carries a resolvable identity — **nothing exists**

`MEASURED-BY:` the criteria document's own state column.

Two supporting observations were recorded on 2026-08-31 and **have not been re-measured for this row**:

- `app.intralign.ai` — the deployed surface — appears in **zero files** in this repository.
- `vercel.json` hardcodes a single Heroku origin.

⚠️ Both are carried here as **recorded, not re-verified**. Step 1 of the done condition re-measures them rather than inheriting them, because a row that reasons from a remembered measurement is the failure mode this apparatus exists to end.

## 2 · Why this is the precondition, not one criterion among eighteen

Every other row in the R2.0 set closes on measurement **against the deployed build**. B0, B1, B2, B3, B5 and the entitlement row each say so explicitly, and the criteria document requires every WALK criterion to be executed against *that* build, each result citing `MEASURED-BY:`.

**A measurement that cannot name what it measured is not evidence.** With no resolvable identity:

- "eight pass, six fail, four untested" is a statement about an unnamed artifact;
- a re-measurement after a fix cannot be shown to have run against a different build than the one before it;
- a regression cannot be bisected, because there is nothing to bisect between;
- and the difference between *"fixed"* and *"measured somewhere else"* is not decidable by anyone, including the person who ran it.

This is already live rather than hypothetical. The R2.0 identity fix is recorded as verified *"locally against the local API and seeded database"*, with staging explicitly unchanged. That statement is honest precisely because someone wrote down which surface they used. Nothing in the system made them, and nothing would have caught it if they had not.

⚠️ **So the ordering matters:** closing the other R2.0 rows before this one produces evidence that cannot be attributed. The work would be real and the record would not be.

## 3 · RULED 2026-09-02 — production-blocking

**Owner ruling, 2026-09-02: N-5 is production-blocking.** The row's `Class:` field is therefore the
decided value, not a recommendation operating ahead of a decision — which is what the code-owner review
correctly objected to.

⚠️ **The decisive basis is not the inclusion test.** §4.4 of `R2.0_PRODUCTION_ACCEPTANCE_CRITERIA`
already requires *"the build carries a resolvable identity (N-5, DL-243 §6e)"* as a **condition of a
pass**, independently of §4b's subset. So N-5 does not need to satisfy the subset's *"is a user actively
misled or blocked?"* test to gate: **§4 gates it directly.** That test triages *product* defects; N-5 is a
property of the *gate*, and applying a product-defect test to a measurement precondition is a category
error. The two arguments below are kept because they were the reasoning at the time, not because either
one carries the ruling.

**The recommendation as filed, retained for the record:**

The subset's inclusion test is *if this fails, is a user actively misled or blocked?* On a literal reading, no: a missing build identity misleads no user. It makes it impossible for **the owner** to know whether users are being misled, which is a different claim and arguably a different tier.

The counter-argument, and the reason it is filed as blocking: R2.0's gate is the twenty criterion ids (corrected by #277 — *eighteen* was the CLASSIFIED count). If N-5 is deferred, the other nineteen results are unattributable, and the gate reports a verdict about nothing in particular. A gate that cannot say what it examined is the same shape as a check that cannot fail.

⚠️ **Had it been ruled non-blocking it would have become a P2 row — never an optional one before the R2.0 verdict is recorded.** It was not.

## 4 · DONE CONDITION

All six, each reported with the command or observation that produced it:

1. **Re-measure the two carried observations.** Confirm or refute, on current `main`, that the deployed hostname appears nowhere in the repository and that the deployment configuration names a single hardcoded origin. Report the result either way; a refutation is as useful as a confirmation and changes the scope below.
2. **The running surface exposes an identity.** A deployed build reports the commit sha it was built from, retrievable from the surface itself — not from a deploy dashboard, a chat message, or someone's memory.
3. **It is machine-readable.** Retrievable by a command that can be pasted into a `MEASURED-BY:` line and re-run by someone else. A human-visible footer alone does not satisfy this.
4. **It round-trips to source.** Given the reported identity, `git cat-file -e <sha>` succeeds in this repository and the checked-out tree is the one that was built. An identity that names something unreachable is a label, not an identity.
5. **The deployed surface is named in the repository.** Which host serves which line is recorded in a file, so "the deployed build" resolves to something a reader can find without asking a person.
6. **The first attributed measurement exists.** One R2.0 criterion — any of the eighteen — is re-measured and its result records both `MEASURED-BY:` and the build identity. Until one result carries an identity, this row has produced a capability rather than a change.

## 5 · Out of scope, filed as a pointer

The hardcoded single origin in the deployment configuration is a separate question from identity: it concerns **which** environments can exist, not **what** a given build is. It is likely to be touched by the same work and should not be silently folded into it. If step 1 confirms it, it wants its own row.
