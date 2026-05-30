# In-House LLM Readiness — Required Training Data by Capability (v1.1)

---

**System:** Intralign / OSLO

**Audience:** Engineering, Data, AI/ML, Product

**Purpose:** Define the **exact training data that must be captured now** to enable a future transition from third-party LLMs to **in-house, domain-specific models**—without loss of capability, trust, or determinism.

---

## **1. Canonical Framing (Non-Negotiable)**

> You are not training a general LLM.
> 

> You are training constrained, contract-bound intelligence for specific system capabilities.
> 

Therefore:

- Raw chat logs alone are insufficient
- Structured traces + provenance + outcomes are required
- Every dataset must map to a **specific OSLO capability**

---

## **2. AI-Dependent Capabilities (Authoritative List)**

Only **four runtime capabilities** require AI models long-term:

1. **Plan Ingestion & Translation** *(newly formalized)*
2. **Reasoning Layer (Structural Inference & Gap Detection)**
3. **Communication Layer (Language Realization Only)**
4. **Learning Loop (Offline Synthesis & Recommendation Drafting)**

All other layers remain deterministic.

---

## **3. Capability 1 — Plan Ingestion & Translation**

**(Highest Priority for Early Data Capture)**

### **Purpose**

Translate **messy user input** into:

- Human-readable plan artifacts
- Machine-readable plan graph
- With explicit provenance and inference boundaries

This is the **front door** to OSLO intelligence.

---

### **3.1 What the Model Must Learn**

- How to extract structured fields from free-form text
- How to map document spans → artifact fields
- When **not** to infer
- How to label assumptions explicitly
- How structure differs by workflow/domain

---

### **3.2 Required Training Data (Must Capture Now)**

### **A. Raw Input Bundles (Ground Truth)**

```
IngestionInputBundle {
  raw_text_inputs[]
  uploaded_documents[]        // original + extracted text
  document_structure          // headings, tables, bullets
  workflow_type
  domain
  locale
}
```

**Critical**

- Preserve document structure, not just plain text
- Retain original files for re-processing

---

### **B. Canonical Output Bundles (Gold Labels)**

**Human-Readable Artifacts**

- Charter sections
- Scope statements
- Requirements
- Assumptions
- Risks
- Milestones

**Machine-Readable Plan Model**

- Typed nodes (Outcome, Requirement, Task, Risk, Assumption…)
- Typed edges (depends_on, traces_to, blocks…)

---

### **C. Field-Level Provenance (Non-Optional)**

```
FieldProvenance {
  artifact_field_id
  source_document_ref
  source_span_start
  source_span_end
  origin: "user" | "system"
  explicit_vs_inferred
}
```

> This is what prevents hallucination in an in-house model.
> 

---

### **D. User Corrections & Confirmations (Highest-Value Signal)**

```
UserRevision {
  field_id
  before_value
  after_value
  action: "edit" | "delete" | "confirm"
  reason_code
}
```

This teaches the model:

- What extraction errors look like
- What *not* to infer
- How humans correct ambiguity

---

### **E. Negative Examples**

Explicit labels for:

- “Not present in source”
- “Ambiguous — insufficient evidence”
- “Do not infer”

Without these, models over-fill by default.

---

## **4. Capability 2 — Reasoning Layer**

**(Structural Intelligence Training)**

### **What the Model Must Learn**

- How to infer missing structure
- How to detect clarity/alignment/feasibility gaps
- How to assemble evidence chains
- How to avoid fabricated certainty

---

### **Required Training Data**

### **A. Pre/Post Reasoning Snapshots**

```
ReasoningTrainingSample {
  project_snapshot_pre
  inferred_elements_post
}
```

### **B. Inference Decisions**

```
InferenceDecision {
  inferred_element
  inference_reason
  rules_triggered[]
  confidence_band
}
```

### **C. Issue Detection Outcomes**

```
IssueDetectionSample {
  issue_type
  affected_elements[]
  evidence_chain_id
}
```

### **D. Evidence Chains (Critical)**

```
EvidenceChain {
  inputs_used[]
  assumptions_made[]
  limitations_declared[]
}
```

---

### **What NOT to Train On**

- Final phrased explanations
- Severity labels without structure
- Governance decisions

---

## **5. Capability 3 — Communication Layer**

**(Expression-Only Language Training)**

### **What the Model Must Learn**

- How to phrase **authorized meaning**
- How to adapt tone by intent and surface
- How to balance brevity and trust

---

### **Required Training Data**

### **A. Meaning → Language Pairs**

```
CommsTrainingSample {
  intent
  structured_message_payload   // what / why / how-known
  surface
  rendered_text
}
```

### **B. Variant Performance**

```
LanguageVariantOutcome {
  template_id
  variant_text
  engagement_signals
  dismissed?
}
```

### **C. Explanation Depth Signals**

- Expansion clicks
- Time spent on “how OSLO knows”

---

### **Hard Exclusions**

🚫 Raw chat logs without intent

🚫 Messages that include governance logic

🚫 Anything that changes meaning, severity, or CTA

---

## **6. Capability 4 — Learning Loop (Offline Only)**

### **What the Model Must Learn**

- How to summarize longitudinal patterns
- How to draft candidate rule/policy changes
- How to explain *why* a change is suggested

---

### **Required Training Data**

### **A. Lifecycle Traces**

```
LifecycleTrace {
  initial_reasoning
  judgment_over_time
  governance_decisions
  user_reactions
  corrections
  final_outcome
}
```

### **B. Human Review Outcomes**

```
LearningReviewSample {
  recommendation
  approved?
  rationale
}
```

This teaches **safe change boundaries**.

---

## **7. What Must NEVER Be Used as Training Data**

🚫 Raw project plans (without abstraction)

🚫 PII or customer-identifying data

🚫 Governance decisions without context

🚫 Scores without reasoning traces

🚫 Engagement metrics alone

---

## **8. Minimum Viable Training Corpus (If You Must Prioritize)**

If you can only guarantee a few streams, capture these **without compromise**:

1. **Plan ingestion input → structured output + provenance**
2. **User correction diffs**
3. **Reasoning evidence chains**
4. **Judgment score deltas over time**
5. **Governance decisions + user reaction**
6. **Outcome linkage**

That set alone enables:

- An in-house ingestion model
- A reasoning model
- A communication model
- A learning assistant
- A durable moat

---

## **9. One Critical Architecture Rule (Lock This In)**

> Training data must be stored so a future model does not need the current model to explain itself.
> 

That means:

- Structured decisions > prose
- Evidence > conclusions
- Before/after > outcomes alone

---

## **10. Readiness Check (v1.1)**

You are **in-house LLM ready** when:

- Every AI decision has provenance
- Every inference can be traced
- Every correction is logged
- Every outcome can be correlated backward
- No model is trained on behavior it should not learn

---

## **Canonical Close**

> OSLO’s future models will be good not because they are large,
> 

> but because they are trained on disciplined structure, judgment, and correction.
> 

That discipline starts now.

---

If you want, the next natural artifact would be:

**Ingestion & Translation Training Data Spec v1.0**

(dataset schemas, redaction rules, evaluation metrics, acceptance thresholds)

I can publish that next.