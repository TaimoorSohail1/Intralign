# PLG 60-Second Flow Wireframes

## Purpose

Define the first-time freemium activation experience.

This flow is separate from the core daily Outcome Space workspace.

Primary goal:
Create the realization: “OSLO understands my project.”

---

# Flow Overview

```text
Landing / Start
   ↓
Multi-Input Intake
   ↓
Project MRI Reveal
   ↓
Initial Confidence + Findings
   ↓
Deep Refinement
   ↓
Activation Moment
   ↓
Transition to Outcome Space
```

---

# Screen 1 — Start New Outcome Space

```text
┌─────────────────────────────────────────────┐
│ Create an Outcome Space                     │
│                                             │
│ Bring anything OSLO should understand.      │
│                                             │
│ [ Paste project description...           ]  │
│                                             │
│ Drag files here:                            │
│ Charter | Plan | Transcript | Jira export   │
│                                             │
│ Quick Start Examples:                       │
│ [SaaS Launch] [AI Initiative] [PMO Rollout] │
│ [Customer Onboarding] [Enterprise Change]   │
│                                             │
│ [Analyze with OSLO]                         │
└─────────────────────────────────────────────┘
```

## Requirements

Inputs:
- text prompt
- file upload
- exported Jira/Asana/Linear/Planner data
- transcript
- sample project buttons

Sample buttons:
- auto-paste realistic sample project description
- optionally attach synthetic example artifacts

---

# Screen 2 — Project MRI Reveal

```text
┌─────────────────────────────────────────────┐
│ OSLO is building an understanding...        │
│                                             │
│ ✓ Goals detected                            │
│ ✓ Stakeholders identified                   │
│ ✓ Assumptions extracted                     │
│ ✓ Dependencies mapped                       │
│ ✓ Constraints detected                      │
│ ✓ Execution signals interpreted             │
│                                             │
│ Generating Outcome Confidence...            │
└─────────────────────────────────────────────┘
```

## Requirements

This screen should create trust and perceived intelligence.

Avoid:
- too much technical detail
- raw logs
- model trace language

---

# Screen 3 — Initial Findings

```text
┌─────────────────────────────────────────────┐
│ Initial Outcome Confidence                  │
│                                             │
│ 68  Initial                                 │
│                                             │
│ Clarity: 61                                 │
│ Alignment: 74                               │
│ Feasibility: 66                             │
│                                             │
│ OSLO found 3 important concerns:            │
│ 🔴 Ownership unclear                        │
│ 🟡 KPI definition incomplete                │
│ 🔴 Timeline feasibility weak                │
│                                             │
│ Fixing these may improve confidence +18     │
│                                             │
│ [Start Deep Refinement] [Enter Outcome Space]│
└─────────────────────────────────────────────┘
```

---

# Screen 4 — Deep Refinement

```text
┌─────────────────────────────────────────────┐
│ Deepening understanding...                  │
│                                             │
│ ✓ Comparing artifacts                       │
│ ✓ Evaluating evidence strength              │
│ ✓ Checking feasibility assumptions          │
│ ✓ Looking for interpretation conflicts      │
│                                             │
│ New finding: stakeholder ownership conflict │
│ New finding: staffing assumption weak       │
│                                             │
│ Confidence updated: 68 → 76                 │
└─────────────────────────────────────────────┘
```

## Requirement

Freemium must include both:
- Fast Pass
- Deep Refinement

Paid tiers unlock:
- frequency
- scale
- continuous monitoring
- integrations
- collaboration
- automation

---

# Screen 5 — Activation Summary

```text
┌─────────────────────────────────────────────┐
│ OSLO Understanding Created                  │
│                                             │
│ Confidence: 76 Expanded                     │
│ Integrity State: Clarified but Fragile      │
│                                             │
│ Most important issue:                       │
│ Launch ownership is unresolved.             │
│                                             │
│ Recommended next action:                    │
│ Clarify final approval ownership.           │
│                                             │
│ [Enter Outcome Space]                       │
└─────────────────────────────────────────────┘
```

---

# PLG Design Rules

1. Do not expose full artifact complexity during minute one.
2. Show insight before asking users to work.
3. Use confidence maturity labels to prevent false certainty.
4. Present problems as improvable potential.
5. Transition into workspace only after activation.
