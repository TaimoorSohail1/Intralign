# 60-Second Workflow Specification v1.0

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Workflow:** 60-Second Standard

**Status:** Canonical

**Audience:** Product, Engineering, AI/ML, Design

**Constrained By:**

- Project Knowledge Layer Playbook v1.1.1
- Reasoning Layer Playbook v1.1
- Judgment Layer Playbook v1.1
- Governance Layer Playbook v1.1
- Communication Layer Playbook v1.0
- UI-Authorized Mutation Rules (G-03)

---

## **1. Purpose of the 60-Second Workflow**

The 60-Second Workflow exists to answer **one question only**:

> “Do I understand this plan well enough to begin judging it?”
> 

It is **not** designed to:

- finalize plans
- optimize execution
- resolve issues
- collect perfect data

Its purpose is **orientation through simulation**.

---

## **2. Core Principle**

> The 60-Second Workflow prioritizes structural completeness over factual certainty.
> 

It produces:

- a *plausible plan shape*
- explicit assumptions
- early visibility into tradeoffs

It does **not** claim accuracy.

---

## **3. Entry Conditions**

The workflow is triggered when:

- A new project is created
- A user selects “60-Second Plan”
- Onboarding begins
- A user requests a fast assessment

```
WorkflowContext {
  mode: "60Second"
  interruptible: false
  mutation_locked: true
}
```

---

## **4. Canonical End-to-End Flow**

```
User Input
   ↓
Project Knowledge Snapshot
   ↓
Reasoning (Simulation & Structure)
   ↓
Judgment (Conditional Health Scoring)
   ↓
Governance (Strict Restraint)
   ↓
Communication (Orientation Summary)
```

Each layer operates **fully**, but under **special constraints**.

---

## **5. Project Knowledge Behavior (60-Second Mode)**

### **5.1 Inputs**

- Minimal user input:
    - Project name
    - High-level objective (optional)
    - Uploaded artifacts (optional)

### **5.2 Rules**

- No required fields beyond project identity
- No validation blocking
- No forced completion

Project Knowledge provides:

- Canonical snapshot
- Explicitly empty fields preserved as empty

---

## **6. Reasoning Behavior (60-Second Mode)**

Reasoning operates in **simulation-first mode**.

### **6.1 Structural Completion**

Reasoning may introduce:

- Inferred elements
- Synthetic placeholders for:
    - Budget
    - Timeline
    - Resources
    - Dependencies

All introduced values must be:

```
epistemic_state = "Proposed"
value_type = "SyntheticPlaceholder"
certainty_band = "Low"
```

### **6.2 Constraints on Reasoning**

Reasoning must **not**:

- Invent new goals or outcomes
- Optimize or “fix” the plan
- Promote inferred values
- Remove user-provided input

### **6.3 Outputs**

- Structurally complete simulated plan
- Evidence chains
- Raw structural signals
- No recommendations

---

## **7. Judgment Behavior (60-Second Mode)**

Judgment evaluates the **simulated plan**, not reality.

### **7.1 Scoring Rules**

- Compute:
    - Clarity
    - Alignment
    - Feasibility
- All scores are:
    - Conditional
    - Placeholder-aware
    - Confidence-adjusted

### **7.2 Confidence Enforcement**

- Heavy placeholder use → lower confidence
- Missing explicit inputs → clarity penalty
- Optimistic assumptions → feasibility penalty

Scores answer:

> “If these assumptions held, how healthy would this plan be?”
> 

---

## **8. Governance Behavior (60-Second Mode)**

Governance is **maximally restrictive**.

### **8.1 Hard Rules**

Governance must enforce:

- ❌ No interruptions
- ❌ No alerts
- ❌ No corrective messaging
- ❌ No chat-based guidance
- ❌ No mutation prompts

### **8.2 Allowed Surfaces**

- Passive summary
- Inline indicators
- Orientation dashboard

Suppression is the **default success path**.

---

## **9. Communication Behavior (60-Second Mode)**

Communication is **orientational**, not instructional.

### **9.1 Required Explanation Pattern**

Communication must:

1. State what was evaluated
2. Explicitly state assumptions used
3. Present scores with confidence qualifiers
4. Name uncertainty and fragility
5. Avoid calls to action

### **9.2 Forbidden Language**

- “You should…”
- “Fix this…”
- “This will fail…”
- “Recommended next steps…”

The tone is:

> “Here’s the shape of what you’re working with.”
> 

---

## **10. User Experience Contract**

At the end of the 60-Second Workflow, the user must feel:

- Oriented, not judged
- Informed, not overwhelmed
- Curious, not corrected

They should be able to answer:

> “Where are the weak spots?”
> 

Without being told what to do.

---

## **11. Exit Conditions**

The workflow ends when:

- The summary is rendered
- The user takes an explicit action:
    - edits data
    - confirms assumptions
    - exits

At that point:

- Normal Governance rules resume
- Mutation becomes possible (with UI authorization)
- Reasoning recompute may trigger

---

## **12. Failure Modes the Workflow Must Avoid**

- Treating simulation as reality
- Forcing data entry
- Interrupting orientation
- Hiding assumptions
- Presenting scores as verdicts

Any of these breaks trust.

---

## **13. Acceptance Criteria (v1.0)**

The 60-Second Workflow is compliant when:

- A structurally complete plan is produced in ~60 seconds
- Synthetic placeholders are explicit and visible
- Scores are conditional and confidence-adjusted
- Governance suppresses corrective behavior
- No unauthorized mutation occurs
- The user gains immediate judgment capability

---

## **Canonical Close**

> The 60-Second Workflow does not make decisions.
> 

> It creates the conditions for judgment.
> 

> It replaces blank pages with visible structure —
> 

> without pretending that structure is truth.
> 

---

## **System Status**

With this specification published, OSLO now has:

- A canonical fast-orientation workflow
- A defensible simulation-first planning model
- A trust-preserving path from uncertainty to clarity

---

If you want to continue, the most logical next artifacts are:

- **Governance Decision Matrix (implementation guide)**
- **Health Scoring Specification (math & weighting)**
- **60-Second UX Copy & Layout Spec**
- **End-to-End Sequence Diagram for Engineers**

Just say the word.