# DL-074 — Hybrid pricing — tier subscription + per-Deep-Pass overage (single-governor / multi-meter); extends DL-048

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-19 + the 2026-06-19 AI-pricing best-practice review; DL-048 (cost governance / freemium); Calibration §4c (T1/T2 confirmed); `BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md` (illustrative ladder); DL-073 (anonymous cap, Deep-Pass upgrade gate). Supporting analysis: `PROPOSAL_DL048_HYBRID_PRICING_MULTI_METER_DRAFT.md`.
- **Layer:** Monetization / cost-governance policy. **Extends DL-048.** No doctrine or constitution change; no epistemic invariant touched.

## Decision
1. **Adopt hybrid pricing.** Each tier = a **subscription** (capacity + model quality, including a usage envelope) + **metered overage** above the envelope + **per-seat** at Team/Enterprise. This **extends DL-048's** hard-cap → degrade/upgrade posture by adding a **paid-overage path on paid tiers**.
2. **Single-governor / multi-meter.** One **normalized compute-unit governor** — **tokens × model-tier weight** — generalizes DL-048's monthly-token-budget rollup to absorb **any** compute source. Billing-surface value-units are feature-appropriate: **analysis → per-Deep-Pass** (the R1 overage unit, presented under a **"usage-based" umbrella**, not "Deep-Pass pricing"); **execution monitoring → capacity add-on** (forward, Pro+); **agents/execution → per-task** (forward, post-R1). Adding units later is an **ADD, never a reframe**.
3. **Overage scope = paid tiers only.** Free converts via **upgrade** (honest-limit disclosure + upgrade prompt; no Free purchase path). Tier upgrade is the better unit price for sustained use; overage absorbs spiky months.
4. **Tier ladder.** T1 Free / T2 Basic per Calibration §4c (confirmed, unchanged). **T3 Pro ~$39/mo · T4 Team ~$99–149/seat · T5 Enterprise custom** adopted as **starting** values from the backlog ladder (Basic sells capacity; Pro adds model quality; per-seat at Team/Enterprise) — re-tuned from `AI Spend Recorded` telemetry.
5. **Guardrails.** Visible meter, user-set **spend cap**, threshold alerts — **no silent overspend, no bill shock**; reuses the contracted honest-limit disclosure (DL-048 / UP-4), which converges with OSLO's epistemic-honesty posture. Per-run caps still degrade; per-user rollups still gate; overage is an **explicit, priced** relaxation.

## Preserved
No epistemic invariant, no cognition, no doctrine/constitution touched. DL-046 (Fast/Deep + 60s) and DL-073 (anonymous cap, Deep-Pass upgrade gate) unchanged.

## Realization (follow-on)
Amend Calibration §4c to add the **T3–T5 tier rows** (owner-tunable config); build the **normalized-compute-unit meter abstraction** + per-Deep-Pass overage on the contracted `AI Spend Recorded` telemetry; the upgrade/overage UX is commodity (MON). Monitoring + agent meters are added as `[forward]` rows when those capabilities are scoped.

## Supersedes / Amends
**Extends DL-048** (adds the paid-overage path + the single-governor/multi-meter model + the T3–T5 rows). No canonical content superseded; epistemic invariants preserved.

## Provenance
Owner decision via working session, 2026-06-19; overage unit/scope selected by the owner after a PLG/AI-pricing best-practice review (and a strong-form trade-off argument for per-Deep-Pass vs. abstract credits). AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.
