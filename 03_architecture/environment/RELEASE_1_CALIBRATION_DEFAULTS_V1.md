# Release 1 Calibration Defaults v1

**Document Type:** Calibration Parameter Defaults (numeric dials) · **Status:** **Adopted as operative defaults under DL-044 constituent C — 2026-06-04 (tunable; owner may retune any value without a new Decision)** · **Date:** 2026-06-04
**Satisfies:** DL-043 Condition 4 (numeric determinism/drift/band calibration) and the Environment-Profile R5 retention residual — provisionally, with **safe conservative defaults** the owner can tune later. **These are dials, not architecture:** changing any value changes behavior sensitivity, not the model. Per `CLAUDE.md`, the owner ratifies.

> **Why defaults now:** they unblock implementation without forcing premature precision. Every value is **conservative** (errs toward *surfacing* a concern rather than hiding it, consistent with OSLO's anti-false-certainty doctrine) and **independently tunable**. Engineering should treat these as configuration, not constants.

---

## 1. Determinism / Replay Tolerances

*(How close a re-run must match the record to count as conformant — per the two-axis replay model.)*

| Output class | Replay tier | Default tolerance |
|---|---|---|
| **Record replay** (any Cognition History / Acceptance / Attested record) | **exact** | **0** — byte/value-identical; any difference is a Critical trust failure |
| **Rule / formula-derived** (CAF formula step, structural findings, rule confidence) | **exact** | **0** — identical given same inputs + rule version |
| **AI-assisted numeric** (confidence, reliability, outcome confidence) | **band-semantic** | **± 7 points** on a 0–100 scale **and** same band (below) — within tolerance = conformant |
| **AI-assisted textual** (findings, issues, recommendations, clarifications) | **semantic** | **semantic-equivalence** (same finding identity / same recommendation intent); wording may differ |
| **Set-level** (which findings/issues exist) | **set** | **≥ 90%** overlap of stable identities across replay; new/dropped beyond that flags review |

## 2. Confidence Bands (0–100)

*(Where "low / medium / high" start and stop. Used for display and for band-semantic replay stability.)*

| Band | Range | Meaning |
|---|---|---|
| **Low** | **0–49** | understanding is weak/contested — surface prominently |
| **Medium** | **50–74** | partial understanding — usable with caution |
| **High** | **75–100** | well-grounded understanding |

- **Band-edge guard:** a value within **± 3 points of a band boundary** is treated as the **lower** band for display (conservative — never overstate confidence).
- Confidence = **trust in understanding, never project health** (preserved).

## 3. Drift Thresholds

*(How much a value must move before OSLO flags it. Outcome Drift is surfaced as a **feature**; these thresholds decide when it's worth the user's attention.)*

| Drift type | Default trigger | Treatment |
|---|---|---|
| **Outcome / Confidence drift** (a score moved between emissions) | **≥ 10 points** change **or** a **band change** | **surfaced** to user (product feature — "understanding shifted; here's why") |
| **Acceptance-Impact drift** (a value behind a *user-accepted* item moved) | **≥ 10 points** or **band change** vs. the version-pinned acceptance | **surfaced as an Acceptance-Impact alert** ("a decision you confirmed is affected") |
| **Determinism drift** (replay exceeded §1 tolerance) | **any** exceedance | **trust failure** (not a feature) — Critical/Major per QA & Observability Governance |
| **Confidence inflation** (confidence rises without new grounding evidence) | rise **≥ 10 points** with no new Attested input | **trust-failure flag** for investigation |

*(Outcome/Acceptance drift = product signal. Determinism drift / inflation = trust failure. Kept distinct on dashboards per R5.)*

## 4. Retention Durations

| Log / record class | Default retention |
|---|---|
| **Operational logs** (service/runtime telemetry) | **90 days** (per Environment Profile) |
| **Canonical records** (Attested Assertions · Cognition History Records · User Acceptance Records / plan facts) | **retained for project lifetime + 1 year** (append-only; never deleted while the project is active) — these are the system of record |
| **Audit receipts** (integrity-clearance, user-action) | **≥ 1 year** default; **owner to confirm against any compliance regime** (the "per compliance" residual) |

## 4b. Performance — Fast Pass NFR (proposed; resolves DL-046 open items)

*(Proposed starting values for the two items DL-046 left as `TBD – Owner Decision Required`: the latency **distribution** within the 60s ceiling, and the **supported-project-size envelope** for which the 60s target holds. Conservative; owner to confirm/tune. The **< 60s ceiling itself is ratified** — these only shape the distribution and the scope it applies to.)*

| Dial | Proposed default | Note |
|---|---|---|
| **Time-to-First-MRI — p50** | **≤ 25 s** | typical case should *feel* fast, well inside the ceiling |
| **Time-to-First-MRI — p95** | **≤ 50 s** | tail stays clear of the ceiling |
| **Time-to-First-MRI — hard ceiling (p100)** | **< 60 s** | **ratified** (Master Spec §20 / M1); the QA performance gate fails above this |
| **Fast Pass timeout** | **60 s** | at the ceiling: on breach, return partial orientation + transition to `analyzing` (never hang) |

**Supported-project-size envelope — Tier-1 / Free (the scope the 60s holds for; tier-keyed, paid-tier envelopes TBD):**

| Dimension | Proposed default | Note |
|---|---|---|
| Source artifacts per project | **≤ 20 artifacts** | Fast Pass orientation scope |
| Total project text | **≤ ~50,000 words** (~65–75k tokens) | the content the Fast Pass reasons over |
| Concurrency (R1) | **1 active Fast Pass per project** | single-user project; Deep Pass is async/coalesced |

- **Outside the envelope:** Fast Pass still runs but the 60s target is **not guaranteed** — it returns a partial orientation within budget and continues in `analyzing`/Deep Pass. The QA performance gate (DL-046) is asserted **on envelope-sized fixtures**.
- **✓ Tier-1 owner-confirmed (2026-06-05):** the **Free / Tier-1** envelope is set at **~20 artifacts / ~50k words / 1 active**, confirmed against typical free-tier project scale (brief/PRD/charter-sized document sets). This is the **guaranteed Tier-1 envelope** where the <60s gate and the DL-048 ~$3 Tier-1 cost math hold; larger projects are **not rejected** — they degrade gracefully (partial orientation + coalesced Deep).
- **Tier-keyed:** the envelope is a **tier dimension** (like the §4c cost caps + routing). **Paid-tier envelopes are TBD** (Open-TBD A1/E3) — add tier rows, not code, when defined.
- **Still to verify post-build:** real Fast-Pass latency (Phase III telemetry) may warrant raising/lowering the Tier-1 guarantee; re-tune alongside the cost defaults (§4c).

## 4c. Cost Governance — Freemium Unit Economics (proposed; DL-048, Balanced ~$3/mo)

*(Tier-keyed cost config adopted under DL-048. **The values are owner-tunable configuration; the enforcement mechanism, QA gate, and `AI Spend Recorded` event are contracted** — Wave B / Wave S / Wave I. Owner selected the **Balanced (~$3/active-free-user/month)** posture. Numbers are estimate-based starting defaults; the contracted cost telemetry replaces them with measured medians. **Per-run caps trigger graceful degradation; per-user rollups gate further AI spend — never silent overspend.**)*

**Free / Tier 1 defaults:**

| Config knob (tier-keyed) | Free / Tier 1 default | Note |
|---|---|---|
| Max active projects | **1** | structural |
| Model routing | **extraction → nano · synthesis/eval → mini · Haiku fallback** | primary cost lever; engine must honor per tier |
| Fast Pass per-run token cap (→ degrade) | **150,000** | envelope-driven (posture-independent); over → partial orientation |
| Deep Pass per-run token cap (→ coalesce/defer) | **600,000** | bounds worst case |
| Deep concurrency | **1** + coalescing **on** | structural; prevents runaway re-analysis |
| Deep runs / day | **2** | gate the expensive path |
| Suggested fixes / day | **5** | API `429 rate_limited` on breach |
| Chat messages / day | **20** | bound interactive burn |
| Daily token budget / user | **500,000** | burst smoothing |
| **Monthly token budget / user (hard rollup)** | **4,000,000** | the binding governor |
| Monthly $ ceiling / user (alert KPI) | **~$3.00** | business target |

**Cost basis (June 2026 pricing, verified):** GPT-4.1 $2/$8 · GPT-4.1-mini $0.40/$1.60 · GPT-4.1-nano $0.10/$0.40 · Sonnet 4.6 $3/$15 · Haiku 4.5 $1/$5 per 1M tokens (in/out). Per-run estimates: Fast ~120k tok ≈ $0.08 (mini); Deep ~500k tok ≈ $0.32 (mini) / $1.60 (GPT-4.1) / $2.70 (Sonnet). Monthly rollup: 4.0M tok/mo blended (nano-in/mini-out) ≈ **$3.04 worst-case if maxed daily**; median far below. Keep nano on extraction (pure-mini ≈ $3.52).

**Tier 2 — Basic (owner-confirmed 2026-06-05; first paid step, $12/mo):** differentiates on **capacity, not model quality** (routing stays cheap-class — full-quality model is the Tier-3 Pro upsell).

| Config knob | Basic / Tier 2 | Δ vs Free |
|---|---|---|
| Max active projects | **3** | the primary upgrade trigger |
| Model routing | **extraction → nano · synthesis/eval → mini** (same class as Free) | capacity is the differentiator |
| Fast Pass per-run token cap | **300,000** | 2× envelope (40 docs / ~100k words) |
| Deep Pass per-run token cap | **1,000,000** | larger-project expansion |
| Deep concurrency | **1** + coalescing **on** | structural |
| Deep runs / day | **6** | burst ceiling (not the governor) |
| Suggested fixes / day | **20** | removes daily-limit friction |
| Chat messages / day | **75** | |
| Daily token budget / user | **1,500,000** | burst smoothing |
| **Monthly token budget / user (hard rollup)** | **10,000,000** | the binding governor (~12 Deep or ~80 Fast/mo across 3 projects) |
| Monthly cost @ budget | **~$7.90 worst-case** / ~$2 typical (25% util) | $12 price → 34% worst / ~84% typical margin |

- **Per-tier, not free-vs-paid:** all knobs are **tier rows**. **Tier 1 (Free) and Tier 2 (Basic) are owner-confirmed; Tiers 3–5 (Pro · Team · Enterprise) remain TBD** (Open-TBD A1/E3; ladder draft `01_governance/backlog/BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md`) — add rows, not code.
- **⚠ Confidence note:** these are **estimate-based starting placeholders**, not measured runs. Re-tune from the `AI Spend Recorded` telemetry in the first weeks. Free posture = Balanced (~$3); Basic = $12/mo capacity tier.

## 4d. Upgrade-Prompt timing — Tier-1 (proposed; FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001)

*(Tunable timing config for MON-04 Upgrade Prompts. The **trigger taxonomy** is in `02_product/tiering/12_freemium_tier_behavior_logic.md`; these are the **numbers** — conservative starting defaults, re-tuned from TEL-07 against the optimality objective. Friction triggers consume the DL-048 constraint-detection signals.)*

| Knob | Proposed default | Note |
|---|---|---|
| Global prompt cap | **≤ 2 / day**, **≤ 1 / session** | hard ceiling across all triggers; anti-annoyance |
| Per-trigger cooldown (friction, daily-cap) | **24 h** | UP-1/2/5: once/day each |
| Per-trigger cooldown (monthly) | **1 / month** | UP-6 |
| High-intent trigger (UP-3, 2nd project) | **immediate, no cooldown** | intent moment — exempt from the per-day softening |
| Value-trigger cooldown (UP-7) | **≥ 7 days** | rare by design |
| First-value guard | **on** — no prompt before first MRI delivered | session/activation guard |
| No-interrupt guard | **on** — never during an active Fast/Deep pass | |
| Annoyance threshold (auto-suppress) | **dismiss-rate > 60% AND convert-rate < 2%** over a trigger's last N shows | suppress + flag for re-tune |

- These are **owner-tunable placeholders**, not measured; TEL-07 (displayed/clicked/converted + dismiss) provides the tuning signal. UP-3 (high-intent) and UP-4 (honest-disclosure, fired with the Wave E partial-orientation surface) are exempt from the per-day cap when they coincide with a genuine constraint event.

## 5. Status & Tuning

- **All values above are owner-review-pending defaults.** They are **configuration**, surfaced for ops to adjust per environment; none changes the architecture or any contract's structure.
- **Tuning guidance:** lower thresholds = more sensitive (more flags, fewer missed shifts); raise = quieter. Defaults lean **sensitive** by design (surface over suppress).
- **Open for owner:** confirm the **± 7 / 10-point** sensitivities, the **75/50** band edges, and the **audit retention vs. compliance** duration.

---

*This document provides conservative, owner-review-pending numeric defaults satisfying DL-043 Condition 4 and the Environment-Profile retention residual: determinism/replay tolerances (exact for records and rule/formula outputs; ±7 points and same-band for AI-assisted numeric; semantic-equivalence for AI-assisted text; ≥90% set overlap), confidence bands (0–49 low / 50–74 medium / 75–100 high, with a ±3-point conservative band-edge guard), drift thresholds (≥10 points or a band change to surface Outcome/Acceptance drift as a product feature; any replay-tolerance exceedance or unexplained ≥10-point confidence rise as a trust failure), and retention durations (90-day operational logs; project-lifetime+1-year canonical records; ≥1-year audit receipts pending compliance confirmation). All values are tunable configuration that leans toward surfacing over suppressing, change no architecture or contract structure, and are routed to the owner for review.*

**Release 1 Calibration Defaults v1 — proposed, owner-review pending.**
