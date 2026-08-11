# DR-7 — Pricing (RATIFIED)

*Resolve-first decision · ratified by Idris, 2026-08-04 · closes the last OPEN item from
`DL-200-205_R2_RESOLVE_FIRST_DECISIONS.md`. Staged in `release-2/`, withheld from `main` until R1
graduation (Framework 001: AI drafts; owner ratifies canon).*

## Decision

**Basic = $29/mo, flat per account.** Annual **$290/yr (2 months free, ≈$24/mo)**. The placeholder
flag is dropped in the prototype (`_PRICING.basic.ph = false`).

**Pro = $79/mo — PROVISIONAL.** Kept as a marked placeholder (`ph:true`) because nothing gates to
Pro in R2; Pro's value line (continuous monitoring, auto-import / two-way sync) is post-R2. Finalize
when those capabilities ship. Open consideration: tighten $79 → ~$69 so the Basic→Pro step isn't 2.7×.

## Premise (doctrine-forced, not a free choice)

OSLO is priced **flat, per account — never per seat.** Seat-metering would charge for people in the
reviewer / Viewer loop, which the doctrine forbids ("record, reviewers, Viewers free forever"). So one
paying owner radiates value to a whole team at no per-head cost — the opposite of every per-seat
competitor. Seats reappear only at the post-R2 **Team/Enterprise** tier, and only for *active
collaborators* (CM-1 seated collab, CM-2 governance) — never for Viewers/reviewers.

## What Basic actually unlocks (the one live R2 fence)

All three current paywalls resolve to Basic: **optimize all outcomes** (not just the primary),
**run more than one plan**, **read a larger corpus**. It gates **capacity, never the quality** of the
read — the accuracy bar is identical on every plan (one bar for all; doctrine).

## Rationale

- **Learn-first.** The commitment gate (DR-3) is a *willingness-to-pay instrument*. Launch at the
  low-friction, under-$30, individual-expensable price to maximize the conversion signal, then raise
  with evidence rather than guessing high now.
- **Anchors (Aug 2026).** Prosumer AI (Claude Pro / ChatGPT Plus) $20/mo single-user; ClickUp Business
  $12/seat/mo annual (+$9/seat AI add-on); ClickUp Business Plus $19/seat annual; Claude Team
  $25–30/seat. A flat $29 OSLO account with free radiating reviewers is *cheaper than a 3-seat ClickUp
  Business + AI add-on*, while being one predictable line item.
- **$29 position.** Just above the $20 prosumer anchor — justified because Basic unlocks
  team-radiating capacity, not a single-user power-up.

## Prototype changes (this pass)

`_PRICING.basic`: `ph:true → ph:false`; added `annual:'$290/yr'`, `annualNote:'2 months free'`.
`_payGate()` renders an annual line under the price when `t.annual && !t.ph` (`.pw-annual` style).
Pro unchanged (still `ph:true`). Verified: 29/29 `_S10` green, 0 JS errors; paywall shows
"Basic · $29/mo / or $290/yr · 2 months free" with no placeholder tag, doctrine copy intact.

## Still open

- Pro final price (revisit at continuous-monitoring/sync launch).
- Annual billing mechanics (proration/dunning/self-serve) — deferred build item, as noted in checkout stub.
