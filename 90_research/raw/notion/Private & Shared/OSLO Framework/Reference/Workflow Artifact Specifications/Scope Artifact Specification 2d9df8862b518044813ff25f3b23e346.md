# Scope Artifact Specification

---

**OSLO Knowledge Layer — Scope v1.1**

---

## **1. Purpose of the Scope Artifact**

The Scope Artifact defines **what is included and excluded** in order to achieve the declared outcomes — and, just as importantly, **what is intentionally not being pursued**.

Scope exists to:

- bound delivery effort
- prevent outcome dilution
- make tradeoffs explicit
- enable alignment and feasibility judgment without ambiguity
- support Charter-grade scope sections without duplication

Scope is the **bridge between Intent and Requirements**.

---

## **2. Scope and Ownership**

### **What Scope owns (strictly)**

- Inclusions (what the project will deliver)
- Exclusions (what the project will not deliver)
- Scope boundaries and edge conditions
- Justification of why this scope is sufficient for the outcomes

### **What Scope does**

### **not**

### **own**

- Outcomes, goals, objectives (Intent)
- Constraints and assumptions (Context)
- Detailed requirements (Requirements)
- Execution decomposition (WBS)
- Resources or schedule

Scope defines **the shape of effort**, not its detail.

---

## **3. Design Principles**

1. **Outcome-bounded**: Scope must be explainable in terms of outcomes
2. **Explicit exclusions**: Absence of exclusions is itself a risk
3. **Human-familiar**: Reads like a real PM scope section
4. **Judgment-ready**: Structured anchors exist for alignment and feasibility
5. **No duplication**: Scope never restates intent or requirements

---

## **4. Scope Fields — Structured (Canonical Anchors)**

Scope is composed of **entries**, not free prose. Each entry is a first-class object.

All structured entries carry:

- statement
- criticality (where applicable)
- source_state (explicit / inferred / proposed)

---

### **4.1 In-Scope Items (1..n) —**

### **Required**

**Definition:** Capabilities, deliverables, or solution elements the project *will* deliver.

Each In-Scope entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| In-Scope Statement | **Hard Required** | Clear description of what is included |
| Scope Type | Soft Required | Capability, feature, process, integration, deliverable, other |
| Criticality | Optional | Critical / Important / Nice-to-have |
| Outcome Link(s) | Soft Required | Which Outcome(s) this item supports |

**OSLO invariants**

- At least one In-Scope item is required
- In-scope items without outcome linkage reduce **alignment confidence**
- OSLO must not infer inclusion silently

---

### **4.2 Out-of-Scope Items (0..n) —**

### **Strongly Recommended**

**Definition:** Explicit declarations of what the project will *not* deliver.

Each Out-of-Scope entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Out-of-Scope Statement | **Soft Required** | What is explicitly excluded |
| Reason for Exclusion | Optional | Why this is excluded |
| Risk if Misinterpreted | Optional | What happens if assumed in-scope |

**OSLO invariants**

- Absence of Out-of-Scope items increases ambiguity risk
- OSLO may raise **clarity issues** if scope boundaries are vague

---

### **4.3 Scope Boundaries (0..n) —**

### **Edge Conditions**

**Definition:** Conditions where scope applicability changes.

Examples:

- “Only Phase 1 markets”
- “Internal users only”
- “Read-only integration”

Each Boundary entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Boundary Statement | **Hard Required** | The boundary condition |
| Boundary Type | Soft Required | Geographic, user group, system, lifecycle, other |
| Impacted Outcomes | Optional | Outcomes affected if boundary shifts |

---

## **5. Scope Fields — Structured (Judgment-Critical Additions)**

These fields close real judgment gaps and were identified during audit.

---

### **5.1 Scope Justification —**

### **Soft Required**

**Purpose:** Explain *why this scope is sufficient* to achieve the outcomes.

| **Field** | **Description** |
| --- | --- |
| Scope Justification | Narrative explanation tied to outcomes |

**Why this matters**

- Prevents over- or under-scoping
- Improves alignment explanations
- Strengthens Charter defensibility

OSLO may reference this but never score it directly.

---

### **5.2 Scope Completeness Declaration —**

### **Optional but Powerful**

**Purpose:** Human assertion of completeness.

| **Field** | **Description** |
| --- | --- |
| Scope Completeness Confidence | High / Medium / Low |

**OSLO usage**

- Used to contextualize clarity and alignment confidence
- Not a substitute for structural analysis

---

## **6. Scope Fields — Narrative (Bounded)**

Narrative is allowed but bounded.

### **6.1 Scope Summary (Optional)**

Human-readable overview of scope shape.

### **6.2 Known Scope Risks (Optional)**

Early callouts (e.g., “scope likely to expand if X happens”).

Narrative fields:

- never replace structured entries
- never establish scope authority

---

## **7. Canonical Objects Produced**

The Scope artifact produces:

- Scope Item (in-scope)
- Scope Exclusion (out-of-scope)
- Scope Boundary

All objects are:

- versioned
- source-labeled
- eligible for downstream traceability

---

## **8. Relationship to Downstream Artifacts**

### **Alignment flow**

- Scope Items → Requirements
- Scope Items → Deliverables (indirect via requirements)
- Scope Boundaries constrain:
    - Requirements
    - WBS
    - Schedule

Scope **does not** map directly to Work Items.

---

## **9. Judgment Coverage**

### **Clarity**

- Explicit inclusions and exclusions
- Boundary conditions
- Scope completeness confidence

### **Alignment (primary contribution)**

- Scope items linked to outcomes
- Detection of scope not supporting outcomes
- Detection of outcomes with insufficient scope support

### **Feasibility (secondary contribution)**

- Scope breadth and criticality inform effort pressure
- Boundary shifts can trigger feasibility re-evaluation

**If Scope is vague or exclusion-free, OSLO must raise clarity issues.**

---

## **10. Charter Coverage**

The following Charter sections are fully derivable from Scope:

- Project Scope Description
- Inclusions
- Exclusions
- Assumptions about boundaries
- Major scope risks (if captured)

No Charter-specific fields are required.

---

## **11. Inference Rules (Explicit)**

- OSLO may **propose** inferred scope items or exclusions
- Proposed values:
    - are labeled
    - are not authoritative
    - do not count as present for judgment
- Scope authority always requires explicit human confirmation

---

## **12. Invariants (Locked)**

1. Scope defines *what*, not *why* or *how*
2. Scope must include at least one in-scope item
3. Scope items should link to outcomes
4. Explicit exclusions are strongly recommended
5. Scope justification improves alignment trust
6. Inferred scope never substitutes for explicit scope
7. Scope gaps primarily affect clarity and alignment judgment

---

## **13. Canonical Summary**

> The Scope Artifact defines the shape and limits of effort. Without explicit inclusions, exclusions, and boundaries, alignment cannot be trusted and feasibility becomes guesswork.
> 

---

If you want, the next natural steps are to:

- align **Requirements Artifact** to the same rigor, or
- produce a **side-by-side comparison** (Intent vs Context vs Scope) to validate no overlap or leakage

Tell me where you want to go next.