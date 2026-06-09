# The OSLO Documentation Stack

---

## **(How to Make Layer Implementation Unambiguous)**

The key insight:

> Different docs answer different questions.
> 

> You are currently over-indexing on “what” and “rules,”
> 

> but engineers also need “how,” “why,” and “what not to do.”
> 

You need **five complementary doc types**, each with a distinct purpose.

---

## **1.**

## **Layer Playbooks**

## **(Primary Missing Piece)**

### **Purpose**

Teach engineers **how to think when implementing a layer**.

### **Audience**

Day-to-day implementers (especially AI-assisted coding).

### **Format (per layer, 4–6 pages max)**

Each layer gets its own **Playbook**, not a spec.

### **Required sections**

1. **Mental Model**
    - “This layer exists to do X and *only* X”
    - 3–5 sentences, plain language
2. **Questions This Layer Is Allowed to Answer**
    - Explicit list
3. **Questions This Layer Must Never Answer**
    - Explicit list (this prevents 80% of violations)
4. **Golden Path Example**
    - One concrete, end-to-end example *within the layer*
    - Inputs → outputs → invariants
5. **Common Failure Modes**
    - “If you find yourself doing X, you’re in the wrong layer”
6. **PR Review Heuristics**
    - “Reject if…”
    - “Ask why if…”

### **Example (Governance)**

> If you are deciding
> 
> 
> *what something means*
> 

> If you are deciding
> 
> 
> *whether to say it now*
> 

This is **not** redundant with contracts — it’s cognitive scaffolding.

---

## **2.**

## **Executable Scenarios (Truth Tables for Behavior)**

### **Purpose**

Remove ambiguity by showing **exact behavior under specific conditions**.

### **Audience**

Engineers, QA, AI prompt authors.

### **Format**

Scenario tables, not prose.

### **Example**

| **Condition** | **Judgment** | **Posture** | **Expected Outcome** |
| --- | --- | --- | --- |
| Inference exists | Low severity | Onboarding | Suppressed |
| Inference exists | High impact | Review | Panel only |
| Issue exists | High severity | Critical-only | Chat + Panel |

These scenarios become:

- Unit tests
- Acceptance criteria
- QA scripts

> Specs describe intent.
> 

> Scenarios describe reality.
> 

---

## **3.**

## **Negative Space Docs (“This Must Never Happen”)**

### **Purpose**

Prevent subtle trust-destroying shortcuts.

### **Audience**

Senior engineers, reviewers.

### **Format**

Short, brutal lists.

### **Example: “What Reasoning Must Never Do”**

- Assign severity
- Mention CAF
- Say “risk”
- Decide whether to communicate
- Generate user-visible text

These docs should be **cited in PR reviews**.

---

## **4.**

## **Layer-Boundary Diagrams with Data Flow (Not Boxes)**

### **Purpose**

Prevent “it’s kind of here” thinking.

### **What most diagrams do wrong**

Boxes + arrows → ambiguity.

### **What you need instead**

**Data-object flow diagrams**:

```
ProjectState
   ↓
Finding[]
   ↓
JudgmentRecord[]
   ↓
CommunicationCandidate[]
   ↓
RCU
   ↓
ViewModel
```

Engineers reason better about **objects moving** than boxes interacting.

---

## **5.**

## **Reference Implementations (Minimal, Canonical)**

### **Purpose**

Give engineers a *known-good example*.

### **Characteristics**

- One per layer
- Minimal logic
- Heavily commented
- Not optimized
- Not AI-generated

These act as:

- Style guides
- Guardrails for AI coding tools
- Anchors during refactors

> When in doubt: “Does this behave like the reference?”
> 

---

# **Recommended Production Order (Important)**

Do **not** write everything at once.

### **Phase 1 (Highest ROI)**

1. Governance Playbook
2. Governance State Machine (you already did this)
3. 6–8 Executable Scenarios

### **Phase 2**

1. Reasoning Playbook
2. Judgment Playbook
3. Negative Space Docs

### **Phase 3**

1. Contract Spec v1.0 (schemas + invariants)
2. Reference implementations

This sequence mirrors **how engineers learn**:

Behavior → thinking → rules → code.

---

## **Why This Works (Critically)**

- **AI-first teams** need cognitive constraints, not just APIs
- Nuance is preserved without bloated specs
- PR reviews become objective (“this violates the playbook”)
- New engineers ramp faster
- Drift becomes visible early

Most importantly:

> You are documenting
> 
> 
> **how OSLO thinks**
> 

---

## **My Strong Recommendation (Next Step)**

Produce **one Layer Playbook first** — **Governance** — using the state machine you just approved.

If that lands well with the team, the rest will follow naturally.

If you want, I can:

- Draft the **Governance Layer Playbook v1.0**
- Create a **template Playbook** the team can reuse
- Turn this into a **Notion documentation structure**
- Define **which doc is authoritative when conflicts arise**

Just tell me which you want next.