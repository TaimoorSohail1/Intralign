# Slice 9 — Collaboration, Sharing & Export · Frontend UI

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. Single openable `prototype.html` (inline CSS/JS + `localStorage`, D016; ~8,940 lines). This documents the Slice-9 UI surfaces, DOM, CSS and functions. Slices 1–8 UI is unchanged except for the two rewired seam handlers, the two new Overview/Attention blocks, the Issue-Panel additions, the History filter chip, and the rewritten Settings → Collaboration section.

## Rewired seams (top bar)
- **Share:** `#tbShare` `onclick` `openShareSeam()` (stub toast) → **`openShare()`**; `aria-haspopup="dialog"`.
- **Export:** `#tbExport` `onclick` `openExportSeam()` (stub toast) → **`openExport()`**; `aria-haspopup="dialog"`.
- Legacy `openShareSeam()` / `openExportSeam()` kept as aliases → the real surfaces.

## Sharing dialog — `#shareScrim` (D110)
Reuses `.scrim`; new `.wmodal` shell (`.wm-h` / `.wm-b` / `.wm-f`, `max-width:620px`, `max-height:88vh`, internal scroll).
- **Invite row:** `#shareEmail` (`.wm-in`) + `#shareRolePick` (`.rolepick` buttons, `aria-pressed`) + `#shareInviteBtn` (disabled until a valid email). `_shareValidate()` / `setInviteRole(k)` / `sendInvite()`.
- **Participant types:** `#shareTypes` → `.ptype` rows (`<b>` type + plain line).
- **Participants:** `#sharePeople` → `.pt-row` (`.pt-av` · `.pt-b`>`.pt-n`/`.pt-e` · `.pt-t` type chip · Remove). `removeParticipant(email)`.
- **Snapshot link:** `#shareLinkBox` (`.lnkbox`) → `.lnk-meta` + `.lnk-scope` + `.lnk-stale` ("Shows a previous analysis") + `.lnk-url[.revoked]` + `.tbd` expiry chip + `.lnk-acts` (Copy · Preview · Revoke).
- **Rendered by** `renderShare()`. `openShare` / `closeShare` / `_shareIsOpen`.

## Export — `#exportScrim` (D112)
`.wmodal`.
- `#exportCurrency` (`.ex-cur`) — the **analysis-currency marker**, from `_readCurrency()` (reads `HISTORY` / `TREND` / `ANALYSIS_STATE` — never invented).
- `#exportDisclaimer` (`.ex-disc`) — the **required disclaimer** (`EXPORT_DISCLAIMER`).
- `#exportFormats` (`.ex-fmt`) → three `button.ex-opt` (`.ei` glyph · `.eb` name/sub · `.ex-lock` "Paid plan"); non-Free formats carry `disabled aria-disabled="true"`.
- `#exportTierNote` — the Free-plan line + *See plans →*.
- **Rendered by** `renderExport()`; `doExport(kind)`; `openExport` / `closeExport` / `_exportIsOpen`.

## Review Package — `#crrScrim` (D114 · CRR-02)
`.wmodal`. `#crrBody` is rendered by `renderCrr()`:
- the package preview (reuses the reviewer-view `.rvv-pkg` / `.rvv-sec` / `.rvv-sl` / `.rvv-p` / `.rvv-ev` classes) — **finding → context → recommendation (`.elabel.derived` *From OSLO*) → artifact reference + evidence**;
- reviewer chips (`.set-btn[.primary]` per teammate) + `#crrEmail` free-text;
- `#crrNote` (`textarea.wm-in`);
- the "what their answer will and will not do" `.wm-note`;
- `.ip-primecand` on validation issues (REC-05);
- the D118 counter (`_crrCounterHTML()`).
- `#crrSendBtn` is disabled until a reviewer is chosen **or** when `_crrCapReached()`.
- `openCrr(id)` / `closeCrr` / `_crrIsOpen` / `pickReviewer(email)` / `crrEmailInput()` / `sendReviewRequest()`.

## Issue Panel additions — `#issuepanel` (D111 · D114 · D115)
Inserted by `openIssue(id)`, in order, after the recommendations block:
1. **`.ip-life`** now ends with **`_awaitChip(id)`** → `.crr-chip.await` *"◷ Awaiting review · {name}"* (CRR-05).
2. **`.ip-shareb`** — the **⤴ Share for review** action (`btn-primary` on validation issues, `btn-ghost` otherwise) + its limit sentence; `.ip-primecand` REC-05 line; then `_crrCounterHTML()`.
3. **`_reviewsHTML(id)`** — one `.rv-card` per request: `.rv-hd` (avatar · `.rv-who` · `.crr-chip.await` **or** **`.elabel.attested3` "Attested by \<name\>"** · `.rv-ts`), `.rv-note`, then either the awaiting actions (`Preview reviewer view →` / `Copy the review link` / `Revoke link`) or the response: `.rv-kind` chip + the plain verb (*"Marcus Hale **approved this**"*) + `.rv-body` (preserved in full) + **`.rv-evid`** ("This is evidence, not a verdict… ISS-01 is still Open").
4. **`_commentsHTML(id)`** — the standing **`COMMENT_HONESTY`** line, `.cm-thread` of `.cm[.cm-reply]` rows, then `.cm-box` (`#cmInput` + `#cmMention` + `.cm-foot` with the append-only note + **Reply** / **Comment**).

## Issues list — `_issueCard(id)` (CRR-05)
`.ic-m` now ends with `_awaitChip(id)` — the same neutral "◷ Awaiting review" chip.

## Understanding dependencies — `#udepOverview` / `#udepAttention` (CRR-05 / MRI-07)
New `.udep` card, `display:none` until something is awaiting.
- `.uh` (h3 + ⓘ) · `.us` headline sentence (*"N issues awaiting sponsor review… blocked on a person"*) · `.ul` → `.ui` rows (`.crr-chip.await` reviewer · `.t` issue title · `.g` artifact · dimension · `›`), each `role="button" tabindex="0"` → `openIssue(id)`.
- Placed on **Overview** (between *Start here* and *Progress*) and on the **Attention map** (above `.heatwrap`).
- **Rendered by** `renderDeps()`, called from `_refreshIssueSurfaces()` and boot.

## Reviewer view — `#reviewerView` (D116 · **proposal**)
Full-screen `.rvv` (`position:fixed; inset:0; z-index:400`; `.show` = `display:block`).
- **`.rvv-ribbon`** (sticky) — `.rr-t` **"Proposal"** pill + *"pending owner ratification"* + `.rr-x` back button. Warning-token tint, present in both themes.
- `#reviewerBody`, rendered by `renderReviewerView()`:
  - **revoked-link state** — a bare "This link has been revoked" page (no read shown);
  - **package state** — `.rvv-brand` · `.rvv-h1` · `.rvv-sub` (*"No account needed"*) · `.rvv-pkg` (finding / why / what it weakens / recommendation / evidence) · `.rvv-acts` with **exactly four** `.rvv-ab button` (Comment · Approve · Reject · Suggest Alternative), then `#rvvBody` + **Send my response**;
  - **done state** — `.rvv-done` (what it did / what it didn't) + **`.rvv-conv`** the **convert-moment**, which exists **only** in this state.
- `openReviewerView(rid)` / `closeReviewerView` / `rvvPick(k)` / `rvvSend()` / `rvvConvert()`.

## Settings → Collaboration — `#sec-collaboration` (D113)
Rewritten from the *"Not built yet"* stub. `.set-card` rows: Participants (`#setPartCount`) · **Default role** (`#setDefRole` → `.rolepick`) · Snapshot links (`#setLinkState` → `.set-chip`) · **Link expiry** (`#setLinkExpiry` → **`.tbd`** "Not yet set — owner decision") · Revoking a link · **Review requests used** (`#setCrrCount` → `_crrCounterHTML()`). The nav button lost its `.vtag "later"`.
**Rendered by** `renderSettingsCollab()`; `setDefaultShareRole(k)` persists to `LS.defaultShareRole`.

## Notifications (D113)
`NOTIF_CATS` — `mention` / `reply` / `shared with me` flipped `later:true → false`; `_NOTIF_DEFAULTS` flipped to `true`. `renderNotifPrefs()` therefore drops the *"Arrives with Collaboration"* label and enables the switches. `applyReviewResponse()` unshifts a live `reply` notification (`route:'issues'`).

## History (D111/D112/D114)
- `_histicon` + `_histCatOf` + `_histCatLabel` extended with **`comment`** · **`review_request`** · **`review_response`** · **`share`** · **`export`**, all in a new **`collab`** category.
- A **Collaboration** filter chip added to `.hist-filter`.

## CSS added (one block before `</style>`)
`.elabel.attested3` / `.epi-tag.attested3` (the third epistemic variant, on `--cool`, with light-theme overrides) · `.crr-chip[.await|.done]` · **`.tbd`** (the dashed owner-TBD chip) · `.wmodal` family (`.wm-h/.wm-b/.wm-f/.wm-lab/.wm-in/.wm-x/.wm-note/.wm-row`) · `.pt-*` participants · `.ptype` · `.rolepick` · `.lnkbox` / `.lnk-*` · `.cm-*` comments (incl. `.cm-men` mention menu, `.mention`) · `.rv-*` review cards · `.ip-shareb` / `.ip-primecand` · `.udep` · `.ex-*` export · `.rvv-*` reviewer view (incl. `.rvv-ribbon`, `.rvv-conv`) · `.set-chip`.

**Color discipline (D003).** Every Slice-9 chrome element is neutral or brand. Collaboration state — awaiting, attested, revoked, capped — is **never** severity-colored. The third epistemic class uses `--cool` (a neutral blue-grey already in the token set), visually distinct from `--subtle` (*From OSLO*) and `--primary-light` (*Confirmed by you*), and is not a traffic-light signal. The owner-TBD chip uses `--warning` **as a "this is unset" marker**, not as a severity.

## Boot
`init()` gains `renderShare(); renderSettingsCollab(); renderDeps();`. `openSettings()` gains `renderSettingsCollab()`. `_refreshIssueSurfaces()` gains `renderDeps()` + `renderSettingsCollab()`.

## Keyboard / a11y
- **Escape** closes, top of stack first: reviewer view → review package → export → share (a dedicated `keydown` listener; the Slice-1–8 stack is untouched).
- `@` menus (chat and comments) are `role="listbox"` with ↑/↓/Enter/Tab/Esc.
- All new interactive elements are real `<button>`s or carry `role="button" tabindex="0"` + Enter/Space; `:focus-visible` rings inherit from the theme.


---

## AMENDMENT — Controlled Release & Demand UI (D119–D122)

### New DOM
- **`#accessScrim`** — the **Access & invites** modal (`.wmodal`, `#accessBody`), painted by `renderAccess()`. Opened by `openAccess()` / closed by `closeAccess()`; ESC-ordered **above** Export/Share and **below** the reviewer view and the review package.
- **`#phBeta`** — the third phase button in `#phasebar .seg` (Alpha · **Beta** · GA). **`#phaseLabel`** — the phase word in the bar's title, now driven by `setPhase()`.
- **`#shareAlloc`** — the allocation rule box at the top of the Share dialog body.
- **Settings → `#sec-access`** ("Access & invites") + its nav button — rows: Release phase (`#setPhaseName`) · Invite allocation (`#setAllocation`) · Waitlist (`#setWaitlist`) · **Access, waitlist & demand →**; hint `#setAccessPhaseNote`.
- **Reviewer view** — the grant landing is rendered into the existing `#reviewerBody`; the ribbon text is now `#rvvRibbonText`.

### New CSS (all on existing semantic tokens; **severity color is never used for access state**)
- `.pk` / `.pk-av` / `.pk-b` / `.pk-n` / `.pk-r` — the reviewer picker rows.
- **`.pk-free`** — *"free — already in"* on the neutral **`--cool`** token (the same token as the third epistemic class).
- **`.pk-new`** — *"new — admits them"*, a **dashed neutral** chip. Deliberately **not** warning-colored: a cost is not a hazard.
- `.rule-box` — the standing D120 rule block (left-ruled, `--cool`).
- `.acc-blk` / `.acc-h` / `.acc-p` / `.acc-stat` / `.acc-s` / **`.acc-retired`** (dashed + muted — the GA sunset state).
- `.wl-row` / `.wl-pos` (mono position) / `.wl-b` / `.wl-n` / `.wl-m` / `.wl-sig` (+ `.wl-sig.review` on `--cool`) / `.wl-you` / `.wl-note` / `.wl-toggle`.
- `.dm-sim` — the **`simulated data`** chip (dashed, on `--warning`, the same treatment as `.tbd`, because "simulated" and "unset" are the same *kind* of honesty). `.dm-spark` / `.dm-notcomp` (the "not computable" blocks).
- `.rvv-grant` / `.rvv-scope` / `.rvv-id` — the token-grant landing, the scope statement, the identity chip.
- Light-theme overrides provided for every new token-bearing class.

### New / changed functions
| Function | Purpose |
|---|---|
| `_gated()` | `PHASE !== 'ga'` — the single source of truth for whether the gate is live. |
| `setPhase(p)` | Now three-way (`alpha` / `beta` / `ga`); repaints **every** access surface so the ramp is visible. |
| `_principal(e)` / `_isPrincipal(e)` | The `PRINCIPALS[]` registry (DL-049). |
| **`_reviewCost(email)`** | **The D120 rule, in one function**: `'free'` if already a principal, else `'admit'`. |
| `admitPrincipal(email,name,kind,via,scope)` | The only place an invite is spent. Handles **DL-049 in-place promotion** (reviewer → user; no duplicate). Returns `false` when the allocation is spent in a gated phase. |
| `_admitted()` / `_allocSpent()` / `_allocLeft()` / `_allocLine()` | The allocation. `_allocLine()` renders **unset** when `{N}` is null — never a fake balance. |
| `joinWaitlist()` / `_waitPos()` / `_waitlistOrdered()` / `_waitlistDrop()` / `admitFromWaitlist()` / `toggleWlPreview()` | The waitlist, its real positions, skip-the-line, and the **off-by-default** unratified-ordering preview. |
| `renderAccess()` / `openAccess()` / `closeAccess()` / `renderDemand()` | The Access & invites modal + demand instrumentation. |
| `rvvAcceptGrant()` / `_rvvConvertHTML()` / `rvvJoinWaitlist()` | The token grant, and the post-value waitlist convert-moment. |
| `crrWaitlist()` | The honest fallback when the allocation is spent. |
| `_tbdSpan(code,label,why)` / `_costWord()` | Owner-TBD rendering (reuses the existing `.tbd` token). |
| `simCrrCap()` (relabelled **Sim allocation spent**) | Pins the **allocation** to admissions already made — reachable at-cap state, **no invented {N}**. |

### Removed (deliberately)
- **`_crrCapReached()`** and every disable it drove — including the **at-cap disable on the Issue Panel's "Share for review" button**. Under D120 that button is **never disabled**: evidence-seeking is never bounded.

### History / notifications
- New event types `admit` (⊕ *Access granted*) and `waitlist` (◷ *Waitlist*), both in the **Collaboration** filter bucket — the append-only log (D096) is unchanged.
- New notification category **`access`** ("Access & invites"), on by default, routing to the Access modal (`route:'settings:access'`).

### Build integrity
- `node --check` on the extracted script: **PASS**.
- jsdom (no `runScripts`) body children: **28** (prior 27 + `#accessScrim`).
- jsdom (`runScripts:'dangerously'`): boot **0 errors**; all Slice 1–9 + 9b entry points resolve; full surface exercise **0 runtime errors**.

---

# AMENDMENT — D123–D126: new/changed UI surfaces, DOM, CSS and functions

Prototype is now **~10,199 lines**. Single `<script>`; `node --check` clean; jsdom body child count **29** (was 28 — the new `#plansScrim` is the +1).

## New DOM

| Element | Purpose |
|---|---|
| `#plansScrim` / `#plansBody` | **Plans** modal — the Free vs Basic comparison + the real (simulated) upgrade path (T-1 / T-3 / T-4 / D123). |
| `#shareBlock` | **The D124 block notice.** The one place in the Share dialog where the product names *which* limit blocked the user. |
| `#shareAlloc` | Rewritten: now renders **both** limits as two separate boxes, plus the CR-2 never-metered box. |
| `#seatCapBtn` | Demo trigger — *Sim seat cap reached* (the TIER-blocked state). |
| `#crrCapBtn` | Repurposed — *Sim allocation spent* (the PHASE-blocked state); now calls `simAllocSpent()`. |
| `#sbTier` / `#sbTierName` / `#sbTierSub` / `#sbTierBtn` / `#tbPlan` / `#wsPlanChip` | Tier chrome, painted from **one** function (`renderTierChrome()`) so the displayed tier can never drift. |
| `#setSeats` / `#setSubSeats` / `#setSubAlloc` / `#setSubExport` / `#setPlanName` / `#setGrantExpiry` | Settings mirrors for seats, allocation, export formats, plan, grant lifetime. |
| `#upLimBody` / `#upPlanChip` | The project-cap prompt, rewritten to **name the TIER limit** explicitly and disclaim the phase limit. |

## New CSS (Slice 9c block)

- **`.limbox.lim-phase`** (cool/blue, `--cool`) vs **`.limbox.lim-tier`** (brand/orange, `--primary`) — the two limits are given **two different visual identities on purpose**, so a supply constraint can never be mistaken for an upsell. Neither uses urgency colour, a countdown, or loss framing.
- **`.d126`** — the governing principle, printed in-product.
- **`.free-forever`** — the "free & unmetered" badge (CR-2). Appears wherever a review grant is priced.
- **`.plan` / `.plans` / `.plan-never` / `.billing-stub`** — the Plans comparison, the never-sold block, and the explicitly-labelled T-4 billing stub.
- **`.wl-band`** — the three CR-4 bands (band 1 uses `--cool`).
- **`.seat-y` / `.seat-n`** — seat / no-seat chips in the member list.
- Owner-TBD values continue to use the **existing `.tbd` token** — visibly unset, never a fake number.

## New / changed functions

| Function | What it does |
|---|---|
| **`checkAdmission(email, role)`** | **THE D124 FUNCTION.** Returns `{ok, phase, tier, newHuman, takesSeat, limit:'phase'\|'tier'\|'both'\|null}`. Every blocked state in the product comes from here. |
| **`admissionBlockHTML(name, chk, remedy)`** | Renders the block, **naming the limit** — one box per limit, never merged. The phase box carries **no upgrade CTA**. |
| **`_grantReviewerAccess(email, name, issueId)`** | **THE CR-2 SITE.** Creates a `Principal` + a scoped `ReviewGrant`. **No Membership, no seat, no invite.** Carries a **runtime regression guard** asserting `ADMISSIONS.length` did not move, plus a DO-NOT-REMOVE comment block. |
| **`admitPrincipal(email,name,kind,via)`** | A **new human becomes a member** — the only thing that spends an invite (PHASE). Promotes a reviewer **in place** (DL-049). |
| **`_members()`** | The **"Participant" VIEW** (N-2) — derived from `MEMBERSHIPS` × `PRINCIPALS`. `PARTICIPANTS[]` **no longer exists**. |
| **`_seatsUsed()` / `_seatCap()` / `_seatCapSet()` / `_seatCapWord()` / `_seatLine()`** | The **TIER seat cap**, enforced on Membership. Unset renders unset. |
| **`_allocCap()` / `_allocSpent()` / `_allocLeft()` / `_allocLine()` / `_replenishDate()`** | The **PHASE allocation** — real, ratified numbers (Basic 5/mo · Free 2/mo) and a **real** replenish date. |
| **`setTier(t)` / `renderTierChrome()` / `openPlans()` / `renderPlans()`** | The live tier + the real (simulated) upgrade path (D123 / T-3 / T-4). |
| **`upgradeMemberRole(email)`** | **N-3** — one-click Viewer → Collaborator. Costs no invite; costs a seat. |
| **`admitFromWaitlist(email, role)`** | **N-3** — admits as **Viewer** by default. |
| **`_wlBand(p)` / `WL_BANDS` / `_waitlistOrdered()`** | **CR-4** — three bands, date-ordered within each. No score anywhere. |
| **`_linkLifetime(l)` / `_sweepGrantExpiry()`** | **CR-6** — 30-day share links; review grants that die when the issue resolves (or at 14 days). Swept from `_refreshIssueSurfaces()`. |
| **`simAllocSpent()` / `simSeatCap()`** | Demo triggers making the **PHASE-blocked** and **TIER-blocked** states reachable in one click. `simSeatCap()` **pins the cap to the seats already filled** — so the state is reachable **without inventing an owner number** (T-1). |

## Deleted (do not resurrect)

`CRR_CAP` · `_crrCapSet()` · `simCrrCap()` · `_costWord()` · `REVIEWER_GRANT_COST` · `crrWaitlist()` · `toggleWlPreview()` / `WL_PREVIEW_WEIGHTS` · `PARTICIPANTS[]` · `SHARE_LINK_EXPIRY`.
Every one of these encoded a question the owner has now answered. `_reviewCost()` survives **as a constant function returning `'free'`** — it is the guard, not a calculation.

---

# AMENDMENT — D128–D131 UI (2026-07-11)

## Functions changed / added

| Function | Behaviour |
|---|---|
| ~~`_seatCapSet()` / `_seatCapWord()` renders **unset**~~ | **SUPERSEDED (X-1).** The cap is **real**: `_seatCap()` → `SEAT_CAP[TIER]` (3 / 10). `_seatCapWord()` renders the number; `_seatLine()` renders *"N of CAP filled · **unlimited Viewers** (they hold no seat)"*. |
| **`_viewerCap()` / `_viewersUsed()` / `_viewerCapHit()`** 🆕 | X-1 — viewers are unlimited. `_viewerCapHit()` returns `false` **structurally**. |
| **`_assertViewersUnlimited()`** 🆕 | **Runtime guard.** Probes `checkAdmission(…, 'Viewer')` and logs an X-1 violation if the seat cap ever blocks a Viewer. |
| **`inviteNewHuman()` / `acceptInvite()` / `expireInvite()`** 🆕 | **X-2 invite state machine.** The only three functions that move an invite between states, so the balance can never drift from the ledger. |
| **`_allocHeld()` / `_allocUsed()`** 🆕 | Pending invites **hold** supply; expired invites **return** it. |
| **`_inviteWindowWord()`** | Renders the ratified pending-invite window: *"a pending invite expires after **14 days** (X-2a, ratified), and is **refunded** if it was never accepted."* **No TBD chip — X-2a is closed (D132).** |
| **`_inviteExpiryAt()` / `_inviteDateWord()` / `_inviteExpiryLine(inv)`** 🆕 | The **real** expiry date of a pending invite (`now + 14d`, stamped once at send). `_inviteExpiryLine()` is the single honest string: *"Expires **{date}** — the invite **returns to your balance** if unused (X-2)."* **The date and the refund are always emitted together** — never a date on its own, which would read as scarcity. |
| **`_seatsOverCap()`** 🆕 | `_seatsUsed() > _seatCap()`. True only after a **downgrade** with more collaborators than the new cap. Not an error state — a **legibility** state. |
| **`_overCapNoticeHTML()`** 🆕 | The D132 over-cap notice, painted from **one** function into the Share panel, Settings → Collaboration, Settings → Subscription and every TIER-blocked message, so it can never drift. **Leads with *"No one has been removed"***, then names the only real consequence (can't **add**), then the free remedies (Viewer · review request). No urgency, no loss framing, no countdown. |
| **`_assertNoEvictionOnDowngrade(before)`** 🆕 | **D132 runtime guard.** `setTier()` snapshots the Membership roster and calls this after. If a tier change ever removes a Membership it **fails loudly** (`console.error`) and **restores the roster**. Sibling of the CR-2 and X-1 guards. |
| `simSeatCap()` | **Rewritten.** The cap is ratified, so it no longer pins a fiction — it **seats demo colleagues who are already principals** (so **no invite is spent**), making the TIER-blocked state reachable in one click. Never adds or blocks a Viewer. |
| `renderPlans()` | **Rewritten** for T-1. Both columns now carry **unlimited artifacts · full History · unlimited Viewers · link security · unlimited review requests** as `.core` rows. A new panel **above** the columns states that the epistemic record is never metered. The "never sell you" panel now has **four** clauses: evidence · the record · safety · supply. |
| `renderTierChrome()` | Sidebar sub-line: *"1 project · 3 seats · 2 invites/mo"* / *"10 projects · 10 seats · 5 invites/mo"*. New `#setSubAnalysis` row renders the Extended-Analysis **shape + unset number**. |
| `admissionBlockHTML()` | The **tier** box now names the real cap, says *"including you"*, states the invite allocation is **untouched**, and offers the **free remedies first** (Viewer — unlimited; review request — free) before the upgrade path. |
| `pushHistory()` / `_artKey()` `_artVersion()` | **Comment-guarded (D128 P1).** No cap, no trim, no tier check — and the comments say why, so it cannot be quietly reintroduced. |

## Surfaces touched

- **Plans (`#plansScrim`)** — the D128 record panel, the ratified caps, the four-clause "never sell you" panel, the
  closed CR-6 chip, the owner-TBD price + owner-TBD analysis budget.
- **Share (`#shareScrim`)** — seat line names the real cap and *"unlimited Viewers"*; participant rows show
  **`invite pending`** with **Simulate: they accept** / **Simulate: it expires** (X-2); a pending-invite summary box;
  the link-lifetime row now carries **"same on every plan — safety is never sold"** (replacing the old
  *configurable expiry (Basic) — owner-open* chip).
- **Settings → Subscription** — new rows: **Viewers (unlimited)** · **Extended Analysis (shape + unset)** · **Plan
  artifacts (unlimited)** · **History (full)** · **Link revocation & purpose-scoped expiry (every plan)**. Plus a
  hint stating **the whole metering list** (D128).
- **Settings → Collaboration** — *Configurable expiry (Basic)* → **"Closed — not built (D128)"**; new row **"Link
  security by plan → identical on every plan"**.
- **Access & invites** — Demand now shows **invites spent** vs **invites held**, real utilization, and a standing
  **D130** note that the numbers are hypotheses. The Framework-001 note now names the **D131 consolidated proposal**
  and now states that **Reject-moves-CAF is RATIFIED (D133) and built** — symmetrically for an Approve, with every
  D115 bound intact.

## D133 — Alignment is a live CAF row

- **Overview** — `#cg-align` / `#cg-align-fill` / `#cg-align-lvl` / `#cg-align-tip` (previously static markup).
  `renderAlignRow()` paints the level, the bar and the tooltip, and **computes which dimension carries `.lim`** —
  Alignment can now *be* the limit. The **Why** box (`#why-caf`) names the limiting dimension accordingly.
- **Confidence popover** — `#cpp-align` / `#cpp-align-bar`, painted by `renderConfPop()`.
- **Response card** (`_reviewsHTML`) — a second `.rv-evid` block on Approve/Reject: the `.elabel.attested3`
  *"Attested by \<name\>"* token + *"Folded into Alignment — as evidence (D133)"*, the linkage, and **what it does
  not mean**. Identical wording shape in both directions — the copy itself carries the symmetry.
- **No new CSS.** Reuses `.cafrow` / `.caffil` / `.cafband` / `.caftip` / `.lim` / `.rv-evid` / `.elabel.attested3`.
- **Upgrade-or-archive** — now says archiving costs nothing epistemically: **every artifact and the entire History
  are kept** (D128).

**No new CSS.** Everything reuses the existing `.tbd`, `.free-forever`, `.limbox`/`.lim-phase`/`.lim-tier`,
`.plan-never`, `.crr-chip`, `.pv` and `.set-fact` tokens. Owner-TBD values continue to render with the dashed
`.tbd` token — **visibly unset, never a fake number**.
