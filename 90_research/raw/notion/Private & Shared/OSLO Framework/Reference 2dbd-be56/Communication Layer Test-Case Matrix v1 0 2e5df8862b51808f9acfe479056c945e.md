# Communication Layer Test-Case Matrix v1.0

**BDD / Gherkin-ready (feature-grouped), strict constraint enforcement, CI-friendly**

**Scope:** Communication consumes CommunicationContextEnvelope + GovernanceOutcome and renders **only** permitted output per constraints.

**Out of scope:** deciding permissions (Governance), deciding correctness (Reasoning/Judgment), executing actions (Execution).

---

## **Feature A — Input Contract & Validation**

### **A1 Missing required context fails closed**

- **Given** a communication render request
- **And** one of channel | audience | locale | presentation_intent | ui_density is missing
- **When** render() runs
- **Then** render a **safe fallback denial** (no data disclosure)
- **And** emit audit event status=FAILED_VALIDATION

### **A2 Missing governance_outcome fails closed**

- **Given** context is present
- **And** governance_outcome is missing
- **When** render runs
- **Then** safe fallback denial
- **And** audit status=FAILED_VALIDATION

### **A3 Unknown fields rejected (strict parsing)**

- **Given** request includes unknown field(s)
- **When** render runs
- **Then** safe fallback denial (or explicit error in API mode per contract)
- **And** audit includes COMM_ERR_SCHEMA_VIOLATION

### **A4 Invalid enums fail closed**

- **Given** governance_outcome.outcome_type is invalid
- **When** render runs
- **Then** safe fallback denial
- **And** audit includes COMM_ERR_INVALID_ENUM

---

## **Feature B — Determinism & Replay**

### **B1 Same inputs yield identical rendered output (byte-level in API mode)**

- **Given** identical context + governance_outcome
- **When** render runs twice
- **Then** output payload is identical

### **B2 Deterministic template selection**

- **Given** reason_codes = [A,B] in fixed order
- **When** render runs
- **Then** same template/copy mapping chosen every run

### **B3 Order independence where specified**

- **Given** reason_codes contains same set in different order
- **When** render runs
- **Then** output identical **if** contract says reason_code selection is set-based; otherwise verify order-based behavior (pick one and test)

---

## **Feature C — Outcome Handling (PERMIT / DENY / REQUIRE_APPROVAL / DOWNGRADE / REDACT / RATE_LIMIT / LOG_ONLY)**

### **C1 PERMIT renders within ALLOWED_SCOPE**

- **Given** outcome_type=PERMIT
- **And** constraints include ALLOWED_SCOPE=SUMMARY
- **When** render runs
- **Then** show summary only
- **And** no details/evidence sections appear

### **C2 DENY renders denial state only**

- **Given** outcome_type=DENY
- **When** render runs
- **Then** show denial message using reason_code mapping
- **And** show no restricted content (summary/details/evidence)

### **C3 REQUIRE_APPROVAL renders approval request UI state**

- **Given** outcome_type=REQUIRE_APPROVAL
- **And** constraints include APPROVER_ROLES and APPROVAL_TTL
- **When** render runs
- **Then** render approval-needed state
- **And** do not imply execution occurred

### **C4 DOWNGRADE renders downgraded options only**

- **Given** outcome_type=DOWNGRADE
- **And** constraints include ALLOWED_FORMAT=PDF
- **When** render runs
- **Then** offer PDF only
- **And** hide/disable DOCX/CSV/JSON options

### **C5 REDACT hides specified content and indicates redaction if allowed**

- **Given** outcome_type=REDACT
- **And** constraints include REDACT_FIELDS=[x,y]
- **When** render runs
- **Then** fields x and y are removed/obfuscated
- **And** output contains no raw values for x or y

### **C6 RATE_LIMIT shows cooldown message**

- **Given** outcome_type=RATE_LIMIT
- **And** constraints include COOLDOWN_SECONDS=60
- **When** render runs
- **Then** show rate-limit message
- **And** show cooldown duration (if policy allows)

### **C7 LOG_ONLY renders nothing user-visible**

- **Given** outcome_type=LOG_ONLY
- **When** render runs
- **Then** no user-visible output is produced
- **And** audit event is emitted

---

## **Feature D — Constraint Enforcement (Fail-Closed)**

### **D1 Missing required constraint for an outcome fails closed**

- **Given** outcome_type=DOWNGRADE
- **And** ALLOWED_FORMAT constraint is missing
- **When** render runs
- **Then** safe fallback denial (or safe minimal output per policy)
- **And** audit includes COMM_ERR_MISSING_CONSTRAINT

### **D2 Ambiguous constraint value fails closed**

- **Given** constraint ALLOWED_SCOPE has an unknown value
- **When** render runs
- **Then** safe fallback denial

### **D3 Channel mismatch fails closed**

- **Given** context.channel=PDF
- **And** constraints disallow export formats
- **When** render runs
- **Then** safe fallback denial or downgrade to allowed format (policy-defined)

---

## **Feature E — Evidence Visibility**

### **E1 Evidence hidden when EVIDENCE_VISIBILITY=HIDDEN**

- **Given** constraints include EVIDENCE_VISIBILITY=HIDDEN
- **When** render runs
- **Then** do not display evidence content
- **And** do not display evidence paths/ids (unless explicitly allowed)
- **And** optionally show “Evidence hidden” indicator (if allowed)

### **E2 Evidence visible when entitled**

- **Given** outcome_type=PERMIT
- **And** constraints include EVIDENCE_VISIBILITY=VISIBLE
- **When** render runs
- **Then** evidence section is rendered

---

## **Feature F — Scope Enforcement (Summary vs Details vs Full)**

### **F1 Summary-only scope excludes details blocks**

- **Given** ALLOWED_SCOPE=SUMMARY
- **When** render runs
- **Then** details blocks are absent

### **F2 Details scope excludes evidence if not allowed**

- **Given** ALLOWED_SCOPE=DETAILS
- **And** evidence visibility is hidden
- **When** render runs
- **Then** details present, evidence absent

### **F3 Full scope requires explicit allowance**

- **Given** ALLOWED_SCOPE=FULL is not present
- **When** render runs
- **Then** do not render full content even if other constraints absent

---

## **Feature G — Export Format & Watermarking**

### **G1 Enforce ALLOWED_FORMAT in export**

- **Given** channel=PDF
- **And** ALLOWED_FORMAT=PDF
- **When** render runs
- **Then** output is produced in PDF mode (or PDF-ready payload)

### **G2 Watermark required is enforced**

- **Given** WATERMARK_REQUIRED=true
- **When** render runs
- **Then** watermark flag is set / watermark applied (implementation-specific)
- **And** audit notes watermark applied

### **G3 Attempted non-allowed export format blocked/downgraded**

- **Given** requested_export_format=CSV
- **And** ALLOWED_FORMAT=PDF
- **When** render runs
- **Then** CSV is not produced
- **And** downgrade messaging shown (or denial, per policy)

---

## **Feature H — Redaction Semantics (No Leaks)**

### **H1 Redacted fields do not appear anywhere**

- **Given** REDACT_FIELDS=[email,phone]
- **When** render runs
- **Then** no email/phone values appear in:
    - visible text
    - metadata fields
    - tooltips
    - logs (other than counts)
- **And** audit records only counts, not raw values

### **H2 Redaction is applied before templating**

- **Given** templates reference a redacted field
- **When** render runs
- **Then** template renders safely (placeholder/omission), not the raw value

---

## **Feature I — Reason Code Mapping (Copy Selection)**

### **I1 Copy is selected only from reason_code dictionary**

- **Given** reason_codes=[TIER_CAPABILITY_MISSING]
- **When** render runs
- **Then** message equals mapped copy for that reason_code
- **And** no policy text is shown

### **I2 Unknown reason code uses safe generic copy**

- **Given** reason_codes contains unknown code X
- **When** render runs
- **Then** generic safe message displayed
- **And** no internal code X shown to end user

### **I3 Multiple reason codes deterministic prioritization**

- **Given** reason_codes=[A,B,C]
- **When** render runs
- **Then** chosen primary message is from the highest-priority reason code (priority table locked)

---

## **Feature J — No Action Implication (Non-Execution)**

### **J1 Approval required does not imply action executed**

- **Given** outcome_type=REQUIRE_APPROVAL
- **When** render runs
- **Then** UI does not say “applied” or “synced”
- **And** labels state “pending approval” (or equivalent)

### **J2 Downgrade does not execute alternatives**

- **Given** outcome_type=DOWNGRADE
- **When** render runs
- **Then** only presents downgraded options; does not auto-export

---

## **Feature K — Audit Emission**

### **K1 Audit event emitted for every render**

- **Given** any valid governance_outcome
- **When** render runs
- **Then** audit event includes:
    - request_id
    - channel + presentation_intent
    - outcome_type
    - constraints applied
    - redaction counts
    - timestamp

### **K2 Audit does not leak redacted content**

- **Given** redaction constraints
- **When** render runs
- **Then** audit contains counts/flags only, not raw redacted values

---

## **Suggested Feature File Layout**

- A_input_validation.feature
- B_determinism.feature
- C_outcome_handling.feature
- D_constraint_enforcement.feature
- E_evidence_visibility.feature
- F_scope_enforcement.feature
- G_export_watermark.feature
- H_redaction_no_leaks.feature
- I_reason_code_copy.feature
- J_no_action_implication.feature
- K_audit.feature

If you want, I can now generate the **starter .feature files** with Scenario Outlines + Examples tables by assuming your exact constraint values (ALLOWED_SCOPE, EVIDENCE_VISIBILITY, formats, etc.) and your reason_code priority order.