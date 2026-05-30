# OSLO Raw Record Identity & Idempotency Contract (v1.0)

---

---

**Layer Authority:** Context Plane

**Determinism Level:** REQUIRED

---

## **1. Purpose**

To guarantee:

- Immutable storage
- No duplicate ingestion
- Idempotent sync behavior
- Traceable provenance

---

## **2. Record Types**

Two identifiers are REQUIRED:

### **2.1 raw_record_id (Immutable Identity)**

Computed as:

```
SHA-256(
    source_system +
    source_object_type +
    canonicalized_payload +
    source_native_id (if present)
)
```

### **2.2 source_pointer_id**

Provider-native ID used for incremental sync:

- Gmail: message-id
- Slack: channel + ts
- CRM: activity id
- Calendar: event UID

---

## **3. Canonicalization Rules**

Before hashing:

- Normalize whitespace
- Remove transient fields (retrieved_at, cursor, pagination metadata)
- Sort JSON keys deterministically
- Normalize timestamps to ISO 8601 UTC
- Strip volatile headers unless semantically meaningful

---

## **4. Deduplication Rules**

### **If**

### **source_native_id**

### **is stable:**

It MUST be included in hash input.

### **If not stable or absent:**

Hash must include:

- Structured payload
- Key metadata (sender, subject, event start, etc.)

---

## **5. Mutation Policy**

Raw records are IMMUTABLE.

If a source object changes:

- New raw_record_id is generated
- New record references:

```
supersedes_raw_record_id
```

No updates in place.

---

## **6. Ingestion Idempotency Rule**

If a raw_record_id already exists:

- Skip write
- Log idempotent ingest
- Do not promote again

---

## **7. Failure Conditions**

- Hash collisions (must trigger alert)
- Mutable raw records
- Re-ingestion producing different raw_record_id for identical content

---

---

#