# Layer Architecture Review Template (Forced Invariant Extraction)

---

**Layer:** __________________________

**Playbook Version:** ______________

**Reviewer(s):** ___________________

**Date:** __________________________

> Review Goal:
> 
> 
> *implicit invariants, authority boundaries, attention rules, and failure defaults*
> 
> **before implementation**
> 

---

## **PRE-READ REQUIREMENT (Non-Negotiable)**

Before the meeting, all participants must have:

- Read the layer playbook end-to-end
- Identified at least **one place they were tempted to “simplify”**

---

## **PASS 1 — Authority Pass**

**(Who is allowed to do what?)**

> Goal: eliminate ambiguous ownership.
> 

### **Questions (Answer explicitly)**

- What **can this layer mutate**?
- What **can it never mutate**, even if it knows it’s wrong?
- Where does **authority enter** this layer?
- Where does authority **explicitly stop**?
- Can this layer ever act **without user authorization**? If yes, when?

### **Forced Outputs**

- **Authority Invariants**
    - Example: “This layer may only write via X”
- **Authority Anti-Invariants**
    - Example: “This layer must never patch Y”

⬜ Completed

⬜ Gaps found → list below

---

## **PASS 2 — Attention Pass**

**(What has a right to user attention?)**

> Goal: prevent accidental interruption or spam.
> 

### **Questions**

- Which entities can surface automatically?
- Which entities **exist silently by default**?
- Which entities **must never interrupt**?
- What requires Governance approval before surfacing?

### **Forced Outputs**

- **Attention-Eligible Entities**
- **Attention-Forbidden Entities**
- **Silent-by-Default Entities**

⬜ Completed

⬜ Gaps found → list below

---

## **PASS 3 — Default Behavior Pass**

**(What happens if no one intervenes?)**

> Goal: make “do nothing” behavior explicit.
> 

### **Questions**

- If the system is unsure, what does it do?
- If the user ignores this, what persists?
- If no action is taken, what changes?
- Is silence an acceptable outcome?

### **Forced Outputs**

- **Default Actions**
- **Default Suppressions**
- **No-Op Outcomes**

⬜ Completed

⬜ Gaps found → list below

---

## **PASS 4 — Failure & Degradation Pass**

**(What happens when things go wrong?)**

> Goal: remove magical recovery assumptions.
> 

### **Questions**

- What happens if input is malformed?
- What happens if upstream data is wrong?
- What happens if authorization is missing or expired?
- What happens under **Safe / Degraded / Constrained** reliability states?

### **Forced Outputs**

- **Failure Behaviors**
- **Freeze Semantics**
- **Last-Known-Good Rules**

⬜ Completed

⬜ Gaps found → list below

---

## **PASS 5 — Misuse & Temptation Pass**

**(How might a smart engineer accidentally break this?)**

> This is the most important pass.
> 

### **Ask explicitly:**

> “If you were trying to be helpful, where would you be tempted to cheat?”
> 

### **Capture:**

- Tempting shortcuts
- “Just this once” logic
- Optimizations that violate boundaries
- Places where logic *feels redundant*

### **Forced Outputs**

- **Known Temptations**
- **Explicitly Forbidden Shortcuts**

⬜ Completed

⬜ Gaps found → list below

---

## **POST-REVIEW ARTIFACT (MANDATORY)**

### **Layer Invariants & Anti-Invariants v1.0**

This is the only artifact produced from the review.

### **Invariants (Must Always Hold)**

- …
- …

### **Anti-Invariants (Must Never Occur)**

- …
- …

> This artifact becomes:
> 
- onboarding material
- PR review reference
- dispute resolution authority

---

## **IMPLEMENTATION READINESS CHECK**

Implementation **may not begin** until:

⬜ All five passes completed

⬜ Invariants document written

⬜ Known gaps either resolved or explicitly deferred

⬜ Lead engineer agrees with this statement:

> “If everything else fails, this layer should still behave exactly as described here.”
> 

---

## **REVIEW SIGN-OFF**

**Lead Engineer:** ___________________  Date: ________

**Founder / Architect:** ______________ Date: ________

---

## **USAGE NOTE (IMPORTANT)**

- Do **not** skip passes
- Do **not** merge passes
- Do **not** accept “that’s obvious” as an answer

> If something had to be explained verbally, it must be written down.
> 

---

## **Why This Template Works**

- Forces negative space into view
- Prevents “helpful” violations
- Converts tacit understanding into enforceable invariants
- Scales across layers and future execution phase

---

### **If you want next, I can:**

- Pre-fill this template **specifically for the Knowledge Layer**
- Convert it into a **Notion database + checklist**
- Create a **PR review checklist auto-derived from invariants**
- Design a **“layer confidence score”** for implementation readiness