# Reasoning Layer — Engineer Start Here

---

**System:** OSLO / Intralign

**Layer:** Reasoning

**Status:** Canonical

**Audience:** Engineering (Backend, Platform, AI/ML), QA

**Purpose:** Enable correct, deterministic implementation of the Reasoning Layer without architectural guesswork.

---

## **1. What the Reasoning Layer Is (In One Sentence)**

The Reasoning Layer evaluates **structural truth** in project data by detecting gaps, conflicts, and fragility—**without making decisions, scores, or recommendations**.

It answers:

> “Given the current project data, what is structurally true, incomplete, inconsistent, or fragile?”
> 

Nothing more.

---

## **2. What the Reasoning Layer Is NOT**

Reasoning **does not**:

- score health
- interpret severity
- decide acceptability
- recommend actions
- communicate with users
- mutate canonical knowledge
- enforce governance

If you are about to do any of the above, you are in the **wrong layer**.

---

## **3. Inputs (Authoritative)**

Reasoning operates on **read-only inputs only**.

### **3.1 Canonical Knowledge (Primary Input)**

From the **Knowledge Layer**:

- canonical entities
- canonical relationships
- constraints
- artifact containers
- assumptions and context signals

Rules:

- inputs are immutable
- reasoning never writes back
- inferred data is never promoted to canonical

---

### **3.2 Execution Context**

Every reasoning run includes a context object:

```
ReasoningContext:
  mode: canonical | hypothetical
  trigger: onboarding | recompute | whatif | 60second
```

Rules:

- **canonical** and **hypothetical** runs are fully isolated
- no cross-contamination of results
- outputs are tagged with context

---

## **4. Core Outputs (What You Must Produce)**

Reasoning produces **semantic artifacts**, not language.

### **4.1 Issues**

Structural deficiencies detected in the data.

```
Issue:
  issue_id
  type: clarity | alignment | feasibility
  subtype
  affected_elements[]
  evidence_chain_id
```

Rules:

- issues are structural, not advisory
- every issue must be reproducible
- no severity, score, or recommendation here

---

### **4.2 Inferred Elements & Synthetic Placeholders**

Used only to enable structural evaluation.

```
InferredElement:
  element_id
  inferred_value
  value_type: derived | synthetic_placeholder
  inference_reason
  certainty_band: low | medium | high
  epistemic_state: proposed
  evidence_chain_id
```

Rules:

- placeholders are **simulation scaffolding**
- must be explicitly labeled
- never promoted without UI authorization
- may influence signals, never facts

---

### **4.3 Raw Structural Signals**

Uninterpreted indicators for Judgment.

Examples:

- dependency tension
- schedule compression
- assumption density
- load pressure

Rules:

- no scoring
- no normalization
- Judgment owns interpretation

---

### **4.4 Evidence Chains (Mandatory)**

Every output must trace back to inputs.

```
EvidenceChain:
  chain_id
  input_snapshot_ids[]
  rules_applied[]
  assumptions_made[]
  placeholders_used[]
  limitations[]
  rule_version
```

If an output cannot produce an evidence chain, **it must not exist**.

---

## **5. Rule Execution Model (High-Level)**

Reasoning runs in **explicit passes**:

### **Pass 1 — Explicit Capture**

- no inference
- no placeholders
- snapshot canonical data

### **Pass 2 — Structural Completion**

- introduce inferred elements if required
- tag everything as proposed

### **Pass 3 — Structural Evaluation**

- detect issues
- emit raw signals
- generate evidence chains

### **Pass 4 — Incremental Recompute**

- re-evaluate only impacted structures
- requires authorized input changes

Rules:

- same inputs + same rules = same outputs
- rule order is deterministic
- no rule may suppress another rule’s output

---

## **6. Rule Definitions (Externalized)**

All reasoning logic lives in **external rule definition files**.

- loaded at startup
- versioned
- immutable once canonical
- explainable

The engine executes rules — it does not define them.

---

## **7. Persistence & Replay**

Reasoning outputs:

- **may be persisted** as derived artifacts
- must reference exact input snapshots
- must be replayable for audit
- are superseded, never deleted

Reasoning outputs are **truth claims at a point in time**, not permanent facts.

---

## **8. Determinism Guarantees**

Engineering must ensure:

- deterministic rule execution
- rule version pinning per run
- no hidden state
- bounded AI inference
- reproducible evidence chains

Non-deterministic behavior is a **defect**, not a feature.

---

## **9. Boundaries With Other Layers**

### **Reasoning produces**

- issues
- inferred elements (proposed)
- raw signals
- evidence chains

### **Judgment**

- scores
- severity interpretation
- confidence adjustments

### **Governance**

- whether outputs surface
- suppression vs exposure
- authorization

### **Communication**

- explanation
- phrasing
- guidance

---

## **10. Common Implementation Errors (Avoid These)**

- ❌ adding severity in Reasoning
- ❌ mutating canonical data
- ❌ inventing outcomes or goals
- ❌ suppressing issues
- ❌ generating prose
- ❌ skipping evidence chains

If you feel tempted to do any of these, stop.

---

## **11. Implementation Checklist**

Before shipping Reasoning, confirm:

- all inputs are read-only
- all outputs have evidence chains
- inferred elements are explicitly labeled
- hypothetical runs are isolated
- outputs are deterministic
- no scoring logic exists
- no canonical mutation occurs

---

## **Canonical Close**

> Reasoning exists to make structure visible—
> 

> even when that structure rests on assumptions.
> 

> 
> 

> It simulates reality honestly.
> 

> Judgment decides what to do with it.
> 

---