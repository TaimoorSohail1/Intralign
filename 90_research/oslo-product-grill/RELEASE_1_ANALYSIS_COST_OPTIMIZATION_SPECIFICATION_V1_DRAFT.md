# RELEASE 1 — Analysis Cost Optimization Specification v1 *(DRAFT)*
**Status:** Draft for owner ratification · **Layer:** `30_engineering/analysis_engine` (engineering-authoritative; **owner ratifies the policy intent**) · **Date:** 2026-07-12
**Commissioned by:** DL-103 §3 (E1–E3). AI authored as scribe — **non-ratifying**.

---

## 0. Why this exists

**Deep Pass is currently specified as a full re-derivation on every run.** A grep of `30_engineering/analysis_engine/` for *prompt caching · incremental · differential · scoped recompute · cache* returns **zero hits**. AE-03 ratifies *"no change → no reanalysis"* — but **nothing ratifies *scoped* reanalysis.**

Consequence (§4c June-2026 price basis, 450k in / 50k out):

| | $/analysis | Analyses/month at the $3 Free ceiling |
|---|---|---|
| Today — brute-force | $0.260 | **12** |
| + **E1** prompt caching | $0.122 | 25 |
| + **E2** scoped recompute | $0.068 | 44 |
| **E1 + E2** | **$0.040** | **~74 (6.4×)** |

**No model change. No quality trade.** DL-103 suspends §4c's numeric basis until cost-per-analysis is re-derived **from the real engine** — so this specification is a **prerequisite for setting any tier number.**

---

## 1. E1 — Prompt caching / KV-cache reuse

**The plan corpus is stable between runs. Only the delta changes.**

**Rule.** The analysis engine SHALL cache the stable portion of the model input across runs and pay full price only for what has changed.
- **Rented providers:** provider prompt-caching (cached input billed at a fraction of list).
- **Local runtime (DL-069 — primary):** **KV-cache reuse** across runs behind the same `/services/llm_provider` seam.

**Scope.** **Seam-only.** Confined to `code/backend/services/llm_provider/*`. The three call sites (**Perceive** extraction, **Infer** synthesis/generation, **Infer** findings) are **unchanged** — consistent with DL-069 condition 1.

**Epistemic impact: NONE.** Caching changes *what is paid for*, never *what is computed*. Determinism (ADR-0004, recorded fixtures) is unaffected.

**Release:** **R1 — build now.** No product surface, no doctrine impact, no risk.

---

## 2. E2 — Incremental / scoped recompute  ⚠️ *carries an epistemic hazard; the constraint below is binding*

### 2.1 The hazard — state it before the mechanism

> **A scoped recompute that updates only PART of the read produces an internally INCONSISTENT assessment** — some CAF dimensions reflecting the new plan, others the old. **That is worse than honest staleness, because it is silently mixed.** OSLO's entire claim is a **coherent** read. A half-updated read is a **quiet lie**.

### 2.2 The binding constraint — **scope the LLM stages; ALWAYS run Evaluate in full**

**DL-069 condition 1 (ratified): *"Evaluate remains rule-arithmetic (no LLM)."*** So the expensive stages are **Perceive** (extraction) and **Infer** (synthesis / findings). **Evaluate is cheap and deterministic.**

> **BINDING:**
> - **Perceive and Infer MAY be scoped** to the changed artifact and its dependency closure.
> - **Evaluate MUST ALWAYS run in FULL**, over the **complete** claim set.
>
> The assessment is therefore **always derived from the whole plan** — never partially stale — while the expensive re-reading is scoped to what actually moved. **The cheap stage is the one that guarantees coherence.**

**Without this constraint, E2 is an epistemic hazard and MUST NOT ship.**

### 2.3 Dependency closure

A scoped run recomputes: the **changed artifact**, plus every **claim** whose provenance touches it, plus every artifact those claims bind to (transitively).

**Soundness rule — widen, never narrow.** If the closure is uncertain, **widen it**. A scoped run that is too wide is merely expensive. **A scoped run that is too narrow is wrong** — and wrong is unaffordable.

### 2.4 Acceptance criterion (the QA gate that makes E2 safe)

> **EQUIVALENCE:** for any project state, a **scoped** Deep run MUST produce an assessment **identical** to what a **full** Deep run would produce for that same state.

This is directly testable against recorded fixtures (ADR-0004). **If equivalence fails, the scoping is unsound and the run MUST fall back to a full re-derivation.** Equivalence is a **P1 gate**, not a performance target.

**Release:** **R1, conditional on §2.2 and §2.4.** Without them → **R2.**

---

## 3. E3 — Evidence coalescing  *(this one has genuine Alpha urgency)*

### 3.1 The problem

**CR-2 (DL-102, load-bearing):** evidence-seeking is **never metered**. **CRR-04:** every reviewer response **triggers an Extended Analysis**. So five reviewers answering = five runs, silently consuming the inviter's analysis budget.

**CR-2 then holds in letter and dies in practice:** users learn that **asking for evidence costs them their own read**, and stop asking — killing the loop DL-102 exists to protect.

### 3.2 The rule

**Reviewer responses arriving within the coalescing window SHALL settle into ONE analysis run.** The existing coalescer (§4c: *"Deep concurrency 1 + coalescing on"*) is extended to CRR responses.

**This is also the correct UX:** you do not want the read churning as each reviewer replies — you want it to **settle once they have answered**.

### 3.3 CR-2 vs the budget gate (DL-103 / §4c *"the binding governor"*)

When evidence arrives **after** the budget has gated:
> **Record the evidence. Defer the run. Disclose honestly.**
> The attestation is **appended immediately** (append-only, CR-2 honoured — evidence is **never refused**). The **run defers**, with an honest line: *"Priya's answer is recorded. Your read will update when your monthly analysis budget resets, or on upgrade."*
> **Evidence is never lost. Cost is bounded. The product is honest about what it has not yet done.**

**Release:** **R1 — build now.** **C14 ("CAF Review Requests show stakeholder participation") is an Alpha exit criterion.** Without E3, CRR is validated against a broken incentive.

---

## 4. Telemetry — this is what unblocks every suspended number

§4c is explicit: *"Numbers are estimate-based starting defaults; **the contracted cost telemetry replaces them with measured medians**."* **Cost-per-analysis cannot be re-derived from a specification — only from measured usage.** Emit on the contracted `AI Spend Recorded` event:

| Metric | Unblocks |
|---|---|
| **Tokens per Deep run** (pre/post E1, pre/post E2) · **cache-hit rate** | The **real cost-per-analysis** → the tier numbers DL-103 suspended |
| **Analyses per user per month** (distribution, not mean) | **Free / Basic monthly analysis budgets** |
| **Fixes per session** (distribution) | **UP-APPLY threshold** — *above activation, below power use* (DL-103 §7d) |
| **Chat messages per day** | Validates uncapping chat (D126) |
| **CRR responses per project · runs they trigger** | **Free CRR cost ceiling** (B-1) |
| **Coalescing ratio** (qualifying events per run) | **OD-10 — the coalescing window** |
| **Actual $ per active user per month** | The **~$3 Free posture** (DL-048) |

**At R1/R2 audience scale (<5, then 10–20 users) budgets SHALL NOT be enforced** — the cost is ~$15–60/month, and **enforcement would corrupt the very signal Alpha exists to buy.** **Instrument; do not gate.** Enforcement begins when it matters: **Beta (50+ users)**.

---

## 5. Non-goals

Model selection (DL-069) · tier numbers (DL-103 — suspended, re-derived from §4 telemetry) · billing/entitlement · **any change to what OSLO computes**. **E1–E3 change what is *paid for* and what is *re-read* — never what is *concluded*.**

## 6. Acceptance criteria

1. **AC-1 (E1):** cache-hit rate emitted; measured cost-per-Deep-run falls; **assessment output unchanged** against recorded fixtures.
2. **AC-2 (E2 — P1):** **EQUIVALENCE** — scoped run ≡ full run for the same state. On failure → **fall back to full re-derivation**.
3. **AC-3 (E2 — P1):** **Evaluate always runs in full.** A scoped Evaluate is a **build-breaking** defect.
4. **AC-4 (E3):** N reviewer responses inside the window produce **exactly one** analysis run.
5. **AC-5 (E3 — P1, CR-2):** a reviewer's evidence is **recorded even when the budget has gated**; the run **defers**; the evidence is **never refused**.
6. **AC-6:** every §4 metric is emitted on `AI Spend Recorded`.
7. **AC-7:** determinism (ADR-0004) preserved throughout.

## 7. Open — owner decision required

**OD-10 coalescing window** (settle/idle-based recommended; the Deep Pass spec already lists **`manual`** as a qualifying trigger, so *"Update now"* exists and is free on every tier per DL-103 §7d-bis) · **CRR coalescing window** (may differ from OD-10 — reviewers answer over hours, not seconds) · **the R1 terminology collision** (see below).

## 8. ⚠️ Terminology collision — register it

**"R1" is overloaded.** **DL-076 (ratified)** defines **R1–R5 as *audience-scale* rungs** (*"R1 = owner + <5 users; R2 = 10–20; 50+ = the Beta gate"*), while **every specification in the repository uses `RELEASE_1_*` to mean *Release 1, the product*.** Same token, two meanings, in the same sentences.
**Recommend: add to the DL-053 Disambiguation Register** with a canonical distinction (e.g. *Release 1* vs *Audience Rung R1*).
