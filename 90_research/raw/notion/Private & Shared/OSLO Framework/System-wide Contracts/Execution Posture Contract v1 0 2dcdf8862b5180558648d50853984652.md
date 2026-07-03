# Execution Posture Contract v1.0

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** Execution Posture Contract
- **Document Type:** Contract Specification (Normative)
- **Version:** v1.0
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform, Product
- **Scope:** System-Wide (Execution + Governance + Communication)
- **Authoritative For:**
    - Defining user/workspace-selected execution postures
    - Constraining execution behavior by posture
    - Binding posture to authorization, disclosure, and audit requirements
- **Non-Authoritative For:**
    - Tier entitlements (Tier Capability Contract owns)
    - Action semantics (Action Class Catalog owns)
    - Truth, severity, confidence (Reasoning/Judgment own)
- **Depends On:**
    - Governance Layer Specification v1.0
    - Execution Layer Specification v1.1
    - Communication Layer Specification v1.1
    - Tier Capability Contract v1.0
    - Compute Budget Contract v1.0
    - Observability Scope Specification v1.0
- **Supersedes:** N/A

---

## **1. Purpose**

This contract defines **Execution Postures**: explicit, user/workspace-selected operating modes that control **how much coordination OSLO may perform** after changes occur, while preserving OSLO’s core principles of:

- Outcome accountability
- User trust
- Explicit authority
- Auditability
- Epistemic honesty

Execution Postures are **trade-off profiles**, not AI autonomy levels.

They control **how changes are applied**, not what is true, important, or permitted.

---

## **2. Core Invariants**

### **Invariant A — No Hidden Authority**

> A posture may reduce user effort, but SHALL NOT reduce epistemic honesty or disclosure.
> 

### **Invariant B — No Ungoverned Action**

> Execution SHALL NOT apply mutations unless they are authorized by
> 
> 
> **(Tier ∩ Posture ∩ Governance)**
> 

### **Invariant C — No Silent Trade-offs**

> Postures SHALL NOT permit OSLO to introduce cross-outcome trade-offs without explicit governance alignment.
> 

### **Invariant D — One Meaning Across Surfaces**

> Posture MAY affect verbosity and bundling, but SHALL NOT affect meaning, severity framing, or truth claims.
> 

---

## **3. Definitions**

### **3.1 Posture**

A **Posture** is a named configuration that constrains:

- Allowed action classes
- Confirmation requirements
- Propagation radius
- Bundling/automation intensity
- Rollback requirements
- Disclosure obligations

### **3.2 PostureContext**

A mandatory context object injected into Governance, Execution, and Communication.

```
PostureContext {
  posture_id
  posture_version
  scope { workspace_id, project_id? }
  selected_by { actor_id, actor_type }
  selected_at
  effective_from
  effective_until?
}
```

### **3.3 Action Class**

A bounded, named category of mutations defined in the **Action Class Catalog** (e.g., ScheduleConsistencyPropagation).

---

## **4. Posture Set (v1.0)**

OSLO SHALL support exactly three postures in v1.0.

### **4.1 Deliberate**

**Intent:** Maximize transparency, minimize delegated change.

- OSLO may **propose** changes
- OSLO SHALL NOT **apply** multi-object coordinated mutations
- User confirmation is required for any mutation beyond direct edits
- Propagation is **understanding-only** (issues + explanations)

**Trade-off profile:** Highest trust / highest effort

---

### **4.2 Assisted**

**Intent:** Reduce friction through bundling and guided application.

- OSLO may propose **bundled** change sets
- OSLO may apply coordinated mutations **only after explicit user confirmation**
- OSLO may perform first-order consistency propagation within an approved bundle
- Second-order effects MAY be simulated and disclosed, but SHALL NOT be applied without governance alignment

**Trade-off profile:** Balanced trust / lower effort

---

### **4.3 Delegated**

**Intent:** Minimize user effort via pre-authorized coordination.

- OSLO may apply **pre-authorized** action classes within strict bounds
- User confirmation MAY be waived only for action classes explicitly marked “delegatable” by tier + governance
- All delegated changes MUST be:
    - reversible (rollbackable)
    - logged with full diff
    - disclosed as delegated

**Trade-off profile:** Lowest friction / highest responsibility transfer

**Note:** Delegated does **not** mean autonomous decision-making. It means **delegated execution within explicit constraints**.

---

## **5. Authorization Logic (Normative)**

### **5.1 Authorization Must Intersect**

For any attempted action A, the system SHALL compute:

> Allowed(A) = TierAllows(A) ∩ PostureAllows(A) ∩ GovernanceAuthorizes(A)
> 

If any component denies, the action SHALL NOT execute.

### **5.2 Governance Supremacy**

Governance decisions override posture preferences.

> A posture SHALL NOT expand permissions beyond governance.
> 

### **5.3 Posture Cannot Override Tier**

Tier entitlements override posture.

> A posture SHALL NOT enable action classes not included in the active tier.
> 

---

## **6. Confirmation Requirements (Normative)**

Each posture SHALL enforce confirmation as follows:

| **Action Type** | **Deliberate** | **Assisted** | **Delegated** |
| --- | --- | --- | --- |
| Direct user edit | Allowed | Allowed | Allowed |
| Single-object OSLO proposal | Confirm required | Confirm required | Confirm optional* |
| Bundled multi-object change set | Confirm required | Confirm required | Confirm optional* |
| Delegatable action class | Not allowed | Allowed w/ confirm | Allowed without confirm* |
- Only when explicitly enabled by Governance + Tier and marked delegatable in Action Class Catalog.

---

## **7. Propagation Rules (Normative)**

### **7.1 Meaning Propagation Always On**

Regardless of posture, OSLO SHALL:

- Recompute implications
- Surface issues
- Update plan health signals
- Preserve epistemic labeling
- Disclose uncertainty

### **7.2 Change Propagation Is Posture-Gated**

Only the application of mutations is posture-gated.

Postures SHALL NOT suppress issue detection or health recomputation.

---

## **8. Disclosure Requirements (Normative)**

Whenever a posture affects behavior, Communication SHALL disclose:

- The active posture name
- Whether a change was:
    - user-confirmed
    - delegated within policy
- That absence of surfaced issues does not imply safety (where applicable)
- That changes were bounded by tier/governance constraints

### **8.1 Delegation Disclosure (Required)**

If any change is applied without explicit confirmation, the message MUST include:

- “Applied under Delegated posture”
- The action class name
- Rollback availability and window (if applicable)

---

## **9. Audit & Observability Requirements (Normative)**

For every action applied (confirmed or delegated), the system MUST log:

- posture_id + posture_version
- tier + compute context
- governance authorization reference
- action class
- object IDs touched
- diff summary + full diff pointer
- rollback id (if executed)

Posture MUST be included in all replay/audit trails.

---

## **10. Lifecycle Constraints (Normative)**

Postures MAY be constrained by lifecycle stage via governance policy.

Default v1.0 rule:

- Delegated posture MAY be disabled in:
    - onboarding
    - hypothetical / what-if contexts
- Delegated posture SHOULD require explicit opt-in per workspace

(Exact allow/deny per lifecycle is governed by the Governance Decision Matrix; this contract defines the capability, not the policy.)

---

## **11. Prohibited Behaviors (Hard Violations)**

No posture SHALL permit OSLO to:

- Redefine outcomes
- Introduce cross-outcome trade-offs without governance alignment
- Apply irreversible mutations without rollback guarantees
- Suppress disclosures about delegation
- Alter severity/confidence semantics
- Bypass governance or tier limitations

Any such behavior is a **system breach**.

---

## **12. Acceptance Criteria**

This contract is satisfied if and only if:

- PostureContext is injected and enforced system-wide
- Authorization is computed as Tier ∩ Posture ∩ Governance
- Meaning propagation remains always-on
- Delegated actions are reversible, auditable, and disclosed
- Communication accurately represents posture effects
- No posture expands authority beyond governance

---

## **Canonical Close**

> Execution Postures allow users to choose their trade-offs explicitly—
> 

> without allowing OSLO to hide authority, uncertainty, or responsibility.
> 

---

## **End of Contract**