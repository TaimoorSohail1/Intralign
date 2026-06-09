# AI Support Requirements by System Capability

---

## **Executive Summary (One-Line Rule)**

> AI is required only where interpretation, synthesis, or abstraction is unavoidable.
> 

> Everywhere else, deterministic systems must dominate.
> 

---

## **Capability Map**

### **1.**

### **Project Knowledge Layer**

**AI REQUIRED? → ❌ NO**

**Why**

This layer is the **source of truth**, not interpretation.

**Responsibilities**

- Store artifacts
- Store explicit user input
- Store inferred elements (flagged)
- Track versions and provenance

**AI would be harmful here**

- AI hallucination risk
- Silent mutation risk
- Loss of epistemic clarity

**Allowed**

- Schema validation
- Type enforcement
- Provenance tagging

✅ **Purely deterministic**

---

### **2.**

### **Reasoning Layer**

**AI REQUIRED? → ✅ YES (Constrained & Bounded)**

**Why**

This layer must:

- Interpret incomplete information
- Infer missing structural elements
- Detect nuanced gaps and inconsistencies
- Build evidence chains across complex graphs

These tasks **cannot be fully rule-based** at scale.

**AI-Dependent Capabilities**

- Structural inference (e.g., “what’s likely missing?”)
- Semantic gap detection
- Pattern recognition across artifacts
- Evidence synthesis

**Hard Constraints**

- AI outputs must be:
    - deterministic where possible
    - evidence-backed
    - replayable
    - bounded by rules
- AI never speaks
- AI never decides severity
- AI never mutates data

✅ **AI-assisted, rule-governed**

---

### **3.**

### **Judgment Layer**

**AI REQUIRED? → ⚠️ OPTIONAL / LIMITED**

**Why**

Judgment translates structure into scores and severity.

This is **primarily mathematical**, but AI can assist calibration.

**Deterministic Core**

- Scoring formulas
- Threshold comparisons
- Severity classification

**Optional AI Support**

- Weight tuning recommendations (offline)
- Sensitivity analysis
- Pattern detection across cohorts

**Strict Prohibition**

- No AI at runtime for scoring decisions
- No probabilistic severity output remember this is trust-critical

✅ **Deterministic runtime, AI-assisted design-time**

---

### **4.**

### **Governance Layer**

**AI REQUIRED? → ❌ NO (Explicitly Avoid)**

**Why**

Governance defines **product behavior and trust boundaries**.

If AI decides:

- when to interrupt
- what to suppress
- which CTA to allow

…you lose predictability and auditability.

**Governance Must Be**

- Policy-table driven
- Versioned
- Replayable
- Explainable in plain English

**Allowed**

- AI suggestions for *draft policy changes* (offline only)

🚫 **No AI in runtime governance**

---

### **5.**

### **Communication Layer**

**AI REQUIRED? → ⚠️ YES (Expression Only)**

**Why**

Natural language generation is inherently an AI task.

**AI-Dependent Capabilities**

- Message phrasing
- Tone adjustment
- Conciseness vs clarity balance
- Surface-aware wording

**Hard Constraints**

- AI only operates on **authorized intents**
- AI cannot introduce new claims
- AI cannot change severity
- AI cannot add CTAs
- AI must stay within template boundaries

**Governance + Templates → AI → Rendered Message**

✅ **AI for expression, never authority**

---

### **6.**

### **Learning & Feedback Loop**

**AI REQUIRED? → ✅ YES (Offline, Advisory)**

**Why**

Learning requires pattern detection across:

- user interactions
- dismissals
- confirmations
- long-term outcomes

AI excels here.

**AI Responsibilities**

- Identify candidate rule improvements
- Detect false positives / negatives
- Suggest threshold adjustments
- Recommend new issue types

**Hard Boundary**

- AI never deploys changes
- Humans approve and promote

✅ **AI as analyst, not operator**

---

## **Canonical Capability Matrix**

| **Capability** | **AI Required** | **Notes** |
| --- | --- | --- |
| Project Knowledge | ❌ No | Must remain factual |
| Reasoning | ✅ Yes | Bounded, evidence-based |
| Judgment | ⚠️ Optional | Runtime deterministic |
| Governance | ❌ No | Trust-critical |
| Communication | ⚠️ Yes | Expression only |
| Learning Loop | ✅ Yes | Offline only |

---

## **One Critical Architecture Rule (Lock This In)**

> AI may interpret reality, but it may never decide behavior.
> 

Interpretation → Reasoning

Evaluation → Judgment

Permission → Governance

Expression → Communication

---

## **Practical Guidance for Engineering**

### **Use AI when:**

- The task involves ambiguity
- The task involves synthesis
- The task involves language

### **Avoid AI when:**

- The task affects trust boundaries
- The task must be replayable
- The task must be provably correct
- The task controls user interruption

---

## **Recommended Next Step (Optional)**

To operationalize this cleanly, the next artifact would be:

**AI Usage Contract v1.0**

- Allowed AI calls per layer
- Input/output constraints
- Logging requirements
- Fallback behavior
- Failure modes

If you want, I can publish that next.