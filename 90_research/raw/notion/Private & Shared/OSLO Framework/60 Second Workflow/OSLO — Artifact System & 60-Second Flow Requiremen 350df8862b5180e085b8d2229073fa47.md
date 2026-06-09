# OSLO — Artifact System & 60-Second Flow Requirements

---

**Prepared for:** Hasma (Engineering)

**Purpose:** Define the canonical artifact system, schema, visibility rules, and interaction model for OSLO, including the 60-second onboarding experience and ongoing usage.

---

# **1. System Objective**

OSLO must function as:

> **A governed artifact system that continuously evaluates and improves project integrity across Clarity, Alignment, and Feasibility.**
> 

The system must:

- Generate structured artifacts
- Evaluate them continuously
- Surface issues and recommendations
- Drive user interaction through guided resolution

---

# **2. Core Architectural Principles**

---

## **2.1 Single Canonical Artifact Model**

Each artifact must exist as:

```
Artifact = Canonical Data + Visibility Mode
```

- No duplicate “lightweight” vs “full” artifacts
- One source of truth

---

## **2.2 Visibility Modes (Required)**

All artifacts must support:

```
render(mode: "snapshot" | "full")
```

- **Snapshot Mode** → 60-second experience
- **Full Mode** → ongoing usage

---

## **2.3 Non-Negotiable Rule**

> Snapshot mode is NOT a simplified artifact.
> 

> It is a
> 
> 
> **prioritized, governed abstraction**
> 

---

## **2.4 Continuous Judgment**

Judgment must be applied at:

- Intent
- Planning artifacts
- Schedule signals

NOT as a final step.

---

# **3. Artifact Categories**

OSLO supports:

1. Intent Artifact
2. Planning Artifact Set
3. Schedule Artifact

---

# **4. Canonical Artifact Definitions**

---

# **4.1 Intent Artifact**

### **Purpose**

Defines **why the project exists and what success means**

---

### **Required Elements**

- Business Objectives
- Desired Outcomes
- Success Metrics (KPIs)
- Strategic Alignment Drivers
- Stakeholders
- Constraints
- Assumptions (explicit + inferred)
- Priority Logic
- Outcome Risks
- High-Level Dependencies

---

### **Snapshot Mode**

Show:

- 1–3 outcomes
- High-level objectives
- Critical constraints
- High-impact assumptions

Include:

- confidence indicators
- missing element flags
- inferred vs explicit markers

---

### **Full Mode**

Show all elements with:

- full structure
- edit capability
- traceability

---

# **4.2 Planning Artifact Set**

---

## **4.2.1 Global Base Structure (REQUIRED)**

All planning artifact elements must inherit:

```
{
  "id": "string",
  "name": "string",
  "description": "string",
  "epistemic_status": "explicit | inferred | missing",
  "confidence": "0-100",
  "source_refs": [],
  "linked_intent_ids": [],
  "assumptions": [],
  "risks": []
}
```

---

## **4.2.2 Scope Artifact**

### **Required Elements**

- Deliverables (in-scope / out-of-scope)
- Scope boundaries
- Constraints
- Acceptance criteria (linked)

---

### **Schema**

```
{
  "scope_items": [
    {
      "deliverable": "string",
      "in_scope": true,
      "out_of_scope": false,
      "acceptance_criteria": [],
      "linked_requirements": [],
      "constraints": []
    }
  ]
}
```

---

## **4.2.3 Requirements Artifact**

### **Required Elements**

- Requirement statements
- Type (functional / non-functional / constraint)
- Priority
- Acceptance criteria
- Dependencies

---

### **Schema**

```
{
  "requirements": [
    {
      "requirement_id": "string",
      "type": "functional | non-functional | constraint",
      "statement": "string",
      "priority": "high | medium | low",
      "acceptance_criteria": [],
      "linked_scope_items": [],
      "linked_intent_ids": [],
      "dependencies": []
    }
  ]
}
```

---

## **4.2.4 Work Breakdown Structure (WBS)**

```
{
  "wbs_nodes": [
    {
      "wbs_id": "string",
      "name": "string",
      "level": "integer",
      "parent_id": "string | null",
      "child_ids": [],
      "linked_requirements": [],
      "estimated_effort": "number",
      "dependencies": []
    }
  ]
}
```

---

## **4.2.5 Resource Plan**

```
{
  "resources": [
    {
      "resource_id": "string",
      "role": "string",
      "type": "human | system | external",
      "capacity": "number",
      "availability": "string",
      "assigned_wbs_ids": [],
      "constraints": []
    }
  ]
}
```

---

## **4.2.6 Dependency Mapping**

```
{
  "dependencies": [
    {
      "dependency_id": "string",
      "type": "FS | SS | FF | SF",
      "predecessor_id": "string",
      "successor_id": "string",
      "lag": "number"
    }
  ]
}
```

---

## **4.2.7 Risk Register**

```
{
  "risks": [
    {
      "risk_id": "string",
      "description": "string",
      "impact": "high | medium | low",
      "likelihood": "high | medium | low",
      "mitigation": [],
      "linked_artifacts": []
    }
  ]
}
```

---

## **4.2.8 Assumptions Register**

```
{
  "assumptions": [
    {
      "assumption_id": "string",
      "statement": "string",
      "impact": "high | medium | low",
      "validation_required": true,
      "linked_artifacts": []
    }
  ]
}
```

---

## **4.2.9 Acceptance Criteria**

```
{
  "acceptance_criteria": [
    {
      "criteria_id": "string",
      "description": "string",
      "linked_scope_items": [],
      "linked_requirements": []
    }
  ]
}
```

---

## **4.2.10 Snapshot Mode (Planning)**

Show:

- Scope themes
- Requirement clusters
- Top-level WBS
- Resource signals

Hide:

- full structures
- deep hierarchies

---

## **4.2.11 Full Mode**

Expose:

- full schemas
- editing
- traceability

---

# **4.3 Schedule Artifact**

---

### **Required Elements**

- Activities
- Durations
- Dependencies
- Resource assignments
- Milestones
- Timeline
- Critical path

---

### **Snapshot Mode**

Show:

- duration range
- high-level phases
- risk indicators

DO NOT show:

- full schedule
- Gantt
- exact dates

---

### **Full Mode**

Expose:

- full schedule
- dependencies
- timeline

---

# **5. Epistemic + Confidence Layer (Global)**

Every element must include:

- Epistemic status:
    - Explicit
    - Inferred
    - Missing
- Confidence score

---

# **6. Scoring System**

---

### **Dimensions**

- Clarity
- Alignment
- Feasibility

---

### **Requirements**

- numeric
- explainable
- dynamic

---

# **7. Issue System**

---

## **Structure**

Each issue includes:

- Type (gap, misalignment, assumption, risk)
- Impact level
- Affected scores
- Description
- Recommendation

---

## **Constraints**

- Show top 3–5 issues only
- Must include score improvement projection

---

# **8. Interaction Model**

---

## **Issue Panel**

- prioritized issues

---

## **Chat Integration**

Click issue → opens chat with context

---

## **Fix Now Interaction**

- immediate resolution capability

---

# **9. 60-Second Flow Output**

Must include:

### **A. Project Snapshot**

- Intent
- Planning
- Schedule signal

---

### **B. Scores**

- Clarity
- Alignment
- Feasibility

---

### **C. Top Issues**

(3–5 only)

---

### **D. Next Best Action**

(single, required)

---

### **E. Chat Entry**

---

# **10. Progressive Loop**

- user action
- artifact update
- score update
- issue refresh

---

# **11. Prohibited Behaviors**

- full plan generation at 60 seconds
- detailed schedules prematurely
- static reports
- large issue dumps

---

# **12. Success Criteria**

User must:

- understand project state
- take at least 1 action
- perceive system as intelligent

---

# **13. Final Directive**

OSLO must behave as:

> **A real-time, governed co-pilot for improving project integrity**
> 

NOT:

> A project plan generator
> 

---

## **Final note (important)**

This document now does something most systems never achieve:

- **Artifact structure**
- **Evaluation model**
- **UX behavior**
- **Engagement loop**

are all aligned.

That alignment is what will allow OSLO to:

- reason correctly
- guide users effectively
- and scale into a true Outcome Orchestration system

---

If you want the next high-leverage step, I’d strongly recommend:

→ translating this into **Pydantic models + validation + issue rules per field**

That’s where this goes from “well-designed” to **hard to replicate**.