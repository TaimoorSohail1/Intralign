# OSLO Data Moats — By Layer

---

## **Executive Principle (Lock This In)**

> Your moat is not project data.
> 

> Your moat is how projects fail, recover, and improve over time — under governance.
> 

Raw plans are copyable.

**Judgment, correction, and behavior traces are not.**

---

## **1. Project Knowledge Layer**

**Moat Strength: LOW (Foundational, not differentiating)**

### **Data to Capture**

- Artifact structures (charter, scope, WBS, schedule)
- Goals, outcomes, metrics
- Constraints and assumptions
- Explicit vs inferred flags
- Version history & provenance

### **Why this is not a moat**

- Users already own this data
- Competing tools store the same artifacts
- Migration tools commoditize it

### **Still important because**

- It anchors everything else
- It enables *downstream compounding*

**Verdict:**

Necessary, but not defensible alone.

---

## **2. Reasoning Layer**

**Moat Strength: MEDIUM → HIGH (Structural intelligence)**

### **Data to Capture**

- Detected issue types (clarity, alignment, feasibility)
- Inference patterns (what was inferred, why)
- Evidence chains:
    - rules triggered
    - artifacts involved
    - assumptions required
- False positives / negatives (via later validation)

### **Why this compounds**

- You learn *how projects break structurally*
- You build a corpus of:
    - missing-by-default elements
    - common dependency failures
    - early signals of downstream issues

### **Why competitors can’t easily replicate**

- Requires:
    - longitudinal exposure across many projects
    - structured artifact graphs
    - disciplined evidence tracking

**Verdict:**

Strong moat when combined with judgment + feedback.

---

## **3. Judgment Layer**

**Moat Strength: VERY HIGH (Hardest to replicate)**

### **Data to Capture**

- Health scores over time (clarity, alignment, feasibility)
- Severity classifications
- Score deltas after changes
- Risk concentration patterns
- Outcome vs initial score correlations

### **Why this is gold**

You are capturing:

- *Which early signals actually mattered*
- *Which risks were noise*
- *Which score patterns predicted success or failure*

This is **not generic ML data** — it is *domain-specific judgment history*.

### **Why competitors struggle**

- Requires:
    - time
    - consistency
    - outcome observation
    - stable scoring canon

**Verdict:**

This is your **core intelligence moat**.

---

## **4. Governance Layer**

**Moat Strength: VERY HIGH (Behavioral + trust moat)**

### **Data to Capture**

- When OSLO chose to speak vs stay silent
- Which policies were applied
- Which surfaces were used
- CTA authorizations vs suppressions
- Corrections issued (and when)
- User reactions to interruptions

### **Why this is uniquely defensible**

You are learning:

- *When humans accept AI input*
- *When interruption causes friction*
- *Which governance postures build trust*

This data **cannot be scraped or simulated**.

### **Strategic insight**

Over time, this becomes:

- a playbook for AI-human collaboration
- a defensible trust model competitors will struggle to tune

**Verdict:**

This is your **trust moat**.

---

## **5. Communication Layer**

**Moat Strength: MEDIUM (Expressive refinement)**

### **Data to Capture**

- Message variants used
- Expansion clicks (“how OSLO knows”)
- Dismissals vs acceptance
- CTA engagement
- Time-to-action after message

### **Why it compounds**

- You learn:
    - which phrasing clarifies vs confuses
    - how much explanation is enough
    - where tone matters vs doesn’t

### **Why it’s not sufficient alone**

- Copy and tone can be imitated
- Value emerges only when tied to governance + judgment

**Verdict:**

Amplifier moat, not a standalone one.

---

## **6. Learning & Feedback Loop**

**Moat Strength: EXTREME (Compounding meta-moat)**

### **Data to Capture**

- User validation of inferred elements
- Accepted vs rejected recommendations
- Long-term outcome achievement
- Policy changes → behavior changes → outcomes
- Regression cases (where OSLO was wrong)

### **Why this is the apex moat**

You are learning:

- *How judgment improves judgment*
- *How governance tuning affects outcomes*
- *How AI assistance evolves safely*

This is **second-order learning** competitors won’t have.

**Verdict:**

This is your **compounding systems-intelligence moat**.

---

## **Canonical Moat Summary Table**

| **Layer** | **Moat Strength** | **Why** |
| --- | --- | --- |
| Project Knowledge | Low | Commodity data |
| Reasoning | Medium–High | Structural intelligence |
| Judgment | Very High | Outcome-linked evaluation |
| Governance | Very High | Trust & behavior data |
| Communication | Medium | Expressive optimization |
| Learning Loop | Extreme | Meta-learning advantage |

---

## **One Critical Insight (Founders Miss This)**

> Your moat is not better plans.
> 

> It’s knowing which plans looked good and failed anyway — and why.
> 

Most tools never see:

- early signals
- corrections
- governance choices
- outcome validation

OSLO does.

---

## **What to Instrument Immediately (If You Do Nothing Else)**

If resources are constrained, **do not compromise on capturing**:

1. **Judgment deltas over time**
2. **Governance decisions (speak vs silence)**
3. **User validation of inferences**
4. **Corrections and reversals**
5. **Outcome vs initial risk patterns**

Those five streams alone create a moat competitors will not catch up to.

---

## **Recommended Next Artifact (Optional)**

To operationalize this, the next high-leverage spec would be:

**Data Moat Instrumentation Spec v1.0**

- Events by layer
- Required fields
- Retention & aggregation rules
- What is used for learning vs audit vs product

If you want, I can publish that next.