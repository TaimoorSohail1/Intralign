# Judgment Layer — Detailed Responsibilities

---

## **Canonical Role**

> Judgment interprets reasoning outputs and decides their significance, confidence, and consequences.
> 

It does **not** discover facts.

It does **not** generate language.

It does **not** control delivery timing.

It answers one question only:

> “Given what is structurally true, what does this mean for the user right now?”
> 

---

## **Inputs (Strict)**

The Judgment Layer **only consumes**:

- Reasoning findings
- Evidence chains
- Dependency paths
- Inference flags

It **never** queries raw Project Knowledge directly.

This ensures judgment is:

- Testable
- Replayable
- Auditable

---

## **Core Responsibilities (What Judgment Owns)**

### **1. Issue Classification**

Judgment determines **whether a reasoning finding constitutes an issue**.

Examples:

- Structural gap → *Issue*
- Ambiguity → *Potential issue*
- Inference → *Non-blocking concern*
- Benign variance → *No issue*

This is where OSLO decides:

- “This is a problem”
- vs “This is worth noting”
- vs “This is acceptable”

---

### **2. Severity Assessment**

Judgment assigns **impact severity**, not structural magnitude.

Severity answers:

- *How bad is this if unresolved?*
- *What scale of outcome degradation occurs?*

Typical dimensions:

- Local vs systemic
- Reversible vs irreversible
- Blocking vs degradational

Severity is **contextual**, not absolute.

---

### **3. Confidence Assessment**

Judgment assigns **confidence in the conclusion**, not in the data.

Confidence reflects:

- Completeness of evidence
- Presence of assumptions
- Degree of inference
- Data freshness

This is critical for trust.

Judgment must be able to say:

> “We believe this is an issue, but with moderate confidence.”
> 

---

### **4. Boundary Definition (What OSLO Will NOT Claim)**

Judgment explicitly defines:

- Unknowns
- Assumptions
- Data gaps
- Ambiguous interpretations

This is where OSLO earns credibility.

Every judgment must carry:

- What OSLO knows
- What OSLO does not know
- What could change the judgment

---

### **5. Impact Analysis (Meaning, Not Mechanics)**

Judgment determines **why the finding matters** in outcome terms.

Not:

- “A requirement is missing”
    
    But:
    
- “Outcome success cannot be measured”
- “Schedule reliability is reduced”
- “Alignment risk increases”

Impact is always framed **relative to outcomes**, not artifacts.

---

### **6. Communication Eligibility (Critical Gate)**

Judgment decides **whether a finding is eligible to be communicated as an issue**.

Eligibility considers:

- Severity threshold
- Confidence threshold
- User context
- Flow state (e.g. onboarding)
- Redundancy with existing issues

This prevents:

- Over-alerting
- Premature critique
- Undermining onboarding experiences

---

### **7. Allowed Actions Definition**

Judgment determines:

- What actions are appropriate
- What actions are *not* appropriate

Examples:

- Ask for clarification
- Suggest refinement
- Block execution
- Defer action

Actions must be **proportional to confidence and severity**.

---

## **Outputs (Judgment Record)**

Every judgment produces a **Judgment Record**, containing:

- Issue classification (or non-issue)
- Severity
- Confidence
- Impact framing
- Boundaries
- Allowed actions
- Allowed communication channels

This record is **immutable downstream**.

---

## **What Judgment Explicitly Does NOT Do**

| **❌ Not Judgment** | **Why** |
| --- | --- |
| Fact discovery | That’s reasoning |
| Schema validation | That’s knowledge |
| Language generation | That’s communication |
| Tone selection | That’s rendering |
| Timing decisions | That’s governance |
| User education | That’s guidance class |
| Flow orchestration | That’s governance |

If judgment leaks into these areas, trust erodes.

---

## **Relationship to Adjacent Layers**

### **Reasoning → Judgment**

Reasoning provides **truth**

Judgment provides **meaning**

### **Judgment → Governance**

Judgment provides **eligibility & constraints**

Governance decides **when and how** to act

### **Judgment → Communication**

Judgment provides **what may be said**

Communication decides **how it is explained**

---

## **Why Judgment Must Be Explicit (Not Implicit)**

If judgment is implicit:

- AI feels opinionated
- Users feel judged
- Explanations feel hand-wavy
- Audits fail

If judgment is explicit:

- OSLO can say “here’s why”
- Confidence is calibrated
- Silence is defensible
- Trust compounds

---

## **One-Sentence Canonical Definition**

**The Judgment Layer interprets reasoning outputs to determine issue status, severity, confidence, impact, and communication eligibility—without discovering facts or generating language.**

If you want next, I can:

- Define a **formal Judgment Record schema**
- Map **judgment levels → allowed comms behaviors**
- Create **review checklists for judgment logic**
- Show **failure modes when judgment is mis-scoped**

Just say which.