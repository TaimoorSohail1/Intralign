# /knowledge/constraints/

# **— Canonical Bundle (vNext)**

---

## **project_minimums.yaml**

## 

## **(updated)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.project_minimums
  version: 1.1.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Project-level structural minimums
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: REQUIRED.OUTCOME.MIN_COUNT
    description: Every project must define at least one Outcome
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: Outcome
        min: 1
```

---

## **relationship_integrity.yaml**

## 

## **(unchanged)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.relationship_integrity
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Structural integrity rules for canonical relationships
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: NO.DANGLING.RELATIONSHIPS
    description: Relationships must reference existing canonical entities
    applies_to:
      relationship: "*"
    rule:
      type: referential_integrity
      parameters:
        source_must_exist: true
        target_must_exist: true

  - id: NO.CROSS_PROJECT.EDGES
    description: Source and target of a relationship must belong to the same project
    applies_to:
      relationship: "*"
    rule:
      type: same_project_scope
      parameters: {}

  - id: REL.ENDPOINT.TYPE_ENFORCEMENT
    description: Relationship endpoints must match the allowed source_types/target_types for that relationship
    applies_to:
      relationship: "*"
    rule:
      type: relationship_endpoint_types_allowed
      parameters: {}
```

---

## **prohibited_fields_global.yaml**

## 

## **(unchanged)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.prohibited_fields_global
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Prevent persistence of non-canonical evaluation fields across all entities
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: NO.EVALUATION.FIELDS.IN.ENTITIES
    description: Canonical entities must not persist evaluation artifacts (score/severity/confidence/health)
    applies_to:
      entity: "*"
    rule:
      type: prohibited_fields_absent
      parameters:
        fields: [score, severity, confidence, health]
```

---

## **versioning_integrity.yaml**

## 

## **(unchanged)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.versioning_integrity
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Structural versioning integrity constraints (append-only supersession model)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: NO.IN_PLACE.MUTATION
    description: Canonical entities must not be overwritten in place; updates must create a new version
    applies_to:
      entity: "*"
    rule:
      type: append_only_enforced
      parameters: {}

  - id: NO.IN_PLACE.RELATIONSHIP.MUTATION
    description: Canonical relationships must not be overwritten in place; updates must create a new version
    applies_to:
      relationship: "*"
    rule:
      type: append_only_enforced
      parameters: {}
```

---

---

## **unique_active_versions.yaml**

## 

## **(new)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.unique_active_versions
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Enforces a single active (non-superseded) version per canonical entity identifier per project
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: UNIQUE.ACTIVE.ENTITY.VERSION
    description: Only one active version may exist per entity primary key within a project
    applies_to:
      entity: "*"
    rule:
      type: unique_active_version
      parameters:
        scope: project
```

---

## **edge_uniqueness.yaml**

## 

## **(new)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.edge_uniqueness
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Prevents duplicate active relationships of the same type between the same endpoints
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: UNIQUE.ACTIVE.RELATIONSHIP
    description: Prevent duplicate active relationship edges for identical (relationship, source, target) within a project
    applies_to:
      relationship: "*"
    rule:
      type: unique_active_edge
      parameters:
        scope: project
        key_fields: [relationship_name, source_id, target_id]
```

---

## **contains_domain_scoping.yaml**

## 

## **(new, important now that you added containers)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.contains_domain_scoping
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Enforces artifact-to-entity domain scoping for the contains relationship
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: CONTAINS.DOMAIN.SCOPE.INTENT
    description: IntentArtifact may only contain intent-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: IntentArtifact
        allowed_target_types:
          - Goal
          - Objective
          - Outcome
          - SuccessCriterion
          - IntentOwnership
          - TradeoffPosture
          - IntentNarrative

  - id: CONTAINS.DOMAIN.SCOPE.CONTEXT
    description: ContextArtifact may only contain context-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: ContextArtifact
        allowed_target_types:
          - ContextSignal
          - Assumption
          - Constraint

  - id: CONTAINS.DOMAIN.SCOPE.SCOPE
    description: ScopeArtifact may only contain scope-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: ScopeArtifact
        allowed_target_types:
          - ScopeBoundary
          - Deliverable

  - id: CONTAINS.DOMAIN.SCOPE.REQUIREMENTS
    description: RequirementsArtifact may only contain requirements-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: RequirementsArtifact
        allowed_target_types:
          - Requirement

  - id: CONTAINS.DOMAIN.SCOPE.WBS
    description: WBSArtifact may only contain WBS-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: WBSArtifact
        allowed_target_types:
          - WorkElement

  - id: CONTAINS.DOMAIN.SCOPE.RESOURCE_PLAN
    description: ResourcePlanArtifact may only contain resource-plan-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: ResourcePlanArtifact
        allowed_target_types:
          - Resource
          - ResourceAllocation

  - id: CONTAINS.DOMAIN.SCOPE.SCHEDULE
    description: ScheduleDefinitionArtifact may only contain schedule-related canonical entities
    applies_to:
      relationship: contains
    rule:
      type: allowed_targets_by_source_type
      parameters:
        source_type: ScheduleDefinitionArtifact
        allowed_target_types:
          - ScheduleElement
```

---

## **acyclic_wbs.yaml**

## 

## **(new)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.acyclic_wbs
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Prevents cycles in work breakdown structures
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: NO.CYCLES.WBS
    description: WorkElement decomposition must be acyclic
    applies_to:
      relationship: decomposes_into
    rule:
      type: acyclic_graph
      parameters: {}
```

---

## **schedule_date_ordering.yaml**

## 

## **(new)**

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.schedule_date_ordering
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Ensures valid ordering of schedule dates when both are present
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: SCHEDULE.DATE.ORDER
    description: If both start_date and end_date exist, start_date must be on or before end_date
    applies_to:
      entity: ScheduleElement
    rule:
      type: date_order
      parameters:
        start_field: start_date
        end_field: end_date
```

---

## **Optional: artifact_minimums.yaml**

## 

## **(not required unless you want artifacts mandatory)**

If you want every project to always have the standard artifact containers, publish this too:

```
meta:
  schema: oslo.knowledge.constraints.v1
  id: constraints.artifact_minimums
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Ensures standard workflow artifact containers exist per project (optional)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

constraints:
  - id: REQUIRED.ARTIFACT.INTENT
    description: Every project must have an IntentArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: IntentArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.CONTEXT
    description: Every project must have a ContextArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: ContextArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.SCOPE
    description: Every project must have a ScopeArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: ScopeArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.REQUIREMENTS
    description: Every project must have a RequirementsArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: RequirementsArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.WBS
    description: Every project must have a WBSArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: WBSArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.RESOURCE_PLAN
    description: Every project must have a ResourcePlanArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: ResourcePlanArtifact
        min: 1

  - id: REQUIRED.ARTIFACT.SCHEDULE
    description: Every project must have a ScheduleDefinitionArtifact container
    applies_to:
      entity: Project
    rule:
      type: minimum_count
      parameters:
        scope: project
        entity: ScheduleDefinitionArtifact
        min: 1
```

---

## **Notes on intent and scope (still true)**

- No success-criteria adequacy rules
- No alignment quality rules
- No confidence penalties
- No scoring thresholds
- Nothing evaluative

---

If you want, next I can **update /knowledge/index.yaml** so it lists these new constraint files explicitly (so CI can validate the full bundle).