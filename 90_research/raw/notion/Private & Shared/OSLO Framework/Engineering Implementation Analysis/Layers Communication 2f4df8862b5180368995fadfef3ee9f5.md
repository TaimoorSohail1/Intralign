# Layers Communication

Below is a **strict, OSLO-aligned critique**. I’m not optimizing for diagram aesthetics here—I’m optimizing for **implementation correctness, epistemic safety, and governance fidelity**.

---

## **1. Foundational framing issue: this is a control sequence, not a data contract map**

**Misalignment**

- The stated purpose says “explain the layers communication” and “which data transfers when.”
- The diagram, however, mixes **control flow**, **policy branching**, **data flow**, and **user experience rendering** into a single swimlane narrative.

This creates a real engineering risk:

👉 devs will implement **procedural orchestration** instead of **contract-governed layer interaction**.

OSLO is not a workflow engine.

It is a **layered judgment system with contracts**.

**Fix**

- Explicitly label this as a **“Layer Interaction Sequence (Illustrative)”**
- Pair it with (or reference) a **separate canonical artifact**:
    - *Layer-to-Layer Consumption Contracts* (schemas + invariants)
- Add a banner note:
    
    > “This diagram illustrates typical sequencing. All layer interactions MUST comply with their formal consumption contracts.”
    > 

---

## **2. Reasoning layer is still doing too much “decision-shaped” work**

**Misalignment**

- “Identifies Structural Truth” is ambiguous and dangerous language.
- “Findings + EvidenceChains” is correct—but the diagram implies **closure** rather than **hypothesis generation**.

In OSLO:

- Reasoning **never asserts truth**
- It produces **epistemic claims** with provenance and uncertainty

**Fix**

Rename Reasoning outputs to:

- **“Candidate Findings (Epistemic Claims)”**
- **“Evidence Chains (Non-normative)”**

And add a small annotation:

> “Reasoning does not assign severity, permission, or actionability.”
> 

This matters because otherwise Judgment logic will leak backward.

---

## **3. Judgment layer is missing explicit**

## **normative inputs**

**Misalignment**

- Judgment is shown assigning “Severity & Significance,” which is correct.
- But **what norms are applied** is invisible.

OSLO judgment is not free-form:

- It depends on **defined evaluative frames**
    - outcome integrity
    - risk posture
    - tier constraints
    - confidence thresholds

Without this, engineers will hardcode heuristics.

**Fix**

Add an inbound annotation to Judgment:

- **“Normative Frames / Evaluation Criteria (from Canon & Governance context)”**

This preserves:

- separation of epistemic vs normative reasoning
- future policy evolution without rearchitecting judgment logic

---

## **4. Governance is depicted as a binary gate — this is a major risk**

**Misalignment**

The decision branch shows:

- DENY / DEFER
- PERMIT / AUTHORIZE

This subtly collapses Governance into an **access control layer**.

In OSLO, Governance:

- does not just allow/deny
- it **shapes expression, disclosure, timing, and modality**

**Concrete risk**

Teams will implement Governance as:

```
else → block```

Which breaks:
- partial disclosure
- safe explanations
- suppressed-but-visible states
- deferred clarification loops

**Fix**
Replace the binary framing with **Decision Classes**, e.g.:
- SUPPRESS
- DEFER (await evidence / user input)
- EXPOSE (with constraints)
- ESCALATE
- AUTHORIZE ACTION
- REQUIRE DISCLOSURE

Visually: replace “Decision Branch” with **“Disposition Resolver”**.

---

## 5. Communication layer is being treated as a renderer, not a translator

**Misalignment**
- “Display RCUs (Explanation)” implies Communication explains decisions.
- In OSLO, Communication **never explains on its own authority**.

It translates:
- judgment outcomes
- governance constraints
- epistemic labels
into user-facing language.

**Risk**
This framing will cause:
- explanation hallucination
- tone drift
- post-hoc rationalization

**Fix**
Rename Communication outputs to:
- **“Governed Communication Units (GCUs)”**
And add annotation:
> “All explanations must reference upstream judgment + evidence metadata.”

---

## 6. Canon updates are dangerously under-specified

**Misalignment**
- “Execute Motion / Update Canon” appears as a single step.
- It is unclear *what* is written:
  - asserted facts?
  - inferred state?
  - action outcomes?
  - confidence changes?

Given your earlier insistence (correctly) that:
> *the schema of the knowledge layer is the contract*

this is too loose.

**Fix**
Split Canon updates conceptually into:
- **Observed Reality Updates** (from Execution)
- **Inferred State Updates** (from Reasoning)
- **Judgment Records** (decisions + dispositions)
- **Governance Events** (authorizations, suppressions)

Even a footnote here will prevent catastrophic ambiguity.

---

## 7. The recompute loop is correct — but insufficiently constrained

**Alignment (mostly good)**
- “Recompute Trigger (Always-On Loop)” is conceptually right.
- OSLO *is* continuously reactive.

**Risk**
Without constraints, engineers may:
- recompute everything on every signal
- create unstable oscillations
- violate determinism expectations

**Fix**
Annotate the loop with:
- **Trigger classes** (signal, mutation, threshold breach)
- **Scope of recomputation** (local vs global)
- **Idempotency requirement**

Example note:
> “Recompute is scoped and incremental; full recomputation requires explicit trigger class.”

---

## 8. User → system interaction is still under-modeled

**Misalignment**
User input appears only as:
- trigger
- denial fallback

But OSLO critically depends on:
- clarifications
- confirmations
- contested assumptions
- partial acknowledgments

**Fix**
Add explicit user-originating inputs:
- “User Clarification”
- “User Override (where permitted)”
- “User Evidence Submission”

And show they route through **Intake / Canon**, not directly into Reasoning.

---

## Summary: what this diagram *gets right*
- Correct layer ordering
- Correct epistemic → normative → control → translation → action progression
- Correct existence of closed-loop recomputation
- Correct distinction between execution and communication

## Summary: what must be fixed to protect OSLO’s intent
1. Separate **sequence illustration** from **data contracts**
2. Strip decision authority out of Reasoning
3. Make Judgment’s normative basis explicit
4. Expand Governance beyond binary gating
5. Constrain Communication to translation, not explanation
6. Specify Canon mutation classes
7. Constrain recompute semantics
8. Properly model user clarification loops

If you want, next step I’d recommend is:
- a **one-page “Layer Interaction Invariants” doc** that sits *above* both diagrams and prevents misimplementation regardless of how the visuals are interpreted.

That doc will save you months of rework.
```

===

For clarity on specific Layer interactions reference following invariant document.

[**OSLO — Layer Interaction Invariants (v1.0)**](../OSLO%20%E2%80%94%20Layer%20Interaction%20Invariants%20(v1%200)%202f4df8862b518087901cddfa8dcc0d39.md)