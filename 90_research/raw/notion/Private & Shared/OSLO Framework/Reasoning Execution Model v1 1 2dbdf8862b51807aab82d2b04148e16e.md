# Reasoning Execution Model v1.1

---

---

**System:** OSLO

**Layer:** Reasoning

**Spec Type:** Normative (Execution Semantics)

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** CANONICAL

**Supersedes:** Reasoning Execution Model v1.0

---

## **1. Purpose**

This document defines **how the Reasoning Layer executes**, end-to-end, with explicit separation between:

- **Lifecycle context** — *why reasoning is invoked*
- **Reasoning mode** — *how much reasoning is allowed*

It governs:

- execution sequencing
- scope control
- determinism guarantees
- evidence capture
- recompute behavior

This model is **implementation-independent** and **binding**.

---

## **2. Core Execution Inputs**

Every reasoning run MUST be initiated with the following inputs:

```
ReasoningExecutionRequest:
  lifecycle_context: <LifecycleContext>
  reasoning_mode: <ReasoningMode>
  knowledge_snapshot_id: <uuid>
  authorized_changeset_id?: <uuid>
  profile_override_ids?: [<profile_id>]
```

---

## **3. Lifecycle Context (WHY)**

### **3.1 Definition**

Lifecycle context explains **why reasoning is occurring now**.

Lifecycle is:

- system-level
- non-optional
- non-computational

### **3.2 Canonical Lifecycle Contexts**

| **Lifecycle Context** | **Description** |
| --- | --- |
| ONBOARDING | Initial system or workspace setup |
| PROJECT_CREATION | First creation of a project |
| PROJECT_UPDATE | Canonical data mutation occurred |
| RECOMPUTE | Authorized recomputation after change |
| WHATIF | Hypothetical, non-canonical scenario |

Lifecycle context:

- **does not affect rule logic**
- **does not change correctness**
- **does not imply reasoning depth**

---

## **4. Reasoning Mode (HOW MUCH)**

### **4.1 Definition**

Reasoning mode constrains **scope, depth, and breadth** of reasoning.

Mode is:

- execution-level
- computational
- explicitly selected

### **4.2 Canonical Reasoning Modes**

| **Mode** | **Description** |
| --- | --- |
| 60SECOND | Bounded, high-signal structural reasoning |
| FULL | Complete reasoning coverage (future-safe) |
| INCREMENTAL | Delta-based reasoning (future-safe) |

Reasoning mode:

- selects eligible profiles
- limits traversal depth
- constrains rule eligibility
- never alters truth definitions

---

## **5. Execution Phases (Canonical)**

Every reasoning run proceeds through the following **fixed phases**.

---

### **Phase 1 — Request Validation**

Validate:

- lifecycle_context is present
- reasoning_mode is present
- knowledge_snapshot_id exists
- WHATIF snapshots are isolated

Failure here aborts execution.

---

### **Phase 2 — Profile Resolution**

1. Identify all profiles compatible with the selected **reasoning mode**
2. Apply any explicit profile overrides
3. Resolve final executable profile set

Rules:

- Profiles MUST declare supported modes
- Lifecycle context MUST NOT affect profile selection

---

### **Phase 3 — Rule Eligibility Filtering**

From resolved profiles:

- load rule definitions
- filter rules based on:
    - reasoning mode
    - declared dependencies
    - structural prerequisites

Skipped rules MUST be recorded as limitations.

---

### **Phase 4 — Structural Evaluation**

Execute eligible rules against the Knowledge snapshot:

- read-only
- deterministic
- order-independent

Outputs may include:

- issues
- inferred elements (proposed only)
- structural signals

No scoring. No judgment.

---

### **Phase 5 — Evidence Chain Assembly**

For every output, assemble an Evidence Chain capturing:

```
EvidenceChain:
  lifecycle_context
  reasoning_mode
  profiles_used[]
  rules_executed[]
  rules_skipped[]
  limitations[]
  knowledge_snapshot_id
```

---

### **Phase 6 — Output Emission**

Emit a **Reasoning Output Set**:

- scoped to the execution
- tagged with lifecycle + mode
- immutable and replayable

Outputs are handed downstream to **Judgment**.

---

## **6. Recompute Semantics (Explicit)**

When lifecycle_context = RECOMPUTE:

- reasoning must:
    - identify impacted subgraphs
    - restrict evaluation to affected areas
    - supersede prior reasoning outputs

Recompute **does not** imply a different reasoning mode.

---

## **7. WHATIF Execution Rules**

When lifecycle_context = WHATIF:

- execution uses a **non-canonical snapshot**
- outputs MUST be tagged hypothetical
- outputs MUST NOT:
    - update canonical reasoning history
    - influence future recompute runs

---

## **8. Determinism Guarantees**

For any execution:

Same snapshot

- same lifecycle context
- same reasoning mode
- same profiles
- same rule versions

→ **identical outputs**

Lifecycle context does not weaken determinism.

---

## **9. Prohibited Execution Behaviors**

The execution engine must never:

- infer lifecycle from mode
- infer mode from lifecycle
- change rule logic based on lifecycle
- suppress outputs for performance reasons
- emit partial results without declared limitations
- mutate canonical data

---

## **10. Canonical Execution Truth**

> Lifecycle answers
> 
> 
> **why now**
> 

> Mode answers
> 
> 
> **how much**
> 

> 
> 

> Execution requires both.
> 

> 
> 

> They must remain separate.
> 

---

## **End of Specification — v1.1**

---

### **Optional next steps**

If you want to fully close engineering readiness, the last high-value artifacts would be:

1. **Lifecycle × Mode Compatibility Matrix**
2. **Reasoning Output Persistence & Supersession Rules**
3. **Judgment Consumption Contract (Reasoning → Judgment)**

Just tell me which one to publish next.