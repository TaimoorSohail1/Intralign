# OSLO Evidence Chain Integrity Contract (v1.0)

**Layer Authority:** Knowledge (storage), Reasoning (proposal), Judgment (validation), Governance (enforcement)

**Determinism Level:** STRICT

**Scope:** All assertions promoted into the Knowledge Layer

---

# **1. Purpose**

To guarantee that:

- Every promoted assertion is traceable to immutable raw evidence
- No claim exists without provenance
- Evidence cannot silently break
- Replay preserves semantic traceability
- Governance can audit any decision at any time

This contract ensures **Outcome Integrity is evidence-bound**, not narrative-bound.

---

# **2. Core Principle**

> No authoritative assertion may exist without a resolvable evidence chain.
> 

An assertion without evidence must be explicitly labeled and governed.

---

# **3. Evidence Chain Model**

An evidence chain consists of:

```
Assertion
   ↓
Evidence Reference
   ↓
Knowledge Projection Node
   ↓
raw_record_id
   ↓
Immutable Raw Record
```

Each link must be resolvable and version-stable.

---

# **4. Assertion Requirements (Mandatory Fields)**

Every promoted assertion must contain:

| **Field** | **Required** | **Description** |
| --- | --- | --- |
| assertion_id | YES | Stable UUID |
| assertion_type | YES | e.g., FACT, INFERENCE, ASSUMPTION, RISK, SIGNAL |
| epistemic_status | YES | CONFIRMED / DERIVED / CANDIDATE |
| evidence_refs[] | YES* | At least one unless explicitly allowed |
| created_by_layer | YES | Reasoning / Judgment |
| created_at | YES | ISO timestamp |
| schema_version | YES | Projection schema version |
| assertion_hash | YES | Canonicalized structured hash |
- If empty, see Section 8 (Unsupported Assertions).

---

# **5. Evidence Reference Structure**

Each evidence reference must include:

```
{
  raw_record_id: string,
  projection_node_id: string,
  span_locator: optional,
  timestamp_bundle: {
      event_occurred_at,
      source_recorded_at,
      oslo_ingested_at
  }
}
```

### **span_locator (if applicable)**

Used for emails, transcripts, chat messages.

May include:

- character offsets
- paragraph index
- transcript segment ID
- structured field reference (e.g., CRM.stage)

This allows precise evidence replay.

---

# **6. Evidence Validity Rules**

An assertion is valid only if:

1. Every raw_record_id resolves to an immutable raw record
2. The projection node exists
3. The raw record has not been tombstoned
4. The span_locator (if present) resolves correctly
5. The timestamp bundle matches stored raw record

Failure of any rule triggers Evidence Chain Invalid state.

---

# **7. Epistemic Classification Rules**

OSLO enforces strict classification:

| **Type** | **Evidence Required** | **Promotion Allowed** |
| --- | --- | --- |
| FACT | Yes | Yes |
| DERIVED (inference) | Yes (traceable inputs) | Yes |
| ASSUMPTION | Optional | Only with governance approval |
| CANDIDATE | Yes | Not authoritative |

No assertion may be silently upgraded.

Epistemic state transitions require Governance approval.

---

# **8. Unsupported Assertions (Edge Case Handling)**

If Reasoning produces an assertion without resolvable evidence:

It must be tagged:

```
epistemic_status = UNSUPPORTED
```

Governance options:

- Reject
- Request additional context
- Promote as ASSUMPTION (explicitly visible)
- Defer

Unsupported assertions may never be silently promoted.

---

# **9. Broken Evidence Handling**

If a raw record is removed (e.g., revoked API access, user disconnects CRM):

The system must:

1. Mark affected assertions as EVIDENCE_STALE
2. Prevent them from being used in new reasoning cycles
3. Surface impact report
4. Queue Governance review

Authoritative state must not rely on missing evidence.

---

# **10. Replay Integrity Rule**

On replay:

- All evidence chains must resolve identically
- All assertion hashes must match
- Any mismatch triggers determinism violation

If evidence structure differs:

→ block promotion

→ escalate audit

---

# **11. Canonicalization of Assertions**

Before storing:

1. Sort JSON keys
2. Normalize whitespace
3. Normalize timestamps
4. Validate epistemic status
5. Validate evidence structure
6. Compute assertion_hash (SHA-256)

Only canonicalized assertion structures are stored.

---

# **12. Cross-Layer Enforcement**

### **Reasoning**

- Must emit structured evidence references
- Cannot emit free-text-only assertions

### **Judgment**

- Must verify evidence existence before decision
- Cannot promote without evidence chain

### **Governance**

- Only layer authorized to:
    - Promote
    - Downgrade
    - Invalidate
    - Archive assertions

---

# **13. Audit Guarantees**

Given an assertion_id, the system must be able to:

1. Retrieve full structured assertion
2. Retrieve raw record(s)
3. Reconstruct original source payload
4. Display span-highlighted evidence
5. Recompute assertion_hash

If any step fails → system integrity alert.

---

# **14. Prohibited Behaviors**

- Narrative-only reasoning without evidence
- Implicit evidence references
- Post-hoc evidence rewriting
- Silent epistemic state change
- Deleting raw records without invalidation cascade

---

# **15. Determinism Invariant**

Given identical raw records and projection state:

- Evidence chains must resolve identically
- Assertion hashes must be identical
- Governance decisions must be identical

---

# **16. Outcome Integrity Alignment**

This contract operationalizes Outcome Integrity at the system level by ensuring:

- Meaning is anchored to observable signals
- Inference is traceable
- Assumptions are visible
- Drift cannot hide in abstraction

---

# **System State After This Contract**

With all four contracts now defined:

1. Time Semantics & Ordering
2. Raw Record Identity & Idempotency
3. Replay Determinism & Semantic Stability
4. Evidence Chain Integrity

You now have:

- Deterministic ingestion
- Immutable provenance
- Controlled probabilistic layers
- Replay-stable canonical state
- Evidence-bound governance

This is a complete epistemic containment model.

---

If you want to push this to “production-ready architecture discipline,” the final missing piece would be:

> **Projection & Knowledge Mutation Contract (v1.0)**
> 

> Which defines how Knowledge Layer nodes are versioned, tombstoned, branched, and merged.
> 

That’s the last structural contract needed before implementation begins.