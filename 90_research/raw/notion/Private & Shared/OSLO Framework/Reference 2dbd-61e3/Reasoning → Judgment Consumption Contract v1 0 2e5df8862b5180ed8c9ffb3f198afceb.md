# Reasoning → Judgment Consumption Contract v1.0

**System:** OSLO

**From Layer:** Reasoning

**To Layer:** Judgment

**Spec Type:** Normative (schema + constraints)

**Audience:** Engineering, AI/ML, QA

**Status:** Canonical

---

## **1. Purpose**

This contract defines the **only** data structures and guarantees the Judgment Layer may consume from the Reasoning Layer, and the **obligations** Reasoning must meet so Judgment can be:

- deterministic
- auditable
- bounded (non-generative)
- lifecycle-aware

Judgment must treat any Reasoning output that violates this contract as **invalid**.

---

## **2. Core Principle**

Reasoning produces **findings** (deterministic assessments).

Judgment produces **decisions** (bounded outcomes) based on those findings.

Reasoning must be **explainable via evidence references**.

Judgment must be **anchored to those evidence references**.

---

## **3. Hard Constraints**

### **3.1 What Judgment May Consume**

Judgment may consume only:

1. ReasoningRunHeader
2. Finding[]
3. EvidenceIndex
4. ContextEnvelope (lifecycle/mode/tier passed through, not inferred)

### **3.2 What Judgment Must Not Consume**

Judgment must not consume:

- raw user text
- free-form LLM completions
- UI state
- system prompts
- “recommendations” or suggested actions
- any non-canonical fields or vendor-specific metadata

---

## **4. Context Envelope**

Reasoning must emit a **ContextEnvelope** that is carried into Judgment unchanged.

```
{
  "context": {
    "project_id": "string",
    "run_id": "string",
    "timestamp_utc": "RFC3339",
    "lifecycle_stage": "INITIATION|PLANNING|EXECUTION|MONITORING|CLOSURE",
    "mode": "PASS_1_STRUCTURAL|PASS_2_INFERENTIAL|CONTINUOUS",
    "tier": "FREE|PRO|TEAMS|ENTERPRISE",
    "policy_version": "string",
    "reasoning_ruleset_version": "string"
  }
}
```

### **Requirements**

- lifecycle_stage is **required** and must be explicit.
- mode is **required** and must be explicit.
- tier is **required** and must be explicit.
- No field in context may be inferred by Judgment.

---

## **5. Reasoning Run Header**

```
{
  "reasoning_run": {
    "run_id": "string",
    "input_hash": "string",
    "determinism_key": "string",
    "started_at_utc": "RFC3339",
    "completed_at_utc": "RFC3339",
    "status": "SUCCESS|FAILED_VALIDATION|FAILED_EXECUTION",
    "error_code": "string|null"
  }
}
```

### **Requirements**

- input_hash must be reproducible for identical canonical inputs.
- determinism_key must uniquely identify the ruleset + config that produced the outputs.
- If status != SUCCESS, findings must be empty and error_code must be present.

---

## **6. Finding Schema**

Reasoning outputs are a list of canonical findings. Each finding is a **typed, bounded object**.

```
{
  "finding": {
    "finding_id": "string",
    "finding_type": "STRUCTURE_GAP|SMART_GAP|CONTENT_QUALITY_GAP|ALIGNMENT_GAP|FEASIBILITY_RISK|DRIFT_SIGNAL|CONFLICT|INCONSISTENCY|MISSING_EVIDENCE",
    "domain": "CHARTER|SCOPE|REQUIREMENTS|WBS|RESOURCE_PLAN|SCHEDULE|CROSS_ARTIFACT",
    "target_ref": {
      "artifact": "string",
      "element_path": "string",
      "element_id": "string|null"
    },
    "severity": "INFO|LOW|MEDIUM|HIGH|CRITICAL",
    "confidence": 0.0,
    "status": "OPEN|RESOLVED|SUPPRESSED",
    "evidence_refs": ["evidence_id"],
    "summary_code": "string",
    "parameters": {
      "key": "value"
    },
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

### **Finding Requirements (Normative)**

- finding_type must be from the allowed enum only.
- severity must be from the allowed enum only.
- confidence must be in [0.0, 1.0].
- evidence_refs must be non-empty for all findings with severity != INFO.
- summary_code must be a stable code (no prose) suitable for downstream mapping.
- parameters must be JSON-serializable primitives/arrays/objects (no functions, no text blobs).
- status is informational to Judgment; **Judgment decides what to do**.

---

## **7. Evidence Index**

Reasoning must emit an Evidence Index that is **referentially complete**.

```
{
  "evidence_index": {
    "evidence_id": {
      "evidence_type": "CANON_FACT|CANON_INFERENCE|DERIVED_METRIC|RULE_TRACE",
      "source_ref": "string",
      "canonical_path": "string",
      "snapshot_hash": "string",
      "captured_at_utc": "RFC3339"
    }
  }
}
```

### **Evidence Requirements**

- Every evidence_ref in every Finding must exist in evidence_index.
- Evidence must reference **canonical** data locations, not UI locations.
- Evidence must be immutable for the duration of the run (snapshot semantics).

---

## **8. Determinism Guarantees (Reasoning Obligations)**

Reasoning must provide the following guarantees:

1. **Stable ordering**
    - Findings must be emitted in a deterministic order:
        
        domain → target_ref.element_path → severity → finding_type → finding_id
        
2. **Stable IDs**
    - finding_id must be deterministic (e.g., hash of {type, target_ref, summary_code, key parameters, ruleset_version}).
3. **No prose**
    - Reasoning outputs must not include natural-language explanation fields intended for UI.
4. **No action suggestions**
    - Reasoning does not instruct; it detects and classifies.

If any determinism guarantee is violated, Judgment must treat the run as invalid.

---

## **9. Judgment Consumption Rules (Must Implement)**

Judgment must:

- Validate all enums and required fields
- Validate evidence referential integrity
- Reject non-canonical/unknown fields (strict parsing)
- Enforce “no missing context”
- Refuse to evaluate if reasoning_run.status != SUCCESS

Judgment must not:

- re-run Reasoning
- fetch raw data outside the evidence index
- invent a severity mapping different from the contract (unless explicitly configured)

---

## **10. Error Handling Contract**

### **10.1 Reasoning → Judgment Failure Modes**

| **Condition** | **Required Behavior** |
| --- | --- |
| status != SUCCESS | Judgment returns DEFER with evidence referencing the run error (or errors out if contract requires hard fail) |
| Missing evidence ref | Judgment errors J_ERR_EVIDENCE_INTEGRITY |
| Unknown finding_type | Judgment errors J_ERR_INVALID_FINDING_TYPE |
| Missing lifecycle/mode/tier | Judgment errors J_ERR_MISSING_CONTEXT |

> Recommended v1 posture:
> 
> 
> **fail hard on contract violations**
> 

---

## **11. Supersession & Retention Fields**

Reasoning must support supersession without deleting history:

- supersedes[] points to replaced finding IDs
- Findings are never mutated in-place across runs
- New run emits new findings and explicit supersession links

Judgment may use supersedes to:

- prefer the most recent applicable finding
- ignore stale findings deterministically

---

## **12. Minimal Working Example (Valid Payload)**

At minimum, a valid payload contains:

- context
- reasoning_run (SUCCESS)
- findings (possibly empty)
- evidence_index (possibly empty if findings empty)

---

## **13. Acceptance Tests (Contract-Level)**

The integration passes only if:

1. Judgment can validate and parse the payload strictly
2. Every finding evidence ref resolves
3. Findings order is deterministic across identical inputs
4. Removing any required context field causes validation failure
5. Reasoning never emits prose or action suggestions

---

If you want, I can also produce:

- **JSON Schema files** for ReasoningPayload and Finding
- A **contract conformance test harness** (unit + property tests)
- The complementary **Judgment → Governance Consumption Contract**