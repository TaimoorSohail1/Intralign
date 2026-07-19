# DL-146 — Execution-ready planning, Phase-2 · 2A — the Work breakdown becomes an authored, graded task tree

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-2 · 2A — the Work breakdown becomes an authored, graded task tree

**Class:** B (a build within the ratified execution-ready framework — no new scope; DL-145 already ratified the identity) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** **DL-145** (execution-ready planning identity), Phase-2 slice **2A** — *task-altitude decomposition with graded inference-marking.* **Upholds** DL-145 §2/§3 (OSLO authors + marks every inference for validation), §3 depth rule (graded inference), D011/D069 (From OSLO / Confirmed by you), D003 (maturity, not health), D173/DL-109 (computed, then marked).

---

## Decision

The **Work breakdown** document is no longer a flat five-row table at deliverable altitude. It is now an **authored task tree** — OSLO has decomposed the plan to the task level needed to execute, and marked what it inferred for the user to validate. This is the first visible manifestation of DL-145.

1. **Decomposition.** The five workstreams are broken down to task and subtask level (outline-numbered `1 · 1.1 · 1.3.1 …` with indentation showing the hierarchy). OSLO authored the decomposition where the brief did not specify it.
2. **Everything is From OSLO until confirmed.** Every row is marked **From OSLO** by the existing table-provenance engine (`_seedTableProvenance` marks all cells derived); the user confirms a row the same way they always have — by editing/accepting the cell, which flips it to **Confirmed by you** (attested). **No new validation path was built** — authoring reuses the ratified attestation engine at task altitude, exactly as DL-145 §3.1 anticipated.
3. **Graded inference.** The thinnest, most speculative inferences (e.g. *Map AV power drops*, *Lay out badging & check-in stations*, *Confirm 500-person Wi-Fi capacity* as a discrete task) carry a **`low confidence`** grade — a louder prompt to confirm those first (DL-145 §3, "graded inference"). The grade is a **neutral epistemic mark, never a severity colour** — low confidence is a statement about the evidence, not a health signal (D003).

The table format is **unchanged**, so every piece of the artifact-editing machinery keeps working on the deeper tree: `attachTableControls`, `_seedTableProvenance`, the per-cell hover provenance chips, the row provenance dots, row/column ops, autosave, and version bumps. The context-inference model (CI-32–38 tied to `art:'WBS'`) and the ISS-05 unassigned-owner anchor are preserved.

## Guardrails

- **Mark-for-validation intact** (DL-145 §2/§3) — nothing OSLO inferred is presented as fact; every row reads From OSLO until the user confirms it, and the confirm path is the existing attestation (no shadow path).
- **Graded inference is neutral, not severity** (D003 / DL-109) — `.conf-low` is a tentative epistemic grade (dashed, subtle), never a red/amber health mark; low confidence names the evidence, not a defect in the plan.
- **Computed, then marked** (D173) — OSLO authors plan structure, but the whole tree is From OSLO until validated; nothing is asserted as confirmed that the user has not confirmed.
- **The engine is reused, not duplicated** — the table stays a `<table>`; all table machinery and its boot guards verify on the deeper structure. Class-resolve clean (D195a): the new classes (`wbs-n`, `wbs-t`, `wbs-h`, `conf-low`) all carry CSS; indentation is a `data-lvl` attribute, not a class.
- **Maturity unchanged** — this adds plan *detail*, not confidence; the Outcome Confidence read is untouched (a deeper, still-inferred plan is not a more mature one — DL-145 §3, completeness ≠ readiness).

## Scope — 2A of Phase-2

This is the **foundation** slice. The remaining Phase-2 slices are their own DLs: **2B** — the assessment (CAF + issue model) scaled to task/subtask altitude (an unowned subtask, a dateless task against the freeze); **2C** — the sequencing-dependency model + critical path; **2D** — the eighth consolidated pre-export view (readiness coverage + critical path, validate-enabled). Phase-3 remains the Asana export.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing DL-145 Phase-2 · 2A. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the decomposed tree renders with 19 task rows, 4 low-confidence grades, outline hierarchy, per-row provenance, and the ISS-05 anchor preserved — all on the unchanged table engine). AI drafted + built; **only the owner ratifies.**
