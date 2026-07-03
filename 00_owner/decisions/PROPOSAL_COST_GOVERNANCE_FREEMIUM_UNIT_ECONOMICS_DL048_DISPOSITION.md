# DL-048 (DISPOSITION DRAFT) — Cost Governance / Freemium Unit Economics (Tier-1 Token-Cost Enforcement)

**Status:** **RATIFIED — DL-048 (2026-06-05); applied across contracts / calibration / NFR / matrix / register; CHG-055.** Owner-directed (owner: "unit economics / token-cost management for tier-1 freemium users *will need to be enforced* for the release") and owner-selected **Balanced (~$3/mo)** posture. Per `CLAUDE.md`, only the owner ratifies.

> **Why a Decision (not just config):** today, free-tier cost control lives as **commodity billing** (`MON-01…04`, Category C, DL-043 J) plus a **soft NFR principle** (NFR §12 "depth is gated to protect unit economics") with the actual budgets `TBD – Owner Decision`. It is **stated, not enforced** — no contracted obligation on the spend-bearing engine, no QA gate, no cost observability. This is the same class of gap DL-046 closed for the 60s target. Making it an *enforced, tested, observable* criterion touches the cognitive contracts (Wave B / Wave S) and adds an NFR gate, so it is a Decision, not a silent setting change. The **values** are owner-set config; the **enforcement** is contracted.

---

## The principle: separate the number from the mechanism

- **The cap value is configuration** — tier-keyed, owner-set, env-bound (lives in `RELEASE_1_CALIBRATION_DEFAULTS_V1.md`; tracked as TBD in `OPEN_TBD_REGISTER.md` until the owner sets it). Tunable without a code change.
- **The enforcement is the contract** — read the cap from config, meter spend per run / per user / per tier, **gate or degrade gracefully** when a cap is hit (cap depth / defer Deep Pass / surface "limit reached" — never silent overspend or runaway re-analysis), and **emit a cost event**. This is behavior the engine must guarantee regardless of the number plugged in.

Today some caps are written as fixed structural rules (`single active project` on free). Recommendation: make **even those config-driven** (tier capability flags) so the whole freemium envelope is **one tunable surface**, not part-config / part-hardcoded.

---

## Part A — Enforcement obligation (contract; Fast/Deep engine)

Add a **cost-governance obligation** to the analysis-engine contracts (**Wave B `IC-WB-INFER`/`IC-WB-EVAL`** and **Wave S `IC-WS-SYNTH`**, where the tokens are actually burned):

- Every **Fast Pass** and **Deep Pass** run operates within a **per-tier token budget** read from config.
- **Per-run cap exceeded → graceful degradation**, not silent overspend: Fast Pass truncates/degrades scope; Deep Pass coalesces or defers. The user is told a limit was reached.
- **Per-user rollup cap exceeded (daily / monthly) → gate** further AI spend for that user/tier until the window resets; surface upgrade prompt (commodity MON).
- Free tier enforces: single active project, **single active Deep run + event coalescing** (no runaway re-analysis), daily fix cap, daily chat cap — all as **tier-keyed config**.
- **Model routing is tier-keyed config** (the single biggest cost lever): free tier routes to the cheap model class.

This adds **no new responsibility and no new object** — it is a bounded behavior of the existing Infer/Evaluate/Synthesize engines plus the existing recompute/coalescing backbone (`IC-WA-00R`). The billing layer (MON) reads the **same** config; it does not own enforcement.

## Part B — QA acceptance gate

- **Positive:** a free-tier run on the supported envelope stays **≤ the configured per-run and per-user budgets**; a representative-fixture test asserts cost-per-free-user ≤ the owner-set monthly ceiling.
- **Negative (where assumptions get caught):** reject **budget bypass**; reject **runaway re-analysis** (coalescing must hold — a burst of edits collapses to ≤ the configured Deep concurrency); reject **silent overspend** (over-budget must degrade/gate **and** emit, never proceed quietly); reject **wrong-tier routing** (free run on a full-quality model when config says cheap).

## Part C — Cost observability

Emit a first-class **`AI Spend Recorded`** event (per the Observability Governance two-axis-replay model): **tokens + estimated cost, per run, per user, per tier, per mode (fast/deep), per model**. Add a **trust/drift signal** when a tier exceeds its budget. This is what lets the owner **replace the starting estimates with measured medians** in the first weeks and re-tune — the reason the values can start conservative.

## Part D — Proposed starting config (Balanced ~$3/mo posture — owner-selected)

Tier-keyed; **Free / Tier 1**. Values are **proposed defaults**, owner-ratifiable, sized from token *estimates* (not yet measured runs) against the Fast-Pass envelope (≤20 artifacts / ~50k words ≈ ~67k tokens evidence). All land in Calibration Defaults on ratification and as TBD-resolved entries in the Open-TBD Register.

| Config knob (tier-keyed) | Free / Tier 1 default | Basis |
|---|---|---|
| Max active projects | **1** | structural (existing) |
| Model routing | **nano (extraction) / mini (synthesis+eval); Haiku fallback** | biggest cost lever |
| Fast Pass per-run token cap (→ degrade) | **150,000** | envelope + headroom (posture-independent) |
| Deep Pass per-run token cap (→ coalesce/defer) | **600,000** | bounds worst case |
| Deep concurrency | **1** + coalescing **on** | structural (existing) |
| Deep runs / day | **2** | gate the expensive path |
| Suggested fixes / day | **5** | existing "daily allowance" |
| Chat messages / day | **20** | bound interactive burn |
| Daily token budget / user | **500,000** | burst smoothing |
| **Monthly token budget / user (hard rollup)** | **4,000,000** | the binding governor |
| Monthly $ ceiling / user (alert KPI) | **~$3.00** | business target |

**Cost basis (June 2026 pricing, verified):** GPT-4.1 $2/$8 · GPT-4.1-mini $0.40/$1.60 · GPT-4.1-nano $0.10/$0.40 · Sonnet 4.6 $3/$15 · Haiku 4.5 $1/$5 per 1M tokens (in/out).
- Per-run estimate: **Fast Pass** ~120k tok (100k in / 25k out) = **$0.08 mini** ($0.40 GPT-4.1); **Deep Pass** ~500k tok (400k in / 100k out) = **$0.32 mini** ($1.60 GPT-4.1 / $2.70 Sonnet).
- **Headline:** one *full-quality* Deep Pass (~$1.6–2.7) alone consumes most of a $3 budget → free-tier viability depends on **cheap routing + Deep-gating**, not on any single numeric cap.
- Monthly rollup check: 4.0M tok/mo blended (2.4M nano-heavy in / 1.6M mini out) = **~$3.04 worst-case if maxed every day**; median free user far below. Hits the ~$3 target. (Pure-mini routing ≈ $3.52 — keep nano on extraction to stay at ~$3.)

## Part E — Tier parameterization (forward scope)

Enforcement is **parameterized by tier**, not hard-coded to "free vs paid." `OSLO_CAPABILITY_MATRIX_V2` note 10 records **paid tiers beyond Free are currently undefined** — that remains an open scope item. When paid tiers are defined they become **additional config rows**, not new code. (Out of scope for this Decision; flagged.)

---

## Disposition / conditions
- **Disposition:** **Accepted** (owner ratified 2026-06-05; Balanced ~$3/mo posture). All parts A–E adopted.
- **No architecture changed;** no new responsibility/object. Adds a contracted behavior (A), a QA gate (B), an observability event (C), and proposed config (D) to the existing engines.
- **Supersedes:** nothing. Extends the DL-043/046/047 foundation by making freemium unit economics enforced rather than implicit.
- **Relation to commodity:** MON-01…04 remain commodity billing; they **consume** the same tier config. This Decision adds the *spend governor* on the cognitive engine, which billing alone cannot provide.

## Owner decision required
- [ ] **A:** Adopt the cost-governance enforcement obligation on Wave B + Wave S (per-run degrade; per-user gate; tier-keyed routing; coalescing).
- [ ] **B:** Adopt the QA acceptance gate (free-tier ≤ ceiling; negatives: bypass / runaway / silent-overspend / wrong-tier-routing).
- [ ] **C:** Adopt the `AI Spend Recorded` observability event + over-budget trust signal.
- [ ] **D:** Approve the Conservative starting defaults (Part D table) as proposed Calibration Defaults + Open-TBD-resolved values — or amend any value.
- [ ] **E:** Note paid-tier limits remain an open scope item (not resolved here).
- [ ] On ratification: amend Wave B / Wave S (and Wave I for chat/fix caps) contracts; add Calibration Defaults §; resolve the cost rows in the Open-TBD Register; add a Build/Test/Observe matrix row (`MON-COST` cognitive-enforcement) + NFR §12 gate; re-run conformance; record DL-048 + changelog (CHG-055).

---
*This draft makes tier-1 freemium unit economics an **enforced, tested, observable** release criterion rather than a soft NFR principle plus commodity billing. It separates the cap **value** (tier-keyed, owner-set, env-bound config, TBD-tracked) from the **enforcement mechanism** (a contracted cost-governance obligation on the Fast/Deep analysis engine: per-run graceful degradation, per-user/tier budget gating, coalescing against runaway re-analysis, tier-keyed model routing), backed by a QA acceptance gate with negative tests (no bypass, no runaway, no silent overspend, no wrong-tier routing) and an `AI Spend Recorded` cost-observability event that lets the owner re-tune from measured data. It proposes a Balanced (~$3/active-free-user/month) starting default set, reconciled against verified June 2026 token pricing, and flags that paid tiers remain an open scope item. It edits no ratified contract and routes ratification and application to the owner.*

**DL-048 (DRAFT) — Cost Governance / Freemium Unit Economics prepared. Pending Owner Ratification.**
