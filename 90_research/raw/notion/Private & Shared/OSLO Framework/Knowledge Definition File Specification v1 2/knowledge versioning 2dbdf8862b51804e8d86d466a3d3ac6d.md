# /knowledge/versioning/

---

## **— Canonical Bundle (v1.1)**

---

## **supersession.yaml**

*(global model + enforcement prerequisites)*

> No change required
> 

```
meta:
  schema: oslo.knowledge.versioning.v1
  id: versioning.supersession
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Global append-only supersession model for canonical knowledge
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

supersession:
  model: append_only
  preserves_history: true
  requires:
    - governance_authorization
```

---

## **entity_mutation_rules.yaml**

*(allowed operations per entity — UPDATED)*

**Changes**

- Added **all workflow artifact containers**
- No behavioral changes to existing entities
- Version bumped → **1.1.0**

```
meta:
  schema: oslo.knowledge.versioning.v1
  id: versioning.entity_mutation_rules
  version: 1.1.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Allowed mutation operations for canonical entities (append-only)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

mutation_rules:

  # --- Project root ---
  - entity: Project
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  # --- Workflow artifact containers ---
  - entity: IntentArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ContextArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ScopeArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: RequirementsArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: WBSArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ResourcePlanArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ScheduleDefinitionArtifact
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  # --- Intent primitives ---
  - entity: Goal
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Objective
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Outcome
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: SuccessCriterion
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: IntentOwnership
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: TradeoffPosture
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: IntentNarrative
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  # --- Scope / execution structure ---
  - entity: Requirement
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Deliverable
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: WorkElement
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Resource
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ResourceAllocation
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ScheduleElement
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ScopeBoundary
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: ContextSignal
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Assumption
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: Constraint
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  # --- Future-safe / governance ---
  - entity: ActionProposal
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  - entity: AuthorizationEvent
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]

  # --- Read-only ingestion ---
  - entity: ExecutionFact
    allowed_operations: [create]
    prohibited_operations: [delete, overwrite, supersede]
```

---

## **relationship_mutation_rules.yaml**

*(allowed operations for relationship records)*

> No change required
> 

> This is already consistent with your append-only + supersession model.
> 

```
meta:
  schema: oslo.knowledge.versioning.v1
  id: versioning.relationship_mutation_rules
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Allowed mutation operations for canonical relationships (append-only)
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

mutation_rules:
  - relationship: "*"
    allowed_operations: [create, supersede]
    prohibited_operations: [delete, overwrite]
```

---

## **supersession_requirements.yaml**

*(fine-grained gating; still structural)*

> No change required
> 

```
meta:
  schema: oslo.knowledge.versioning.v1
  id: versioning.supersession_requirements
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Requirements that must be met to supersede canonical records
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null

supersession_requirements:
  - applies_to:
      entity: "*"
    requires:
      - governance_authorization

  - applies_to:
      relationship: "*"
    requires:
      - governance_authorization
```

---

## **Canonical Status Check**

✔ Artifact containers now have explicit mutation rules

✔ Append-only invariant preserved

✔ ExecutionFact remains create-only

✔ No reasoning, scoring, or workflow leakage

✔ Fully backward-compatible (v1.0 → v1.1)

---

### **What’s left (optional but clean):**

- /knowledge/index.yaml (manifest for CI / completeness validation)
- /knowledge/relationships/produces.yaml (if you want explicit artifact → deliverable semantics)
- A short **“Knowledge ↔ Workflow boundary”** note for engineers onboarding

If you want, say which one to publish next.