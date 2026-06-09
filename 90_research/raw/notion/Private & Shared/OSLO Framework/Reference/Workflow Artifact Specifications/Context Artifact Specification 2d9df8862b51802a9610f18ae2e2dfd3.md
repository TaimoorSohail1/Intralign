# Context Artifact Specification

**OSLO Knowledge Layer — Context v1.1**

---

## **1. Purpose of the Context Artifact**

The Context Artifact defines the **operating conditions** under which the project must achieve its outcomes.

It captures the **non-negotiables, assumptions, and environmental realities** that constrain or shape planning decisions.

Context exists to:

- prevent false feasibility
- reduce ambiguity in “what’s possible”
- make constraints explicit so OSLO can judge tradeoffs credibly
- provide Charter-grade assumptions and constraints as derived content

Context does **not** define what success is (that is Intent).

---

## **2. Scope and Ownership**

### **What Context owns (strictly)**

- Constraints (hard limits)
- Assumptions (beliefs treated as true)
- Dependencies and external conditions
- Stakeholder and environment factors that shape feasibility and risk
- Risk posture inputs (not the risks themselves, unless you choose to store risks here)

### **What Context does**

### **not**

### **own**

- Outcomes, goals, objectives (Intent)
- Deliverables, requirements (Scope/Requirements)
- Resource capacity (Resource Plan)
- Dates and sequencing (Schedule)

---

## **3. Design Principles**

1. **Human-familiar**: Context reads like a real PM artifact, not a database form.
2. **Judgment-ready**: Every context element has a structured anchor.
3. **Strict scoping**: Context never restates intent or scope; it only constrains them.
4. **No inference as substitute**: Context-critical signals must be explicitly captured.
5. **Traceable constraints**: When possible, constraints can be linked to impacted objects (optional in v1).

---

## **4. Context Fields — Structured (Canonical Anchors)**

Context is composed of **entries** (0..n) in each category. Each entry is a first-class object.

All entries include:

- statement (the content)
- type (classification)
- criticality (importance)
- optional references (what it impacts)

### **4.1 Constraints (0..n) —**

### **Primary feasibility gate**

**Definition:** A constraint is a condition that **must be true** for the plan to be acceptable.

Each Constraint entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Constraint Statement | **Hard Required** | The constraint in clear language |
| Constraint Type | **Hard Required** | Time, budget, regulatory, technical, vendor, security, legal, scope-boundary, other |
| Criticality | Soft Required | Critical / High / Medium / Low |
| Constraint Owner | Optional | Person or role who owns/sets the constraint |
| Enforcement Mode | Optional | Hard stop vs flexible guidance (default hard) |
| Evidence / Source | Optional | Link or reference (policy doc, contract, exec note) |

**OSLO invariants**

- A missing Critical constraint should trigger **Feasibility** issues (not Clarity) once sufficient plan elements exist to evaluate it.
- Constraints are not “preferences.” Preferences belong in Intent tradeoff posture, not here.

---

### **4.2 Assumptions (0..n) —**

### **Confidence and risk amplifier**

**Definition:** An assumption is a belief treated as true, but not fully verified.

Each Assumption entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Assumption Statement | **Hard Required** | The assumption in testable language |
| Assumption Type | Soft Required | Market, technical, dependency, staffing, vendor, stakeholder, financial, timing, other |
| Confidence Level | Soft Required | High / Medium / Low |
| Validation Plan | Optional | How/when assumption will be validated |
| Expiry / Review Date | Optional | When to revisit |
| Evidence / Source | Optional | Why it’s believed true |

**OSLO invariants**

- Low-confidence assumptions should increase Feasibility risk signals.
- Assumptions should never silently become constraints.

---

### **4.3 Operating Environment (0..n) —**

### **Conditions that shape feasibility**

**Definition:** Environmental realities that influence delivery but are not explicit constraints.

Each Operating Environment entry includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Environment Statement | **Hard Required** | Condition that matters |
| Environment Type | Soft Required | Org/process, tooling, data, security posture, deployment model, governance, vendor landscape, other |
| Impact Area | Soft Required | Clarity / Alignment / Feasibility (one or more) |
| Evidence / Source | Optional | Supporting reference |

**OSLO invariants**

- Environment entries can trigger **Clarity** issues if they introduce ambiguous boundaries (e.g., “must comply with security requirements” without specifying which).

---

## **5. Context Fields — Structured (Optional but Highly Valuable)**

These are “context enhancers” that increase trust and charter completeness without bloating artifacts.

### **5.1 Stakeholders (Optional, v1)**

If you want Charter completeness and better judgment explanations, include:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Stakeholder Name/Role | Optional | Role or group |
| Stakeholder Type | Optional | Sponsor, decision-maker, approver, impacted, contributor |
| Concern / Priority | Optional | What they care about |
| Engagement Level | Optional | High/Medium/Low |

**Note:** If you prefer not to store stakeholders in Knowledge Layer yet, this can be deferred. But Charter reports often expect it.

---

### **5.2 External Dependencies (Optional, v1)**

Dependencies are not the same as requirements. They are *conditions outside the project’s control.*

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Dependency Statement | Optional | What must happen externally |
| Dependency Owner | Optional | Who controls it |
| Due Window | Optional | Timing expectation |
| Risk Level | Optional | High/Medium/Low |

**OSLO benefit:** improves feasibility and schedule realism.

---

## **6. Context Fields — Narrative (Bounded)**

Narrative fields are allowed but must not replace structured entries.

### **6.1 Context Summary (Optional)**

A short human summary of the overall environment.

### **6.2 Key Risks Implied by Context (Optional)**

Not a full risk register, but a human callout of “watch-outs.”

OSLO may reference this in explanations but must not treat it as a substitute for explicit constraint/assumption entries.

---

## **7. Canonical Objects Produced**

Context produces:

- Constraint
- Assumption
- Operating Environment
- (Optional) Stakeholder
- (Optional) External Dependency

All objects are:

- versioned
- source-labeled (explicit / inferred / proposed)
- eligible for linking to affected plan objects via edges

---

## **8. Relationship to Downstream Artifacts**

Context does not “own” downstream objects but constrains them.

Common constraint applications:

- Constraint -> Scope
- Constraint -> Resource Plan
- Constraint -> Schedule
- Assumption -> Requirements feasibility
- Environment -> Tooling/workflow implications

In v1, linking constraints to specific objects can be optional. If omitted, OSLO still applies them globally at the project level.

---

## **9. Judgment Coverage**

### **Clarity**

- Reduces ambiguity about boundaries and conditions
- Surfaces missing specificity in “must comply” statements

### **Alignment**

- Context can reveal misalignment when outcomes violate constraints (e.g., “ship in 30 days” vs “procurement lead time 60 days”)

### **Feasibility (primary contribution)**

- Constraints define hard feasibility limits
- Assumptions define confidence-weighted risk
- Environment defines operating realism

**If Context is missing, OSLO feasibility confidence is capped.**

---

## **10. Charter Coverage**

The following Charter sections are derivable from Context:

- Assumptions
- Constraints
- Dependencies (if captured)
- Stakeholder context (if captured)
- Operating conditions

No Charter-specific fields are required.

---

## **11. Invariants (Locked)**

1. Constraints, Assumptions, and Environment entries are first-class and separately tracked
2. Context never restates outcomes or scope
3. Constraints are hard limits unless explicitly marked otherwise
4. Assumptions always carry confidence and optionally a validation plan
5. Context critical signals must be explicit; inference cannot substitute
6. Context gaps primarily impact feasibility confidence and issue detection

---

## **12. Canonical Summary**

> The Context Artifact makes the real-world conditions explicit. Without it, feasibility judgment becomes optimistic, explanations become fragile, and outcome confidence cannot be trusted.
>