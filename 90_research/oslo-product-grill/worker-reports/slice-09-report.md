# Slice 9 — Collaboration, Sharing & Export · Worker Report

**Built:** 2026-07-10 · **Base:** `slice-08-workspace-awareness/prototype.html` (7,662 lines) → **`slice-09-collaboration-sharing-export/prototype.html` (8,942 lines, +1,280)**
**Decisions implemented:** D110 · D111 · D112 · D113 · D114 (CRR-01…05) · D115 · D116 · D117 · D118
**Status:** Complete. `node --check` passes; jsdom structural parse healthy; **27/27 runtime behavior tests pass, 0 non-environment errors**; Slices 1–8 non-regression verified.

---

## What was built

**D110 — Sharing dialog.** The top-bar **⤴ Share** seam is now real. Invite by email + role picker; **three participant types each with one plain statement** (Owner / Collaborator / Viewer); the current participant list; and a **view-only snapshot link** with copy/preview/revoke. Explicitly **presentation-only** ("roles are shown, not enforced"). A snapshot whose analysis has moved on is **automatically relabelled "previous analysis"** — a stale read is never passed off as current.

**D111 — Comments + @mentions.** Threaded, **append-only** comments **inside the Issue Panel only** (Panel Model — no orphan surface; there is no `editComment`/`deleteComment` in the code). `@` autocompletes teammates plus **"Invite someone new…"** (which opens the sharing dialog). Persistent line: **"Comments never change the assessment."** Every comment appends a History event.

**D112 — Export.** The **⤓ Export** seam is now real: an **analysis-currency marker** (which run produced the read, when, and whether it is Current / Provisional / Last-good — read off `HISTORY`/`TREND`/`ANALYSIS_STATE`, never invented) + the **required disclaimer**. PDF · Copy · Link, with **Free = PDF only** and the others **shown-and-tier-locked**. *"Export generates no new assessment and never triggers an analysis"* — and it is structurally true (no trend point, no status change, no confidence move).

**D113 — Un-gating + Settings.** `mention` / `reply` / `shared with me` flipped to live and on-by-default; a reviewer's response fires a real **reply** notification. **Settings → Collaboration** rewritten from a *"Not built yet"* stub into a real section: participants · **default share role** (persisted) · snapshot-link state · **link expiry (owner-TBD)** · review-request counter.

**D114 — CRR (the centerpiece).**
- **CRR-01** — *Share for review* in the **Issue Panel action row** and the **artifact annotation flyout**. **REC-05**: a new `ISSUES[].rectype` marks validation recommendations (ISS-01, ISS-03), and on those the action is the **primary** button with a *"prime candidate"* line.
- **CRR-02** — a **Review Package preview** before sending: **finding + context + recommendation + artifact reference** (with the traceable evidence lines), a reviewer picker, and an optional note. Send is disabled until a reviewer is chosen.
- **CRR-03** — exactly four responses (**Comment · Approve · Reject · Suggest Alternative**), structured and **preserved in full, forever**.
- **CRR-04** — a response lands as **evidence** and triggers an **Extended Analysis** run **through the existing machinery** (`pushHistory` / `pushTrend` / `_refreshIssueSurfaces` — no parallel path was invented): a real trend point, a real `reanalysis_run` History event, a real Attention repaint, and **reliability rises** (evidence availability).
- **CRR-05** — an **"◷ Awaiting review"** chip on the issue in **both** the Issues list and the Issue Panel, and **MRI-07 Understanding Dependencies** as a **first-class block on Overview *and* Attention**: *"1 issue awaiting sponsor review… this is where understanding is blocked on a person."* Neutral chrome — waiting on a person is not a severity.

**D115 — Reviewer-response semantics (the doctrinal core).** A third epistemic class, **"Attested by \<name\>"** (`.elabel.attested3`, on the neutral `--cool` token), sits beside **"From OSLO"** and **"Confirmed by you"**. A response **never auto-resolves the issue** (`applyReviewResponse()` never writes to `_istatus` — a structural guarantee, not a copy promise). **OSLO never self-accepts.** An Approve renders as *"Marcus Hale **approved this**"* and carries a standing block: *"This is evidence, not a verdict… it is not a finding that the plan is sound, correct, or resolved… **ISS-01 is still Open.** The call is yours."* Confidence may move because **reliability** improved; the **band and the assessment are never overwritten**.

**D116 — Reviewer view (PROPOSAL).** A full-screen demo route with a permanent, non-dismissible **"Proposal — pending owner ratification"** ribbon. **No signup wall**; the reviewer lands straight in the package; responds with one of the four actions; and **only then** does the **convert-moment** appear. A **revoked** link opens **nothing** — not even an old read.

**D117 — Link hygiene.** Links are **revocable** (real revoked state, both sides) and **scoped** (`kind: 'snapshot' | 'issue'`). **Expiry is `null` in code** and renders as **"Not yet set — owner decision"** in a dashed TBD chip.

**D118 — Free CRR cap.** `CRR_CAP = null`. The counter reads **"X of {N} review requests used"** with **{N} as an explicit owner-TBD chip**. The bounded-cap **mechanism** works (`_crrCapReached()` gates *Share for review* and *Send*); with no ratified number it returns `false`, so **Free sends freely** — virality seeds on Free. A *Sim CRR cap* demo trigger pins the cap to what has already been used, making the at-cap state reachable **without inventing an owner value**.

**Chat.** New entry points reusing `askOslo(ctx)` / context pills / `_chatState()` (extended with `awaiting` · `responded` · `blockedIds`): ask about a **review request**, ask about a **reviewer's response**, and **"what's blocking my understanding?"**. Chips track live state. The boundary is hard-coded: `_crrActionAsk()` → `_ansCrrBoundary()` → **"That one isn't mine to take."** The chat **cannot** send, accept, share, export, or resolve; it opens the **preview** and hands the user back to the surface that owns the action.

---

## Verification

1. **`node --check`** — extracted `<script>` body (417 KB, 1 script tag) → **PASS**.
2. **jsdom structural parse (no `runScripts`)** — `body.children.length = **27**` (Slice 8 = 23, + the 4 new top-level overlays: `#shareScrim`, `#exportScrim`, `#crrScrim`, `#reviewerView`). All **33** expected element IDs present.
3. **Grep verification** — every decision has an implementation: D110 (13 refs) · D111 (6) · D112 (8) · D113 (9) · D114 (14) · D115 (11) · D116 (7) · D117 (9) · D118 (10) · CRR-01…05 · MRI-07 · REC-05. All key symbols present (`openShare`, `sendInvite`, `createSnapshotLink`, `revokeLink`, `addComment`, `openCrr`, `sendReviewRequest`, `applyReviewResponse`, `_reviewAnalysisRun`, `openReviewerView`, `renderDeps`, `openExport`, `doExport`, `_crrCounterHTML`, `renderSettingsCollab`, `_ansBlocking`, `_ansReview`, `_ansCrrBoundary`, `attested3`, `SHARE_LINK_EXPIRY = null`, `CRR_CAP = null`).
4. **jsdom runtime suite — 27/27 PASS, 0 non-environment errors.** Every D110–D118 clause is asserted, including the doctrinal ones: an **Approve does not move `_istatus`**; the **band is unchanged** after a response; the panel **explicitly denies** the correct/verified/resolved reading; the **convert-moment is absent before responding and present after**; `CRR_CAP === null`; `SHARE_LINK_EXPIRY === null`; the chat **refuses** to send/accept/resolve.
5. **Non-regression (Slices 1–8)** — onboarding, intake, Overview, Attention map + heatmap, artifact editor, Issues + Issue Panel, History + trend + the new Collaboration filter, Workspace Home, project switcher, notifications, Settings, dark/light theme, ⌘K palette, OSLO chat, feature tour — **all verified intact**.

> jsdom note: top-level `let`/`const` in a classic script are **not** on `window`; the runtime harness reads them via global `eval`. `startTour()` needs `scrollIntoView`, which jsdom does not implement — an **environment** limit, not a product defect (present in Slice 8 too).

---

## Canon tension escalated (NOT invented — see `open-items.md`)

1. **D116 vs the Alpha invite-only constraint (the big one).** `canonical-truth.md` (owner, 2026-07-09) states: *"Alpha & Beta are invite-only (users authenticated from activation, **never anonymous**). Anonymous product access begins at GA."* D116's **no-account-required reviewer** is, on its face, an anonymous product interaction. **I did not resolve this.** I built the reviewer view exactly as D116 specifies, gave it the mandated **"Proposal — pending owner ratification"** ribbon, and escalated the collision in `open-items.md` §1 with three sub-decisions for the owner: (a) is the no-account reviewer R1 or a fast-follow; (b) does the reviewer get a link-borne identity; (c) is the convert-moment in R1 at all when there is nothing to convert into without an invite. My non-binding read — that a link-borne token *is* the invite, which would preserve DL-073/DL-080 phasing **and** leave k unconstrained — is offered as a recommendation, **not** applied.

2. **D110's snapshot link vs D112's tier-locked export "Link".** D112 says *"Free = PDF-only"* (so the export **Link** format is locked); D110 says the sharing dialog carries a *"view-only snapshot link (copy-link)"* with **no tier restriction**. Both are implemented as written, which means a Free user cannot export a "link" but *can* copy a share link. The only reading under which **both decisions are simultaneously true** is that they are **two different objects** — a live, revocable, view-only *share* link vs a frozen, hosted *export* document. I implemented and worded them that way, but **that is an inference about intent** and is flagged in `open-items.md` §4 for ratification or correction.

3. **Does a Reject move CAF?** D115 authorizes confidence movement via **reliability**. A Reject is evidence (reliability rises) — but it arguably also signals *misalignment* between OSLO's read and a stakeholder's, which could plausibly lower **Alignment**. **The prototype does not do this**, because nothing ratifies it. Flagged in `open-items.md` §5.

4. **"Sponsor" — role vs type.** MRI-07's headline (*"awaiting **sponsor** review"*) is driven by the reviewer's *human* role (`TEAMMATES[].role`), not their participant **type** (Owner/Collaborator/Viewer) — two different axes. The decision log's example copy implies the human role is the one meant. Flagged for confirmation.

---

## Deliverables

`vertical-slices/slice-09-collaboration-sharing-export/`
- `prototype.html` — cumulative Slices 1–9, single self-contained file (8,942 lines)
- `product-detail.md` · `user-experience.md` · `workflow.md` · `frontend-ui.md` · `product-data.md` · `success-criteria.md` · `e2e-test-scenarios.md` — **the established 7-doc house format**, matching Slices 1–8 exactly
- `edge-cases.md` — new (this slice has a large doctrinal surface worth enumerating)
- `open-items.md` — **the owner-open items**: reviewer experience R1-vs-fast-follow (D116, proposal) · share-link expiry (D117, gap #339) · the Free CRR cap number (D118) · the D110/D112 link tension · four lower-stakes items

**Doc-naming note.** The task brief listed `README / user-stories / acceptance-criteria / ux-notes / data-model / edge-cases / open-items`, but instructed *"matching the format of the slice-08 docs exactly."* Slices 1–8 all use `product-detail / user-experience / workflow / frontend-ui / product-data / success-criteria / e2e-test-scenarios` — the same seven content areas under the house names. I followed the **house format** (cumulative consistency wins) and added **`edge-cases.md`** and **`open-items.md`** on top, so every content area the brief named is covered. Say the word if you want the files renamed.


---

# AMENDMENT — Controlled Release & Demand (D119–D122) · 2026-07-10

Owner-directed amendment to **D116 / D117 / D118**, per `controlled-release-demand-framework.md`. Amended **in place** in `vertical-slices/slice-09-collaboration-sharing-export/prototype.html` (8,942 → **9,563 lines**). No Slice 1–8 surface was touched except the phase bar (which gained **Beta**) and the notification/History enums (which gained access events).

## What changed

**D119 — the reviewer view is now GATED, not open.** The review link carries a **token that grants Reviewer Principal access (DL-049)**, scoped to exactly that package. **The invite is the authentication.** The reviewer lands on a one-click grant screen — *"Idris invited you to review one finding"* — named, invited, **never anonymous** (D021 satisfied), with **no password field anywhere in the flow**. The scope is stated out loud: *this one package, nothing else in the project*. At **GA** the grant screen is skipped entirely. The **Proposal ribbon stays** — CR-7 is still owner-open. **This closes my escalation #1.**

**D120 — bound seats, never bound evidence.** This is the rule I was most careful with, because getting it wrong does real damage. `_reviewCost(email)` returns **`free`** for an existing principal and **`admit`** for a new person — that one function *is* the rule. Consequences, all verified:
- **`Share for review` is never disabled.** I **removed** the D118-era at-cap disable on the Issue-Panel button.
- With the allocation **fully spent**, sending to an **existing** principal is **still enabled**. Verified in a headless run.
- Sending to an existing principal **never increments `ADMISSIONS`**.
- The picker states the cost **on the person**: *"free — already in"* vs *"new — admits them (cost owner-TBD · CR-2)"*.
- The counter is a **fact, not a limit**: *"N review requests sent · never metered when the person is already here."*
- **DL-049 in-place promotion**: granting a reviewer a seat promotes the **same** Principal (`reviewer → user`) — no duplicate account.

**D121 — controlled release.** Bounded, replenishing allocation (**{N}/{period} = CR-1, `null`, rendered unset**). A waitlist with **real positions** (#N of M) and recorded demand signals (referral · **review-requested** · fit). **Skip-the-line** from the Access modal *and* from the issue (*"Grant Marcus a seat →"*). The **convert-moment is the waitlist, post-value only**. A **three-phase ramp wired to the existing D072 phase bar** — Alpha → Beta → **GA (open, anonymous permitted, waitlist retired, tier-based limits)**; switching the phase **visibly** changes the gating, so the mechanism demonstrably **sunsets**. **Demand instrumentation** (waitlist size/velocity, admissions, review-request→admit, k) — real counts where they exist, **`simulated data`** chip where they don't, and **holes rather than numbers** where a metric needs an unset owner value.

**D122** — the **CHG-061 tension is stated in-product** as an escalation requiring a Framework 001 proposal. Not resolved.

**D118 reconciled.** `CRR_CAP` stays `null` — but it now governs **new-principal admissions**, never review requests.

**Escalation #2 (share link vs export link) — resolved as directed.** Two objects, two names, an explicit disambiguation block in **both** surfaces. Export's `Link` format is renamed **`Export link`**.
**Escalation #3 (does a Reject move CAF?)** — still unimplemented, still escalated. Nothing ratifies it.
**Escalation #4 ("sponsor" = `TEAMMATES[].role`)** — kept, still flagged.

## Guardrails — how I held them

- **No fabricated scarcity.** Grep-verified: the built file contains **no** *"spots left"* / *"only N left"* / *"limited time"* / *"act now"*. With `{N}` unset there is **no remaining-balance number at all** — the field renders as a dashed **owner-TBD (CR-1)** chip. The only counts on screen are real ones.
- **No dark patterns.** No countdown, no pulse, no urgency color, no loss framing. Access chips use the **neutral** `--cool`/`--muted` tokens — the **severity ramp is never used for access state** (D003).
- **The waitlist says what it is, and why**, in the first sentence: *"we are deliberately limiting how many people we let in — not to make you want it, but because we can only do this properly for a small number of people at a time."*
- **Simulated data carries a chip** in the same visual family as the owner-TBD chip — because *"we made this up for the demo"* and *"nobody has decided this"* are the same **kind** of honesty.

## Verification (all four, all passing)

1. **`node --check`** on the extracted script body → **PASS**.
2. **jsdom without `runScripts`** → body children **28** (prior build 27, + `#accessScrim`). Healthy.
3. **D110–D122 grep** → every decision has an implementation (D119: 14 refs · **D120: 34** · D121: 28 · D122: 6).
4. **Non-regression** — headless jsdom (`runScripts:'dangerously'`): **0 boot errors**; every Slice 1–8 entry point resolves (onboarding, intake, Overview, Attention, Artifacts+editor, Issues, History, Workspace/Settings, chat, theme, palette); every Slice-9 surface resolves; exercising all surfaces → **0 runtime errors**.
   Behavioral asserts: free-request → 0 admissions · grant landing renders & is scoped · post-grant identity line · convert = waitlist (and **no** pre-value signup) · new-person request → 1 admission + principal created · **allocation spent + existing principal → Send still enabled** · in-place promotion → `PRINCIPALS.length` unchanged · GA → waitlist retired + anonymous permitted.

**One bug caught and fixed during verification:** the Issue Panel's *Share for review* button still called the deleted `_crrCapReached()` and **disabled itself at the cap** — precisely the D120 violation the direction warns about. Removed.

## NEW canon tension — escalated, NOT invented (see `open-items.md`)

- **N-1 — Do tier limits (Free = PDF-only, D112/D118) even cohere during Alpha?** In Alpha *everyone* is on Free (billing is deferred, D048), so the **tier** limit and the **phase** limit stack on a population that can lift neither. That may be intended — or tier limits may need to be **inert until GA**, which is the mirror image of the D122 reconciliation. **I changed nothing.** Owner decision.
- **N-2 — `PARTICIPANTS[]` (D110) and `PRINCIPALS[]` (DL-049) are now two registries of "who is here."** I kept them **separate**, because a Reviewer Principal's grant is **scoped to one package**, not to the project — that is the only reading consistent with D119. But the relationship between the two models **is not specified in canon**. If a single registry is intended, that is a data-model decision to ratify.
- **N-3 — Skip-the-line admits someone as *what*?** D121 says "admit someone from the waitlist immediately" but never says **which seat**. I used **Collaborator** (the useful default for someone who just gave you evidence). **The framework does not make this choice.** Confirm or correct.

## Docs updated

`product-detail` · `user-experience` · `workflow` · `frontend-ui` · `product-data` · `success-criteria` · `e2e-test-scenarios` (the house 7) + `edge-cases` + `open-items` — each carrying an **AMENDMENT (D119–D122)** section, with the now-superseded D116/D118 passages marked in place rather than deleted (lineage preserved). **`open-items.md` now carries the full CR-1…CR-7 owner-TBD register**, the D122 escalation, and N-1…N-3.

---

# APPENDED 2026-07-11 — Amendment: the ratified register (D123 · D124 · D125 · D126)

Amended `slice-09-collaboration-sharing-export/prototype.html` **in place** (9,563 → **10,199 lines**) plus all 8 house docs + `open-items.md`.

## The headline change

**Tier gating is LIVE in Alpha (D123).** The previous build assumed tier limits were effectively moot in Alpha. They are not — Basic is purchasable. That reversal (**N-1 withdrawn**) is the load-bearing change, and it forced everything else.

**D126, printed verbatim in-product** (Access & invites, and Plans):
> *Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.*

## What changed in the prototype

**D124 — two limits, never conflated.** One function, `checkAdmission(email, role)`, produces **every** blocked state in the product and returns `limit: 'phase' | 'tier' | 'both'`. `admissionBlockHTML()` renders **one box per limit**, in two deliberately different colours (`.lim-phase` cool · `.lim-tier` brand). They are never merged.
- The **PHASE** message says *"You're out of invites for this month — replenishes {date}"*, states that this is **supply, not plan**, offers the **waitlist**, and **carries no upgrade CTA** — because selling a way out of a supply constraint is the dark pattern D124 prohibits. (That Basic carries more invites is stated on the **Plans** surface, where it belongs — never at the moment of blocking.)
- The **TIER** message says *"Free projects hold {N} collaborators — Basic holds more"*, states that **your invites are untouched**, offers the **free remedy first** (Viewer takes no seat), then a real upgrade path.

**CR-2 — reviewer grants free and unmetered.** `_reviewCost()` is now a **constant function returning `'free'`**. `sendReviewRequest()` has **no allocation check and no tier check** — deliberately, and the comment says so. A **regression guard** sits at `_grantReviewerAccess()`: a runtime assertion that the invite ledger did not move (logs `CR-2 VIOLATION` and reverts), above a DO-NOT-REMOVE block explaining that this is the *sole* thing keeping the framework consistent with CHG-061 now that the tier rule is live in Alpha, and that changing it is a **canon violation** requiring Framework 001 — not a product tweak. The **DL-048 token budget** is described in-product as a **cost** control on compute, never a monetization gate.

**N-2 — one identity.** `PARTICIPANTS[]` is **deleted**. `Principal` (DL-049) + **`Membership`** (principal × project × role — *where the tier seat cap is enforced*) + **`ReviewGrant`** (principal × package, scoped, expiring). "Participant" is now a **view** (`_members()`). A reviewer holding only a `ReviewGrant` is **not a member and consumes no seat**, and is shown as such in the Share dialog.

**N-3 · CR-4 · CR-5 · CR-6 · CR-7 · CR-1/T-2 · CR-3 · T-1 · T-3 · T-4** — all implemented; see `product-detail.md` → *AMENDMENT*. Notably: waitlist admits land as **Viewer** (one click to Collaborator); the waitlist is **three honest bands, date-ordered** with **no points economy** and the old weighting-preview toggle deleted; share links are **30 days** and review grants die **when the issue resolves or at 14 days**; **pay-to-skip is not built and not hinted at**; a real **(simulated) Free→Basic upgrade path** ships with an **unset price**.

**Deleted (do not resurrect):** `CRR_CAP`, `_crrCapSet()`, `simCrrCap()`, `_costWord()`, `REVIEWER_GRANT_COST`, `crrWaitlist()`, `toggleWlPreview()`/`WL_PREVIEW_WEIGHTS`, `PARTICIPANTS[]`, `SHARE_LINK_EXPIRY`.

## Verification — all four, all passing

1. **`node --check` on every `<script>` body** — 1 script, 7,096 lines → **PASS**.
2. **jsdom parse WITHOUT `runScripts`** → **body child count 29** (prior build 28; +1 = the new `#plansScrim`). All expected IDs present.
3. **Grep-verified D110–D126** — every decision has an implementation (D125×5, D126×14, D124×32, CR-2×56, T-1×32 …).
4. **Non-regression** — boot with `runScripts:'dangerously'`: **0 console errors**; every Slice 1–8 and Slice 9 surface renders without throwing.

## Behavioural checks — all passing

| Check | Result |
|---|---|
| **(a)** Allocation fully spent + reviewer is a **NEW** person → **review request STILL SENDS** | **PASS** — `REVIEWS` +1, `ADMISSIONS` unchanged, `_seatsUsed()` unchanged |
| **(b)** Tier seat cap hit → message names the **TIER** limit (and never says "out of invites"); allocation exhausted → message names the **PHASE** limit (and carries **no upgrade CTA**) — never swapped | **PASS** — asserted on the rendered HTML, both directions, plus the `'both'` case rendering two separate boxes |
| **(c)** Reviewer with only a `ReviewGrant` consumes **no seat** | **PASS** — is a Principal, is **not** a Member, seats unchanged |
| **(d)** Flip phase to **GA** → allocation + waitlist + gate retire; **tier limits stay in force** | **PASS** — `phase:false`, `tier:true`; Free still PDF-only |

## Owner-TBD — rendered UNSET, never invented

**Basic price (T-3)** · **exact Free-vs-Basic numeric caps** — projects/artifacts/analysis-frequency/retention **and the collaborator-seat number** (T-1 gives the shape, not the numbers) · **configurable link expiry for Basic (CR-6)** · **whether revenue ever expands onboarding capacity** (would re-open CR-7 — not modelled, not hinted at).

## NEW canon tension found while building — **escalated, not invented**

**X-1 — is the collaborator-seat NUMBER owner-TBD, or was it ratified?** The task's own TBD list names *"projects/artifacts/analysis-frequency/retention"* but **omits seats**, while T-1's shape list **includes seats** and D124's own example copy uses a placeholder (*"Free projects hold N collaborators"*). Nothing in D123–D126 ratifies a seat number. **I therefore treated it as owner-TBD**: the cap renders **unset** and **enforces nothing**, and a demo trigger pins it to seats already filled so the tier-blocked state is *reachable* without inventing a value. **If the owner intended a ratified seat number, it needs to be stated** — this is the only place in the register where the shape is ratified but the number is load-bearing for a *live* Alpha limit.

**X-2 — does an invite get refunded when a Membership ends?** Not specified. The build says **no** (an invite admits a *human*, not a membership; the human is still a Principal). Stated in the History event so the user is never surprised. **Confirm or correct.**

**X-3 — CR-1 says "per month" but not *which* month boundary.** The build derives a **real** replenish date as the **1st of the next calendar month** from the ratified `ALLOCATION_PERIOD = 'month'`. If the owner intended a rolling 30-day window per user, that is a different (and equally honest) reading. **Low stakes; flagged rather than assumed.**

**Still routing through Framework 001** (recommendation, not canon — nothing in the build treats these as ratified): D122's CHG-061 reconciliation **via CR-2** · D123's tier-live-in-Alpha consequences (DL-048 "paid-tier limits TBD" is now **blocking**, not deferred) · the **T-1 numbers**.

**Prior escalations, still unresolved:** does a **Reject** move CAF (not just reliability)? · is *"sponsor"* in MRI-07's headline `TEAMMATES[].role` (the build assumes yes — **confirm**)? · should a removed member's **pending** review grant be auto-revoked?

---

# Slice 9 — D128–D131 fold-in (open-items register, RATIFIED) · 2026-07-11

**Target:** `vertical-slices/slice-09-collaboration-sharing-export/prototype.html` — amended **in place**.
Plain JS · localStorage · fake data · simulated AI. No backend, no auth, no real AI, no billing.

## What changed

### D128 — the two governing principles (they now sit *above* every metering rule in the file)

**P1 — never meter the epistemic record.** New constant block at the top of the tier section declares the **entire**
set of meters: `METERED_DIMENSIONS = ['extended-analysis-runs','projects','collaborator-seats']`. Added
`ARTIFACTS_METERED = false`, `HISTORY_METERED = false`, `ARTIFACT_CAP = {∞,∞}`, `HISTORY_RETENTION = {full,full}`.

**Removed the pre-existing violation.** The previous build **sold the epistemic record**: `BASIC_ARTIFACT_CAP` and
`BASIC_RETENTION` existed as constants, and Plans / Settings / the upgrade prompt all advertised *"more artifacts"*
and *"longer history retention"* as **Basic features**. Both constants are **deleted** and every line of that copy is
**gone**. (No enforcement code ever existed — the violation was in the selling proposition, not the mechanism.)
**Comment guards** now sit at `pushHistory()` and at the artifact-version store stating that the record is never
metered, so it cannot be quietly reintroduced.

**P2 — never sell safety.** `CONFIGURABLE_EXPIRY_BASIC` moved from `null` (owner-open) to **`false` (CLOSED, not
built)**. Added `LINK_SECURITY_TIER_LOCKED = false`. Every "configurable expiry (Basic) — owner-open" chip is
replaced with *"same on every plan — safety is never sold"* / *"Closed — not built (D128)"*. Verified: `revokeLink()`
contains **no `TIER` reference**.

### D129 — the ratified register

- **X-1 (seats).** `SEAT_CAP = {free: 3, basic: 10}` — **ratified and enforced** (replaces the previously
  unset/unenforced cap). `VIEWER_CAP = {∞, ∞}` — **viewers unlimited on every tier**. The seat cap is enforced on
  **Membership**, and only for seat-holding roles, so **a Viewer is structurally unblockable** on the seat axis.
  Added `_assertViewersUnlimited()` as a runtime guard alongside the existing CR-2 guard. The tier-blocked state is
  now **genuinely reachable** through the ordinary UI (Free starts at 2 of 3 seats).
- **X-2 (invite refunds) — the missing mechanism, now built.** New `INVITES[]` state machine:
  `inviteNewHuman()` → **pending** (HOLDS an allocation unit) → `acceptInvite()` (**spent for good, never refunded**)
  or `expireInvite()` (**REFUNDED**, with a History event, and the reserved seat released). Allocation arithmetic is
  now `_allocUsed() = accepted + pending`. Both outcomes are reachable in one click from the participant row.
- **X-3.** Confirmed as built; `ALLOCATION_PERIOD = 'calendar-month'`, UI says *"resets {1st of next month}"*.
- **T-1.** `FREE_ACTIVE_CAP = 1` · `BASIC_PROJECT_CAP = 10` · `SEAT_CAP` above · **artifacts unlimited · History
  full** on both tiers. Extended Analysis: `ANALYSIS_BUDGET = {free: null, basic: null}` (**numbers NOT invented**)
  plus `ANALYSIS_BUDGET_SHAPE` for the ratified shape (small / generous). Plans + Settings → Subscription rewritten
  to state, prominently, that **artifacts and History are unlimited on every tier**.
- **Sponsor = `TEAMMATES[].role`** — confirmed, unchanged.

### D130 / D131 (docs + one in-product note each)

D130: a standing note in the Demand panel that 3 / 10 / 1 are **hypotheses, easy to loosen and painful to tighten**,
plus a full "what to instrument" section in `open-items.md`. D131: the Access modal now names the **ONE consolidated
Framework 001 proposal — "Controlled Release & Tiering-in-Alpha"** — and states plainly that **Reject-moves-CAF is
unratified and unbuilt**.

### Deliberately NOT built (owner-open)

**Basic price (T-3)** — renders unset. **Extended-Analysis run counts** — render unset. **Reject-moves-CAF** — out of
the build, escalated. **Pay-to-skip** — prohibited, unbuilt, unhinted. **Configurable expiry for Basic** — closed.

## Verification

| Check | Result |
|---|---|
| `node --check` on the extracted `<script>` | **PASS** |
| jsdom parse **without** `runScripts` | **29 body children** (unchanged from the prior build) |
| Boot with `runScripts: 'dangerously'` | **0 runtime errors** |
| D110–D131 each have an implementation | **PASS** (D131 = the in-product Framework-001 routing note + docs) |
| Non-regression: Slices 1–8 + existing Slice 9 | **PASS** — every shell id, pane, overlay and render path exercised; all 5 views switch; D127 dark default intact |
| **Behavioural assertions** | **43 / 43 PASS** |

**(a)** Free, 3 collaborators → a 4th **Collaborator** is **blocked**; `limit === 'tier'`; the message names the
**TIER** limit and **never** says "out of invites". ✅
**(b)** Same project → adding a **Viewer** **succeeds**; `_seatsUsed()` unchanged; viewers unlimited. ✅
**(c)** Allocation fully spent + brand-new reviewer → the review request **still sends**; **no invite consumed**; the
CR-2 guard holds. ✅
**(d)** Pending invite **expires → REFUNDED** (balance restored, History event, seat released); **accepted → never
refunded**, including on removal. ✅
**(e)** **No tier caps artifacts. No tier truncates or expires History.** Asserted structurally (constants, absence of
any cap/trim/tier code, `HISTORY.length` invariant across tier switches, deleted constants). ✅
**(f)** Link **revocation + purpose-scoped expiry work on Free**; no tier-lock anywhere. ✅
**(g)** **GA:** allocation + waitlist + gate **retire**; the **tier seat cap still binds**; viewers still unlimited. ✅

## NEW canon tensions — **ESCALATED, not invented**

1. **X-2a 🆕 — how long does a pending invite live before it expires?** D129 ratifies the **refund**, not the
   **window**. The refund is fully built and real; the **window renders unset** (`INVITE_EXPIRY_DAYS = null`) and
   expiry is driven explicitly rather than by an invented clock. **Needs an owner decision** (a number of days).
2. **Seat cap vs downgrade.** Basic (10 seats filled) → Free (cap 3): **nothing ratifies what should happen.** The
   build takes the conservative, non-destructive path — **nobody is evicted**; you simply cannot *add* another
   Collaborator until you are back under the cap. Evicting humans from a project to enforce a billing change would
   be a severe move on a product built on trust. **Flagged as a recommendation, not assumed as canon.**

Both are recorded in `open-items.md`.

## Docs updated

All 7 house docs + `edge-cases.md` + `open-items.md`. Superseded passages are **marked in place** (struck through /
banner-flagged), never deleted — including the now-dead "T-1 numbers unset", "seat cap enforces nothing", "Basic
sells more artifacts / longer retention" and "configurable expiry — owner-open" rows.

---

# Fold-in — D132 (Slice 9 CLOSED) — 2026-07-11

The two items the previous build **escalated rather than assumed** came back **ratified**. Both are now built, and
both TBD placeholders are gone. Nothing else changed.

## 1. X-2a — `INVITE_EXPIRY_DAYS = 14` (was `null` / "unset")

The pending-invite window is real. Every invite is stamped with an **`expiresAt`** at send (`now + 14 days`,
computed **once**), and the date is surfaced honestly on the pending row, in the pending-invites box, in
Settings → Collaboration, in History, in the notification and in the toast:

> *"Expires **25 July** — the invite **returns to your balance** if unused."*

**The design rule I held to:** *the date and the refund are never separated.* An expiry date on its own reads as
manufactured scarcity; the refund is the entire point of X-2. So `_inviteExpiryLine()` is the single function that
emits both, and every surface calls it. There is **no countdown, no urgency colour, and no "expires soon" nudge** —
there is nothing to hurry, because you are made whole automatically. On expiry the invite **refunds** (D129) with a
History event that names the 14-day window and the before/after balance. An **accepted** invite is still **never**
refunded. The `owner-TBD (X-2a)` chip is **removed from the code and the DOM.**

## 2. Seat cap vs downgrade — **NO EVICTION** (the conservative path, now ratified)

Basic (10 collaborators) → Free (cap 3): **nobody is removed.** Confirmed by construction and by test —
**`setTier()` touches `MEMBERSHIPS` zero times**, and there is **no code path anywhere that removes a Membership on
a tier change.**

Made legible rather than merely true. `_seatsOverCap()` is the new state; `_overCapNoticeHTML()` is the single
function that renders it into the **Share panel · Settings → Collaboration · Settings → Subscription · the Plans
modal · every TIER-blocked message**, so it can never drift. It **leads with the reassurance**, because that is the
reader's actual question:

> *"This project has **10** collaborators; Free adds up to **3**. **No one has been removed** — you can't add more
> until you're under 3, or upgrade."*

…then the only real consequence (**you can't ADD**), then the free remedies (**Viewer** — unlimited, no seat;
**review request** — free, CR-2). Every TIER-blocked message was audited so that **none of them can imply an
eviction**: over the cap, "all N seats are filled" would be both false and alarming, so those messages now branch.

Enforced in code, not just in prose:
- `const EVICT_ON_DOWNGRADE = false;` — *"There is no number to set and no branch to add."*
- **Code comment (verbatim, as directed):** *evicting humans from a project to enforce a billing change is
  prohibited on a trust product* — with the reasoning: it mutates the cast of characters in an append-only record
  as a side-effect of a payment event, and it is the most self-refuting act a trust product could commit.
- **Runtime guard `_assertNoEvictionOnDowngrade()`** — `setTier()` snapshots the roster and asserts afterwards. A
  deliberate eviction was staged in test: the guard **fired and restored the full roster**. It is the sibling of the
  existing CR-2 and X-1 guards.
- The **Plans modal now states the downgrade contract up-front**, on the page where a downgrade is initiated — so a
  Basic user never has to wonder what will happen to their people.

## Verification (all re-run after the fold-in)

| Check | Result |
|---|---|
| `<script>` extracted → `node --check` | ✅ **PASS** |
| jsdom parse **without** `runScripts` → body child count | ✅ **29** (unchanged from prior) |
| Boot **with** `runScripts` → console errors | ✅ **0** |
| **D110–D132** all present & implemented (grep) | ✅ all 23 present |
| **(a)** pending invite expires after 14 days → **REFUNDED** (5→4→5); `expiresAt` exactly **+14d**; History event names the window | ✅ **PASS** |
| **(a)** **accepted** invite → **NOT** refunded (5→4, stays 4); `expireInvite()` on it is a **no-op** | ✅ **PASS** |
| **(b)** Basic @ 10 seats → Free (cap 3) → **not one Membership removed** (roster byte-identical); `_seatsOverCap()` true; History only grows | ✅ **PASS** |
| **(b)** 11th Collaborator **blocked** — `.limit === 'tier'`, `.phase === false`; message names the **plan/tier** limit, says **nobody removed**, **never** says "out of invites" | ✅ **PASS** |
| **(b)** the no-eviction guard **actually fires** on a staged eviction and **restores the roster** | ✅ **PASS** |
| **(c)** **CR-2 guard**: allocation fully spent (0 left) + **brand-new** reviewer → review request **still sends**, spends **no invite**, creates **no Membership**, no CR-2 violation | ✅ **PASS** |
| **(c)** `_assertViewersUnlimited()` — a Viewer is still admissible **over the cap** | ✅ **PASS** |
| **(d)** no artifact cap (`ARTIFACT_CAP = {∞,∞}`), no History truncation (200 events pushed, none dropped); `METERED_DIMENSIONS` is exactly the ratified 3 | ✅ **PASS** |
| **(e)** Slices 1–8 + 9 non-regression: **22 render functions** across all slices open/close/render on **Free and Basic** | ✅ **0 errors** |
| Guardrails: `PAY_TO_SKIP === false` · `BASIC_PRICE === null` · `ANALYSIS_BUDGET {null,null}` · `REJECT_MOVES_CAF` **undefined** · `CONFIGURABLE_EXPIRY_BASIC === false` | ✅ **PASS** |

## Still deliberately UNBUILT / owner-open (unchanged)

**Basic price (T-3)** — renders unset · **"Does a Reject move CAF?"** — recommendation exists, nothing ratifies it,
**stays out of the build** · **pay-to-skip (CR-7)** — **PROHIBITED**, unbuilt, unhinted · **T-1 residual**
(Extended-Analysis run counts) — unset · **T-4** (billing rail) — out of scope.

## New tension surfaced

**None.** D132 closed both of the items this slice had escalated, and the fold-in surfaced no new canon gap. Slice 9
carries **zero escalations** out of this build.

One observation, offered as an observation and **not** acted on: the waitlist copy contains the sentence *"Nobody can
pay to skip this queue (CR-7)"*, and the Settings search index contains the token *"skip the line"*. Both are
**pre-existing**, both are **prohibition/among-search text rather than a feature hint**, and I left them alone — but
if the owner reads "unhinted" strictly enough to exclude even *naming the prohibition*, that line is the one to look
at. I did not change it, because stating what OSLO will not do is the same move the "never sell safety" and "never
meter the record" copy already makes, and removing it would make the guardrail invisible rather than absent.

## Docs updated

`edge-cases.md` (E9d-6, E9d-12 → RATIFIED) · `open-items.md` (X-2a + downgrade moved **OPEN → CLOSED by D132**;
remaining owner-open items preserved: Basic price, Reject-moves-CAF, whether revenue expands onboarding capacity) ·
`product-data.md` · `product-detail.md` · `frontend-ui.md` (new helpers + the guard) · `workflow.md` (new **Flow C″**
— downgrade with no eviction) · `user-experience.md` (the pending-invite date; the new *"you downgrade, and nobody
disappears"* moment) · `success-criteria.md` (two new D132 sections) · `e2e-test-scenarios.md` (**S9e-1…S9e-6**).

---

# FOLD-IN — D133: a Reject MOVES CAF, via Alignment (owner: ratified, 2026-07-10)

**The last open Slice 9 escalation is closed.** `REJECT_MOVES_CAF` — carried as owner-open and deliberately
**unbuilt** through D129/D132 — is now **RATIFIED and BUILT**.

## What changed in the prototype

**1. Alignment became a live CAF dimension.** It was hardcoded (`Moderate` / 55%) in the Overview markup, the
confidence popover, and `_chatCaf()`. It now lives on the `READ` model as `alignLvl` / `alignW`, exactly as
`feasLvl` / `feasW` already did:
- `renderAlignRow()` paints `#cg-align`, and **computes the limiting dimension** rather than hardcoding it —
  Alignment can now *be* the limit, and the **Why** box (`#why-caf`) names it when it is.
- `renderConfPop()` paints `#cpp-align`. `_chatCaf()` reads it live, so every chat answer that cites CAF is
  grounded in the real read (never fabricated).
- `_cafLevelFor(w)` derives the band word from the **same scale the drafted read already used**
  (Clarity 76 = High · Alignment 55 = Moderate · Feasibility 38 = Low · 30 = Very Low).

**2. A Reject is Alignment evidence — through the existing machinery, not a new path.**
`ALIGN_EVIDENCE[]` (`{rid, issueId, by, kind}`) records the attested input; `_reviewAnalysisRun()` — the **same**
function, the **same** `pushHistory` / `pushTrend` / `_refreshIssueSurfaces` calls every other run in the app makes
— now moves **Alignment** as well as **Reliability**. There is no parallel analysis path and no special case for
Reject.

**3. Symmetry is structural, not editorial.** `ALIGN_STEP = 8` is applied `+` for an **Approve** and `−` for a
**Reject** — one constant, one ledger, one run. The code cannot privilege a direction without someone deliberately
splitting that constant, and the comment at the site says so. The **copy** carries the same symmetry: the response
card's alignment block has an identical wording shape in both directions, and states outright that *"an Approve and
a Reject carry the same weight here — OSLO does not privilege the direction it is pointed in."*

**4. The D115 bounds are untouched — and now guarded in two directions.**
- **Evidence, not truth** — `.elabel.attested3` *"Attested by \<name\>"*; the assessment is never overwritten.
- **Never auto-resolves, never auto-re-opens** — the CRR module writes `_istatus` **zero times**. Verified
  behaviourally on **both** a Reject and an Approve (`_istatus` byte-identical before/after).
- **OSLO never self-accepts** — the card reads *"\<Name\> **rejected this**"*. Every occurrence of
  "wrong" / "invalid" / "re-opened" in the response card is an explicit **negation** ("it is **not** a finding that
  OSLO was wrong, and the issue has **not** been re-opened or invalidated").

**5. The read may now fall.** A Reject sends Alignment down and Reliability up, so the confidence index can drop.
That is the honest outcome, and the trend line already renders a fall **with its cause** (D097). The run copy names
the cause explicitly: *"…that is evidence about alignment, and the read now knows the plan is contested (not that it
is wrong)."*

**6. Copy surfaces updated:** the response card (new *"Folded into Alignment — as evidence (D133)"* block, with a
**what this does not mean** clause), the chat run narration, `_ansReview()`, the Alignment tooltip and the Why box
(both now state the attested evidence on the record), the Sim-response demo tooltip, and the Access modal — which
flipped from *"deliberately absent from this build"* to *"ratified (D133) and built"*.

## What was deliberately NOT built

**Comment** takes no position; **Suggest alternative** proposes a *path* rather than attesting agreement or
disagreement. **Neither moves Alignment** (both still move reliability). D133 names **Approve** and **Reject** and
names no others — so nothing else was assumed.

## Verification

| Check | Result |
|---|---|
| `<script>` extracted → `node --check` | ✅ **PASS** |
| jsdom (no `runScripts`) → body child count | ✅ **29** (unchanged) |
| **D110–D133** all present/implemented | ✅ **PASS** (D127 dark-default intact) |
| (a) Reject triggers an analysis run; moves **Alignment** (55→47) **+ Reliability** (evidence → High); TREND + HISTORY grow; run is a `reanalysis_run` through the existing machinery | ✅ **PASS** |
| (b) Reject does **NOT** change `_istatus` — no auto-resolve, no auto-re-open | ✅ **PASS** (byte-identical) |
| (c) Labelled **"Attested by Priya Raman"**; never OSLO's read; every "wrong/invalid/re-opened" string is a **negation** | ✅ **PASS** |
| (d) **Approve is also Alignment evidence** (47→55) — **equal magnitude**, opposite sign; likewise never auto-resolves | ✅ **PASS** |
| Comment/alternative → reliability only; `ALIGN_EVIDENCE` records only approve/reject | ✅ **PASS** |
| (e) `CR2_REVIEWER_GRANTS_FREE === true` · `ARTIFACTS_METERED === false` · `HISTORY_METERED === false` · History append-only (no truncation) · `EVICT_ON_DOWNGRADE === false` · `PAY_TO_SKIP === false` · `BASIC_PRICE === null` · phase/tier messages never swapped (D124) | ✅ **PASS** |
| (f) Slices 1–8 + Slice 9 non-regression; Overview + popover Alignment rows render the live level; no runtime errors | ✅ **PASS** |

## NEW TENSION — escalated, not invented

**Is a *Suggest alternative* also Alignment evidence?** A reviewer proposing a different path has arguably said
something about alignment (*"I wouldn't do it this way"*) — but they have **not** attested that the finding does or
does not read right. D133 ratifies Approve and Reject only.

The trap: if an alternative counted as a **half-Reject** and there is no symmetric **half-Approve**, the system
quietly acquires a **negative bias** — the exact failure D133's symmetry clause exists to prevent. So the build
leaves it as reliability-only evidence.

**Recommendation (NOT built, NOT canon):** split *"Suggest alternative"* into *"…and I disagree with the finding"*
vs *"…and I accept the finding, I'd just fix it differently."* That makes the alignment signal **stated by the
reviewer** rather than **inferred by OSLO** — which is the only version consistent with "evidence, not truth." But
it changes CRR-03's four responses, so it needs an owner decision.

## Docs updated

`open-items.md` (**`REJECT_MOVES_CAF` OPEN → ✅ RATIFIED (D133)**, history preserved in place; new D133 closure
section; new escalation) · `edge-cases.md` (approve/reject/symmetry/alternative rows rewritten; **E9d-13** flipped
to RATIFIED; new **E9d-13a**) · `product-detail.md` (new **D133** section) · `product-data.md` (`ALIGN_EVIDENCE[]`,
`ALIGN_STEP`, `READ.alignLvl/alignW`) · `frontend-ui.md` (the live Alignment row, no new CSS) · `workflow.md` ·
`user-experience.md` · `success-criteria.md` (new D133 section) · `e2e-test-scenarios.md` (five new D133 checks).
