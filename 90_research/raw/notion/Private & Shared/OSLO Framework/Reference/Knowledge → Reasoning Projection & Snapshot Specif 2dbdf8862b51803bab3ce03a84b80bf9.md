# Knowledge → Reasoning Projection & Snapshot Specification v1.0 - Update 1/15

---

**System:** OSLO / Intralign

**Layers:** Knowledge → Reasoning

**Spec Type:** Normative (read semantics & isolation contract)

**Status:** Canonical

**Audience:** Engineering, Platform, AI/ML, QA

---

## **1. Purpose**

This document defines **how canonical Knowledge assertions are projected into Reasoning**.

It specifies:

- snapshot creation rules
- immutability guarantees
- projection shape
- version pinning
- isolation boundaries

It prevents:

- write-time logic leaking into reasoning
- nondeterministic reads
- accidental epistemic coupling between layers

---

## **2. Core Principle (Non-Negotiable)**

> Reasoning never reads live canonical data.
> 

> 
> 

> It reasons only over immutable snapshots.
> 

All reasoning conclusions are relative to a **specific snapshot in time**.

---

## **3. Snapshot Definition**

### **3.1 What a Snapshot Is**

A **Knowledge Snapshot** is:

- an immutable, read-only projection
- of canonical **assertions, entities, and relationships**
- at a specific logical time
- with explicit version references
- with epistemic context preserved

Snapshots are **not caches**.

They are **faithful historical projections of asserted knowledge**.

---

### **3.2 Snapshot Identity**

Each snapshot must have:

```
{
  "snapshot_id": "uuid",
  "project_id": "uuid",
  "created_at": "ISO-8601",
  "created_by": "system | user | agent",
  "source_version_set": {
    "entities": ["entity_version_ids"],
    "relationships": ["relationship_version_ids"]
  }
}
```

---

## **4. Snapshot Creation Triggers**

Snapshots may be created when:

| **Trigger** | **Description** |
| --- | --- |
| Onboarding | Initial baseline snapshot |
| Authorized write | Post-mutation snapshot |
| Recompute request | Incremental snapshot |
| What-If | Isolated hypothetical snapshot |
| Audit | Explicit historical snapshot |

Snapshots are **explicitly requested**, never implicit.

---

## **5. Projection Rules (What Is Included)**

### **5.1 Included (Required)**

Snapshots MUST include:

- canonical entities (latest versions as of snapshot time)
- canonical relationships
- **epistemic status for every entity and relationship**
- assertion source metadata
- explicit assumptions
- explicit constraints
- execution facts (observational, factual only)
- authorization record references

> Epistemic context MUST NOT be stripped or normalized.
> 

---

### **5.2 Excluded (Explicitly)**

Snapshots MUST NOT include:

- inferred elements
- synthetic placeholders
- reasoning outputs
- judgment scores
- governance decisions
- UI state
- transient system metadata

> If it was
> 
> 
> *derived*
> 

---

## **6. Projection Shape (Canonical)**

The snapshot projection must conform to a **stable, machine-readable schema**.

Example (simplified):

```
{
  "snapshot_id": "uuid",
  "entities": {
    "Outcome": [ { "data": { ... }, "epistemic_status": "intent" } ],
    "Requirement": [ { "data": { ... }, "epistemic_status": "assumption" } ],
    "ScheduleElement": [ { "data": { ... }, "epistemic_status": "estimate" } ]
  },
  "relationships": [
    {
      "type": "depends_on",
      "source": "...",
      "target": "...",
      "epistemic_status": "assumption"
    }
  ],
  "execution_facts": [ { ... } ]
}
```

The shape is:

- deterministic
- order-stable
- schema-validated

---

## **7. Version Pinning & Replay**

### **7.1 Version Pinning**

Every snapshot must pin:

- entity version IDs
- relationship version IDs
- knowledge definition versions

This guarantees:

- exact replay
- historical audit
- deterministic reasoning

---

### **7.2 Replay Guarantee**

Given:

- snapshot_id
- reasoning rule versions
- reasoning profile
- reasoning mode

The system must be able to:

- reproduce identical reasoning outputs
- without access to live Knowledge data

---

## **8. Isolation Rules**

### **8.1 Reasoning Isolation**

Reasoning:

- cannot modify snapshots
- cannot request partial live reads
- cannot request “latest” outside a snapshot

---

### **8.2 Hypothetical Isolation**

For WHAT-IF:

- snapshot is cloned
- hypothetical deltas applied **outside Knowledge**
- canonical snapshot remains unchanged
- hypothetical snapshot is explicitly tagged

No hypothetical artifact may:

- be persisted to Knowledge
- influence canonical snapshots

---

## **9. Incremental Snapshot Optimization (Allowed)**

Performance optimizations MAY:

- reuse unchanged entity versions
- reuse unchanged relationship versions
- record delta references

As long as:

- snapshot immutability holds
- logical equivalence is preserved
- replay produces identical results

---

## **10. Error Handling**

If snapshot creation fails:

- reasoning must not proceed
- error must be explicit
- no partial snapshot allowed

If snapshot is incomplete:

- reasoning must record limitations
- must not fabricate missing data

---

## **11. Audit & Observability**

Every snapshot creation must log:

- trigger
- initiating actor
- reason
- entity/relationship counts
- snapshot_id

Snapshots are first-class audit artifacts.

---

## **12. Explicit Non-Responsibilities**

The Knowledge → Reasoning projection must not:

- filter “unimportant” data
- normalize for UX
- apply heuristics
- interpret meaning
- collapse epistemic distinctions

That belongs to **Reasoning**, not projection.

---

## **Canonical Invariant**

> Snapshots define what Reasoning may know.
> 

> 
> 

> Reasoning defines what follows.
> 

> 
> 

> Knowledge defines what was
> 
> 
> **asserted**
> 

---

## **End of Specification**

---

## **3. Why this matters**

With these changes:

- Reasoning **cannot silently treat assumptions as facts**
- AI inference is epistemically first-class, not second-class
- Replay truly reproduces *belief context*, not just structure
- Drift becomes explainable, not mysterious
- The 60-second experience stays fast **without lying**

---

### **✅ Knowledge Layer is now epistemically complete**

At this point, your Knowledge layer:

- cannot fabricate
- cannot infer
- cannot promote belief
- cannot mislead downstream logic

This is **far beyond** what most PM or AI planning systems do.

---

##