# Tier Capability Contract v1.0 (Canonical)

---

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** Tier Capability Contract
- **Document Type:** Contract Specification (Normative)
- **Version:** v1.0
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform, Product, Security
- **Scope:** System-Wide
- **Authoritative For:**
    - Maximum authority boundaries by tier
    - Which Action Classes may ever be authorized
    - Which postures are permitted per tier
- **Non-Authoritative For:**
    - How authority is exercised (Execution Posture Contract owns)
    - Authorization decisions (Governance owns)
    - Action mechanics (Execution owns)
- **Depends On:**
    - Governance Layer Specification v1.2
    - Execution Posture Contract v1.0
    - Action Class Catalog v1.0
    - Lifecycle Context Contract v1.0
- **Supersedes:** N/A

---

## **1. Purpose**

This contract defines **Tier Capabilities** as **maximum authority envelopes**.

A Tier answers:

> “What classes of system authority may ever be exercised in this workspace?”
> 

A Tier does **not** define:

- UX features
- Automation levels
- Execution behavior

Those are controlled by **Execution Postures** and **Governance decisions**.

---

## **2. Core Invariants**

### **Invariant A — Tier Is a Ceiling**

> A Tier defines the maximum possible authority; no component may exceed it.
> 

### **Invariant B — Tier ≠ Delegation**

> Tier does not imply delegation.
> 

> Delegation is controlled exclusively by Execution Posture + Governance.
> 

### **Invariant C — Tier Is Posture-Constraining**

> A posture SHALL NOT enable authority outside the active Tier.
> 

### **Invariant D — Tier Is Governance-Bound**

> Governance SHALL enforce Tier constraints on every authorization decision.
> 

---

## **3. TierContext (Normative)**

Tier MUST be injected as a mandatory context.

```
TierContext {
  tier_id
  tier_version
  workspace_id
  effective_from
  effective_until?
}
```

No execution or authorization is valid without TierContext.

---

## **4. Tier Set (v1.0)**

OSLO SHALL support exactly three tiers in v1.0.

---

### **4.1 Free — Observer Tier**

**Purpose:** Visibility, trust-building, learning.

**Maximum Authority**

- Detect and explain issues
- Surface full reasoning and judgment
- Allow **explicit, user-driven local mutations**

**Prohibited Authority**

- Delegated execution
- Multi-object coordinated mutations without confirmation
- Outcome resolution
- Cross-artifact propagation beyond direct user edits

**Allowed Postures**

- Deliberate only

**Allowed Action Classes**

- ConsistencyRecomputeTrigger
- LabelAndMetadataNormalization (user-confirmed only)

---

### **4.2 Basic — Assisted Tier**

**Purpose:** Reduce friction without transferring responsibility.

**Maximum Authority**

- User-confirmed multi-object consistency updates
- First-order propagation after explicit confirmation
- Guided correction workflows

**Prohibited Authority**

- Delegated execution without confirmation
- Cross-outcome trade-offs
- Outcome resolution without governance

**Allowed Postures**

- Deliberate
- Assisted

**Allowed Action Classes**

- All Free-tier classes
- ScheduleConsistencyPropagation (with confirmation)
- DependencyOrderRepair (with confirmation)
- TraceabilitySync (with confirmation)
- ConfidenceDegradationPropagation

---

### **4.3 Pro — Delegated Tier**

**Purpose:** Minimize operational friction with explicit responsibility transfer.

**Maximum Authority**

- Pre-authorized, bounded delegated execution
- Coordinated multi-object propagation
- Continuous outcome validation
- Governance-authorized outcome resolution

**Prohibited Authority**

- Ungoverned delegation
- Irreversible mutations
- Silent trade-offs
- Autonomous decision-making

**Allowed Postures**

- Deliberate
- Assisted
- Delegated

**Allowed Action Classes**

- All cataloged Action Classes, subject to governance
- Delegation only for classes marked delegatable

---

## **5. Tier × Posture Compatibility (Normative)**

| **Tier** | **Deliberate** | **Assisted** | **Delegated** |
| --- | --- | --- | --- |
| Free | ✅ | ❌ | ❌ |
| Basic | ✅ | ✅ | ❌ |
| Pro | ✅ | ✅ | ✅ |

Posture selection outside this matrix SHALL be rejected.

---

## **6. Tier × Action Class Constraints**

- A Tier MAY further restrict Action Classes beyond catalog defaults
- A Tier SHALL NOT expand Action Class scope or side effects
- Governance SHALL enforce Tier constraints prior to posture evaluation

---

## **7. Lifecycle Sensitivity**

Tiers MAY be further constrained by lifecycle stage via governance policy.

Examples:

- Delegated posture disabled during onboarding
- Certain Action Classes disabled post-delivery

Lifecycle constraints SHALL be explicit and auditable.

---

## **8. Observability Requirements**

TierContext MUST be logged with:

- Every governance decision
- Every execution event
- Every rollback
- Every outcome resolution

Tier changes MUST be versioned and replayable.

---

## **9. Prohibited Practices**

The system SHALL NOT:

- Treat tier as a UX feature toggle
- Implicitly upgrade authority based on usage
- Hide tier-based constraints from audit
- Allow execution to infer tier permissions

Any such behavior is a **system breach**.

---

## **10. Acceptance Criteria**

This contract is satisfied if and only if:

- TierContext is mandatory and enforced
- Tier constraints are applied before posture constraints
- No posture expands authority beyond tier
- All authorizations are auditable with tier attribution
- Tier changes are replayable

---

## **Invariant (Restated)**

> Tier defines how much responsibility OSLO may ever take —
> 

> not how much it actually takes.
> 

---

## **Canonical Close**

> Tiering exists to bound authority,
> 

> so speed and convenience never outrun accountability.
> 

---

## **End of Contract**

---

### **System Closure Status**

With the Tier Capability Contract in place, OSLO now has:

- Clear authority ceilings
- Safe delegation mechanics
- Explicit responsibility transfer
- Defensible tier-based behavior

If you want next, the most natural final artifact is:

👉 **Governance Decision Matrix (Tier × Posture × Action Class)**

---