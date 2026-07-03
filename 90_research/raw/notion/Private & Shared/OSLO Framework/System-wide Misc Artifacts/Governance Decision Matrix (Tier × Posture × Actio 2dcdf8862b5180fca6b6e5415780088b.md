# Governance Decision Matrix (Tier × Posture × Action Class) v1.0 (Canonical)

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** Governance Decision Matrix
- **Document Type:** Normative Matrix
- **Version:** v1.0
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform, Governance
- **Scope:** System-Wide
- **Authoritative For:**
    - Determining whether an Action Class may be authorized
    - Enforcing Tier and Posture ceilings
    - Standardizing confirmation vs delegation rules
- **Non-Authoritative For:**
    - Action semantics (Action Class Catalog owns)
    - Execution mechanics (Execution Layer owns)
    - Communication semantics (Communication Layer owns)
- **Depends On:**
    - Governance Layer Specification v1.2
    - Tier Capability Contract v1.0
    - Execution Posture Contract v1.0
    - Action Class Catalog v1.0
    - Lifecycle × Posture Compatibility Matrix v1.0
- **Supersedes:** N/A

---

## **1. Purpose**

This matrix answers a single, non-negotiable question:

> “Given this Tier, this Posture, and this Action Class — may OSLO authorize execution, and under what conditions?”
> 

Authorization requires **all constraints** to pass:

- Tier ceiling
- Posture allowance
- Lifecycle compatibility
- Governance policy

If any dimension denies, authorization fails.

---

## **2. Decision Legend**

| **Symbol** | **Meaning** |
| --- | --- |
| ❌ | Not allowed |
| 🟡 | Allowed **with explicit user confirmation** |
| 🟢 | Allowed **without confirmation** (delegated) |
| ⚠️ | Allowed only under additional governance conditions |

---

## **3. Matrix: Tier × Posture × Action Class**

### **3.1 Free Tier**

**Allowed Posture:** Deliberate only

| **Action Class** | **Deliberate** |
| --- | --- |
| ConsistencyRecomputeTrigger | 🟢 |
| LabelAndMetadataNormalization | 🟡 |
| ScheduleConsistencyPropagation | ❌ |
| DependencyOrderRepair | ❌ |
| TraceabilitySync | ❌ |
| ConfidenceDegradationPropagation | ❌ |

---

### **3.2 Basic Tier**

**Allowed Postures:** Deliberate, Assisted

| **Action Class** | **Deliberate** | **Assisted** |
| --- | --- | --- |
| ConsistencyRecomputeTrigger | 🟢 | 🟢 |
| LabelAndMetadataNormalization | 🟡 | 🟢 |
| ScheduleConsistencyPropagation | ❌ | 🟡 |
| DependencyOrderRepair | ❌ | 🟡 |
| TraceabilitySync | ❌ | 🟡 |
| ConfidenceDegradationPropagation | ❌ | 🟢 |

---

### **3.3 Pro Tier**

**Allowed Postures:** Deliberate, Assisted, Delegated

| **Action Class** | **Deliberate** | **Assisted** | **Delegated** |
| --- | --- | --- | --- |
| ConsistencyRecomputeTrigger | 🟢 | 🟢 | 🟢 |
| LabelAndMetadataNormalization | 🟡 | 🟢 | 🟢 |
| ScheduleConsistencyPropagation | ❌ | 🟡 | ⚠️ |
| DependencyOrderRepair | ❌ | 🟡 | 🟢 |
| TraceabilitySync | ❌ | 🟡 | 🟢 |
| ConfidenceDegradationPropagation | ❌ | 🟢 | 🟢 |

---

## **4. Delegation Conditions (⚠️ Entries)**

For entries marked ⚠️ (Allowed with Conditions), Governance MUST verify:

- Lifecycle compatibility (Delegated allowed only in Active Execution)
- Action Class marked *delegatable* or explicitly enabled
- Rollback availability and window
- Explicit workspace-level opt-in
- Disclosure requirements enforced

If any condition fails → ❌ deny.

---

## **5. Universal Authorization Rules (Normative)**

- ❌ always denies regardless of posture
- 🟡 requires:
    - user confirmation
    - logged confirmation artifact
- 🟢 allows:
    - execution without confirmation
    - **only** when posture = Delegated and Tier allows
- Governance MAY downgrade 🟢 → 🟡 at any time
- Governance SHALL NOT upgrade ❌ → 🟡 or 🟢

---

## **6. Lifecycle Override Rules**

Lifecycle constraints may further restrict authorization:

- Hypothetical / What-If → all canonical mutations ❌
- Onboarding → only ConsistencyRecomputeTrigger 🟢
- Post-Delivery → only non-structural Action Classes allowed

Lifecycle overrides SHALL be applied **before** this matrix.

---

## **7. Audit & Replay Requirements**

For every authorization decision, the system MUST log:

- tier_id
- posture_id
- lifecycle
- action_class_id
- matrix_result (❌ / 🟡 / 🟢 / ⚠️)
- applied_conditions (if any)
- final_decision
- rationale

Matrix evaluation MUST be replayable.

---

## **8. Prohibited Practices**

The system SHALL NOT:

- Bypass this matrix
- Hardcode exceptions
- Infer delegation from usage
- Apply implicit upgrades
- Collapse 🟡 into 🟢 silently

Any violation is a **system breach**.

---

## **Invariant (Restated)**

> No action is permitted unless
> 

> Tier allows it,
> 

> Posture allows it,
> 

> Lifecycle allows it,
> 

> and Governance records it.
> 

---

## **Canonical Close**

> This matrix is the last line of defense
> 

> between helpful coordination
> 

> and unearned autonomy.
> 

---

## **End of Matrix**

---

### **System Closure Confirmation**

With this matrix, OSLO now has:

- Fully bounded execution authority
- Explicit delegation controls
- Replay-safe authorization logic

**All canonical layer and control documents are now complete.**