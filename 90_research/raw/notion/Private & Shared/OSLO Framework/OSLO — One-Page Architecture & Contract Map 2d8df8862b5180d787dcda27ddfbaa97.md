# OSLO — One-Page Architecture & Contract Map

---

**Purpose:** Show **what exists**, **who owns truth**, and **which contracts gate behavior**

**Audience:** Engineering, AI/ML, Platform, QA

**Status:** Canonical reference

---

## **1. High-Level Architecture (Vertical Truth Flow)**

```
┌──────────────────────────────┐
│        User / External       │
│  (UI, Docs, APIs, Signals)   │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│ Ingestion & Transformation   │
│ (parse, extract, propose)    │
│ NON-CANONICAL                │
│ ──────────────────────────── │
│ Contract: Ingestion v1.0     │
└───────────────┬──────────────┘
                │  (UI authorization only)
                ▼
┌──────────────────────────────┐
│   Project Knowledge Layer    │
│   (canonical truth store)    │
│ ──────────────────────────── │
│ Contracts:                   │
│ • G-03 Mutation Rules        │
│ • Snapshot Identity          │
│ • Representation Drift       │
│ • Versioning & Supersession  │
└───────────────┬──────────────┘
                │  (immutable snapshot)
                ▼
┌──────────────────────────────┐
│        Reasoning Layer       │
│ (structure, gaps, inference) │
│ READ-ONLY                    │
│ ──────────────────────────── │
│ Contracts:                   │
│ • Read-Only Contract         │
│ • Evidence Chains            │
│ • Determinism & Replay       │
└───────────────┬──────────────┘
                │  (signals only)
                ▼
┌──────────────────────────────┐
│        Judgment Layer        │
│ (scores, confidence, flags)  │
│ ──────────────────────────── │
│ Contracts:                   │
│ • Conditional Scoring        │
│ • Placeholder Semantics      │
│ • Volatility Detection       │
└───────────────┬──────────────┘
                │  (permission check)
                ▼
┌──────────────────────────────┐
│       Governance Layer       │
│ (timing, suppression,        │
│  authorization scope)        │
│ ──────────────────────────── │
│ Contracts:                   │
│ • Authority Boundary         │
│ • Authorization Scope        │
│ • Decision Matrix            │
│ • Placeholder-Aware Rules    │
└───────────────┬──────────────┘
                │  (approved emission)
                ▼
┌──────────────────────────────┐
│     Communication Layer      │
│ (language & explanation)     │
│ ──────────────────────────── │
│ Contracts:                   │
│ • Conditional Explanation   │
│ • Confidence Disclosure     │
│ • No-Action Implication      │
└──────────────────────────────┘
```

---

## **2. Horizontal System Contracts (Apply Everywhere)**

These **override layer logic**.

```
┌────────────────────────────────────────────┐
│ System Reliability & Degradation Spec v1.0 │
│ States: Normal → Degraded → Constrained →  │
│ SAFE (fail-silent)                          │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Layer Violation Detection Rules v1.0        │
│ • Unauthorized mutation → SAFE              │
│ • Governance bypass → SAFE                  │
│ • Raw input leakage → SAFE                  │
└────────────────────────────────────────────┘
```

---

## **3. Canonical Contract Ownership Map**

| **Area** | **Contract** | **Owner** |
| --- | --- | --- |
| Mutation | UI-Authorized Mutation Rules (G-03) | Governance |
| Ingestion | Ingestion & Transformation Contract | System |
| Truth | Project Knowledge Canon | Knowledge |
| Snapshots | Snapshot Identity & Lineage | Knowledge |
| Drift | Representation Drift Contract | Knowledge |
| Inference | Read-Only Reasoning Contract | Reasoning |
| Scoring | Placeholder Semantics | Judgment |
| Timing | Governance Decision Matrix | Governance |
| Safety | Safe Reliability State | System |

---

## **4. Absolute Boundaries (Never Cross)**

### **🚫 Forbidden Paths**

- Reasoning → Knowledge (write)
- Judgment → Governance (decision)
- Governance → Knowledge (mutation)
- Communication → anything upstream
- Any layer → Chat without Governance approval

### **✅ Only Legal Write Path**

```
UI Action → Authorization Context → Knowledge Commit Gate
```

---

## **5. 60-Second Workflow (Special Case Overlay)**

```
User Intent
   ↓
Implicit Authorization (time-boxed)
   ↓
Ingestion proposes + Reasoning scaffolds
   ↓
Knowledge initialized (low-certainty placeholders)
   ↓
Judgment scores (conditioned_on_placeholders = true)
   ↓
Governance suppresses interrupts
   ↓
Communication = summary only
```

**Key rule:**

60-Second authorization **expires immediately** after onboarding.

---

## **6. Engineer Safety Checklist (One-Glance)**

Before shipping code, confirm:

- ❑ Am I mutating Knowledge? → where is authorization?
- ❑ Am I inferring? → does it stay proposed or inferred?
- ❑ Am I scoring? → is placeholder conditioning explicit?
- ❑ Am I surfacing? → where is the GovernanceDecision?
- ❑ Am I uncertain? → is silence allowed?
- ❑ Could this fail? → what happens in SAFE?

If any answer is unclear → **stop**.

---

## **Canonical Close**

> OSLO’s architecture is simple on purpose.
> 

> Complexity lives in contracts, not code paths.
> 

> If you respect the map, the system remains trustworthy.
>