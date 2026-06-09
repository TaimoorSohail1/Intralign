# Rules & Policy Repository Architecture v1.0

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Scope:** Reasoning rules, Judgment criteria, Governance policies, Communication templates

**Goal:** Enable safe evolution of rules/criteria/policies/templates via repository-managed, versioned artifacts—without code rewrites.

---

## **1. Design Principles**

1. **Behavior lives in versioned artifacts**
    
    If it may change over time, it’s a versioned artifact (repo-managed), not hard-coded.
    
2. **Deterministic by default**
    
    Same inputs + same artifact versions ⇒ same outputs.
    
3. **No silent behavior changes**
    
    Changes deploy via explicit promotion + rollback paths.
    
4. **Separation of concerns**
- **Reasoning**: structural rules + issue detection + inference rules
- **Judgment**: scoring + thresholds + severity mapping
- **Governance**: communication permissions + routing + suppression policy
- **Communication**: templates, tone variants, surface rendering rules (no behavior logic)
1. **Every runtime output is traceable**
    
    All outputs must carry the artifact version IDs used (for auditing and replay).
    

---

## **2. Repository Layout**

A single mono-repo is simplest initially:

```
oslo-rules/
  README.md
  tooling/
    validate/          # schema + invariants validation
    lint/              # style + anti-footgun checks
    test-harness/      # scenario replay runner
    packager/          # build bundles for deployment
  schemas/
    reasoning.schema.json
    judgment.schema.json
    governance.schema.json
    comms.schema.json
  reasoning/
    v1/
      inference/
      issues/
      evidence/
      profiles/
  judgment/
    v1/
      scoring/
      severity/
      thresholds/
      profiles/
  governance/
    v1/
      policies/
      routing/
      suppression/
      correction/
      onboarding/
  communication/
    v1/
      templates/
      tone/
      surface/
      lexicon/
  bundles/
    manifest.json      # build output mapping -> bundle versions
```

### **Profiles (optional but recommended)**

Profiles allow controlled variation (later: “Agile vs Waterfall”, “Enterprise vs Startup”) without branching code.

- reasoning/profiles/<profile>.yaml
- judgment/profiles/<profile>.yaml
- governance/policies/<profile>.yaml
- communication/tone/<profile>.yaml

---

## **3. Artifact Types and Required Fields**

### **3.1 Reasoning Rules**

**Artifacts**

- InferenceRuleSet
- IssueRuleSet
- EvidenceRuleSet

**Required metadata**

- id (stable)
- version (semver)
- engine_compat (min/max supported engine versions)
- inputs_required (for determinism)
- outputs_produced (issue subtypes, inference types)
- test_cases_ref

### **3.2 Judgment Criteria**

**Artifacts**

- ScoringModel
- SeverityMap
- ThresholdSet

**Required metadata**

- id, version, engine_compat
- dimension_weights
- issue_contribution_map
- severity_cutoffs
- display_contract (explicitly: “no confidence exposed”)

### **3.3 Governance Policy Sets**

**Artifacts**

- PolicySet (primary)
- RoutingPolicy
- SuppressionPolicy
- CorrectionPolicy
- OnboardingPosturePolicy

**Required metadata**

- policy_version (semver)
- guardrail_refs (G-01…G-08)
- state_constraints (InputCapture/PlanGenerating/PlanPresented/SteadyState)
- surface_authorization_rules
- cta_authorization_rules

### **3.4 Communication Templates**

**Artifacts**

- TemplateSet
- TonePack
- SurfacePack
- Lexicon

**Hard constraint**

- No logic that changes behavior (no thresholds, no suppression decisions).

---

## **4. Versioning Strategy**

### **4.1 SemVer Rules (per artifact family)**

- **MAJOR**: breaking meaning or schema (requires migration plan)
- **MINOR**: new rules/fields with backward compatibility
- **PATCH**: bug fixes, typo fixes, non-breaking adjustments

### **4.2 Runtime “Version Pinning”**

Every OSLO run must pin:

- reasoning_rules_version
- judgment_model_version
- governance_policy_version
- comms_template_version

This enables:

- Replay/debug
- Audit trails
- Safe gradual rollout

---

## **5. Promotion Workflow (Draft → Active)**

### **Environments**

- **dev**: fast iteration
- **staging**: scenario replay + product validation
- **prod**: only promoted artifacts

### **Lifecycle States**

1. **Draft**
2. **Candidate**
3. **Approved**
4. **Active**
5. **Deprecated**
6. **Retired**

### **Required Gates**

- **Schema validation** (all artifacts)
- **Static linting** (anti-footguns, forbidden patterns)
- **Scenario replay** (Execution Scenarios v1.0 + any regression pack)
- **Golden output diff** (must be explainable and expected)
- **Human approval** (owner sign-off; required for prod)

---

## **6. Rollout and Rollback**

### **Rollout Modes**

1. **Hard pin** (default for early alpha): one version active per environment
2. **Segmented pin** (later): user/project cohort selection
3. **Shadow evaluation** (later): compute with candidate versions, do not disclose

### **Rollback Guarantee**

Rollback is a **configuration change**, not a code deploy:

- Re-point active bundle to previous version in bundles/manifest.json
- Preserve:
    - already-generated RCUs referencing old policy versions
    - replay ability for past outputs

---

## **7. Loading Model in the Application**

### **7.1 Bundle Packaging**

At build time, pack artifacts into immutable bundles:

- rules_bundle_{hash}.json
- policy_bundle_{hash}.json
- comms_bundle_{hash}.json

### **7.2 Runtime Resolver (single responsibility)**

A small “resolver” component selects:

- which bundle to use per project/run (based on env + pin + cohort)
- returns version IDs to attach to outputs

### **7.3 Caching & Safety**

- Cache bundles in memory with checksum verification
- Fail closed:
    - If Governance policy missing → default to silence (safe)
    - If Communication templates missing → fallback minimal template
    - If Reasoning/Judgment missing → block evaluation disclosure, log error

---

## **8. Validation and Invariants Tooling**

### **8.1 Schema Validation**

- JSON Schema or equivalent for each artifact family
- Mandatory metadata fields enforced

### **8.2 Invariant Validation (must be automated)**

Examples:

- **Governance** policies must reference guardrails and must not authorize forbidden transitions (G-01..)
- **Communication** templates must not include policy thresholds or suppression logic
- **Judgment** must not expose confidence for UI consumption
- **Reasoning** must require evidence chain generation for every issue subtype

### **8.3 “Policy Lint”**

A custom linter flags:

- missing state constraints
- chat surface allowed when forbidden (InputCapture, PlanGenerating)
- CTA execution without confirmation boundary

---

## **9. Testing Strategy**

### **9.1 Scenario Replay Harness (Core)**

Given:

- a frozen project snapshot
- pinned versions
- a sequence of events (execution scenario)

The harness asserts:

- state transitions are legal
- authorizations match expectations
- outputs carry correct version IDs
- no forbidden communications occur

### **9.2 Golden Fixtures**

Maintain canonical fixtures for:

- onboarding flow
- critical feasibility blocker
- chat “why” explanation
- hypothetical analysis isolation

### **9.3 Diff Rules**

Not all diffs are failures; require classification:

- **Expected improvement**
- **Behavior change (requires approval)**
- **Regression (blocked)**

---

## **10. Ownership and Change Control**

Assign owners per artifact family:

- Reasoning rules: AI/ML + Product (joint)
- Judgment criteria: Product + Eng (joint)
- Governance policies: Product owner (final) + Eng
- Communication templates: Design/UX writing + Product

Every change requires:

- PR with scenario references
- artifact version bump
- changelog entry (human readable)

---

## **11. What This Enables Immediately**

- Rapid iteration of issue taxonomy and inference rules
- Scoring tuning without re-architecting
- Governance behavior changes with auditability
- Voice/template improvements without logic drift
- Safe rollback when behavior surprises users

---

## **Recommended Next Artifact**

To make this implementable with minimal ambiguity, produce:

**Policy Spec v1.0**

- PolicySet schema (fields + types)
- Decision tables (routing, suppression, CTA authorization, correction)
- Default policies for onboarding + steady-state

If you want, I’ll publish **Policy Spec v1.0** next in the same Notion-ready format.