# Issue Taxonomy & Severity Specification

---

**OSLO Architecture — Issues v1.0**

---

## **1. Purpose of the Issue System**

The Issue System is OSLO’s mechanism for **making risk, ambiguity, and infeasibility explicit**.

Issues exist to:

- surface problems early
- explain *why* judgment scores are what they are
- guide corrective action
- preserve trust by exposing uncertainty

> Issues are not failures.
> 

> Issues are
> 
> 
> **signals**
> 

---

## **2. Canonical Constraints (Non-Negotiable)**

1. **Every issue belongs to exactly one health dimension**
2. **Every issue has a severity cap determined by source tier**
3. **Execution-derived issues may not redefine planning truth**
4. **Issues explain evidence; they do not prescribe action**
5. **No “miscellaneous” issue category exists**

---

## **3. Health Dimension Classification (Locked)**

All issues must be classified under **one—and only one—dimension**:

- **Clarity Issue**
- **Alignment Issue**
- **Feasibility Issue**

Cross-cutting issues must be decomposed into multiple issues, one per dimension.

---

## **4. Issue Source Tiers & Authority**

Each issue is tagged with a **Source Tier**, inherited from the object(s) that triggered it.

| **Source Tier** | **Origin** |
| --- | --- |
| Tier 1 | Intent |
| Tier 2 | Context, Scope, Requirements |
| Tier 3 | WBS, Resource Plan, Schedule Definition |
| Tier 4 | Work Objects (Execution Signals) |

Source Tier governs **severity limits** and **judgment impact**.

---

## **5. Severity Levels (Global Definition)**

Severity reflects **potential impact on outcome achievement**, not urgency.

| **Severity** | **Meaning** |
| --- | --- |
| **Low** | Minor ambiguity or early signal |
| **Medium** | Material risk requiring attention |
| **High** | Outcome-threatening condition |

Severity is **not user-adjustable**.

---

## **6. Severity Caps by Source Tier (Critical)**

| **Source Tier** | **Max Severity** |
| --- | --- |
| Tier 1–3 | **High** |
| **Tier 4 (Execution)** | **Medium** |
| Tier 4 — Critical Path Blockage | **High (Feasibility only)** |

Execution signals **cannot independently escalate** to governance violations.

---

## **7. Canonical Issue Types by Dimension**

### **7.1 Clarity Issues**

Clarity issues indicate **ambiguity, incompleteness, or interpretability gaps**.

| **Issue Type** | **Typical Source** |
| --- | --- |
| Missing Required Field | Tier 1–3 |
| Ambiguous Definition | Tier 1–3 |
| Inferred-Only Critical Field | Tier 1–3 |
| Conflicting Statements | Tier 1–3 |
| Orphaned Object | Tier 2–4 |
| Unbounded Scope | Tier 2 |
| Execution Churn (signal) | Tier 4 |

**Severity Guidance**

- Planning gaps: Medium–High
- Execution churn: Low–Medium (capped)

---

### **7.2 Alignment Issues**

Alignment issues indicate **misalignment between effort and outcomes**.

| **Issue Type** | **Typical Source** |
| --- | --- |
| Orphaned Requirement | Tier 2 |
| Weak Outcome Linkage | Tier 2–3 |
| Scope Drift | Tier 2 |
| Misallocated Effort | Tier 4 |
| Over-investment in Secondary Outcome | Tier 3–4 |

**Severity Guidance**

- Structural misalignment: Medium–High
- Execution skew: Medium (capped)

---

### **7.3 Feasibility Issues**

Feasibility issues indicate **execution impossibility or high risk**.

| **Issue Type** | **Typical Source** |
| --- | --- |
| Structural Incompleteness | Tier 3 |
| Capacity Shortfall | Tier 3 |
| Temporal Infeasibility | Tier 3 |
| Constraint Conflict | Tier 2–3 |
| Blocked Critical Path Work | Tier 4 |
| Persistent Execution Stalls | Tier 4 |

**Severity Guidance**

- Structural infeasibility: High
- Execution blockage: Medium–High (only if on critical path)

---

## **8. Issue Attributes (Required Schema)**

Every Issue must include:

- issue_id
- issue_type (canonical)
- health_dimension
- severity
- confidence
- source_tier
- triggering_objects
- evidence_summary
- explanation
- resolution_guidance
- created_at
- last_evaluated_at

Issues without explanations are invalid.

---

## **9. Issue Confidence**

Each issue includes a **confidence score** reflecting evidence quality.

Confidence is influenced by:

- source state (explicit vs inferred)
- number of corroborating signals
- consistency over time

Execution-derived issues typically have **lower confidence** than planning-derived issues.

---

## **10. Issue Lifecycle**

Issues move through states:

1. **Detected**
2. **Explained**
3. **Acknowledged** (user-visible)
4. **Addressed** (conditions no longer present)
5. **Resolved** (historical record retained)

Issues are **never deleted**—only resolved.

---

## **11. Relationship to Health Scores**

- Issues directly influence **dimension confidence**
- Multiple low-severity issues may outweigh a single medium issue
- Execution issues primarily affect **confidence**, not raw score
- Resolved issues restore confidence gradually (no instant rebound)

---

## **12. Explanation Contract (Mandatory)**

Each issue explanation must answer:

1. What is the issue?
2. What evidence triggered it?
3. Which artifact(s) are affected?
4. Why it matters for outcomes
5. What would resolve or reduce it

No opaque or model-only explanations are allowed.

---

## **13. Governance Guarantees**

The Issue System guarantees:

1. No issue without evidence
2. No severity inflation
3. No execution-driven authority drift
4. Full traceability to artifacts
5. Stable, explainable behavior

Violations are **system defects**.

---

## **14. Invariants (Locked)**

1. All issues map to Clarity, Alignment, or Feasibility
2. Severity is capped by source tier
3. Execution issues are confidence modifiers
4. Issues explain judgment; they do not replace it
5. No silent inference is permitted

---

## **15. Canonical Summary**

> Issues are how OSLO tells the truth—clearly, early, and without exaggeration. They surface risk without inventing certainty and guide correction without stealing authority.
> 

---

If you want, next I can:

- generate a **developer-ready Issue schema (JSON)**,
- produce an **OSLO explanation style guide for issues**, or
- create a **traceability map from Issue → Judgment → Score → Report**

Just tell me what to do next.