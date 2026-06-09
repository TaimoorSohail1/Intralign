# Health Scoring Specification

---

**OSLO Architecture — Health Scoring v1.0**

---

## **1. Purpose of Health Scoring**

Health Scoring converts OSLO’s judgments into **stable, explainable indicators of outcome viability**.

Health scores exist to:

- summarize complex plan quality into interpretable signals
- support executive and practitioner decision-making
- surface risk early without overreacting to noise
- provide a consistent basis for comparison across projects and outcomes

Health scores **do not** replace judgment; they **express it**.

---

## **2. Canonical Health Dimensions**

All health scoring is performed across **exactly three dimensions**:

1. **Clarity**
2. **Alignment**
3. **Feasibility**

No additional dimensions are permitted in v1.0.

---

## **3. Scoring Unit of Analysis**

### **3.1 Primary Unit: Outcome**

All health scores are computed **per Outcome**.

- Each Outcome has:
    - Clarity Score
    - Alignment Score
    - Feasibility Score
    - Outcome Health Score (aggregate)

### **3.2 Secondary Aggregations**

- Project Health = weighted aggregation of Outcome Health Scores
- Program / Portfolio Health (future) = aggregation across projects

---

## **4. Authority Tiers & Scoring Influence**

Health scores respect OSLO’s **four-tier authority model**.

| **Tier** | **Source** | **Scoring Role** |
| --- | --- | --- |
| Tier 1 | Intent | Defines scoring truth |
| Tier 2 | Context, Scope, Requirements | Constrains and aligns |
| Tier 3 | WBS, Resource Plan, Schedule | Structural feasibility |
| **Tier 4** | **Work Objects (Execution)** | **Confidence modifiers only** |

**Tier-4 signals may only reduce confidence; they may not increase scores.**

---

## **5. Source State Weighting**

Every scoring input is tagged with a source_state.

| **Source State** | **Scoring Treatment** |
| --- | --- |
| Explicit | Full weight |
| Derived | Full weight |
| Inferred (allowed fields) | Discounted |
| Inferred (prohibited fields) | Treated as missing |

Inference-prohibited fields are never scored, even if proposed.

---

## **6. Dimension Scoring Definitions**

### **6.1 Clarity Score**

**Question answered:**

> Is the plan explicit, interpretable, and free of ambiguity?
> 

### **Primary Inputs**

- Intent completeness (outcomes, success criteria, time horizon)
- Explicit scope boundaries
- Requirement testability
- Structural integrity (WBS completeness)
- Absence of orphaned elements

### **Scoring Rules**

- Missing required fields produce step-down penalties
- Ambiguity produces confidence penalties
- Inferred-only critical fields cap the score

### **Special Rule (Prerequisite)**

> Low Clarity caps Alignment and Feasibility confidence.
> 

---

### **6.2 Alignment Score**

**Question answered:**

> Does all planned effort support declared outcomes?
> 

### **Primary Inputs**

- Requirement-to-outcome traceability
- Scope item outcome linkage
- WBS coverage of requirements
- Effort distribution vs outcome priority

### **Scoring Rules**

- Alignment is scored **per outcome**
- Many-to-many relationships are expected
- Orphaned requirements or scope items reduce score
- Over-investment in secondary outcomes reduces score

---

### **6.3 Feasibility Score**

**Question answered:**

> Can this plan be executed successfully within constraints and time?
> 

### **Primary Inputs**

- Structural completeness (WBS depth and balance)
- Resource capacity vs workload
- Schedule realism vs time horizon
- Constraint conflicts
- Execution signals (Tier-4)

### **Special Rule**

> Feasibility is the only dimension where Tier-4 signals have material influence—but still capped and one-directional.
> 

---

## **7. Tier-4 (Work Object) Scoring Rules**

### **7.1 Allowed Impacts**

Work objects may:

- reduce feasibility confidence
- raise early warning issues
- signal misallocation or execution drift

Work objects may **not**:

- improve scores
- resolve planning issues
- override structural deficits

---

### **7.2 Severity Caps**

| **Work-Object Signal** | **Max Impact** |
| --- | --- |
| Orphaned tasks | Medium |
| Execution churn | Low–Medium |
| Misaligned effort | Medium |
| Critical-path blockage | High (Feasibility only) |

---

## **8. Score Stability & Dampening**

To prevent volatility:

1. **Negative bias**
    - Negative signals weigh more than positive ones
2. **Dampening**
    - Small execution changes do not cause large score swings
3. **Temporal smoothing**
    - Scores consider recent history, not just the latest snapshot

---

## **9. Score Normalization**

- All dimension scores are normalized to **0–100**
- Scores are internally continuous but may be displayed in bands:
    - Healthy
    - At Risk
    - Critical

Banding is a **presentation concern**, not a scoring rule.

---

## **10. Outcome Health Score (Aggregation)**

Outcome Health Score is derived from:

- Clarity Score
- Alignment Score
- Feasibility Score
- Confidence modifiers

### **Aggregation Rules**

- Low Clarity caps overall score
- Outcome Priority influences weighting
- Confidence discounts apply multiplicatively

---

## **11. Project Health Score**

Project Health Score is an aggregation of:

- Outcome Health Scores
- Outcome Priority weights

Projects with a single weak primary outcome should still score poorly, even if secondary outcomes are healthy.

---

## **12. Confidence vs Score (Explicit Distinction)**

OSLO always maintains:

- a **Score** (what the plan suggests)
- a **Confidence** (how much trust to place in the score)

Execution signals primarily affect **confidence**, not raw score.

---

## **13. Explanation Requirements**

Every score must be explainable.

Explanations must include:

- which inputs mattered
- what was missing or inferred
- why confidence changed
- what would improve the score

Scores without explanations are invalid.

---

## **14. Governance Guarantees**

Health Scoring guarantees:

1. No hidden inference
2. No execution-driven intent drift
3. Stable, non-volatile scores
4. Deterministic behavior
5. Full traceability to evidence

Violations are system defects.

---

## **15. Invariants (Locked)**

1. All scoring is outcome-based
2. Only three health dimensions exist
3. Tier-4 influence is capped and one-directional
4. Inferred truth is never scored
5. Low clarity constrains all other scores
6. Scores are explainable by design

---

## **16. Canonical Summary**

> Health Scoring expresses judgment, not optimism. It reflects what is known, discounts what is assumed, and surfaces risk without letting execution noise overwhelm strategic truth.
> 

---

If you want to continue, the most natural next steps are:

- publish the **Issue Taxonomy & Severity Specification**, or
- create a **Judgment + Health API contract**, or
- consolidate everything into a **single OSLO Architecture Playbook v1.0**

Tell me where you want to go next.