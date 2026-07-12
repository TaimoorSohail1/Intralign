# Slice 6 — Issues & Recommendations · Frontend UI

Cumulative Slices 1–6. Single openable `prototype.html` (Tailwind-independent inline CSS/JS + `localStorage`, D016). This documents the Slice-6 UI surfaces, DOM, CSS, and functions. Slices 1–5 UI is unchanged.

## Navigation (D093 — persistent left sidebar + top-bar shell; reconciled to the owner-APPROVED design, 2026-07-09)
Primary navigation lives in a **persistent left sidebar** (`aside.sidebar#appSidebar`), present in every project view. `#app` is a **3-column grid** — `grid-template-columns:240px 1fr 340px` = **[sidebar | main `.body` | OSLO chat rail]** — with the topbar spanning all columns (`grid-column:1 / -1`); `#app.chat-collapsed` → `240px 1fr 0`. `.body` is `grid-column:2`, `.chatp` is `grid-column:3`. The former **`.vswitch` top-center switch stays deleted**.

**Top bar (approved).** Left cluster: the **Intralign** brand (`.tb-brand`, orange `I` `.logo`) → **project switcher** chip `#tbProj` (`.tb-proj`, holds the project-name span `#projName` + `▾`; opens `openProjectSwitcher()` — a **Slice-8 seam** stub, multi-project not yet built) → a **`sample`** tag (`.tb-tag`) → breadcrumb `.crumb-sep › ` + `#tbCrumb` (the **current view or open artifact**, kept live by `_setCrumb()`/`_viewLabel()`). `.tb-sp` spacer. Right cluster: the **confidence pill `#confpill` (unchanged, D050)** → search `#tbSearch` (⌕, `openSearchStub()`) → **Share** `#tbShare` (⤴, `openShareSeam()` — **Slice-9 seam**) → **Export** `#tbExport` (⤓, `openExportSeam()` — **Slice-9 seam**) → report/donut `#tbReport` (◕, `openReportStub()`) → **Free** plan chip `#tbPlan` (`openUpgrade()`). The `#sbHamburger` (☰) drawer toggle sits far left. The former top-right account circle is **removed** — account moved into the sidebar foot (below).

Sidebar structure (`.sb-scroll` scroll area + pinned `.sb-foot`):
1. **Project** group — `.sb-nav` buttons in approved order: `#sbOverview` (◎ Overview → `showView('overview')`), `#sbIssues` (⚑ **Issues** → `showView('issues')`, neutral count `.sb-badge#vsIssuesBadge`), `#sbHistory` (◔ History → `showView('history')` — routes to the **`#pane-history` Slice-7 seam** pane, not the Attention map), `#sbAttention` (▦ Attention map → `showView('attention')`, neutral count `.sb-badge#vsAttnBadge`). The ratified term is **"Issues"** (the approved image's "Findings" is *not* used); the badge is kept. Badges are **neutral nav chrome** (surface/border, never severity color — D003).
2. **Plan artifacts** group — split into two labeled `.sb-subgroup` subgroups: **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown/WBS · Schedule · Resources). Seven `.sb-nav.sb-art` buttons (`data-art`), each with a live `.ex-fb[data-badge]` severity issue badge (D066), calling `openArtifact(id)`. This remains the global explorer (`.aw-explorer` stays removed; `.aw-pane` single-column = editor).
3. **`.sb-foot`** (pinned bottom) — three approved elements: the bordered `.sb-tour#railTour` (✦ Take a quick tour → `startTour()`; hidden by `tourComplete()` once seen); a neutral **tier chip** `.sb-tier` (◆ **Free plan** · 1 active project) with an **Upgrade** button (`.sb-tier-up` → `openUpgrade()`, a visibility-first stub); and a **Your account** row `.sb-acct#acctBtn` (avatar "ID" + "Your account" / "Settings" subtext → `toggleAcctMenu()`). Settings stays reachable as an item inside the account menu (`openSettings()` → `#sbToast` stub). The account menu (`.acctmenu`) is re-anchored bottom-left to open from this row.

- **Active-state:** `_syncNav()` is the single sync helper (called from **both** `showView()` and `openArtifact()`). It toggles `.active` + `aria-current="page"` on the matching Project-view item (now including `#sbHistory`), and on the matching `.sb-art` item **only while** the Artifacts view is showing (`CURVIEW==='artifacts'` && `dataset.art===_curArt`). `showView()` toggles `#pane-history.active` alongside the other panes and calls `_setCrumb(_viewLabel(v))`; `openArtifact()` sets the crumb to `dispName(name)`. Live badge counts still flow through `updateIssueCounts()` (`#vsAttnBadge`/`#vsIssuesBadge`) and `renderExplorerBadges()`.
- **Seam stubs** (labeled, never broken links): History→`#pane-history` "History & timeline — arrives in Slice 7"; project switcher→Slice 8; Share/Export→Slice 9; search/report/upgrade→`_stubToast()` toasts. None pull forward those slices' internals.
- **Responsive:** at ≤860px the sidebar becomes a fixed overlay **drawer** (`transform:translateX(-100%)`, shown via `#app.sidebar-open`), opened by `#sbHamburger` (☰); a `.sb-scrim` closes it. `toggleSidebar()`/`closeSidebar()` drive it; `_collapseSidebarOnNarrow()` (end of `showView()`) auto-closes after a pick. The chat-rail collapse at ≤760px is unchanged.

## All-issues surface — `#pane-issues`
DOM:
- `.iss-head` → `h1 "Issues"` + `#iss-count` (live count).
- `#iss-sub` — advisory sub-line; static minimal text **"What needs your attention"** in every group mode (D092b — verbose mechanism tails removed; the group tabs already name the grouping).
- `.grp-tabs` → `#grpDim` / `#grpSev` / `#grpArt` ("By dimension" / "By severity" / "By artifact"), `role=tab`, `aria-selected` (D092b — third mode). `setGroup('dim'|'sev'|'art')` toggles `.grp.on`.
- `.iss-filters` → four `.if-row`s: **Artifact** (`#if-art`, built by `renderArtFilters`), **Dimension** (`#if-dim`), **Severity** (`#if-sev`), **Status** (`#if-status`). Chips = `.ff` buttons with `data-f`/`data-v`; active = `.ff.on`; zero-count = `.ff.ff-empty` (dimmed); per-chip count = `.ffn`.
- `#iss-list` — rendered by `renderIssues()`.

Cards & groups:
- `.iss-group` → `.iss-gh` header + `.icard`s.
- `.icard` = `.isevbar` (severity color only) + `.ic-main` (`.ic-t` title, `.ic-m` meta: `.ic-sev` severity chip, `.ic-loc` "Artifact · Dimension", `.ic-life` lifecycle pill, optional `.ic-clarflag`) + `.ic-go`. `role=button`, `tabindex=0`, Enter/Space → `openIssue`.
- **Triage** (By severity): `.triage` with `.tg.crit/.tg.mod/.tg.warn`.
- **By artifact** (D092b): groups keyed on the issue `sec` field, using `_ISSARTORDER` (Intent · Context · Scope · Requirements · WBS · Schedule · Resources); headers show the plain display name via `dispName()` (e.g. WBS → "Work breakdown"); only artifacts with matching issues render. No triage strip. Same `.iss-group`/`.iss-gh`/`.icard` structure; filters + `.iss-hidden` count unaffected.
- **Hidden count:** `.iss-hidden` → "N issues hidden by filters · clear".
- **Empty states:** `.iss-empty` variants `.good` / `.wait` / `.err` (`_issEmpty(kind)`).

## Full Issue Panel — `#issueScrim` / `#issuepanel`
Reuses the existing right-slide scrim; `openIssue(id)` now renders the full panel:
- `.ip-top` (severity chip `.ip-sev`, `.ip-title`, close `×`), `.ip-meta` (Dimension · **Artifact** link · issue id), `.ip-life` lifecycle track (`.st.on` current, `.st.done` past) followed by a single subtle `.info` ⓘ hover — the **only** place the honesty guarantee is surfaced as standing text (tip: "Issues close as OSLO's understanding updates — you don't close them by hand.").
- `.ip-h "Why this matters"` + `.ip-p`.
- **Evidence** collapsible: `.ip-evsec.collapsed` with `.ip-evh` (chevron `.chev`, "N sources") toggling `.ip-evbody` (`.ip-ev` items). Keyboard-operable.
- **What this weakens:** `.ip-weak` with `.wk-dim` dimension tag.
- **Clarification:** `.ip-clar` (question `.cl-q`, `textarea#clarInput` placeholder "Type your answer…", `.cl-note` neutral prompt "Add the detail OSLO is missing.", **Submit answer** button) — when `clar` present and not resolved. No mechanism copy (D092).
- **Recommendations:** `.ip-rec` (`◆ OSLO Recommended` + `From OSLO` `.epi-tag.derived`, `rec` text, **Apply this fix** button `.ip-applyrow`, `.ip-applynote`). `.ip-otherlab "Possible resolution paths"` + `.ip-path` rows (`.selmark`; selected = `.ip-path.sel` "✓ Selected Path"). Selected → `.ip-selpath` banner with `Confirmed by you` `.epi-tag`. `.ip-ownfix` "Write my own fix in {Artifact} →".
- **Banners:** `.ip-addressed` ("Addressed · updating…") / `.ip-resolved` ("Resolved" — plain outcome copy, no mechanism talk).
- **History:** `.ip-hist` pointer → `openHistorySeam()` (Slice-7 stub).
- **Honesty guarantee:** carried on the single `.ip-life` ⓘ hover (above). The standing `.ip-rean` note was **removed** (D092, single-home + hover §6.7); the guarantee stays enforced by behavior.

## Key functions (inline `<script>`)
- List: `renderIssues`, `renderArtFilters`, `_issueCard`, `_issEmpty`, `_issPreview`, `previewIssState`, `setFilt`, `setGroup`, `clearFilt`, `_statusMatch`.
- Panel: `openIssue`, `closeIssue`, `openIssueArtifact`, `selectPath`, `applyFix`, `answerClarification`, `_refreshIssueSurfaces`.
- Routing: `openFindingsFor`, `openFindingsForArtifact`, `scopeIssuesTo` (graduated D058).
- `updateIssueCounts` now also drives `#vsIssuesBadge`; `showView` re-renders the list on Issues entry.

## Inherited editor — annotation hover popover (Rev 7 fix)
- The weakness annotation summary popover (inherited from S5) was a `.anno-pop` span `position:absolute` **inside** the contenteditable; under the app-shell it was clipped by `.aw-center{overflow-y:auto}` and painted **under** the `.art-bar` toolbar, so editor content bled through it (appeared transparent) near the top of the editor. Fix: the inline `.anno-pop` is `display:none !important` (kept only as content source); a single body-level **`#annoPop`** (`position:fixed`, `z-index:240` — below the issue flyout's 260, above editor chrome, fully opaque) is populated on `.anno` hover / ⚠ focus-tap and positioned from the annotation's `getBoundingClientRect()`: prefers **above**, **flips below** near the toolbar, **clamps** horizontally. Escapes all local stacking/overflow; `curAnnos()` still selects only `.anno`. (Full detail in Slice-5 `frontend-ui.md`.)

## Theme / accessibility
- Dark default, one semantic token set (inherited). **Severity color only** (D003) on `.ip-sev`, `.ic-sev`, `.isevbar`; confidence/CAF/lifecycle pills use neutral tokens.
- WCAG 2.1 AA: all list cards, filter/group chips, the evidence toggle, resolution paths and panel controls are keyboard-operable (`role=button`/`tab`, `tabindex`, Enter/Space handlers, `focus-visible` rings). `aria-selected` on tabs; `aria-label`s on cards and the close control.

## Command palette — search / jump-to (D094)
A centered modal overlay (`#palScrim`, dim scrim, `z-index:250` — above the app chrome but below the `#issueScrim` flyout at 260; the two are mutually exclusive) holding `.palette`:
- **Input:** `#palInput` (placeholder **"Search or jump to…"**, autofocused on open, `role=combobox` + `aria-controls=#palResults` + `aria-activedescendant`), preceded by a `⌕` mark.
- **Results:** `#palResults` (`role=listbox`), grouped `.pal-group` blocks each with a `.pal-glabel` header and `.pal-item` rows (`role=option`, `aria-selected`). Groups render only when non-empty (live filter).
  - **GO TO** — ◎ Overview · ⚑ Issues · ◔ History · ▦ Attention map → `showView('overview'|'issues'|'history'|'attention')`. (The approved reference image labels this list "Findings"; the ratified term **"Issues"** is used.)
  - **PLAN ARTIFACTS** — the 7 artifacts (▤ + `dispName(id)`, so WBS shows "Work breakdown") → `openArtifact(id)` with the internal id.
  - **OPEN AN ISSUE** — each still-open issue (`_istatus[id]!=='resolved'`): `.pal-nm` title (left) + `.pal-meta` "{Severity} · {Artifact}" (right, muted), e.g. "Keynote backups are unconfirmed — Moderate · Resources" → `openIssue(id)`. (The approved image labels this "OPEN A FINDING"; the ratified **"OPEN AN ISSUE"** is used.)
- **Footer:** `.pal-foot` "↑↓ navigate · ↵ open · esc close".
- **Highlight** = `.pal-item.active` neutral `--surface-2` tint (never a severity color); issue rows may show their severity *word* in `.pal-meta` text, but the row highlight stays neutral.

### Key functions (inline `<script>`)
- `openSearch()` / `closeSearch()` — open (closes any live issue flyout first, clears + refocuses the input, builds results) / hide. `openSearchStub()` is a legacy alias → `openSearch()`; the top-bar `#tbSearch` now calls `openSearch()`.
- `_palModel()` builds the grouped model fresh each keystroke (live issue statuses); `_palFilter()` renders it filtered by case-insensitive substring into a flat `_palVisible` array; `_palPaint()` maintains the `.active` highlight + `aria-activedescendant`; `_palKeydown(e)` handles ↑/↓ (wrap), Enter (activate), Esc (close); `_palActivate(i)` closes the palette **first**, then runs the item action; `_palSetActive(i)` handles hover. A global `keydown` listener toggles the palette on **⌘/Ctrl+K** (`preventDefault`).

### Theme / accessibility
- Dark default, one semantic token set (inherited). Neutral chrome only; the highlight uses `--surface-2` (no severity color on the row).
- WCAG 2.1 AA: labelled input, `role=dialog`/`aria-modal` on `.palette`, `role=listbox`/`role=option` results, `aria-selected` + `aria-activedescendant`; fully keyboard-operable (↑↓/Enter/Esc), scrim-click and item-click close/activate.

---

## Chat integration (D108 cascade)

The persistent OSLO rail is now a **working advisor** in this slice — the composer, Send, and Enter-to-send are live, and every reply is simulated but **state-grounded** (derived from `currentRead()`, `ISSUES` / `_istatus` / `_selpath`, the CAF rows, `ANALYSIS_STATE`, `_curArt`). Nothing in the chat mutates the plan (D001): it only ever **offers** actions as links that run the surfaces' own functions.

### DOM
- `#chatCtx` — the context pill (`Context` label · `#chatCtxLabel` · `#chatCtxClear` ×), hidden until a surface hands context in.
- `#chatscroll` — `role="log"`, `aria-live="polite"`, `aria-relevant="additions"`; carries `#chatEmpty` (first-run empty state) until the first turn lands.
- `#chatChips` — state-derived suggested prompts; `#chatInput` (`onkeydown="chatKey(event)"`) + `#chatSend`.
- Messages: `.cmsg` (OSLO) · `.cmsg.user` (your turn) · `.cmsg.done` (completion notice); in-reply actions are `.chat-acts` / `.chat-act` buttons.

### Functions
- `sendChat()` / `chatKey(e)` — Send (click) · **Enter** sends · **Shift+Enter** newline. `pushUserChat()` appends the escaped user turn; `pushChat()` appends OSLO's.
- `askOslo(ctx)` — **the one entry point** every surface hands context through. `ctx.type` ∈ `issue | span | artifact | confidence | cell | recommendation`. It stands down the issue flyout / annotation popover, un-collapses the rail, sets `_chatCtx`, paints the pill, pushes a grounded opening message, and focuses the composer. `clearChatContext()` backs the × .
- `_oslloReply(q)` — prototype-grade intent routing (next / issue by id or name / "can you fix it" / a CAF dimension / confidence / artifact / clarifications / the active context / fallback summary), answered by `_ansNext`, `_ansIssue`, `_ansDimension`, `_ansConfidence`, `_ansArtifact`, `_ansCell`, `_ansRecommendation`, `_ansHowIssuesClose`, `_ansClarifications`, `_ansSummary`.
- `renderChatChips()` — rebuilt on every context change and from `_refreshIssueSurfaces()`, so the chips track the live read.

### Entry points wired in Slice 6
| Surface | Affordance | Call |
| --- | --- | --- |
| Overview (confidence) | `#askWhyConf` — "✦ Ask OSLO why" pill under the number | `askOslo({type:'confidence'})` |
| Attention map → scoped Issues list | "Ask OSLO about this cell →" header (shown when artifact × dimension are both scoped) | `askOslo({type:'cell',art,dim})` |
| Issue panel | "✦ Ask OSLO about this issue →" | `askOslo({type:'issue',id})` |
| Issue panel → clarification | "Answer in chat →" | `askOslo({type:'issue',id})` |
| **Issue panel → recommendations** | **`Discuss`** on the **OSLO Recommended** block **and on every resolution path** (`.ip-discuss`) | `askOslo({type:'recommendation',id,pathIndex})` (`pathIndex:null` = OSLO Recommended) |
| Artifact editor | toolbar `#artAskBtn` (✦) | `askOslo({type:'artifact',id:name})` |
| Artifact editor | annotation popover "Ask about this →" | `askAboutSpan(id)` → `askOslo({type:'span',id})` |

### Discuss — the signature action (never selects)
`.ip-discuss` sits inside the `.ip-path` row, whose own click handler is `selectPath()`. The Discuss handler therefore calls **`event.stopPropagation()`** (on both `onclick` and `onkeydown`) before `askOslo(...)`, so discussing a path **never** selects it — `_selpath` and `_istatus` are untouched. `_ansRecommendation()` explains what the path buys, weighs it against the alternatives and the recommendation, states that "talking a path through with me doesn't select it", and *offers* **Select this path →** / **Apply this fix →** as links the user still has to click.

### Clarifications — one shared path, one live box
`answerClarification()` (panel) and `answerClarificationFromChat()` (chat) both funnel into **`_submitClarification(id, val, src)`** — the same project-info attestation, the same `Open → Addressed → Resolved` lifecycle, the same analysis-update timing; only the reporting surface differs. `_chatClarBlock(id)` calls **`_retireClarBoxes(id)`** before emitting a new box (and `_submitClarification` retires on answer), stripping the `id` attributes off any earlier box and hiding its input. Raising the same clarification repeatedly therefore leaves **exactly one live answer box per issue** and **no duplicate DOM ids**.

No History links: the timeline is Slice 7, so no chat reply points at one.
