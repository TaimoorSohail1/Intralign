# Work Breakdown Structure (WBS) Artifact Specification

---

**OSLO Knowledge Layer — WBS v1.1**

---

## **1. Purpose of the WBS Artifact**

The WBS Artifact defines the **structural decomposition of deliverables and requirements into manageable components**.

Its role is to:

- provide a **complete structural map** of planned work
- enable feasibility and completeness judgment
- support downstream task creation and scheduling
- expose missing or over-fragmented work
- prevent hidden scope and effort

The WBS answers **“what must exist”**, not **“who does what when.”**

---

## **2. Scope and Ownership**

### **What WBS owns (strictly)**

- Hierarchical decomposition of work
- Parent–child relationships
- Structural completeness of planned effort
- Mapping to upstream requirements (indirectly to outcomes)

### **What WBS does**

### **not**

### **own**

- Outcomes, goals, objectives (Intent)
- Scope definitions (Scope)
- Requirement definition (Requirements)
- Task execution logic (Work Items)
- Resource assignments
- Schedule sequencing

---

## **3. Design Principles**

1. **Structure before execution**
    
    WBS exists to ensure completeness *before* tasks or schedules exist.
    
2. **Deliverable-oriented**
    
    Decomposition represents outputs, not activities.
    
3. **Judgment-ready**
    
    WBS must enable feasibility and alignment judgment without relying on tasks.
    
4. **Human-familiar**
    
    Reads like a PMBOK-aligned WBS, not a task list.
    
5. **Inference-safe**
    
    Missing structure cannot be silently inferred.
    

---

## **4. WBS Object Model**

Each WBS Element is a **first-class structural object**.

All WBS Elements include:

- name
- description
- level
- parent_id (except root)
- source_state (explicit / derived / inferred)

---

## **5. WBS Fields — Structured (Canonical Anchors)**

### **5.1 WBS Root —**

### **Hard Required**

**Definition:** The top-level representation of total project work.

| **Field** | **Description** |
| --- | --- |
| WBS Root Name | Usually project name or major deliverable |
| Decomposition Basis | Deliverable / Phase / Capability |

**OSLO invariant**

- Exactly one WBS Root per project

---

### **5.2 WBS Elements (1..n) —**

### **Required**

Each WBS Element represents a **decomposed unit of work**.

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| WBS Element Name | **Hard Required** | Clear, noun-based label |
| Description | Soft Required | What this element represents |
| Level | Derived | Depth in hierarchy |
| Parent Element | Derived | Structural parent |
| Leaf Indicator | Derived | Whether further decomposition exists |

**Rules**

- Elements must form a strict tree (no cycles)
- Leaf elements represent the **lowest level of decomposition**, not tasks

---

### **5.3 Requirement Linkage —**

### **Soft Required**

**Purpose:** Structural alignment anchor.

| **Field** | **Description** |
| --- | --- |
| Supported Requirement(s) | One or more Requirements |

**OSLO invariants**

- WBS Elements without requirement linkage reduce **alignment confidence**
- Linkage may be many-to-many

---

## **6. WBS Fields — Structured (Judgment-Critical Additions)**

These fields strengthen feasibility and completeness judgment.

---

### **6.1 Decomposition Completeness Confidence —**

### **Optional**

| **Field** | **Description** |
| --- | --- |
| Completeness Confidence | High / Medium / Low |

**OSLO usage**

- Contextualizes feasibility scoring
- Does not replace structural checks

---

### **6.2 Complexity Indicator —**

### **Optional**

| **Field** | **Description** |
| --- | --- |
| Complexity Level | Low / Medium / High |
| Complexity Rationale | Why this element is complex |

Used to:

- flag high-risk structural nodes
- inform resource and schedule pressure later

---

## **7. WBS Fields — Narrative (Bounded)**

### **7.1 WBS Summary (Optional)**

High-level explanation of decomposition approach.

### **7.2 Known Decomposition Risks (Optional)**

Examples:

- “Vendor dependencies embedded”
- “Integration work spans multiple branches”

Narrative fields:

- are not scored
- support explanations only

---

## **8. Canonical Objects Produced**

The WBS artifact produces:

- WBS Root
- WBS Element
- Parent–Child Relationships
- WBS-to-Requirement edges

All objects are:

- versioned
- source-labeled
- structurally validated

---

## **9. Relationship to Downstream Artifacts**

### **Downstream flow**

- WBS Elements → Work Items / Tasks
- WBS Elements → Resource Plan
- WBS Elements → Schedule Definition

**Rule**

- Tasks and subtasks must map to a WBS Element
- WBS Elements may exist without tasks (early planning)

---

## **10. Judgment Coverage**

### **Clarity**

- Clear structure and naming
- Leaf-node definition
- Absence of structural ambiguity

### **Alignment**

- Coverage of requirements by WBS Elements
- Detection of requirements without structural support
- Detection of WBS Elements with no requirement justification

### **Feasibility (primary contribution)**

- Structural volume vs capacity
- Overly shallow or deep decomposition
- High-complexity nodes

**If WBS is missing or incomplete, feasibility confidence is capped.**

---

## **11. Inference Rules (Explicit)**

- OSLO may **propose** inferred WBS Elements or structure
- Inferred structure:
    - is labeled
    - does not count as present for judgment
    - triggers clarity or feasibility issues
- Structural completeness always requires explicit confirmation

---

## **12. Charter Coverage**

The following Charter sections are derivable from WBS:

- Major deliverables
- High-level work structure
- Planning completeness indicators

No Charter-specific fields are required.

---

## **13. Invariants (Locked)**

1. WBS is a structural decomposition, not a task list
2. Exactly one WBS root exists
3. WBS forms a strict hierarchy (tree)
4. Leaf nodes are decomposed work, not tasks
5. WBS Elements should link to requirements
6. Inferred structure never substitutes for explicit structure
7. WBS gaps primarily affect feasibility judgment

---

## **14. Canonical Summary**

> The WBS Artifact exposes whether the project has been structurally thought through. Without a complete and coherent WBS, feasibility judgment is speculative and execution risk is hidden.
> 

---

If you want to continue in order, the next artifacts to align are:

- **Resource Plan Artifact** (capacity realism)
- **Schedule Definition Artifact** (temporal feasibility)
- or **Work / Task Objects** (execution-layer boundary)

Just tell me which one to do next.