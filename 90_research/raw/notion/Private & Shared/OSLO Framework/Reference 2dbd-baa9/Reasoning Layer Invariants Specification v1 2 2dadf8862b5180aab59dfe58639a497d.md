# Reasoning Layer Invariants Specification v1.2

---

---

**System:** OSLO

**Layer:** Reasoning

**Spec Type:** Normative (Invariants & Anti-Invariants)

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** CANONICAL

---

## **1. Purpose**

This document defines the **non-negotiable invariants** and **explicit anti-invariants** governing the Reasoning Layer.

These rules establish:

- hard architectural boundaries
- execution guarantees
- lifecycle vs mode semantics
- determinism and audit requirements

Invariants are **enforced across all Reasoning implementations**, regardless of trigger, profile, or execution environment.

---

## **2. Authority & Scope**

Reasoning invariants:

- are **authoritative**
- apply to **all reasoning executions**
- override playbooks, profiles, and heuristics
- are enforced independently of product surface or UI

If any implementation violates these invariants, it is **non-compliant**.

---

## **3. Canonical Distinction: Lifecycle vs Mode (NEW — LOCKED)**

### **3.1 Lifecycle Context**

A **lifecycle context** describes **when** reasoning occurs within the system’s operational timeline.

Lifecycle contexts are **system-level** and **non-optional**.

**Canonical lifecycle contexts:**

- ONBOARDING
- POST_ONBOARDING (implicit)
- PROJECT_CREATION
- PROJECT_UPDATE
- RECOMPUTE
- WHATIF

Lifecycle context answers:

> Why is reasoning being invoked now?
> 

---

### **3.2 Reasoning Mode**

A **reasoning mode** describes **how deeply and broadly** reasoning is allowed to operate.

Modes are **execution-level** and **selectable**.

**Canonical reasoning modes:**

- 60SECOND
- FULL (future-safe)
- INCREMENTAL (future-safe)

Reasoning mode answers:

> How much reasoning is allowed in this execution?
> 

---

### **3.3 Hard Separation Rule**

> Lifecycle context and reasoning mode are orthogonal and must never be conflated.
> 
- Lifecycle determines **when**
- Mode determines **depth and scope**

No lifecycle context implies a reasoning mode.

No reasoning mode defines a lifecycle state.

---

## **4. Trigger Mapping Invariant (Clarified)**

The trigger field in the Execution Context:

- represents the **reasoning mode**
- does **not** represent lifecycle state

Example:

- ONBOARDING (lifecycle) **may invoke** 60SECOND (mode)
- 60SECOND **does not imply** onboarding

---

## **5. Core Reasoning Invariants**

### **Invariant R-1: Determinism**

Given:

- identical canonical Knowledge snapshot
- identical reasoning mode
- identical profiles
- identical rule versions

→ outputs **must be identical**

No randomness. No execution-order dependency.

---

### **Invariant R-2: Read-Only Canonical Data**

Reasoning must:

- treat Knowledge as immutable input
- never create, update, or delete canonical entities or relationships

---

### **Invariant R-3: Mode Does Not Change Truth**

Reasoning mode:

- may limit **coverage**
- may limit **depth**
- may limit **rule eligibility**

It must **never**:

- change truth definitions
- suppress known violations
- downgrade correctness

---

### **Invariant R-4: Lifecycle Does Not Change Logic**

Lifecycle context must **never**:

- change rule logic
- alter evaluation semantics
- relax determinism guarantees

Lifecycle only affects **why reasoning is invoked**, not **how it reasons**.

---

### **Invariant R-5: Explicit Limitations**

If reasoning mode constrains evaluation:

- limitations **must be recorded**
- skipped domains **must be explicit**
- Evidence Chains must reflect constraints

Silent omission is prohibited.

---

### **Invariant R-6: Evidence Chain Completeness**

Every reasoning execution must record:

- lifecycle context
- reasoning mode (trigger)
- profiles used
- rule IDs and versions
- declared limitations

---

## **6. Anti-Invariants (Explicitly Prohibited)**

The Reasoning Layer must never:

- infer lifecycle state from reasoning mode
- use lifecycle to justify weaker reasoning
- suppress issues due to speed optimization
- assign severity, score, or health
- recommend actions
- mutate canonical data

---

## **7. Cross-Layer Boundary Invariant**

Reasoning may:

- detect structural issues
- surface signals
- provide explanations

Reasoning may **not**:

- judge correctness (Judgment)
- authorize change (Execution)
- redefine canonical meaning (Knowledge)

---

## **Canonical Lock-In Statement**

> Lifecycle defines
> 
> 
> **when reasoning happens**
> 

> Mode defines
> 
> 
> **how much reasoning is allowed**
> 

> 
> 

> They are intentionally separate,
> 

> and must remain so.
> 

---

## **End of Specification — v1.2**

---

### **Next high-value follow-ups (optional)**

1. Update **Reasoning Execution Model** to use lifecycle + mode explicitly
2. Add a **Lifecycle × Mode Compatibility Matrix**
3. Align **Judgment Layer Invariants** to consume Reasoning limitations formally

If you want, say which one to do next.