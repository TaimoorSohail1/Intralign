# Execution Layer Specification v1.2 (Canonical)

---

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Layer:** Execution
- **Document Type:** Specification (Normative)
- **Version:** v1.2
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform
- **Scope:** Layer-Level
- **Authoritative For:**
    - Coordination and application of authorized actions
    - Signal ingestion and outcome validation
    - Enforcement of posture- and governance-bounded execution
- **Non-Authoritative For:**
    - Structural truth (Reasoning-owned)
    - Interpretation, severity, confidence (Judgment-owned)
    - Permission and exposure (Governance-owned)
    - Meaning and explanation (Communication-owned)
- **Depends On:**
    - Governance Layer Specification v1.2
    - Execution Posture Contract v1.0
    - Action Class Catalog v1.0
    - Tier Capability Contract v1.0
    - Compute Budget Contract v1.0
    - Observability Scope Specification v1.0
- **Supersedes:** v1.1

---

## **1. Purpose of the Execution Layer**

The Execution Layer exists to **keep OSLO anchored to reality while work and outcomes evolve**.

It answers **one question only**:

> “What is happening, and what authorized coordination may occur as a result?”
> 

Execution coordinates motion and observes reality.

It does **not** decide meaning, priority, or correctness.

---

## **2. Core Invariants**

### **Invariant A — Execution Is Not Decision-Making**

> Execution SHALL NOT interpret, judge, or prioritize.
> 

### **Invariant B — No Ungoverned Action**

> Execution SHALL NOT apply any mutation unless authorized by
> 

> Tier ∩ Posture ∩ Governance
> 

### **Invariant C — Meaning Propagation Is Always On**

> Regardless of posture, Execution SHALL always trigger recomputation and validation.
> 

### **Invariant D — Execution Is Reversible by Design**

> Any applied mutation MUST be reversible when rollback is required by its Action Class.
> 

---

## **3. Required Inputs (Normative)**

The Execution Layer SHALL require the following inputs for all operations:

- ActionAuthorization (from Governance, if mutation requested)
- ActionClass (from Action Class Catalog)
- PostureContext (**required**)
- TierContext
- LifecycleContext
- ComputeContext
- Canonical artifact references (by ID only)

Execution SHALL NOT operate without a valid PostureContext.

---

## **4. Execution Responsibilities**

Execution has **three distinct responsibilities**, all posture-aware.

---

### **4.1 Signal Ingestion & Outcome Validation**

Execution ingests real-world signals to reflect reality.

This includes:

- Progress updates
- External system signals
- Human-entered observations
- Outcome actuals

**Constraints**

- Observational only
- Non-canonical
- No interpretation or scoring

Validation signals MAY trigger recomputation but SHALL NOT cause mutation.

---

### **4.2 Coordination of Authorized Actions**

Execution MAY coordinate and apply mutations **only when all are true**:

1. An ActionAuthorization exists
2. The ActionClass is defined in the catalog
3. The active Posture allows the ActionClass
4. Tier and lifecycle constraints are satisfied

Execution SHALL:

- Apply only the mechanical steps defined by the ActionClass
- Respect propagation bounds
- Record full diffs and rollback references

Execution SHALL NOT:

- Invent new actions
- Expand scope
- Apply second-order trade-offs

---

### **4.3 Recompute Triggers (Always-On)**

After any mutation or signal ingestion, Execution SHALL:

- Trigger Reasoning recomputation
- Trigger Judgment reevaluation
- Trigger Governance reassessment (if required)

This responsibility is **posture-invariant**.

---

## **5. Posture-Aware Execution Rules (Normative)**

### **5.1 Proposal vs Application**

Execution MAY always:

- Generate proposals
- Simulate outcomes
- Produce previews

Execution MAY apply mutations **only** under explicit authorization.

---

### **5.2 Posture Constraints**

| **Posture** | **Execution Behavior** |
| --- | --- |
| Deliberate | No coordinated mutations applied |
| Assisted | Mutations applied only after confirmation |
| Delegated | Mutations applied only if delegatable and authorized |

Execution SHALL enforce these constraints mechanically.

---

## **6. Action Class Enforcement**

Execution SHALL:

- Reject any mutation not mapped to an ActionClass
- Enforce preconditions and forbidden side effects
- Enforce propagation radius
- Require rollback metadata when specified

Any violation SHALL abort execution.

---

## **7. Lifecycle-Sensitive Behavior**

Execution MAY adjust **cadence and breadth**, not semantics, based on lifecycle:

- Onboarding → passive observation
- Active execution → full coordination
- Post-delivery → outcome validation only
- Hypothetical / What-If → simulated execution only

Delegated posture MAY be disallowed by governance in certain stages.

---

## **8. Observability & Audit Requirements**

For every applied or attempted action, Execution MUST log:

- posture_id + version
- tier + lifecycle
- action_class_id
- governance authorization reference
- affected object IDs
- diff + rollback reference (if applicable)
- execution timestamp

No execution event is valid without posture attribution.

---

## **9. Prohibited Behaviors (Hard Violations)**

Execution SHALL NEVER:

- Apply unauthorized Action Classes
- Modify outcomes or success criteria
- Reprioritize work
- Escalate or suppress issues
- Act without PostureContext
- Perform irreversible mutations
- Communicate meaning directly to users

Any such behavior is a **system breach**.

---

## **10. Acceptance Criteria**

The Execution Layer is compliant if and only if:

- PostureContext is required and enforced
- All mutations map to authorized Action Classes
- Tier ∩ Posture ∩ Governance is enforced
- Meaning propagation remains always-on
- All actions are auditable and replayable
- Rollback guarantees are respected

---

## **Invariant (Restated)**

> Execution coordinates motion —
> 

> never authority, meaning, or truth.
> 

---

## **Canonical Close**

> The Execution Layer exists to ensure that
> 

> work, reality, and outcomes remain connected —
> 

> without allowing speed to outrun responsibility.
> 

---

## **End of Specification**

---

### **System Status**

With this update:

- Execution is posture-aware
- Delegation is explicit and bounded
- No accidental autonomy is possible

If you want next, the clean remaining artifacts are:

1. **Observability & Audit Spec (posture-aware update)**
2. **Tier Capability Contract (clarifying tier vs posture)**
3. **End-to-End Posture Trace (example walkthrough)**