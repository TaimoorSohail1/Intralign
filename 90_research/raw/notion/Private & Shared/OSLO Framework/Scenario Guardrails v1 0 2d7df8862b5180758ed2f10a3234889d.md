# Scenario Guardrails v1.0

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Scope:** OSLO Communication Engine — Governance

**Status:** Canonical / Non-Negotiable

**Applies To:** All governance scenarios, state machines, policies, and implementations

---

## **Purpose**

Scenario Guardrails define **global, invariant constraints** on OSLO behavior.

They exist to ensure:

- Product intent remains stable as scenarios evolve
- Trust is not eroded by “technically correct” but behaviorally wrong implementations
- Governance logic is implemented consistently across teams and AI-assisted workflows
- Authority boundaries between chat, UI, and system layers are never blurred

> If a scenario, policy, or implementation conflicts with a guardrail, the guardrail wins.
> 

---

## **Authority Hierarchy**

Guardrails have higher authority than:

- Scenarios
- State machines
- Policy tables
- Implementation details

Only the **Layer Playbooks** outrank guardrails.

---

## **G-01 — Evaluation Embargo Before Plan Presentation**

### **Rule**

OSLO must not surface **any evaluative artifacts** before the plan is fully generated and presented to the user.

### **This Prohibits**

- Issues
- Warnings
- Critiques
- Health scores
- Validation prompts

during:

- Input capture
- Plan generation

### **Allowed**

- Educational messages
- Forward-looking explanations
- Process narration (“Here’s what I’m doing next…”)

### **Rationale**

Users must never feel judged on partial or unseen work.

---

## **G-02 — Disclosure Is Not Computation**

### **Rule**

Internal computation may occur at any time, but **user disclosure is strictly gated by governance state**.

### **This Means**

- Reasoning and judgment may run early for performance reasons
- Their outputs are embargoed until disclosure is allowed
- Engineers must not equate “computed” with “shown”

### **Violated If**

- Scores, issues, or critiques appear simply because they were already computed

### **Rationale**

Trust requires separation between *system readiness* and *user readiness*.

---

## **G-03 — Explicit User-Authorized UI Actions Are the Only Source of Plan Mutation**

### **Rule**

All canonical project plan mutations must originate from **explicit user-authorized UI actions**.

### **Clarified Semantics (Important)**

- **Artifact UI edits** and **panel-based fixes** are authoritative
- **Chat is advisory and initiatory, not authoritative**

Chat **may**:

- Explain issues
- Suggest fixes
- Recommend actions
- Present CTA buttons (e.g., “Apply Fix”, “Update Scope”)

Chat **may not**:

- Mutate artifacts on its own
- Apply fixes without user authorization
- Trigger recompute as if a change occurred

### **Authorization Boundary**

A plan mutation occurs **only after**:

- The user explicitly clicks a CTA, or
- The user performs an equivalent UI confirmation action

Once confirmed:

- The mutation is treated identically to a direct UI edit
- Recompute occurs
- Issues are removed or revised
- Health scores update
- Chat remains silent unless a new critical blocker is introduced

### **Rationale**

Users must always understand **what changed, when, and why**.

---

## **G-04 — Validation Requires Timing Restraint**

### **Rule**

Inferences and assumptions may only be raised for validation **after the user has had an opportunity to view the plan**.

### **Minimum Conditions (at least one must be true)**

- User opens the plan or issues panel
- A short post-generation idle window elapses
- User explicitly asks a validation-related question

### **Rationale**

Immediate critique feels punitive; delayed validation feels collaborative.

### **Violated If**

- Validation prompts appear immediately upon plan completion

---

## **G-05 — Hypothetical Analysis Must Be Isolated**

### **Rule**

“What-if” or hypothetical analysis must never affect canonical project state unless explicitly confirmed via UI.

### **Requirements**

- Use a sandboxed evaluation context
- Clearly label outputs as non-binding
- Do not update artifacts, issues, or scores

### **Rationale**

Exploration must be safe, reversible, and clearly distinguished from reality.

---

## **G-06 — Chat Is the Most Restricted Surface**

### **Rule**

Chat is reserved for:

- Education
- Next-step guidance
- Explicit user questions
- High-impact, interruption-worthy conditions

### **Chat Must Not**

- Enumerate all issues
- Narrate routine system activity
- React to every recompute

### **Rationale**

Chat carries emotional weight and must be used sparingly.

---

## **G-07 — Silence Is a Valid and Often Correct Outcome**

### **Rule**

Governance must explicitly allow **no communication** as a correct and intentional decision.

### **This Means**

- No message is preferable to a weak message
- Suppression ≠ deletion
- Silence must be deliberate and auditable

### **Rationale**

Restraint is a feature, not a failure.

---

## **G-08 — Accountability Scales With Exposure**

### **Rule**

The visibility of a correction must scale with the visibility of the original communication.

### **Examples**

- Chat-delivered error → explicit chat correction
- Panel-only message → silent supersession allowed

### **Rationale**

Trust depends on owning mistakes proportionally.

---

## **How These Guardrails Are Used**

- **Scenarios** reference applicable guardrails (e.g., G-01, G-03)
- **State machines** encode guardrails as transition guards
- **PR reviews** cite guardrail IDs for acceptance or rejection
- **QA tests** assert guardrail invariants
- **AI-assisted coding** uses guardrails as hard constraints

---

## **Canonical Reminder**

> Guardrails protect OSLO from doing the wrong thing correctly.
> 

They are:

- Not heuristics
- Not suggestions
- Not optional

They are the system’s **behavioral constitution**.

---

### **Next Logical Step**

With guardrails now clarified and stable, the system is ready for:

👉 **Governance State Machine v1.1**, encoding:

- InputCapture → PlanGenerating → PlanPresented
- User-initiated vs system-initiated paths
- Guarded transitions referencing G-01 through G-08

If you want, I can proceed to update the state machine with these guardrails explicitly embedded.