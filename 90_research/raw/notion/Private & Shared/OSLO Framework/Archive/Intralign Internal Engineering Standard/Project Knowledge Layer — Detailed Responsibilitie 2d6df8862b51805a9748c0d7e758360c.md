# Project Knowledge Layer — Detailed Responsibilities

---

## **Canonical Role**

> The Project Knowledge Layer defines what exists and how it is structured—nothing more.
> 

It is the **single source of truth** for project meaning.

It does **not** evaluate, interpret, judge, or communicate.

It answers one question only:

> “What is the current, canonical representation of this project?”
> 

---

## **Nature of the Layer (Critical Framing)**

- **Passive**: It does not “think”
- **Deterministic**: Same input → same state
- **Versioned**: All changes are explicit
- **Query-only for downstream layers**
- **Domain-grounded**: No language generation

Think of this layer as a **typed, versioned knowledge substrate**, not a model.

---

## **Core Responsibilities (What Project Knowledge Owns)**

---

## **1. Canonical Entity Definitions**

The layer owns the **existence and identity** of all project entities.

Examples:

- Project
- Outcome
- Objective
- Requirement
- Scope element
- Milestone / phase
- Assumption
- Constraint
- Risk (as a declared object, not evaluated)

Each entity has:

- A unique ID
- A type
- A schema
- A version

No downstream layer may invent entities.

---

## **2. Ontology & Schema Enforcement**

The layer defines:

- What entity types exist
- What fields they may have
- Which fields are required vs optional
- Field data types
- Allowed enumerations

**Example**

- An Outcome may have *success criteria*
- A Requirement may have *acceptance criteria*
- A Milestone must have a *date or condition*

This is **structural validity**, not quality.

---

## **3. Relationship & Graph Structure**

The layer owns **how entities may relate**.

Includes:

- Allowed relationship types (e.g., depends_on, satisfies, blocks)
- Cardinality rules
- Directionality
- Graph integrity

**Example**

- A Requirement may satisfy one or more Outcomes
- An Outcome may depend on multiple Requirements
- A Milestone may gate a Phase

The layer does **not** traverse or analyze the graph.

It only stores it.

---

## **4. Constraint Definitions (Not Evaluation)**

The Project Knowledge Layer defines **constraints as declarative rules**, such as:

- “Milestones must occur after prerequisite milestones”
- “Outcomes must have at least one success criterion”
- “Requirements must map to at least one outcome”

It does **not** evaluate whether these constraints are met.

That belongs to Reasoning.

---

## **5. Canonical State & Versioning**

The layer maintains:

- Current project state
- Historical versions
- Change lineage

Every change is:

- Explicit
- Traceable
- Replayable

This allows OSLO to reason about:

- What changed
- When it changed
- Relative deltas (via downstream layers)

---

## **6. Declared Assumptions & Inputs**

The layer stores **explicitly declared**:

- Assumptions
- Constraints
- External dependencies
- User-provided inputs

It does **not**:

- Infer assumptions
- Validate assumptions
- Evaluate risk

Declared ≠ true.

Declared ≠ safe.

Declared = recorded.

---

## **7. Domain Vocabulary & Normalization**

The layer may normalize:

- Terminology
- Synonyms
- Canonical labels

But it must not:

- Interpret intent
- Resolve ambiguity
- Guess meaning

Ambiguity is preserved for Reasoning to detect.

---

## **Outputs of the Project Knowledge Layer**

The layer outputs:

- Typed entities
- Structured relationships
- Declarative constraints
- Versioned state snapshots

These outputs are:

- Deterministic
- Side-effect free
- Judgment-agnostic
- Language-agnostic

---

## **What the Project Knowledge Layer Explicitly Does NOT Do**

| **❌ Not Project Knowledge** | **Why** |
| --- | --- |
| Structural validation | That’s reasoning |
| Constraint evaluation | That’s reasoning |
| Gap detection | That’s reasoning |
| Ambiguity detection | That’s reasoning |
| Severity assessment | That’s judgment |
| Confidence scoring | That’s judgment |
| Communication | That’s downstream |
| Inference | Ever |

If this layer starts *evaluating*, the system collapses.

---

## **Relationship to Adjacent Layers**

### **Project Knowledge → Reasoning**

Project Knowledge provides:

- Facts
- Structure
- Constraints (definitions)
- Relationships

Reasoning evaluates those facts.

Project Knowledge never knows if something is “good” or “bad”.

---

## **Why This Layer Must Be Rigid**

If Project Knowledge is loose:

- Reasoning becomes inconsistent
- Judgment becomes subjective
- Explanations feel hand-wavy
- Trust collapses under scrutiny

If Project Knowledge is rigid:

- Reasoning is deterministic
- Judgment is explainable
- Communication is credible
- OSLO scales safely

---

## **One-Sentence Canonical Definition**

**The Project Knowledge Layer is the passive, canonical, versioned representation of all project entities, relationships, and constraints—defining what exists, without evaluating, interpreting, or communicating.**

If you want next, I can:

- Provide a **formal Project Knowledge schema**
- Map this layer to **Intralign artifacts (Charter, Scope, WBS, Schedule)**
- Show **anti-patterns when knowledge and reasoning are merged**
- Define **API contracts between Project Knowledge and Reasoning**

Just say which.