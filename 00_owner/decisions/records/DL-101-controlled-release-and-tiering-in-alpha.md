# DL-101 — Controlled Release & Tiering-in-Alpha (reconciles CHG-061; amends DL-048 scope, extends DL-049/DL-055/DL-062)

- **Date:** 2026-07-10 · **Status:** Draft — awaiting owner ratification · **Decided by:** — (owner; not yet ratified)
- **Class:** A

- **Source:** Owner direction (working session 2026-07-10, R1 product-grill of Slice 9). Proposal: `../PROPOSAL_CONTROLLED_RELEASE_AND_TIERING_IN_ALPHA_DRAFT.md`. Recorded by AI contributor as scribe (**non-ratifying** — the owner ratifies, per `CLAUDE.md` Authority Constraint).
- **Layer:** Product scope / monetization + collaboration seam (`10_product`, `20_handoff`). **Non-doctrinal.** No epistemic invariant is amended; the D115/CRR bounds are tightened, never loosened.
- **Numbering note:** Numbered at landing per DL-065 (`tools/dl_records.py next` → **DL-101**; DL-099/DL-100 were taken by the reliability-qualifier work while this branch was out). Status remains **Draft** — **the owner ratifies by setting Status to Ratified and merging.** AI may not ratify (`CLAUDE.md` Authority Constraint).

## Decision

Adopt as a **single package** (constituents are interdependent; B is the sole resolution of A's conflict, and E exists only because of B's premise):

**A. Reviewer identity — the invite IS the authentication.** A review-request link carries a token granting **Reviewer Principal** access (DL-049), **scoped to that review package only**. The reviewer is *identified and invited* — **never anonymous** — satisfying DL-021 with no signup wall and without breaking the CRR loop. Resolves matrix gap #337 residue.

**B. Bound seats; never bound evidence. (Load-bearing.)** An invite is consumed **only when a NEW principal is admitted**. **Review requests are never metered for monetization** — on any tier, in any phase. Reviewer grants are **free and unmetered**. **This is the sole resolution of the CHG-061 conflict:** with reviewer grants free, the *seed* of the loop is ungated on every tier and in every phase; only **seats** are metered, so CHG-061 holds literally.

**B-1. The CRR cost ceiling — clarifies the one apparent conflict with `12_freemium_tier_behavior_logic.md`.** Canon states CRR is *"available on Free with a **bounded daily/active CRR cap** (cost-governed under DL-048)… **gate CRR depth/volume, not its existence**."* An earlier draft of this record said review requests are *"never metered,"* full stop — which reads as contradicting that cap. **Reconciliation:** the CRR bound is a **cost ceiling** (each response triggers an Extended Analysis → real tokens → DL-048), **not a monetization gate.** It therefore:
- is set **above realistic working volume**, so it does not bind a genuine user doing genuine work;
- **never fires an Upgrade Prompt** — no UP-* trigger may key off the CRR cap, because selling an upgrade at the moment a user is trying to *get an answer* is precisely the failure this decision exists to prevent;
- exists to bound **cost and abuse**, and is documented as such wherever it is surfaced.
So construed, canon's "gate depth/volume, not existence" and this decision's "never meter who gets an answer" **both hold**. Any future use of the CRR cap as an upsell lever is a **supersession** of this decision, not a tuning change.

**C. Controlled release + waitlist, with an explicit sunset.** Bounded, replenishing allocation (**Basic 5/mo · Free 2/mo**, calendar-month, non-cumulative; Free non-zero — virality must seed on Free). Waitlist with a **real, earned** position (converted referrals; **being review-requested** = strongest inbound signal; role/org fit). **No points economy.** Skip-the-line by spending an invite. Reviewer **convert-moment = the waitlist**, offered **only after they respond**. **Ramp:** Alpha (tight) → Beta (loosening) → **GA (open; anonymous permitted per DL-021; waitlist retired; limits become tier-based)** — the mechanism is **phase-scoped and self-terminating**. **Pay-to-skip is PROHIBITED in Alpha:** the queue is throttled by onboarding capacity, and **payment does not create capacity**, so selling passage past it is a toll booth on an invented constraint.

**D. Two limits, never conflated.** **PHASE** (supply) and **TIER** (depth) are orthogonal and both live in Alpha. The product must **always name which limit blocked the user**. Presenting a supply constraint as an upsell is a **prohibited dark pattern**.

**E. Tier boundary (unblocks DL-048 "paid-tier limits TBD").** **Free fully delivers the core read** (intake → Fast Pass → Overview → Attention → Issues → **CRR**). **Basic sells depth and volume.**
**Per-tier values — canon is authoritative where it speaks:**
- **Projects: Free 1 · Basic 3** — per **UP-3** (`12_freemium_tier_behavior_logic.md`), which is ratified. *(An earlier draft of this record proposed Basic = 10; it contradicted UP-3 and is **withdrawn** — see Corrections of record #3.)*
- **Daily fixes: Free 5 · Basic 20** (UP-1) · **Daily chat: Free 20** (UP-2) · **Deep runs/day: Free 2** (UP-5) — all ratified; adopted unchanged.
- **Export: Free = PDF only** (SHARE-04, MON-01).
- **Collaborator seats: Free 3 · Basic 10; Viewers unlimited** — **proposed into a genuine gap** (see Condition 7): the "Release 1 Tier Definitions" document that 18 canonical documents defer to for seat limits **does not exist**. These values are a recommendation, not a reading of canon, and are **superseded the moment Tier Definitions is written.**
- **Extended Analysis budget:** shape ratified (Free small / Basic generous); **numbers owner-open.**

**E-1. Limit-reached interaction rule (adopted from Seam Audit 001 — applies to EVERY cap in this decision, including seats).** A limit-bearing affordance **stays enabled**; the *attempt* is gated and surfaces the matching value-framed prompt **with resolutions** (e.g. "upgrade **or** archive the current project"). **Never disabled, never hidden** — disabling suppresses the highest-intent moment — and **never a raw error.**

**E-2. Seat limits become ENFORCED, overriding visibility-first (stated, not smuggled).** `INVITE_AND_SHARE_MODAL_EXPERIENCE_SPECIFICATION_V1` §N specifies seat limits as **"visibility-first… no billing/entitlement implementation."** Because **Basic is purchasable during Alpha**, tier limits are live and seats are **enforced** (subject to E-1 and to "no eviction on downgrade"). This **amends** that specification's visibility-first seat rule. No other part of that specification changes.
Two **durable metering constraints** (not slice-local):
- **Meter only what costs money or defines scope. NEVER meter the epistemic record.** Artifacts **never capped**; History **never expires or truncates** (DL-096). The append-only trace of how understanding evolved *is* the product's core promise.
- **Never sell safety.** Link revocation + purpose-scoped expiry are trust hygiene **for every tier**.
**No eviction on downgrade:** an over-cap account cannot *add* a Collaborator; **no human is ever removed** to enforce a billing change.

**F. A Reject moves CAF, via Alignment (extends DL-062).** A stakeholder **Reject** is **evidence about Alignment** — a first-class CAF dimension — and may move Alignment and Reliability through a normal Extended Analysis run. **An Approve is equally Alignment evidence; neither direction is privileged.**

**Governing principle (canonical statement):**
> **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

## Rationale

OSLO's **core value action is also its viral action** (Virality audit): a CAF Review Request invites a stakeholder *because the user needs their evidence*. Metering a review request therefore degrades the user's understanding **by design** — it is not a marketing share, it is how the user gets their answer. Constituent B protects the product mechanism and the growth mechanism with one rule, and is simultaneously the only honest reconciliation with CHG-061 now that Basic is purchasable in Alpha (which killed the earlier "tier rule sunsets past phase rule" argument).

Constituent F closes a genuine epistemic hole: refusing to let a Reject touch CAF would mean OSLO watched a sponsor reject a finding and learned nothing about **alignment** — the dimension the event speaks to.

## Conditions

1. **D115 / CRR bounds preserved absolutely.** Every reviewer response is **evidence, not truth** — a **third-party attestation** ("Attested by \<name\>"), never OSLO's own read; it **never auto-resolves and never auto-re-opens** an issue; **OSLO never self-accepts**. Issues close only via an analysis update.
2. **Constituent B is non-erodable.** Any future change that meters review requests to existing principals, or charges for reviewer grants, **re-breaks CHG-061** and must be treated as a supersession of this decision — not a tuning change.
3. **The epistemic record is never metered.** No tier may cap artifacts or expire/truncate History (DL-096). No tier may gate link security.
4. **Numbers are instrumented hypotheses.** 3 / 10 / 1-project / 5 / 2 / 14-day are judgments chosen to be *easy to loosen, painful to tighten*. They must be instrumented (waitlist velocity, invite utilization, review-request→admit conversion, k per loop — TEL-06) and revisited against alpha behaviour. **Waitlist growth must not be read as product validation** — scarcity amplifies desire but cannot manufacture it.
5. **No fabricated scarcity, no dark patterns.** Real counts only; unset values render unset. OSLO's growth engine *is* its epistemic credibility — the growth surfaces cannot lie.
6. **Owner-open residues (DO NOT ASSUME):** **Basic price** · **Extended-Analysis budget numbers** · **whether a *Suggest alternative* response carries Alignment signal** (counting it as a partial Reject with no symmetric partial Approve would introduce a **negative bias** — deliberately unbuilt) · **whether revenue ever expands onboarding capacity** (would reopen pay-to-skip).

7. **BLOCKING GAP — "Release 1 Tier Definitions" does not exist.** **18 canonical documents** defer to a document titled *"Release 1 Tier Definitions"* as authoritative for tier, seat, and sharing limits (e.g. `INVITE_AND_SHARE_MODAL_EXPERIENCE_SPECIFICATION_V1` §N: *"Collaborator/seat limits per Release 1 Tier Definitions"*). **No such document exists in the repository.** The tier layer therefore rests on a citation to a hole. Per the Anti-Assumption Build Protocol this is **escalated, not filled**: the seat values in constituent E are an explicit **recommendation into the gap**, and are **superseded on sight** by a written Tier Definitions. **Recommendation: commission `RELEASE_1_TIER_DEFINITIONS_V1` as a blocking prerequisite for shipping Basic in Alpha**, consolidating every per-tier number now scattered across MON-01…04, the UP-* taxonomy, and this decision.

## Supersedes / Amends

- **Amends scope of DL-048** — "paid-tier limits TBD" → constituent E. Token budgets unchanged; reaffirmed as a **cost** control, never a monetization gate.
- **Extends DL-049** (Principal/reviewer — the token grant is the authentication), **DL-055** (Share For Review as a collaboration affordance), **DL-062** (CAF dimensions — Alignment receives attested third-party evidence).
- **Resolves** the CHG-061 / Virality-audit-P2 conflict (via B); gap **#337** residue (via A); gap **#339** link hygiene.
- **Preserves unchanged:** all epistemic invariants; D115/CRR bounds; **DL-096** append-only History (now explicitly protected from metering); DL-021 (invite-only Alpha/Beta — satisfied, not amended).

## Corrections of record

1. **"CRR is a genuine spec gap; defer it" — FALSE.** CRR-01…05 are Alpha-scope, High-priority canon (exit criterion C14), and **DL-049 had already resolved gap #337**. The escalation was an over-escalation and is withdrawn.
2. **"CHG-061 is a GA-phase tier rule that sunsets past the Alpha phase rule" — DEAD** once Basic is purchasable in Alpha. The reconciliation rests solely on constituent B.

3. **"Basic = 10 projects" — WITHDRAWN.** An earlier draft of this record carried Basic = 10 active projects. **Canon already ratifies Basic = 3** (UP-3, `12_freemium_tier_behavior_logic.md`). The number was recommended by the AI contributor **without first checking the upgrade-prompt taxonomy** — an Anti-Assumption failure — and was ratified by the owner on that advice. **Canon prevails: Basic = 3.** Recorded here rather than silently corrected, so the failure mode is inspectable.

4. **"Review requests are never metered" (unqualified) — REFINED to B-1.** Stated flatly, it contradicted canon's cost-governed CRR cap. The rule is: **never metered *for monetization*; bounded only by a cost ceiling that never fires an Upgrade Prompt.**
