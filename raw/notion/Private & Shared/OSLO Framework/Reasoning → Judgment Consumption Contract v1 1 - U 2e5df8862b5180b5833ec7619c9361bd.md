# Reasoning → Judgment Consumption Contract v1.1 - Update 1/15

---

**System:** OSLO

**From Layer:** Reasoning

**To Layer:** Judgment

**Spec Type:** Normative (schema + constraints)

**Audience:** Engineering, AI/ML, QA

**Status:** Canonical

---

## **1. Purpose**

This contract defines the **only permissible interface** between the Reasoning and Judgment layers.

Its goals are to ensure that Judgment is:

- deterministic
- bounded (non-generative)
- auditable
- lifecycle-aware
- epistemically constrained

Judgment must treat Reasoning output as **authoritative detections**,

not authoritative truth.

---

## **2. Core Principle**

- **Reasoning** detects, classifies, and evidences conditions *relative to a snapshot*.
- **Judgment** decides posture and outcome *based on detected conditions and their epistemic strength*.

Reasoning answers: *“What conditions were detected, and why?”*

Judgment answers: *“What action posture is appropriate given belief strength?”*

No overlap. No reprocessing.

---

## **3. Hard Constraints**

### **3.1 What Judgment May Consume**

Judgment may consume **only**:

1. ContextEnvelope
2. ReasoningRunHeader
3. Finding[]
4. EvidenceIndex

### **3.2 What Judgment Must Not Consume**

Judgment must not consume:

- raw user text
- free-form LLM completions
- UI state
- policy definitions
- suggested actions or prose explanations
- non-canonical or undocumented fields

Violation = hard failure.

---

## **4. ContextEnvelope (Required)**

*(unchanged)*

---

## **5. ReasoningRunHeader (Required)**

*(unchanged)*

---

## **6. Finding Schema (Core Payload)**

```
{
  "finding": {
    "finding_id": "string",

    "finding_type":
      "STRUCTURE_GAP|
       CONTENT_QUALITY_GAP|
       SMART_GAP|
       ALIGNMENT_GAP|
       FEASIBILITY_RISK|
       DRIFT_SIGNAL|
       CONFLICT|
       INCONSISTENCY|
       MISSING_EVIDENCE",

    "domain":
      "CHARTER|
       SCOPE|
       REQUIREMENTS|
       WBS|
       RESOURCE_PLAN|
       SCHEDULE|
       CROSS_ARTIFACT",

    "target_ref": {
      "artifact": "string",
      "element_path": "string",
      "element_id": "string|null"
    },

    "severity": "INFO|LOW|MEDIUM|HIGH|CRITICAL",

    "confidence": 0.0,

    "epistemic_basis":
      "COMMITTED_FACT|
       ASSERTED_FACT|
       ASSUMPTION|
       ESTIMATE|
       INFERENCE|
       MIXED",

    "status": "OPEN|RESOLVED|SUPPRESSED",

    "evidence_refs": ["evidence_id"],

    "summary_code": "string",

    "parameters": { "key": "value" },

    "supersedes": ["finding_id"],

    "created_at_utc": "RFC3339",

    "expiry_conditions": [
      {
        "type": "TIME_WINDOW|ON_EVIDENCE_CHANGE|ON_LIFECYCLE_TRANSITION",
        "value": "string"
      }
    ]
  }
}
```

### **Finding Constraints (Normative)**

- epistemic_basis is **required**
- Severity ≠ certainty
- Findings based solely on assumptions or estimates MUST NOT escalate directly to enforcement outcomes
- Confidence ∈ [0.0, 1.0]
- evidence_refs required unless severity == INFO
- summary_code must be symbolic (not prose)
- Findings must be deterministically ordered

---

## **7. EvidenceIndex (Required)**

```
{
  "evidence_index": {
    "evidence_id": {
      "evidence_type":
        "COMMITTED_CANON|
         ASSERTED_CANON|
         CANON_ASSUMPTION|
         CANON_ESTIMATE|
         CANON_INFERENCE|
         DERIVED_METRIC|
         RULE_TRACE",

      "canonical_path": "string",
      "snapshot_hash": "string",
      "captured_at_utc": "RFC3339"
    }
  }
}
```

### **Constraints**

- Evidence MUST declare epistemic type
- Judgment must be able to distinguish belief strength
- Evidence is immutable per run

---

## **8. Determinism Guarantees (Reasoning Obligations)**

*(ordering & ID rules unchanged)*

Additional obligation:

- Reasoning must compute epistemic_basis deterministically from evidence types

---

## **9. Judgment Consumption Rules (Must Implement)**

Judgment must:

- Validate schema strictly
- Validate epistemic completeness
- Weight decisions by epistemic_basis
- Reject enforcement on non-committed evidence
- Enforce lifecycle-specific behavior

Judgment must not:

- reinterpret epistemic basis
- upgrade belief strength
- collapse confidence into certainty
- invent missing evidence

---

## **10. Error Handling Contract**

Add:

| **Condition** | **Required Judgment Behavior** |
| --- | --- |
| Missing epistemic_basis | J_ERR_EPISTEMIC_MISSING |
| Enforcement on assumption | J_ERR_EPISTEMIC_VIOLATION |

---

## **11. Supersession & Retention**

*(unchanged)*

---

## **12. Acceptance Criteria**

This contract is satisfied only if:

1. Judgment receives epistemic context explicitly
2. Decisions differ when evidence strength differs
3. Identical inputs yield identical outputs
4. Inferred risk cannot masquerade as committed violation

---

## **Canonical Close**

> Reasoning detects conditions.
> 

> 
> 

> Judgment decides posture.
> 

> 
> 

> Epistemic strength determines authority.
> 

---

## **3. Why this change is non-optional**

Without this revision:

- You **reintroduce certainty inflation** at the most dangerous point
- Governance will enforce on inferred structure
- Users will feel “AI overreach” even when the system is behaving correctly

With this revision:

- Judgment becomes **belief-aware**, not just rule-aware
- Drift, risk, and gaps become explainable
- Enforcement becomes defensible
- Your system stays epistemically honest end-to-end

---

##