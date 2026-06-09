# OSLO AI Components

Let’s answer this precisely, because this question affects **architecture, trust, explainability, and defensibility**.

Not every part of OSLO should be AI-driven or probabilistic. In fact, **only specific portions should be**, otherwise you lose predictability and governance control.

Below is a clean breakdown.

---

# **First: Deterministic vs Probabilistic in OSLO**

## **Deterministic components**

Produce the same output given the same input.

Used for:

- Governance
- policy enforcement
- scoring
- system state
- execution actions
- auditability

## **Probabilistic (AI-driven) components**

Outputs vary based on inference.

Used for:

- interpretation
- reasoning
- judgment suggestions
- pattern detection
- ambiguity resolution

---

# **OSLO Layer Breakdown**

## **1. Knowledge Layer**

(Core structured truth)

### **Deterministic**

- Canonical project model
- Intent graph
- Outcome graph
- Artifact storage
- Relationships between entities
- Traceability mapping

Example:

Outcome A maps to Requirement B.

No AI needed.

---

### **AI involvement (limited)**

Used to:

- Extract structured data from text
- Interpret user inputs
- Suggest missing relationships

Example:

User uploads charter → AI extracts goals.

But once stored, it becomes deterministic truth.

---

### **Conclusion**

Knowledge layer is mostly deterministic with AI-assisted ingestion.

---

## **2. Reasoning Layer**

(Detecting structural problems)

This layer is heavily AI-driven.

### **AI-driven / probabilistic**

Tasks include:

- Detecting outcome drift
- Identifying alignment gaps
- Recognizing assumption decay
- Inferring causal issues
- Diagnosing structural problems

Example:

Schedule slipped → does this threaten outcome?

Requires reasoning, not rules.

---

### **Deterministic parts**

Once drift is detected:

- Rule thresholds
- Validation checks
- structural constraints

are deterministic.

---

### **Conclusion**

Reasoning = hybrid, mostly probabilistic.

---

## **3. Judgment Layer**

(Severity & recommendation evaluation)

Highly AI-driven.

### **Probabilistic elements**

- Severity interpretation
- Tradeoff reasoning
- Impact estimation
- Intervention quality assessment

Example:

Is this delay critical or manageable?

Requires context interpretation.

---

### **Deterministic elements**

Severity scoring formulas may be deterministic:

Example:

If revenue impact > X → severity high.

---

### **Conclusion**

Judgment mixes AI reasoning + deterministic scoring.

---

## **4. Governance Layer**

(Control & enforcement)

This layer must be deterministic.

### **Deterministic functions**

- Notification timing
- suppression rules
- escalation routing
- authority boundaries
- workflow enforcement
- audit logging

Example:

If severity high → notify PM.

No AI randomness allowed.

---

### **AI involvement (optional)**

Used only for prioritization assistance.

But execution decisions must remain deterministic.

---

### **Conclusion**

Governance should be deterministic.

---

## **5. Communication Layer**

(Translation & messaging)

Mixed layer.

### **AI-driven**

- Natural language generation
- Tone adaptation
- explanation synthesis
- summarization

Example:

Explain risk to executive vs engineer.

---

### **Deterministic**

- Message routing
- message timing
- notification triggers

---

### **Conclusion**

Language probabilistic, routing deterministic.

---

# **Summary Table**

| **OSLO Layer** | **AI-driven?** | **Deterministic?** | **Role** |
| --- | --- | --- | --- |
| Knowledge | Low | High | Truth storage |
| Reasoning | High | Medium | Drift detection |
| Judgment | High | Medium | Decision evaluation |
| Governance | Low | High | Control & enforcement |
| Communication | Medium | Medium | Human translation |

---

# **Architectural Principle**

## **Intelligence should be probabilistic.**

## **Authority should be deterministic.**

Meaning:

AI can recommend.

System enforces predictably.

---

# **Strategic Insight**

Your moat is not just AI reasoning.

It is:

**AI reasoning wrapped in deterministic governance.**

Most AI products fail because they allow probabilistic outputs to control execution.

OSLO prevents that.

---

# **Important Future Decision**

Next major architecture decision:

Should OSLO reasoning become:

A) Single orchestrator model

B) Multiple specialized agents

C) Hybrid reasoning pipeline

That decision affects scalability and defensibility long-term.