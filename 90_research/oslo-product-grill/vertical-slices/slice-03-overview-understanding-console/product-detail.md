# Slice 3 — Project Overview & Understanding Console · Product Detail

**Scope:** the compact understanding console layered on the confidence-led Overview. Cumulative (Slices 1–3). Decisions D050–D056 plus all inherited/cross-cutting decisions.

## Component: Confidence pill (top bar) — D050
- **Always visible.** Contents: `Confidence` label · **index** (mono) · **band word** · **reliability qualifier** ("{Level} reliability"). A quiet neutral dot appears when the false-confidence flag holds (never severity-colored). A ▾ chevron signals it opens.
- **The single home for the metrics.** The Overview does not restate index/band/reliability as separate cards; the pill + its popover own the live console.
- **Click → popover** (`toggleConfPop`). Outside-click / re-click closes.

## Component: Confidence popover (compact console) — D050/D051/D052/D053
Structure, top to bottom:
1. **Header:** "Confidence · From OSLO" + quiet **stage marker** (Stage **Orientation** ▸ Expanded ▸ Validated).
2. **Band line:** dot · band word · `idx/100`.
3. **Caveat line:** "Understanding maturity — not health, readiness, or probability. Qualified by {level} reliability."
4. **CAF dimensions** (first level): Clarity / Alignment / Feasibility, each with a neutral maturity bar + band word.
5. **Reliability basis** (D051): Coverage · Evidence availability · **How assessable**, each with a bar + level (High/Moderate/Low). Sub-line: "Determined independently of Clarity · Alignment · Feasibility … can rise as evidence improves."
6. **False-confidence flag** (D052): conditional; neutral surface + info glyph; names the cause.
7. **"Open full breakdown → Overview"** button.

## Component: Reliability basis — D051
- Three dimensions, **independent of CAF**: **Coverage**, **Evidence availability**, **How assessable** (plain label for Assessability, D012).
- Level scale: **High / Moderate / Low** (distinct from the 5-band confidence/CAF scale; reliability is a qualifier, not a maturity index).
- **Two reach paths:** (a) the pill popover; (b) the Overview **"Why"** disclosure, in prose. **No separate Overview reliability card** (D046).

## Component: False-confidence flag — D052 (CONF-06)
- **Condition:** band ∈ {High, Very High} AND reliability level ∈ {Low, Very Low}. Evaluated by `falseConfidenceHolds(read)`.
- **Behavior:** advisory, non-alarming, **neutral** (no red/amber/green; info glyph on a neutral surface). Names the **cause** — reliability shortfall vs CAF weakness — and the remedy (confirm dependencies / add evidence).
- **Placement:** both the popover and the Confidence card (mirrored copy). A neutral dot also appears on the pill.
- **Absence:** when the condition is false, the flag is not rendered anywhere.
- **Demo:** phase-bar "Sim false-confidence" toggle flips to a High/Low read and opens the popover.

## Component: Confidence stages — D053 (CONF-05)
- Stages: **Orientation ▸ Expanded ▸ Validated.** Surfaced in (a) the Confidence info tooltip; (b) a quiet stage marker beside the number and in the popover header. Not standing chrome.
- Progression: Fast Pass = **Orientation**; Extended Analysis supersede = **Expanded**. Validated reserved for later depth.

## Component: "How this is calculated" — D054
- Affordance by the confidence number (info-glyph pill). Hover or click opens a small explainer:
  - CAF-derived (lowest dimension sets the ceiling);
  - reliability-qualified (a strong read on thin evidence is flagged, not hidden);
  - cause-bound (every move names a reason; movement is direction-only);
  - below-band jitter is not dramatized.

## Component: Project summary (More) — D055
- Plain-language narrative with five beats: **what this is · understanding level (+ stage) · main limiter · reliability basis · caveat** ("not project health, readiness, or a probability of success"). Kept inside the collapsed **More** — the read above is still the summary.

## Behavior: confidence movement — D056
- Movement is **direction-only** (▲/▼ + named cause). No fabricated magnitude is treated as canonical: the deep-pass chat notice and the trend row are worded direction-only. Confidence **can fall** (better understanding, not worse project). Real deltas remain owner-TBD.

## Non-goals / seams (do not build here)
- Attention deep interactions (Slice 4); artifact editor (Slice 5); full Issues UI / recommendation apply (Slice 6). The light Issue panel + clarification loop are the Slice-2 minimum, preserved.
