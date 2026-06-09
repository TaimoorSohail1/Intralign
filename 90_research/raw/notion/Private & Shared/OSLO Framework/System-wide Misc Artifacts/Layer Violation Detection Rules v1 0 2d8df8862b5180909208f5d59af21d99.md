# Layer Violation Detection Rules v1.0

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Artifact Type:** System Guardrails + Lint Rules

**Status:** Canonical

**Audience:** Engineering, AI/ML, QA

**Applies Across:** Project Knowledge · Ingestion/Transformation · Reasoning · Judgment · Governance · Communication · Workflows

---

## **1. Purpose**

These rules define **what constitutes a layer violation** and how OSLO must **detect, block, and audit** violations at build-time and runtime.

> Core idea:
> 

> Violations are not “bugs” — they are
> 
> 
> **trust-breaking behavior**
> 

---

## **2. Canonical Violation Classes**

### **V-01: Unauthorized Mutation**

Any write to Project Knowledge not backed by explicit UI authorization (G-03) or approved onboarding scope.

- **Examples**
    - Reasoning writes inferred nodes directly into canonical graph
    - Governance applies a “quiet fix”
    - Communication triggers a “save” side effect

**Severity:** Blocker

---

### **V-02: Cross-Layer Role Collapse**

A layer performs the responsibilities of another layer.

- **Examples**
    - Reasoning decides suppression timing (“not important, ignore it”)
    - Judgment recommends actions (“you should change the date”)
    - Communication chooses surface (“show in chat”)

**Severity:** High

---

### **V-03: Hidden Assumption / Placeholder Masking**

Any output influenced by assumptions/placeholders without explicit labeling in the appropriate artifact.

- **Examples**
    - Judgment emits scores without placeholder_conditioned
    - Communication presents conditional outputs as unconditional
    - Ingestion commits parsed values without uncertainty metadata

**Severity:** High

---

### **V-04: Non-Deterministic Reasoning**

Same inputs + same rule versions produce materially different Reasoning outputs.

- **Examples**
    - Random sampling without pinning
    - Model version drift without tagging
    - Unlogged heuristics

**Severity:** High (becomes Blocker for core issues)

---

### **V-05: Raw Input Leakage**

Reasoning/Judgment consumes raw inputs or ingestion proposals directly.

- **Examples**
    - Reasoning reads document text from ingestion store
    - Judgment scores based on uncommitted proposals

**Severity:** Blocker

---

### **V-06: Silent Supersession**

High-impact conclusions change without explicit supersession linkage.

- **Examples**
    - Recompute overwrites prior surfaced score without trace
    - “Updated” messages replace earlier claims silently

**Severity:** High

---

### **V-07: Governance Bypass**

Any system component surfaces content on a restricted surface without Governance authorization.

- **Examples**
    - Communication posts to chat directly
    - Backend job triggers notifications

**Severity:** Blocker

---

### **V-08: Action Without Consent**

Any automation or “execution” behavior occurs without explicit opt-in contract (future-proof rule).

- **Examples**
    - System writes to external tools (Jira/Asana) without opt-in
    - Background reconciliation changes the plan

**Severity:** Blocker

---

## **3. Layer Contracts as Enforceable Capabilities**

Each layer gets a **capability token** (compile-time + runtime) that gates what it can do.

### **Allowed Capabilities by Layer**

| **Layer** | **Allowed** | **Forbidden** |
| --- | --- | --- |
| **Ingestion** | parse, propose, attach confidence, store raw | commit canonical, trigger reasoning, message user |
| **Project Knowledge** | store canonical, version, snapshot | infer, score, decide timing, generate language |
| **Reasoning** | issues, evidence chains, placeholders (proposed), raw signals | write canonical, decide display, generate language |
| **Judgment** | scores, confidence, condition tags | mutate knowledge, recommend actions, decide surfaces |
| **Governance** | suppress/surface decisions, surface selection, state transitions | change truth, change scores, generate language |
| **Communication** | language, progressive disclosure, explanation structure | choose to speak, mutate, trigger actions |

**Detection rule:** if a layer calls an API outside its capability set → violation.

---

## **4. Detection Mechanisms**

### **4.1 Build-Time (Lint) Rules**

Static checks in PR/CI:

- **LINT-01:** No Knowledge write methods imported outside Knowledge service
- **LINT-02:** No “notify/chat” methods callable outside Communication service
- **LINT-03:** Reasoning module cannot import Governance/Communication modules
- **LINT-04:** Judgment module cannot import UI/action handlers
- **LINT-05:** Any function named commit, save, mutate, update must be in whitelisted packages
- **LINT-06:** Every Reasoning output type must include evidence_chain_id and rule_version

**CI gating:** any lint failure blocks merge.

---

### **4.2 Runtime Guards (Policy Firewall)**

Even with lint, enforce at runtime:

### **Guard A: Canonical Write Gate**

All writes to Project Knowledge go through a single function:

commit_canonical_change(change, authorization_context)

Rules:

- reject if no authorization_context
- reject if authorization not UI_ACTION or ONBOARDING_SCOPED
- reject if change source is Reasoning/Judgment/Governance/Communication
- log every commit with provenance

### **Guard B: Surface Emission Gate**

All user-visible emission must go through:

emit(surface, payload, governance_decision_id)

Rules:

- reject if missing governance decision
- reject if surface not allowed by decision
- reject if Chat without override_justification

### **Guard C: Reasoning Determinism Gate**

Reasoning outputs must include:

- input_snapshot_id
- rule_version
- model_version (if used)
- seed (if any stochasticity exists)

If missing → downgrade reliability to **Constrained** and suppress.

---

### **4.3 Audit Assertions**

On every run, emit a **LayerBoundaryAudit**:

```
LayerBoundaryAudit {
  request_id
  invoked_layers[]
  canonical_mutations[]
  governance_decisions[]
  emissions[]
  violations_detected[]
}
```

QA can replay audits to detect drift.

---

## **5. Canonical Violation Rules by Layer**

### **5.1 Ingestion Violations**

- **IV-01:** Writes canonical directly (V-01)
- **IV-02:** Marks proposals as confirmed without user acceptance (V-03)
- **IV-03:** Triggers messaging (V-07)

**Automated check:** any ingestion output must be ProposedElement only.

---

### **5.2 Project Knowledge Violations**

- **KV-01:** Accepts mutation without authorization_context (V-01)
- **KV-02:** Stores derived outputs as canonical (scores/issues) (V-02)
- **KV-03:** Allows auto-sync overwrite between human/machine (V-03)

**Automated check:** schema-level constraints:

- derived_* tables cannot be in canonical schema
- epistemic_state required on insert/update

---

### **5.3 Reasoning Violations**

- **RV-01:** Calls any canonical commit function (V-01)
- **RV-02:** Uses “should”/recommendation language in any output (V-02)
- **RV-03:** Outputs without evidence chain (V-02)
- **RV-04:** Consumes non-canonical ingestion proposals (V-05)

**Automated check:** Reasoning outputs must be non-textual data types only.

---

### **5.4 Judgment Violations**

- **JV-01:** Writes to knowledge or modifies inferred elements (V-01)
- **JV-02:** Uses thresholds to decide visibility (V-02)
- **JV-03:** Emits scores without confidence + placeholder conditioning flags (V-03)

**Automated check:** Score must include:

- confidence
- conditioned_on_placeholders
- judgment_snapshot_id

---

### **5.5 Governance Violations**

- **GV-01:** Recomputes truth/overrides evidence (V-02)
- **GV-02:** Generates language (V-02)
- **GV-03:** Allows emission without decision object (V-07)

**Automated check:** Governance output must be decision object only.

---

### **5.6 Communication Violations**

- **CV-01:** Speaks without governance authorization (V-07)
- **CV-02:** Presents conditional outputs as absolute (V-03)
- **CV-03:** Implies mutation/action (“I updated…”) without UI authorization (V-01/V-08)

**Automated check:** Communication templates must support:

- condition disclosure slot
- boundary statement slot
- confidence-aware phrasing

---

## **6. Severity & System Response**

| **Severity** | **Examples** | **Response** |
| --- | --- | --- |
| **Blocker** | V-01, V-05, V-07, V-08 | Reject action, enter **Safe** reliability state, log incident |
| **High** | V-02, V-03, V-06 | Suppress output, degrade to **Constrained**, require remediation |
| **Medium** | Minor determinism drift | Suppress chat, allow panel summary only |
| **Low** | Formatting/verbosity mismatch | Log + fix in next iteration |

---

## **7. Minimum QA Test Suite**

1. **No layer can write canonical without authorization context**
2. **Reasoning outputs never contain natural language**
3. **Judgment outputs always include confidence + conditioned flags**
4. **Any emission requires governance decision id**
5. **60Second mode blocks all interruptive emissions**
6. **Replay test: same snapshot + versions → identical issues**
7. **Supersession required when prior surfaced conclusion changes**

---

## **Canonical Close**

> OSLO is trustworthy only if its layers remain separable under pressure.
> 

> Layer violations are treated as trust incidents, not edge cases.
> 

---

If you want, next I can convert this into:

- a **policy YAML** your services can enforce,
- a **TypeScript/Go interface set** (capability tokens + guards),
- or a **QA checklist + automated test specs** mapped to each violation class.