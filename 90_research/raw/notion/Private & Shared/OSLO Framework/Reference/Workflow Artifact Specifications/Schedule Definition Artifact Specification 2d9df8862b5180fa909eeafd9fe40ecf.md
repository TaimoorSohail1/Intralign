# Schedule Definition Artifact Specification

---

**OSLO Knowledge Layer — Schedule Definition v1.2**

---

## **1. Purpose of the Schedule Definition Artifact**

The Schedule Definition defines the **temporal feasibility and execution readiness** of the plan by combining:

1. **Authoritative planning-time schedule elements** (milestones, dependencies, horizons), and
2. **Non-authoritative execution-time work objects** (tasks, work items, subtasks)

Schedule Definition exists to:

- validate whether outcomes can be achieved within the declared time horizon
- expose temporal conflicts and infeasible sequencing
- integrate execution reality without allowing it to redefine planning truth
- support milestone-based outcome tracking
- provide Charter-grade timeline summaries

> Schedule answers “when outcomes and structures must exist,” while work objects answer “what is being done to make that happen.”
> 

---

## **2. Authority Model (Critical Update)**

Schedule Definition contains **two authority tiers**:

### **Tier A — Planning-Time Schedule Elements (Authoritative)**

- Schedule Horizon
- Milestones
- Dependencies
- Duration Estimates
- Temporal Constraints
- Buffers / Slack

These elements:

- define temporal truth
- are judgment-authoritative
- require explicit human confirmation
- cannot be inferred for judgment

---

### **Tier B — Execution-Time Work Objects (Non-Authoritative)**

- Work Items
- Tasks
- Sub-tasks
- Epics / Stories (optional, workflow-specific)

These elements:

- may be **planning-authored** (by OSLO or humans)
- may be **execution-tracked** (synced from tools)
- are **evaluated for judgment signals**
- **never redefine** milestones, dependencies, or schedule truth unless explicitly promoted

This separation is non-negotiable.

---

## **3. Scope and Ownership**

### **What Schedule Definition owns (strictly)**

- Temporal structure and feasibility
- Milestone meaning and timing
- Dependency logic
- Execution signal evaluation

### **What Schedule Definition does not own**

- Outcomes or success definitions (Intent)
- Scope inclusions/exclusions (Scope)
- Structural completeness (WBS)
- Capacity truth (Resource Plan)

---

## **4. Design Principles (Updated)**

1. **Planning authority is explicit**
2. **Execution signals inform, not redefine**
3. **Milestones precede tasks**
4. **Outcome-aware scheduling**
5. **Inference-safe temporal reasoning**
6. **Judgment-weighted execution signals**

---

## **5. Schedule Object Model**

All Schedule Elements carry:

- element_type
- source_state (explicit / derived / inferred / synced)
- authority_tier (Planning / Execution)

---

## **6. Schedule Fields — Structured (Planning-Time, Authoritative)**

### **6.1 Schedule Horizon — Soft Required**

| **Field** | **Description** |
| --- | --- |
| Schedule Start Window | Earliest feasible start |
| Schedule End Window | Latest acceptable completion |

**Invariant**

- Must align with Intent Time Horizon
- Misalignment triggers feasibility issues

---

### **6.2 Milestones (1..n) —**

### **Required**

Each Milestone includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Milestone Name | **Hard Required** | Outcome- or deliverable-based |
| Milestone Type | Soft Required | Outcome / Deliverable / Phase / Decision |
| Target Date or Window | **Hard Required** | Date or bounded range |
| Supported Outcome(s) | Soft Required | Outcomes advanced |
| Critical Path Flag | Optional | On critical path or not |

**Invariants**

- At least one milestone required
- Milestones define temporal intent
- Milestones must not be task-based

---

### **6.3 Dependencies (0..n) — Judgment-Critical**

Each Dependency includes:

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Predecessor | **Hard Required** | Milestone or WBS element |
| Successor | **Hard Required** | Milestone or WBS element |
| Dependency Type | Soft Required | FS / SS / FF / SF |
| Constraint Strength | Optional | Hard / Soft |

**Invariants**

- Cycles are invalid
- Dependencies cannot be inferred for judgment

---

### **6.4 Duration Estimates (Optional)**

Used to support feasibility math.

| **Field** | **Description** |
| --- | --- |
| Duration | Time required |
| Confidence Level | High / Medium / Low |
| Basis of Estimate | Historical / Expert / Assumption |

---

## **7. Execution Sub-Layer — Work Objects (Updated Scope)**

### **7.1 Work Object Definition**

Work Objects are **execution primitives** that operationalize WBS elements.

They may be:

- OSLO-proposed (planning-authored)
- User-created
- Tool-synced

They **always belong to the Execution Authority Tier**.

---

### **7.2 Work Object Fields**

| **Field** | **Requirement** | **Description** |
| --- | --- | --- |
| Work Object ID | **Hard Required** | Unique identifier |
| Type | Soft Required | Task / Sub-task / Epic / Story |
| Title | **Hard Required** | Short execution description |
| Status | Soft Required | Open / In Progress / Blocked / Done |
| Effort Estimate | Optional | Hours / points |
| Start / Due Date | Optional | Execution timing |
| Linked WBS Element | **Hard Required** | Structural anchor |
| Linked Milestone(s) | Optional | Progress tracking |
| Source State | Derived | explicit / proposed / synced |

---

### **7.3 Structural Rules (Unchanged but Reinforced)**

- Every Work Object must map to **exactly one WBS Element**
- Work hierarchies may exist **only within execution**
- Execution hierarchies never replace WBS
- Orphaned work always triggers issues

---

## **8. Promotion Rule (New, Explicit)**

> No Work Object may affect planning-time schedule elements unless explicitly promoted by a human action.
> 

Promotion examples:

- Task → Milestone
- Task dependency → Schedule Dependency
- Task date → Target Milestone Date

Promotion:

- creates a new planning element
- requires confirmation
- preserves audit trail

---

## **9. Judgment Coverage (Updated)**

Work Objects are evaluated with **bounded impact**.

### **9.1 Clarity (Signal-Level)**

- Orphaned work
- Conflicting execution boundaries
- Excessive churn or rework

Impact:

→ Clarity confidence reduction (capped)

---

### **9.2 Alignment (Signal-Level)**

- Work skewed toward low-priority outcomes
- Work under weakly-aligned WBS branches

Impact:

→ Alignment risk issues (non-authoritative)

---

### **9.3 Feasibility (Primary Execution Impact)**

- Burn vs capacity
- Blocked critical-path work
- Throughput vs milestone timing

Impact:

- Feasibility confidence reduction
- Early risk detection
- **Execution signals may only decrease feasibility confidence, never increase it**

---

## **10. Weighting & Stability Rules (Conceptual, Locked)**

- Planning artifacts dominate health scores (≥70%)
- Work-object contribution is capped (≤30%)
- Negative signals outweigh positive ones
- Volatility is dampened (no oscillation)

---

## **11. Inference Rules (Updated)**

- OSLO may **propose** work objects freely
- OSLO may **analyze** execution patterns
- OSLO may **not** infer:
    - milestones
    - dependencies
    - authoritative dates
- Inferred or synced execution data never substitutes for planning truth

---

## **12. Charter Coverage**

Derived from Schedule Definition:

- Key milestones
- Timeline summary
- Major dependencies
- Execution risk signals (summarized, not detailed)

Work objects themselves do **not** appear in Charter reports.

---

## **13. Invariants (Locked)**

1. Schedule Definition contains both planning and execution layers
2. Planning elements define temporal truth
3. Work objects inform judgment with bounded impact
4. Execution may reduce confidence, never redefine intent
5. Promotion is the only path from execution to planning authority
6. Orphaned work is always an issue

---

## **14. Canonical Summary**

> Schedule Definition integrates planning authority with execution reality. Milestones define when success must exist; work objects reveal how execution is unfolding—without ever being allowed to redefine the plan.
> 

---

If you want, next we can:

- update the **cross-artifact dependency matrix** to reflect this revision, or
- formalize **promotion workflows & permissions**, or
- codify **health score contribution math** in a deterministic spec

Just tell me which direction to go.