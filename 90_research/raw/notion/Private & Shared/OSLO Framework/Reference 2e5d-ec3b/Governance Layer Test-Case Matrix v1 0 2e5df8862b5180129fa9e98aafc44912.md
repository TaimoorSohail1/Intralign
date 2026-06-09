# Governance Layer Test-Case Matrix v1.0

**Format:** BDD / Gherkin-ready (Feature grouping + scenario outlines)

**Scope:** Governance only (permission + policy enforcement).

**Excludes:** Reasoning correctness, Judgment correctness, Communication wording, Execution side-effects.

---

## **Feature Group A — Input Contract & Validation**

### **A1 — Missing required context fails validation**

- **Given** a Governance evaluation request
- **And** lifecycle_stage is missing **or** tier missing **or** role missing **or** policy_version missing
- **When** evaluateGovernance() runs
- **Then** return **error** GOV_ERR_MISSING_CONTEXT
- **And** emit audit event with status=FAILED_VALIDATION

### **A2 — Reject forbidden inputs**

- **Given** inputs include raw_user_text **or** freeform_llm_output **or** ui_only_flags
- **When** evaluation runs
- **Then** return **error** GOV_ERR_FORBIDDEN_INPUT

### **A3 — Reject invalid enums**

- **Given** action_class or posture or tier is not a supported enum
- **When** evaluation runs
- **Then** return **error** GOV_ERR_INVALID_ENUM

### **A4 — Reject unknown fields (strict parsing)**

- **Given** request includes unknown field x_unknown
- **When** evaluation runs
- **Then** return **error** GOV_ERR_SCHEMA_VIOLATION

---

## **Feature Group B — Determinism & Replay**

### **B1 — Same input → same output**

- **Given** identical evaluation request payloads (deep-equal)
- **When** evaluation runs twice
- **Then** GovernanceOutcome is byte-for-byte identical

### **B2 — Policy version pins behavior**

- **Given** identical payload except policy_version differs
- **When** evaluation runs
- **Then** outcome may differ only if policy changes for that version
- **And** audit record includes the policy_version used

### **B3 — Tie-break determinism**

- **Given** two policies could apply (e.g., posture rule + enterprise rule)
- **When** evaluation runs
- **Then** the same precedence rule is applied deterministically every run

---

## **Feature Group C — Output Contract & Boundedness**

### **C1 — Output validates against schema**

- **Given** valid request
- **When** evaluation runs
- **Then** output validates against GovernanceOutcome schema

### **C2 — Only allowed outcomes emitted**

- **Given** any valid request
- **When** evaluation runs
- **Then** outcome_type ∈ {PERMIT,DENY,REQUIRE_APPROVAL,DOWNGRADE,REDACT,RATE_LIMIT,LOG_ONLY}

### **C3 — reason_code presence required for non-PERMIT**

- **Given** outcome_type != PERMIT
- **When** evaluation runs
- **Then** reason_code[] is non-empty
- **And** each reason_code is a stable enum/code (not prose)

### **C4 — constraints field bounded and typed**

- **Given** any outcome
- **When** evaluation runs
- **Then** constraints[] contains only allowed constraint types (no free-form text blobs)

---

## **Feature Group D — RBAC & Tenant Isolation**

### **D1 — Deny cross-tenant access**

- **Given** actor tenant != resource tenant
- **When** evaluation runs
- **Then** outcome_type = DENY
- **And** reason_code includes TENANT_ISOLATION

### **D2 — Deny insufficient role**

- **Given** actor role lacks required permission for intent
- **When** evaluation runs
- **Then** outcome_type = DENY
- **And** reason_code includes INSUFFICIENT_ROLE

### **D3 — Permit within-tenant authorized access**

- **Given** actor tenant == resource tenant
- **And** role has permission
- **When** evaluation runs
- **Then** outcome_type = PERMIT

---

## **Feature Group E — Tier Gating**

### **E1 — Deny restricted integration without entitlement**

- **Given** intent = EXTERNAL_SYNC
- **And** tier capabilities exclude integrations
- **When** evaluation runs
- **Then** outcome_type = DENY
- **And** reason_code includes TIER_CAPABILITY_MISSING

### **E2 — Downgrade export format when restricted**

- **Given** intent = EXPORT
- **And** tier allows only PDF
- **When** evaluation runs
- **Then** outcome_type = DOWNGRADE
- **And** constraints include ALLOWED_FORMAT=PDF

### **E3 — Permit integration when entitled**

- **Given** intent = EXTERNAL_SYNC
- **And** tier capabilities include integration X
- **When** evaluation runs
- **Then** outcome_type = PERMIT

---

## **Feature Group F — Posture Enforcement**

> Assumes posture contract exists and is provided explicitly.
> 

### **F1 — Deny auto-apply in conservative posture**

- **Given** posture = SUGGEST_ONLY
- **And** intent = MUTATE_CANON (auto-apply)
- **When** evaluation runs
- **Then** outcome_type = DENY
- **And** reason_code includes POSTURE_DISALLOWS_AUTO_APPLY

### **F2 — Require approval in guarded posture**

- **Given** posture = REQUIRE_APPROVAL
- **And** intent = MUTATE_CANON
- **When** evaluation runs
- **Then** outcome_type = REQUIRE_APPROVAL
- **And** constraints include approver roles + TTL

### **F3 — Permit auto-apply in autonomous posture (if enabled)**

- **Given** posture = AUTO_APPLY
- **And** intent = MUTATE_CANON
- **And** policy allows AUTO_APPLY for this action_class
- **When** evaluation runs
- **Then** outcome_type = PERMIT

---

## **Feature Group G — High-Risk Action Classes**

### **G1 — Require approval for delete**

- **Given** action_class = DELETE
- **When** evaluation runs
- **Then** outcome_type = REQUIRE_APPROVAL
- **And** reason_code includes HIGH_RISK_ACTION

### **G2 — Require approval for external write**

- **Given** action_class = EXTERNAL_WRITE
- **When** evaluation runs
- **Then** outcome_type = REQUIRE_APPROVAL

### **G3 — Downgrade scope reduction to proposal**

- **Given** action_class = SCOPE_REDUCTION
- **And** policy requires proposal-only handling
- **When** evaluation runs
- **Then** outcome_type = DOWNGRADE
- **And** constraints include WRITE_MODE=PROPOSED_ONLY

---

## **Feature Group H — Visibility, Redaction, and Evidence Access**

### **H1 — Redact evidence details for lower tiers**

- **Given** intent = VIEW_EVIDENCE
- **And** tier does not include evidence visibility
- **When** evaluation runs
- **Then** outcome_type = REDACT
- **And** constraints include EVIDENCE_CONTENT=HIDDEN
- **And** audit_refs preserved

### **H2 — Permit evidence viewing for entitled tiers**

- **Given** intent = VIEW_EVIDENCE
- **And** tier includes evidence visibility
- **When** evaluation runs
- **Then** outcome_type = PERMIT

### **H3 — Redact sensitive fields in exports**

- **Given** intent = EXPORT
- **And** content classification contains SENSITIVE_FIELDS
- **When** evaluation runs
- **Then** outcome_type = REDACT or DOWNGRADE (per policy)
- **And** constraints include REDACT_FIELDS=[...]

---

## **Feature Group I — Lifecycle Gating**

### **I1 — Deny lifecycle transition when Judgment is BLOCK**

- **Given** intent = LIFECYCLE_TRANSITION
- **And** JudgmentDecision.decision_type = BLOCK
- **When** evaluation runs
- **Then** outcome_type = DENY
- **And** reason_code includes BLOCKED_BY_JUDGMENT

### **I2 — Require approval for lifecycle transitions in enterprise**

- **Given** intent = LIFECYCLE_TRANSITION
- **And** workspace policy = ENTERPRISE_GATED
- **When** evaluation runs
- **Then** outcome_type = REQUIRE_APPROVAL

### **I3 — Permit lifecycle transition when conditions met**

- **Given** intent = LIFECYCLE_TRANSITION
- **And** JudgmentDecision.decision_type != BLOCK
- **And** policy gate satisfied
- **When** evaluation runs
- **Then** outcome_type = PERMIT

---

## **Feature Group J — Rate Limiting & Abuse Controls**

### **J1 — Rate limit repeated heavy requests**

- **Given** intent = HEAVY_EVAL
- **And** request rate exceeds policy threshold
- **When** evaluation runs
- **Then** outcome_type = RATE_LIMIT
- **And** constraints include cooldown duration

### **J2 — Permit under threshold**

- **Given** intent = HEAVY_EVAL
- **And** request rate under threshold
- **When** evaluation runs
- **Then** outcome_type = PERMIT

---

## **Feature Group K — Audit-Only / Shadow Mode**

### **K1 — Log-only in shadow rollout**

- **Given** environment rollout flag = SHADOW
- **When** evaluation runs
- **Then** outcome_type = LOG_ONLY
- **And** audit event includes full evaluation context

### **K2 — Normal enforcement when not shadowed**

- **Given** rollout flag != SHADOW
- **When** evaluation runs
- **Then** outcome_type != LOG_ONLY (unless policy explicitly says so)

---

## **Feature Group L — Precedence Rules (Most-Restrictive Wins)**

> You should codify this as a single deterministic precedence chain.
> 

### **L1 — Deny overrides permit**

- **Given** one rule returns PERMIT
- **And** another rule returns DENY
- **When** evaluation runs
- **Then** final outcome_type = DENY

### **L2 — Require approval overrides permit**

- **Given** one rule returns PERMIT
- **And** another returns REQUIRE_APPROVAL
- **When** evaluation runs
- **Then** final outcome_type = REQUIRE_APPROVAL

### **L3 — Redaction can coexist with permit**

- **Given** base outcome would be PERMIT
- **And** visibility rule requires REDACT
- **When** evaluation runs
- **Then** outcome_type = REDACT
- **And** constraints include what is redacted
- **And** access to non-redacted summary remains permitted (if policy says so)

---

## **Suggested Feature File Layout**

- A_input_contract.feature
- B_determinism.feature
- C_output_contract.feature
- D_rbac_tenant.feature
- E_tier_gating.feature
- F_posture.feature
- G_high_risk_actions.feature
- H_visibility_redaction.feature
- I_lifecycle_gating.feature
- J_rate_limit.feature
- K_shadow_mode.feature
- L_precedence.feature

---

If you want, I can now generate the **starter Gherkin suite** (actual .feature files with Scenario Outlines + Examples tables) by assuming your enums for:

- posture (SUGGEST_ONLY, REQUIRE_APPROVAL, AUTO_APPLY)
- action intents/classes
- tier names
    
    …and I’ll keep it strict and CI-friendly.