# Release 1 Model Judgment Evaluation v1

**Type:** Analysis Engine Specification (model qualification — the DL-069 gate)
**Status:** Realization of **DL-106** (commissioning decision). **Engineering-authoritative; the owner ratifies the bar.** · **Date:** 2026-07-12
**Implements (does not redefine):** **DL-069** *(authority — internal Gemma as primary LLM; three LLM call sites; Evaluate is rule-arithmetic)* · **DL-103 §1** *(never tier judgment quality)* · ADR-0004 (determinism / recorded fixtures) · DL-056 (the five curated templates)
**Authoritative inputs:** `ACCEPTANCE_CRITERIA.md` (**AC-V1/V2/V3**) · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` · `FAST_PASS_STAGE_IO_SPEC.md` · `DEEP_PASS_STAGE_IO_SPEC.md` · `analysis_enums` · `10_product/experience/templates/`

> **Scope guardrail.** This specification defines **how a candidate model is qualified for OSLO's cognition** — it does **not** select a model, set a quality bar, or change what OSLO computes. **The bar is an owner decision.** No formulas, weights, percentages or thresholds are introduced; every numeric bar is **`TBD – Owner Decision Required`**.

---

## 0. Why this exists — and why the bar just went up

**DL-069 (ratified) made an internal Gemma on a local Llama runtime the primary LLM**, demoting OpenAI/Anthropic to a **disabled-by-default fallback**, expressly to remove external token cost and data egress. **Whether the local model can carry OSLO's *judgment* has never been tested.** It is an **empirical** question and cannot be settled on paper.

**DL-103 §1 raised the bar.** Before it, an escape hatch existed — *"Gemma for Free; full-quality GPT-4.1 for Pro"* (literally §4c's T3 routing row). **DL-103 prohibits tiering judgment quality**, because a tiered model would make **Reliability a function of the billing plan**. Therefore:

> **The qualified model must clear the bar for the BEST-PAYING customer, not the cheapest free one.** Whatever is chosen, **everyone gets it.**

---

## 1. What is evaluated — **per call-site, never monolithically**

**DL-069 condition 1** names exactly **three LLM call sites**. **Evaluate is rule-arithmetic (no LLM) and is out of scope.**

| # | Call site | Stage | Token mass |
|---|---|---|---|
| **CS-1** | **Extraction** | Perceive | **Dominant** — the corpus is read here (~450k in) |
| **CS-2** | **Synthesis / artifact generation** | Infer | Moderate |
| **CS-3** | **Findings / issue detection** | Infer | Small (~50k out) — **but this is the judgment** |

**DL-103 forbids routing by *tier*. It does NOT forbid routing by *step*** — §4c already routes by step (`extraction → nano · synthesis/eval → mini`). **Each call site is therefore qualified independently.**

> **A likely — and entirely acceptable — outcome is that the local model clears CS-1 but not CS-3.**
> **Extraction is where the token mass is.** *Local extraction + best-available judgment* captures most of the cost saving while keeping frontier-grade judgment, **and remains fully DL-103-compliant, because every user receives the same judgment.**
> **The local model does not need to be good at everything. It needs to be good at the expensive thing.**

---

## 2. Gate 1 — Mechanical (automate first; no human required)

**Run these before spending a single hour on human evaluation. They may settle the question outright, and they cost nothing.**

| Gate | Criterion | Source |
|---|---|---|
| **M-1** | Output **conforms to the fixed schema** or is rejected and retried | **AC-V1** |
| **M-2** | Enum-valued fields **validate against `analysis_enums`**; unknown values rejected | **AC-V2** |
| **M-3** | **No LLM output introduces a formula, weight, percentage, threshold, or a bare confidence value** | **AC-V3** *(canonical)* |
| **M-4** | **Determinism envelope** — repeated runs on identical input stay within the recorded-fixture tolerance | **ADR-0004** |

**M-3 is the sharp one.** Small models violate structured-output and abstention constraints far more often than frontier models. **A model that keeps emitting a bare confidence number cannot be used at any tier**, because AC-V3 is canonical and the epistemic model depends on it.

**Report:** per call-site **violation rate** for M-1…M-4. **M-3 failure is disqualifying**, not a tuning matter.

---

## 3. Gate 2 — Judgment (golden set)

### 3.1 The corpus — it already exists

The **five curated templates** (DL-056; `10_product/experience/templates/`) — `event` · `generic_project_plan` · `marketing_campaign` · `product_software_launch` · `strategic_initiative` — are **pre-authored, static and owner-curated**. Annotate each with **ground truth**:
- the **claims** actually present (goals, outcomes, stakeholders, assumptions, constraints, dependencies — EI-02), each bound to its **source span**;
- the **issues** a competent planner would flag, bound to a **CAF dimension**;
- the points where the **evidence is thin** and a **Clarification Request** is the correct output.

**Annotation is owner/expert work.** It is the eval's ground truth, and it doubles as the **fixture source** (DL-069 cond. 3: `gemma4` records/refreshes fixtures).

### 3.2 Metrics — derived from doctrine, not from benchmarks

| # | Metric | Call site | Why it matters |
|---|---|---|---|
| **J-1** | **Fabrication rate — ZERO TOLERANCE.** Every extracted claim MUST trace to a **span in the source**. | CS-1 | **The cardinal sin.** A model that invents a stakeholder or an assumption **destroys the product**, and it is the failure small models commit most. |
| **J-2** | **Claim precision / recall** | CS-1 | Missing a dependency is a missed issue downstream. |
| **J-3** | **Issue precision / recall** | CS-3 | **False issues erode trust fastest** — a noisy read is worse than a quiet one. |
| **J-4** | **Epistemic honesty** — *derived* (From OSLO) is never presented as *attested*; **thin evidence yields a Clarification Request, not a confident assertion** | CS-1, CS-3 | Reliability qualification is the product. |
| **J-5** | **Artifact coherence** — synthesized artifacts are internally consistent and traceable to evidence | CS-2 | PS-01/PS-02. |

### 3.3 The comparator — it is free

**DL-069 retains OpenAI/Anthropic as a disabled-by-default fallback behind the same `/services/llm_provider` seam.** Run the **identical** golden set through both.

**Report relative, not absolute.** *"Gemma vs GPT-4.1 on OSLO's actual task, per call-site"* is decision-useful; an abstract score is not.

---

## 4. Prerequisite — the DL-069 condition-4 STOP gate

**DL-069 condition 4 (ratified):** the Llama runtime's **OpenAI-compatible `/v1` endpoint is *assumed* — "confirm before code."** If the runtime is **not** OpenAI-compatible, adding a native model class is a **separate dependency decision → STOP / new owner approval.**

**Confirm this FIRST.** It is an afternoon's work and it gates everything downstream.

---

## 5. Outcomes and what each implies

| Outcome | Implication |
|---|---|
| **Local clears all three call sites** | Marginal token cost collapses to GPU amortization. The governor becomes a **throughput** bound, not a **cost** bound. Most of the tier debate evaporates. |
| **Local clears CS-1 (extraction) only** | **The expected case.** Route **extraction local, judgment best-available** — by **step**, never by tier. Captures the bulk of the token cost; **DL-103 §1 fully preserved.** |
| **Local clears nothing** | **You are renting.** **E1–E3 (DL-105) then becomes existential** — the difference between **~12 and ~74 analyses/month** at the $3 Free ceiling. |

**E1–E3 hedges this decision in every branch.** Its commissioning to R1 (DL-105) **de-risks DL-069 regardless of how this eval lands.**

---

## 6. The bar is an owner decision

**How much judgment quality will be traded for the cost collapse — knowing that, per DL-103 §1, it CANNOT be tiered, so every user receives whatever is chosen?**

**This specification produces the evidence. It does not set the bar.** `TBD – Owner Decision Required`.

---

## 7. Non-goals

Model selection · setting the quality bar · prompt engineering · any change to what OSLO computes or concludes · tier numbers (DL-103 — suspended; re-derived from DL-105 §4 telemetry).
