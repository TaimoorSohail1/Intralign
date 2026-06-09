# OSLO Advisory Cognition Architecture Specification v1

**Document Type:** Architecture Specification (role definition — additive) · **Status:** **Draft · Canonical upon Owner Ratification** · **Date:** 2026-05-31
**Establishes (the role evaluated and recommended in):** `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001.md` · `OSLO_RUNTIME_RECOMMENDATION_OWNERSHIP_REVIEW_001.md` · `OSLO_COGNITIVE_ENGINE_ARCHITECTURE_REVIEW_001.md` · `OSLO_ADVISORY_COGNITION_RATIFICATION_REVIEW_002.md` (verdict: **Adopt with modifications**).
**Consistent with / preserves (must not redefine):** `OSLO_ARCHITECTURE_BASELINE_V1.md` (six documented layers + separation-of-concerns doctrine) · `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` · `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md` (MRI umbrella) · `RECOMMENDATION_RESOLUTION_PATHS_RECONCILIATION_DECISION_001.md` (AMB-1, Option A — Resolution Paths presentation-only).

> **Constraints.** **Additive** — preserve all six documented layers; move no responsibility between them except as defined here for the (currently orphaned) generation responsibility. **Architecture only** — no implementation, databases, APIs, frameworks, prompts, or models. **Governance = authority; Advisory = generation.** **Per `CLAUDE.md`, only the owner ratifies/adopts canonical content** — this specification is **canonical upon owner ratification**.

---

## 1. Purpose

**Advisory Cognition exists to own the generation of candidate responses** — the cognitive responsibility that answers **"What should be considered?"** It closes the documented, recurring ownership gap in which **Recommendations, Clarification Requests, Suggested Actions, Candidate Improvements, and Alternative Recommendations** are produced by OSLO yet owned by **no** existing layer (Reasoning, Judgment, Governance, and Communication each explicitly disclaim recommendation generation).

**Architectural problem solved:** OSLO's documented cognitive chain runs *understand → evaluate → authorize → express* (Reasoning → Judgment → Governance → Communication) with **no stage that generates the candidates Governance is meant to authorize.** A complete Outcome Orchestration architecture requires an **option-generation stage between evaluation and authorization** (Review 002). Advisory Cognition is that stage, added **additively** without disturbing existing layers.

**Gap closed:** a single cognitive role now owns all generative-advisory outputs, restoring clean separation of concerns and giving Governance a defined producer to govern.

## 2. Core Responsibility

**Advisory Cognition = "What should be considered?"** — the **forward-generative** synthesis of candidate responses to a judged situation.

| Role | Question | Cognitive operation |
|---|---|---|
| **Reasoning** | What does this imply? | backward-analytic (descriptive inference) — Findings |
| **Judgment** | How important / how sure? | evaluative (state-descriptive) — severity, confidence, CAF |
| **Advisory Cognition** | **What should be considered?** | **forward-generative (candidate synthesis)** — Recommendations, Clarifications |
| **Governance** | What is allowed? | authority (constrain/authorize/expose) |
| **Communication** | How is it explained? | expression (render/disclose) |

**How it differs:** it **generates candidate futures** (interventions, requests, next steps), whereas Reasoning and Judgment **describe the current state**, Governance **authorizes**, and Communication **expresses**. Advisory **produces options**; it does not assess them (Judgment), permit them (Governance), or present them (Communication).

## 3. Ownership Boundaries

| Responsibility | Owner | Advisory owns? |
|---|---|---|
| **Findings** | Reasoning Layer | **No** |
| **Issues** | Judgment Layer | **No** |
| **Recommendations** | **Advisory Cognition** | **Yes** |
| **Clarification Requests** | **Advisory Cognition** | **Yes** |
| **Suggested Actions** | **Advisory Cognition** (a recommendation type) | **Yes** |
| **Alternative Recommendations** | **Advisory Cognition** (multiplicity of Recommendations — *not* a distinct object) | **Yes** (as multiple Recommendations) |
| **Candidate Improvements** | **Advisory Cognition** | **Yes** |
| **Resolution Paths** | **Communication Layer** (presentation construct over multiple Recommendations; **no Resolution-Path object** — AMB-1) | **No** |
| **Reliability** | **Judgment Layer** (descriptive supportability of confidence) | **No** |
| **MRI** | **Communication Layer** (diagnostic rendering — MRI umbrella decision) | **No** |

**Explicit non-ownership.** Advisory Cognition does **not** own: Findings, Issues, severity, confidence, CAF, Reliability (all Judgment/Reasoning); exposure/suppression/authorization (Governance); rendering, MRI, Resolution-Path presentation, panels (Communication). It owns **only the generation of candidate responses.**

## 4. Advisory Cognitive Engines

Advisory Cognition is a **cognitive domain containing single-responsibility engines** (per the Cognitive Engine review and Review 002, Option B).

**Engines that belong (core):**
- **Recommendation Engine** — generates **Recommendations** (advisory candidate responses anchored to a Finding/Issue), including **next-best-action recommendations** and **multiple alternatives** (multiplicity, not a separate object).
- **Clarification Engine** — generates **Clarification Requests** (advisory candidate requests to resolve ambiguity and improve understanding; feed user input → reanalysis).

**Candidate engines — folded or excluded (taxonomy discipline):**
- **Suggested Action Engine** — **folded into the Recommendation Engine** as a recommendation type unless the owner elects to separate it (avoids bloat); Suggested Actions are advisory candidate next steps = recommendations.
- **Alternative Recommendation Engine** — **does NOT belong.** "Alternatives" are the Recommendation Engine producing **multiple Recommendations** for one Finding/Issue; "Possible Resolution Paths" is the **Communication** presentation over them (AMB-1). No separate engine, no Resolution-Path object.
- **Resolution Path Engine** — **excluded.** Resolution Paths are presentation-only; generating Resolution-Path objects would violate AMB-1.

**Engine qualification criteria (for any future Advisory engine):** an engine qualifies **only if** it (1) **generates candidate responses** (forward-generative, prospective); (2) **anchors traceably** to a Finding or Issue; (3) is **advisory** — non-authoritative, non-executing; (4) is a **single cognitive capability** (one responsibility); and (5) produces outputs that are **governable by Governance**. An "engine" that assesses state (Judgment), authorizes (Governance), or renders (Communication) does **not** qualify.

## 5. Runtime Placement

Advisory Cognition sits **between Judgment and Governance** in cognitive order:

```text
Context Plane → Knowledge → Reasoning → Judgment → Advisory Cognition → Governance → Communication
                                                          ▲   │
                                          (constrained by │   │ candidate responses)
                                           Governance      │   ▼
                                           posture/tier)   Governance disposition/authorization
```

- **Inputs:** **Issues** (from Judgment) and their **Findings** (Reasoning) and **canonical context** (Knowledge, read-only); plus **Governance constraints** (posture/tier/policy) that **bound the candidate-generation space** (§6).
- **Outputs:** **candidate responses** (Recommendations, Clarification Requests) — anchored to their Finding/Issue, advisory, **ungoverned at the point of generation** and handed to Governance for disposition.
- **Dependencies:** Judgment (for Issues), Reasoning/Knowledge (for grounding), Governance (for input constraint and output disposition), Communication (downstream rendering). **Recompute loop** includes Advisory: when Knowledge/Reasoning/Judgment change, Advisory re-generates.

## 6. Governance Interaction Model

Advisory Cognition is **governed on both sides** while remaining **non-authoritative**:

- **Input constraint (Governance → Advisory).** **Posture, Tier, and Policy bound the candidate space** Advisory may generate — Advisory does not generate candidates outside what current Posture/Tier/Governance permit to exist (matching documented Stage 12, "constrained by Posture/Tier/Governance policy"). This is a **constraint on generation**, not authorization.
- **Output disposition (Advisory → Governance).** Generated candidates are handed to Governance, which applies **exposure governance — expose / suppress / defer / block** — and **authorization** where an action is implicated. Advisory **never** decides exposure or authorization.
- **Posture:** bounds which candidate responses are generable (e.g., delegated-posture-only candidate types) and how they may later be coordinated; Advisory respects posture as an input constraint only.
- **Tier:** bounds candidate availability per Tier Capability policy; an input constraint.
- **Policy / exposure / suppression / deferment / authorization:** **all owned by Governance**, applied to Advisory outputs.

**Non-authority invariant:** Advisory **generates**; Governance **governs**. Advisory holds no approval, authorization, exposure, suppression, or execution authority. *(The bidirectional relationship — input constraint + output disposition — keeps authority wholly in Governance.)*

## 7. Release 1 Mapping

| Release 1 concept | Owner | Producer | Consumer | Governance involvement | Communication involvement |
|---|---|---|---|---|---|
| **Recommendations** | **Advisory Cognition** | Advisory (Recommendation Engine) | user (via render) | constrains generation; governs exposure | renders (Recommendation Panel) |
| **Clarifications** | **Advisory Cognition** | Advisory (Clarification Engine) | user → reanalysis | constrains/governs exposure | renders (in context) |
| **Suggested Actions** | **Advisory Cognition** (rec type) | Advisory (Recommendation Engine) | user | governs exposure/authorization | renders |
| **Reliability** | **Judgment Layer** | Judgment | Governance/Communication | — | renders (reliability-qualified) |
| **MRI** | **Communication Layer** | — (renders Reasoning/Judgment outputs) | user | exposure of contents | **renders** (diagnostic) |
| **Recommendation Panel** | **Communication** (presentation construct) | renders **Advisory** outputs | user | governed exposure of recommendations | **renders** |
| **Finding Panel** | **Communication** (presentation construct) | renders Finding (Reasoning) + Issue (Judgment) + Recommendation (**Advisory**) | user | governed exposure | **renders** |
| **Companion** | **Communication** (presentation surface) | renders existing understanding (incl. Advisory recs via Finding) | user | governed exposure | **renders** |

**Net Release 1 resolution:** Advisory Cognition gives **Recommendations, Clarifications, and Recommendation-Panel content** a documented producer (closing the C-1 gap and the Recommendation-Panel conflict); **Finding Panel** cleanly spans Reasoning + Judgment + Advisory; **Reliability** (Judgment) and **MRI** (Communication) are **unaffected**; **Resolution Paths** stay presentation-only.

## 8. Conformance Rules

A conforming Advisory Cognition role MUST satisfy (architecture-level, objective):
- **AC-1.** Advisory Cognition **generates candidate responses** (Recommendations, Clarification Requests, candidate actions/improvements).
- **AC-2.** Advisory Cognition **never authorizes.**
- **AC-3.** Advisory Cognition **never exposes/suppresses/defers/blocks** (Governance owns exposure).
- **AC-4.** Advisory Cognition **never executes** or coordinates actuation.
- **AC-5.** Advisory Cognition **never determines severity** (Judgment).
- **AC-6.** Advisory Cognition **never determines confidence, CAF, or Reliability** (Judgment).
- **AC-7.** Advisory Cognition **never produces Findings or Issues** (Reasoning/Judgment).
- **AC-8.** Advisory Cognition **never renders** or owns MRI/panels/Resolution-Path presentation (Communication).
- **AC-9.** Advisory outputs **anchor traceably** to a Finding/Issue.
- **AC-10.** Advisory generation is **constrained by** Governance posture/tier/policy (input), and Advisory outputs are **governed by** Governance (output).
- **AC-11.** Advisory may generate **multiple Recommendations**; it **does not** generate **Resolution-Path objects** (AMB-1 — presentation-only).
- **AC-12.** **Governance never generates recommendations** (authority ≠ generation); **Reasoning/Judgment/Communication never generate recommendations** (preserved non-responsibilities).
- **AC-13.** Advisory Cognition is **additive** — it removes no responsibility from any existing layer and adds none to them; it claims only the previously-orphaned generation responsibility.
- **AC-14.** Engines within Advisory Cognition satisfy the **§4 qualification criteria** (single forward-generative, finding/issue-anchored, advisory, governable capability).

**Non-responsibilities (explicit):** authority, approval, authorization, execution, exposure, suppression, severity, confidence, CAF, Reliability, Findings, Issues, rendering, MRI, panel presentation, Resolution-Path objects.

## 9. Future Evolution

Advisory Cognition is the **bridge from understanding to governed action**, and becomes the keystone of OSLO's forward capabilities:
- **Execution Intelligence** — drift signals (Reasoning/Judgment) require **generated candidate responses** for Governance to authorize and Execution to coordinate; Advisory supplies them.
- **Outcome Orchestration** — the closed loop (understand → evaluate → **generate** → authorize → coordinate → observe → adapt) cannot close without Advisory's generation stage.
- **Agent Governance** — agent actions are **generated candidates** that must be governed; Advisory provides the bounded, governable generation surface that Agent Governance authorizes.
- **Governed Automation** — automated responses are pre-authorized **candidate generations**; Advisory is where they originate, under Governance bounds.
- **Autonomous Coordination** — multi-actor coordination depends on a stream of governable candidate actions; Advisory is their cognitive home.

**Future Advisory responsibilities** (naturally belonging, by the §4 criteria, subject to owner ratification): candidate **next-best-action** generation; candidate **drift-response** generation; candidate **coordination plans** (generation only — authorization and actuation remain Governance/Execution). All remain **advisory and governed** — Advisory never gains authority or execution.

## 10. Final Architecture Recommendation

**Recommended: Option B — Advisory Cognition is a *cognitive domain containing engines*.**

- **B (recommended):** a named **cognitive domain** ("Advisory Cognition") hosting single-responsibility engines (Recommendation, Clarification). **Advantages:** names the **cognitive role** (real, governable boundary) while keeping **engines as the single-responsibility unit** (separation of concerns at the finest grain); unifies with the Cognitive Engine review; additive and minimal. **Disadvantage:** requires formalizing the domain/engine taxonomy.
- **A (acceptable alternative):** a **new runtime layer** peer to Reasoning/Judgment. **Advantage:** clearest parity expression of a cognitive stage. **Disadvantage:** heavier; coarser than engines. *(A and B express the same truth; choose per owner preference for layer-parity vs domain-granularity.)*
- **C (rejected):** embedding in an existing layer — **invalid**; every existing layer is the wrong cognitive operation and disclaims generation; reintroduces the leak.
- **D (not preferred):** a cross-cutting service — misplaces a **sequential** stage (between evaluate and authorize) as cross-cutting.

**Rationale:** Option B is the most architecturally correct **additive** model — it adds exactly the missing generation stage as a governed cognitive domain, preserves all six layers and OSLO's separation doctrine, keeps Governance's authority intact (generation constrained and governed by Governance), and honors the ratified Release 1 decisions (MRI = Communication; Resolution Paths presentation-only; Reliability = Judgment).

---

## Final Question — Does adopting Advisory Cognition improve OSLO's architectural completeness, clarity, and long-term ability to support governed execution?

**Yes — on all three.**

- **Completeness:** it **closes a structural omission.** OSLO's documented chain lacked the option-generation stage required by any complete decision/orchestration architecture; Advisory Cognition supplies it, completing *understand → evaluate → **generate** → authorize → express → act.*
- **Clarity:** it **removes ambiguity and ends the recurring ownership conflicts.** Recommendations, Clarifications, and candidate actions now have a **single owner**; every adjacent layer's documented non-responsibility becomes coherent (they disclaim generation precisely because Advisory owns it). Separation of concerns is **strengthened**, not diluted — the orphaned, leaking responsibility is given a clean home.
- **Long-term governed execution:** it is the **prerequisite** for everything OSLO intends to become. Governed execution is *governed action on generated candidates*; without a bounded, governable generation stage, generated actions have no clean home or governance boundary — undermining OSLO's core promise of **governed AI**. Advisory Cognition is the role that turns understanding into **governable candidate action**, with authority preserved wholly in Governance.

Adopting Advisory Cognition (as an additive cognitive domain, governed on both sides, correctly scoped) **completes OSLO's cognitive architecture, clarifies its ownership boundaries, and equips it for governed execution** — while preserving OSLO's original intent, its six existing layers, its separation-of-concerns doctrine, and its ratified Release 1 decisions.

---

*This specification defines Advisory Cognition — OSLO's additive cognitive role answering "What should be considered?" — that owns the generation of candidate responses (Recommendations, Clarification Requests, Suggested Actions, Candidate Improvements, and multiple Alternative Recommendations) which no existing layer owns. It defines the core responsibility (forward-generative synthesis, distinct from Reasoning's inference, Judgment's evaluation, Governance's authority, and Communication's expression); ownership boundaries (Advisory owns recommendation/clarification generation; it does NOT own Findings, Issues, severity/confidence/CAF/Reliability (Judgment/Reasoning), exposure/authorization (Governance), or MRI/Resolution-Path-presentation/panels (Communication)); a cognitive-engine model (Recommendation and Clarification engines core; Suggested Action folded; Alternative Recommendation = multiplicity not an engine; Resolution Path excluded) with qualification criteria; runtime placement between Judgment and Governance with two-sided Governance interaction (posture/tier/policy constrain generation; Governance governs exposure/authorization); a Release 1 mapping that closes the Recommendation/Clarification producer gaps while leaving Reliability (Judgment) and MRI (Communication) unaffected and Resolution Paths presentation-only; conformance rules (Advisory generates, never authorizes/exposes/executes/judges); future evolution as the keystone for execution intelligence, outcome orchestration, agent governance, governed automation, and autonomous coordination; and a final recommendation that Advisory Cognition be modeled as a cognitive domain containing engines (Option B), additive and governance-preserving. It is architecture only — no implementation, databases, APIs, frameworks, prompts, or models — and is canonical upon owner ratification.*

**OSLO Advisory Cognition Architecture Specification v1 complete.**
