# Communication Layer — Detailed Responsibilities

---

## **Canonical Role**

> The Communication Layer translates governed intent into clear, bounded human communication—without inventing truth, meaning, or authority.
> 

It does **not** decide what is true.

It does **not** decide what something means.

It does **not** decide when to speak.

It answers one question only:

> “How do we explain or guide, given what we are allowed to say?”
> 

---

## **Inputs (Strict)**

The Communication Layer consumes **only governed inputs**:

- Approved Judgment Records (for issue communications)
- Approved Communication Requests (for guidance / education)
- Communication class (issue, guidance, education, etc.)
- Allowed actions and boundaries
- Channel permissions (chat, panel, inline, etc.)

It **never consumes**:

- Raw project knowledge
- Reasoning findings
- Ungoverned prompts
- Free-form user state inference

If the input is not already approved upstream, Communication must not speak.

---

## **Core Responsibilities (What Communication Owns)**

---

## **1. Structured Message Composition (RCU Enforcement)**

Communication is responsible for **assembling messages using RCUs (Reusable Communication Units)**.

This includes:

- Selecting the correct RCU *class*
- Enforcing required sections
- Omitting disallowed sections
- Preserving boundary statements

RCUs prevent:

- Hallucination
- Over-claiming
- Inconsistent explanations

**Example**

- Issue RCU includes: diagnostic, why it matters, evidence, boundary, actions
- Guidance RCU excludes: severity, risk, corrective language

---

## **2. Class-Aware Language Rendering**

Communication renders language **appropriate to the communication class**.

| **Class** | **Language Characteristics** |
| --- | --- |
| Issue | Precise, bounded, evidentiary |
| Guidance | Neutral, supportive, non-evaluative |
| Education | Explanatory, conceptual |
| Clarification | Question-oriented, scoped |
| Orientation | Expectation-setting |

**Hard rule**

Guidance must never *sound like judgment*.

Issues must never *sound casual or speculative*.

---

## **3. Boundary & Confidence Preservation**

Communication must **explicitly preserve**:

- Confidence levels
- Assumptions
- Unknowns
- Scope limits

It may *rephrase* boundaries for clarity, but may not:

- Upgrade confidence
- Remove uncertainty
- Introduce implied authority

If a boundary is lost in translation, the system is broken.

---

## **4. Action Presentation (Within Limits)**

Communication presents **only actions explicitly allowed upstream**.

Examples:

- Ask for clarification
- Suggest refinement
- Offer to explain further
- Provide next step guidance

It must not:

- Invent new actions
- Imply urgency beyond severity
- Suggest corrective steps in guidance messages

Actions are **options**, not commands.

---

## **5. Channel-Specific Adaptation (Not Selection)**

Communication adapts messages **to the constraints of the channel**.

Owns:

- Length adaptation (chat vs panel)
- Formatting
- Call-to-action placement
- Progressive disclosure

Does NOT own:

- Channel selection
- Timing
- Frequency

Governance decides *where*.

Communication decides *how it reads there*.

---

## **6. Voice Consistency (OSLO Voice)**

Communication enforces the **OSLO voice**, which is:

- Calm
- Precise
- Non-judgmental
- Explicit about limits
- Outcome-oriented

Voice consistency is enforced via:

- Templates
- Phrase constraints
- Disallowed language lists

This ensures OSLO sounds like a **system**, not a personality.

---

## **7. User-Initiated vs System-Initiated Handling**

Communication distinguishes:

- User-asked questions → direct, scoped responses
- System-initiated messages → restrained, contextual explanations

It must never escalate:

- A user question into a system critique
- A guidance moment into an issue

Escalation requires Judgment + Governance approval.

---

## **What Communication Explicitly Does NOT Do**

| **❌ Not Communication** | **Why** |
| --- | --- |
| Fact discovery | That’s reasoning |
| Issue classification | That’s judgment |
| Severity/confidence | That’s judgment |
| Timing/frequency | That’s governance |
| Suppression decisions | That’s governance |
| Flow control | That’s governance |
| UX layout ownership | That’s frontend |

If Communication starts deciding *what* or *when*, trust collapses.

---

## **Relationship to Adjacent Layers**

### **Governance → Communication**

Governance provides:

- Permission
- Constraints
- Class
- Channels

Communication provides:

- Language
- Structure
- Clarity

Communication never exceeds its permissions.

---

## **Why Communication Must Be Constrained**

If Communication is free-form:

- Users feel judged
- AI feels opinionated
- Errors feel personal
- Trust erodes quickly

If Communication is constrained:

- Messages feel intentional
- Boundaries are visible
- Silence feels respectful
- OSLO feels reliable

---

## **One-Sentence Canonical Definition**

**The Communication Layer renders governed judgments and guidance into clear, class-appropriate, boundary-preserving language—without inventing truth, meaning, or authority.**

If you want next, I can:

- Define **RCU schemas per communication class**
- Create a **“disallowed language” checklist**
- Show **examples of good vs broken communication outputs**
- Map communication responsibilities to **chat vs issue panel UX**

Just say which.