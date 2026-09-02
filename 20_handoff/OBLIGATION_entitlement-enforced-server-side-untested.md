# OBLIGATION — GT-106 · GT-110: server-side entitlement enforcement has never been tested

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-09-01, filed on discovering that the subset's own "highest-value unrun check" has no obligation object
**Invariants violated:** GT-106 · GT-110 — named in the production-gating subset. ⚠️ The precise invariant statements live in the acceptance register on the design line and have not been read into this row. **Escalated, not restated from memory.**

## 1 · What was measured — and what was not

`R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b Tier 4 records:

> **GT-106 · GT-110** entitlement enforced server-side — **untested — highest-value unrun check**

That is the whole of the evidence. The controls have not been exercised, in either direction, on any build.

`MEASURED-BY:` the criteria document's own state column, which is an absence of measurement rather than a measurement.

## 2 · Why an untested control is a defect and not merely a gap

The capacity gate is enforced somewhere. `GT-01 · GT-02` — the gate names capability, tier and price, and exemptions are free — read ✅ passing, which is a **client-surface** result. Nothing has established that a request bypassing that surface is refused by the server.

Freemium doctrine gates **capacity, never judgment quality**. That promise is only true if the boundary is enforced where the user cannot reach it. If enforcement is client-side, the tier structure is a suggestion, and the product's pricing model is unbacked in exactly the way the honesty doctrine forbids elsewhere: a surface asserting something the mechanism does not make true.

**Untested is not passing.** §2 of the criteria document establishes that a deferred criterion with no named iteration is PENDING-SUBJECT, which is not a pass. An untested control shipped to production is the same claim with less paperwork.

⚠️ **This row asserts no failure.** It asserts that no one knows. The RED proof below may show enforcement is already correct, in which case the row closes on evidence rather than on work. That outcome is a success, not a wasted row.

## 3 · Owner ruling required on the classification

This row is filed as production-blocking on the reasoning above — an unverified server-side entitlement boundary is a defect in itself. **That classification is a recommendation, not a ruling.**

The subset's inclusion test is: *if this fails, is a user actively misled or blocked?* An entitlement bypass does not mislead the user who exercises it; it misleads everyone who paid. Whether that satisfies the test is the owner's call. If the owner rules otherwise, this becomes a P2 row and the `Class:` line changes — but it does not become untested-and-shipped.

## 4 · DONE CONDITION

All five, on the deployed build, each reported with the command or observation that produced it:

1. **The boundary is named.** State which server endpoints enforce entitlement, and for which capabilities and tiers. An enforcement claim that names no endpoint cannot be tested.
2. **RED proof — the bypass is attempted.** A request that skips the client surface and asks for a capability above its tier is issued directly against the deployed API, and is **refused by the server**. The refusal is recorded with the status and body. If it succeeds, that result is the finding and it escalates immediately.
3. **The exemption path is proved in the same run.** Exemptions are free per `GT-01 · GT-02`; prove that an exempt request is *not* refused, so the check is shown to discriminate rather than to deny uniformly. A control that refuses everything is not enforcement.
4. **Both directions, both invariants.** GT-106 and GT-110 are separate statements and each gets its own recorded result. One aggregate "entitlement works" closes neither.
5. **The result reaches the register.** Whatever is measured is written back to the acceptance register so the state column stops reading `untested`. A fix that is not recorded where the gate reads it has not moved the gate.

## 5 · Related, not covered here

`GT-01 · GT-02` read ✅ passing on the client surface and are not re-opened by this row. If step 2 shows the server does not enforce, that passing state becomes misleading rather than wrong — the gate does name capability, tier and price; it simply is not the thing that holds. Record that relationship rather than silently flipping the other row.
