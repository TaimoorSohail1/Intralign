# Open-TBD Register — DO NOT ASSUME · ESCALATE

**Status:** Authoritative list of unresolved owner decisions · **Date:** 2026-06-04
**Rule (see `ANTI_ASSUMPTION_BUILD_PROTOCOL.md`):** every item below is **`TBD – Owner Decision Required`**. If your work depends on one, **escalate to the repository owner — do not pick a value to unblock yourself.** Build the **structure** and **scaffold the metric/harness**; add the numeric pass/fail only when the owner sets it. **No thresholds are invented.**

> The corpus already enforces "no invented numbers." This register **consolidates** the open items so an external team/LLM sees them in one place. The detailed, owner-assigned source of truth is **`02_product/specs/data_api_nfr/RELEASE_1_NFR_ACCEPTANCE_MATRIX.md`** (+ Performance/NFR §20). Where this register and that matrix differ, **the matrix wins.**

> ## ✅ OWNER CONFIRMATION (2026-06-05) — `OWNER_DECISION_QUEUE.md` Q17–Q29
> The owner **confirmed all proposed defaults** in Sections A–E as the **R1 working values** (rationale: R1 optimizes learning velocity/telemetry/trust validation; *defaults stay unless implementation constraints emerge; future adjustments are telemetry-informed*). Therefore: where a row below has a **proposed default**, treat it as **owner-confirmed-for-R1 (refine from telemetry)**; where a row had **no concrete default**, adopt a sensible starting value, scaffold the metric, and refine from telemetry. **Still genuinely open:** paid-tier values (A1-paid / E3 → R2), brand type/logo/microcopy (E4 → designer), and the CAF/Confidence formula (F1 → TBD-by-design). Accessibility (E2) = **WCAG 2.1 AA adopted.**

## A. Performance / latency (almost all numeric NFRs)

| # | Item | Status | Source |
|---|---|---|---|
| A1 | **Fast Pass project-size *envelope*** (artifacts / words / concurrency the 60s holds for) — **tier-keyed** | **Tier-1 (Free) owner-confirmed (2026-06-05): ~20 artifacts / ~50k words / 1 active** (typical free-tier project is brief/PRD/charter-scale). This is the **guaranteed Tier-1 envelope** where the <60s gate + the DL-048 ~$3 Tier-1 cost math hold; **larger projects degrade gracefully** (partial orientation + coalesced Deep), not rejected. **Paid-tier envelopes are TBD** (parameterize like the cost config — see E3). **Re-confirm Tier-1 latency post-build (Phase III).** | Perf/NFR §20.1; Calibration §4b/§4c; E3 |
| A2 | **Time-to-First-MRI latency distribution** (p50/p95 percentile) | Proposed (DL-046: p50≤25s/p95≤50s/<60s ceiling) — **owner to confirm.** The **< 60s ceiling itself is ratified** (Master Spec §20/M1). | Calibration §4b; Perf/NFR §3 |
| A3 | **Deep Pass** completion target / acceptable range / timeout | TBD | Perf/NFR §4 |
| A4 | **API latencies** (project create/load, artifact save, evidence upload, findings/recs load, reporting, notifications) | TBD | Perf/NFR §3, §7 |
| A5 | **Event throughput / lag** (quantitative) — *guarantees* are fixed by the Event Model; only the *numbers* are TBD | TBD | Perf/NFR §5 |
| A6 | **Fast/Deep AI call + token budgets** (overall, per-run, per-tier) | **Proposed defaults adopted (DL-048, Balanced ~$3/mo Free tier — Calibration §4c): Fast per-run 150k, Deep per-run 600k, daily 500k, monthly 4M, ~$3 ceiling; nano/mini routing.** **Enforcement, QA gate, and `AI Spend Recorded` telemetry are contracted (Wave B/S/I).** Values are estimate-based **starting placeholders — confirm/re-tune against first-weeks telemetry.** | Perf/NFR §12; Calibration §4c; DL-048 |

## B. Scale / capacity / availability

| # | Item | Status | Source |
|---|---|---|---|
| B1 | Per-dimension supported scale (projects/artifacts/evidence/users) | TBD | Perf/NFR §6 |
| B2 | Availability / uptime SLO | TBD | Perf/NFR §9 |
| B3 | Storage capacity bound (history vs cost) | TBD | Perf/NFR §8 |

## C. Data retention (storage/cost decision only — NOT a governance policy)

| # | Item | Status | Source |
|---|---|---|---|
| C1 | Canonical/audit **retention + hard-delete (incl. GDPR)** durations | TBD — Release-1 retention is a **storage/cost** decision; no governance retention policy is introduced. Calibration §4 proposes defaults (90d ops / project-life+1yr canonical / ≥1yr audit) — **owner to confirm vs. compliance.** | Perf/NFR §8; Data §20.5; Calibration §4 |

## D. Determinism / quality tolerances

| # | Item | Status | Source |
|---|---|---|---|
| D1 | **Bounded-equivalence tolerance** for AI non-determinism (the numeric band; *that* it must be bounded over the governable outputs is fixed) | TBD | Analysis Engine §; Testing §20.1; Calibration §1 proposes ±7/same-band — **owner to confirm** |

## E. Platform / compatibility / tiering (commodity — normal engineering until set)

| # | Item | Status | Source |
|---|---|---|---|
| E1 | Supported-browser matrix | **Owner-confirmed (2026-06-05): evergreen** — latest Chrome / Edge / Safari / Firefox. | Perf/NFR §16 |
| E2 | Accessibility target (WCAG tier) | **Owner-ADOPTED (2026-06-05): WCAG 2.1 AA** (Visual Spec §3). | Perf/NFR §16; Visual Spec §3 |
| E4 | **Visual branding / design-token values** (palette, type, spacing, logo, microcopy) | **Palette FORMALIZED (owner, 2026-06-05, CHG-068)** — canonical Intralign palette in Visual Spec §1.1 (core: charcoal `#111315` · warm-white `#F5F4F0` · orange `#D97A3A`). **Still designer-pending:** type scale/fonts, logo/favicon/OG assets, any component redlines, microcopy. Token contract holds; designer refines via token-swap; lint forbids hardcoded brand. | Visual Spec §1, §4; CHG-067/068 |
| E3 | Paid-tier limits / relaxed quotas — **Tiers 3–5: Pro · Team · Enterprise** | **Partly resolved — Tier 2 (Basic) owner-confirmed 2026-06-05 ($12/mo; Calibration §4c, CHG-057); Tiers 3–5 still TBD.** Canonical tiers: **Free · Basic · Pro · Team · Enterprise** (glossary). Enforcement is **tier-parameterized**, so remaining tiers are added as **config rows in Calibration §4c, not new code**. Illustrative costed ladder: `01_governance/backlog/BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md`. | Perf/NFR §12; MON; Calibration §4c; DL-048; backlog |

## F. Cognition scoring (model formula)

| # | Item | Status | Source |
|---|---|---|---|
| F1 | **CAF / Confidence scoring formula** — how Clarity/Alignment/Feasibility compute to 0–100 and how Confidence aggregates | **TBD BY DESIGN (owner, 2026-06-05, KIA-11):** *mark TBD pending calibration + empirical validation* — do **not** hardcode a formula; scaffold the computation and **calibrate from real data** (consistent with the track-and-tune discipline). Confidence remains **maturity, not probability** (S6). | Capability Matrix gap #1; KIA-11; `models/` |

## What is NOT on this register (already decided — do not re-open)

The **architecture and epistemic model are settled** (DL-043), the **engineering-enablement layer** is ratified (DL-044), **Fast/Deep + the <60s ceiling** are contracted (DL-046), the **cognitive contract-coverage gaps** are closed (DL-047), and **freemium cost-governance enforcement** (the mechanism: per-tier budget gating, graceful degradation, `AI Spend Recorded` telemetry, QA gate) is **contracted** (DL-048) — only the cost *numbers* (A6) remain tunable config. The **< 60-second Time-to-First-MRI** is the **one ratified numeric target.** These are authoritative — build to them; they are not TBD.

---
*This register consolidates every open `TBD – Owner Decision Required` item across the corpus — Fast-Pass project-size envelope (the single highest-priority decision) and latency distribution, Deep-Pass and API latencies, throughput, AI/token budgets, scale/availability/storage, retention+hard-delete, the AI determinism tolerance band, and commodity compatibility/tiering values — into one place so an external team or LLM never silently fills a blank. Each is marked DO-NOT-ASSUME/escalate, with the instruction to build the structure and scaffold the metric while leaving the numeric pass/fail for the owner; the detailed owner-assigned source of truth remains the NFR Acceptance Matrix, and the ratified decisions (architecture, <60s ceiling) are explicitly excluded as already-decided.*
