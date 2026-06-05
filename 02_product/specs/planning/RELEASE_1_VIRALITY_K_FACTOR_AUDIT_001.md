# Release 1 — Virality / K-Factor Audit 001

**Document Type:** Owner-directed growth audit (Framework 001A Review schema) · **Status:** **Findings recorded — optimizations route to owner; nothing redefined.** · **Date:** 2026-06-05
**Question (owner-directed):** *Audit Release 1 for virality; suggest optimizations to maximize k-factor.*
**Frame:** **k = i × c**, where **i** = invitations/exposures generated per active user and **c** = the share→signup conversion rate of those exposures; **cycle time T** governs how fast k compounds. Self-sustaining growth needs **k > 1**; even k < 1 materially lowers blended CAC.
**Sources:** `OSLO_CAPABILITY_MATRIX_V2.md` (CRR-01…05, SHARE-01…05, COLLAB-01…03, REC-02/05, OVL-03, TEL-02/05/06, MON-01, gaps #337/#339) · `12_freemium_tier_behavior_logic.md` · DL-048/CHG-056-059 (tiering) · `FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001`.

---

## 0. Verdict

**OSLO's structural virality is unusually strong — but the conversion side of the loop is undefined, which caps k near zero today.** Uniquely, OSLO's **core value action is also its viral action**: a CAF Review Request (CRR) invites a stakeholder *because the user needs their input*, and the stakeholder's response becomes evidence that improves the user's understanding (CRR-04 → Deep Pass). Virality isn't bolted on; it **is** the workflow. Two loops are designed in — **CRR (active)** and **MRI share links (passive)** — and **TEL-06 already instruments them.** The blocker is that the **external-stakeholder experience (the conversion moment) is unspecified** (matrix gap #337), so invitations are generated but have **no defined path to become users.** Fixing the recipient side is the single highest-leverage move; everything else amplifies it.

## 1. The loops R1 already has

| Loop | Surface | Role | k-lever |
|---|---|---|---|
| **Active** | **CRR-01 "Share For Review"** (→ package → response → Deep Pass) | invite a stakeholder for input | **i + c** (high-context exposure) |
| **Passive** | **SHARE-02 MRI links** (public/private) | spread understanding | **i** |
| **Portable** | **SHARE-04 PDF export** (free-tier's only export) | artifact travels outside the app | **i** |
| **In-context** | **COLLAB-01/03 comments + @-mentions**, **OVL-03 / REC-02 "Share For Review"** | pull people into a finding | **i** |
| **Instrumentation** | **TEL-06 Virality Telemetry** (shared / invited / joined / returned / converted) + TEL-02 (invited/accepted/activated) | measure the loop | enables k computation |

## 2. Findings

**F1 — (CRITICAL) The external-stakeholder / recipient experience is undefined → c ≈ 0.** Matrix gap #337: "no Stakeholder/Reviewer object distinct from User, and no external-auth model." A CRR or shared MRI generates an *invitation*, but **what the recipient lands in — and how they become a user — is unspecified.** If the recipient hits a signup wall before value, c collapses; if there's no convert-moment after value, c is left to chance. **This is the binding constraint on k.**

**F2 — No defined convert-moment for recipients.** Even where a stakeholder reviews a finding or views an MRI, there is **no specified "create your own project" moment** at the point of realized value (post-review / post-view). The highest-intent instant in the loop is unowned.

**F3 — Shared artifacts are not specified as viral surfaces.** PDF export (the free tier's *only* output) and shared MRI links have **no specified attribution/CTA** ("Made with OSLO — see your project's understanding"). The cheapest i×c lever — every exported artifact carrying a tasteful invitation — is unclaimed.

**F4 — Free-tier availability of the viral primitives is ambiguous.** MON-01 lists "Sharing, Comments" on Free but **not CRR explicitly**, and the freemium constraints gate "team collaboration depth." If the **active loop (CRR) is gated off Free**, the largest user base can't drive the strongest loop. Virality must seed on Free; monetize *depth*, not the *seed*.

**F5 — No share/invite prompt timing.** Like the upgrade-prompt gap (audit 001), sharing is a capability with **no defined trigger** — nothing prompts "invite a reviewer / share this MRI" at the **value moments** (strong MRI produced, finding resolved, confidence raised) that maximize i. Left to user initiative alone, i underperforms.

**F6 — No referral/incentive loop.** There is **no mechanic that rewards inviting** (e.g. invite a reviewer who joins → a bounded capacity bump). A cost-aware referral reward is a direct i+c multiplier and is currently absent.

**F7 — k-factor is measurable but not a tracked objective.** TEL-06 captures the events, but **no spec computes k (or cycle time) per loop, or sets a target.** Without the objective function, optimization is blind (same shape as the upgrade-prompt optimality gap).

**F8 — Trust hygiene gates spread (gap #339).** Share-link expiry/revocation/scoping is unspecified; recipients and inviters spread links more freely when the trust/safety model is clear.

## 3. Concerns (value-alignment guardrails — non-negotiable)

OSLO's **credibility is its growth engine**: people share honest, high-trust understanding, and recipients convert because the output is manifestly valuable. Growth tactics that erode that trust are net-negative. Therefore:

- **No autonomous invites/sends** — OSLO never acts autonomously; every invitation is **user-initiated** (preserves the core invariant).
- **No dark patterns** — no forced-invite-to-proceed walls, no misleading attribution. Share/referral prompts follow the **same honesty rules as upgrade prompts** (value-based, no "wallpaper").
- **Referral rewards bounded by unit economics** — any incentive is **tier-keyed, capped, and gaming-resistant** (reuse the DL-048 budget + the Internal-style abuse guards); a viral reward must not open a cost hole.
- **Recipient AI cost is governed** — a stakeholder viewing/responding must not trigger uncapped recompute; fold recipient-driven cost under the cost governance.

## 4. Dependencies
- **External Stakeholder/Reviewer model** (gap #337) — the foundation for F1/F2; an architecture/identity scoping item.
- **DL-048 cost governance** — bounds referral rewards (F6) and recipient-driven recompute.
- **FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001** — the share/invite prompt timing (F5) reuses its two-class trigger + timing-config pattern.
- **TEL-06 / TEL-02 / TEL-05** — the measurement substrate for F7.
- **Wave A Perceive (CRR-04 intake)** — recipient responses already enter as evidence; the conversion overlay must not disturb that contracted seam.

## 5. Recommendation — prioritized k-factor optimizations (owner-routed; nothing redefined)

**P0 — Define the external-stakeholder experience (unblocks c; resolves F1/F2).** A **low-friction, no-account-required (or one-tap) review/view** for invited recipients, with a **natural "create your own project" convert-moment at realized value** (after they review a finding or explore a shared MRI). This is the single highest-leverage change; route to a dedicated scoping item (it's also a real architecture gap, #337).

**P1 — Make every shared artifact a viral surface (F3).** Specify tasteful attribution + CTA on **PDF exports and shared MRI links** ("Made with OSLO — map your own project's understanding"). Cheapest i×c lever; pure presentation; no cognition touched.

**P2 — Guarantee the viral primitives on Free (F4).** Confirm **CRR (at least limited), MRI share links, PDF export, comments** are **Free-tier** capabilities. Gate collaboration *depth* and *capacity* for monetization; never gate the *seed* of the loop. (Ties to the tier config — a Calibration row clarification.)

**P3 — Time the share/invite prompts at value moments (F5).** Reuse the upgrade-prompt **two-class trigger** pattern: at a **value peak** (strong MRI delivered, finding resolved, confidence raised) surface "**invite a stakeholder to strengthen this finding**" / "share this MRI." User-initiated, value-framed, cooldown-governed (Calibration §4d-style).

**P4 — Lean into the value=virality identity (compounding).** Make "**invite a stakeholder**" a **primary CTA on findings/validation recs** (REC-05 are already "prime CRR candidates"), framed as *strengthening understanding* — because CRR-04 turns the invite into evidence, each invitation **both grows the network and improves the inviter's outcome.** This is OSLO's structural edge; foreground it.

**P5 — Add a bounded, cost-aware referral reward (F6).** "Invite a reviewer/teammate who joins → a **capped** capacity bump (extra fixes / temporary envelope)." **Tier-keyed, unit-economics-bounded, abuse-guarded.** Direct i+c multiplier; optional / fast-follow.

**P6 — Make k a tracked objective (F7).** Compute **k and cycle-time per loop** (CRR vs MRI-share vs PDF) from TEL-06/02, with a target and a dashboard — so P0–P5 are tuned on data, not intuition (mirrors the upgrade-prompt optimality objective).

**P7 — Share-link hygiene (F8).** Specify expiry/revocation/scoping so links spread safely.

## 6. Owner decision required
- [ ] Approve **P0 (external-stakeholder experience)** as the priority — and whether it is **R1 scope** or fast-follow (it's also architecture gap #337).
- [ ] Approve **P1 (artifact attribution/CTA)** and **P2 (viral primitives guaranteed on Free)**.
- [ ] Approve **P3 (share-prompt timing)** reusing the upgrade-prompt pattern.
- [ ] Decide **P5 (referral reward)** in/out for R1 (cost-bounded) vs fast-follow.
- [ ] Approve **P6 (k as a tracked metric + target)**.
- [ ] Confirm the **value-alignment guardrails (§3)** as binding on all growth work.
- [ ] On approval: route P0 to an external-reviewer scoping item; the rest are commodity (SHARE/COLLAB/MON/TEL) + reuse of existing patterns; record via changelog.

## 7. Status
**FINDINGS RECORDED — strong structural virality; one CRITICAL conversion-path gap (F1, = architecture gap #337), several amplifiers, value-alignment guardrails attached.** No spec edited; routes to owner.

---
*This owner-directed audit finds that Release 1 has unusually strong **structural** virality — its core value action (CAF Review Requests) is also its viral action, with an active loop (CRR), a passive loop (MRI share links), portable PDF exports, in-context @-mentions, and TEL-06 virality telemetry all present — but that the **conversion side of the loop is undefined** (no external-stakeholder/reviewer experience or convert-moment, matrix gap #337), which caps k near zero regardless of how many invitations are generated. It decomposes k = invites × conversion, maps each R1 surface, and recommends a prioritized set of optimizations led by P0 (define the low-friction external-stakeholder experience + a realized-value convert-moment), then artifact attribution/CTA, guaranteeing the viral primitives on Free, value-moment share-prompt timing (reusing the upgrade-prompt pattern), foregrounding the invite-as-evidence value=virality identity, a bounded cost-aware referral reward, k as a tracked objective, and share-link hygiene — all bound by non-negotiable value-alignment guardrails (no autonomous sends, no dark patterns, referral rewards bounded by unit economics, recipient cost governed) because OSLO's epistemic credibility is itself the growth engine. Nothing is redefined; choices route to the owner.*

**Release 1 Virality / K-Factor Audit 001 complete. Pending Owner Direction.**
