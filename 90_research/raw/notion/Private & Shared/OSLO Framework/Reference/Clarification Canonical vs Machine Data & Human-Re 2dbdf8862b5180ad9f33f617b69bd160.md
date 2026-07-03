# Clarification: Canonical vs Machine Data & Human-Readable Plan View

---

**Audience:** Lead Engineer

**Purpose:** Correct earlier explanation and align on how implicit / inferred plan data is stored and displayed

---

## **1. The Correction (Plain English)**

I previously said that the **canonical store contains explicit and implicit (proposed) plan objects**.

That was **incorrect**.

**Correct model:**

- **Canonical store contains only explicitly confirmed plan data**
- **Implicit / inferred / proposed data lives in the machine (non-canonical) repository**
- **Both are shown together in the human-readable plan view**

Visibility ≠ authority.

---

## **2. Three Plan Representations (Storage)**

The Knowledge Layer stores plan data in **three forms**:

### **1) Human-Authored**

- What the user types or edits
- Drafts, confirmations, edits
- Not canonical until authorized

### **2) Canonical**

- Asserted source of truth
- Explicitly confirmed by the user
- Governance-authorized (G-03)
- Used for execution, reporting, guarantees

### **3) Machine (Non-Canonical)**

- System-derived data only
- Includes:
    - Inferred elements
    - Implicit assumptions
    - Synthetic placeholders
    - Findings
    - Evidence chains
- Never asserted as truth
- Always supersedable

**Key rule:**

👉 **Implicit / inferred data is never stored in the canonical store.**

---

## **3. Human-Readable Plan View (Important Distinction)**

The **human-readable plan view is not a storage form**.

It is a **projection** (a composed UI view).

### **What the user sees during onboarding**

The plan view combines:

- **Explicit, confirmed data** (from Canonical)
- **Proposed / implicit data** (from Machine)

Side-by-side.

This is intentional and required for onboarding.

---

## **4. How Explicit and Implicit Data Appear Together**

From the user’s perspective:

```
Outcome: Improve customer onboarding completion rate   ✔ Confirmed

Target timeframe: 90 days
Status: Proposed (Inferred by OSLO)
Reason: Derived from similar initiatives
```

From the system’s perspective:

| **Element** | **Storage** | **Authority** |
| --- | --- | --- |
| Outcome | Canonical | Asserted truth |
| Timeframe | Machine (Proposed) | Non-canonical |

The UI **renders both**, but **does not collapse them**.

## **Human Plan View — Narrative Example (What the User Reads)**

**Outcome:** Improve customer onboarding completion rate ✔️

OSLO has identified a **proposed target timeframe of 90 days** for this outcome, based on patterns observed in similar onboarding initiatives.

This timeframe is suggested to provide a realistic window for measurable improvement, but it has not yet been confirmed.

You can review, adjust, or confirm this assumption before it becomes part of the plan.

---

## **Inline Annotation Model (What’s Actually Happening)**

### **Visual Treatment (Passive Reading)**

- **“90 days”** appears with subtle annotation (e.g. soft underline or muted accent color)
- No warning icon
- No interruption
- Reads naturally as part of the plan

Example (conceptual):

> OSLO has identified a proposed target timeframe of
> 
> 
> **90 days**
> 

---

## **Hover / Focus Interaction (Active Attention)**

When the user hovers over **“90 days”**, a contextual panel appears:

```jsx
Target timeframe: 90 days

Status: Proposed (Inferred by OSLO)
Confidence: Medium

Why this exists:
Derived from historical onboarding initiatives with similar scope and constraints.

What you can do:
[Confirm]  [Edit]  [Reject]
```

---

## **5. Critical UI Rules (Must Be Enforced)**

When implicit data is shown in the human-readable view, it must:

- Be clearly marked **Proposed / Inferred**
- Never appear indistinguishable from confirmed data
- Be editable, confirmable, or rejectable
- Link to “why OSLO inferred this”

If implicit data appears unmarked, **that is a trust bug**.

UI must annotate inferred data and support authorized decisions by user, proposed UI approach can be found here: [**Human Plan View — Implicit Data Annotation & Interaction Model**](../Reference%202dbd-be56/Human%20Plan%20View%20%E2%80%94%20Implicit%20Data%20Annotation%20&%20Inter%202dbdf8862b5180e089b1c772c1da198d.md) 

---

## **6. Promotion Path (No Shortcuts)**

Implicit data becomes canonical **only** through this path:

```
Machine (Proposed / Inferred)
        ↓ shown in plan view
Human confirms or edits
        ↓ G-03 authorization
Canonical store
```

Reasoning never writes canon.

Rendering never implies truth.

---

## **7. One-Sentence Mental Model (Use This)**

> Canonical = confirmed reality
> 

> Machine = system claims about reality
> 

> Human-readable view = both, clearly labeled
> 

---

## **8. Why This Matters**

This design ensures:

- Onboarding is readable and complete
- Inference is transparent
- Trust is preserved
- Canonical truth is never polluted
- Replays and hypotheticals are safe

---

## **Final Check**

If you remember only one thing:

> Implicit data is visible to humans, but authoritative only after confirmation.
> 

That’s the system.

---

If you want, I can also provide:

- A **diagram version** of this page for onboarding engineers, or
- A **worked onboarding example** with actual data objects to validate implementation details.