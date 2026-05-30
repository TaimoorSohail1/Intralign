# Relational Database Schema vs OSLO Design Intent

---

## **High-level verdict**

This schema is **impressively complete** for a first pass and shows real alignment with the layered model.

However, in its current form it has **four structural risks** that would undermine OSLO’s core guarantees:

1. **Epistemic collapse** (facts, inferences, judgments blended)
2. **Temporal flattening** (loss of decision history)
3. **Governance dilution** (policy as attributes, not first-class events)
4. **Communication hallucination risk** (RCUs insufficiently constrained)

All four are fixable without blowing up the schema.

---

## **1. Epistemic state is not first-class enough**

### **Misalignment**

You have epistemic concepts spread across:

- ELEMENTVERSION (asserted, inferred, assumptions)
- REASONINGEVENT (findings, evidence)
- JUDGMENTEVENT (confidence, severity)
- ARTIFACT / ELEMENT

But **epistemic status is not a universal invariant**.

Right now:

- Some tables encode epistemic meaning
- Others implicitly assume it
- Some omit it entirely

This violates a core OSLO rule:

> If it influenced a decision, its epistemic status must be explicit and queryable.
> 

### **Risk**

You will not be able to:

- reconstruct *why* something was believed
- distinguish asserted vs inferred data globally
- safely evolve reasoning logic

Over time, engineers will “just trust the latest row.”

### **Fix**

Introduce a **universal epistemic envelope** pattern.

Minimal fix (low disruption):

- Add to **every table that represents knowledge or interpretation**:
    - epistemic_status ENUM (asserted, inferred, assumed, observed, unknown)
    - epistemic_source ENUM (user, system, execution, external)
    - confidence FLOAT NULL

At minimum:

- ARTIFACT
- ELEMENT
- REASONINGEVENT
- JUDGMENTEVENT
- GOVERNANCEEVENT
- COMMUNICATIONEVENT

This enforces epistemic honesty system-wide.

---

## **2. ReasoningEvent is doing too much semantic work**

### **Misalignment**

REASONINGEVENT includes:

- finding_type
- finding_text
- evidence_ref

This subtly turns reasoning outputs into **semi-conclusions**, not proposals.

In OSLO:

- Reasoning produces *candidate claims*
- It does not “find” truth

### **Risk**

Judgment logic will be built assuming Reasoning outputs are authoritative.

You lose clean epistemic → normative separation.

### **Fix**

Rename and restructure conceptually (no need to rename table if costly):

- Treat each REASONINGEVENT row as a **proposal**
- Add:
    - proposal_status ENUM (candidate, withdrawn, superseded)
    - superseded_by_reasoning_event_id

Optional but powerful:

- Separate EVIDENCE_NODE table
- Let Reasoning assemble chains without asserting findings

---

## **3. JudgmentEvent lacks explicit normative frames**

### **Misalignment**

JUDGMENTEVENT has:

- severity
- confidence
- health_score

But *what standard* these are measured against is implicit.

Judgment in OSLO is not free-form scoring.

It evaluates against:

- outcome intent
- CAF dimensions
- tolerance thresholds
- posture context

### **Risk**

Judgment becomes:

- opaque
- hard-coded
- impossible to audit or evolve

### **Fix**

Add explicit normative references:

In JUDGMENTEVENT:

- normative_frame_id
- health_dimension ENUM (clarity, alignment, feasibility)
- threshold_applied

Optionally:

- separate NORMATIVEFRAME table (versioned)

This preserves Judgment as **rule-based interpretation**, not intuition.

---

## **4. GovernanceEvent is modeled as a record, not a control system**

### **Misalignment**

GOVERNANCEEVENT contains:

- disposition
- action_allowed
- policy_version

But governance in OSLO is not a passive record.

It is an **active constraint system**.

### **Risk**

Governance degenerates into:

- “last decision wins”
- attribute flags
- scattered checks in application code

That breaks:

- posture enforcement
- disclosure control
- fail-closed guarantees

### **Fix**

Make governance decisions **composable and inspectable**.

Minimal changes:

- Add decision_class ENUM (suppress, expose, defer, escalate, authorize)
- Add scope ENUM (communication, execution, recompute)
- Add expires_at

Stronger fix:

- Split:
    - GOVERNANCEDECISION
    - GOVERNANCEPOLICYREFERENCE

This keeps governance authoritative and evolvable.

---

## **5. CommunicationEvent risks becoming an explanation store**

### **Misalignment**

COMMUNICATIONEVENT includes:

- diagnostic
- why_narrative
- how_narrative

This is extremely dangerous in OSLO.

Why?

Because it suggests Communication *creates narrative*.

Communication must:

- translate
- preserve epistemic labels
- never invent explanation

### **Risk (high)**

- hallucinated explanations
- post-hoc rationalization
- erosion of trust

### **Fix**

Constrain Communication hard.

In COMMUNICATIONEVENT:

- Replace narrative fields with:
    - message_template_id
    - referenced_judgment_event_id
    - referenced_evidence_ids[]

Add invariant:

> Communication rows must reference upstream Judgment + Evidence.
> 

> No free-text explanations without provenance.
> 

If you keep free text:

- Require generated_by = system | human
- Require epistemic_label

---

## **6. Temporal integrity is insufficiently enforced**

### **Misalignment**

You have created_at timestamps everywhere, which is good.

But OSLO requires:

- *temporal traceability*
- *supersession awareness*
- *decision lineage*

Right now, nothing prevents:

- overwriting meaning via “latest row”
- ignoring prior decisions

### **Risk**

You cannot answer:

> “What did the system believe at time T, and why?”
> 

That breaks auditability and trust.

### **Fix**

Add **explicit lineage**:

- supersedes_id
- valid_from
- valid_to

At least for:

- JUDGMENTEVENT
- GOVERNANCEEVENT
- ELEMENTVERSION

This preserves decision history as a first-class concept.

---

## **7. Execution feedback is underrepresented**

### **Misalignment**

Execution appears indirectly (signals, recompute triggers) but is not clearly modeled as **observed reality**.

In OSLO:

- Execution produces evidence
- Not conclusions

### **Risk**

Execution outcomes will be interpreted as success/failure without Judgment.

### **Fix**

Add or formalize:

- EXECUTIONEVENT
    - observed_signal
    - source
    - confidence
    - related_action_id

Ensure Execution **feeds Reasoning**, not Judgment directly.

---

## **8. The schema is relational — but OSLO is graph-native**

### **Alignment (partial)**

Relational storage is fine.

### **Risk**

If this schema is treated as *the* reasoning substrate, you will hit:

- brittle joins
- hard-coded traversal logic
- poor evidence chaining

### **Fix (architectural, not immediate)**

- Treat this schema as **canonical persistence**
- Layer a **graph projection** (logical or physical) for reasoning
- Never reason directly over raw relational joins

This keeps OSLO scalable.

---

# **Summary of Critical Risks**

| **Risk** | **Severity** |
| --- | --- |
| Epistemic collapse | 🔴 High |
| Governance dilution | 🔴 High |
| Communication hallucination | 🔴 High |
| Loss of temporal lineage | 🟠 Medium |
| Judgment opacity | 🟠 Medium |

---

# **Minimal Fix Set (High Leverage)**

If you do **only six things**, do these:

1. Make epistemic status mandatory everywhere
2. Treat Reasoning outputs as proposals, not facts
3. Add explicit normative frames to Judgment
4. Expand Governance beyond yes/no flags
5. Constrain Communication to reference upstream decisions
6. Add supersession / lineage fields for temporal integrity

---

## **Bottom line**

This schema is **very close to OSLO-grade**.

But without the fixes above, it will gradually morph into:

> a sophisticated planning database
> 

> instead of
> 

> a governed outcome-orchestration system
> 

Relational schemas *freeze intent*.

This is the last place to be ambiguous.

If you want next, I can:

- produce a **revised canonical schema (DDL-level)**, or
- generate a **“why this table exists” invariant for each table**, so engineers don’t misuse them.