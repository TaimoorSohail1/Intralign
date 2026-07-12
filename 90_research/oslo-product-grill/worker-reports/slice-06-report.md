# Slice 6 — Issues & Recommendations (Panel Model) · Worker Report

**Status:** Complete. Cumulative Slices 1–6 built by extending the signed-off Slice-5 prototype 1:1.

## Files created
In `oslo-product-output/vertical-slices/slice-06-issues-recommendations/`:
- `prototype.html` (cumulative Slices 1–6; copied from Slice 5 and extended)
- `user-experience.md` (INHERITED vs NEW)
- `product-detail.md`
- `product-data.md`
- `workflow.md`
- `frontend-ui.md`
- `success-criteria.md`
- `e2e-test-scenarios.md` (20 scenarios)
- This report: `oslo-product-output/worker-reports/slice-06-report.md`

## What's new vs Slice 5 (decisions encoded)
- **D086 — All-issues surface:** new fourth co-primary view `#pane-issues` ("⚠ Issues" + live badge). Filters **Artifact · Dimension · Severity** (+ Status) — artifact-scoping chip labeled **"Artifact"** (not "Section"). **"By dimension / By severity"** group toggle (By severity adds a triage strip). Honest **"N hidden by filters · clear"**. Cards = title + severity + location (`Artifact · Dimension`) + lifecycle pill. Wired to the 6 real issues.
- **D087 — Full Issue Panel:** graduated `openIssue()` — Header (title · severity · dimension·artifact · lifecycle) → Why this matters → **Evidence (collapsible)** → What this weakens → Recommendations → History (pointer → Slice-7 seam) → reanalysis note.
- **D088 — Lifecycle Open → Addressed → Resolved:** `_istatus` extended with `addressed`; no Acknowledge, **no manual resolve**. "Addressed · awaiting reanalysis" after acting; Resolved only via reanalysis. Reflected on cards, Attention cells, artifact badges, Overview counts (active = non-resolved, so counts and routing stay in agreement).
- **D089 — Recommendations + Apply this fix:** OSLO Recommended (From OSLO) + Possible Resolution Paths → **Selected Path = Confirmed by you**; single **Apply this fix** drafts (ISS-01/ISS-02) → applies → reanalysis → Addressed then Resolved; confidence **direction-only** (D056). Recommendations live **only** inside the issue.
- **D090 — Clarification loop:** kept in-panel; answering → updates project info → reanalysis → issue closes (now on the Addressed→Resolved track).
- **D091 — Empty states:** four honest (`none` / `none-lens` / `wait` / `unavail`) + honest hidden count; not-yet-analyzed/unavailable reachable via a subtle prototype-preview control.
- **D058 graduated:** the Attention-map cell/row routing now opens **into this full Issues surface** (`scopeIssuesTo` → scoped center pane, both filters lit; single active issue → its panel). The old separate scoped scrim is retired from the routing path (code left in place, unused, to avoid regression).

Each of the 6 issues gained `caf` (What this weakens), `rec` (OSLO Recommended); `fixes`→`paths`; `draft` added to ISS-01/ISS-02. New state: `_selpath`, `_LIFE`, `_lifeword`, `_filt`, `_group`, `_issuesState`.

## Verification
- **`node --check`** on the extracted inline script: **PASS** (no JS error).
- **jsdom structural parse (no runScripts):** `document.body.children.length = 15`; all key elements present (`pane-issues`, `iss-list`, `if-art/dim/sev/status`, `grpDim/grpSev`, `vsIssues`, `issueScrim`, `issuepanel`, prior panes, `heatGrid`). 11 filter chips, 2 group tabs, 4 view buttons.
- **jsdom runtime flow (runScripts):** all Slice-6 functions defined; `renderIssues`/`setFilt`/`setGroup`/`openIssue`/`selectPath` run without error; panel contains Why / Evidence / What this weakens / OSLO Recommended / Apply this fix / Selected Path / History / Confirmed by you. **Apply this fix** shows "Re-analyzing…" (Addressed) then the **"Resolved by reanalysis"** banner (~1.9s). Attention routing enters the Issues pane. Resolving all issues renders the **none-found** empty state. Only warning: font-CDN network load (irrelevant, offline).
- **No regression:** the change to "active = non-resolved" was applied uniformly (`_istatus[id]==='open'` → `!=='resolved'`) so heatmap counts, badges, routing and Overview counts remain consistent; Slice-5 editor/annotations/stepper untouched.

## Flags / notes for the owner (nothing invented)
- **Added a fourth filter, "Status" (Open/Resolved/All).** The decision text lists filters as Artifact·Dimension·Severity; Status was added because the lifecycle needs a way to view Resolved issues (matches the v4 reference's Status filter). Flag for ratification.
- **Prototype-preview control for empty states.** The not-yet-analyzed / unavailable states aren't naturally reachable in a single analyzed session, so a small labeled "prototype preview" switch under the list makes all four D091 states inspectable. Prototype-only affordance.
- **Confidence move on resolve is illustrative (D056-compliant).** Direction-only, no number; the CAF/idx nudge fires only for the critical Resources gap, consistent with prior slices' illustrative values.
- **Scoped scrim retained but unused.** The Slice-4 scoped-issues scrim code remains in the file (harmless dead code) so nothing that referenced it breaks; routing now goes to the full surface.

## Revision 2 (2026-07-09)
**Copy/UX-only declutter of the Issue Panel + remove user-facing "reanalysis/re-analyze" language (D092).** Behavior, lifecycle logic, apply-fix, and how issues actually close are unchanged — reanalysis still closes issues under the hood; only the surfaced text was trimmed. Per single-home + hover (§6.7) the honesty guarantee now appears in **exactly one** subtle place.

Trimmed/removed in `prototype.html`:
- **Removed the standing `.ip-rean` note** ("Only reanalysis changes this assessment. You can't resolve an issue by hand — change the plan… and OSLO reanalyzes automatically") — deleted as standing chrome.
- **Clarification block:** removed the standing `.cl-note` mechanism line ("OSLO asks; you answer; you decide. Answering updates your project info, re-runs analysis, and closes this issue") → short neutral prompt **"Add the detail OSLO is missing."**; textarea placeholder → **"Type your answer…"**; button **"Submit & re-analyze" → "Submit answer"**.
- **Recommendations:** apply-note trimmed to what applying does (`Applying drafts the change into your plan.` / `…updates your plan.`) — dropped "re-runs analysis / acceptance isn't success / reanalysis confirms"; Recommendations ⓘ tip trimmed to "Recommendations live only inside the issue. Selecting a path records your choice."; Selected-Path banner dropped "…until the plan is updated and OSLO reanalyzes."
- **Banners:** `.ip-addressed` → **"Addressed · updating…"** (was "Addressed · awaiting reanalysis" + explanation); `.ip-resolved` → **"Resolved. You acted on this issue and OSLO's read updated to close it. Confidence was refined accordingly."** (dropped "Resolved by reanalysis / re-ran the analysis / only reanalysis moves an issue").
- **Transient statuses:** apply-fix and clarification panels now show **"Updating…"** (was "Re-analyzing…") with mechanism copy trimmed.
- **Issues pane:** subtitle (static + `renderIssues()` by-dim/by-sev) trimmed to plain "What needs your attention…" (dropped "OSLO advises; you decide" chrome + "closes only when reanalysis confirms it — never by hand"); empty resolved state → "Resolved issues will appear here."; History pointer statuses → "you acted on it" / "now resolved"; the Overview clarification-pointer tip dropped "re-runs analysis".

**Single honesty hover (the only allowed spot):** a subtle `.info` ⓘ placed **beside the `.ip-life` lifecycle track** in `openIssue()`. Wording (plain outcome, no "reanalysis" word): *"Issues close as OSLO's understanding updates — you don't close them by hand."*

Out of scope, intentionally untouched: the Slice-5 artifact autosave/reanalysis chip (D070 "Reanalyzing…") and the Overview confidence-read strings (ustate pill, why-box, artifact empty-state) — not part of the Issue Panel/clarification/apply-fix; and code comments (documentation of the behavior-enforced invariant).

**Verification (Revision 2):**
- `node --check` on the extracted inline `<script>`: **PASS** (syntax OK).
- jsdom structural parse (no runScripts): `document.body.children.length = 15` (> 0).
- jsdom runtime flow (runScripts): opening `ISS-01` renders the lifecycle track + honesty ⓘ hover, "Submit answer" button, and **no** "reanaly/re-analy" text; `applyFix('ISS-01')` shows transient **"Updating…"** (no "Re-analyzing"), then resolves to a **Resolved** banner with no reanalysis text; **0 jsdom errors**.
- Grep confirms the removed strings are gone; the only remaining "reanaly*" hits in the Issue Panel/clarification/apply-fix scope are **code comments**, not user-facing UI.

## Revision 3 (2026-07-09)
**Two edit-in-place changes to the Issues view (D092b) — behavior of every other slice and all existing Issues behavior preserved.**

1. **Added a third group-toggle "By artifact".** New `#grpArt` button (`data-g="art"`, `role=tab`, `onclick="setGroup('art')"`) alongside "By dimension" / "By severity", same styling/keyboard behavior. `setGroup()` was already generic, so it wires in unchanged (2 modes → 3). In `renderIssues()`, the group selection generalized from a boolean to three modes: `byArt` groups on the issue `sec` field using `_ISSARTORDER` (Intent · Context · Scope · Requirements · WBS · Schedule · Resources) — the same plan-artifact order used by the Artifact filter — with headers rendered via `dispName(k)` (plain display name, e.g. WBS → "Work breakdown"). Only artifacts holding matching issues render; within a group, items stay sorted most-urgent first; the existing `.iss-group`/`.iss-gh`/`.icard` structure is reused. The per-group early-return guards were made mode-correct (`_group==='dim'` for the dim filter, `bySev` for the sev filter, added `byArt` for the art filter) so the dim/sev modes behave exactly as before. Filters (Artifact/Dimension/Severity/Status), the `.iss-hidden` count, and per-issue cards all work unchanged in artifact mode. No triage strip in artifact mode (triage stays severity-only).

2. **Trimmed the verbose subtitle.** Both the static `#iss-sub` and the `renderIssues()` assignment now emit the single minimal, static string **"What needs your attention"** for every mode. Removed: "— most urgent first. Severity is qualitative." and "— grouped by dimension (Clarity · Alignment · Feasibility)." No mechanism copy; the group tabs already name the grouping.

**Verification (Revision 3):**
- `node --check` on the extracted inline `<script>`: **PASS** (syntax OK).
- jsdom structural parse (no runScripts): `document.body.children.length = 15` (> 0); three group tabs render — `grpDim`/`grpSev`/`grpArt` = "By dimension" / "By severity" / "By artifact"; static `#iss-sub` = "What needs your attention".
- By-artifact grouping confirmed against the 6-issue dataset: groups emit in plan order with only non-empty artifacts — **Context · 1** (ISS-06), **Requirements · 1** (ISS-02), **Work breakdown · 1** (ISS-05, WBS→dispName), **Schedule · 1** (ISS-04), **Resources · 2** (ISS-01 critical, ISS-03 moderate — critical first); Intent and Scope omitted (no issues).
- Docs updated: `frontend-ui.md` (`#grpArt` tab, By-artifact group rule, static subtitle) and `user-experience.md` (three-way toggle + minimal-subtitle note), both marked D092b.

## Revision 4 (2026-07-09)
**App-shell restructure to a persistent left navigation sidebar (D093) — edit-in-place; all prior views and behavior preserved 1:1.**

Added a persistent left sidebar as primary nav and moved `#app` to a 3-column grid; removed the top-center `.vswitch`.

1. **Grid + shell.** `#app` `grid-template-columns` → **`240px 1fr 340px`** = [sidebar | main `.body` | chat rail]; `#app.chat-collapsed` → `240px 1fr 0`. `.body` → `grid-column:2`, `.chatp` → `grid-column:3`; topbar still spans all columns. The 38px phase-bar offset (`margin-top:38px` on `#app`) is unchanged.
2. **Sidebar (`aside.sidebar#appSidebar`).** Scroll area (`.sb-scroll`) + pinned footer (`.sb-foot`):
   - **Project** — `#sbOverview` / `#sbAttention` (badge `#vsAttnBadge`) / `#sbIssues` (badge `#vsIssuesBadge`); badges are **neutral** nav chrome (`.sb-badge`, surface/border — never severity color, D003).
   - **Plan artifacts** — the 7 `.sb-nav.sb-art` items (`data-art`, live `.ex-fb[data-badge]` severity badges kept so `renderExplorerBadges()` works unchanged), each calling `openArtifact(id)`.
   - **Footer** — `#railTour` (→ `startTour()`; `tourComplete()` still hides `#railTour`) and `#sbSettings` (→ `openSettings()` stub → `#sbToast`).
3. **Removed the top-center `.vswitch`** (and its `#vsOverview`/`#vsArtifacts` tabs) from the topbar; kept brand, `#confpill`, and `#acctBtn`. Added a `#sbHamburger` (☰) topbar button for the narrow-width drawer.
4. **Artifacts view = editor only.** Deleted the in-view `.aw-explorer` aside + `#awExplorerToggle`; `.aw-pane` → single column (`grid-template-columns:1fr`). The artifact list now lives only in the global sidebar.
5. **Active-state sync.** New `_syncNav()` helper (single source of truth) called from **both** `showView()` and `openArtifact()`; toggles `.active` + `aria-current` on the active Project-view item and on the active `.sb-art` (only while `CURVIEW==='artifacts'`). `showView()`'s old per-tab `vs*` toggles were replaced by `_syncNav()` (removing now-dead `getElementById` calls on deleted `#vsOverview`/`#vsArtifacts`, which had no null guard).
6. **Responsive.** New `@media(max-width:860px)`: sidebar → fixed overlay drawer (`transform:translateX(-100%)`; `#app.sidebar-open` shows it), `#sbHamburger` visible, `.sb-scrim` closes it; `toggleSidebar()`/`closeSidebar()`, and `_collapseSidebarOnNarrow()` (end of `showView()`) auto-closes after a pick. The ≤760px chat-rail collapse is unchanged.
7. **Tour fix.** The Attention-map tour step selector `.vswitch` → `#sbAttention` (the spotlighted element moved into the sidebar).

**Verification (Revision 4):**
- `node --check` on the extracted inline `<script>`: **PASS** (1 script block, syntax OK).
- jsdom structural parse (no runScripts): `document.body.children.length = 15` (> 0); `aside.sidebar#appSidebar` present with `#sbOverview`/`#sbAttention`/`#sbIssues`, both count badges, all **7** `.sb-art` items + **7** `.ex-fb` badges, footer Tour + Settings; `.vswitch` **gone**; `#confpill` + `#acctBtn` present; `.aw-explorer` **gone**; 4 panes intact; **no duplicate IDs** (`#railTour`/`#vsAttnBadge`/`#vsIssuesBadge` each count 1); `_syncNav`/`toggleSidebar`/`openSettings` defined.
- jsdom runtime flow (runScripts): `showView('attention')` → `#sbAttention.active` + `aria-current="page"`, Overview cleared; `showView('issues')` → `#sbIssues.active`; `openArtifact('Schedule')` → `#pane-artifacts.active`, `.sb-art[data-art=Schedule].active` + `aria-current="page"`, editor renders (`.art-head h1` = "Schedule"); switching back to Overview clears the artifact highlight and re-activates Overview; `toggleSidebar()`/`closeSidebar()` flip `#app.sidebar-open`; `openSettings()` turns on `#sbToast`; **0 jsdom errors**.
- Docs updated: `frontend-ui.md` (rewritten Navigation section — 3-col grid, sidebar structure, `_syncNav`, responsive drawer) and `user-experience.md` (new "App-shell navigation — persistent left sidebar (D093)" section; D093 added to decisions-encoded).

## Revision 5 (2026-07-09)

**App-shell reconciled to the owner-APPROVED design (D093 refined) — edit-in-place; every view/behavior preserved, grid intact.**

Adjusted the Revision-4 sidebar/top bar to match the approved layout. No slice internals pulled forward; not-yet-built features are labeled seams.

1. **Sidebar PROJECT group** — reordered to the approved **Overview · Issues · History · Attention map**. Added `#sbHistory` (◔) as a real nav item routing to `showView('history')`. **Kept the ratified label "Issues"** (the approved image says "Findings" — not used) and its neutral open-issue badge.
2. **History = Slice-7 seam pane** — new `#pane-history` center pane ("History & timeline — arrives in Slice 7"), toggled in `showView()` and highlighted by `_syncNav()` (now includes `['sbHistory','history']`). It is **not** the Attention map and **not** a broken link. The existing modal `openHistorySeam()` (Overview "Timeline →", issue-panel "Open full timeline") is untouched.
3. **PLAN ARTIFACTS split** — the 7 artifacts are now grouped under two `.sb-subgroup` labels: **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown · Schedule · Resources). Same `openArtifact(id)` wiring + live `.ex-fb[data-badge]` severity badges.
4. **Sidebar foot** — replaced Tour+Settings with the approved three: bordered `.sb-tour#railTour` (Take a quick tour); a neutral `.sb-tier` chip (◆ **Free plan** · 1 active project) with an **Upgrade** button (`openUpgrade()` stub); and a **Your account** row `.sb-acct#acctBtn` (avatar "ID" + "Your account"/"Settings" → `toggleAcctMenu()`). Settings stays reachable as an item inside the account menu.
5. **Top bar (approved)** — left: brand → **project switcher** chip `#tbProj` (holds `#projName` + ▾; `openProjectSwitcher()` = **Slice-8 seam**) → **`sample`** tag → breadcrumb `#tbCrumb` (current view/artifact, driven by `_setCrumb()`/`_viewLabel()`). Right: `#confpill` (unchanged) → search `#tbSearch` → **Share** `#tbShare` (**Slice-9 seam**) → **Export** `#tbExport` (**Slice-9 seam**) → report `#tbReport` → **Free** chip `#tbPlan`. The old top-right account circle was removed (account moved to the sidebar foot); `.acctmenu` re-anchored bottom-left.
6. **JS** — `showView()` toggles `#pane-history` + sets the crumb; `_syncNav()` handles History; `openArtifact()` sets the crumb to `dispName(name)`. Added helpers `_viewLabel()`/`_setCrumb()` and a shared `_stubToast(msg)` backing `openSettings`/`openProjectSwitcher`/`openSearchStub`/`openShareSeam`/`openExportSeam`/`openReportStub`/`openUpgrade`. `_scrollMem` gains `history`. Tour selectors (`#confpill`, `#sbAttention`, `#artdoc`, `#chatp`, `#focus`) all still resolve.
7. **CSS** — added `.tb-proj`/`.tb-tag`/`.tb-ic`/`.tb-plan` (top bar), `.sb-subgroup`, `.sb-tour`, `.sb-tier*`, `.sb-acct*`, `.hist-seam*`; neutral/brand chrome only (severity color reserved for issue badges).

**Verification (Revision 5):**
- `node --check` on the extracted inline `<script>` (1 block): **PASS**.
- jsdom structural parse (no runScripts): `body.children.length = 15`; PROJECT nav order = **Overview → Issues → History → Attention map**; label is **"Issues"** (no "Findings"); Understanding + Execution subgroups present; **7** `.sb-art` + badges; foot Tour + Free-plan/Upgrade + Your-account; top bar brand + project switcher + `sample` + breadcrumb + `#confpill` + search + Share + Export + report + Free; `#pane-history` labels the Slice-7 seam. **All PASS.**
- jsdom runtime (runScripts): clicking Overview/Issues/History/Attention switches panes + highlights the nav + updates the breadcrumb (History shows the Slice-7 seam); `openArtifact('Requirements')` shows the editor, highlights the artifact, and sets the crumb to "Requirements"; `startTour()`/`openSettings()`/`openUpgrade()`/`openProjectSwitcher()`/`openShareSeam()`/`openExportSeam()`/`toggleAcctMenu()` all fire correctly. **0 errors** (the sole jsdom exception is `Element.scrollIntoView` not being implemented in jsdom — an environment gap in the pre-existing `tourGo`, not a prototype bug; polyfilling it yields a clean run).
- Docs updated: `frontend-ui.md` (Navigation section rewritten for the approved sidebar + top bar, seams enumerated) and `user-experience.md` ("App-shell navigation — persistent left sidebar + top bar" reconciled to the approved design).

## Revision 6 (2026-07-09)

**Command palette (search / jump-to) built to the owner-APPROVED design (D094) — edit-in-place; every view/behavior/pane preserved, HTML structurally valid.**

Replaced the top-bar Search **seam stub** (`openSearchStub()` → `_stubToast('Search — command palette arrives in a later slice')`) with a real palette. No slice internals pulled forward; History still routes to its Slice-7 seam pane.

1. **Trigger.** `#tbSearch` (⌕) `onclick` → `openSearch()` (was `openSearchStub()`); a new global `keydown` listener opens/toggles the palette on **⌘/Ctrl+K** (`preventDefault` so the browser doesn't intercept). `openSearchStub()` kept as a legacy alias → `openSearch()`.
2. **Overlay.** New `#palScrim` centered modal (dim scrim, `z-index:250` — above phasebar/toast chrome, below the `#issueScrim` flyout at 260) holding `.palette` (`role=dialog`/`aria-modal`): autofocused input `#palInput` ("Search or jump to…", `role=combobox`), scrollable `#palResults` (`role=listbox`), and a `.pal-foot` "↑↓ navigate · ↵ open · esc close".
3. **Groups (live-filtered, case-insensitive substring; empty groups hidden).** **GO TO** — ◎ Overview · ⚑ Issues · ◔ History · ▦ Attention map → `showView(...)`. **PLAN ARTIFACTS** — the 7 artifacts (▤ + `dispName(id)`, WBS → "Work breakdown") → `openArtifact(id)`. **OPEN AN ISSUE** — each `_istatus[id]!=='resolved'` issue = title + muted "{Severity} · {Artifact}" → `openIssue(id)`. **Ratified terms used, not the reference image's "Findings"/"OPEN A FINDING".**
4. **Keyboard/behavior.** `_palKeydown` handles ↑/↓ (wrap the highlight across all visible items), Enter (activate), Esc (close); first visible item pre-highlighted; hover sets the highlight. `_palActivate(i)` **closes the palette first, then runs the action** so the destination is visible. Scrim-click closes; item-click activates. Opening the palette closes any live issue flyout (the two are never both open).
5. **Theme / a11y.** Neutral dark chrome; highlight = `.pal-item.active` `--surface-2` tint (never severity color — D003). Labelled input, `role=listbox`/`option`, `aria-selected` + `aria-activedescendant`; fully keyboard-operable.
6. **New functions:** `openSearch`, `closeSearch`, `_palIsOpen`, `_palModel`, `_palFilter`, `_palPaint`, `_palSetActive`, `_palKeydown`, `_palActivate`, `_palEsc`. New CSS: `#palScrim`, `.palette`, `@keyframes palin`, `.pal-inwrap`/`.pal-mag`, `#palInput`, `.pal-results`, `.pal-group`/`.pal-glabel`, `.pal-item`/`.pal-ic`/`.pal-nm`/`.pal-meta`, `.pal-empty`, `.pal-foot`.

**Verification (Revision 6):**
- `node --check` on the extracted inline `<script>`: **PASS** (both block-wrapped and plain-concat forms).
- jsdom structural parse (no runScripts): `body.children.length = 16` (> 0); `#palScrim` present; `#palInput` placeholder = "Search or jump to…"; `#palResults` `role=listbox`; foot = "↑↓ navigate · ↵ open · esc close"; `#tbSearch` onclick = `openSearch()`.
- jsdom runtime (runScripts): `openSearch()` shows the palette with **GO TO** (Overview/Issues/History/Attention map), **PLAN ARTIFACTS** (all 7, WBS → "Work breakdown"), **OPEN AN ISSUE** (6 open issues; sample row "Keynote backups are unconfirmed — Moderate · Resources"); first item pre-highlighted. Typing **"res"** filters to Resources + the two Resources issues (Wi-Fi, Keynote backups) — empty GO TO group hidden. **ArrowDown+Enter** activates "Issues" → `#pane-issues.active`, crumb "Issues", palette closed. Clicking the Work-breakdown row → `#pane-artifacts.active`, crumb "Work breakdown". Clicking an issue row → `#issueScrim` flyout open + palette closed. **Esc** closes; **⌘K** opens then toggles closed. Labels are **"Issues"/"OPEN AN ISSUE"** (no "Findings" text anywhere in results). Opening the palette while a flyout is up closes the flyout. Prior slices intact (`showView`/`openArtifact`/`openIssue`/`renderIssues`/`renderHeat`/`dispName` all defined). **0 code errors** (only jsdom's external Google-Fonts `<link>` fetch warning, unrelated to the prototype).

## Revision 7 (2026-07-09)

**Fixed the artifact-editor annotation hover popover (`.anno-pop`) showing editor content bleeding through it (appeared transparent / overlapped by the toolbar near the top of the editor). Edit-in-place; every view/behavior preserved; HTML structurally valid.**

**Diagnosis.** The per-annotation `.anno-pop` was `position:absolute` **inside** the contenteditable (`.doc>*{position:relative}`, `.aw-center{position:relative;overflow-y:auto}`). Its background was opaque, but after the app-shell change it was trapped by editor chrome — clipped by the `.aw-center` overflow scroll and painted **under** the `.art-bar` toolbar — so content painted over/through it (worst when the annotation sat in the first line, overlapping the header). A z-index bump alone inside that trapped context would not reliably fix it.

**Approach — viewport-anchored shared popover (the preferred, definitively-immune option).**
1. **Single body-level `#annoPop`.** One `<div id="annoPop">` is appended to `<body>` on first use, `position:fixed`, `z-index:240` (**below** the issue flyout's 260, **above** phasebar 200 / toast 210 / editor toolbar), fully opaque (`background:var(--surface)` + solid `--border-2` + shadow), `display:none` by default. It escapes every local stacking context and the `.aw-center` overflow clip, so nothing can paint through or over it.
2. **Inline `.anno-pop` kept only as content source.** Set to `display:none !important` (never painted); the old CSS reveal rules (`.anno:hover>.anno-pop`, `.anno:focus-within>.anno-pop`, `.anno.anno-peek>.anno-pop`) were removed. On show, JS copies the inline span's `innerHTML` (same summary + `<a class="anno-open" onclick="openIssueFromAnno(id)">Open issue →</a>`) into `#annoPop`, so the content and the click wiring are unchanged.
3. **Positioning + flip + opacity.** `showAnnoPop(anno)` reads `anno.getBoundingClientRect()`. `_positionAnnoPop()` **prefers ABOVE** (`top = r.top − popHeight − 6`); if that would cross `_annoPopTopFloor()` (the `.art-bar` bottom edge + 4, i.e. near the top / would overlap the toolbar) it **flips BELOW** (`top = r.bottom + 6`); it also **clamps horizontally** into the viewport (`left ∈ [8, innerWidth − popWidth − 8]`) and nudges up if it would fall off the bottom. Opacity is guaranteed by the fixed, body-level, fully-opaque surface — there is no ancestor to bleed through.
4. **Hover-stable.** Delegated `mouseover`/`mouseout` on `#artdoc` show/hide; the popover stays open while the pointer is over the `.anno` **or** over `#annoPop` (its own `mouseenter` cancels the ~140ms hover-intent hide timer). Editor scroll (`#artCenter`) and window resize hide it (re-shows on next hover/focus). **Esc** and click-away close it; `openIssueFromAnno(id)` (link **and** ⚠ marker) closes it then opens the issue.
5. **A11y + editability preserved (D074).** The ⚠ marker's focus/Enter and tap paths now also call `showAnnoPop()`/`hideAnnoPop()`. Clicking the annotated **text** still places the caret and edits (entering the caret adds `.editing` and calls `hideAnnoPop()`, suppressing the summary while editing). `curAnnos()` still selects only `.anno` — `#annoPop` is body-level, not inside `.doc`.

**New CSS:** `#annoPop` (fixed, z-240, opaque), `#annoPop b`; `.anno-pop{display:none !important}` (was the shown popover); removed the `.anno:hover/.anno:focus-within/.anno-peek > .anno-pop{display:block}` reveals. **New JS:** `_annoPop()`, `_scheduleAnnoPopHide()`, `hideAnnoPop()`, `_annoPopTopFloor()`, `_positionAnnoPop()`, `showAnnoPop()`, plus `mouseover`/`mouseout`/scroll/resize wiring in `_wireA11yReveals()`; `openIssueFromAnno()` and the `.editing` path now call `hideAnnoPop()`.

**Verification (Revision 7):**
- **`node --check`** on the extracted inline `<script>`: **PASS**.
- **jsdom static parse** (no `runScripts`): `body.children.length = 16` (> 0); `#annoPop` CSS present; inline `.anno-pop{display:none !important}` present.
- **Positioning unit-test** (extracted `showAnnoPop`/`_positionAnnoPop` against a stubbed DOM, toolbar bottom = y120, popover 280×90, viewport 1000×800): first-line anno (top 110) → **flips BELOW** (`top=136px`); mid-editor anno (top 400) → **ABOVE** (`top=304px`); right-edge anno (left 900) → **clamped** (`left=712px`); `.editing` anno → **suppressed** (stays `display:none`). All as expected.
- **Reasoned checks:** popover is `position:fixed` at z-240 on `<body>`, so the `.aw-center` overflow can't clip it and the `.art-bar` can't overlap it; content is copied from the same source, so "Open issue →" and the ⚠ marker still call `openIssueFromAnno(id)`; `curAnnos()` query (`#artdoc .anno`) is unchanged and excludes the body-level `#annoPop`.
