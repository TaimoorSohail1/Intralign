# Judgment Definition File Specification v1.0

**System:** OSLO / Intralign

**Layer:** Judgment

**Spec Type:** Normative (evaluation schema + contracts)

**Status:** Canonical

**Audience:** Engineering, AI/ML, Data, QA

---

## **1. Purpose**

This specification defines the **externalized definition files** used by the **Judgment Layer**.

Judgment exists to:

- evaluate Reasoning outputs
- produce scores, bands, and confidence
- make evaluation deterministic, explainable, and replayable

Judgment **does not**:

- detect structure
- authorize actions
- decide visibility
- generate language
- mutate canonical data

---

## **2. Authority & Scope**

Judgment is the **evaluation authority**, not the execution authority.

Judgment:

- consumes Reasoning outputs
- applies versioned evaluation models
- emits evaluative artifacts

Judgment **never**:

- suppresses or prioritizes issues
- blocks user actions
- initiates execution
- communicates meaning

---

## **3. File Taxonomy (Canonical)**

```
/judgment/
  /models/          # score models and rollups
  /mappings/        # reasoning outputs → score impact
  /confidence/      # confidence calibration rules
  /bands/           # interpretation bands
  /profiles/        # bundled evaluation configurations
```

---

## **4. Global File Requirements**

### **4.1 Required Header Metadata (All Files)**

```
meta:
  schema: oslo.judgment.<category>.v1
  id: <string>                   # stable identifier
  version: <semver>              # immutable once published
  status: DRAFT | CANONICAL | DEPRECATED
  created_at: <ISO-8601>
  owner: <team-or-role>
  description: <string>
  compatibility:
    min_engine_version: <semver>
    max_engine_version: <semver|null>
```

### **4.2 Immutability Rules**

- CANONICAL versions are immutable
- Changes require a new version
- Old versions remain replayable

---

## **5. Score Model Files (**

## **/models/*.yaml**

## **)**

### **5.1 Purpose**

Define **what scores exist** and **how they aggregate**.

### **5.2 Score Model Schema**

```
meta: { ... }

score_model:
  id: judgment.model.core
  description: Core evaluation model
  scale:
    type: numeric
    min: 0
    max: 100

  dimensions:
    - id: Clarity
      aggregation: weighted
      weight: 0.33

    - id: Alignment
      aggregation: weighted
      weight: 0.33

    - id: Feasibility
      aggregation: weighted
      weight: 0.34

  rollups:
    - id: OutcomeHealth
      from: [Clarity, Alignment, Feasibility]
      method: weighted_average
```

### **5.3 Rules**

- Scores must be deterministic
- No thresholds for action
- Rollups are arithmetic only

---

## **6. Mapping Files (**

## **/mappings/*.yaml**

## **)**

### **6.1 Purpose**

Define how **Reasoning outputs affect scores**.

### **6.2 Issue → Score Mapping**

```
meta: { ... }

issue_to_score:
  - issue_type: Clarity
    subtype: MissingRequiredField
    impact:
      dimension: Clarity
      penalty: 10
      scope: local
```

### **6.3 Signal → Score Mapping**

```
signal_to_score:
  - signal_id: SIGNAL.SCHEDULE_COMPRESSION
    impact:
      dimension: Feasibility
      curve: linear
      slope: -1.5
```

### **6.4 Rules**

- Mapping is declarative
- No conditionals beyond explicit fields
- No governance semantics

---

## **7. Confidence Calibration Files (**

## **/confidence/*.yaml**

## **)**

### **7.1 Purpose**

Define **how confident Judgment is in its evaluation**.

### **7.2 Confidence Schema**

```
meta: { ... }

confidence_calibration:
  default: High

  rules:
    - condition:
        placeholder_count: ">0"
      downgrade_to: Medium

    - condition:
        evidence_limitations_present: true
      downgrade_to: Low
```

### **7.3 Rules**

- Confidence is evaluative, not permissive
- Confidence must reference evidence

---

## **8. Interpretation Band Files (**

## **/bands/*.yaml**

## **)**

### **8.1 Purpose**

Provide **non-authoritative interpretation labels**.

### **8.2 Band Schema**

```
meta: { ... }

bands:
  dimension: Clarity
  labels:
    - name: Healthy
      range: [80, 100]

    - name: Watch
      range: [60, 79]

    - name: Risk
      range: [0, 59]
```

### **8.3 Rules**

- Bands do not trigger actions
- Bands do not suppress outputs
- Governance decides what bands matter

---

## **9. Profiles (**

## **/profiles/*.yaml**

## **)**

### **9.1 Purpose**

Bind evaluation behavior to **Reasoning context**.

### **9.2 Profile Schema**

```
meta: { ... }

profile:
  id: judgment.profile.sixty_second
  description: Conservative evaluation for 60SECOND reasoning
  accepts:
    reasoning_modes: [60SECOND]
  uses:
    score_model_id: judgment.model.core
    score_model_version: 1.0.0
    issue_mapping_id: judgment.map.issue_to_score
    issue_mapping_version: 1.0.0
    confidence_id: judgment.conf.calibration
    confidence_version: 1.0.0
  policy:
    conservative_confidence: true
```

### **9.3 Rules**

- Profiles must pin versions
- Profiles must not contain logic
- Profiles must not alter authority

---

## **10. Evidence & Replay Requirements**

Judgment outputs must record:

- input Reasoning run ID
- reasoning mode
- profile ID
- all file versions used
- confidence adjustments applied

Judgment must be replayable using:

- Reasoning outputs
- pinned Judgment files
- no external state

---

## **11. Explicit Non-Responsibilities**

Judgment files must **never** include:

- structural detection logic
- authorization thresholds
- UI display rules
- communication text
- execution semantics

---

## **Canonical Invariant**

> Judgment evaluates truth.
> 

> It does not decide what happens next.
> 

---

## **End of Specification**

---

### **Logical next artifacts (optional)**

- Sample **Judgment score model + mappings**
- **Judgment Test Case Matrix**
- **Judgment ↔ Governance boundary spec**

If you want, say which one to publish next.