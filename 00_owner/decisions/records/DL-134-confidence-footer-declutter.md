# DL-134 — Confidence-panel footer declutter — one Why, trend-as-Timeline, no Steady

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Confidence-panel footer declutter — one "Why", trend-as-Timeline, no "Steady"

**Class:** B (experience-doctrine refinement — the confidence card footer) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Refines** D062 (the Overview's Attention pointer), DL-096 / Fix 2 (Why paired with Timeline), and D056 (direction + cause). **Upholds** D051 (reliability basis reachable via "Why").

---

## Decision

The confidence card's footer carried four things where one was load-bearing. It is decluttered to what the read actually needs, in three moves.

1. **"Attention map →" is removed from the footer.** The Attention map is co-primary and always reachable from the **left nav**; a second in-panel pointer duplicated it. D062's intent — the map is reachable from the Overview — is met by the ever-present nav. (Together with the earlier removal of the Start-here overflow pointer, the Attention map now has **one** Overview home: the nav.)
2. **"Timeline →" is removed; the trend chip becomes the Timeline door.** The History/timeline surface is also the "History" nav item, so the standalone link was redundant. The episodic **trend chip** — which is *about* how the read moved over time — is now itself clickable and routes to History (`openHistorySeam`). One affordance, in the place trend belongs, instead of a chip plus a separate link.
3. **The trend chip shows only when the read moved; "Steady" is hidden.** A held read is the absence of news, so the chip appears only when the read actually moved (Strengthened / Softened) — `renderHero` shows it when `_directionIsComputable() && _readDirection() !== 0`. Direction + cause is preserved (D056) for the cases that carry news; the no-movement case simply says nothing.

What remains in the footer is the one link that does unique work: **"Why ▾"**, which opens this read's reasons and — crucially — the **reliability basis** (D051). That stays untouched.

## Why — the constraint that shaped it

Every item questioned here was reachable elsewhere or was non-news, but two were held by build guards, so the declutter is a **deliberate refinement, not a silent deletion**. The limiter line was explicitly **kept** (it carries the next-action verb and the "read never stands bare" duty, D002/D051/D186c) — only genuinely duplicated navigation and genuinely absent news were removed. The test applied throughout: an affordance stays only if it does work no other surface on the Overview already does.

## Guardrails (executable)

- **The trend is shown iff the read moved** — computable **and** direction ≠ 0; "Steady" is legitimately hidden. The direction guard is **amended** to grade `shown ⇔ (computable && direction ≠ 0)` (was `shown ⇔ computable`). → `_assertConfidenceCafCoupled()` (amended).
- **The trend chip is an action** — it is registered interactive (`HERO_INTERACTIVE_CLASSES`), so its brand-orange focus ring is graded as a link, not as state wearing an amber-adjacent orange (D179d). → `_assertHeroCardCarriesNoSeverityColour()` / `_assertBrandOrangeIsActionsOnly()` (both green).
- **"Why" still surfaces the reliability basis** (D051) — the one footer link is untouched.
- **Direction still carries its cause when shown** (D056) — unchanged for Strengthened/Softened.

## Governance

Lands as Class-B canon via `dl-land`, refining D062, DL-096, and D056. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; footer verified reduced to "Why", trend show/hide verified across fast-pass and post-deep-pass; both hero-card colour guards green). AI drafted + built; **only the owner ratifies.**
