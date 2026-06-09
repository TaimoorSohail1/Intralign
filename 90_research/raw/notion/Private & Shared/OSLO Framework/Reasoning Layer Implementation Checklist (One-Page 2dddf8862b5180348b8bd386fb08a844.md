# Reasoning Layer Implementation Checklist (One-Pager)

---

**Purpose**

Implement the Reasoning Layer as a **deterministic implication engine**, not a decision-maker.

Reasoning derives *what appears to follow*—it never decides *what should happen*.

---

## **PHASE 1 — Epistemic Scope Lock (Before Any Code)**

☐ **Read the Reasoning Layer Playbook (only)**

Engineer must be able to explain:

- What reasoning *is* in this system
- What reasoning *is not* (decisions, approvals, actions)
- Which layers it consumes from (Knowledge only)
- Which layer it produces for (Judgment only)

☐ **Confirm Non-Authority Explicitly**

Engineer must acknowledge:

- Reasoning does **not** authorize actions
- Reasoning does **not** resolve tradeoffs
- Reasoning does **not** communicate truth to users
- Reasoning does **not** mutate Knowledge

☐ **Whiteboard the Epistemic Flow**

```
Knowledge → Reasoning → Judgment
(no bypasses)
```

**Exit gate:**

If reasoning outputs are described as “decisions,” “recommendations,” or “actions” → stop.

---

## **PHASE 2 — Reasoning Invariants (Non-Negotiable)**

☐ **List Core Reasoning Invariants**

Each invariant must be mechanically testable.

Minimum required invariants:

- Same inputs → same outputs (determinism)
- Reasoning outputs are explicitly non-normative
- All outputs include confidence propagation
- Reasoning never mutates Knowledge
- Reasoning never triggers execution
- Reasoning never communicates to users
- Reasoning outputs reference input provenance
- Stale reasoning outputs cannot be reused

☐ **Translate Each Invariant into Assertions**

Example:

```
assert output.decision_flag == false
assert output.provenance.references exist
assert output.confidence ≤ min(input.confidence)
```

☐ **Define Violation Behavior**

- Halt reasoning
- Reject output
- Escalate to observability

**Exit gate:**

Violations are defined *before* rules exist.

---

## **PHASE 3 — Test Matrix & Gherkin (Before Rules)**

☐ **Create Reasoning Layer Test-Case Matrix**

Map:

- invariant → scenario → expected outcome

Include:

- conflicting knowledge inputs
- low-confidence inputs
- stale knowledge inputs
- identical inputs (replay test)
- lifecycle-restricted execution

☐ **Generate Gherkin / BDD Tests**

Example:

```
Given identical knowledge inputs
When reasoning is executed twice
Then outputs are identical
```

☐ **Wire Tests into CI**

- Tests must fail initially
- No conditional bypasses

**Exit gate:**

Reasoning behavior is now *fully specified*.

---

## **PHASE 4 — Contracts & Schemas (Hard Gates)**

☐ **Implement Reasoning Output Schema**

Schema must include:

- implication type (issue, risk, signal, dependency, gap)
- confidence score
- input references
- lifecycle scope
- validity window
- non-normative flag

☐ **Implement Confidence Propagation Rules**

- Confidence must never increase
- Weak inputs downgrade outputs
- Missing confidence blocks output

☐ **Implement Epistemic → Judgment Consumption Contract**

- Explicit “not a decision” marker
- Required confidence thresholds
- Required provenance completeness

☐ **Implement Supersession & Retention Rules**

- Old reasoning outputs expire
- Superseded outputs are retained but ignored

**Exit gate:**

Invalid reasoning cannot reach Judgment.

---

## **PHASE 5 — Rule Execution (Only Now)**

☐ **Implement Reasoning Rules / Logic**

- Rule files
- Operators
- Evaluation order

☐ **Respect Lifecycle × Mode Constraints**

- Reasoning only runs where permitted
- Illegal lifecycle execution hard-fails

☐ **No Inline Judgment Logic**

- No prioritization
- No approval logic
- No execution hints

**Exit gate:**

Rules exist but cannot act.

---

## **PHASE 6 — Observability & Replayability**

☐ **Emit Reasoning Trace Events**

- Inputs used
- Rules fired
- Outputs produced
- Timing

☐ **Ensure Replayability**

- Same inputs → same outputs
- Deterministic rule ordering
- Versioned rule sets

☐ **Capture Failure States**

- Conflicts
- Overload
- Timeout
- Ambiguity

**Exit gate:**

You can replay and explain any reasoning result.

---

## **FINAL SANITY CHECKS (Critical)**

☐ Can reasoning say *what should be done*?

→ ❌ If yes, stop.

☐ Can reasoning trigger execution?

→ ❌ If yes, stop.

☐ Can reasoning explain outcomes directly to users?

→ ❌ If yes, stop.

☐ Would deleting the Judgment Layer break reasoning?

→ ❌ If yes, architecture is wrong.

---

## **Golden Rules (Reasoning Layer)**

- **Reasoning derives implications, not decisions**
- **Determinism over cleverness**
- **Confidence always degrades, never inflates**
- **Rules explain why, not what to do**
- **If reasoning feels “smart,” you probably crossed a boundary**

---

## **One-Line Operating Principle**

> “Reasoning may reveal consequences—but it never commits to them.”
> 

---

If you want next, I can:

- tailor this for **Judgment**, **Governance**, or **Execution**
- compress this into a **CI-ready engineering checklist**
- or walk through a **sample Reasoning rule → invariant → test → implementation** end-to-end