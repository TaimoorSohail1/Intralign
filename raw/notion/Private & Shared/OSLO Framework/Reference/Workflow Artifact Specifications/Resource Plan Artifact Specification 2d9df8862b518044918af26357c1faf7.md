# Resource Plan Artifact Specification

---

**OSLO Knowledge Layer — Resource Plan v1.1**

---

## **1. Purpose of the Resource Plan Artifact**

The Resource Plan defines **whether the project has sufficient capacity and capability** to realize the planned WBS within the declared intent, constraints, and time horizon.

It exists to:

- ground feasibility judgment in reality
- expose overcommitment and skill gaps
- contextualize schedule realism
- support outcome-confidence explanations
- provide Charter-grade resource assumptions

The Resource Plan answers **“with what and with whom”**, not **“when”** or **“how tasks are sequenced.”**

---

## **2. Scope and Ownership**

### **What the Resource Plan owns (strictly)**

- Resource capacity (people, skills, tools)
- Availability assumptions
- Allocation intent (at a planning level)
- Capability coverage vs WBS needs

### **What the Resource Plan does**

### **not**

### **own**

- Task assignments (Work Items)
- Detailed timelines (Schedule)
- Hiring plans or procurement execution
- Performance management

---

## **3. Design Principles**

1. **Capacity before schedule**
    
    Feasibility must be judged on available capacity, not optimistic dates.
    
2. **Skill-aware**
    
    Headcount alone is insufficient; capability matters.
    
3. **Planning-level abstraction**
    
    Resources are planned at a level appropriate for early judgment.
    
4. **Judgment-ready**
    
    Structured anchors exist to support feasibility scoring.
    
5. **Inference-safe**
    
    Missing capacity cannot be silently inferred.
    

---

## **4. Resource Object Model**

Each Resource Entry is a **first-class planning object**, not an HR record.

All Resource Entries include:

- resource_type
- capability
- capacity
- availability_window
- source_state (explicit / derived / inferred)

---

## **5. Resource Plan Fields — Structured (Canonical Anchors)**

### **5.1 Resource Categories —**

### **Required**

Resources are categorized to support judgment.

Common categories:

- Human (roles, skills)
- Vendor / External
- Systems / Tools
- Infrastructure
- Budgetary (if treated as a consumable resource)

At least one category must be present.

---

### **5.2 Human Resources (0..n)**

Each Human Resource entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Role / Capability | **Hard Required** | Skill or role (e.g., Backend Engineer, Data Analyst) |
| Quantity | **Soft Required** | Number of people or FTE equivalent |
| Capacity Allocation | Soft Required | % allocation or hours per period |
| Availability Window | Soft Required | Start–end availability |
| Skill Level | Optional | Junior / Mid / Senior / Expert |
| Criticality | Optional | Critical / Important / Nice-to-have |

**OSLO invariants**

- Missing quantity or allocation caps feasibility confidence
- Role-based planning is acceptable in v1 (named individuals optional)

---

### **5.3 Non-Human Resources (0..n)**

Examples:

- Vendors
- Tools
- Environments
- Budget envelopes

Each entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Resource Name | **Hard Required** | Vendor, tool, or asset |
| Resource Type | Soft Required | Vendor / Tool / Platform / Budget |
| Availability | Soft Required | Confirmed / Tentative / Unknown |
| Constraint Link | Optional | Related constraint or dependency |
| Criticality | Optional | Critical / Supporting |

---

## **6. Resource-to-WBS Coverage —**

## **Judgment-Critical**

**Purpose:** Determine whether planned structure is resourced.

| **Field** | **Description** |
| --- | --- |
| Covered WBS Element(s) | One or more WBS Elements |
| Coverage Mode | Primary / Shared / Contingent |

**OSLO invariants**

- WBS Elements without resource coverage reduce feasibility confidence
- Many-to-many coverage is expected
- OSLO must not infer coverage silently

---

## **7. Resource Availability & Assumptions**

### **7.1 Availability Assumptions (0..n)**

| **Field** | **Description** |
| --- | --- |
| Assumption Statement | Availability belief |
| Confidence Level | High / Medium / Low |
| Review Date | Optional |

Low-confidence availability assumptions amplify feasibility risk.

---

### **7.2 Utilization Constraints (Optional)**

Examples:

- “Team cannot exceed 70% sustained utilization”
- “Shared resource capped at 20%”

These may be linked to Context constraints.

---

## **8. Resource Plan Fields — Narrative (Bounded)**

### **8.1 Resource Strategy Summary (Optional)**

How the project intends to staff and support delivery.

### **8.2 Known Resource Risks (Optional)**

Early warnings (e.g., “Single point of failure skill”).

Narrative fields:

- are not scored
- support explanations only

---

## **9. Canonical Objects Produced**

The Resource Plan produces:

- Resource Entry
- Capability
- Capacity Allocation
- Resource-to-WBS edges
- Availability Assumptions

All objects are:

- versioned
- source-labeled
- traceable

---

## **10. Judgment Coverage**

### **Clarity**

- Explicit roles and quantities
- Clear availability windows
- Declared assumptions

### **Alignment**

- Resource coverage mapped to outcome-supporting WBS elements
- Detection of resources allocated to non-essential structure

### **Feasibility (primary contribution)**

- Capacity vs WBS volume
- Skill coverage gaps
- Over-allocation risk
- Dependency on tentative resources

**If Resource Plan is missing or vague, feasibility confidence is capped.**

---

## **11. Inference Rules (Explicit)**

- OSLO may **propose** inferred resource needs or coverage
- Inferred resources:
    - are labeled
    - do not count as present for judgment
    - trigger feasibility issues until confirmed
- Capacity, availability, and skill coverage are **inference-prohibited for judgment**

---

## **12. Charter Coverage**

The following Charter sections are derivable from the Resource Plan:

- Resource assumptions
- Key roles
- Staffing approach
- Capacity risks

No Charter-specific fields are required.

---

## **13. Invariants (Locked)**

1. Resource Plan precedes schedule judgment
2. Capacity and capability are both required
3. Resource coverage must map to WBS elements
4. Named individuals are optional; roles are sufficient
5. Inferred resources never substitute for explicit capacity
6. Resource gaps primarily affect feasibility judgment

---

## **14. Canonical Summary**

> The Resource Plan determines whether the project can realistically be executed. Without explicit capacity and capability coverage, schedule confidence is artificial and outcome judgment is not credible.
> 

---

If you want to continue the default workflow, the next artifact to align is:

- **Schedule Definition Artifact** (temporal feasibility), or
- **Work / Task Objects** (execution boundary)

Tell me which one to do next.