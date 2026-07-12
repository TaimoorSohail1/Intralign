# OSLO — Controlled Release & Demand Framework (Alpha / Beta)
Owner-directed, 2026-07-10. Status: **recommendation — requires owner ratification via Framework 001.**
Governs: reviewer (third-party) access, invite supply, waitlist, and the phase ramp to GA.

---

## 1. The problem this solves

Two constraints collided in Slice 9:

- **Canon (D021 / canonical-truth):** Alpha and Beta are **invite-only — users are never anonymous.** GA is the first phase permitting anonymous access.
- **Canon (CRR-01…05, DL-049):** the product's core value action *is* its viral action — you invite a stakeholder **because you need their evidence**, and their response improves your understanding.

The Virality audit's P0 recommended a **no-account-required** reviewer view. That is, on its face, an anonymous product interaction in a phase that forbids them. The worker escalated it rather than resolving it. Correct call.

**The resolution:** a review-request link carries a **token that grants Reviewer Principal access** (DL-049: single `Principal`, `type: reviewer | user`, in-place promotion). **The invite IS the authentication.** A gated reviewer is *identified and invited* — never anonymous. Zero-friction and invite-only are not in conflict once we stop conflating "no password" with "no identity."

This preserves the loop *and* the constraint. It is also the mechanism that makes supply controllable.

---

## 2. Strategic principle

**Scarcity is a supply lever, not a growth hack.**

Superhuman, Gmail (2004), Arc, Raycast, Clubhouse: the waitlist did not *create* demand — it **metered** demand for something people already wanted, and converted the wait into signal, status, and word-of-mouth.

The honest version of the lesson, which we should hold to:

> **Scarcity amplifies desire; it cannot manufacture it.** Superhuman's waitlist worked because it was paired with an exceptional product and concierge onboarding. If the underlying read isn't compelling, a waitlist doesn't create outsized demand — it just hides a weak funnel behind a velvet rope, and delays the feedback that would have told us so.

So the framework below is built to **generate demand *and* keep the truth-telling instrumentation on**, so we can tell the difference.

---

## 3. The crux: bound *seats*, never bound *evidence*

This is the single most important design rule, and it's where a naive "limit shares" policy would do real damage.

| | What it is | Bounded? |
|---|---|---|
| **Granting a new principal access** | A new human enters OSLO (collaborator seat, or first-time reviewer) | **YES — this is supply. Meter it.** |
| **Seeking evidence from someone already in** | Sending a review request to an existing principal | **NO — never bounded. Free, forever.** |

**Why:** a review request is not a marketing share. It is how the user *gets their answer*. Every review request you block is a user whose understanding you deliberately degraded. Bounding new-principal grants controls supply; bounding evidence-seeking sabotages the product.

Practical rule: **an invite is spent only when a *new* human is admitted.** Re-asking a known reviewer costs nothing, forever. This makes the invite feel like what it is — a key to the building, not a tax on doing your job.

---

## 4. Mechanics

**1 — Bounded, replenishing invite allocation.**
Each Alpha/Beta user holds **{N} invites per {period}**, replenishing (Gmail/Superhuman model). Spent on: admitting a **collaborator** (full seat), or admitting a **first-time reviewer**. Balance and replenish date are always visible — real numbers, never theatrical.
*Recommended (not ratified): reviewer grants cost less than collaborator seats, or nothing at all — see §3.*

**2 — Waitlist with earned position.**
Anyone not admitted lands on a waitlist showing a **real position**. Position improves through genuine demand signal:
- **Referrals that convert** (the classic lever).
- **Being review-requested by an existing user** — an inbound demand signal, and the strongest one we have: someone with a real plan needs *this specific person's* input. That should jump the queue.
- Role/org fit (we are selling to project leaders).

**3 — Skip-the-line.** A user may spend an invite to pull someone off the waitlist immediately. This is the status good — the thing users brag about.

**4 — Reviewer access = a scoped grant, not an account.** The token grants access to **exactly that review package** — nothing else in the project. (Also satisfies the D117 / gap-#339 hygiene requirement: scoped + revocable.)

**5 — The convert-moment becomes the waitlist, not a signup.**
After a reviewer responds — *only after they've delivered value and seen OSLO work* — they are offered a **place on the waitlist** (with position), not an instant account. The inviter can grant them a seat directly from their allocation. **This is the demand engine:** every review request is a qualified, high-context prospect who has already experienced the product doing real work.

**6 — Phase ramp with an explicit sunset.**

| Phase | Reviewer access | Invite supply | Waitlist |
|---|---|---|---|
| **Alpha** | Gated — token grant only | Tight | Long; hand-curated admits |
| **Beta** | Gated — token grant | Loosening | Active; faster admits |
| **GA** | **Open** (anonymous permitted — D021/D024) | Retired → **tier-based** limits (freemium) | **Retired** |

The scarcity mechanism is **phase-scoped and self-terminating.** It is not the permanent business model.

**7 — Instrument it or don't do it.**
Track waitlist size + velocity, invite utilization, **review-request → admit conversion**, and **k per loop** (TEL-06 already instruments CRR vs MRI-share vs PDF). Throttling supply without measuring demand is just throttling growth. If waitlist velocity is flat, scarcity is not the constraint — **the product is** — and we need to know that fast, not late.

---

## 5. Guardrails (non-negotiable)

OSLO's growth engine **is its epistemic credibility.** A product whose whole claim is "we tell you the truth about your plan, including what we don't know" cannot lie in its growth surfaces. That would be self-refuting.

- **No fabricated scarcity.** No "3 spots left!" unless there are exactly 3. Real counts or no counts.
- **No dark patterns** (canonical — Virality audit value-alignment guardrails).
- **The waitlist says plainly what it is**, including that it exists because we're deliberately limiting access during Alpha.
- **Never bound evidence-seeking** (§3).
- **Reviewers are never spammed.** A review request is invited work, not a marketing email.

---

## 6. Canon tension — escalated, requires a Framework 001 proposal

**CHG-061 / Virality audit P2 (applied):** *"Guarantee the viral primitives on Free… never gate the seed of the loop."*

> ⚠️ **Revised 2026-07-10 (D123).** My earlier reconciliation — *"CHG-061 is a GA-phase **tier** rule; controlled release is an Alpha/Beta **phase** rule that sunsets at GA, so both hold"* — **is dead.** The owner has confirmed **Basic tier is purchasable during Alpha**, so the tier rule **does not wait for GA**. The two axes are now live simultaneously.

**The resolution now rests entirely on CR-2.** If **reviewer grants are free and unmetered** (§3, D120), then the **seed of the loop — CRR evidence-seeking — is not gated in any phase or on any tier.** Only **seats** are metered. CHG-061 then holds **literally**, not by argument.

**This makes CR-2 = free load-bearing, not a preference.** If reviewer grants were ever made to consume the allocation, OSLO would be gating the seed of its own loop, in direct conflict with applied canon — *and* breaking D120. Still requires a Framework 001 proposal to ratify. Flagged, not assumed.

**The two axes must never be conflated in the UI.** A user may be blocked by **phase** (no seat available) or by **tier** (Free can't do that) — the product must always say **which**. Presenting a supply constraint as an upsell would manufacture a purchase out of scarcity: a dark pattern, and disqualified by §5.

---

## 7. Open — owner decision required (DO NOT ASSUME)

| # | Item |
|---|---|
| CR-1 | **{N} invites per user, per {period}** — and the period length. |
| CR-2 | Does admitting a **first-time reviewer** consume an invite, or are reviewer grants free/cheaper? (*Recommend: free or cheap — see §3.*) |
| CR-3 | **Waitlist admit rate** and curation policy (hand-picked vs automatic). |
| CR-4 | **Referral weighting** — how much a converted referral moves position. |
| CR-5 | Does an inbound **review request** move the requested person up the queue? (*Recommend: yes — strongest demand signal we have.*) |
| CR-6 | Share-link **expiry** (gap #339, still unspecified). |
| CR-7 | Is the reviewer **convert-moment** in R1, or a fast-follow? |
