# Slice 7 — History & Confidence Trend · Worker Report

**Status:** Complete. Cumulative Slices 1–7 built by extending the signed-off Slice-6 prototype 1:1 (copied from `slice-06-issues-recommendations/prototype.html`).

## Files created
In `oslo-product-output/vertical-slices/slice-07-history-trend/`:
- `prototype.html` (cumulative Slices 1–7; copied from Slice 6 and extended — 5324 lines)
- `user-experience.md` (INHERITED vs NEW)
- `product-detail.md`
- `product-data.md` (HistoryEvent + TrendPoint schemas; append-only rules; localStorage; no DB)
- `workflow.md`
- `frontend-ui.md`
- `success-criteria.md`
- `e2e-test-scenarios.md` (20 scenarios)
- This report: `oslo-product-output/worker-reports/slice-07-report.md`

## What's new vs Slice 6

**The Slice-6 History seam is replaced by the real History & timeline surface + an "Understanding over runs" confidence trend.**

- **D096 — Append-only History timeline.** `#pane-history` now holds `.hist-pane` → header + `#hist-trend` (trend) + `#hist-list` (events) + `#hist-first` (first-run) + read-only note. Model = `HISTORY[]`, **append-only** (`unshift` newest-first, never mutated/removed). Rows show icon + label + optional detail + illustrative timestamp + **current/prior** tag. Event types: `analysis_run`, `reanalysis_run`, `artifact_version`, `issue_lifecycle`, `selected_path`, `clarification`, `last_good`. It **grows live**: wired into `deepComplete` (Extended run + 7 retained v1 versions + 6 detected issues, once via `_deepHistDone`), `applyFix` (applied path + version bump + Resolved), `answerClarification` (answered + Resolved), `selectPath` (path selected), and `commitArtEdit` (artifact vN). `showView('history')` renders both surfaces on entry; `openHistorySeam()` **re-pointed** from the seam modal to the real pane, so the Overview "Timeline →" and Issue-panel "Open full timeline →" pointers land here (and the "(Slice 7)" tail is removed).
- **D097 — "Understanding over runs" trend.** `renderHistTrend()` draws a **neutral** sparkline (`var(--conf-medium)`, never severity color) at the top of the pane. `TREND[]` points are **band-qualified** (5-band) + **cause-bound** (SVG `<title>` + caption). The line **rises OR falls** (▲/▼ direction-only, no fabricated magnitude in UI; illustrative index in code only); the ⓘ hover says a fall usually means deeper analysis found something real. The Overview `#ov-trend` quiet row is **kept** unchanged.
- **D098g — Last-good + read-only.** Foot note "Read-only · viewing history changes nothing" (+ ⓘ). No render/view path mutates any assessment; re-visiting is stable. `deepFail()` appends a `last_good` row and leaves the trend/read untouched.
- **D099 — Version lineage.** `artifact_version` rows are `.hrow.clickable` with a "view snapshot →" affordance → `histVersionNote()` → a **read-only toast** (reusing `_stubToast`). Keyboard-operable (focusable, Enter/Space). Prototype-grade labeled read-only view (no full diff).
- **D100 — First-run minimal state.** `#hist-first` ("Your history starts here … More appears as your plan evolves") shows while only the Initial Analysis exists (`HISTORY.length ≤ 1 && TREND.length ≤ 1`), then yields to the full timeline.

New JS: `HISTORY`, `TREND`, `_hEventSeq`, `_histicon`, `_deepHistDone`, `pushHistory`, `pushTrend`, `renderHistory`, `renderHistTrend`, `histVersionNote`. New CSS: `.hist-pane/.hist-head/.hist-sub/.hist-trend/.ct-h/.ct-x/.hrow(.clickable)/.hicon/.hbody/.hlab/.hd/.ht/.hview/.hstate(.cur)/.hist-first/.hist-ro` (v4-matched). Sidebar `#sbHistory` title updated off "arrives in Slice 7". The retired `#historyScrim` modal + `.hist-seam*` CSS remain inert (no regression).

## Boundaries honored
Advisory-only; **"analysis update"/"analysis run"**, never "reanalysis" (D092); "Issues" not "Findings"; Clarity·Alignment·Feasibility; From OSLO / Confirmed by you; 5-band scale; **severity color only on issue severity** — the trend line and all History chrome are neutral maturity. Dark default + WCAG 2.1 AA (keyboard-navigable timeline, focusable version rows, ⓘ single-home honesty). **Threaded comments left as a Slice-9 seam** — History reflects lifecycle/analysis/version/clarification events only.

## Verification
- **`node --check`** on the extracted inline script: **PASS**.
- **jsdom structural parse (no runScripts):** `body.children.length = 16`; `#pane-history` holds the **real** timeline (`.hist-pane`, no `.hist-seam` child); `#hist-list`, `#hist-trend`, `#hist-first` present; sidebar History title no longer says "Slice 7".
- **jsdom runtime (runScripts):** **0 console errors** on boot and through the flow. Verified: History nav opens the real pane (active); trend renders with a polyline and "Understanding over runs" title; first-run minimal state visible (1 seed row); `deepComplete` grows the timeline (1→4 rows) and the trend (rise), hiding the first-run card; current + prior labels present; a clickable version row exists; `applyFix` appends events (4→6); `answerClarification` appends (6→7); a version click yields a read-only toast; the read-only note is present; all prior panes (`pane-overview/attention/issues/artifacts`) and the Overview `#ov-trend` remain; navigating away and back leaves the row set unchanged (read-only).

## Flags / notes
- Illustrative timestamps ("now − 2m", "just now") and trend indices are in code only (direction-only in UI, per D056) — real timestamps/magnitudes remain owner-TBD.
- Version lineage is prototype-grade (a labeled read-only toast note), not a full diff/restore (D099 scope).
- `openHistorySeam()` kept its name (many call sites) but now routes to the real pane; the `#historyScrim` modal is dead code left in place to avoid touching unrelated markup.

## Revision 1 (2026-07-09)
Initial Slice-7 delivery. Replaced the `#pane-history` seam with the real append-only History & timeline (current/prior labels + illustrative timestamps) and the neutral "Understanding over runs" trend (rise/fall, band-qualified, cause-bound); wired live appends across `deepComplete`/`deepFail`/`applyFix`/`answerClarification`/`selectPath`/`commitArtEdit`; added version-lineage read-only toast (D099) and first-run minimal state (D100); re-pointed the Overview/Issue-panel timeline pointers to the real pane. `frontend-ui.md` and `user-experience.md` document INHERITED vs NEW. Build verified: `node --check` PASS; jsdom structural parse + runtime smoke pass with 0 console errors.

## Revision 2 (2026-07-09, D101 refinements)
History gap-analysis refinements, edited in place. **All prior Slice-7 behavior, live-append wiring, and Slices 1–6 preserved; append-only + read-only + last-good honesty unchanged.**

- **1 — enum leak removed.** `renderHistory()` no longer prints the internal `type` string in monospace. New `_histCatLabel{}` maps `type` → a human category label (Analysis run / Version / Issue update / Your decision) on each row + group header. (jsdom confirms no `analysis_run`/`issue_lifecycle`/… text in the rendered timeline; enums live only in code.)
- **2 — grouped by analysis run + day, collapsible.** `_histGroups()` clusters the append-only log by run (newest first); each `.hgroup` is a collapsible header (`toggleHistGroup`/`_histCollapsed`) with a Today/Yesterday day marker (`_histDay`). Nested child events sit in a `role="list"`.
- **3 — per-run "what changed" delta.** `_runDelta()` renders chips: N opened / M resolved (M counted live from child Resolved rows), CAF band moves, stage change (→ Expanded), confidence direction ▲/▼ (direction-only, D056). Hints carried via extended `pushHistory(...,{run,delta})`.
- **4 — trend ↔ timeline link.** Trend circles + captions (`.hf-point`, keyboard-operable) call `histFocusRun()` → scroll-to + `.flash` highlight of the run group (headerless points fall back to newest). Each group shows its confidence band (`_bandFor`). Trend stays neutral; hover meaning unchanged.
- **5 — filter chips.** `.hist-filter` bar (All · Analysis · Issues · Versions · Your decisions) as keyboard `<button aria-pressed>` reusing Issues `.ff` styling; `setHistFilter()` filters + writes honest `#hist-hidden` "N hidden · show all".
- **Polish.** Hover `title=_absTime(ts)` absolute timestamps; only the newest run marked *current* (others *history*, per-event tags dropped); list a11y `role=list`/`listitem` with version rows still `role=button` keyboard-operable.

**Prototype caveats:** timestamps/band-moves/opened/direction/indices are illustrative (direction-only, not canon); "After your fix"/"After your answer" trend points have no dedicated run header so they focus the newest group; `opened` is per-run, so Initial and Extended each read "6 opened".

**Verification:** `node --check` PASS. jsdom structural parse — `body.children.length = 16`, `#pane-history` present, **no** raw enum in rendered timeline, 5 filter chips. jsdom runtime — first-run minimal state intact; after Extended run: 2 run groups, newest = current (exactly 1 current badge), per-run delta + band shown; filter chips filter with honest hidden count; trend-point click flashes its group; apply-fix appends Resolved + version snapshot into the newest group and grows its resolved count to 1; version rows read-only + keyboard-operable; `role=list`/`listitem` present — **0 console errors**.
