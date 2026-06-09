# Action Class Catalog v1.0

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** Action Class Catalog
- **Document Type:** Catalog Specification (Normative)
- **Version:** v1.0
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform, Governance
- **Scope:** System-Wide (Execution + Governance + Posture Enforcement)
- **Authoritative For:**
    - Enumerating all mutation classes OSLO may ever apply
    - Defining scope, bounds, and constraints per mutation class
    - Enabling posture- and governance-based authorization
- **Non-Authoritative For:**
    - Tier entitlements (Tier Capability Contract owns)
    - Execution posture semantics (Execution Posture Contract owns)
    - Truth, severity, confidence (Reasoning/Judgment own)
- **Depends On:**
    - Execution Layer Specification v1.1
    - Governance Layer Specification v1.0
    - Execution Posture Contract v1.0
- **Supersedes:** N/A

---

## **1. Purpose**

This catalog defines the **complete, closed set of mutation classes** that OSLO may apply to canonical system artifacts.

An **Action Class** represents a *bounded, mechanical category of change* that:

- Has predictable effects
- Is auditable and reversible
- Does not require interpretation or judgment
- Can be safely authorized by policy

> If a change is not listed in this catalog, OSLO SHALL NOT perform it.
> 

---

## **2. Core Invariants**

### **Invariant A — Closed World**

> OSLO may only apply mutations belonging to an explicitly defined Action Class.
> 

### **Invariant B — Mechanical Only**

> Action Classes SHALL encode
> 
> 
> *how*
> 
> *why*
> 

### **Invariant C — No Outcome Redefinition**

> No Action Class may redefine outcomes, success criteria, or priorities.
> 

### **Invariant D — Bounded Blast Radius**

> Every Action Class MUST define strict scope and propagation limits.
> 

---

## **3. Action Class Schema**

Every Action Class MUST conform to the following schema.

```
ActionClass {
  action_class_id
  description
  scope {
    object_types[]
    propagation_radius
  }
  preconditions[]
  forbidden_side_effects[]
  allowed_postures[]
  delegatable_by_default (boolean)
  rollback_required (boolean)
  notes
}
```

---

## **4. Action Classes (v1.0 Canonical Set)**

### **4.1 ScheduleConsistencyPropagation**

**Description**

Restore dependency-consistent dates after a user-initiated schedule change.

**Scope**

- Objects: Milestones, ScheduleElements, directly dependent WorkItems
- Propagation Radius: One dependency hop

**Preconditions**

- Dependency graph is acyclic
- No outcome target dates are modified
- Change initiated by user or governance-approved proposal

**Forbidden Side Effects**

- Changing outcome deadlines
- Resource reassignment
- Scope modification

**Allowed Postures**

- Assisted (with confirmation)
- Delegated (if explicitly authorized)

**Delegatable by Default**

- No

**Rollback Required**

- Yes

---

### **4.2 DependencyOrderRepair**

**Description**

Reorder dependent elements to restore logical execution order without changing dates.

**Scope**

- Objects: WorkItems, Tasks
- Propagation Radius: Local chain only

**Preconditions**

- Ordering conflict detected
- No schedule date changes required

**Forbidden Side Effects**

- Date mutation
- Priority changes
- Dependency creation/removal

**Allowed Postures**

- Assisted
- Delegated

**Delegatable by Default**

- Yes (low-risk)

**Rollback Required**

- Yes

---

### **4.3 TraceabilitySync**

**Description**

Propagate linkage metadata (e.g., Requirement ↔ WorkItem ↔ Test) after a user adds or removes a reference.

**Scope**

- Objects: ArtifactElements (Requirements, Tests, Tasks)
- Propagation Radius: Direct references only

**Preconditions**

- Source reference confirmed by user
- No conflicting links detected

**Forbidden Side Effects**

- Creating new requirements or tests
- Changing artifact content

**Allowed Postures**

- Assisted
- Delegated

**Delegatable by Default**

- Yes

**Rollback Required**

- Yes

---

### **4.4 LabelAndMetadataNormalization**

**Description**

Normalize labels, tags, or metadata to conform to canonical vocabularies.

**Scope**

- Objects: ArtifactElements
- Propagation Radius: None (single-object)

**Preconditions**

- Canonical vocabulary exists
- Change does not affect semantics

**Forbidden Side Effects**

- Textual content changes
- Structural linkage changes

**Allowed Postures**

- Assisted
- Delegated

**Delegatable by Default**

- Yes

**Rollback Required**

- Yes

---

### **4.5 ConfidenceDegradationPropagation**

**Description**

Apply confidence degradation flags to dependent elements when upstream assumptions weaken.

**Scope**

- Objects: Findings, Issues, HealthIndicators
- Propagation Radius: One reasoning hop

**Preconditions**

- Upstream confidence reduction validated by Judgment
- No mutation of underlying facts

**Forbidden Side Effects**

- Severity escalation
- Issue creation or closure

**Allowed Postures**

- Assisted
- Delegated

**Delegatable by Default**

- Yes

**Rollback Required**

- Yes

---

### **4.6 ConsistencyRecomputeTrigger**

**Description**

Trigger recomputation of reasoning/judgment outputs after a mutation.

**Scope**

- Objects: Derived views, health scores
- Propagation Radius: System-defined

**Preconditions**

- Upstream mutation applied

**Forbidden Side Effects**

- Canonical data mutation
- Exposure decisions

**Allowed Postures**

- All

**Delegatable by Default**

- Yes

**Rollback Required**

- No (non-mutating)

---

## **5. Explicitly Prohibited Action Classes**

The following categories SHALL NEVER be represented as Action Classes:

- Outcome redefinition
- Outcome retirement or declaration of success
- Priority rebalancing across outcomes
- Scope expansion or reduction
- Resource reallocation
- Strategy substitution
- Silent remediation

These require **governance decisions**, not mechanical execution.

---

## **6. Posture Compatibility Rules**

- Deliberate posture:
    - No Action Class application without explicit confirmation
- Assisted posture:
    - Action Classes may be applied only with user confirmation
- Delegated posture:
    - Only Action Classes marked “delegatable” AND authorized by governance may be applied without confirmation

---

## **7. Governance Integration**

Governance policies may:

- Enable or disable specific Action Classes
- Restrict Action Classes by lifecycle stage
- Require previews or simulations
- Override delegatable defaults

Governance MAY NOT:

- Modify Action Class semantics
- Expand scope or side effects beyond catalog definition

---

## **8. Audit & Replay Requirements**

For every applied Action Class, the system MUST record:

- action_class_id
- posture_id
- governance authorization reference
- affected object IDs
- before/after diff
- rollback reference (if applicable)

---

## **9. Change Control**

- Adding a new Action Class requires:
    - New catalog version
    - Governance approval
    - Explicit posture compatibility declaration
- Modifying an existing Action Class requires:
    - Version bump
    - Backward-compatibility analysis

---

## **Canonical Close**

> Action Classes define the
> 
> 
> **only legal ways**
> 

> 
> 

> They exist to ensure that speed never outruns responsibility.
> 

---

## **End of Catalog**