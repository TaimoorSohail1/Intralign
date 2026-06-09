# Knowledge Layer Data Model (Logical / Canonical) - Revised 1/15

---

**System:** OSLO / Intralign

**Layer:** Knowledge

**Version:** vNext

**Status:** Canonical

**Audience:** Engineering, Data, Architecture

---

## **1. Purpose**

This document defines the **logical canonical data model** of the Knowledge Layer.

It describes:

- what canonical entities may exist
- how assertions are represented
- how epistemic status is recorded
- how versions and lineage are preserved

It does **not** define:

- physical storage
- APIs
- mutation mechanics
- reasoning, judgment, or scoring logic

---

## **2. Modeling Principles**

The Knowledge Layer data model is:

- **Logical** (not physical)
- **Graph-oriented** (entities + relationships)
- **Append-only** (versioned lineage)
- **Assertion-first** (no implicit truth)
- **Explicit** (no derived fields)
- **Storage-agnostic**

> Presence in the Knowledge Layer does not imply truth, certainty, or importance.
> 

---

## **3. Canonical Assertion Model (Foundational)**

### **3.1 Assertion (Foundational Primitive)**

**Purpose:**

Represents a claim asserted into the system by a source.

All domain entities MUST be backed by an Assertion record.

**Core properties:**

- assertion_id
- source_type (user | ai | imported_system)
- source_reference
- asserted_at
- assertion_text (normalized)
- epistemic_status (see below)
- justification (optional, structured)
- version_parent_id (if revised)

Assertions are **not facts by default**.

---

### **3.2 Epistemic Status (Canonical Field)**

Every Assertion MUST declare exactly one epistemic status:

- **asserted_fact** (claimed as true, not yet verified)
- **committed_fact** (approved / contractually fixed)
- **assumption**
- **estimate**
- **intent**
- **inference**
- **unknown**

> source_type = user MUST NOT imply epistemic_status = fact.
> 

Promotion between statuses requires explicit action or evidence.

---

## **4. Core Canonical Domain Entities**

All entities below are **domain projections backed by Assertions**.

---

### **4.1 Project (Root Context)**

Defines the bounded context for all knowledge.

- project_id
- created_at
- lifecycle_state

---

### **4.2 Outcome**

Represents an **intended result**, not an achieved one.

- Must reference an Assertion
- Epistemic default: **intent**

---

### **4.3 Requirement**

Represents a condition believed necessary to achieve an outcome.

- Must reference an Assertion
- Epistemic default: **assumption**

---

### **4.4 ScheduleElement**

Represents temporal structure only.

- No implied feasibility
- No implied commitment
- Epistemic default: **estimate**

---

### **4.5 Assumption**

Represents an explicitly declared belief.

- Always explicit
- Never inferred
- First-class entity
- Epistemic status: **assumption**

---

### **4.6 Constraint**

Represents a limiting rule or boundary.

- Epistemic default: **assumption**
- May be promoted to **committed_fact** with evidence

---

### **4.7 ExecutionFact**

Represents observed reality from external systems.

- Time-stamped
- Non-interpretive
- Epistemic status: **committed_fact**

---

### **4.8 AuthorizationRecord**

Represents formal approval.

- Audit artifact
- May promote epistemic status of related assertions

---

### **4.9 ActionProposal (Stub)**

Represents a proposed future action.

- Never executable by Knowledge
- Always epistemic status: **intent**

---

## **5. Relationship Types (Logical)**

Relationships are first-class canonical records.

All relationships:

- reference Assertions
- are versioned
- carry epistemic status
- never imply causality by default

---

## **6. Version Lineage Model**

Every Assertion, Entity, and Relationship:

- has a stable identity
- preserves lineage
- is append-only
- is never overwritten

---

## **7. Scope & Isolation**

- All knowledge is project-scoped
- Cross-project relationships are forbidden
- Snapshots reference version IDs only

---

## **8. Explicit Exclusions**

This data model excludes:

- probabilistic scoring
- optimization metrics
- reasoning artifacts
- confidence percentages
- UI state

> Epistemic status and provenance are
> 
> 
> **canonical**
> 

---

## **Canonical Close**

> This model defines what may be asserted and how belief is represented —
> 

> not what is true, risky, or important.
> 

---

# **Part 4 — What this enables downstream (important)**

With this revision:

- Reasoning can safely classify without fabricating
- Judgment can weight decisions correctly
- Governance can enforce only on committed facts
- Communication can speak honestly about uncertainty
- Engineers cannot accidentally treat “typed” as “true”

This is a **structural safeguard**, not a philosophical one.

---

## **Next step (as planned)**

Once you confirm this revision direction, the **next document to upload** is:

👉 **Knowledge Layer Invariants & Anti-Invariants (Canonical)**

That is where we will:

- lock these rules as non-negotiable
- prevent future regression

Say the word when ready.

---

##