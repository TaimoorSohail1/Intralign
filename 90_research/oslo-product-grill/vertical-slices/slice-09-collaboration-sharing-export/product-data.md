# Slice 9 — Collaboration, Sharing & Export · Product Data

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


Cumulative Slices 1–9. **Client-side only — no database, no backend, no network, no auth, no email (D016).** All state is in-memory JS plus `localStorage`. Numbers, names and emails are **illustrative**.

## Entity: Person / Teammate (`TEAMMATES[]`)

| Field | Type | Notes |
|---|---|---|
| `name` | string | display name |
| `email` | string | illustrative |
| `init` | string | avatar initials (also derived by `_initials9()`) |
| `role` | string | the role they *play* (`Programme lead`, `Operations`, **`Sponsor`**, `Venue contact`) — **not** a permission |

Seed: Sam Okafor · Priya Raman · **Marcus Hale (Sponsor)** · Dana Whitlock (Venue contact). `role` drives the MRI-07 headline (*"awaiting **sponsor** review"*).

## Entity: Participant (`PARTICIPANTS[]`) — D110

| Field | Type | Notes |
|---|---|---|
| `name` / `email` | string | |
| `type` | enum | **`Owner` \| `Collaborator` \| `Viewer`** |
| `you` | boolean | the owner row; cannot be removed |

`PARTICIPANT_TYPES[]` = `{k, line}` — the **one plain statement** per type rendered in the sharing dialog. **Presentation-only: nothing is enforced.** Seed: Idris (Owner, you) · Sam (Collaborator) · Priya (Viewer).

## Entity: ShareLink (`SHARELINKS[]`) — D110 / D117

| Field | Type | Notes |
|---|---|---|
| `id` | string | `lnk-N` |
| `kind` | enum | **`snapshot`** (whole project, view-only) \| **`issue`** (one review package) — the **scope** |
| `scope` | string\|null | the issue id when `kind==='issue'` |
| `url` | string | illustrative |
| `ts` | string | relative stamp |
| `runIndex` | number | `TREND.length` **at creation** — the staleness anchor |
| `revoked` | boolean | **revocable**; a revoked link opens nothing |

`_linkStale(l)` = `TREND.length > l.runIndex` → the link is relabelled **"previous analysis"**. **`SHARE_LINK_EXPIRY = null`** — an explicit **owner-TBD** (D117 / gap #339). **No expiry default exists in the code.**

## Entity: Comment (`COMMENTS{issueId → []}`) — D111

| Field | Type | Notes |
|---|---|---|
| `id` | string | `CM-N` |
| `who` / `email` | string | the author (the signed-in user in this prototype) |
| `ts` | string | relative stamp |
| `body` | string | raw text; `@Name` rendered as `.mention` |
| `parent` | string\|null | a reply threads under its parent |
| `mentions` | string[] | names detected in the body |

**Append-only.** No `edit`/`delete` field, and no `editComment()`/`deleteComment()` function exists. Keyed by **issue** — comments have no home outside the Issue Panel (Panel Model, D009). Every comment appends a `comment` History event.

## Entity: ReviewRequest (`REVIEWS[]`) — D114 / D115

| Field | Type | Notes |
|---|---|---|
| `id` | string | `RVW-N` |
| `issueId` | string | the one issue this package is about |
| `reviewer` | `{name, email}` | a teammate or any typed email |
| `note` | string | optional note from the sender |
| `ts` | string | relative stamp |
| `status` | enum | **`awaiting` \| `responded`** — *this is not the issue's status* |
| `response` | `{kind, body, at, by}` \| null | **CRR-03**: `kind ∈ comment \| approve \| reject \| alternative`; `body` preserved in full, forever |
| `linkId` | string | the **issue-scoped**, revocable ShareLink |

`CRR_RESPONSES[]` = the four kinds + their one-line meanings.

### `ALIGN_EVIDENCE[]` — attested alignment inputs (**D133**)

| Field | Type | Meaning |
|---|---|---|
| `rid` | string | the `REVIEWS[]` id this evidence came from |
| `issueId` | string | the issue it was attested against |
| `by` | string | the attesting reviewer (**never** OSLO) |
| `kind` | enum | **`approve` \| `reject`** — the two ratified alignment-evidence kinds (D133). `comment` and `alternative` are **not** recorded here |

Constants: **`REJECT_MOVES_CAF = true`** (ratified, D133 — not a feature flag: there is no "off" branch) ·
**`ALIGN_STEP = 8`** (**symmetric** — the *same* step for Approve `+` and Reject `−`; never split it) ·
`ALIGN_MIN / ALIGN_MAX` (illustrative bounds; the UI states **direction and cause**, never a magnitude — D056).

**`READ.*` gains `alignLvl` / `alignW`** — **Alignment is now a live CAF dimension**, exactly as `feasLvl`/`feasW`
already were. The **limiting dimension is computed**, not hardcoded, so Alignment can become the limit. Alignment
evidence is written to **both** `READ.provisional` and `READ.current` (it is evidence about the *project*, not about
one run), so it does not vanish when the analysis state flips.

**Invariants (D115 · D133) — enforced by construction:**
- `applyReviewResponse()` and `_reviewAnalysisRun()` **never write `_istatus`** — no auto-resolve, **no auto-re-open**.
- The assessment is **never overwritten** by a reviewer's assertion; it is recorded as *"Attested by \<name\>"*.
- **Symmetry:** Approve and Reject use the **same** `ALIGN_STEP`, the same ledger, and the same run.

**Invariants (D115) — enforced by construction:**
- `applyReviewResponse()` **never writes to `_istatus`.** The issue's lifecycle is untouched by a request *or* a response.
- `_reviewAnalysisRun()` mutates only `READ.*.reliability` (+ a small illustrative index nudge) — **never `band`**, never CAF, never `_istatus`.
- There is no code path in which OSLO accepts a response.

## Recommendation type (`ISSUES[].rectype`) — REC-05

New field on the existing `ISSUES` model: `validation` \| `definition` \| `planning` \| `alignment`.
`ISS-01` (venue Wi-Fi) and `ISS-03` (keynote backups) = **`validation`** → `_isPrimeCrr()` → *Share for review* is the **primary** action + the *prime candidate* line. The rest are not.

## Free-tier CRR cap (D118)

| Symbol | Value | Notes |
|---|---|---|
| `CRR_CAP` | **`null`** | **OWNER-TBD. The number is not ratified and is NOT invented.** |
| `_crrUsed()` | `REVIEWS.length` | |
| `_crrCapSet()` | `typeof CRR_CAP === 'number'` | |
| `_crrCapReached()` | `_crrCapSet() && _crrUsed() >= CRR_CAP` | → `false` while unset ⇒ **Free can always send** |
| `_crrCounterHTML()` | *"X of **{N} — owner-TBD}** review requests used"* | `{N}` renders as a `.tbd` chip |

`simCrrCap()` (demo) pins `CRR_CAP = _crrUsed()` so the at-cap state is reachable **without inventing an owner value**; toggling it off restores `null`.

## Export (D112)

`EXPORT_FORMATS[]` = `{k:'pdf', free:true}` · `{k:'copy', free:false}` · `{k:'link', free:false}`. `TIER = 'free'` ⇒ PDF only; the others are **shown and locked** (visibility-first). `EXPORT_DISCLAIMER` is a constant, always rendered. `_readCurrency()` derives the currency marker from `HISTORY` (last analysis event), `TREND` (last run name) and `ANALYSIS_STATE` — no invented timestamps.

## History events (append-only; D096)

New types, all in the new **`collab`** category: **`comment`** (Comment) · **`review_request`** (Review request) · **`review_response`** (Review response) · **`share`** (Sharing — invites, link created, link revoked, participant removed) · **`export`** (Export). Icons in `_histicon`; labels in `_histCatLabel`; a **Collaboration** filter chip on the History surface.

An `export` event and a `comment` event carry **no `run`** and **no trend point** — they cannot move the read, and the data model makes that structurally true.

## Notifications (D113)

`NOTIF_CATS` — `mention`, `reply`, `shared with me` are `later:false` (un-gated) and default **on**. `applyReviewResponse()` unshifts a live item: `{cat:'reply', l:'\<name\> responded to your review request', route:'issues', unread:true}`. Still **presentation-only** (D104): routing navigates; it never triggers an analysis.

## localStorage keys (namespaced `oslo-s1-*`, via `LS`)

Inherited: `account`, `staySignedIn`, `phase`, `orientSeen`, `tourSeen`, `theme`, `profileName`, `profileRole`, `wsName`, `notifPrefs`, `chat-*`, per-artifact `<key>` + `<key>-ver`.
**New in Slice 9:** **`defaultShareRole`** (`"Collaborator"` | `"Viewer"`). Cleared by `resetDemo()`.

## Persistence & lifecycle

- **No DB, no server.** Participants, links, comments and reviews are in-memory; only the default share role persists.
- **Nothing is destructive.** Revoking a link, removing a participant, and clearing the cap are all non-destructive; comments and responses are never deleted (append-only).
- **No collaboration action can change an assessment.** Only `_reviewAnalysisRun()` (an analysis run, driven by *evidence*) moves the read — and it moves **reliability**, never the assessment.


---

## AMENDMENT — Controlled Release & Demand entities (D119–D122)

### Entity: Principal (`PRINCIPALS[]`) — DL-049 · D119 · D120
| Field | Type | Notes |
|---|---|---|
| `email` | string | identity |
| `name` | string | |
| `type` | `'user' \| 'reviewer'` | **ONE Principal object**, promoted **in place** (DL-049). A reviewer principal holds scoped reviewer access and **no seat**. |
| `seat` | `'Owner' \| 'Collaborator' \| 'Viewer' \| 'Reviewer'` | presentation-only |
| `since` | string | illustrative |
| `scope` | string \| null | for reviewers: the issue id their grant is scoped to. **Not the whole project.** |

Seeded: Idris (owner) · Sam (user) · Priya (user) · **Marcus (reviewer)**. **Dana is deliberately NOT a principal** — she is the *new person* case, so the D120 cost difference is visible in the picker without inventing anything.

**`_reviewCost(email)`** → `'free'` when `_isPrincipal(email)`, else `'admit'`. That function **is** D120.

### Entity: Admission (`ADMISSIONS[]`) — D120
`{email, name, kind:'collaborator'|'reviewer', via:'invite'|'review request'|'skip-the-line', ts, scope}`
**The only ledger an invite draws on.** `_admitted()` counts admissions. **Review requests are never counted here** — `REVIEWS[]` is a record, not a meter.

### Entity: WaitlistEntry (`WAITLIST[]`) — D121
`{email, name, org, role, joined, signals:[{k:'referral'|'review'|'fit', l}]}`
- **Position is real**: the entry's actual index in the list (`_waitPos()`), shown as *"#3 of 5"* against a real total.
- **Ordering is arrival order by default** — because the weightings (**CR-4 / CR-5**) are **not ratified**. `WL_PREVIEW_WEIGHTS` (default `false`) exposes the *recommended* ranking (`_SIG_RANK`: review 3 > referral 2 > fit 1) as an explicitly-labelled preview of an **unratified recommendation**.
- A principal with a **seat** cannot join (nothing to wait for). A **reviewer** principal **can** — they have no seat, and DL-049 promotes them in place when granted one.

### Owner-TBD register — the values that DO NOT EXIST in this build
| Const | Value | Owner item |
|---|---|---|
| `CRR_CAP` | `null` | **CR-1** — {N} invites (the allocation) |
| `INVITE_PERIOD` / `REPLENISH_DATE` | `null` | **CR-1** — the {period} |
| `REVIEWER_GRANT_COST` | `null` | **CR-2** — what admitting a first-time reviewer costs |
| `WAITLIST_ADMIT_RATE` | `null` | **CR-3** — admit rate + curation |
| `REFERRAL_WEIGHT` | `null` | **CR-4** — referral weighting |
| `REVIEW_REQ_MOVES_QUEUE` | `null` | **CR-5** — does an inbound review request move the queue |
| `SHARE_LINK_EXPIRY` | `null` | **CR-6** — link expiry (gap #339) |
| `CONVERT_MOMENT_IN_R1` | `null` | **CR-7** — convert-moment R1 vs fast-follow |

Every one renders through `_tbdSpan()` as an explicit **owner-TBD** chip. **No default is assigned anywhere.**

### Simulated demand data (`DEMAND_SIM`) — D121
`{weeks[], joins[], velocityNote}` — **simulated**, rendered under a `simulated data` chip. Real counts (waitlist size, admissions, review requests) are drawn from live state. Metrics that need an owner value (utilization) or real cohorts (k per loop) are shown as **holes, not numbers**.

### History events (added)
`admit` (⊕ *Access granted*) · `waitlist` (◷ *Waitlist*) — both in the **Collaboration** filter bucket. Append-only (D096).

### Notifications (added)
Category **`access`** — *"when someone you invited asks for a seat, or an invite from your allocation is spent"*. On by default; routes to the Access modal.

---

# AMENDMENT — D123–D126: the data model (N-2 — ONE IDENTITY)

**`PARTICIPANTS[]` is deleted.** There is one identity and two relations over it.

```
Principal            (DL-049 — THE single identity registry)
  { email, name, type: 'user' | 'reviewer', seat, since, scope }
        │
        ├── Membership          (principal × project × role)      ← THE TIER SEAT CAP IS ENFORCED HERE
        │     { email, project, role: 'Owner'|'Collaborator'|'Viewer' }
        │       · Owner / Collaborator  → TAKES A SEAT
        │       · Viewer               → TAKES NO SEAT   (N-3)
        │
        └── ReviewGrant         (principal × package, scoped, expiring)
              { email, name, issueId, ts }
                · NOT a Membership. TAKES NO SEAT. COST NO INVITE.   (N-2 · CR-2)
                · Expires when the issue RESOLVES, or in 14 days — whichever first (CR-6)
```

**"Participant" is a VIEW** — `_members()` joins `MEMBERSHIPS × PRINCIPALS`. Nothing writes to it.

**Promotion is IN PLACE** (DL-049): a reviewer given a seat keeps the **same Principal**. Everything they already attested stays attributed to the same human. There is never a second account.

## The two meters (D124)

| | Ledger | Cap | Ratified? |
|---|---|---|---|
| **PHASE — invites** | `ADMISSIONS[]` (+ `_simSpent` for the demo) — appended **only** by `admitPrincipal()`, i.e. **only when a NEW HUMAN becomes a member** | `PHASE_ALLOCATION = {free: 2, basic: 5}` per **calendar month**, `ALLOCATION_CUMULATIVE = false` | **YES** (CR-1/T-2) |
| **TIER — seats** | `MEMBERSHIPS[]` filtered by `_roleTakesSeat()` → `_seatsUsed()` | `SEAT_CAP = {free: null, basic: null}` — **owner-TBD (T-1)**; renders **unset**, enforces nothing. `SEAT_CAP_SIM` pins it for the demo only, and is labelled *simulated*. | Shape yes, **numbers NO** |

**`REVIEW_GRANTS[]` never appears in `ADMISSIONS[]`.** That is asserted at runtime in `_grantReviewerAccess()` (the CR-2 regression guard).

## Ratified constants

```js
PHASE_ALLOCATION            = { free: 2, basic: 5 };  // CR-1 / T-2
ALLOCATION_PERIOD           = 'month';                // CR-1
ALLOCATION_CUMULATIVE       = false;                  // CR-1 — unused invites do NOT roll over
CR2_REVIEWER_GRANTS_FREE    = true;                   // CR-2 — structurally required
CR2_ANTI_ABUSE_CEILING      = 200;                    // CR-2 — anti-abuse ONLY, never scarcity
WAITLIST_CURATION           = 'hand-curated';         // CR-3 — throttled by onboarding capacity
POINTS_ECONOMY              = false;                  // CR-4 — there is none
REVIEW_REQ_TOP_BAND         = true;                   // CR-5
SHARE_LINK_EXPIRY_DAYS      = 30;                     // CR-6
REVIEW_GRANT_MAX_DAYS       = 14;                     // CR-6
REVIEW_GRANT_ENDS_ON_RESOLVE= true;                   // CR-6
CONVERT_MOMENT              = 'waitlist';             // CR-7
PAY_TO_SKIP                 = false;                  // CR-7 — PROHIBITED. Not built. Not hinted at.
TIER                        = LS.get('tier','free');  // D123 — MUTABLE, live in Alpha
```

## Still `null` — owner-TBD. **These render UNSET. Never invent them.**

```js
BASIC_PRICE               = null;   // T-3 — Basic IS charged; the price is the owner's
SEAT_CAP                  = { free: null, basic: null };  // T-1 — shape ratified, numbers not
BASIC_PROJECT_CAP         = null;   // T-1
BASIC_ANALYSIS_FREQ       = null;   // T-1
BASIC_ARTIFACT_CAP        = null;   // T-1
BASIC_RETENTION           = null;   // T-1
CONFIGURABLE_EXPIRY_BASIC = null;   // CR-6 — owner-open; deliberately NOT built
```

## Waitlist (CR-4 — no points economy)

```js
WL_BANDS = [ {k:'review',   n:1},   // CR-5 — an inbound review request lands you here
             {k:'referral', n:2},   // referred by an active user — a SIGNAL, not a currency
             {k:'cold',     n:3} ]; // no signal — and no penalty for it
_waitlistOrdered() → sort by band, then by arrival date (`seq`). Nothing else. No score.
```

## localStorage

Adds one key: **`oslo-s1-tier`** (`'free' | 'basic'`). Cleared by `resetDemo()`.

---

# AMENDMENT — D128–D131 data model (2026-07-11)

## The meter registry (D128 P1) — the whole list, as constants

| Constant | Value | Meaning |
|---|---|---|
| `METERED_DIMENSIONS` | `['extended-analysis-runs','projects','collaborator-seats']` | **The entire set of metered dimensions.** Nothing else is metered by tier. |
| `ARTIFACTS_METERED` | `false` | **Never.** Artifacts are uncapped on every tier, in every phase. |
| `HISTORY_METERED` | `false` | **Never.** History never expires and is never truncated. |
| `ARTIFACT_CAP` | `{free: Infinity, basic: Infinity}` | There is no cap, and therefore no number to set. |
| `HISTORY_RETENTION` | `{free:'full', basic:'full'}` | Full, forever, on every tier. |
| `LINK_SECURITY_TIER_LOCKED` | `false` | **D128 P2** — revocation + purpose-scoped expiry are free on every tier. |
| `CONFIGURABLE_EXPIRY_BASIC` | `false` | **CLOSED, not built** (was `null` / owner-open). |

> **DELETED constants:** `BASIC_ARTIFACT_CAP` and `BASIC_RETENTION` — they encoded the idea that the epistemic
> record is a tier dimension. **It is not.** Code comments now sit at `pushHistory()` and the artifact-version
> store forbidding their reintroduction.

## Tier caps (D129 · T-1 · X-1) — RATIFIED

| Constant | Value |
|---|---|
| `SEAT_CAP` | `{free: 3, basic: 10}` — **collaborator seats, including the owner** |
| `VIEWER_CAP` | `{free: Infinity, basic: Infinity}` — **X-1: viewers are unlimited** |
| `FREE_ACTIVE_CAP` / `BASIC_PROJECT_CAP` | `1` / `10` — projects |
| `ANALYSIS_BUDGET` | `{free: null, basic: null}` — ⚠️ **owner-TBD; renders unset** |
| `ANALYSIS_BUDGET_SHAPE` | `{free:'a small monthly budget', basic:'a generous monthly budget'}` — the **ratified shape** |
| `BASIC_PRICE` | `null` — ⚠️ **owner-TBD (T-3)** |

**Seat accounting.** `_seatsUsed()` counts **Memberships whose role holds a seat** (Owner, Collaborator). Viewers
are excluded by construction; reviewers holding only a `ReviewGrant` are not Memberships at all (N-2).
`checkAdmission()` can only raise a `tier` hit when `takesSeat` is true — so **a Viewer is structurally
unblockable** on the seat axis. `_assertViewersUnlimited()` is a runtime guard that logs loudly if that ever breaks.

## Entity: Invite (`INVITES[]`) — **NEW (X-2)**

```
{ email, name, role, status: 'pending' | 'accepted' | 'expired', ts, via }
```

| Transition | Function | Effect on the balance |
|---|---|---|
| **sent** → `pending` | `inviteNewHuman(email, name, role, via)` | **HOLDS** one allocation unit. A pending `Membership` (`pending:true`) is created, so a Collaborator invite also **reserves** its seat. |
| `pending` → `accepted` | `acceptInvite(email)` | Moves to `ADMISSIONS[]`. **SPENT FOR GOOD — never refunded** (`INVITE_REFUND_ON_ACCEPT = false`). Net balance change: zero (held → spent). |
| `pending` → `expired` | `expireInvite(email)` | **REFUNDED** (`INVITE_REFUND_ON_EXPIRY = true`). The pending Membership is removed, releasing any seat it held. **History event** records the refund and the before/after balance. |

**Allocation arithmetic (X-3 — calendar month):**

```
_admitted()  = ADMISSIONS.length + _simSpent      // accepted — spent for good
_allocHeld() = _pendingInvites().length            // pending — refundable on expiry
_allocUsed() = _admitted() + _allocHeld()          // what the balance reflects
_allocLeft() = max(0, _allocCap() - _allocUsed())
```

✅ **`INVITE_EXPIRY_DAYS = 14` — RATIFIED (D132, X-2a).** A pending invite lives **14 days**, then expires and is
**refunded** (X-2) with a History event. The expiry date is **stamped once at send** onto the invite record
(`expiresAt`) and surfaced honestly wherever the invite appears: *"Expires {date} — the invite returns to your
balance if unused."* **The date and the refund are always stated together** — a date without the refund would read
as manufactured scarcity. **No countdown, no urgency colour, no "expires soon" nudge.** In the prototype, expiry is
still *driven* by an explicit control (there is no clock in a static page), but the **window itself is real**.

```
INVITE record  = {email, name, role, status:'pending'|'accepted'|'expired', ts, via, expiresAt:Date}
_inviteExpiryAt()      → now + INVITE_EXPIRY_DAYS      // computed ONCE, at send
_inviteExpiryLine(inv) → "Expires {date} — the invite returns to your balance if unused (X-2)"
```

✅ **`EVICT_ON_DOWNGRADE = false` — RATIFIED (D132).** The seat cap gates **ADMISSION**, never **EVICTION**.
Dropping from Basic (10 collaborators) to Free (cap 3) removes **nobody**. `_seatsOverCap()` (`_seatsUsed() >
_seatCap()`) is the over-cap state; `_overCapNoticeHTML()` renders it, leading with *"No one has been removed."*
`setTier()` snapshots the Membership roster and calls `_assertNoEvictionOnDowngrade()`, which **fails loudly and
restores the roster** if any tier change ever removes a Membership. **No code path removes a Membership on
downgrade.**
