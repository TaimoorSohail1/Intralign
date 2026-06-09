# OSLO Architecture Review — Cognitive Responsibility Architecture vs Layer Architecture

**Document Type:** First-Principles Architecture Review (advisory — owner ratifies) · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Mode (as instructed):** Optimize for **architectural correctness, cognitive-systems design, decision-architecture design, scalability, agentic evolution, governed automation, outcome orchestration.** **Do not** optimize for preservation, minimal change, current terminology, or backward compatibility. Documentation may be cited as evidence but does **not** constrain the conclusion; redesign is permitted. Per `CLAUDE.md`, adoption is owner-ratified.
**Builds on:** the Advisory Cognition arc (`OSLO_ADVISORY_COGNITION_RATIFICATION_REVIEW_002.md`, `OSLO_ADVISORY_COGNITION_ARCHITECTURE_SPECIFICATION_V1.md`).

---

## Primary Question

> Has OSLO discovered that it is fundamentally a **Layer Architecture** or a **Cognitive Responsibility Architecture**?

**Answer (first-principles): OSLO is fundamentally a *Cognitive Responsibility Architecture* that has been *represented* as a Layer Architecture.** "Layers" are a (partially lossy) **representation** of underlying cognitive responsibilities — specifically a **dependency-ordering representation**. The recurring ownership conflicts, culminating in Advisory Cognition, are the signature of a **representation that lost a responsibility**: you cannot "discover a missing responsibility with no layer" unless responsibilities — not layers — are the fundamental unit.

---

## Task 1 — Minimum complete architecture from first principles

*Purpose:* **continuously align execution toward desired outcomes through understanding, evaluation, guidance, governance, and adaptation.** Ignoring all layer names, the **minimum set of responsibilities (verbs)** this purpose requires:

1. **Perceive** — acquire external information (intake, normalization, promotion-readiness).
2. **Retain** — hold canonical state (knowledge, assumptions, history, epistemics).
3. **Infer** — derive implications (findings, gaps, conflicts, risks).
4. **Evaluate** — weigh importance and certainty (severity, confidence, CAF, reliability, epistemic state).
5. **Advise** — generate candidate responses (recommendations, clarifications, candidate actions). *(The stage the layer model lost.)*
6. **Authorize** — govern what is allowed (exposure, suppression, deferment, blocking, authorization; posture/tier/policy).
7. **Express** — communicate (rendering, disclosure, presentation).
8. **Act** — coordinate authorized execution (posture-gated mutation).
9. **Adapt** — recompute/learn on change (always-on feedback closing the loop).

These nine are **responsibilities**, not layers. Each is a distinct *thing the system must do*; remove any and the purpose cannot be met. This is the **minimum complete responsibility set** — and it is a **loop**, not a stack (Adapt feeds Infer; Perceive and Adapt are continuous/cross-cutting).

## Task 2 — Canonical cognitive stages vs known architectures

| Responsibility (OSLO purpose) | OODA | BDI agents | Control systems | Decision theory | Autonomous agents | Multi-agent governance |
|---|---|---|---|---|---|---|
| Perceive | Observe | Perception | Sense | (inputs) | Sensors | Observation |
| Retain | (Orient) | Beliefs | State estimate | State/model | World model | Shared state |
| Infer | Orient | Belief revision | Plant model | Inference | Reasoning | — |
| Evaluate | Orient | Desire weighting | Error/cost | Utility | Utility/value | — |
| **Advise (generate options)** | (pre-Decide) | **Means–ends / option generation** | **Candidate control law** | **Alternative generation** | **Planning / option generation** | **Proposal generation** |
| Authorize | Decide | Intention selection | Actuation gate | Choice | Action selection | **Governance / authorization** |
| Act | Act | Act | Actuate | — | Actuation | Coordinated execution |
| Adapt | (loop) | Reconsideration | Feedback | Update | Learning | Renegotiation |

**A canonical pattern emerges, identically, across all of them:**
```text
Perceive → Retain → Infer → Evaluate → Advise → Authorize → Express/Act → Adapt (loop)
```
Two invariants are decisive: **(a) option-generation (Advise) is always a distinct stage** between evaluation and decision — never absent; **(b) in multi-agent governance, authorization is a distinct responsibility separate from generation** — exactly OSLO's Governance-≠-Advisory split. OSLO's *responsibilities* map perfectly onto this universal loop; OSLO's *layer naming* is one particular (and incomplete) packaging of it. **The canonical pattern is a responsibility loop, not a layer stack.**

## Task 3 — Classification of each current OSLO element

| Element | Best classification | Justification |
|---|---|---|
| **Context Plane** | **Cross-cutting Responsibility (Perceive)** — represented as a *Plane*, not a Layer | OSLO **already** declines to call it a "Layer" (it is a cross-cutting *Plane*) — direct evidence the layer metaphor is inconsistent and responsibilities are primary. |
| **Knowledge Layer** | **Cognitive Responsibility (Retain)** | A single responsibility (memory) housed in a "layer" container. |
| **Reasoning Layer** | **Cognitive *Domain* (Infer)** containing engines | Holds multiple engines (gap/alignment/traceability/feasibility) → a domain of a responsibility, not an atomic layer. |
| **Judgment Layer** | **Cognitive Domain (Evaluate)** containing engines | Severity/confidence/CAF/reliability engines. |
| **Advisory Cognition** | **Cognitive Domain (Advise)** containing engines | Recommendation/Clarification engines. |
| **Governance Layer** | **Cross-cutting Cognitive Domain (Authorize)** containing engines | Exposure/authorization engines; **constrains Advisory input and governs all outputs** → cross-cutting authority, not a single stacked layer. |
| **Communication Layer** | **Cognitive Domain (Express)** containing engines | Rendering/disclosure engines (incl. MRI diagnostic, panels). |
| **Execution Coordination** | **Cross-cutting Responsibility (Act/Adapt)**, posture-gated | Signal ingestion + recompute (cross-cutting) + posture-gated actuation. |

**Result:** **every element is a cognitive responsibility or a domain of engines** — *none* is fundamentally a "Layer." "Layer" is the **representation word**; the **invariant unit is the responsibility.** Note two are already *not* layers (Context **Plane**; Execution **Coordination**) and two are inherently **cross-cutting** (Perceive, Authorize) — the stack metaphor mis-describes them.

## Task 4 — Is "Layer" the wrong abstraction?

**Layers get one thing right and one thing wrong.**
- **Right (keep):** layers encode **dependency direction** — lower responsibilities are read-only to higher ones (Reasoning reads Knowledge; Judgment reads Reasoning; nothing writes downward). This **dependency-ordering discipline is valuable and correct.**
- **Wrong (correct it):** layers are treated as the **primary unit**, implying a **strict linear stack** where each consumes only the one below. OSLO's real flow is **not** a clean stack: it is a **loop** (Adapt → Infer), with **cross-cutting** responsibilities (Perceive, Authorize) and **bidirectional** Governance (constrains Advisory input *and* governs its output). The stack metaphor **cannot represent** these — and it **hid Advisory** (a stage with "no layer").

**Conclusion:** **"Layer" is not the correct *primary* organizing principle. Cognitive Responsibility is.** Layers are a **secondary, representational concept — a dependency-ordering view of responsibilities** — useful but lossy. The canonical organizing abstraction should become the **Cognitive Responsibility** (expressed as a **Domain of Engines**), with **layering retained only as a dependency-ordering representation.**

## Task 5 — Layer vs Responsibility vs Hybrid

**Recommended: Option C — Hybrid, with Cognitive Responsibility *primary* and Layer *representational*.**

- **Pure Layer (A):** rejected as primary — it mis-models loops, cross-cutting, and bidirectional governance, and it lost Advisory.
- **Pure Responsibility (B):** correct fundamentally, but discards the *valuable* dependency-ordering discipline layers encode and the human-legibility of grouped stages.
- **Hybrid (C) — recommended.** Define the relationship precisely (primacy ordered top-to-bottom):

```text
PRIMARY    Cognitive Responsibility   — the invariant verb (Perceive, Retain, Infer, Evaluate, Advise, Authorize, Express, Act, Adapt)
           Cognitive Domain           — a responsibility containing engines (Inference/Reasoning, Evaluation/Judgment, Advisory, Authority/Governance, Expression/Communication)
           Engine                     — single-capability unit within a domain (one responsibility; the finest separation-of-concerns grain)
SECONDARY  Layer (dependency view)    — a representational ordering of responsibilities by read-only dependency direction (NOT the primary unit)
SUPPORT    Service                    — cross-cutting operational concern not in the cognitive loop (e.g., determinism/replay, identity, time-semantics)
```

**Which is primary:** **Responsibility → Domain → Engine** is the primary structural axis; **Layer** is a **secondary representation** (dependency-ordering); **Services** are cross-cutting support. This preserves what layers got right (dependency direction) while fixing the primacy error that produced the ownership gaps.

## Task 6 — Canonical Architecture Model (blank-sheet)

A **Cognitive Responsibility Architecture** — responsibilities as domains of engines, arranged as a governed control loop:

```text
                         ┌──────────────────────── ADAPT (always-on recompute/learn) ───────────────────────┐
                         │                                                                                   │
   PERCEIVE ─▶ RETAIN ─▶ INFER ─▶ EVALUATE ─▶ ADVISE ─▶ [AUTHORIZE] ─▶ EXPRESS ─▶ ACT(posture-gated)        │
  (Context)  (Knowledge)(Reason.) (Judgment)  (Advisory)  (Governance)  (Comms)   (Execution Coord.) ─────────┘
                                                  ▲           │
                                  constrains input│           │governs output (expose/suppress/defer/block/authorize)
                                                  └───────────┘
  Cross-cutting: PERCEIVE (intake), AUTHORIZE (governance over every output), ADAPT (recompute loop).
  Each domain = a set of single-responsibility ENGINES.  Dependency direction is read-only upward (the "layer" discipline, retained).
```

**Domains & engines (illustrative):**
- **Perception** — intake/normalization/promotion engines (cross-cutting).
- **Retention** — canonical-knowledge/assumption/history/epistemic engines.
- **Inference** — gap/alignment/traceability/feasibility engines.
- **Evaluation** — severity/confidence/CAF/reliability/epistemic engines.
- **Advisory** — recommendation/clarification/(suggested-action) engines.
- **Authority (Governance)** — exposure/suppression/deferment/blocking/authorization engines (cross-cutting; posture/tier/policy).
- **Expression (Communication)** — rendering/disclosure engines (incl. MRI diagnostic, panels).
- **Coordination (Execution)** — signal-ingestion/recompute/posture-gated-actuation engines (cross-cutting).

**Why this supports every required future:** each future capability is **a new engine or governed responsibility within the same loop**, not a re-stacking:
- **Planning Intelligence** = Inference + Evaluation + Advisory engines (already present).
- **Execution Intelligence / Outcome Orchestration** = Coordination + Adapt engines closing the loop on real execution.
- **Agent Governance / Multi-Agent Systems** = each agent is an instance/participant of the responsibility loop, with **Authority as the shared cross-cutting governor** — the responsibility model **scales to multi-agent** (a rigid stack does not).
- **Governed Automation / Autonomous Coordination** = pre-authorized Advisory generation + Authority + Coordination engines, all within the same governed loop.
**Extensibility = add engines/domains; never re-architect the stack.** This is the model that **naturally emerges** from designing Outcome Orchestration correctly.

## Task 7 — Advisory Cognition assessment

- **Classification:** a **Cognitive Domain (Advise)** containing engines — *not* a mere capability/engine (too large — a whole responsibility), *not* a "Layer" (wrong primary abstraction).
- **Necessity:** **(1) architecturally necessary** (the universal option-generation stage — Task 2) **and (3) evidence of a larger architecture shift** — its discovery is the *proof* that OSLO is a Cognitive Responsibility Architecture. It is **not (2) structurally optional.**
- **Deeper meaning:** Advisory Cognition is **a missing cognitive stage whose discovery exposed the deeper truth** — that **responsibilities, not layers, are OSLO's fundamental organizing abstraction.** The system did not merely find a missing capability; it found that its **representation model** (layers) was hiding a responsibility, which means the **responsibility model is primary.**

## Deliverables

### 1. Architectural Findings
- OSLO's recurring ownership conflicts are not missing capabilities; they are a **representation losing a responsibility** — possible only if **responsibilities are primary** and layers are a representation.
- The minimum complete architecture is a **9-responsibility governed control loop**, matching the canonical pattern across OODA/BDI/control/decision/agent/multi-agent systems.
- **Every** current OSLO element classifies as a **responsibility or domain-of-engines**, not a fundamental layer; two are already non-layers (Plane, Coordination) and two are cross-cutting (Perceive, Authorize).
- Layers correctly encode **dependency direction** but wrongly serve as the **primary unit**; the stack metaphor mis-models OSLO's loop, cross-cutting, and bidirectional governance.

### 2. Architecture Classification
**Hybrid — Cognitive Responsibility Architecture (primary) with a Layer (dependency-ordering) representation (secondary).** Fundamentally a Cognitive Responsibility Architecture.

### 3. Canonical Architecture Model
Task 6 — responsibilities as **Domains of Engines** in a **governed control loop**, with Authority/Perception/Adapt cross-cutting and read-only dependency direction retained.

### 4. Responsibility Hierarchy
**Cognitive Responsibility (primary) → Domain → Engine; Layer = secondary dependency-ordering representation; Service = cross-cutting support.** Responsibility/Domain/Engine is the primary axis; Layer is representational; Engines are the single-responsibility grain.

### 5. Advisory Cognition Assessment
**A necessary cognitive stage (Advise) and the evidence of the deeper discovery** that OSLO is a Cognitive Responsibility Architecture. Best modeled as a **Cognitive Domain of engines**; architecturally necessary; not optional.

### 6. Architectural Recommendation
**If designing OSLO today from first principles, adopt a Cognitive Responsibility Architecture (Hybrid, responsibility-primary).** Reframe OSLO's "Layers" as **Cognitive Domains** (each a responsibility composed of engines), retain **layering only as a dependency-ordering representation**, recognize **Perception/Authority/Adaptation as cross-cutting**, and model **Advisory Cognition as a domain** within the loop. **OSLO should evolve toward this model** — *additively and owner-ratified*: it changes **vocabulary and primacy, not the actual responsibilities** (the responsibilities already exist; this names them correctly and adds the missing Advisory domain). Sequence the reframing **after / alongside** the architecture-representation governance review (GOV-ARCH-001/001A/000), since *which representation is canonical* is the exact question that review must settle — and this analysis is the strongest evidence for resolving it toward a **responsibility-primary** model.

**Why:** the responsibility model is **complete** (it cannot "lose" a stage — every required verb is named), **scalable** (extend by adding engines, not re-stacking), **multi-agent-ready** (agents instantiate the loop under shared Authority), and **self-correcting** (it explains *why* the ownership gaps occurred and prevents their recurrence). It preserves OSLO's true intent and its separation-of-concerns doctrine — indeed it **strengthens** separation by making the **engine** the unit of single responsibility — while discarding only the **lossy layer-as-primary representation** that caused the conflicts.

---

*This first-principles review determines that OSLO is fundamentally a Cognitive Responsibility Architecture that has been represented as a Layer Architecture. Deriving the minimum complete architecture for Outcome Orchestration from scratch yields a nine-responsibility governed control loop (Perceive → Retain → Infer → Evaluate → Advise → Authorize → Express → Act → Adapt) that matches the canonical pattern across OODA, BDI, control systems, decision theory, autonomous agents, and multi-agent governance — in all of which option-generation (Advise) is a distinct stage and authorization is separate from generation. Classifying each current OSLO element shows every one is a cognitive responsibility or domain-of-engines, not a fundamental layer (two are already non-layers; two are cross-cutting), revealing that "Layer" correctly encodes dependency direction but wrongly serves as the primary unit and cannot model OSLO's loop, cross-cutting responsibilities, or bidirectional governance — and that the layer-as-primary representation is what hid the Advisory responsibility. It concludes a Hybrid architecture with Cognitive Responsibility primary (Responsibility → Domain → Engine) and Layer as a secondary dependency-ordering representation, supported by cross-cutting services; presents a blank-sheet canonical model of responsibilities-as-domains-of-engines in a governed control loop that extends to planning/execution intelligence, agent governance, governed automation, and multi-agent systems by adding engines rather than re-stacking; assesses Advisory Cognition as a necessary cognitive stage and the evidence of this deeper architectural discovery; and recommends OSLO evolve — additively and owner-ratified, sequenced with the GOV-ARCH architecture-representation review — toward a responsibility-primary model that names the responsibilities OSLO already performs, adds the missing Advisory domain, and strengthens separation of concerns at the engine grain. It optimizes for architectural correctness over preservation, as instructed, and frames adoption as an owner decision.*

**OSLO Architecture Review — Cognitive Responsibility Architecture vs Layer Architecture complete.**
