# Slice 3 — Project Overview & Understanding Console · Frontend / UI

Single openable HTML; dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables. Colour discipline: the arc/read use only the cool `--maturity` accent; **severity red/amber/green appears only on issues** (D003); no percentage fills, no health bars.

> Regenerated to the frozen build (md5 `a327d702`). The Overview hero is the **journey arc above the persistent Outcome Confidence read** — not a "Confidence" card with a 0–100 index. The retired index, "How this is calculated" pill, stage marker (Orientation/Expanded/Validated), and standing Project-summary panel are gone.

## Overview layout (top to bottom)

`<div class="card hero">` contains, in order:
1. `#ov-arc` — the journey arc (written by `renderHeroArc()`).
2. `.ch-nest` (tab "The read") — the persistent Outcome Confidence read, nested below the arc.
Then, as sibling cards below the hero:
3. `#ovStartHere` — Start here (beat-aware guidance).
4. `#ovProgress` — Progress (pure work-state + the maturity ladder rung).

The relative order of `#ovStartHere` and `#ovProgress` is **computed** (`_orderOverview` / `renderProgress`) — first-run → Start here first; after first value → Progress first.

## The journey arc — `#ov-arc`

| Element | Selector / class | Notes |
|---|---|---|
| Frame label | `.ovj-lab` | "Your plan, on the way to the outcome" |
| Track | `.ovj-track` | four `.ovj-stage` nodes |
| Node dot | `.ovj-dot` | `.now` → filled `--maturity` with soft ring; `.done` → `✓`; `.dest` → dashed square with `↗` |
| Node name / meta | `.ovj-name` / `.ovj-meta` | Understand · Validate ("N of M") · Improve (band) · Execute ("to Asana · anytime") |
| Optimize bracket | `.ovj-brk` / `.ovj-brk-lab` | spans nodes 2–3 (25%–75%), label "Optimize" |
| Active spine | `.ovj-drop` | the active node drops a 2px `--maturity` spine toward the read |
| Beat body | `.ovj-body` (`.ovj-act` link) | per-beat intent + "Review & execute →" / "Execute whenever →" |

**Guard `_assertHeroArcIsHonest()`** — 4 nodes; exactly one `.ovj-stage.now` equal to `_planStage()`; the `.dest` node is Execute, never `.now`; no forecast/health words in the arc text.

## The persistent read — `.ch-nest`

| Element | Selector / id | Decision | Notes |
|---|---|---|---|
| Inset + tab | `.ch-nest` / `.dtab` "The read" | D179a | left border `--maturity`; always visible; guard `_assertUnderstandDetailIsNested` |
| Heading + info | `.ch h3` "Outcome Confidence" + `.info` | D199 | ⓘ carries the method essence |
| State chip | `#ustate` (`.ustate prov` / `.cur`) | D175/D040 | **neutral** — Provisional (hollow dot/muted/600) → Current (filled/--text/700); `error` → "Last-good" |
| Lead-line | `#ov-leadline` (`.lead-line`) | DL-132 | `_leadLineHTML()`; sunsets after first engagement; no number (guard `_assertLeadLineIsASynthesisNotAScore`) |
| Maturity ramp | `#ov-ramp` (`.ramp`) | D174/D003 | five ordinal steps `_BANDORD`; lit+named current; **no fill, no health colour**; band move = prev ghosted → current lit + arrow |
| Limiter | `#ov-limit` (`.cr-limit`) | D186c | lowest CAF + grounding-aware verb; **never "Blocker"** |
| Payoff | `#payoff` (`.payoff`, `#pay-act`/`#pay-note`/`#pay-x`) | D179b/c | dismissible "What changed", ≤20 words, no counts; `dismissPayoff()` |
| Card false-conf flag | `#ov-flag` (`.card-flag`) | D052 | neutral; `.on` when it holds; mirrors the popover |
| CAF rows | `#cg-clar` / `#cg-align` / `#cg-feas` (`.cafrow`) | Option C | caret + name + `.ramp.mini` + `.cafband` level + `.caf-ev` evidence cue + `.cafmark` "the limit"; click toggles `.cafdrill` |
| Grounding rollup | `#ov-grounding` (`.caf-ground`) | D179e | one home for global grounded/inferred; "✓ largely grounded" marker when live |
| Trend chip | `#ov-trend` / `#ov-trend-lab` / `#ov-trend-svg` | D056 | direction + word only; routes to History; shown **only when the read moved** |
| Why box | `#whybox` / `#why-band` / `#why-caf` / `#why-rel` | D046/D051 | reliability basis in prose + "✦ Ask OSLO a follow-up →"; **no separate reliability card** |

## Start here — `#ovStartHere`

| Element | Selector / class | Notes |
|---|---|---|
| Heading | `.ch h3` "Start here" + `.info` | advisory; the calls stay yours |
| Focus list | `#focus` (`renderFocus()`) | beat-aware order (`_beatOrder`) |
| Beat intent | `.focus-beat` | one line: Validate / Improve / Understand variant; no tally |
| Lead issue | `.focus-lead` (`.fl-head` / `.fl-derisk` "✦ Confirm first" / `.fl-btn` Confirm → / `.fl-review` Review the issue →) | `startInlineConfirm` inline attest; `openIssue` review |
| Secondary items | `.focus-item` (`.fi-drh` de-risk hint) | up to three; jump to `openIssue` |
| Standalone confirm | `.focus-cfm` (`.fl-cfm-go` "Confirm on the map →") | `showView('inference')` |
| Resolved | `.focus-item.resolved` | ✓, last |
| Clarification pointer | `#clarPrompt` (`.clar-prompt`) | pointer, not a tally (D179e) |

**Guard `_assertStartHereFollowsTheBeat()`** — on Improve the lead is on the limiter dimension (if any open issue is); on Validate the lead has a load-bearing de-risk (if any open issue does).

## Progress — `#ovProgress`

| Element | Selector / id | Notes |
|---|---|---|
| Counts | `#pg-counts` (`.pgx`, `_progressHTML`) | Open (issues · critical · questions) / Closed (resolved · answered); `.pgx-workonly` — **no burndown, no target** |
| Since-line | `#pg-since` | shown only when a delta exists; "Timeline →" |
| Ladder rung | `renderStageSeq(_readRung())` | "Grounded · 3 of 5" over Oriented → Corroborated → Grounded → Anchored → Validated |

## Top-bar chip + popover

| Element | Selector / id | Decision | Notes |
|---|---|---|---|
| Chip | `#confpill` (`.conf-pill`) | D050 | label "Outcome Confidence" + `#cp-band` band + `#cp-grd` ladder rung; **no 0–100 index**; DL-130 cut the grounding word; `.flagdot` + `.cpchev`; `aria-haspopup="dialog"` |
| Popover | `#confpop` (`.confpop`) | D050 | `role="dialog"`; `toggleConfPop` / outside-click closes |
| Band line | `.cpp-band` / `#cpp-bandword` / `#cpp-grdword` | D183c | band + grounding word |
| Stage seq | `#cpp-stage` / `#cpp-stage-seq` | DL-129 | the ladder rung marker + ⓘ naming the five rungs |
| CAF (popover) | `#cpp-clar` / `#cpp-align` / `#cpp-feas` (`.cpp-d`) | D176b | bands on the same ramp; limiter marked |
| Limiter note | `#cpp-limnote` | D186c | ≤8 words, verb |
| Way out | `#cpp-out` (`cppWayOut`) | D185.3d | opens limiter's top issue or full breakdown |
| Reliability basis | `#cpp-cov` / `#cpp-evd` / `#cpp-asr`, `#cpp-thin`, `#cpp-basis-all` | D051 | Coverage · Evidence · How assessable (High/Mod/Low); weakest resident, all three on demand |
| Trust-check | `#cpp-thin` (`.rel-sound` / `.rel-gap`) | — | "✓ Sound basis" calm / "Read this with care" loud; never celebrated |
| Popover false-conf flag | `#cpp-flag` (`.cflag`) | D052 | neutral; `.on` when it holds |

## Color discipline (D003)

Arc, read, ramp, CAF, grounding, ladder, and the false-confidence flag use the **neutral / `--maturity`** palette — **no percentage fill, no health bar, no RAG.** Severity red/amber/green stays on issue badges only. The single earned colour (`--earned`) marks a user-driven rising count / a met milestone, never severity.

## Accessibility

- Chip: `aria-haspopup="dialog"`, `aria-expanded` toggled; popover `role="dialog"` with keyboard-reachable controls.
- CAF rows / arc links / payoff dismiss / trend chip / confirm buttons: `role="button"`, `tabindex="0"`, Enter/Space handlers.
- Ramp: `role="img"` with an ordinal ARIA label ("Step N of 5 …").
- Focus-visible rings and reduced-motion inherited (no analysis animation under reduced-motion); colour is never the sole signal (the false-confidence flag is text, not colour).

## App shell (inherited)

Persistent left sidebar (Overview live · Issues · History · Inference map · Reports · Documents subgroups · Full plan), top bar (brand · project switcher w/ summary hovercard · sample tag · breadcrumb · the Outcome Confidence chip · search/share/export/report/Free chip), command palette (⌘/Ctrl+K), chat rail. Nav chrome neutral; badges neutral. The standing Project-summary panel is retired into the project-name hovercard (`#projSummaryPop`).
