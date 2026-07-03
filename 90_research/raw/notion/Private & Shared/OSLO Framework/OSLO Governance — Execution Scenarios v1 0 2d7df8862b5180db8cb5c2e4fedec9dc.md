# OSLO Governance — Execution Scenarios v1.0

---

**Scope:** OSLO Communication Engine (Governance Layer)

**Applies To:** Onboarding, plan generation, plan updates, chat interactions

**Constrained By:** Scenario Guardrails v1.0 (G-01 → G-08)

---

## **Scenario E-01 — Input Capture (No Evaluation Allowed)**

**Initial State:** InputCapture

**Trigger:** User provides onboarding inputs

### **Given**

- Plan does not yet exist
- Inputs are partial or in progress

### **When**

- User enters or updates onboarding fields

### **Then**

- OSLO may:
    - Acknowledge inputs
    - Provide educational context
- OSLO must not:
    - Generate issues
    - Compute or display scores
    - Surface critiques or assumptions

**Guardrails:** G-01

**Expected Surfaces:** Chat (educational only), Input UI

---

## **Scenario E-02 — Plan Generation with Educational Narration**

**Initial State:** PlanGenerating

**Trigger:** User completes onboarding input

### **Given**

- All required inputs are present
- Plan generation is in progress

### **When**

- OSLO constructs human-readable and machine-readable plans

### **Then**

- OSLO may:
    - Explain what it is doing
    - Set expectations for scores, issues, validation
- OSLO may internally:
    - Run reasoning and judgment computations
- OSLO must not:
    - Disclose results of reasoning
    - Show scores, warnings, or issues

**Guardrails:** G-01, G-02

**Expected Surfaces:** Chat (process narration only)

---

## **Scenario E-03 — Plan Presentation (First Evaluation Disclosure)**

**Initial State:** PlanPresented

**Trigger:** Plan generation completes

### **Given**

- Plan artifacts now exist

### **When**

- OSLO transitions into presentation mode

### **Then**

- OSLO must:
    - Render the full plan
    - Populate the Issues / Context Panel
    - Display Clarity, Alignment, Feasibility scores
- OSLO may:
    - Send a single chat message summarizing availability
- OSLO must not:
    - Enumerate issues in chat
    - Immediately prompt validation

**Guardrails:** G-01, G-04

**Expected Surfaces:** Plan UI, Panel, Chat (summary only)

---

## **Scenario E-04 — Selective Validation Nudge (Post-View)**

**Initial State:** SteadyState

**Trigger:** High-impact inferred element exists

### **Given**

- User has viewed the plan or idle window elapsed
- An inferred element materially affects outcomes

### **When**

- Governance evaluates validation eligibility

### **Then**

- OSLO may:
    - Raise **one** validation nudge
    - Clearly label it as assumed / needs confirmation
- OSLO must not:
    - Raise multiple validations simultaneously
    - Use alarmist language

**Guardrails:** G-04

**Expected Surfaces:** Chat or Panel (single nudge)

---

## **Scenario E-05 — Silent UI-Driven Plan Update**

**Initial State:** SteadyState

**Trigger:** User edits artifact or resolves issue via UI

### **Given**

- User explicitly modifies plan artifacts

### **When**

- UI confirms the change

### **Then**

- OSLO must:
    - Update canonical plan
    - Recompute reasoning and judgment
    - Update issues and scores
- OSLO must not:
    - Send a chat message unless a new critical blocker exists

**Guardrails:** G-03, G-07

**Expected Surfaces:** Plan UI, Panel

---

## **Scenario E-06 — Chat-Suggested Fix with CTA (Authorized Mutation)**

**Initial State:** SteadyState

**Trigger:** User engages with chat explanation

### **Given**

- An issue exists
- OSLO suggests a fix via chat with CTA

### **When**

- User clicks CTA (“Apply Fix”)

### **Then**

- System treats action as UI-authorized mutation
- OSLO must:
    - Update affected artifacts
    - Recompute reasoning and judgment
    - Revise or remove issue
    - Update scores
- OSLO must not:
    - Narrate routine updates in chat

**Guardrails:** G-03

**Expected Surfaces:** Chat (pre-CTA), Plan UI / Panel (post-CTA)

---

## **Scenario E-07 — UI Update Introduces Critical Blocker**

**Initial State:** SteadyState

**Trigger:** User-initiated UI edit

### **Given**

- Edit introduces a high-severity feasibility issue

### **When**

- Recompute completes

### **Then**

- OSLO must:
    - Proactively notify via chat
    - Clearly explain causal link (“After updating X…”)
- OSLO must:
    - Also surface issue in panel

**Guardrails:** G-06, G-08

**Expected Surfaces:** Chat, Panel

---

## **Scenario E-08 — User Asks “Why?” in Chat**

**Initial State:** SteadyState

**Trigger:** User asks an explanatory question

### **Given**

- Issue or score exists

### **When**

- User asks “Why is this flagged?” or equivalent

### **Then**

- OSLO may:
    - Explain reasoning and evidence
- OSLO must not:
    - Introduce new issues
    - Change posture or severity

**Guardrails:** G-06

**Expected Surfaces:** Chat (with links to panel)

---

## **Scenario E-09 — Hypothetical / What-If Analysis**

**Initial State:** SteadyState

**Trigger:** User asks hypothetical question

### **Given**

- Question is exploratory, not directive

### **When**

- OSLO analyzes scenario

### **Then**

- OSLO must:
    - Use isolated evaluation context
    - Clearly label results as hypothetical
- OSLO must not:
    - Mutate plan
    - Update issues or scores

**Guardrails:** G-05

**Expected Surfaces:** Chat only

---

## **Scenario E-10 — No Communication Is the Correct Outcome**

**Initial State:** Any

**Trigger:** Recompute or background change

### **Given**

- No critical change occurred

### **When**

- Governance evaluates communication necessity

### **Then**

- OSLO intentionally does nothing
- Suppression is logged

**Guardrails:** G-07

**Expected Surfaces:** None

---

## **Canonical Close**

> These execution scenarios define
> 
> 
> **exactly how OSLO behaves at runtime**
> 

They are now stable enough to be used for:

- Acceptance testing
- PR review criteria
- AI-assisted implementation
- QA regression coverage

---

###