# DL-077 — Ratify the planning-artifact model architecture - Option C hybrid core (fixed understanding core + extensible execution-planning layer)

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-19 (advise on the artifact-model decision per the platform vision + disciplined prove-first rollout, then ratify). Resolves `00_owner/architecture_decisions/PLANNING_ARTIFACT_MODEL_EXTENSIBILITY_ESCALATION_001.md`. Grounded in DL-047 (synthesis), DL-062 (CAF), the Outcome-Integrity doctrine, DL-076 (release model), Onboarding §V (deferred type-gating).
- **Layer:** Planning-artifact architecture (Infer · Evaluate · Disclose) — owner-ratified architecture **intent**; engineering authors realization. No epistemic invariant changed; no doctrine introduced.

## Decision — Option C (hybrid core)
1. **Two-layer planning-artifact model.**
   - **Fixed understanding core (domain-agnostic):** Intent · Context · Scope · Requirements — the "what / why / success" layer where the epistemic invariants and CAF live. **Fixed across all domains and methodologies.** *(The exact artifact-by-artifact boundary — e.g. the precise placement of Requirements — is an engineering realization detail to confirm.)*
   - **Extensible execution-planning layer:** the "how" — **WBS · Resources · Schedule is the classical-PM default profile**; other profiles may add or replace artifacts (agile: epics / stories / sprints; construction: + submittals / RFIs / permits / inspections; manufacturing: + BOM / routing / capacity).
   - **Profile selection is multi-dimensional and compositional — NOT a fixed domain×methodology matrix.** Domain and methodology are the two **primary** dimensions but **not the only** ones; others include **compliance / regulatory regime** (FDA / ISO / SOX / gov), **scale / complexity** (task → project → program → portfolio), **risk / criticality**, **commercial / contract model**, and **project nature** (new-build vs maintenance, delivery vs R&D). The execution-planning layer must therefore be a **composable set of artifact modules** selected by a profile computed from multiple signals — **not** a pre-enumerated N-dimensional lookup (which explodes combinatorially and falsely assumes orthogonality). A domain pack (E6) is a **bundle of modules**, not a single fixed profile.
2. **R1 stays fixed.** R1 ships the **classical-PM profile only** and is **scoped to fitting domains** (per the DL-076 validation-cohort note); **no extensibility is built in R1.**
3. **Sub-sequence:** **domain-artifact extensibility before methodology-cadence extensibility.** Methodology changes the planning **cadence** (iterative vs phase-gated), which touches the recompute / drift / Outcome-Integrity loop — the deepest, most-governed part — so it lands later.
4. **Epistemic invariants preserved (binding).** Any execution-planning profile lives under **Attested / Derived, CAF (Clarity / Alignment / Feasibility), Confidence, recompute / CHR.** The fixed understanding core protects the governed-cognition trust differentiator.

## Opportunity (why this direction)
Option C unlocks the **L2 domain-pack ecosystem** (E6) — domain-native planning authored by domain experts — the deepest moat: a supply-side network effect + per-domain data calibration, turning OSLO from a classical-PM product into a **domain-spanning planning platform** — **without ever risking the epistemic core.** It is the safe path to full extensibility, sequenced behind a proven core.

## Realization (engineering follow-on)
Define the precise fixed-core boundary; design the **execution-planning profile mechanism** in the synthesis engine (Infer / `SynthesizedPlanningModel` / `PlanningArtifact`), CAF (Evaluate), and MRI (Disclose), preserving the epistemic model; an **artifact-profile registry** (the substrate for domain packs, E6); methodology-cadence as a later sub-phase. **Built post-R1**; engineering proposes the realization (ratify ≠ author).

## Supersedes / Amends
**Resolves** the deferred Onboarding §V question (project / workflow type will eventually **select an execution-planning profile, post-R1**; stays **non-gating in R1**) and the extensibility escalation (Option C). Sets architecture direction; no ratified content superseded; epistemic invariants and DL-047 / DL-062 unchanged.

## Provenance
Owner decision via working session, 2026-06-19; the owner requested a recommendation grounded in the platform vision and disciplined rollout, and ratified **Option C (hybrid core)**. AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.
