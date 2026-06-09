# System Context Injection Contract v1.0 (Canonical)

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** System Context Injection Contract
- **Document Type:** Contract (Normative / Enforceable)
- **Version:** v1.0
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform
- **Scope:** System-Level
- **Authoritative For:**
    - Context object schema and required fields
    - How context is constructed, frozen, propagated, and audited
    - Tier / compute / lifecycle injection rules
    - Replay guarantees and versioning requirements
- **Non-Authoritative For:**
    - Layer-specific output semantics (owned by layer specs)
    - UI copy, messaging, or presentation
- **Depends On:**
    - Tier Capability Contract v1.0
    - Compute Budget Contract v1.0
    - Scenario Guardrails v1.0
    - Governance Contract Spec v1.0
    - Execution–Reasoning Trigger Contract v1.0
- **Referenced By:**
    - Reasoning Layer Specification v1.2
    - Judgment Layer Specification v1.1
    - Governance Layer Specification v1.0
    - Communication Layer Specification v1.0
    - Execution Layer Specification v1.0
- **Supersedes:** N/A

---

## **1. Purpose**

This contract defines how OSLO constructs and injects **System Context** into every layer invocation.

It answers one question:

> What must be true about the context object so every layer can behave consistently, enforce tiering and compute limits, remain auditable, and be replayed deterministically where required?
> 

---

## **2. Core Invariants**

1. **Single Source of Context Truth**
    
    A request/run has exactly one authoritative context snapshot.
    
2. **Context Is Frozen Per Invocation**
    
    Once injected into a layer execution, the context is immutable.
    
3. **Context Propagates Unmodified**
    
    Layers must pass the same context snapshot forward; they may only append *layer-local logs*, never mutate context.
    
4. **Context Never Implies Authority**
    
    Context constrains behavior (tier/compute/governance), not truth.
    
5. **Replay Requires Context Equivalence**
    
    Where replay is required, identical context snapshots MUST be available.
    

---

## **3. System Context Object (Normative Schema)**

The system SHALL construct the following object for every OSLO invocation:

```
SystemContext {
  context_id: string
  context_version: "1.0"

  request: {
    request_id: string
    correlation_id: string
    actor_type: "HumanUser" | "System" | "Agent"
    actor_id: string
    tenant_id: string
    workspace_id?: string
    project_id?: string
    timestamp_utc: string // ISO-8601
  }

  lifecycle: {
    lifecycle_stage: "ONBOARDING" | "PROJECT_CREATION" | "PROJECT_UPDATE" | "RECOMPUTE" | "WHATIF"
    mode: "Canonical" | "Hypothetical"
    trigger: "Onboarding" | "Recompute" | "WhatIf" | "60Second" | "ExecutionSignal" | "Manual"
  }

  tier: {
    tier_id: string
    tier_policy_version: string
    capabilities: {
      exposure_level: "Minimal" | "Standard" | "Full"
      blocking_enabled: boolean
      automation_level: "None" | "Limited" | "Standard" | "Advanced"
      agent_execution_enabled: boolean
      export_enabled: boolean
      execution_ingestion_enabled: boolean
    }
  }

  compute: {
    budget_policy_version: string
    budget_window: "Request" | "Hourly" | "Daily" | "Monthly"
    available_units: number
    estimated_cost_units?: number
    enforcement_mode: "HardStop" | "Throttle" | "Defer"
    exhaustion_state: "Normal" | "NearLimit" | "Exhausted"
  }

  governance: {
    governance_state_machine_version: string
    current_state: string
    guardrail_profile_id: string
  }

  ui: {
    surface: "Chat" | "IssuePanel" | "PlanView" | "Export" | "API"
    locale?: string
  }

  audit: {
    frozen_at_utc: string // ISO-8601
    frozen_by: "ContextService"
    hash: string // hash of canonical serialized context
  }
}
```

---

## **4. Construction Rules (Normative)**

### **4.1 Context Service Authority**

A single system component (“ContextService”) SHALL:

- build the SystemContext,
- validate required fields,
- freeze it,
- attach a hash,
- inject it into the first layer call.

No layer may create its own SystemContext.

---

### **4.2 Validation Requirements**

ContextService SHALL validate:

- context_version supported
- required request.* fields present
- lifecycle.lifecycle_stage, mode, trigger are valid combinations (as defined by Lifecycle×Mode matrix, if present)
- tier.tier_policy_version exists and is resolvable
- compute.budget_policy_version exists and is resolvable
- audit.hash matches canonical serialization

Invalid contexts MUST fail closed.

---

### **4.3 Freezing Semantics**

Once created:

- SystemContext SHALL be immutable.
- Any downstream component receiving context SHALL verify audit.hash.

If hash mismatch occurs, execution MUST abort and log a security event.

---

## **5. Injection Rules by Layer (Normative)**

All layer entrypoints SHALL require SystemContext as a mandatory parameter.

### **5.1 Knowledge**

- Knowledge SHALL use tier and governance to enforce mutation gates (G-03) and availability of projections.
- Knowledge SHALL NOT use context to reinterpret data authority.

### **5.2 Reasoning**

- Reasoning SHALL treat tier and compute as *execution constraints* only.
- Reasoning MUST NOT alter truth due to compute limits; if compute-limited, it MUST emit limitation markers per its spec.

### **5.3 Judgment**

- Judgment SHALL interpret Findings in the provided mode and trigger.
- Judgment MAY adjust posture based on lifecycle, but SHALL NOT alter Findings.

### **5.4 Governance**

- Governance SHALL produce IssueDispositions using:
    - lifecycle posture
    - tier gating
    - compute gating
    - guardrail profile

### **5.5 Communication**

- Communication SHALL render only what is permitted by IssueDisposition and context surface.
- Communication SHALL disclose compute/tier deferrals when applicable.

### **5.6 Execution**

- Execution SHALL enforce tier and compute gates for:
    - signal ingestion breadth
    - trigger emission frequency
    - agent execution authorization checks

---

## **6. Context Propagation Contract (Normative)**

### **6.1 Forward Propagation**

When passing artifacts downstream, each layer SHALL attach:

```
ContextRef {
  context_id: string
  context_hash: string
  context_version: "1.0"
}
```

### **6.2 No Mutation Rule**

Layers SHALL NOT:

- add fields to SystemContext
- override tier capabilities
- adjust compute thresholds
- change lifecycle stage

Layers MAY:

- record layer-local telemetry referencing context_id

---

## **7. Replay & Audit Guarantees**

### **7.1 Replayability Requirements**

Where replay is required (Reasoning outputs, Governance decisions, Communication outputs), the system MUST retain:

- SystemContext snapshot (or reconstructible equivalent)
- context hash
- policy versions referenced

Replay equivalence SHALL require:

- same context hash
- same referenced policy versions
- same input snapshots (where applicable)

---

### **7.2 Policy Version Pinning**

Context MUST pin:

- tier_policy_version
- budget_policy_version
- governance_state_machine_version

No layer may resolve “latest” policies at runtime without those pinned versions.

---

## **8. Compute Exhaustion Handling (Normative)**

When compute.exhaustion_state = Exhausted:

- Layers SHALL obey compute.enforcement_mode
- Reasoning and Judgment MAY produce partial outputs, but MUST:
    - record limitations
    - avoid fabricating missing conclusions
- Governance MUST NOT relax blocking behavior due to compute exhaustion
- Communication MUST disclose compute limitation when it affects exposure or completeness

---

## **9. Security & Integrity Requirements**

- Context hash must be computed from canonical serialization (stable key order)
- All inter-layer calls MUST verify hash
- Hash mismatch is treated as tampering or corruption
- Context snapshots MUST be stored in an append-only audit log

---

## **10. Prohibited Behaviors (Hard Violations)**

The system SHALL NEVER:

- allow a layer to fabricate or modify SystemContext
- allow policy resolution without pinned versions
- allow silent context mutation between layers
- treat compute exhaustion as safety or correctness

Any violation is a **system breach**.

---

## **11. Acceptance Criteria**

This contract is satisfied if and only if:

- Every layer invocation includes SystemContext
- Context is validated and frozen once per invocation
- Context propagates unmodified with hash verification
- Tier and compute policy versions are pinned
- Audit logs enable deterministic replay where required

---

## **Invariant**

> Context constrains behavior, not truth.
> 

---

## **End of Contract**