# /knowledge/index.yaml

**— Canonical Knowledge Registry**

```
meta:
  schema: oslo.knowledge.index.v1
  id: knowledge.index
  version: 1.0.0
  status: CANONICAL
  created_at: 2025-12-31
  owner: platform
  description: Canonical registry of all Knowledge Layer definition files
  compatibility:
    min_engine_version: 1.0.0
    max_engine_version: null
```

---

## **entities**

```
entities:

  # --- Project root ---
  - project.yaml

  # --- Artifact containers ---
  - intent_artifact.yaml
  - context_artifact.yaml
  - scope_artifact.yaml
  - requirements_artifact.yaml
  - wbs_artifact.yaml
  - resource_plan_artifact.yaml
  - schedule_definition_artifact.yaml

  # --- Intent primitives ---
  - goal.yaml
  - objective.yaml
  - outcome.yaml
  - success_criterion.yaml
  - intent_ownership.yaml
  - tradeoff_posture.yaml
  - intent_narrative.yaml

  # --- Scope / execution structure ---
  - requirement.yaml
  - deliverable.yaml
  - work_element.yaml
  - resource.yaml
  - resource_allocation.yaml
  - schedule_element.yaml
  - scope_boundary.yaml

  # --- Context & constraints ---
  - context_signal.yaml
  - assumption.yaml
  - constraint.yaml

  # --- Future-safe / governance ---
  - action_proposal.yaml
  - authorization_event.yaml
  - execution_fact.yaml
```

---

## **relationships**

```
relationships:
  - contains.yaml
  - supports.yaml
  - aligns_to.yaml
  - decomposes_into.yaml
  - allocates_to.yaml
  - scheduled_within.yaml
  - defines_success_criteria.yaml
  - owned_by.yaml
```

---

## **constraints**

```
constraints:
  - project_minimums.yaml
  - relationship_integrity.yaml
  - prohibited_fields_global.yaml
  - versioning_integrity.yaml
```

---

## **versioning**

```
versioning:
  - supersession.yaml
  - entity_mutation_rules.yaml
  - relationship_mutation_rules.yaml
  - supersession_requirements.yaml
```

---

## **index_invariants**

```
index_invariants:
  - Every file listed here must exist and validate
  - No canonical file may exist outside this index
  - All referenced entity and relationship names must match definitions
  - Version compatibility must be satisfied at load time
```

---

## **Canonical Notes**

- This file is the **single source of truth** for Knowledge Layer completeness
- CI / boot-time validation should:
    - load this index
    - validate schemas
    - confirm cross-file referential integrity
- Adding a new canonical definition **requires updating this file**
- Removing a file requires **deprecation, not deletion**

---

## **Canonical Close**

> If it is not indexed here, it is not canonical knowledge.
> 

---

If you want next, the natural close-out steps are:

- publish the remaining **artifact container YAMLs** (Context, Scope, etc.)
- add a **CI validation checklist** mapped to this index
- freeze **Knowledge Layer v1.0** as a tagged release