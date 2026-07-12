# Slice 9 — Collaboration, Sharing & Export · Edge Cases

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. Each row states the case, the prototype's behavior, and the doctrine that decides it.

## Sharing (D110 / D117)

| Case | Behavior | Why |
|---|---|---|
| Invite an email that is already a participant | Their **type is updated**, no duplicate row | Idempotent; the participant list is a set keyed by email |
| Invite a malformed email | **Invite** stays disabled | No silent failure, no fake success |
| Invite yourself (the Owner) | Handled as an update; the Owner row cannot be removed (`you:true`) | There is always exactly one Owner |
| Remove a participant who left comments / gave a response | They are removed from the list; **their comments and responses remain** | The record is **append-only** (D096). Removing a person does not rewrite history |
| Remove a participant with a **pending** review request | The request and its link stay **live** | Auto-revoking is **not specified** — see `open-items.md` §5. The owner can revoke explicitly |
| A snapshot link exists and analysis then moves on | The link is **automatically relabelled "previous analysis"** | **Never present a stale read as current** (D110) |
| A recipient opens a **revoked** link | They see *"This link has been revoked"* — **nothing else**, not even an old copy of the read | Revocation must be a real boundary, not a soft one (D117) |
| Link expiry | The control renders **"Not yet set — owner decision"** | **No default is invented** (D117 / gap #339) |
| Multiple snapshot links | All are listed, each with its own scope, staleness state and Revoke | Links are **scoped**, and scope is per-link |

## Comments (D111)

| Case | Behavior | Why |
|---|---|---|
| Post an empty comment | The box border flags red; nothing is posted | No empty append |
| Try to edit or delete a posted comment | **There is no affordance and no function** (`editComment` / `deleteComment` do not exist) | **Append-only** by construction, not by convention (D111) |
| `@` a person who is not a participant | The autocomplete still offers them (they're a known teammate); the mention renders | Mentioning is not granting access — roles are presentation-only anyway |
| `@` someone entirely new | The final autocomplete item — **"Invite someone new…"** — closes the panel and opens the **sharing dialog** | The action is handed to the surface that owns it |
| Comment on a **Resolved** issue | Allowed; the thread is still there | A resolved issue can still be discussed. Comments never move the read either way |
| A comment that looks like a decision ("approved!") | Renders as a comment. It changes nothing | **"Comments never change the assessment."** Only an analysis update moves the read (D006) |

## Export (D112)

| Case | Behavior | Why |
|---|---|---|
| Export while the read is **Provisional** (Extended Analysis still running) | Allowed; the currency marker says **"Provisional (Extended Analysis is still deepening it)"** | The recipient must know *what they are holding* |
| Export after an analysis run **failed** | Allowed; the marker says **"Last-good (the most recent run did not complete)"** | Last-good is preserved and **named** (D041) |
| Export a **Copy** or **Link** on Free | The option is **visible and disabled**, with a *Paid plan* chip and *See plans →* | **Visibility-first** — show the boundary, don't hide the capability (D048) |
| Export twice | Two `export` History events; **nothing else moves** | An export is a **read**, not an analysis |
| Does an export ever trigger an analysis? | **Never.** No trend point, no status change, no confidence move | Stated in the copy **and** true in the data model (D112) |

## CRR (D114 / D115 / D118)

| Case | Behavior | Why |
|---|---|---|
| Send a review request with **no reviewer** chosen | **Send is disabled** | A package with no recipient is not a request |
| Send **two** requests on the same issue | Both are listed; the chip names **both** reviewers; MRI-07 counts the **issue once** | The dependency is on the *issue*, the attestations are per *person* |
| Reviewer **approves** | Recorded as **"Marcus Hale approved this"** + *"Attested by Marcus Hale"*. **The issue stays Open.** Reliability rises **and — D133 — Alignment rises**: an Approve is Alignment evidence too | An approval is **evidence that a stakeholder approves** — never proof the plan is sound (**D115**). Alignment moves because *that is the dimension the event speaks to* (**D133**) |
| Reviewer **rejects** | Recorded in full. Reliability **rises** (a disagreement is evidence) **and — D133 — Alignment falls**: a stakeholder disagreeing is evidence about *alignment*. The **assessment is still not overwritten**, and the issue **does not move** | ✅ **D133 (was `REJECT_MOVES_CAF`, escalated).** A Reject is Alignment evidence — **but it is still evidence, not truth.** It never becomes OSLO's own read, never resolves, never re-opens, never invalidates |
| **Approve vs Reject — symmetry** | **Identical magnitude, opposite sign** (`ALIGN_STEP`, `+` or `−`), same ledger (`ALIGN_EVIDENCE`), same run. Neither is treated as more informative | **D133.** A build in which a Reject were "louder" than an Approve would be OSLO deciding that disagreement is more true than agreement. It is not — both are just evidence |
| Reviewer **suggests an alternative** | Preserved in full on the issue, forever. It is **not** auto-added as a Resolution Path, and it does **not** move Alignment — it moves reliability only | OSLO **never self-accepts**. D133 ratifies **Approve** and **Reject** as alignment evidence and names no others, so nothing else is assumed. **Escalated, not invented** — see `open-items.md` |
| Reviewer **comments** | Takes no position → **reliability only**, Alignment unchanged | A comment is context, not an attestation of agreement or disagreement |
| The confidence read **falls** after a Reject | **Allowed and honest.** Alignment down, reliability up → the index can go down. The trend line renders the fall with its **cause** | **D097** — a fall after a deeper read usually means it found something real. Suppressing it would be flattery |
| Reviewer responds while an issue is **Addressed** | The response lands; the issue **stays Addressed** | Only an analysis update moves an issue to Resolved (D088) |
| Does *anything* here resolve the issue? | **No.** `applyReviewResponse()` never writes to `_istatus` | Structural guarantee, not a copy promise (**D115**) |
| The analysis run triggered by a response | Reuses the **existing machinery** (`pushHistory` / `pushTrend` / `_refreshIssueSurfaces`) — a real trend point, a real History event, a real Attention repaint | **CRR-04**; no parallel analysis path was invented |
| Revoke the review link **before** they answer | The link dies; the request stays listed as *awaiting*; the reviewer sees the revoked page | Revocation is real (D117) |
| **At the Free cap** | **Share for review** and **Send** are disabled with an honest message: *the cap is real; the number is an owner decision* | The mechanism is canon; the number is not (**D118**) |
| **No cap number ratified** (the default state) | `_crrCapReached()` is **false** → **Free sends freely** | **Virality seeds on Free** — gate depth, never the seed (**D118**) |

## Reviewer view (D116 — proposal)

| Case | Behavior | Why |
|---|---|---|
| Reviewer arrives before responding | **No signup wall**, **no convert-moment**, no ask of any kind | **Never before value** (D116) |
| Reviewer arrives and leaves without responding | Nothing happens. The issue is untouched | A non-response is not evidence |
| Reviewer opens a **revoked** link | The revoked page — **no read is shown** | D117 |
| Reviewer responds | *Then* the convert-moment appears — *and* the done-state tells them plainly what their answer **did not** do | Honesty is owed to the recipient too (D115) |
| Is this canon? | **No.** A permanent **"Proposal — pending owner ratification"** ribbon says so, in-product | The recipient experience is **owner-open** (audit P0). **Proposed, not inferred** |

## Chat (D108/D109 machinery)

| Case | Behavior | Why |
|---|---|---|
| *"Send the review request for me"* | **"That one isn't mine to take."** → offers **Open the review package →** (the *preview*) | The chat explains; it never acts |
| *"Accept his response"* / *"Just resolve it, he approved it"* | The same boundary. The chat **cannot** resolve an issue — the function does not exist for it | Advisory-only (D001) + D115 |
| *"What's blocking my understanding?"* with nothing awaiting | *"Nothing is blocked on anyone else right now"* — and it names the real limiter (an evidence problem, not a people problem) | Grounded in live state; never a canned answer |
| Asked about a response | States what it **did** (evidence → run → reliability rose) **and** what it **did not do** (didn't resolve; OSLO didn't self-accept; the issue is still Open) | The honesty is in the *negative* half of the answer |

## Analysis-state interactions

| Case | Behavior | Why |
|---|---|---|
| A response arrives while another run is in flight | `_crrRunning` guards re-entry; the run is not double-started | One run at a time |
| A response arrives while the read is in **error** (last-good) | The run operates on the **provisional** read (the last-good one); last-good is never overwritten | D041 |
| Reliability is already **High** on all three basis dimensions | It stays High (`{High: 'High'}` in the ramp); the index nudge still applies | Monotonic, bounded, and never fabricated beyond the ramp |


---

## AMENDMENT — Controlled Release & Demand edge cases (D119–D122)

### Access / allocation (D120 · D121)
| Case | Behavior |
|---|---|
| **Allocation spent + review request to an EXISTING principal** | **Sends. Always. Never blocked, never metered.** This is the whole rule (D120) and the single most important edge case in the slice. |
| **Allocation spent + review request to a NEW person** | Send is disabled and the dialog says why, in plain words — then offers the **waitlist**, recording the review request as an **inbound demand signal**. No upsell, no urgency, no fake scarcity. |
| **Allocation spent + invite from the Share dialog** | The person is **put on the waitlist**, not silently dropped. The toast says exactly what happened. |
| **`CRR_CAP` is `null` (the honest default)** | `_allocSpent()` is `false` → **nothing is blocked**. The balance renders **unset** (*"{N} per {period} — owner-TBD (CR-1)"*), not as zero, not as infinite, and not as a count. |
| **Re-inviting an existing participant with a new role** | Free — no admission, no invite spent. Only their role changes. |
| **Admitting someone already on the waitlist** | They are removed from the waitlist the moment they are in. No ghost entries. |
| **A reviewer principal joins the waitlist** | Allowed — a reviewer has **scoped reviewer access and no seat**. Someone who already **has a seat** is told *"there is nothing to wait for."* |
| **Granting a reviewer a seat** | **DL-049 in-place promotion** — the same `Principal`, `reviewer → user`. **No second account.** Their prior attestations stay attributed to the same person. |
| **Demo trigger with 0 admissions** | *Sim allocation spent* refuses and explains: it pins the allocation to what has actually been spent, so the at-cap state is reachable **without inventing {N}**. |

### Reviewer grant (D119)
| Case | Behavior |
|---|---|
| **Reviewer opens a link whose grant they haven't accepted** | The **grant landing** — named, invited, one click. No password field is ever shown. |
| **Reviewer opens a REVOKED link** | The revoked page, **before** any grant. Not even an old copy of the read (unchanged from D117). |
| **Reviewer tries to see the rest of the project** | There is nothing to try: the grant is **scoped to the package**, and the surface says so out loud. |
| **The phase flips to GA while the reviewer view is open** | The view **re-renders**: the grant screen is skipped, the identity line becomes *"Open link (GA) — anonymous access is permitted"*, and the convert-moment becomes an ordinary *Create your own project*. |
| **The phase flips to Alpha at GA** | The gate comes back. The mechanism is phase-scoped both ways. |

### Waitlist (D121)
| Case | Behavior |
|---|---|
| **The waitlist is empty** | Honest empty state — *"Nobody is waiting."* No fake queue, no seeded numbers presented as demand. |
| **Position is asked for before any weighting is ratified** | The position shown is the person's **real arrival index**, and the UI says the order **is** arrival order because **CR-4/CR-5 are not decided**. It does not show a rank it cannot justify. |
| **The recommended-ordering preview is on** | Every surface that shows it also says, in the same breath, that it is **not ratified and not what OSLO does**. It is **off by default**. |
| **Somebody joins twice** | Deduplicated; a new demand signal is appended to the same entry rather than creating a second one. |
| **A duplicate demand signal** | Ignored — signals are unique by their text. |

### Guardrail edge cases (the ones that would be self-refuting to get wrong)
| Case | Behavior |
|---|---|
| **"3 spots left"** | **Never rendered.** The only counts shown are real ones (spent admissions, waitlist size, position). With `{N}` unset there is **no** remaining-balance number at all — the field says **owner-TBD**. |
| **An unset owner value** | Rendered as a **dashed TBD chip naming the CR item**. Never as `0`, never as `∞`, never as a plausible-looking default. |
| **A metric that cannot be computed** | Rendered as a **hole with the reason** (*"utilization needs {N}; {N} is unset"*), never as a number. |
| **Simulated data** | Carries a **`simulated data`** chip. The same visual family as the owner-TBD chip — because *"we made this up for the demo"* and *"nobody has decided this"* are the same **kind** of honesty. |

---

# AMENDMENT — D123–D126 edge cases

| # | Case | Behaviour | Doctrine |
|---|---|---|---|
| E9c-1 | **Allocation spent, reviewer is a total stranger, user is on Free, phase is Alpha.** | **The review request SENDS.** No invite, no seat, no block. The dialog says so *before* you press send. | **CR-2** — reviewer grants are free and unmetered on every tier, in every phase. **Structurally required.** Blocking here would gate the seed of the loop (CHG-061). |
| E9c-2 | **Invites left, but the project's collaborator seats are full.** | Blocked — and the message names the **TIER** limit. It states that your **invites are untouched** (and shows how many). It offers **Viewer (no seat, free)** first, then a real upgrade. | **D124** — never present a tier limit as a supply limit, or vice versa. |
| E9c-3 | **Seats free, but the monthly invites are spent.** | Blocked — and the message names the **PHASE** limit, with the **real replenish date**. **It does not offer an upgrade.** It offers the waitlist. | **D124/CR-7** — payment does not create onboarding capacity, so selling a way out of a supply constraint is a **dark pattern**. Prohibited. |
| E9c-4 | **Both limits hit at once.** | **Two separate boxes**, two different colours, two different names. Never one merged "you've hit your limit — upgrade." | **D124.** |
| ~~E9c-5~~ | ~~**The seat cap number is not ratified (T-1).**~~ | ~~The cap renders **unset** and **enforces nothing**.~~ **→ SUPERSEDED by D129 (X-1).** The cap is **ratified and enforced**: **Free 3 (incl. the owner) · Basic 10.** See E9d-1. | **Anti-Assumption** still holds — but there is no longer anything to leave unset here. |
| ~~E9c-6~~ | ~~**On Basic, how many projects can you have?**~~ | ~~**Unset (T-1)** → nothing enforced.~~ **→ SUPERSEDED by D129 (T-1).** **Basic = 10 projects**, enforced. Free = 1. | Same. |
| E9c-7 | **A reviewer answers, then the issue resolves.** | The **grant expires** (CR-6) and a History event records it. The **attestation stays on the record forever** — the record is append-only (D096). Only the *key* dies. | **CR-6** — scope link lifetime to purpose. The key was cut for one question. |
| E9c-8 | **A reviewer's grant expires; the same person is later given a seat.** | **Same Principal, promoted in place** (DL-049 / N-2). Everything they attested stays attributed to the same human. The seat spends **one invite** (they are a new *member*) and takes **one tier seat**. | **N-2** — one identity, never a second account. |
| E9c-9 | **A member is removed.** | Their **Membership ends** and a **tier seat is returned**. They remain a **Principal in OSLO**. The invite is **not refunded** — an invite admits a *human*, not a membership. Comments and attestations are **kept**. | **N-2 · D096.** |
| E9c-10 | **A Viewer is promoted to Collaborator while seats are full.** | Refused — and the message says **TIER**, never phase. They **stay a Viewer**, which costs nothing. | **D124 / N-3.** |
| E9c-11 | **Phase flipped to GA while the seat cap is full.** | The allocation and waitlist **retire**; the **seat cap still binds**, and Free is **still PDF-only**. | **D123** — the tier mechanism was never a phase mechanism. |
| E9c-12 | **User asks "can I pay to get someone in faster?"** | There is **no such affordance anywhere in the product**, and the waitlist says so in plain words: admits are hand-curated, and money does not create onboarding capacity. | **CR-7** — pay-to-skip is **prohibited in Alpha**. Not built. Not hinted at. |
| E9c-13 | **Unused invites at the end of the month.** | They **do not roll over**. The allocation line says *"non-cumulative"* before the user can be surprised by it. | **CR-1** — replenishing, non-cumulative, and honest about it. |
| E9c-14 | **A user on Free wants to know what Basic costs.** | The Plans surface shows an explicit **unset owner-TBD chip** where the price would be, and says plainly that Alpha Basic *is* charged (T-3) but the number is the owner's. | **Anti-Assumption.** Never a fake price. |
| E9c-15 | **Someone tries to make reviewer grants consume the allocation.** | `_grantReviewerAccess()`'s **runtime guard** detects the ledger moving, logs `CR-2 VIOLATION`, and **reverts**. The comment block above it explains that this is a **canon violation** requiring Framework 001, not a product tweak. | **CR-2 · CHG-061 · D120 · D126.** |

---

# AMENDMENT — D128–D131 edge cases

> **D128 P1 — never meter the epistemic record. D128 P2 — never sell safety.** These two override every metering
> edge case above. Where an earlier row assumed artifacts or history retention were tier dimensions, it is
> superseded (marked in place).

| # | Edge case | Behaviour | Why |
|---|---|---|---|
| **E9d-1** | **Free project, 3 collaborators (incl. the owner). You invite a 4th as Collaborator.** | **BLOCKED — by the TIER limit**, named in those words: *"Free projects hold **3** collaborator seats, including you — and all 3 are filled. Basic holds 10."* It **never says "out of invites"**, and it states that your allocation is untouched. It offers the **free remedy first** (Viewer — unlimited, no seat) and the review-request remedy (free, CR-2), *then* the upgrade path. | D124 — always name the limit. Presenting a supply constraint as an upsell is a dark pattern; so is presenting a tier limit as a supply one. |
| **E9d-2** | **Same project, same moment. You add someone as a VIEWER.** | **SUCCEEDS.** Viewers hold **no seat** and are **unlimited on every tier** (X-1). `checkAdmission()` cannot block a Viewer on the seat axis — `takesSeat` is false, so the branch is unreachable. A runtime guard (`_assertViewersUnlimited()`) fails loudly if anyone ever changes that. | X-1. Read-only access changes nothing about scope or cost. Unlimited read-only spread is pure upside. |
| **E9d-3** | **Allocation fully spent. You need a read from someone brand new to OSLO.** | **The review request STILL SENDS.** Free tier, Alpha, zero invites, total stranger — it sends. The CR-2 regression guard in `_grantReviewerAccess()` snapshots the invite ledger and **reverts + logs an error** if a reviewer grant ever touches it. The Share dialog says so before you ask. | CR-2 / CHG-061. Bounding evidence-seeking sabotages the product. It is structurally required, not a courtesy. |
| **E9d-4** | **A pending invite is never accepted and expires.** | **REFUNDED.** The held allocation unit **returns to your balance**, the pending Membership is removed (so any seat it was holding is released), and a **History event** records it: *"Invite to X expired — returned to your allocation."* | X-2. **No human was admitted, so no supply was consumed.** |
| **E9d-5** | **An accepted invite. You then remove the person from the project.** | **NO REFUND. Ever.** The invite admitted a **human to OSLO**, not a membership to a project. The tier **seat** comes back; the **invite** does not. History says exactly this. | X-2. Refunding on removal would create an add/remove recycling exploit. |
| **E9d-6** | **How long does a pending invite live?** | ✅ **RATIFIED (D132): 14 days.** A pending invite carries a **real expiry date**, stamped once at send (`expiresAt`), and shows it plainly: *"Expires {date} — the invite returns to your balance if unused."* On expiry it is **refunded** (X-2) with a History event. **No countdown, no urgency colour, no "expires soon" nudge** — the date is a fact, and the refund is automatic. Long enough for a busy stakeholder; short enough that supply is not parked indefinitely. | The date and the refund are **always stated together**. A date without the refund reads as manufactured scarcity; the refund is the whole point. |
| **E9d-7** | **Does any tier cap artifacts?** | **NO. Uncapped on every tier, forever.** There is no artifact-count check anywhere in the file. `ARTIFACTS_METERED = false`, `ARTIFACT_CAP = {free:∞, basic:∞}`. Code comments at the artifact store forbid reintroducing one. | **D128 P1.** Artifacts are the epistemic record. |
| **E9d-8** | **Does any tier truncate or expire History?** | **NO. History never expires and is never truncated, on any tier, in any phase.** `pushHistory()` has no cap, no trim, no tier check — and carries a comment saying so. `HISTORY_METERED = false`, `HISTORY_RETENTION = {full, full}`. Switching tier does not change `HISTORY.length`. | **D128 P1.** The append-only trace of how understanding evolved (D096) *is* the product's promise. Monetising it would sell the one thing OSLO declares inviolable. |
| **E9d-9** | **A Free user wants to revoke a link, or wants purpose-scoped expiry.** | **Both are available on Free**, identical to Basic. `revokeLink()` contains **no tier check**. Link lifetime (30 days / issue-resolve-or-14-days) is the same on both tiers. `LINK_SECURITY_TIER_LOCKED = false`. | **D128 P2 — never sell safety.** A product whose pitch is trustworthiness does not charge for the secure default. |
| **E9d-10** | **Configurable link expiry for Basic.** | **CLOSED. NOT BUILT.** Shown as *"Closed — not built (D128)"*, next to a line stating link security is **identical on every plan**. `CONFIGURABLE_EXPIRY_BASIC = false`. | D128 P2. It was the one place safety could have been sold. It is shut. |
| **E9d-11** | **GA is reached with the seat cap full.** | The **allocation and the waitlist retire** (`_gated() === false`, no phase block). The **TIER seat cap still binds** (`checkAdmission().tier === true`, `.phase === false`), Free is still PDF-only, and **Viewers are still unlimited**. | The phase mechanism is self-terminating; the tier mechanism never was one (D123). |
| **E9d-12** | **A Basic user with 10 seats filled downgrades to Free (cap 3).** | ✅ **RATIFIED (D132) — NO EVICTION. Nobody is removed.** All 10 collaborators stay, with everything they contributed still attributed to them in History. The **only** consequence: the account **cannot ADD another Collaborator** until it is back under 3, or it upgrades. Viewers stay unlimited (X-1); review requests stay free (CR-2). The over-cap state is **surfaced explicitly** wherever seats are shown: *"This project has 10 collaborators; Free adds up to 3. No one has been removed — you can't add more until you're under 3, or upgrade."* | **The seat cap gates ADMISSION, never EVICTION.** Evicting humans from a project to enforce a billing change is **prohibited on a trust product**. Enforced in code by `EVICT_ON_DOWNGRADE = false` and the runtime guard `_assertNoEvictionOnDowngrade()`, which fails loudly and restores the roster if any tier change ever removes a Membership. |
| **E9d-13** | **Does a Reject move CAF?** | ✅ **RATIFIED (D133) — NOW BUILT.** ~~STILL NOT BUILT.~~ **Yes — via Alignment**, a first-class CAF dimension (DL-062). A Reject enters as **evidence** and moves **Alignment + Reliability** through a **normal Extended Analysis run** (the existing `pushHistory`/`pushTrend`/`_refreshIssueSurfaces` path — no parallel machinery). **Symmetrically, an Approve does too** — same step, opposite sign; neither direction is privileged. **All D115 bounds hold, unweakened:** third-party attestation (*"Attested by \<name\>"*), never OSLO's own read, **never auto-resolves, never auto-re-opens** (nothing writes `_istatus`), and OSLO never self-accepts — the copy reads *"\<Name\> rejected this"*, **never** *"this is now wrong / invalid / re-opened"*. | **D133.** Refusing to let a Reject touch CAF would mean OSLO watched a sponsor reject a finding and learned **nothing about alignment** — precisely the dimension the event speaks to. `REJECT_MOVES_CAF = true`. Still rides in the Framework 001 package (D131) to become **repository** canon. |
| **E9d-13a** | **Does a *Suggest alternative* move Alignment?** | **NOT BUILT — and NOT assumed.** It moves **reliability only**. D133 names **Approve** and **Reject**; it names no others. | **Anti-Assumption + the symmetry clause.** Counting an alternative as a "half-Reject" with no symmetric "half-Approve" would give the system a quiet **negative bias** — the exact failure D133's symmetry rule exists to prevent. **Escalated** in `open-items.md` (recommendation: let the reviewer *state* it, rather than have OSLO infer it). |
| **E9d-14** | **The Extended Analysis run counts.** | **Unset (T-1 residual).** The *shape* is ratified — Free *a small monthly budget*, Basic *a generous* one — and renders in words; the **run count renders as an owner-TBD chip**. Nothing is enforced against an unset number. | The one honest **cost**-linked meter (DL-048). The shape is ratified; the number is the owner's. |
| **E9d-15** | **The demo trigger "Sim seat cap reached".** | The cap is now **real**, so the trigger no longer pins a fiction — it **seats demo colleagues who are already principals in OSLO**, so **no invite is spent** filling seats (the two meters stay separate). It never adds or blocks a Viewer. The blocked state is *also* reachable through the ordinary UI on Free (promote the Viewer, then invite one more Collaborator). | No fabricated scarcity. The state is honestly reachable. |
