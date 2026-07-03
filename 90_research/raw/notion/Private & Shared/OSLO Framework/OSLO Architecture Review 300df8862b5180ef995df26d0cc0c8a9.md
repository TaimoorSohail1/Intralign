# OSLO Architecture Review

## **Intelligence Modules vs Agent-Based Layer Design**

**Audience:** OSLO Engineering Leadership

**Purpose:** Provide architectural guidance on implementing OSLO layers using an agent-based execution model while preserving determinism, auditability, and governance guarantees.

---

## **Executive Summary**

The current proposal from engineering leadership is to implement each OSLO layer as an independent, schema-typed “agent” with:

- Explicit input/output contracts (Pydantic models)
- Strict tool whitelisting
- Stateless execution
- Scoped access to shared project memory
- Validated inter-layer communication
- Deterministic orchestration via Pydantic AI

This proposal is **architecturally sound** and aligns well with OSLO’s long-term goals **if certain invariants are enforced**.

However, it is critical to clarify:

> This design should be understood as a
> 
> 
> **contract-driven modular pipeline executed via an agent runtime**
> 

OSLO is a governance and orchestration system. Its architecture must remain:

- deterministic at control boundaries,
- auditable,
- replayable,
- benchmarkable,
- and explainable.

Agent flexibility must exist **inside layers**, not across system control.

---

## **Context: The Architectural Question**

The earlier architectural discussion revolved around whether OSLO should be built as:

1. Intelligence modules in a deterministic pipeline, or
2. A distributed agent system with autonomous coordination.

The engineering proposal reframes this:

Each OSLO layer becomes an “agent,” but with strict contracts and deterministic orchestration.

This effectively combines both models.

---

## **Strengths of the Proposed Design**

### **1. Typed Contracts Enable Determinism**

Using Pydantic models for agent inputs and outputs ensures:

- deterministic interfaces,
- strict validation,
- schema stability,
- independent testing,
- safe composability.

Layers can evolve internally without breaking system contracts.

---

### **2. Tool Whitelisting Supports Governance**

Restricting which tools each agent may use:

- prevents authority creep,
- reduces accidental side effects,
- improves auditability,
- keeps execution boundaries clear.

This is essential for enterprise trust.

---

### **3. Stateless Agents Improve Testability**

Stateless agents avoid:

- hidden context accumulation,
- unpredictable memory effects,
- cross-run contamination.

This supports reproducibility and deterministic replay.

---

### **4. Chain-of-Custody is Preserved**

Validated outputs between layers create:

- traceable reasoning flow,
- replayable pipelines,
- auditable decision history.

This is foundational for future certification and benchmarking.

---

### **5. Layer Independence Accelerates Development**

Layers can be:

- built independently,
- versioned independently,
- tested independently,
- optimized independently.

This improves engineering velocity and maintainability.

---

## **The Core Risk**

Even with contracts and statelessness, agent internals remain **probabilistic**.

Risks include:

- semantic variation between runs,
- unstable thresholds,
- inconsistent outputs,
- flaky automated tests,
- non-reproducible reasoning.

Contracts validate **shape**, not **semantic stability**.

Therefore, probabilistic reasoning must not directly control system behavior.

---

## **Required Architectural Invariants**

To make this architecture safe and scalable, the following invariants must be enforced.

---

### **Invariant 1 — Deterministic Orchestration Graph**

Execution flow must remain deterministic.

Agents must NOT:

- dynamically call other agents,
- alter orchestration flow,
- create spontaneous execution paths.

Pipeline control belongs to orchestration policy.

---

### **Invariant 2 — Proposal vs Decision Separation**

AI layers must output proposals, not decisions.

Pattern:

```
Reasoning Agent → proposal
Judgment/Governance → decision
```

Example:

- Agent proposes severity.
- Governance layer applies deterministic thresholds.

This preserves control predictability.

---

### **Invariant 3 — Evidence-Carrying Outputs**

All outputs must include:

- evidence references,
- rationale,
- confidence,
- assumptions.

Otherwise explainability collapses.

Outputs must allow reconstruction of reasoning.

---

### **Invariant 4 — Memory Access Discipline**

Agents must not mutate shared state directly.

Correct pattern:

```
Read snapshot → propose patch → reducer applies change
```

State updates must flow through deterministic reducers.

---

### **Invariant 5 — Replayability & Test Harness Support**

System must support:

- replay of runs,
- versioned prompts,
- model version locking,
- context reconstruction,
- semantic diff evaluation.

Replay is essential for debugging and benchmarking.

---

### **Invariant 6 — Threshold Calibration Discipline**

Alerting and scoring must be calibrated:

- false positive budgets,
- confidence thresholds,
- dataset calibration,
- severity classification rules.

Otherwise alert fatigue destroys trust.

---

## **Clarifying Terminology**

Externally, OSLO should not be described as an “agent system.”

Preferred framing:

**Contract-driven orchestration pipeline with constrained reasoning components.**

This communicates:

- reliability,
- governance,
- enterprise readiness.

“Agent” terminology often implies autonomy and unpredictability.

---

## **Architectural Recommendation**

Proceed with the engineering proposal under the following interpretation:

- Each OSLO layer is implemented as a contract-bound reasoning component.
- Agent runtime executes layers.
- Internal reasoning may be probabilistic.
- External system control remains deterministic.
- Governance layers retain authority over execution actions.
- State changes are deterministic and auditable.

This yields:

- agent flexibility internally,
- modular determinism externally.

---

## **Execution Authority Constraint**

One critical decision remains:

Should agents be allowed to directly execute external actions?

Recommended constraint:

```
Agents propose actions
Governance dispatcher executes actions
```

All side effects should pass through a deterministic execution dispatcher.

This preserves:

- authority control,
- auditability,
- safety,
- intervention control.

---

## **Conclusion**

The engineering proposal is strong and aligned with OSLO’s goals.

However, OSLO must ensure:

- probabilistic reasoning does not equal probabilistic control,
- contracts define behavior,
- governance retains authority,
- reasoning remains auditable,
- system behavior remains reproducible.

With these constraints enforced, the architecture becomes:

**Flexible, composable, testable, deterministic, and future-proof.**

---

## **Final Guidance**

Adopt:

**Schema-typed layer agents executed via deterministic orchestration with strict governance boundaries.**

Avoid:

Unconstrained autonomous agent collaboration controlling system execution.

---

End of document.