# Intralign Internal Engineering Standard

---

## **OSLO Communication Framework**

### **Layered Architecture, Communication Classes, and AI-First Development**

**Audience:** Engineering, AI/ML, Product

**Applies to:** All OSLO communication-related development

**Status:** Canonical (Authoritative)

---

## **1. Purpose**

This document defines:

1. The **canonical system layers** of the OSLO Communication Framework
2. The **communication classes** OSLO is allowed to produce
3. The **ownership and boundaries** of each layer
4. The **AI-first development standards** for this scope of work

The goal is to ensure OSLO scales as a **trusted, judgment-driven system** while also supporting **guided, educational interactions** (e.g., onboarding, 60-Second flow) without eroding trust.

This document is **binding** for design, implementation, and review.

---

## **2. Canonical OSLO Communication Architecture**

OSLO communication is **strictly layered and one-directional**.

```
Project Knowledge
          ↓
       Reasoning
          ↓
        Judgment
          ↓
       Governance
          ↓
     Communication
```

No downstream layer may reinterpret, override, or invent upstream outputs.

---

## **3. System Layer Definitions & Ownership**

---

### **3.1**

### **Project Knowledge Layer**

[**Project Knowledge Layer — Detailed Responsibilities**](Intralign%20Internal%20Engineering%20Standard/Project%20Knowledge%20Layer%20%E2%80%94%20Detailed%20Responsibilitie%202d6df8862b51805a9748c0d7e758360c.md)

*(Meaning / Truth Substrate)*

**Purpose**

Define **what exists** in the project and how it is structured.

**Owns**

- Canonical project entities (projects, outcomes, requirements, schedules, etc.)
- Ontology and schemas
- Relationships (graph)
- Constraint definitions (not evaluation)
- Versioned project state

**Produces**

- Structured, queryable project state

**Does NOT**

- Evaluate conditions
- Detect problems
- Traverse for conclusions
- Infer meaning
- Judge importance

**Invariant**

This layer is **passive and inert**. It does not “reason.”

---

### **3.2**

### **Reasoning Layer**

[**Reasoning Layer — Detailed Responsibilities**](Intralign%20Internal%20Engineering%20Standard/Reasoning%20Layer%20%E2%80%94%20Detailed%20Responsibilities%202d6df8862b5180ffafc6c7a7bc04b9c8.md)

*(Analytical Evaluation Engine)*

**Purpose**

Evaluate project knowledge to determine **what conditions hold or fail**.

**Owns**

- Structural validation
- Constraint evaluation
- Dependency traversal
- Gap detection
- Ambiguity detection
- Inference detection (not resolution)
- Evidence assembly

**Produces**

- Findings (violations, gaps, ambiguities)
- Evidence chains
- Dependency paths

**Does NOT**

- Assign severity
- Assess confidence
- Decide importance
- Trigger communication
- Generate language

**Invariant**

This layer establishes **structural truth with evidence, without opinion**.

---

### **3.3**

### **Judgment Layer**

[**Judgment Layer — Detailed Responsibilities**](Intralign%20Internal%20Engineering%20Standard/Judgment%20Layer%20%E2%80%94%20Detailed%20Responsibilities%202d6df8862b518029a4dff76c5d8a34bb.md)

*(Interpretation & Decision)*

**Purpose**

Interpret reasoning outputs and decide **what they mean in context**.

**Owns**

- Issue classification
- Severity scoring
- Confidence assessment
- Impact analysis
- Risk framing
- Communication eligibility (for issue-driven messages)

**Consumes**

- Reasoning findings only (never raw project data)

**Produces**

- Judgment records
- Allowed actions
- Allowed channels
- Explicit boundaries

**Invariant**

Every issue-related OSLO message must trace back to a **judgment record**.

---

### **3.4**

### **Governance Layer**

[**Governance Layer — Detailed Responsibilities**](Intralign%20Internal%20Engineering%20Standard/Governance%20Layer%20%E2%80%94%20Detailed%20Responsibilities%202d6df8862b5180b7a43bf2664ea5ddef.md)

*(Behavior Control & Safety)*

**Purpose**

Ensure OSLO behaves **intentionally, consistently, and safely** across *all* communications.

**Owns**

- Suppression logic
- Frequency caps
- Deduplication
- Threading
- Message lifecycle state
- Flow awareness (e.g., onboarding, 60-Second flow)
- Policy enforcement
- Versioning & feature flags

**Produces**

- Delivery decisions
- State transitions
- Enforcement outcomes

**Invariant**

Silence is a **valid and intentional** outcome.

---

### **3.5**

### **Communication Layer**

[**Communication Layer — Detailed Responsibilities**](Intralign%20Internal%20Engineering%20Standard/Communication%20Layer%20%E2%80%94%20Detailed%20Responsibilities%202d6df8862b5180edbc71d9db12002d84.md)

*(Explanation & Delivery)*

**Purpose**

Translate governed intent into **clear, bounded human communication**.

**Owns**

- RCU (Reusable Communication Unit) schemas
- Message composition rules
- Templates
- OSLO voice constraints
- Channel adapters (chat, panels, inline, etc.)

**Produces**

- Human-readable explanations
- Guidance and education
- Actionable next steps (when allowed)

**Invariant**

Language is an **output**, never a source of truth.

---

## **4. Communication Classes (Canonical)**

OSLO supports **two primary communication classes**, which must never blur.

---

### **4.1**

### **Judgment-Driven Communications (Issues)**

**Triggered by**

- Reasoning → Judgment outputs

**Examples**

- Missing success criteria
- Infeasible timelines
- Alignment conflicts

**Requirements**

- Must have a Judgment Record
- Must disclose confidence and boundaries
- Must follow issue-class RCU structure
- Must respect governance eligibility rules

**Hard Rule**

> If something is presented as “wrong,” it requires judgment.
> 

---

### **4.2**

### **Guided / Educational Communications (Non-Judgment)**

**Triggered by**

- Onboarding state
- 60-Second flow progression
- User-initiated questions
- Known educational moments

**Examples**

- “Here’s why this question matters”
- “You can answer this loosely for now”
- “This step helps establish shared understanding”
- “Next, we’ll connect outcomes to requirements”

**Constraints**

- Must not imply errors, risk, or severity
- Must not recommend corrective action
- Must not use issue language

**Key Property**

> These messages orient, guide, or educate — they do
> 
> 
> **not**
> 

---

## **5. How Non-Judgment Communications Flow**

**Origin Path (Non-Judgment)**

```
Project Knowledge / Flow State
          ↓
       Governance
          ↓
     Communication
```

**Judgment and Reasoning are not invoked unless an evaluation is being made.**

---

## **6. RCU (Reusable Communication Unit) Standard**

All OSLO communications use RCUs, with **class-specific variants**.

### **RCU Message Classes**

- Issue
- Guidance
- Education
- Clarification
- Orientation

Each class has:

- A defined structure
- Allowed language patterns
- Explicit prohibitions

**RCU enforcement is mandatory.**

---

## **7. AI-First Development Model**

### **Core Principle (Non-Negotiable)**

**OSLO is judgment-first, language-second.**

AI accelerates development, but **never defines truth or authority**.

---

## **8. Phase-Based Development Standards**

---

### **Phase 1 —**

### **Prototype (Truth & Flow Discovery)**

**Objective**

- Validate Project Knowledge
- Validate Reasoning correctness
- Validate Judgment logic
- Draft onboarding / 60-Second flow guidance

**AI Usage**

- Draft schemas and ontologies
- Generate reasoning edge cases
- Simulate onboarding conversations

**Disallowed**

- Tone optimization
- UX polish
- Mixed judgment/guidance language

---

### **Phase 2 —**

### **MVP (Trust Construction)**

**Objective**

- Prove OSLO behaves credibly in real usage

**Required**

- Enforced RCU schemas
- Governance rules for all communication classes
- Flow-aware eligibility logic

**Disallowed**

- Messages without clear class labeling
- Unstructured prompts
- Implicit escalation from guidance → issue

---

### **Phase 3 —**

### **Production (Governed Intelligence)**

**Objective**

- Scale safely without trust degradation

**Required**

- Versioned schemas (knowledge, reasoning, judgment, RCUs)
- Audit logs
- Rollback capability
- Feature flags per communication class

**Disallowed**

- Silent behavior changes
- Autonomous reasoning updates
- Unreviewed template changes

---

## **9. Cursor & AI Tooling Policy**

**Approved**

- Drafting schemas
- Refactoring code
- Generating adversarial inputs
- Exploring alternatives for review

**Prohibited**

- Defining issue truth
- Modifying reasoning/judgment without review
- Bypassing RCU enforcement
- Introducing implicit reasoning

All AI-assisted output is reviewed as if written by a junior engineer.

---

## **10. Universal Definition of Done**

A change is **not complete** unless:

- Project Knowledge is canonical
- Reasoning is deterministic and explainable
- Judgment (if applicable) is explicit and logged
- Governance rules apply
- Communication follows RCU
- Trust impact is neutral or positive

---

## **11. Canonical Closing Statement**

**OSLO communicates for two reasons:**

1. To explain *judgments*
2. To *guide and educate* users intentionally

Both are governed.

Neither is allowed to blur into the other.

---