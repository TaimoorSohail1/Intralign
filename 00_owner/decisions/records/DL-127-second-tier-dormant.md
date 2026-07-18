# DL-127 — Second-tier upsell motion dormant until billing is live

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Second-tier upsell motion is dormant until billing is live — the limit moment measures intent instead

**Class:** B (scope / monetization) · **Framework 001** — AI drafts + builds; **owner ratifies at land.** · **Amends D123.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-17 · **Build:** `slice-10-tiering-limits/prototype.html`.

---

## Decision

While no paid tier has a live purchase path (the billing rail is `UNSET` — T-4), OSLO does not push an upsell at Free users. The **upsell MOTION is dormant**, gated on one switch (`SECOND_TIER_LIVE`, currently **false**):

1. **The limit moment MEASURES willingness instead of selling.** When a Free user hits a real cap, the honest disclosure and the **free resolution still lead** (D170 preserved), but the paid resolution — the "Upgrade to Basic — $12/mo" button that cannot complete a purchase — becomes an honest **intent probe**: **"I'd upgrade for this."** Clicking records a demand event (which limit, tier, timestamp) and confirms truthfully that nothing was purchased, the tier isn't on sale, and it is not a paid waitlist. This captures **willingness-to-upgrade at the exact instant the ceiling is felt** — intent-clicks over prompt-impressions, per limit — so we learn which limits drive upgrade intent before a tier exists to sell (the fake-door / demand-signal pattern; the D121 "simulated, and it says so" precedent).

2. **The proactive value-moment upsell (UP-7) is retired here.** It pitched a tier that can't be bought, *and* its "Your confidence just improved" framing celebrated the confidence **band** rising — the one move the earned-recognition layer is built never to make (a rise celebrated turns a fall into a failure — D187/D173c). Recognition now carries the "good moment" honestly (on grounding / stage, never the band), so UP-7 has no job while dormant.

3. **The Plans page tells one consistent story.** Basic joins the forward ladder — shown, priced, **not purchasable** (exactly as Pro/Team already are) — and its card carries the same "I'd upgrade for this" intent probe. No surface offers to buy Basic while another says it isn't available.

## What this amends, and what it keeps (D123)

D123 ratified two things: **(a) tier gating is LIVE in Alpha — the Free boundary is real and enforced;** and **(b) Basic is purchasable in Alpha.** This decision **keeps (a)** — Free's caps still bind, and hitting one still discloses honestly — and **amends (b)**: the paid tier is **not purchasable until a billing rail exists**; until then the limit moment measures upgrade intent. Since every upgrade in the build was already *simulated* (no billing rail, T-4), this aligns the product's behavior with its actual capability rather than changing a real purchase flow.

## The switch — the motion returns in one flip

`SECOND_TIER_LIVE = true` restores the full motion everywhere with no other change: limit prompts sell again (the live "Upgrade to Basic — $12/mo" resolution returns), the Plans card's real upgrade button returns, and UP-7 fires again (as a **capability** pitch — never band-tied; that guardrail is permanent). To preview the Basic tier while dormant, flip the switch.

## Guardrails (executable — `_assertNoPurchaseCtaWhileTierDormant`)

- While dormant: **no purchase CTA** is pushed at the user (the limit-prompt paid resolution is the intent probe, not a "$price" buy); the intent probe **records demand** and is **honestly labelled** (says the tier isn't on sale, nothing is purchased, not a paid waitlist).
- The honest **disclosure + FREE resolution still lead** on every limit prompt (D170).
- **UP-7 does not arm** while dormant.
- The live purchase branch is **retained behind the switch**, so the guard proves the motion **returns** when it flips.
- MON-04 preserved: the disclosure still names the specific limit and the tier (`_assertNoGenericUpgradeCopy` green).
- D183a preserved: "I'd upgrade for this" is the **user's** voice, declared `data-voice="user"`.

## Governance

Lands as canon via `dl-land`, amending D123. Built + verified in the deliverable prototype (boot self-check **147/147**, 0 pageerrors; new guard `noPurchaseWhileTierDormant` green; `mon04` / `d183OsloVoice` still green). AI drafted + built; **only the owner ratifies.**
