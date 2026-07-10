# Slice 4 — Attention Map (MRI) · Worker Report

**Workflow:** oslo-product-grill · **Release:** OSLO R1 (ALPHA) · **Date:** 2026-07-09
**Cumulative:** Slice 1 + Slice 2 + Slice 3 + **Slice 4** (started from the signed-off Slice-3 prototype and extended).

## Files created (host paths)
`.../oslo-product-output/vertical-slices/slice-04-attention-map/`
- `prototype.html` — cumulative Slices 1–4 (base = Slice-3 copy, extended)
- `user-experience.md` (INHERITED vs NEW)
- `product-detail.md`
- `product-data.md` (AttentionCell, HeatModel, FieldModel, Scope, view-context; no DB)
- `workflow.md`
- `frontend-ui.md`
- `success-criteria.md`
- `e2e-test-scenarios.md` (20 scenarios)
- `.../worker-reports/slice-04-report.md` (this file)

## What's NEW vs Slice 3 (D057–D062)
- **D057 — Heatmap primary:** deepened the Slice-2 heatmap. Rows = 7 plan artifacts × columns = Clarity · Alignment · Feasibility; cells shaded by attention severity (l0→l3, brighter = more attention); each non-empty cell shows the open-issue count + a mini severity label; multi-issue cells carry a "multiple" pip. Legend now reads **"Brighter = more attention — not a health score."** Corner label switched to "Plan artifact ↓".
- **D058 — Cell → Issues routing:** real `openFindingsFor(artifact, dimension)` — exactly one open issue opens THAT issue (light issue panel); more than one opens a **scoped Issues list with both filters visibly lit** (removable chips) + a dashed Slice-6 seam note. Row headers and field cards route too. `openCell`/`showSectionIssues` kept as aliases (no Slice-2/3 caller breaks).
- **D059 — Field view:** the "Dimensions" toggle became a light secondary **Field** view (heat primary / field secondary), with per-dimension open counts and routing pointers.
- **D060 — Severity-only coloring:** verified the red/amber ramp lives only on attention cells; confidence, CAF, reliability, and field-view levels stay neutral. Empty l0 cells no longer hover-scale.
- **D061 — Empty/all-clear:** l0 cells are neutral and **inert** (no role/tabindex/onclick). Added a map-wide all-clear state + a "Sim all-clear" phase-bar trigger to reach it (and restore).
- **D062 — Co-primary + context:** Attention reachable from the top-center switch AND a new Overview **"Attention map →"** pointer (replaced the dead "Timeline →" link). `showView()` now remembers/restores each pane's scroll — returning preserves prior context.

## Verification
- **`node --check`** on the extracted `<script>`: **PASS** (no JS error).
- Routing model checked against the fake issue set: one multi cell **Resources × Feasibility** (ISS-01 critical + ISS-03 moderate) → scoped list; four single cells (Requirements×Clarity, Schedule×Feasibility, WBS×Alignment, Context×Clarity) → issue panel; remaining 16 cells inert l0.
- Wiring presence check: openFindingsFor, openScopedIssues/renderScoped, heatModel, toggleAllClear, scroll memory, field render, scoped/all-clear markup, Overview pointer, multi pip, inert l0 — all present.
- No regression to Slice 1–3 surfaces (confidence pill/popover, false-confidence flag, clarification loop, tour, chat, "Plan artifacts" term, "Strengthened" trend label all preserved).

## Boundaries respected
- No Slice 5 artifact editor; no full Slice 6 Issues surface (only the scoped seam + lit filters). Overview kept lean (only the pointer added).

## Flags / spec gaps
- **None invented.** All new data is derived over the existing illustrative issue set. The multi-issue demo cell (Resources × Feasibility) reuses the Slice-2 fake issues — no fabricated severities. No open-TBD values were assumed.

## Revision 2 (2026-07-09)

Five owner-directed feedback fixes applied to `prototype.html` (edited in place; no other behavior regressed). `node --check` on the extracted `<script>` passes.

1. **Stale heatmap count / wrong routing (bug).** `showView('attention')` now calls `renderHeat(); renderDims(); updateIssueCounts();` on entry so displayed cell counts are always live and agree with `openFindingsFor` routing. Both `_istatus` mutation sites (`answerClarification`, `toggleAllClear`) already re-rendered the map + dims + counts; no other status-change sites exist (the issue-panel lifecycle is display-only). Resolving one of two issues in a cell now yields "1" + single-issue open on return.
2. **Timeline → History seam.** Added a **"Timeline →"** link (`openHistorySeam()`) to the Confidence-card link row (Why · Timeline → · Attention map →). It opens a new centered Slice-7 seam (`#historyScrim`, "History & timeline — arrives in Slice 7"), reusing the `#orient` overlay pattern — **not** the heatmap. No other timeline-implying element routed to `showView('attention')`.
3. **"How this is calculated" double tooltip + placement.** Removed the native `title` from `#howcalc` (custom `.howcalc-pop` kept). Moved the chip to sit **directly under the `#ov-idx` number**.
4. **Stage context.** Added a visible `.info` ⓘ next to the Stage marker on the Overview (`#ov-stage`) and in the popover (`#cpp-stage`), explaining Orientation → Expanded → Validated and which stage is current. Popover ⓘ tooltip right-anchored to avoid offscreen overflow.
5. **CAF hover scope.** Changed `.caftip` trigger from `.cafrow:hover` to `.cafrow .cn:hover ~ .caftip`; added `.cn{cursor:help}`. Tip now opens only on the dimension word; row click-to-navigate unchanged.

**Left alone (owner discussing separately):** the "not project health / readiness / probability" sentence and the "Clarification request" / "Confirmed by you" wording — untouched.

## Revision 3 (2026-07-09)

**Owner decision D063 — remove the secondary Field / Dimensions view from the Attention map.** The heat/field toggle wasn't helpful; the map should carry only the heatmap. Edited `prototype.html` in place; the heatmap and all other Slice 1–4 behavior are preserved.

Removed (reverses D059):
- **Toggle bar** — the `.mfilter` block with `#mfHeat` ("▦ Heatmap") and `#mfDim` ("⌖ Field"), including its `role="tab"` / `aria-selected` semantics. With one view, no toggle is needed.
- **Field/Dimensions pane** — `#dimGrid` / `.dimwrap` markup and all field-only CSS (`.mfilter`, `.mf`, `.dimwrap`, `.dimcard`, `.dimbar`, `.fieldlead`, etc.).
- **JS** — the `renderDims()` function, the `mview()` toggle function, the `MVIEW` variable, and the now-orphaned `openFindingsDim()` router. All `renderDims()` calls removed from init, `showView('attention')`, the post-resolution re-render batch, `toggleAllClear()`, and `deepComplete()`. The `mview('heat')` call in `toggleAllClear()` was removed.
- **`renderHeat()` simplified** — no longer branches on `MVIEW`. The grid always renders; visibility and the `#heatClear` all-clear are now driven solely by `heatModel().openTotal===0` (D061 unchanged in behavior).

Kept / verified:
- Heatmap (`#heatGrid` / `renderHeat`) still renders on load and on `showView('attention')`.
- All-clear empty state (`#heatClear`) still reachable via the "Sim all-clear" trigger, now driven by total open issues rather than `MVIEW`.
- Legend and all other surfaces intact. No other slices touched.

**Verification:** `node --check` on the extracted `<script>` **PASS**. Grep confirms **no remaining** `renderDims`, `mview(`, `MVIEW`, `#mfDim`/`#mfHeat`, `#dimGrid`, `.dimwrap`, `openFindingsDim`, or Field/Dimensions toggle references. The D059 header-comment entry is annotated as removed per D063. Docs updated: `frontend-ui.md` and `user-experience.md` note the D063 removal.
