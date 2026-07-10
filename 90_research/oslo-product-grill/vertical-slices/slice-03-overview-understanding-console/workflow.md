# Slice 3 — Project Overview & Understanding Console · Workflow

Cumulative (Slices 1–3). This slice adds no new route; it deepens the confidence surface. Flows below are the Slice-3 additions layered on the preserved Slice-1/2 journey.

## Preserved end-to-end journey (INHERITED)
Invite → Activate → Welcome → Intake (4 methods) → **Fast Pass ≈30s** → land on **confidence-led Overview** (Attention co-primary) → **Extended Analysis** auto-runs, supersedes provisional→current → clarification loop closes issues via reanalysis. Completion notices land in OSLO chat (D043). Optional tour (D044).

## Flow A — Open the compact console (D050)
1. User clicks the top-bar **Confidence pill** → `toggleConfPop()`.
2. Popover renders from the **current read**: CAF dimensions → **Reliability basis** → (conditional) **false-confidence flag** → "Open full breakdown → Overview."
3. "Open full breakdown → Overview" closes the popover and shows the Overview.
4. Outside-click or re-click closes it. The pill remains the single metrics home.

## Flow B — Reach the reliability basis from the Overview (D051)
1. On the Confidence card, user expands **"Why ▾"**.
2. The Why box states the band cause **and the reliability basis in prose** (Coverage / Evidence availability / How assessable), noting reliability is judged independently of CAF and can rise as evidence improves.
3. A pointer notes the full basis is in the pill popover. **No separate reliability card is shown** (D046).

## Flow C — False-confidence flag appears/disappears (D052)
1. Condition check (`falseConfidenceHolds`): high band + low reliability.
2. If true: a **neutral** flag renders in the popover and on the Confidence card; a neutral dot appears on the pill; the flag **names the cause** (reliability shortfall vs CAF weakness).
3. If false: flag absent everywhere.
4. **Demo:** phase-bar **"Sim false-confidence"** flips to a High/Low read, re-renders, and opens the popover so the flag is visible; toggling again restores the normal read.

## Flow D — Stage + how-calculated (D053/D054)
1. The confidence-info tooltip names the stages (Orientation ▸ Expanded ▸ Validated); a quiet stage marker sits by the number and in the popover.
2. Hover/click **"How this is calculated"** → explainer (CAF-derived · reliability-qualified · cause-bound · jitter-not-dramatized).

## Flow E — Extended Analysis supersede, direction-only (D040 + D056)
1. Extended Analysis completes → `ANALYSIS_STATE = current`; the chip flips provisional → **Current**.
2. The **stage** advances Orientation ▸ **Expanded**.
3. The chat notice and the trend row report movement **direction-only** (▲ up, named cause) — **no fabricated magnitude**.
4. On failure (D041): last-good preserved; chat offers Retry. Unchanged from Slice 2.

## Flow F — Clarification loop → reanalysis (INHERITED, D042)
Answer a clarification in the tied Issue → simulate reanalysis → issue resolves → confidence refined (direction-only) → Feasibility rises. Unchanged, but the refined read now also updates the stage marker, popover, reliability basis prose, and Project summary via `renderOverview()`.

## Simulated-AI boundary
All analysis is timers + fixed illustrative data. No real model, no network. Confidence movement obeys D056 in every simulated path.
