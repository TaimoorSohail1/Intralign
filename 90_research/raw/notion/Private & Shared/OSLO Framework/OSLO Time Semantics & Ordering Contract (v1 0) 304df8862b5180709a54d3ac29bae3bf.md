# OSLO Time Semantics & Ordering Contract (v1.0)

---

**Layer Authority:** Context Plane + Knowledge Layer

**Effective Scope:** All externally sourced signals

**Determinism Level:** REQUIRED

---

## **1. Purpose**

To ensure:

- Temporal conflicts are explicitly modeled (not resolved heuristically)
- Event ordering is deterministic
- Replay produces identical ordered event streams

Time is treated as a **bundle**, not a single field.

---

## **2. Canonical Timestamp Bundle**

Every immutable raw record MUST contain:

| **Field** | **Description** | **Required** |
| --- | --- | --- |
| event_occurred_at | When the event is asserted to have happened (source-provided) | OPTIONAL |
| source_recorded_at | When the source system committed the record | OPTIONAL |
| oslo_ingested_at | When OSLO ingested the record | REQUIRED |
| clock_confidence | Enum: HIGH / MEDIUM / LOW | OPTIONAL |

No timestamp may be overwritten after storage.

---

## **3. Conflict Handling Rule**

OSLO SHALL NOT collapse timestamp fields.

Conflicts are preserved as fact.

---

## **4. Deterministic Event Ordering Algorithm**

When reconstructing timelines, the system MUST apply this priority:

1. event_occurred_at (if present)
2. source_recorded_at
3. oslo_ingested_at
4. raw_record_id (lexicographic fallback)

This ensures:

- Total ordering
- Stable replay
- No dependency on ingestion order alone

---

## **5. Prohibited Behavior**

- Inferring “true time” by overwriting source timestamps
- Using ingestion time as a substitute for event time
- Ordering events without a deterministic fallback key

---

## **6. Replay Invariant**

Given identical raw records, ordered results MUST be identical across replays.

Failure condition: any non-deterministic sort outcome.

---

---

#