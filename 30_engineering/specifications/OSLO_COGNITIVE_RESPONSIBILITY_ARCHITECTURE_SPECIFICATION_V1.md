# OSLO Cognitive Responsibility Architecture Specification v1

**Document Type:** Architecture Specification · **Status:** **Canonical — Ratified under DL-043 (2026-06-04)** · **Date:** 2026-05-31
**Derives from (validated corrections):** `OSLO_ARCHITECTURE_VALIDATION_REVIEW_003.md` · `OSLO_COGNITIVE_RESPONSIBILITY_VS_LAYER_ARCHITECTURE_REVIEW_001.md` · the Advisory Cognition arc. **Supersedes, as the primary architectural model, the layer-as-primary representation** of `OSLO_ARCHITECTURE_BASELINE_V1.md` (the layers are retained as a secondary dependency-ordering representation, §14).

> **Constraints.** Architecture only — **no** implementation, APIs, schemas, databases, frameworks, prompts, vendors, or tooling. Old layer terminology is **not** preserved where it creates architectural confusion (it is mapped, §14). **Per `CLAUDE.md`, only the owner ratifies/adopts canonical content** — this specification is **canonical upon owner ratification**, and adoption should be **sequenced with the GOV-ARCH-001/001A/000** architecture-representation review.

---

## 1. Purpose

Define OSLO's **canonical architectural model** as a **Cognitive Responsibility Architecture**: a governed control loop of distinct cognitive responsibilities (each realized as a domain of single-capability engines), incorporating the corrections validated in `OSLO_ARCHITECTURE_VALIDATION_REVIEW_003.md`. This specification names the responsibilities OSLO must perform, their boundaries and non-responsibilities, the cross-cutting concerns, and the relationship to OSLO's prior layer representation — so that ownership is unambiguous, the architecture can compute its own central output (outcome alignment), and it extends cleanly to OSLO's future (execution intelligence, governed automation, multi-agent coordination).

## 2. Architectural Thesis

**OSLO is fundamentally a Cognitive Responsibility Architecture.** The **responsibility** (the invariant cognitive verb) is the primary unit; a **Domain** is a responsibility containing multiple engines; an **Engine** is the single-capability grain. **Layers** are a **secondary, representational** concept — a dependency-ordering *view* of responsibilities (read-only upward), not the primary unit. **Planes** are cross-cutting concerns within cognition; **Services** are cross-cutting non-cognitive support. Treating a *layer* as primary is what previously hid the Advise responsibility and produced recurring ownership conflicts; treating the *responsibility* as primary resolves them and makes the architecture complete.

## 3. Corrected Responsibility Set

**In-loop cognitive responsibilities (single-actor minimum complete set):**

```text
Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act
```

**Cross-cutting concerns (not in-line stages):**
- **Authority (Governance)** — constrains inputs and governs outputs at every stage.
- **Perception** — continuous intake (origin of the loop; cross-cutting).
- **Adapt** — *emergent loop behavior* (recompute on trigger) — **not** a primary responsibility.

**Evolution & extension responsibilities:**
- **Learn** — improvement of engines/rules/priors from observed outcomes (distinct from recompute).
- **Coordinate** — inter-agent arbitration/negotiation (multi-agent extension).

**Non-cognitive support:**
- **Render** — surface output formatting (a Service, outside cognition).

*(Corrections applied vs the pre-validation set: added **Intend** and **Learn**; reclassified **Authority** as cross-cutting; demoted **Adapt** to emergent; split former **Express** into cognitive **Disclose** + service **Render**; added/scoped **Coordinate**; re-grounded **Advise**.)*

## 4. Responsibility Definitions

| Responsibility | Question | Owns | Does **not** own |
|---|---|---|---|
| **Perceive** | What is observed? | intake, normalization, staging, promotion-readiness | inference, judgment, authority |
| **Retain** | What is known? | canonical knowledge, assumptions, history, epistemic records (append-only) | inference, scoring, generation, exposure |
| **Intend** | What outcome are we aligning to? | the **declared desired outcome** as a maintained, decomposed **reference** (goal model, success criteria) against which drift is computed | perceiving, judging, authorizing |
| **Infer** | What does this imply? | findings, structural implications, gaps (alignment/coverage/quality/SMART), conflicts, risks | severity/confidence, recommendations, authority |
| **Evaluate** | How important / how sure? | severity, confidence, CAF, **reliability**, epistemic state, prioritization (of the **current state**) | generation of candidates, exposure, authority |
| **Advise** | What should be considered? | **governable candidate generation** — recommendations, clarification requests, candidate actions/improvements (incl. candidate-comparison) | severity/confidence, authorization, exposure, rendering, execution |
| **Disclose** | How is meaning safely conveyed? | posture-aware **disclosure**, epistemic-safety, surface-invariant meaning preservation | reasoning, judgment, authority, generation, pixel-level rendering |
| **Act** | What authorized action is coordinated? | coordination of **authorized** execution (posture-gated), recompute triggering | interpretation, severity, authority, generation |
| **Learn** *(evolution)* | How does the system improve? | improvement of engines/rules/priors from observed outcomes | runtime inference/judgment/generation (it changes *future* behavior, not current outputs) |
| **Coordinate** *(multi-agent)* | How are multiple actors reconciled? | inter-agent **arbitration/negotiation** of competing candidate actions, under shared Authority | single-actor generation, authority, execution |

## 5. Cross-Cutting Planes

Three concerns are **cross-cutting** — they are not sequential stages and must not be drawn in-line:
- **Authority Plane (Governance)** — §9. Constrains inputs (posture/tier/policy bound what may be perceived/advised) and governs outputs (expose/suppress/defer/block; authorize actuation) across **Perceive, Advise, Disclose, Act**.
- **Perception** — continuous, multi-source intake; the loop's always-on origin (OSLO's prior "Context **Plane**" already recognized this).
- **Adapt** — the **emergent** recompute behavior: when Retain/Infer/Evaluate change (signal or mutation), the loop re-runs. It is a **property of the loop**, owned by no single responsibility; its **trigger detection** belongs to Perceive/Act.

## 6. Domains and Engines

Each in-loop responsibility is realized as a **Domain** containing **single-capability Engines** (the single-responsibility grain):
- **Infer Domain** — gap / alignment / traceability / feasibility engines.
- **Evaluate Domain** — severity / confidence / CAF / reliability / epistemic engines.
- **Advise Domain** — **Recommendation** engine, **Clarification** engine (Suggested-Action folded into Recommendation; **no** Alternative-Recommendation engine — alternatives are *multiple* recommendations; **no** Resolution-Path engine — presentation-only).
- **Authority Domain (Governance)** — exposure / suppression / deferment / blocking / authorization engines (cross-cutting).
- **Disclose Domain** — disclosure / epistemic-safety / meaning-preservation engines.
- **Retain / Perceive / Intend / Act / Learn / Coordinate** — each a domain of its respective engines.

**Engine qualification (any future engine):** it (1) performs a **single cognitive capability**; (2) within **one** responsibility; (3) **traceable** to its inputs; (4) for Advise engines, produces **governable candidate** outputs; (5) is **not** an authority, rendering, or execution act unless that is its domain's responsibility.

## 7. Services vs Cognitive Responsibilities

**Cognitive responsibilities** are *in the loop* (they reason, judge, generate, disclose, or coordinate meaning). **Services** are **cross-cutting, non-cognitive support** that the responsibilities use but that perform no cognition:
- **Render** — surface/pixel/layout formatting of disclosed content (the non-cognitive half of the former "Express").
- **Determinism/Replay, Identity, Time-Semantics** — operational guarantees supporting Retain/Perceive.
A Service **never** owns a cognitive responsibility; **Disclose** (cognitive) is distinct from **Render** (service).

## 8. Runtime Flow

```text
   AUTHORITY PLANE (Governance)  ───── constrains inputs · governs outputs across the loop ─────────────────────
        │ (constrain)                                  │ (govern: expose/suppress/defer/block/authorize)
        ▼                                              ▼
 PERCEIVE → RETAIN → INTEND → INFER → EVALUATE → ADVISE → DISCLOSE → ACT ─┐  (→ COORDINATE, multi-agent)
   ▲ (continuous intake)                                                  │
   └──────────────── ADAPT (emergent recompute on signal/mutation) ◀──────┘
 LEARN: improves engines from observed outcomes (changes future behavior)        RENDER (service): formats disclosed output
```

- **Inputs/outputs (key):** Intend supplies the **reference outcome**; Infer reads Retain (+ Intend) → Findings; Evaluate → Issues/severity/confidence/CAF/reliability (current-state, vs Intend reference for drift); Advise → **governable candidates** (constrained by Authority); Authority governs candidate **exposure/authorization**; Disclose conveys meaning (Render formats it); Act coordinates **authorized** execution; Adapt re-runs the loop on change; Learn improves engines over time.
- **Drift/alignment** is computed by Evaluate comparing **current state (Retain) against the reference (Intend)** — the capability the pre-correction model could not express.

## 9. Governance / Authority Model

**Governance is a cross-cutting Authority Plane, not a sequential stage.** It:
- **Constrains inputs** — posture/tier/policy bound what may be perceived, retained, and (critically) **advised** (the candidate space).
- **Governs outputs** — applies **expose / suppress / defer / block** to any stage's outputs and **authorizes** actuation (Tier ∩ Posture ∩ Governance).
- **Holds all authority; generates nothing.** *Cognition generates; Authority governs.* Advise generates candidates; Authority constrains and governs them. Authority never performs Infer/Evaluate/Advise/Disclose/Act.
The Authority Plane is a **Domain of engines** (exposure/authorization) positioned **across** the loop (peer in kind to Perception), correcting the prior in-line placement.

## 10. Advisory Cognition Placement

**Advise is a first-class in-loop responsibility**, positioned **after Evaluate and before Disclose**, **governed by the Authority Plane on both sides** (input constraint + output governance). **Re-grounded boundary (validated):** an output is **Advisory iff it is a governable candidate action** — something a user/agent could choose to enact, and therefore subject to Authority for exposure and authorization. Findings/Issues are descriptive truths (governed for *exposure*, never *authorized as actions*) and are **not** Advisory. Advise owns Recommendations, Clarification Requests, and candidate actions/improvements; it does **not** own severity/confidence/reliability (Evaluate), authority (Governance), rendering (Render/Disclose), or execution (Act). **Resolution Paths remain presentation-only** (multiple Recommendations rendered as paths; no object).

## 11. Intend / Goal Reference Model

**Intend** is the responsibility that establishes and maintains the **desired outcome as a live reference** — the architectural correction without which OSLO cannot compute alignment/drift (its central purpose).
- **Owns:** the declared outcome, its decomposition (success criteria, constraints, intended reality), and its maintenance over time as the **comparison target**.
- **Distinct from Retain:** Retain *stores* facts (including the declared outcome as a record); **Intend** *maintains it as the reference* against which Evaluate computes drift. (Analogous to a control setpoint vs stored data, and to BDI's Desire/Goal vs Belief.)
- **Does not** judge, authorize, or generate; it provides the **reference** every alignment computation requires.
- **Release 1 note:** the project's declared outcome/charter is the Intend reference; in Release 1 it is primarily user-declared (Perceived) and maintained as the alignment target.

## 12. Learn vs Adapt

- **Adapt is emergent, not a responsibility.** "Continuous recompute" is the **loop re-running** on triggers — a property of having a loop + change-detection, owned by no single responsibility (trigger detection belongs to Perceive/Act). It produces **no new behavior**, only re-evaluation on new data.
- **Learn is a distinct responsibility (evolution).** It **improves engines/rules/priors from observed outcomes**, changing **future** behavior. Recompute ≠ learning.
- **Release 1 note:** Adapt (recompute) is **active** in Release 1 (the reanalysis loop); **Learn** is a **future** responsibility (engine improvement over time), not Release 1 scope.

## 13. Coordinate / Multi-Agent Extension

**Coordinate** is the responsibility that **arbitrates/negotiates competing candidate actions across multiple actors/agents**, under the shared Authority Plane. It is distinct from single-actor Advise (one actor's options), Authority (one decision), and Act (one actor's execution). It is the responsibility multi-agent governance and distributed coordination systems require and that the single-actor loop lacks.
- **Scope:** a **future extension** for OSLO's multi-agent/autonomous-coordination direction; **out of Release 1 scope** (Release 1 is single-actor). Named here so the architecture extends additively (add the Coordinate domain under the same Authority) rather than being re-architected later.

## 14. Relationship to Existing OSLO Layers

The prior six "layers" map onto responsibilities; layers are retained only as a **dependency-ordering representation** (read-only upward), not the primary unit:

| Prior layer (representation) | Canonical responsibility / concern |
|---|---|
| **Context Plane** | **Perceive** (cross-cutting Perception) — already a *Plane*, confirming cross-cutting |
| **Knowledge Layer** | **Retain** domain — *and* the **Intend** reference is maintained as a first-class responsibility (newly named, partly drawn from what Knowledge stored) |
| **Reasoning Layer** | **Infer** domain |
| **Judgment Layer** | **Evaluate** domain |
| *(none — was orphaned)* | **Advise** domain *(the previously-missing responsibility)* |
| **Governance Layer** | **Authority Plane** (cross-cutting) — *reclassified from in-line layer* |
| **Communication Layer** | **Disclose** domain (cognitive) **+ Render** service (non-cognitive) — *split* |
| **Execution Coordination** | **Act** domain (+ **Coordinate** for multi-agent); **Adapt** = emergent recompute |
| *(none — future)* | **Learn** responsibility *(evolution)* |

**Dependency direction is preserved** (the valid part of the layer model): responsibilities read lower concerns read-only; nothing writes downward. **Old layer names are retained only where they aid communication; the canonical unit is the responsibility.**

## 15. Release 1 Impact

| Release 1 concept | Responsibility / concern | Notes |
|---|---|---|
| Findings | **Infer** | unchanged |
| Issues, severity, confidence, **CAF, Reliability** | **Evaluate** | Reliability stays here (not Advise) |
| Recommendations, Clarifications, candidate actions | **Advise** (governable candidate generation) | resolves the recurring producer gap |
| Resolution Paths | **Disclose/Render** (presentation-only) | multiple Recommendations rendered as paths; no object (AMB-1) |
| MRI | **Disclose/Render** (Communication) | unchanged (MRI umbrella decision) |
| Finding Panel / Recommendation Panel / Companion | **Disclose/Render** presentation constructs | over Infer/Evaluate/Advise outputs |
| Project outcome / charter | **Intend** (reference) | the alignment target; user-declared in R1 |
| Reanalysis / stale loop | **Adapt** (emergent recompute) | active in R1 |
| Exposure / suppression / authorization | **Authority Plane** | governs R1 output exposure |
| **Learn**, **Coordinate** | — | **out of Release 1 scope** (future) |

**Net:** Release 1 maps cleanly onto the corrected model; the recommendation/clarification ownership gap is closed (Advise); Reliability (Evaluate), MRI (Disclose), and Resolution-Paths (presentation-only) are preserved; **Intend** names the alignment target Release 1 already relies on; **Learn/Coordinate** are explicitly future.

## 16. Conformance Rules

A conforming OSLO architecture MUST (architecture-level, objective):
- **CR-1.** Treat **Responsibility** as the primary unit; **Domain → Engine** as its realization; **Layer/Service/Plane** as orthogonal (representation / support / cross-cutting), not as the primary tree.
- **CR-2.** Implement **Intend** — maintain the desired outcome as a live reference; **Evaluate computes drift against Intend.** (Without Intend, alignment is undefined — non-conformant.)
- **CR-3.** Model **Authority (Governance) as cross-cutting** — constrains inputs and governs outputs across the loop; **Authority generates nothing**; **cognition generates, Authority governs.**
- **CR-4.** Treat **Adapt as emergent** (recompute), **not** a primary responsibility; implement **Learn** separately where evolution is in scope.
- **CR-5.** Keep **Advise** as governable candidate generation (boundary = governable candidate action); it never judges, authorizes, renders, or executes; **Resolution Paths remain presentation-only**.
- **CR-6.** Split **Disclose (cognitive)** from **Render (service)**.
- **CR-7.** **Reliability is Evaluate**, **MRI is Disclose** — not Advise.
- **CR-8.** Preserve **dependency direction** (read-only upward); no responsibility writes downward.
- **CR-9.** **Coordinate** (multi-agent) is additive under the shared Authority; it is not single-actor Advise/Authority/Act.
- **CR-10.** No responsibility overlap, duplication, or orphaning; every cognitive output has exactly one owning responsibility.

**Explicit non-responsibilities (preserved):** Authority generates nothing; Infer/Evaluate/Disclose/Act generate no recommendations; Advise holds no authority/execution; Render performs no cognition; Adapt is not a responsibility.

## 17. Deferred Items

Deferred / out of scope here: implementation, APIs, schemas, databases, frameworks, prompts, vendors, tooling; **Learn** mechanisms and **Coordinate**/multi-agent realization (future responsibilities, named not specified); the **engine catalogs** per domain (named illustratively); numeric/calibration values; and the **GOV-ARCH-001/001A/000** architecture-representation resolution (with which this adoption should be sequenced).

## 18. Final Architecture Recommendation

**Adopt the Cognitive Responsibility Architecture as OSLO's canonical model** (owner-ratified, sequenced with GOV-ARCH-001): **Responsibility-primary**, with the **corrected, validated responsibility set** —
```text
Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act   (→ Coordinate, multi-agent)
```
— **Authority/Perception/Adapt cross-cutting**, **Learn** for evolution, **Render** a service, and **layers retained only as a dependency-ordering representation.** This model is **complete** (it computes alignment via Intend), **correctly governed** (cross-cutting Authority), **evolvable** (Learn), **multi-agent-ready** (Coordinate), and **faithful** to OSLO's intent and separation-of-concerns doctrine — strengthened at the engine grain. It survived adversarial validation; the corrections it incorporates are precisely the ones that validation proved necessary.

---

*This specification canonicalizes OSLO's architecture as a Cognitive Responsibility Architecture, incorporating the corrections validated in Architecture Validation Review 003. It establishes responsibility-primary structure (Responsibility → Domain → Engine, with Layer/Service/Plane as orthogonal axes) and the corrected, validated responsibility set Perceive → Retain → Intend → Infer → Evaluate → Advise → Disclose → Act (→ Coordinate), with Authority/Perception/Adapt cross-cutting, Learn for evolution, and Render as a non-cognitive service. It adds Intend (the maintained outcome reference without which drift/alignment cannot be computed), reclassifies Governance as a cross-cutting Authority Plane that constrains inputs and governs outputs while generating nothing, demotes Adapt to emergent recompute and adds Learn as the distinct evolution responsibility, splits the former Express into cognitive Disclose and service Render, scopes Coordinate as the multi-agent arbitration extension, and preserves Advisory Cognition re-grounded as governable candidate generation. It maps the prior six layers onto these responsibilities (retaining layers only as dependency-ordering representation), assesses Release 1 impact (Findings→Infer; Issues/CAF/Confidence/Reliability→Evaluate; Recommendations/Clarifications→Advise; MRI/Resolution-Paths/panels→Disclose/Render presentation; outcome/charter→Intend; reanalysis→Adapt; Learn/Coordinate future), and defines conformance rules. It is architecture only — no implementation, APIs, schemas, databases, frameworks, prompts, vendors, or tooling — and is canonical upon owner ratification, sequenced with the GOV-ARCH architecture-representation review.*

**OSLO Cognitive Responsibility Architecture Specification v1 complete.**


---

## DL-047 Architecture Update (ratified 2026-06-04) — Synthesis, Extraction, Interaction

No new responsibility is introduced; the change is **additive within existing responsibilities** (DL-047 Part A2 Option 1).

- **Perceive — source-attributed extraction.** "No cognition" is clarified to **"no *Derived* cognition."** Perceive extracts admitted evidence into **evidence-attested assertions** (source-attributed, re-derivable) for Retain. It still produces **no** Findings/assessments.
- **Infer — synthesis + generation (Derived).** Infer additionally **constructs a `SynthesizedPlanningModel` and generates `PlanningArtifact`s** (Intent/Context/Scope/Requirements/WBS/Resources/Schedule). These are **Derived Cognition** — recomputable, history-tracked (CHR per generation), two-axis replay, user-editable, never promoted to Attested-as-truth. Generation is *interpretation*, not authority.
- **Evaluate — seeds from the synthesized model; False-Confidence Detection (CONF-06); Understanding State Model (AE-04).**
- **Disclose — OSLO Chat** (interaction surface; consumes/triggers cognition, generates no canonical), **MRI sub-components**, **assisted-editing intelligence layer**, **CRR status**.
- **Suggested Fixes** = Advise candidate + **user-applied** edit (no autonomous OSLO write). **CAF Review Requests** = stakeholder response → **evidence** (Perceive) → Deep Pass; workflow UI is commodity.

This preserves the epistemic invariants (Canonical=Attested; Derived recomputable; recompute-appends; one-way flow; OSLO-never-accepts; no Authority engine in R1).
