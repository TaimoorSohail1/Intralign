# Communication Layer — Implementation-Ready Checklist (v1.0)

**System:** OSLO

**Layer:** Communication

**Audience:** Frontend, Backend API, UX, QA

**Goal:** Render **only** what Governance permits, enforce all constraints deterministically, and produce user-safe, auditable outputs across UI, API, and Export channels—without executing actions or loosening permissions.

---

## **1) Foundations & Contracts**

☐ **Lock the Communication input contract**

- Required inputs:
    - CommunicationContextEnvelope
    - GovernanceOutcome
- No other upstream data may be consumed unless explicitly permitted via constraints.

☐ **Lock supported channels**

- UI | API | PDF | EMAIL | INTEGRATION

☐ **Lock presentation intents**

- DISPLAY | EXPORT | NOTIFY

☐ **Strict parsing**

- Unknown fields → **fail closed** (safe denial/minimal output)
- Invalid enums → **fail closed**

---

## **2) Entrypoint & Purity**

☐ **Single deterministic entrypoint**

```
render(context, governanceOutcome) => RenderResult
```

☐ **No side effects**

- No writes to canon
- No network calls
- No approvals, no execution
- Logging allowed but must not influence output

☐ **Determinism**

- Same inputs → identical rendered output (byte-level for API/export payloads)

---

## **3) Input Validation (Fail-Closed)**

☐ **Context completeness required**

- channel
- presentation_intent
- audience
- locale
- ui_density
- brand_profile
- accessibility_mode

☐ **GovernanceOutcome validity**

- outcome_type enum valid
- policy_version_used present
- If outcome_type != PERMIT → reason_codes non-empty

☐ **Channel compatibility**

- Channel must be allowed by constraints (e.g., export formats)

---

## **4) Outcome Handling (Authoritative)**

☐ **PERMIT**

- Render **only** within constraints (ALLOWED_SCOPE, ALLOWED_FORMAT, visibility)
- Never exceed scope

☐ **DENY**

- Render denial state only
- Use reason-code mapped copy
- No restricted content shown

☐ **REQUIRE_APPROVAL**

- Render approval-needed state
- Show approver roles/TTL **only if** present
- Do not imply execution

☐ **DOWNGRADE**

- Render downgraded options only
- Hide/disable disallowed formats/modes

☐ **REDACT**

- Remove/obfuscate specified fields
- Indicate redaction only if allowed

☐ **RATE_LIMIT**

- Render rate-limit state
- Respect COOLDOWN_SECONDS

☐ **LOG_ONLY**

- Produce **no** user-visible output
- Emit audit only

---

## **5) Constraint Enforcement (Non-Negotiable)**

☐ **Scope**

- ALLOWED_SCOPE=SUMMARY → summary only
- DETAILS → no evidence unless visibility allows
- FULL → only if explicitly permitted

☐ **Evidence Visibility**

- EVIDENCE_VISIBILITY=HIDDEN → no evidence content, ids, or paths
- VISIBLE → render evidence sections

☐ **Formats**

- Enforce ALLOWED_FORMAT
- Downgrade or deny when mismatched

☐ **Write Modes (Labels Only)**

- WRITE_MODE=PROPOSED_ONLY → label clearly as proposal (no execution)

☐ **Redaction**

- Apply REDACT_FIELDS **before** templating
- Ensure redacted data never appears in tooltips, metadata, or logs

☐ **Watermarking**

- WATERMARK_REQUIRED=true → apply watermark flag or rendering hook

☐ **Missing/Ambiguous Constraint**

- **Fail closed** (deny/minimal output)

---

## **6) Copy & Messaging Rules**

☐ **Reason-code driven copy**

- Select copy strictly by reason_codes
- No policy text, no internal codes shown

☐ **Priority resolution**

- Deterministic priority table for multiple reason codes
- Fallback to safe generic copy if unknown code

☐ **Tone control**

- Severity may affect tone, **never** permissions

---

## **7) Channel-Specific Requirements**

### **UI**

☐ Hide/disable disallowed options

☐ No implied execution (labels matter)

☐ Accessibility respected (screen reader, density)

### **API**

☐ Bounded JSON only (no extra fields)

☐ Byte-level determinism

☐ Standardized error shapes for DENY/RATE_LIMIT

### **PDF / Export**

☐ Enforce format, scope, redaction, watermark

☐ Export-ready payload only (file generation downstream)

### **EMAIL / NOTIFY**

☐ Reason-code copy only

☐ No restricted content

☐ Approval/TTL shown only if allowed

### **INTEGRATION**

☐ Messaging/status payload only

☐ No side effects or sync execution

---

## **8) Redaction Safety (Zero-Leak)**

☐ **Pre-template redaction**

- Redact fields before any rendering logic

☐ **No leaks**

- Redacted values must not appear in:
    - visible text
    - metadata
    - logs (counts only)

☐ **Templates resilient to missing fields**

- No crashes; safe placeholders/omission

---

## **9) Validation & Fallbacks**

☐ **Invalid outcome/constraints**

- Render safe denial or minimal output

☐ **Channel mismatch**

- Deny or downgrade per policy

☐ **Unknown reason codes**

- Safe generic messaging

---

## **10) Observability & Audit**

☐ **Audit event per render**

Must include:

- request_id
- channel + presentation_intent
- outcome_type
- constraints applied
- redaction counts
- timestamp

☐ **Audit does not affect rendering**

---

## **11) Test Suite (Implementation-Ready)**

☐ **Contract tests**

- Strict parsing
- Enum validity
- Fail-closed behavior

☐ **Determinism tests**

- Same input → identical output

☐ **Outcome tests**

- One test per outcome type (PERMIT/DENY/…)

☐ **Constraint tests**

- Scope, evidence visibility, format, watermark, redaction

☐ **Channel tests**

- UI/API/PDF behaviors aligned

☐ **Negative tests**

- Missing constraints → fail closed
- Redaction leak checks

---

## **12) Explicitly Out of Scope (v1)**

☐ Permission decisions (Governance)

☐ Correctness decisions (Reasoning/Judgment)

☐ Executing actions or approvals

☐ Policy interpretation or learning

☐ Free-form AI copy generation

---

## **“Done” Gate**

> Communication can render exactly what Governance permits—no more, no less—across all channels, deterministically, with zero data leakage and a complete audit trail.
> 

If you want next, I can convert this checklist into a **Notion-ready table** or generate a **channel-by-channel acceptance test pack** aligned to the Communication Test-Case Matrix.