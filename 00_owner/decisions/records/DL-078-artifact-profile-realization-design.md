# DL-078 — Ratify the artifact-profile mechanism & registry realization design (DL-077 Option C realization intent)

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-19 (ratify the DL-077 realization design after advice). Ratifies the design framing in `00_owner/architecture_decisions/ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001.md`; realizes `DL-077` (Option C hybrid core). Grounded in DL-047 + `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md`, DL-062 (CAF), DL-061 (Project MRI), DL-049, DL-076.
- **Layer:** Planning-artifact architecture (Infer · Evaluate · Disclose) — owner-ratified realization **intent**; engineering authors the mechanism. No epistemic invariant changed; no doctrine introduced.

## Decision — adopt the four-surface realization design
1. **Profile-aware generation (Infer).** Generalize the single Wave S generation step: the **fixed understanding core is always generated**, plus the **profile's execution modules**. Every generated `PlanningArtifact` keeps its Derived semantics unchanged — `epistemic_state=derived`, a **Cognition History Record per generation**, semantic-equivalence replay, and **user-edit = new Attested input → recompute** (never in-place mutation). The five Wave S Critical negatives (Derived-as-Attested, change-without-recompute, history overwrite, silent gap-fill, autonomous artifact write) are **unchanged**. **No new responsibility.**
2. **Fixed-core boundary.** The fixed core is **Intent · Context · Scope · Requirements**, generated for every profile. **Requirements stays in the fixed core**; profiles may **add** requirement-type modules (e.g. compliance/regulatory) but **may not remove** the core Requirements artifact.
3. **Compositional profile mechanism.** The execution-planning layer is a set of typed **artifact modules** composed by a **profile resolver reading multiple signals** (domain, methodology, compliance regime, scale/complexity, risk/criticality, commercial/contract model, project nature) — **compositional, NOT a pre-enumerated domain×methodology matrix.** Classical-PM (WBS · Resources · Schedule) is the **default profile**.
4. **Artifact-profile registry (E6 substrate).** An owner-governed registry of modules + profile/resolver contributions. **Governance posture: first-party (owner-curated) at launch → certified partners → open/third-party**, staged; **build-time-curated before runtime/third-party registration.** The registry admits **L2 structure, never L3 cognition** — **CAF / confidence / all scoring stay first-party** (the E4 boundary; the E4 doctrine call is the separate DL-079).
5. **Evaluate / Disclose preserved.** CAF (Clarity/Alignment/Feasibility — DL-062) applies to any module, seeded from the first-party basis; reliability drivers stay decomposable. The **Project MRI** (DL-061) renders a **variable artifact set** without implying false completeness; the fixed core is always present.
6. **R1 stays fixed.** R1 ships the **classical-PM profile only, hard-wired** (no resolver/registry), scoped to fitting domains (DL-076 validation cohort). The mechanism is **built post-R1**.
7. **Sequencing.** **Domain-artifact extensibility before methodology-cadence.** Methodology-cadence (iterative vs phase-gated) touches the recompute / drift / Outcome-Integrity loop and lands later as a **separately-escalated** sub-phase.

## Opportunity (why this direction)
Unlocks the **L2 domain-pack ecosystem (E6)** — domain-native planning authored by experts, a supply-side network effect + per-domain calibration — the deepest moat, **without ever risking the governed epistemic core.** The staged registry governance and first-party CAF keep the trust differentiator intact while extensibility ramps.

## Realization (engineering follow-on)
Engineering proposes the **resolver algorithm + signal-composition policy**, the **module/profile schemas**, and the **registry storage**, preserving every Wave S invariant; methodology-cadence as a later sub-phase. **Built post-R1; engineering proposes (ratify ≠ author).**

## Supersedes / Amends
Realizes **DL-077**; resolves the design questions in `ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001`. Sets the registry-governance posture and confirms the fixed-core boundary. **No ratified content superseded;** epistemic invariants and DL-047/062/061 unchanged. The **E4 third-party-lens cognition boundary is the separate doctrine decision (DL-079)**; the GA-onboarding realization is DL-080.

## Provenance
Owner decision via working session, 2026-06-19; the owner requested advice on the open realization questions and ratified the recommended positions (registry governance first-party→certified→open; Requirements stays core with additive compliance modules; R1 fixed; methodology-cadence later). AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.
