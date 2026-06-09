# Judgment Layer — Use Case Matrix (v1.0)

---

**System:** OSLO

**Layer:** Judgment

**Spec Type:** Normative (behavioral coverage)

**Audience:** Engineering, QA, Product Architecture

**Status:** Canonical

---

## **1. Purpose**

This document enumerates **all supported Judgment Layer use cases** in v1 and defines:

- when Judgment is invoked
- what inputs are required
- what decision outcomes are permitted
- what is explicitly *out of scope*

This matrix ensures **complete behavioral coverage** without feature creep.

---

## **2. Judgment Invocation Scope**

Judgment is invoked:

- after a **successful Reasoning run**
- with **explicit lifecycle + mode + tier**
- in **non-interactive, deterministic evaluation**

Judgment is **not user-triggered** directly.

---

## **3. Dimensions Used in the Matrix**

Each use case is defined across these dimensions:

- **Lifecycle Stage**
- **Reasoning Signal Type**
- **Data Sufficiency**
- **Judgment Intent**
- **Allowed Decision Types**

---

## **4. Use Case Matrix**

### **UC-J-01 — Clean State Acceptance**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | Any |
| Reasoning Signals | None |
| Data Sufficiency | Sufficient |
| Judgment Intent | Confirm readiness |
| Decision Types | ACCEPT |
| Severity | INFO |
| Notes | Baseline “all clear” |

---

### **UC-J-02 — Structural Incompleteness (Early)**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | INITIATION |
| Reasoning Signals | STRUCTURE_GAP |
| Data Sufficiency | Insufficient |
| Judgment Intent | Avoid premature blocking |
| Decision Types | DEFER |
| Severity | LOW–MEDIUM |
| Notes | Preserves 60-second aha without fabrication |

---

### **UC-J-03 — Structural Incompleteness (Planning)**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | PLANNING |
| Reasoning Signals | STRUCTURE_GAP |
| Data Sufficiency | Insufficient |
| Judgment Intent | Enforce planning rigor |
| Decision Types | BLOCK |
| Severity | MEDIUM–HIGH |
| Notes | Mandatory artifacts missing |

---

### **UC-J-04 — Content Quality Degradation**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | PLANNING |
| Reasoning Signals | CONTENT_QUALITY_GAP |
| Data Sufficiency | Sufficient |
| Judgment Intent | Surface improvement need |
| Decision Types | WARN |
| Severity | LOW–MEDIUM |
| Notes | Non-blocking quality issues |

---

### **UC-J-05 — SMART Deficiency**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | PLANNING |
| Reasoning Signals | SMART_GAP |
| Data Sufficiency | Partial |
| Judgment Intent | Highlight risk without halt |
| Decision Types | WARN or DEFER |
| Severity | MEDIUM |
| Notes | Depends on severity mapping |

---

### **UC-J-06 — Alignment Breakdown**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | PLANNING / EXECUTION |
| Reasoning Signals | ALIGNMENT_GAP |
| Data Sufficiency | Sufficient |
| Judgment Intent | Prevent outcome drift |
| Decision Types | WARN or BLOCK |
| Severity | MEDIUM–CRITICAL |
| Notes | Contextual severity |

---

### **UC-J-07 — Feasibility Risk Detected**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | EXECUTION |
| Reasoning Signals | FEASIBILITY_RISK |
| Data Sufficiency | Sufficient |
| Judgment Intent | Protect delivery viability |
| Decision Types | BLOCK |
| Severity | HIGH–CRITICAL |
| Notes | Execution realism enforcement |

---

### **UC-J-08 — Execution Drift Signal**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | EXECUTION |
| Reasoning Signals | DRIFT_SIGNAL |
| Data Sufficiency | Sufficient |
| Judgment Intent | Signal corrective attention |
| Decision Types | WARN |
| Severity | MEDIUM–HIGH |
| Notes | No actions generated |

---

### **UC-J-09 — Monitoring Degradation**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | MONITORING |
| Reasoning Signals | DRIFT_SIGNAL / QUALITY_GAP |
| Data Sufficiency | Sufficient |
| Judgment Intent | Maintain awareness |
| Decision Types | WARN |
| Severity | LOW–MEDIUM |
| Notes | Prefer WARN over BLOCK |

---

### **UC-J-10 — Late-Stage Non-Impacting Issue**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | CLOSURE |
| Reasoning Signals | Any non-critical |
| Data Sufficiency | Sufficient |
| Judgment Intent | Reduce noise |
| Decision Types | SUPPRESS |
| Severity | INFO–LOW |
| Notes | Explicit suppression |

---

### **UC-J-11 — Insufficient Evidence**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | Any |
| Reasoning Signals | MISSING_EVIDENCE |
| Data Sufficiency | Insufficient |
| Judgment Intent | Avoid hallucination |
| Decision Types | DEFER |
| Severity | INFO–LOW |
| Notes | Never fabricate completion |

---

### **UC-J-12 — Conflicting Signals**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | Any |
| Reasoning Signals | CONFLICT |
| Data Sufficiency | Ambiguous |
| Judgment Intent | Force deterministic posture |
| Decision Types | WARN or DEFER |
| Severity | MEDIUM |
| Notes | Rule-order resolution |

---

### **UC-J-13 — Tier-Based Visibility Limitation**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | Any |
| Reasoning Signals | Any |
| Data Sufficiency | Sufficient |
| Judgment Intent | Respect tier constraints |
| Decision Types | SUPPRESS |
| Severity | Any |
| Notes | Governance enforces access |

---

### **UC-J-14 — Expiring Condition Detected**

| **Field** | **Value** |
| --- | --- |
| Lifecycle | Any |
| Reasoning Signals | TIME-SENSITIVE |
| Data Sufficiency | Sufficient |
| Judgment Intent | Trigger re-evaluation |
| Decision Types | WARN or BLOCK |
| Severity | Contextual |
| Notes | expiry_conditions required |

---

## **5. Explicit Non-Use Cases (Out of Scope)**

Judgment **does not** handle:

- generating recommendations
- proposing actions
- rewriting plans
- explaining decisions in prose
- learning from outcomes
- cross-project comparison

These belong to **Communication, Execution, or Learning layers**.

---

## **6. Coverage Guarantees**

This matrix guarantees coverage for:

- all lifecycle stages
- all reasoning signal categories
- all decision types
- all data sufficiency states

Any new Judgment behavior **must map to a new use case entry**.

---

## **7. Engineering Acceptance Rule**

> If a Judgment behavior cannot be mapped to
> 
> 
> **exactly one use case in this matrix**
> 

> it is
> 
> 
> **not v1-compliant**
> 

---

If you want, the next logical artifacts are:

- **Judgment → Governance Use Case Matrix**
- **Lifecycle × Use Case Compatibility Matrix**
- **Tier × Use Case Visibility Matrix**

Say which one to generate next.