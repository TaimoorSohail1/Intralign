# Human Plan View — Implicit Data Annotation & Interaction Model

---

## **1. Goal (What this must achieve)**

The Human Plan View must allow users to:

- Read the plan naturally (no cognitive overload)
- Immediately distinguish **explicit vs inferred** content
- Interact with inferred content **at the point of meaning**
- Confirm, edit, or reject implicit assumptions safely
- Never confuse inference with asserted truth

This is not optional — it is how trust is preserved.

---

## **2. Core Principle**

> Implicit data should be readable inline,
> 

> but authoritative only on interaction.
> 

In other words:

- Passive reading → minimal annotation
- Active attention (hover / focus) → full epistemic clarity + controls

---

## **3. Annotation Strategy (Recommended)**

### **3.1 Inline Visual Treatment (Low Noise)**

Implicit / inferred content should be:

- **Visually distinct but subtle**
- Never loud or alarming
- Never hidden or footnoted

Recommended patterns (pick one primary):

- Slightly different text color (e.g. muted accent)
- Dotted or soft underline
- Light background tint (very low contrast)

❌ Avoid:

- Warning icons inline
- Red / error styling
- Tooltip-only disclosure (too hidden)

The goal is *recognition*, not interruption.

---

## **4. Hover / Focus Interaction (Where authority appears)**

When a user hovers, clicks, or focuses on an inferred word or phrase, a **context panel** appears.

### **4.1 Required Information (Non-Negotiable)**

The hover panel must include:

1. **Epistemic Status**
    - Proposed / Inferred / Synthetic
2. **Source**
    - “Derived by OSLO”
3. **Why it exists**
    - Short, concrete explanation
4. **Confidence / certainty**
    - Low / Medium / High
5. **Actions**
    - Confirm
    - Edit
    - Reject

Example (conceptual):

```
Target timeframe: 90 days
Status: Proposed (Inferred)
Why: Derived from similar onboarding initiatives
Confidence: Medium

[Confirm] [Edit] [Reject]
```

---

## **5. Action Semantics (Very Important)**

Actions must map cleanly to system behavior:

### **Confirm**

- Converts this value into **human-authored**
- Triggers G-03 authorization flow
- Promotes to canonical upon approval
- Retires machine-derived artifact

### **Edit**

- Opens inline edit
- Edited value becomes human-authored
- Original inference retained for audit

### **Reject**

- Marks inference as rejected
- Removes it from projection
- Does **not** delete evidence chain
- Prevents re-suggestion unless context changes

No silent mutation. Ever.

---

## **6. Reading vs Editing Modes (Strong Recommendation)**

To reduce cognitive load:

- **Default mode**: Reading
    - Subtle annotation only
- **Edit / Review mode**: Explicit
    - Clear highlighting
    - All inferred elements discoverable

This aligns perfectly with:

- Onboarding
- 60-second plan review
- Executive walkthroughs

---

## **7. What Must Never Happen (Hard Rules)**

The human plan view must never:

- Render inferred content without labeling
- Auto-confirm inferred content
- Persist changes without explicit action
- Use language implying truth (“will”, “is”, “confirmed”)
- Collapse multiple inferred elements into one action

If any of these occur, the architecture is violated.

---

## **8. One-Line Design Invariant (Use This)**

> Inference should feel helpful when read,
> 

> and accountable when touched.
> 

---

## **9. Why This Design Is Correct**

This approach:

- Preserves canonical authority
- Makes implicit assumptions visible
- Encourages intentional confirmation
- Avoids onboarding overwhelm
- Scales from novice → expert users
- Aligns perfectly with your Reasoning → Projection → Promotion model

---

## **Optional Next Steps (If Helpful)**

I can next:

- Produce a **simple wireframe sketch description** engineers can build from
- Define a **UI Projection Contract** that formally maps machine artifacts → hover panels
- Walk through a **real onboarding example** with 3 inferred elements and all interactions

But directionally:

**Yes — annotate inline, disclose on hover, act deliberately.**

You’re designing epistemic trust, not just UI.