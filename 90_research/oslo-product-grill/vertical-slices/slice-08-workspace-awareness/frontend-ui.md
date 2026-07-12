# Slice 8 — Multi-Project Workspace & Awareness · Frontend UI

Cumulative Slices 1–8. Single openable `prototype.html` (inline CSS/JS + `localStorage`, D016). This documents the Slice-8 UI surfaces, DOM, CSS and functions. Slices 1–7 UI is unchanged except for the four rewired seam handlers and the added top-bar bell.

## Rewired seams (top bar / account)
- **Logo → Workspace Home:** `.tb-brand` gains `role="button" tabindex="0" onclick="showWorkspace()"` + Enter/Space handler (was `title` only).
- **Project switcher:** `#tbProj` `onclick` changed `openProjectSwitcher()` (stub) → `toggleProjMenu(event)`; `aria-haspopup="menu"`.
- **Notifications:** new `#tbNotif` (`.tb-ic.tb-notif`) button with `.nbadge#nbadge`, before the Free plan chip.
- **Settings:** `openSettings()` (was a stub toast) now shows the `#settings` surface; the account-menu **Settings** item and the sidebar **Your account** row both reach it.
- **Upgrade:** `openUpgrade()` (was a stub toast) now shows the `#upgradeScrim` prompt.
- Legacy `openProjectSwitcher()` kept as an alias → `toggleProjMenu()`.

## Workspace Home — `#workspace` (D102)
Full-viewport overlay (`position:fixed;inset:0;z-index:120;display:none` → `.show` = `display:flex`), "Workspace" context.
- `.ws-top` — brand (*Intralign · Workspace*) + `.ws-planchip` (Free · Upgrade) + `#wsNotif` bell (`.nbadge#nbadgeWs`) + account avatar → `openSettings()`.
- `.ws-body` → `.ws-h` (title + **+ New project**) → `.ws-sech "★ Pinned"` + `#wsPinned` grid → `.ws-sech "Recent"` + `#wsRecent` grid → `.ws-noscore` **no-computed-scores** note → `.ws-sech "Archived (N)"` (`#wsArchCnt`) + `#wsArchived` → `.ws-note` footer.
- Card = `button.ws-card`: `.ws-cardtop` (`.ws-name` + `.chip`), `.ws-conf` (neutral `.conf-dot` + "Understanding **{band}** · qualified by {reliability} reliability"), `.ws-meta` (Analyzed/`.ws-stale` chip + recency + issues + artifacts), `.ws-tags` (`.ws-tag` Owned/Shared + `.ws-tag.pin`).
- New card = `.ws-card.ws-new`; archived = `.ws-arch-card` + `.ws-restore`.
- **Rendered by** `renderWorkspace()` (`_wsCard`, `_wsArchCard`).

## Project switcher — `#projmenu` (D103)
`.projmenu` fixed dropdown (`z-index:230`, `.open` shows), positioned under `#tbProj`. Rendered live by `renderProjMenu()`: `.pm-lab`, `.pm-item` rows (`.pm-dot` + `.nm` + `.pm-stale`/`.chip`), `.pm-sep`, **New project**, **Workspace Home**. `toggleProjMenu()` / `closeProjMenu()`; ESC + outside-click close.

## Notifications — `#notifpanel` + `#notifScrim` (D104)
Right drawer `.notifpanel` (`transform:translateX(106%)` → `.open` = `none`; `z-index:236`) + `#notifScrim` (`z-index:235`).
- `.np-h` (title + `.np-close`), `.np-tools` (`.np-mark` "Mark all read" + `#npUnread`), `#np-list` (`role="list"`), `.np-foot` (**"never triggers an analysis"** note).
- Item = `button.np-item[.unread|.read]`: `.np-dot` + `.np-ic` + `.np-b` (`.l` / `.m` / `.tm` + `.np-cat`).
- Bell + badge: `.tb-notif` + `.nbadge` (neutral/brand `var(--primary)`; `.zero` hides at 0).
- **Rendered by** `renderNotif()`; `openNotif`/`closeNotif`/`markAllNotifRead`/`notifGo`/`updateNotifBadges`.

## Settings — `#settings` (D105)
Full-viewport overlay (`z-index:122`). `.set-top` (brand → `closeSettings()` + Back) → `.set-main` grid `216px 1fr`:
- `.set-nav` — grouped keyboard-operable `button.set-navbtn[data-sec]` (You / Workspace / Plan); `.vtag` "view" markers on visibility-first areas.
- `.set-scroll#setScroll` — `h1` + intro + eleven `section.set-sec#sec-<sec>` blocks, each `h2` (+ `.set-vis` tag) + `.set-card` of `.set-row`s. Appearance uses `.segwrap`/`.segbtn`; toggles use `.tog`/`.tog.on`.
- `setNav(sec)` highlights the nav button and `scrollTo`s the section (fallback `scrollTop`), then focuses the button. `openSettings`/`closeSettings`.

## Upgrade-or-archive — `#upgradeScrim` (D048)
Reuses `.scrim`/`.modal`. `.up-plan` chip + `h2` + copy + `.up-opts` (two `button.up-opt`: Upgrade → Settings→Subscription; Archive → `archiveAndCreate()`) + Not-now. `openUpgrade`/`closeUpgrade`.

## Appearance / theme (D106)
- Tokens pre-exist: `:root` (dark) + `:root[data-theme="light"]` overrides (identical token names).
- `setTheme(t,save)` sets/removes `data-theme` on `documentElement`, persists `LS.theme`, calls `syncThemeToggle()`. `currentTheme()`, `matchSystemTheme()`, `initTheme()` (boot; system fallback + `matchMedia` listener).
- Segmented control `#thDark`/`#thLight` (`aria-pressed`). Reduced-motion `@media` + `:focus-visible` ring pre-exist and are honored.

## CSS added (one block before `</style>`)
Workspace (`#workspace`, `.ws-*`), switcher (`.projmenu`, `.pm-*`), notifications (`#notifScrim`, `.notifpanel`, `.np-*`, `.tb-notif`/`.nbadge`), settings (`#settings`, `.set-*`, `.segwrap`/`.segbtn`, `.tog`), upgrade (`.up-*`). Neutral chrome throughout; understanding dots use the maturity ramp; the unread badge uses `var(--primary)` (never severity). All new interactive elements have `:focus-visible` rings.

## JavaScript added (one module before the ACCOUNT MENU section)
`PROJECTS[]`, `NOTIFS[]`, `_bandDot`, `_ensureApp`; theme (`currentTheme`, `setTheme`, `syncThemeToggle`, `matchSystemTheme`, `initTheme`); workspace (`showWorkspace`, `closeWorkspace`, `renderWorkspace`, `_wsCard`, `_wsArchCard`, `openProject`, `restoreProject`); switcher (`renderProjMenu`, `toggleProjMenu`, `closeProjMenu`); notifications (`updateNotifBadges`, `renderNotif`, `openNotif`, `closeNotif`, `markAllNotifRead`, `notifGo`); settings (`openSettings`, `closeSettings`, `setNav`); upgrade (`openUpgrade`, `closeUpgrade`, `wsNewProject`, `archiveAndCreate`); a global ESC handler (upgrade → notif → switcher → settings → workspace) + a switcher outside-click closer. Boot wires `initTheme()` + `updateNotifBadges()`.

---

# Revision 2 — D107 gap-analysis refinements

Edited in place. Everything above still holds except where restated here.

## 1. No dead affordances in Settings
Every `<a role="button" tabindex="0">` in `#settings` is **gone** (`#settings a` count = 0). Each row is now exactly one of: a real control, an honestly-labelled seam, or plain text.

**New CSS:** `.set-input`, `.set-edit`, `.set-saved(.on)`, `.set-btn(.primary|.danger)`, `.swx` (switch), `.set-catrow`/`.set-cat-r`/`.set-cat-state`, `.set-later`, `.set-hint`, `.set-search*`, `.set-noresult`, `.sr-only`, `.np-empty`, `.ws-cta`, `.ws-detail`, `.ws-card.full`, `.ws-empty`, `.ws-multi-note`.

**Functional rows (persisted to `localStorage`):**
- **Profile** — `#setName` (display name) + `#setRole` → `saveProfileName()` / `saveProfileRole()` → `LS.profileName` / `LS.profileRole`.
- **Workspace** — `#setWsName` → `saveWorkspaceName()` → `LS.wsName`.
- **Account** — `#setStay` (`role="switch"`, `toggleStayApp()`), **Sign out** (`signOutFromSettings()` → `logout()`), **Delete account…** → `openDeleteConfirm()`.
- **Notifications** — six `role="switch"` buttons rendered by `renderNotifPrefs()` → `toggleNotifCat(k)` → `LS.notifPrefs`.
- **Subscription** — `See plans` → `openUpgrade()`. **Appearance** — `Match system` is now a `<button>`.

**Identity reflection:** `applyIdentity()` paints `[data-username]`, `[data-avinitials]`, `[data-wsname]`, `[data-wsinitial]` (top bar, Workspace Home top bar, Settings top bar, sidebar account row, account menu, Membership row) plus the `#setAvPreview` / `#setWsAvPreview` initials. `_initials(n)` derives the avatar text. Called on boot, on `openSettings()`, and on every keystroke of the three name inputs.

**Delete account:** new `#deleteScrim` (`.scrim`/`.modal`) — `openDeleteConfirm` / `closeDeleteConfirm` / `confirmDeleteAccount` (closes + honest toast; nothing is destroyed). ESC closes it first in the stack.

**Stay-signed-in:** `toggleStayApp()` now delegates painting to the new `syncStayToggle()`, which keeps `#amStay` (account menu) and `#setStay` (Settings) on one state.

## 2. Awareness categories (D104 + Slice-9 gate)
`NOTIF_CATS[]` (key · label · `later` · note) + `NOTIF_PREFS` (persisted; collaboration keys force-set to `false` at load). `_notifOn(cat)` / `_visibleNotifs()` filter `renderNotif()` and `updateNotifBadges()`. `mention` · `reply` · `shared with me` switches render `disabled aria-disabled="true"` with a `.set-later` "Arrives with Collaboration" tag; their seed items stay in `NOTIFS[]` but never render in Alpha. The retained items (analysis complete / failed / stale) now all reference **DevNorth 2026**. Empty list → `.np-empty` "You're all caught up". `#npMark` disables at zero unread.

## 3. Workspace Home — Alpha 1-project presentation (D102/D048)
`ALPHA_SINGLE = true`, `FREE_ACTIVE_CAP = 1`; `_visibleProjects()` / `_activeProjects()` / `_archivedProjects()`. Illustrative registry rows carry `illustrative:true` and are hidden in Alpha (grid code retained and returns automatically at 2+ active).

`renderWorkspace()` now branches: **0 active** → `#wsEmpty` (restore + new-project actions) · **1 active** → `#wsSingleHead` + `#wsSingle` ("Your project", `_wsCard(p, true)` with `.ws-detail` + `.ws-cta`) · **2+** → the original `#wsPinned` / `#wsRecent` grids. `#wsMultiNote` explains when Pinned/Recent appear. `#wsArchived` unchanged; the no-computed-scores note is untouched. `archiveAndCreate()` really archives (non-destructive) and `restoreProject()` really restores the real project — which is what makes the zero-project empty state reachable. `wsNewProject()` → upgrade prompt at the cap, else `wsStartIntake()` (the real intake). New phase-bar demo trigger `#staleBtn` → `toggleStaleProject()`.

## 4. Light-mode AA sweep (`:root[data-theme="light"]`)
Token values changed (component code untouched):

| token | was | now | why |
|---|---|---|---|
| `--subtle` | `#79818B` | `#666D77` | 3.78:1 on `--bg` → **5.01:1** (it is used for small text everywhere) |
| `--primary-light` | `#B45309` | `#A34A07` | 4.44:1 on the 12% brand tint (`.set-navbtn.active`, `.sb-nav.active`, chips) → **5.24:1**; 5.93:1 on surface |
| `--warning` | `#A8791F` | `#8A6100` | 3.87:1 on surface → **5.54:1**; 4.90:1 on the amber heat tint |
| `--conf-low` | `#C7CCD3` | `#7F8792` | 1.3:1 → **3.63:1** (graphical object, AA 1.4.11) |
| `--conf-medium` | `#8C939D` | `#4A515A` | keeps the ramp monotonic (3.63 → 8.03 → 16.56) |
| `--conf-high` | `#2C333B` | `#1B1F24` | ditto |
| `--color-focus` | `#B45309` | `#A34A07` | tracks `--primary-light` |

`--primary` (`#D97A3A`) is **fill/border only** and is never used as text — verified by grep; on white it is 3.09:1, which clears the 3:1 non-text threshold, and `--primary-fg` on it is 5.36:1, so buttons/badges/segmented controls keep AA. The maturity ramp stays **pure neutral grey** (no hue) and severity keeps its hue, so issues stay distinguishable from the ramp in light.

## 5. Polish
- `filterSettings(q)` / `clearSettingsSearch()` — `#setSearch` filters the eleven `.set-sec`s **and** their `.set-navbtn`s (+ empties the group headings), `#setNoResult` on zero, `#setSearchCount` (`.sr-only`, `aria-live`) announces the count. Escape inside the box clears it.
- Stale project card → `.ws-cta` "→ Open to bring the read up to date".
- Empty states: notifications (`.np-empty`) and zero-project workspace (`.ws-empty`).
- `resetDemo()` also clears `profileName`, `profileRole`, `wsName`, `notifPrefs`.

## Verification (Revision 2)
- `node --check` on the extracted script: **PASS** (single `<script>` block, 270,879 chars).
- jsdom structural parse (no `runScripts`): `body.children.length = 23` (> 0); 11 settings sections intact.
- jsdom runtime (`runScripts:"dangerously"`): **56/56 assertions pass, 0 errors** — 0 dead affordances and 0 `<a>` in Settings; profile/workspace name edits persist and reflect in the shell; category switches filter the panel; Sign out + Stay-signed-in in Account; honest seam labels (no internal spec phrasing anywhere); collaboration categories gated + labelled; Alpha 1-project dashboard (Pinned/Recent hidden at 1); theme flips + persists; settings search filters; both empty states reachable; prior slices intact.
- Contrast harness over the light tokens: **21/21 combinations pass** at their AA threshold (4.5:1 text, 3:1 non-text).

---

# Revision 3 — D108 · Conversational OSLO (chat is functional + integrated)

The chat rail was inert: the composer `<textarea>` had no `id` and no handler, **Send had no `onclick`**, and there was no send/reply logic — a read-only notice feed. No surface handed it context, and the canonical v4 recommendation action **Discuss** was missing. D108 makes the chat work and wires it into the workflows.

## 1. The composer (`#chatInput` / `#chatSend`)
- `sendChat()` — Send click; `chatKey(e)` — **Enter sends, Shift+Enter newlines**.
- `pushUserChat(text)` renders the user's turn (`.cmsg.user`, always escaped via `_chatEsc`); `pushChat(html, cls)` is unchanged for OSLO turns and still carries the existing fast-pass/deep-pass completion notices.
- `#chatscroll` is now `role="log" aria-live="polite"`; `#chatEmpty` is the first-run state and is removed by the first message.

## 2. State-grounded replies (simulated, never fabricated)
`_chatState()` derives the answer's facts from the live model on every turn: `currentRead()` (index · band · reliability basis · stage), the CAF rows (`_chatCaf` — Clarity/Alignment fixed, **Feasibility tracks the live read**), the **limiting dimension** (lowest CAF), open/addressed/resolved issue counts + the most-severe open issue, the open clarifications (`_openClarIds`), `ANALYSIS_STATE`, and the open artifact (`_curArt`).

Answer builders: `_ansConfidence` · `_ansNext` · `_ansIssue` · `_ansDimension` · `_ansArtifact` · `_ansCell` · `_ansRecommendation` (Discuss) · `_ansHowIssuesClose` · `_ansClarifications` · `_ansSummary` (fallback).
Routing: `_oslloReply(q)` — keyword intents (next / issue by id or name / advisory boundary / CAF dimension / confidence / artifact / clarification), then **the active context**, then a grounded summary. `_matchIssueQ` / `_matchArtQ` resolve names and ids. Prototype-grade; no real AI.

**Advisory-only (D001).** Replies never mutate: every action is a link (`_cAct` → `.chat-act`) that calls the **existing** function (`openIssue` · `openArtifact` · `openFindingsFor` · `applyFix` · `selectPath` · `showView`). Asking OSLO to "just fix it" returns the boundary: issues reach **Resolved** only via an **analysis update** (D088/D092) — never a manual step, never "OSLO did it".

## 3. Context handoff — `askOslo(ctx)` + the context pill
One entry point: `askOslo({type:'issue'|'span'|'artifact'|'confidence'|'cell'|'recommendation', id?, art?, dim?, pathIndex?})`. It stands down the Issue panel / annotation popover, opens + focuses the rail, sets `#chatCtx` (**"Context · Venue Wi-Fi capacity is unconfirmed (ISS-01)"**) with an **× clear** (`clearChatContext()`), seeds a context-appropriate opening message, and rebuilds the chips. Subsequent turns are answered **within** that context until it is cleared.

## 4. Entry points wired
| Surface | Affordance | Call |
|---|---|---|
| Issue panel | `✦ Ask OSLO about this issue →` (`.ip-ownfix`) | `askOslo({type:'issue',id})` |
| Issue panel · clarification | `Answer in chat →` (in `.cl-foot`) | `askOslo({type:'issue',id})` |
| Recommendations · OSLO Recommended | **`Discuss`** button (beside Apply this fix) | `askOslo({type:'recommendation',id,pathIndex:null})` |
| Recommendations · each resolution path | **`Discuss`** (`.ip-discuss`, `event.stopPropagation()`) | `askOslo({type:'recommendation',id,pathIndex:ix})` |
| Artifact toolbar | `✦` (`#artAskBtn`) | `askOslo({type:'artifact',id:name})` |
| Annotation popover (`#annoPop`) | `Ask about this →` | `askAboutSpan(id)` → `askOslo({type:'span',id})` |
| Overview confidence card | `✦ Ask OSLO why` (`#askWhyConf`, beside the number) | `askOslo({type:'confidence'})` |
| Attention cell → scoped Issues header | `Ask OSLO about this cell →` (shown when artifact **and** dimension are both scoped) | `askOslo({type:'cell',art,dim})` |

**Discuss never selects.** It only opens the conversation; `_ansRecommendation` weighs the path against the alternatives and *offers* `Select this path →` / `Apply this fix →` as links. Selection stays the user's explicit action (`selectPath`), taken in the issue.

## 5. Clarifications are conversational — one path, one History
`_chatClarBlock(id)` renders the question + an inline answer box in the thread. `answerClarificationFromChat(id)` echoes the answer as the user's turn and calls **`_submitClarification(id, val, 'chat')`** — the same function `answerClarification(id)` (the panel) now calls with `'panel'`. Identical project-info update (artifact → *Confirmed by you*, reliability bump), identical lifecycle (**Addressed → analysis update → Resolved**), and the **identical `pushHistory` events** (`clarification` + `issue_lifecycle`) and `pushTrend` point (D096). `src` only decides which surface reports back. There is no side channel around governance or the timeline.

## 6. Polish / a11y
- **Suggested chips** (`#chatChips`, `renderChatChips()` / `chatChip()`): state-derived and context-aware — unscoped they read *"What should I do next?" · "Why is {limiting dim} {level}?" · "Explain the top issue"*; they fill the composer and send. Rebuilt by `_refreshIssueSurfaces()` so they track the live read.
- Replies **link to the surface** they reference rather than only describing it.
- a11y: live-region message list; labelled composer and answer boxes; chips/Discuss/actions are `<button>` or `role="button" tabindex="0"`; a delegated keydown makes in-thread links Enter/Space-operable.
- Neutral chrome (D003) — the chat carries no severity color; severity stays a word in the copy.

## Verification (Revision 3)
- `node --check` on the extracted script (single `<script>` block): **PASS**.
- jsdom structural parse (no `runScripts`): `body.children.length = 23` (> 0).
- jsdom runtime: **65/65 assertions pass, 0 errors** — Send + Enter send, Shift+Enter doesn't; replies quote the live index/band/limiter and link to the surface; all six entry points set the right pill and opening message; clear-context works; **Discuss does not mutate `_selpath`/`_istatus`**; chips fill+send; clarification-in-chat produces the **same state change and the same History events** as the panel path; prior slices intact.

---

# Revision 4 — D109 · Chat UX refinements (epistemic replies · citations · AI-native interaction)

D108 made the chat *work*. D109 makes it **OSLO** — the rail now inherits the product's epistemic doctrine instead of merely quoting its numbers. Edited in place; every prior slice and every D108 behavior is preserved.

## 1. Epistemic replies (P1)
- **`_relBlock(S)`** — appended to every substantive answer. The qualifier is read off the **live `currentRead()`**: `r.relWord` (High/Moderate/Low/Very Low) picks the sentence from `_RELQUAL`, and the basis line prints the real `r.reliability` triple (Coverage · Evidence availability · How assessable). `falseConfidenceHolds(r)` adds the *"Read this with care"* line. `.chat-rely.thin` when reliability is Low/Very Low.
- **`_epiOf(name)` / `_epiWord()` / `_epiBlock([names])`** — the **derived vs attested** distinction from real state: `PLAN_SECTIONS[].basis` (which `applyFix()` and `_submitClarification()` actually mutate), overridden by the live editor DOM (`#artdoc [data-epi="attested"]`) when that artifact is open. Renders as a chip: *"Resources: From OSLO"* / *"Resources: Confirmed by you"*.
- **`_thinBasis(name, S)`** — the honesty gate. When the basis is **derived-only** *and* (the artifact's `rel` is Low **or** the read's reliability is Low), the reply says **"I inferred this — it isn't confirmed in your inputs"** instead of asserting.

## 2. Citations / provenance (P1)
`_cite(act, src, quote)` → `.chat-cite` buttons under the message, grouped by `_cites()` under *"What this rests on"*. Each routes to the **owning surface**:
- **issue** → `_citeIssue(id)` prints the real `ISSUES[id].ev[]` evidence pairs (*"Resources · Vendors — 'Venue — rooms, power, Wi-Fi (must confirm 500-person Wi-Fi capacity)'"*) → `openArtifact(f.sec)`; plus the issue itself → `openIssue(id)`.
- **read** → `_citeRead(S)`: the CAF limiting dimension + the reliability basis → `chatOpenConfidence()` (Overview + confidence popover); the top open issue → `openIssue()`.
- **artifact** → `_citeArt(name)`: body + epistemic state → `openArtifact()`.
- **what changed** → `_citeRun()`: the newest `analysis_run` from `HISTORY` → `histFocusRun(_slug(e.run))`.

## 3. Honest fallback (P1) — no canned summary standing in for an answer
- **`_ansFallback(q, S)`** replaces `_ansSummary` as route 10: *"I don't have a grounded answer to that — so I'm not going to invent one"*, then `_capList()` (what OSLO can actually do) + working chips. It carries **no reliability block and no citations** — there is no claim to qualify or source.
- **`_outOfScope(t)`** (route 0b) catches "draft an email", "book the venue", "handle it for me" → **`_ansOutOfScope()`**: *"That's outside what I do."* "Just fix it" still lands on `_ansHowIssuesClose()` (the D001/D088 boundary), now with the capability list.
- `_ansSummary` remains reachable via an explicit *"where do I stand / status"* route (7b).
- New route 1b: **`_ansChanged(S)`** — "what changed" off `HISTORY` + `TREND` (direction-only, D056/D097).

## 4. Streaming + message actions (P2)
- **`_thinkingEl()`** renders *"OSLO is reading your plan…"* (`.cmsg.chat-think`), then `_streamInto(bub, done)` reveals the **already-rendered** reply word-by-word by blanking and refilling its text nodes via a `TreeWalker` — the DOM (and every action/citation in it) is never rebuilt mid-stream. Time-boxed to ~1.15s (`TICKS = 44`, adaptive budget). `.bub.streaming` hides the action/citation/follow-up blocks until the reply lands. **`_reduceMotion()`** (`prefers-reduced-motion`) → no thinking state, no streaming, instant render. `_chatFlush()` snaps an in-flight stream to done, so sending again never drops a question.
- **`_msgActs(rec)`** → `.msg-acts` on every OSLO reply: **Copy** (`chatCopyMsg`), **Retry** (`chatRetryMsg` — re-answers from the read *as it stands now*), **👍/👎** (`chatFeedback`, presentation-only, persisted), **Save to History** (`chatSaveToHistory` → `pushHistory('chat_note', …)`, append-only, D096). All `<button>`, all keyboard-operable. Completion notices (`cls==='done'`) carry no action bar.
- New History type **`chat_note`** registered in `_histicon` (`✎`), `_histCatOf` (`decisions`) and `_histCatLabel` (**"Your note"** — no enum leak).

## 5. Context & control (P3)
- **`_follow([...])`** — 2–3 contextual follow-up chips per answer, derived from that answer (after an issue: *"Compare the resolution paths" · "What evidence supports this?" · "What would move Feasibility?"*). They reuse `chatChip()`, so they take the same path as a typed question.
- **`@`-mention + multi-context** — `chatComposerInput()` detects `@…` at the caret and opens `#chatMention` (`_mentionItems()` — issues, the 7 artifacts, the 3 CAF dimensions; loose matching so "wifi" finds "Wi-Fi"). ↑/↓/Enter/Tab/Esc navigate it. `chatPickMention()` strips the `@token` and calls **`pinChatContext()`**. The pill area is now **multi**: `_chatCtx` (the handed-in context) + `_chatPins[]`, rendered as removable `.cx-pill`s in `#chatCtxList` (`unpinChatContext(i)`). **`_ansPins()`** appends a grounded roll-up (*"Also in view"*) so answers demonstrably use every pinned context. New context type: `dimension`.
- **Expand mode** — `toggleChatExpand()` toggles `#app.chat-wide` (`grid-template-columns:240px 1fr 560px`); persisted as `LS 'chat-wide'`, restored in `seedChat()` via `_chatApplyExpandPref()`.
- **Consequence-stating actions** — `_cAct(onclick, label, cons)` now takes a consequence, rendered as `.ca-cons` beneath the label and as the `title`: *"Apply this fix → Drafts the change into Resources; the issue moves to Addressed and your read updates after the analysis run."* (`_consApply` / `_consSelect` / `_CONS_OPEN_ISSUE` / `_CONS_DISCUSS`). Still user-initiated — the chat never acts.

## 6. Persistence & polish (P4)
- **Per-project thread persistence** — the thread is a record set (`_CHAT_MSGS`), projected to DOM by `_chatMount()`. `_chatPersist()` writes the last 60 records to `LS 'chat-thread-<projectId>'` (`_chatProjKey()` — `devnorth` / `new` for the anon run); `_chatRestore()` rebuilds it in `seedChat()`. **Nothing is regenerated on restore** — restored turns are exactly what was said, and any clarification box from a past turn is stood down (`.superseded`, disabled) so no stale box can fire. `resetDemo()` clears the thread keys.
- Replies **lead with the so-what**, then detail. Keyboard: **⌘/Ctrl+Shift+K** focuses the chat, **⌘/Ctrl+Enter** sends from anywhere in the rail, **Esc** closes the `@` picker or clears the pinned contexts. *(⌘/Ctrl+K remains the D094 command palette — that prior-slice binding was not taken.)*
- **Teaching empty state** — three example questions as one-click buttons + the keyboard hints.
- **The advisory boundary lives in ONE home** (§6.7): the composer's `↳ advisory` chip and its hover tip. Generic boundary boilerplate was pulled out of the answer bodies; the substantive D088 lifecycle facts (what selecting/applying actually does) stay, and now appear as **consequences on the actions themselves**.

## CSS added (one D109 block after `.chat-clar`)
`#app.chat-wide` · `.chat-exp` · `.chat-rely(.thin)` · `.chat-epi .ep(.attested)` · `.chat-cites` / `.chat-cite` · `.chat-acts.cons` / `.ca-cons` · `.chat-pins` · `.cmsg.chat-think` + `@keyframes cthink` · `.bub.streaming` · `.msg-acts` / `.msg-act` · `.chat-follow` · `.chat-mention` · `.cx-pill` · `.chat-empty .ce-ex/.ce-q/.ce-k` — plus a `prefers-reduced-motion` block that kills the thinking dots and the stream caret. Chrome stays **neutral** (D003): no severity color anywhere in the rail.

## Verification (Revision 4)
- `node --check` on the extracted script (single `<script>` block): **PASS**.
- jsdom structural parse (no `runScripts`): `body.children.length = 23` (> 0).
- jsdom runtime, **0 JS errors**: replies carry a reliability qualifier + the derived/attested chip; the thin-evidence line fires on Resources (derived + Low); citation chips render from the real `ev[]` pairs and route (clicking one opened the Artifacts pane on Resources); an off-script question ("what is the weather in Oslo tomorrow?") yields the honest fallback — **no fabricated number, no citations, no reliability claim**; "draft an email to the venue" yields the out-of-scope boundary; the thinking state appears then resolves, and renders instantly under `prefers-reduced-motion`; Copy / Retry / 👍 / **Save to History** work (History gains one `chat_note`, shown as *"Your note"*); follow-up chips are contextual and answer when clicked; `@` pins **3** contexts (issue + artifact + dimension) and the answer's *"Also in view"* block uses them; expand mode toggles and persists; action links state their consequences; the thread survives a **simulated reload** (fresh document, seeded `localStorage` → 10 records restored with their citations, actions and saved state); **Discuss still leaves `_selpath`/`_istatus` untouched**; the chat mutated nothing else (read, issue statuses unchanged — the only History growth was the note the user explicitly saved); prior slices (Attention map, artifact editor, Issue panel, History, clarification-through-chat) intact.
