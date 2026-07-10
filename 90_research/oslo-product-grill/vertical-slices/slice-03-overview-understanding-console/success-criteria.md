# Slice 3 — Project Overview & Understanding Console · Success Criteria

## Cumulative-integrity (no regression)
- [ ] SC-0 Every Slice 1/2 route, screen, interaction, theme token, and localStorage key still works: activation funnel, four-method intake, Fast Pass ≈30s, confidence-led Overview (Confidence→Start here→Progress→More), Attention map, chat + completion notices, feature tour, clarification loop, Fast/Deep analysis-state machine, "Plan artifacts" term.
- [ ] SC-0b `node --check` on the extracted script passes with no error.

## D050 — Confidence pill + popover
- [ ] SC-1 The top-bar pill always shows index + band + reliability qualifier.
- [ ] SC-2 Clicking the pill opens a popover with the three CAF dimensions (first level), a Reliability basis section, and "Open full breakdown → Overview."
- [ ] SC-3 Metrics are not duplicated as new Overview cards — the pill/popover is the single live-metrics home.

## D051 — Reliability basis
- [ ] SC-4 Popover shows Coverage · Evidence availability · **How assessable**, each at High/Moderate/Low, independent of CAF.
- [ ] SC-5 The reliability basis is also reachable from the Overview "Why" (in prose).
- [ ] SC-6 There is **no separate Reliability card** on the Overview.

## D052 — False-confidence flag
- [ ] SC-7 When a high band sits on low reliability, a flag appears in the popover and on the card, **naming the cause** (reliability shortfall vs CAF weakness).
- [ ] SC-8 The flag is advisory, non-alarming, and **neutral** — no health/severity color.
- [ ] SC-9 It is demoable (phase-bar trigger) and **absent** when the condition doesn't hold.

## D053 — Confidence stages
- [ ] SC-10 Orientation ▸ Expanded ▸ Validated appear in the Confidence info tooltip and a quiet stage marker; not standing chrome.
- [ ] SC-11 The stage advances Orientation → Expanded after Extended Analysis.

## D054 — How this is calculated
- [ ] SC-12 A "how this is calculated" affordance sits by the number; hover/click explains CAF-derived, reliability-qualified, cause-bound, jitter-not-dramatized.

## D055 — Project summary
- [ ] SC-13 The Project summary in More is a plain-language narrative covering what it is · understanding level · main limiter · reliability basis · the "not health/readiness/probability" caveat.

## D056 — Confidence movement direction-only
- [ ] SC-14 Every confidence-move surface is direction-only (▲/▼ + named cause); no fabricated magnitude is shown as canonical.
- [ ] SC-15 Copy makes clear confidence can fall while meaning better understanding, not a worse project.

## Cross-cutting
- [ ] SC-16 Advisory-only throughout (D001); confidence never a bare number (band + reliability + cause).
- [ ] SC-17 5-band scale used for confidence + CAF (D020); reliability uses High/Moderate/Low.
- [ ] SC-18 Dark default + light parity; WCAG 2.1 AA (focus, keyboard, reduced-motion).
