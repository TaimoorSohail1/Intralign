# OSLO Contract Index (Engineer Onboarding Edition)

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Purpose:** Provide a single source of truth for **what contracts exist, where they live, and what they govern**

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** Canonical Index

---

## **How to Use This Document**

If you are new to OSLO:

1. **Read Sections 1–3 once**
2. Use **Section 4 (Contract Table)** as your reference
3. Treat **any contract listed here as non-negotiable**

> If behavior is not explicitly allowed by a contract, it is forbidden.
> 

---

## **1. Mental Model: What a “Contract” Means in OSLO**

A **contract** in OSLO is:

- A hard behavioral boundary
- Enforced by code, linting, and runtime guards
- Cross-referenced by multiple layers
- Designed to preserve **trust, determinism, and clarity**

Contracts are **stronger than playbooks**:

- Playbooks explain intent
- Contracts enforce reality

---

## **2. Contract Ownership Model**

Contracts fall into three categories:

### **A. Layer-Owned Contracts**

- Defined *inside* a layer playbook
- Enforced primarily by that layer
- Referenced by others

### **B. System Contracts**

- Apply across all layers
- Not owned by any single layer
- Never duplicated into playbooks

### **C. Implementation Contracts**

- Machine-enforceable artifacts
- Used directly by engineers (guards, matrices)

---

## **3. Reading Order (Recommended for New Engineers)**

1. **Project Knowledge Playbook v1.3**
2. **Reasoning Playbook v1.1**
3. **Judgment Playbook v1.2**
4. **Governance Playbook v1.3**
5. **System Reliability & Degradation Spec v1.0**
6. **Layer Violation Detection Rules v1.0**
7. **Governance Decision Matrix v1.0**

---

## **4. Canonical Contract Index**

### **4.1 Knowledge & Truth Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Project Knowledge Canon** | Layer | Knowledge | Schema + Commit Gate |
| **Snapshot Identity & Lineage** | Layer | Knowledge | Snapshot API |
| **Representation Drift Contract** | Layer | Knowledge | Drift Detector |
| **Versioning & Supersession** | Layer | Knowledge | Version Store |
| **Reasoning Read-Only Contract** | Layer | Reasoning | API Isolation |

---

### **4.2 Authorization & Mutation Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **UI-Authorized Mutation Rules (G-03)** | System | Governance | Commit Gate |
| **Authorization Scope & Lifetime** | Layer | Governance | Context Validator |
| **Onboarding Implicit Authorization** | Layer | Governance | Workflow Gate |

---

### **4.3 Ingestion & Input Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Ingestion & Transformation Contract v1.0** | System | Platform | Airlock Boundary |
| **Capture → Transform → Commit Boundary** | Layer | Knowledge | API Separation |
| **Raw Input Isolation** | System | Platform | Storage Partition |

---

### **4.4 Reasoning & Inference Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Evidence Chain Requirement** | Layer | Reasoning | Output Schema |
| **Determinism & Replayability** | Layer | Reasoning | Version Pinning |
| **Hypothetical Isolation** | Layer | Reasoning | Context Guard |
| **Placeholder Introduction Rules** | Layer | Reasoning | Output Flags |

---

### **4.5 Judgment & Scoring Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Conditional Scoring Contract** | Layer | Judgment | Score Schema |
| **Placeholder Semantics & Weighting** | Layer | Judgment | Confidence Model |
| **Volatility Detection** | Layer | Judgment | Delta Tracker |
| **Score → Signal Separation** | Layer | Judgment | Output Types |

---

### **4.6 Governance & Timing Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Governance Authority Boundary** | System | Governance | Capability Tokens |
| **Governance Decision Matrix v1.0** | Impl | Governance | Policy Engine |
| **Placeholder-Aware Suppression** | Layer | Governance | Decision Rules |
| **Surface Discipline (Chat Restrictions)** | Layer | Governance | Emission Gate |

---

### **4.7 Communication & Expression Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Conditional Explanation Patterns** | Layer | Communication | Template System |
| **Confidence Disclosure Rules** | Layer | Communication | Template Validation |
| **No-Action Implication Rule** | Layer | Communication | Phrase Linting |

---

### **4.8 System Reliability & Safety Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **System Reliability & Degradation Spec v1.0** | System | Platform | State Manager |
| **Safe Reliability State** | System | Platform | Global Kill-Switch |
| **Freeze / Last-Known-Good Rule** | System | Knowledge | Snapshot Control |

---

### **4.9 Enforcement & Integrity Contracts**

| **Contract** | **Type** | **Owned By** | **Enforced By** |
| --- | --- | --- | --- |
| **Layer Violation Detection Rules v1.0** | System | Platform | Lint + Runtime Guards |
| **Canonical Write Gate** | Impl | Platform | Commit Function |
| **Surface Emission Gate** | Impl | Platform | Emission API |
| **Determinism Gate** | Impl | Platform | Replay Validator |

---

## **5. Non-Negotiable Engineer Rules**

Every engineer working on OSLO must internalize:

1. **No layer writes canonical data without authorization**
2. **Reasoning never generates language**
3. **Judgment never decides timing or urgency**
4. **Governance never changes truth**
5. **Communication never implies action**
6. **If confidence is low, silence is preferred**
7. **Safe mode is success, not failure**

Violating these rules is a **trust incident**, not a style issue.

---

## **6. When You Are Unsure**

Ask yourself:

> “Which contract explicitly allows this behavior?”
> 

If you cannot name one:

- The behavior is forbidden
- Escalate before implementing

---

## **Canonical Close**

> OSLO works because its contracts are stricter than its code.
> 

> Engineers do not invent behavior —
> 

> they implement what the contracts already permit.
> 

---

If you want next, I can:

- Convert this into a **Notion database**
- Produce a **one-page architecture + contract map**
- Create an **engineer onboarding checklist (Day 1 / Week 1)**

Just tell me.