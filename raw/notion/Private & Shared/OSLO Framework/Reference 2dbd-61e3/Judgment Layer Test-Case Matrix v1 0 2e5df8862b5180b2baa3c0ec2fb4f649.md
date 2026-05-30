# Judgment Layer Test-Case Matrix v1.0

**Format:** BDD/Gherkin-ready (Feature-file grouping + Scenario outlines)

**Scope:** Judgment Layer only (no Governance/Execution/Communication behavior)

---

## **Feature Group A — Input Contract & Validation**

### **A1 — Reject missing required context**

- **Given:** ReasoningOutput present
- **And:** lifecycle is missing OR mode/pass missing OR tier missing
- **When:** evaluateJudgment() runs
- **Then:** return **error** J_ERR_MISSING_CONTEXT
- **And:** emit audit log with status=FAILED_VALIDATION

### **A2 — Reject forbidden inputs**

- **Given:** Inputs include raw_user_text OR freeform_llm_output OR ui_state
- **When:** evaluation runs
- **Then:** return **error** J_ERR_FORBIDDEN_INPUT

### **A3 — Reject invalid enums**

- **Given:** decision enums referenced in configs include an unknown value
- **When:** evaluation runs
- **Then:** return **error** J_ERR_INVALID_ENUM

### **A4 — Accept canonical-only minimal input**

- **Given:** canonical ReasoningOutput + lifecycle + mode + tier
- **When:** evaluation runs
- **Then:** return a valid JudgmentDecision (any decision_type)
- **And:** audit log emitted

---

## **Feature Group B — Determinism & Replay**

### **B1 — Same input → same output (strict determinism)**

- **Given:** identical inputs (deep-equal)
- **When:** evaluation runs twice
- **Then:** decisions are byte-for-byte identical (including ordering)

### **B2 — Input hash reproducibility**

- **Given:** identical inputs
- **When:** evaluation runs
- **Then:** emitted input_hash is identical across runs

### **B3 — Deterministic conflict resolution**

- **Given:** two competing findings that could drive different decisions
- **When:** evaluation runs
- **Then:** the same tie-break path is chosen every run (rule-order anchored)

---

## **Feature Group C — Output Schema & Boundedness**

### **C1 — Output always matches schema**

- **Given:** valid inputs
- **When:** evaluation runs
- **Then:** output validates against JudgmentDecision schema

### **C2 — Only allowed decision types are emitted**

- **Given:** any valid inputs
- **When:** evaluation runs
- **Then:** decision_type ∈ {ACCEPT,WARN,BLOCK,DEFER,SUPPRESS}

### **C3 — Severity enum bounded**

- **Given:** any valid inputs
- **When:** evaluation runs
- **Then:** severity ∈ {INFO,LOW,MEDIUM,HIGH,CRITICAL}

### **C4 — Confidence in range**

- **Given:** any valid inputs
- **When:** evaluation runs
- **Then:** 0.0 ≤ confidence ≤ 1.0

---

## **Feature Group D — Evidence Anchoring**

### **D1 — Non-ACCEPT must reference evidence**

- **Given:** output is WARN or BLOCK or DEFER or SUPPRESS
- **When:** evaluation runs
- **Then:** evidence_refs is non-empty
- **And:** each evidence ref resolves to an existing Reasoning finding or trace id

### **D2 — ACCEPT may omit evidence (optional rule)**

- **Given:** no issues detected
- **When:** evaluation runs
- **Then:** output decision_type=ACCEPT
- **And:** evidence_refs is empty OR contains a “clean run” trace id (whichever your contract states)

### **D3 — Evidence referential integrity**

- **Given:** ReasoningOutput contains evidence ids A,B,C
- **When:** evaluation returns evidence_refs
- **Then:** every ref is in {A,B,C} (no new ids)

---

## **Feature Group E — No Fabrication & No Mutation**

### **E1 — Judgment does not create facts/assumptions**

- **Given:** inputs contain no “assumption X”
- **When:** evaluation runs
- **Then:** output contains no newly introduced assumptions, facts, or derived fields beyond the decision schema

### **E2 — Judgment does not mutate inputs**

- **Given:** inputs are provided (immutable baseline snapshot)
- **When:** evaluation runs
- **Then:** input object remains unchanged (deep-equal pre/post)

### **E3 — No re-running Reasoning**

- **Given:** a stubbed Reasoning engine exists
- **When:** evaluation runs
- **Then:** Reasoning engine is never invoked (0 calls)

---

## **Feature Group F — Lifecycle Sensitivity**

> Use a Scenario Outline with examples per lifecycle stage.
> 

### **F1 — Initiation bias favors DEFER over BLOCK (when incomplete)**

- **Given:** lifecycle=INITIATION
- **And:** Reasoning indicates missing required structural data
- **When:** evaluation runs
- **Then:** decision_type is DEFER (not BLOCK)
- **And:** evidence_refs include missing-data finding ids

### **F2 — Planning strictness blocks structural violations**

- **Given:** lifecycle=PLANNING
- **And:** Reasoning indicates missing mandatory artifacts
- **When:** evaluation runs
- **Then:** decision_type is BLOCK
- **And:** severity at least MEDIUM (per your severity mapping)

### **F3 — Execution strictness blocks feasibility/drift-critical findings**

- **Given:** lifecycle=EXECUTION
- **And:** Reasoning indicates feasibility failure or drift-critical signal
- **When:** evaluation runs
- **Then:** decision_type is BLOCK or WARN (per mapping)
- **And:** expiry_conditions set if the issue is time-sensitive

### **F4 — Monitoring prefers WARN for degradations**

- **Given:** lifecycle=MONITORING
- **And:** Reasoning indicates non-fatal degradation
- **When:** evaluation runs
- **Then:** decision_type is WARN (not BLOCK)

### **F5 — Closure suppresses non-impacting issues**

- **Given:** lifecycle=CLOSURE
- **And:** Reasoning indicates minor/late issues that don’t affect closure
- **When:** evaluation runs
- **Then:** decision_type is SUPPRESS
- **And:** suppression_reason = LIFECYCLE_MISMATCH (or your enum)

---

## **Feature Group G — Severity Independence**

### **G1 — BLOCK with LOW is permitted**

- **Given:** mapping rules produce decision_type=BLOCK
- **And:** severity mapping produces LOW
- **When:** evaluation runs
- **Then:** output is valid (do not auto-escalate severity)

### **G2 — WARN with CRITICAL is permitted**

- **Given:** decision_type=WARN
- **And:** severity=CRITICAL
- **When:** evaluation runs
- **Then:** output is valid (do not auto-convert to BLOCK)

### **G3 — Severity derived, not invented**

- **Given:** Reasoning provides severity tags per finding
- **When:** evaluation runs
- **Then:** decision severity is computed only from declared mapping rules (no ad-hoc LLM logic)

---

## **Feature Group H — Suppression Semantics & Auditability**

### **H1 — SUPPRESS requires explicit reason**

- **Given:** decision_type=SUPPRESS
- **When:** evaluation runs
- **Then:** suppression_reason is present and valid enum

### **H2 — Suppressed decisions still emit audit logs**

- **Given:** decision_type=SUPPRESS
- **When:** evaluation runs
- **Then:** audit event includes decision + evidence_refs + suppression_reason

### **H3 — Suppression remains replayable**

- **Given:** same inputs at same lifecycle+mode
- **When:** evaluation runs later
- **Then:** SUPPRESS repeats deterministically (unless inputs changed)

---

## **Feature Group I — Expiry & Re-evaluation**

### **I1 — Time-based expiry condition supported**

- **Given:** a time-sensitive finding (e.g., capacity window)
- **When:** evaluation runs
- **Then:** expiry_conditions includes TIME_WINDOW with deadline timestamp

### **I2 — Condition-based expiry supported**

- **Given:** a finding tied to “until assumption validated”
- **When:** evaluation runs
- **Then:** expiry_conditions includes ON_EVIDENCE_CHANGE referencing evidence ids

---

## **Feature Group J — Observability Contract**

### **J1 — Successful evaluation emits required audit fields**

- **Given:** valid inputs
- **When:** evaluation runs successfully
- **Then:** audit log includes:
    - input_hash
    - timestamp
    - lifecycle
    - mode/pass
    - tier
    - decision_type
    - severity
    - confidence
    - evidence_refs

### **J2 — Failed validation emits failure audit**

- **Given:** missing required context
- **When:** evaluation runs
- **Then:** audit log includes status=FAILED_VALIDATION + error code

---

## **Suggested Feature File Layout (directly usable)**

- A_input_contract.feature
- B_determinism.feature
- C_output_schema.feature
- D_evidence_anchoring.feature
- E_no_fabrication_no_mutation.feature
- F_lifecycle_sensitivity.feature
- G_severity_independence.feature
- H_suppression.feature
- I_expiry.feature
- J_observability.feature

---

If you want the next step to be maximally practical, I can generate the **actual starter Gherkin suite** (Feature files + Scenario Outlines + Examples tables) from this matrix in one shot, using your exact lifecycle enum names and your tier names.