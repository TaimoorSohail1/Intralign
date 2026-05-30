# Judgement → Governance Consumption Contract v1.1 - Update 1/15

---

**System:** OSLO

**From Layer:** Judgement

**To Layer:** Governance

**Spec Type:** Normative (schema + constraints)

**Audience:** Engineering, Security, QA

**Status:** Canonical

---

## **1. Purpose**

This contract defines the **only permissible interface** between **Judgement** and **Governance**.

Its goals are to ensure Governance:

- enforces policy deterministically
- never re-decides or re-reasons
- never inspects raw project data
- respects epistemic limits on authority
- produces bounded, auditable enforcement outcomes

Judgement decides **recommended posture**.

Governance decides **what may be permitted, constrained, or denied**.

---

## **2. Core Principles**

1. **Non-overlap**
    - Governance must not reinterpret Judgement outcomes.
    - Governance must not access Reasoning outputs directly (v1).
2. **Epistemic Respect**
    - Governance must honor epistemic limits embedded in Judgement decisions.
3. **Boundedness**
    - Governance outcomes are constrained to a fixed enum.
    - No prose, no suggestions, no actions.
4. **Determinism**
    - Same Judgement input + same policy → same Governance outcome.
5. **Fail-closed**
    - Contract violations result in denial or hard failure (policy-defined).

---

## **3. Hard Constraints**

### **3.1 What Governance MAY Consume**

Governance may consume **only**:

1. JudgementDecision
2. GovernanceContextEnvelope
3. GovernanceIntent
4. ActionIntent (conditional)
5. Policy, tier, and posture **by version reference only**

### **3.2 What Governance MUST NOT Consume**

Governance must not consume:

- Reasoning findings
- raw user text
- UI state
- free-form LLM output
- suggested actions or explanations
- canonical project data

---

## **4. Governance Request Envelope**

*(unchanged)*

---

## **5. GovernanceContextEnvelope**

*(unchanged)*

---

## **6. GovernanceIntent**

*(unchanged)*

---

## **7. JudgementDecision (Required)**

Governance consumes a **bounded, epistemically qualified** JudgementDecision.

```
{
  "judgement_decision": {
    "decision_id": "string",
    "decision_type": "ACCEPT|WARN|BLOCK|DEFER|SUPPRESS",
    "severity": "INFO|LOW|MEDIUM|HIGH|CRITICAL",
    "confidence": 0.0,

    "epistemic_basis":
      "COMMITTED_FACT|
       ASSERTED_FACT|
       ASSUMPTION|
       ESTIMATE|
       INFERENCE|
       MIXED",

    "evidence_refs": ["string"],
    "lifecycle_scope": "INITIATION|PLANNING|EXECUTION|MONITORING|CLOSURE",

    "expiry_conditions": [
      {
        "type": "TIME_WINDOW|ON_EVIDENCE_CHANGE|ON_LIFECYCLE_TRANSITION",
        "value": "string"
      }
    ],

    "suppression_reason": "TIER_GATING|LIFECYCLE_MISMATCH|COGNITIVE_LOAD|POLICY_VISIBILITY|null",
    "dominant_finding_ids": ["string"],
    "created_at_utc": "RFC3339"
  }
}
```

### **Judgement Constraints**

- epistemic_basis is **required**
- confidence ∈ [0.0, 1.0]
- If decision_type ≠ ACCEPT → evidence_refs must be non-empty
- Governance must not modify or reinterpret this object

---

## **8. ActionIntent**

*(unchanged)*

---

## **9. GovernanceOutcome**

*(unchanged)*

---

## **10. Interpretation Rules (Normative)**

### **10.1 No Re-decision**

Governance must not:

- change decision_type
- reinterpret severity or confidence
- upgrade epistemic authority
- re-evaluate evidence meaning
- fetch Reasoning data

---

### **10.2 Epistemic Gating (Mandatory)**

If:

- judgement_decision.epistemic_basis ∈ {ASSUMPTION, ESTIMATE, INFERENCE}
- and intent implies mutation, lifecycle transition, or external effect

→ Governance **must not auto-permit or auto-deny**

→ Governance must return **REQUIRE_APPROVAL** or **DOWNGRADE**, per policy.

---

### **10.3 Lifecycle Transition Gating (Revised)**

If:

- intent_type = LIFECYCLE_TRANSITION
- decision_type = BLOCK
- epistemic_basis = COMMITTED_FACT

→ DENY (unless explicit override policy exists).

If epistemic_basis ≠ COMMITTED_FACT:

→ REQUIRE_APPROVAL or DOWNGRADE (policy-driven).

---

### **10.4 Visibility & Redaction**

*(unchanged)*

---

### **10.5 Posture Enforcement**

*(unchanged)*

---

### **10.6 High-Risk Actions**

*(unchanged, but epistemic gating applies first)*

---

### **10.7 Precedence (Most-Restrictive Wins)**

*(unchanged)*

---

## **11. Validation Rules**

Additions:

- Missing epistemic_basis → GOV_ERR_EPISTEMIC_MISSING
- Enforcement attempt on weak epistemic basis → GOV_ERR_EPISTEMIC_VIOLATION

Existing rules unchanged.

---

## **12. Audit Requirements**

Audit records must additionally include:

- epistemic_basis
- whether outcome was epistemically constrained

---

## **13. Acceptance Criteria**

This contract is satisfied only if:

1. Governance never enforces on weak belief
2. Epistemic limits are respected deterministically
3. Judgement authority is preserved, not amplified
4. Enforcement decisions are explainable and auditable

---

## **3. Why this is non-optional**

Without these changes:

- Governance can **silently over-enforce**
- Users experience “AI said no” without recourse
- Your epistemic discipline collapses at the last mile

With these changes:

- Authority scales correctly with certainty
- Governance remains policy-pure
- OSLO behaves like a **trustworthy system**, not an overconfident one

---

##