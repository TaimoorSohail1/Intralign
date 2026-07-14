## Decision

**Commission the DL-069 model-judgment evaluation**, and record the **coupling DL-103 created**. Realization artifact: `RELEASE_1_MODEL_JUDGMENT_EVALUATION_V1` (`30_engineering/analysis_engine`). **This decision produces evidence; it does NOT select a model or set the bar.**

**1. DL-103 §1 RAISED the bar on DL-069 — record the coupling.**
Before DL-103 an escape hatch existed: ***"Gemma for Free; full-quality GPT-4.1 for Pro"*** — literally §4c's T3 routing row (*"Pro adds model quality"*). **DL-103 §1 prohibits tiering judgment quality**, because a tier-keyed model would make **Reliability a function of the billing plan**. Therefore:
> **The qualified model must clear the bar for the BEST-PAYING customer, not the cheapest free one. Whatever is chosen, EVERY user receives it.**
**DL-069's viability test is strictly harder than when it was ratified**, and that consequence is recorded nowhere. It is recorded here.

**2. STOP GATE FIRST — confirm the DL-069 condition-4 assumption.**
**DL-069 condition 4 (ratified):** the Llama runtime's **OpenAI-compatible `/v1` endpoint is *assumed* — "confirm before code."** **If the runtime is NOT OpenAI-compatible, adding a native model class is a SEPARATE DEPENDENCY DECISION → STOP / new owner approval.** **Confirm this before any evaluation work.** It is an afternoon's work and it gates everything downstream.

**3. Evaluate PER CALL-SITE, never monolithically.**
DL-069 condition 1 names **three LLM call sites**; **Evaluate is rule-arithmetic (no LLM)** and is out of scope.
- **CS-1 — Extraction (Perceive).** **The dominant token mass** (~450k in).
- **CS-2 — Synthesis / artifact generation (Infer).**
- **CS-3 — Findings / issue detection (Infer).** Small output (~50k) — **but this is the judgment.**

**DL-103 forbids routing by TIER. It does NOT forbid routing by STEP** — §4c already routes by step (`extraction → nano · synthesis → mini`). **Each call site is qualified independently.**
> **A likely — and entirely acceptable — outcome is that the local model clears CS-1 but not CS-3.** Extraction is where the token mass is. ***Local extraction + best-available judgment*** captures most of the cost saving while keeping frontier-grade judgment, **and remains fully DL-103-compliant, because every user receives the same judgment.**
> **The local model does not need to be good at everything. It needs to be good at the expensive thing.**

**4. GATE 1 — Mechanical. Automate first; no human required. It may settle the question outright.**
- **M-1 (AC-V1)** — output conforms to the fixed schema or is rejected and retried.
- **M-2 (AC-V2)** — enum fields validate against `analysis_enums`; unknown values rejected.
- **M-3 (AC-V3, *canonical*)** — **no LLM output introduces a formula, weight, percentage, threshold, or a bare confidence value.**
- **M-4 (ADR-0004)** — determinism envelope holds against recorded fixtures.
**M-3 is the sharp one, and M-3 FAILURE IS DISQUALIFYING — not a tuning matter.** Small models violate structured-output and abstention constraints far more often than frontier models. **A model that keeps emitting a bare confidence number cannot be used at ANY tier**, because AC-V3 is canonical and the entire epistemic model depends on it. **Run this before spending a single hour on human evaluation.**

**5. GATE 2 — Judgment, on a golden set that already exists.**
**Corpus:** the **five curated templates** (DL-056) — `event` · `generic_project_plan` · `marketing_campaign` · `product_software_launch` · `strategic_initiative` — pre-authored, static, owner-curated. Annotate each with ground truth: the **claims** present (each bound to its **source span**), the **issues** a competent planner would flag (bound to a **CAF dimension**), and the points where evidence is thin and a **Clarification Request** is the correct output. Annotation is **owner/expert work**; it doubles as the **fixture source** (DL-069 cond. 3).

**Metrics — from doctrine, not benchmarks:**
- **J-1 — Fabrication rate: ZERO TOLERANCE.** Every extracted claim MUST trace to a **span in the source**. **This is the cardinal sin.** A model that invents a stakeholder or an assumption **destroys the product** — and it is the failure small models commit most.
- **J-2** — claim precision/recall (CS-1). **J-3** — issue precision/recall (CS-3); **false issues erode trust fastest — a noisy read is worse than a quiet one.**
- **J-4 — Epistemic honesty:** *derived* is never presented as *attested*; **thin evidence yields a Clarification Request, not a confident assertion.**
- **J-5** — artifact coherence (CS-2).

**6. The comparator is free — report RELATIVE, not absolute.**
DL-069 retains OpenAI/Anthropic as a **disabled-by-default fallback behind the same seam**. Run the **identical** golden set through both. ***"Gemma vs GPT-4.1 on OSLO's actual task, per call-site"*** is decision-useful; an abstract score is not.

**7. Outcomes and what each implies.**
- **Local clears all three call sites** → marginal token cost collapses to GPU amortization; the governor becomes a **throughput** bound, not a **cost** bound; **most of the tier debate evaporates.**
- **Local clears CS-1 only** → **the expected case.** Route **extraction local, judgment best-available — by step, never by tier.**
- **Local clears nothing** → **you are renting**, and **E1–E3 (DL-105) becomes existential** — the difference between **~12 and ~74 analyses/month** at the $3 Free ceiling.
**E1–E3 hedges this decision in EVERY branch.** Its commissioning to R1 **de-risks DL-069 regardless of how the eval lands.**

**8. The bar is an OWNER decision.**
**How much judgment quality will be traded for the cost collapse — knowing that, per DL-103 §1, it CANNOT be tiered, so every user receives whatever is chosen?** **This decision produces the evidence. It does not set the bar.** `TBD – Owner Decision Required`.

## Rationale

**DL-069 made a local model primary expressly to remove external token cost — but whether it can carry OSLO's *judgment* has never been tested.** It is an **empirical** question and cannot be settled on paper, and **everything downstream depends on it**: the cost basis (DL-103 suspended §4c pending re-derivation), the tier numbers, the Free tier's ability to activate, and the urgency of E1–E3.

**DL-103 then removed the fallback.** With judgment quality untierable, a local model that is merely *good enough for free users* is **not good enough** — it must serve the paying user too. That coupling was created by DL-103 and never written down. Recording it is the point of this decision.

## Conditions

1. **Evidence, not selection.** This decision commissions an evaluation. It **selects no model** and **sets no bar**.
2. **The condition-4 STOP gate is a prerequisite** (item 2). No evaluation work begins until the integration mechanism is confirmed.
3. **AC-V3 (M-3) failure is disqualifying at every tier** — it is canonical, and the epistemic model depends on it.
4. **Routing by STEP is permitted; routing by TIER is PROHIBITED** (DL-103 §1). A per-call-site outcome (local extraction + best-available judgment) is **fully compliant**.
5. **Determinism (ADR-0004) preserved.** A model-version change is a **new baseline (DT-6)**, never a regression (DL-069 cond. 3).
6. **Anti-Assumption.** The **quality bar**, the **annotation of the golden set**, and any **model selection** are **owner-open**. **No numbers are set here.**

## Supersedes / Amends

- **Amends DL-069** — records that **DL-103 §1 raised its bar** (the "Gemma for Free / frontier for Pro" hatch is closed); reaffirms conditions 1–5, and elevates **condition 4 to a prerequisite STOP gate**.
- **Extends DL-103 §1** — establishes that *never tier judgment quality* is satisfied by **per-step routing**, and that a local-extraction / best-available-judgment split is compliant.
- **Amends** `30_engineering/analysis_engine/` — new spec `RELEASE_1_MODEL_JUDGMENT_EVALUATION_V1`.
- **Reaffirms** ADR-0004 (determinism / recorded fixtures) · DL-056 (the five curated templates) · **AC-V1/V2/V3** · DL-105 (E1–E3 — the hedge that holds in every branch).
