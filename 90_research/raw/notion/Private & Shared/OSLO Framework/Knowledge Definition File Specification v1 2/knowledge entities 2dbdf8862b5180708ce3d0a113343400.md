# /knowledge/entities/

# **— Artifact Container Additions (Canonical)**

> Use these as
> 
> 
> **new files**
> 

---

## **intent_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.intent_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for intent-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: IntentArtifact
  description: Grouping root for project intent
  versioning: APPEND_ONLY
  identifiers:
    primary_key: intent_artifact_id
    external_keys: []

  fields:
    - name: intent_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **context_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.context_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for context-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: ContextArtifact
  description: Grouping root for project context
  versioning: APPEND_ONLY
  identifiers:
    primary_key: context_artifact_id
    external_keys: []

  fields:
    - name: context_artifact_id
      type: uuid
      required: true
     immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

> Fix:
> 

```
    - name: context_artifact_id
      type: uuid
      required: true
      immutable: true
```

---

## **scope_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.scope_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for scope-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: ScopeArtifact
  description: Grouping root for project scope
  versioning: APPEND_ONLY
  identifiers:
    primary_key: scope_artifact_id
    external_keys: []

  fields:
    - name: scope_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **requirements_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.requirements_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for requirements-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: RequirementsArtifact
  description: Grouping root for project requirements
  versioning: APPEND_ONLY
  identifiers:
    primary_key: requirements_artifact_id
    external_keys: []

  fields:
    - name: requirements_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **wbs_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.wbs_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for WBS-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: WBSArtifact
  description: Grouping root for work breakdown structure
  versioning: APPEND_ONLY
  identifiers:
    primary_key: wbs_artifact_id
    external_keys: []

  fields:
    - name: wbs_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **resource_plan_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.resource_plan_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for resource-plan-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: ResourcePlanArtifact
  description: Grouping root for resource planning intent
  versioning: APPEND_ONLY
  identifiers:
    primary_key: resource_plan_artifact_id
    external_keys: []

  fields:
    - name: resource_plan_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **schedule_definition_artifact.yaml**

```
meta:
  schema: oslo.knowledge.entity.v1
  id: entity.schedule_definition_artifact
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Container for schedule-definition-related canonical entities (workflow artifact root)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

entity:
  name: ScheduleDefinitionArtifact
  description: Grouping root for schedule definition (phases/milestones)
  versioning: APPEND_ONLY
  identifiers:
    primary_key: schedule_definition_artifact_id
    external_keys: []

  fields:
    - name: schedule_definition_artifact_id
      type: uuid
      required: true
      immutable: true

    - name: project_id
      type: uuid
      required: true
      immutable: true

    - name: label
      type: string
      required: false
      immutable: false

  prohibited_fields:
    - score
    - severity
    - confidence
    - health
```

---

## **Required follow-up (so these containers are actually usable)**

To connect containers to their constituent entities, you’ll want **one canonical relationship** (if you haven’t published it yet):

- /knowledge/relationships/contains.yaml (Artifact → Entity)

And ideally a constraint:

- “each artifact container must belong to a project” (already via project_id required)

---

If you want, I’ll publish next:

1. /knowledge/relationships/contains.yaml (plus optional contains.role property like primary|supporting)
2. /knowledge/index.yaml update to include these new entity files (so CI can validate completeness)