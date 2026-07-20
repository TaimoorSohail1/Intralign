# Slice 3 — Project Overview & Understanding Console · Product Data

Client-side prototype only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no API, no real AI.** "Persistence" below means browser localStorage; real-store tech is owner-TBD and out of scope. These are the **product entities, visible fields, and prototype-local data concepts** the Overview reads — not a schema.

> Regenerated to the frozen build. The retired `index` (0–100), `stage` (Orientation/Expanded/Validated), and "how-calc" copy fields are **gone** and are not documented as present.

---

## OutcomeConfidenceRead (the Overview focal object)

The read on screen (`currentRead()`), paraphrased in plain words by the lead-line and drawn on the ramp.

| Concept | Values | Notes |
|---|---|---|
| `band` | 5-band ordinal: **Very Low · Low · Moderate · High · Very High** (`_BANDORD`) | The read's maturity position. **Never a 0–100 index** (D183b). Shown as the lit step on the ramp; paraphrased in the lead-line. |
| CAF triple | Clarity · Alignment · Feasibility, each `{ dim, lvl:<5-band word>, w:0–100 }` (`_cafOf`) | The lowest `w` is the **limiter** (`_limitingOf`). Frozen defaults: Clarity High (76), Alignment Moderate (55), Feasibility the limiter. Shown as mini ramps (bands, never fills). |
| per-dimension evidence | grounded / inferred / total per dimension (`_ciDimInferenceStats`) → word (`_evWord`) | **Provenance, separate from the level** (level ≠ trust, Option C DL-123/124). Cue words: Well-grounded / Mixed evidence / Mostly inferred / Thinly evidenced / "no evidence yet". |
| analysis state | `provisional · current · error` (`ANALYSIS_STATE`) | The neutral state chip (D175/D040): Provisional → Current; `error` → "Last-good" (D041). Weight/shape, not colour. |
| `reliability` | `{ coverage, evidence, assessable }`, each **High · Moderate · Low** | Independent of CAF (D051). "How assessable" is the plain label for Assessability (D012). Frozen default: all Moderate. |
| direction | `{ dir: up|down, cause:<string> }` (from `TREND`) | Movement is **direction + cause only**, never a magnitude (D056). Needs two runs to exist. |
| false-confidence | derived: high band + low reliability (`falseConfidenceHolds`) | Neutral advisory flag naming the cause (reliability shortfall vs CAF weakness); absent when false. |

- **No 0–100 index anywhere** (D183b) — hero, chip, popover, trend, chat, reports.
- **No composite/forecast score** (D183b) — the read is an ordinal band + a grounding word, nothing more.

## Grounding (global) — the read's rollup, one home (D179e)

- Every statement OSLO extracted splits into two ratified **epistemic classes**: **From OSLO** (inferred) and **Confirmed by you** (attested). Named via `EPI_CLASSES` / `_epiLabelHTML`; the unit is the **statement** (D253).
- Rollup: "`a` of `a+d` statements Confirmed by you · `d` From OSLO · ✓ largely grounded", computed from `_progressRows()` / `_ovGroundingHTML`. This is the **single home** for the global grounded/inferred counts — they do not appear on Progress.
- `_groundedShare()` = grounded / (grounded + inferred); a read with no claims says nothing (D173). Grounding word (`_GROUNDING_WORDS`, `_groundingWord`): barely / thinly / partly / largely / well grounded. **Shares no word with the band** (D183c).

## Maturity ladder (DL-129) — computed rung, not a stored stage

`_LADDER` = **Oriented → Corroborated → Grounded → Anchored → Validated** (`_readRung`, `renderStageSeq`). Each rung is an **earned, evidence-computed** condition (never an analysis-depth default):

| Rung | Earned when |
|---|---|
| Oriented | baseline — the read rests on inference |
| Corroborated | grounded share ≥ .35 (`_isCorroborated`) |
| Grounded | grounded share ≥ .60 (`_isLargelyGrounded`) |
| Anchored | no load-bearing statement remains (`_isFullyAnchored`) |
| Validated | Anchored **and** stakeholder corroboration — an Approve in `ALIGN_EVIDENCE` (`_isValidated`) |

Monotonic-with-work; a crossing is a timestamped event, never a revocable badge.

## Execution readiness (the arc's Validate metric) — `_execReadiness()`

Computed over the **WBS · Schedule · Resources** statement subset (`_ciStatements` filtered to those documents):

| Field | Meaning |
|---|---|
| `total` | execution-critical statements |
| `confirmed` | `total − inferred` (grounded by the user) |
| `inferred` | still OSLO's draft |
| `frac` | `confirmed / total` — drives `_planStage` (≥ .5 → Improve) |
| `state` | named validation-progress: `Mostly OSLO's draft` (<.5) / `Load-bearing confirmed` (≥.5) / `Fully validated` (=1) — never a "will-succeed" verdict |

## Plan-stage (the arc's active node) — `_planStage()`

`understand` (no coverage / `DEMO_FIRSTRUN`) → `validate` (frac < .5) → `improve` (frac ≥ .5). Understand is a **first-time behavioural milestone** (left on the first confirmed detail), not a band threshold.

## Issue (the Start here / Progress unit) — INHERITED

Internal object = **Finding**; user-facing label = **Issues** (D017). `{ title, sev: critical|moderate|warning, dim, sec, status: open|addressed|resolved, ... }`. A **load-bearing de-risk** is the inferred statement whose `.sup` names the issue (`_issueDerisk` / `_ciLoadBearingStatements`). Lifecycle Open → Addressed → Resolved; **only an analysis update resolves** (D088). Beat-aware ordering by `_beatOrder`.

## Progress counts — pure work-state (`PAYOFF_COUNTS` / `_progressRows`)

Open: `issues · critical · questions`. Closed: `resolved · answered`. Computed from live state; an uncomputable count is absent (D173). **No burndown, no denominator, no target** — a rising count is a deeper read, not a regression. Grounding counts are **not** here (they live on the read, D179e).

## Plan documents ×7 (INHERITED, D035) — unchanged

Intent · Context · Scope · Requirements · Work breakdown (WBS) · Schedule · Resources. User-facing term "Documents"; the Overview reads them but does not edit them (editor is a later slice).

## localStorage keys (browser-local persistence)

- `leadLineDone` — the lead-line's spent-nudge flag (retires it for good, DL-132).
- CAF drill open/L2 state persisted on container classes (survives refresh).
- Milestone/ladder crossings recorded once (seeded silently at boot for a returning user).
- Inherited Slice 1/2 keys (phase, orientation-seen, tour-seen, account, stay-signed-in). Popover-open and demo toggles (`DEMO_FIRSTRUN`, `SHOW_FALSECONF`) are ephemeral UI state, not persisted.
