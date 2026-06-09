# Judgment Layer — Engineering Start Here (v1.0)

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Layer:** Judgment

**Audience:** Lead Engineer, AI/ML Engineer, Platform Engineer

**Status:** Canonical

**Purpose:** Enable correct, bounded, and auditable decision-making over Reasoning outputs

---

## **1. What the Judgment Layer Is (and Is Not)**

### **1.1 Core Responsibility**

The Judgment Layer is responsible for **deciding what should happen**, given:

- Structured project knowledge (facts + inferences)
- Deterministic Reasoning outputs (findings, gaps, risks, signals)
- System constraints (policy, tier, lifecycle state)

It produces **bounded decisions**, not explanations and not actions.

> Judgment answers:
> 

> “Given what we know and the rules we operate under, what is the correct decision posture right now?”
> 

---

### **1.2 What Judgment Is**

### **Not**

| **Not This** | **Why** |
| --- | --- |
| Not Reasoning | It does not derive facts or detect issues |
| Not Governance | It does not enforce permission or policy |
| Not Execution | It does not perform actions |
| Not Communication | It does not optimize wording or UX |
| Not Optimization | It does not learn or self-improve in v1 |

Judgment is **decisive but restrained**.

---

## **2. Mental Model for Engineers**

Think of the Judgment Layer as:

> A policy-aware decision compiler
> 

> that transforms
> 
> 
> *findings*
> 
> *decisions*
> 

### **Input → Judgment → Output**

```
Knowledge (facts + inferences)
        ↓
Reasoning (signals, gaps, risks)
        ↓
Judgment (decisions + posture)
        ↓
Governance / Communication / Execution
```

Judgment **never mutates knowledge**

Judgment **never invents facts**

---

## **3. Core Judgment Outputs (v1)**

Every Judgment evaluation must produce **exactly one** of the following:

### **3.1 Decision Object**

```
JudgmentDecision {
  decision_type: enum,
  severity: enum,
  confidence: float,
  evidence_refs: EvidenceID[],
  lifecycle_scope: enum,
  expiry_conditions?: Condition[]
}
```

### **3.2 Supported Decision Types (v1)**

| **Decision Type** | **Meaning** |
| --- | --- |
| ACCEPT | Current state is sufficient |
| WARN | Issue exists but does not block |
| BLOCK | Issue prevents progression |
| DEFER | Insufficient information |
| SUPPRESS | Issue exists but is intentionally hidden |

> No action decisions. No instructions. No suggestions.
> 

---

## **4. Judgment Inputs (Strict Contract)**

Judgment **only consumes structured outputs**.

### **4.1 Required Inputs**

- Reasoning Findings (canonical)
- Lifecycle State (e.g. Initiation, Planning, Execution)
- Mode / Pass (e.g. Pass 1 Structural, Pass 2 Inferential)
- Tier Capabilities (Free / Pro / Enterprise)

### **4.2 Forbidden Inputs**

- Raw user text
- LLM free-form output
- UI state
- Historical optimization data (v1)

If it’s not canonical → Judgment must ignore it.

---

## **5. Judgment Invariants (Non-Negotiable)**

These invariants **must be enforced in code**.

### **J-INV-01 — Determinism**

Same inputs → same decision

### **J-INV-02 — No Fabrication**

Judgment cannot create new facts, assumptions, or inferences

### **J-INV-03 — Bounded Outputs**

Only allowed decision types may be emitted

### **J-INV-04 — Evidence Anchoring**

Every non-ACCEPT decision must reference evidence

### **J-INV-05 — Lifecycle Awareness**

Judgment behavior must vary by lifecycle state

### **J-INV-06 — Expiry Awareness**

Judgment may declare when it should be re-evaluated

---

## **6. Lifecycle Sensitivity (Critical)**

Judgment decisions are **contextual**, not absolute.

| **Lifecycle Stage** | **Judgment Bias** |
| --- | --- |
| Initiation | Favor DEFER over BLOCK |
| Planning | Strict on structure and alignment |
| Execution | Strict on feasibility and drift |
| Monitoring | Prefer WARN over BLOCK |
| Closure | Suppress non-impacting issues |

Lifecycle must be passed explicitly — never inferred.

---

## **7. Severity Model**

Severity is **orthogonal** to decision type.

| **Severity** | **Meaning** |
| --- | --- |
| INFO | Informational only |
| LOW | Minor impact |
| MEDIUM | Material but manageable |
| HIGH | Significant risk |
| CRITICAL | Outcome-threatening |

> BLOCK + LOW is allowed
> 

> WARN + CRITICAL is allowed
> 

Do not conflate severity with action.

---

## **8. Judgment vs Governance (Hard Boundary)**

| **Judgment** | **Governance** |
| --- | --- |
| Decides what *should* happen | Decides what *may* happen |
| Evaluates correctness | Enforces policy |
| Stateless | Policy-state aware |
| No permissions | Permission-driven |

Judgment **never checks permissions**.

Governance may override or gate Judgment outputs.

---

## **9. Suppression Is a First-Class Outcome**

Judgment may intentionally suppress a valid issue when:

- It is outside the current lifecycle scope
- It violates tier visibility rules
- It would overload the user prematurely

Suppression must be explicit and auditable.

```
suppression_reason: enum
```

---

## **10. Observability Requirements (v1)**

Every Judgment evaluation must emit:

- Input hash
- Decision object
- Evidence references
- Evaluation timestamp
- Lifecycle + mode context

No metrics optimization in v1.

This is **audit-first**, not learning-first.

---

## **11. What to Implement First (Order Matters)**

1. Decision schema + enums
2. Judgment evaluation function (pure, deterministic)
3. Invariant enforcement
4. Lifecycle branching
5. Evidence binding
6. Observability hooks

**Do not implement UI logic.**

**Do not implement actions.**

---

## **12. Common Engineering Mistakes to Avoid**

- ❌ Letting Judgment “suggest next steps”
- ❌ Re-running Reasoning inside Judgment
- ❌ Inferring lifecycle or tier
- ❌ Returning prose instead of structured decisions
- ❌ Collapsing WARN vs BLOCK semantics

---

## **13. One-Sentence Test of Correctness**

> If Judgment were removed, the system could still
> 
> 
> *understand*
> 

> but it would no longer be able to
> 
> 
> *decide responsibly*
> 

That’s the layer you are building.

---

If you want, next I can:

- Produce a **Judgment Layer Implementation Checklist (1-pager)**
- Generate a **Judgment Test-Case Matrix (BDD-ready)**
- Or write the **Judgment Output Supersession & Retention Rules v1.0**

Just say which one to do first.