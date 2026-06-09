# Governance Decision Diagram vs OSLO Intent

## **High-level verdict**

This diagram correctly identifies the **three inputs that must jointly constrain behavior**:

- **Tier context**
- **Posture context**
- **Governance policy**

That’s a big win.

However, the diagram currently teaches this incorrect mental model:

> “Governance decides what happens next.”
> 

In OSLO, governance **does not decide outcomes** — it **decides constraints on exposure, action, and communication**.

That distinction matters a lot in implementation.

---

## **1) The “Triple Intersection” is treated as a decision engine (wrong abstraction)**

### **Misalignment**

The central diamond (“Triple Intersection”) emits:

- PERMIT
- DENY
- REQUIRE_APPROVAL
- DOWNGRADE

This makes governance look like a **binary/ternary decision gate**.

In OSLO:

- Governance resolves **a disposition package**
- Not a single decision verb

### **Risk**

Engineers will implement:

```
if permit → do thing
else if deny → suppress
```

This collapses:

- partial disclosure
- epistemic labeling requirements
- posture-based constraint shaping
- modality control (ask vs warn vs suggest)

### **Fix**

Rename the diamond to:

> Disposition Resolver (Constraint Resolution)
> 

And change outputs from **verbs** to **packages**:

- DispositionPackage {
    - decision_class
    - scope (communication | execution | both)
    - allowed_action_classes
    - required_disclosures
    - posture_adjustment
    - policy_version
        
        }
        

This keeps governance authoritative without making it “the decider.”

---

## **2) “Execute Mutation / Expose Issue” is dangerously combined**

### **Misalignment**

The PERMIT path leads to:

> Execute Mutation / Expose Issue
> 

This merges two fundamentally different authorities:

- **Execution authority** (L6)
- **Exposure authority** (L5)

In OSLO, these are never the same decision.

### **Risk (high)**

This is how you get:

- silent execution without user awareness
- user-facing messages that imply action happened when it didn’t
- unsafe automation escalation

### **Fix**

Split this into two distinct outcomes:

- **Authorize Execution (Action Class + Scope)** → L6
- **Authorize Exposure (Visibility + Disclosure Rules)** → L5

They may both be authorized by the *same* disposition package — but they must be separate edges.

---

## **3) “Silence / Log-Only” hides an epistemic obligation**

### **Misalignment**

DENY → Silence / Log-Only

This implies:

> “If denied, nothing is shown.”
> 

But OSLO explicitly allows:

- *internal awareness without external exposure*
- *latent issues that affect health but are not surfaced*
- *suppressed-but-counted risk*

### **Risk**

You’ll lose:

- internal risk accumulation
- health degradation signals
- future escalation context

### **Fix**

Rename this to:

> Suppress External Exposure (Retain Internal Signal)
> 

And explicitly note:

- Issue remains in canon
- Health scores still update
- Governance may revisit later

This preserves OSLO’s “silent risk” capability.

---

## **4) “Request User Confirmation” is underspecified and unsafe**

### **Misalignment**

REQUIRE_APPROVAL → Request User Confirmation

This sounds like a UX step, but OSLO treats confirmation as:

- a **new assertion**
- not a final authorization

### **Risk**

Engineers may:

- treat confirmation as a bypass
- skip re-governance
- allow user input to directly trigger execution

### **Fix**

Change this path to:

> Request User Confirmation → Intake (New Assertion Event)
> 

And explicitly require:

- re-entry through L1
- re-evaluation by Judgment
- re-resolution by Governance

This preserves fail-closed behavior.

---

## **5) “Apply Safe/Restricted Variant” hides posture semantics**

### **Misalignment**

DOWNGRADE → Apply Safe/Restricted Variant

This suggests:

- a pre-baked fallback
- static behavior

In OSLO, downgrade is:

- **posture-aware**
- **context-sensitive**
- **policy-driven**

### **Risk**

This becomes:

- “enterprise-lite”
- “dumbed-down mode”
- hard-coded variants that rot over time

### **Fix**

Rename to:

> Apply Policy-Constrained Variant (Posture-Adjusted)
> 

And annotate:

- Variant selection is derived from:
    - posture context
    - tier limits
    - policy rules
- Not a fixed alternative

---

## **6) Tier context is treated as a gating input (too strong)**

### **Misalignment**

Tier (Free vs Pro vs Enterprise) feeds directly into the decision diamond.

Tier **should constrain capabilities**, not *decide behavior*.

### **Risk**

You’ll encode:

- “free users don’t deserve safety”
- “enterprise users bypass governance”
    
    (both bad outcomes)
    

### **Fix**

Annotate Tier as:

> Capability Constraint (Upper Bound)
> 

Tier should:

- limit what *can* be authorized
- never force what *must* happen

This is subtle but important.

---

## **7) Missing: epistemic disclosure requirements**

### **Misalignment**

Nowhere in the diagram is it explicit that governance controls:

- epistemic labeling
- uncertainty disclosure
- explanation limits

This is one of OSLO’s defining features.

### **Risk**

Communication will drift into:

- overconfidence
- unqualified claims
- unsafe explanations

### **Fix**

Add an explicit output from governance:

> Disclosure Requirements
> 
- epistemic status must be shown
- confidence thresholds
- limitations required

Even a small annotation is enough.

---

# **Minimal Fix Set (Diagram-Safe)**

If you want to keep the diagram visually simple, do these **six changes**:

1. Rename “Triple Intersection” → **Disposition Resolver**
2. Replace PERMIT/DENY/etc. with **Disposition Packages**
3. Split “Execute / Expose” into two separate authorizations
4. Reframe “Silence” as **Suppress External Exposure**
5. Route “User Confirmation” back through Intake
6. Rename “Safe/Restricted Variant” as **Policy-Constrained Variant**

These changes **do not add complexity**, but they prevent catastrophic misimplementation.

---

## **Bottom line**

Right now, this diagram teaches:

> governance decides what happens
> 

OSLO must teach:

> governance decides what is
> 
> 
> *allowed*
> 
> *how it may be expressed*
> 
> *what must be disclosed*
> 
> *what actions may occur under which posture*
> 

You’re very close.

This is a **strong governance core**, it just needs its authority boundaries made explicit.

If you want next, I can:

- rewrite this diagram as a **governance disposition contract**, or
- produce a **governance test-case matrix (BDD-ready)** that engineering can implement directly.