# Slice 9 — Collaboration, Sharing & Export · Success Criteria

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. A criterion passes only if it holds in the single openable `prototype.html`. **All boxes below are verified by the automated runtime suite (27/27 passing, 0 non-environment errors).**

## D110 — Sharing dialog
- [x] The top-bar **Share** seam opens a real sharing dialog (no stub toast).
- [x] **Invite by email** works and appends the person to the participant list + a History event.
- [x] **Three participant types** — Owner · Collaborator · Viewer — each with **one plain statement** of what they can do.
- [x] The **current participants** are listed (avatar · name · email · type).
- [x] A **view-only snapshot link** can be created and **copied**.
- [x] Roles are stated as **presentation-only** ("shown, not enforced") — no permission engine is implied.
- [x] A **stale** snapshot is labelled **"previous analysis"** — a stale read is never presented as current.

## D111 — Comments + @mentions
- [x] Threaded comments exist **inside the Issue Panel only** — no orphan comment surface anywhere.
- [x] Comments are **append-only** — no edit, no delete (no such function exists).
- [x] **`@` triggers autocomplete** of teammates **plus "invite someone new…"** (which opens the sharing dialog).
- [x] The persistent line **"Comments never change the assessment."** is always visible.
- [x] Every comment appends a **History** event; the assessment and the issue's status are unchanged.

## D112 — Export
- [x] The top-bar **Export** seam opens a real export dialog.
- [x] It carries an **analysis-currency marker** (which run produced the read, when, and its state) — read off real state.
- [x] It carries the **required disclaimer** (understanding maturity — **not** project health, readiness, or probability of success).
- [x] **PDF · Copy · Link** are all shown; **Free = PDF only**, the others **tier-locked** (not hidden).
- [x] The copy states **"Export generates no new assessment and never triggers an analysis"** — and this is *true*: no trend point, no status change, no confidence move.

## D113 — Collaboration notifications + Settings
- [x] **mention · reply · shared-with-me** are **un-gated** (no "Arrives with Collaboration" label; switches enabled; items visible).
- [x] A reviewer's response fires a live **reply** notification that routes to source.
- [x] **Settings → Collaboration** is a real section — **participants · default share role · link settings** — no longer "Not built yet".
- [x] The **default share role** is a working, persisted preference.

## D114 — CRR (CAF Review Requests)
- [x] **CRR-01** — **Share for review** is an action on an Issue, in the **Issue Panel action row** *and* the artifact **annotation flyout**.
- [x] **CRR-01/REC-05** — **validation-type recommendations** surface it most prominently (primary button + "prime candidate" line); non-validation issues get the quiet variant.
- [x] **CRR-02** — a **Review Package preview** is shown before sending: **the finding + its context + the recommendation + the artifact reference**, plus a reviewer picker and an optional note.
- [x] **CRR-03** — the reviewer responds with **exactly** Comment · Approve · Reject · Suggest Alternative; the response is **structured and preserved in full**, shown on the issue.
- [x] **CRR-04** — a response lands as **evidence** → triggers an **Extended Analysis** run (**reusing the existing analysis machinery** — `pushHistory` / `pushTrend` / `_refreshIssueSurfaces`) → **confidence + the Attention map update** → a **History event** is appended.
- [x] **CRR-05** — an **"Awaiting review"** chip appears on the issue in **both** the Issues list and the Issue Panel.
- [x] **CRR-05 / MRI-07** — **Understanding Dependencies** is a first-class block on **Overview *and* Attention**, reading e.g. *"1 issue awaiting sponsor review"*, and it says where understanding is **blocked awaiting someone else**.

## D115 — Reviewer-response semantics (DOCTRINAL)
- [x] A third epistemic class — **"Attested by \<name\>"** — exists, reusing the epistemic-notation styling as a **third variant** (`.elabel.attested3`), visually and semantically distinct from **"From OSLO"** and **"Confirmed by you"**.
- [x] A response **never auto-resolves the issue** — the issue stays **Open/Addressed** (verified after an **Approve**).
- [x] **OSLO never self-accepts** — there is no autonomous-acceptance path anywhere.
- [x] An **Approve** reads as **"\<Name\> approved this"** — evidence that a stakeholder approves — and **never** as correct / resolved / verified / sound. The panel explicitly denies that reading.
- [x] **Confidence may move** (reliability / evidence availability improves) — but the **band and the assessment are not overwritten** by the stakeholder's assertion.

## D116 — Reviewer (recipient) view — **PROPOSAL**
- [x] A **"Preview reviewer view"** demo route exists (no real auth).
- [x] The reviewer lands **directly in the review package** — **no signup wall**.
- [x] They respond with one of the **four CRR-03 actions**.
- [x] The **convert-moment** ("Create your own project") appears **only after they respond** — **never before value**.
- [x] The view carries a visible **"Proposal — pending owner ratification"** ribbon; it is not presented as settled canon.

## D117 — Share-link hygiene
- [x] Links are **revocable**; a revoked link shows a revoked state and opens **nothing** (not even an old read).
- [x] Links are **scoped** — one snapshot, **or** one issue package; the scope is shown.
- [x] **Expiry** is surfaced as an explicit **"Not yet set — owner decision"** state (sharing dialog + Settings). **No expiry default is invented.**

## D118 — Free-tier CRR cap
- [x] The **bounded-cap mechanism** exists and gates sending when a cap is set.
- [x] The **counter** reads **"X of {N} review requests used"**, with **{N} rendered as an explicit owner-TBD placeholder**.
- [x] **No number is invented** — `CRR_CAP === null` in the code.
- [x] **Free can still SEND review requests** (virality seeds on Free).

## Chat (must stay integrated)
- [x] Slice-9 chat entry points exist: **ask about a review request**, **ask about a reviewer's response**, **"what's blocking my understanding?"**.
- [x] They reuse `askOslo(ctx)` + the context-pill machinery + `_chatState()` (extended with `awaiting` / `responded` / `blockedIds`).
- [x] The chat **never sends a review request, never accepts a response, never resolves an issue** — asked to, it says *"That one isn't mine to take"* and **hands the user back to the surface that owns the action** (it opens the *preview*; the user clicks Send).

## Boundaries
- [x] Advisory-only; the calls stay with the user.
- [x] Neutral chrome — collaboration state (awaiting · attested · revoked · capped) is **never** severity-colored (D003).
- [x] No real auth, no permission enforcement, no real email, no real PDF generation, no billing.
- [x] Every owner-TBD is surfaced as a TBD — **nothing is assumed** (Anti-Assumption).

## Non-regression (Slices 1–8)
- [x] Onboarding, intake, Overview, Attention map, artifact editor, Issues, History + trend, Workspace Home, project switcher, notifications, Settings, theme, ⌘K palette, OSLO chat, feature tour — all intact.

## Build integrity
- [x] Extracted `<script>` passes **`node --check`**.
- [x] **jsdom structural parse (no `runScripts`)**: `body.children.length === 27` (Slice 8 = 23, + the 4 new top-level overlays); all 33 expected element IDs present.
- [x] **jsdom runtime**: **27/27 behavior tests pass**, **0 non-environment errors**.


---

## AMENDMENT — Controlled Release & Demand (D119–D122)

### D119 — Reviewer access is a scoped token grant
- [x] In Alpha/Beta, `openReviewerView()` lands on a **grant screen**, not the package: *"Idris invited you to review one finding."*
- [x] The reviewer is **named** on the landing (identity chip) — **never anonymous**.
- [x] One click (**Open the review →**) enters the package. **No password field, no signup wall, no account creation** anywhere in the flow.
- [x] The **scope** is stated: this **one review package**, nothing else in the project. Revocable.
- [x] Inside the package: *"Signed in by invitation as \<name\> · reviewer access, scoped to this package."*
- [x] At **GA** the grant screen is **skipped** and the surface states that anonymous access is permitted (D021/D024).
- [x] The **"Proposal — pending owner ratification"** ribbon is **retained** (convert-moment = CR-7, still owner-open).

### D120 — Bound seats, never bound evidence
- [x] `_reviewCost(email)` returns **`free`** for an existing principal and **`admit`** for a new person.
- [x] Sending a review request to an **existing principal never increments `ADMISSIONS`** — verified: 0 admissions after a request to Marcus.
- [x] **`Share for review` is never disabled** — the D118-era at-cap disable is **removed**.
- [x] With the **allocation fully spent**, the Send button for an **existing principal is still enabled** — verified.
- [x] The picker shows **"free — already in"** on known principals and **"new — admits them (cost owner-TBD · CR-2)"** on a new person.
- [x] Admitting a new person via a review request **does** spend an invite, and admits them as a **Reviewer Principal scoped to that package**.
- [x] **DL-049 in-place promotion**: granting a reviewer a seat promotes the **same** `Principal` (`reviewer → user`) — verified: `PRINCIPALS.length` unchanged, no duplicate.

### D121 — Controlled release
- [x] `CRR_CAP` stays `null`; the balance renders **"{N} per {period} — owner-TBD (CR-1)"**, never a number.
- [x] Waitlist positions are **real** (#N of M against the real list length).
- [x] Demand signals (referral · **review-requested** · fit) are recorded and displayed.
- [x] Ordering is **arrival order** by default, and says so; the recommended ordering is an **off-by-default, explicitly-unratified preview**.
- [x] **Skip-the-line** works from the Access modal **and** from the issue ("Grant \<name\> a seat →").
- [x] The **convert-moment is the waitlist**, offered **only after** a response — never before value.
- [x] **Phase ramp is visible**: Alpha → Beta → GA changes the grant screen, the allocation block, the waitlist block, the Share dialog and the convert-moment. At **GA** the allocation and waitlist read **"Retired at GA"**.
- [x] **Demand instrumentation** exists, is marked **simulated** where it is simulated, and shows **holes rather than numbers** where a metric needs an unset owner value.

### D122 — Canon tension
- [x] The **CHG-061 conflict is stated in-product** (Access modal) as an **escalation requiring a Framework 001 proposal** — not as a resolved position.

### Guardrails (hard requirements)
- [x] **No fabricated scarcity** — the built file contains **no** "spots left" / "only N left" / "limited time" / "act now" string (grep-verified).
- [x] **No dark patterns** — no countdown, no pulse, no urgency color, no loss framing; access chips use the **neutral** `--cool`/`--muted` tokens, never the severity ramp (D003).
- [x] **The waitlist states plainly what it is and why.**
- [x] **Evidence-seeking is never bounded.**
- [x] **Reviewers are never spammed** — no marketing path to a reviewer exists in the code.

### Escalation #2 — share link vs export link
- [x] Both objects exist, are **named differently** (**share link** vs **export link**), and each surface carries an explicit *"a share link is not an export link"* disambiguation block.

---

# AMENDMENT — D123–D126 criteria

**Verification run 2026-07-11:** single `<script>` → `node --check` **PASS** · jsdom parse **without** `runScripts` → body child count **29** (28 + the new `#plansScrim`) · **D110–D126 all grep-verified present** · boot with `runScripts:'dangerously'` → **0 console errors** · every surface renders without throwing · **all four mandatory behavioural checks PASS**.

- [x] **D126 is printed verbatim in-product** (Access & invites; Plans): *"Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit."*
- [x] **D123 — tier gating is LIVE in Alpha.** `TIER` is mutable and persisted; Free = PDF-only genuinely applies; a real (simulated) Free→Basic upgrade path exists and is reachable from **every** tier-locked surface. **No dead ends.**
- [x] **D124 — the product ALWAYS names which limit blocked the user.** One function (`checkAdmission`) produces every blocked state; `admissionBlockHTML` renders one box per limit; **phase and tier are never merged into a single sentence.**
- [x] **D124 — the PHASE block carries NO upgrade CTA.** Verified by assertion: the phase message matches */out of invites for this month/* and *does not* match */Compare Free and Basic/* or `.lim-tier`.
- [x] **D124 — the TIER block names seats, offers the free Viewer remedy, and offers a real upgrade.** Verified by assertion; it *does not* match */out of invites/*.
- [x] **CR-2 — a review request sends with the allocation fully spent, on Free, in Alpha, to a total stranger.** No invite spent. No seat taken. **Asserted.**
- [x] **CR-2 — a regression guard exists at the code site** (`_grantReviewerAccess()`): runtime assertion + DO-NOT-REMOVE comment block explaining why it is load-bearing (CHG-061 / D120 / D126).
- [x] **CR-2 — the DL-048 token budget is described in-product as a COST control, never a monetization gate.**
- [x] **CR-1/T-2 — Basic 5/month · Free 2/month**, replenishing, **non-cumulative**, with a **real** replenish date. Free is **non-zero**.
- [x] **CR-3 — the waitlist says admits are hand-curated, throttled by onboarding capacity.** No admit-rate is invented.
- [x] **CR-4 — no points economy anywhere.** Three named bands, date-ordered within each. **No referral-for-credit or discount in the DOM.** The old weighting-preview toggle is deleted.
- [x] **CR-5 — an inbound review request puts you in the top band.** Asserted (`_waitPos() === 1`).
- [x] **CR-6 — share link 30 days; review grant expires on resolve or at 14 days, whichever first.** The on-resolve sweep is asserted. Configurable-expiry-for-Basic renders **owner-open, not built**.
- [x] **CR-7 — convert-moment is the waitlist only, post-response. PAY-TO-SKIP IS NOT BUILT AND IS NOT HINTED AT.** Grep-verified: no "skip the line for £/$", no purchase affordance anywhere on the waitlist or reviewer surfaces. The **Proposal ribbon remains** on the reviewer view (D116).
- [x] **N-2 — one identity.** `PARTICIPANTS[]` is gone. `Principal` + `Membership` + `ReviewGrant`. **A reviewer holding only a ReviewGrant is not a member and consumes no seat** — asserted.
- [x] **N-3 — waitlist admits land as Viewer**, with one-click promotion to Collaborator — asserted.
- [x] **T-1 — Free fully delivers the core read** (intake → Fast Pass → Overview → Attention → Issues → CRR), and the Plans surface says so with ticks. **Basic sells depth and volume.** Free is never crippled on the core read.
- [x] **T-3 — the price renders UNSET** (owner-TBD chip). No number is invented anywhere.
- [x] **T-4 — billing is a labelled stub.** No card field, no invoice, no charge.
- [x] **Owner-TBD values render UNSET, never as fake values and never as fabricated scarcity** — the seat cap, the Basic caps, the price, and configurable expiry all use the `.tbd` token.
- [x] **Non-regression:** Slices 1–8 (onboarding, intake, Overview, Attention, Artifacts + editor, Issues, History, Workspace/Settings, chat) and all pre-existing Slice-9 surfaces still work.

---

# AMENDMENT — D128–D131 success criteria

## D128 P1 — the epistemic record is NEVER metered (**hard, structural**)

- [x] `ARTIFACTS_METERED === false` · `ARTIFACT_CAP = {free: ∞, basic: ∞}` — **no artifact-count check exists
      anywhere in the file.**
- [x] `HISTORY_METERED === false` · `HISTORY_RETENTION = {free:'full', basic:'full'}` — **`pushHistory()` contains no
      cap, no trim, no expiry and no tier check**, and carries a comment saying why.
- [x] **Switching tier does not change `HISTORY.length`.** Verified.
- [x] `BASIC_ARTIFACT_CAP` and `BASIC_RETENTION` are **deleted from the source.** The old *"more artifacts / longer
      retention"* selling copy is **gone** from Plans, Settings and the upgrade prompt.
- [x] The **Plans surface visibly states** that artifacts and History are **unlimited on every tier** — as a
      feature, above the plan columns, in both columns, and in the "never sell you" panel.

## D128 P2 — safety is never sold (**hard, structural**)

- [x] `revokeLink()` contains **no `TIER` reference.** `LINK_SECURITY_TIER_LOCKED === false`.
- [x] Link revocation + purpose-scoped expiry work **identically on Free** (verified end-to-end on Free).
- [x] `CONFIGURABLE_EXPIRY_BASIC === false` — **CLOSED, not built.** Rendered as *"Closed — not built (D128)"*, never
      as an upsell and never as "owner-open".

## D129 X-1 — seats meter collaborators only

- [x] `SEAT_CAP = {free: 3, basic: 10}` — **enforced**, and the tier-blocked state is **genuinely reachable**.
- [x] A 4th **Collaborator** on a full Free project is **blocked**, and the message **names the TIER limit** and
      **never says "out of invites"**.
- [x] A **Viewer** on the same project **still succeeds** — no seat consumed, never blocked by the cap.
      `VIEWER_CAP = {∞, ∞}`; `_assertViewersUnlimited()` is a runtime guard.
- [x] Reviewers remain free and unmetered (**CR-2 regression guard intact**).

## D129 X-2 — invite refunds

- [x] **Accepted → never refunded** (including on removal from the project).
- [x] **Pending → expired → REFUNDED**, with a History event, and the seat released.

## D132 X-2a — pending-invite expiry = **14 days** (RATIFIED)

- [x] `INVITE_EXPIRY_DAYS = 14`. **The owner-TBD placeholder is removed** — nothing renders "unset" for X-2a.
- [x] Every pending invite carries a **real `expiresAt`**, stamped **once at send**.
- [x] The date is surfaced **honestly and everywhere** the invite appears — pending row, pending-invites box,
      Settings → Collaboration, History, notification, toast: *"Expires {date} — the invite returns to your balance
      if unused."*
- [x] **The date and the refund are never separated.** A date on its own would read as manufactured scarcity.
- [x] **No countdown, no urgency colour, no "expires soon" nudge.** It is a fact, not a lever.
- [x] Expiry → **refund**, with a History event that names the 14-day window and the before/after balance.
- [x] An **accepted** invite is still **never** refunded — `expireInvite()` on it is a no-op.

## D132 — seat cap vs downgrade: **NO EVICTION** (RATIFIED)

- [x] `EVICT_ON_DOWNGRADE = false`. Basic (10 collaborators) → Free (cap 3): **nobody is removed.**
- [x] **No code path removes a Membership on a tier change.** `setTier()` touches `MEMBERSHIPS` **zero times**.
- [x] **Runtime guard** `_assertNoEvictionOnDowngrade()` fails loudly and **restores the roster** if that ever
      changes (verified: a deliberate eviction is caught and reversed).
- [x] The over-cap state is **explicit and legible** wherever seats are shown, and **leads with the reassurance**:
      *"This project has 10 collaborators; Free adds up to 3. No one has been removed — you can't add more until
      you're under 3, or upgrade."*
- [x] Adding an **11th Collaborator is blocked by the TIER limit**, named in those words, with the invite allocation
      explicitly cleared of blame — and the block message **never implies an eviction**.
- [x] **Viewers stay unlimited** over the cap (X-1); **review requests stay free** (CR-2).
- [x] The **Plans modal states the downgrade contract up-front**, where a downgrade is actually initiated.
- [x] Code comment records the principle: **evicting humans from a project to enforce a billing change is
      prohibited on a trust product.**

## D129 X-3 / T-1

- [x] Allocation period = **calendar month**; UI says *"resets {1st of next month}"*.
- [x] Free = **1 project**; Basic = **10**. Both enforced.
- [x] Extended Analysis: the **shape** renders (small / generous); the **run count renders UNSET** (owner-TBD).

## D130 / D131

- [x] The Demand panel carries a standing note that **3 / 10 / 1 are hypotheses, not canon** (D130).
- [x] The Access modal names the **ONE consolidated Framework 001 proposal** — *"Controlled Release &
      Tiering-in-Alpha"* — and now states that **Reject-moves-CAF is RATIFIED (D133) and built** (still routing
      through the package to become **repository** canon).

## D133 — a Reject moves CAF, via Alignment

- [x] A **Reject** enters as **evidence** and triggers an **Extended Analysis run** through the **existing**
      machinery (`pushHistory` / `pushTrend` / `_refreshIssueSurfaces`) — **no parallel path**.
- [x] It moves **Alignment** (down) **and Reliability** (up). The confidence read **may fall** — and the trend
      line renders the fall **with its cause** (D097).
- [x] **Symmetry** — an **Approve** is *also* Alignment evidence, moving it **up** by the **same** `ALIGN_STEP`.
      Neither direction is privileged; both are attested inputs to the same run.
- [x] It is recorded as a **third-party attestation** — *"Attested by \<name\>"* — **never** as OSLO's read, and
      it **never overwrites** the assessment.
- [x] It **never auto-resolves** and **never auto-re-opens** an issue: **nothing in the CRR module writes
      `_istatus`** (verified behaviourally, both directions).
- [x] **OSLO never self-accepts** — the copy reads *"\<Name\> rejected this"*. Every occurrence of
      "wrong" / "invalid" / "re-opened" in the response card is an explicit **negation**.
- [x] The **Alignment linkage is legible**: the card explains that a stakeholder disagreeing is information about
      **alignment**, that OSLO folded it in **as evidence** — and what that does **not** mean.
- [x] **Comment** and **Suggest alternative** move **reliability only** — D133 names Approve and Reject and no
      others. The "does an alternative count?" question is **escalated, not invented**.

## Guardrails (unchanged, still hard)

- [x] No fabricated scarcity · no dark patterns · unset numbers render **unset**.
- [x] **Evidence-seeking is never bounded** (CR-2 guard).
- [x] **A phase limit is never presented as a tier upsell** (D124) — the phase message carries **no upgrade CTA**.
- [x] **Pay-to-skip: prohibited and unbuilt.** **Basic price: unset.** **Reject-moves-CAF: RATIFIED (D133) and
      built — and still bounded by D115** (evidence not truth · never auto-resolves · never auto-re-opens · OSLO
      never self-accepts · symmetric with Approve).
- [x] Reviewers are never spammed.

## Build integrity

- [x] `node --check` on the extracted `<script>` — **PASS**.
- [x] jsdom parse without `runScripts` — **29 body children** (unchanged).
- [x] Boot with `runScripts: 'dangerously'` — **zero runtime errors.**
- [x] **43/43 behavioural assertions pass.**
- [x] Non-regression: all Slice 1–8 surfaces + all existing Slice 9 surfaces open and render.
