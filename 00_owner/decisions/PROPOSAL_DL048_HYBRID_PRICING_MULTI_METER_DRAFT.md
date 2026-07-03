# PROPOSAL — DL-048 Extension: Hybrid Pricing (Multi-Meter / Single-Governor)

- **Status:** **Owner-ratified (intent), 2026-06-19.** Decisions resolved (§4); formalized as **DL-074** (extends DL-048). Realization (Calibration §4c T3–T5 rows + the meter abstraction + upgrade/overage UX) is a follow-on. AI-drafted; owner ratified.
- **Framework 001 stage:** Proposal.
- **Class:** Monetization / cost-governance policy. **Extends DL-048**; consumes the Calibration §4c tier config and the tier-progression backlog. No doctrine/constitution change; no epistemic invariant touched.
- **Source:** Owner direction 2026-06-19; the 2026-06-19 AI-pricing best-practice review (hybrid is the emerging standard); DL-048 (cost governance / freemium, Balanced ~$3); Calibration §4c (T1/T2 confirmed); `BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md` (illustrative ladder); DL-073 (anonymous cap + Deep-Pass upgrade gate).

---

## 1. Proposed change

1. **Adopt a hybrid model.** Each tier = a **subscription** (capacity + model quality) that **includes** a usage envelope, **plus metered overage** above that envelope, **plus per-seat** pricing at Team/Enterprise. This **extends DL-048's current posture** (hard-cap → graceful-degrade + upgrade prompt) by adding a **paid-overage path** for paid tiers — a third option between "degrade" and "upgrade a whole tier."
2. **Single-governor / multi-meter architecture.** Keep **one universal back-end cost governor** — a **normalized compute unit** (tokens × model-tier weight), generalizing DL-048's "monthly token budget = the binding governor" so it absorbs *any* compute source (Fast, Deep, monitoring, agents). Expose **feature-appropriate value-units** on the billing surface rather than forcing all compute into one unit.
3. **Meter map (value-units by capability):**
   - **Analysis (Fast/Deep)** → **Deep Passes / analyses** — the R1 overage unit.
   - **Execution monitoring (Pro+)** → **capacity add-on** (per monitored project / connected platform × cadence) — subscription-shaped, not per-event. `[forward — scoped when exec-monitoring lands]`
   - **Agents / execution** → **per-task / per-action** meter (the outcome-based candidate). `[forward — out of R1; scoped when agents land]`

## 2. Tier ladder (confirmed vs owner-decision)

| Tier | Price / mo | Included capacity (key knobs) | Model quality | Overage | Status |
|---|---|---|---|---|---|
| **Anonymous** (pre-signup) | $0 | a few capped Fast Passes; no save | cheap | none (must sign up) | DL-073; cap value TBD |
| **T1 Free** | $0 | 1 project · ~20 art/50k words · 2 Deep/day · 4M tok/mo (~$3 cost) | cheap (nano/mini) | **none — upgrade to convert** | confirmed (§4c) |
| **T2 Basic** | $12 | 3 projects · ~40 docs/100k · 6 Deep/day · 10M tok/mo | cheap (same class) | optional metered Deep | confirmed (§4c) |
| **T3 Pro** | ~$39 *(illustrative)* | ~10 projects · ~80/200k · 15 Deep/day · 25M tok/mo · +exec-monitoring | mid (mini + full fallback) | metered Deep + monitoring add-on | **owner-decision** |
| **T4 Team** | ~$99–149 / seat *(illustrative)* | per-seat · ~150/400k · 50M tok/seat | premium (GPT-4.1 synth) | metered Deep + agent meter (fwd) | **owner-decision** |
| **T5 Enterprise** | custom | negotiated; dedicated routing; SSO | premium + dedicated | negotiated / committed-use | **owner-decision** |

**Design rules (already owner-set, retained):** Basic sells **capacity**; Pro adds **model quality** (premium routing held above Basic); **routing quality, not token volume, is the dominant cost driver at the top** — so premium routing must be priced high or metered, more than tokens.

## 3. Overage rules (proposed)

- **Included first.** Each tier's subscription includes its §4c envelope unchanged. Overage applies only above it.
- **Free does not buy overage** — Free hitting its ceiling **upgrades** (preserves the conversion funnel); paid tiers may buy overage to absorb spiky months without a full tier jump.
- **Tier upgrade is the better unit price** for sustained heavier use; overage is for bursts. Both coexist (the hybrid standard).
- **Guardrails (converge with epistemic honesty).** A visible meter ("12 of 15 Deep used"), a user-set **spend cap**, and **threshold alerts** — no bill shock. This reuses the contracted **honest-limit disclosure** (DL-048 / UP-4): the surfaced constraint *is* the upgrade/overage moment.
- **One governor, no silent overspend.** All meters reconcile to the normalized compute unit; per-run caps still degrade gracefully, per-user rollups still gate — overage is an *explicit, priced* relaxation, never silent.

## 4. Owner Decisions — RESOLVED (owner, 2026-06-19; ratified as DL-074)

- **Overage:** ADOPTED — **per-Deep-Pass** under a **"usage-based" umbrella**, with a **normalized compute-unit governor (tokens × model-tier weight)** underneath; future units (monitoring, agents) attach as ADDs, never a reframe.
- **Scope:** **paid tiers only**; Free converts via upgrade (no Free purchase path).
- **T3–T5:** adopt the **illustrative ladder** as starting values (Pro ~$39, Team ~$99–149/seat, Enterprise custom), re-tuned from telemetry.
- **Per-seat:** **seat + usage hybrid** at Team/Enterprise.
- **Forward meters:** monitoring = capacity add-on; agents = per-task — added when scoped.

Original open-decision list, retained for provenance:

1. **Adopt paid overage at all?** (vs. keep DL-048 hard-cap-only). This is the load-bearing call.
2. **Overage unit + price:** per-Deep-Pass top-up vs. prepaid credit block; the price per unit (anchored to §4c cost basis + margin).
3. **Where overage is allowed:** confirm Free is excluded (upgrade-only); which paid tiers can buy how much.
4. **T3–T5 envelopes + prices:** the §4c tier rows for Pro/Team/Enterprise (Open-TBD A1/E3).
5. **Normalized compute-unit definition:** raw tokens vs. tokens × model-tier weight (recommended — reflects true cost as routing diverges).
6. **Per-seat at Team/Enterprise:** confirm seat + usage hybrid (vs. pure usage).

## 5. Framework 001A Review

- **Findings:** hybrid (subscription + metered overage) is the emerging standard and fits OSLO's AI cost structure (compute is the cost driver, not seats). DL-048 already meters on a token-budget governor, so the single-governor/multi-meter model is an extension, not a re-architecture. Deep-Pass overage is correct for R1; monitoring/agent meters are forward, scoped with their capabilities.
- **Concerns:** a single Deep-Pass meter does not generalize to T3+ heterogeneous compute (continuous monitoring; variable agent tasks) — addressed by the multi-meter design. Credit opacity and bill-shock are the known failure modes — addressed by legible value-units + spend caps + honest disclosure. Adopting paid overage changes DL-048's cap posture and must not become "silent overspend."
- **Dependencies:** DL-048 (cost governance); Calibration §4c (tier rows); DL-046 (Fast/Deep + 60s); DL-073 (anonymous cap, Deep-Pass upgrade gate); the `AI Spend Recorded` telemetry (the meter's data source); exec-monitoring + agents scoping decisions (forward meters).
- **Recommendation:** adopt the **hybrid, single-governor/multi-meter** model; ship **Deep-Pass overage for paid tiers in R1** with spend-cap guardrails; lock the **normalized-compute-unit governor** now; add monitoring/agent meters as `[forward]` rows when those capabilities are scoped. Set T3–T5 rows (Decision 4) and the overage unit/price (Decision 2) before enabling. I recommend only; owner ratifies.
- **Status:** Ready for owner decision on §4; realization (meter abstraction + §4c rows + upgrade/overage UX) follows ratification.

## 6. Owner decision required (summary)

1. Adopt paid overage (yes/no) and the single-governor/multi-meter model.
2. Set the overage unit + price and where it's allowed (§4.2–4.3).
3. Set the T3–T5 tier rows (§4.4) and the normalized compute unit (§4.5); confirm per-seat at Team/Enterprise (§4.6).
4. On ratification: extend DL-048 (a DL), add the §4c Pro/Team/Enterprise rows, and route the meter abstraction + upgrade/overage UX as engineering/commodity realization.
