# Knowledge Layer Data Schema (Physical Realization)

**System:** OSLO / Intralign

**Layer:** Knowledge

**Version:** vNext

**Status:** Canonical-Implementation (Non-Authoritative)

**Audience:** Engineering, Data, Platform

---

## **⚠️ Authority Notice (Required)**

> This document defines
> 
> 
> **one physical storage implementation**
> 

> It is
> 
> 
> **subordinate**
> 
- Knowledge Layer Specification
- Knowledge Layer Invariants & Anti-Invariants
- Knowledge Layer Data Model (Logical)

> 
> 

> If a conflict exists, this document
> 
> 
> **does not prevail**
> 

---

## **1. Purpose**

This document specifies the **physical data schema** used to persist Knowledge Layer data.

It exists to:

- enable implementation
- enforce storage-level integrity
- support replayable snapshots

It does **not** define:

- business meaning
- evaluation logic
- reasoning behavior
- governance decisions

---

## **2. Schema Design Principles**

- Reflect the **logical data model exactly**
- Preserve **append-only versioning**
- Avoid computed or derived fields
- Support **efficient snapshot assembly**
- Remain replaceable without semantic loss

---

## **3. Core Tables (Illustrative)**

> Note: Table names and structures are illustrative and may evolve.
> 

> Logical compatibility is mandatory.
> 

---

### **3.1**

### **projects**

Stores project root context.

**Key fields (physical):**

- project_id (PK)
- created_at
- lifecycle_state

---

### **3.2**

### **entities**

Stores versioned canonical entities.

**Key fields:**

- entity_version_id (PK)
- entity_id (stable identity)
- entity_type
- project_id (FK)
- payload (JSON / structured)
- created_at
- supersedes_version_id (nullable)

No entity is ever updated in place.

---

### **3.3**

### **relationships**

Stores versioned canonical relationships.

**Key fields:**

- relationship_version_id (PK)
- relationship_id
- relationship_type
- source_entity_version_id
- target_entity_version_id
- payload
- created_at
- supersedes_relationship_version_id (nullable)

---

### **3.4**

### **assumptions**

May be stored as entities or a dedicated table depending on implementation.

Must remain:

- explicit
- versioned
- scoped

---

### **3.5**

### **execution_facts**

Stores observed external state.

**Key fields:**

- execution_fact_id
- external_system
- external_object_id
- mapped_entity_id
- payload
- observed_at

No interpretation fields allowed.

---

### **3.6**

### **authorization_records**

Stores governance authorization metadata.

Used for audit only.

---

### **3.7**

### **snapshots**

Stores snapshot metadata.

**Key fields:**

- snapshot_id
- project_id
- created_at
- trigger
- entity_version_set
- relationship_version_set

Snapshot contents may be materialized or reconstructed.

---

## **4. Constraints & Indexes (Storage-Level Only)**

Allowed constraints:

- primary keys
- foreign keys
- non-null fields
- uniqueness constraints
- referential integrity

Forbidden:

- business rule enforcement
- inferred constraints
- cross-layer semantics

---

## **5. Mapping to Logical Model**

Every table and field must map cleanly to:

- an entity type
- a relationship type
- or a metadata concept

If a field cannot be mapped, it does not belong here.

---

## **6. Replaceability Guarantee**

This schema:

- may be replaced
- may be migrated
- may be re-implemented (graph, hybrid, etc.)

As long as:

- the logical data model is preserved
- invariants hold
- snapshots remain replayable

---

## **Canonical Close**

> This schema is an implementation detail —
> 

> not a definition of reality.
> 

---

### **✔️ Outcome**

- Engineers know exactly how to treat this doc
- No confusion with the logical model
- Safe future migration path
- No logic leakage

---