# OSLO Advisory Cognition Review 001

**Document Type:** Architecture Review (evidence-based reconciliation; advisory — owner ratifies) · **Status:** **Pending Owner Decision** · **Date:** 2026-05-31
**Builds on:** `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001.md` · `OSLO_RUNTIME_RECOMMENDATION_OWNERSHIP_REVIEW_001.md` · `OSLO_COGNITIVE_ENGINE_ARCHITECTURE_REVIEW_001.md`. **Evidence:** `OSLO_ARCHITECTURE_BASELINE_V1.md` (§1 purpose & cognitive framing, §2 layer responsibilities + "strict separation of concerns / single responsibility," §3 Stages 11–12, §5 capability inventory) · `01_governance/` · `CLAUDE.md` · `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` · ratified UX/terminology decisions (AMB-1; MRI umbrella).

> **Constraints.** Repository evidence first; no inference of undocumented responsibilities without labeling them proposed extensions; evaluate OSLO **as a cognition system** against its **intended purpose**, not documentation alone. **Per `CLAUDE.md`, only the owner ratifies/adopts canonical content** — every "Ratify" here is a recommendation to the owner. **Evaluation standard (as instructed): not "does the documentation contain Advisory Cognition?" but "does OSLO *require* it to satisfy its intended cognitive responsibilities?"**

---

## 0. The Decisive Evidence (the gap has a shape)

Two documented facts, read together, are decisive:

1. **OSLO's documented cognitive chain is incomplete relative to its own purpose.** §1 frames the layers as separating *"what is known, what is implied, what is judged, **what is allowed**, and what is explained."* That chain runs **implied (Reasoning) → judged (Judgment) → allowed (Governance) → explained (Communication).** There is **no documented cognitive role for "what should be considered / done in response."** The chain jumps from *how serious is it* (Judgment) straight to *what is allowed* (Governance) — with **nothing that generates the candidate responses Governance is meant to allow or suppress.**

2. **OSLO's stated purpose explicitly requires generating candidate action.** §1: Outcome Orchestration is *"continuously aligning execution to declared outcomes by detecting drift, **recommending action**, and (where authorized) coordinating execution."* §5 names a **Recommendation Engine** and a **Clarification Engine**; §3 Stage 12 asserts **Recommendation Generation.** OSLO is *intended* to recommend — yet **no cognitive role owns the generation of what is recommended.**

**Conclusion of the evidence:** the recurring recommendation/clarification/guidance ownership gaps are **not isolated ownership defects** — they are the **symptom of a missing cognitive role.** Every existing role (Reasoning, Judgment, Governance, Communication) **explicitly disclaims recommendation generation** precisely because **it is none of their jobs** — which is exactly the signature of a responsibility the architecture performs but never named. That unnamed role is **Advisory Cognition: "what should be considered?"**

## 1. Cognitive Responsibility Assessment — Is Advisory Cognition a valid role?

**Yes — it is a valid, distinct cognitive role**, on three evidence-grounded distinctions:
- **Reasoning** is *descriptive / structural* — "what does this imply?" (Findings, gaps). Non-normative.
- **Judgment** is *evaluative / state-descriptive* — "how important is it?" (severity, confidence, CAF). Still describes the *current* state.
- **Advisory Cognition** is *generative / prospective* — "what should be considered in response?" (candidate recommendations, clarifications, next actions). It **generates candidate futures**, a cognitively different operation from detecting a gap or scoring its severity.

Generating a candidate action requires reasoning about **possible interventions and their fit to the judged state** — a forward, generative act, not a backward, analytic one. This is **cognitively distinct** from both Reasoning and Judgment, and **categorically not** Governance (authority) or Communication (presentation). The architecture's own non-responsibilities corroborate: all four documented roles disclaim recommendation generation.

## 2. Architectural Gap Assessment — symptom of a missing role?

**Yes.** The repeated findings across prior reviews — "no documented owner" / "conflicting ownership" for Recommendations, Clarifications, Candidate Improvements, Alternative Recommendations, Suggested Next Actions — are **one gap, not many.** They all share the property of being **generative-advisory** outputs ("candidate X"). A single missing role (Advisory Cognition) explains **all** of them at once; isolated ownership patches (assign to Reasoning? Judgment? Governance?) each fail against a documented non-responsibility. The **simplest explanation that fits all the evidence** is a missing cognitive role — Occam's razor favors the role over a series of exceptions.

This also unifies the prior reviews: "recommendations are governed cognitive outputs; cognition generates, Governance governs" (Recommendation Ownership Review) and "engines are the unit of single-responsibility" (Cognitive Engine Review) were both **partial views of the same thing** — Advisory Cognition is the **cognitive role** whose **engines** (Recommendation, Clarification) are the capabilities, governed by Governance.

### Review Questions 1–5
- **Q1 — Missing responsibility or allocation issue?** **A missing cognitive responsibility.** Allocation cannot resolve it (every candidate owner disclaims it); the gap's *recurrence across distinct capabilities* shows a structural omission, not a placement oversight.
- **Q2 — Are Reasoning / Judgment / Advisory fundamentally different?** **Yes.** Reasoning = imply (descriptive); Judgment = weigh (evaluative); Advisory = propose (generative/prospective). Three different cognitive operations (analyze → assess → generate-response).
- **Q3 — Does generating a recommendation require distinct cognition?** **Yes.** Proposing a candidate response is a **generative** act over possible interventions, distinct from inferring implications (Reasoning) or scoring importance (Judgment). The documented non-responsibilities confirm the architecture already treats it as separate.
- **Q4 — Does Advisory Cognition better explain ownership of Recommendations/Clarifications/Suggested Actions/Guidance/Alternatives than Reasoning/Judgment/Governance?** **Yes** — it explains **all of them with one role**, each being a generative "candidate response," whereas the existing roles each disclaim them.
- **Q5 — Strengthen or weaken separation of concerns?** **Strengthen.** Today, recommendation generation is an **orphan responsibility** — disclaimed by all, smeared across workflow stages — which is itself a *separation-of-concerns violation by omission*. Naming Advisory Cognition gives the responsibility a **single clear home**, restoring clean separation. It is the **most** separation-faithful resolution.

## 3. Release 1 Impact Assessment (Q7) — through the Advisory Cognition lens

| Release 1 concept | Advisory Cognition lens | Resolves? |
|---|---|---|
| **Recommendations** | Generated by Advisory Cognition (Recommendation engine), governed by Governance | **Yes — resolves the core gap** |
| **Clarification Requests** | Generated by Advisory Cognition (Clarification engine) — candidate request to improve understanding | **Yes — resolves** |
| **Reliability** | **Not advisory** — a Judgment signal (descriptive supportability of confidence). Advisory does **not** own it | **No** — remains a Judgment-extension owner decision |
| **MRI** | **Not advisory** — a Communication-layer diagnostic rendering governed Reasoning/Judgment outputs (Decision 001 Q-D) | **No** — unchanged (Communication) |
| **Companion** | Communication presentation surface | **No** — unchanged (Communication) |
| **Finding Panel** | Communication presentation construct over Finding (Reasoning) + Issue assessment (Judgment) + Recommendation (Advisory) — now cleanly spans the roles | **Clarifies** the terminology gap |
| **Recommendation Panel** | Communication presentation over **Advisory Cognition** outputs | **Yes — resolves the producer gap** |

**Honest scope:** Advisory Cognition resolves **Recommendations, Clarifications, and Recommendation-Panel content**, and clarifies the Finding Panel. It does **not** resolve **Reliability** (Judgment) or **MRI** (Communication) — those are separate decisions; attributing them to Advisory Cognition would be over-reach. **Resolution Paths remain presentation-only** (AMB-1) — Advisory Cognition emits *multiple Recommendations*, not a Resolution-Path object.

## 4. Evolution Assessment (Q8) — long-term importance

**Advisory Cognition becomes more central, not less, as OSLO evolves.** Its purpose statement (§1) is *understanding → recommending action → (authorized) coordinating execution.* Every forward capability depends on **generating candidate actions** that Governance then authorizes:
- **Execution Intelligence / Outcome Orchestration** — drift detection (Reasoning/Judgment) is inert without **candidate responses** (Advisory) to govern and coordinate.
- **Autonomous Recommendation Systems / Agent Coordination / Governed Automation** — all require a **well-bounded generative role** whose outputs are governable; without a named Advisory Cognition, generated actions have no clean home and no clean governance boundary, undermining OSLO's central promise (governed AI).

Advisory Cognition is therefore the **pivot between cognition and governed execution** — the role that turns "we understand the situation" into "here is what could be done," which Governance authorizes and Execution coordinates. As OSLO moves from understanding toward action, **this role is the linchpin.**

## 5. Recommended Architecture

Preserve all documented roles; **recognize Advisory Cognition as a first-class cognitive role** positioned between Judgment and Governance in cognitive order:

```text
Context Plane        — intake
Knowledge Layer      — what is known
Reasoning Layer      — what does this imply?        (Findings, gaps)
Judgment Layer       — how important is it?         (Issues, severity, confidence, CAF)
Advisory Cognition   — what should be considered?   (Recommendations, Clarification Requests, candidate next actions)
Governance Layer     — what is allowed?             (expose/suppress/defer/block/authorize — incl. of advisory outputs)
Communication Layer  — how is it explained?         (render — incl. MRI diagnostic, panels)
```

**Ownership model:** Advisory Cognition **generates** candidate responses (its engines: Recommendation, Clarification, Suggested-Action); generation is **constrained by** Governance policy and its outputs are **governed (exposed/suppressed/deferred/blocked) by** Governance — *cognition generates; Governance governs* (the conclusion carried from the prior reviews, now with a named owner). **Flow** honors documented Stage 11→12: Issues disposed by Governance → Advisory generates candidates constrained by Governance → Governance governs candidate exposure → Communication renders.

**Representation (Q6):** Advisory Cognition is a **cognitive role**; its **representation** is the owner's choice between:
- **(A) a named runtime layer** (clearest expression of "it is a cognitive role" — peer to Reasoning/Judgment); or
- **(B) a cognitive-engine grouping** (lighter; consistent with the Cognitive Engine review — the role hosts the Recommendation/Clarification engines).
**Recommended:** recognize the **role** explicitly (this is the substantive decision), and represent it as **Option A or B** per owner preference — *not* Option C (a capability inside an existing layer), which is **blocked** because every existing layer disclaims recommendation generation, and *not* "between layers as free-floating," which breaks single-host clarity.

## 6. Final Verdict

**RATIFY MODIFIED ADVISORY COGNITION** — recognize **Advisory Cognition ("what should be considered?") as OSLO's missing fourth cognitive role**, distinct from Reasoning and Judgment — **as a recommendation requiring owner ratification.**

**Modifications/conditions:**
- **M-1:** Recognize it as a **cognitive role**; owner chooses representation (named **Layer** vs **engine grouping**) — not a capability inside an existing layer (blocked).
- **M-2:** **Cognition generates; Governance governs** — Advisory generates candidates constrained by Governance and exposed by Governance; it does **not** take on authority.
- **M-3:** **Scope correctly** — Advisory owns Recommendations, Clarification Requests, candidate actions; it does **not** own **Reliability** (Judgment) or **MRI** (Communication). **Resolution Paths stay presentation-only** (AMB-1 — multiple Recommendations, no object).
- **M-4:** **Clarification** and **Reliability-binding** are **proposed extensions** (Planned/undocumented) — ratify explicitly, do not infer.
- **M-5:** Honor documented **Stage 11→12** placement (governed sequence); **sequence the change after GOV-ARCH-001/001A/000** (architecture representation under review).
- **M-6:** Confirm **MRI-as-Communication-diagnostic** and **panels-as-presentation-constructs** (well-supported).

**Why Ratify (modified) over Reject:** the evidence is strong and convergent — OSLO's **stated purpose includes recommending action**, its **cognitive chain has no role that generates it**, and **every documented role disclaims it**; the recurring gaps are the **shape of that omission**. Naming the role **strengthens** separation of concerns and **unifies** the prior reviews (recommendations as governed cognitive outputs; engines as capabilities) under one coherent concept. **Why "Modified," not unmodified:** the candidate model must be **scoped** (exclude Reliability/MRI), its **representation** is an owner choice, **Resolution Paths** must remain presentation-only, and adoption is **owner-ratifiable doctrine** sequenced after the architecture-representation review. **Why not Defer:** the analysis is conclusive enough to *recommend* the role; only **ratification** (owner) and the GOV-ARCH-001 sequencing remain.

---

*This review evaluates whether OSLO is missing a fundamental cognitive role — Advisory Cognition ("what should be considered?") — and whether the recurring recommendation/clarification/guidance ownership gaps are symptoms of that omission rather than isolated defects. It finds, on documented evidence, that OSLO's cognitive chain (known → implied → judged → allowed → explained) contains no role that generates candidate responses, while OSLO's stated purpose explicitly includes "recommending action," and every documented role disclaims recommendation generation — the signature of a real but unnamed responsibility. It establishes that generating a recommendation is a distinct, generative/prospective cognitive act (vs Reasoning's descriptive implication and Judgment's evaluative weighting), that a single Advisory Cognition role explains all the recurring gaps at once, and that naming it strengthens (not weakens) separation of concerns by giving an orphaned responsibility a single home. It scopes the role honestly (it owns Recommendations, Clarification Requests, and candidate actions — resolving the Recommendation-Panel producer gap — but not Reliability (Judgment) or MRI (Communication), and not Resolution-Path objects, which remain presentation-only per AMB-1), shows it becomes the pivotal role as OSLO evolves toward execution intelligence, outcome orchestration, and governed automation, and recommends Ratify Modified Advisory Cognition — advisory, owner ratification required — recognizing it as the missing fourth cognitive role with cognition-generates/Governance-governs discipline, owner-chosen representation (layer or engine grouping), correct scoping, presentation-only Resolution Paths, explicit treatment of the Clarification/Reliability extensions, and sequencing after the GOV-ARCH architecture review. It infers no undocumented responsibility, labels every extension, resolves no conflict unilaterally, and proposes no implementation.*

**OSLO Advisory Cognition Review 001 complete.**
