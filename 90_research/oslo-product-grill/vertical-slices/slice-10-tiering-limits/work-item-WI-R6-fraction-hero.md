# WI-R6 — Progress hero: fraction + evidence-forward caption — SLICE-10 REOPEN

**Opened:** 2026-07-14 · **Slice:** 10 (Overview / Progress panel) · **Status:** Signed off (closed 2026-07-14)
**Trigger:** Owner feedback — "17 grounded facts" (absolute) lacked context ("17 out of what?") and "Confirmed by you" was not intuitive.

## Change (owner-selected variant B, from a 3-up mockup)
The Progress hero becomes a **fraction**: **`17 of 28`** — grounded (attested) of total claims (grounded + inferred) — with an evidence-forward caption: *"grounded in your evidence / the rest of your read is OSLO's inference."* The denominator gives the missing context; the caption puts "your evidence" in the hero prose so **"Confirmed by you" is contextualized rather than carrying the meaning alone**.

## Kept (canon)
"Confirmed by you" stays on the segment — `_assertConfirmIsTheVerbAndGroundedIsTheState` (D196/D194c) HARD-requires `epiClassName('you') === "Confirmed by you"` present on the panel. Renaming the class to "Your evidence" would reverse D196 and change it on 4 surfaces (evidence attribution, recommendation tag, Readout, Progress) — NOT done.

## Consistency with canon
Consistent with **DL-112**: the hero's primary number is still **grounded/attested only** (17); the "of 28" is a denominator for context, and the caption states the rest is inference (never claims 28 are grounded). No reversal → no new canon DL required. (A one-line DL-112 addendum noting the denominator-context presentation is optional.)

## Guards
`_assertPgxBarIsComputedFromRealCounts` extended: the hero denominator "of N" is verified `== grounded + inferred` (computed, not typed). Percentage hero (variant C) was rejected — it would trip `_assertNoZeroToHundredIndexAnywhere` (the deleted 0–100 index) and falls when OSLO infers more. Prototype: **136/136, 0 pageerrors**, both themes.

## Re-signoff
**SIGNED OFF 2026-07-14 by owner** (Decision 252, variant B). Docs reconciled + pushed to main (c20ef5b). WI-R6 CLOSED.
