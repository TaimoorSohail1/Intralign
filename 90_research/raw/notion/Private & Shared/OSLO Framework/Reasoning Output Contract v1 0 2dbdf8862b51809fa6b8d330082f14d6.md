# Reasoning Output Contract v1.0

---

**System:** OSLO / Intralign

**Layer:** Reasoning

**Spec Type:** Normative (output schema + guarantees)

**Status:** Canonical

**Audience:** Engineering, Platform, QA, Downstream Layer Owners (Judgment, Governance)

---

## **1. Purpose**

This contract defines the **only valid outputs** the Reasoning Layer may emit.

It establishes:

- output structure
- determinism guarantees
- replay & audit requirements
- hard boundaries with Judgment, Governance, and Communication

Anything not defined here **must not be produced** by Reasoning.

---

## **2. Output Envelope (Required)**

Every reasoning run produces exactly **one envelope**.

```
ReasoningOutput:
  reasoning_run_id: uuid
  generated_at: datetime
  context:
    mode: canonical | hypothetical
    trigger: onboarding | recompute | whatif | 60second
  inputs:
    input_snapshot_ids: uuid[]
    knowledge_version_refs: string[]
  rule_context:
    rule_bundle_id: string
    rule_versions: string[]
  outputs:
    issues: Issue[]
    inferred_elements: InferredElement[]
    raw_signals: RawSignal[]
    evidence_chains: EvidenceChain[]
  guarantees:
    deterministic: true
    replayable: true
```

---

## **3. Issue Output (Structural Deficiencies)**

```
Issue:
  issue_id: uuid
  type: clarity | alignment | feasibility
  subtype: string
  affected_elements:
    - entity_type: string
      entity_id: uuid
  evidence_chain_id: uuid
```

### **Rules**

- Issues are **structural**, not advisory
- No severity, score, confidence, or recommendation
- Every issue **must** reference an EvidenceChain
- Issues may not suppress or override one another

---

## **4. Inferred Elements & Synthetic Placeholders**

```
InferredElement:
  element_id: uuid
  entity_type: string
  inferred_value: any
  value_type: derived | synthetic_placeholder
  inference_reason: string
  certainty_band: low | medium | high
  epistemic_state: proposed
  evidence_chain_id: uuid
```

### **Rules**

- Used only to enable structural evaluation
- Must be explicitly labeled as **proposed**
- Must never mutate canonical knowledge
- Must never be promoted without UI authorization (Governance)
- May influence structural signals but not facts

---

## **5. Raw Structural Signals (Judgment Inputs)**

```
RawSignal:
  signal_id: uuid
  signal_type: string
  scope:
    entity_type: string
    entity_id: uuid
  value: number | string | object
  evidence_chain_id: uuid
```

### **Rules**

- Signals are **unscored and uninterpreted**
- No normalization or thresholding
- Judgment owns interpretation and scoring
- Signals must be reproducible

---

## **6. Evidence Chains (Foundational Primitive)**

Every output object must reference **exactly one** evidence chain.

```
EvidenceChain:
  chain_id: uuid
  input_snapshot_ids: uuid[]
  rules_applied: string[]
  assumptions_made: string[]
  placeholders_used: uuid[]
  limitations: string[]
  rule_version: string
```

### **Rules**

- Evidence chains are mandatory
- Chains must be replayable
- Chains must reference **exact input snapshots**
- No output may exist without a chain

---

## **7. Input Snapshot Guarantees**

- Input snapshots are immutable
- Each snapshot references a specific Knowledge Layer state
- Snapshots are sufficient to replay reasoning deterministically

---

## **8. Determinism Guarantees**

Given:

- identical input snapshots
- identical rule versions
- identical execution context

The Reasoning Layer **must produce identical outputs**.

Any non-determinism is a **defect**.

---

## **9. Persistence Rules**

Reasoning outputs:

- may be persisted as **derived artifacts**
- must be superseded, not deleted
- must retain historical versions for audit
- must remain replayable even after rule evolution

---

## **10. Explicit Non-Responsibilities**

Reasoning outputs must **never** include:

- severity
- health scores
- confidence adjustments
- recommendations
- remediation steps
- UI copy
- governance decisions

Those belong to downstream layers.

---

## **11. Validation & Compliance**

A Reasoning implementation is compliant if:

- all outputs match this schema
- all outputs have evidence chains
- no canonical mutation occurs
- determinism guarantees hold
- hypothetical and canonical contexts remain isolated

---

## **Canonical Invariant**

> Reasoning outputs are
> 
> 
> **truth claims about structure at a point in time**
> 

> 
> 

> They are not decisions.
> 

> They are not advice.
> 

> They exist to enable judgment.
> 

---

If you want next, I can:

- align this contract explicitly with the **Judgment input contract**
- produce a **Reasoning ↔ Judgment handoff schema**
- draft a **determinism & replay test suite**
- generate a **CI validation checklist**