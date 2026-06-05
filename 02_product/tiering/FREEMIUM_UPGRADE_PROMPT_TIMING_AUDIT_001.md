# Release 1 — Freemium Upgrade-Prompt Timing Audit 001

**Document Type:** Owner-directed capability audit (Framework 001A Review schema) · **Status:** **APPLIED — owner-directed 2026-06-05; CHG-058.** Recommendation adopted: trigger taxonomy + timing criteria written to the freemium spec, timing config to Calibration §4d, UP-4 unified with the Wave E honest-limit disclosure, MON-04 matrix note + tier-name drift fixed. · **Date:** 2026-06-05
**Question (owner-directed):** *For the Free / Tier-1 tier in Release 1, are the upsell (Upgrade-Prompt) capabilities defined to be **initiated at the optimal moment of the user experience, based on criteria** — or only defined to exist?*
**Scope:** Free / Tier-1 only; the **timing + trigger criteria** of MON-04 Upgrade Prompts (not the billing/checkout flow). **Canonical term:** **Upgrade Prompt** (MON-04); "upsell notification" = the same concept — use the canonical term to avoid drift.
**Sources audited:** `02_product/tiering/12_freemium_tier_behavior_logic.md` · `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (MON-01…04, TEL-07, REC-04) · `02_product/specs/ux/NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · DL-048 / Calibration §4c (constraint events) · CHG-056 (envelope) · CHG-057 (Basic tier) · the tier-progression backlog.

---

## 0. Verdict

**Defined to exist and in principle — NOT defined to fire at the optimal moment by criteria.** The corpus establishes the *intent* ("contextual, value-based, appear at limits, no persistent wallpaper") and the *measurement* (TEL-07), but **does not enumerate the trigger set, the timing/suppression criteria, or what "optimal" means** — and it contains an **unreconciled tension** between *value-moment* and *limit-moment* triggering. The newer **DL-048/CHG-056 constraint events are not mapped to prompts at all.** This is the commodity side of the "constraint → upgrade moment" seam the tier-progression backlog flagged as unowned.

---

## 1. Findings

**F1 — Trigger set is not enumerated.** MON-04 says "appear contextually at limits"; only **fix / chat / project** limits are implied (via TEL-07). The **DL-048 / CHG-056 Tier-1 constraints are unmapped to any prompt:** envelope-exceeded (partial orientation), Deep-runs/day cap, daily/monthly token-budget gate. A user can hit a real wall with **no defined prompt**.

**F2 — "Optimal time" / timing criteria are undefined.** "Contextual and value-based" and "no persistent wallpaper" are the *only* timing rules. There is **no criterion for when to fire vs suppress**: no frequency cap / cooldown, no "don't interrupt an active analysis," no "not before first value delivered / first session," no per-trigger specificity rule. "Optimal" is asserted, not operationalized.

**F3 — Latent conceptual tension: value-moment vs limit-moment.** The matrix frames prompts at **friction** ("when limits are reached"); the freemium spec's only example fires at a **value peak** ("after user improves confidence"). These are **two different trigger philosophies** and the corpus never reconciles them. Both are valid — but a build team would have to *guess* which governs, which is the drift this audit exists to prevent.

**F4 — The commodity prompt is not wired to the contracted detection events.** Constraint *detection* (cap-hit, envelope-exceeded → partial orientation, budget gate) is now a **contracted DL-048 behavior** emitting signals (`AI Spend Recorded`, the degradation/gating events). The **prompt (commodity MON-04) is not defined to consume those events** — so "fire at the exact moment the limit is hit" has no specified mechanism. The seam is real but unbuilt.

**F5 — Optimality is measured but not defined.** TEL-07 captures displayed/clicked/converted + limits-reached, but **no criterion defines success** (e.g. prompt→convert rate vs an annoyance/dismissal signal), so there is nothing for the team to *tune timing against*. Measurement without an objective function.

**F6 — Upgrade target is now concrete (positive — unblocks copy).** Previously "paid tiers undefined" (Matrix note 10) left prompts with no target. **CHG-057 defined Tier-2 Basic** (and the ladder names Pro), so prompts can now name a **specific destination and benefit** ("…Basic gives you 20 fixes/day") instead of a generic "upgrade." This removes the prior blocker on prompt specificity.

**F7 — Minor: terminology drift in the source spec.** `12_freemium_tier_behavior_logic.md` uses **"Professional Tier"** and **"Team / Business Tier"** — pre-canonical names. Canonical (CHG-057 / glossary) is **Pro** and **Team**. Align to prevent drift.

## 2. Concerns

- **Under-prompting vs over-prompting both lose:** with no cooldown/criteria, a build team will either fire on every cap-hit (annoyance → churn, violating "no wallpaper" in spirit) or under-fire (missed conversions). The criteria are the guardrail against both.
- **Epistemic-honesty coupling:** the envelope-exceeded case is **also** an epistemic-safety obligation (partial analysis must be disclosed honestly — DL-046/047/048). If the upgrade prompt and the honest-limit disclosure are built separately, they may **conflict or double up**. They should be **one surface** (the backlog's "graceful-limit-as-upgrade-moment" principle).
- **R1 reality:** MON-01…04 are Alpha (R1), so this *is* in Release 1 — the timing gap is a launch-quality issue, not a future one.

## 3. Dependencies

- **DL-048 / Calibration §4c** — the constraint events that are the friction triggers (caps, envelope, budget).
- **CHG-057 (Basic)** — the concrete upgrade target + benefit copy.
- **NOTIFICATION_AND_AWARENESS_SURFACE_SPEC** — the delivery surface (prompts must fit its construct taxonomy, not a new channel).
- **TEL-07** — the optimality measurement.
- **Wave E Disclose** — where the envelope-exceeded honest-limit disclosure lives (the one contracted touch).

## 4. Recommendation (owner-routed; no spec edited here)

Define the Upgrade-Prompt **trigger taxonomy + timing criteria** as an explicit addition to the freemium behavior spec (the *structure* below; the *numbers* are owner/calibration config). Specifically:

1. **Adopt a two-class trigger model** (resolves F3): **value-moment** prompts (fire at a positive peak — sell the *next* capability) and **friction-moment** prompts (fire when a Tier-1 constraint is hit — honest limit disclosure + the specific relief). Every prompt is one or the other, explicitly.
2. **Enumerate the trigger taxonomy** (resolves F1/F4) — map **each Tier-1 constraint/value event → a prompt, its moment, its target tier, and its timing rule** (table in §5). Friction triggers **consume the DL-048 detection signals** (wires the seam).
3. **Define timing/suppression criteria** (resolves F2) as tier-keyed config: **per-trigger cooldown**, **global frequency cap** (max prompts / session / day), **no-interrupt** (never during active analysis), **session/value guard** (not before first MRI delivered), **specificity rule** (name the exact limit + exact tier). Numeric values → **owner-set (Calibration / Open-TBD)**, not invented.
4. **Define "optimal" as an objective** (resolves F5): maximize **prompt→conversion** while keeping a **dismissal/annoyance signal** below a threshold; TEL-07 already captures the inputs. A trigger that under-converts and over-annoys is auto-suppressed/re-tuned.
5. **Unify with the honest-limit disclosure** (the envelope case): the partial-orientation disclosure (contracted, Wave E) **is** the friction-moment prompt surface — build one, not two.
6. **Fix terminology** (F7): Professional→**Pro**, Business→**Team**.

## 5. Proposed Upgrade-Prompt trigger taxonomy (for owner ratification — structure firm, numbers owner-set)

| # | Trigger event (Tier-1) | Moment | Target | Value-framed message (illustrative) | Timing rule |
|---|---|---|---|---|---|
| UP-1 | Daily **fix cap** reached (5/day) | friction | Basic | "You've used today's fixes — **Basic** gives you 20/day." | at cap-hit; **once/day**; cooldown |
| UP-2 | Daily **chat cap** reached (20/day) | friction | Basic | "More questions? **Basic** raises your daily chat limit." | at cap-hit; once/day |
| UP-3 | **2nd active project** attempted (Free = 1) | friction (high-intent) | Basic | "Free includes 1 active project — **Basic** gives you 3." | fire **immediately** (intent moment); no cooldown |
| UP-4 | **Envelope exceeded** → partial orientation | friction + **honest disclosure** | Basic | "This is a **partial** analysis — your project exceeds the Free size. **Basic** analyzes projects up to ~100k words." | fire **with** the Wave E partial-orientation disclosure (one surface) |
| UP-5 | **Deep-runs/day** cap reached (2/day) | friction | Basic | "You've used today's deep analyses — **Basic** gives you more." | at cap-hit; once/day |
| UP-6 | **Monthly budget** gate reached | friction (soft) | Basic | "You've reached this month's analysis limit." | once/month; gentle |
| UP-7 | **Confidence improved / outcome achieved** | **value** | Pro | "**Continuous monitoring** can protect this confidence over time." *(→ the Pro exec-monitoring capability)* | at value peak; **rare**, strict cooldown |
| UP-8 | **First MRI delivered** (activation) | value | — / Basic (soft) | celebrate value; **no hard sell** | once, first project only |

**Global guards (all triggers):** no persistent wallpaper (existing); never interrupt an active Fast/Deep pass; not before first value delivered; honor per-trigger cooldown + a global per-day cap; always name the **specific** limit + **specific** tier.

## 6. Owner decision required
- [ ] Adopt the **two-class (value/friction) trigger model** and the **§5 taxonomy** as the R1 definition of Upgrade-Prompt timing.
- [ ] Approve wiring friction triggers to the **DL-048 detection signals** (the contracted seam), and **unifying UP-4 with the Wave E honest-limit disclosure** (one surface).
- [ ] Set the **timing numbers** (cooldowns, per-day cap, value-trigger rarity) as Calibration config (or route to Open-TBD).
- [ ] Approve the **optimality objective** (convert-rate up, annoyance-signal bounded) for TEL-07.
- [ ] Approve the **terminology fix** (Professional→Pro, Business→Team) in the freemium spec.
- [ ] On approval: amend `12_freemium_tier_behavior_logic.md` (+ enumerate MON-04 triggers); note the one contracted touch in Wave E; record via changelog.

## 7. Status
**FINDINGS RECORDED — under-specified system (timing/criteria), one conceptual tension (F3), one coverage gap (F1/F4), one minor drift (F7); no Critical conflict.** No spec edited. Routes to owner; consistent with the tier-progression backlog (same seam, commodity side).

---
*This owner-directed audit finds that Release-1 Free-tier Upgrade Prompts (MON-04) are defined in principle — contextual, value-based, no persistent wallpaper, measured by TEL-07 — but are **not defined to fire at an optimal moment by criteria**: the trigger set is not enumerated (the DL-048/CHG-056 constraint events are unmapped), the timing/suppression criteria and the meaning of "optimal" are undefined, the prompt is not wired to the contracted constraint-detection signals, and the spec leaves an unreconciled value-moment-vs-limit-moment tension plus minor tier-name drift. It recommends (owner-routed, nothing redefined) a two-class trigger model, an enumerated trigger taxonomy mapping each Tier-1 constraint/value event to a value-framed prompt and timing rule, tier-keyed timing criteria with owner-set numbers, an explicit optimality objective for TEL-07, and unifying the envelope-exceeded prompt with the contracted honest-limit disclosure — now unblocked because CHG-057 gives the prompts a concrete Basic target.*

**Freemium Upgrade-Prompt Timing Audit 001 complete. Pending Owner Direction.**
