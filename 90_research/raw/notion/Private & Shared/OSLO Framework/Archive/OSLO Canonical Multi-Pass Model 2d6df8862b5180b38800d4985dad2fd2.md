# OSLO Canonical Multi-Pass Model

## **(With Provisional Plans & Canon-Aligned Scoring)**

This model separates **truth capture**, **analysis**, **provisional synthesis**, **scoring behavior**, and **human validation** into explicit passes with clear ownership and authority boundaries.

---

## **Pass 0 — Interaction Posture & Flow Context**

**Owner:** Governance

**Purpose:** Determine how OSLO should behave *before* any content is evaluated or rendered.

### **Responsibilities**

- Identify flow mode:
    - Onboarding
    - 60-Second Plan
    - Refinement
    - Review
- Set communication posture:
    - Speed-first
    - Education-first
    - Evaluation-first
- Suppress premature issue framing during onboarding

> This pass controls behavior, not content.
> 

---

## **Pass 1 — Explicit Capture (Truth Preservation Pass)**

**Owner:** Project Knowledge

**Purpose:** Store **only what the user explicitly provides**.

### **What happens**

- Inputs are structured, normalized, and versioned
- Entities, fields, and relationships are stored **verbatim**
- All data marked:
    - source = explicit

### **What is forbidden**

- Filling missing fields
- Inferring relationships
- Applying “helpful defaults”

> Pass 1 answers:
> 

> “What did the user actually say?”
> 

This pass guarantees epistemic honesty.

---

## **Pass 2 — Reasoning & Inference Detection (Findings)**

**Owner:** Reasoning

**Purpose:** Determine **what is missing, assumed, ambiguous, or implied**.

### **What happens**

- Structural validation
- Constraint evaluation
- Dependency traversal
- Gap detection
- Inference detection
- Evidence chain assembly

### **Output**

- Findings:
    - Gaps
    - Ambiguities
    - Inferences
- No mutation of Project Knowledge

> Pass 2 answers:
> 

> “What must be assumed for this plan to hold together?”
> 

This pass is **diagnostic only**.

---

## **Pass 3 — Judgment & Impact Assessment (Issues)**

**Owner:** Judgment

**Purpose:** Interpret reasoning findings and assess **meaning and impact**.

### **What happens**

- Classify findings (issue vs acceptable inference)
- Assess severity (if applicable)
- Assign internal confidence
- Determine outcome impact:
    - Clarity
    - Alignment
    - Feasibility
- Define communication eligibility

### **Key distinction**

- Many inferences are **acceptable but unconfirmed**
- Not all findings become issues

> Pass 3 answers:
> 

> “Which assumptions matter, and to which outcome dimensions?”
> 

---

## **Pass 4 — Provisional Plan Synthesis (Speed Pass)**

**Owner:** Communication (constrained by Judgment & Governance)

**Purpose:** Present a **complete, usable plan immediately**.

### **What happens**

- OSLO materializes inferred elements into a **Rendered Plan**
- Every inferred element is tagged:
    - source = inferred
    - validation_status = unconfirmed
- Canonical Project Knowledge is **not updated**

### **Critical constraint**

> This creates a
> 
> 
> **view-model**
> 

> Pass 4 answers:
> 

> “What would a complete plan look like if these assumptions hold?”
> 

This is where speed is delivered without lying.

---

## **Pass 5 — Health Scoring (Canon-Aligned, Confidence-Weighted)**

**Owner:** Scoring Engine (uses Judgment signals)

**Purpose:** Compute **Outcome Health** using the canonical dimensions.

### **Visible Scores (Only)**

- **Clarity**
- **Alignment**
- **Feasibility**

### **Internal Mechanics (Not Visible)**

Each dimension is computed as:

```
Dimension Score
  = Structural Coverage × Validation Modifier
```

Where:

- **Structural Coverage**
    - Includes explicit + inferred elements
    - Enables fast plan completeness
- **Validation Modifier**
    - Penalizes unconfirmed assumptions
    - Improves only via user validation
    - Never exposed directly

### **Key rule**

> Validation confidence affects score behavior, not score visibility.
> 

> Pass 5 answers:
> 

> “How healthy is this plan across clarity, alignment, and feasibility—given what is confirmed?”
> 

---

## **Pass 6 — Epistemic Labeling & Behavioral Nudges**

**Owner:** Governance + Communication

**Purpose:** Encourage **selective validation** without friction.

### **What happens**

- Inferred elements are subtly labeled:
    - “Assumed”
    - “Draft”
    - “Needs confirmation”
- OSLO highlights **high-impact assumptions first**
- Guidance explains *why validation helps the visible scores*

### **What does NOT happen**

- No confidence percentages
- No warnings or alarms
- No blocking progress

> Pass 6 answers:
> 

> “Which assumptions most affect clarity, alignment, or feasibility?”
> 

---

## **Pass 7 — Guided Validation Loop (Human Authority Pass)**

**Owner:** User (authority) + Communication (guide)

**Purpose:** Convert assumptions into explicit truth.

### **What happens**

- User confirms, edits, or rejects inferred elements
- Upon confirmation:
    - Element becomes source = explicit
    - Project Knowledge is updated
    - Validation modifier improves
    - Relevant health score increases

> Pass 7 answers:
> 

> “Which assumptions do we want to stand behind?”
> 

---

## **Pass 8 — Re-Reasoning & Stabilization**

**Owner:** Reasoning → Judgment

**Purpose:** Re-evaluate the plan as truth hardens.

- Fewer inferences
- Higher confidence judgments
- More stable health scores
- Improved predictability

This pass may loop repeatedly.

---

## **End-to-End Canonical Flow**

```
User Input
   ↓
Pass 0: Governance (posture)
   ↓
Pass 1: Project Knowledge (explicit truth)
   ↓
Pass 2: Reasoning (detect gaps & inferences)
   ↓
Pass 3: Judgment (assess impact by CAF)
   ↓
Pass 4: Provisional Plan Synthesis (rendered view)
   ↓
Pass 5: CAF Health Scoring (confidence-weighted)
   ↓
Pass 6: Epistemic Labeling & Nudges
   ↓
Pass 7: User Validation
   ↓
Project Knowledge updated
   ↓
Pass 8: Re-Reasoning & Stabilization
```

---

## **Why This Model Is Now Complete**

- **Speed**: Users see a full plan immediately
- **Honesty**: Assumptions are never hidden
- **Simplicity**: Only CAF scores are visible
- **Behavioral Pull**: Scores improve only through validation
- **Trust**: No invisible auto-promotion of inferred truth

---