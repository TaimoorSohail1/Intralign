# R2 → main — CAF / Finding reconciliation catalog (DL-209 + DL-210)

**Date:** 2026-08-09 · **Author:** AI (analysis/checklist only — owner ratifies; owner/dev execute at graduation) · **Status:** graduation checklist — **nothing edited on `main` now.**

**Purpose.** DL-209 (load-bearing sensitivity + the verify/build/decide resolution model) and **DL-210** (CAF dimension boundaries; deterministic **structural-target** dimension assignment; relational top-down alignment; the escalation model) are R2-staged and land in `main` at **R1 graduation**. DL-210 amends founder-approved **CAF Assessment Model Positions #10/#11**, which several `10_product/domain` models are built on. This catalog lists **every main product-canon doc the amendment touches and what each requires**, so the graduation edit is complete and no product doc silently contradicts the new model. Executed on the `integration/r2-to-main` branch per `R2_TO_MAIN_INTEGRATION_PLAN.md` Phase-B.

---

## 1. The reconciliation principle — surgical, not wholesale

Most of the finding/CAF doctrine **survives unchanged**. The edit is narrow:

**What changes**
- **Dimension assignment: judgment → deterministic.** "Which dimension(s) a finding affects is settled in Impact Assessment by judgment" (CAF §9; Finding Model §59; Finding-System §89) becomes: **the affected dimension(s) are determined deterministically from the finding's structural target in the graph** (`definition → Clarity · edge → Alignment · achievability → Feasibility · truth → Grounding · coverage → Adaptability`), with the sole judgment quarantined to L0 extraction and **surfaced via escalation**, never applied silently.
- **Impact Assessment is re-characterized as the deterministic sensitivity pipeline.** Its other three factors (Significance, Scope, Evidence Support) are realized by the L1/L2 sensitivity engine (DL-209); only dimension-*identity* moves from judgment to structural target.

**What is preserved (do NOT rewrite these)**
- **"A finding's type does not predetermine its dimension"** stays **true** — precisely because DL-210 keys on the *structural target*, not the finding-type (CAF Position #11 intact).
- **Independent dimensions; a finding may bear on several** (Position #2) — carried in the existing `affected_dimensions` / `dims[]` set, with a single primary `dim` per resolved issue.
- **Flat finding taxonomy** (Position #13); findings are **descriptive, never prescriptive**; findings **never directly modify CAF** (only via assessment). All intact.

Because of this, most rows below are **surgical amendments or field additions**, not rewrites. The one substantive *enrichment* is the Alignment evaluation (relational/top-down).

## 2. Per-document reconciliation

| Doc (`10_product/domain/`) | Passages built on the old model | Required change at graduation | Class |
|---|---|---|---|
| **CAF_ASSESSMENT_MODEL_V1** | Positions #10/#11; §9 "weighed in judgment — not in formula" | **Primary amendment.** Dimension assignment → deterministic-by-structural-target; Impact Assessment = the deterministic sensitivity pipeline (significance/scope/evidence), dimension-identity deterministic; add the escalation valve. Add the dimension **boundary cut** (Clarity=definition · Alignment=edge/relational · Feasibility=achievability) + **Clarity→Alignment→Feasibility precedence**. Preserve #2/#13. | **AMEND (primary)** |
| **FINDING_MODEL_V1** | §59 ("which dimensions… settled in Impact Assessment"); §58, §201, §236 | Reconcile §59: dimension is now determined by **structural target** (type-independence still holds; it is simply no longer *judgment*). Impact Assessment **sizes magnitude**, not dimension identity. Note the decompose ⇄ multi-dim layering (`dims[]` at observation · single `dim` per resolved issue). | **AMEND (surgical)** |
| **FINDING_SYSTEM_SPECIFICATION_V1** | §34, §45, §58 `affected_dimensions`, §89 (magnitude via IA), §117–119 | Add a **`structural_target`** field as the basis for `affected_dimensions` (which stays the multi-dim set + primary). Magnitude via the deterministic sensitivity engine. Add the **escalation / known-unknown** finding state (unmapped target → escalate; leverage-gated known-unknown). | **ADD-FIELD + AMEND** |
| **PLANNING_INTELLIGENCE_SPECIFICATION_V1** | §10 Alignment Evaluation (§118–120); §65, §140, §146 | **Largest substantive change — ENRICH.** Replace the thin "misalignment = Conflict + drift-from-intent" with the **relational, top-down outcome→roots, edge-based** model: per-edge alignment sufficiency, the **tangent check**, the two per-path outputs (optimization + misalignment). Add the **load-bearing gate** + the escalation lifecycle. | **ENRICH** |
| **RECOMMENDATION_MODEL_V1** (+ `RECOMMENDATION_SYSTEM_SPECIFICATION_V1`, `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1`) | resolution paths; multiplicity Positions #6/#7 | Map the **verify / build / decide** acts + derived primary + "also-offered" onto recommendation paths (the existing multiplicity model already fits — primary path = recommendation, alternatives = "other ways"). Add the escalation → **clarify/verify** recommendation. Largely consistent — mapping, not conflict. | **RECONCILE (mapping)** |
| **CONFIDENCE_MODEL_V1** | §217, §254 (Confidence = CAF × Reliability) | Reflect the **incompleteness ceiling**: an unassessed **load-bearing** region caps *claimable* Confidence as **incomplete**, never a low score (**unknown ≠ bad**). | **RECONCILE-LENS** |
| **RELIABILITY_MODEL_V1** | §101–112 (Coverage / Assessability; the dual-lens note §112) | Express the DL-210 **model-gap** through the **existing dual lens** (§112): a model gap = reduced **Assessability/Coverage** (Reliability) **+** an incomplete-region marker — **not a new mechanism, not a CAF penalty**. Verify the leverage-gate/known-unknown maps onto Assessability. | **RECONCILE-LENS (verify)** |
| **MRI_MODEL_V1** | (consumes findings; surfaces attention) | Verify the **load-bearing / leverage gate** (DL-193/209) and the **known-unknown** surface are reflected in what MRI brings to attention (no dimension tag / band color on a known-unknown). | **VERIFY** |
| **MODEL_LINEAGE_INDEX_V1** | §6 "authoritative, **unmodified**" list; §257 principles | Update the "unmodified" claim for the amended models; add **DL-209 / DL-210** to the model lineage. | **INDEX** |

## 3. Cross-cutting callouts

- **The Alignment enrichment is the real work** (`PLANNING_INTELLIGENCE_SPECIFICATION_V1 §10`). Everything else is surgical; this section is currently far thinner than the ratified relational model and should be rewritten to the top-down outcome→roots traversal.
- **The incompleteness ceiling has a home already** — `RELIABILITY_MODEL_V1 §112`'s dual-lens treatment of an incomplete surface. Reuse it: a model gap is an Assessability/Coverage reduction *and* an incomplete-region marker; do **not** invent a parallel mechanism, and never score the unknown as weak (`GT-49`/`GT-50`).
- **The Recommendation model needs no doctrinal change** — the verify/build/decide acts fit its existing multiplicity/alternatives model; this is a mapping exercise plus the new clarify/verify escalation path.
- **Preserve the CARE-POINT** (DL-196 §5): Adaptability issues never leak into the CAF band/rows/heat, throughout the reconciliation.

## 4. Execution

Apply on the `integration/r2-to-main` branch at graduation (Phase-B), alongside promoting the DL-209/DL-210 records. **After** the amendments land, run a **full product-grill pass** to verify whole-canon coherence (finding · recommendation · MRI · confidence · reliability) against the new deterministic model — that is the right trigger for the grill, not before the amendment is in `main`. Doc-integrity gate must be green; owner merges.

---

_AI-drafted checklist (Framework 001). Realizes the graduation obligations of DL-209/DL-210; no `main` edit until graduation. Paired with `R2_TO_MAIN_INTEGRATION_PLAN.md` (Phase-B) and `SIGNOFF.md` (Slice 10)._
