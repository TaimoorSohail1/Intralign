# Communication Authorization State Machine v1.0

**Purpose:** Ensure Communication can *prepare* messages early but only *emit* after explicit Governance authorization.

---

### **State Set (Enum)**

1. **DRAFTING**
    
    Communication is generating/formatting candidate messages from an input payload.
    
2. **STAGED**
    
    A message is assembled and stored, but **not eligible** to emit yet.
    
3. **PENDING_GOVERNANCE**
    
    Communication has registered an emission request and is waiting on Governance evaluation.
    
4. **BLOCKED**
    
    Governance has evaluated and **denied** emission (conditions not satisfied).
    
5. **AUTHORIZED**
    
    Governance has evaluated and **approved** emission (conditions satisfied).
    
6. **EMITTED**
    
    Message has been delivered to at least one UI surface.
    
7. **ACKED**
    
    User (or system) acknowledged/consumed the message per required rule (e.g., confirmation gate satisfied).
    
8. **EXPIRED**
    
    Message became stale (TTL or superseded) before emission or completion.
    
9. **CANCELLED**
    
    Message was withdrawn intentionally (superseded, revoked, or user context changed).
    

---

### **Canonical Transitions (Events → Next State)**

### **Build & Stage**

- **on_payload_received**: ∅ → DRAFTING
- **on_message_composed**: DRAFTING → STAGED
- **on_emit_intent_registered**: STAGED → PENDING_GOVERNANCE

### **Governance Decision**

- **on_governance_denied(reason_code)**: PENDING_GOVERNANCE → BLOCKED
- **on_governance_approved(auth_token, audience, channel, ttl)**: PENDING_GOVERNANCE → AUTHORIZED

### **Blocked Re-check / Recovery**

- **on_condition_update** (e.g., confirmation received, approval obtained): BLOCKED → PENDING_GOVERNANCE
- **on_superseded_by_newer_message**: BLOCKED → CANCELLED
- **on_ttl_elapsed**: BLOCKED → EXPIRED

### **Emit**

- **on_emit_success(ui_receipt_id)**: AUTHORIZED → EMITTED
- **on_emit_failed(transient_error)**: AUTHORIZED → PENDING_GOVERNANCE *(optional: retry requires governance-valid TTL/token)*
- **on_auth_revoked**: AUTHORIZED → CANCELLED
- **on_ttl_elapsed**: AUTHORIZED → EXPIRED

### **Post-Emit Completion**

- **on_user_ack_required**: EMITTED → (wait) → ACKED *(when ack arrives)*
- **on_user_ack_received**: EMITTED → ACKED
- **on_ack_timeout**: EMITTED → EXPIRED *(if ack required but not received within TTL)*

### **Global Cancellation/Expiry**

- **on_hard_cancel**: DRAFTING|STAGED|PENDING_GOVERNANCE|BLOCKED|AUTHORIZED|EMITTED → CANCELLED
- **on_global_ttl_elapsed**: DRAFTING|STAGED|PENDING_GOVERNANCE|BLOCKED|AUTHORIZED|EMITTED → EXPIRED

---

### **Governance Authorization Contract (Minimal Fields)**

When Governance approves, it returns an **Authorization Grant**:

- auth_token (opaque, required to emit)
- audience_scope (e.g., user, project-role, org-role)
- channel_scope (UI banner, inline, digest, notification)
- priority (low/med/high/critical)
- ttl (hard expiry)
- conditions_snapshot (what was true at approval time)
- revocation_policy (revocable if conditions change)

**Hard rule:** Communication **MUST** present a valid, unexpired auth_token to emit.

---

### **Block Reasons (Reason Codes)**

Governance denial should return a structured reason:

- GATE_INFERENCE_CONFIRMATION_REQUIRED
- GATE_TIER_AUTHORITY_INSUFFICIENT
- GATE_APPROVALS_INCOMPLETE
- GATE_RISK_NOT_MET_FOR_INTERRUPT
- GATE_USER_CONTEXT_NOT_READY (e.g., not in project, onboarding incomplete)
- GATE_RATE_LIMIT_ACTIVE
- GATE_SUPPRESSION_ACTIVE (duplicate / noisy)
- GATE_DEPENDENCY_MISSING (evidence chain incomplete, upstream missing)

These reason codes drive deterministic re-check triggers.

---

### **Emission Modes (Governance-Selected)**

Governance should specify *how* it may surface:

- SILENT_BADGE (no interrupt)
- INLINE_CALLOUT
- BANNER
- MODAL
- DIGEST_ONLY
- NOTIFICATION_PUSH *(if supported)*

This prevents Communication from “choosing drama.”

---

### **Invariants (Non-Negotiable)**

1. **No Auth, No Emit**
    
    AUTHORIZED is the only state that may transition to EMITTED.
    
2. **Authorization is scoped**
    
    Auth is bound to {message_id, audience_scope, channel_scope, ttl}.
    
3. **Silence is default**
    
    If Governance can’t decide, system remains BLOCKED or PENDING_GOVERNANCE, not “best-effort emit.”
    
4. **Revocation is real**
    
    If any gating condition invalidates, AUTHORIZED → CANCELLED (or back to PENDING_GOVERNANCE if re-evaluable).
    

---

### **Minimal Mermaid Diagram (Optional Spec Artifact)**

```
stateDiagram-v2
  [*] --> DRAFTING: on_payload_received
  DRAFTING --> STAGED: on_message_composed
  STAGED --> PENDING_GOVERNANCE: on_emit_intent_registered

  PENDING_GOVERNANCE --> BLOCKED: on_governance_denied
  PENDING_GOVERNANCE --> AUTHORIZED: on_governance_approved

  BLOCKED --> PENDING_GOVERNANCE: on_condition_update
  BLOCKED --> CANCELLED: on_superseded
  BLOCKED --> EXPIRED: on_ttl_elapsed

  AUTHORIZED --> EMITTED: on_emit_success
  AUTHORIZED --> PENDING_GOVERNANCE: on_emit_failed
  AUTHORIZED --> CANCELLED: on_auth_revoked
  AUTHORIZED --> EXPIRED: on_ttl_elapsed

  EMITTED --> ACKED: on_user_ack_received
  EMITTED --> EXPIRED: on_ack_timeout

  DRAFTING --> CANCELLED: on_hard_cancel
  STAGED --> CANCELLED: on_hard_cancel
  PENDING_GOVERNANCE --> CANCELLED: on_hard_cancel
  EMITTED --> CANCELLED: on_hard_cancel
```

---

If you want, I can also produce:

- the **exact event schema** (JSON) for each transition
- the **Governance policy checklist** that decides approve/deny
- or a **BDD test matrix** for this state machine (happy paths + denial + retry + revocation).