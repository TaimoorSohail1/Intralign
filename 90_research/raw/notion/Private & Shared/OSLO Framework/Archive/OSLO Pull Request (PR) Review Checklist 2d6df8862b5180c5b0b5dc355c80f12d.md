# OSLO Pull Request (PR) Review Checklist

> **Goal:** Protect trust, layer integrity, and explainability while moving fast in an AI-first workflow.
> 

---

## **1. Layer Discipline (Non-Negotiable)**

**Every change must belong to exactly ONE OSLO layer.**

- I can clearly identify which OSLO layer this change belongs to
    
    ☐ Project Knowledge
    
    ☐ Reasoning
    
    ☐ Judgment
    
    ☐ Governance
    
    ☐ Communication
    
    ☐ Rendering / Surface
    
- No logic in this PR crosses layer boundaries
- No downstream layer is doing upstream work
- If multiple layers are touched, the boundary is explicit and justified

**Auto-reject if:**

- Reasoning assigns severity or confidence
- Judgment discovers new facts
- Communication decides timing or suppression
- Rendering alters meaning or policy

---

## **2. Epistemic Safety (Truth vs Assumption)**

- Explicit data remains explicit
- Inferred data is clearly marked as inferred
- Inferred nodes do **not** satisfy required constraints
- No inferred data is silently promoted to canonical truth
- Promotion from inferred → confirmed requires explicit user action

**Ask explicitly:**

> “Can OSLO still distinguish what the user said vs what it assumed?”
> 

---

## **3. Reasoning Integrity**

(Only if Reasoning layer is touched)

- Reasoning outputs are deterministic and replayable
- Findings are structural (gap, ambiguity, inference), not judgments
- Evidence chains are complete and traceable
- No severity, confidence, or impact language appears in Reasoning

**Red flag phrases:**

“risk”, “problem”, “important”, “bad”, “likely to fail”

---

## **4. Judgment Correctness**

(Only if Judgment layer is touched)

- Judgment consumes Reasoning outputs, not raw Project Knowledge
- Severity, confidence, and CAF impact are assigned explicitly
- CAF mapping (Clarity / Alignment / Feasibility) is clear
- Confidence is internal only (not exposed as a metric)

**Ask:**

> “Could two engineers replay this judgment and get the same result?”
> 

---

## **5. Governance & Policy Compliance**

(Only if Governance layer is touched)

- Behavior is policy-driven, not hard-coded
- Suppression rules are respected
- Timing and surface routing follow posture (e.g., critical-only)
- Policy versioning is preserved or updated intentionally
- No communication bypasses Governance

**Auto-reject if:**

Any component directly emits user-visible messages without governance approval.

---

## **6. Communication Safety (RCUs)**

(Only if Communication layer is touched)

- RCUs are render-agnostic
- Minimum trust-complete structure is enforced:
    - What is happening
    - Why it matters
    - How OSLO knows
    - Limits / assumptions
- Language does not imply certainty beyond evidence
- Allowed actions match confidence and policy

**Red flag phrases:**

“definitely”, “guaranteed”, “will fail”, “must”

---

## **7. Scoring & CAF Alignment**

(If scoring logic is touched)

- Only Clarity, Alignment, Feasibility are visible
- Validation confidence is internal only
- Inference improves coverage, not confidence
- Scores improve only through user validation
- Score behavior is explainable via user actions

**Ask:**

> “Would a user understand why this score changed?”
> 

---

## **8. Surface & Rendering Constraints**

(If UI or exports are touched)

- Surface does not alter meaning
- Surface does not re-evaluate logic
- Labels (“Draft”, “Assumed”, “Needs confirmation”) are applied correctly
- No hidden logic embedded in the UI layer

**Rule:**

Rendering may vary wording, never truth.

---

## **9. Correction & Accountability**

- Changes do not break supersession or correction logic
- High-impact corrections are explicitly handled
- Old RCUs are not silently invalidated

---

## **10. Trust Regression Check (Final Gate)**

Answer **YES** to all:

- OSLO could explain this change to a skeptical user
- A future engineer could audit this behavior
- No assumption is hidden
- Silence is intentional, not accidental

If any answer is **NO**, request changes.

---

## **Canonical PR Review Rule (Memorize This)**

> If a PR makes OSLO faster but less explainable, it is a bad PR.
> 

> If it makes OSLO smarter but less trustworthy, it is a bad PR.
> 

---

If you want, next I can:

- Create a **short “auto-reject” checklist**
- Produce **layer-violation examples with code snippets**
- Draft a **PR template pre-filled with these sections**
- Define **review ownership by layer (who must approve what)**