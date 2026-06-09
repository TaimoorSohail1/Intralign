# Governance Layer — Implementation-Ready Checklist (v1.0)

**System:** OSLO

**Layer:** Governance

**Audience:** Lead Engineer, Security, QA

**Goal:** Implement a deterministic, auditable constraint engine that decides what is **permitted**, **denied**, **approval-gated**, **redacted**, **downgraded**, **rate-limited**, or **log-only**—based on explicit context, tier capabilities, posture, and policy.

---

## **1) Foundations and Contracts**

☐ **Lock the Governance output contract (GovernanceOutcome)**

- Required: outcome_type, reason_codes[] (non-empty when non-PERMIT), constraints[], audit_refs[], policy_version_used
- Outcome types: PERMIT | DENY | REQUIRE_APPROVAL | DOWNGRADE | REDACT | RATE_LIMIT | LOG_ONLY

☐ **Lock core enums**

- intent (e.g., VIEW_SUMMARY | VIEW_EVIDENCE | EXPORT | EXTERNAL_SYNC | MUTATE_CANON | LIFECYCLE_TRANSITION | HEAVY_EVAL)
- action_class (e.g., READ | WRITE | DELETE | EXTERNAL_WRITE | SCOPE_REDUCTION | NOTIFY | EXPORT)
- posture (e.g., SUGGEST_ONLY | REQUIRE_APPROVAL | AUTO_APPLY)
- tier (your tier set)
- reason_code stable codes (no prose)

☐ **Strict parsing**

- Unknown request fields → GOV_ERR_SCHEMA_VIOLATION
- Unknown enum values → GOV_ERR_INVALID_ENUM

---

## **2) Entrypoint and Purity**

☐ **Implement a single deterministic entrypoint**

```
evaluateGovernance(governanceRequest) => GovernanceOutcome
```

☐ **Side-effect free**

- No writes (except audit logging)
- No network calls
- No LLM calls
- No randomness
- No time dependence unless time is explicitly passed in the request

---

## **3) Input Contract Enforcement**

☐ **Require explicit context fields**

- Actor: actor_id, role, tenant_id, workspace_id
- Resource: resource_id, resource_type, tenant_id, workspace_id
- intent, action_class (if applicable)
- tier
- posture
- lifecycle_stage
- policy_version

☐ **Reject forbidden inputs**

- raw user text
- free-form model outputs
- UI-only flags not present in canon
- “common sense” hints

☐ **Upstream consumption bounded**

- If JudgmentDecision is included, it must be the canonical schema only
- Governance does not inspect Reasoning payloads directly in v1

---

## **4) Policy Model (Executable Constraints)**

☐ **Externalize policy as versioned data**

- Policy files / tables keyed by policy_version
- No hard-coded magic numbers in code (except the policy loader bootstrap)

☐ **Define policy sections explicitly**

- RBAC / permissions
- Tenant/workspace isolation rules
- Tier capability rules
- Posture rules
- High-risk action rules
- Visibility/redaction rules
- Lifecycle gating rules
- Rate limiting rules
- Shadow/log-only rollout rules

☐ **Policy validation at load**

- Schema validation
- Enum validation
- Duplicate/conflicting rule detection (where possible)

---

## **5) Rule Evaluation Order (Precedence Chain)**

☐ **Codify a single deterministic precedence chain**

Recommended most-restrictive-first order:

1. Tenant isolation
2. RBAC role permission
3. Rate limiting
4. High-risk action gating
5. Posture constraints
6. Tier capability gating
7. Visibility/redaction
8. Lifecycle gating
9. Rollout (shadow/log-only) modifiers

☐ **Precedence tests**

- DENY overrides PERMIT
- REQUIRE_APPROVAL overrides PERMIT
- REDACT overrides PERMIT for protected components
- DOWNGRADE overrides PERMIT for restricted formats/modes
- LOG_ONLY overrides enforcement in SHADOW mode (if enabled)

---

## **6) RBAC and Tenant Isolation**

☐ **Tenant isolation rule**

- Cross-tenant → DENY (TENANT_ISOLATION)

☐ **Workspace boundary rule**

- Cross-workspace access rules (permit/deny) explicitly defined

☐ **Role permission table**

- Each role × intent × resource_type mapped to permit/deny/require-approval
- No implicit defaults (pick “default deny” or “default permit,” lock it)

---

## **7) Tier Capability Enforcement**

☐ **Tier capability contract integration**

- Capability checks for:
    - integrations
    - evidence visibility
    - export formats
    - automation/auto-apply eligibility (if tier-gated)
- Missing capability → DENY or DOWNGRADE (policy-defined)

☐ **Downgrade rules**

- Export downgrade (e.g., PDF-only)
- Action downgrade (e.g., proposed-only instead of mutate canon)

---

## **8) Posture Enforcement**

☐ **Posture contract applied consistently**

- SUGGEST_ONLY denies MUTATE_CANON
- REQUIRE_APPROVAL gates mutating intents
- AUTO_APPLY only permits when not high-risk and tier/policy allow

☐ **Posture never inferred**

- Must be explicit request field

---

## **9) High-Risk Actions and Approvals**

☐ **High-risk action classification**

- Define high-risk action_class set: DELETE, EXTERNAL_WRITE, SCOPE_REDUCTION (and any others)
- High-risk default → REQUIRE_APPROVAL (unless policy says deny)

☐ **Approval constraints emitted**

- approver_roles[]
- approval_ttl
- approval_scope (resource / workspace / action intent)

---

## **10) Visibility and Redaction**

☐ **Redaction rules are explicit and granular**

- Evidence visibility (hide content, show presence)
- Sensitive field redaction (PII/secrets) for exports/displays

☐ **Redaction emits constraints**

- REDACT_FIELDS=[...]
- EVIDENCE_CONTENT=HIDDEN
- WATERMARK_REQUIRED=true (if applicable)

---

## **11) Lifecycle Gating**

☐ **Lifecycle transitions are gated**

- If intent is LIFECYCLE_TRANSITION and JudgmentDecision is BLOCK → DENY
- Enterprise policies may require approval for transitions

☐ **Lifecycle stage must be explicit**

- No inferred lifecycle from artifacts

---

## **12) Rate Limiting**

☐ **Deterministic rate limiting**

- Rate counters passed in (or fetched deterministically from local store with explicit keying)
- Thresholds are policy-defined per intent

☐ **Rate limit outcome**

- RATE_LIMIT + COOLDOWN_SECONDS constraint

---

## **13) Shadow / Audit-Only Mode (Optional but Recommended)**

☐ **Shadow mode support**

- rollout_mode=SHADOW forces LOG_ONLY
- Audit record includes “would-have-enforced” outcome (optional, policy-defined)

☐ **No user-facing enforcement in SHADOW**

- Only logs

---

## **14) Observability and Audit**

☐ **Audit event emitted for every evaluation**

Must include:

- input hash (deterministic)
- actor + resource scope identifiers (non-sensitive)
- intent + action_class + posture + tier + lifecycle_stage
- policy_version_used
- outcome_type + reason_codes + constraints
- evaluation timestamp (passed in or captured, but never affects decision)

☐ **Replay**

- Same request + same policy_version → same outcome

---

## **15) Error Handling**

☐ **Standard error codes**

- GOV_ERR_MISSING_CONTEXT
- GOV_ERR_FORBIDDEN_INPUT
- GOV_ERR_INVALID_ENUM
- GOV_ERR_SCHEMA_VIOLATION
- GOV_ERR_POLICY_LOAD_FAILED

☐ **Fail-closed posture**

- If policy fails to load/validate → deny by default (or system error). Pick and lock.

---

## **16) Test Suite (Implementation-Ready)**

☐ **Contract tests**

- Schema validation
- Enum boundedness
- Strict unknown-field rejection

☐ **Determinism tests**

- Same input → same output
- Precedence chain determinism

☐ **RBAC/Tenant tests**

- Cross-tenant deny
- Role-based deny/permit

☐ **Tier tests**

- Integration denied without capability
- Export downgraded to allowed format

☐ **Posture tests**

- Suggest-only denies mutations
- Require-approval gates high-risk

☐ **Redaction tests**

- Evidence redaction for lower tiers
- Sensitive field redaction in export

☐ **Lifecycle gating tests**

- Judgment BLOCK prevents transition
- Enterprise transition requires approval

☐ **Rate limiting tests**

- Over threshold → RATE_LIMIT + cooldown

☐ **Shadow mode tests**

- SHADOW → LOG_ONLY + audit includes would-have result (if enabled)

---

## **“Done” Gate**

> Governance can take a canonical request, apply a versioned policy deterministically, and emit a bounded outcome with enforceable constraints and an audit trail—without relying on UI state, LLM prose, or implicit assumptions.
> 

If you want next, I can generate the **Judgment → Governance Consumption Contract (v1.0)** to lock the exact request/response schemas between the layers.