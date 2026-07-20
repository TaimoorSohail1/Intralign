# Slice 3 — Project Overview & Understanding Console · Workflow

Cumulative (Slices 1–3). Actor workflows on the Overview surface of the frozen build. Actors: **User** · **System** (client-side prototype render/state) · **AI** (simulated OSLO — timers + fixed illustrative data; no real model, no network).

> Regenerated to match the frozen build. Flows reference the current arc/read/ladder model, not the retired index/stage model.

## Preserved end-to-end journey (INHERITED)

Invite → Activate → Welcome → Intake (4 methods) → **Fast Pass ≈30s** → land on the **read-led Overview** (Attention map co-primary) → **Outcome Analysis** auto-runs, non-blocking, supersedes provisional→current → clarification loop closes issues via an analysis update. Completion notices land in OSLO chat. Optional tour.

## Flow A — Land on the Overview (first run)

1. **System** renders the hero card: `renderHeroArc()` (arc at **Understand** — no coverage yet), `renderLeadLine()` (the plain-language nudge), `renderHero()` (ramp + limiter + trend), `renderCafRows()` (CAF bands + grounding rollup), the pill (band + ladder rung).
2. **System** orders the Overview (`_orderOverview`): no value earned → **Start here leads**, Progress second.
3. **User** reads the lead-line and follows it into **Start here**.

## Flow B — Confirm the first detail (cross Understand → Validate)

1. **User** clicks the lead issue's **"✦ Confirm first"** (`startInlineConfirm`) — or a standalone confirmation on the Inference map.
2. **System** attests the load-bearing assumption; `markLeadLineDone()` retires the lead-line; `_execReadiness().confirmed` rises above 0.
3. **System** re-renders: `_planStage()` now returns `validate` → the arc crosses **Understand → Validate** (Understand shows ✓ done), the active node's spine drops to the read, and `_orderOverview` flips **Progress to lead** (first value earned).
4. **AI** runs the analysis update: the issue moves Addressed → Resolved (**only the update resolves**, D088); the band may move on the ramp; the payoff shows "What changed"; the trend chip appears if the read moved. **The band does not jump on the confirm itself** — it moves at the update.

## Flow C — Validate → Improve (the two Optimize beats)

1. **User** confirms further load-bearing inferences (Start here leads with de-risking issues on **Validate**, `_beatOrder`).
2. **System** raises `_execReadiness().frac`. When `frac ≥ 0.5`, `_planStage()` returns `improve` → the arc crosses to **Improve**.
3. **System** re-ranks Start here to the **limiter dimension** (`_beatLimiterDim` / `_issueOnDim`); the beat intent line changes to "Resolve these to lift the read — your limit is <dim>."
4. **User** resolves limiter-dimension issues → **AI** analysis update → the band lifts on the ramp. Execute stays reachable throughout (never gated).

## Flow D — Read the read (persistent panel)

1. **User** scans the nested read (`.ch-nest`): ramp (band), limiter (+ grounding-aware verb), CAF rows, grounding rollup.
2. **User** clicks a CAF row → **System** toggles the drill-down (grounded/inferred, open issues by severity, the lift). The band stays a band; only drivers are quantified.
3. **User** expands **"Why ▾"** → **System** shows the reliability basis in prose (band cause + Coverage/Evidence/How-assessable) and the "✦ Ask OSLO a follow-up" hand-off.

## Flow E — Top-bar chip + popover

1. **User** clicks the **Outcome Confidence chip** (band + ladder rung) → **System** opens the popover (`renderConfPop`): CAF bands, limiter verb, one computed way-out, reliability basis (weakest named; all three on demand), the **trust-check** ("✓ Sound basis" or "Read this with care").
2. **User** clicks the way-out → **System** opens the limiter's top issue or the full Overview breakdown. Outside-click/re-click closes.

## Flow F — Outcome Analysis supersede, direction-only

1. **AI** completes an analysis update → `ANALYSIS_STATE = current`; **System** flips the state chip Provisional → **Current** (neutral, D175).
2. **System** updates the ladder rung (`_readRung`, computed from evidence), the payoff, and — only if the read moved — the trend chip (direction + cause, **no magnitude**, D056).
3. On failure (D041): last-good preserved; the chip reads "Last-good"; chat offers Retry.

## Flow G — Clarification loop (INHERITED)

1. **User** answers a clarification in the tied issue (or in chat — same door).
2. **AI** runs the analysis update → issue resolves → the read is refined (direction-only) → **System** re-renders the whole Overview (arc, read, CAF, grounding rollup, Progress, ladder). The chat never claims to have closed the issue itself.

## Flow H — Demo triggers (Simulate ▾ menu)

- **Sim first-run (Understand)** (`simFirstRun` → `DEMO_FIRSTRUN = true`): forces the arc back to Understand so the Understand → Validate crossing is demoable; cleared on the first confirm.
- **Replay onboarding** (`demoReplayOnboarding`).
- **Sim false-confidence** (`toggleFalseConf`): flips to a high-band/low-reliability read so the neutral false-confidence flag surfaces (popover + card + pill dot).

## Simulated-AI boundary

All analysis is timers + fixed illustrative data. Position on the arc, the ladder rung, coverage, and the read are all **computed from state** (D173) — never authored. Movement obeys D056 (direction + cause) and D088 (moves only at an analysis update) in every simulated path.
