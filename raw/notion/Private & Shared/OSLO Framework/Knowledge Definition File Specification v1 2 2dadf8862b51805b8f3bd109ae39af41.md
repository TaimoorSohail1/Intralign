# Knowledge Definition File Specification v1.2

*(adds explicit support for workflow artifact containers)*

---

**System:** OSLO / Intralign

**Layer:** Knowledge

**Spec Type:** Normative (schema + integrity contracts)

**Status:** Canonical

**Audience:** Engineering, Data, Platform, QA

---

## **1. Purpose**

This specification defines the **externalized definition files** that govern the **Knowledge Layer**, including:

- canonical entity definitions
- canonical relationship definitions
- integrity constraints
- versioning and mutation rules

These files define **what may exist** and **how it may be stored**.

They do **not** define evaluation, inference, scoring, or behavior.

---

## **2. Authority & Scope**

The Knowledge Layer is the **system of record**.

Definition files:

- are **authoritative**
- are enforced at **write time**
- apply to **all layers downstream**
- are **immutable once published**

Anything not defined here is **not canonical**.

---

## **3. File Taxonomy (Canonical)**

```
/knowledge/
  /entities/          # canonical objects (including artifact containers)
  /relationships/     # allowed edges
  /constraints/       # integrity rules
  /versioning/        # mutation + history rules
```

### **File formats**

- YAML preferred (.yaml)
- JSON allowed (.json)
- No executable logic
- No embedded scripts
- No evaluation expressions

---

## **4. Global File Requirements**

### **4.1 Required Header Metadata (All Files)**

```
meta:
  schema: oslo.knowledge.<category>.v1
  id: <string>                   # stable identifier
  version: <semver>              # immutable once published
  status: DRAFT | CANONICAL | DEPRECATED
  created_at: <ISO-8601>
  owner: <team-or-role>
  description: <string>
  compatibility:
    min_engine_version: <semver>
    max_engine_version: <semver|null>
```

### **4.2 Immutability Rules**

- CANONICAL versions are immutable
- Changes require publishing a **new version**
- Old versions remain valid for replay and audit

---

## **5. Entity Definition Files (/entities/*.yaml)**

### **5.1 Purpose**

Define **canonical objects** stored in the Knowledge Layer.

### **5.2 Entity Schema**

```
meta: { ... }

entity:
  name: <EntityName>
  description: <string>
  versioning: APPEND_ONLY
  identifiers:
    primary_key: <field_name>
    external_keys: []
  fields:
    - name: <field>
      type: <type>
      required: <bool>
      immutable: <bool>

  prohibited_fields:
    - score
    - severity
    - confidence
```

### **5.3 Entity Rules**

- Entities **must not contain inferred or synthetic fields**
- All required fields must be present at write time
- Versioning behavior must be explicit

---

## **5.4 Workflow Artifact Containers (Explicitly Canonical) ✅**

## **(New in v1.2)**

The Knowledge Layer **explicitly supports workflow artifact containers** as canonical entities.

Artifact containers are:

- **first-class, addressable** objects (have IDs)
- **append-only / supersedable**
- **project-scoped**
- **non-evaluative**
- **purely structural grouping roots**

Artifact containers:

- **do not duplicate** primitive fields (e.g., Outcome fields remain on Outcome)
- **do not contain** scoring, confidence, or inference outputs
- **do not imply** adequacy or quality

### **Canonical artifact container entity types**

- IntentArtifact
- ContextArtifact
- ScopeArtifact
- RequirementsArtifact
- WBSArtifact
- ResourcePlanArtifact
- ScheduleDefinitionArtifact

### **Required relationship for composition**

Artifact containers are composed via:

- contains relationship
    
    (ArtifactContainer → CanonicalEntity) with optional role: primary|supporting
    

Artifact composition **must be explicit** (no implicit containment).

---

## **6. Relationship Definition Files (/relationships/*.yaml)**

### **6.1 Purpose**

Define **allowed canonical relationships** between entities.

### **6.2 Relationship Schema**

```
meta: { ... }

relationship:
  name: <relationship_name>
  description: <string>
  direction: directed | undirected
  source_types: [<EntityType>...]
  target_types: [<EntityType>...]
  cardinality:
    source: one | many
    target: one | many
  properties:
    - name: <prop_name>
      type: <type>
      required: <bool>
```

### **6.3 Relationship Rules**

- All edges must match allowed source → target types
- Cardinality must be enforced
- Relationships do not imply meaning or severity

---

## **7. Integrity Constraint Files (/constraints/*.yaml)**

### **7.1 Purpose**

Enforce **structural correctness** of canonical data.

### **7.2 Constraint Rules**

- Constraints are enforced at write time
- Violations reject the mutation
- Constraints do **not** emit issues or warnings (Reasoning does that)

---

## **8. Versioning & Mutation Rules (/versioning/*.yaml)**

### **8.1 Purpose**

Define **how canonical data evolves**.

### **8.2 Versioning Rules**

- No in-place mutation of canonical records
- All updates create new versions
- Superseded records remain queryable

---

## **9. Execution & Proposal Stubs (Future-Safe)**

The Knowledge Layer may store, but never execute:

- ActionProposal
- AuthorizationEvent
- ExecutionFact (read-only ingestion)

---

## **10. Explicit Non-Responsibilities**

Knowledge Definition files must **never** include:

- inference logic
- evaluation criteria
- scoring or thresholds
- severity definitions
- signals
- recommendations

Those belong to **Reasoning or Judgment**.

---

## **11. Validation & Compliance**

A Knowledge Definition file set is compliant if:

- All schemas validate
- No inferred fields exist
- Versioning rules are explicit
- Constraints are enforceable at write time
- Workflow artifact containers (if used) only compose via contains
- No overlap with Reasoning responsibilities

---

## **Canonical Invariant**

> The Knowledge Layer defines what is allowed to exist.
> 

> It does not decide what that data means.
> 

---

## **End of Specification**

---

## Bundles

[**/knowledge/index.yaml**](Knowledge%20Definition%20File%20Specification%20v1%202/knowledge%20index%20yaml%202dbdf8862b518055b857f1ae8f7339ce.md)

[**/knowledge/entities/**](Knowledge%20Definition%20File%20Specification%20v1%202/knowledge%20entities%202dbdf8862b5180708ce3d0a113343400.md)

[
 /knowledge/relationships
](Knowledge%20Definition%20File%20Specification%20v1%202/knowledge%20relationships%202dbdf8862b51808ebe06c8c85d2c6b23.md)

[**/knowledge/constraints/**](Knowledge%20Definition%20File%20Specification%20v1%202/knowledge%20constraints%202dbdf8862b518017a95df78b6c0c421e.md)

[**/knowledge/versioning/**](Knowledge%20Definition%20File%20Specification%20v1%202/knowledge%20versioning%202dbdf8862b51804e8d86d466a3d3ac6d.md)