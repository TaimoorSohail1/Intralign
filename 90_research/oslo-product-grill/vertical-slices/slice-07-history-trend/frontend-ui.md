# Slice 7 — History & Confidence Trend · Frontend UI

Cumulative Slices 1–7. Single openable `prototype.html` (Tailwind-independent inline CSS/JS + `localStorage`, D016). This documents the Slice-7 UI surfaces, DOM, CSS, and functions. Slices 1–6 UI is unchanged except where noted (the History seam is replaced).

## History pane — `#pane-history` (D096)
Replaces the Slice-6 seam (`.hist-seam` "arrives in Slice 7"). DOM (inside `.pane#pane-history`):
- `.hist-pane` wrapper.
  - `.hist-head` → `h1 "History & timeline"` + `.hist-sub "append-only · prior states retained"` + a single `.info` ⓘ (hover: prior states never overwritten; viewing changes nothing; only an analysis update changes the assessment).
  - `#hist-trend` — the **"Understanding over runs"** sparkline (D097), rendered by `renderHistTrend()`.
  - `#hist-list` (`.hist-list`) — the append-only event rows, rendered by `renderHistory()`.
  - `#hist-first` (`.hist-first`, hidden by default) — the **first-run minimal state** (D100).
  - `.hist-ro` — the **"Read-only · viewing history changes nothing"** foot note + a ⓘ (D098g).

### Event rows (`renderHistory()`)
Each event → `.hrow` (`div`), or `.hrow.clickable` for `artifact_version` rows (D099):
- `.hicon` — the type glyph (`_histicon[type]`; `aria-hidden`).
- `.hbody` → `.hlab` (label + `.hstate` **current**/**prior** tag + optional `.hview "view snapshot →"`), optional `.hd` (detail), `.ht` (illustrative timestamp + mono `type`).
- Version rows carry `onclick="histVersionNote(id)"` and are keyboard-operable (`role="button" tabindex="0"`, Enter/Space → same handler).
- The **first-run** predicate (`HISTORY.length ≤ 1 && TREND.length ≤ 1`) toggles `#hist-first` on and renders the single seed row.

### Trend (`renderHistTrend()` → `#hist-trend`)
- `.ct-h` header: **"Understanding over runs"** + ⓘ (rises or falls; a fall usually means deeper analysis found something real) + right-aligned "rises or falls with the read".
- `<svg>` polyline + point circles, stroke `var(--conf-medium)` (**neutral maturity, never severity color** — D003); each circle has a `<title>` = `{run} — {band}: {cause}` (band-qualified + cause-bound, D097). `role="img"` + `aria-label`.
- `.ct-x` per-run captions: `{run} {band}` + ▲ (`var(--success)`) / ▼ (`var(--warning)`) direction arrow (direction-only, no magnitude) + a `.cause` sub-line.

## CSS added (near the retired `.hist-seam` block)
`.hist-pane`, `.hist-head`/`h1`, `.hist-sub`; `.hist-trend`, `.ct-h`, `.ct-x`, `.ct-x .cause`; `.hist-list`, `.hrow`, `.hrow.clickable` (+ `:hover`/`:focus-visible`), `.hicon`, `.hbody`, `.hlab`, `.hd`, `.ht`, `.hview`, `.hstate`, `.hstate.cur`; `.hist-first` (+ `.hf-ic`/`.hf-t`/`.hf-s`); `.hist-ro`. Values match the v4 reference (`.hrow`/`.hicon`/`.hstate`, `.ct-h`/`.ct-x`). The old `.hist-seam*` classes remain only as unused fallback styles.

## JavaScript added
- **Data:** `HISTORY[]` (seed = Initial Analysis), `TREND[]` (seed = Initial point), `_hEventSeq`, `_histicon{}`, `_deepHistDone`.
- **Append (append-only):** `pushHistory(type,label,{d,cur,ver})` (unshift newest-first; live re-render if pane active); `pushTrend(run,index,band,cause)` (push; live re-render).
- **Render:** `renderHistTrend()`, `renderHistory()` (+ first-run toggle).
- **Version lineage:** `histVersionNote(evId)` → `_stubToast(...)` read-only note (D099).
- **Routing:** `showView('history')` now calls `renderHistTrend()` + `renderHistory()` on entry (still toggles `#pane-history.active`, `_setCrumb`, `_syncNav`). `openHistorySeam()` **redefined** to `closeIssue(); showView('history')` — the Overview "Timeline →" and Issue-panel "Open full timeline →" pointers now route to the real pane (no seam modal). The retired `#historyScrim` markup + `closeHistorySeam()` remain inert.

## Wired live-append points (existing functions extended)
- `deepComplete()` — appends the Extended run (`reanalysis_run`, current), 7 retained versions (`artifact_version`), 6 detected issues (`issue_lifecycle`), and an Extended `TREND` point — **once** (`_deepHistDone`).
- `deepFail()` — appends a `last_good` row (D098g); trend untouched.
- `applyFix(id)` — appends `selected_path` (applied) + a tied-artifact `artifact_version` (bumped via `LS.set(_artKey(sec)+'-ver', …)`), then on the update a `issue_lifecycle` **Resolved** row + (critical) a `TREND` point.
- `answerClarification(id)` — appends `clarification`, then on the update a `issue_lifecycle` **Resolved** row + (critical) a `TREND` point.
- `selectPath(id,ix)` — appends `selected_path` (Open → Addressed).
- `commitArtEdit()` — appends an `artifact_version` (vN) row on autosave commit.

## Nav / label changes
- Sidebar `#sbHistory` title updated from "…arrives in Slice 7" to "…append-only record of how OSLO's read changed".
- Issue-panel History pointer no longer prints "(Slice 7)".

## Accessibility (D015, WCAG 2.1 AA)
- The timeline is keyboard-navigable; version rows are focusable (`tabindex="0"`, Enter/Space) with a visible `:focus-visible` ring.
- The trend `<svg>` has `role="img"` + `aria-label`; point causes are exposed via `<title>`.
- Honesty invariants (append-only, read-only, viewing changes nothing, rises-or-falls meaning) live in **single ⓘ hovers**, not repeated chrome (§6.7). Neutral maturity color throughout — severity color is reserved for issue severity only (D003).

---

## Revision 1 (2026-07-09)
Initial Slice-7 build: the Slice-6 `#pane-history` seam is replaced by the real **History & timeline** surface (append-only event list with current/prior labels + illustrative timestamps) and the **"Understanding over runs"** neutral trend sparkline (rise/fall, band-qualified, cause-bound). Live-append wiring added to `deepComplete`/`deepFail`/`applyFix`/`answerClarification`/`selectPath`/`commitArtEdit`; `openHistorySeam()` re-pointed to the real pane; version-lineage read-only toast (D099) and first-run minimal state (D100) added. Verified: `node --check` passes; jsdom structural parse (`body.children.length > 0`, `#pane-history` holds the real timeline, trend sparkline present) and jsdom runtime smoke (History opens live, trend renders with rise/fall, apply-fix / answer-clarification / Extended-complete append events, version click is read-only, prior slices intact) — **0 console errors**.

## Revision 2 (2026-07-09, D101 refinements)
History gap-analysis refinements. **Edited in place; all prior behavior, wiring, and other slices preserved. Append-only + read-only + last-good honesty unchanged.**

- **No raw enum leak (§1).** `renderHistory()` no longer prints the internal `type` string in monospace. New `_histCatLabel{}` maps each `type` → a human category label (`Analysis run` / `Version` / `Issue update` / `Your decision`) shown on the row's `.ht` line (`.hcatlab`) and the group `.hg-meta`. jsdom asserts no `analysis_run` / `issue_lifecycle` / … enum text in the rendered timeline markup (present only in code).
- **Run-grouped, collapsible timeline (§2).** New `_histGroups()` clusters the append-only log by **analysis run** (buffers non-run events onto the next run header, newest run first). Each group renders `.hgroup` → `.hg-head` (collapsible `role="button"`, `aria-expanded`, `.hg-caret ▾/▸`, run icon, `.hg-title`, `.hg-meta` with **day marker** via `_histDay()`), delta row, and a `.hg-children[role=list]`. `toggleHistGroup(gid)` flips a `_histCollapsed{}` flag (view-only); groups expanded by default.
- **Per-run delta (§3).** `_runDelta(run,children)` derives `.hg-chip`s: `N opened` / `M resolved` (M counted live from child `issue_lifecycle` "Resolved" rows), CAF band moves (e.g. `Feasibility Very Low → Low`), stage change (`→ Expanded`), and confidence **direction** (`▲`/`▼`, direction-only per D056 — no fabricated magnitude). Hints attached to run events via new `pushHistory(...,{run,delta})` opts (seed Initial `{opened:6}`; Extended `{opened:6, bands:[…], stage:'Expanded'}`).
- **Trend ↔ timeline link (§4).** `renderHistTrend()` circles + `.ct-x` captions (now `.hf-point`, `role="button"`, keyboard-operable) call `histFocusRun(slug)` → scroll-to + `.hgroup.flash` highlight of the matching run group (points without their own header, e.g. "After your fix", fall back to the newest group). Each group header shows the confidence **band** it produced (`.hg-band`, from `TREND` via `_bandFor()`). Trend stays neutral; hover meaning unchanged.
- **Filter chips (§5).** New `.hist-filter` bar (reuses Issues-surface `.ff` chip styling) — **All · Analysis · Issues · Versions · Your decisions** as keyboard-accessible `<button aria-pressed>`. `setHistFilter(cat)` filters child events by category and writes an honest `#hist-hidden` "N hidden by this filter · show all".
- **Polish.** Absolute timestamp on hover (`title=_absTime(ts)`, illustrative). "Current" now marks **only the newest run group** (`.hstate cur`); older groups read `history` — per-event current/prior tags dropped. List a11y: `.hg-children[role=list]` + `.hli[role=listitem]`; version rows stay `role="button" tabindex=0` keyboard-operable.
- **New CSS:** `.hist-filter`/`.flab`, `.hist-hidden`, `.hgroup`(+`.flash`), `.hg-head`/`.hg-caret`/`.hg-titlewrap`/`.hg-title`/`.hg-meta`/`.hg-band`, `.hg-delta`/`.hg-dlabel`/`.hg-chip`(+`.ok`/`.subtle`), `.hg-children`/`.hg-empty`, `.hicon.sm`, `.hcatlab`, `.hf-point`.
- **New JS:** `_histCatOf{}`, `_histCatLabel{}`, `_histCat()`, `_histFilter`, `_histCollapsed{}`, `_slug()`, `_absTime()`, `_histDay()`, `_bandFor()`, `_confDir()`, `_histGroups()`, `_runDelta()`, `_histRow()`, `setHistFilter()`, `toggleHistGroup()`, `histFocusRun()`; `renderHistory()` rewritten; `renderHistTrend()` points made interactive; `pushHistory` opts extended with `run`/`delta`.

**Prototype caveats:** timestamps, band moves, opened/stage/direction, and the trend indices are illustrative (direction-only, not canonical numbers). "After your fix"/"After your answer" trend points have no dedicated run header (existing model appends their Resolved event into the current run) so they focus the newest group. `opened` is reported per run, so Initial and Extended each show `6 opened` (each run legitimately reports what it assessed).

Verified: `node --check` passes; jsdom structural parse (`body.children.length > 0`, `#pane-history` present, **no** raw enum in rendered timeline); jsdom runtime (first-run minimal state intact; grouped-by-run with per-run delta + band; filter chips filter + show "N hidden"; trend-point click flashes its run group; version rows read-only/keyboard-operable; apply-fix appends Resolved + version snapshot into the newest run group and its resolved count grows to 1; exactly 1 "current" badge) — **0 console errors**.

## Chat integration (D108 cascade)

The OSLO chat rail is now **functional** in this slice (composer + Send were inert). Ported from the Slice-8 D108 build and **adapted to Slice 7's History & trend surface**. Edited in place; every Slice-7 behavior (append-only timeline, run-grouping, per-run deltas, trend↔timeline linking, Issues surface, artifact editor, sidebar/palette, clarification loop) is preserved.

- **Working composer.** `#chatInput` + `#chatSend` → `sendChat()`; `chatKey(e)` sends on **Enter**, newline on **Shift+Enter**. `pushUserChat()` renders the user's turn (escaped); `pushChat()` renders OSLO's. `#chatEmpty` first-run state is dropped by `_chatDropEmpty()` on the first message. `#chatscroll` is `role="log" aria-live="polite" aria-relevant="additions"`.
- **State-grounded replies (simulated, never fabricated).** `_chatState()` reads the live model — `currentRead()` (index/band/reliability basis), `_chatCaf()` (limiting dimension), `ISSUES`/`_istatus`/`_sevrank` (open · addressed · resolved, top issue), `ANALYSIS_STATE` (provisional/current/last-good), `_curArt`, `_openClarIds()`. Answers: `_ansConfidence` · `_ansNext` · `_ansIssue` · `_ansDimension` · `_ansArtifact` · `_ansCell` · `_ansRecommendation` · `_ansHowIssuesClose` · `_ansClarifications` · `_ansSummary` · **`_ansHistory`**. Routing is prototype-grade keyword matching (`_oslloReply`, `_matchIssueQ`, `_matchArtQ`).
- **NEW — the History answer (`_ansHistory` + `_chatRun`).** Grounded in the **real** Slice-7 log: `_histGroups()` resolves the run group (newest, or a specific `runId`), `_runDelta()` yields issues **opened/resolved**, CAF **band moves**, **stage** change and confidence **direction** (`_confDir` — ▲/▼ only, no fabricated magnitude, D056), `_bandFor()`/`TREND` yields the band + cause it produced, and the run's own child events are named from `HISTORY`. Replies **link into the run group** via `_cAct("histFocusRun('<slug>')")`, and restate the append-only/read-only guarantee. First-run honesty preserved ("nothing before it to compare").
- **Context handoff + pill.** `askOslo(ctx)` is the single entry point (`{type:'issue'|'span'|'artifact'|'confidence'|'cell'|'recommendation'|'history', id?, art?, dim?, pathIndex?, runId?}`) — stands down the annotation popover/issue scrim, opens the rail, sets `#chatCtx` (`_chatCtxLabel`/`renderChatCtx`), pushes a grounded opening (`_chatOpening`), focuses the composer. `#chatCtxClear` (×) → `clearChatContext()`.
- **Entry points.** Issue panel → `✦ Ask OSLO about this issue` (`.ip-ownfix`) · **Discuss** on **OSLO Recommended** (`.ip-applyrow .btn-ghost`) **and every resolution path** (`.ip-discuss`, `event.stopPropagation()` so **Discuss never selects the path**) · panel clarification → `Answer in chat →` · editor toolbar `#artAskBtn` (✦) and annotation popover `Ask about this →` (`askAboutSpan`) · Overview `#askWhyConf` (`.howcalc.askwhy`) → `Ask OSLO why` · Attention-map cell → scoped Issues header `Ask OSLO about this cell →` · **History pane `#histAskBtn` (`.hist-ask`) and a per-run-group `.hg-ask` on every `.hg-head`** → `askOslo({type:'history', runId})`.
- **Clarifications in chat — one shared path.** `answerClarification()` (panel) and `answerClarificationFromChat()` (chat) both call **`_submitClarification(id, val, src)`**: identical project-info update (`basis='attested'`, reliability step), identical `_istatus` lifecycle (Open → **Addressed** → **Resolved** only on the analysis update, D088), and **identical History/trend events** (`pushHistory('clarification', …)`, `pushHistory('issue_lifecycle', … Resolved)`, `pushTrend('After your answer', …)`, D096). Only the report-back surface differs.
- **Duplicate-clarification defect FIXED (regression from the Slice-8 source).** Raising the same clarification twice used to mint a second `#chatClarBox-<id>`/`#chatClarInput-<id>`. `_chatClarBlock()` now calls **`_retireClarBoxes(id)`** first (strips ids, marks the older copy `.superseded`), and `_submitClarification()` retires any chat copy when answered from the panel — **exactly one live answer box + one live textarea id per issue**, no duplicate DOM ids anywhere.
- **Suggested chips.** `_chatChipList()`/`renderChatChips()` derive from the live read + context, including a **"What changed in the last run?"** chip; rebuilt on send, on context change and in `_refreshIssueSurfaces()`.
- **New CSS:** `.chat-ctx`/`.cx-lab`/`.cx-v`/`.cx-x`, `.chat-empty`/`.ce-t`, `.chat-chips`/`.chat-chip`, `.chat-acts`/`.chat-act`, `.chat-clar`/`.cc-q`/`.cc-foot`/`.cc-note`/`.cc-sup` (+`.answered`/`.superseded`), `.howcalc.askwhy`, `.ip-discuss`, **`.hist-ask`**, **`.hg-ask`**.

**Advisory-only (D001):** the chat never mutates the plan, never selects a path, never resolves an issue, and never writes to the timeline on its own — every action it offers is a link the **user** clicks, running the existing functions (`openIssue` / `openArtifact` / `applyFix` / `selectPath` / `openFindingsFor` / `histFocusRun` / `_submitClarification`). Issues close only via an **analysis update** (D088); "issues", never "findings"; "analysis update/run", never "reanalysis" (D092).

Verified: `node --check` **PASS**; jsdom structural parse (`body.children = 16`, all chat/History ids present); jsdom runtime — Send + Enter with grounded replies, History ask explains the latest run's real deltas (6 opened · *Feasibility Very Low → Low* · *→ Expanded* · ▲ confidence) and links to its run group, Discuss opens context **without** selecting, issue/artifact/span/confidence/cell asks work, chat clarification appends **byte-identical** History events to the panel path, exactly 1 live clarification box (4 raised), History/Trend/Issues/editor intact — **0 console errors**.
