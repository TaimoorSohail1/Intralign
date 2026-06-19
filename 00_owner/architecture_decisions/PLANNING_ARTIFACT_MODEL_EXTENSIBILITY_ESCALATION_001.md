# Escalation — Is the Planning-Artifact Model Fixed (Doctrine) or Extensible (Default)?

- **Status:** **RESOLVED — DL-077** (2026-06-19): owner ratified **Option C (hybrid core)** — fixed understanding core (Intent/Context/Scope/Requirements) + extensible execution-planning layer; R1 fixed & scoped to fitting domains; domain-artifact extensibility before methodology-cadence. This document is retained as the decision analysis; the ratified decision is `00_owner/decisions/records/DL-077-planning-artifact-model-hybrid-core.md`. **Realization design — ratified intent (DL-078, post-R1):** `ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001.md` → `00_owner/decisions/records/DL-078-artifact-profile-realization-design.md`.
- **Source:** 2026-06-19 ecosystem deepening — owner asked whether all domains/methodologies align to the R1 planning sequence (Intent → Context → Scope → Requirements → WBS → Resourcing → Schedule).
- **Gates:** the ecosystem **L2 domain-pack layer** (`BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM` E6), methodology support, and the **R1 validation-cohort** selection (see §5).

---

## 1. The question

Is OSLO's **7-artifact planning model** — Intent · Context · Scope · Requirements · WBS · Resources · Schedule — a **fixed canonical model (doctrine)**, or an **extensible default** that can vary by **domain** (construction, manufacturing, software…) and **methodology** (agile, lean, hybrid, waterfall)?

## 2. What the canon fixes vs. defers (current state)

- The **7-artifact set is the canonical R1 model** — Master Spec ("Project MRI synthesizes Intent, Context, Scope, Requirements, WBS, Resources, Schedule…"); the synthesis engine produces exactly these `PlanningArtifact`s (DL-047, `SynthesizedPlanningModel`). It is applied **uniformly** to every project.
- **Project type / workflow type are *non-gating*** in R1 — "descriptive context only; drives no computation, generation, or governance"; OB-C2 even **fails** if metadata gates value.
- **Whether type ever gates behavior is *deferred* — owner decision** (Onboarding §V). **Methodology is unaddressed** beyond a non-gating "workflow type" field.

So the canon has **consciously not decided** this. Today every domain gets the same classical-PM pipeline.

## 3. Why it doesn't universally fit

The 7-artifact set is **classical / waterfall-leaning** (WBS, Resource Plan, Schedule/Gantt). Other domains and methodologies have different artifact ontologies and cadences:

- **Agile software:** epics → stories → sprints → velocity (no WBS, no Gantt); iterative, not phase-gated.
- **Construction:** + submittals, RFIs, permits, inspections, punch lists.
- **Manufacturing:** + BOM, routing, capacity, quality plans.
- **Methodology is *deeper* than domain:** agile vs. phase-gated changes not just the artifacts but the **planning cadence** (continuous re-plan vs. one-time plan), which ripples into what "drift" and the **Outcome-Integrity loop** mean.

## 4. Options (for owner decision)

- **Option A — Fixed (doctrine).** The 7-artifact model is universal; OSLO is opinionated *classical-PM* planning intelligence. *Simplest; narrowest fit; risks excluding agile/construction/manufacturing.*
- **Option B — Extensible default.** Project/workflow type selects a **domain/methodology artifact profile** (add/remove/reorder artifact types + cadence). Requires the synthesis engine, evaluation, and MRI to handle **variable artifact sets**. *Broadest fit; enables domain packs; significant architecture + governance work.*
- **Option C — Hybrid (recommended for evaluation).** A **fixed canonical core** (e.g., Intent / Context / Scope — domain-agnostic *understanding* layer) **+ an extensible execution-planning layer** (WBS/Schedule → or epics/sprints, submittals, BOM…) that varies by domain/methodology. *Keeps the epistemic core stable while allowing domain variation.*

## 5. Constraints any option must preserve (epistemic)

- **Attested / Derived**, **CAF** (Clarity/Alignment/Feasibility — plausibly domain-agnostic), **Confidence**, and **recompute/CHR** must still apply to *any* artifact set.
- **Methodology changes the cadence** (iterative vs. phase-gated) → affects recompute triggers, drift, and the Outcome-Integrity loop — the deepest and most carefully-governed part.
- Therefore extensibility is an **architecture decision, not a config toggle** — it touches Infer (synthesis), Evaluate (CAF), and Disclose (MRI surfaces).

## 6. R1 scope / validation-cohort implication (flagged separately, per owner)

Because R1 applies the **fixed** classical set, **R1 is implicitly scoped to projects that fit Intent → … → Schedule** — strategic initiatives, OKRs, classical PM. Consequence for the DL-076 release ladder:

- **R1 (<5) and R2 (10–20) validation users should be drawn from *fitting* domains.** Agile-software or construction users may not validate well against the R1 model.
- **Decision needed:** is "classical-PM-only" an **intentional R1 boundary** (onboard fitting domains first), or an unrecognized constraint to address sooner? This should inform the **validation-cohort selection** in the release model (DL-076).

## 7. Recommendation (AI — owner ratifies)

- **Long-term: Option C** (fixed understanding core + extensible execution-planning layer) — it preserves the governed epistemic core while admitting domain/methodology variation, and it unlocks the **L2 domain-pack** ecosystem (E6) — the deepest moat.
- **For R1: keep the model fixed (Option-A behavior)** and **scope R1 validation to fitting domains** (§6) — do not build extensibility into R1.
- **Decide the extensibility architecture (A/B/C) before scoping L2 / domain packs**, since the ecosystem layer hangs on it.
- Route through Framework 001 (likely a DL). *AI recommends; owner ratifies.*

## 8. Dependencies

DL-047 (synthesis engine / `PlanningArtifact`); DL-062 (CAF first-class); the Outcome-Integrity doctrine (drift/cadence); Onboarding §V (the deferred type-gating question this would resolve); DL-076 (release model / validation cohort); `BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM` (E6 domain packs, gated on this).

---

*This escalation surfaces an open architecture/doctrine question deferred in the canon (Onboarding §V): whether OSLO's 7-artifact planning model is fixed doctrine or an extensible default varying by domain and methodology. It records that the canon currently fixes the set and applies it uniformly (project/workflow type non-gating), shows where the classical set does not fit (agile, construction, manufacturing; methodology cadence), lays out three options (fixed / extensible / hybrid-core), states the epistemic constraints any option must preserve, flags the R1 validation-cohort implication, and recommends a hybrid long-term architecture with R1 kept fixed and scoped to fitting domains — explicitly as advice for owner ratification, resolving nothing and introducing no doctrine.*
