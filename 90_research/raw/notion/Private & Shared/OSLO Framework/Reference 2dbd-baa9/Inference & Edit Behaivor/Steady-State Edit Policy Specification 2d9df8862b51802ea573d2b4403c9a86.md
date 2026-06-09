# Steady-State Edit Policy Specification

---

**OSLO Architecture — Steady-State Edit Policy v1.0**

---

## **1. Purpose**

This specification defines how OSLO must behave **after a project plan has exited the initial onboarding / 60-Second flow and entered steady state**, when users edit artifacts through the UI.

The goal is to:

- preserve trust and plan stability
- maintain provenance and auditability
- prevent silent AI drift
- ensure judgment remains explainable and deterministic

> Steady state optimizes for
> 
> 
> **control and predictability**
> 

---

## **2. Definition of Steady State**

A plan is considered in **steady state** when **all** of the following are true:

1. The default workflow (Intent → Context → Scope → Requirements → WBS → Resource Plan → Schedule) has been instantiated
2. Canonical representation exists and has passed invariant validation
3. At least one judgment pass has been completed
4. The plan is no longer in onboarding or “draft plan” mode

Steady state is a **plan-level status**, not an artifact-level status.

---

## **3. Core Principle (Non-Negotiable)**

> Steady-state edits use the same canonical pipeline as onboarding, but inference scope is constrained and auto-expansion is disabled by default.
> 

The pipeline does not change.

The **policy envelope** does.

---

## **4. What Does NOT Change in Steady State**

The following behaviors are invariant across onboarding and steady state:

- Artifact versioning rules
- Immutability of published versions
- Field-level provenance (explicit, derived, inferred)
- Canonical derivation logic
- Structural invariant validation
- Issue creation semantics
- Judgment discounting rules
- Explainability and traceability guarantees

Any deviation is a **policy violation**.

---

## **5. Steady-State Edit Pipeline (Authoritative)**

Every steady-state artifact edit must execute the following **six passes**, in order.

---

### **Pass 1 — Authorial Write**

**Trigger**

- User edits a field via UI

**Behavior**

- A new artifact version is created
- Only the edited field(s) change
- Edited fields are stored as:
    - source_state = explicit
- No other fields are modified

**Invariant**

> OSLO must never auto-edit adjacent fields during Pass 1.
> 

---

### **Pass 2 — Canonical Delta Derivation**

**Behavior**

- Knowledge Layer re-derives **only canonical objects impacted by the edit**
- Downstream objects are:
    - marked stale, or
    - flagged for re-evaluation
- No new objects are created

**Explicit rule**

> This is an
> 
> 
> **incremental delta pass**
> 

---

### **Pass 3 — Local Invariant Validation**

Only invariants affected by the edit are evaluated.

**Examples**

- Editing an Outcome → validate success criteria completeness
- Editing a Requirement → validate Outcome linkage
- Editing a WBS node → validate tree structure
- Editing a Schedule date → validate dependency graph

Unrelated artifacts are not revalidated.

---

### **Pass 4 — Constrained Inference (Default: Disabled)**

**Default behavior**

- No inference is performed
- OSLO does not generate or modify any content

**Allowed behaviors**

- Flag gaps
- Raise issues
- Explain downstream impact
- Suggest optional repair actions (without writing them)

**Prohibited behaviors**

- Auto-generating new artifacts
- Auto-creating work objects
- Auto-updating schedules
- Auto-expanding scope

---

### **Pass 5 — Reasoning & Judgment Delta**

**Behavior**

- Reasoning Layer re-evaluates only impacted canonical objects
- Judgment Layer:
    - recalculates affected dimension scores
    - updates confidence deltas
    - applies Tier-4 execution weighting where applicable

**Invariant**

> No unaffected score or issue may change.
> 

---

### **Pass 6 — Explanation & Visibility**

OSLO must explain:

- what changed
- which objects were impacted
- why scores or issues changed
- what is now missing, invalid, or at risk
- what optional next steps exist

No silent outcomes are permitted.

---

## **6. Inference in Steady State (Strictly Controlled)**

Inference is **not forbidden**, but it is **never automatic**.

### **6.1 Allowed Inference Triggers**

Inference may run only if **one of the following is true**:

1. User explicitly requests it (e.g., “Ask OSLO to update related artifacts”)
2. User edits within a UI surface explicitly labeled “Draft with AI”
3. A governance policy allows auto-proposals
4. A hard invariant violation requires OSLO to propose repair options

---

### **6.2 Inference Constraints (Still Enforced)**

When inference runs in steady state:

- All inferred content is labeled source_state = inferred
- New artifact versions are created
- No inferred content is authoritative
- No inferred content silently overwrites explicit content
- Judgment discounting applies

---

## **7. Blast Radius Rules**

Steady-state inference is **local by default**.

- Inference may only affect:
    - the edited artifact, or
    - directly downstream artifacts
- Cross-workflow or upstream inference requires explicit user action

---

## **8. Prohibited Behaviors (Hard Stops)**

The following are **explicitly forbidden** in steady state:

- Silent inference
- Cross-artifact auto-expansion
- Implicit provenance promotion
- Full plan regeneration
- Background inference jobs without user intent
- Score improvement via inferred content

Any occurrence is a **severity-1 defect**.

---

## **9. Interaction with Judgment & Health Scoring**

- Explicit edits can improve or degrade scores
- Inferred content:
    - may increase issue count
    - may reduce confidence
    - may never improve scores
- Tier-4 execution signals remain severity-capped

---

## **10. Audit & Compliance Guarantees**

The system guarantees that in steady state:

1. Every edit is versioned
2. Every inference is intentional
3. Every score change is explainable
4. No AI-driven drift can occur
5. Users retain full control

---

## **11. Canonical Summary (Reusable)**

> In steady state, OSLO applies the same canonical derivation pipeline as onboarding, but inference is constrained, local, and never auto-expands the plan without explicit user intent.
> 

---

## **12. Status**

- **Version:** v1.0
- **Applies to:** Post-onboarding plans
- **Compatible with:**
    - Knowledge Layer v1.1
    - Inference Policy v1.0
    - Judgment Layer v1.0
    - Health Scoring v1.0

---

If you want, next I can:

- generate a **state machine diagram** (Onboarding → Steady → Assisted Repair),
- produce a **CI test matrix** specific to steady-state edits, or
- draft **developer guardrails** mapping UI actions to allowed inference scopes.