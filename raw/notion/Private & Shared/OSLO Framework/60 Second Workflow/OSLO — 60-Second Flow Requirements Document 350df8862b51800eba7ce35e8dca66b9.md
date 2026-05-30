# OSLO — 60-Second Flow Requirements Document

---

**Purpose:**

Define the user experience, system behavior, and interaction model for OSLO’s first-time 60-second flow, ensuring alignment with Outcome Orchestration principles and preventing “false completion” patterns.

---

## **1. Objective**

The 60-second flow must:

- Deliver **immediate, high-value insight** into a user’s project
- Establish **trust through transparency (not completeness)**
- Drive **active user engagement within the first session**
- Demonstrate OSLO’s core capability:
    
    → **Continuous governance of outcome integrity**
    

---

## **2. Core Design Principles**

### **2.1 No False Completion**

- The system must NOT present a “complete project plan”
- All outputs must reflect:
    - uncertainty
    - partial completeness
    - inferred vs. explicit distinctions

---

### **2.2 Judgment is Continuous (Not Terminal)**

- Evaluation must occur at:
    - Intent
    - Planning artifacts
    - Schedule signals
- There is NO “final validation step”

---

### **2.3 Engagement Over Exhaustiveness**

- The goal is NOT full analysis
- The goal is:
    
    → **User takes at least one meaningful action**
    

---

### **2.4 Issue-Driven Interaction Model**

- All recommendations must originate from:
    
    → **Detected issues (gaps, misalignment, weak definitions, assumptions)**
    

---

## **3. High-Level Flow**

```
User Input (project description / uploads)
        ↓
Context Ingestion + Knowledge Extraction
        ↓
Intent Generation + Judgment
        ↓
Planning Artifact Snapshot + Judgment
        ↓
Preliminary Schedule Signal + Judgment
        ↓
Issue Detection + Scoring
        ↓
User Experience Output (≤ 60 seconds)
```

---

## **4. Output Requirements (User-Facing)**

### **4.1 Project Snapshot (Structured, Not Complete)**

### **Intent Summary**

Must include:

- Outcomes
- Objectives
- Constraints (if present)
- Assumptions (explicit + inferred)

Must display:

- Confidence indicator
- Missing elements (e.g., “no measurable success criteria”)
- Inferred vs. user-provided distinctions

---

### **Planning Snapshot (Partial Only)**

May include:

- Early scope themes
- Initial requirements clusters
- High-level work breakdown (if confidence allows)
- Resource assumptions (if available)

Each item must be labeled:

- Complete
- Partial
- Inferred

---

### **Schedule Signal (NOT full schedule)**

Must NOT render full Gantt or detailed timeline unless high confidence.

Instead show:

- Estimated duration range (e.g., 6–10 weeks)
- High-level phases (if derivable)
- Risk indicators:
    - missing dependencies
    - resource gaps
    - sequencing uncertainty

---

## **5. Scoring System (Required)**

OSLO must compute and display:

- **Clarity Score**
- **Alignment Score**
- **Feasibility Score**

---

### **5.1 Score Characteristics**

Each score must be:

- Numerically represented (e.g., 0–100)
- Explainable via contributing issues
- Dynamically updatable as user resolves issues

---

### **5.2 Score Drivers**

- Clarity → definition quality, specificity, completeness
- Alignment → consistency between intent, scope, and outputs
- Feasibility → realism of resources, sequencing, constraints

---

## **6. Issue System (Core Interaction Model)**

### **6.1 Issue Definition**

Each issue must include:

- Title
- Type:
    - Gap
    - Misalignment
    - Assumption
    - Risk
- Impact level:
    - High / Medium / Low
- Affected dimension(s):
    - Clarity / Alignment / Feasibility
- Explanation (human-readable)
- Recommended resolution

---

### **6.2 Issue Prioritization (Critical Requirement)**

At 60-second output:

- Show ONLY top **3–5 highest impact issues**

System must:

- Rank issues based on impact to scores
- Suppress lower-priority issues initially

---

### **6.3 Score Impact Visibility (Required)**

Each issue must display:

- Expected score improvement if resolved
    
    Example:
    
    → “Improves Clarity from 68 → 78”
    

---

## **7. Interaction Model**

### **7.1 Issue Panel**

- Primary structured list of issues
- Supports:
    - filtering (future)
    - prioritization (initially system-controlled)

---

### **7.2 OSLO Chat Integration (Critical)**

The chat console must be **tightly integrated**, not optional.

### **Behavior:**

- Clicking an issue:
    
    → Opens OSLO chat with:
    
    - issue context preloaded
    - suggested action prompt ready
- Chat must support:
    - guided resolution
    - structured inputs
    - follow-up clarification

---

### **7.3 “Fix Now” Interaction**

For each issue:

- User must be able to:
    - take immediate action
    - provide missing data
    - refine definitions

Avoid passive recommendations.

---

## **8. Guided Engagement (Key to Retention)**

### **8.1 Next Best Action (Required)**

At end of flow, system must highlight:

→ **ONE highest-impact action**

Example:

- “Define measurable success metrics for Outcome X”

Criteria:

- highest score impact
- lowest friction to complete
- unlocks downstream improvements

---

### **8.2 Progressive Improvement Loop**

System must support:

1. User resolves issue
2. System updates:
    - artifacts
    - scores
    - issue set
3. New priority issue is surfaced

---

## **9. What Must NOT Be Built**

To protect product intent, explicitly prohibit:

- Full project plan generation at 60 seconds
- Fully detailed artifacts presented as “complete”
- Detailed schedules without validated inputs
- Static reports without interaction pathways
- Large unfiltered issue lists

---

## **10. Success Criteria**

The 60-second flow is successful if:

- User clearly understands:
    - what exists
    - what is missing
    - what matters most
- User takes at least:
    
    → **1 meaningful corrective action**
    
- User perceives OSLO as:
    - intelligent
    - transparent
    - helpful in real-time

---

## **11. Key Risks (Engineering + Product)**

### **Risk 1: Over-generation**

→ Producing full artifacts prematurely

**Mitigation:** enforce partial + confidence labeling

---

### **Risk 2: Issue Overload**

→ Too many issues shown

**Mitigation:** strict top 3–5 prioritization

---

### **Risk 3: Chat Disconnected from Issues**

→ Two parallel systems

**Mitigation:** issue → chat must be seamless

---

### **Risk 4: Static Experience**

→ User reads but does not act

**Mitigation:** enforce “Fix Now” + Next Best Action

---

## **Final Directive**

This flow must behave as:

> **A guided, intelligent co-pilot that helps users improve their project in real time**
> 

Not:

> A system that generates a plan and asks users to review it
> 

---

If you want, I can next convert this into:

- a **system architecture spec (OSLO layer mapping)**
- or a **UI wireframe flow** your team can implement directly

Both would help eliminate ambiguity before build.