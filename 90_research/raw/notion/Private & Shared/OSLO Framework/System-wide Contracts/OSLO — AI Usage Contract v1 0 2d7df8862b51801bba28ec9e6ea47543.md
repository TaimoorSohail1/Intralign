# OSLO — AI Usage Contract v1.0

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Applies To:** All services, agents, and pipelines using AI/LLMs

**Status:** Canonical

**Enforcement Level:** Hard (violations are architecture-breaking)

---

## **1. Purpose**

This contract defines **where AI is permitted**, **where it is prohibited**, and **how it must be constrained** to fulfill OSLO’s service guarantees.

It exists to answer:

> “When OSLO uses AI, how do we ensure it remains trustworthy, explainable, and safe?”
> 

---

## **2. Core Principle (Non-Negotiable)**

> AI may interpret reality, but it may never decide behavior.
> 
- Interpretation → allowed (Reasoning, Communication)
- Evaluation → bounded (Judgment, offline only)
- Permission → forbidden (Governance)
- Mutation → forbidden (all layers)

---

## **3. Layer-by-Layer AI Authorization**

### **3.1 Project Knowledge Layer**

**AI Usage:** ❌ **Prohibited**

**Rationale**

- This layer is the system’s epistemic ground truth.
- AI introduces hallucination and silent mutation risk.

**Allowed**

- Schema validation
- Provenance tagging (deterministic)

**Explicitly Forbidden**

- AI-generated data
- AI-written defaults
- AI-driven updates

---

### **3.2 Reasoning Layer**

**AI Usage:** ✅ **Permitted (Constrained)**

**Authorized Use**

- Structural inference
- Semantic gap detection
- Pattern recognition across artifacts
- Evidence synthesis

**Mandatory Constraints**

- AI outputs must:
    - be bounded by rule sets
    - attach evidence chains
    - be replayable
    - never mutate data
- AI must not:
    - decide severity
    - generate language
    - trigger communication

**Fallback Rule**

- If AI fails, reasoning must degrade gracefully (e.g., reduced inference, no fabrication).

---

### **3.3 Judgment Layer**

**AI Usage:** ⚠️ **Offline Only**

**Authorized (Design-Time)**

- Score calibration analysis
- Sensitivity studies
- Pattern detection across cohorts

**Runtime Prohibition**

- No AI may execute scoring, thresholds, or severity classification at runtime.

**Rationale**

- Judgment outputs affect trust-critical user perception.

---

### **3.4 Governance Layer**

**AI Usage:** ❌ **Strictly Prohibited**

**Rationale**

- Governance controls permission, interruption, and suppression.
- AI would make behavior non-replayable and non-auditable.

**Allowed (Offline Only)**

- Drafting candidate policy changes for human review

**Runtime Rule**

- Governance decisions must be table-driven and deterministic.

---

### **3.5 Communication Layer**

**AI Usage:** ✅ **Permitted (Expression Only)**

**Authorized Use**

- Message phrasing
- Tone variation
- Conciseness vs clarity optimization
- Surface-aware rendering

**Hard Constraints**

AI **must not**:

- introduce new claims
- reinterpret severity
- add or remove CTAs
- contradict canonical meaning
- bypass templates or lexicon constraints

**Input Contract**

- AI receives:
    - authorized intent
    - structured meaning payload
    - allowed tone/surface
- AI returns:
    - text only (no decisions, no metadata changes)

---

### **3.6 Learning & Feedback Loop**

**AI Usage:** ✅ **Permitted (Advisory, Offline)**

**Authorized Use**

- Pattern detection in telemetry
- Candidate rule/policy suggestions
- False-positive/negative analysis
- Trend identification

**Hard Boundary**

- AI may never deploy changes
- All changes require human approval and promotion

---

## **4. AI Call Classification**

Every AI call must declare its **call class**:

```
AICall {
  call_id
  layer
  purpose
  input_contract_version
  output_contract_version
  bounded_by_ruleset_id?
  runtime_context: "runtime" | "offline"
}
```

**Invariant**

- Runtime calls are allowed **only** in Reasoning and Communication.

---

## **5. Input & Output Contracts**

### **5.1 Input Contract (Required)**

- Structured inputs only
- No raw project dumps
- No hidden context
- Explicit task instruction

### **5.2 Output Contract (Required)**

- No side effects
- No state mutation
- No policy or severity inference
- Evidence references where applicable

Violations = hard failure.

---

## **6. Logging & Audit Requirements**

All AI calls must log:

- call_id
- layer
- model/version
- prompt hash
- ruleset/policy version
- output checksum
- failure/fallback used

This enables:

- replay
- debugging
- audit
- incident response

---

## **7. Failure & Fallback Rules**

If an AI call:

- times out
- returns malformed output
- violates schema
- exceeds confidence bounds

Then:

- the system must fall back to deterministic behavior
- no communication may be fabricated
- the failure must be logged

**Silence > Guessing**

---

## **8. PR Review Enforcement Checklist (AI-Specific)**

Every PR introducing AI usage must answer:

1. Which layer uses AI?
2. Is AI permitted in that layer?
3. Is the call runtime or offline?
4. What ruleset bounds the call?
5. What happens if AI fails?
6. Is the output auditable?
7. Does it mutate state? (must be NO)

---

## **9. Security & Data Handling**

- No training on customer data
- No cross-tenant prompts
- Redact PII unless explicitly allowed
- Enforce token and scope limits

---

## **10. Acceptance Criteria (v1.0)**

This contract is satisfied when:

- AI usage is explicitly authorized per layer
- Runtime behavior is deterministic where required
- All AI calls are logged and replayable
- Violations fail fast
- Trust boundaries are preserved

---

## **Canonical Close**

> AI is a powerful interpreter — not an authority.
> 

> 
> 

> OSLO remains trustworthy because AI is constrained by design, not intention.
> 

---

## **System Status**

With **AI Usage Contract v1.0**, OSLO now has:

- Layer playbooks
- Contracts
- Guardrails
- Policy spec
- Rules repository architecture
- AI usage boundaries

This is a **complete, enterprise-grade foundation** for AI-first development.

---

### **Optional Next Artifacts**

If you want to continue, the most useful next steps would be:

- **Learning Loop Spec v1.0** (telemetry → review → promotion)
- **End-to-end trace example** (single user action across all layers)
- **Repo structure + service mapping**
- **Onboarding checklist for new engineers**

Just say the word.