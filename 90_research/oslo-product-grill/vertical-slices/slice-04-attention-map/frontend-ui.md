# Slice 4 — Attention Map (MRI) · Frontend / UI

Single openable HTML; dark default + light theme via one semantic token set (D015). Look-and-feel inherited 1:1 from `oslo_r1_experience_mockup_v4.html`. Cumulative over Slices 1–3.

## Screens / regions touched

### Attention pane (`#pane-attention`) — deepened
- **Header:** "Attention map" · "Where the plan needs attention".
- **Bar:** lead **"Brighter = more attention — not a health score."** + info tooltip. *(Revision 3 / D063: the heat/field toggle was removed — the map now shows only the heatmap, so no toggle bar remains.)*
- **`.heatwrap`** contains:
  - **`#heatGrid`** — the heatmap (rendered by `renderHeat()`).
  - **`#heatClear`** — the all-clear state (`.heat-clear`, shown via `.show`).
  - **`#heatLegend`** — Calm → Needs attention swatches + axis note + "Brighter = more attention — not a health score."

### Heatmap cells (`.heat-cell`)
- `.l0` neutral/inert (no hover scale — overridden), `.l1` amber-light, `.l2` amber-mid, `.l3` red + glow (v4 values 1:1).
- Content: count + `.mini` severity label; `.multi` pip (top-right) when >1 open issue.
- Live cells: `role=button`, `tabindex=0`, `onkeydown` Enter/Space → route; `l0` cells carry none of these (inert).
- Row headers `.heat-rowh.hart` are clickable/focusable (open the artifact's issues).

### Field / Dimensions view — REMOVED (Revision 3, owner decision D063)
- The secondary "field"/Dimensions view (`#dimGrid` / `.dimwrap` / `.dimcard`, `renderDims()`) and the heat/field toggle (`.mfilter`, `#mfHeat` / `#mfDim`, `mview()` / `MVIEW`) were removed — the map now has only the heatmap. Associated CSS and the `openFindingsDim()` router were removed with it. The all-clear state is now driven solely by `heatModel().openTotal`.

### Scoped Issues list (`#scopedScrim` / `.scopedpanel`) — NEW seam
- Slides from the right (same pattern as the issue panel).
- `.sp-top` title + close; `.sp-sub` count; **`.sp-filters`** with **`.sp-chip.lit`** chips (one per active filter, each with a removable `×`); **`.sp-seam`** dashed note ("full Issues surface arrives in Slice 6"); `.sp-list` of `.sp-card` rows (severity chip + title + location + `›`).

### Overview pointer (D062)
- The Confidence-card footer link is now **"Attention map →"** (`showView('attention')`), keyboard-activatable — the Overview's Attention pointer. No other Attention content added to the Overview (kept lean per D046).

### Confidence-card link row (Revision 2)
- Row order: **Why ▾** · **Timeline →** · **Attention map →**. "Timeline →" (`openHistorySeam()`) opens the **History & timeline** Slice-7 seam (`#historyScrim`, centered scrim) — a labeled stub, NOT the heatmap. "Attention map →" stays the separate co-primary pointer.
- **`#howcalc`** ("How this is calculated") now sits **directly under the `#ov-idx` number**; its native `title` was removed so only the custom `.howcalc-pop` shows (no double tooltip).
- **`#ov-stage` / `#cpp-stage`** stage markers now carry a visible **`.info` ⓘ** explaining Orientation → Expanded → Validated and which stage is current. Popover ⓘ tip is right-anchored so it never runs offscreen.
- **`.caftip`** (CAF dimension detail) now opens only on **`.cn` hover** (the dimension word, `cursor:help`) via `.cafrow .cn:hover ~ .caftip`, not on row-wide hover; row click-to-navigate is unchanged.

### History & timeline seam (`#historyScrim`) — NEW Slice-7 seam
- Centered scrim (reuses the `#orient` overlay pattern); labeled **"History & timeline — arrives in Slice 7"**. Opened by the Timeline link; closed by scrim click or "Got it". `openHistorySeam()` / `closeHistorySeam()`.

## Color discipline (D003/D060)
- **Severity ramp (red/amber) only on `.heat-cell` `l1`–`l3` and issue/scoped severity chips.**
- Confidence pill, CAF bars, reliability bars → **neutral maturity ramp** (`--conf-low/medium/high`). Never health-colored.

## Accessibility (D015)
- All live cells, row headers, scoped rows: focusable + Enter/Space activation + visible focus ring (`:focus-visible`).
- `l0` empty cells removed from the tab order (inert).
- Scoped panel + issue panel are `role=dialog aria-modal`.
- Reduced-motion respected (inherited global rule); hover scale is a transform only.

## Phase-bar demo triggers (scaffolding, not product chrome)
- Inherited: "Sim false-confidence" (D052), "Sim Extended-Analysis fail" (D041).
- **NEW: "Sim all-clear"** (`#allClearBtn`, `toggleAllClear()`) — resolves/restores all open issues to reach the map all-clear (D061).

## Files
- `prototype.html` — the cumulative Slice 1–4 build. JS: `_cellFor`, `heatModel`, `renderHeat`, `openFindingsFor`/`openFindingsForArtifact`, `openScopedIssues`/`renderScoped`/`closeScoped`/`clearScopeFilter`/`openIssueFromScope`, `toggleAllClear`, scroll-memory in `showView`. **Revision 2:** `showView('attention')` re-renders the heatmap + issue counts on entry (live cell counts); `openHistorySeam()`/`closeHistorySeam()` for the Slice-7 History seam. **Revision 3 (D063):** removed `renderDims`/`mview`/`MVIEW`/`openFindingsDim` and the field view; `renderHeat` no longer branches on `MVIEW` — the heatmap always renders and the all-clear is driven only by `heatModel().openTotal`.
