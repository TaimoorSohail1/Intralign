# OSLO Advisory Cognition Ratification Review 002

**Document Type:** Systems Architecture Review (first-principles; advisory — owner ratifies) · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Mode:** **First-principles architectural evaluation — optimize for architectural correctness, not repository consistency.** Repository evidence is used where relevant (OSLO original intent: `OSLO_ARCHITECTURE_BASELINE_V1.md` §1–§3), but the question is whether a **complete Outcome Orchestration architecture** *requires* Advisory Cognition, evaluated as architecture. Builds on `OSLO_ADVISORY_COGNITION_REVIEW_001.md` (and the three prior reviews). Per `CLAUDE.md`, formal adoption is owner-ratified; this is the architectural recommendation.

---

## Framing: what a complete outcome-cognition system must do

Evaluated as a cognitive architecture, OSLO's purpose (preserve trustworthy understanding **and** drive toward outcomes — §1: *"detecting drift, recommending action, and (where authorized) coordinating execution"*) is a **decision-and-control** purpose. Every mature decision/control architecture decomposes into the same canonical stages:

| Canonical stage | OODA | BDI agents | Decision theory | Control | OSLO (documented) |
|---|---|---|---|---|---|
| Perceive | Observe | Perception | — | Sense | **Context Plane** |
| Hold state | — | Beliefs | State | State | **Knowledge** |
| Infer | Orient | (belief revision) | Model | Estimate | **Reasoning** |
| Evaluate | Orient | Desire weighting | Utility/value | Error/cost | **Judgment** |
| **Generate options** | (pre-Decide) | **Means–ends / option generation** | **Alternative generation** | **Candidate control law** | **— (absent)** |
| Decide / authorize | Decide | Intention selection | Choice | Actuation gate | **Governance** |
| Express / act | Act | Act | — | Actuate | **Communication** / Execution |

**The cross-architecture invariant:** in every complete decision architecture, **option/candidate generation is a distinct stage *between* evaluation and decision.** You cannot decide among options that were never generated; you cannot authorize a candidate action that no stage produced. OSLO's documented chain **collapses this stage** — it runs **Judgment (evaluate) → Governance (authorize)** with **no stage that generates the candidates Governance is meant to authorize.** That collapse is the architectural defect; the recurring ownership gaps are the system **rediscovering the missing stage.**

This is the first-principles answer, independent of documentation: **a complete Outcome Orchestration architecture necessarily contains an option-generation (Advisory) stage.**

## Cognitive Analysis — Is Advisory Cognition a valid cognitive responsibility?

**Yes — it is a canonical, distinct cognitive responsibility.** Reasoning, Judgment, and Advisory are three different cognitive *operations*:
- **Reasoning** is **backward-analytic**: given the current structure, *what is implied?* (descriptive — Findings/gaps).
- **Judgment** is **evaluative**: given the implications, *how important / how sure?* (state-descriptive — severity/confidence/CAF).
- **Advisory** is **forward-generative**: given the judged situation, *what should be considered in response?* (prospective synthesis — candidate recommendations/clarifications/actions).

The first two **describe reality**; the third **generates candidate futures.** Generating a candidate intervention is a *synthesis* over a space of possible actions and their fit to the judged state — a categorically different operation from inferring a gap or scoring it. OSLO already draws the finer line between *implication* (Reasoning) and *importance* (Judgment); the **same granularity logic** mandates separating *response generation* (Advisory) from both. Advisory is **not** Governance (authority, not generation) and **not** Communication (expression, not generation).

### Evaluation Questions 1–6
- **Q1 — Is Recommendation Generation fundamentally different from Reasoning/Judgment/Governance?** **Yes.** It is *generative/prospective* (proposing candidate responses) versus Reasoning's *descriptive inference* and Judgment's *evaluative weighting*; and it is *production*, not Governance's *authorization*. Different cognitive direction, object, and output.
- **Q2 — Merely a capability, or a distinct cognitive responsibility?** **A distinct responsibility.** A "capability" framing is why it kept failing to find a home — capabilities attach to a responsibility; generating candidate responses is a *responsibility* (a cognitive stage), of which Recommendation/Clarification are capabilities.
- **Q3 — Would a complete Outcome Orchestration architecture contain Understanding → Evaluation → Advisory → Authorization as separate stages?** **Yes — necessarily.** This is the canonical decision decomposition (see the cross-architecture table). Authorization without an Advisory stage has nothing to authorize; Advisory without Authorization is ungoverned generation. Both stages are required and distinct.
- **Q4 — Strengthen or weaken separation of concerns?** **Strengthen — decisively.** A missing stage forces its work to **leak** into adjacent stages (Reasoning over-reaching into recommendations, or Governance generating what it should only authorize) — *that* is the separation violation. Naming Advisory gives the work a single home and **restores** clean role boundaries. The current orphaned state is the violation; Advisory is the fix.
- **Q5 — Does Advisory better explain the recurring conflicts than alternatives?** **Yes — it is the single hypothesis that fits all the data.** Alternatives ("assign to Reasoning / Judgment / Governance") each fail against a role's nature (each is the wrong cognitive operation) and would each require an exception. One missing stage explains **all** the recurring gaps (recommendations, clarifications, candidate improvements, alternatives, next-best-actions) simultaneously — they are all "generated candidate responses." Parsimony favors the role.
- **Q6 — As OSLO evolves toward Execution Intelligence / Outcome Orchestration / Autonomous Coordination / Agent Governance / Governed Automation, does Advisory become more or less important?** **Far more important — it becomes the keystone.** Every one of those capabilities is *governed action on generated candidates.* Drift detection (Reasoning/Judgment) is inert without **generated candidate responses** for Governance to authorize and Execution to coordinate. Autonomy and agent coordination specifically require a **well-bounded, governable generation stage** — without a named Advisory role, generated actions have no clean home and no clean governance boundary, which would undermine OSLO's central promise of **governed** AI. Advisory Cognition is precisely the **bridge from understanding to governed action.**

## Architectural Analysis — Is OSLO currently missing it?

**Yes.** OSLO's documented chain has the Advisory stage **collapsed**: Judgment → Governance with no generation stage, while the purpose statement requires recommending action and §5 asserts a Recommendation/Clarification Engine with no owning role. This is a **structural omission**, not a documentation oversight: the architecture *performs* advisory work (it must, to recommend) but has **no role boundary for it**, which is why every adjacent role disclaims it and why the ownership conflicts recur. The architecture is **incomplete relative to its own purpose.**

## Future-State Analysis — Does Outcome Orchestration naturally require it?

**Yes — unavoidably.** Outcome Orchestration is *closed-loop governed action toward outcomes.* Its loop is: understand → evaluate → **generate candidate responses** → authorize → coordinate → observe → adapt. Remove the generation stage and the loop cannot close (there is nothing to authorize or coordinate). As OSLO scales from single-outcome understanding to portfolio orchestration and autonomous/agent coordination, the **volume, governability, and accountability** of generated candidates grow — making a **distinct, bounded, governable Advisory stage** not merely useful but **load-bearing.** A first-principles Outcome Orchestration architecture *cannot* omit it.

## Recommended Architecture (Q7) — first-principles, preserving OSLO intent

**Seven cognitive roles + posture-gated execution**, preserving OSLO's documented roles and adding the missing generation stage:

```text
Context Plane       — perceive     — "What information exists?"
Knowledge Layer     — remember     — "What is known?"
Reasoning Layer     — infer        — "What does this imply?"            → Findings, gaps
Judgment Layer      — evaluate     — "How important / how sure?"        → Issues, severity, confidence, CAF
Advisory Cognition  — deliberate   — "What should be considered?"       → Recommendations, Clarification Requests,
                                                                          candidate actions / improvements / alternatives
Governance Layer    — authorize    — "What is allowed?"                 → expose/suppress/defer/block/authorize
Communication Layer — express      — "How is it explained?"             → rendering, disclosure (incl. MRI diagnostic, panels)
Execution Coord.    — act (gated)  — "What authorized coordination?"    → posture-gated mutation, recompute triggers
```

**Cognitive responsibilities & ownership boundaries:**
- **Advisory Cognition owns generation** of candidate responses (Recommendation, Clarification, Suggested-Action engines). It **generates**; it does **not** authorize, render, or assess importance.
- **Governed on both sides:** Governance **constrains the advisory input space** (posture/tier bound which candidates may even be generated — matching documented Stage 12 "constrained by Posture/Tier/Governance") **and governs the advisory output** (expose/suppress/defer/block). *Cognition generates; Governance governs — on input and output.*
- **Scope discipline (what Advisory does NOT own):** **Reliability** stays in **Judgment** (a descriptive supportability assessment, not a candidate response); **MRI** stays in **Communication** (diagnostic rendering); **Resolution Paths** are **presentation-only** (multiple Recommendations rendered as paths — no Resolution-Path object; preserves the ratified AMB-1 decision).

**Information flow:**
```text
Context → Knowledge → Reasoning → Judgment → Advisory(⟵ constrained by Governance posture/tier)
        → Governance(disposition/authorization of candidates) → Communication → Execution(gated)
        ↺ recompute on signal/mutation → Reasoning
```

This is the **minimal complete** Outcome Orchestration cognitive architecture: it adds exactly the one missing stage, preserves every documented role and OSLO's separation doctrine, and makes the generation→authorization boundary explicit and governable.

## Representation (Q8) — how to model Advisory Cognition

| Option | Advantages | Disadvantages |
|---|---|---|
| **A. New runtime layer** | Clearest peer-role expression (parity with Reasoning/Judgment as a cognitive stage); unambiguous boundary | Heavier; adds a top-level layer; less granular than engines |
| **B. Cognitive *domain* containing engines** | Expresses it as a **cognitive role** *and* uses engine granularity (single-responsibility per engine: Recommendation/Clarification/Suggested-Action); unifies with the Cognitive Engine review | Requires formalizing the layer/domain/engine taxonomy |
| **C. Capability inside an existing layer** | Minimal nominal change | **Invalid** — every existing layer is the wrong cognitive operation and disclaims generation; reintroduces the leak |
| **D. Cross-cutting service** | Flexible | Advisory is **sequential** in the decision flow (between evaluate and authorize), not cross-cutting; a cross-cutting model misrepresents its place in the loop |

**Recommended: Option B — a Cognitive Domain ("Advisory Cognition") containing engines.** It is the most architecturally correct: it names the **role** (so the boundary is real and governable) while making **engines the single-responsibility unit** (Recommendation, Clarification, Suggested-Action). Option **A** is acceptable if the owner prefers strict layer-parity; **C** is invalid; **D** misplaces it. *(B and A are representations of the same underlying truth: Advisory is a distinct cognitive stage.)*

## Final Verdict

**ADVISORY COGNITION SHOULD BE ADOPTED — WITH MODIFICATIONS.**

**The role is architecturally necessary** (not optional): a complete Outcome Orchestration architecture **cannot omit** an option-generation stage between evaluation and authorization; OSLO's documented chain omits it; the recurring ownership conflicts are the symptom; and it becomes the keystone as OSLO evolves toward governed action. On **architectural correctness** the answer is unequivocal: **adopt the role.**

**The "modifications"** concern *form and scope*, not *whether*:
- **M-1 (representation):** model it as a **Cognitive Domain containing engines** (Option B) — or a named layer (Option A) at owner preference — **not** a capability inside an existing layer (invalid).
- **M-2 (governed both sides):** Governance **constrains** the advisory input space (posture/tier) **and governs** advisory output exposure; Advisory **generates only** — it holds no authority. *Cognition generates; Governance governs.*
- **M-3 (scope):** Advisory owns Recommendations / Clarifications / candidate actions; it does **not** own **Reliability** (Judgment) or **MRI** (Communication); **Resolution Paths remain presentation-only** (AMB-1).
- **M-4 (placement):** position between Judgment and Governance in cognitive order, honoring the documented governed sequence; **recompute loop** includes Advisory.
- **M-5 (governance of adoption):** formal adoption is **owner-ratified** and should be **sequenced after the GOV-ARCH-001/001A/000** architecture-representation review (so the new role is registered against the settled representation).

**Why "with modifications" and not unqualified "adopt":** the *necessity of the role* is unqualified; but the **candidate model as drawn** needs the scoping (exclude Reliability/MRI; Resolution-Paths presentation-only), the **bidirectional governed relationship** (input constraint + output disposition), and a **representation choice** (domain-with-engines preferred). **Why not "should not be adopted":** that would leave a complete decision architecture missing its generation stage — architecturally incoherent for a system whose purpose is to recommend and orchestrate. **Why not "further analysis required":** the first-principles case is conclusive; what remains is owner ratification and the form/scope refinements above, not further analysis of necessity.

**Bottom line (architectural correctness):** OSLO did not encounter a series of ownership bugs — it **rediscovered a universal cognitive stage it had left unnamed.** Adopting Advisory Cognition completes OSLO's decision architecture, strengthens its separation of concerns, and is the prerequisite for everything OSLO intends to become.

---

*This first-principles systems-architecture review evaluates whether Advisory Cognition is a necessary cognitive role for OSLO to achieve its intended Outcome Orchestration purpose, optimizing for architectural correctness rather than repository consistency. Decomposing OSLO's decision-and-control purpose against the canonical stages shared by OODA, BDI agent architectures, decision theory, and control theory, it shows that every complete decision architecture contains an option/candidate-generation stage between evaluation and authorization, and that OSLO's documented chain collapses exactly this stage (Judgment → Governance with no generator), so the recurring recommendation/clarification/guidance ownership conflicts are the symptom of a missing cognitive stage, not isolated defects. It establishes Advisory Cognition as a distinct forward-generative responsibility (vs Reasoning's backward-analytic inference and Judgment's evaluative weighting, and categorically not Governance's authority or Communication's expression), shows it strengthens separation of concerns (the orphaned, leaking responsibility is the violation; naming it is the fix), best explains the recurring conflicts (one hypothesis fits all the data), and becomes the keystone as OSLO evolves toward execution intelligence, outcome orchestration, autonomous coordination, agent governance, and governed automation. It recommends a minimal complete seven-role architecture inserting Advisory Cognition between Judgment and Governance — governed on both input (posture/tier constraint) and output (exposure) — with correct scope (it owns recommendations/clarifications/candidate actions, not Reliability or MRI; Resolution Paths remain presentation-only), and represents it as a Cognitive Domain containing engines (Option B) or a named layer (Option A) at owner preference, not a capability inside an existing layer (invalid). Final verdict: Advisory Cognition should be adopted with modifications — the role is architecturally necessary; the modifications concern representation, the bidirectional governed relationship, scope, placement, and owner-ratified sequencing after the GOV-ARCH architecture review.*

**OSLO Advisory Cognition Ratification Review 002 complete.**
