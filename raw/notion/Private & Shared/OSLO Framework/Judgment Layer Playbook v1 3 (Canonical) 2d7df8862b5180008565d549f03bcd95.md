# Judgment Layer Playbook v1.3 (Canonical)

*(Supersedes v1.2)*

---

## **Document Control**

- **System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)
- **Document Name:** Judgment Layer Playbook
- **Document Type:** Playbook
- **Version:** v1.3
- **Status:** Canonical
- **Audience:** Engineering, AI/ML, Product
- **Scope:** Layer-Level
- **Authoritative For:**
    - Intent and philosophy of judgment
    - Interpretation of structural findings
    - Issue creation semantics
    - Health assessment logic
- **Non-Authoritative For:**
    - Structural truth
    - Canonical data mutation
    - Exposure timing or suppression
- **Consumes:**
    - Findings
    - Evidence Chains (by reference)
    - Structural Signals
- **Constrained By:**
    - Reasoning Layer Specification v1.2
    - Knowledge Layer Playbook v1.3
    - Tier Capability Contract v1.0
    - Compute Budget Contract v1.0
    - Governance Contract Spec v1.0
    - Governance State Machine v1.1
    - Scenario Guardrails v1.0
    - UI-Authorized Mutation Rules (G-03)
- **Supersedes:** Judgment Layer Playbook v1.2

---

> This document explains
> 
> 
> **intent, philosophy, and interpretive posture**
> 

> 
> 

> It is
> 
> 
> **non-normative**
> 

> 
> 

> Enforcement MUST follow system contracts and downstream governance rules.
> 

---

## **1. Purpose of the Judgment Layer**

*(No semantic change)*

The Judgment Layer exists to answer **one question only**:

> “Given these structural findings, does this matter—and if so, how?”
> 

Judgment is OSLO’s **normative engine**.

It does **not** determine truth.

It determines **significance, impact, and posture**.

---

## **2. Epistemic Boundary (Reinforced)**

*(No change; already correct)*

Judgment **never disputes structural truth**.

It **consumes**:

- Findings
- Evidence chains
- Structural signals

And **adds**:

- Interpretation
- Severity
- Risk framing
- Confidence adjustments
- Decision posture

Judgment is **explicitly value-laden** and **context-sensitive**.

---

## **3. Inputs to the Judgment Layer**

### **3.1 Required Inputs**

Judgment operates only on **completed Reasoning outputs**:

- Finding[]
- EvidenceChain[] (by reference)
- StructuralSignal[]
- Execution context (mode + trigger)

Judgment **must not**:

- Recompute structure
- Invent facts
- Modify evidence chains

---

### **3.2 Formal Finding Consumption Contract**

*(No schema changes; terminology now locked)*

Each Finding is evaluated independently before aggregation.

```
JudgmentInput {
  finding_id
  finding_type
  dimension
  affected_elements[]
  structural_claim
  evidence_chain_id
  context {
    mode
    trigger
  }
}
```

**Rules**

- Every judgment MUST reference a finding_id
- No judgment exists without a finding
- Multiple judgments MAY reference the same finding under different modes

---

## **4. Authoritative Responsibilities of Judgment**

Judgment is responsible for:

1. Interpreting **structural findings** in context
2. Determining whether a finding constitutes an **issue**
3. Assigning **severity, confidence, and scope**
4. Aggregating issues into **health assessments**
5. Producing **actionable interpretations** *(not actions)*
6. Adjusting posture based on **mode, tier, and governance state**

> Tier and compute constraints affect
> 
> 
> **when and where**
> 

> never
> 
> 
> **what conclusions are drawn**
> 

---

## **5. Core Judgment Outputs**

### **5.1 Issues (Primary Judgment Artifact)**

*(No schema changes)*

```
Issue {
  issue_id
  source_finding_id
  issue_type
  dimension: "Clarity" | "Alignment" | "Feasibility"
  severity: "Low" | "Medium" | "High" | "Critical"
  confidence
  affected_elements[]
  judgment_rationale
}
```

**Rules**

- Issues are contextual, not absolute
- Issues MAY be suppressed or deferred by Governance
- Issues MAY be downgraded or removed without invalidating findings

---

### **5.2 Health Scores (Aggregated Judgment)**

*(No changes)*

Health scores are **interpretive rollups**, never raw measurements.

```
HealthScore {
  dimension
  score
  contributing_issue_ids[]
  confidence_band
}
```

**Rules**

- Scores are mode-dependent
- Scores vary with tolerance parameters
- No score exists without underlying issues

---

### **5.3 Judgment Signals (Derived Interpretation)**

*(No changes)*

Judgment may emit interpretive signals:

```
JudgmentSignal {
  signal_id
  signal_type
  severity
  confidence
  source_issue_ids[]
}
```

Judgment signals:

- Are **non-structural**
- MUST NOT feed back into Reasoning

---

## **6. Mode-Aware Judgment Behavior**

*(No changes; fully aligned)*

| **Mode** | **Judgment Posture** |
| --- | --- |
| Canonical | Conservative, standards-based |
| Hypothetical | Exploratory, assumption-tolerant |
| 60Second | Salience-driven, high-signal only |
| WhatIf | Comparative, delta-focused |

**Rules**

- Findings remain invariant across modes
- Interpretation varies
- Mode MUST be recorded on every issue

---

## **7. Confidence & Severity Semantics**

### **7.1 Confidence**

Confidence reflects:

- Evidence completeness
- Reliance on placeholders
- Rule stability

It does **not** reflect urgency.

---

### **7.2 Severity**

Severity reflects:

- Outcome impact
- Structural leverage
- Downstream risk

Severity is **explicitly judgmental**.

---

## **8. Governance Interaction (Explicit Boundary)**

Judgment produces **candidate interpretations**.

Governance decides:

- Whether issues surface
- Where they surface
- When they surface
- Whether they are suppressed, deferred, or blocked

Judgment **cannot override governance**.

---

## **9. Determinism & Replayability**

Judgment is **not deterministic**.

Replay requires:

- Same findings
- Same execution context
- Same tolerance parameters

Judgment MUST always:

- Reference evidence
- Explain rationale
- Declare uncertainty

---

## **10. Prohibited Behavior (Hard Boundary)**

Judgment SHALL NEVER:

- Modify or recompute findings
- Invent evidence
- Write to canonical project data
- Generate UI copy
- Ask users questions directly
- Perform execution or remediation

---

## **11. Acceptance Criteria (v1.3)**

Judgment is compliant when:

- Every issue maps to a finding
- Every interpretation is explainable
- Structural truth is preserved
- Modes affect interpretation, not facts
- Governance controls exposure
- Tier/compute limits do not alter conclusions
- Outputs remain auditable

---

## **Invariant**

> Judgment may interpret truth,
> 

> but may never alter it.
> 

---

## **Canonical Close**

*(Unchanged — strong and aligned)*

> Judgment exists to translate structure into meaning —
> 

> without distorting the structure itself.
> 

> 
> 

> It makes consequences visible,
> 

> while leaving truth intact.
> 

---

# **What changed (brief)**

- Updated **Document Control** to match the unified system template
- Explicitly referenced **Tier Capability** and **Compute Budget** contracts
- Clarified that tier/compute affect **exposure**, not **interpretation**
- No schema, logic, or semantics changed

---

## **Status check**

At this point:

- **Knowledge**: locked
- **Reasoning (spec + playbook)**: locked
- **Judgment (playbook)**: locked

The **next required document** to complete the enforceable chain is:

👉 **Judgment Layer Specification (normative)**

That will fully harden issue creation and scoring rules.

If you want, I can produce that next in the same disciplined style.