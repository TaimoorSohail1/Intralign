# Inference Policy Specification

**OSLO Architecture — Inference Policy v1.1**

---

## **1. Purpose**

This specification defines **when, how, and under what constraints OSLO may infer information**, and how inferred information is **stored, labeled, evaluated, discounted, and promoted**.

The goal is to:

- enable fast onboarding and AI assistance
- preserve trust and auditability
- prevent hallucinated authority
- ensure explainable judgment

> Inference is a
> 
> 
> **tool for acceleration**
> 

---

## **2. Core Principles (Non-Negotiable)**

1. **Inference is never silent**
2. **Inference is always labeled**
3. **Inference never defines truth**
4. **Inference is reversible**
5. **Inference is discounted for judgment**
6. **Inference promotion requires explicit confirmation**

Any violation of these principles is a **system defect**.

---

## **3. Definitions**

### **3.1 Explicit Information**

Information directly authored or confirmed by a human.

- source_state = explicit
- Defines canonical truth
- Fully weighted for judgment

---

### **3.2 Derived Information**

Information deterministically computed from explicit inputs.

Examples:

- rollups
- counts
- deterministic mappings
- source_state = derived
- Defines canonical truth
- Fully weighted for judgment

---

### **3.3 Inferred Information**

Information proposed by OSLO that was **not explicitly stated**.

Examples:

- suggested outcomes
- draft scope boundaries
- proposed WBS structure
- estimated schedules
- inferred work objects
- source_state = inferred
- Does **not** define truth
- Discounted or ignored for judgment depending on field type

---

## **4. Inference Modes (Controlled Expansion)**

OSLO operates in **one of three inference modes**, selected explicitly by system state or user action.

---

### **4.1 Pass-Through Mode (No Inference)**

**Trigger**

- User provides structured inputs
- User edits specific fields
- Validation pass without gaps

**Behavior**

- No inference performed
- Inputs stored as explicit
- Canonical derivation proceeds deterministically over explicit data only

**Applies to**

- Human-readable artifacts (no AI augmentation)
- Canonical representation (no inferred objects or fields)

**Use Cases**

- Experienced users
- Late-stage refinement
- Enterprise governance contexts

---

### **4.2 Gap-Flagging Mode (Detect Only)**

**Trigger**

- Required fields missing
- Ambiguous or incomplete inputs
- Validation failures

**Behavior**

- No inference performed
- Missing elements remain empty
- Issues raised for clarity, alignment, or feasibility

**Use Cases**

- Trust-sensitive environments
- Users who prefer full manual control

---

### **4.3 Assisted Expansion Mode (Inference Allowed)**

**Trigger**

- Initial onboarding
- “Draft a plan with AI”
- **Uploading unstructured documents during onboarding**
- Explicit user opt-in

**Behavior**

- OSLO may infer and propose content
- All inferred elements are labeled
- No inferred element is authoritative

**Use Cases**

- Fast onboarding
- AI-assisted drafting
- Education and guided planning

---

## **5. Onboarding Input Handling (Updated — Authoritative)**

### **5.1 Semantic Input Rule**

> During onboarding, all unstructured inputs are treated as semantic intent signals, not partial artifacts.
> 

This includes:

- free-text project descriptions
- uploaded documents (PRDs, charters, decks, notes, PDFs)

---

### **5.2 Onboarding Behavior (Explicit)**

When any unstructured input is provided during onboarding:

- Assisted Expansion Mode is activated
- OSLO generates **full draft artifacts across the default workflow**:
    - Intent
    - Context
    - Scope
    - Requirements
    - WBS
    - Resource Plan
    - Schedule
- Generated content is:
    - stored as human-readable artifacts
    - labeled source_state = inferred
- Canonical representation is derived from inferred meaning
- Judgment is discounted and issues are expected

> There is
> 
> 
> **no parse-only or partial-mapping onboarding path**
> 

---

### **5.3 What Document Upload Does**

### **Not**

### **Do**

Uploading documents during onboarding does **not**:

- populate only a subset of artifacts
- treat documents as authoritative
- bypass inference labeling
- change provenance rules
- shortcut confirmation requirements

Documents improve **extraction confidence**, not authority.

---

## **6. Field-Level Inference Eligibility**

Every field is classified as:

### **6.1 Inference-Allowed (Judgment-Discounted)**

- Scope candidates
- WBS structure
- Schedule drafts
- Work objects
- Resource assumptions

---

### **6.2 Inference-Allowed but Judgment-Prohibited**

- Outcomes
- Success criteria
- Time horizons
- Constraints
- Scope inclusions/exclusions

Stored canonically but treated as **missing for judgment** until confirmed.

---

### **6.3 Inference-Prohibited**

*(Reserved for future; none in v1.1)*

---

## **7. Provenance Enforcement**

### **7.1 Mandatory Tagging**

Every object, field, and edge must include:

- source_state
- created_by (human or OSLO agent)
- created_at

No exceptions.

---

### **7.2 No Silent Promotion**

- Inferred → Explicit requires explicit human confirmation
- New artifact version is created
- Audit trail preserved

OSLO may **never** auto-promote inference.

---

## **8. Canonical Representation Rules**

- Inferred content may exist canonically
- Inferred content does **not** define truth
- Conflicts are surfaced, not resolved silently
- Canonical ≠ confirmed

---

## **9. Judgment Interaction Rules**

### **9.1 Weighting**

| **Source State** | **Judgment Weight** |
| --- | --- |
| Explicit | Full |
| Derived | Full |
| Inferred (allowed) | Discounted |
| Inferred (judgment-prohibited) | Zero |

---

### **9.2 Issue Generation**

- Inferred content may trigger issues
- Inferred content may never resolve issues
- Inferred content may never improve scores

---

## **10. Execution-Level Inference (Tier-4)**

OSLO may infer:

- tasks
- subtasks
- execution sequencing

Constraints:

- Tier-4 impact only
- Severity-capped
- Confidence-only influence

---

## **11. User Visibility & Explainability**

Users must always be able to see:

- what was inferred
- why it was inferred
- confidence level
- judgment impact

Inference visibility is mandatory across:

- artifacts
- issues
- explanations
- reports (subject to report intent)

---

## **12. Audit & Compliance Guarantees**

The system guarantees:

1. All inference is traceable
2. All promotions are explicit
3. All judgments are explainable
4. No hallucinated authority exists

---

## **13. Invariants (Locked)**

1. Inference never equals intent
2. Inference never upgrades silently
3. Inference is always labeled
4. Inference is always discountable
5. Inference is reversible via versioning

---

## **14. Canonical Summary**

> OSLO treats onboarding inputs—free text or uploaded documents—as semantic intent signals and may infer to accelerate drafting, but it never confuses inference with intent or allows inferred meaning to become authoritative without confirmation.
> 

---

## **15. Status**

- **Version:** v1.1
- **Supersedes:** Inference Policy v1.0
- **Compatible with:**
    - Knowledge Layer v1.1
    - Steady-State Edit Policy v1.0
    - Judgment Layer v1.0
    - Health Scoring v1.0

---

If you want next, the logical follow-ups are:

- updating the **Knowledge Layer Spec onboarding section** to reference this directly, or
- generating **CI test cases** that assert onboarding document uploads always trigger Assisted Expansion (and never partial parse).