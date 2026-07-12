# Slice 9 — Collaboration, Sharing & Export · Open Items

Owner-decision-required items surfaced (not resolved) by this slice. **Nothing below was assumed.** Each is rendered in-product as an explicit unset state, per the Anti-Assumption Build Protocol.

---

> ## ⚑ AMENDED 2026-07-11 — the register is RATIFIED (D123 · D124 · D125 · D126)
>
> The owner has ratified the controlled-release register. **Most of what follows is now settled**, and the passages it supersedes are marked in place below (struck through / banner-flagged) rather than deleted — the history is the point.
>
> **The governing principle (D126), verbatim:**
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> **What is now RATIFIED and built:**
> - **D123 — tier gating is LIVE in Alpha**, because **Basic is purchasable in Alpha**. This **reverses N-1** below.
> - **D124 — two limits, never conflated.** **PHASE** allocation (how many *new humans* you may bring into the Alpha) vs **TIER** seat cap (how many *collaborators a project may hold*). The product must **always name which one blocked you**. Presenting a supply constraint as an upsell is a **dark pattern** and is **prohibited**.
> - **CR-1 / T-2** — allocation **scales with tier: Basic 5/month · Free 2/month**, replenishing, **non-cumulative**. Free is deliberately **non-zero** (CHG-061).
> - **CR-2** — **reviewer grants are FREE and UNMETERED, on every tier, in every phase.** *Structurally required, not a preference* (see the escalation section). Anti-abuse ceiling only.
> - **CR-3** — waitlist admits are **hand-curated**, throttled by **owner onboarding capacity** — not a formula.
> - **CR-4** — **no points economy.** Three honest bands, date-ordered within each. No referral-for-credit.
> - **CR-5** — an inbound review request puts you in the **top band**.
> - **CR-6** — link lifetime is scoped to purpose: **share link 30 days**; **review grant expires when the issue resolves, or 14 days, whichever first.**
> - **CR-7** — convert-moment = **waitlist only**, post-response. **Pay-to-skip is PROHIBITED in Alpha.**
> - **N-2** — **one identity.** `Principal` + `Membership` + `ReviewGrant`. "Participant" is a **view**.
> - **N-3** — waitlist admits land as **Viewer**, one click to Collaborator.
> - **T-1** — **Free fully delivers the core read**; Basic sells **depth and volume**. (Shape ratified; **numbers still open** — see below.)
> - **T-3** — Alpha Basic is **charged**. **T-4** — billing is **out of prototype scope**.
>
> **What is STILL OPEN is consolidated in the two sections at the very bottom of this file.**

---

## 1. Reviewer experience — R1 vs fast-follow (D116) · **PARTLY RESOLVED by D119**

> **UPDATE 2026-07-10 — the identity half is RESOLVED.** **D119** supersedes D116's *no-account* reviewer view: the review link carries a **token that grants Reviewer Principal access (DL-049)**, scoped to that package. **The invite IS the authentication** — the reviewer is *identified and invited*, never anonymous, so **D021 (Alpha/Beta invite-only) and the zero-friction CRR loop are both satisfied**. The escalation below is retained for lineage; **sub-decisions (a) and (b) are answered.** What remains open is **CR-7 — is the convert-moment in R1 or a fast-follow** — which is why the **Proposal ribbon stays on the surface**.

> **FURTHER UPDATE 2026-07-11 — the convert-moment is RESOLVED too (CR-7, ratified).** The convert-moment is the **WAITLIST ONLY**, shown **post-response** (never pre-value). **Pay-to-skip is PROHIBITED in Alpha** and is neither built nor hinted at. What remains an owner *proposal* is the **reviewer experience as a whole (D116)** — so **the "Proposal — pending owner ratification" ribbon stays on the surface**, now citing D116 rather than an open CR-7.

**Status:** Identity/gating **resolved (D119)**. Convert-moment scope ~~still owner-open (CR-7)~~ → **resolved (CR-7: waitlist only, post-response; no pay-to-skip)**. The **reviewer experience itself is still an owner proposal (D116)** — ribbon retained.

**What was built.** A low-friction, **no-account-required** reviewer view: the recipient lands directly in the review package, reads the finding in context, and responds with one of the four CRR-03 actions. The **convert-moment** ("Create your own project") appears **only after they respond** — never before value.

**How it is labelled.** The surface carries a permanent, non-dismissible ribbon: **"Proposal — Reviewer experience — pending owner ratification. Built to be looked at, not adopted. (D116; virality audit P0.)"** It is reachable only via an explicit *Preview reviewer view* demo route.

**The decision the owner owns.**
- **(a) Is the no-account reviewer experience in R1 (Alpha), or a fast-follow?** This collides with a ratified constraint: **canonical-truth.md** states *"Alpha & Beta are invite-only (users authenticated from activation, **never anonymous**). Anonymous product access begins at GA."* A reviewer who answers **without an account** is, on its face, an anonymous product interaction. Either (i) an external reviewer is a distinct principal-type that is *not* "product access" (DL-049 gives some cover here — single `Principal`, `type: reviewer|user`, in-place promotion — which suggests the reviewer *is* a first-class principal and therefore may need to be authenticated too), or (ii) the no-signup reviewer view is a **GA-phase** capability and R1 ships a lighter, invite-authenticated variant.
- **(b) If it is R1, does the reviewer get an identity (magic-link / token) or none at all?** The prototype assumes none. That is a *simulation*, not a claim.
- **(c) Is the convert-moment in R1 at all**, given that R1 is invite-only and there is nothing for a reviewer to convert *into* without an invite?

**Why it matters.** The virality/k-factor audit rates this **P0** — the binding constraint on **k**. It is the highest-leverage decision in the slice, and it is the one the product cannot make for the owner.

**Recommendation (non-binding).** Ratify (a) as *"reviewer is an authenticated principal from first touch, via a link-borne token — invite-only is preserved because the owner issued the link"*. That keeps DL-073/DL-080 phasing intact **and** keeps k unconstrained, because the token *is* the invite. But this is the owner's call — the prototype does not assume it.

---

## 2. Share-link expiry (D117 · gap #339) — ~~unspecified~~ · **RESOLVED by CR-6 (2026-07-11)**

> **SUPERSEDED.** **CR-6 (ratified)** scopes link lifetime to **purpose**:
> - **Share link (a view of a project): 30 days**, revocable, auto-labelled *"previous analysis"* when the read moves on. → `SHARE_LINK_EXPIRY_DAYS = 30`.
> - **Review grant (a key cut for one question): expires when the issue RESOLVES, or 14 days — whichever is first.** → `REVIEW_GRANT_MAX_DAYS = 14`, `REVIEW_GRANT_ENDS_ON_RESOLVE = true`, swept in `_sweepGrantExpiry()` on every issue refresh so **every** resolve path retires the grant.
> - Sub-question **(b)** ("does it differ by scope?") is answered **yes** — that is the whole shape of CR-6.
> - **STILL OWNER-OPEN:** **configurable expiry as a Basic feature.** *Not assumed, and deliberately not built* — rendered as `owner-open · not built`. → `CONFIGURABLE_EXPIRY_BASIC = null`.

**Status:** ~~Surfaced in-product as an explicit unset value. **No default invented.**~~ → **Ratified (CR-6).** Real values, real behaviour.

**What was built.** Links are **revocable** and **scoped** (one snapshot, or one issue package). The **expiry control exists** and renders as a dashed TBD chip: **"Not yet set — owner decision"** — in the sharing dialog and in Settings → Collaboration. In code, `SHARE_LINK_EXPIRY = null`.

**The decision the owner owns.**
- **(a) Is there a default expiry at all?** (Never expires · fixed default · owner-chosen per link.)
- **(b) If yes, what is it** — and does it differ by scope (a review-package link probably has a shorter natural life than a snapshot link)?
- **(c) What does an expired link show?** The prototype's *revoked* state ("This link has been revoked — nothing is shown here, not even an old copy of the read") is a reasonable template, but **expired ≠ revoked** semantically and the copy would differ.
- **(d) Does expiry interact with staleness?** A link that shows a **"previous analysis"** is already degrading in usefulness; the owner may want staleness *itself* to be an expiry trigger. The prototype does **not** assume this.

---

## 3. ~~Free-tier CRR cap — the number (D118)~~ · **DISSOLVED by CR-2 (2026-07-11)**

> **SUPERSEDED — the question no longer exists.** **CR-2 (ratified)**: **reviewer grants are free and unmetered, on every tier, in every phase.** There is **no Free-tier CRR cap**, and there must never be one — metering a review request would gate the *seed* of the loop (CHG-061) and break D120 and D126. `CRR_CAP` has been **deleted from the code**. What replaced it is a *seat* meter (`checkAdmission()` → tier seat cap) and a *supply* meter (the phase allocation) — **neither of which touches evidence-seeking**.
>
> The three sub-questions below are all answered by "there is no cap": (a) there is no {N}; (b) neither requests nor reviewers are capped; (c) at-cap behaviour cannot occur. **A CR-2 regression guard sits at the code site** (`_grantReviewerAccess()` — a runtime assertion that the invite ledger did not move) so this cannot be quietly reintroduced.

**Status:** ~~The **mechanism** is built. The **number is not ratified and is not invented.**~~ → **The mechanism is REMOVED.** Kept here for lineage.

**What was built.** `CRR_CAP = null`. The counter renders **"X of {N} review requests used"** with `{N}` as an explicit owner-TBD chip (tooltip: *"the Free-tier review-request cap is canon; the NUMBER is not ratified. OSLO does not invent it. The owner sets {N}."*). `_crrCapReached()` gates **Share for review** and the package's **Send**; with `CRR_CAP === null` it returns `false`, so **Free sends freely** — virality seeds on Free. A demo trigger (*Sim CRR cap*) pins the cap to what has already been used, making the at-cap state reachable **without** inventing an owner value.

**The decision the owner owns.**
- **(a) What is {N}?** (Per project · per month · lifetime? The prototype's counter is per-project-lifetime by construction; that framing is itself unratified.)
- **(b) Is the cap on requests *sent*, or on distinct *reviewers*?** Sending 3 requests to one sponsor is a different economic event from sending 3 requests to 3 strangers — and the second is the one that seeds the loop.
- **(c) What is at-cap behavior?** The prototype **disables sending** and points to *See plans*. An alternative reading of "gate depth, never the seed" is that Free should **always** be able to send the *first* request to a *new* reviewer, with the cap applying only to repeat/depth usage. **This is not assumed.**

---

## 4. Export "link" vs share link (D110 vs D112) — **RESOLVED as two objects (owner-directed 2026-07-10)**

> **UPDATE 2026-07-10.** The owner confirmed the worker's read: **they ARE two different objects.** The UI now labels them so they cannot be confused — a **share link** (view-only snapshot of the **live project**, revocable, free — D110) is **not** an **export link** (a hosted copy of **one exported snapshot**, frozen at export time, a paid format — D112). **Both surfaces carry an explicit "a share link is not an export link" disambiguation block.** No further owner decision is required; the item is retained for lineage.

**Status:** **Resolved.** Implemented as two labelled objects.

**D112** says *"PDF / copy / link. **Free = PDF-only**"* — so the export **Link** format is tier-locked on Free.
**D110** says the sharing dialog carries *"a **view-only snapshot link** (copy-link)"* — with **no tier restriction stated**.

Both are implemented as written, so a Free user **cannot** export a "link" from the Export dialog but **can** create and copy a view-only snapshot link from the Share dialog. Functionally these are close enough that a user will notice.

**The decision the owner owns:** are these the **same object** under two doors (in which case one of the two decisions needs correcting), or **two genuinely different objects** — *sharing* (a live, revocable, view-only link into the project) vs *exporting* (a frozen, hosted copy of a snapshot document)? The prototype treats them as **two different objects** and words them accordingly, because that is the only reading under which both decisions are simultaneously true. **This is an inference about intent and should be ratified or corrected.**

---

## 5. Noted, lower-stakes, not assumed

> **AMENDED 2026-07-11.** These items are **carried forward and consolidated** into *"Still open, lower-stakes"* at the bottom of this file, updated for the N-2 identity refactor (there is no `PARTICIPANTS[]` any more — "removing a participant" is now "ending a Membership"). The originals are kept here for lineage.

- ~~**Reject and confidence direction (D115).** A response is evidence, so **every** response kind raises *evidence availability* and therefore reliability. That is what D115 authorizes ("Confidence may move (Reliability/evidence improves)"). But a **Reject** arguably also signals *misalignment* between OSLO's read and a stakeholder's — which could plausibly *lower* an Alignment read. **The prototype does not do this**, because nothing ratifies it. If the owner wants a Reject to be able to move CAF (not just reliability), that is a new decision.~~
  > **`REJECT_MOVES_CAF` — OPEN → ✅ RATIFIED (D133), 2026-07-10. NOW BUILT.** The owner ratified it: a **Reject** *is* evidence about **Alignment** (a first-class CAF dimension, DL-062) and moves it through a normal Extended Analysis run — and **so is an Approve**, symmetrically. **Neither direction is privileged.** The D115 bounds are untouched: evidence not truth · *"Attested by \<name\>"* · never auto-resolves · **never auto-re-opens** · OSLO never self-accepts. History preserved above; see the D133 section at the foot of this file.
- **Role of "Sponsor".** MRI-07's headline (*"awaiting **sponsor** review"*) is driven by the reviewer's *human* role (`TEAMMATES[].role`), not by their participant **type** (Owner/Collaborator/Viewer). Those are two different axes. The decision log's example copy ("2 issues awaiting sponsor review") implies the human role is the one that matters. **Confirm.**
- **Comment notifications.** A comment `@mention` currently appends a History event but does **not** fire a `mention` notification (the mentioner is the only user in this prototype, so it would be self-addressed). The category is un-gated and ready; wiring it needs a second real user.
- **Removing a participant.** Non-destructive: their comments and responses are **kept** (the record is append-only, D096). Whether a removed participant's *pending* review request should be auto-revoked is **not specified** — the prototype leaves the link live and lets the owner revoke it explicitly.


---

# ~~OWNER-TBD~~ → **RATIFIED** — Controlled Release & Demand (CR-1 … CR-7)

> **AMENDED 2026-07-11 (D125).** The register below was a list of **open owner decisions**. **It has been ratified.** The table is rewritten to record *what was decided* and *where it lives in code*. The old "owner-TBD chip" column is gone because the chips are gone — **the values are real now**, and the surfaces show real numbers. The only remaining `null`s are the ones listed in the **STILL OPEN** section at the bottom, and those still render **unset**.

| # | **RATIFIED** | Where it lives in the build |
|---|---|---|
| **CR-1 / T-2** | Allocation **scales with tier: Basic 5/month · Free 2/month.** Replenishing, **non-cumulative**. Free is **non-zero** — virality must be able to seed on Free (CHG-061). | `PHASE_ALLOCATION = {free:2, basic:5}`, `ALLOCATION_PERIOD='month'`, `ALLOCATION_CUMULATIVE=false`. Real balance + a **real replenish date** (1st of next month) in the Share dialog, the Access modal, Settings → Access and Settings → Subscription. Invite **utilization is now a real rate** — the denominator is ratified. |
| **CR-2** | **Reviewer grants are FREE and UNMETERED. On every tier. In every phase.** **STRUCTURALLY REQUIRED, not a preference.** Anti-abuse ceiling only (high, non-scarcity). | `CR2_REVIEWER_GRANTS_FREE = true`, `CR2_ANTI_ABUSE_CEILING = 200`. `_reviewCost()` is a **constant function returning `'free'`**. `sendReviewRequest()` has **no allocation check and no tier check**. **`_grantReviewerAccess()` carries a runtime REGRESSION GUARD** that asserts the invite ledger did not move, and a large DO-NOT-REMOVE comment block explaining why it is load-bearing. The **DL-048 token budget** is stated in-product as a **cost** control on compute — *never* a monetization gate. |
| **CR-3** | Waitlist admits are **HAND-CURATED in Alpha**, throttled by **owner onboarding capacity** — **not a formula**, and not an admit-rate. | `WAITLIST_CURATION='hand-curated'`. The waitlist copy says it plainly, and the demand view no longer pretends an admit rate exists. |
| **CR-4** | **NO POINTS ECONOMY.** Three honest bands, **date-ordered within each**: (1) review-requested · (2) referred by an active user · (3) cold. **No referral-for-credit or discount anywhere in Alpha.** | `POINTS_ECONOMY=false`, `WL_BANDS`, `_wlBand()`, `_waitlistOrdered()` (band, then arrival date — nothing else). The old "preview the recommended weighting" toggle is **deleted**; there is nothing left to weight. |
| **CR-5** | An inbound **review request puts you in the TOP band.** | `REVIEW_REQ_TOP_BAND=true`. A `{k:'review'}` signal lands the entry in band 1. Stated on the reviewer's own waitlist screen. |
| **CR-6** | **Link lifetime is scoped to purpose.** Share link **30 days**, revocable, auto-labelled *"previous analysis"* when stale. Review grant **expires when the issue resolves, or 14 days — whichever first.** | `SHARE_LINK_EXPIRY_DAYS=30`, `REVIEW_GRANT_MAX_DAYS=14`, `REVIEW_GRANT_ENDS_ON_RESOLVE=true`, `_linkLifetime()`, `_sweepGrantExpiry()` (called from `_refreshIssueSurfaces()`, so **every** resolve path retires the grant). |
| **CR-7** | Convert-moment = **WAITLIST ONLY**, post-response, never pre-value. **PAY-TO-SKIP IS PROHIBITED IN ALPHA** — not built, and not hinted at. | `CONVERT_MOMENT='waitlist'`, `PAY_TO_SKIP=false`. **Rationale carried in-product and in code:** the queue is throttled by **onboarding capacity**, so **payment does not create capacity** — selling passage past it would be a toll booth on an invented constraint (a dark pattern, §5). The **"Proposal — pending owner ratification" ribbon stays** on the reviewer view (D116 is still an owner proposal). |

### The N-items — resolutions

| # | Was | **Now** |
|---|---|---|
| **N-1** | *"Should tier limits be inert during Alpha?"* | **REVERSED / WITHDRAWN (D123).** **Tier gating stays LIVE in Alpha** — Basic is purchasable. **Free = PDF-only (D112) genuinely applies in Alpha**, and it is **not a dead end**: a real (simulated) **Free→Basic upgrade path** ships with it (`openPlans()` / `setTier()`). The premise of N-1 ("all Alpha users are on Free, with no way up") was simply false. |
| **N-2** | *"Two registries of who is here."* | **RESOLVED — ONE IDENTITY (D125).** `Principal` (DL-049) is the single identity. **"Participant" is a VIEW**, derived from two relations: **`Membership`** (principal × project × role — **this is where the TIER SEAT CAP is enforced**) and **`ReviewGrant`** (principal × package, scoped, expiring). **A reviewer holding only a `ReviewGrant` is not a project member and consumes no seat.** In code: `MEMBERSHIPS[]`, `REVIEW_GRANTS[]`, `_members()` (the view), `_seatsUsed()`. `PARTICIPANTS[]` **no longer exists**. |
| **N-3** | *"Skip-the-line grants a Collaborator seat."* | **RESOLVED — VIEWER BY DEFAULT (D125).** Waitlist admits land as a **Viewer** (least privilege *and* least cost — a Viewer takes **no tier seat**), with **one-click upgrade to Collaborator** (`upgradeMemberRole()`), which is exactly where the seat cap bites. |

---

# ESCALATED — canon tension (D122 / CHG-061). **Recommendation, not canon. Still routing through Framework 001.**

> **AMENDED 2026-07-11.** The **old** reconciliation is **dead**, and the **new** one is **load-bearing**. Both are recorded.

**~~The old reconciliation (D122):~~** ~~"CHG-061 is a *tier* rule governing GA-phase freemium; controlled release is a *phase* rule that sunsets at GA — so both hold."~~ **KILLED BY D123.** Basic is purchasable *during Alpha*, so **the tier rule does not wait for GA**. The two axes are now live simultaneously and the "they never meet" argument evaporates.

**The reconciliation that now holds — and it rests entirely on CR-2.**
Because **reviewer grants are free and unmetered on every tier and in every phase (CR-2)**, the **seed of the loop — CRR evidence-seeking — is gated nowhere**. Only **seats** are metered. **CHG-061 (*"guarantee the viral primitives on Free… never gate the seed of the loop"*) then holds *literally*, not by argument.**

**This is why CR-2 = free is load-bearing and not a preference.** If a reviewer grant were ever made to consume the allocation — or a review request gated behind a tier — OSLO would be gating the seed of its own loop, in direct conflict with applied canon, in breach of D120, and in breach of D126. **That change would not be a product tweak; it would be a canon violation, and it must route Backlog → Proposal → Review → Decision before a line of it is written.** A regression guard sits at the code site to make that visible.

**Still routing to Framework 001 (recommendation, NOT canon — nothing in the build treats these as ratified):**
1. **D122 — the CHG-061 reconciliation via CR-2.** Stated in-product (Access & invites → *The ramp — and where it ends*) as an escalation.
2. **D123 — the consequences of tier-gating-live-in-Alpha** (DL-048's "paid-tier limits TBD" moves from *deferred* to *blocking*).
3. **T-1 — the Free↔Basic numbers.** The *shape* is ratified; the *numbers* are not (below).

---

# STILL OWNER-TBD — **DO NOT ASSUME. DO NOT INVENT.**

Each of these renders in-product as an **explicit unset state** (the dashed `.tbd` token), never as a fake value and never as fabricated scarcity.

> ⚠️ **SUPERSEDED IN PART — 2026-07-11 (D128 · D129 · D132).** The table below was written when the T-1 numbers, the
> seat cap and CR-6's configurable expiry were all open. **They are now closed.** The rows are struck through and
> restated in the **D128–D131 amendment** at the bottom of this file. **X-2a (pending-invite expiry = 14 days) and
> seat-cap-vs-downgrade (NO EVICTION) are also now CLOSED — ratified by D132.** ~~Only **T-3 (price)**, **"Does a
> Reject move CAF?"**, **CR-7 (does revenue expand onboarding capacity)** and **T-4 (billing rail)** remain
> owner-open.~~ **AMENDED — "Does a Reject move CAF?" is now RATIFIED (D133) and BUILT.** Owner-open now:
> **T-3 (price)** · **CR-7** · **T-4 (billing rail)** · residual **T-1** (Extended-Analysis run counts).

| # | Open item | In-product state | Constant |
|---|---|---|---|
| **T-3** | **The PRICE of Basic.** Alpha Basic **is charged** (founding-member pricing permitted) — but the number is the owner's. | Plans modal: *"price not set — owner-TBD (T-3)"*, with the ratified position stated next to it. Settings → Billing: same. **No number is invented anywhere.** | `BASIC_PRICE = null` |
| ~~**T-1**~~ | ~~**The exact Free-vs-Basic numeric caps** — projects · artifacts · Extended-Analysis frequency · history retention · **collaborator seats**. T-1 ratifies the **shape** ("Basic sells depth and volume"), **not the numbers.**~~ | ~~Plans modal shows each as *"number unset — owner-TBD (T-1)"*. The **seat cap renders unset and enforces nothing**; a demo trigger pins it to seats already filled so the tier-blocked state is *reachable* without inventing a value. On Basic the **project cap is unset and therefore unenforced**.~~ | ~~`SEAT_CAP={free:null,basic:null}`, `BASIC_PROJECT_CAP`, `BASIC_ANALYSIS_FREQ`, `BASIC_ARTIFACT_CAP`, `BASIC_RETENTION` — all `null`~~ **→ CLOSED by D129.** Seats **3 / 10**, projects **1 / 10** — ratified and enforced. **Artifacts and history retention are NOT tier dimensions at all** (D128) — those two constants are **deleted**. Only the **Extended-Analysis run counts** remain unset. |
| ~~**CR-6**~~ | ~~**Configurable link expiry as a Basic feature.**~~ | ~~Shown as *"owner-open · not built"*.~~ | ~~`CONFIGURABLE_EXPIRY_BASIC = null`~~ **→ CLOSED by D128 P2: never sell safety. NOT BUILT, and it will not be.** `CONFIGURABLE_EXPIRY_BASIC = false` |
| **CR-7** | **Does revenue ever genuinely expand onboarding capacity?** If it ever did, pay-to-skip would stop being a toll booth on an invented constraint and **CR-7 would re-open**. | **Not modelled, not hinted at, not built.** Carried here and in the code comments only. | — |
| **T-4** | **Billing/payment rail.** Required by T-3, **out of prototype scope** — carried to **Slice 10 / engineering**. | Settings → Billing is an explicit **stub**, labelled *"Stub · T-4"*. The upgrade in the Plans modal is **simulated** and says so. No card field, no price, no invoice. | — |

### Still open, lower-stakes (carried forward)

- ~~**Does a Reject move CAF?** — **STILL OWNER-OPEN. STILL NOT BUILT.** A recommendation now exists and is recorded in D129: *yes, via **Alignment**, a first-class CAF dimension (DL-062) — it may move Alignment and Reliability while **never** auto-resolving the issue and **never** overwriting OSLO's read (D115).* **Nothing ratifies it**, so it stays out of the build. It rides in the **consolidated Framework 001 proposal** (D131). In-product: a Reject is recorded as evidence and changes no assessment on its own, and the Access modal states plainly that this question is unratified and unbuilt.~~ → ✅ **RATIFIED (D133) and BUILT.** See below.
- ~~**"Sponsor" = `TEAMMATES[].role`.**~~ **CONFIRMED AS-IS (D129)** — cosmetic; the human role, not the Membership role. No change.
- **Removing a member.** Non-destructive: their comments and attestations are **kept** (append-only, D096), and they **remain a Principal in OSLO** (N-2 — one identity). Ending a Membership **returns a tier seat**; it does **not** refund the invite (**X-2, now ratified**) — an invite admits a *human*, not a membership. Whether a removed member's **pending review request** should be auto-revoked is **still not specified** — the prototype leaves the grant live and lets the owner revoke it explicitly.
- **Comment notifications.** A comment `@mention` appends a History event but does not fire a `mention` notification (the mentioner is the only user in this prototype). The category is un-gated and ready; wiring it needs a second real user.

---

# AMENDMENT — D128 · D129 · D130 · D131 (open-items register, RATIFIED 2026-07-11)

> The owner has ratified the open-items register. **Everything above that this contradicts is superseded** (marked
> in place; nothing deleted). Two governing principles now sit **above** every metering rule in the build.

## D128 — the two governing principles (they override any conflicting code)

**P1 — Meter only what costs money or defines scope. NEVER meter the epistemic record.**

| Dimension | Metered? | Why |
|---|---|---|
| **Extended Analysis runs** | **YES** — cost-linked | Real tokens (DL-048). An honest lever. |
| **Projects** | **YES** — scope-linked | Defines how much you are actively working. |
| **Collaborator seats** | **YES** — scope-linked | Defines how many people work *inside* OSLO with you. |
| **Artifacts** | **NEVER — uncapped** | The epistemic record. |
| **History** | **NEVER — never expires, never truncated** | The epistemic record (D096). |
| **Viewers** | **NEVER — unlimited** (X-1) | Read-only changes nothing about scope or cost. |
| **Review requests / reviewer grants** | **NEVER — free & unmetered** (CR-2) | Evidence-seeking. Metering it degrades understanding on purpose. |
| **Link revocation / purpose-scoped expiry** | **NEVER** (P2) | Safety. |

> That table **is** the whole list of meters. Nothing else in OSLO is metered by tier.

**P2 — Never sell safety.** Link revocation + purpose-scoped expiry (CR-6) are trust hygiene for **every** tier.
**CR-6 configurable-expiry-for-Basic: NOT BUILT — CLOSED.** There is **no tier-lock on any link-security control**
anywhere in the prototype (verified: `revokeLink()` contains no `TIER` reference; `LINK_SECURITY_TIER_LOCKED = false`).

**What was removed from the previous build.** The old Plans/Settings/upgrade copy sold *"more artifacts"* and
*"longer history retention"* as Basic features. **That language is gone**, and the constants `BASIC_ARTIFACT_CAP` /
`BASIC_RETENTION` are **deleted**. Code comments now sit at `pushHistory()` and at the artifact-version store
stating that the epistemic record is never metered, so it cannot be quietly reintroduced.

## D129 — the ratified register, as built

| # | Ratified | In code |
|---|---|---|
| **X-1** | **Seats meter COLLABORATORS only. Free = 3 (incl. the owner) · Basic = 10.** **Viewers UNLIMITED** on every tier. **Reviewers free/unmetered** (CR-2). Enforced on **Membership** (N-2), only for seat-holding roles. | `SEAT_CAP = {free:3, basic:10}` · `VIEWER_CAP = {free:∞, basic:∞}` · `checkAdmission()` (`takesSeat` is false for a Viewer, so a Viewer can never trip the cap) · `_assertViewersUnlimited()` runtime guard |
| **X-2** | **No refund once ACCEPTED.** **NEW — an invite that expires UNACCEPTED is REFUNDED** (no human admitted → no supply consumed). | `INVITES[]` state machine: `inviteNewHuman()` (holds) → `acceptInvite()` (spent for good) / `expireInvite()` (refunded, with a History event). `_allocUsed() = accepted + pending`. |
| **X-3** | **Allocation period = CALENDAR MONTH.** Confirmed as built. | `ALLOCATION_PERIOD = 'calendar-month'` · `_replenishDate()` → 1st of next month · UI says *"resets {date}"* |
| **T-1** | **Free:** 1 project · small monthly Extended Analysis budget · **UNLIMITED artifacts** · **FULL History**. **Basic:** 10 projects · generous budget · **UNLIMITED artifacts** · **FULL History**. | `FREE_ACTIVE_CAP = 1` · `BASIC_PROJECT_CAP = 10` · `ANALYSIS_BUDGET = {free:null, basic:null}` (**numbers NOT invented**) + `ANALYSIS_BUDGET_SHAPE` (the ratified shape) · `ARTIFACT_CAP = {∞,∞}` · `HISTORY_RETENTION = {full,full}` |
| **Sponsor** | `TEAMMATES[].role` — confirmed as-is. | unchanged |

**The Plans surface now visibly states that artifacts and History are unlimited on every tier** — above the plan
columns, inside both columns, and in the "what OSLO will never sell you" panel. That is a **feature**, and it is
doctrinally load-bearing.

## D130 — the numbers are instrumented hypotheses, not settled canon

**3 seats · 10 seats · 1 project · 10 projects · 2 and 5 invites** are **judgments, not derivations.** They were
chosen to be **easy to loosen and painful to tighten** — the right direction of error before real alpha data
exists. Loosening a cap delights people; tightening one breaks trust with people who already built on it.

**They must be instrumented and revisited against alpha behaviour.** What to watch:

- **Seat cap (3):** what fraction of Free projects hit it, and how fast? If most Free users hit 3 in week one, 3
  is a tax on the *experience* that creates the want, not a boundary — loosen it. If almost nobody hits it, the
  cap is not the conversion lever and the upgrade story must come from somewhere else (probably projects).
- **Project cap (1):** does a second project arrive *before* the user has got value from the first? If so, the cap
  is blocking exploration, not scope.
- **Extended Analysis budget (unset):** the only *cost*-linked meter. Set it from observed run-cost, not from a
  feel for what sounds generous.
- **Invite allocation (2/5):** watch **invite utilization** and **pending-invite expiry rate**. A high expiry rate
  means people are inviting into a void — that is a *product* signal, not a supply one.

**The instrument is live in-product:** Access & invites → Demand shows invites **spent vs held**, real utilization
against a ratified denominator, and a standing note that these numbers are hypotheses (D130).

## D131 — Framework 001 routing: **ONE consolidated proposal**

**Package title: "Controlled Release & Tiering-in-Alpha."**

Contents (all five ride together):
1. **D122** — the CHG-061 reconciliation **via CR-2** (reviewer grants free and unmetered).
2. **D123** — tier gating **live in Alpha** (Basic is purchasable now).
3. **T-1** — the Free↔Basic **boundary + the ratified caps**.
4. **CR-6** — **closure** (link security on every tier; configurable-expiry-for-Basic **not built**).
5. **"Does a Reject move CAF?"** — ~~the recommendation (yes, via **Alignment**, DL-062), **unratified and unbuilt**.~~ **Now RATIFIED as D133 and BUILT.** It still rides in the package — the D133 ratification is a *product* decision; it becomes **repository canon** only through Framework 001.

**Rationale — why one and not four.** These are **interdependent**. **CR-2 is the *sole* resolution of D122**: if
reviewer grants were ever metered, the seed of the loop would be gated and CHG-061 would break. And **T-1 exists
only because of D123**: the Free↔Basic boundary is only *blocking* because Basic ships in Alpha. Split into four
proposals, a reviewer could **ratify one while silently breaking another** — e.g. ratify a tier boundary while
leaving CR-2 unratified, and thereby gate the seed of the loop by omission. One package, one decision.

---

# STILL OWNER-OPEN after D128–D131 — **DO NOT ASSUME. DO NOT INVENT. DO NOT BUILD.**

| # | Open item | In-product state | Constant |
|---|---|---|---|
| **T-3** | **The PRICE of Basic.** Alpha Basic **is charged** (T-3, ratified); the **number** is the owner's. *Method recommended (not ratified):* price against **the alternative** — the plan review a consultant would run — **not** against PM tools at $10–25/seat. Pick a **founding-member price you would be embarrassed to lower later**, declare it time-limited, and lock it for early users. | Plans modal + Settings → Billing: *"price not set — owner-TBD (T-3)"*. **No number anywhere.** | `BASIC_PRICE = null` |
| **T-1 (residual)** | **The Extended Analysis run counts.** The **shape** is ratified (Free *small* · Basic *generous*); the **numbers** are not. This is the one legitimately cost-linked meter (DL-048). | Plans + Settings → Subscription render *"a small/generous monthly budget · **runs per month unset** — owner-TBD (T-1)"*. | `ANALYSIS_BUDGET = {free:null, basic:null}` |
| ~~**"Does a Reject move CAF?"**~~ | ~~**Recommendation exists; nothing ratifies it → NOT BUILT.**~~ **→ ✅ RATIFIED (D133) and BUILT.** See the D133 section below. | A Reject (and, symmetrically, an **Approve**) is **Alignment evidence** and moves Alignment + Reliability through a normal Extended Analysis run. It still **never** resolves, re-opens or invalidates the issue, and it is never OSLO's own read. | `REJECT_MOVES_CAF = true` |
| **CR-7** | **Does revenue ever genuinely expand onboarding capacity?** Only if it did would pay-to-skip stop being a toll booth on an invented constraint. | **PAY-TO-SKIP REMAINS PROHIBITED AND UNBUILT.** Not modelled, not hinted at. | `PAY_TO_SKIP = false` |
| **T-4** | **Billing/payment rail.** Required by T-3; **out of prototype scope** → Slice 10 / engineering. | Settings → Billing is a labelled **stub**. The Plans upgrade is **simulated** and says so. | — |

### ✅ CLOSED by D132 (owner: accepted, 2026-07-10) — both were escalated by the previous build, and both are now canon

| # | Was open | **RATIFIED (D132)** | In-product state | Constant |
|---|---|---|---|---|
| **X-2a** | **HOW LONG does a pending invite live before it expires?** D129 ratified the *refund*, not the *window*. The build rendered the window **unset** rather than invent one. | ✅ **14 days.** Long enough for a busy stakeholder; short enough that supply is not parked indefinitely. On expiry the invite **refunds** to the balance (D129) with a **History event**. | Every pending invite carries a **real expiry date**, stamped once at send, and states it honestly: *"Expires {date} — the invite returns to your balance if unused."* Shown on the pending row, in the pending-invites box, in Settings → Collaboration, in History and in the toast. **The TBD placeholder is removed.** **No countdown, no urgency colour, no "expires soon" nudge** — it is a date, not a scarcity device. | `INVITE_EXPIRY_DAYS = 14` |
| **Seat cap vs downgrade** | Basic (10 seats used) → Free (cap 3): does anyone get removed? The build took the conservative non-destructive path but **nothing ratified it**, so it was escalated. | ✅ **NO EVICTION. Nobody is removed.** The account simply cannot **ADD** another Collaborator until it is back under the cap, or it upgrades. **Evicting humans from a project to enforce a billing change is prohibited on a trust product.** | The over-cap state is **explicit and legible** wherever seats are shown: *"This project has 10 collaborators; Free adds up to 3. No one has been removed — you can't add more until you're under 3, or upgrade."* Rendered in the Share panel, Settings → Collaboration, Settings → Subscription, the Plans modal (the downgrade contract, stated where a downgrade is initiated), and every TIER-blocked message. **No code path removes a Membership on a tier change** — `setTier()` touches `MEMBERSHIPS` zero times, and a runtime guard fails loudly and restores the roster if that ever changes. | `EVICT_ON_DOWNGRADE = false` + `_assertNoEvictionOnDowngrade()` |

**Nothing is left escalated from D132.** ~~The remaining owner-open items are the three in the table above:
**T-3 (Basic price)** · **"Does a Reject move CAF?"** · **CR-7 (whether revenue ever expands onboarding capacity)**~~
**AMENDED by D133 — Reject-moves-CAF is now ratified and built.** The remaining owner-open items are
**T-3 (Basic price)** · **CR-7 (whether revenue ever expands onboarding capacity)**
— plus the residual **T-1** Extended-Analysis run counts and the **T-4** billing rail (out of prototype scope).

---

# ✅ CLOSED by D133 (owner: ratified, 2026-07-10) — **the last Slice 9 escalation**

## `REJECT_MOVES_CAF` — **OPEN → RATIFIED. NOW BUILT.**

**The question, as it stood:** a reviewer response is evidence, so every kind raises *evidence availability* and
therefore reliability (D115). But a **Reject** is not just "more evidence" — it says something specific: *a
stakeholder does not read the plan the way OSLO does.* Was OSLO allowed to let that touch **CAF**?

**Ratified: yes — via ALIGNMENT.** A Reject is **evidence about Alignment**, a first-class CAF dimension (DL-062).
It moves **Alignment** and **Reliability** through a **normal Extended Analysis run** — the *existing* machinery
(`pushHistory` / `pushTrend` / `_refreshIssueSurfaces`). There is **no parallel path** and **no special case**.

**Rationale (owner):** refusing to let a Reject touch CAF would mean OSLO watched a sponsor reject a finding and
learned **nothing about alignment** — precisely the dimension the event speaks to.

### Symmetry — the load-bearing half of D133
An **Approve** is *also* Alignment evidence. **Neither direction is privileged.** Both are attested inputs to the
same run, moving the same dimension by the **same step** (`ALIGN_STEP`, applied `+` or `−`). A build in which a
Reject were "louder" than an Approve would be OSLO putting a thumb on the scale — and it would be OSLO deciding,
quietly, that disagreement is more true than agreement. It is not; both are just evidence.

### The bounds — **unchanged**, exactly as D115 binds every reviewer response
| Bound | How it holds in the build |
|---|---|
| **Evidence, not truth** | Recorded as a **third-party attestation** — `Attested by <name>`, the third epistemic class (never *From OSLO*, never *Confirmed by you*). The assessment is **never overwritten**. |
| **Never auto-resolves. Never auto-re-opens.** | **Nothing in the CRR module writes to `_istatus`** — not on Reject, not on Approve. Only an analysis update moves an issue, and the human still decides. Verified behaviourally. |
| **OSLO never self-accepts** | Copy reads *"\<Name\> **rejected this**"* — evidence that a stakeholder **disagrees**. It is **never** rendered as *"this is now wrong / invalid / re-opened"*. Every occurrence of "wrong"/"invalid"/"re-opened" in the response card is an explicit **negation**. |
| **Direction is honest** | The confidence read **may fall** on a Reject (alignment down, reliability up) and **may rise** on an Approve. The trend line already supports a fall (D097): a fall after a deeper read usually means it found something real. |

### What is deliberately **NOT** built (and is a new escalation — see below)
**Comment** takes no position, and **Suggest alternative** proposes a *path* rather than attesting agreement or
disagreement. **Neither moves Alignment.** They still move **reliability** (they are evidence on the record). D133
ratifies *Approve* and *Reject* as alignment evidence and names no others — so nothing else is assumed.

---

# ⚠️ NEW — escalated, not invented

**Is a *Suggest alternative* also Alignment evidence?**
A reviewer who proposes a different path has arguably said something about alignment too — *"I would not do it this
way"* — but they have **not** attested that the finding does or does not read right. D133 names **Approve** and
**Reject**, and only those. The build therefore treats **Suggest alternative** as *reliability-only* evidence, and
**does not** move Alignment on it.

- **Recommendation (NOT built, NOT canon):** treat it as **weak alignment evidence in the disagreement direction** —
  a proposed alternative implies the current path is not the one this stakeholder would take. *But this is exactly
  the kind of inference the Anti-Assumption protocol forbids*, and the asymmetry risk is real: if an alternative
  counted as a half-Reject and there is no half-Approve, the system would quietly acquire a **negative bias** — the
  very thing D133's symmetry clause exists to prevent.
- **Owner call required.** Options: (a) leave it reliability-only (**current build**); (b) count it as alignment
  evidence in the disagreement direction, and identify its symmetric counterpart; (c) split "Suggest alternative"
  into *"…and I disagree with the finding"* vs *"…and I accept the finding, I'd just fix it differently"* — which
  would make the alignment signal **stated by the reviewer** rather than inferred by OSLO. **(c) is the honest one,
  and it is the recommendation — but it changes CRR-03's four responses, so it is not built.**
