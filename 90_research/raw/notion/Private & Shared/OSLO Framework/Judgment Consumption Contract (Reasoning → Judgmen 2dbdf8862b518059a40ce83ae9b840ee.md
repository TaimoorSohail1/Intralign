# Judgment Consumption Contract (Reasoning → Judgment) v1.0

---

---

**System:** OSLO

**From Layer:** Reasoning

**To Layer:** Judgment

**Spec Type:** Normative (Inter-Layer Contract)

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** CANONICAL

---

## **1. Purpose**

This contract defines **exactly how the Judgment Layer consumes Reasoning outputs**.

It establishes:

- allowed inputs
- required validations
- consumption timing
- supersession behavior
- hard boundaries between layers

It prevents leakage of inference, heuristics, or execution logic across layers.

---

## **2. Authority & Scope**

This contract is **binding** for all implementations.

Judgment **must not**:

- reinterpret Reasoning semantics
- mutate Reasoning outputs
- infer missing evidence
- backfill suppressed coverage

Anything not explicitly allowed here is **prohibited**.

---

## **3. Canonical Inputs to Judgment**

Judgment consumes **only** a persisted **Reasoning Output Set (ROS)**.

```
JudgmentInput:
  ros_id
  lifecycle_context
  reasoning_mode
  knowledge_snapshot_id
```

Judgment **must not** consume:

- live Reasoning streams
- partial outputs
- non-persisted results
- WHATIF ROS unless explicitly requested

---

## **4. Required ROS Preconditions**

Before consumption, Judgment **must validate**:

1. ROS is complete and immutable
2. Evidence Chains exist for all outputs
3. lifecycle_context and reasoning_mode are present
4. rule versions and profile IDs are recorded
5. limitations (if any) are explicit

Failure of any check **aborts judgment**.

---

## **5. Allowed Reasoning Outputs**

Judgment may consume **only** the following output classes:

### **5.1 Issues**

- Structural deficiencies
- Gaps, conflicts, fragility
- No severity, score, or recommendation

### **5.2 Inferred Elements (Proposed Only)**

- Explicitly labeled epistemic_state: proposed
- May influence confidence weighting
- Must never be promoted to fact by Judgment

### **5.3 Structural Signals**

- Unscored
- Uninterpreted
- Used as raw inputs for scoring logic

### **5.4 Evidence Chains**

- Mandatory
- Used to explain *why* scores exist
- Not editable or compressible

---

## **6. Prohibited Reasoning Artifacts**

Judgment **must never** consume:

- synthetic placeholders as facts
- suppressed/skipped outputs
- rule internals
- traversal traces
- intermediate inference steps

Only **final, emitted outputs** are eligible.

---

## **7. Consumption Semantics**

### **7.1 Deterministic Consumption**

Given the same ROS:

- Judgment must produce the same scores
- Judgment must produce the same explanations
- No stochastic interpretation allowed

---

### **7.2 Mode-Aware Interpretation**

Judgment **must honor reasoning limitations**.

If ROS contains limitations due to mode:

- scores must reflect reduced confidence
- missing coverage must be explicit
- Judgment must not infer absent checks

Example:

> “Alignment score capped due to 60SECOND mode constraints.”
> 

---

## **8. Supersession Handling**

### **8.1 Canonical Supersession Rule**

When a new ROS supersedes a prior ROS:

- Judgment **may** recompute
- Judgment **must not** merge ROS
- Judgment **must not** reuse prior Evidence Chains

---

### **8.2 WHATIF Handling**

For WHATIF ROS:

- Judgment output must be tagged hypothetical
- Judgment outputs must not supersede canonical scores
- Judgment outputs must not persist as authoritative

---

## **9. Judgment Output Independence**

Judgment outputs:

- are derived artifacts
- may be superseded independently
- must reference the ROS they consumed

```
JudgmentResult:
  judgment_id
  ros_id
  scores
  confidence_adjustments
  explanations
```

Judgment **must not** back-propagate changes to Reasoning.

---

## **10. Cross-Layer Anti-Invariants**

The Judgment Layer must never:

- alter Reasoning outputs
- suppress Reasoning issues
- invent evidence
- reinterpret rule intent
- collapse multiple ROS into one
- infer correctness from recency

---

## **11. Audit & Traceability Requirements**

Judgment must record:

- ros_id
- lifecycle_context
- reasoning_mode
- rule versions (via Evidence Chain references)
- limitation acknowledgments

This enables **end-to-end replay**:

```
Knowledge Snapshot
→ Reasoning Execution
→ Reasoning Output Set
→ Judgment Result
```

---

## **Canonical Lock-In**

> Reasoning reveals structure.
> 

> Judgment assigns meaning.
> 

> 
> 

> Judgment consumes Reasoning outputs
> 

> exactly as they are —
> 

> not as it wishes them to be.
> 

---

## **End of Specification — v1.0**

---

### **Engineering Readiness Status**

With this contract, you now have:

- clean Reasoning/Judgment separation
- deterministic handoff
- auditable lineage
- mode-aware scoring safety

If you want, the **final optional closeout** would be:

- **Judgment Output Supersession & Retention Rules**
    
    (mirrors the Reasoning output model for symmetry)
    

Just say the word.