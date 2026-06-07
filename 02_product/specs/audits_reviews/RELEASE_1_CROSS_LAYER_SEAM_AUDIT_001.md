# Release 1 — Cross-Layer Seam Audit 001 (the "UP-3 class")

**Document Type:** Owner-directed audit (Framework 001A Review schema) · **Status:** **APPLIED — S1–S3 fixed via the shared limit-reached interaction rule; S4 reconciled (stale); S5/S6 flagged for owner. CHG-066.** · **Date:** 2026-06-05
**Question (owner-directed):** *The 2nd-project gap (CHG-065) was a behavior defined in two layers (API `422` + UP-3) with the connecting surface unspecified. Are there **other** issues of that class in R1?*
**Defect class audited:** a behavior is specified in one layer (**API error / monetization rule / doctrine**) but the **connecting UX surface/affordance is unspecified**, so a builder can implement each half correctly yet break the end-to-end behavior (most damagingly: disable/hide an affordance and **suppress an upgrade trigger**, or surface a raw error).
**Sources:** `RELEASE_1_API_CONTRACT_SPECIFICATION_V1` (error taxonomy §) · `12_freemium_tier_behavior_logic` (UP-1…8) · `OSLO_CAPABILITY_MATRIX_V2` (open-gaps list) · Finding/Recommendation Panel + Chat + Project-Overview UX specs.

---

## 0. Verdict

**Yes — UP-3 was not isolated. The same gap exists at every *other* monetization-limit moment** (fix cap, chat cap, deep-runs cap, monthly budget). Each has an API gate (`429`) and a UP trigger (UP-1/2/5/6), but the **UX surfaces specify no cap-reached behavior** — the Finding Panel, Recommendation Panel, and Chat specs contain **zero** limit/allowance/upgrade handling. So the same risk CHG-065 just fixed for projects is live for fixes, chat, and analysis depth. Three secondary seam-class items are also noted. **No issue is Critical; the limit-moment cluster is the high-value fix** because each is a conversion trigger that a builder could silently suppress.

## 1. Findings — monetization-limit seams (same class as UP-3; confirmed)

| # | Seam | Defined where | UX surface | Gap |
|---|---|---|---|---|
| **S1** | **Daily fix cap** (UP-1) | API `429` (free-tier suggested-fix daily limit) + MON-02 + UP-1 | Finding/Recommendation Panel (where Suggested Fixes apply) | **No cap-reached behavior specified.** Does "Apply fix" stay enabled→gated→UP-1, or get disabled/hidden? Matrix note #7 itself says *"treat fixes and fix-limits as one design"* — not yet done at the surface. |
| **S2** | **Daily chat cap** (UP-2) | `429` + MON-03 + UP-2 | OSLO Chat spec | **No cap-reached behavior.** Does chat input stay enabled→gated→UP-2, or disabled? |
| **S3** | **Deep-runs/day cap (UP-5) + monthly budget gate (UP-6)** | DL-048 (degrade/gate) + UP-5/6 | analyze/refresh / Project Overview | **No cap-reached behavior.** DL-048 defines graceful degradation/gating but the UX moment isn't wired to UP-5/UP-6 (what the user sees when deep analysis is capped). |

**All three are the UP-3 defect exactly:** API/behavior defined, connecting surface unspecified → risk of (a) a disabled/hidden affordance that **suppresses the upgrade trigger**, or (b) a raw error shown instead of the value-framed prompt. **The fix is the same pattern CHG-065 applied:** the affordance **stays enabled**, the attempt is **gated server-side (`429`)**, and the surface presents the **UP prompt with resolutions** (upgrade; and where applicable wait-for-reset / archive / cap-depth).

## 2. Findings — other seam-class items (secondary)

| # | Seam | Status | Note |
|---|---|---|---|
| **S4** | **Notification surface vs Matrix gap #5** | **STALE gap** | Matrix #5 says "no notification object or surface," but `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1` **exists** (and §18 has a Notification object). The *gap note* is out of date — reconcile it, and confirm the CRR/comment/mention → notification wiring is actually expressed (the "how a reviewer learns a request is waiting" seam). |
| **S5** | **Concurrency / multi-user edit conflicts** (Matrix #9) | **OPEN** | Collaboration + direct editing imply simultaneous edits; no conflict/locking model. **Low real risk for R1** (owner's single-user validation vehicle) but a genuine seam — flag for when multi-user (R2 Team) lands. |
| **S6** | **Confidence ↔ probability UI guard** (Matrix #15) | **OPEN (epistemic)** | Doctrine asserts confidence ≠ probability; Wave E carries epistemic labels/band guards, but **no explicit UI rule prevents the 0–100 from being read/rendered as a probability.** A presentation-layer epistemic-safety guard. |

## 3. Correctly NOT this class (excluded)
- **Resolved this session:** Matrix #6 external-reviewer (DL-049), #8 share-link security (P7), #13 supported-project-sizes (CHG-056), #10 paid-tiers partly (Free/Basic defined). 
- **Different defect class (under-specified *computation*, not interaction seams) — out of scope here:** CAF scoring methodology (#1), confidence thresholds (#2), template catalog (#3), guided-intake flow (#4), AC coverage (#11), retention policy (#12). These are real but are *content-undefined*, not *cross-layer-seam*, items.

## 4. Concerns
- **Conversion leakage is silent.** A suppressed limit-moment trigger produces no error and no signal — it just quietly fails to convert. Only the seam spec prevents it.
- **Consistency multiplies value.** Specifying the limit-moment pattern **once** (a shared "limit-reached interaction" rule) and referencing it from each surface is cleaner than four ad-hoc handlers — mirrors how UP-1…8 already share the §4d/§4e timing pattern.

## 5. Recommendation (owner-routed; nothing redefined)
1. **Apply the UP-3 pattern to S1–S3** (the confirmed cluster): each limit-bearing affordance (Apply-fix, Chat-send, Analyze/Deep) **stays enabled**, attempt **gated (`429`)**, surface presents the **matching UP prompt + resolutions**; **never disabled/hidden**. State it as **one shared "limit-reached interaction" rule** in the freemium behavior spec + a note on each UX spec (Finding/Recommendation Panel, Chat, Project Overview) + matrix anchors — exactly the CHG-065 shape.
2. **S4:** reconcile the stale Matrix gap #5 (notification surface exists) and confirm the reviewer/comment/mention → notification wiring.
3. **S5:** record for R2 Team (multi-user) — low R1 risk; no action needed for the single-user validation release.
4. **S6:** add the explicit UI guard ("never render Confidence as a probability / %-likelihood") to the epistemic-safety presentation rules (reinforces Wave E).

## 6. Status
**FINDINGS RECORDED — one confirmed same-class cluster (S1–S3, the monetization-limit moments), one stale gap (S4), two lower-risk seams (S5 multi-user, S6 epistemic UI guard). No Critical.** Routes to owner; the S1–S3 fix is the direct continuation of CHG-065.

---
*This owner-directed audit generalizes the CHG-065 second-project gap into its defect class — a behavior specified at the API/monetization/doctrine layer with the connecting UX surface left unspecified — and finds the same gap at every other monetization-limit moment: the daily fix cap (UP-1), daily chat cap (UP-2), and deep-runs/budget caps (UP-5/UP-6) all have an API `429` gate and a UP upgrade trigger but no cap-reached behavior in the Finding Panel, Recommendation Panel, Chat, or Project-Overview specs, so a builder could disable the affordance and silently suppress the upgrade trigger or surface a raw error. It recommends applying the CHG-065 pattern as one shared "limit-reached interaction" rule (affordance stays enabled, attempt gated, value-framed prompt with resolutions, never hidden), flags a stale notification gap (the surface now exists), and notes two lower-risk seams (multi-user edit-conflict handling for R2 Team, and an explicit UI guard against rendering Confidence as a probability), while excluding both the items already resolved this session and the different class of under-specified-computation gaps. Nothing is redefined; fixes route to the owner.*

**Release 1 Cross-Layer Seam Audit 001 complete. Pending Owner Direction.**
