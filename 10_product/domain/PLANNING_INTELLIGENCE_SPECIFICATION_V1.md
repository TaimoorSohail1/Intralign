# Planning Intelligence Specification v1

**Type:** Core Reasoning Specification (conceptual; reasoning-focused)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Derived from (does not redefine):** CAF Assessment Model · CAF Scoring Model · Confidence Model · Reliability Model · Finding Model · Recommendation Model · MRI Model · Overlay Model · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md`

> **Scope guardrails.** Active Release 1 only. **No governance concepts, no future architecture, no agent behavior, no execution intelligence.** This is a **conceptual reasoning** specification — it is **not** a data model, state model, event model, API, UI, governance, or execution-intelligence specification (those exist separately and are authoritative for their domains). Consistent with the founder CAF decisions, this document introduces **no scoring formulas, weights, percentages, or numeric thresholds** — it defines *how OSLO reasons*, not how values are arithmetically computed. It restates existing model meaning where needed and **does not introduce new doctrine.**

---

## 1. Purpose

This document specifies **Planning Intelligence** — the reasoning framework by which Release 1 transforms project inputs (intent, evidence, artifacts, context) into **confidence, findings, recommendations, and expanded understanding**. It is the conceptual account of *how OSLO thinks* during the Fast and Deep analysis passes: what it takes in, what it evaluates, what it produces, and why. It is the bridge between the architecture's outer specs (data/state/event/API/UI) and the analysis engine that will implement it — describing the reasoning those specs assume but do not themselves define.

---

## 2. Role of Planning Intelligence in Release 1

In the Architecture Baseline, Planning Intelligence is the **reasoning layer** that sits above the Context Plane and Knowledge Layer. It consumes synthesized understanding and produces the assessment outputs the user sees. Its role is bounded and specific:

- It **understands** a project's planning state (what is known, assumed, unclear, or in conflict).
- It **assesses** that understanding along the CAF dimensions and summarizes it as Outcome Confidence, reliability-qualified.
- It **surfaces** findings (descriptive observations) and **proposes** recommendations (advisory improvements).
- It **improves** understanding over time as evidence and user action accumulate.

It does **not** decide, govern, accept, or execute. Planning Intelligence is descriptive-and-advisory: *only user action and new evidence change the assessment.* It produces understanding; the user acts on it.

---

## 3. Planning Intelligence Inputs

| Input | Source | Role in reasoning |
|---|---|---|
| **Intent** | user-provided purpose/goal of the project | the frame against which alignment and coverage are judged |
| **Evidence** | raw inputs (text, documents, structured, imported) | the ground truth from which understanding is built; basis for explainability |
| **Artifacts** | synthesized planning artifacts (intent charter, scope, requirements, WBS, etc.) | the structured expression of the plan being assessed |
| **Context items** | extracted/enriched units — claims, assumptions, relationships, entities, metrics, interpretations | the working vocabulary of understanding (fast-horizon and deep-horizon) |
| **Prior understanding** | the assessment state from previous analysis runs | the baseline that recalculation refines (supersession, not replacement) |
| **User actions** | acknowledgements, fixes applied, accepted recommendations | signals that legitimately change understanding on the next pass |

Reasoning is grounded in these inputs only. Planning Intelligence never asserts beyond what evidence and context support — unsupported claims become findings, not silent conclusions.

---

## 4. Planning Intelligence Outputs

| Output | Nature | Notes |
|---|---|---|
| **Understanding** | the internal model of the project's planning state | the substrate; expressed to the user via the others |
| **CAF assessment** | Clarity, Alignment, Feasibility — the three first-class dimensions | each reliability-qualified; the only assessment dimensions |
| **Outcome Confidence** | a summarized, reliability-qualified signal | a summary *of* the CAF assessment, not a separate fourth dimension |
| **Findings** | descriptive observations about understanding | flat 7-type taxonomy (§6); governable objects |
| **Recommendations** | advisory, prescriptive improvements | tied to findings; 3 types (§7) |
| **Expanded understanding** | deepened findings/recommendations + recalculated confidence | the product of the Deep Analysis Pass |

Outputs are **explainable to basis**: every CAF judgment, finding, and recommendation can be traced to the evidence/context that produced it.

---

## 5. Understanding Model

"Understanding" is Planning Intelligence's internal representation of *what is known about the project and how well it hangs together.* Conceptually it is the set of context items (claims, assumptions, relationships) plus their support in evidence and their coherence with intent. Understanding has three salient qualities Planning Intelligence continuously evaluates:

- **How clear it is** — are claims well-formed and unambiguous? (→ Clarity)
- **How aligned it is** — do the parts agree with the intent and with each other? (→ Alignment)
- **How feasible it is** — is the plan it describes achievable given constraints? (→ Feasibility)

Understanding is **never final** — it is the current best account, always subject to refinement by Deep Analysis and by new evidence. The Fast Pass produces an *initial* understanding (orientation); the Deep Pass produces an *expanded* understanding. Understanding is **history-preserving**: prior understanding is superseded, not erased.

---

## 6. Finding Generation Framework

A **Finding** is a descriptive observation about the state of understanding — a governable object, never an action. Planning Intelligence generates findings by examining understanding for the conditions in the **flat 7-type taxonomy** (Finding Model, authoritative):

1. **Missing Information** — a needed input is absent.
2. **Ambiguity** — a claim admits multiple readings (§12).
3. **Assumption** — something is taken as true without evidence (§13).
4. **Inference** — a conclusion drawn beyond direct evidence.
5. **Conflict** — two elements contradict (§14).
6. **Constraint** — a limiting condition bearing on feasibility.
7. **Coverage Gap** — an area of the plan the evidence/artifacts do not address.

Each finding records the dimension(s) it affects (Clarity/Alignment/Feasibility), a severity (critical/moderate/warning), and its basis (linked evidence/context). Findings are **descriptive**: they state *what is observed*, leaving *what to do* to recommendations. The Fast Pass produces initial findings; the Deep Pass expands them (§19).

---

## 7. Recommendation Generation Framework

A **Recommendation** is an advisory, prescriptive improvement that operates **on a finding**. Planning Intelligence proposes recommendations to move understanding toward greater clarity, alignment, or feasibility. Per the Recommendation Model (authoritative), recommendations are of three types:

- **Improvement** — a change that strengthens the plan/understanding.
- **Validation** — a request to confirm/verify an assumption or inference.
- **Suggested Fix** — a concrete, directly-applicable correction.

Each recommendation carries a rationale (the basis) and the dimension it is expected to improve. Recommendations are **advisory** — they are never auto-applied; the user accepts, rejects, or implements them. Implementing one produces new evidence/edits that drive the next analysis pass — closing the active loop. The Deep Pass expands recommendations (§20).

---

## 8. Confidence Generation Framework

**Outcome Confidence** is a **summary** of the CAF assessment, qualified by **reliability** (supportability of the assessment). Planning Intelligence generates confidence by:

1. assessing each CAF dimension (Clarity, Alignment, Feasibility — §9–§11),
2. qualifying each with its **reliability** (how well-supported that judgment is, per the Reliability Model), and
3. summarizing into a single reliability-qualified Outcome Confidence signal (per the Confidence Model).

Confidence is therefore **never a bare number** — it is always accompanied by its reliability qualifier, so the user knows both *how confident* and *how trustworthy that confidence is*. Confidence is **derived, not primary**: it changes only because CAF changed, which changes only because understanding changed, which changes only through evidence or action. Consistent with the founder CAF decisions, **no weighting/threshold/percentage formula is specified here** — this document defines the reasoning relationship (CAF → reliability-qualified summary), and the arithmetic is owner-calibrated elsewhere.

---

## 9. Clarity Evaluation

**Clarity** asks: *is the understanding well-formed and unambiguous?* Planning Intelligence evaluates clarity by examining whether claims are precise, terms are defined, and statements admit a single reading. Low clarity is driven by **Ambiguity** and **Missing Information** findings; clarity improves as ambiguities are resolved and gaps filled. Clarity is reliability-qualified (a clarity judgment on thin evidence is itself low-reliability). Clarity is one of the three first-class dimensions — no sub-dimensions are introduced.

---

## 10. Alignment Evaluation

**Alignment** asks: *do the parts agree with the intent and with each other?* Planning Intelligence evaluates alignment by checking artifacts and claims against the stated intent and against one another for coherence. Misalignment is driven primarily by **Conflict** findings (internal contradiction) and by drift from intent (a claim/artifact pulling away from the project's purpose). Alignment improves as conflicts are resolved and elements are reconciled to intent. Alignment is reliability-qualified.

---

## 11. Feasibility Evaluation

**Feasibility** asks: *is the plan achievable given what is known?* Planning Intelligence evaluates feasibility against **Constraint** findings (limiting conditions — resource, schedule, dependency) and **Coverage Gaps** that hide risk. Feasibility reflects whether the plan, as understood, can plausibly be carried out. It improves as constraints are addressed and gaps closed. Feasibility is reliability-qualified.

*(Clarity, Alignment, Feasibility are the complete, exclusive set of assessment dimensions. No additional dimension is defined.)*

---

## 12. Ambiguity Identification

Planning Intelligence identifies **Ambiguity** where a claim, term, or artifact element admits more than one reasonable interpretation. Reasoning approach: detect under-specified language, multiple plausible referents, or interpretations that would lead to materially different plans. Each ambiguity becomes an **Ambiguity** finding affecting **Clarity**, with a recommendation (often **Validation** or **Improvement**) to disambiguate. Ambiguity is a primary driver of low Clarity in the Fast Pass and a focus of expansion in the Deep Pass.

---

## 13. Assumption Identification

Planning Intelligence identifies **Assumptions** where understanding treats something as true without supporting evidence. Reasoning approach: locate claims that rest on no evidence link, or inferences presented as facts. Each becomes an **Assumption** finding (affecting the dimension it underpins — often Alignment or Feasibility), typically paired with a **Validation** recommendation to confirm or source it. Surfacing assumptions is central to OSLO's honesty: rather than hide unsupported leaps, it makes them visible and governable.

---

## 14. Conflict Identification

Planning Intelligence identifies **Conflict** where two elements of understanding contradict — claims that cannot both hold, an artifact that contradicts the intent, or requirements at odds. Reasoning approach: compare claims/relationships for logical incompatibility and check coherence against intent. Each becomes a **Conflict** finding affecting **Alignment**, with an **Improvement** or **Suggested Fix** recommendation to reconcile. **Contradiction discovery** is a signature activity of the Deep Pass (§17), which has the depth to surface conflicts the Fast Pass cannot.

---

## 15. Relationship Discovery

Planning Intelligence discovers **Relationships** between context items — dependencies, references, implications, and structural links among claims, entities, and artifacts. Reasoning approach: connect related elements so understanding is a coherent web rather than isolated statements. Relationships enrich every other evaluation: they reveal hidden conflicts (incompatible linked claims), expose coverage gaps (a referenced area with no evidence), and clarify feasibility (dependency chains). Relationship discovery is shallow in the Fast Pass (fast-horizon) and a major expansion activity in the Deep Pass (deep-horizon enrichment).

---

## 16. Fast Analysis Pass

The **Fast Analysis Pass** produces the **60-Second Orientation** — an initial, speed-optimized understanding. Reasoning characteristics:

- **Horizon:** fast — fast-horizon context extraction; shallow relationship discovery; surface-level ambiguity/assumption/gap detection.
- **Goal:** give the user a trustworthy *first* read quickly, not an exhaustive one.
- **Outputs:** initial CAF assessment, **initial Outcome Confidence** (reliability-qualified), **initial Findings**, **initial Recommendations**, and the MRI visualization.
- **Explicit limit:** Fast Analysis is **not final understanding** — it is orientation. It communicates lower reliability where depth was traded for speed, and it is always followed by the Deep Pass.

---

## 17. Deep Analysis Pass

The **Deep Analysis Pass** improves understanding through deeper reasoning. It **performs no governance** — it expands and refines, it does not accept or decide. Reasoning activities (the work the Fast Pass defers):

- **Additional claim discovery** — surface claims the fast pass missed.
- **Context enrichment** — deep-horizon extraction; richer context items.
- **Assumption expansion** — find more, deeper assumptions.
- **Relationship expansion** — connect the understanding web more completely.
- **Contradiction discovery** — surface conflicts requiring depth to see.
- **Confidence refinement** — re-assess CAF on the enriched understanding.
- **Finding & recommendation expansion** — produce expanded findings/recommendations.

**Outputs:** **Confidence Recalculation** (§18), **Expanded Findings** (§19), **Expanded Recommendations** (§20). The Deep Pass recurs as evidence and action accumulate (event-driven), each run superseding prior assessment while preserving history.

---

## 18. Confidence Recalculation

When the Deep Pass (or any later run) re-assesses understanding, it produces a **recalculated** Outcome Confidence. Reasoning account: enriched understanding → re-evaluated CAF → re-summarized, reliability-qualified confidence. The new confidence **supersedes** the prior (history preserved as a chain), so the user sees confidence *evolve* — typically with **higher reliability** as depth increases, even if the headline confidence moves up or down as new findings surface. Recalculation is driven only by changed understanding (new evidence/action), never by mere re-running on identical inputs (determinism, §determinism in Testing).

---

## 19. Expanded Findings

**Expanded Findings** are findings first surfaced (or materially deepened) by a Deep Pass — observations the Fast Pass's shallow horizon could not reach: deeper assumptions, discovered contradictions, subtle coverage gaps, relationship-revealed conflicts. They are the same descriptive 7-type objects (§6), distinguished only by having first appeared in a deep run. Expansion is how understanding visibly *grows*: the user sees new, well-founded observations appear as analysis deepens — each explainable to its basis.

---

## 20. Expanded Recommendations

**Expanded Recommendations** are recommendations generated for the new/deepened findings of a Deep Pass. Same three advisory types (§7), tied to their findings. They give the user a richer, prioritized improvement path as understanding matures. Like all recommendations they are advisory; acting on them feeds the next pass. Recommendations superseded by better ones are retained (history), so the improvement trail is auditable.

---

## 21. End-to-End Reasoning Flow

```text
Intent + Evidence + Artifacts
      ↓  (Context Plane → context items; Knowledge Layer → synthesized understanding)
Understanding (initial)
      ↓  FAST ANALYSIS PASS  (fast horizon)
   ├─ CAF assessment (Clarity / Alignment / Feasibility), each reliability-qualified
   ├─ Initial Outcome Confidence (summary, reliability-qualified)
   ├─ Initial Findings (7-type, descriptive)
   └─ Initial Recommendations (3-type, advisory)
      ↓  = 60-SECOND ORIENTATION  ("not final understanding")
      ↓  DEEP ANALYSIS PASS  (deep horizon: claim/assumption/relationship expansion, contradiction discovery)
   ├─ Confidence Recalculation (supersedes prior; reliability ↑)
   ├─ Expanded Findings
   └─ Expanded Recommendations
      ↓  = EXPANDED UNDERSTANDING
      ↓  user acts (acknowledge / accept / implement) → new evidence
      ↺  (recurs — event-driven; history preserved by supersession)
```

The loop is monotonic in *understanding maturity*, not in any single number: each pass deepens what is known and how well it is supported.

---

## 22. Worked Examples

**Example 1 — Ambiguity → Clarity (Fast Pass).**
Evidence states "the system must be fast." Planning Intelligence flags an **Ambiguity** finding (affects **Clarity**: "fast" is undefined — latency? throughput? perceived?) and proposes a **Validation** recommendation ("confirm what 'fast' means and add a measurable target"). Clarity is assessed lower with a reliability qualifier reflecting the thin evidence. *Outcome:* the user sees, within the orientation, exactly what is unclear and what to do.

**Example 2 — Assumption → Alignment (Fast → Deep).**
An artifact assumes a third-party API is available, with no evidence. Fast Pass raises an **Assumption** finding + **Validation** recommendation. Deep Pass, through **relationship discovery**, links this assumption to three downstream requirements and discovers a **Conflict** (one requirement presumes an offline mode the API can't support) — an **Expanded Finding** affecting **Alignment**, with an **Expanded Recommendation** (Improvement: reconcile offline requirement vs API dependency). **Confidence Recalculation** lowers Alignment but at **higher reliability** (now better supported). *Outcome:* understanding deepened; a real contradiction surfaced that the fast read missed.

**Example 3 — Constraint/Coverage Gap → Feasibility (Deep Pass).**
Deep enrichment surfaces a **Constraint** (a fixed launch date) and a **Coverage Gap** (no resourcing artifact addresses staffing for it). Two **Expanded Findings** affect **Feasibility**; a **Suggested Fix** recommendation proposes adding a resource plan. *Outcome:* feasibility risk made explicit with a concrete, applicable fix.

*(Examples are illustrative reasoning traces; they introduce no new types, formulas, or values.)*

---

## 23. Open Questions (not resolved here)

1. **Determinism contract** — is reasoning bit-exact on identical inputs, or bounded-semantic-equivalent? (Shared with Testing/engine.)
2. **Severity assignment reasoning** — the principled basis for critical/moderate/warning is owner-calibrated (no thresholds here).
3. **CAF → Confidence summarization method** — the calibration formula is owner-track (Matrix §22 g1); this spec defines only the relationship.
4. **Reliability qualifier scale** — how reliability is expressed/qualified is owned by the Reliability Model calibration.
5. **Fast/Deep horizon boundary** — what precisely the fast horizon defers to deep is an engine-tuning concern.
6. **Prioritization of expanded findings/recommendations** — ordering logic for large expansions.
7. **Relationship-discovery depth limits** — how far the web is traced in deep enrichment.

---

## 24. Validation

- Release 1 only — ✅
- No governance — ✅ (Deep Pass explicitly performs none; descriptive/advisory only)
- No execution intelligence — ✅ (reasons; never acts/executes)
- No future architecture — ✅
- Fast Analysis defined — ✅ (§16)
- Deep Analysis defined — ✅ (§17)
- Findings defined — ✅ (§6; 7-type taxonomy, descriptive)
- Recommendations defined — ✅ (§7; 3-type, advisory)
- Confidence defined — ✅ (§8; reliability-qualified summary of CAF)
- Clarity defined — ✅ (§9)
- Alignment defined — ✅ (§10)
- Feasibility defined — ✅ (§11)
- No new doctrine / no formulas, weights, thresholds introduced — ✅

**Planning Intelligence Specification complete.**
