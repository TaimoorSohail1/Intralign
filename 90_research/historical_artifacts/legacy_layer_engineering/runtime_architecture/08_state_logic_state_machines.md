# State Logic & State Machines

> **⚠ DL-043 re-home (2026-06-04).** Implementation-detail backing for runtime **state / recompute** behavior, owned under **Adapt (emergent) + Act** and expressed canonically in the **Runtime Behavior Model**. Secondary to the Cognitive Responsibility Architecture. Note: recompute **appends** Cognition History Records (never overwrites) per DL-043.

## Outcome Space State

Possible states:
- Not Created
- Intake Started
- Fast Pass Running
- Initial Understanding Created
- Deep Refinement Running
- Expanded Understanding Created
- Active
- Archived

---

## Confidence Maturity State

```text
Initial → Expanded → Validated → Continuous
```

### Initial
Fast-pass analysis complete.

### Expanded
Deep refinement complete.

### Validated
Key assumptions/stakeholders/evidence validated.

### Continuous
Live monitoring and execution telemetry active.

---

## Integrity State

Possible states:
- Initial
- Clarified
- Aligned
- Feasible
- Governed
- Execution Ready
- Fragile
- Drift Emerging
- At Risk

Transitions depend on:
- clarity
- alignment
- feasibility
- policy satisfaction
- unresolved critical issues
- confidence trend

---

## Attention Item State

Possible states:
- Detected
- Acknowledged
- Assigned
- In Resolution
- Resolved
- Deferred
- Dismissed with Rationale
- Escalated
- Blocked by Governance

---

## Recommendation State

Possible states:
- Generated
- Viewed
- Accepted
- Modified
- Rejected
- Deferred
- Superseded
- Applied
- Reverted

---

## Override State

Possible states:
- Proposed
- Low Impact Accepted
- Rationale Required
- Rationale Provided
- Approved
- Rejected
- Escalated
- Recorded

---

## Shared View State

Possible states:
- Draft
- Shared
- Viewed
- Commented
- Clarified
- Approved
- Closed
- Expired

---

## OSLO Companion State

Possible states:
- Collapsed
- Ambient
- Explaining
- Resolving
- Simulating
- Drafting
- Clarifying
- Governance Review
- Escalation
