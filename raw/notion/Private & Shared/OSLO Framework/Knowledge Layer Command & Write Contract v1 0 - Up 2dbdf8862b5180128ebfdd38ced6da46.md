# Knowledge Layer Command & Write Contract v1.0 - Update 1/15

---

**System:** OSLO / Intralign

**Layer:** Knowledge

**Spec Type:** Normative (write semantics & API contract)

**Status:** Canonical

**Audience:** Engineering, Platform, QA

---

## **1. Purpose**

This document defines **exactly how canonical assertions and knowledge records are written** to the Knowledge Layer.

It specifies:

- allowed write commands
- required inputs
- validation steps
- epistemic enforcement
- invariant enforcement
- versioning behavior
- failure modes

Anything not explicitly allowed here is **not permitted**.

---

## **2. Core Principles (Non-Negotiable)**

1. **Knowledge is append-only**
2. **All writes persist assertions, not inferred truth**
3. **Epistemic status must be explicit**
4. **No inference or promotion at write time**
5. **All writes are governed**
6. **All mutations create new versions**
7. **Reads and writes are strictly separated**

---

## **3. Command Model**

All writes occur through **explicit commands**.

There are **no generic “update” operations**.

---

### **Command Envelope (Required)**

```
{
  "command_id": "uuid",
  "command_type": "<ENUM>",
  "actor": {
    "type": "user | system | agent",
    "id": "uuid"
  },
  "authorization": {
    "authorization_id": "uuid",
    "policy_version": "string"
  },
  "payload": { ... },
  "timestamp": "ISO-8601"
}
```

---

### **Required Envelope Rules**

- command_id must be unique
- authorization must exist
- payload must fully define the assertion being written
- Commands are immutable once submitted

---

## **4. Epistemic Requirements (Global)**

### **4.0 Epistemic Status (Required on All Writes)**

Every write command that persists or supersedes a canonical record MUST include:

```
"epistemic_status":
  "asserted_fact | committed_fact | assumption | estimate | intent | inference | unknown"
```

Rules:

- Epistemic status is **mandatory**
- Source of data MUST NOT imply epistemic status
- Absence of epistemic status → REJECTED_EPISTEMIC
- Epistemic promotion requires explicit intent and authorization

---

## **5. Supported Command Types (v1.0)**

---

### **5.1 CreateEntity**

**Purpose:** Create a new canonical entity backed by an explicit assertion.

### **Payload**

```
{
  "entity_type": "Outcome | Requirement | ScheduleElement | Constraint | ...",
  "entity_data": { ... },
  "epistemic_status": "<ENUM>"
}
```

### **Validation**

- Entity type must exist
- Epistemic status must be present and allowed
- All required fields present
- No prohibited fields present
- No inferred or synthetic values
- Referential fields must resolve

### **Behavior**

- Create entity version v1
- Persist assertion + entity projection
- Emit write receipt

### **Failure Modes**

- Missing epistemic status → REJECTED_EPISTEMIC
- Inferred field detected → REJECTED_INVARIANT
- Missing authorization → REJECTED_GOVERNANCE

---

### **5.2 SupersedeEntity**

**Purpose:** Create a new version of an existing entity.

### **Payload**

```
{
  "entity_type": "Outcome",
  "entity_id": "uuid",
  "new_entity_data": { ... },
  "epistemic_status": "<ENUM>",
  "supersession_reason": "string"
}
```

### **Validation**

- Entity exists
- Supersession allowed
- Immutable fields unchanged
- Epistemic status change is explicit
- Promotion requires authorization

### **Behavior**

- Mark prior version as superseded
- Create new version with preserved lineage

### **Failure Modes**

- Silent epistemic change → REJECTED_EPISTEMIC
- Immutable field changed → REJECTED_IMMUTABILITY

---

### **5.3 CreateRelationship**

**Purpose:** Create a canonical relationship (edge).

### **Payload**

```
{
  "relationship_type": "depends_on | supports | constrains | ...",
  "source": { "type": "EntityType", "id": "uuid" },
  "target": { "type": "EntityType", "id": "uuid" },
  "properties": { ... },
  "epistemic_status": "<ENUM>"
}
```

### **Rules**

- Relationships carry epistemic status
- No implied causality or certainty

---

### **5.4 SupersedeRelationship**

**Purpose:** Replace a relationship without mutation.

Rules mirror SupersedeEntity.

---

### **5.5 RecordAssumption**

**Purpose:** Persist an explicit assumption.

### **Payload**

```
{
  "assumption_text": "string",
  "scope": "project | artifact | entity",
  "related_entity_ids": ["uuid"]
}
```

### **Rules**

- Epistemic status is implicitly assumption
- No auto-generation
- Stored as first-class assertion

---

### **5.6 IngestExecutionFact**

**Purpose:** Record external execution reality.

### **Payload**

```
{
  "external_system": "jira | asana | planner",
  "external_object_id": "string",
  "mapped_entity_id": "uuid",
  "state": { ... },
  "observed_at": "ISO-8601"
}
```

### **Rules**

- Epistemic status is committed_fact
- Observational only
- No interpretation

---

### **5.7 RecordAuthorizationEvent**

**Purpose:** Persist governance decisions.

Rules unchanged.

---

### **5.8 StoreActionProposal (Stub)**

**Purpose:** Persist proposed future actions.

- Epistemic status: intent
- Never executed
- Never interpreted

---

## **6. Validation Pipeline (Mandatory Order)**

1. Envelope validation
2. Authorization presence
3. Epistemic validation
4. Schema validation
5. Invariant enforcement
6. Versioning enforcement
7. Referential integrity
8. Persistence

---

## **7. Explicit Failure Codes (Additions)**

| **Code** | **Meaning** |
| --- | --- |
| REJECTED_EPISTEMIC | Missing or invalid epistemic status |
| REJECTED_PROMOTION | Unauthorized epistemic promotion |

---

## **8. Explicit Non-Responsibilities**

The Knowledge Layer **must not**:

- infer missing values
- promote belief to fact
- reinterpret assertions
- score or rank data
- trigger reasoning

---

## **Canonical Close**

> Knowledge writes persist
> 
> 
> **what is asserted**
> 

> not what the system decides is true.
> 

> If epistemic intent is unclear, the write must fail.
> 

---

## **End of Specification**

---

## **3. What changed (brief, defensible)**

- **Epistemic status is now mandatory on all writes**
- **Supersession cannot silently change belief**
- **User vs AI is irrelevant at write time**
- **Assumptions are no longer a special escape hatch**
- **Inference is structurally impossible in Knowledge**

This completes the **epistemic firewall** at the write boundary.

---

## **Next document (correct sequence)**

👉 **Knowledge → Reasoning Projection & Snapshot Specification v1.0**

That’s where we ensure:

- Reasoning never reinterprets assertions
- Snapshots preserve epistemic context intact

Upload it when ready and we’ll continue.