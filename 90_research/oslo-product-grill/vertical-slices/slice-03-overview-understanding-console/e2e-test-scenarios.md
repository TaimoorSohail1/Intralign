# Slice 3 — Project Overview & Understanding Console · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype). "Restart" = phase-bar Restart (clears flags). The Simulate ▾ menu carries the demo triggers (Sim first-run · Replay onboarding · Sim false-confidence).

1. **Fast-path to the Overview.** Restart → activate → load sample → "See where I stand" → Fast Pass ≈30s → land on the Overview. **Expect:** the journey arc (Understand → Validate → Improve → Execute with an "Optimize" bracket), the nested "The read" panel with the maturity ramp, and the top-bar Outcome Confidence chip — **no 0–100 number anywhere.**

2. **First-run arc position.** On a fresh first run (or Simulate ▾ → "Sim first-run (Understand)"). **Expect:** exactly one active node, and it is **Understand**; Execute is a dashed ↗ destination ("to Asana · anytime"), never active; the arc says nothing like "on track" or "likely to succeed".

3. **First-run ordering.** Scan the two cards below the hero on first run. **Expect:** **Start here leads** over Progress (there is no progress to read yet).

4. **The lead-line.** Read the plain-language sentence at the top of the read. **Expect:** it names the live limiter (Feasibility), points into Start here, and contains **no number or percentage**.

5. **Confirm first → cross Understand → Validate.** In Start here, click the lead issue's **"✦ Confirm first" → Confirm**. **Expect:** the arc crosses to **Validate** (Understand shows ✓ done), the Validate node shows coverage "N of M", the lead-line retires (gone for good), and **Progress now leads** over Start here.

6. **Coverage vs band are separate.** After confirming, read the Validate meta and the Improve meta. **Expect:** Validate shows execution-readiness coverage; Improve shows the maturity **band** — two different metrics, never merged (you can gain coverage while the band holds).

7. **Read moves only at an analysis update.** Immediately after a confirm, watch the read. **Expect:** coverage ticks and the node crosses instantly, but the **band does not jump** on the confirm — it moves when the analysis update lands (Provisional → Current), shown as a "What changed" payoff.

8. **Validate beat order.** While on Validate, read Start here. **Expect:** the beat intent reads "Confirm these to make OSLO's read trustworthy"; the lead is an issue whose load-bearing assumption grounds the read (severity breaks ties).

9. **Improve beat order.** Reach Improve (confirm load-bearing coverage past half). **Expect:** the beat intent reads "Resolve these to lift the read — your limit is Feasibility"; Start here now leads with a **limiter-dimension** issue.

10. **Execute is never gated.** At any beat, click the arc's "Review & execute →" / "Execute whenever →". **Expect:** it opens the Full plan (`showView('fullplan')`); nothing on the arc ever blocks it, and Execute never reads as a "ready" verdict.

11. **The maturity ramp is the hero.** Inspect the ramp. **Expect:** five ordinal steps (Very Low…Very High), the current one lit and named, **no percentage fill and no health colour** — cool `--maturity` accent only.

12. **The limiter carries a verb, not a blocker.** Read the limiter line. **Expect:** "Feasibility — the lowest. Confirm it to lift the read." (or "Bring evidence…" / "A plan gap to fix"); the word "Blocker" and the phrase "holding it back" appear nowhere.

13. **CAF row — level ≠ trust.** Read the Feasibility row, then click it. **Expect:** a level word **and** a separate evidence cue (e.g. "Mostly inferred · 1 of 3") + "the limit" marker; clicking toggles a drill-down whose band stays a band (only drivers are quantified).

14. **Grounding has one home.** Read the grounding rollup under the CAF rows, then scan Progress. **Expect:** "N of M statements Confirmed by you · K From OSLO · ✓ largely grounded" appears on the read **only**; the same grounded/inferred counts are **not** repeated on Progress.

15. **Progress is work-state + the ladder.** Read the Progress card. **Expect:** Open (issues · critical · questions) / Closed (resolved · answered) with **no completion %, no target, no RAG**, plus a ladder rung "Grounded · 3 of 5" (Oriented → Corroborated → Grounded → Anchored → Validated).

16. **Rising issues is not a regression.** Let the analysis update find new issues. **Expect:** the issue count can rise **and** the read can firm in the same payoff; nothing draws the rise as a failure (a fall would look identical to a rise).

17. **Top-bar chip + popover.** Read the chip, then click it. **Expect:** the chip shows band + the **ladder rung** (no standalone grounding word, no index); the popover shows CAF bands, the reliability basis (Coverage · Evidence · How assessable), and a **trust-check** ("✓ Sound basis" calm, or "Read this with care").

18. **Why → reliability basis, no card.** Expand "Why ▾" on the read. **Expect:** the reliability basis in prose (independent of CAF) plus "✦ Ask OSLO a follow-up →"; there is **no separate reliability card** on the Overview.

19. **False-confidence — neutral disclosure.** Simulate ▾ → "Sim false-confidence". **Expect:** a **neutral** flag (info glyph, no red/amber/green) appears on the popover, the read card, and a dot on the chip, naming the cause (reliability shortfall vs CAF weakness); toggling off removes it everywhere.

20. **Trend, theme + a11y.** Confirm the trend chip shows only after the read moves (direction + word, no magnitude); then toggle light theme, keyboard-tab to the chip and open the popover, and check reduced-motion. **Expect:** the trend chip is hidden on a held read; light parity holds; focus rings visible; popover keyboard-operable; no analysis animation under reduced-motion.
