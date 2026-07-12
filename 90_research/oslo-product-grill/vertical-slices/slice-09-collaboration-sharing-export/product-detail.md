# Slice 9 — Collaboration, Sharing & Export · Product Detail

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. This document specifies the behavior of each Slice-9 surface at product-requirement granularity. Advisory-only, presentation-only, client-side (D016). No auth, no permission enforcement, no email, no PDF engine, no billing.

## Doctrinal spine of this slice (D115) — read first

A reviewer's response is **evidence, not truth**. Every surface below is built to that constraint:

- It enters the record as a **third epistemic class — "Attested by \<name\>"** — distinct from **"From OSLO"** (derived) and **"Confirmed by you"** (owner-attested).
- It **never auto-resolves the issue.** The issue stays Open/Addressed. Only an analysis update moves the read (D006/D088), and the user still decides.
- **OSLO never self-accepts.** There is no autonomous acceptance path anywhere in this slice.
- An **Approve** reads as *"\<Name\> approved this"* — evidence that a stakeholder approves. It is never rendered as correct, resolved, verified, or sound.
- **Confidence may move** because **reliability** improved (a third party put evidence on the record). The **assessment is never overwritten** by a stakeholder's assertion.

## D110 — Sharing dialog

**Entry.** Top-bar **⤴ Share** (was a Slice-9 seam toast) → `openShare()`. Also reachable from Settings → Collaboration → *Manage sharing*.

**Content.**
- **Invite by email** — an email field + a role picker (Collaborator / Viewer) + **Invite**. Adding a participant appends a **History** event. No email is sent; the copy says so.
- **Participant types**, each with **one plain statement** of what they can do:
  - **Owner** — Can change the plan, share it, export it, and send review requests.
  - **Collaborator** — Can comment and answer a review request — but can't change the plan.
  - **Viewer** — Can read the plan and OSLO's read of it. Nothing else.
- **People on this project** — avatar · name · email · type chip · Remove. Removing a person keeps their comments and responses (the record is append-only, D096).
- **View-only snapshot link** — *Create a view-only link* → a revocable, project-scoped link with **Copy link**, **Preview what they see**, and **Revoke**.

**Honesty.**
- **Roles are shown, not enforced.** R1 has no permission engine; the dialog states the *intent* of each type so it is legible before it is enforced.
- **A stale snapshot is labelled "previous analysis."** If analysis has moved on since the link was made, the link is automatically relabelled — a stale read is **never** presented as current.
- Sharing changes no assessment. Only an analysis update does.

## D111 — Threaded comments + @mentions

**Location.** **Inside the Issue Panel only** (Panel Model, D009). There is **no orphan comment surface**, no comment inbox, no standalone thread view.

**Behavior.**
- **Append-only.** No edit, no delete — by design. There is no `editComment()` and no `deleteComment()` in the code. The footer says so.
- **@ triggers autocomplete** of teammates and current participants, plus a final **"Invite someone new…"** item which closes the panel and opens the sharing dialog.
- **Reply** posts into the thread (a child comment, visually indented). Comment / Reply are the only two actions.
- Every comment appends a **History** event (`comment`, category *Collaboration*), including who was mentioned.

**Persistent line (always visible).** **"Comments never change the assessment."** They are a conversation *about* the read, recorded next to it.

## D112 — Export / share-out a snapshot

**Entry.** Top-bar **⤓ Export** (was a Slice-9 seam toast) → `openExport()`.

**Content.**
- **Analysis-currency marker** — *"This read was produced by the **{run}** analysis run, **{when}**. State: Current / Provisional / Last-good."* Read off real state (`HISTORY`/`TREND`/`ANALYSIS_STATE`), never invented.
- **Required disclaimer** — *"This reflects OSLO's **understanding maturity** … It is **not** a measure of project health, readiness, or probability of success."*
- **Formats** — **PDF** · **Copy summary** · **Export link** (renamed for D-escalation #2 — an *export link* is a frozen, hosted copy of **one exported snapshot**; it is **not** the **share link** of D110, which is revocable view-only access to the **live project**. Both surfaces now carry an explicit "an export link is not a share link" disambiguation block). **Free tier = PDF only**; the other two are **shown and tier-locked** (visibility-first, D048), each with a *Paid plan* chip and a *See plans →* path. Nothing is enforced.

**Rules.** *"Export generates no new assessment and never triggers an analysis."* An export appends an `export` History event (a record of the share-out) and moves nothing: no trend point, no issue-status change, no confidence move.

## D113 — Collaboration notifications un-gated + Settings → Collaboration

**Notifications.** The **mention · reply · shared-with-me** categories (gated in Slice 8 / D107 because nobody could mention, reply to, or share with a single invite-only user) are **now live** — sharing, comments and review requests exist. They are **on by default**, switchable, seeded in the panel, and route to source. They remain **presentation-only**: a switch changes only what the panel *shows*; routing only navigates. A reviewer's response fires a **reply** notification.

**Settings → Collaboration** (was *"Not built yet"*). Now a real section:
- **Participants** (count + *Manage sharing →*)
- **Default role for new invites** — a real, persisted picker (Collaborator / Viewer); pre-selects in the sharing dialog.
- **Snapshot links** — live/revoked count.
- **Link expiry** — an explicit **owner-TBD** state: *"Not yet set — owner decision"* (D117 / gap #339).
- **Revoking a link** → *Review your links →*
- **Review requests used** — the D118 counter with the `{N}` owner-TBD placeholder.

## D114 — CRR · CAF Review Requests (the centerpiece)

**CRR-01 — Share for review.** An action on an **Issue**, in the **Issue Panel action row** and in the **artifact annotation flyout** (the issue overlay in the editor). Sending it copy-states its limit: *"Sends the finding + its context + the recommendation + the artifact reference. It never changes the issue."* **Validation-type recommendations are prime CRR candidates (REC-05)**: on those issues the action is rendered as the **primary** button and carries *"◆ This is a validation recommendation — the kind a second pair of eyes settles fastest."* On other issues it is a quiet ghost button.

**CRR-02 — Review Package preview, before anything is sent.** A modal showing exactly what the reviewer will see:
1. **The finding** (title · severity · dimension)
2. **Its context** (why it matters + what it weakens)
3. **The recommendation** (tagged *From OSLO*)
4. **The artifact reference** (the plan artifact + the traceable evidence lines)
Then: **pick a reviewer** (a teammate chip, or any email) + an **optional note**. **Send** is disabled until a reviewer is chosen. A standing paragraph states what their answer will and will not do.

**CRR-03 — Exactly four responses.** **Comment · Approve · Reject · Suggest Alternative.** Each is a structured record `{kind, body, at, by}`, **preserved in full and shown on the issue forever**.

**CRR-04 — A response is evidence → it triggers an Extended Analysis run.** The response lands, an `Extended Analysis` run starts (reusing the existing analysis machinery — `pushHistory` / `pushTrend` / `_refreshIssueSurfaces`, the same path every other run takes), **reliability rises** (evidence availability), the confidence read may move, the **Attention map** repaints, and a **History** event is appended. The run explicitly reports what did **not** happen.

### D133 — A Reject moves CAF, via **Alignment** (RATIFIED — the last Slice 9 escalation, now closed)

A stakeholder **Reject** is **evidence about Alignment** — a first-class CAF dimension (DL-062) — not merely a comment. It therefore moves **Alignment** (and **Reliability**, as any attested evidence does) **through the same Extended Analysis run described above**. No parallel path was invented; `ALIGN_EVIDENCE` + `_reviewAnalysisRun()` are the only place alignment evidence enters.

**Symmetry (load-bearing).** An **Approve** is *also* Alignment evidence. **Neither direction is privileged** — the same `ALIGN_STEP` is applied `+` for an Approve and `−` for a Reject, from the same ledger, through the same run. A **Comment** takes no position and a **Suggest alternative** proposes a path rather than attesting agreement or disagreement — **neither moves Alignment** (they still move reliability). D133 names Approve and Reject and no others; nothing else is assumed. *(Whether "Suggest alternative" should count is **escalated**, not invented — see `open-items.md`.)*

**The D115 bounds are untouched:**
- **Evidence, not truth** — a **third-party attestation**, *"Attested by \<name\>"*. It **never** becomes OSLO's own read and **never** overwrites the assessment.
- **Never auto-resolves. Never auto-re-opens.** Nothing in the CRR module writes to `_istatus` — on any response kind.
- **OSLO never self-accepts.** The copy reads ***"\<Name\> rejected this"*** — evidence that a stakeholder **disagrees**. It is **never** *"this is now wrong / invalid / re-opened."*
- The confidence read **may fall** on a Reject (Alignment down, Reliability up). That is honest, and the trend line renders the fall **with its cause** (D097).

**Where it surfaces.** Alignment is now a **live CAF row** (Overview `#cg-align`, confidence popover `#cpp-align`), it can become the **limiting dimension**, and the response card carries a *"Folded into Alignment — as evidence (D133)"* block that states the linkage **and** what it does not mean, identically for Approve and Reject.

**CRR-05 — Review status is visible everywhere.**
- An **"◷ Awaiting review · {name}"** chip on the issue — in the **Issues list** and the **Issue Panel** lifecycle row.
- **MRI-07 "Understanding Dependencies"** — a **first-class block on Overview *and* Attention** — e.g. *"2 issues awaiting sponsor review."* It names where understanding is **blocked awaiting someone else**: *"OSLO can't firm up its read on these until someone else answers. This isn't a weakness in the plan — it's where understanding is blocked on a person."* Neutral chrome only: waiting on a person is not a severity (D003).

## D115 — Reviewer-response semantics (see the doctrinal spine above)

On the issue, a returned response renders as:
- an **"Attested by \<name\>"** chip (`.elabel.attested3` — the third epistemic variant, on the neutral `--cool` token, never a severity color);
- the response kind + the plain verb (*"Marcus Hale **approved this**"*);
- the response body in full;
- and a standing block: **"This is evidence, not a verdict."** — *"It records that a stakeholder approves — it is not a finding that the plan is sound, correct, or resolved. It went into an analysis run as evidence — that firmed up **reliability**. The assessment itself was not overwritten, the issue was not resolved, and OSLO did not accept it on your behalf. **ISS-01 is still Open.** The call is yours."*

## D116 — Reviewer (recipient) view — **SUPERSEDED BY D119 (see the amendment at the end)**

> **AMENDED 2026-07-10.** D116's *no-account-required* reviewer view is **superseded by D119**: the reviewer view is now **GATED by a token grant**. The link carries a token that **grants Reviewer Principal access (DL-049)**, scoped to exactly that review package. **The invite IS the authentication** — the reviewer is *identified and invited*, never anonymous, which satisfies D021 with **no signup wall**. The convert-moment is now the **waitlist** (D121), not a signup. The section below is retained for lineage; where it says *"no account needed"*, read **"no signup wall — your invite is your access."** The **Proposal ribbon stays**: the convert-moment (CR-7) is still owner-open.

**Entry.** *Preview reviewer view →* from the awaiting-review card on the issue (a demo route; no real auth). A full-screen surface.

**The ribbon (non-dismissible).** **"Proposal — Reviewer experience — pending owner ratification. Built to be looked at, not adopted. (D116; virality audit P0.)"** The recipient experience is owner-open, so it is not presented as settled canon — in-product or in the docs.

**The experience.**
- **No signup wall.** *"No account needed. Read it, answer it, and you're done."*
- The reviewer **lands directly in the review package** — the finding, why it matters, what it weakens, OSLO's recommendation, and where it comes from (with the evidence lines).
- They respond with **exactly one of the four CRR-03 actions**, plus an optional body.
- **Only after they respond** does the **convert-moment** appear: *"Want to see your own plan the way they see theirs?"* → *Create your own project*. **Never before value.**
- The done-state tells them plainly what their answer did (it became evidence; it firmed up reliability) and what it did **not** do (it did not close the issue; OSLO did not treat their view as the answer; *they* still decide).
- A **revoked** link opens **nothing** — not even an old copy of the read.

## D117 — Share-link hygiene

- **Revocable.** Every link (snapshot or review package) has a **Revoke** action and a revoked state. A revoked link shows a struck-through URL in the owner's view and a *"This link has been revoked"* page to the recipient.
- **Scoped.** A link is either **one snapshot** (whole project, view-only) or **one issue package** (a review request). The scope is shown on the link.
- **Expiry is an explicit owner-TBD (gap #339).** The control is present and shows *"Not yet set — owner decision"* in a dashed TBD chip, in both the sharing dialog and Settings → Collaboration. **No default is invented.**

## D118 — Bounded-cap mechanism — **REFRAMED BY D120**

> **AMENDED 2026-07-10.** `CRR_CAP` stays `null` (owner-TBD), but **what it governs has changed**: it is the **invite allocation** and it bounds **NEW-PRINCIPAL ADMISSIONS** — never review requests. **Sending a review request to an existing principal is free, forever, and is never metered (D120).** The at-cap *disable* on **Share for review** has been **removed**: evidence-seeking is never bounded. The section below is retained for lineage; read "cap" as "invite allocation on admissions".

- The **bounded-cap mechanism is built**: `_crrCapReached()` gates sending; the Review Package's Send button and the issue's *Share for review* button disable at the cap; an at-cap message points to *See plans →*.
- The **counter** reads **"X of {N} review requests used"** — with **{N} rendered as an explicit owner-TBD placeholder** (`{N} — owner-TBD`, with a tooltip naming D118). **`CRR_CAP` is `null` in code. No number is invented.**
- **Free must still be able to SEND.** With no ratified number, `_crrCapReached()` is `false` — Free sends freely. Doctrine: **virality seeds on Free** — gate collaboration *depth*, never the *seed* of the loop. A phase-bar demo trigger (*Sim CRR cap*) makes the at-cap state reachable by pinning the cap to what has already been used — **without inventing an owner value**.

## Chat (Slice-9 scoped; D108/D109 machinery reused)

New entry points, all grounded in live state via `_chatState()` (which now exposes `awaiting`, `responded`, `blockedIds`):
- **Ask OSLO about a review request / a reviewer's response** — `askOslo({type:'review', id})` sets a context pill (*"Response from Marcus Hale · ISS-01"*) and answers with what the response **did** (evidence → analysis run → reliability rose) and what it **did not do** (did not resolve; OSLO did not self-accept; the issue is still Open).
- **"What's blocking my understanding?"** — the Understanding-Dependencies lens, named per issue and per person.
- Suggested-prompt chips track the live state (an awaiting review surfaces *"What's blocking my understanding?"*; a returned response surfaces *"What did the reviewer say?"*).

**The boundary is hard-coded.** The chat **cannot** send a review request, accept a response, share, export, or resolve an issue. Asked to, `_crrActionAsk()` routes to `_ansCrrBoundary()`: *"That one isn't mine to take."* — and it hands the user back to the surface that owns the action (`openCrr()` opens the **preview**; the user still clicks Send).


---

# AMENDMENT — Controlled Release & Demand (D119 · D120 · D121 · D122)

Owner-directed 2026-07-10, per `controlled-release-demand-framework.md`. **Amends D116 / D117 / D118.** Everything below is built in `prototype.html`. Nothing below invents an owner value.

## D119 — Reviewer access is a scoped token grant (supersedes D116's open view)

**The mechanism.** A review-request link carries a **token that grants Reviewer Principal access** (DL-049 — one `Principal`, `type: reviewer | user`, promoted in place). **The invite IS the authentication.** A gated reviewer is therefore *identified and invited* — **never anonymous** — which satisfies **D021** (Alpha/Beta are invite-only, users are never anonymous) with **no signup wall** and **no damage to the CRR evidence loop**. Zero-friction and invite-only only conflict if you conflate *"no password"* with *"no identity."* (This closes the prior worker's escalation #1.)

**The surface.**
- **Landing = the grant.** `openReviewerView(rid)` in a gated phase renders a **grant screen**: an identity chip (*"Invited as Marcus Hale · marcus@northstar.vc"*), the headline *"Idris invited you to review one finding."*, the sender's note, and one button — **Open the review →** (`rvvAcceptGrant()`). One click. No form, no password, no account creation.
- **Scope block, always present.** *"This link is your access — no password, no signup. It lets you into **this one review package** and nothing else in DevNorth 2026: you won't see the rest of the plan, the other issues, or anyone else's comments. Idris can revoke it at any time."*
- **Inside the package**, an identity line replaces the old *"no account needed"*: *"Signed in by invitation as Marcus Hale · reviewer access, scoped to this package."*
- **At GA** (`_gated() === false`) the grant screen is skipped entirely and the line reads *"Open link (GA) — anonymous access is permitted at GA (D021/D024)."* The gate visibly retires.
- **The Proposal ribbon stays** — the convert-moment (**CR-7**) is still owner-open: *"Reviewer experience — pending owner ratification. Access is a scoped token grant (D119); the convert-moment is still owner-open (CR-7)."*
- A **revoked** link still opens nothing (D117 unchanged).

## D120 — Bound seats, never bound evidence (the crux rule)

| | What it is | Bounded? |
|---|---|---|
| **Admitting a new principal** | A new human enters OSLO — a collaborator seat, or a first-time reviewer | **YES.** This is supply. It is what an invite is spent on. |
| **Seeking evidence from someone already in** | A review request to an existing principal | **NO. Free, forever, never metered.** |

**Implementation.**
- `_reviewCost(email)` → `'free'` if `_isPrincipal(email)`, else `'admit'`. That one function *is* the rule.
- `ADMISSIONS[]` is the only ledger an invite draws on. `_admitted()` counts admissions — **never review requests**.
- **`Share for review` is never disabled.** The D118-era at-cap disable on the Issue-Panel button has been **removed**. The only blocked path is *admitting a new person while the allocation is spent* — and even then the request isn't silently dropped: the dialog offers the **waitlist** and records the request as an inbound demand signal.
- **The picker states the cost on the person, before you choose.** A known principal shows **"free — already in"** (`.pk-free`, neutral `--cool` token). A new person shows **"new — admits them (cost owner-TBD · CR-2)"** (`.pk-new`, dashed). Selecting either paints an explicit `.rule-box` explaining exactly what happens.
- **The counter is a fact, not a limit:** *"N review requests sent · never metered when the person is already here."*
- **DL-049 promotion.** A reviewer principal holds scoped reviewer access and **no seat**. Giving them a seat is a genuine admission (it spends an invite) and is a **promotion in place** — the same `Principal` object, `type: reviewer → user`. No second account, and everything they attested stays attributed to the same person.

## D121 — Controlled release, waitlist, phase ramp, instrumentation

**1 — Bounded, replenishing invite allocation.** `CRR_CAP` (= **{N}**, **CR-1**) is `null`. `INVITE_PERIOD` / `REPLENISH_DATE` (**CR-1**), `REVIEWER_GRANT_COST` (**CR-2**), `WAITLIST_ADMIT_RATE` (**CR-3**), `REFERRAL_WEIGHT` (**CR-4**), `REVIEW_REQ_MOVES_QUEUE` (**CR-5**), `CONVERT_MOMENT_IN_R1` (**CR-7**) are all `null`. Every one renders as an explicit **owner-TBD** chip (the existing `.tbd` token). `_allocLine()` shows **spent** (a real count) and **balance {N} per {period} — owner-TBD (CR-1)**. When the demo trigger pins the allocation, it is labelled **"simulated allocation"**.

**2 — Waitlist with a real position.** `WAITLIST[]` with `{email, name, org, role, joined, signals[]}`. Position = the person's **actual index in the list**, shown as **"#3 of 5"** — a real number, out of a real total. Demand signals are recorded and displayed: **converted referral · review-requested · role/org fit**. **The weightings are not ratified** (**CR-4 / CR-5**), so **the default order is arrival order and the UI says exactly that**. A **clearly-labelled, off-by-default preview** (`toggleWlPreview()`) shows the *recommended* ordering (review-requested > converted referral > role/org fit) and states in the same breath that it is **not ratified and not what OSLO does**.

**3 — Skip-the-line.** `admitFromWaitlist(email)` spends one invite and admits immediately — the status good. Also surfaced on the issue itself as **"Grant Marcus a seat →"** once the reviewer has asked for one.

**4 — The convert-moment is the waitlist, not a signup — and it is post-value.** It appears **only after** the reviewer responds. It states the position plainly, states what moves it, states that the weightings are owner-TBD, and says the inviter can grant them a seat from their allocation. It carries the honest reason: *"OSLO is in Alpha, and we are deliberately limiting how many people we let in — not to make you want it, but because we can only do this properly for a small number of people at a time."*

**5 — Phase ramp, wired to the existing D072 phase bar.** `setPhase('alpha' | 'beta' | 'ga')`; `_gated()` = `PHASE !== 'ga'`.

| Phase | Reviewer access | Invite allocation | Waitlist |
|---|---|---|---|
| **Alpha** | Gated — scoped token grant | Tight; {N} owner-TBD | Long; hand-curated (CR-3) |
| **Beta** | Gated — scoped token grant | Loosening | Active; faster admits |
| **GA** | **Open** — anonymous permitted (D021/D024) | **Retired** → tier-based | **Retired** |

Switching the phase **visibly changes the gating**: the grant screen disappears, the allocation block reads *"Retired at GA — limits are tier-based"*, the waitlist reads *"Retired at GA — nobody waits; there is nothing to wait for"*, the Share dialog's allocation line flips to *"GA — the gate is retired"*, and the reviewer convert-moment becomes an ordinary *Create your own project*. **The scarcity mechanism is phase-scoped and self-terminating. It is not the business model.**

**6 — Demand instrumentation** (`renderDemand()`, inside **Access & invites**). Real prototype counts where they exist; a **simulated** weekly series where they don't, marked with a `simulated data` chip. Where a metric **cannot be computed without an owner value, it shows the hole rather than a number**:
- *Invite utilization* — **not computable**: the denominator {N} is unset (CR-1). Spent admissions are shown as a real count.
- *Review-request → admit conversion* — shown as **"X of Y"**, explicitly **"a count, not a rate"** at this sample size.
- *k per loop* — **not computable in a prototype**; TEL-06 instruments it in the product.
- *Waitlist velocity* — simulated, with the honest note: *"if velocity is flat, scarcity is not the constraint — the product is — and we need to know that fast, not late."*

## D122 — Canon tension, escalated (not resolved)

Gating the seed of the loop in Alpha/Beta conflicts with applied canon **CHG-061 / Virality-audit P2** (*"guarantee the viral primitives on Free… never gate the seed"*). The recommended reconciliation — **CHG-061 is a *tier* rule** governing GA-phase freemium; **controlled release is a *phase* rule** that sunsets exactly where CHG-061 takes effect — is stated **in-product, in the Access & invites modal, as a recommendation requiring a Framework 001 proposal**. Nothing in this build treats it as ratified.

## Guardrails, as implemented

- **No fabricated scarcity.** Verified: the built prototype contains no "spots left" / "only N left" / "limited time" / "act now" string. Unset numbers render **unset**.
- **No dark patterns.** No countdowns, no pulsing, no urgency color, no loss framing. The scarcity surfaces use the neutral chrome (`--cool`, `--muted`); the severity ramp is never used.
- **The waitlist says what it is**, and why, in plain words, on the surface itself.
- **Evidence-seeking is never bounded.**
- **Reviewers are never spammed** — a review request is invited work; there is no marketing path to a reviewer anywhere in the code.

---

# AMENDMENT — D123 · D124 · D125 · D126 (the ratified register)

**This section supersedes every earlier passage it touches.**

## D126 — the governing principle (canonical statement)

> **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

## D123 — tier gating is LIVE in Alpha

Basic is **purchasable during Alpha**. The earlier N-1 recommendation ("make tier limits inert until GA") is **reversed**: it rested on the false premise that every Alpha user is on Free with no way up. Consequences carried into the build:

- `TIER` is **mutable and persisted** (`LS 'tier'`), not a constant.
- **Free = PDF-only export (D112) genuinely applies in Alpha** — and it is **not a dead end**. Every tier-locked surface routes to a real (simulated) upgrade path.
- **Slice 10 (Tiering & Limits) is an Alpha-live surface**, not a GA preview.

## D124 — TWO limits, never conflated. Always named.

| | **PHASE limit** (supply) | **TIER limit** (depth) |
|---|---|---|
| **What it meters** | How many **NEW HUMANS** you may bring into the OSLO Alpha (waitlist bypass) | How many **COLLABORATORS a PROJECT may hold** |
| **Enforced on** | `ADMISSIONS` ledger vs the invite allocation | **`Membership`** (N-2) — `_seatsUsed()` vs the seat cap |
| **Ratified value** | **Basic 5/month · Free 2/month**, replenishing, **non-cumulative** (CR-1/T-2) | Shape ratified (Basic > Free); **the number is owner-TBD (T-1)** and renders **unset** |
| **Retires at GA?** | **Yes** — phase-scoped and self-terminating | **No** — it is the business model, and it is live now |
| **Visual token** | `.limbox.lim-phase` (cool/blue) | `.limbox.lim-tier` (brand/orange) |

**The rule.** A user can have invites remaining and still hit the seat cap, or vice versa. **The product must ALWAYS name which limit blocked them.** Presenting a *phase/supply* constraint as a *tier/upsell* constraint is a **DARK PATTERN and is PROHIBITED.**

- Every blocked state in the product is produced by **one function** — `checkAdmission(email, role)` → `{ok, phase, tier, limit: 'phase'|'tier'|'both'}` — so the two can never drift apart.
- `admissionBlockHTML()` renders them as **two separately-labelled boxes**, never merged into one "you've hit your limit — upgrade" sentence.
- **The PHASE message carries NO upgrade CTA.** It says: *"You're out of invites for this month — replenishes {date}"*, states that this is a supply limit, and offers **the waitlist**. It does not sell. Selling here would be manufacturing a purchase out of a supply constraint. (The fact that Basic carries more invites is stated plainly on the **Plans** surface, where it belongs — never at the moment of blocking.)
- **The TIER message DOES offer a real upgrade path**, plus the free remedy: *"{Free} projects hold {N} collaborator seats — Basic holds more. A Viewer holds no seat — you can add them as a Viewer today, for free."*

## D125 — the register, as built

- **CR-1 / T-2** — allocation **scales with tier: Basic 5/month · Free 2/month**, replenishing, **non-cumulative** (unused invites do not roll over). **Free is deliberately non-zero** — virality must be able to seed on Free (CHG-061). A **real** replenish date is shown (1st of next month), derived from the ratified period.
- **CR-2 — reviewer grants are FREE and UNMETERED. On every tier. In every phase. This is STRUCTURALLY REQUIRED, not a preference.** It is the sole thing keeping the framework consistent with CHG-061 now that the tier rule is live in Alpha. A reviewer grant **spends no invite** and **takes no seat**. `sendReviewRequest()` has **no allocation check and no tier check** — a user with a fully-spent allocation, on Free, in Alpha, sending to a total stranger, **still sends**. Anti-abuse ceiling only (`CR2_ANTI_ABUSE_CEILING = 200` — high, non-scarcity, never surfaced as a plan feature). **A regression guard sits at the code site** (`_grantReviewerAccess()`) with a runtime assertion and a DO-NOT-REMOVE comment block. **Cost note carried in UI and docs:** each reviewer response triggers an Extended Analysis → a **DL-048 token budget** applies; that is a **cost** control on compute, **never** a monetization gate.
- **CR-3** — waitlist admits are **hand-curated in Alpha**, throttled by **owner onboarding capacity** — not a formula, not an admit-rate. Reflected in the waitlist copy and the demand view.
- **CR-4 — no points economy.** Three honest bands, **date-ordered within each**: (1) **review-requested** · (2) **referred by an active user** · (3) **cold**. **No referral-for-credit and no referral discount anywhere in Alpha.** The old "preview the recommended weighting" toggle is deleted — there is nothing left to weight.
- **CR-5** — an inbound **review request puts you in the TOP band**.
- **CR-6 — link lifetime is scoped to purpose.** **Share link: 30 days**, revocable, auto-labelled *"previous analysis"* when stale. **Review grant: expires when the issue RESOLVES, or 14 days — whichever is first** (the key was cut for one question). Swept in `_sweepGrantExpiry()` from `_refreshIssueSurfaces()`, so every resolve path retires the grant. *Configurable expiry for Basic remains **owner-open** and is **not built**.*
- **CR-7** — convert-moment = **WAITLIST ONLY**, post-response, never pre-value. **PAY-TO-SKIP IS PROHIBITED IN ALPHA — not built, and not hinted at.** Rationale: per CR-3 the queue is throttled by onboarding capacity, so **payment does not create capacity**; selling passage past it would be a toll booth on an invented constraint. The **"Proposal — pending owner ratification" ribbon stays** on the reviewer view (D116 remains an owner proposal).
- **N-1 — REVERSED.** Tier gating stays live in Alpha (see D123).
- **N-2 — ONE IDENTITY.** `Principal` (DL-049) is the single identity registry. **"Participant" is a VIEW**, derived from **`Membership`** (principal × project × role — **where the tier seat cap is enforced**) and **`ReviewGrant`** (principal × package, scoped, expiring). **A reviewer holding only a `ReviewGrant` is not a project member and consumes no seat.** Promotion is **in place** (DL-049) — a reviewer given a seat keeps the same Principal, and everything they attested stays attributed to the same human.
- **N-3** — waitlist admits land as **Viewer** by default (least privilege *and* least cost — a Viewer takes no seat), with **one-click upgrade to Collaborator**, which is where the seat cap bites.
- **T-1 — the Free ↔ Basic boundary.** **Free FULLY DELIVERS THE CORE READ** — intake → Fast Pass → Overview → Attention → Issues → **CRR**. **Basic sells depth and volume** — more projects, more Extended Analysis frequency, more artifacts, more seats, more export formats, longer history retention. **Free is never crippled on the core read** (a crippled Free tier destroys the honest product signal the Alpha exists to buy). The **shape** is ratified; the **numbers are owner-TBD** and render unset.
- **T-3** — **Alpha Basic is CHARGED** (founding-member pricing permitted). A real, simulated upgrade path ships. **The price is owner-TBD and is never invented.**
- **T-4** — **billing/payment is OUT of prototype scope**, carried to Slice 10 / engineering. Settings → Billing is an explicit, labelled **stub**.

## Roles and seats (the seat rule, precisely)

| Role | What it can do | Takes a **tier seat**? |
|---|---|---|
| **Owner** | Change the plan, share it, export it, send review requests | **Yes** |
| **Collaborator** | Comment, answer a review request; cannot change the plan | **Yes** |
| **Viewer** | Read the plan and OSLO's read of it | **No** (N-3) |
| **Reviewer** (`ReviewGrant` only — not a Membership) | See **one review package** and respond to it. Nothing else in the project. | **No** (N-2) — and the grant cost **no invite** (CR-2) |

---

# AMENDMENT — D128 · D129 · D130 · D131 (2026-07-11)

> **These two principles override any conflicting passage above.** Where earlier text sold *"more artifacts"* or
> *"longer history retention"* as Basic features, it is **superseded** — those are not tier dimensions at all.

## D128 — the two governing principles

**P1 — Meter only what costs money or defines scope. NEVER meter the epistemic record.**

- **Metered (the entire list):** **Extended Analysis runs** (cost-linked — real tokens, DL-048) · **projects** and
  **collaborator seats** (scope-linked).
- **Never metered:** **artifacts (uncapped)** · **History (never expires, never truncated)** · **Viewers
  (unlimited)** · **review requests & reviewer grants (free, CR-2)** · **link security (free, P2)**.

The append-only trace of how understanding evolved (**D096**) *is* the product's core promise. Monetising it would
sell the one thing OSLO declares inviolable. The prototype now states this **as a feature**, prominently, on the
Plans surface and in Settings → Subscription — because it is doctrinally load-bearing, not fine print.

**P2 — Never sell safety.** Link revocation and purpose-scoped expiry (CR-6) are **trust hygiene for every tier**.
**CR-6 configurable-expiry-for-Basic: NOT BUILT — CLOSED.** No tier-lock exists on any link-security control.

## D129 — the ratified register

- **X-1 — seats meter COLLABORATORS only.** **Free = 3 collaborator seats (including the owner) · Basic = 10.**
  **Viewers are UNLIMITED** on every tier — read-only access changes nothing about scope or cost, and a Viewer is
  closer to a reviewer than to a seat. **Reviewers remain free and unmetered** (CR-2). The cap is enforced on
  **Membership** (N-2), and **only for seat-holding roles** — adding a Viewer can never consume a seat and can
  never be blocked by the cap. This **replaces the previously unset/unenforced cap**; the tier-blocked state is
  now genuinely reachable (Free starts with 2 of 3 seats filled).
- **X-2 — invite refunds.** **No refund once ACCEPTED** (an invite admits a *human to OSLO*, not a membership to a
  project — refunding on removal would create an add/remove recycling exploit). **NEW: an invite that is never
  accepted and expires RETURNS to the balance** — no human was admitted, so no supply was consumed. Implemented as
  a real state machine (pending → accepted | expired) with a History event on the refund.
- **X-3 — the allocation period is the CALENDAR MONTH.** Confirmed as built; the UI says *"resets {1st of next
  month}"*. Legible, and it shares a cycle with billing now that Basic is charged (T-3).
- **T-1 — the numeric caps.** **Free:** 1 project · a **small** monthly Extended Analysis budget · **unlimited
  artifacts** · **full History**. **Basic:** 10 projects · a **generous** monthly Extended Analysis budget ·
  **unlimited artifacts** · **full History**. The Extended-Analysis **numbers** are **not** ratified and render
  **unset**; the **shape** (small vs generous) is.
- **"Sponsor" = `TEAMMATES[].role`** — confirmed as-is (cosmetic).

## D130 — the numbers are instrumented hypotheses

3 / 10 / 1 / 10 / 2 / 5 are **judgments, not derivations**, chosen to be **easy to loosen and painful to tighten**.
They are instrumented (Access → Demand shows spent vs held and real utilization) and must be revisited against
alpha behaviour. **Not settled canon.**

## D131 — Framework 001 routing

**ONE consolidated proposal: "Controlled Release & Tiering-in-Alpha"** — D122 (CHG-061 via CR-2) · D123 (tier live
in Alpha) · T-1 boundary + caps · CR-6 closure · Reject-moves-CAF (**now ratified as D133 and built** — a *product*
decision; it becomes **repository** canon only through this package). The parts are **interdependent**; splitting
them risks ratifying one while silently breaking another.

## Still owner-open (NOT built, NOT invented)

- **T-3 — the price of Basic.** Renders **unset** everywhere.
- **T-1 residual — the Extended Analysis run counts.** Renders **unset** (the shape is ratified, the number is not).
- ~~**X-2a — how long a pending invite lives before it expires.**~~ ✅ **CLOSED by D132: 14 days**, then **refunded**.
  The expiry date is real, shown as a date, and always stated alongside the refund. Not a countdown.
- ~~**Seat cap vs downgrade — does anyone get evicted?**~~ ✅ **CLOSED by D132: NO EVICTION.** Nobody is removed; you
  simply cannot **add** another Collaborator until you are back under the cap. Evicting humans from a project to
  enforce a billing change is **prohibited on a trust product**.
- ~~**"Does a Reject move CAF?"** — recommendation exists (yes, via **Alignment**, DL-062; never auto-resolving, never
  overwriting OSLO's read per D115). **Nothing ratifies it → it stays OUT of the build.**~~ ✅ **CLOSED by D133:
  YES, via Alignment — and it is BUILT.** Symmetrically for an **Approve**. All D115 bounds hold. It still routes
  through the Framework 001 package (D131) to become **repository** canon.
- **NEW — is a *Suggest alternative* also Alignment evidence?** **Escalated, not invented.** It moves reliability
  only. D133 names Approve and Reject and no others; treating an alternative as a "half-Reject" with no symmetric
  "half-Approve" would give the system a quiet **negative bias**.
- **Whether revenue expands onboarding capacity** — **pay-to-skip remains PROHIBITED and unbuilt.**
