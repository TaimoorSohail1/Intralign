# Reasoning Rule File Specification v1.1

---

**System:** OSLO

**Layer:** Reasoning

**Spec Type:** Normative (schema + constraints)

**Audience:** Engineering, AI/ML, QA

**Status:** CANONICAL

---

## **1. Purpose**

This specification defines the **externalized rule and definition files** used by the Reasoning Layer, including:

- canonical file taxonomy
- required metadata
- rule schemas
- execution context semantics
- determinism and audit requirements
- allowed structural operations

Reasoning rules are:

- **declarative**
- **side-effect free**
- **deterministic**
- **version-pinned per execution**

These files define **how reasoning is performed**, not what is stored (Knowledge) or how correctness is judged (Judgment).

---

## **2. Authority & Scope**

Reasoning rule files:

- are **authoritative within the Reasoning Layer**
- are **read-only at runtime**
- are **version-locked per execution**
- apply uniformly across all products and surfaces using OSLO

Reasoning rules:

- may interpret canonical Knowledge
- may emit findings, signals, or observations
- may **never** mutate canonical data
- may **never** assign scores, severity, or health

---

## **3. File Taxonomy (Canonical)**

```
/reasoning/
  /definitions/     # shared constants, enums, vocabularies
  /rules/           # atomic reasoning rules
  /inference/       # inference patterns (non-executing)
  /signals/         # signal definitions (types only)
  /profiles/        # rule bundles bound to execution context
```

### **File Format Rules**

- YAML required (.yaml)
- No executable code
- No embedded scripts
- No network access
- No system-time access

---

## **4. Global Requirements (All Files)**

### **4.1 Required Header Metadata**

Every reasoning file must include:

```
meta:
  schema: oslo.reasoning.<category>.v1
  id: <string>
  version: <semver>
  status: DRAFT | CANONICAL | DEPRECATED
  created_at: <ISO-8601>
  owner: <team-or-role>
  description: <string>
  compatibility:
    min_engine_version: <semver>
    max_engine_version: <semver|null>
```

---

### **4.2 Immutability Rules**

- CANONICAL versions are immutable
- Any change requires a new version
- Old versions remain valid for replay, audit, and explanation

---

## **5. Execution Context & Trigger Semantics**

### **5.1 Execution Context**

Every reasoning run executes within a required **Execution Context**:

```
ExecutionContext:
  trigger: ONBOARDING | RECOMPUTE | WHATIF | 60SECOND
```

The trigger defines the **sanctioned reasoning context** for that execution.

---

### **5.2 Canonical Trigger Definitions**

### **ONBOARDING**

A **lifecycle initialization context**.

ONBOARDING is used to:

- establish baseline compatibility
- initialize evidence chains
- apply default governance posture

ONBOARDING **does not define reasoning depth**.

ONBOARDING **may delegate** to another trigger (typically 60SECOND).

---

### **60SECOND**

A **bounded reasoning mode** optimized for rapid structural orientation.

60SECOND:

- uses constrained rule profiles
- limits graph traversal depth
- prioritizes high-signal structural checks
- favors speed and explainability over completeness

Used for:

- first-pass project evaluation
- fast reassessment
- executive-level orientation

---

### **RECOMPUTE**

An **incremental reasoning context** triggered by authorized canonical change.

RECOMPUTE:

- evaluates only impacted subgraphs
- supersedes prior reasoning outputs
- preserves determinism and replayability

---

### **WHATIF**

A **hypothetical, isolated context**.

WHATIF:

- runs against a non-canonical snapshot
- must never contaminate canonical reasoning
- emits outputs explicitly tagged as hypothetical

---

### **5.3 Trigger Semantics (Hard Rules)**

Triggers:

- select **eligible profiles**
- constrain **computational scope**
- must be recorded in Evidence Chains

Triggers must **never**:

- alter truth definitions
- suppress findings
- downgrade correctness
- modify severity or judgment boundaries

---

### **5.4 Trigger vs Profile (Clarified)**

| **Aspect** | **Trigger** | **Profile** |
| --- | --- | --- |
| Purpose | Execution context | Rule bundle |
| Controls depth | Indirect | Direct |
| Selects rules | No | Yes |
| Appears in EvidenceChain | Yes | Yes |
| Editable | Rare | Yes |

**Trigger selects profiles.**

**Profiles select rules.**

---

## **6. Profiles**

### **/profiles/*.yaml**

Profiles define **which rules may execute** under which execution contexts.

```
profile:
  id: profile.sixty_second
  description: Fast structural orientation
  contexts:
    trigger: [60SECOND]
  rules:
    - rule.missing_outcome
    - rule.dangling_requirement
```

Profiles:

- must explicitly declare supported triggers
- must not redefine trigger semantics
- may limit rule count, depth, or category

---

## **7. Rule Files**

### **/rules/*.yaml**

Rules define **atomic, deterministic reasoning logic**.

Rules:

- evaluate canonical Knowledge snapshots
- emit observations, signals, or findings
- never mutate Knowledge
- never assign score, severity, or health

---

### **7.1 Rule Schema (Normative)**

```
meta:
  schema: oslo.reasoning.rule.v1
  id: rule.<string>
  version: <semver>
  status: DRAFT | CANONICAL | DEPRECATED
  created_at: <ISO-8601>
  owner: <team-or-role>
  description: <string>

rule:
  applies_to:
    entity: <EntityType | "*">
    relationship: <RelationshipType | "*">

  condition:
    operator: <logical | structural | temporal>
    operands: [...]

  emits:
    type: SIGNAL | FINDING
    id: <string>
    description: <string>
```

---

### **7.2 Determinism Requirements**

Rules **must be deterministic**.

Given:

- identical canonical inputs
- identical rule versions
- identical execution context (trigger + profile)

→ outputs **must be identical**.

Rules must not rely on:

- system time
- execution order
- randomness
- external services

---

### **7.3 Output Guarantees**

Rule outputs are:

- additive
- version-traceable
- consumed by Judgment
- never altered post-emission

---

### **7.4 Explicit Prohibitions**

Rules must never:

- mutate canonical entities or relationships
- create or delete canonical data
- assign severity, score, confidence, or health
- override trigger or profile constraints
- bypass Evidence Chain recording

---

## **8. Evidence Chain Requirements**

Every reasoning execution must record:

- trigger
- profile ID
- rule IDs + versions
- execution limitations imposed by trigger or profile

Example:

```
limitations:
  - Alignment rules skipped due to 60SECOND trigger constraints
```

---

## **9. Determinism Guarantee (System-Level)**

For any execution:

> Same Knowledge snapshot
> 
- same trigger
- same profiles
- same rule versions

→ **identical outputs**

---

## **10. Explicit Non-Responsibilities**

Reasoning must never:

- score outcomes
- determine correctness
- assign severity
- recommend actions
- mutate canonical data

Those belong to **Judgment** or **Execution**.

---

## **Canonical Clarification (Locked)**

> ONBOARDING is a lifecycle context.
> 

> 60SECOND is a reasoning mode.
> 

> 
> 

> ONBOARDING may invoke 60SECOND,
> 

> but they are not interchangeable.
> 

---

## **End of Specification — v1.1**

---

If you want next, the logical follow-ups are:

1. **Update Reasoning Invariants Spec** to explicitly reference lifecycle vs mode
2. **Add Trigger × Profile Compatibility Appendix**
3. **Cross-layer audit** (Reasoning ↔ Judgment ↔ Knowledge) for boundary integrity

Just tell me which to do.