# OSLO Architecture Approaches — One-Pager

---

**Decision Question**

Should OSLO be built using a **traditional workflow/state-machine architecture**, or a **layered agentic orchestration model with deterministic enforcement**?

---

## **Option A — Traditional Workflow / State-Machine Architecture**

### **What it is**

- Explicit workflows (BPMN, state machines, custom orchestration code)
- Hard-coded transitions and branches
- Logic embedded in services and handlers

### **Strengths**

- Predictable execution paths
- Easy to reason about single flows
- Strong static guarantees
- Familiar to many engineers

### **Limitations**

- Slow to evolve as flows grow
- Branch explosion for real-world exceptions
- Rigid when integrating external tools
- Complex logic spreads across services
- High cost to support variability (tiers, postures, lifecycle)

### **Operational Reality**

- Early velocity is moderate
- Maintenance cost grows non-linearly
- Every new edge case adds code + tests + state

---

## **Option B — Layered Agentic Orchestration + Deterministic Enforcement**

### **What it is**

- An **orchestrator agent** sequences work and adapts to context
- **Specialist agents** propose steps or gather information
- **Deterministic layers** (Knowledge, Reasoning, Judgment, Governance, Execution) enforce constraints via contracts, schemas, and tests
- Agents **cannot bypass enforcement layers**

### **Strengths**

- Faster iteration on complex, multi-step flows
- Naturally handles variability and exceptions
- Easier integration with external tools
- Logic centralized in contracts instead of code branches
- Behavior adaptable without rewiring architecture

### **Risks (if done incorrectly)**

- Authority creep if agents are not bounded
- Hard-to-debug behavior if invariants aren’t enforced
- Prompt-driven logic becomes business logic (anti-pattern)

### **Operational Reality**

- Fast early velocity **if contracts are locked**
- Maintenance is cheaper when policies change
- Behavior remains inspectable with observability + artifacts

---

## **The Critical Design Choice (This Determines Success)**

| **Dimension** | **Traditional Workflow** | **Layered Agentic Orchestration** |
| --- | --- | --- |
| Who decides? | Code paths | **Judgment layer only** |
| Who enforces rules? | Scattered services | **Deterministic governance + validators** |
| Who sequences steps? | Hard-coded | **Orchestrator agent** |
| Where logic lives | Code + workflows | **Contracts + invariants + tests** |
| Adaptability | Low | High |
| Debuggability | Good early, poor later | Strong if observability exists |
| Maintenance cost | Increases sharply | Flatter over time |

---

## **When Each Approach Wins**

### **Choose Traditional Workflow if**

- Flows are short and stable
- Few external integrations
- Low variability by tier/posture
- Minimal autonomy required

### **Choose Layered Agentic Orchestration if**

- Flows are long, variable, and evolving
- Multiple external systems involved
- Execution posture varies (manual → assistive → auto)
- Trust, auditability, and learning matter
- You expect rapid iteration in early phases

---

## **Recommended Approach for OSLO**

**Layered Agentic Orchestration with deterministic enforcement**

**Key constraints (non-negotiable):**

- Agents may **coordinate**, not authorize
- All actions require **Judgment artifacts**
- Governance gates all execution
- Invariants, validators, and tests block violations
- Observability is mandatory

This preserves speed **without** sacrificing trust or control.

---

## **One-Line Summary (Engineering-safe)**

> Agents for coordination. Deterministic layers for authority.
> 

> Fast to build, safe to scale, and easier to maintain.
> 

---

If you want, next I can:

- convert this into a **diagram slide**
- add a **“phased rollout” plan (MVP → Beta → GA)**
- or tailor this one-pager to **engineering vs product audiences**