# Slice 3 — Project Overview & Understanding Console · Success Criteria

The developer's checklist for the Overview surface of the frozen build (md5 `a327d702`, boot 157/157). **FREEZE-INTACT:** these assert the build as frozen — not new enhancements.

## Cumulative-integrity (no regression)
- [ ] SC-0 Every Slice 1/2 route, screen, interaction, theme token, and localStorage key still works (activation funnel, four-method intake, Fast Pass ≈30s, read-led Overview, Attention/Issues, chat + completion notices, tour, clarification loop, analysis-state machine).
- [ ] SC-0b The build boots green (157/157 guards) with no console error.

## The journey arc (DL-152→156)
- [ ] SC-1 The arc shows exactly **four** nodes: Understand → Validate → Improve → Execute, with an **"Optimize" bracket** over Validate · Improve.
- [ ] SC-2 The active node is **computed** from state (`_planStage`): no coverage → Understand; frac < 0.5 → Validate; frac ≥ 0.5 → Improve. Exactly one active node, and it equals `_planStage()`.
- [ ] SC-3 **Understand** is a first-time milestone — left on the first confirmed detail (coverage > 0), shown ✓ done afterward; never re-gated by band.
- [ ] SC-4 **Validate** carries execution-readiness coverage ("N of M", `_execReadiness` over WBS·Schedule·Resources); **Improve** carries the maturity band. The two metrics are **never merged** (23/23 can still be Moderate).
- [ ] SC-5 **Execute** is a destination ("to Asana · anytime", dashed ↗) — never marked active, never a "ready" verdict; export is non-blocking (nothing is gated).
- [ ] SC-6 The arc contains **no forecast/health vocabulary** ("on track", "likely", "ready to succeed", "at risk"…) and uses only the `--maturity` accent — no brand-orange on state, no RAG. (`_assertHeroArcIsHonest`)

## The persistent read (D179a)
- [ ] SC-7 The Outcome Confidence read is **always visible**, nested in `.ch-nest` below the arc (tab "The read"), across every beat; the active node drops a spine to it. (`_assertUnderstandDetailIsNested`)
- [ ] SC-8 The concept is named **"Outcome Confidence"** wherever named (D199); there is **no 0–100 index** anywhere — hero, chip, popover, trend, chat (D183b). No composite/forecast score.
- [ ] SC-9 The maturity ramp is the hero: five ordinal bands (Very Low…Very High), lit+named current, **neutral, no percentage fill, no health colour** (D174/D003).
- [ ] SC-10 The lead-line is one plain-language sentence, **computed from state** (names the live limiter), **carries no number/percentage**, and **sunsets after first engagement** (DL-132). (`_assertLeadLineIsASynthesisNotAScore`)
- [ ] SC-11 The limiter names the lowest CAF dimension + a grounding-aware verb ("Confirm it to lift the read" / "Bring evidence to firm it" / "A plan gap to fix"); it is **never a "Blocker"**, and "holding it back" appears nowhere (D186c).
- [ ] SC-12 The analysis-state chip is **neutral** — Provisional → Current by weight/shape (dot + word), never colour (D175/D040); `error` → "Last-good" (D041).
- [ ] SC-13 The payoff is a dismissible "What changed" delta on the card, ≤20 words, computed, and carries **no counts** (D179b/c).

## CAF rows (Option C — DL-123/124)
- [ ] SC-14 Each of Clarity/Alignment/Feasibility shows a mini ramp + level word + a **per-dimension evidence cue** (e.g. "Mostly inferred · 1 of 3"); the lowest carries "the limit" (by weight, never hue).
- [ ] SC-15 **Level ≠ trust**: the evidence cue is provenance, never folded into the band. Clicking a row toggles a drill-down whose band stays a band (only drivers quantified); Alignment is live (D133).

## Grounding rollup — one home (D179e)
- [ ] SC-16 Global grounding lives in exactly **one place** — the read's rollup ("N of M statements Confirmed by you · K From OSLO · ✓ largely grounded"), naming both epistemic classes and the statement unit; it is **absent from Progress**. (`_assertProvenanceCountsHaveOneHome` / `_assertNoCountIsRenderedTwice`)

## Start here — beat-aware (D183g)
- [ ] SC-17 Start here re-ranks the same open-issue set by the current beat (`_beatOrder`): Validate leads with load-bearing/de-risking issues, Improve leads with limiter-dimension issues; **severity breaks ties**. (`_assertStartHereFollowsTheBeat`)
- [ ] SC-18 A one-line beat intent (`.focus-beat`) states what the list is for; the lead carries an inline "✦ Confirm first" (`startInlineConfirm`) + "Review the issue →". Start here is advisory, non-blocking, and carries **no tally**.

## Progress + the maturity ladder (DL-129)
- [ ] SC-19 Progress is **pure work-state** (Open: issues·critical·questions / Closed: resolved·answered) with **no burndown grammar** — no completion %, no target, no denominator, no RAG; a rising count is a deeper read, not a regression.
- [ ] SC-20 The ladder rung reads "Grounded · 3 of 5" over Oriented → Corroborated → Grounded → Anchored → Validated, **computed from evidence** (grounded share / load-bearing / stakeholder corroboration), never from running an analysis.
- [ ] SC-21 Which of Start here vs Progress leads is **computed** (`_orderOverview`): first-run → Start here first; after first value → Progress first.

## Top-bar chip + popover (D050/D051)
- [ ] SC-22 The chip shows band + the **ladder rung** (DL-130 cut the standalone grounding word); clicking opens the popover with CAF bands, the reliability basis (Coverage · Evidence · How assessable, independent of CAF, D051), and the **trust-check** ("✓ Sound basis" calm / "Read this with care" loud — never celebrated).
- [ ] SC-23 There is **no separate Overview reliability card** (D046); reliability is also reachable from "Why" in prose.

## Movement + boundary
- [ ] SC-24 Every movement surface is **direction + named cause**, never a magnitude (D056); a fall looks exactly like a rise. The trend chip shows **only when the read moved**.
- [ ] SC-25 The read moves **only at an analysis update** (D088): confirming crosses a node and ticks coverage immediately, but the band does not jump on the confirm.
- [ ] SC-26 The false-confidence flag (high band on low reliability) is **neutral, advisory, never RAG**, names the cause, appears in popover + card + pill dot, and is absent when the condition is false (D052).

## Cross-cutting
- [ ] SC-27 Advisory-only throughout (D001); severity red/amber/green only on issues (D003); dark default + light parity; WCAG 2.1 AA (focus, keyboard, reduced-motion).
