# Communication Layer — Use Case Matrix v1.0

**System:** OSLO

**Layer:** Communication

**Spec Type:** Normative (behavioral coverage)

**Audience:** Engineering, UX, QA

**Status:** Canonical

**Upstream Contract:** Governance → Communication Consumption Contract v1.0

---

## **1. Purpose**

This matrix enumerates the **supported Communication Layer use cases** in v1 and specifies:

- when Communication is invoked
- what Governance outcomes it consumes
- what channels it must support
- what constraints it must enforce
- what it must *never* do (non-responsibilities)

Communication’s job is to **render permitted information safely**—not to decide permissions or perform actions.

---

## **2. Invocation Scope**

Communication is invoked whenever the system needs to:

- display something in the UI
- return something via API
- generate an export payload (e.g., PDF-ready)
- compose a notification payload (email/in-app)
- provide an integration-facing message payload

Communication must accept only:

- CommunicationContextEnvelope
- GovernanceOutcome

---

## **3. Dimensions Used in the Matrix**

Each use case is characterized by:

- **Channel**: UI | API | PDF | EMAIL | INTEGRATION
- **Presentation Intent**: DISPLAY | EXPORT | NOTIFY
- **Governance Outcome Type**
- **Required Constraints**
- **Permitted Output Scope**

---

## **4. Use Case Matrix**

### **COM-UC-01 — Permit: Summary Display (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | PERMIT |
| Required Constraints | ALLOWED_SCOPE=SUMMARY |
| Output | Summary-only view |
| Notes | No details/evidence blocks |

---

### **COM-UC-02 — Permit: Details Display (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | PERMIT |
| Required Constraints | ALLOWED_SCOPE=DETAILS |
| Output | Details view (no evidence unless allowed) |
| Notes | Enforce evidence visibility separately |

---

### **COM-UC-03 — Permit: Evidence Display (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | PERMIT |
| Required Constraints | EVIDENCE_VISIBILITY=VISIBLE and scope allowing evidence |
| Output | Evidence section rendered |
| Notes | Must not show evidence if visibility hidden |

---

### **COM-UC-04 — Redact: Evidence Hidden (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | REDACT |
| Required Constraints | EVIDENCE_VISIBILITY=HIDDEN (and/or REDACT_FIELDS) |
| Output | Evidence section removed/obfuscated |
| Notes | May show “evidence hidden” indicator if allowed |

---

### **COM-UC-05 — Deny: Access Denied (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | DENY |
| Required Constraints | none (reason_codes required) |
| Output | Denial state |
| Notes | Use reason-code mapped copy; no internal policy text |

---

### **COM-UC-06 — Require Approval: Pending Approval (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | REQUIRE_APPROVAL |
| Required Constraints | APPROVER_ROLES, APPROVAL_TTL |
| Output | Approval-needed state |
| Notes | Must not imply action executed |

---

### **COM-UC-07 — Downgrade: Export Option Restriction (UI)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI |
| Intent | DISPLAY |
| Governance Outcome | DOWNGRADE |
| Required Constraints | ALLOWED_FORMAT and/or WRITE_MODE |
| Output | Restricted options UI |
| Notes | Hide/disable disallowed options |

---

### **COM-UC-08 — Permit: API Response (Summary)**

| **Field** | **Value** |
| --- | --- |
| Channel | API |
| Intent | DISPLAY |
| Governance Outcome | PERMIT |
| Required Constraints | ALLOWED_SCOPE=SUMMARY |
| Output | Summary JSON payload |
| Notes | Strictly bounded; no extra fields |

---

### **COM-UC-09 — Redact: API Response With Field Redaction**

| **Field** | **Value** |
| --- | --- |
| Channel | API |
| Intent | DISPLAY |
| Governance Outcome | REDACT |
| Required Constraints | REDACT_FIELDS=[...] |
| Output | JSON with redacted fields removed/obfuscated |
| Notes | No leakage via metadata |

---

### **COM-UC-10 — Deny: API Error Response**

| **Field** | **Value** |
| --- | --- |
| Channel | API |
| Intent | DISPLAY |
| Governance Outcome | DENY |
| Required Constraints | none |
| Output | Standardized error payload |
| Notes | No internal codes exposed; reason_codes mapped to safe error types |

---

### **COM-UC-11 — Permit: PDF Export (PDF Channel)**

| **Field** | **Value** |
| --- | --- |
| Channel | PDF |
| Intent | EXPORT |
| Governance Outcome | PERMIT |
| Required Constraints | ALLOWED_FORMAT=PDF, ALLOWED_SCOPE |
| Output | PDF-ready render payload |
| Notes | Communication outputs content; exporter renders file |

---

### **COM-UC-12 — Downgrade: PDF-Only Export**

| **Field** | **Value** |
| --- | --- |
| Channel | PDF |
| Intent | EXPORT |
| Governance Outcome | DOWNGRADE |
| Required Constraints | ALLOWED_FORMAT=PDF |
| Output | PDF-ready payload only |
| Notes | Do not generate other formats |

---

### **COM-UC-13 — Watermarked Export**

| **Field** | **Value** |
| --- | --- |
| Channel | PDF |
| Intent | EXPORT |
| Governance Outcome | PERMIT or DOWNGRADE |
| Required Constraints | WATERMARK_REQUIRED=true |
| Output | PDF-ready payload with watermark flag |
| Notes | Watermark application can be downstream but must be enforced/flagged here |

---

### **COM-UC-14 — Redact: Sensitive Fields in Export**

| **Field** | **Value** |
| --- | --- |
| Channel | PDF |
| Intent | EXPORT |
| Governance Outcome | REDACT |
| Required Constraints | REDACT_FIELDS=[...] |
| Output | Export payload with fields removed/obfuscated |
| Notes | Redact before templating/layout |

---

### **COM-UC-15 — Rate Limit Message (UI/API)**

| **Field** | **Value** |
| --- | --- |
| Channel | UI or API |
| Intent | DISPLAY |
| Governance Outcome | RATE_LIMIT |
| Required Constraints | COOLDOWN_SECONDS |
| Output | Rate-limit state/message |
| Notes | Show cooldown if allowed; otherwise generic |

---

### **COM-UC-16 — Log Only (No User Output)**

| **Field** | **Value** |
| --- | --- |
| Channel | Any |
| Intent | Any |
| Governance Outcome | LOG_ONLY |
| Required Constraints | none |
| Output | No user-visible output |
| Notes | Still emit audit; optional admin-only indicator only if explicitly permitted |

---

### **COM-UC-17 — Notification Payload: Deny/Approval/Rate Limit**

| **Field** | **Value** |
| --- | --- |
| Channel | EMAIL |
| Intent | NOTIFY |
| Governance Outcome | DENY / REQUIRE_APPROVAL / RATE_LIMIT |
| Required Constraints | Varies (e.g., approval TTL) |
| Output | Notification payload (subject/body fields) |
| Notes | Must not include restricted content; reason-code mapped copy only |

---

### **COM-UC-18 — Integration Message Payload (Non-Execution)**

| **Field** | **Value** |
| --- | --- |
| Channel | INTEGRATION |
| Intent | NOTIFY or DISPLAY |
| Governance Outcome | PERMIT / DENY / DOWNGRADE |
| Required Constraints | ALLOWED_SCOPE, possibly ALLOWED_FORMAT |
| Output | Integration-facing message payload |
| Notes | Communication never performs the sync; only prepares messaging/status content |

---

## **5. Explicit Non-Use Cases (Out of Scope v1)**

Communication does **not**:

- bypass constraints to “be helpful”
- fetch additional data not explicitly permitted
- interpret policy logic
- execute actions or approvals
- generate new recommendations (unless already provided as permitted, bounded content)
- show internal codes, policy text, or rule traces

---

## **6. Coverage Guarantees**

This matrix covers v1 across:

- all Governance outcome types
- primary channels (UI, API, PDF) and optional (EMAIL, INTEGRATION)
- scope enforcement (summary/details/evidence)
- export enforcement (format, watermark, redaction)
- safe failure modes (deny, rate limit, log only)

---

## **7. Engineering Acceptance Rule**

> If a Communication behavior cannot be mapped to
> 
> 
> **exactly one**
> 
> **not v1-compliant**
> 

---

If you want, next I can generate:

- **Communication Layer Implementation-Ready Checklist (v1.0)**, or
- **Reason-Code → UX Copy Mapping Spec (v1.0)** (including priority rules for multiple reason codes).