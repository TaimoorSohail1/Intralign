# Conflict Escalation State Machine (v1.0)

---

## **Core idea**

A **conflict** is any condition where **two layers produce incompatible outputs** under the current **tier + posture + action class + constraints**.

Resolution is **system-only**. Layers can **detect + report**.

---

## **State definitions**

### **S0 — No Conflict**

**Entry:** Normal operation

**Exit condition:** A layer emits CONFLICT_SIGNAL

**Output:** none

---

### **S1 — Conflict Detected**

**Entry:** Any layer emits a conflict signal with:

- conflict_type
- layers_involved
- blocking_layer (if known)
- proposed_action (what the layer wanted)
- why_blocked (what it collided with)

**Transition:** to S2 always

---

### **S2 — Normalize and Classify**

System canonicalizes the event:

- dedupe (same conflict repeated)
- assign severity
- assign governance_impact
- assign epistemic_impact
- map to action_class (e.g., infer/fill, recommend, auto-edit, export, etc.)

**Transition rules:**

- If **Governance veto** applies → S3
- Else → S4

---

### **S3 — Governance Veto**

Governance asserts a hard stop:

- prohibited action
- non-negotiable disclosure requirements
- allowed alternatives (if any)

**Transition rules:**

- If an allowed alternative exists → S5
- Else → S8

---

### **S4 — Tradeoff Required**

No hard veto, but incompatible outputs remain.

System requests **Judgment arbitration** within bounds:

- select posture-compliant option (speed vs certainty vs accountability)
- apply tier restrictions
- determine whether user confirmation is required

**Transition rules:**

- If Judgment selects an option that does **not** require user input → S6
- If user input required → S7
- If Judgment cannot choose (insufficient info) → S7

---

### **S5 — Alternative Path Synthesis**

System constructs one or more compliant paths:

- “Do X instead of Y”
- “Proceed but downgrade confidence”
- “Proceed with explicit assumptions”
- “Delay output until confirmation”

Each path includes:

- capability_cost (what user loses: completeness, automation, etc.)
- risk_profile
- required_disclosures

**Transition rules:**

- If only one viable path → S6
- If multiple viable paths → S7

---

### **S6 — Controlled Continue**

System proceeds with selected path, enforcing:

- disclosures (epistemic labels, governance notes)
- output constraints (what must be omitted)
- audit logging (full conflict payload)

**Exit:** returns to S0 after emitting an OUTCOME_WITH_CONFLICT_METADATA

---

### **S7 — User Escalation**

System must ask the user to resolve a decision, choosing the **minimum question** that unblocks progress.

**UX rule:** present options, not open-ended confusion.

- option A: comply + degrade
- option B: provide missing info
- option C: change posture/tier (if allowed)
- option D: stop

**Transition rules:**

- If user provides info → S2 (reclassify with new facts)
- If user selects a path → S6
- If user refuses / times out → S8

---

### **S8 — Safe Halt**

System stops the attempted action and returns:

- what was blocked
- why (in plain language)
- what would unblock it
- what can be done now

**Exit:** returns to S0 only when user changes inputs or posture/tier.

---

## **Transition map (compact)**

- **S0 → S1:** conflict signal
- **S1 → S2:** always
- **S2 → S3:** governance veto true
- **S2 → S4:** no veto
- **S3 → S5:** alternative exists
- **S3 → S8:** no alternative
- **S4 → S6:** judgment chooses + no user input
- **S4 → S7:** needs user input / cannot decide
- **S5 → S6:** single viable alternative
- **S5 → S7:** multiple viable alternatives
- **S7 → S2:** user adds info
- **S7 → S6:** user selects option
- **S7 → S8:** user refuses / timeout
- **S6 → S0:** after controlled output
- **S8 → S0:** after user change triggers new attempt

---

## **Required event payloads (implementation hint)**

### **Conflict signal (emitted by a layer)**

- conflict_id (stable hash)
- source_layer
- target_layer
- conflict_type
- proposed_action
- blocked_by (constraint / invariant / policy)
- evidence_refs (if any)
- epistemic_status (fact/inferred/unknown)
- confidence (if applicable)

### **Resolution record (emitted by system)**

- conflict_id
- resolution_state_path (e.g., S0→S1→S2→S3→S5→S6)
- selected_option
- disclosures_applied
- output_degradation (if any)
- user_input (if any)
- audit_refs

---

## **Two concrete examples (so it’s not abstract)**

### **Example 1: “Generate complete plan in 60 seconds” vs missing facts**

- S1: Reasoning wants to infer milestones
- S2: epistemic impact high
- S4: Judgment decides “okay, but label as assumptions”
- S6: output with assumption tags + confidence + “confirm in Pass 2”

### **Example 2: “Auto-update Jira tasks” on Free tier**

- S1: Execution proposes action
- S2: tier restriction triggers governance impact
- S3: Governance veto
- S5: Alternative = “export PDF only” + “upgrade for sync”
- S7: user chooses export vs upgrade
- S6: proceed

---

If you want next: I can convert this into a **diagram spec** (Mermaid or PlantUML) and/or a **BDD/Gherkin test matrix** that covers every transition path.