# DL-122 — The notification router: one awareness record, global toast delivery attributed to no panel (realizes NOTIFICATION_MODEL_V1 §17)

- **Date:** 2026-07-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — The notification router: one awareness record, global toast delivery attributed to no panel (realizes NOTIFICATION_MODEL_V1 §17)

**Class:** A (capability commission + delivery-layer realization) · **Framework 001A** (AI drafts + builds on commission; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-17 · **Realizes:** `NOTIFICATION_MODEL_V1` §17 (the deferred routing/delivery capability) via the ratified proposal `notification-routing-delivery-proposal.md` (§4 tiers + §6 open items **RATIFIED 2026-07-15**). Grill record: **Enhancement #4**; commissioned by owner 2026-07-17.

## Problem
The Notification **model** was settled, but OSLO had **two unrelated delivery mechanisms**: the durable awareness panel/bell/badge (D104) and the episodic "What changed" payoff bar (D179a). No layer said *which event goes to which surface*, and the payoff bar was never recorded in the awareness panel — so a dismissed "What changed" notice was simply lost. Enhancement #4 supplies the routing/delivery layer that reconciles them.

## Decision
**Commission and build the notification router** as the single in-app dispatch, on the ratified proposal. Its governing principle is **one record, many views** (§2): every event is recorded **once** in the awareness record; channels are VIEWS onto that record, never separate stores.

**The notification is delivered by two channels — the durable record and the global toast — and is attributed to NO panel:**
- **B — the awareness panel + bell + badge.** The **durable record on every screen** (the top bar). **Every** notification lands here (the single record). Presentation-only; routes to source; neutral badge (D003).
- **G — the global transient toast.** A brief app-level toast that reaches you **anywhere in the app** (including the Overview), carries its project context, auto-dismisses (never permanent chrome, D179a), and **belongs to no panel** — so a notification is never mis-read as being "about" whatever panel it sits near. **Interrupt tier only** (so it never becomes fatigue). Carries the "· in Notifications" affordance back to the record (§6.6).

**Why the notification is NOT an in-context panel bar (attribution).** The model's channel A ("a 'What changed' bar at the top of the surface") is **not realized on the Overview**: **D179a** forbids an event outranking state in the layout, and **`_assertConfidenceIsTheFirstPanel`** keeps Outcome Confidence first — so a notification cannot sit above the panels there, and nesting it *inside* a panel (the first cut put it in the Confidence card) wrongly implies the event is *about* that panel. The global toast (G) is the doctrine-clean page-level surface instead. The Confidence card's own "What changed" bar is a **separate** thing — the **read-movement delta** (D179b), which is legitimately about the read and stays on the card; it carries no notification framing.

**Routing (qualitative tiers, no score — §4):** interrupt events (analysis landed/failed, a reviewer responding) record in **B** and toast via **G**, anywhere in the app; ambient events (mentions, replies, dispositions, shared-with-me, stale, governance) record in **B** only (the badge). The toast is reserved for the interrupt tier so it never becomes fatigue.

## Conformance basis (every model invariant preserved)
- **Awareness only (D104):** the router **records + surfaces**; it never assesses, governs, decides, or **triggers analysis / mutates the read**.
- **Neutral (D003):** the badge and toast are neutral/brand, never a severity signal.
- **Transient not chrome (D179a):** state outranks event — the toast is auto-dismissing and belongs to no panel, never sitting above the state in the layout; durable project state lives in Progress/Overview, and the durable *record* lives in B.
- **No priority formula (§4):** the interrupt/ambient split is qualitative, not a computed score.
- **Explainable (§14):** every notice traces to its source object and routes to it.
- **⛔ D182 — the probe fence.** Routing is suppressed whenever a probe/self-check is active (`_probeActive()`), so the guard suite's re-runs of the resolution paths **never emit a stray record or toast**. This is why boot shows **zero notifications** while the router is fully wired to the live resolution paths.

## Scope boundary (explicitly NOT here)
- **External channels (email/Slack) — out of R1** (§17 future / §6.2), per the ratified proposal. In-app (toast + badge + bar) suffices for the Alpha cohort.
- **R1 inclusion is a SEPARATE, deferred call.** DL-120 placed the router **out of R1** (it was unbuilt at freeze-planning). This decision **commissions and builds** it (resolving "unbuilt") but does **not** fold it into R1: whether it rides in R1 is a **DL-120 amendment to ratify at freeze**. Built-and-ready ≠ in-scope; the fold stays an explicit owner call.

## Guards (executable — `window._S10`)
Boot holds at **145/145, 0 pageerrors**, both themes, with **zero stray notifications at boot** (the probe fence). Functional verification: an interrupt event (confirm/fix/answer/reviewer) fires the **global toast anywhere in the app, including the Overview**, and records in the badge; the Confidence-card "What changed" bar carries **no** notification framing (it is the read-delta, D179b); ambient events record in the badge with no toast. The neutral badge (D003), `_assertPayoffLivesInsideTheConfidenceCard` (D179b — the read-delta stays on the card, **unamended**), and the never-triggers-analysis invariant (D104) all hold after routing.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). A **commissioned capability build** realizing an already-ratified model (§17) and proposal (§4/§6 closed) — no model rule is changed. Overview / notification surfaces reopened; re-signoff required. AI implemented on commission; only the owner ratifies.

## Provenance
Owner commissioned Enhancement #4 (2026-07-17: "proceed with #2"). Built into slice-10: `routeNotification` (the single dispatch), `_globalToast` (channel G, the ratified toast design), the awareness record (channel B), and the "· in Notifications" affordance on the in-context bar (channel A); wired to the interrupt sources (confirm/fix/answer/reviewer). Owner then flagged an **attribution defect** — a "What changed" notice inside the Confidence card wrongly implies the event is *about* confidence, and asked for a notification "not directly associated with any panel… effective globally." Since D179a forbids an event above the state in the layout, the doctrine-clean realization is **the notification = the global toast (G) + the record (B)**, attributed to no panel; the Confidence-card bar was reverted to a pure read-delta (D179b, unamended). Verified 145/145, boot-clean. AI implemented; owner ratifies.

### Sources
- Model + proposal: **NOTIFICATION_MODEL_V1** §12/§17, `notification-routing-delivery-proposal.md` (§4 tiers + §6 open items ratified 2026-07-15).
- Doctrine: **D104** (awareness panel, presentation-only), **D179a** (episodic; state outranks event), **D003** (neutral badge), **D182** (the probe fence — a probe must never touch the user), **D043** (analysis-completion delivery).
- Prototype: `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` — `routeNotification` / `_globalToast` / `_barVisibleNow` / `_payInNotif`, and the resolution-path hooks in `applyFix` / `answerClarification` / the reviewer-response path.
