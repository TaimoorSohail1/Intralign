# Slice 9 — Collaboration, Sharing & Export · E2E Test Scenarios

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. Manual/automatable scenarios against the single `prototype.html`. (≤20.)

1. **Share opens.** Top bar → **⤴** → the sharing dialog opens. Expect: invite-by-email row, three participant types each with one plain line, three participants, the *roles are shown, not enforced* note, and the snapshot-link box.
2. **Invite by email.** Type `marcus@northstar.vc`, pick **Viewer**, click **Invite** → he appears in the participant list as *Viewer*; a **Sharing** event lands on History; a toast says no email was actually sent.
3. **Snapshot link — create · copy · stale · revoke.** **Create a view-only link** → a scoped, revocable link appears with *"Shows the current read"* and **Expiry · Not yet set — owner decision**. Trigger an analysis run (e.g. *Sim reviewer response*) → the link is relabelled **"Shows a previous analysis"**. **Revoke** → the URL is struck through; **Preview what they see** on a revoked link reports a revoked page, never an old read.
4. **Export.** Top bar → **⤓** → expect the **analysis-currency marker** ("produced by the *Initial* run, *now − 2m* · Provisional") and the **disclaimer** (*not project health, readiness, or probability of success*). **PDF** is enabled; **Copy summary** and **Link** are visible but **tier-locked** with a *Paid plan* chip.
5. **Export changes nothing.** Note the confidence number and the History depth → **Export as PDF** → an `Export` event is appended; **the confidence read, the trend and every issue status are unchanged**.
6. **Comments are panel-only and append-only.** Open **ISS-01** → scroll to **Comments** → the line *"Comments never change the assessment."* is present. There is **no** comment surface anywhere else in the app.
7. **@mention.** In the comment box type `@` → the autocomplete lists teammates **plus "Invite someone new…"**. Pick *Sam Okafor* → `@Sam Okafor` is inserted. Post → the comment renders with the mention highlighted, a **Comment** event lands on History, and the confidence read is unchanged. **No edit or delete affordance exists.**
8. **Invite from a mention.** In the comment box type `@`, pick **"Invite someone new…"** → the Issue Panel closes and the **sharing dialog** opens.
9. **CRR-01 prominence (REC-05).** Open **ISS-01** (venue Wi-Fi — a *validation* recommendation) → **⤴ Share for review** is the **primary** button and carries *"◆ This is a validation recommendation… Prime candidate for a review request."* Open **ISS-02** → the same action is present but **quiet** (ghost), with no prime-candidate line.
10. **CRR-02 review package.** Click **Share for review** on ISS-01 → the preview shows **the finding**, **why it matters / what it weakens**, **the recommendation** (tagged *From OSLO*), and the **artifact reference** with its evidence lines. **Send is disabled** until a reviewer is picked. Pick **Marcus Hale · Sponsor**, add a note → Send enables and reads *"Send to Marcus Hale"*.
11. **D118 counter.** In the package, the counter reads **"0 of {N} — owner-TBD review requests used"**. Hovering `{N}` explains that the Free cap is canon but the number is an owner decision. **Send is not blocked** — Free can seed the loop.
12. **CRR-01 send.** **Send review request** → the modal closes; the issue now shows **"◷ Awaiting review · Marcus"** in the **Issue Panel** *and* in the **Issues list**; a **Review request** event lands on History. **The issue's status is unchanged** (still *Open*).
13. **CRR-05 / MRI-07.** Go to **Overview** → the **Understanding dependencies** block reads *"1 issue awaiting sponsor review… this is where understanding is blocked on a person."* Go to the **Attention map** → the same block is there, above the heatmap. Click the row → the blocked issue opens.
14. **D116 reviewer view.** On the issue → **Preview reviewer view →** → a full-screen surface opens with a **"Proposal — pending owner ratification"** ribbon. It reads *"No account needed"*, lands **straight in the package**, and shows **exactly four** actions. **There is no "Create your own project" anywhere on this screen yet.**
15. **CRR-03 respond.** Pick **✓ Approve**, type *"Confirmed — the concern is real."*, **Send my response** → the screen switches to a thank-you that says what the answer **did** (evidence → an analysis run → reliability firmed up) and what it **did not do** (it did not close the issue; OSLO did not treat it as the answer). **Only now** does the **convert-moment** — *"Create your own project"* — appear.
16. **D115 the doctrine.** Back in the workspace, open **ISS-01**:
    - the response carries an **"Attested by Marcus Hale"** chip (a third epistemic class, distinct from *From OSLO* and *Confirmed by you*);
    - it reads **"Marcus Hale approved this"** — **not** "this is correct/resolved/verified";
    - the standing block says *"This is evidence, not a verdict… It records that a stakeholder approves — it is not a finding that the plan is sound, correct, or resolved… **ISS-01 is still Open.** The call is yours."*;
    - **the issue is still Open.** An Approve resolved nothing.
17. **CRR-04 the run.** Watch History: an **Extended Analysis complete — a review response was taken as evidence** run lands, with a new **trend point** on *Understanding over runs*. The confidence read moves and **reliability (evidence availability) rises**; the **band is unchanged** — the assessment was not overwritten. A **reply** notification fires (D113) and routes to Issues.
18. **D113 Settings → Collaboration.** Settings → **Collaboration** (no *later* tag) → participants count, **Default role for new invites** (change it → it persists and pre-selects in the sharing dialog), snapshot-link state, **Link expiry · Not yet set — owner decision**, and the review-request counter. Settings → **Notifications** → Mentions / Replies / Shared-with-me are **switchable**, with no *"Arrives with Collaboration"* label.
19. **D118 at the cap.** Phase bar → **Sim CRR cap** → the counter reads *"1 of 1 · at the cap"*, and both **Share for review** and the package's **Send** are disabled with an honest message (*the cap is real; the number is an owner decision*). Toggle it off → back to the `{N}` owner-TBD state.
20. **Chat: explains, never acts.** Ask *"what's blocking my understanding?"* → OSLO names the issue, the person, and what will happen when they answer. Ask *"can you accept his response for me"* or *"just resolve the issue, he approved it"* → **"That one isn't mine to take."** — and it offers **Open the review package →** (the *preview*) and **Open the issue →**, never a send/accept/resolve. Ask about the response → it states what it did and what it did **not** do. **Non-regression:** ⌘K palette, Overview/Attention/Issues/History, the artifact editor, Workspace Home, the switcher, notifications, Settings, dark/light and the tour all still work; console shows 0 errors.


---

## AMENDMENT — Controlled Release & Demand scenarios (D119–D122)

### S9b-1 — Asking a known reviewer is free, forever (D120) — **the crux test**
1. Open any issue → **⤴ Share for review**.
2. **Expect:** Marcus Hale carries **"free — already in"**; Dana Whitlock carries **"new — admits them (cost owner-TBD · CR-2)"**.
3. Pick **Marcus** → **Expect:** a rule box — *"Marcus Hale is already here. This costs you nothing — now or ever."*; the Send button reads **"Send to Marcus Hale"**.
4. **Send** → **Expect:** the request lands; **`ADMISSIONS` stays at 0**; the counter reads *"1 review request sent · never metered when the person is already here."*

### S9b-2 — The allocation is spent; evidence-seeking still isn't bounded (D120)
1. Send a review request to **Dana** (a new person) → she is **admitted** as a Reviewer Principal, scoped to that package; `ADMISSIONS` = 1.
2. Phase bar → **Sim allocation spent** → **Expect:** `CRR_CAP` pins to 1; the allocation reads *"0 of 1 left · 1 spent · simulated allocation"*.
3. Open a **different** issue → **⤴ Share for review** → **Expect the button is enabled** (it is never disabled).
4. Pick **Sam** (an existing principal) → **Expect: Send is ENABLED.** The request goes. **This is the test that matters.**
5. Now pick a **new** email → **Expect:** Send **disabled**, and an honest block: *"you can't admit them right now… you can put them on the waitlist"* → **Add to the waitlist →** records the review request as an **inbound demand signal**. **No upsell.**

### S9b-3 — The reviewer is granted access, not let in anonymously (D119)
1. From an awaiting-review card → **Preview reviewer view →**.
2. **Expect the grant landing:** *"Invited as Marcus Hale · marcus@northstar.vc"* · **"Idris invited you to review one finding."** · **Open the review →** · a scope block naming **this one review package**. **No password field anywhere.**
3. **Open the review →** → **Expect:** the package, and the identity line *"Signed in by invitation as Marcus Hale · reviewer access, scoped to this package."*

### S9b-4 — The convert-moment is the waitlist, and it is post-value (D121)
1. In the reviewer view, respond (**Approve**) → **Expect:** *"Thanks — that's on the record."* + the honest what-it-did / what-it-didn't.
2. **Expect the offer:** *"Want OSLO on your own plan?"* — with the plain reason (*"we are deliberately limiting how many people we let in"*) and **Join the waitlist**. **Expect NO signup offer before the response.**
3. **Join the waitlist** → **Expect:** *"Position 5 of 5"* (real numbers), the **review-requested** signal chip, and *"how much each signal moves you is not decided yet (CR-4/CR-5)"*.
4. Back on the issue → **Expect:** *"Marcus Hale asked for a seat after answering"* + **Grant Marcus a seat →**.

### S9b-5 — Skip-the-line is a promotion, not a second account (DL-049)
1. **Grant Marcus a seat →** → **Expect:** one invite spent; `PRINCIPALS.length` **unchanged** (no duplicate); Marcus's `type` flips **`reviewer → user`**; he leaves the waitlist; History records a **promotion in place**.

### S9b-6 — The mechanism sunsets at GA (D121) — **the point of the whole design**
1. Phase bar → **GA**.
2. **Expect:** Access modal — allocation **"Retired at GA — limits are tier-based"**; waitlist **"Retired at GA — nobody waits. There is nothing to wait for."**
3. **Expect:** Share dialog — *"GA — the gate is retired… anonymous access is permitted (D021/D024)."*
4. **Expect:** reviewer view — **no grant screen**; the convert-moment becomes an ordinary **Create your own project**.
5. Phase bar → **Alpha** → **Expect:** it all comes back.

### S9b-7 — No fabricated scarcity (guardrail)
1. With `CRR_CAP === null`, open **Share**, the **review package**, and **Access & invites**.
2. **Expect:** every allocation number renders as **"{N} per {period} — owner-TBD (CR-1)"** in a dashed TBD chip. **Expect no count, no countdown, no "spots left", no urgency color anywhere.**
3. Grep the built file for `spots left` / `only N left` / `limited time` / `act now` → **zero hits.**

### S9b-8 — Demand instrumentation is honest about what it can't compute
1. Open **Access & invites** → **Demand**.
2. **Expect:** a **`simulated data`** chip on the block; real counts for waitlist size / admissions / review requests; and three explicit **holes** — *invite utilization is not computable without {N} (CR-1)*, *review-request → admit is a count, not a rate*, *k per loop is not computable in a prototype (TEL-06 instruments it)*.

### S9b-9 — A share link is not an export link (escalation #2)
1. **Share** → **Expect** the block *"A share link is not an export link"* with a link to Export.
2. **Export** → **Expect** the format is named **"Export link"** and carries the mirror block *"An export link is not a share link"*, with a link back to Share.

---

# AMENDMENT — D123–D126 scenarios (all four mandatory behavioural checks, plus the register)

All of the below are **automated and PASSING** against `prototype.html` in jsdom (`runScripts:'dangerously'`).

| # | Scenario | Steps | Expected — **and observed** |
|---|---|---|---|
| **S9c-1** | **CR-2 — the request that must never be blocked** | Spend the whole allocation (*Sim allocation spent*). Open any issue → **Share for review** → address a **brand-new** person (`dana@thegridvenue.com`, not a principal) → **Send**. | **The request SENDS.** `REVIEWS.length` +1. `ADMISSIONS.length` **unchanged** (no invite spent). `_seatsUsed()` **unchanged** (no seat taken). A `ReviewGrant` is created. The dialog says so out loud before you press it. ✅ |
| **S9c-2** | **D124 — the PHASE message** | Allocation spent → try to invite a **new** person as Collaborator. | `checkAdmission().limit === 'phase'`. Message: *"You're out of invites for this month — replenishes {date}"*, `.lim-phase` box. **Contains no upgrade CTA and no `.lim-tier` box.** ✅ |
| **S9c-3** | **D124 — the TIER message** | Restore the allocation. Fill the seats (*Sim seat cap reached*) → try to promote the Viewer (Priya) to Collaborator. | `checkAdmission().limit === 'tier'`. Message: *"Free projects hold {N} collaborator seats — Basic holds more"*, `.lim-tier` box, **offers Viewer (free) + a real upgrade path**. **Does NOT say "out of invites"** and contains no `.lim-phase` box. Priya **stays a Viewer**. ✅ |
| **S9c-4** | **D124 — both at once, never merged** | Spend the allocation **and** fill the seats → invite a brand-new Collaborator. | `limit === 'both'`. **TWO separate boxes** render (`.lim-phase` **and** `.lim-tier`). ✅ |
| **S9c-5** | **N-2 — a ReviewGrant is not a seat** | After S9c-1: inspect Dana. | `_isPrincipal('dana@…') === true` · `_isMember('dana@…') === false` · `_seatsUsed()` unchanged · she appears in the Share dialog under *"Review grants — not memberships, and not seats."* ✅ |
| **S9c-6** | **N-3 — Viewer by default** | Access & invites → waitlist → **Admit as Viewer**. | Lands as **Viewer** (`_memberRole() === 'Viewer'`), **no seat taken**, **one invite spent** (phase). A **Make Collaborator** button appears next to them. ✅ |
| **S9c-7** | **(d) GA retires the phase machinery — and only that** | Flip the phase to **GA**. | `_gated() === false` · allocation and waitlist **retired** in the Access modal · `checkAdmission().phase === false`. **But `checkAdmission().tier === true`** — the seat cap still binds — and **Free is still PDF-only**. ✅ |
| **S9c-8** | **D123 / T-3 / T-4 — the real upgrade path** | Plans → *Upgrade to Basic (simulated)*. | `TIER === 'basic'`, `_allocCap() === 5`. Export formats unlock. **The price renders as an unset owner-TBD chip.** Billing is a labelled stub. Downgrade returns the allocation to **2**. ✅ |
| **S9c-9** | **CR-5 / CR-4 — bands, not points** | Add a review-requested person to the waitlist. | They are **#1** (top band). The list shows **three named bands**, date-ordered within each. **No score, no credits, no referral discount anywhere in the DOM.** ✅ |
| **S9c-10** | **CR-6 — the grant dies with the question** | Send a review request, then resolve that issue. | `_sweepGrantExpiry()` marks the grant **expired**; a History event records it. The **attestation stays on the record**. The share link's lifetime reads **30 days**; the grant's reads **"when the issue resolves, or 14 days — whichever first"**. ✅ |
| **S9c-11** | **CR-2 regression guard** | Call `_grantReviewerAccess()` directly. | `ADMISSIONS.length` **unchanged**. (If a future change made it move, the guard logs a **CR-2 VIOLATION** and reverts the ledger.) ✅ |
| **S9c-12** | **Non-regression (Slices 1–8 + Slice 9)** | Boot; exercise onboarding, intake, Overview, Attention, Artifacts+editor, Issues, History, Workspace, Settings, chat, Share, Export, CRR, Reviewer view, Access. | **No console errors on boot. Every surface renders without throwing.** jsdom body child count **29**. ✅ |

---

# AMENDMENT — D128–D131 scenarios (the seven mandatory behavioural checks)

| # | Scenario | Steps | Expected | Result |
|---|---|---|---|---|
| **S9d-a** | **(a) TIER seat cap blocks the 4th Collaborator, and names the TIER** | Free. Make Priya a Collaborator (**3 of 3** — you + Sam + Priya). Invite a 4th as **Collaborator**. | `checkAdmission().ok === false`, `.tier === true`, `.limit === 'tier'`. The `.lim-tier` box reads *"Free projects hold **3** collaborator seats, including you — and all 3 are filled. Basic holds 10."* It **does NOT contain "out of invites"**, contains **no `.lim-phase` box**, states the allocation is untouched, and offers the **Viewer remedy first**. | ✅ **PASS** |
| **S9d-b** | **(b) A Viewer still succeeds at the seat cap** | Same project, same moment. Switch the role to **Viewer** → Invite. | **Succeeds.** `_seatsUsed()` **unchanged** (3 → 3). `_isMember()` true. `checkAdmission(…,'Viewer').tier === false`. `_viewerCap() === Infinity`. `_assertViewersUnlimited() === true`. | ✅ **PASS** |
| **S9d-c** | **(c) CR-2 holds with the allocation fully spent** | *Sim allocation spent* (`_allocSpent() === true`, 0 left). Send a review request to a **brand-new stranger**. | **It sends.** `_reviewCost() === 'free'`. `REVIEW_GRANTS.length` +1. **`ADMISSIONS.length` unchanged** (no invite consumed). No Membership, no seat. The CR-2 regression guard does not trip. | ✅ **PASS** |
| **S9d-d** | **(d) Pending invite expires → REFUNDED; accepted → NOT refunded** | Free (2 invites). Invite `pending1@x.io` as Collaborator → balance **2 → 1** (*1 held*). Participant row → **Simulate: it expires**. Then invite `accept1@x.io` → **Simulate: they accept** → then **Remove** them. | Expiry: balance **1 → 2** (**refunded**), History: *"Invite to Pending1 expired — returned to your allocation"*, the reserved seat is released. Accept: balance stays at **1** and **removal does not refund it** (`_allocLeft()` unchanged). | ✅ **PASS** |
| **S9d-e** | **(e) No tier caps artifacts; no tier truncates/expires History** | Inspect the source and switch tiers. | `ARTIFACTS_METERED === false` · `HISTORY_METERED === false` · `ARTIFACT_CAP = {∞,∞}` · `HISTORY_RETENTION = {full,full}`. **No artifact-count cap in code. No `HISTORY.slice/splice/length=` anywhere. No `TIER` within 80 chars of `HISTORY` in code.** `HISTORY.length` identical across Free → Basic → Free. `BASIC_ARTIFACT_CAP` / `BASIC_RETENTION` **absent from the source.** The Plans surface **states artifacts + History are unlimited on every tier.** | ✅ **PASS** |
| **S9d-f** | **(f) Link revocation + purpose-scoped expiry work on FREE** | On **Free**: create a snapshot link → **Revoke**. | Link created; `revoked === true`. `SHARE_LINK_EXPIRY_DAYS === 30`, `REVIEW_GRANT_MAX_DAYS === 14`, `REVIEW_GRANT_ENDS_ON_RESOLVE === true` — **all active on Free**. `LINK_SECURITY_TIER_LOCKED === false`, `CONFIGURABLE_EXPIRY_BASIC === false`. **`revokeLink()` contains no `TIER` check.** | ✅ **PASS** |
| **S9d-g** | **(g) GA retires the phase machinery — tier limits remain in force** | Flip the phase to **GA**. | `_gated() === false`. Allocation + waitlist **retired** (`checkAdmission().phase === false`; the Access modal says the waitlist is retired). **But the TIER seat cap still binds**: with 3/3 filled, `checkAdmission('…','Collaborator').tier === true` and `.phase === false`. **Viewers still unlimited at GA.** | ✅ **PASS** |

### D132 — the two final closures (new)

| # | Scenario | Steps | Expected | Result |
|---|---|---|---|---|
| **S9e-1** | **X-2a — the 14-day window is REAL, and the date is shown honestly** | Invite a new person → inspect the pending row. | `INVITE_EXPIRY_DAYS === 14`. The invite carries `expiresAt` = **now + 14 days** (verified: exactly 14). The row, the pending-invites box, Settings → Collaboration, History, the notification and the toast **all show a real date**, always with the refund: *"Expires {date} — the invite returns to your balance if unused."* **No `owner-TBD (X-2a)` chip anywhere in the DOM.** **No countdown, no urgency colour, no "expires soon".** | ✅ **PASS** |
| **S9e-2** | **X-2a — pending expires → REFUNDED; accepted → NOT** | Invite `zoe@ext.io` (balance 5 → 4, *1 held*) → **Simulate: it expires**. Then invite `yan@ext.io` → **Simulate: they accept**. | Expiry: balance **4 → 5** (**refunded**); History event *"Invite to Zoe expired — returned to your allocation"* names the **14-day** window and the before/after balance; **no Membership left behind**. Accept: balance **5 → 4** and **stays there** — `expireInvite()` on an accepted invite is a **no-op** (`false`), balance unchanged. | ✅ **PASS** |
| **S9e-3** | **D132 — Basic (10 seats) → Free (cap 3): NO EVICTION** | Basic → *Sim seat cap reached* (10 seats) → Plans → back to **Free**. | **Not one Membership removed** (12 memberships in, 12 out — byte-identical roster). `_seatsUsed() === 10` while `_seatCap() === 3`. `_seatsOverCap() === true`. **`HISTORY` only grows** — nothing truncated. The `setTier()` History event states **"NOBODY WAS REMOVED"**. No `D132 VIOLATION` fired. | ✅ **PASS** |
| **S9e-4** | **D132 — the over-cap state is legible, and leads with the reassurance** | Stay over the cap. Open Share, Settings → Collaboration, Settings → Subscription, Plans. | Every surface renders the over-cap notice: *"This project has **10** collaborators; Free adds up to **3**. **No one has been removed** — you can't add more until you're under 3, or upgrade."* It offers the **Viewer** remedy (unlimited) and the **review-request** remedy (free — CR-2). The **Plans modal states the downgrade contract up-front**. | ✅ **PASS** |
| **S9e-5** | **D132 — the 11th Collaborator is blocked, by the TIER limit** | Over the cap, try to add an 11th **Collaborator**. | `checkAdmission().ok === false` · `.limit === 'tier'` · `.tier === true` · **`.phase === false`**. The block names the **plan/tier** limit, **says nobody has been removed**, and **never says "out of invites"**. A **Viewer is still admissible** (`.ok === true`, `.tier === false`) — X-1 holds. | ✅ **PASS** |
| **S9e-6** | **D132 — the no-eviction guard actually fires** | Deliberately splice 4 Memberships out and call `_assertNoEvictionOnDowngrade(before)`. | It **fails loudly** (`console.error` → *"D132 VIOLATION…"*) and **restores the full roster**. The prohibition is enforced by code, not just by a comment. | ✅ **PASS** |

### Guardrail assertions (also automated)

| Check | Expected | Result |
|---|---|---|
| Pay-to-skip | `PAY_TO_SKIP === false`; **no pay-to-skip code path exists** | ✅ **PASS** |
| **No eviction on downgrade** | `EVICT_ON_DOWNGRADE === false`; **no code path removes a Membership on a tier change** (`setTier()` touches `MEMBERSHIPS` zero times); runtime guard restores the roster if it ever does | ✅ **PASS** |
| **Reject-moves-CAF (D133 — RATIFIED, now BUILT)** | ~~Not built.~~ `REJECT_MOVES_CAF === true`. A **Reject** triggers an Extended Analysis run through the **existing** machinery and **moves Alignment (down) + Reliability (up)**; `ALIGN_EVIDENCE` records it | ✅ **PASS** |
| **D133 — no auto-resolve, no auto-re-open** | `_istatus` is **byte-identical** before and after a Reject **and** after an Approve. `applyReviewResponse()` / `_reviewAnalysisRun()` write `_istatus` **zero** times | ✅ **PASS** |
| **D133 — attestation, not OSLO's read** | The card renders *"Attested by Priya Raman"* + *"Priya Raman **rejected this**"*. Every "wrong"/"invalid"/"re-opened" string in the card is an explicit **negation**; no affirmative self-accept phrasing exists | ✅ **PASS** |
| **D133 — symmetry** | An **Approve** moves Alignment **up** by the **same magnitude** a Reject moves it down (`ALIGN_STEP`, one ledger, one run). Verified: `55 → 47` on Reject, `47 → 55` on Approve | ✅ **PASS** |
| **D133 — nothing else assumed** | **Comment** and **Suggest alternative** leave Alignment **unchanged** (reliability only). `ALIGN_EVIDENCE` records only `approve` / `reject` | ✅ **PASS** |
| Basic price | Renders **unset** — *"price not set — owner-TBD (T-3)"*. **No number.** | ✅ **PASS** |
| Extended Analysis run counts | `ANALYSIS_BUDGET = {free: null, basic: null}` — **not invented.** The *shape* renders in words. | ✅ **PASS** |
| Runtime errors during the whole suite | **None** | ✅ **PASS** |

**Build integrity (re-verified after the D132 fold-in):** `node --check` **PASS** · jsdom (no `runScripts`) → **29
body children** (unchanged) · boot with `runScripts` → **0 console errors** · **all assertions pass (51 behavioural +
8 non-regression)** · **22 render functions across Slices 1–9** open/close/render cleanly on **both Free and Basic**
· D110–D132 all present and implemented.
