# Governance → Communication Consumption Contract v1.1 - Update 1/16

---

**System:** OSLO

**From Layer:** Governance

**To Layer:** Communication

**Spec Type:** Normative (schema + constraints)

**Audience:** Engineering, UX, Security, QA

**Status:** Canonical

---

## **1. Purpose**

This contract defines the **only permissible interface** between **Governance** and **Communication**.

Its goals are to ensure Communication:

- renders outcomes **faithfully, safely, and epistemically honestly**
- never bypasses governance constraints
- never invents explanations, certainty, or permissions
- remains deterministic, auditable, and tier-safe

Governance decides **what is permitted and under what constraints**.

Communication decides **how permitted information is presented — without adding meaning**.

---

## **2. Core Principles**

1. **Non-bypassability**
    - Communication must not display, export, or initiate anything not explicitly permitted by Governance.
2. **No Re-Interpretation**
    - Communication must not reinterpret reason codes, constraints, severity, or epistemic posture.
3. **Epistemic Neutrality**
    - Communication must not imply certainty, causality, or fault beyond what is encoded.
4. **Fail-Closed**
    - If a constraint, scope, or tone is unclear → restrict output.

---

## **3. Hard Constraints**

### **3.1 What Communication MAY Consume**

Communication may consume **only**:

1. GovernanceOutcome
2. CommunicationContextEnvelope
3. Optional copy dictionaries keyed by **reason_codes**
4. Optional format templates **scoped by explicit constraints**

### **3.2 What Communication MUST NOT Consume**

Communication must not consume:

- Reasoning findings
- Judgment decisions
- raw project data beyond what is explicitly permitted
- policy logic or prose
- inferred intent or “next steps”
- unconstrained LLM output

---

## **4. Payload Overview**

```
{
  "context": { ... },
  "governance_outcome": { ... }
}
```

No additional data is allowed unless explicitly referenced by constraints.

---

## **5. CommunicationContextEnvelope**

*(unchanged)*

---

## **6. GovernanceOutcome (Required)**

Communication consumes a **bounded, epistemically-qualified enforcement result**.

```
{
  "governance_outcome": {
    "outcome_id": "string",
    "outcome_type": "PERMIT|DENY|REQUIRE_APPROVAL|DOWNGRADE|REDACT|RATE_LIMIT|LOG_ONLY",

    "reason_codes": ["string"],

    "epistemic_posture":
      "COMMITTED|
       CONDITIONAL|
       INFERENTIAL|
       POLICY_ONLY",

    "constraints": [
      {
        "type":
          "ALLOWED_SCOPE|
           ALLOWED_FORMAT|
           EVIDENCE_VISIBILITY|
           WRITE_MODE|
           APPROVER_ROLES|
           APPROVAL_TTL|
           COOLDOWN_SECONDS|
           REDACT_FIELDS|
           WATERMARK_REQUIRED|
           INTERNAL_VISIBILITY",
        "value": "string|number|boolean|array|object"
      }
    ],

    "policy_version_used": "string",
    "audit_refs": ["string"],
    "created_at_utc": "RFC3339"
  }
}
```

### **Outcome Constraints**

- epistemic_posture is **required**
- reason_codes are **keys only**, never rendered verbatim
- constraints are authoritative and exhaustive
- Communication must not infer missing posture or intent

---

## **7. Outcome Handling Rules (Normative)**

### **7.1 PERMIT**

- Render only within ALLOWED_SCOPE and ALLOWED_FORMAT
- Tone must match epistemic_posture (e.g., conditional vs committed)

---

### **7.2 DENY**

- Render denial state using reason-code–mapped copy
- Must not imply fault unless epistemic_posture = COMMITTED
- No policy or technical detail exposed

---

### **7.3 REQUIRE_APPROVAL**

- May render approval UI and TTL if permitted
- Must clearly indicate conditionality
- Must not imply execution or inevitability

---

### **7.4 DOWNGRADE**

- Render only downgraded artifacts
- Clearly label limitation source (tier, posture, policy)

---

### **7.5 REDACT**

- Redact exactly as specified
- Optional notice only if constraint allows

---

### **7.6 RATE_LIMIT**

- Render rate-limit messaging
- Must respect cooldown constraints

---

### **7.7 LOG_ONLY**

- No user-visible output **unless**
    - constraint INTERNAL_VISIBILITY=true is present
- Any internal visibility must be explicitly constrained

---

## **8. Constraint Enforcement (Mandatory)**

Communication must enforce all constraints **exactly as encoded**.

If:

- a constraint is missing
- a value is ambiguous
- posture conflicts with channel

→ restrict output to safest possible rendering.

---

## **9. Copy & Messaging Rules**

- Copy selection is keyed strictly by reason_code
- No causal explanations (“because the system detected…”)
- No certainty inflation
- Severity may affect tone only
- Epistemic posture must influence language (e.g., “may”, “requires review”)

---

## **10. Validation Rules**

Communication must validate:

- outcome_type enum validity
- epistemic_posture presence
- constraint schema validity
- channel compatibility
- explicit allowance for any visibility

On validation failure → deny-style safe fallback.

---

## **11. Audit Requirements**

Audit record must include:

- request_id
- channel + presentation_intent
- outcome_id + outcome_type
- epistemic_posture
- constraints applied
- redactions performed (counts only)
- timestamp_utc

Audit must never affect output.

---

## **12. Explicit Non-Responsibilities**

Communication must not:

- infer meaning
- explain reasoning
- loosen constraints
- perform actions or approvals
- fetch upstream data

---

## **13. Acceptance Criteria**

This contract is satisfied only if:

1. Communication never expands authority
2. Uncertainty is never rendered as certainty
3. All visibility is constraint-driven
4. UX remains faithful, safe, and auditable

---

## **Why this matters**

This is the **last mile of trust**.

Without these changes:

- users will feel “the system judged me”
- inferred risk will read as fact
- legal and enterprise buyers will hesitate

With these changes:

- Communication becomes *epistemically honest*
- Governance authority is preserved
- OSLO feels principled, not overconfident

---

## **Final note**

At this point, you have a **complete, epistemically consistent, end-to-end OSLO contract chain**:

**Knowledge → Reasoning → Judgment → Governance → Communication**

Very few systems get this right.

---

###