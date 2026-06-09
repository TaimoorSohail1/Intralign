# Implementation-ready Prep Checklist

---

## **1. Establish the Non-Negotiables (5 minutes)**

You want explicit verbal alignment on these. If there’s hesitation here, pause implementation.

### **Confirm shared understanding of:**

- **Canonical truth is sacred**
    - Knowledge stores *what is known*, not what is useful, correct, or convenient
- **No layer except Knowledge mutates canon**
- **No silent interpretation**
    - Every structural change must be traceable to user authorization
- **Snapshots, not live state, feed Reasoning**
- **Silence is acceptable**
    - Missing data is better than invented certainty (outside onboarding scope)

📌 *If your lead tries to “simplify” any of these, that’s a red flag.*

---

## **2. Clarify the Physical Data Model vs Logical Model (Critical)**

This is where many systems quietly drift.

### **Explicit questions to ask:**

- Are we modeling Knowledge as:
    - a **graph**
    - a **relational schema**
    - or a **hybrid**?
- How are **explicit / inferred / proposed** states represented:
    - separate node types?
    - flags on nodes?
    - separate stores?

### **You want agreement that:**

- **Physical colocation ≠ epistemic equivalence**
- Inferred elements may live in the same graph **only if epistemic state is first-class and enforced**
- Proposed elements **never enter canonical reads**

📌 *This avoids “it’s all just data” thinking.*

---

## **3. Walk Through the Only Legal Write Paths**

Do not assume this is obvious.

### **You should explicitly review:**

- The **single canonical commit function**
- What constitutes a valid authorization_context
- How onboarding implicit authorization is detected and expired
- What happens when authorization is missing or malformed

### **Ask directly:**

> “Show me how an unauthorized write fails.”
> 

If the answer is vague → stop and design this first.

---

## **4. Snapshot Semantics (Often Missed, Very Expensive Later)**

Ensure your lead understands this is **not optional plumbing**.

### **Align on:**

- Snapshot immutability guarantees
- Snapshot identity propagation to:
    - Reasoning
    - Judgment
    - Governance decisions
- Whether snapshots are:
    - copy-on-write
    - version pointers
    - materialized views

### **Ask:**

> “Can we deterministically replay a reasoning run from a snapshot six months later?”
> 

If not, the design is incomplete.

---

## **5. Representation Drift Is a Feature, Not a Bug**

This is subtle and important.

### **Ensure agreement that:**

- Human-readable and machine-readable **will diverge**
- Drift is **detectable, not auto-fixed**
- Drift does **not block progress**
- Drift surfaces as a *signal*, not a mutation

### **Ask:**

> “What happens if a user edits narrative text that contradicts structured fields?”
> 

You want:

- proposal
- review
- explicit acceptance
    
    —not silent sync.
    

---

## **6. Boundaries With Ingestion (Prevent Scope Creep)**

Many engineers will want to “just parse it here.”

### **Make explicit:**

- Knowledge does **not** parse
- Knowledge does **not** extract
- Knowledge does **not** interpret text
- Knowledge only accepts **authorized commits**

Ask:

> “Where does raw text live, and how does it die?”
> 

If raw text can leak into canonical reads → that’s a violation.

---

## **7. Reliability & Safe State Expectations**

Make sure they understand Knowledge behavior under failure.

### **Align on:**

- Freeze semantics under **Safe**
- Last-known-good snapshot usage
- No auto-recovery
- Explicit transitions only

Ask:

> “If something feels wrong, what does the Knowledge layer do?”
> 

Correct answer: **stop mutating, preserve state, wait.**

---

## **8. Minimal Implementation Order (Practical Guidance)**

Give your lead a **safe build sequence**.

Recommended order:

1. Canonical schema + epistemic state modeling
2. Commit gate + authorization context validation
3. Snapshot creation + retrieval
4. Versioning & supersession
5. Drift detection (read-only)
6. Reliability freeze behavior

📌 *Anything else is premature.*

---

## **9. Define “Done” for v1 Knowledge**

Avoid endless refinement.

### **v1 is complete when:**

- Unauthorized writes are impossible
- Snapshot-based reads exist
- Explicit/inferred/proposed are distinguishable
- Drift is detectable
- Reasoning can consume snapshots safely

Not required for v1:

- Performance optimization
- Fancy graph traversal
- Execution-phase modeling

---

## **10. Close With One Framing Statement (Use This Verbatim)**

End the discussion by saying:

> “The Knowledge layer is the part of the system we must still trust when everything else is wrong.”
> 

If your lead engineer agrees with that sentence, you’re aligned.

---

## **Optional: One-Page Prep You Can Share Ahead of the Meeting**

If you want, I can condense this into:

- a **1-page pre-read for your lead**
- a **meeting agenda with decision checkboxes**
- or a **post-meeting implementation contract** both of you sign off on

Just tell me how you want to proceed.