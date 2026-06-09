# Lifecycle × Mode Compatibility Matrix v1.0

---

---

**System:** OSLO

**Layer:** Reasoning

**Spec Type:** Normative (Execution Constraints)

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** CANONICAL

---

## **1. Purpose**

This matrix defines the **allowed and prohibited combinations** of:

- **Lifecycle Context** (why reasoning is invoked)
- **Reasoning Mode** (how much reasoning is allowed)

It exists to:

- prevent illegal executions
- enforce architectural separation
- guarantee determinism and auditability
- eliminate ambiguity during implementation

This matrix is **binding**.

Any execution outside this matrix is **invalid**.

---

## **2. Canonical Definitions (Reminder)**

### **Lifecycle Context**

System-level reason for invocation (non-computational).

### **Reasoning Mode**

Execution-level constraint on scope and depth (computational).

---

## **3. Compatibility Matrix**

| **Lifecycle Context** | **60SECOND** | **FULL** | **INCREMENTAL** | **Notes** |
| --- | --- | --- | --- | --- |
| **ONBOARDING** | ✅ Allowed | ❌ Not Allowed | ❌ Not Allowed | ONBOARDING establishes baseline; must delegate to bounded mode |
| **PROJECT_CREATION** | ✅ Allowed | ⚠️ Optional (future) | ❌ Not Allowed | FULL allowed only when explicitly requested |
| **PROJECT_UPDATE** | ⚠️ Optional | ❌ Not Default | ❌ Not Allowed | Updates normally trigger recompute, not full runs |
| **RECOMPUTE** | ⚠️ Allowed | ⚠️ Allowed | ✅ Preferred | INCREMENTAL is the canonical recompute mode |
| **WHATIF** | ✅ Allowed | ✅ Allowed | ⚠️ Allowed | Must remain isolated from canonical history |

Legend:

- ✅ **Allowed**
- ⚠️ **Allowed with constraints**
- ❌ **Prohibited**

---

## **4. Hard Rules (Non-Negotiable)**

### **R-1: ONBOARDING Constraint**

ONBOARDING **must not** invoke FULL or INCREMENTAL modes.

Reason:

ONBOARDING is about **initialization**, not completeness or optimization.

---

### **R-2: RECOMPUTE Preference Rule**

When lifecycle = RECOMPUTE:

- INCREMENTAL is the **preferred mode**
- FULL may be used only when:
    - explicitly authorized
    - full invalidation is required
- 60SECOND may be used for **quick verification only**

---

### **R-3: WHATIF Isolation Rule**

All modes are allowed for WHATIF, **but**:

- outputs must be tagged hypothetical
- outputs must not supersede canonical reasoning
- outputs must not affect future recomputes

---

### **R-4: Mode Does Not Imply Lifecycle**

At no time may the system:

- infer lifecycle from mode
- infer mode from lifecycle

Each must be **explicitly declared**.

---

## **5. Evidence Chain Requirements**

Every Evidence Chain must record:

- lifecycle_context
- reasoning_mode
- compatibility decision (implicit or explicit)
- justification if ⚠️ path used

Example:

```
compatibility_note: >
  FULL mode permitted for PROJECT_CREATION due to explicit user request
```

---

## **6. Invalid Execution Handling**

If an invalid lifecycle × mode combination is requested:

- execution must **fail fast**
- error must be **structural**, not heuristic
- no partial outputs may be emitted

---

## **7. Canonical Lock-In**

> Lifecycle determines
> 
> 
> **why reasoning happens**
> 

> Mode determines
> 
> 
> **how much reasoning is allowed**
> 

> 
> 

> This matrix defines the only legal combinations.
> 

> 
> 

> Anything else is a system error.
> 

---

## **End of Specification — v1.0**

---

### **Recommended next (optional)**

If you want to fully close reasoning engineering readiness, the last missing piece would be:

- **Reasoning Output Supersession & Retention Rules**
    
    (how outputs are stored, superseded, and queried over time)
    

Just say the word.