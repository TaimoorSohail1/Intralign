# Reasoning Layer Use Case Matrix v1.0

---

**System:** OSLO

**Layer:** Reasoning

**Audience:** Engineering, Product, QA

**Status:** Canonical

---

## **1. Use Case Classification**

Reasoning use cases are classified by **trigger intent**, not UI surface.

| **Class** | **Description** |
| --- | --- |
| **Initialization** | Establish baseline structural truth |
| **Validation** | Detect gaps, inconsistencies, fragility |
| **Impact Analysis** | Assess downstream structural effects |
| **Hypothetical Simulation** | Explore “what-if” without canon mutation |
| **Incremental Recompute** | Efficient re-evaluation after change |
| **Monitoring Support** | React to new signals from execution/telemetry |

---

## **2. Core Use Case Matrix**

| **UC ID** | **Use Case** | **Trigger** | **Input Scope** | **Reasoning Passes** | **Outputs** | **Invariants Emphasized** |
| --- | --- | --- | --- | --- | --- | --- |
| R-UC-01 | Initial Structural Baseline | Project created / first load | Full canonical snapshot | Pass 1–3 | Issues, signals, evidence chains | I-01, I-04, I-06 |
| R-UC-02 | Planning Completeness Check | User requests validation | Canonical artifacts | Pass 1–3 | Gaps, inferred elements | I-08, I-10 |
| R-UC-03 | Alignment Consistency Detection | Artifact update | Affected subgraph | Pass 2–3 | Alignment issues | I-02, I-05 |
| R-UC-04 | Feasibility Stress Detection | Schedule/resource edit | Dependency graph | Pass 2–3 | Feasibility signals | I-04, I-06 |
| R-UC-05 | Dependency Impact Analysis | Requirement change | Transitive closure | Pass 3 | Impacted elements, issues | I-04 |
| R-UC-06 | Assumption Density Analysis | Explicit assumptions added | Canonical + assumptions | Pass 3 | Assumption density signals | I-12 |
| R-UC-07 | Hypothetical Scenario Simulation | What-If request | Isolated snapshot | Pass 1–3 (isolated) | Hypothetical issues/signals | I-13 |
| R-UC-08 | Incremental Recompute | Authorized mutation | Delta graph | Pass 4 | Updated issues/signals | I-06 |
| R-UC-09 | Execution Drift Detection | External sync event | Execution facts + canon | Pass 3 | Drift signals | I-04, I-14 |
| R-UC-10 | Evidence Replay | Audit request | Stored snapshots | Replay only | Reproduced outputs | I-07 |
| R-UC-11 | Failure-Mode Reasoning | Missing structure | Partial graph | Pass 1–3 (incomplete) | Partial signals + limitations | I-14 |

---

## **3. Detailed Use Case Descriptions (Selected)**

### **R-UC-01 — Initial Structural Baseline**

**Purpose:** Establish ground truth for the project’s structure.

**Key rule:** No inference until Pass 2.

**Failure condition:** Missing mandatory artifacts → record limitations, do not fabricate.

---

### **R-UC-05 — Dependency Impact Analysis**

**Purpose:** Determine what downstream elements are structurally affected by a change.

**Output:** Affected elements list + evidence chain.

**Explicit non-output:** No severity, no recommendation.

---

### **R-UC-07 — Hypothetical Scenario Simulation**

**Purpose:** Explore alternative structural realities without contaminating canon.

**Key constraint:** Must run in isolated context; outputs tagged HYPOTHETICAL.

**Invariant:** Hypotheticals never persist or influence canonical runs.

---

### **R-UC-09 — Execution Drift Detection**

**Purpose:** Identify divergence between planned structure and execution reality.

**Inputs:** Read-only execution facts.

**Outputs:** Drift signals only (no action proposals).

---

## **4. Explicit Non-Use Cases (Out of Scope)**

The Reasoning Layer **does not support**:

| **Category** | **Reason** |
| --- | --- |
| Action recommendation | Violates I-02 |
| Scoring or prioritization | Judgment responsibility |
| User prompting or Q&A | Communication responsibility |
| Direct execution | Execution Coordination (future) |
| Canonical updates | Knowledge + Governance only |

---

## **5. Input → Output Mapping Summary**

| **Input Change** | **Reasoning Reaction** |
| --- | --- |
| New artifact added | Recompute structural completeness |
| Artifact modified | Incremental recompute on affected subgraph |
| Assumption added | Update assumption density + evidence |
| External execution update | Drift detection only |
| Hypothetical input | Isolated reasoning run |

---

## **6. QA Acceptance Hooks**

Each use case must verify:

- Evidence chain exists
- Determinism across replays
- No canonical mutation
- Correct context tagging
- No layer violations

---

## **7. Invariant Coverage Check**

| **Invariant** | **Covered By** |
| --- | --- |
| I-01 (No mutation) | All |
| I-04 (Structural truth) | All |
| I-06 (Determinism) | R-UC-01, 08, 10 |
| I-08 (Evidence required) | All |
| I-13 (Hypothetical isolation) | R-UC-07 |
| I-14 (No fabrication) | R-UC-11 |

---

## **Canonical Close**

> Reasoning is triggered by change,
> 

> constrained by structure,
> 

> and judged elsewhere.
> 

---

### **Next logical artifacts**

- **Use Case → Gherkin Test Mapping**
- **Reasoning Variant Matrix (60-Second vs Deep Audit)**
- **Incremental Recompute Dependency Rules**

Say which one to publish next.