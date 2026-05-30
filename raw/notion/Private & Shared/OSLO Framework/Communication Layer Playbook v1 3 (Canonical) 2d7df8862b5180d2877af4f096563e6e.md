# Communication Layer Playbook v1.3 (Canonical)

---

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Layer:** Communication

**Status:** Canonical (Intent & Behavioral Constraints)

**Audience:** Product, UX, Content, Engineering

**Consumes (Authoritative Inputs Only):**

- IssueDisposition[] (from Governance Layer)
- Referenced Issue[] (read-only, by ID)
- Referenced Finding[] and EvidenceChain[] (read-only, by ID)

**Upstream Signal Context (Non-Consumptive):**

- Observability signals MAY inform upstream layers but are **never directly consumed** by Communication.

**Constrained By:**

- Governance Contract Spec v1.0
- Governance State Machine v1.1
- Scenario Guardrails v1.0
- UI Surface Contracts
- Observability Scope & Boundaries (informational only)

> This document defines
> 
> 
> **intent, boundaries, and invariants**
> 

> 
> 

> It is
> 
> 
> **canonical but non-normative**
> 

> implementation must follow the Communication Specification, Interaction Templates, and UI Contracts.
> 

---

## **1. Purpose of the Communication Layer**

The Communication Layer exists to answer **one question only**:

> “Given an approved issue disposition, how should this be explained so it is correctly understood?”
> 

Communication is OSLO’s **sense-making layer**.

It does **not** decide:

- What is true (Reasoning)
- What matters (Judgment)
- What may surface (Governance)
- What is remembered (Data Moat)
- What actions occur (Execution)

It translates **authorized outputs** into **human-comprehensible structure**.

---

## **2. Hard Boundary: Communication Is Not Control**

Communication **never**:

- Selects which issues surface
- Escalates or suppresses content
- Adjusts severity, confidence, or disposition
- Alters timing, ordering, or placement
- Introduces interpretation beyond upstream meaning
- Assumes retention, learning, or compounding

Communication receives **permission**, not authority.

---

## **3. Inputs to the Communication Layer**

### **3.1 Primary Input: IssueDisposition[]**

Communication operates **only** on Governance-approved artifacts.

```
CommunicationInput {
  issue_id
  disposition
  allowed_surfaces[]
  timing
  rationale
}
```

**Rules**

- Communication may render **only** Expose dispositions
- Deferred or Suppressed issues are invisible to Communication
- Allowed surfaces are strictly enforced
- Timing constraints are honored, not inferred

---

### **3.2 Referential Inputs (Read-Only)**

To explain an exposed issue, Communication may reference:

- Issue (judgment rationale, severity, confidence)
- Finding (structural claim)
- EvidenceChain (how OSLO knows)

**Rules**

- References are explanatory only
- No recomputation
- No reinterpretation
- No aggregation or learning

---

## **4. Authoritative Responsibilities of Communication**

Communication is responsible for:

1. Translating issues into **clear, faithful explanations**
2. Preserving **structural and judgmental integrity**
3. Selecting the appropriate **message pattern**
4. Adapting **depth and compression** to surface and mode
5. Making **assumptions, uncertainty, and boundaries explicit**
6. Maintaining user trust through **precision, not persuasion**

Communication optimizes for **clarity of understanding**, not influence.

---

## **5. Canonical Communication Units (RCU Model)**

All messages are composed of **Reasoned Communication Units (RCUs)**.

An RCU is a **structured explanatory artifact**, not prose.

```
RCU {
  diagnostic
  why_it_matters
  how_we_know
  boundaries
  implications?
}
```

### **RCU Component Semantics**

- **diagnostic**
    
    What is structurally or judgmentally present
    
- **why_it_matters**
    
    Why Judgment considers this consequential
    
- **how_we_know**
    
    Evidence chain summary (traceable, non-exhaustive)
    
- **boundaries**
    
    Assumptions, uncertainty, scope limits
    
- **implications** (optional)
    
    What this affects — never what to do
    

---

## **6. Surface-Aware Rendering Rules**

Communication adapts **presentation**, never meaning.

| **Surface** | **Constraints** |
| --- | --- |
| Issue Panel | Concise, scannable, expandable |
| Summary View | High-level, non-exhaustive |
| Detail View | Full RCU |
| Export (PDF) | Canonical, audit-friendly |

**Rules**

- Semantic equivalence across surfaces is mandatory
- Truncation must not distort meaning
- No new information may be introduced by surface

---

## **7. Mode-Aware (Not Lifecycle-Aware) Tone Adjustment**

Tone varies by **mode**, not lifecycle stage and not content.

| **Mode** | **Communication Posture** |
| --- | --- |
| Canonical | Neutral, formal |
| 60Second | Compressed, signal-first |
| Hypothetical | Conditional, assumption-forward |
| WhatIf | Comparative, delta-focused |

Lifecycle context (planning vs execution) is **upstream** and must not alter explanation semantics.

---

## **8. Prohibited Behaviors (Layer Violations)**

The Communication Layer must **never**:

- Ask the user questions
- Suggest actions, fixes, or next steps
- Reframe severity, confidence, or importance
- Introduce metaphor implying intent or persuasion
- Override Governance constraints
- Trigger execution or mutation
- Generate new insights or learning

Any violation constitutes a **contract breach**.

---

## **9. Determinism & Auditability**

Communication must be:

- Deterministic given identical inputs
- Replayable for audit
- Traceable to:
    - Issue ID
    - Finding ID
    - EvidenceChain ID
    - Disposition rationale

Language may vary slightly.

**Meaning may not.**

---

## **10. Boundary With Other Layers**

### **Communication Consumes**

- IssueDisposition[] (Governance)
- Referenced Issue / Finding / EvidenceChain (read-only)

### **Communication Produces**

- Explanatory messages
- Structured RCUs

### **Communication Does Not Produce**

- Decisions
- Judgments
- Actions
- Mutations
- Retained learning artifacts

---

## **11. Acceptance Criteria (v1.3)**

Communication is compliant when:

- Every message maps to an IssueDisposition
- Only exposed issues are rendered
- Meaning is faithful to upstream layers
- Assumptions and uncertainty are explicit
- No authority is exercised
- Outputs are auditable and replayable
- No retention or learning assumptions are embedded

---

## **Invariant**

> Communication may explain reality, but may never shape it.
> 

---

## **Canonical Close**

> Communication exists to make structure and judgment understandable —
> 

> not persuasive,
> 

> not directive,
> 

> not controlling.
> 

> 
> 

> It turns authorized signals into shared understanding,
> 

> and then stops.
> 

---

### **Pipeline (sealed, authoritative)**

```
Knowledge → Reasoning → Finding[]
Finding[] → Judgment → Issue[]
Issue[] → Governance → IssueDisposition[]
IssueDisposition[] → Communication → Understanding
```

The Communication Layer is now **fully sealed**, **non-authoritative**, and **architecturally clean**.

---

### **Suggested next artifacts (highest leverage)**

1. **Communication Specification (Normative, engineer-ready)**
2. **RCU Rendering Templates by Surface**
3. **End-to-End Trace Example (single issue across all layers)**
4. **Observability ↔ Communication Boundary Test Cases**

If you want, say which one to generate next and I’ll proceed directly.