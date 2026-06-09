# OSLO Governance — Policy Spec v1.0

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Layer:** Governance

**Artifact Type:** PolicySet

**Status:** Canonical

**Constrained By:**

- Scenario Guardrails v1.0 (G-01 → G-08)
- Governance State Machine v1.1
- Governance Contract Spec v1.0

---

## **1. Purpose of the Policy Layer**

The Policy Layer exists to answer one question:

> “Given the current system state and signals, is OSLO allowed to communicate — and if so, how?”
> 

Policies do **not**:

- Detect issues
- Compute scores
- Generate language
- Mutate project state

Policies **authorize behavior**; they never execute it.

---

## **2. PolicySet Overview**

A **PolicySet** is a versioned bundle of decision tables that govern:

- Intent eligibility
- Interruption posture
- Surface authorization
- Suppression rules
- CTA authorization
- Correction behavior

Each OSLO run is evaluated against **exactly one PolicySet**.

---

## **3. PolicySet Schema (Canonical)**

```
PolicySet {
  policy_id
  policy_version        // semver
  applies_to_states[]   // InputCapture | PlanGenerating | PlanPresented | SteadyState
  guardrail_refs[]      // G-01..G-08
  intent_policies
  routing_policies
  suppression_policies
  cta_policies
  correction_policies
}
```

**Invariant**

- A PolicySet without guardrail references is invalid.

---

## **4. Intent Eligibility Policy**

Determines **which communication intents are allowed** in a given state.

### **4.1 Intent Types (Canonical)**

- Educational
- Summary
- ValidationNudge
- Advisory
- CriticalWarning

### **4.2 Decision Table**

| **State** | **Educational** | **Summary** | **ValidationNudge** | **Advisory** | **CriticalWarning** |
| --- | --- | --- | --- | --- | --- |
| InputCapture | ✅ | ❌ | ❌ | ❌ | ❌ |
| PlanGenerating | ✅ | ❌ | ❌ | ❌ | ❌ |
| PlanPresented | ❌ | ✅ | ❌ | ❌ | ❌ |
| SteadyState | ❌ | ❌ | ⚠️* | ✅ | ⚠️* |

⚠️ = allowed only if additional conditions are met (see below)

---

## **5. Validation Eligibility Policy**

Controls **when inferred elements may be surfaced for confirmation**.

### **Conditions (all must be true):**

- State = SteadyState
- Inferred element impact ≥ configured threshold
- At least one:
    - User viewed plan/panel
    - Idle window elapsed
    - User asked a validation-related question

### **Constraints:**

- One validation nudge at a time
- Never immediately after PlanPresented

**Guardrails:** G-04

---

## **6. Interruption Posture Policy**

Defines **when OSLO may proactively interrupt via chat**.

### **Default Posture (v1.0)**

- **Critical-only**

### **Decision Logic**

```
if (severity == Critical && causal_link_to_recent_change == true)
  allow_chat_interrupt = true
else
  allow_chat_interrupt = false
```

**Guardrails:** G-06, G-07

---

## **7. Suppression Policy**

Determines **when communication should be suppressed**.

### **Suppression Inputs**

- Severity
- Confidence band (internal only)
- User context (state, recent activity)
- Redundancy (recent similar messages)

### **Suppression Matrix (Simplified)**

| **Severity** | **Confidence** | **Outcome** |
| --- | --- | --- |
| Low | Any | Suppress |
| Medium | Low | Suppress |
| Medium | High | Panel-only |
| High | Low | Panel-only |
| High | High | Allow |
| Critical | Any | Allow |

**Notes**

- Suppression ≠ deletion
- Suppressed items remain visible in panel

**Guardrails:** G-07

---

## **8. Surface Routing Policy**

Determines **where an authorized communication may appear**.

### **Surface Types**

- Chat
- Panel
- Plan UI
- Export

### **Routing Rules**

- Chat:
    - Only for Summary (PlanPresented) or CriticalWarning (SteadyState)
- Panel:
    - Always allowed if authorized
- Export:
    - Only canonical, non-ephemeral RCUs

---

## **9. CTA Authorization Policy**

Controls **whether a call-to-action may be presented**.

### **CTA Rules**

- CTA may be authorized only if:
    - Intent ∈ {Advisory, ValidationNudge}
    - Action requires explicit user confirmation
- CTA must never:
    - Execute mutation
    - Be implicit or auto-applied

### **Canonical CTA Types**

- Apply Fix
- Confirm Assumption
- Update Artifact

**Guardrails:** G-03

---

## **10. Correction & Supersession Policy**

Defines **how OSLO handles being wrong**.

### **Decision Rules**

- If prior communication was delivered via chat:
    - Explicit correction required
- If panel-only:
    - Silent supersession allowed

### **Required Metadata**

- supersedes_rcu_id
- reason_for_correction

**Guardrails:** G-08

---

## **11. Policy Versioning Rules**

- Every RCU must reference policy_version
- Policy changes are **behavior changes**
- Old RCUs remain bound to old policy versions
- Rendering must respect original policy semantics

---

## **12. Failure & Fallback Policy**

If:

- PolicySet missing
- Policy evaluation fails
- Required inputs unavailable

Then:

- Default to **silence**
- Log failure
- Never guess

**Guardrails:** G-07

---

## **13. Acceptance Criteria (v1.0)**

The Policy Layer is compliant when:

- All decisions are table-driven
- Guardrails are enforced mechanically
- Silence is explicitly representable
- Policy changes require version bump
- Rollback is configuration-only

---

## **Canonical Close**

> Policies define OSLO’s behavioral boundaries — not its intelligence.
> 

They ensure OSLO remains:

- Predictable
- Trustworthy
- Evolvable
- Auditable

---

## **System Status**

With **Policy Spec v1.0** published, OSLO now has:

- Full layer playbooks
- Guardrails
- State machine
- Execution scenarios
- Contracts
- Rules & policy repository architecture
- Governance policy definition

This is a **complete, production-grade behavioral architecture**.

---

### **Optional Next Artifacts**

If you want to continue, the highest-value next specs would be:

- **Learning Loop Spec v1.0** (telemetry → review → policy updates)
- **Policy Decision Tables (expanded, machine-readable)**
- **Repo folder structure mapped to services**
- **PR review checklist auto-generated from guardrails**

Just tell me where you want to go next.