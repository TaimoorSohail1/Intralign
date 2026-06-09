# /knowledge/relationships

```jsx
meta:
  schema: oslo.knowledge.relationship.v1
  id: rel.contains
  version: 1.1.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Artifact container groups canonical entities as part of a workflow artifact (structural only)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

relationship:
  name: contains
  description: Artifact contains (groups) canonical entities to form an artifact view
  direction: directed
  source_types:
    - IntentArtifact
    - ContextArtifact
    - ScopeArtifact
    - RequirementsArtifact
    - WBSArtifact
    - ResourcePlanArtifact
    - ScheduleDefinitionArtifact

  target_types:
    - Goal
    - Objective
    - Outcome
    - SuccessCriterion
    - IntentOwnership
    - TradeoffPosture
    - IntentNarrative
    - ContextSignal
    - Assumption
    - Constraint
    - ScopeBoundary
    - Requirement
    - Deliverable
    - WorkElement
    - Resource
    - ResourceAllocation
    - ScheduleElement

  cardinality:
    source: one
    target: many

  properties:
    - name: role
      type: enum
      values: [primary, supporting]
      required: false

  prohibited_properties:
    - score
    - severity
    - confidence
    - health
```