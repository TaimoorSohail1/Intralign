# Slice 3 — Project Overview & Understanding Console · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype). "Restart" = phase-bar Restart (clears flags).

1. **Fast-path to console.** Restart → activate → load sample → "See where I stand" → Fast Pass ≈30s → land on Overview. **Expect:** pill shows index + Moderate + "Moderate reliability."
2. **Open the popover.** Click the pill. **Expect:** popover with CAF (Clarity High, Alignment Moderate, Feasibility Very Low), a Reliability basis section, and "Open full breakdown → Overview."
3. **Reliability basis contents.** In the popover, read the basis. **Expect:** Coverage · Evidence availability · **How assessable**, each labelled High/Moderate/Low.
4. **Console → Overview.** Click "Open full breakdown → Overview." **Expect:** popover closes; Overview shown; no duplicated metric cards appeared.
5. **Outside-click closes.** Open popover, click elsewhere. **Expect:** popover closes.
6. **Reliability from Why.** Expand "Why ▾" on the Confidence card. **Expect:** prose names the reliability basis (Coverage/Evidence availability/How assessable); no separate reliability card exists.
7. **Stage marker present.** **Expect:** a quiet "Stage Orientation ▸ Expanded ▸ Validated" marker by the number and in the popover; info tooltip names the stages.
8. **How this is calculated (hover).** Hover "How this is calculated." **Expect:** explainer with CAF-derived / reliability-qualified / cause-bound / jitter-not-dramatized.
9. **How this is calculated (click).** Click it. **Expect:** same explainer toggles open/closed; outside-click closes.
10. **False-confidence — arm it.** Phase bar → "Sim false-confidence." **Expect:** read flips to High band on Low reliability; popover opens; a **neutral** flag appears naming a **reliability shortfall**; a neutral dot appears on the pill.
11. **False-confidence — neutrality.** Inspect the flag. **Expect:** no red/amber/green; info glyph on a neutral surface; advisory wording.
12. **False-confidence — card mirror.** Close popover; look at the Confidence card. **Expect:** the same neutral flag is mirrored on the card.
13. **False-confidence — disarm.** Toggle "Sim false-confidence" off. **Expect:** flag disappears from popover, card, and pill; read returns to normal.
14. **Extended Analysis supersede.** Wait for Extended Analysis (or observe on arrival). **Expect:** chip flips Provisional → Current; **stage advances to Expanded**; chat says movement **▲ up** (direction-only, no "58 → 62").
15. **Trend row direction-only.** After supersede, read the trend row. **Expect:** "Up — deeper analysis firmed up the read"; no fabricated number.
16. **Clarification loop still closes issues.** Open the Wi-Fi issue → answer the clarification → reanalyze. **Expect:** issue resolves; Feasibility rises; popover/why/summary re-sync; movement stays direction-only.
17. **Project summary depth.** Open More → Project summary. **Expect:** five beats — what it is · understanding level (+stage) · main limiter · reliability basis · "not health/readiness/probability" caveat.
18. **Overview structure intact.** Scan the Overview. **Expect:** exactly Confidence → Start here → Progress → More; no new standing sections; no reliability card.
19. **Attention co-primary + tour.** Switch to Attention; run the feature tour. **Expect:** heatmap works; tour includes a step spotlighting the pill/console; nothing regressed.
20. **Theme + a11y.** Toggle light theme; keyboard-tab to the pill and open the popover; check reduced-motion. **Expect:** parity in light; focus rings visible; popover keyboard-operable; no analysis animation under reduced-motion.
