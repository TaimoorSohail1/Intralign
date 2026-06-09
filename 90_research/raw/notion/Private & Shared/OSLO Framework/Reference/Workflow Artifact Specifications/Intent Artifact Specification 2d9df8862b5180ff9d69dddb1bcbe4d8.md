# Intent Artifact Specification

---

**OSLO Knowledge Layer — Intent v1.1**

---

## **1. Purpose of the Intent Artifact**

The Intent Artifact defines **why the project exists** and **what constitutes success**.

It is the **semantic root** of the project plan and the **primary anchor** for:

- outcome judgment
- alignment reasoning
- feasibility context
- executive communication
- Charter derivation

No downstream artifact may redefine intent.

---

## **2. Scope and Ownership**

### **What Intent owns (strictly)**

- Strategic intent
- Desired outcomes
- Success definitions
- Temporal expectations
- Tradeoff posture
- Intent accountability

### **What Intent does**

### **not**

### **own**

- Scope of work
- Requirements
- Deliverables
- Execution details
- Schedules or task plans

---

## **3. Supported Intent Objects (Multiplicity)**

The Intent artifact supports **collections**, not single values:

| **Object** | **Cardinality** |
| --- | --- |
| Goals | 0..n |
| Objectives | 0..n |
| Outcomes | **1..n (minimum 1)** |

There is **no requirement** that:

- Goals exist
- Objectives exist
- Goals → Objectives → Outcomes form a perfect hierarchy

Partial ladders are valid and explicitly supported.

---

## **4. Intent Fields — Structured (Canonical Anchors)**

These fields are **judgment-critical** and feed the OSLO canonical model directly.

### **4.1 Goals (Optional)**

**Purpose:** High-level strategic framing

| **Field** | **Description** |
| --- | --- |
| Goal Statement | Broad strategic intent |
| Notes (optional) | Clarifying context |

**Rules**

- Not scored
- Not required
- Used for executive explanation only

---

### **4.2 Objectives (Optional)**

**Purpose:** Measurable refinement of intent

| **Field** | **Description** |
| --- | --- |
| Objective Statement | Specific, measurable aim |
| Target Indicator (optional) | KPI or indicator |
| Timeframe (optional) | When objective should be met |

**Rules**

- May aggregate multiple outcomes
- Not required for judgment correctness

---

### **4.3 Outcomes (**

### **Required**

### **)**

**Purpose:** Unit of accountability and judgment

Each Outcome must include:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Outcome Statement | **Hard Required** | Outcome-focused result (not activity) |
| Outcome Priority | Soft Required | Primary / Secondary / Equal |
| Outcome Type | Soft Required | Revenue, efficiency, risk, capability |
| Time Horizon | Soft Required | When outcome must exist to retain value |
| Completion Mode | Optional | Binary or Graduated |

**Rules**

- At least one Outcome is required
- Outcomes are judged **independently**
- Project health is an aggregation of outcome health

---

### **4.4 Success Criteria (Per Outcome)**

**Purpose:** Measurability and clarity

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Metric | Soft Required | What is measured |
| Target Value | Soft Required | Threshold for success |
| Measurement Method | Optional | How measurement is obtained |

**Rules**

- Outcomes without success criteria are allowed in v1
- Missing criteria reduce confidence and may trigger clarity issues

---

### **4.5 Intent Ownership**

**Purpose:** Accountability and governance

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Intent Owner | Soft Required | Role or individual accountable for outcomes |

**Rules**

- Used for explanation, escalation, and Charter attribution
- Not used for scoring

---

### **4.6 Tradeoff Posture (Optional)**

**Purpose:** Contextualize judgment under conflict

| **Field** | **Description** |
| --- | --- |
| Primary Tradeoff Preference | Speed / Quality / Cost / Balanced |

**Rules**

- Used when OSLO detects conflicts
- Does not override governance or constraints

---

## **5. Intent Fields — Narrative (Bounded)**

Narrative fields are **human-facing**, bounded, and never the sole source of judgment.

### **5.1 Definition of Success**

**Purpose:** Human interpretation of what “good” looks like

- Describes success beyond metrics
- Used for explanations and Charter narrative
- Never scored directly

---

### **5.2 Out-of-Intent Considerations**

**Purpose:** Explicit non-goals

- What does *not* constitute success
- Prevents misinterpretation and scope creep
- Improves trust in judgment explanations

---

## **6. Canonical Objects Produced**

The Intent artifact produces:

- Goal (optional)
- Objective (optional)
- Outcome (**required**)
- Success Criterion
- Intent metadata (priority, horizon, ownership)

All objects are:

- versioned
- source-labeled (explicit / inferred / proposed)
- traceable downstream

---

## **7. Relationship to Downstream Artifacts**

### **Alignment anchor**

All downstream planning objects must declare **which Outcome(s) they support**, directly or indirectly.

Canonical alignment chain:

```
Outcome
  → Requirement
    → Deliverable
      → WBS Element
        → Work Item
          → Milestone
```

Multiple-to-multiple relationships are allowed and expected.

---

## **8. Judgment Coverage**

The Intent artifact supplies critical signals for:

### **Clarity**

- Explicit outcomes
- Measurable success criteria
- Definition of success
- Outcome boundaries

### **Alignment**

- Outcome priority
- Objective aggregation
- Downstream traceability anchor

### **Feasibility**

- Time horizon
- Tradeoff posture
- Completion mode

**If Intent is weak or incomplete, OSLO caps downstream confidence.**

---

## **9. Charter (Report) Coverage**

The following Charter sections are fully derivable from Intent:

- Business Purpose
- Objectives
- Outcomes
- Success Criteria
- Time Horizon
- Definition of Success
- Strategic Context

No Charter-specific fields are required.

---

## **10. Invariants (Locked)**

1. Every project must have ≥ 1 Outcome
2. Outcomes are judged independently
3. Goals and Objectives are optional
4. Time Horizon is an intent-level concept
5. Intent defines success boundaries and tradeoff posture
6. Intent is the sole authoritative source of outcome meaning
7. Inference may assist but never replace explicit intent

---

## **11. Canonical Summary**

> The Intent Artifact defines success, boundaries, and accountability. Without a complete Intent, no outcome judgment can be trusted—regardless of execution detail.
> 

---

If you want next, I can:

- align **Context Artifact** to this same rigor
- generate a **one-page Intent template** for PMs
- create a **field-to-judgment trace matrix** showing exactly how each Intent field influences scoring

Just tell me what to do next.