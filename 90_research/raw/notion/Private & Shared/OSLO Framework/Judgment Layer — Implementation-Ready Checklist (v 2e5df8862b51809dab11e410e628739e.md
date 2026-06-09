# Judgment Layer — Implementation-Ready Checklist (v1.1) - Update 1/15

---

**System:** OSLO

**Layer:** Judgment

**Audience:** Lead Engineer, QA

**Goal:** Build a deterministic, bounded, auditable Judgment Layer that converts Reasoning detections into decisions **without upgrading belief, fabricating facts, or enforcing on weak epistemic ground**.

---

## **1) Contracts and Schemas**

☐ **Lock the Judgment output schema (JudgmentDecision)**

- Required:
    - decision_type
    - severity
    - confidence
    - evidence_refs
    - lifecycle_scope
    - **epistemic_basis**
- Optional:
    - expiry_conditions
    - suppression_reason
    - dominant_finding_ids

☐ **Lock enums**

- decision_type: ACCEPT | WARN | BLOCK | DEFER | SUPPRESS
- severity: INFO | LOW | MEDIUM | HIGH | CRITICAL
- suppression_reason: TIER_GATING | LIFECYCLE_MISMATCH | COGNITIVE_LOAD | POLICY_VISIBILITY | OTHER
- **epistemic_basis:**
    - COMMITTED_FACT
    - ASSERTED_FACT
    - ASSUMPTION
    - ESTIMATE
    - INFERENCE
    - MIXED

☐ **Strict parsing**

- Unknown fields in inputs or outputs → **hard fail**, not best effort
- Missing epistemic fields → **hard fail**

---

## **2) Entrypoint and Purity**

☐ **Implement a single pure entrypoint**

```
evaluateJudgment(reasoningPayload, judgmentContext) => JudgmentDecision
```

- No DB writes
- No network calls
- No randomness
- No reading global mutable state

☐ **No side effects**

- Logging allowed but must not influence output

---

## **3) Input Contract Enforcement**

☐ **Consume only the canonical Reasoning payload**

- ContextEnvelope
- ReasoningRunHeader
- Findings[]
- EvidenceIndex

☐ **Require epistemic completeness**

- Every Finding MUST include epistemic_basis
- Every evidence_ref MUST resolve to an epistemically typed EvidenceIndex entry

☐ **Require explicit context (no inference)**

- lifecycle_stage
- mode/pass
- tier
- policy_version
- reasoning_ruleset_version

☐ **Reject upstream invalidity**

- If reasoning_run.status != SUCCESS →
    - **Option A (recommended):** hard error J_ERR_UPSTREAM_RUN_FAILED
    - **Option B:** deterministic DEFER referencing upstream failure

☐ **Forbidden inputs rejected**

- raw user text
- free-form LLM output
- UI flags/state
- “recommended actions”

---

## **4) Invariants (Enforced in Code)**

☐ **Determinism**

- Same input payload → identical output (byte-for-byte)

☐ **No epistemic promotion**

- Judgment must never upgrade epistemic_basis
- INFERENCE / ASSUMPTION / ESTIMATE cannot become COMMITTED_FACT

☐ **No fabrication**

- Judgment cannot create facts, assumptions, or inferences

☐ **Bounded outputs**

- decision_type and severity ∈ enums
- confidence ∈ [0.0, 1.0]

☐ **Evidence anchoring**

- decision_type != ACCEPT → evidence_refs required
- All evidence_refs must resolve

☐ **Lifecycle awareness**

- Decision behavior varies by lifecycle stage via explicit tables

---

## **5) Decision Policy Implementation**

☐ **Implement a policy table (mandatory)**

Mapping inputs:

```
(lifecycle_stage,
 finding_type,
 severity,
 epistemic_basis,
 sufficiency,
 tier)
→ decision_type
```

☐ **Epistemic guardrails (mandatory)**

- Findings with epistemic_basis ∈ {ASSUMPTION, ESTIMATE, INFERENCE}
    
    → **cannot produce BLOCK**
    
    → default to DEFER or WARN unless explicitly allowed
    
- Only COMMITTED_FACT may escalate to enforcement-grade BLOCK

☐ **Deterministic dominance/tie-break**

1. BLOCK candidates (epistemically valid only)
2. DEFER (insufficient or weak epistemic basis)
3. WARN
4. ACCEPT

☐ **Lifecycle bias rules enforced**

- INITIATION → bias DEFER
- PLANNING → BLOCK allowed for structural gaps
- EXECUTION → BLOCK allowed for committed feasibility violations
- MONITORING → WARN unless committed drift
- CLOSURE → suppress non-impacting issues

☐ **Data sufficiency classifier**

- Missing evidence or weak epistemic_basis → insufficient
- Insufficient → DEFER (unless policy table overrides)

---

## **6) Severity Handling**

☐ **Severity ≠ authority**

- Severity does not override epistemic weakness

☐ **Severity sourcing is deterministic**

- Derived from dominant finding or fixed aggregation rule
- No heuristic adjustments

---

## **7) Suppression (First-Class Outcome)**

☐ **SUPPRESS requires suppression_reason**

☐ **Suppression does not erase epistemic record**

- evidence_refs preserved
- dominant_finding_ids preserved

---

## **8) Expiry and Re-evaluation**

☐ **Expiry is epistemically consistent**

- Expiry conditions must not imply belief promotion

☐ **Expiry types**

- TIME_WINDOW
- ON_EVIDENCE_CHANGE
- ON_LIFECYCLE_TRANSITION

---

## **9) Observability and Audit**

☐ **Emit audit record per evaluation**

Must include:

- input_hash
- lifecycle_stage, mode, tier
- decision_type, severity, confidence
- **epistemic_basis**
- evidence_refs
- dominant_finding_ids
- judgment_policy_version

☐ **Replay guarantee**

- Same reasoning payload + policy version → identical decision

---

## **10) Error Handling**

☐ **Define and enforce error codes**

Additions:

- J_ERR_EPISTEMIC_MISSING
- J_ERR_EPISTEMIC_VIOLATION

Existing:

- J_ERR_MISSING_CONTEXT
- J_ERR_INVALID_ENUM
- J_ERR_EVIDENCE_INTEGRITY
- J_ERR_UPSTREAM_RUN_FAILED
- J_ERR_SCHEMA_VIOLATION

---

## **11) Test Suite (Implementation-Ready)**

☐ **Epistemic tests (new, mandatory)**

- Inference-only finding → never BLOCK
- Same severity, different epistemic_basis → different decisions
- Attempted epistemic promotion → hard fail

☐ **Determinism tests**

- N runs → identical output

☐ **Lifecycle tests**

- Same findings, different lifecycle → policy-correct differences

☐ **Negative tests**

- Missing epistemic_basis → J_ERR_EPISTEMIC_MISSING
- Enforcement on assumption → J_ERR_EPISTEMIC_VIOLATION

---

## **12) Out of Scope (v1)**

☐ Natural-language explanations

☐ Permissions enforcement

☐ Actions or mutations

☐ Learning loops

---

## **“Done” Gate**

> Judgment is complete only if it can
> 
> 
> **never**
> 

> never
> 

> and
> 
> 
> **always**
> 

---

### **Why this matters (one sentence)**

This checklist ensures **Judgment authority scales with belief strength**, not model confidence — which is the single biggest difference between a trustworthy orchestration system and an overconfident one.

---

##