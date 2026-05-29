# Ontology Registry

## Status

**Draft — Initial Compilation; Governance-Tier Orientation Surface**

Under the doctrine-centered repository architecture (per Proposal 000 disposition, DL-033), this file sits in the **Governance tier** as an orientation registry. It is not part of the Content tier and does not carry doctrinal or constitutional authority. Canonical authority over ontology entities resides in their Content-tier source files.

This file enumerates the major ontology entities, their relationships, and their source references as currently present in the repository. It does not introduce new entities. Where multiple sources disagree, the disagreement is recorded rather than resolved. Entries are organized by ontological plane.

All entries reference only existing repository content. Ratification rules for promoting entries are pending (see `revision_backlog.md`, RB-005).

---

## Reality Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Intended Reality | Established | `01_doctrine_ontology/04_outcome_integrity_framework.md` |
| Current Reality | Established | `01_doctrine_ontology/04_outcome_integrity_framework.md` |
| Integrity Gap | Established | `01_doctrine_ontology/04_outcome_integrity_framework.md` |
| Outcome Integrity | Established | `01_doctrine_ontology/01_core_philosophical_doctrine.md`; `02_ux_constitution/01_foundational_constitutional_doctrine.md` Article 3 |
| Outcome Integrity States | Established (split source) | `01_doctrine_ontology/04_outcome_integrity_framework.md`; `02_ux_constitution/06_confidence_integrity_constitution.md` Article 33; `03_implementation_specs/08_state_logic_state_machines.md` |

### Relationships

- *Outcome Integrity* = coherence(Intended Reality, Current Reality).
- *Integrity Gap* = divergence(Intended Reality, Current Reality).
- *Outcome Integrity States* are described as conditions over the Reality plane, not workflow phases.

---

## Epistemic Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Dynamic Epistemic Synthesis | Established | `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 7 |
| Fact | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Inference | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Assumption | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Recommendation | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Conflict | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Ambiguity | Established | `01_doctrine_ontology/03_epistemic_system_model.md` |
| Understanding Boundary | Established | `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 9 |
| Progressive Epistemic Depth | Established | `02_ux_constitution/02_epistemic_constitution.md` Article 10 |
| Organizational Epistemic Memory | Established | `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 11 |
| Understanding Evolution | Established | `01_doctrine_ontology/06_confidence_understanding_model.md` |

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
| Confidence | Established | `01_doctrine_ontology/06_confidence_understanding_model.md`; `02_ux_constitution/06_confidence_integrity_constitution.md` Article 30 |
| Confidence Maturity | Established | `02_ux_constitution/06_confidence_integrity_constitution.md` Article 32 |
| Confidence Drivers | Established (split source) | `01_doctrine_ontology/06_confidence_understanding_model.md`; `03_implementation_specs/09_confidence_integrity_logic.md` |
| Confidence Maturity Progression | Established | Same as above; `03_implementation_specs/08_state_logic_state_machines.md` |

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
| Governance | Established | `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 19 |
| Outcome Integrity Policy | Established | `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 20 |
| Human Override | Established | `02_ux_constitution/04_governance_constitution.md` Article 21 |
| Governance Escalation | Established | `02_ux_constitution/04_governance_constitution.md` Article 22 |
| Disagreement Handling | Established | `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 23 |
| Intended Reality Governance | Established | `02_ux_constitution/04_governance_constitution.md` Article 24 |
| Override State Model | Established (split source) | `03_implementation_specs/08_state_logic_state_machines.md`; `03_implementation_specs/11_governance_override_logic.md` |
| Collaboration Role Model | Proposed | `03_implementation_specs/10_collaboration_sharing_logic.md` |
| Agent Governance | Proposed | `01_doctrine_ontology/02_organizational_cognition_model.md`; `03_implementation_specs/12_freemium_tier_behavior_logic.md` |

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

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Organizational Cognition Arc | Established (split source) | `01_doctrine_ontology/02_organizational_cognition_model.md`; `02_ux_constitution/08_product_evolution_constitution.md` Articles 40 and 44 |
| Trust Evolution | Established | `01_doctrine_ontology/09_plg_product_evolution_strategy.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 41 |
| Execution Maturity Phases | Established | `01_doctrine_ontology/10_execution_orchestration_maturity.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 43 |
| Product Evolution Stages | Established | `01_doctrine_ontology/09_plg_product_evolution_strategy.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 40 |
| Portfolio Cognition | Proposed | `01_doctrine_ontology/10_execution_orchestration_maturity.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 44 |

### Known Conflict

The repository contains at least five overlapping progressions across this plane, with inconsistent stage counts (four versus five) and inconsistent stage labels. No mapping among them exists. Reconciliation pending — see `revision_backlog.md`, RB-003.

---

## Workspace and Surface Plane

### Entities

| Entity | Status | Primary Source |
|---|---|---|
| Outcome Space | Established | `02_ux_constitution/03_workspace_constitution.md` Article 13; `02_ux_constitution/10_canonical_definitions.md` |
| Understanding (workspace center) | Established | `02_ux_constitution/03_workspace_constitution.md` Article 12 |
| What OSLO Understands | Established | `02_ux_constitution/03_workspace_constitution.md` Article 14 |
| Artifact | Proposed | `02_ux_constitution/03_workspace_constitution.md` Article 15 |
| Artifact Domains | Established | Intent, Context, Execution, Schedule, Resources — `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; Article 15 |
| Persistent Confidence Shell | Established | `02_ux_constitution/03_workspace_constitution.md` Article 17 |
| Companion Intelligence Panel | Established | `02_ux_constitution/03_workspace_constitution.md` Article 18 |
| Attention Queue | Proposed | `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; `03_implementation_specs/03_outcome_space_workspace_wireframes.md` |
| Adaptive Workspace | Established | `02_ux_constitution/03_workspace_constitution.md` Article 16 |
| Project MRI | Proposed | `repository_manifest.md`; `03_implementation_specs/02_plg_60_second_flow_wireframes.md` |

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
| Calm Strategic Augmentation | Established | `02_ux_constitution/09_emotional_interaction_constitution.md` Article 45 |
| Progressive Visibility | Established | `02_ux_constitution/05_intelligence_visibility_constitution.md` Article 25 |
| Workspace-Native Intelligence | Established | `02_ux_constitution/05_intelligence_visibility_constitution.md` Article 26 |
| Explainability | Established | `02_ux_constitution/05_intelligence_visibility_constitution.md` Article 28 |
| Consequence Illumination | Established | `02_ux_constitution/05_intelligence_visibility_constitution.md` Article 29 |

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

## Concepts Used But Not Registered

The following are referenced in canonical or specification material without ontological placement. Each requires governance review before registration.

- Working Memory (`03_implementation_specs/13_implementation_backlog.md`)
- Outcome Map (`03_implementation_specs/13_implementation_backlog.md`)
- Alternative Outcome Models (`03_implementation_specs/13_implementation_backlog.md`)
- Assumption Expiration (`01_doctrine_ontology/07_governance_policy_doctrine.md`)
- Policy DSL / Policy Grammar (implied)
- Scenario / Simulation (`03_implementation_specs/03_outcome_space_workspace_wireframes.md`; `03_implementation_specs/07_workflow_specifications.md`)
- Shared View (`03_implementation_specs/05_component_system_specification.md`; `03_implementation_specs/10_collaboration_sharing_logic.md`)
- Project MRI subsystem internals (`04_project_mri/`)

---

## Governance Notes

1. This registry is a draft. Entries are not ratified.
2. Entries marked "split source" require reconciliation through the revision backlog.
3. Entries marked "Proposed" require a defining statement in `canonical_definitions.md` before promotion.
4. Adding an entity to this registry must be accompanied by a `decision_log.md` entry recording the ratification.
