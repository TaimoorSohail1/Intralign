# Release 1 Analysis Cost Optimization Specification v1

**Type:** Analysis Engine Specification (cost mechanics — E1/E2/E3)
**Status:** Realization of **DL-105** (commissioning decision). **Engineering-authoritative; the owner ratified the policy intent.** · **Date:** 2026-07-12
**Implements (does not redefine):** **DL-105** *(authority)* · DL-103 §3 · DL-069 (LLM provider seam; *Evaluate remains rule-arithmetic*) · DL-102 (**CR-2**) · DL-048 (cost governance) · AE-03 (event-driven recompute) · ADR-0004 (determinism)
**Authoritative inputs:** `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` · `DEEP_PASS_STAGE_IO_SPEC.md` · `FAST_VS_DEEP_PASS_COMPARISON.md` · `ACCEPTANCE_CRITERIA.md` · `RELEASE_1_CALIBRATION_DEFAULTS_V1.md` §4c · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` (`AI Spend Recorded`)

> **Scope guardrail.** This specification changes **what is paid for** and **what is re-read** — **never what is concluded.** It introduces **no scoring formulas, weights, percentages or thresholds**, and **no new entities, states or events**. All quantitative values are **`TBD – Owner Decision Required`** and are re-derived from measured telemetry (§4), never from this document. **Where any conflict arises, the Planning Intelligence Specification wins.**

---

## 0. Why this exists

**Deep Pass is specified as a full re-derivation on every run.** A search of this directory for *prompt caching · incremental · differential · scoped recompute · cache* returns **zero hits**. **AE-03** ratifies *"no change → no reanalysis"* — but **nothing ratifies *scoped* reanalysis.** A user fixes one line in one artifact and the engine re-reads the entire corpus and regenerates everything.

Effect on cost-per-analysis (§4c June-2026 price basis; 450k in / 50k out):

| | $ / analysis | Analyses / month at the $3 Free ceiling |
|---|---|---|
| Today — brute-force | $0.260 | **12** |
| **+ E1** prompt caching | $0.122 | 25 |
| **+ E2** scoped recompute | $0.068 | 44 |
| **E1 + E2** | **$0.040** | **~74 (6.4×)** |

**No model change. No quality trade.** **DL-103 suspended §4c's numeric basis** until cost-per-analysis is re-derived **from the real engine** — so this specification is a **prerequisite for setting any tier number.**

---

## 1. E1 — Prompt caching / KV-cache reuse

**The plan corpus is stable between runs. Only the delta changes.**

**Rule.** The engine SHALL cache the stable portion of the model input across runs and pay full price only for what has changed.
- **Rented providers:** provider prompt-caching (cached input billed at a fraction of list).
- **Local runtime (DL-069 — the primary LLM):** **KV-cache reuse** across runs.

**Scope — seam-only.** Confined to `code/backend/services/llm_provider/*`. The three call sites — **Perceive** extraction, **Infer** synthesis/generation, **Infer** findings — are **unchanged** (DL-069 condition 1).

**Epistemic impact: NONE.** Caching changes what is *paid for*, never what is *computed*. **Determinism (ADR-0004) is unaffected** — recorded fixtures remain valid.

---

## 2. E2 — Incremental / scoped recompute

> ### 2.1 The hazard — stated first, because the constraints only make sense against it
> **A scoped recompute that updates only PART of the read produces an internally INCONSISTENT assessment** — some CAF dimensions reflecting the new plan, others the old. **This is worse than honest staleness, because it is silently mixed.** OSLO's entire claim is a **coherent** read. **A half-updated read is a quiet lie.**

### 2.2 BINDING — scope the LLM stages; **always run Evaluate in FULL**

**DL-069 condition 1 (ratified):** ***"Evaluate remains rule-arithmetic (no LLM)."*** The expensive stages are therefore **Perceive** (extraction) and **Infer** (synthesis / findings). **Evaluate is cheap and deterministic.**

- **Perceive and Infer MAY be scoped** to the changed artifact and its dependency closure.
- **Evaluate MUST ALWAYS run in FULL**, over the **complete** claim set.

The assessment is therefore **always derived from the whole plan** — never partially stale — while the expensive re-reading is scoped to what actually moved. **The cheap stage is the one that guarantees coherence.**

**A scoped Evaluate is a build-breaking defect.**

### 2.3 BINDING — EQUIVALENCE (P1 gate)

> **For any project state, a SCOPED Deep run MUST produce an assessment IDENTICAL to what a FULL Deep run would produce for that same state.**

Directly testable against **recorded fixtures (ADR-0004)**. **On failure, the run MUST fall back to a full re-derivation.**
**Equivalence is a P1 correctness gate, not a performance target.**

### 2.4 Dependency closure — **widen, never narrow**

A scoped run recomputes: the **changed artifact**; every **claim** whose provenance touches it; and every artifact those claims bind to, **transitively**.

**If the closure is uncertain, WIDEN it.** A closure that is **too wide is merely expensive**. A closure that is **too narrow is wrong — and wrong is unaffordable.**

### 2.5 Ship condition

**E2 MUST NOT ship without §2.2 and §2.3.** Absent either, E2 is an **epistemic hazard** and is deferred.

---

## 3. E3 — Evidence coalescing

### 3.1 The problem

**CR-2 (DL-102 — load-bearing):** evidence-seeking is **never metered**.
**CRR-04:** every reviewer response **triggers an Extended Analysis**.
**§4c:** a Free user's monthly governor permits only a bounded number of Deep runs.

So five reviewers answering = **five runs**, silently consuming the inviter's analysis budget. **CR-2 then holds in letter and dies in practice:** users learn that **asking for evidence costs them their own read**, stop asking, and **the loop DL-102 exists to protect dies.**

### 3.2 The rule

**Reviewer responses arriving within the coalescing window SHALL settle into ONE analysis run**, extending the existing coalescer (§4c: *"Deep concurrency **1** + coalescing **on**"*; `DEEP_PASS_STAGE_IO_SPEC`: *"rapid events are coalesced"*).

**This is also the correct UX.** The read should not churn as each reviewer replies — it should **settle once they have answered**.

### 3.3 CR-2 vs the binding budget governor — **record · defer · disclose**

When evidence arrives **after** the budget has gated:

- **Record the evidence.** The attestation is **appended immediately** — append-only, **CR-2 honoured: evidence is NEVER refused.**
- **Defer the run.** Cost stays bounded.
- **Disclose honestly.** *"…recorded. Your read will update when your monthly analysis budget resets, or on upgrade."*

**Evidence is never lost. Cost is bounded. The product stays honest about what it has not yet done.**

---

## 4. Telemetry — **instrument; do not gate**

`RELEASE_1_CALIBRATION_DEFAULTS_V1` §4c is explicit: *"Numbers are estimate-based starting defaults; **the contracted cost telemetry replaces them with measured medians**."*
**Cost-per-analysis cannot be re-derived from a specification — only from measured usage.**

Emit on the contracted **`AI Spend Recorded`** event:

| Metric | Unblocks |
|---|---|
| **Tokens per Deep run** (pre/post E1, pre/post E2) · **cache-hit rate** | The **real cost-per-analysis** → every tier number DL-103 suspended |
| **Analyses per user per month** (distribution, not mean) | Free / Basic **monthly analysis budgets** |
| **Fixes per session** (distribution) | The **UP-APPLY threshold** — *above activation, below power use* (DL-103 §7d) |
| **Chat messages per day** | Validates uncapping chat (D126) |
| **CRR responses per project · runs they trigger** | The **Free CRR cost ceiling** |
| **Coalescing ratio** (qualifying events per run) | **OD-10** — the coalescing window |
| **Actual $ per active user per month** | The **~$3 Free posture** (DL-048) |

**At audience rungs R1 (<5 users) and R2 (10–20) budgets SHALL NOT be enforced.** The cost is ~$15–60/month, and **enforcement would corrupt the very signal Alpha exists to buy.** **Enforcement begins at Beta (50+ users).**

---

## 5. Acceptance criteria

| # | Criterion | Class |
|---|---|---|
| **AC-1** | **E1:** cache-hit rate emitted; measured cost-per-Deep-run falls; **assessment output unchanged** against recorded fixtures | — |
| **AC-2** | **E2: EQUIVALENCE** — scoped run **≡** full run for the same state. On failure → **fall back to full re-derivation** | **P1** |
| **AC-3** | **E2: Evaluate always runs in FULL.** A scoped Evaluate is **build-breaking** | **P1** |
| **AC-4** | **E3:** N reviewer responses inside the window produce **exactly one** analysis run | — |
| **AC-5** | **E3 / CR-2:** a reviewer's evidence is **recorded even when the budget has gated**; the run **defers**; the evidence is **NEVER refused** | **P1** |
| **AC-6** | Every §4 metric is emitted on `AI Spend Recorded` | — |
| **AC-7** | **Determinism (ADR-0004) preserved** throughout | **P1** |

---

## 6. Non-goals

Model selection (**DL-069**) · tier numbers (**DL-103** — suspended; re-derived from §4 telemetry) · billing / entitlement · **any change to what OSLO computes or concludes**.

---

## 7. Open — `TBD – Owner Decision Required`

| # | Item |
|---|---|
| **OD-10** | The **coalescing window** (settle/idle-based recommended). *`DEEP_PASS_STAGE_IO_SPEC` already lists **`manual`** as a qualifying trigger — so "Update now" exists and is **free on every tier** (DL-103 §7d-bis).* |
| **OD-CRR** | The **CRR coalescing window** — **may differ from OD-10**; reviewers answer over **hours**, not seconds. |
| — | **Every tier number** — re-derived from §4 telemetry, **never from this document**. |
