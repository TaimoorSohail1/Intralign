# Governance Layer — Detailed Responsibilities

---

## **Canonical Role**

> Governance controls OSLO’s behavior over time.
> 

It does **not** decide what is true.

It does **not** decide what something means.

It does **not** decide how something is phrased.

It answers one question only:

> “Given what OSLO is allowed to say, should it say it now, here, and in this way?”
> 

Governance is about **restraint, timing, consistency, and safety**.

---

## **Inputs (Strict)**

The Governance Layer consumes:

- Judgment Records (for issue-driven communications)
- Communication Class requests (guidance, education, orientation)
- User state & flow state (onboarding, 60-Second flow, review mode)
- Prior communication history
- System policies & feature flags

It **never** consumes:

- Raw project knowledge
- Reasoning findings directly
- Free-form language

---

## **Core Responsibilities (What Governance Owns)**

---

## **1. Communication Eligibility Enforcement**

Governance enforces **whether communication is permitted at all**, even if judgment says it *could* be.

Examples:

- Issue exists, but user is mid-onboarding → suppress
- Issue exists, but already acknowledged → suppress
- Issue exists, but confidence below threshold → defer

Judgment says *“this may be communicated.”*

Governance says *“not now.”*

---

## **2. Timing & Context Awareness**

Governance determines **when** OSLO may speak.

Includes awareness of:

- Onboarding vs planning vs execution
- First-time vs returning user
- Active flow steps (e.g., 60-Second plan questions)
- User-initiated vs system-initiated moments

**Example**

> Do not surface alignment issues while the user is still defining outcomes.
> 

This protects user experience **without weakening judgment**.

---

## **3. Frequency Capping & Fatigue Prevention**

Governance limits **how often** OSLO communicates.

Owns:

- Per-session caps
- Per-issue caps
- Per-class caps (issue vs guidance)
- Cooldown periods

This prevents:

- Alert fatigue
- Perceived nagging
- Loss of trust

Over-communication is treated as a **system bug**.

---

## **4. Deduplication & Threading**

Governance ensures OSLO does not repeat itself unnecessarily.

Owns:

- Issue deduplication (same root cause)
- Thread continuity (follow-ups vs new messages)
- Suppression of already-resolved or acknowledged items

**Example**

> One missing success criteria → one thread, not five messages.
> 

---

## **5. Message Lifecycle State Management**

Governance tracks the **state of each communication**.

Typical states:

- Open
- Acknowledged
- Acted upon
- Deferred
- Resolved
- Suppressed

This state influences:

- Whether follow-ups are allowed
- Whether escalation is permitted
- Whether silence is required

---

## **6. Policy & Safety Enforcement**

Governance enforces **system-wide behavioral policies**, including:

- No implied judgment in guidance messages
- No action recommendations without sufficient confidence
- No issue escalation during onboarding unless blocking
- No cross-class contamination (guidance ≠ issue)

This is where OSLO’s **guardrails live**.

---

## **7. Channel & Surface Selection (High-Level)**

Governance determines **which surface is allowed**, not how it looks.

Examples:

- Chat only
- Issue panel only
- Inline only
- Suppressed entirely

Communication decides *how to render*.

Governance decides *where it may appear*.

---

## **8. Feature Flags & Version Control**

Governance owns:

- Which communication classes are enabled
- Which templates are active
- Which behaviors are experimental

This allows:

- Safe rollout
- Controlled experimentation
- Rapid rollback

---

## **What Governance Explicitly Does NOT Do**

| **❌ Not Governance** | **Why** |
| --- | --- |
| Fact evaluation | That’s reasoning |
| Issue classification | That’s judgment |
| Severity or confidence | That’s judgment |
| Message wording | That’s communication |
| Tone selection | That’s rendering |
| Education content | That’s communication |
| UX layout | That’s frontend |

If governance starts “sounding smart,” it’s broken.

---

## **Relationship to Adjacent Layers**

### **Judgment → Governance**

Judgment defines **what may be said**

Governance decides **if and when it should be said**

### **Governance → Communication**

Governance grants **permission and constraints**

Communication produces **language within bounds**

Governance never upgrades authority.

It only restricts it.

---

## **Why Governance Is Essential (Even With Perfect AI)**

Without Governance:

- Correct judgments feel intrusive
- Helpful guidance feels spammy
- Users feel “talked at”
- Trust erodes despite correctness

With Governance:

- Silence feels intentional
- Messages feel timely
- OSLO feels respectful
- Adoption scales

---

## **One-Sentence Canonical Definition**

**The Governance Layer enforces timing, frequency, eligibility, and policy constraints on all OSLO communications to ensure restraint, consistency, and trust—without altering truth or meaning.**

If you want next, I can:

- Define a **Governance rule taxonomy**
- Create **example governance scenarios (good vs bad)**
- Produce a **state machine diagram for message lifecycle**
- Add **governance acceptance criteria for PR reviews**

Just say which.