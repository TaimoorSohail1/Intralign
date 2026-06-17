# Ontology Registry

## Status

**Operative — Governance-Tier Orientation Registry (per DL-036)**

This file is the canonical ontology registry. It enumerates ontology entities with citations to Content-tier sources. Authority resides in the Content tier (Doctrine and Constitution) per DL-033. Surface Authority Rule and Status Taxonomy declared by DL-036 R1 and R2 (see `canonical_definitions.md` Status section for full declarations).

### Status Taxonomy (per DL-036 R2)

Each entry carries exactly one status flag: **Canonical**, **Provisional**, **Proposed**, **Conflicting**, **Undefined**, or **Duplicate**. Tie-breaking priority order (per DL-036 Clarification #8): Conflicting > Undefined > Proposed > Provisional > Duplicate > Canonical.

### Legacy Flag Migration (per DL-036 Clarification #2)

- Pre-DL-036 entries flagged "Established" migrated to "Canonical".
- Pre-DL-036 entries flagged "Established (split source)" migrated to "Conflicting", except Organizational Cognition Arc per Clarification #7 (Duplicate).

This file enumerates the major ontology entities, their relationships, and their source references. It does not introduce new entities. Entries are organized by ontological plane.

---

## Reality Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Intended Reality | Canonical | `01_governance/doctrine/04_outcome_integrity_framework.md` |
| Current Reality | Canonical | `01_governance/doctrine/04_outcome_integrity_framework.md` |
| Integrity Gap | Canonical | `01_governance/doctrine/04_outcome_integrity_framework.md` |
| Outcome Integrity | Canonical | `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` Article 3 |
| Outcome Integrity States | Conflicting | `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` Article 33; `03_implementation_specs/08_state_logic_state_machines.md` |

### Relationships

- *Outcome Integrity* = coherence(Intended Reality, Current Reality).
- *Integrity Gap* = divergence(Intended Reality, Current Reality).
- *Outcome Integrity States* are described as conditions over the Reality plane, not workflow phases.

---

## Epistemic Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Dynamic Epistemic Synthesis | Canonical | `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 7 |
| Fact | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Inference | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Assumption | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Recommendation | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Conflict | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Ambiguity | Canonical | `01_governance/doctrine/03_epistemic_system_model.md` |
| Understanding Boundary | Canonical | `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 9 |
| Progressive Epistemic Depth | Canonical | `01_governance/constitution/02_epistemic_constitution.md` Article 10 |
| Organizational Epistemic Memory | Canonical | `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 11 |
| Understanding Evolution | Canonical | `01_governance/doctrine/06_confidence_understanding_model.md` |

### Relationships

- *Dynamic Epistemic Synthesis* aggregates: Intended Reality, Current Reality, evidence, Assumptions, interpretations, governance conditions, Confidence Maturity, organizational overrides, Understanding Boundaries.
- *Facts*, *Inferences*, *Assumptions*, *Recommendations*, *Conflicts* are the five canonical Epistemic Object Types.
- *Ambiguity* (organizational lack of clarity) is distinct from *Understanding Boundary* (system lack of evidence or visibility).
- *Organizational Epistemic Memory* preserves prior states of the synthesis over time.

### Known Conflict

`03_implementation_specs/05_component_system_specification.md` lists nine "Epistemic Label" types (the five canonical plus Unknown, Provisional, Weakly Supported, Validated). This conflates epistemic kind with epistemic strength. Reconciliation pending.

---

## Confidence Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Confidence | Canonical | `01_governance/doctrine/06_confidence_understanding_model.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` Article 30 |
| Confidence Maturity | Canonical | `01_governance/constitution/06_confidence_integrity_constitution.md` Article 32 |
| Confidence Drivers | Conflicting | `01_governance/doctrine/06_confidence_understanding_model.md`; `03_implementation_specs/09_confidence_integrity_logic.md` |
| Confidence Maturity Progression | Canonical | Same as above; `03_implementation_specs/08_state_logic_state_machines.md` |

### Relationships

- *Confidence* is decomposable into drivers; doctrine lists seven (clarity, alignment, feasibility, evidence density, interpretation stability, governance integrity, assumption stability). Spec 09 lists nine, adding stakeholder coverage and dependency stability.
- *Confidence Maturity* progression: Initial → Expanded → Validated → Continuous.
- *Confidence* must remain inspectable, decomposable, explainable, and historically traceable (Article 31).
- *Confidence* and *Outcome Integrity States* are both surfaced through the Persistent Confidence Shell.

### Known Conflict

The driver list differs by two dimensions between doctrine and spec. Reconciliation pending.

---

## Governance Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Governance | Canonical | `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 19 |
| Outcome Integrity Policy | Canonical | `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 20 |
| Human Override | Canonical | `01_governance/constitution/04_governance_constitution.md` Article 21 |
| Governance Escalation | Canonical | `01_governance/constitution/04_governance_constitution.md` Article 22 |
| Disagreement Handling | Canonical | `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 23 |
| Intended Reality Governance | Canonical | `01_governance/constitution/04_governance_constitution.md` Article 24 |
| Override State Model | Conflicting | `03_implementation_specs/08_state_logic_state_machines.md`; `03_implementation_specs/11_governance_override_logic.md` |
| Collaboration Role Model | Proposed | `03_implementation_specs/10_collaboration_sharing_logic.md` |
| Agent Governance | Proposed | `01_governance/doctrine/02_organizational_cognition_model.md`; `03_implementation_specs/12_freemium_tier_behavior_logic.md` |

### Relationships

- *Governance* preserves Epistemic Integrity and Trustworthy Organizational Understanding (Article 19).
- *Outcome Integrity Policies* are human-readable doctrine, not workflow rule engines.
- *Human Override* may diverge from OSLO interpretation; divergence remains visible and preserved.
- *Governance Escalation* scales proportionally to consequence, confidence degradation, governance severity, and organizational doctrine.
- *Intended Reality* itself is governable; OSLO may question, clarify, challenge, or propose alternatives.

### Known Conflicts

- The Override state model (eight-state machine in Spec 08) is not mapped to the Override severity tiers (Low / Moderate / High / Governance Critical in Spec 11).
- The Collaboration Role Model has no constitutional anchor.

---

## Cognition and Progression Plane

### Framework

The canonical progression taxonomy for this plane is the **OSLO Evolution Framework** (DL-034), comprising four distinct but correlated axes.

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| OSLO Evolution Framework | Canonical | DL-034; `01_governance/decisions/rb_003_disposition.md` |
| Cognition Scope (Axis A) | Canonical | `01_governance/doctrine/02_organizational_cognition_model.md` (canonical); DL-034 |
| Product Identity (Axis B) | Canonical | `01_governance/doctrine/09_plg_product_evolution_strategy.md` (canonical); DL-034 |
| Trust Gradient (Axis C) | Canonical | `01_governance/doctrine/09_plg_product_evolution_strategy.md` (canonical); `01_governance/constitution/08_product_evolution_constitution.md` Article 41 (aligned); DL-034 |
| Execution Depth (Axis D) | Canonical | `01_governance/doctrine/10_execution_orchestration_maturity.md` (canonical); `01_governance/constitution/08_product_evolution_constitution.md` Article 43 (aligned); DL-034 |
| Portfolio Cognition | Provisional (long-term capability, not a ratified stage) | `01_governance/doctrine/10_execution_orchestration_maturity.md` Long-Term Direction; `01_governance/constitution/08_product_evolution_constitution.md` Article 44 (Article 44's stage-promotion is provisional under DL-034) |
| Long-Term Direction items (organizational systems cognition; cascading dependency awareness; organizational drift analysis; cross-initiative consequence modeling) | Provisional | `01_governance/doctrine/10_execution_orchestration_maturity.md` |

### Deprecated Predecessor Entries (per DL-036 R5)

The following entries are formally deprecated as Duplicate-status predecessor names. Source files (Doctrine, Constitution) are not edited; deprecation operates only in this registry. Contributors should cite the canonical name in each row.

| Predecessor Name | Status | Canonical Name | Ratifying Decision | Historical Source |
|---|---|---|---|---|
| Strategic Arc | Duplicate | Cognition Scope (Axis A) | DL-034 | `01_governance/doctrine/02_organizational_cognition_model.md` |
| Organizational Cognition Arc | Duplicate | Cognition Scope (Axis A) | DL-034 (extended by DL-036 R5 per Clarification #7) | `01_governance/doctrine/02_organizational_cognition_model.md` |
| Trust Evolution | Duplicate | Trust Gradient (Axis C) | DL-034 | `01_governance/doctrine/09_plg_product_evolution_strategy.md` |

The DL-034 reframings of *Execution Maturity Phases* and *Product Evolution Stages* remain as reframings (now the Execution Depth and Product Identity axes respectively); they are not in DL-036 R5's formal deprecation table.

### Relationships

- The four axes are **distinct** — each has a separately identifiable subject and origin point.
- The four axes are **correlated** — organizations typically advance on multiple axes together.
- The four axes are **convergent at terminal** — three axes terminate at Outcome Orchestration Infrastructure; Trust Gradient terminates at Orchestration Authority.
- The four axes are **independently measurable** — position on one axis does not mechanically determine position on another.
- The framework does not declare equivalence between Phase numbering (Execution Depth) and Stage numbering (Cognition Scope, Product Identity).

### Reconciled Conflicts

- **Cognition Scope stage count.** Doctrine 02's four-stage arc prevails over Article 44's five-stage arc. Closed by DL-034.
- **Product Identity Stage 3 label.** Doctrine 09's "Governed Organizational Cognition" prevails over Article 40's "Governance Infrastructure." Closed by DL-034.
- **Draft Principle 17.** Absorbed by Doctrine 02 via DL-034.

### Open Items on This Plane

- **B-4** Strategic Cognition Environment definition.
- **B-5** Outcome Orchestration Infrastructure unified definition across axes.
- **B-7** Agent Governance placement.
- **B-9** Phase vs Stage numbering equivalence.
- **B-10** Trust Gradient reachability conditions.
- **B-11** Freemium / PLG entry point position.

---

## Workspace and Surface Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Outcome Space | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 13; `01_governance/constitution/10_canonical_definitions.md` |
| Understanding (workspace center) | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 12 |
| What OSLO Understands | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 14 |
| Artifact | Proposed | `01_governance/constitution/03_workspace_constitution.md` Article 15 |
| Artifact Domains | Canonical | Intent, Context, Execution, Schedule, Resources — `01_governance/doctrine/05_workspace_navigation_doctrine.md`; Article 15 |
| Persistent Confidence Shell | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 17 |
| Companion Intelligence Panel | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 18 |
| Attention Queue | Proposed | `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `03_implementation_specs/03_outcome_space_workspace_wireframes.md` |
| Adaptive Workspace | Canonical | `01_governance/constitution/03_workspace_constitution.md` Article 16 |
| Project MRI | Canonical (R1, DL-061) | `OSLO_RELEASE_1_MASTER_SPEC.md` §7/§15C/§21 (per-project); `repository_manifest.md` |

### Relationships

- *Outcome Space* contains the *Understanding* surface and the *Artifact* layer.
- *Artifacts* support *Understanding*; *Understanding* does not support *Artifacts*.
- The *Persistent Confidence Shell* is a global surface visible across all workspace modes.
- The *Companion Intelligence Panel* exists contextually, not as primary navigation.
- *Project MRI* operates against the Reality, Epistemic, and Confidence planes (manifest scope).

---

## Emotional and Visibility Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Calm Strategic Augmentation | Canonical | `01_governance/constitution/09_emotional_interaction_constitution.md` Article 45 |
| Progressive Visibility | Canonical | `01_governance/constitution/05_intelligence_visibility_constitution.md` Article 25 |
| Workspace-Native Intelligence | Canonical | `01_governance/constitution/05_intelligence_visibility_constitution.md` Article 26 |
| Explainability | Canonical | `01_governance/constitution/05_intelligence_visibility_constitution.md` Article 28 |
| Consequence Illumination | Canonical | `01_governance/constitution/05_intelligence_visibility_constitution.md` Article 29 |

### Relationships

- *Progressive Visibility* inverts presence with stability — recede when stable, surface when uncertain.
- *Consequence Illumination* precedes decision support: OSLO helps users understand consequences before decisions.

---

## Cross-Plane Relationships

- *Dynamic Epistemic Synthesis* (Epistemic plane) integrates *Intended Reality* and *Current Reality* (Reality plane), *Confidence* (Confidence plane), governance conditions (Governance plane), and *Understanding Boundaries* (Epistemic plane).
- *Outcome Integrity States* (Reality plane) depend on satisfaction of governance conditions (Governance plane) and trends in *Confidence* (Confidence plane).
- *Governance Escalation* (Governance plane) is triggered by changes in *Confidence* (Confidence plane) and unresolved *Conflicts* (Epistemic plane).
- *Understanding Evolution* (Epistemic plane) is the temporal projection across all other planes, preserved by *Organizational Epistemic Memory*.

---

## Doctrinal Concepts Registered by DL-036 (R4)

The following nine canonical doctrinal concepts are registered using existing Doctrine sources only. Status: Canonical. Each entry cites the existing doctrinal source. Plane assignments noted.

| Concept | Status | Doctrinal Source | Plane |
|---|---|---|---|
| Dynamic Systems Orientation | Canonical | `01_governance/doctrine/01_core_philosophical_doctrine.md` (Dynamic Systems Orientation section) | Reality / Epistemic |
| Constitutional Principle (Design Tradeoff Test) | Canonical | `01_governance/doctrine/01_core_philosophical_doctrine.md` (closing section) | Cross-plane (foundational test) |
| Epistemic Governance | Canonical | `01_governance/doctrine/02_organizational_cognition_model.md` (Governed Organizational Cognition section) | Governance / Cognition |
| Flawed Intended Reality Handling | Canonical | `01_governance/doctrine/07_governance_policy_doctrine.md` (Flawed Intended Reality Handling section) | Governance / Reality |
| Stability vs Movement | Canonical | `01_governance/doctrine/06_confidence_understanding_model.md` (Stability vs Movement section) | Emotional and Visibility |
| Shared Cognition Principle | Canonical | `01_governance/doctrine/08_collaboration_shared_cognition.md` (Shared Cognition Principle section) | Cognition |
| Narrative Views | Canonical | `01_governance/doctrine/08_collaboration_shared_cognition.md` (Narrative Views section) | Workspace / Collaboration |
| Freemium Doctrine | Canonical | `01_governance/doctrine/09_plg_product_evolution_strategy.md` (Freemium Doctrine section) | Cognition and Progression |
| Strategic UX Doctrine | Canonical | `01_governance/doctrine/11_emotional_interaction_philosophy.md` (Strategic UX Doctrine section) | Emotional and Visibility |

---

## Deprecated Predecessor — Emotional and Visibility (per DL-036 R5)

| Predecessor Name | Status | Canonical Name | Ratifying Decision | Historical Source |
|---|---|---|---|---|
| Intelligence Visibility Doctrine | Duplicate | Progressive Visibility | DL-016 (Stated, grandfathered per DL-032; substantively aligned with Article 25) per DL-036 Clarification #4 | `01_governance/doctrine/11_emotional_interaction_philosophy.md` (Intelligence Visibility Doctrine section) |

---

## Concepts Used But Not Registered

The following are referenced in canonical or specification material without ontological placement. Each requires governance review before registration.

- Working Memory (`03_implementation_specs/13_implementation_backlog.md`)
- Outcome Map (`03_implementation_specs/13_implementation_backlog.md`)
- Alternative Outcome Models (`03_implementation_specs/13_implementation_backlog.md`)
- Assumption Expiration (`01_governance/doctrine/07_governance_policy_doctrine.md`)
- Policy DSL / Policy Grammar (implied)
- Scenario / Simulation (`03_implementation_specs/03_outcome_space_workspace_wireframes.md`; `03_implementation_specs/07_workflow_specifications.md`)
- Shared View (`03_implementation_specs/05_component_system_specification.md`; `03_implementation_specs/10_collaboration_sharing_logic.md`)
- Project MRI subsystem internals (`04_project_mri/`)

---

## Inventory I-A — Unanchored Implementation Concepts (per DL-036 R7; placed inline per Clarification #5)

The following implementation-layer concepts appear in `03_implementation_specs/` without doctrinal or constitutional anchoring. This inventory is an observation output, not a disposition. Items feed RB-004 (Doctrine Stubs) and related backlog items (RB-012, RB-013, RB-014, RB-015, RB-016, RB-017, RB-018) as input. The inventory is open and updateable; future Decisions may add or remove items via clerical changelog entries.

1. **Epistemic Label additional types** (Unknown, Provisional, Weakly Supported, Validated) — `03_implementation_specs/05_component_system_specification.md` Section 3. Reserved for **RB-007**. See DL-036 Clarification #6 for relationship to R6 disambiguation.
2. **Intelligence Diagnostic severity tiers** (Info, Suggestion, Moderate, Critical, Governance Blocker) — `03_implementation_specs/05_component_system_specification.md` Section 4. Doctrinal anchor undefined.
3. **OSLO Companion Panel modes** (specific 8-mode set) — `03_implementation_specs/05_component_system_specification.md` Section 7. Doctrinal anchor undefined.
4. **Override State Model** (8 states) — `03_implementation_specs/08_state_logic_state_machines.md`. Reserved for **RB-009**.
5. **Override Severity Tiers** (4 tiers: Low, Moderate, High, Governance Critical) — `03_implementation_specs/11_governance_override_logic.md`. Reserved for **RB-009**.
6. **Lifecycle State Models** (Outcome Space State, Attention Item State, Recommendation State, Shared View State, OSLO Companion State) — `03_implementation_specs/08_state_logic_state_machines.md`. Doctrinal anchors undefined.
7. **Collaboration Role Model** (6 roles: Viewer, Commenter, Clarifier, Approver, Governance Reviewer, Owner) — `03_implementation_specs/10_collaboration_sharing_logic.md`. Reserved for **RB-012**.
8. **Tier Types** (Freemium, Professional, Team/Business, Enterprise) — `03_implementation_specs/12_freemium_tier_behavior_logic.md`. Doctrinal anchor undefined.
9. **Cursor-like AI-native IDE identity claim** — `03_implementation_specs/00_index.md` Primary UI Model section. Doctrinal anchor undefined.
10. **Compound Integrity States** (e.g., "Clarified but Fragile") — `03_implementation_specs/02_plg_60_second_flow_wireframes.md`. Reserved for **RB-006**.
11. **Fast Pass / Deep Refinement / Activation Moment** — `03_implementation_specs/02_plg_60_second_flow_wireframes.md`. Doctrinal anchor undefined.
12. **Working Memory / Outcome Map / Alternative Outcome Models / Continuous Monitoring** — `03_implementation_specs/13_implementation_backlog.md`, `03_implementation_specs/12_freemium_tier_behavior_logic.md`. Doctrinal anchors undefined. Reserved for **RB-004**.
13. **Engineering core objects** (OutcomeSpace, Artifact, UnderstandingSnapshot, ConfidenceModel, ConfidenceEvent, AttentionItem, Recommendation, EvidenceSource, EpistemicObject, GovernancePolicy, OverrideRecord, SharedView, Simulation, TimelineEvent) — `03_implementation_specs/13_implementation_backlog.md` Engineering Notes. Doctrinal anchors undefined.

---

## Inventory I-B — Registry Entries Lacking Authoritative Definitions (per DL-036 R7; placed inline per Clarification #5)

The following registry entries operate without a doctrinally grounded authoritative definition. This inventory is an observation output, not a disposition. Items feed RB-013, RB-014, RB-015 and (for Outcome Space) RB-004 as input. The inventory is open and updateable.

| Concept | Registry Status | Definition Status | Backlog Destination |
|---|---|---|---|
| Artifact | Proposed | No defining statement in any source | RB-014 |
| Attention Queue | Proposed | Two conflicting framings (doctrinal "persistent operational intelligence surface" vs spec "queue sorted by outcome impact") | RB-013 |
| Project MRI | Canonical (R1, DL-061) | Per-project understanding surface (Master Spec §7); portfolio scope renamed Portfolio Integrity Scan, deferred (DL-034) | RB-015 resolved for R1 by DL-061 |
| Outcome Space | Canonical (Constitutional) | Defined in Article 13 only; lacks doctrinal anchor | RB-004 (general doctrine stubs) |

---

## Governance Notes

1. This registry is operative under DL-036. Status taxonomy and surface authority rule are declared in the Status section (cross-references `canonical_definitions.md`).
2. Legacy "Established" entries have been migrated to "Canonical"; legacy "Established (split source)" entries have been migrated to "Conflicting" (with one exception per DL-036 Clarification #7).
3. New canonical entities must enter through the Content tier (Doctrine or Constitution) first via Proposal-Review-Decision, then propagate here as clerical updates.
4. Inventories I-A and I-B are open observation outputs; clerical updates may add or remove items, recorded in the changelog.
