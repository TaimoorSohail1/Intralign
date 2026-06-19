# Design Proposal — Artifact-Profile Mechanism & Registry (DL-077 Realization)

- **Status:** **Design proposal — Framework 001 Proposal stage. NOT ratified.** AI-drafted recommendation framing the **DL-077 realization follow-on**; **owner ratifies intent, engineering authors the realization** (ratify ≠ author). **Post-R1** (R1 ships the fixed classical-PM profile only) — no Alpha/R1 build pressure.
- **Resolves the realization of:** `00_owner/decisions/records/DL-077-planning-artifact-model-hybrid-core.md` (Option C hybrid core) and continues `PLANNING_ARTIFACT_MODEL_EXTENSIBILITY_ESCALATION_001.md`.
- **Layer:** Planning-artifact architecture (Infer · Evaluate · Disclose). **No epistemic invariant changed; no doctrine introduced.** This is a *structure* (L2 schema) design, explicitly **not** a cognition (L3) change.
- **Source:** Owner direction 2026-06-19 (proceed with the DL-077 artifact-profile realization). Grounded in DL-047 + `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md` (synthesis/generation contract), DL-062 (CAF first-class), DL-061 (Project MRI), DL-049 (the "promotion not migration" precedent), DL-076 (validation cohort), and `BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM` (E6/E4).

---

## 0. What DL-077 ratified vs. what this designs

**Ratified (DL-077 — not reopened):** a two-layer model — a **fixed understanding core** (Intent · Context · Scope · Requirements, domain-agnostic) + an **extensible execution-planning layer** whose profile is **multi-dimensional and compositional, NOT a fixed domain×methodology matrix**; **R1 stays fixed** (classical-PM only); **domain-artifact extensibility before methodology-cadence**; epistemic invariants binding.

**This proposal designs (for owner ratification of intent; engineering authors detail):** the four realization surfaces — (1) the fixed-core boundary, (2) the **artifact-module + compositional-profile** mechanism, (3) the **artifact-profile registry** (the E6 substrate), (4) how all three **thread the cognitive spine** (Infer/Evaluate/Disclose) without touching the epistemic contract — plus the R1 boundary, sequencing, and the open owner/governance decisions.

**The load-bearing realization fact (from Wave S).** The synthesis contract today hard-wires generation of *exactly seven* `PlanningArtifact` types in one step ("Generate `PlanningArtifact`s (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) from the model … as Derived Cognition"). **The entire extensibility design is a generalization of that single step** — *which* artifact types are generated becomes profile-determined; *how* each is generated (Derived, CHR-per-generation, semantic-replay, user-edit = new Attested input → recompute) is **unchanged**. The five Critical negatives that guard the generative boundary (Derived-as-Attested, change-without-recompute, history overwrite, silent gap-fill, autonomous artifact write) remain exactly as contracted.

---

## 1. Surface 1 — The fixed understanding core boundary

The fixed core is **Intent · Context · Scope · Requirements** — the domain-agnostic "what / why / success" layer where CAF and the epistemic invariants live; **always generated, every profile**. The execution-planning layer is the "how" and varies.

- **Open detail (escalated, per DL-077):** the **precise placement of Requirements** — is it always-core, or partly profile-shaped (e.g., regulatory requirements modules)? DL-077 flagged this as an engineering realization detail. **Recommendation:** keep **Requirements in the fixed core** (it is the success-definition the execution layer is evaluated against), and let profiles **add** requirement-type modules (e.g., compliance requirements) **without removing** the core Requirements artifact. **Owner confirms; engineering finalizes the boundary.**

## 2. Surface 2 — Artifact modules + compositional profile mechanism

- **Artifact module** = a typed, self-contained definition of one execution-planning artifact kind, carrying: its **`PlanningArtifact` type**, its **synthesis/generation contract** (how Infer constructs it from the `SynthesizedPlanningModel`), its **CAF applicability** (which of Clarity/Alignment/Feasibility apply and how seeded), and its **MRI surface** (how Disclose renders it). Examples: `wbs`, `resources`, `schedule` (classical-PM); `epics`, `stories`, `sprints` (agile); `submittals`, `rfis`, `permits`, `inspections` (construction); `bom`, `routing`, `capacity` (manufacturing).
- **Profile** = a **composed set of modules**, resolved at synthesis time by a **profile resolver** reading **multiple signals** — per DL-077 the dimensions include **domain, methodology, compliance/regulatory regime, scale/complexity, risk/criticality, commercial/contract model, project nature** (new-build vs maintenance, delivery vs R&D). **Critically (DL-077): this is compositional, not a pre-enumerated N-dimensional lookup** — the resolver composes modules from signals; it does not index a combinatorial matrix (which explodes and falsely assumes orthogonality).
- **Classical-PM is the default profile** = fixed core + `wbs` · `resources` · `schedule` (today's seven). It is the R1 profile and the fallback when signals are weak.
- **Recommendation:** model modules as **first-class registry entries** and the profile as a **resolved composition**, so a "domain pack" (E6) is a *bundle of modules + a resolver contribution*, never a fixed profile blob. **Engineering authors** the resolver algorithm and the signal-combination policy.

## 3. Surface 3 — The artifact-profile registry (E6 substrate)

- **What:** an owner-governed **registry of artifact modules + profile/resolver contributions** that the synthesis engine reads to know which artifacts a given project's profile generates. This is the **substrate for L2 domain packs (E6)**.
- **Governed because it touches Infer/Evaluate/Disclose** — but it is **structure (L2 schema), not cognition (L3).** A module may add artifact *types* and *MRI surfaces*; it **may not inject assessment logic.** **CAF / scoring / confidence stay first-party and governed** — that is the separate, governance-gated E4 boundary ("the marketplace that can't manipulate your judgment"). The registry admits L2 contributions; it **does not** admit L3.
- **Extensibility staging (recommended):** **build-time, owner-curated registry first** (first-party modules: classical-PM + the first domains), then **runtime / third-party registration later**, gated on the **E6 governance model** and the **E4 boundary ratification**. **Owner decides** the registration/certification model.

## 4. Surface 4 — Threading the cognitive spine (invariants preserved)

- **Infer (synthesis/generation).** The `SynthesizedPlanningModel` stays the Derived model from Attested assertions. The generation step becomes **profile-aware**: always generate the fixed core + generate the profile's execution modules. Each generated `PlanningArtifact` keeps `epistemic_state=derived`, a **CHR per generation**, semantic-equivalence replay, and **user-edit = new Attested input → recompute** (never in-place mutation). **No new responsibility; the Wave S Critical negatives are unchanged.**
- **Evaluate (CAF).** CAF (Clarity / Alignment / Feasibility — DL-062) must apply to **any** module; the fixed core anchors CAF, execution modules carry module-specific CAF seeds **drawn from the first-party basis**. Reliability drivers **stay decomposable** (glossary DL-053). CAF is **never** sourced from a third-party module.
- **Disclose (Project MRI).** The Project MRI (per-project, DL-061) must render a **variable artifact set** — the fixed core always present, plus whatever execution modules the profile produced — each with its own confidence/CAF. The MRI becomes profile-driven in *what it shows*, not in *how it judges*.

## 5. R1 boundary (unchanged by this design)

R1 ships the **classical-PM profile only**, **hard-wired** (no resolver, no registry lookup) — i.e., today's Wave S behavior — and is **scoped to fitting domains** (the DL-076 validation cohort). The module/profile/registry machinery is **built post-R1**. This design only ensures the R1 synthesis step is structured so the later generalization is a clean extension, not a rewrite.

## 6. Sequencing — domain-artifact extensibility before methodology-cadence

Per DL-077: ship **domain-artifact extensibility** (which modules exist) first. **Methodology-cadence** (iterative vs phase-gated) changes the **planning cadence** — continuous re-plan vs one-time plan — which touches the **recompute / drift / Outcome-Integrity loop**, the deepest, most-governed part. The registry should be **designed to accommodate** a cadence dimension but **not implement it** until a later sub-phase with its own escalation (cadence governance is not in scope here).

## 7. Open owner / governance decisions (escalated — not assumed)

1. **Fixed-core boundary** — confirm Requirements stays core with additive compliance-requirement modules (§1).
2. **Resolver signal-combination policy** — the dimensions are set (DL-077); the *composition rule* (how signals combine, conflict resolution, default-to-classical thresholds) is **engineering's to propose**; owner ratifies guardrails.
3. **Registry governance model** — who may register modules/profiles (first-party only → certified domain packs → open), certification bar, and per-org catalogs. Ties to **E6** and the **E4 boundary**.
4. **Build-time vs runtime extensibility** — recommended build-time/owner-curated first; runtime/third-party gated on E6/E4 governance.
5. **Methodology-cadence** — deferred to a later sub-phase with its own escalation (recompute/drift/Outcome-Integrity impact).

## 8. Framework 001A Review

- **Findings:** DL-077's hybrid core realizes cleanly as a **generalization of the single Wave S generation step** — the artifact *set* becomes profile-determined while every Derived/CHR/recompute/replay semantic and all five Critical negatives stay exactly as contracted. Modules + a compositional resolver + a governed registry implement the "compositional, not a matrix" mandate and supply the E6 substrate, with CAF/scoring held first-party (the E4 boundary). R1 is untouched.
- **Concerns:** (1) **CAF integrity at the boundary** — execution modules must seed CAF from the first-party basis only; a module must never become a cognition-injection vector (keep L2≠L3 strict). (2) **Resolver complexity** — multi-signal composition must not become an unbounded matrix; needs a bounded, default-to-classical composition policy. (3) **MRI variable-set rendering** — Disclose must handle arbitrary module sets without implying false completeness. (4) **Registry governance** is a real owner/doctrine surface (shared with E6/E4) and must be settled before any third-party registration. No epistemic invariant, doctrine, or constitution content is threatened.
- **Dependencies:** DL-077 (parent), DL-047 + Wave S synthesis contract (the generation step generalized), DL-062 (CAF), DL-061 (Project MRI), DL-076 (validation cohort), `BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM` E6 (domain packs — this is their substrate) and **E4** (the cognition boundary that bounds the registry), and a future methodology-cadence escalation.
- **Recommendation:** **Ratify the intent** of the four surfaces — fixed core (Requirements stays core, additive compliance modules); artifact-module + **compositional** resolver; **governed, build-time-first registry** admitting L2 not L3; profile-aware Infer/Evaluate/Disclose preserving every Wave S invariant — **keep R1 fixed**, **sequence domain-artifact before methodology-cadence**, and **delegate the mechanism to engineering** (resolver algorithm, schemas, storage, registry). Decide the registry-governance model alongside E6/E4. **AI recommends; owner ratifies intent; engineering authors realization.**
- **Status:** Draft design proposal ready for owner review. **Post-R1, no build pressure**; unblocks E6 design once the registry-governance model is set.

## 9. Owner decision required (summary)

1. Ratify the **four-surface design intent** (fixed core · compositional module/profile resolver · governed registry · profile-aware spine), with R1 kept fixed?
2. Confirm **Requirements stays in the fixed core** (additive compliance-requirement modules)?
3. Set the **registry-governance direction** (first-party → certified → open) and **build-time-first** extensibility — jointly with **E6/E4**?
4. Authorize the **engineering realization proposal** (resolver algorithm, module/profile schemas, registry storage), and confirm **methodology-cadence** is a later, separately-escalated sub-phase?

---

*This design proposal frames the DL-077 realization: a planning-artifact architecture in which the fixed understanding core (Intent/Context/Scope/Requirements) is always generated and the execution-planning layer is a composition of typed artifact modules resolved from multiple signals (domain, methodology, compliance, scale, risk, commercial model, project nature) — compositional, never a domain×methodology matrix — held in an owner-governed artifact-profile registry that is the substrate for L2 domain packs (E6) while keeping CAF, confidence, and all scoring first-party and governed (the E4 boundary). It shows the whole mechanism as a generalization of the single Wave S generation step, leaving every Derived/CHR/recompute/semantic-replay invariant and all five Critical generative negatives unchanged, keeps R1 on the fixed classical-PM profile scoped to fitting domains, sequences domain-artifact extensibility before methodology-cadence, escalates (not assumes) the open boundary and governance decisions, and introduces no doctrine. AI recommends; the owner ratifies intent; engineering authors the realization.*
