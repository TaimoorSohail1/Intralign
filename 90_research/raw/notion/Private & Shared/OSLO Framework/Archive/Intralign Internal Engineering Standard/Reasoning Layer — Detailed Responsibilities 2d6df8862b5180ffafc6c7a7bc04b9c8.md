# Reasoning Layer — Detailed Responsibilities

## **Canonical Role**

> Reasoning evaluates project knowledge to determine what conditions hold, fail, or are indeterminate—without assigning importance, confidence, or consequences.
> 

It does **analysis**, not interpretation.

It produces **findings**, not opinions.

It answers one question only:

> “Given the current project state, what is structurally true, false, incomplete, or ambiguous?”
> 

---

## **Inputs (Strict)**

The Reasoning Layer **only consumes**:

- Canonical Project Knowledge
    - Entities
    - Relationships
    - Constraints (definitions)
    - Versioned state

It does **not**:

- Look at user sentiment
- Consider business priority
- Consider onboarding context
- Consider whether OSLO should speak

That is all downstream.

---

## **Core Responsibilities (What Reasoning Owns)**

---

## **1. Structural Validation**

Reasoning checks **existence and structure**, not importance.

Examples:

- Required elements missing
- Orphaned entities
- Invalid relationships
- Schema violations

**Example finding**

> Requirement exists but is not linked to any outcome
> 

This is a *fact*, not a problem statement.

---

## **2. Constraint Evaluation**

Reasoning evaluates **defined constraints** against project state.

Types:

- Temporal constraints (dates, order)
- Dependency constraints (hard vs soft)
- Logical constraints (AND / OR / conditional)
- Cardinality constraints (one-to-many, required minimums)

**Example finding**

> Milestone date precedes prerequisite completion date
> 

No severity. No alarm. Just truth.

---

## **3. Dependency & Graph Traversal**

Reasoning performs **graph operations** to understand structure.

Includes:

- Upstream / downstream traversal
- Reachability analysis
- Isolation detection
- Impact surface identification (what depends on what)

**Example finding**

> Outcome O-3 depends on requirements R-12, R-14, R-19
> 

This enables downstream impact analysis—but does not perform it.

---

## **4. Gap Detection**

Reasoning detects **absence relative to expectations**.

Includes:

- Missing success criteria
- Undefined owners
- Incomplete requirements
- Unspecified assumptions

**Example finding**

> Outcome lacks measurable success criteria
> 

Still not a “risk” yet. Just a gap.

---

## **5. Ambiguity Detection**

Reasoning flags **non-determinism**.

Includes:

- Vague language
- Multiple possible interpretations
- Overloaded entities
- Conflicting definitions

**Example finding**

> Success criteria ambiguous between time-based and usage-based interpretation
> 

This is critical for trust—OSLO must know *when it doesn’t know*.

---

## **6. Inference Detection (Not Resolution)**

Reasoning identifies **implicit assumptions**, but does not resolve them.

Includes:

- Implied dependencies
- Inferred scope
- Unstated constraints

**Example finding**

> Requirement appears to assume availability of external API, but none is defined
> 

Reasoning flags the inference; Judgment decides what it means.

---

## **7. Evidence Assembly (“Because Chains”)**

Reasoning constructs **machine-readable evidence paths**.

This is one of its most important jobs.

Includes:

- Entity IDs
- Constraint references
- Dependency paths
- State deltas

**Example evidence chain**

```
Outcome O-3 → depends on Requirement R-12
R-12 → lacks acceptance criteria
Therefore → O-3 measurability cannot be evaluated
```

No conclusion. Just traceable logic.

---

## **Outputs of the Reasoning Layer**

Reasoning emits **findings**, each with:

- Finding type (gap, violation, ambiguity, inference)
- Affected entities
- Constraint references
- Dependency paths
- Evidence graph

These outputs are:

- Deterministic
- Replayable
- Auditable
- Judgment-agnostic

---

## **What Reasoning Explicitly Does NOT Do**

| **❌ Not Reasoning** | **Why** |
| --- | --- |
| Severity scoring | That’s interpretation |
| Confidence assignment | That’s judgment |
| Risk framing | That’s judgment |
| Action selection | That’s judgment |
| Communication eligibility | That’s judgment |
| Language generation | That’s communication |
| Timing decisions | That’s governance |

If reasoning starts “sounding concerned,” it’s broken.

---

## **Relationship to Adjacent Layers**

### **Project Knowledge → Reasoning**

Knowledge provides **facts and structure**

Reasoning evaluates **conditions and relationships**

### **Reasoning → Judgment**

Reasoning provides **truth with evidence**

Judgment decides **what that truth means**

Reasoning never knows *why it matters*.

Judgment never discovers *what is true*.

---

## **Why This Layer Must Be Deterministic**

If reasoning is probabilistic or implicit:

- Findings can’t be reproduced
- Bugs look like “model behavior”
- Trust collapses under scrutiny

If reasoning is deterministic:

- You can replay it
- You can test it
- You can explain it
- You can evolve it safely

---

## **One-Sentence Canonical Definition**

**The Reasoning Layer deterministically evaluates project knowledge to produce evidence-backed findings about structure, constraints, gaps, and ambiguity—without assigning meaning, importance, or consequence.**

If you want next, I can:

- Formalize a **Reasoning Finding schema**
- Show **example reasoning outputs feeding judgment**
- Create **unit-test patterns for reasoning logic**
- Map reasoning responsibilities to **specific Oslo artifacts (charter, scope, WBS, etc.)**

Just say which.