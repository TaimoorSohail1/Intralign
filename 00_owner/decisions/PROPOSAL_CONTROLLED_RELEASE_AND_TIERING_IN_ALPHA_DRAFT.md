# Proposal — Controlled Release & Tiering-in-Alpha (reconciles CHG-061; amends DL-048 scope, extends DL-049/DL-055/DL-062)

**Document Type:** Governance Proposal (Framework 001 / 001A) — **plan only; nothing ratified** · **Status:** **Draft — awaiting owner ratification** · **Date:** 2026-07-10
**Origin:** Owner direction (working session, 2026-07-10) during the R1 product-grill of Slice 9 (Collaboration, Sharing & Export). Authored by AI contributor as scribe — **non-ratifying** (`CLAUDE.md` Authority Constraint: only the repository owner may ratify).
**Backlog:** RB-TBD. **Draft record:** `records/DL-101-controlled-release-and-tiering-in-alpha.md`.
**Layer:** Product scope / monetization + collaboration seam (`10_product`, `20_handoff`). **Non-doctrinal** — no epistemic invariant is amended; D115/CRR bounds are *tightened*, never loosened.
**Consolidation note (deliberate):** this is **one** proposal, not five. Its constituents are **interdependent** — constituent B is the *sole* resolution of constituent A, and C exists only because of B. Splitting them would permit a reviewer to ratify one while silently breaking another.

---

## Context

Grilling Slice 9 surfaced a live conflict between two ratified positions.

- **DL-021 / release canon:** Alpha and Beta are **invite-only — users are never anonymous.** GA is the first phase permitting anonymous access.
- **CRR-01…05 + `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001` (P0):** OSLO's **core value action is also its viral action** — a CAF Review Request invites a stakeholder *because the user needs their evidence*, and the response becomes evidence that improves understanding (CRR-04 → Deep Pass). The audit recommends a **no-account-required** recipient experience.

A no-account reviewer is, on its face, an anonymous product interaction in a phase that forbids them. Separately, the owner has now confirmed that the **Basic tier is purchasable during Alpha**, which removes the assumption that tier limits are moot pre-GA and puts **CHG-061** ("guarantee the viral primitives on Free… never gate the seed of the loop") into force *immediately* rather than at GA.

Two prior AI positions were **wrong and are corrected here**, on the record:
1. *"CRR is a genuine spec gap; defer it."* — **False.** CRR-01…05 are Alpha-scope, High-priority canon with exit criterion C14, and **DL-049 had already resolved gap #337** (the external-reviewer identity model).
2. *"CHG-061 is a GA-phase tier rule; controlled release is an Alpha phase rule; they sunset past each other."* — **Dead** once Basic is live in Alpha. The reconciliation now rests entirely on constituent B.

## Proposed decision (constituents)

**A. Reviewer identity — the invite IS the authentication.**
A review-request link carries a token granting **Reviewer Principal** access (DL-049: single `Principal`, `type: reviewer | user`, in-place promotion), **scoped to exactly that review package**. The reviewer is therefore *identified and invited* — **never anonymous** — satisfying DL-021 with **no signup wall** and without breaking the CRR evidence loop. Zero-friction and invite-only are not in conflict once "no password" is distinguished from "no identity."

**B. Bound seats; never bound evidence. (Load-bearing.)**
An invite is consumed **only when a NEW principal is admitted** (collaborator seat, or first-time reviewer). **Sending a review request to an existing principal is free, forever, unmetered — on every tier, in every phase.** Reviewer grants are **free and unmetered** and capped only at an anti-abuse ceiling.
**This constituent is the sole resolution of the CHG-061 conflict:** with reviewer grants free, the *seed* of the loop — CRR evidence-seeking — **is not gated on any tier or in any phase**. Only **seats** are metered. CHG-061 then holds **literally**, not by argument. If reviewer grants were ever made to consume an allocation, OSLO would gate the seed of its own loop, in direct conflict with applied canon.
*Cost note:* each response triggers an Extended Analysis → the **DL-048 token budget** applies. That is a **cost** control, never a monetization gate.

**C. Controlled release + waitlist (Alpha/Beta), with an explicit sunset.**
Bounded, replenishing invite allocation (**Basic 5/month · Free 2/month**, calendar-month, non-cumulative; Free non-zero because virality must seed on Free). Waitlist with an **earned, real** position — improved by converted referrals, by **being review-requested** (the strongest inbound demand signal), and by role/org fit; **no points economy**. Skip-the-line by spending an invite. The reviewer **convert-moment is the waitlist**, offered **only after they respond** (post-value, never pre-value). **Phase ramp:** Alpha (tight) → Beta (loosening) → **GA (open; anonymous permitted per DL-021/D024; waitlist retired; limits become tier-based)**. The scarcity mechanism is **phase-scoped and self-terminating** — it is not the business model.
**Pay-to-skip is PROHIBITED in Alpha.** The queue is throttled by *onboarding capacity*; **payment does not create capacity**, so selling passage past it is a toll booth on an invented constraint. It becomes legitimate only if revenue genuinely expands supply — a separate decision.

**D. Two limits, never conflated.**
**PHASE** (supply: may you admit a new human?) and **TIER** (depth: what may a seat do?) are orthogonal and both live in Alpha. The product must **always name which limit blocked the user**. Presenting a *supply* constraint as an *upsell* manufactures a purchase out of scarcity and is prohibited as a dark pattern.

**E. Tier boundary (unblocks DL-048's "paid-tier limits TBD", which is now blocking).**
**Free fully delivers the core read** — intake → Fast Pass → Overview → Attention → Issues → **CRR**. **Basic sells depth and volume.** Canon is authoritative wherever it speaks: **projects Free 1 / Basic 3** (UP-3 — *not* the Basic-10 an earlier draft proposed; withdrawn), **daily fixes Free 5 / Basic 20** (UP-1), **daily chat Free 20** (UP-2), **deep runs/day Free 2** (UP-5), **export Free = PDF only**. **Collaborator seats Free 3 / Basic 10, Viewers unlimited** — a **recommendation into a genuine gap** (see Concern 7), superseded on sight by a written Tier Definitions. Extended Analysis budget: shape ratified, numbers owner-open.
**E-1 — Limit-reached interaction rule (adopted from Seam Audit 001; applies to every cap here, seats included):** the affordance **stays enabled**, the *attempt* is gated, and the surface presents the value-framed prompt **with resolutions** ("upgrade **or** archive"). **Never disabled, never hidden** (disabling suppresses the highest-intent moment); **never a raw error.**
**E-2 — Seats become ENFORCED, amending visibility-first (stated, not smuggled):** `INVITE_AND_SHARE_MODAL_EXPERIENCE_SPECIFICATION_V1` §N specifies seat limits as *"visibility-first… no billing/entitlement implementation."* Because Basic is purchasable in Alpha, tier limits are live and seats are **enforced** (subject to E-1 and to no-eviction-on-downgrade). This **amends** that seat rule; nothing else in that specification changes.
**Two governing metering principles:**
- **Meter only what costs money or defines scope. NEVER meter the epistemic record.** Artifacts are **never capped**; History **never expires or truncates**. The append-only trace of how understanding evolved (DL-096) *is* the product's core promise; monetizing it would sell the one thing OSLO declares inviolable.
- **Never sell safety.** Link revocation and purpose-scoped expiry are trust hygiene **for every tier** — never a paid feature.
**No eviction on downgrade:** an over-cap account cannot *add* a Collaborator, but **no human is ever removed** to enforce a billing change.

**F. A Reject moves CAF, via Alignment (extends DL-062).**
A stakeholder **Reject** on a review request is **evidence about Alignment** — a first-class CAF dimension (DL-062) — and may move Alignment (and Reliability) through a normal Extended Analysis run. **An Approve is equally Alignment evidence; neither direction is privileged.** Bounded exactly as D115 binds every reviewer response: **evidence, not truth**; recorded as a **third-party attestation** ("Attested by \<name\>"), never as OSLO's read; **never auto-resolves and never auto-re-opens** an issue; **OSLO never self-accepts**. Refusing to let a Reject touch CAF would mean OSLO watched a sponsor reject a finding and learned **nothing about alignment** — the very dimension the event speaks to.

## Findings

1. **A real, live conflict is resolved without weakening either side.** DL-021's "never anonymous" and the audit's "no-account reviewer" are both satisfied by constituent A: the token grant makes the reviewer an *invited, identified* Principal. DL-049 already provided the object model; nothing new is invented.
2. **The CHG-061 conflict has exactly one honest resolution, and it is constituent B.** Now that Basic is live in Alpha, the tier rule no longer waits for GA, so the earlier "orthogonal axes / sunset" argument fails. Free, unmetered reviewer grants leave the seed of the loop ungated — which is what CHG-061 actually demands.
3. **The value/virality identity is preserved.** Because a review request is *how a user gets their answer*, metering it would degrade understanding by design. Constituent B protects the product mechanism and the growth mechanism with a single rule.
4. **Scarcity is bounded, honest, and self-terminating.** Real counts only, no fabricated urgency, explicit GA sunset, and instrumented (waitlist velocity, invite utilization, review-request→admit conversion, k per loop via TEL-06).
5. **Constituent F closes a genuine epistemic hole** without loosening any D115 bound; the symmetry clause (Approve and Reject carry equal weight) prevents a negative-bias failure mode.

## Concerns

1. **Scarcity amplifies desire; it cannot manufacture it.** Superhuman's waitlist gated an already-exceptional product paired with concierge onboarding. If OSLO's read is not compelling, a waitlist will not create outsized demand — it will **hide a weak funnel and delay the feedback that would have revealed it.** The instrumentation in constituent C exists precisely so this failure is detectable. **Owner-accepted trade; flagged so waitlist growth is not over-read as product validation.**
2. **Every number here is a judgment, not a derivation** (3 / 10 / 1 project / 5 / 2 / 14 days). They were chosen to be **easy to loosen and painful to tighten** — the correct direction of error before real alpha data exists. They must be treated as **instrumented hypotheses**, not settled canon.
3. **Constituent B is load-bearing and fragile to erosion.** A future "just cap review requests a little" change would silently re-break CHG-061 *and* the product mechanism. Runtime guards exist in the prototype; canon should state the rule explicitly so it cannot be eroded by increments.
4. **DL-048's "paid-tier limits TBD" is now blocking, not deferred.** Basic cannot ship in Alpha without constituent E. The Extended-Analysis budget numbers remain owner-open.
5. **Basic price is undecided** and is not proposed here (business decision, deliberately not inferred).
6. **Anti-Assumption residue.** Whether a *Suggest alternative* response also carries Alignment signal is **undefined** and deliberately unbuilt: counting it as a partial Reject with no symmetric partial Approve would quietly introduce a **negative bias**, defeating constituent F's symmetry clause. Escalated, not resolved.

7. **BLOCKING GAP — "Release 1 Tier Definitions" is cited by 18 canonical documents and DOES NOT EXIST.** Seat, sharing, and tier limits across the product all defer to it. The tier layer therefore rests on a citation to a hole, and it is the reason the seat numbers here are a recommendation rather than a reading. **Recommend commissioning `RELEASE_1_TIER_DEFINITIONS_V1` as a blocking prerequisite for shipping Basic in Alpha**, consolidating every per-tier number now scattered across MON-01…04, the UP-* taxonomy, and this decision. Escalated per Anti-Assumption; **not filled**.

8. **An AI-authored number contradicted ratified canon and was ratified on that advice.** "Basic = 10 projects" was recommended without first checking the UP-* taxonomy (which ratifies **Basic = 3**). Canon prevails; the error is recorded in the decision record rather than silently corrected, because the failure mode — proposing a number into an area canon had already settled — is the one this repository's Anti-Assumption protocol exists to catch.

## Dependencies

- **Resolves:** the CHG-061 / Virality-audit-P2 conflict (via constituent B); matrix gap **#337** residue (via A, on the DL-049 model); gap **#339** link hygiene (revocable + purpose-scoped; expiry 30d share-link / 14d-or-on-resolve review grant).
- **Amends scope of:** **DL-048** (paid-tier limits move from TBD → constituent E; token budgets unchanged and reaffirmed as a *cost* control).
- **Extends:** **DL-049** (Principal/reviewer; token grant is the authentication) · **DL-055** (Share For Review as a collaboration affordance) · **DL-062** (CAF dimensions; Alignment receives attested third-party evidence).
- **Preserves unchanged:** all epistemic invariants; **D115/CRR bounds** (evidence-not-truth, no autonomous acceptance, OSLO never self-accepts, issues close only via an analysis update); **DL-096** append-only History (now explicitly protected from metering).
- **Realization:** `10_product/scope/*` (tier boundary), `20_handoff/*` (CRR/collaboration contracts), engineering (billing infrastructure — out of R1 prototype scope).

## Recommendation

**Adopt as a single package.** The constituents are interdependent: **B alone resolves A's conflict with CHG-061**, and **E exists only because of the tier-live-in-Alpha premise**. Ratifying a subset risks adopting a rule whose safeguard was left behind.

Recommended alongside adoption:
- Record the two **metering principles** (never meter the epistemic record; never sell safety) as **durable constraints**, not slice-local decisions — they are the kind of rule that erodes by increments.
- Record the governing principle verbatim: **"Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit."**
- Open backlog items for the residues: **Basic price**, **Extended-Analysis budget numbers**, **Suggest-alternative alignment signal**, and **whether revenue ever expands onboarding capacity** (which would reopen pay-to-skip).

## Status

**Draft — awaiting owner ratification.** Nothing herein is canon. AI authored this as scribe and **may not ratify, reject, supersede, or adopt** (`CLAUDE.md` Authority Constraint). On ratification: assign the number at landing (`python3 tools/dl_records.py next`), regenerate the records index, land via branch → PR → green doc-integrity gate → owner merge.

## Provenance

Owner working session 2026-07-10 (R1 product-grill, Slice 9). Evidence base: `OSLO_CAPABILITY_MATRIX_V2` (CRR-01…05, MRI-07, OVL-03, REC-05, MON-01, gaps #337/#339) · `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001` (P0/P2/F1/F4/F8, CHG-061/062) · `RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1` §147 (CRR guardrails: evidence-not-truth; no autonomous acceptance) · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1` (M3/M4) · DL-021, DL-048, DL-049, DL-055, DL-062, DL-096.
