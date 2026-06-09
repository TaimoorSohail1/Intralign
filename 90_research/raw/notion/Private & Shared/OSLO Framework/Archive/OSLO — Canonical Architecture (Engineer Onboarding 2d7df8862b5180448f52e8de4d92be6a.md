# OSLO — Canonical Architecture (Engineer Onboarding v1.0)

---

---

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER & UI SURFACES                           │
│                                                                     │
│   Chat  |  Issues Panel  |  Plan / Artifact UI  |  Exports (PDF)    │
│                                                                     │
│   (Humans interact here — no logic authority)                        │
└───────────────────────────────▲─────────────────────────────────────┘
                                │
                                │ Rendered Messages + CTAs
                                │ (language, tone, structure)
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                     COMMUNICATION LAYER                              │
│                                                                     │
│  • Message phrasing & tone                                          │
│  • Surface-specific rendering (chat vs panel vs export)             │
│  • CTA presentation (authorized only)                               │
│  • Consistent structure & uncertainty framing                       │
│                                                                     │
│  Answers: “How do we say it?”                                       │
│                                                                     │
│  🚫 Cannot decide to speak                                          │
│  🚫 Cannot change truth or scores                                   │
└───────────────────────────────▲─────────────────────────────────────┘
                                │
                                │ Authorized Intent + Surface Rules
                                │ (no language)
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                       GOVERNANCE LAYER                               │
│                                                                     │
│  • Whether to communicate                                           │
│  • When to communicate                                              │
│  • Which surface(s) are allowed                                     │
│  • CTA authorization (but not execution)                            │
│  • Suppression & silence                                            │
│  • Policy enforcement & guardrails                                  │
│                                                                     │
│  Answers: “Should we speak — and how?”                              │
│                                                                     │
│  🚫 Cannot phrase messages                                          │
│  🚫 Cannot change scores or issues                                  │
└───────────────────────────────▲─────────────────────────────────────┘
                                │
                                │ Scores, Severity, Risk Signals
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                        JUDGMENT LAYER                                │
│                                                                     │
│  • Clarity / Alignment / Feasibility scores                         │
│  • Severity classification                                          │
│  • Threshold comparisons                                            │
│  • Risk concentration & deltas                                      │
│                                                                     │
│  Answers: “How bad / how risky is it?”                              │
│                                                                     │
│  🚫 Cannot communicate                                              │
│  🚫 Cannot mutate plans                                             │
└───────────────────────────────▲─────────────────────────────────────┘
                                │
                                │ Issues, Inferences, Evidence
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                        REASONING LAYER                               │
│                                                                     │
│  • Structural analysis                                              │
│  • Issue detection (clarity / alignment / feasibility)              │
│  • Inference generation (explicitly labeled)                        │
│  • Evidence chains                                                  │
│  • Deterministic multi-pass reasoning                               │
│                                                                     │
│  Answers: “What is true, missing, inconsistent, or fragile?”        │
│                                                                     │
│  🚫 Cannot decide to speak                                          │
│  🚫 Cannot generate language                                        │
└───────────────────────────────▲─────────────────────────────────────┘
                                │
                                │ Canonical Project Data (read-only)
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                     PROJECT KNOWLEDGE LAYER                          │
│                                                                     │
│  • Artifacts (Charter, Scope, WBS, Schedule, etc.)                  │
│  • Goals, outcomes, metrics                                         │
│  • Constraints & assumptions                                       │
│  • Explicit + inferred elements (flagged)                           │
│                                                                     │
│  Source of truth — mutated only via explicit UI actions             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## **How Engineers Should Read This Diagram**

### **Vertical rule (most important)**

> Truth flows up. Authority flows down.
> 
- Lower layers **produce facts**
- Upper layers **decide exposure**
- UI **never decides logic**

---

## **Single-Sentence Responsibility Test (Use in PR Reviews)**

- **Project Knowledge** → *What data exists?*
- **Reasoning** → *What is structurally true or broken?*
- **Judgment** → *How severe or risky is that?*
- **Governance** → *Should the user be told — and how?*
- **Communication** → *What exact words appear on screen?*

If a piece of code answers the wrong question → it’s in the wrong layer.

---

## **Non-Negotiable Architecture Invariants**

- Chat **never mutates** plans
- Governance **never writes language**
- Reasoning **never considers UX**
- Judgment **never triggers communication**
- Communication **never decides truth or severity**

Violating these makes the system **feel “smart” but untrustworthy**.

---

## **Why This Architecture Matters**

This design:

- Prevents agentic drift
- Enables AI-first development safely
- Allows independent iteration per layer
- Makes bugs diagnosable (“wrong layer”)
- Scales from MVP → enterprise without rewrites

---

## **How to Use This for Onboarding**

Recommended onboarding flow:

1. Walk engineers through this diagram
2. Hand them the **five layer playbooks**
3. Require PRs to cite **which layer they modify**
4. Reject PRs that cross layer boundaries

---

### **If you want next**

I can:

- Turn this into a **printable one-pager PDF**
- Create a **“layer violation checklist”** for PRs
- Map this diagram to **repo folder structure**
- Or produce a **30-minute engineer onboarding script**

Just tell me.