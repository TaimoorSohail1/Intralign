# OBLIGATION — B3: Grounding's numerator and denominator both move, and unknown reads as bad

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 staging fitness audit — `20_handoff/audits/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md` *(path corrected 2026-09-02: this row cited `release-2/…`, which exists on no ref. B0 cited the same audit correctly.)*
**Invariants violated:** ▶ **RULED 2026-09-02 — `GT-61 · GT-93`** *(the grounding counter matches state)*. Not derived here: `R2.0_PRODUCTION_ACCEPTANCE_CRITERIA` §4b binds them to this defect by name — *"GT-61 · GT-93 grounding counter matches state · **B3 — numerator fell to 0 after two attestations** · ⚠️ FAILS"*.
⚠️ **`GT-35` is deliberately NOT bound.** §4b annotates it *"⚠️ B3"*, so the association is on the record — but **R2.0-9 ruled GT-35 UNTESTED**, and binding an untested criterion into this row's acceptance would let B3 close against something never measured. That is skip-as-pass in a new place. GT-35's annotation stands as a cross-reference, not a binding, and it moves here only once it has been tested.
*(The field previously read "NOT YET DETERMINED — the GT acceptance register lives on the design line and was not reachable when this obligation was written." That reason expired: `design/release-2.1` is current and reachable.)*

## 1 · What was measured

On staging, Grounding read in sequence:

```
1 of 24  →  1 of 23  →  0 of 29  →  2 of 29
```

- The **denominator is unstable** — the count of load-bearing items moved run to run on an unedited plan.
- The **numerator fell to 0 after two successful attestations.** The user verified two things and the reading went down.
- Separately, **Adaptability read "Fragile" on "0 of 0" checkpoints** — an unknown rendered as a bad result — until a later re-analysis changed it to 0 of 4.

## 2 · Why this is blocking for production

Grounding is the floor pillar. It is the one number that is supposed to mean *"this much of your plan rests on something verified"*, and the only thing that moves it is verification — **only-verify-moves-Grounding**. A numerator that falls after successful attestations inverts that rule in the most visible way possible: the user does exactly the right thing and is told it counted for less than before.

The "0 of 0 → Fragile" reading is a separate and equally serious failure: **unknown must not render as bad.** A plan with no checkpoints yet has an absent measurement, not a poor one, and showing Fragile turns a gap in the data into a judgement about the user's plan. That is the maturity-read-never-forecast doctrine failing.

## 3 · Cause and current state

**Shared cause with B1 and B2 for the count movement:** an unstable finding set produces an unstable denominator, and attestations that lose their join produce a collapsing numerator. Engineering's remediation report covers persistence of the semantic anchor — *"`graph_node_id`, finding type, and target are stored and restored"* — which is the mechanism the numerator depends on.

Fixed in **PR #249**, commits `1fad48d`, `94dafb1`.

⚠️ **Verified locally only.** The sequence above has not been re-run on staging.

⚠️ **The "0 of 0 reads Fragile" defect is NOT addressed by the identity fix and must not be closed with it.** It is a presentation rule about how an absent measurement is rendered, and nothing in #249 touches it. It is grouped here because it was observed in the same pillar during the same session — the fix is independent.

## 4 · DONE CONDITION

On the deployed build carrying the fix, each result reported with the command or observation that produced it:

1. **The denominator holds** across three re-analyses of an unedited plan. The load-bearing count is a property of the plan, so it may not move when the plan does not.
2. **The numerator never falls after a successful attestation.** Verify two items and re-analyse: Grounding is greater than or equal to its prior reading, every time. A single observed decrease fails this row.
3. **"0 of 0" renders as unknown, never as Fragile** — and no pillar renders a band from an absent measurement. This is a separate change and needs its own evidence; item 1 and 2 passing does not close it.
4. **The two measures stay distinguishable.** Grounding is two measures with two names; confirm the re-measured surface does not collapse them, and that `Grounded g of N` is what appears (`Understanding` is retired).

## 5 · Notes

Items 1 and 2 should follow from the identity fix. **Item 3 will not** — it is a rendering rule with no commit behind it yet, and it is the one most likely to be quietly dropped when the other three go green.

Related and NOT covered by this obligation: the audit's finding that **colour encodes pillar identity rather than maturity** — Grounding/Fragile renders green `rgb(79,195,161)` while Adaptability/Fragile renders pink. That violates the single-hue maturity ramp directly and needs its own obligation; it is filed here only as a pointer so it is not lost.
