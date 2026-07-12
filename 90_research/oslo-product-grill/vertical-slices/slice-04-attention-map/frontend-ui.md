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

## Revision 4 (2026-07-09, shell cascade D095) — persistent app shell ported from Slice 6

The Slice-6 approved app shell (**D093 persistent left sidebar + D094 command palette + top-bar chrome**) was ported in place. The old top-center **`.vswitch`** view switch (Overview · Attention) is **removed**; all its CSS/markup/JS references are gone.

- **App grid (D093):** `#app` is now a 3-column grid — `240px sidebar | 1fr main | 340px chat` (`#app.chat-collapsed` drops the chat column). Phase-bar offset kept via `margin-top:38px; height:calc(100vh - 38px)`. `.body` → `grid-column:2`, `.chatp` → `grid-column:3`.
- **Persistent sidebar (`#appSidebar`):** **PROJECT** group — **Overview** (live), **Issues** (badge; opens the Slice-6 seam), **History** (opens the Slice-7 seam), **Attention map** (live). Neutral nav chrome; `.sb-badge` counts are neutral (never severity). Pinned footer: bordered **Take a quick tour** (`#railTour`, moved out of the old floating rail), **Free plan** tier chip + Upgrade, **Your account** row (`#acctBtn`, opens the account menu). **The PLAN ARTIFACTS sidebar section is intentionally OMITTED** in Slice 4 — the artifact editor arrives in Slice 5 (no broken artifact links).
- **Top bar:** Intralign brand · project switcher (`#tbProj`, holds `#projName`, Slice-8 seam) · `sample` tag · breadcrumb (`#tbCrumb`, reflects the current view) · confidence pill (unchanged) · search `⌕` (`#tbSearch`) · Share/Export (`#tbShare`/`#tbExport`, Slice-9 seams) · report (`#tbReport`) · **Free** plan chip. Narrow-width `☰` (`#sbHamburger`) opens the sidebar drawer.
- **Command palette (D094, `#palScrim`):** centered modal; **GO TO** (Overview/Attention live; Issues/History → labeled seams) + **OPEN AN ISSUE** (each open issue → the light issue panel). **The PLAN ARTIFACTS palette group is OMITTED** in Slice 4. Opens from `⌕` and **⌘/Ctrl+K**; full keyboard nav (↑↓/↵/esc), neutral active-row tint. `_syncNav()` is the single source of truth for the sidebar active highlight + `aria-current`.
- **Seams (labeled stubs, never a wrong view):** `#issuesSeamScrim` — "Full Issues view arrives in Slice 6" (offers "Open the Attention map →"); `#historyScrim` (inherited) — Slice-7. Icon-button/tier seams use `_stubToast()` (`#sbToast`).
- **Responsive:** `@media(max-width:860px)` collapses the sidebar to an overlay drawer (`.sb-scrim`, `toggleSidebar`/`closeSidebar`, auto-close on pick); `@media(max-width:760px)` collapses the chat rail.
- **Preserved:** Attention heatmap, Overview, confidence pill/popover, account menu, tour, chat rail, clarification loop, all Slice 1–4 behavior. `showView()` now drives the sidebar/breadcrumb instead of `.vswitch`.

## Chat integration (D108 cascade)

The persistent OSLO rail is now a **working, state-grounded conversation** in Slice 4 — the composer and Send were inert before. Ported from the D108 implementation and scoped to the surfaces that exist here (the confidence-led Overview, the Attention map, the light issue panel, the clarification loop). No artifact editor (Slice 5), no full Issues/recommendations surface (Slice 6), no History (Slice 7) is offered by the chat.

**Composer.** `#chatInput` + `#chatSend` → `sendChat()`; `chatKey(event)` sends on **Enter**, newline on **Shift+Enter**. The user turn renders via `pushUserChat()` (escaped, `.cmsg.user`); OSLO replies via the existing `pushChat()`. `#chatscroll` is `role="log" aria-live="polite" aria-relevant="additions"`; a first-run `.chat-empty` block (`#chatEmpty`) is dropped by `_chatDropEmpty()` on the first message.

**Grounding.** `_chatState()` reads the LIVE model only — `currentRead()` (index · band · reliability basis · `ANALYSIS_STATE`), `ISSUES`/`_istatus`, the CAF rows (`_chatCaf`, whose Feasibility tracks the live reading), the limiting dimension, and `heatModel()` (lit cells, per-dimension totals, brightest cell). No invented numbers, no invented issues. `_oslloReply()` is prototype-grade keyword routing into the `_ans*` builders: `_ansConfidence` · `_ansNext` · `_ansIssue` · `_ansDimension` · `_ansAttention` · **`_ansCell`** · `_ansArtifact` · `_ansHowIssuesClose` · `_ansClarifications` · `_ansSummary`.

**Context handoff + pill.** `askOslo(ctx)` is the one shared entry point: it stands down the issue/scoped overlays, un-collapses the rail, sets `_chatCtx`, paints the `#chatCtx` pill (`Context · <value>`, with a `×` → `clearChatContext()`), and pushes a grounded opening built from live state. Inside an active context, unrouted follow-ups are answered **within** that context until it is cleared.

**Entry points (Slice-4 surfaces only).**
- **Overview → confidence:** `#askWhy` ("✦ Ask OSLO why", `.howcalc.askwhy` under the number) → `askOslo({type:'confidence'})`.
- **Attention map → cell (signature):** each non-`l0` heat cell carries a quiet `.cellask` ✦ button (`event.stopPropagation()` so it never fires the cell's own routing) → `askOslo({type:'cell', art, dim})`. The **scoped-issues header** (where a multi-issue cell routes) carries `.sp-ask` "✦ Ask OSLO about this cell" for the same context; when only the artifact filter is set it hands `{type:'artifact'}`. The pill reads **`Context · <Artifact> × <Dimension> · Attention map`**, and `_ansCell()` explains what that artifact×dimension bucket means, what's driving its brightness (most-severe issue wins the cell color), the other issues in the cell, and how it weighs against the limiting dimension.
- **Light issue panel:** `.ip-ask` "✦ Ask OSLO about this issue" → `askOslo({type:'issue', id})`.

**Advisory-only (D001).** The chat never mutates: every action it offers is a `.chat-act` button that calls an **existing** Slice-4 function — `openIssue()` · `openFindingsFor()` · `openFindingsForArtifact()` · `showView()` · `askOslo()`. It never closes an issue; it states that an issue closes only when an analysis update confirms the gap is gone.

**Clarifications — one path.** `answerClarification()` (panel) and `answerClarificationFromChat()` (the `.chat-clar` block raised inline in a reply) both call the shared **`_submitClarification(id, val, src)`**: same project-info update (tied artifact → `attested`, reliability step-up), same issue close, same surface refresh (`renderOverview`/`renderFocus`/`renderClarifications`/`renderPlanSections`/`renderHeat`/`updateIssueCounts`/`renderScoped`). `src` only decides which surface reports back — the panel shows its "Re-analyzing…" state and re-opens resolved; the chat posts an acknowledgement then an "Analysis update complete" notice. No side channel.

**Chips.** `renderChatChips()` paints state-derived `.chat-chip` suggestions above the composer (context-aware: issue / cell / artifact / confidence, else read-derived — "Why is Feasibility Very Low?", "Explain the top issue", "What needs the most attention?"). Rebuilt on `seedChat()`, `askOslo()`, `sendChat()`, `updateIssueCounts()` and `deepComplete()`.

**Preserved:** the heatmap and its `l0` inert cells, cell → `openFindingsFor` routing (1 issue → issue panel; >1 → scoped list with both filters lit), the all-clear state, the tour, the existing `pushChat()` completion notices (Fast Pass / Extended Analysis / failure + retry), and every Slice 1–4 behavior. Chat chrome is **neutral** (D003) — severity color stays on cells and issues only.
