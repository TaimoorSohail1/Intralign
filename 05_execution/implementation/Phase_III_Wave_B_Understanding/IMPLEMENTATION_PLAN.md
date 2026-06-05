# Phase III — Wave B: Understanding (Infer · Evaluate)

**Sequence:** After Phase II. · **Status:** Not started · **Owner gate:** required before Phase IV.
**Contracts:** `IC/QA/OBS-WB-INFER`, `IC/QA/OBS-WB-EVAL` (`03_architecture/contracts/WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`).

## Goal
Produce OSLO's **understanding** of the canonical record — Findings (Infer), and Issues with Confidence/Reliability/CAF/Outcome Confidence (Evaluate) — all as **Derived** cognition that is recomputable and history-tracked. This is where OSLO starts to *say something* about a project, with calibrated uncertainty.

## Scope & build order
1. **`IC-WB-INFER` — Finding (Infer)** — generate Findings (gap/conflict/risk) from Attested content; one producer; conflicts **surfaced, not resolved**; each Finding is Derived.
2. **`IC-WB-EVAL` — Issue · Confidence · Reliability · CAF · Outcome Confidence (Evaluate)** — assess Findings into Issues; compute Confidence (trust-in-understanding, **never** project health); reliability-qualified; band-semantic per Calibration Defaults.

## Depends on
Phase II (Attested store + recompute backbone — understanding is recomputed via 00R and appends CHRs).

## Expected outcomes (definition of done)
- ✅ Findings are generated from attested content and stored as **Derived** (never written to the canonical store as Attested).
- ✅ Issues/Confidence/Reliability/CAF/Outcome Confidence compute, each carrying explicit `epistemic_state = derived` and a confidence **band** (0–49/50–74/75–100, with the ±3 edge-guard).
- ✅ Confidence is expressed as **trust in understanding**, reliability-qualified — never as project health/readiness/probability/score (negative tests enforce this).
- ✅ A recompute produces a **new** CHR; comparing two emissions shows confidence/outcome **drift** surfaced at ≥10 pts or a band change (product feature).
- ✅ "Why did confidence change?" is answerable structurally via CHR lineage.
- ✅ Determinism: rule-derived values replay **exactly**; AI-numeric values replay within **±7 pts & same band**.

## Invariants enforced
Cognition is **Derived** and recomputable; confidence ≠ project health; conflicts surfaced not resolved; only-recompute-changes-assessment; one producer per output.

## Testing focus
Behavior layer + determinism tiers: exact replay for rule/formula steps; band-semantic for AI-numeric; semantic for AI-text. Negative tests for the "confidence-as-health" and "Derived-as-Attested" prohibitions.

## Exit gate (owner-approved before Phase IV)
OSLO produces calibrated, Derived understanding with banded confidence and surfaced drift; the determinism tiers hold on replay; uncertainty is explicit, never hidden.
