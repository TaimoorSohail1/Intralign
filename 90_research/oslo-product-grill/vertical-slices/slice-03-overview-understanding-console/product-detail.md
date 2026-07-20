# Slice 3 — Project Overview & Understanding Console · Product Detail

**Scope:** the Overview surface of the frozen R1 build (md5 `a327d702`) — the journey arc, the persistent Outcome Confidence read, Start here, Progress, and the top-bar chip + popover. Cumulative (Slices 1–3). Product behaviour only; no backend/API/DB.

> Regenerated to match the frozen build. The retired original slice-03 components (0–100 confidence index, "How this is calculated" pill, Orientation ▸ Expanded ▸ Validated stages, standing Project-summary panel, "Extended Analysis") are **gone** and are not documented as present.

---

## Component: The journey arc (`#ov-arc`) — DL-152→156 · `renderHeroArc()`

- **Frame:** label "Your plan, on the way to the outcome" over a four-node axis. Neutral `--maturity` accent only (never brand-orange on state, never RAG).
- **Nodes:** Understand → Validate → Improve → Execute, with an **"Optimize" bracket** over nodes 2–3 (Validate · Improve).
- **Node state (computed, `_planStage()`):**
  - `DEMO_FIRSTRUN` on → `understand`.
  - `_execReadiness().confirmed <= 0` → `understand`.
  - `frac >= 0.5` → `improve`; else → `validate`.
  - A node is **now** if it is the active stage, **done** (✓) if the journey passed it, **dest** (dashed ↗) for Execute. Exactly one active node; the active node drops a spine toward the read.
- **Node metrics (each owns exactly one, never merged — D179e; level ≠ trust):**
  - **Understand** — first-time milestone; meta "read is in" / "done". Left on the first confirmed detail (coverage > 0).
  - **Validate** — execution-readiness **coverage** ("N of M") from `_execReadiness` over the WBS · Schedule · Resources statement subset (confirmed = total − inferred). The beat that makes the read **trustworthy**.
  - **Improve** — the maturity **band** (r.band). The beat that **raises** the trustworthy read.
  - **Execute** — a **destination**, meta "to Asana · anytime". Always reachable (export non-blocking, DL-145 §4); never active, never a verdict.
- **Body line (`.ovj-body`):** per-beat intent, always ending with an Execute link and "nothing is gated."
- **Guard `_assertHeroArcIsHonest()`:** 4 nodes; exactly one computed active node equal to `_planStage()`; Execute is a destination, never active, always named "Execute"; no forecast/health vocabulary anywhere.

## Component: The persistent read (`.ch-nest`) — Outcome Confidence · D179a

Nested below the arc, tab **"The read"**, always visible across all beats (guard `_assertUnderstandDetailIsNested` — heading + ramp are genuine descendants of the inset, the inset carries its tab, the arc sits above, the active node drops a spine). Contents, top to bottom:

1. **Heading + info tip + state chip.** Heading "Outcome Confidence"; the ⓘ carries the method essence. The analysis-state chip (`#ustate`, D175) is **neutral**: Provisional (hollow dot / muted / 600) → Current (filled dot / --text / 700) — weight and shape, never hue. `error` → "Last-good" (D041).
2. **Lead-line (`#ov-leadline`, DL-132) — `_leadLineHTML()`.** One plain-language sentence: band in plain maturity words (`_LEAD_BAND_PLAIN`: Very Low "just getting started" … Very High "well-formed"), the computed limiter (`_limitingOf`), and a pointer into Start here (naming the top issue only when its title is number-free). **Carries no number/percentage** (guard `_assertLeadLineIsASynthesisNotAScore`). **Sunsets** after first engagement (`leadLineDone`); once retired it is legitimately empty.
3. **Maturity ramp (`#ov-ramp`, D174) — `renderRamp()`.** Five ordinal bands `_BANDORD` = Very Low · Low · Moderate · High · Very High; the lit step is computed from the read; ARIA states "Step N of 5". **Neutral, no percentage fill, no health colour.** A band move draws prev ghosted → current lit with an arrow; a move that did not happen is never drawn.
4. **Limiter (`#ov-limit`, D186c) — `renderLimiter()`.** Lowest CAF dimension (`_limitingOf`) + a **grounding-aware verb** from `_ciDimInferenceStats()`: `total === 0` → "Bring evidence to firm it"; grounded share < 0.45 → "Confirm it to lift the read"; else → "A plan gap to fix." ≤8 words, verb-carrying, the limit named. **Stays a limiter — never a "Blocker"**; "holding it back" is gone.
5. **Payoff (`#payoff`, D179b/c).** Dismissible "What changed" delta on the card, ≤20 words total, computed from the previous snapshot (`_MOVE`). Never displaces the state; carries **no counts** (Progress owns them). `dismissPayoff()` clears the strip and the ramp ghosts; the read is untouched.
6. **CAF rows (`#cg-clar` / `#cg-align` / `#cg-feas`, Option C) — `renderCafRows()`.** Each row: caret + name + mini ramp (`_cafRampInto`, the hero's own five-step ramp) + level word + a **per-dimension evidence cue** (`_evWord`: Well-grounded ≥.70 / Mixed evidence ≥.45 / Mostly inferred ≥.25 / Thinly evidenced / "no evidence yet", with "· g of tot") + a **"the limit"** marker on the lowest (by weight, never hue). **Level ≠ trust:** the evidence cue is provenance, never folded into the band. Click (or Enter/Space) toggles a drill-down (`_cafDrillHTML`: grounded/inferred split, open issues by severity, the lift = the top issue's own recommendation, the finding-type cut). Alignment is **live** (D133 — an attested reviewer Approve/Reject can move it either way).
7. **Grounding rollup (`#ov-grounding`, D179e) — `_ovGroundingHTML()`.** The **one home** for global grounding: "`a` of `a+d` statements **Confirmed by you** · `d` **From OSLO**" (both epistemic classes single-sourced via `_epiLabelHTML`, statement unit D253), computed from `_progressRows()`, neutral delta (no direction valence). Grows a quiet "✓ largely grounded" marker when `_isLargelyGrounded()` is live true.
8. **Footer.** The **trend chip** (`#ov-trend`) — direction + word only ("↗ Strengthened" / "Softened", D056), routes to History (`openHistorySeam`), **displayed only when the read actually moved** (`_readDirection() !== 0`); a held read shows nothing. **"Why ▾"** (`#whybox`) — opens the reliability basis in prose (band cause + Coverage/Evidence/How-assessable levels), the reliability ⓘ, and **"✦ Ask OSLO a follow-up →"** (`askOslo({type:'confidence'})`).

## Component: False-confidence flag — D052

- **Condition:** `falseConfidenceHolds(r)` — a high band on low reliability. Rendered by `renderFalseConfidence()`.
- **Placement:** the popover flag (`#cpp-flag`), the card flag (`#ov-flag`, in the Why disclosure), and a neutral flag dot on the pill (`.flagged`). All **neutral** — info glyph on a neutral surface, never RAG.
- **Copy:** names the **cause** — a reliability shortfall vs a CAF weakness — and the remedy (confirm key dependencies / add evidence). "This is advisory — the calls stay yours."
- **Absence:** when the condition is false, absent everywhere. **Demo:** the Simulate ▾ menu's "Sim false-confidence" toggle.

## Component: Start here (`#ovStartHere`) — `renderFocus()` · beat-aware

- **Order (`_beatOrder`):** Improve → issues on the limiter dimension first (`_issueOnDim` / `_beatLimiterDim`); Validate/Understand → issues with a load-bearing de-risk first (`_issueDerisk`). Severity (`_sevrank`) breaks ties.
- **Beat intent (`.focus-beat`):** one line naming what the list is for now (Validate / Improve / Understand variants). No tally.
- **Lead issue:** severity chip + title; an inline **"✦ Confirm first"** de-risk block (`startInlineConfirm` — attests the load-bearing assumption in place; the analysis update then resolves the issue, D088) and **"Review the issue →"** (`openIssue`). If the lead is already addressed → "Confirmed — updating the read…".
- **Secondary items:** up to three more, each with its de-risk hint and a jump to `openIssue`.
- **Standalone confirmations:** load-bearing statements holding up the limiter under no open issue → a pointer "Confirm on the map →" (`showView('inference')`).
- **Resolved items** list last with a ✓.
- **Advisory, non-blocking, no tally** (D179e/D183g). Guard `_assertStartHereFollowsTheBeat`.

## Component: Progress (`#ovProgress`) — `renderProgress()`

- **Pure work-state** (`_progressHTML`): Open (issues · critical · open questions) and Closed (resolved · answered), each computed from `_progressRows()` / `PAYOFF_COUNTS`; a count that cannot be computed is absent (D173). Neutral deltas since the last analysis update; a rising count is drawn identically to a falling one (only a user-earned rise is coloured, `_deltaIsEarned`). **No burndown grammar, no target, no denominator on grounding** — grounding left Progress entirely for the read's rollup.
- **The maturity ladder** (`renderStageSeq(_readRung())`, DL-129) — rung "Grounded · 3 of 5" over `_LADDER` = Oriented → Corroborated → Grounded → Anchored → Validated, computed:
  - Corroborated = grounded share ≥ .35; Grounded = ≥ .60 (`_isLargelyGrounded`); Anchored = no load-bearing statement remains (`_isFullyAnchored`); Validated = Anchored **and** stakeholder corroboration (an Approve in `ALIGN_EVIDENCE`); Oriented = baseline. Never earned by running an analysis.
- **Order vs Start here (`_orderOverview`):** `_overviewLeadsWithProgress()` = `!!_firstValue()` — first run → Start here first; after first value → Progress first. Re-read on every render.

## Component: Top-bar chip + popover (`#confpill` / `#confpop`) — D050/D051

- **Chip:** "Outcome Confidence" + band (`#cp-band`) + ladder rung (`#cp-grd` via `_readRung()`). **No 0–100 index** (D183b). **DL-130 cut the standalone grounding word** from the chip. A flag dot appears when false-confidence holds. Click toggles the popover (`toggleConfPop`); outside-click/re-click closes.
- **Popover:** band + grounding word (`_groundingWord`), the three CAF bands on the same ramp (limiter marked), the limiter verb, one computed "way out" (`cppWayOut` — opens the limiter's top issue or the full breakdown), the **reliability basis** (Coverage · Evidence · How assessable, resident line names the weakest, all three on demand), the **trust-check** ("✓ Sound basis" calm when no leg is thin / "Read this with care" loud when a leg is thin or false-confidence holds — never celebrated), and the false-confidence flag when it holds.
- Reliability is judged **independently of CAF** (D051); "How assessable" is the plain label for Assessability (D012). Reliability uses High/Moderate/Low, distinct from the five-band maturity scale. **No separate Overview reliability card** (D046).

## Behaviour: movement is direction-only + moves only at an analysis update

- **D056:** every movement surface (trend chip, payoff, ramp arrow, chat) is direction + named cause, **never a magnitude**. The read can fall and still mean better understanding, not a worse project (a fall looks exactly like a rise).
- **D088:** the read moves **only at an analysis update**. Confirming crosses an arc node and ticks Validate coverage immediately, but the **band does not jump** on the confirm — it moves when Outcome Analysis next runs.

## Non-goals / seams (do not build here)

Execution monitoring (Execute → In execution → Outcome) is a future phase, not built. The Overview is the surface; the Full plan view, Reports trio, and Asana export are their own slices (referenced only as the Execute destination and the arc's "Review & execute" link).
