# OSLO Layer Conflict Resolution Matrix (v1.0)

---

## **1. Resolution principles (non-negotiable)**

**Invariant rules**

1. **No layer may override another layer**
2. **Conflicts are detected by layers, resolved by the system**
3. **Governance always has veto power**
4. **Resolution ≠ erasure** (conflict must remain observable)

---

## **2. Precedence hierarchy (used by the system)**

| **Priority** | **Layer** | **Role in conflict** |
| --- | --- | --- |
| P0 | **Governance** | Hard constraints, safety, compliance |
| P1 | **Judgment** | Tradeoff decisions within allowed bounds |
| P2 | **Reasoning** | Logical derivation and inference |
| P3 | **Knowledge** | Facts, inferences, assumptions |
| P4 | **Communication** | Presentation only (never decision-making) |

> Note:
> 

> It defines
> 
> 
> **blocking power**
> 
> **resolution power**
> 

---

## **3. Conflict resolution matrix**

### **Legend**

- **Detect** = layer may flag the conflict
- **Resolve** = system-level orchestration only
- **Outcome** = what the system is allowed to do

---

### **A. Knowledge ↔ Reasoning**

| **Conflict** | **Example** | **Detecting layer** | **System resolution options** |
| --- | --- | --- | --- |
| Missing facts vs inferred logic | Reasoning needs inputs Knowledge doesn’t have | Reasoning | • Mark inference as provisional• Downgrade confidence• Require Pass 2 confirmation |
| Conflicting evidence | Two sources disagree | Knowledge | • Preserve both claims• Require Judgment to weigh evidence |
| Over-extension | Reasoning extrapolates beyond data | Knowledge | • Clip inference scope• Annotate epistemic risk |

❌ Knowledge may **not fabricate**

❌ Reasoning may **not assume facts into existence**

---

### **B. Reasoning ↔ Judgment**

| **Conflict** | **Example** | **Detecting layer** | **System resolution options** |
| --- | --- | --- | --- |
| Optimal vs acceptable | Reasoning says “best,” Judgment says “too risky” | Judgment | • Prefer Judgment outcome• Preserve rejected rationale |
| Logical validity vs human tradeoff | Reasoning correct but misaligned to intent | Judgment | • Override recommendation• Require explanation surface |
| Ambiguity tolerance | Reasoning unsure, Judgment wants action | Reasoning | • Force conservative posture• Require user confirmation |

❌ Judgment may **not alter reasoning chains**

❌ Reasoning may **not decide tradeoffs**

---

### **C. Judgment ↔ Governance**

| **Conflict** | **Example** | **Detecting layer** | **System resolution options** |
| --- | --- | --- | --- |
| Speed vs policy | Judgment wants fast plan, Governance forbids inference | Governance | • Block action• Offer compliant alternatives |
| Value vs safety | Judgment favors benefit, Governance sees risk | Governance | • Enforce constraint• Escalate to user |
| Tier mismatch | Judgment assumes Pro behavior on Free tier | Governance | • Degrade capability• Surface upgrade path |

**Governance is absolute.**

There is **no override path**.

---

### **D. Governance ↔ Communication**

| **Conflict** | **Example** | **Detecting layer** | **System resolution options** |
| --- | --- | --- | --- |
| Simplification vs truth | Communication wants clarity, Governance requires disclosure | Governance | • Force explicit disclosure• Block simplification |
| Confidence signaling | Communication implies certainty | Governance | • Require epistemic labeling |
| UX vs auditability | Communication hides rationale | Governance | • Mandate rationale visibility |

❌ Communication may **never soften governance constraints**

---

### **E. Judgment ↔ Communication**

| **Conflict** | **Example** | **Detecting layer** | **System resolution options** |
| --- | --- | --- | --- |
| Nuance vs brevity | Judgment requires explanation | Judgment | • Expand explanation• Delay output |
| Human trust | Communication wants reassurance | Judgment | • Allow tone shift only• Preserve substance |

Communication is **presentation only** — it cannot reinterpret decisions.

---

## **4. System-level resolution actions (the only allowed actions)**

When a conflict occurs, the **system** may choose one or more:

| **Action** | **Description** |
| --- | --- |
| **Block** | Prevent output entirely |
| **Degrade** | Reduce fidelity or scope |
| **Annotate** | Explicitly surface conflict |
| **Escalate** | Require user input |
| **Fork** | Present multiple compliant paths |
| **Re-posture** | Switch speed/accuracy/accountability mode |

---

## **5. What this prevents (critically)**

This matrix **explicitly prevents**:

- Hallucination under pressure
- Silent policy violations
- “Helpful” but ungoverned behavior
- Communication-layer deception
- Reasoning laundering through UX

Without this matrix, OSLO collapses into:

> “the model felt confident, so we shipped it.”
> 

---

## **6. Engineering takeaway (the test)**

Ask your engineering lead one question:

> “Where is conflict resolved, and how does the system preserve the disagreement?”
> 

If they answer:

- “In the layer” → ❌ wrong
- “By the model” → ❌ wrong
- “By orchestration with contracts” → ✅ correct

---

If you want next, I recommend:

- **Layer Conflict State Machine (diagram + states)**
- **Conflict Resolution Contract (schema)**
- **BDD/Gherkin test matrix for conflicts**

Those are the next artifacts required before implementation.