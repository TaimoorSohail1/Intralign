# Compute & Safety Contract v1.0

---

---

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Scope:** System-level (Cross-Layer)

**Spec Type:** Normative / Enforceable

**Audience:** Engineering, Platform, Infrastructure, Security

**Status:** Canonical

**Applies To:** All product tiers, all environments

> This contract governs infrastructure-level safeguards that protect system stability, integrity, and cost controls.
> 

> 
> 

> It explicitly does
> 
> 
> **not**
> 

---

## **1. Purpose**

The Compute & Safety Contract exists to:

- Protect OSLO from abuse, overload, and pathological usage
- Ensure system stability under burst and adversarial conditions
- Control worst-case compute exposure
- Preserve epistemic integrity across all layers

This contract enforces **how the system protects itself**, not **what users are allowed to do**.

---

## **2. Non-Negotiable Principle**

> Infrastructure safeguards may throttle, defer, or degrade processing —
> 

> but may never change epistemic outcomes, authority rules, or tier behavior.
> 

Violations of this principle are **system defects**, not acceptable trade-offs.

---

## **3. Scope of Control**

This contract governs **infrastructure behavior only**, including:

- Request throughput
- Compute concurrency
- Burst smoothing
- Abuse detection
- Emergency safety ceilings

It does **not**:

- Define feature access
- Enforce tier caps
- Gate issue resolution
- Modify reasoning, judgment, or governance semantics

---

## **4. Guardrail Classes**

### **4.1 Background Rate Limiting**

**Purpose**

Prevent excessive request frequency from destabilizing services.

**Rules**

- Applied per account, per surface (API, chat, UI)
- Transparent to product logic
- Independent of tier entitlements

**Allowed behaviors**

- Slow responses
- Deferred execution
- Request queuing

**Prohibited behaviors**

- Silent data loss
- Partial writes
- Authority escalation or denial

---

### **4.2 Burst Dampening**

**Purpose**

Smooth sudden spikes in compute demand (e.g., chat storms, retries, automation).

**Rules**

- Temporary throttling only
- Dampening windows are short-lived
- No permanent state changes allowed

**Invariant**

> Burst dampening may delay processing, but must never alter outputs.
> 

---

### **4.3 Per-Account Safety Ceilings**

**Purpose**

Enforce absolute upper bounds on compute usage to protect system viability.

**Characteristics**

- Hard limits
- Rarely triggered
- Treated as fail-safes, not entitlements

**Behavior on breach**

- Processing paused or deferred
- Explicit system-level error returned
- No implicit downgrade or upgrade suggestion

**Explicit Rule**

> Safety ceilings must never masquerade as product tier limits.
> 

---

### **4.4 Abuse Detection**

**Purpose**

Detect and respond to malicious, automated, or exploitative usage patterns.

**Signals may include**

- Non-human interaction rates
- Repeated identical operations
- Patterned probing of limits
- Intentional recompute storms

**Response Ladder**

1. Soft throttling
2. Temporary suspension
3. Manual review
4. Account-level restriction (last resort)

**Invariant**

> Abuse controls are orthogonal to pricing and must never be used as monetization levers.
> 

---

## **5. Graceful Degradation Semantics**

When compute or safety limits are reached, OSLO **must degrade safely**.

### **5.1 Allowed Degradation Modes**

- Deferred recompute
- Slower response times
- Reduced inference breadth (internal only)
- Conservative evaluation paths

### **5.2 Forbidden Degradation Modes**

OSLO must **never**:

- Auto-resolve issues
- Drop findings
- Skip evidence chain generation
- Promote inferred data
- Block authority actions silently

---

## **6. Authority Preservation Guarantees**

Infrastructure controls **must not**:

- Resolve or suppress issues
- Modify findings
- Change severity or confidence
- Bypass Governance decisions
- Alter tier entitlements

> Authority flows only through Governance and explicit user action.
> 

---

## **7. Observability & Auditability**

All safeguard actions must be:

- Logged with timestamps
- Attributed to safeguard class
- Correlated to request IDs
- Reviewable by engineering and security

Safeguard logs **must not** be exposed to users by default.

---

## **8. Failure Semantics**

If safeguards prevent immediate execution:

- The system must fail **loudly and explicitly**
- State must remain consistent
- No partial side effects are allowed

Retry behavior must be deterministic.

---

## **9. Relationship to Product Tiers**

| **Aspect** | **Governed By** |
| --- | --- |
| Issue finalization caps | Tier Capability Contract |
| Severity restrictions | Judgment & Governance |
| Compute ceilings | **This contract** |
| Rate limiting | **This contract** |
| Abuse handling | **This contract** |

There is **no overlap**.

---

## **10. Invariants (Locked)**

1. Compute limits never redefine product capability
2. Safety controls never change epistemic truth
3. Degradation never creates or destroys authority
4. Abuse handling is not monetization
5. Visibility does not imply entitlement

---

## **Canonical Close**

> OSLO monetizes certainty, not compute.
> 

> 
> 

> This contract ensures the system remains safe and stable
> 

> without ever confusing protection with permission.
> 

---

If you want, next I can:

- Wire this into the **Tier Capability Contract** explicitly (cross-refs)
- Draft a **Platform Runbook** for safeguard triggers
- Stress-test this against Free-tier adversarial scenarios
- Or condense this into a **one-page engineering brief**

Just tell me where to go.