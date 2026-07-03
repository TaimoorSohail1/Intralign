# Communication Layer Specification v1.2 (Canonical)

---

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Layer:** Communication
- **Document Type:** Specification (Normative)
- **Version:** v1.2
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Platform, Product, UX
- **Scope:** Layer-Level
- **Authoritative For:**
    - Rendering and delivery of system messages
    - Disclosure rules and epistemic safety guarantees
    - Posture-aware explanation of system behavior
- **Non-Authoritative For:**
    - Structural truth (Reasoning-owned)
    - Severity/confidence (Judgment-owned)
    - Authorization (Governance-owned)
    - Mutation mechanics (Execution-owned)
- **Depends On:**
    - Governance Layer Specification v1.2
    - Execution Layer Specification v1.1
    - Execution Posture Contract v1.0
    - Action Class Catalog v1.0
    - Tier Capability Contract v1.0
- **Supersedes:** v1.1

---

## **1. Purpose of the Communication Layer**

The Communication Layer exists to **make governed system behavior understandable without implying authority, correctness, or safety**.

It answers **one question only**:

> “Given what was authorized and executed, how should this be explained so it is correctly understood?”
> 

Communication explains *what happened* and *why it was allowed* —

never *what should happen* or *what is correct*.

---

## **2. Core Invariants**

### **Invariant A — No Authority Leakage**

> Communication SHALL NOT imply that OSLO decisions are correct, safe, or optimal.
> 

### **Invariant B — Posture Honesty**

> If execution behavior was influenced by posture, Communication SHALL disclose that influence explicitly.
> 

### **Invariant C — Meaning Is Surface-Invariant**

> Presentation may vary by surface; meaning SHALL NOT.
> 

---

## **3. Required Inputs**

The Communication Layer SHALL consume:

- IssueDisposition[] (from Governance)
- ActionAuthorization[] (from Governance, if applicable)
- Referenced Issue[] / Finding[] (read-only, by ID)
- PostureContext (required)
- TierContext
- LifecycleContext

Communication SHALL NOT consume:

- Observability signals directly
- Execution proposals or diffs
- User preferences beyond posture selection

---

## **4. Canonical Communication Artifact**

### **4.1 Communication Unit (CU)**

```
CommunicationUnit {
  cu_id
  source_issue_id?
  source_action_class_id?
  posture_context
  tier_context
  surface
  message_type
  content
  disclosures[]
  references { issue_id?, finding_id? }
}
```

Every user-visible message MUST resolve to one or more CUs.

---

## **5. Posture-Aware Disclosure Rules (Normative)**

### **5.1 Mandatory Posture Disclosure**

If posture affects execution behavior, Communication MUST disclose:

- The **active posture name**
- A short explanation of what that posture permits
- Whether the user:
    - explicitly confirmed the change, or
    - delegated execution within policy

**Example (canonical wording):**

> “This change was applied under the
> 
> 
> *Delegated*
> 

---

### **5.2 Delegated Execution Disclosure (Required)**

If an action was applied without explicit user confirmation:

Communication MUST include:

- The Action Class name
- Confirmation that the action was governance-authorized
- Rollback availability and window (if applicable)

**Example:**

> “OSLO applied a
> 
> 
> *ScheduleConsistencyPropagation*
> 

> You can review or undo this change.”
> 

---

### **5.3 Confirmation Disclosure**

If an action required confirmation:

Communication MUST state:

- That the change required user approval
- That OSLO did not act until confirmation was received

---

## **6. What Communication MAY Compress vs MUST Preserve**

### **May Compress**

- Explanation verbosity
- Step-by-step detail
- Bundling of multiple low-risk changes

### **Must Preserve**

- Epistemic state (inferred vs confirmed)
- Posture influence
- Governance authorization
- Uncertainty and limitations

Compression SHALL NOT imply confidence or safety.

---

## **7. Surface-Specific Rules (Clarified)**

| **Surface** | **Additional Requirements** |
| --- | --- |
| UI (Issue Panel) | Posture badge + expandable explanation |
| Summary View | Posture noted if relevant |
| Detail View | Full posture + authorization disclosure |
| Export / PDF | Explicit posture + authorization footer |

Exports MUST NOT imply stronger authority than UI views.

---

## **8. Prohibited Communication Behaviors**

The Communication Layer SHALL NEVER:

- Hide posture influence
- Describe delegated execution as “automatic” or “self-healing”
- Imply outcome success or safety
- Suggest actions or remediation
- Reframe severity or confidence
- Mask governance constraints

Any violation is a **contract breach**.

---

## **9. Determinism & Replayability (Unchanged)**

Communication MUST be:

- Deterministic given identical inputs
- Replayable with posture and authorization context intact
- Traceable to:
    - Issue IDs
    - Action Class IDs
    - Governance authorization references

---

## **10. Acceptance Criteria**

Communication is compliant if and only if:

- Every message maps to an IssueDisposition or ActionAuthorization
- Posture influence is disclosed whenever relevant
- Delegated actions are explicitly labeled
- Meaning is consistent across surfaces
- No authority or safety is implied
- Outputs are auditable and replayable

---

## **Invariant (Restated)**

> Communication may reduce cognitive load —
> 

> but it may never reduce accountability clarity.
> 

---

## **Canonical Close**

> The Communication Layer exists to ensure that
> 

> even when OSLO acts on a user’s behalf,
> 

> nothing important is hidden.
> 

---

## **End of Specification**

---

### **System Status**

With this update:

- Execution postures are fully surfaced
- Delegated behavior is never silent
- Trust remains intact across all output surfaces

If you want next, the most natural follow-ons are:

1. **UI Posture & Disclosure Guidelines**
2. **Sample Communication Units (by posture)**
3. **End-to-End Posture Trace (edit → governance → execution → communication)**