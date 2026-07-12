# Slice 9 — Collaboration, Sharing & Export · Workflow

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. The Slice-9 flows layer onto the existing shell without disturbing the Slices 1–8 funnel.

## Flow A — Share the project (D110)
1. Top bar → **⤴ Share** → `openShare()`.
2. Read the three **participant types** and their one-line statements (Owner · Collaborator · Viewer) + the *roles are shown, not enforced* note.
3. Type an email, pick **Collaborator / Viewer**, hit **Invite** → `sendInvite()` → the participant list grows; a **History** event lands. (No email is actually sent.)
4. **Create a view-only link** → `createSnapshotLink()` → a project-scoped, revocable link + its **Copy link** / **Preview what they see** / **Revoke** actions, and the **Expiry · Not yet set — owner decision** row.
5. If analysis moves on, the link is relabelled **"Shows a previous analysis"** automatically.
6. **Revoke** → `revokeLink()` → the URL is struck through; recipients get a *revoked* page. Escape / **Done** closes.

## Flow B — Export a snapshot (D112)
1. Top bar → **⤓ Export** → `openExport()`.
2. Read **What you're exporting**: the confidence read + the **analysis-currency marker** (which run produced it, when, and whether it is Current / Provisional / Last-good).
3. Read the **required disclaimer** (understanding maturity — *not* health, readiness, or probability of success).
4. Pick a format: **PDF** (Free) · **Copy summary** / **Link** (shown, tier-locked, with *See plans →*).
5. `doExport('pdf')` → an `export` History event + a confirming toast. **No trend point, no status change, no confidence move** — export never triggers an analysis.

## Flow C — Comment on an issue (D111)
1. Open any issue (Issues list, Attention cell, Start here, or an artifact annotation) → the **Issue Panel**.
2. Scroll to **Comments** — read the standing line *"Comments never change the assessment."*
3. Type in the box; type **`@`** → the autocomplete opens (teammates + participants + **"Invite someone new…"**).
4. Pick a name → it is inserted as an `@mention` (or pick *Invite someone new…* → the sharing dialog).
5. **Comment** (or **Reply** to thread it) → `addComment()` → the comment appends to the thread **and** to History. It cannot be edited or deleted.

## Flow D — Send a review request (D114 · CRR-01/CRR-02)
1. Open an issue → the **Issue Panel** action row → **⤴ Share for review** → `openCrr(id)`.
   (Also reachable from the artifact's annotation flyout: *Share for review →*.)
   On a **validation** issue (e.g. ISS-01, ISS-03) the action is the **primary** button and carries the REC-05 *prime candidate* line.
2. The **Review Package** preview shows exactly what they will see: **the finding** → **its context** → **the recommendation** (*From OSLO*) → **the artifact reference** (+ traceable evidence lines).
3. Pick a **reviewer** (teammate chip, or type any email). **Send** stays disabled until one is chosen.
4. Add an optional **note**.
5. Read the standing paragraph — *what their answer will and will not do* — and the **"X of {N} review requests used"** counter (with `{N}` as an owner-TBD).
6. **Send review request** → `sendReviewRequest()`:
   - a `review_request` History event;
   - a **scoped, revocable** review link (`kind:'issue'`);
   - an **"◷ Awaiting review"** chip on the issue (Issues list + Issue Panel);
   - the **Understanding dependencies** block appears on Overview *and* Attention.
   - **The issue's status does not move.** A request is not an action on the plan.

## Flow E — The reviewer responds (D114 · CRR-03/CRR-04 · D115 · D116)
1. From the awaiting-review card: **Preview reviewer view →** → `openReviewerView(rid)`.
2. The reviewer surface opens with a **"Proposal — pending owner ratification"** ribbon (D116).
3. They land **directly in the package** — no account, no signup wall — and read the finding in context.
4. They pick **exactly one** of **Comment · Approve · Reject · Suggest Alternative**, add an optional body, and **Send my response** → `rvvSend()` → `applyReviewResponse()`.
   - **D133:** if it is an **Approve** or a **Reject**, it is also recorded in `ALIGN_EVIDENCE[]` as **evidence about Alignment** (a CAF dimension, DL-062) and moves **Alignment** in the run that follows — **up** for an Approve, **down** for a Reject, by the **same** `ALIGN_STEP`. **Neither direction is privileged.** It still resolves nothing, re-opens nothing, and never becomes OSLO's own read.
5. **Only now** does the **convert-moment** appear: *"Want to see your own plan the way they see theirs?"* → *Create your own project*.
6. Meanwhile, back in the workspace:
   - the response is recorded as **"Attested by \<name\>"** (the third epistemic class);
   - a `review_response` History event lands;
   - a **reply** notification fires (D113);
   - **CRR-04:** `_reviewAnalysisRun()` starts an **Extended Analysis** run through the existing machinery — after ~2.4s it appends a **trend point** + a `reanalysis_run` History event, **reliability rises** (evidence availability), the confidence read may move, and the Attention map repaints.
7. **What does not happen (D115):** the issue is **not** resolved, the assessment is **not** overwritten, and OSLO does **not** self-accept. The issue panel and the chat both say so explicitly.
8. A **revoked** link (Flow A step 6) opens **nothing** — the reviewer sees a *revoked* page, never a stale read.

## Flow F — "What's blocking my understanding?" (CRR-05 / MRI-07)
1. **Overview** or **Attention map** → the **Understanding dependencies** block: *"1 issue awaiting sponsor review."*
2. Click a row → the blocked issue opens.
3. Or ask OSLO — the chat chip **"What's blocking my understanding?"** → `_ansBlocking()` names the issue, the person, and what will happen when they answer.

## Flow G — Chat about a review (and be refused an action)
1. On a returned response: **Ask OSLO about this response** → `askOslo({type:'review', id})` → a context pill (*"Response from Marcus Hale · ISS-01"*).
2. OSLO explains **what it did** (evidence → analysis run → reliability rose) and **what it did not do** (did not resolve; did not self-accept; the issue is still Open).
3. Ask it to *send*, *accept* or *resolve* → `_crrActionAsk()` → `_ansCrrBoundary()`: **"That one isn't mine to take."** It offers **Open the review package →** (the *preview*, not the send) and hands you back to the owning surface.

## Flow H — Settings → Collaboration (D113)
1. Account menu → **Settings** → **Collaboration** (no longer tagged *later*).
2. See **Participants**, set the **Default role for new invites** (persisted), see **Snapshot links** (live/revoked), see **Link expiry · Not yet set — owner decision**, and the **Review requests used** counter.
3. **Manage sharing →** / **Review your links →** route to the sharing dialog.
4. **Notifications** → the **Mentions · Replies · Shared with me** switches are live (no *"Arrives with Collaboration"* label).

## Demo triggers (phase bar)
- **Sim reviewer response** → `simReviewerResponse()` — the first awaiting reviewer answers (cycling Approve → Comment → Reject → Suggest Alternative), landing as evidence and triggering the run.
- **Sim CRR cap** → `simCrrCap()` — pins the cap to what you have already used so the at-cap state is reachable **without inventing an owner number**. Toggling it off restores the honest `{N}` owner-TBD state.

## Preserved flows (Slices 1–8)
Invite → activation → intake → Initial Analysis → orientation; Overview ↔ Attention ↔ Issues ↔ History; artifact editing; Workspace Home; project switcher; notifications; Settings + theme; command palette (⌘/Ctrl+K); OSLO chat; feature tour. Unchanged.


---

## AMENDMENT — Controlled Release & Demand flows (D119–D122)

### Flow D (amended) — sending a review request now states its cost (D120)
Step 3 of Flow D is replaced. The reviewer picker now shows, **on each person, before you choose**:
- **Marcus Hale · Sponsor** → **"free — already in"** — he is a principal; asking him costs nothing, forever, and is never metered.
- **Dana Whitlock · Venue contact** → **"new — admits them (cost owner-TBD · CR-2)"** — she is not on OSLO; sending admits her as a **Reviewer Principal scoped to this package**, and that draws on your invite allocation.

Selecting either paints an explicit rule box. **Send** reads *"Send to Marcus Hale"* (free) or *"Admit Dana & send"* (an admission).
- `sendReviewRequest()` → if the person is new: `admitPrincipal(email, name, 'reviewer', 'review request', issueId)` **then** the request. If they are already a principal: **nothing is metered.**
- **Share for review is never disabled.** The only blocked path is *new person + allocation spent* → the dialog offers **"Add Dana to the waitlist →"** (`crrWaitlist()`), which records the review request as an **inbound demand signal**. No request is sent, and nothing is faked.

### Flow E (amended) — the reviewer is GRANTED access, not let in anonymously (D119)
1. **Preview reviewer view →** → `openReviewerView(rid)`.
2. **NEW — the grant landing.** In Alpha/Beta the reviewer first sees: an identity chip (*"Invited as Marcus Hale · marcus@northstar.vc"*), **"Idris invited you to review one finding."**, the note, one button — **Open the review →** (`rvvAcceptGrant()`), and the **scope block** (*"this one review package and nothing else in DevNorth 2026"*). No password. No form. The invite **is** the authentication.
   - At **GA** this step is skipped: the link is open, and the surface says so (anonymous permitted, D021/D024).
3. Inside the package the identity line reads *"Signed in by invitation as Marcus Hale · reviewer access, scoped to this package."*
4. They pick one of the four responses and **Send my response** → `rvvSend()` → `applyReviewResponse()` (unchanged: evidence, not truth; Extended Analysis; the issue does not move).
5. **NEW — the convert-moment is the waitlist** (`_rvvConvertHTML()`), and only now:
   - *"Want OSLO on your own plan? … OSLO is in Alpha, and we are deliberately limiting how many people we let in."*
   - **Join the waitlist** → `rvvJoinWaitlist()` → they get a **real position** (*"Position 5 of 5"*), their **review-requested** demand signal is recorded, and the inviter gets an **access** notification.
   - At **GA**: no waitlist. The offer is an ordinary **Create your own project**.

### Flow I (new) — grant a seat from your allocation (skip-the-line, D121)
1. On the issue's returned-response card: **"Grant Marcus a seat →"** (appears only once he has asked).
2. `admitFromWaitlist(email)` → spends one invite → **DL-049 in-place promotion**: the same `Principal`, `reviewer → user`, with a collaborator seat. **No duplicate account.** Everything he attested stays attributed to him.
3. If the allocation is spent: an honest toast — *"you can't admit anyone right now"* — and **no upsell**.

### Flow J (new) — Access & invites (D121)
1. Settings → **Access & invites** → **Access, waitlist & demand →** → `openAccess()` (also reachable from the Share dialog, and from an **access** notification).
2. **Your invite allocation** — spent (real) · balance **{N} per {period} — owner-TBD (CR-1)** · replenish **{period} — owner-TBD** · reviewer-grant cost **owner-TBD (CR-2)** · the D120 rule box.
3. **Waitlist** — plain statement of what it is and why; real positions (#N of M); recorded demand signals; **Admit now** (skip-the-line) per row; the weightings stated as **owner-TBD (CR-4/CR-5)**; an off-by-default **Preview recommended order** toggle labelled *not ratified*.
4. **Demand** — `simulated data` chip; waitlist size (real) · joins/week (simulated sparkline) · admissions spent (real) · review requests (real, *"never metered"*); and the three **honest holes** (utilization not computable without {N}; conversion is a count, not a rate; k per loop not computable in a prototype).
5. **The ramp — and where it ends** — Alpha → Beta → **GA (open, waitlist retired, tier-based limits)** + the **D122 canon-tension** note.

### Flow K (new) — watch the mechanism sunset (D121)
1. Phase bar → **Beta** → the gate loosens (copy changes; the grant, the allocation and the waitlist all persist).
2. Phase bar → **GA** → the grant screen disappears; the allocation and waitlist read **"Retired at GA"**; the Share dialog says the gate is retired; the reviewer's convert-moment becomes *Create your own project*.
3. Phase bar → **Alpha** → it all comes back. **The scarcity mechanism is phase-scoped and self-terminating.**

### Demo triggers (amended)
- **Sim allocation spent** (was *Sim CRR cap*) → `simCrrCap()` — pins the **invite allocation** to the number of admissions already made, so the allocation-spent state is reachable **without inventing {N}**. With it on: **review requests to existing principals still send freely** — that is the D120 test.

---

# AMENDMENT — D123–D126: the flows that changed

## Flow A — invite someone (D124: two meters, checked separately)

1. Share → type an email → pick a role.
2. `checkAdmission(email, role)` evaluates **two independent meters**:
   - **PHASE** — is this a *new human* and is the monthly allocation spent? (`_gated() && newHuman && _allocSpent()`)
   - **TIER** — does this role *take a seat*, and are the project's collaborator seats full? (`_roleTakesSeat(role) && _seatsUsed() >= _seatCap()`)
3. **Blocked → the product names the limit.** Phase → *"You're out of invites for this month — replenishes {date}"* + **waitlist** (no upsell). Tier → *"Free projects hold {N} collaborators — Basic holds more"* + **add as Viewer (free)** + a real upgrade path. Both → **two boxes**.
4. **Not blocked →** a *new* human is admitted (spends **one** invite); an *existing* principal is not (spends nothing). If the role is Collaborator/Owner, a **tier seat** is taken; if Viewer, **none**.

## Flow B — ask for evidence (CR-2: nothing blocks this)

1. Issue Panel → **Share for review** → pick anyone, including a total stranger.
2. `sendReviewRequest()` runs with **no allocation check and no tier check**.
3. If they are new: `_grantReviewerAccess()` creates a **Principal + scoped ReviewGrant**. **No Membership. No seat. No invite.** The runtime guard asserts the invite ledger did not move.
4. A **grant link** is minted with CR-6 lifetime: **expires when the issue resolves, or in 14 days — whichever is first**.
5. The reviewer responds → the response lands as **evidence** (D115, unchanged) → **Extended Analysis** runs → reliability may move; the issue **does not**.
6. When the issue **resolves**, `_sweepGrantExpiry()` retires the grant. The attestation stays on the record forever; the key does not.

## Flow C — the convert-moment (CR-7: waitlist only, post-response)

Reviewer responds → *then* (never before) they are offered **the waitlist**, with a real position and their real band. **Band 1, because they were review-requested (CR-5).** There is **nothing to buy on that screen**: pay-to-skip is prohibited and is not built. The inviter is notified and can spend an invite to admit them — as a **Viewer** (N-3).

## Flow D — upgrade (D123 / T-3 / T-4)

Any tier-locked surface (export formats, seat cap, project cap) → **Plans** → *Upgrade to Basic (simulated)* → `setTier('basic')` → allocation becomes **5/month**, export formats unlock, the seat cap moves. **The price is blank (owner-TBD, T-3). Billing does not exist (T-4).** A History event records the change and states exactly what did **not** change: **evidence-seeking**.

## Flow E — flip the phase to GA (the sunset, and what survives it)

Top bar → **GA**:
- **Retired:** the gate, the invite allocation, the waitlist, the token-grant landing (anonymous access permitted — D021/D024).
- **Still in force:** **every tier limit.** Free is still PDF-only; the seat cap still binds. That was never a phase mechanism — it is the business model, and D123 made it live in Alpha.

---

# AMENDMENT — D128–D131: the flows that changed

## Flow A′ — invite a NEW human (X-2: the invite now has a lifecycle)

1. Share → type an email → pick a role → **Invite**.
2. `checkAdmission()` runs the **two meters separately** (D124): **phase** (a new human → an invite) and **tier**
   (a seat-holding role → a seat). A **Viewer** can only ever trip the *phase* check — **never** the seat cap (X-1).
3. If clear and the person is **new to OSLO** → `inviteNewHuman()`:
   - the invite is **`pending`**, and it **HOLDS** one allocation unit (it is **not yet spent**);
   - a **pending Membership** is created (so a Collaborator invite also **reserves** its seat);
   - the invite is stamped with a **real expiry date** — `now + 14 days` (**X-2a, ratified — D132**);
   - History: *"Invite sent to X — pending, expires {date}. One invite is now HELD… Expires {date} — the invite
     returns to your balance if unused (X-2)."* The date and the refund are **always stated together**, and there
     is **no countdown and no nudge** — you are made whole automatically.
4. **They accept** → `acceptInvite()` → the invite is **SPENT FOR GOOD**. `ADMISSIONS[]` gains an entry. **No refund,
   ever** — not on removal, not on a role change.
5. **It expires unaccepted** → `expireInvite()` → **REFUNDED**. The pending Membership is removed (releasing any
   seat), the balance goes **up**, and History records the before/after.

*(Both outcomes are reachable in one click from the participant row: **Simulate: they accept** / **Simulate: it
expires**.)*

## Flow B′ — hit the TIER seat cap on Free (now genuinely reachable)

1. Free starts with **2 of 3** seats filled (you + Sam; Priya is a Viewer, and holds no seat).
2. **Make Priya a Collaborator** → **3 of 3**. *(Or: phase bar → **Sim seat cap reached**, which seats demo
   colleagues who are **already principals**, so **no invite is spent** — the two meters stay separate.)*
3. Invite a 4th as **Collaborator** → **BLOCKED by the TIER limit**, named in those words, with the invite
   allocation explicitly cleared of blame.
4. **Change the role to Viewer and invite again → it SUCCEEDS.** No seat consumed. **Viewers are unlimited** (X-1).
5. **Send them a review request → it SENDS.** Free, unmetered, on any tier, in any phase (CR-2).

## Flow C′ — what a tier change does, and what it can never touch (D128)

`setTier()` moves: **projects** (1 ↔ 10) · **collaborator seats** (3 ↔ 10) · the **Extended Analysis budget** (small
↔ generous — the *number* stays unset) · **export formats** · the **phase allocation** (2 ↔ 5/month).

`setTier()` **cannot** move — and History says so explicitly on every change:

- **your artifacts** (uncapped on both),
- **your History** (full on both — nothing is trimmed, expired or *unlocked*),
- **your link security** (revocation + purpose-scoped expiry, identical on both — **safety is never sold**),
- **unlimited Viewers**,
- **evidence-seeking** (review requests and reviewer grants — free and unmetered on every tier).

- **your collaborators.** ✅ **NO EVICTION — RATIFIED (D132).**

## Flow C″ — downgrade with more collaborators than the new cap (D132: NOBODY IS REMOVED)

1. On **Basic**, fill all **10** collaborator seats (phase bar → *Sim seat cap reached*).
2. **Plans → back to Free** (cap **3**). **Nobody is removed.** All 10 stay, with everything they contributed still
   attributed to them in History. `setTier()` touches `MEMBERSHIPS` **zero times**.
3. The project is now **over the cap**, and it says so, plainly, wherever seats are shown — leading with the
   reassurance, because that is the reader's actual question: *"This project has 10 collaborators; Free adds up to
   3. **No one has been removed** — you can't add more until you're under 3, or upgrade."*
4. **Adding an 11th Collaborator is BLOCKED — by the TIER limit**, named in those words, with the invite allocation
   explicitly cleared of blame. **Viewers are still unlimited** (X-1) and **review requests are still free** (CR-2).
5. Removing someone is **always the owner's deliberate act**, never a side-effect of a plan change.

> **Evicting humans from a project to enforce a billing change is prohibited on a trust product.** The seat cap gates
> **ADMISSION**, never **EVICTION**. Enforced by `EVICT_ON_DOWNGRADE = false` and the runtime guard
> `_assertNoEvictionOnDowngrade()`, which fails loudly and restores the roster if any tier change ever removes a
> Membership. The **Plans modal states the downgrade contract up-front** — on the page where a downgrade is actually
> initiated — so a user on Basic never has to wonder what will happen to their people.

## Demo triggers (updated)

| Trigger | What it now does |
|---|---|
| **Sim allocation spent** | Fills this month's **ratified** allocation (Free 2 · Basic 5) so the **PHASE**-blocked state is reachable. Pending invites already count as held. **Never touches review requests.** |
| **Sim seat cap reached** | The cap is **ratified and real** (3 / 10), so this no longer pins a fiction — it **seats demo colleagues who are already principals in OSLO**, so **no invite is spent**. Never adds or blocks a Viewer. |
| **Participant row → Simulate: they accept / it expires** | 🆕 X-2 — the two invite outcomes: **spent for good** vs **refunded**. |
