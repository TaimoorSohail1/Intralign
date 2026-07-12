# Slice 3 — Project Overview & Understanding Console · Frontend / UI

Single openable HTML; theme inherited 1:1 from `oslo_r1_experience_mockup_v4.html`. Dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables.

## Reused v4 patterns (pixel-matched)
- **`.confpop` / `.cpp-*`** — the confidence popover + CAF/reliability rows (v4 mockup lines 199–207, 1170–1188).
- **`.stagepips`** — the quiet stage marker (v4 line 375–376).
- **`.conf-pill`** — the top-bar pill (inherited); extended with `.cpchev`, `.flagdot`, `.flagged`.

## New / changed UI elements (Slice 3)
| Element | Selector / id | Decision | Notes |
|---|---|---|---|
| Confidence pill (clickable) | `#confpill` (`.conf-pill`) | D050 | `onclick="toggleConfPop"`, `aria-haspopup="dialog"`, chevron + neutral flag dot. |
| Confidence popover | `#confpop` (`.confpop`) | D050 | `role="dialog"`; positioned under the pill; CAF → reliability → flag → CTA. |
| CAF rows (popover) | `.cpp-d` in `#cpp-caf` | D050 | Neutral maturity bars; band words. |
| Reliability basis rows | `#cpp-cov/-evd/-asr` (+`-bar`) | D051 | Coverage · Evidence availability · **How assessable**; High/Moderate/Low. |
| Stage marker | `#ov-stage` (`.stagepips`), `#cpp-stage` | D053 | Quiet; `cursor:help`; tooltip names the three stages. |
| How-calculated | `#howcalc` + `#howcalc-pop` (`.howcalc`) | D054 | Info-glyph pill; hover + click; small explainer popover. |
| False-confidence flag (popover) | `#cpp-flag` (`.cflag`) | D052 | **Neutral** surface (`--surface-3`), info glyph; conditional `.on`. |
| False-confidence flag (card) | `#ov-flag` (`.card-flag`) | D052 | Mirrors the popover flag; neutral. |
| Why box (reliability basis) | `#whybox` / `#why-rel` | D051 | Reliability basis in prose; synced by `syncReliabilityCopy`. |
| Project summary (rich) | `#proj-summary` (`#ps-*`) | D055 | Five-beat narrative in **More**. |
| Trend row (direction-only) | `#ov-trend` / `#ov-trend-lab` | D056 | "Up — deeper analysis firmed up the read"; no magnitude. |
| Phase-bar demo | `#falseConfBtn` | D052 | "Sim false-confidence" toggle (demo scaffolding, not product chrome). |

## Color discipline (D003)
- The false-confidence flag and all confidence/CAF/reliability surfaces use the **neutral** palette (`--subtle`, `--muted`, `--surface-2/3`, neutral maturity ramp `--conf-low/medium/high`). **Severity red/amber/green appears only on issues** (unchanged from Slice 1/2).

## Accessibility
- Pill: `aria-haspopup="dialog"`, `aria-expanded` toggled. Popover: `role="dialog"`, keyboard-reachable button inside. How-calc: `role="button"`, `tabindex="0"`, `aria-expanded`; opens on hover and click.
- Focus-visible rings inherited; reduced-motion inherited (no analysis animation).
- Neutral flag dot on the pill carries a `title`; the flag itself is text, not color-only (color is never the sole signal).

## Layout constraints (DL-096/D046)
- Overview sections stay **exactly** Confidence → Start here → Progress → More. **No new standing sections. No separate reliability card.** All Slice-3 depth lives in the pill popover, subtle card markers, the Why disclosure, and the More/Project summary.

## App shell (D093/D094/D095 — shell cascade, 2026-07-09)
The approved OSLO app shell was ported in from Slice 6 so Slice 3 matches every later slice. The old top-center Overview·Attention view switch (`.vswitch` / `.vseg`) is **removed**.
- **Grid.** `#app` is now a 3-column grid `[240px sidebar | 1fr main | 340px chat]` (`grid-template-columns:240px 1fr 340px`), offset `margin-top:38px` below the phase bar; `.chat-collapsed` collapses the chat column; a `@media(max-width:860px)` turns the sidebar into a `☰`-toggled overlay drawer (`.sb-hamburger`, `.sb-scrim`, `#app.sidebar-open`), and `@media(max-width:760px)` drops the chat column.
- **Persistent left sidebar** `#appSidebar` — **PROJECT** nav only: Overview (`#sbOverview`, live) · Issues (`#sbIssues`, badge — routes to a labeled seam) · History (`#sbHistory`, Slice-7 seam) · Attention map (`#sbAttention`, live). `_syncNav()` is the single source of truth for the active highlight + `aria-current`. **The PLAN ARTIFACTS sidebar section is OMITTED** in Slice 3 (the artifact editor arrives in Slice 5). Pinned foot: bordered Tour button (`#railTour`, moved here from the old floating `.rail-tour`), Free-plan tier chip + Upgrade, and the **Your account** row (`.sb-acct`, id `#acctBtn`) — the account menu now anchors bottom-left (`left:12px;bottom:70px`).
- **Top bar.** Left: `☰` (`#sbHamburger`) · Intralign brand · project switcher `#tbProj` (Slice-8 seam, keeps `#projName`) · `sample` tag · breadcrumb `#tbCrumb` (reflects the current view). Center-right: the Confidence pill (`#confpill`, unchanged). Right cluster: search `#tbSearch` · Share `#tbShare` (Slice-9 seam) · Export `#tbExport` (Slice-9 seam) · report `#tbReport` · Free-plan chip `#tbPlan`.
- **Command palette** `#palScrim` / `.palette` (D094) — opens from `#tbSearch` and **⌘/Ctrl+K** (`openSearch()`), keyboard-operable (`↑↓`, `↵`, `esc`). Groups: **GO TO** (Overview · Issues · History · Attention map) and **OPEN AN ISSUE** (each still-open issue → light `openIssue()` panel). The **PLAN ARTIFACTS** palette group is OMITTED (no editor in Slice 3).
- **Seam panes** (`.hist-seam` styling, labeled — never a wrong/broken view): `#pane-issues` ("Full Issues view arrives in Slice 6"), `#pane-history` ("History & timeline — arrives in Slice 7").
- **Nav chrome is neutral/brand** (D003): sidebar count badges (`.sb-badge`) are neutral; severity red/amber/green stays on issue badges only.

## Chat integration (D108 cascade)

The OSLO rail's composer is no longer inert. The D108 conversational chat was ported in from Slice 8 and **adapted to the surfaces that exist in Slice 3** — the confidence-led Overview + understanding console, the basic Attention map, the light issue panel, and the clarification loop. The chat never offers an action this slice cannot actually run.

**Markup.** `#chatCtx` context pill (`.cx-lab` / `.cx-v` / `.cx-x` × clear, `clearChatContext()`) sits between the chat header and the scroll. `#chatscroll` is now `role="log" aria-live="polite" aria-relevant="additions"` and holds a first-run empty state (`#chatEmpty`, removed by `_chatDropEmpty()` on the first message). The composer gains `#chatChips` (state-derived suggested prompts), a live `#chatInput` (`onkeydown="chatKey(event)"`), and a live `#chatSend` (`onclick="sendChat()"`).

**CSS (neutral chrome only, D003).** `.chat-ctx`, `.chat-empty`, `.chat-chips`/`.chat-chip`, `.chat-acts`/`.chat-act`, `.chat-clar` (+`.answered`), `.howcalc.askwhy`, `.ip-askrow`. The chat never wears severity color as decoration; severity words stay inline in copy. `.cmsg.user` already existed.

**Composer.** `sendChat()` (click) · `chatKey()` — **Enter sends, Shift+Enter newlines**. `pushUserChat()` renders the user's turn (always `_chatEsc()`-escaped). `chatChip()` fills the composer and sends through the identical path.

**State grounding (`_chatState()`).** Every reply derives from the live model — `currentRead()` (index/band/reliability + its basis/stage), `_chatCaf(r)` (the same Clarity/Alignment/Feasibility rows `renderDims()` paints, so the chat and the console cannot disagree), `ISSUES`/`_istatus`, `ANALYSIS_STATE`, `PLAN_SECTIONS`, `_openClarIds()`. No invented numbers, no invented issues. `_oslloReply()` does prototype-grade keyword routing into the `_ans*` builders: `_ansConfidence` · `_ansNext` · `_ansIssue` · `_ansDimension` · `_ansArtifact` · `_ansCell` · `_ansHowIssuesClose` · `_ansClarifications` · `_ansSummary`.

**Entry points (only Slice-3 surfaces).**
- **Overview confidence card** → `#askWhyConf` "✦ Ask OSLO why" pill (same shape as "How this is calculated", sits directly beneath it) → `askOslo({type:'confidence'})`. This is the **deep** answer in Slice 3 — the console is here, so `_ansConfidence()` returns the limiting CAF dimension, all three CAF rows, the **reliability basis** (Coverage · Evidence availability · How assessable), the **understanding stage**, the **false-confidence condition** when it holds, and **what would move the read**.
- **Light issue panel** → `.ip-askrow` "✦ Ask OSLO about this issue" → `askOslo({type:'issue',id})`.
- `askOslo({type:'cell',art,dim})` is wired in the answer layer but has **no Attention-map affordance in Slice 3** (the map here is the basic Slice-2 one).

**Advisory-only (D001).** The chat mutates nothing. Every action it offers is a `.chat-act` **link the user clicks**, and each one calls a function that **already exists in Slice 3** — `openIssue()` · `showView()` · `showSectionIssues()` · `openCell()` · `toggleConfPop()`. No `applyFix`/`selectPath`/Discuss (S6), no `openArtifact` (S5), no History links (S7).

**Clarifications — ONE path.** `answerClarification()` (panel) was refactored to delegate to the new shared **`_submitClarification(id, val, src)`**; `answerClarificationFromChat(id)` calls the **same** function with `src:'chat'`. `src` changes only **where progress is reported**, never what the answer **does** to the model (project info → `basis:'attested'` + reliability lift; `_istatus[id]='resolved'` via the analysis update; the same `renderOverview/renderFocus/renderClarifications/renderPlanSections/renderHeat/renderDims/updateIssueCounts` re-render). The chat is **not** a side channel.

**Copy.** "Analysis update", never "reanalysis" as a mechanism (D092); "Issues", never "Findings" (D017). The chat never claims to have closed an issue.
