# CAF / Confidence — v0 Scoring Formula (provisional; calibrate from data)

**Document Type:** Operational scoring formula — **v0 provisional starting point** (realizes the arithmetic the CAF/Confidence/Reliability **v2 models deliberately deferred to "future calibration"**) · **Status:** **DRAFT — owner-ratifiable; NOT canonical.** · **Date:** 2026-06-05
**Why this exists (KIA2-4 follow-up):** the v2 models fix the *meaning, structure, and properties* of the scores and even the **bands** (Calibration §2), but defer the **aggregation arithmetic** — leaving R1 with **no formula to compute or test against** (the engine cannot produce the 0–100 confidence the MRI needs). This document supplies a **v0 formula** that **provably satisfies the ratified doctrine**, is transparent and owner-tunable, and is **calibrated from real data** (same track-and-tune discipline as the DL-048 cost defaults, the Trust Index, and the envelope). **The *canonical* formula remains an owner-calibration decision (Open-TBD F1);** this v0 unblocks R1 build/test until then.

> **Provisional, not canonical.** v0 parameters live in Calibration Defaults §4h and are **owner-review-pending**. This realizes deferred arithmetic; it **redefines no meaning** and introduces **no new dimension, finding, entity, state, probability, or project-health** concept.

> **R1 ratification — DL-086 (2026-07-02).** The owner ratified this v0 as the **R1 formula**: the **band scheme is resolved to 5 bands** (§3), and `p = −0.5`, `ε = 5`, and the impact-magnitude table are **adopted as R1-provisional** (refine from data; structure unchanged). The determinism tolerance is **±7 / same-band** (measured to confirm). Resolves `OPEN_TBD` D1/F1 for R1.

---

## 0. Doctrinal constraints the v0 MUST satisfy (and does)

| Constraint (ratified) | Source | How v0 satisfies it |
|---|---|---|
| Dimensions **co-equal; no static weights; no hierarchy** | Calibration Decision 001 D5 | aggregation is **symmetric** in (C,A,F); the only knob is a **shared** exponent `p` |
| **Constrained aggregation — "between an average and a minimum"**; no simple averaging; no weakest-link domination; none ignored, none dominant by default; **weakness must be felt** | Confidence Model v1 §7 / v2 §; Doctrine Decision 001 D6 | **power mean with p ≤ 1** sits *exactly* between arithmetic mean (p=1) and minimum (p→−∞); a dimension floor `ε` prevents hard weakest-link domination |
| Findings reduce dimensions via **Impact Assessment (sized, located, firm)**; **finding type is not a coefficient** | CAF Scoring v2 §; CAF Assessment §ImpactAssessment | per-dimension = baseline reduced by each affecting finding's **impact magnitude** (from its Impact Assessment), *not* its type |
| Confidence = **confidence in understanding, not probability / health** | Interpretation Doctrine; S6 | output is **understanding maturity**, banded, never rendered as %-likelihood |
| **Reliability qualifies, is not arithmetically combined** | Reliability Model v2 §; Doctrine | Reliability is a **separate qualifier label**, never multiplied into the number |
| **Explainability — reduces to its basis, never a bare number** | Confidence Model §10 | every factor (dim → findings → aggregation → reliability) is traceable; the Π-factors give per-finding contribution |
| **Derived; recompute-appends; two-axis replay** | DL-043 | rule-arithmetic is **exact-replay**; AI-derived inputs are **semantic/±7-band** |

---

## 1. Per-dimension score — Clarity / Alignment / Feasibility (0–100)

Each dimension starts at **100** (no detected weakness) and is reduced **multiplicatively** by each Finding whose **Impact Assessment locates it on that dimension**:

```
Dim_d  =  100 × Π_{ findings i affecting d } ( 1 − impact_i )      , clamped to [0, 100]
```

- **`impact_i ∈ [0,1]`** = the finding's **reducing magnitude**, sized from its **Impact Assessment** (significance × evidence-support × pervasiveness), **not** from its type. v0 sizing table (Calibration §4h, tunable):
  | Assessed magnitude | `impact_i` (v0) |
  |---|---|
  | trivial | 0.03 · minor 0.08 · moderate 0.18 · significant 0.35 · **material 0.55** |
- **Multiplicative (damped-union) accumulation** — many findings saturate toward a floor and **never drive a dimension below 0 or sum past total**; no findings → empty product → **100**. A **material weakness** is, by construction, **felt** (a single 0.55 caps the dimension at 45 = low band).

## 2. Outcome Confidence aggregation (CAF dims → 0–100)

Consolidate the three **floored** dimensions with a **power mean** (the "between an average and a minimum" operator), then qualify:

```
let c,a,f = max(Dim_d, ε)           # ε floor prevents hard weakest-link domination
Conf_raw  =  power_mean_p(c, a, f)
            =  ( (c^p + a^p + f^p) / 3 ) ^ (1/p)     for p ≠ 0
            =  ( c · a · f ) ^ (1/3)                  for p = 0   (geometric mean)
```

- **v0 default `p = −0.5`** (revised from geometric `p=0` after pressure-testing — §7) — symmetric, provably between average and minimum, lets weakness be felt **a touch more strongly than geometric**, aligning with OSLO's "surface over suppress" posture (Calibration §5). **Calibration knob** `p ∈ [−2, 1]` (Calibration §4h): `p=1` = arithmetic (too lax, weakness not felt); `p→−∞` = minimum (weakest-link, too harsh); **`p ∈ [−1, 0]` is the doctrinal sweet spot** (geometric `p=0` is the lax end of it; `p=−0.5` the v0 pick). v0 `ε = 5`.
- **No static weights** — `p` is shared across all three; the dimensions remain co-equal.

## 3. Reliability qualifier (NON-arithmetic) + bands + false-confidence

- **Reliability `R ∈ {High, Moderate, Low}`** is carried **alongside** `Conf_raw`, **never multiplied in** (Reliability Model v2). Presentation: *"Confidence «band» · Reliability «level»."*
- **Band** (owner-ratified 5-band — **DL-086, 2026-07-02**; supersedes the earlier 3-band `0–49/50–74/75–100`): `Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100`, with the **±3-point band-edge guard**. Preserves the pressure-tested **50 & 75** edges and subdivides the extremes to the canonical five bands (Master Spec §20 / Data Model / Interpretation Doctrine). *(False-Confidence below reads on the top band — now "High or Very High".)*
- **False-Confidence (CONF-06):** if band = **High** **and** `R = Low` → **flag the dangerous 4th state** (high confidence on weak supportability). The v0 supports this precisely because confidence and reliability are kept separate.
- **Confidence stages (DL-046):** the same formula runs at **Orientation → Expanded → Validated** with the evidence available at each — the stage is *when*, not a different formula.

## 4. Determinism (two-axis replay)
- **Exact-replay:** the Π reduction and the power-mean arithmetic (given the same inputs).
- **Semantic / ±7-band replay:** the AI-derived inputs (finding detection, `impact_i` sizing) — per the Calibration determinism tolerances (±7 / same-band).

## 5. Acceptance criteria (now testable — closes the F1 "no formula to test" gap)
**Positive:** no findings → all dims 100 → Conf_raw 100 (High); a single **material** weakness on one dimension drops that dim into Low and is **felt** in Conf_raw; identical CAF inputs → identical `Conf_raw` (exact replay); High-conf + Low-reliability → false-confidence flag.
**Negative (must fail):** any **static per-dimension weight**; **simple arithmetic averaging** (p=1) as the shipped default; **weakest-link domination** (one non-zero weak dim collapsing the signal); **Reliability multiplied into the number**; Confidence rendered as a **probability/%-likelihood** or project-health; a dimension exceeding 100 or below 0.

## 6. What is structure vs calibration (and what's still owner-canonical)
- **Structure (this doc, doctrine-fixed):** baseline-minus-impact dimensions; power-mean aggregation; reliability-as-qualifier; band mapping; explainability.
- **Calibration (Calibration §4h, owner-tunable, refine from data):** the `impact_i` magnitude table; the power-mean `p`; the floor `ε`; band edges (already §2).
- **Owner-canonical follow-up (Open-TBD F1):** ratify the v0 as the R1 formula (or amend), then **calibrate `p`, `ε`, and the impact table against real cohorts** — the v0 is the thing the calibration *refines*, not a blank.

## 7. Pressure-test findings (v0 sensitivity, 2026-06-05)

Ran a battery of dimension profiles × `p`, finding-stacking, monotonicity, and edge cases (script reproducible). **Structure validated:** monotonic non-increasing per added finding; saturating in [0,100]; output sits between the arithmetic mean and the minimum for every profile; no weakest-link domination (the `ε=5` floor holds — a true-zero dimension `(100,100,0)` → **37 Low**, not 0). Material weakness lands exactly at the **45** low-band edge by design.

**Two calibration findings (acted on / flagged):**
1. **`p` revised 0 → −0.5.** Geometric (`p=0`) read a *severe* single-dimension weakness `(85,85,20)` as **52 (Medium)** and `(100,100,45)` as **High** — too lax for OSLO's "surface over suppress" posture (Calibration §5). At `p=−0.5`, `(85,85,20)` → **46 (Low)** while a *moderate* single weakness `(85,85,60)` stays **~75 (High/Med edge)** — weakness felt, not over-penalized. So **v0 default = −0.5** (still strictly between average and minimum).
2. **Small-finding stacking compounds — calibration watch-item.** Because dimensions reduce multiplicatively, **many small findings accumulate**: 10 × `minor` (0.08) → dim **43 (Low)**. The *shape* is correct (issues add up, saturating) but the *magnitude* could systematically depress dimensions on finding-heavy projects. **Calibrate the `impact_i` table against real finding-count distributions**; candidate refinements if over-penalizing: lower `minor`/`trivial`, or add mild diminishing-returns on same-dimension stacking. **Do not change the structure** — only the magnitudes.

These are exactly the levers calibration-from-data refines; the v0 is safe to build/test against today.

---
*This v0 scoring formula supplies the CAF/Confidence arithmetic that the ratified v2 models deliberately deferred, so Release 1 has a concrete, testable computation rather than an unbuildable gap — while keeping the canonical formula an owner-calibration decision. It satisfies the ratified doctrine by construction: per-dimension scores start at 100 and are reduced multiplicatively by each finding's Impact-Assessment-sized magnitude (never its type), and the three co-equal dimensions consolidate through a symmetric power mean (default geometric, p=0) that provably sits "between an average and a minimum" with a small floor to prevent weakest-link domination, after which Reliability qualifies the banded result without ever entering the arithmetic and a high-confidence/low-reliability combination raises the false-confidence flag. All numeric parameters (the impact table, the power-mean exponent p, the floor ε, the bands) are tunable calibration to be refined from real data; the structure is doctrine-fixed; and the whole thing is provisional and owner-ratifiable, not canonical.*

**CAF / Confidence v0 Scoring Formula — prepared. Pending Owner Ratification + calibration.**
