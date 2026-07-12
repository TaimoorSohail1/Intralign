# Slice 8 — Multi-Project Workspace & Awareness · Worker Report

**Deliverable:** `vertical-slices/slice-08-workspace-awareness/` — cumulative `prototype.html` (Slices 1–8) + 7 product docs. Built by extending the signed-off Slice 7 prototype (5,496 → 5,996 lines). Client-side only; no backend.

## What's NEW vs Slice 7 (four seams filled + one new control)
Slice 8 preserves everything from Slices 1–7 and fills the seams they left as labeled stubs:

1. **Workspace Home (D102)** — the top-left Intralign/OSLO logo (was `title` only) now opens a global **Workspace** context: Pinned + Recent project cards (name · Owned/Shared · analysis status incl. a neutral **stale** chip · reliability-qualified understanding indicator · recency · open-issues count), an **Archived** section with **Restore**, a **"no computed scores across projects"** honesty note, and a **1-active-project** footer. New project → the Free-cap prompt.
2. **Project switcher (D103)** — the top-bar "DevNorth 2026 ▾" chip (was `openProjectSwitcher()` → "arrives in Slice 8" toast) now opens a real dropdown: projects + **New project** + **Workspace Home**.
3. **Notifications / awareness (D104)** — a new top-bar **bell with an unread badge** opens a right-hand awareness panel: categories mention · reply · shared-with-me · analysis complete · analysis failed · stale; **read/unread is presentation-only**; each item **routes to its source**; persistent note **"never triggers an analysis"** (no "reanalysis" language — D092). Badge is neutral/brand, not severity (D003).
4. **Settings (D105)** — the Settings seam (was a stub toast) now opens a real surface with a keyboard-accessible section nav and 11 sections (the 10 D105 areas + Appearance). Subscription/Billing/Integrations/Membership are **visibility-first** — facts + upgrade paths, no enforcement, no real billing.
5. **Appearance (D106)** — Settings → Appearance has a **Dark/Light** toggle (dark default) that flips a single `data-theme` attribute on `document.documentElement` (light token overrides pre-existed) and **persists to localStorage**; **Match system** follows `prefers-color-scheme`. Reduced-motion + focus rings surfaced as facts.

The Free-cap **upgrade-or-archive** prompt (D048) is wired to every New-project action; the old `openUpgrade()` stub is replaced.

## Verification
- **`node --check`** on the extracted `<script>` (single block): **PASS**.
- **jsdom structural parse** (no runScripts): `body.children.length = 22`; all Slice-8 ids present (`workspace`, `settings`, `projmenu`, `notifpanel`, `notifScrim`, `upgradeScrim`, `tbNotif`, `nbadge`, `tbProj`, `wsPinned/wsRecent/wsArchived`, `thDark/thLight`, `np-list`, `setScroll`); 11 settings sections.
- **jsdom runtime** (`runScripts:"dangerously"`): every Slice-8 behavior passes — logo→Workspace Home (Pinned/Recent/Archived + no-scores note + qualified-by wording + stale); switcher lists projects + Workspace Home + New; notifications open with 6 items, all categories, badge 3→2 on route, "never triggers an analysis" note; Settings 11 sections + visibility areas + section-nav highlight; Appearance flips `data-theme` + persists `oslo-s1-theme` + dark removes attr; New-project → upgrade-or-archive prompt with archive option; prior slices intact (Overview/Issues/History views, palette, chat, tour). **0 non-environment errors** on clean boot and through all flows.

## Flags / notes
- **jsdom-only noise:** the runtime harness throws on jsdom's unimplemented `Element.scrollTo`/`scrollIntoView` when a notification routes into the artifact editor. This is an environment limitation, not a prototype bug — stubbing those methods makes every assertion pass. Real browsers implement them.
- **Honesty adaptation:** the v4 reference notification copy used "reanalysis complete/failed/reanalyze"; per D092 this was changed to "analysis complete/failed" and "edited since its last analysis", and the panel note reads "never triggers an analysis."
- **Neutral-chrome choice:** v4 rendered the unread badge and the stale marker in `--danger`/`--warning`. To respect D003 (severity color only on issues), Slice 8 renders the **unread badge in `--primary`** and the **stale state as a neutral dashed chip** — no severity color used as chrome.
- **Illustrative multi-project:** one real project (DevNorth 2026) actually enters the shell; the other cards show honest "demo focuses on DevNorth" toasts. Archive/restore are non-destructive illustrative toasts (no data mutated).
- **Slice-9 seams intact:** Sharing/Export (top-bar icons) and Settings → Collaboration → Manage still point to their clearly-labeled Slice-9 stubs; collaboration/sharing/export internals were not built.

---

## Revision 2 (2026-07-09, D107 refinements)

Folded the Slice-8 gap-analysis findings into `prototype.html` **in place**. All Slice 1–8 behavior preserved; prototype grew 5,996 → ~6,190 lines.

### 1. Dead Settings affordances removed (the headline fix)
Slice 8 shipped rows like *Password & security → **Manage***, *Avatar → **Upload***, *Delete account → **Confirmation-gated*** and *Invite preferences → **Manage*** as `<a role="button" tabindex="0">` with **no handler** — focusable, clickable-looking, inert. Every one is gone: **`#settings a` count is now 0**, and every `<button>` in Settings has a handler or is explicitly `disabled`.

- **Made functional (persist to `localStorage`, reflect in the shell):** editable **display name** + optional **role/title** (`LS.profileName` / `LS.profileRole`) → repaints the sidebar account row, the account menu, avatar **initials** and the Membership row via `applyIdentity()` / `[data-username]` / `[data-avinitials]`; editable **workspace name** (`LS.wsName`) → repaints the top bar, Workspace Home and Settings brand (`[data-wsname]` / `[data-wsinitial]`); **six notification category switches** (`LS.notifPrefs`, `role="switch"`); **Sign out** + **Stay signed in** surfaced in Account (one shared state with the account menu via the new `syncStayToggle()`); **Match system** converted from a dead `<a>` to a real `<button>`.
- **Honest seams instead of dead links:** Billing → *"Billing is handled outside the app in Alpha… No card is stored here."*; Subscription keeps the facts + a real **See plans** button; Collaboration is a plainly labelled **Slice 9** seam; Membership/Integrations are labelled *"Arrives with Collaboration" / "Arrives after this release"*.
- **Delete account** → a **real confirmation dialog** (`#deleteScrim`) that explains the consequence and then says plainly that nothing is deleted in this prototype. The internal phrase **"Confirmation-gated" no longer appears anywhere in the file**, and "visibility-first" no longer leaks into user-facing copy.

### 2. Collaboration notification categories gated
Alpha is invite-only and single-user and sharing is Slice 9, so **mention · reply · shared-with-me cannot occur**. They are now **off and hidden from the panel** (option (a)), listed in Settings as **disabled switches** tagged *"Arrives with Collaboration"* with an explanatory note. The seeded items remain in `NOTIFS[]` (code stays exercised) but never render in Alpha. The three retained categories — analysis complete / failed / stale — were **retargeted to DevNorth 2026** so no notification references a project the user doesn't have. Toggling a category filters the panel and nothing else (legitimate under D104: awareness is presentation-only; D092 respected — no "reanalysis" mechanism).

### 3. Alpha 1-project dashboard
`ALPHA_SINGLE`/`FREE_ACTIVE_CAP` + `_activeProjects()`. The illustrative registry rows are flagged `illustrative` and hidden in Alpha (**grid code retained, not deleted**). `renderWorkspace()` branches: **1 active** → a single **"Your project"** section with the **full-detail card** (understanding · reliability · open issues · artifacts) + New project; **0 active** → the empty state; **2+** → the original Pinned/Recent grid, which returns automatically. A note explains when Pinned/Recent appear. The **"no computed scores across projects"** note is untouched. Archive/restore are now **real** (non-destructive), which is what makes the zero-project state reachable; **New project** → upgrade-or-archive at the cap, else the real intake.

### 4. Light-mode AA contrast sweep
Audited every light token used for text/graphics. Four failed; all fixed (token values only — component code untouched):

| token | was | now | was → now |
|---|---|---|---|
| `--subtle` | `#79818B` | `#666D77` | 3.78 → **5.01:1** on `--bg` (used for small text everywhere) |
| `--primary-light` | `#B45309` | `#A34A07` | 4.44 → **5.24:1** on the 12% brand tint (active nav/chips); 5.93:1 on surface |
| `--warning` | `#A8791F` | `#8A6100` | 3.87 → **5.54:1** on surface; 4.90:1 on the amber heat tint |
| `--conf-low` | `#C7CCD3` | `#7F8792` | 1.3 → **3.63:1** (graphical object, 1.4.11) |
| `--conf-medium` / `--conf-high` | `#8C939D` / `#2C333B` | `#4A515A` / `#1B1F24` | keeps the ramp monotonic: 3.63 → 8.03 → 16.56 |
| `--color-focus` | `#B45309` | `#A34A07` | tracks `--primary-light` |

`--primary` (`#D97A3A`) was verified to be **fill/border only, never text** (3.09:1 on white — clears the 3:1 non-text bar; `--primary-fg` on it is 5.36:1, so buttons/badges/segmented controls keep AA). The maturity ramp remains **pure neutral grey** and severity keeps its hue, so issues stay distinguishable from the ramp in light. A contrast harness over 21 light combinations passes 21/21.

### 5. Polish
Stale card → *"→ Open to bring the read up to date"* (+ a `Sim stale project` phase-bar demo trigger so the state is reachable). **Settings search** (`#setSearch`) filters the eleven sections *and* their nav entries, with an `aria-live` result count and a no-results state. **Empty states**: *"You're all caught up"* (notifications) and *"No active projects"* (workspace, with restore + new). Plain-language pass over Settings/Workspace copy.

### Verification (Revision 2)
- **`node --check`** on the extracted `<script>` (single block): **PASS**.
- **jsdom structural parse** (no `runScripts`): `body.children.length = 23` (> 0).
- **jsdom runtime** (`runScripts:"dangerously"`): **56/56 assertions PASS, 0 JS errors** — zero dead affordances and zero `<a>` in Settings; every Settings button handled-or-disabled; name/workspace edits persist and reflect in the shell; category switches filter the panel and persist; Sign out + Stay-signed-in present and in sync; no internal spec phrasing; collaboration categories gated + labelled; Alpha single-project presentation (Pinned/Recent hidden at 1, grid returns at 2+); archive → zero-project empty state → restore; theme still flips + persists; settings search filters; all inputs labelled and all switches carry `aria-checked`; prior slices (Overview/Issues/History/sidebar) intact.
- **Contrast harness**: 21/21 light-mode combinations pass their AA threshold.

### Notes / boundaries
- **Slice 9 not built.** Collaboration/sharing/export internals remain unbuilt; every surface touching them is a labelled seam, never a control.
- **Advisory-only, "Issues", no "reanalysis" mechanism (D092), neutral chrome with severity color confined to issues (D003)** all held.
- The notification category switches are the one place awareness state is writable — legitimate because awareness is **presentation-only** (D104): a switch changes what the panel *shows*, never an assessment.

---

## Revision 3 (2026-07-09, D108 chat integration)

The OSLO chat rail shipped inert: `#chatp` had only `toggleChat()` / `pushChat()` / `seedChat()`, the composer `<textarea>` had **no id and no handler**, the **Send button had no `onclick`**, and there was zero send/reply logic — a read-only notice feed. No surface handed it context, and the canonical v4 recommendation action **Discuss** was absent. Revision 3 makes chat functional and integrates it into the workflows. Edited in place; all prior slices preserved.

### 1. The chat works
`#chatInput` + `#chatSend` → `sendChat()`; `chatKey()` gives **Enter to send / Shift+Enter for a newline**. `pushUserChat()` renders the user's turn (escaped); `pushChat()` is untouched, so the fast-pass/deep-pass completion notices still land exactly as before. `#chatscroll` is a live region (`role="log" aria-live="polite"`) and carries a first-run empty state.

### 2. Replies are simulated but STATE-GROUNDED
`_chatState()` reads the live model each turn — `currentRead()` (index · band · reliability basis · stage), the CAF rows (Feasibility tracks the live read), the **limiting dimension** (lowest CAF), open/addressed/resolved counts + the most-severe open issue, open clarifications, `ANALYSIS_STATE`, `_curArt`. Ten answer builders (`_ansConfidence`, `_ansNext`, `_ansIssue`, `_ansDimension`, `_ansArtifact`, `_ansCell`, `_ansRecommendation`, `_ansHowIssuesClose`, `_ansClarifications`, `_ansSummary`) are routed by `_oslloReply()` on keyword intents, then the active context, then a grounded fallback. No fabricated numbers or issues.

**Advisory-only (D001):** the chat mutates nothing. Every action is a link that runs an **existing** function (`openIssue` / `openArtifact` / `openFindingsFor` / `applyFix` / `selectPath` / `showView`). "Can you just fix it?" returns the boundary — issues reach Resolved only via an **analysis update** (D088), never a manual step, never "OSLO did it". D092 framing held ("analysis update", never "reanalysis"); "Issues", never Findings.

### 3. Context handoff + context pill
`askOslo(ctx)` is the single entry point (`issue` · `span` · `artifact` · `confidence` · `cell` · `recommendation`). It opens/focuses the rail, sets the visible pill (*"Context · Venue Wi-Fi capacity is unconfirmed (ISS-01)"*) with an **× clear** (`clearChatContext()`), seeds a grounded opening message, and scopes every subsequent answer to that context until cleared.

### 4. Entry points
Issue panel (**✦ Ask OSLO about this issue** + *Answer in chat →* on the clarification) · **Discuss** on OSLO Recommended **and on every resolution path** (NEW — the missing canonical v4 action) · artifact toolbar **✦** and the `#annoPop` **Ask about this →** · Overview **✦ Ask OSLO why** beside the score · **Ask OSLO about this cell →** in the Attention-scoped Issues header. **Discuss never selects a path** (`event.stopPropagation()`; it only offers *Select this path →* as a link the user clicks).

### 5. Clarifications are conversational — same path, same History
`answerClarification()` (panel) and `answerClarificationFromChat()` (chat) both call **`_submitClarification(id, val, src)`**: identical project-info update, identical Open → **Addressed** → analysis update → **Resolved** lifecycle, and the **identical `pushHistory` events** + `pushTrend` point (D096). `src` only chooses which surface reports back — no side channel around governance or the timeline. Verified by asserting the History `type`/`lab`/`d` strings match the panel path exactly.

### Polish
State-derived **suggested chips** (rebuilt by `_refreshIssueSurfaces()`), replies that **link to the surface** they reference, a first-run state, and a11y throughout (live region, labelled composer/answer boxes, keyboard-operable chips + in-thread links). Neutral chrome — no severity color in the rail.

### Verification (Revision 3)
- **`node --check`** on the extracted `<script>` (single block): **PASS**.
- **jsdom structural parse** (no `runScripts`): `body.children.length = 23` (> 0).
- **jsdom runtime** (`runScripts:"dangerously"`): **65/65 assertions PASS, 0 JS errors** — typing + Send yields a user turn and a grounded reply (quotes the live 62/100 · Moderate, the reliability basis, the limiting dimension) that links to the surface; Enter sends and Shift+Enter does not; all six entry points open chat with the right context pill + opening message; clearing context works and is announced; **Discuss leaves `_selpath` and `_istatus` untouched**; chips fill + send; clarification answered in chat produces the same state change **and the same History events** as the panel path (and the panel path still matches); advisory-only refusal contains no "reanalysis"; prior slices (tour, completion notices, History, palette, editor, heat map) intact.

---

## Revision 4 (2026-07-09, D109 chat refinements)

D108 gave the rail a working composer and state-grounded replies. It also gave it a **confident voice** — the one surface in OSLO that didn't say how much to trust itself. Revision 4 makes the chat inherit the product's epistemics and adds the AI-native affordances the interaction was missing. Edited in place in `slice-08-workspace-awareness/prototype.html`; all prior slices and all D108 behavior preserved.

### P1 — Credibility

**Epistemic replies.** `_relBlock(S)` is appended to every substantive answer, built from the **live** `currentRead()`: `r.relWord` selects the qualifier from `_RELQUAL` (High → *"solid, but still a read of your documents"*; Moderate → *"treat it as directional"*; Low/Very Low → *"a hypothesis to test, not a finding"*), and the basis line prints the real `r.reliability` triple. `falseConfidenceHolds(r)` still triggers the *read-this-with-care* line. Derived vs attested comes from **real state**: `_epiOf(name)` reads `PLAN_SECTIONS[].basis` (which `applyFix()` and `_submitClarification()` genuinely mutate) and defers to the live editor DOM (`#artdoc [data-epi="attested"]`) when that artifact is open — so *"Resources: From OSLO"* becomes *"Resources: Confirmed by you"* only when it actually is. `_thinBasis()` fires when the basis is derived-only **and** reliability is Low, and prints **"I inferred this — it isn't confirmed in your inputs"** *in place of* a confident claim.

**Citations.** `_cites()` renders a compact, neutral *"What this rests on"* block. An issue cites its real `ev[]` evidence pairs (*"Resources · Vendors — 'Venue — rooms, power, Wi-Fi (must confirm 500-person Wi-Fi capacity)'"*) → `openArtifact(f.sec)`; the read cites the CAF limiting dimension + the reliability basis → `chatOpenConfidence()`; an artifact cites its body + epistemic state; "what changed" cites the newest analysis run → `histFocusRun()`. Every chip routes to the **owning surface** — no chat-washing.

**Honest fallback.** `_ansFallback()` replaces the canned summary at route 10: *"I don't have a grounded answer to that — so I'm not going to invent one,"* then the true capability list + working chips. It deliberately carries **no reliability qualifier and no citations** — there is no claim to qualify or source. `_outOfScope()` (route 0b) catches "draft an email" / "book the venue" / "handle it for me" → `_ansOutOfScope()`. "Just fix it" still lands on the D001/D088 boundary answer. `_ansSummary()` stays reachable via an explicit *"where do I stand"* route. New: `_ansChanged()` — "what changed" read off `HISTORY` + `TREND`, direction-only (D056/D097).

### P2 — AI-native interaction
`_thinkingEl()` shows *"OSLO is reading your plan…"*, then `_streamInto()` reveals the **already-rendered** reply word-by-word by blanking and refilling text nodes through a `TreeWalker` — the DOM is never rebuilt mid-stream, so citations and actions survive intact. Time-boxed to ~1.15s regardless of answer length; `_chatFlush()` snaps an in-flight stream so a second question is never dropped. `_reduceMotion()` honours `prefers-reduced-motion` (instant render, no thinking state). Each OSLO reply carries `.msg-acts`: **Copy · Retry · 👍/👎 · Save to History**, all `<button>`, all keyboard-operable. Retry re-answers from the read **as it stands now**. Save to History appends a **`chat_note`** (new type; `_histicon` `✎`, category *"Your note"*) — append-only (D096), records the insight, changes no assessment.

### P3 — Context & control
`_follow()` puts 2–3 answer-derived follow-ups under each reply. `@` in the composer opens `#chatMention` (issues · the 7 artifacts · the 3 CAF dimensions, loose-matched so "wifi" finds "Wi-Fi"); picking one pins it. The pill area is now **multi** — `_chatCtx` (handed-in) + `_chatPins[]`, each removable — and `_ansPins()` appends a grounded *"Also in view"* roll-up so answers demonstrably use every pinned context. `toggleChatExpand()` widens the rail (`#app.chat-wide`) and persists the preference. `_cAct(onclick, label, cons)` now states consequences: *"Apply this fix → Drafts the change into Resources; the issue moves to Addressed and your read updates after the analysis run."*

### P4 — Persistence & polish
The thread is a record set (`_CHAT_MSGS`) projected to the DOM, persisted per project to `LS 'chat-thread-<id>'` and restored in `seedChat()`. **Nothing is regenerated on restore** — restored turns are exactly what was said; clarification boxes from past turns are stood down so no stale box can fire. Replies lead with the so-what. ⌘/Ctrl+Shift+K focuses chat, ⌘/Ctrl+Enter sends, Esc closes the picker / clears context. Teaching empty state with 3 example questions. The advisory boundary now lives in **one** home (the composer chip + hover, §6.7) rather than being recited in every reply.

> **Deviation, flagged:** the brief asked for **⌘/Ctrl+K** to focus chat, but that binding is already the **command palette** (D094, Slice 8) and "preserve all prior slices" outranks it. Chat focus is on **⌘/Ctrl+Shift+K**. Owner call if the palette should move.

### Guardrails held
Advisory-only (D001) — the chat mutates nothing; every action runs an **existing** function on the owning surface. **Discuss still does not select** (`_selpath` / `_istatus` untouched, asserted). Issues close only via an analysis update (D088). No "reanalysis" (D092); "Issues", never Findings. Neutral chrome — no severity color in the rail. Anything saved from the chat lands in **History** (D096).

### Verification (Revision 4)
- **`node --check`** on the extracted `<script>` (single block): **PASS**.
- **jsdom structural parse** (no `runScripts`): `body.children.length = 23` (> 0).
- **jsdom runtime** (`runScripts:"dangerously"`), **0 JS errors** across four harnesses: reliability qualifier + derived/attested chip on every substantive reply; thin-evidence line fires on Resources; citation chips render from real `ev[]` pairs and route (clicking one opened Artifacts on Resources); off-script question → honest fallback with **no fabricated number, no citations, no reliability claim**; "draft an email to the venue" → out-of-scope boundary; thinking state appears then resolves, instant under `prefers-reduced-motion`; Copy / Retry / feedback / **Save to History** all work (History gains one `chat_note`, rendered as *"Your note"* with no enum leak); follow-up chips contextual and answering; `@` pinned **3** contexts (issue + artifact + dimension) and the answer's *"Also in view"* block used them; expand mode toggles + persists; consequence text present on 4 actions; thread survives a **simulated reload** (fresh document + seeded `localStorage` → 10 records restored with citations, actions and saved state); **Discuss doesn't select**; the read and all issue statuses unchanged by chat use (the only History growth was the note the user explicitly saved); prior slices (Attention map, artifact editor, Issue panel, History, clarification-through-chat) intact.
