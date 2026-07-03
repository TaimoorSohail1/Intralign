# OSLO Reasoning Layer Data Model v1.0

---

## **Design goals**

- **Never stores canonical truth** (only references canonical IDs + captured snapshots)
- Supports **Canonical vs Hypothetical** contexts
- Supports **Derived vs SyntheticPlaceholder** values
- Every output has an **EvidenceChain**
- Outputs are **versioned + superseded** on recompute
- Full **audit/replay**: “given snapshot S + ruleset R → reproduce run outputs”

---

## **1) Core run + snapshot primitives**

### **reasoning_runs**

One execution of the Reasoning Layer.

- run_id (PK, uuid)
- project_id (FK to knowledge project)
- context_mode (enum: CANONICAL, HYPOTHETICAL)
- trigger (enum: ONBOARDING, RECOMPUTE, WHATIF, 60SECOND)
- status (enum: RUNNING, COMPLETE, FAILED)
- created_at
- completed_at (nullable)
- supersedes_run_id (nullable; links recompute lineage)
- notes (nullable)

**Rules**

- Never overwritten; new runs supersede old runs.

---

### **input_snapshots**

Captures the “what I read” set for replay. Snapshot items can be pointers to Knowledge Layer version IDs.

- snapshot_id (PK, uuid)
- project_id
- created_at
- source_type (enum: KNOWLEDGE_LAYER)
- source_version_id (string/uuid; e.g., knowledge-layer commit/version)
- hash (content hash of snapshot manifest for immutability)

---

### **run_input_snapshots**

Many-to-many: a run references one or more snapshots.

- run_id (FK)
- snapshot_id (FK)
- **PK** (run_id, snapshot_id)

---

## **2) Rule versioning primitives**

### **rule_sets**

A named bundle of rules used by Reasoning.

- rule_set_id (PK, uuid)
- name (e.g., clarity_rules)
- description
- created_at

### **rule_set_versions**

Immutable version of a rule set.

- rule_set_version_id (PK, uuid)
- rule_set_id (FK)
- version (string, e.g., 1.3.0)
- content_ref (pointer to rules repository artifact)
- content_hash
- created_at
- is_deprecated (bool)

### **run_rule_versions**

Which rules were used for a run.

- run_id (FK)
- rule_set_version_id (FK)
- **PK** (run_id, rule_set_version_id)

---

## **3) Reasoning Graph (derived / ephemeral / replayable)**

This is the **project graph as used for computation**. It references canonical nodes/edges but can include inferred/synthetic nodes/edges.

### **rg_nodes**

### **(Reasoning Graph Nodes)**

- rg_node_id (PK, uuid)
- run_id (FK)
- node_kind (enum: CANON_REF, INFERRED, SYNTHETIC)
- canonical_type (nullable string; e.g., Outcome, Requirement)
- canonical_id (nullable string/uuid)
- label (nullable; non-UI, for debugging)
- created_at

**Constraints**

- If node_kind = CANON_REF, then canonical_type and canonical_id are required.
- If node_kind != CANON_REF, canonical fields must be null (keeps boundaries clean).

---

### **rg_edges**

### **(Reasoning Graph Edges)**

- rg_edge_id (PK, uuid)
- run_id (FK)
- src_rg_node_id (FK to rg_nodes)
- dst_rg_node_id (FK to rg_nodes)
- edge_kind (enum: CANON_REF, INFERRED, TEMPORARY)
- edge_type (string; e.g., depends_on, supports, blocks, aligned_to)
- canonical_edge_id (nullable; if CANON_REF)
- created_at

**Constraints**

- If edge_kind = CANON_REF, canonical_edge_id must be populated.

---

## **4) Evidence Chains (foundational primitive)**

### **evidence_chains**

- chain_id (PK, uuid)
- run_id (FK)
- rule_version_fingerprint (string; derived from run_rule_versions)
- created_at
- limitations (jsonb array of strings)

### **evidence_chain_inputs**

- chain_id (FK)
- snapshot_id (FK)
- **PK** (chain_id, snapshot_id)

### **evidence_chain_rule_applied**

(Granular trace for reproducibility and debugging)

- chain_id (FK)
- rule_set_version_id (FK)
- rule_id (string; identifier inside the rules content)
- params (jsonb; bounded)
- **PK** (chain_id, rule_set_version_id, rule_id)

### **evidence_chain_assumptions**

- assumption_id (PK, uuid)
- chain_id (FK)
- assumption_text (string)
- assumption_kind (enum: DECLARED_INPUT, BOUNDED_INFERENCE, SIMULATION_SCaffold)
- created_at

---

## **5) Primary outputs**

### **5.1 Issues**

### **issues**

- issue_id (PK, uuid)
- run_id (FK)
- type (enum: CLARITY, ALIGNMENT, FEASIBILITY)
- subtype (string)
- evidence_chain_id (FK)
- status (enum: OPEN, SUPERSEDED)
- superseded_by_issue_id (nullable FK to issues)
- created_at

### **issue_affected_nodes**

- issue_id (FK)
- rg_node_id (FK)
- **PK** (issue_id, rg_node_id)

---

### **5.2 Inferred elements & synthetic placeholders**

### **inferred_elements**

- inferred_element_id (PK, uuid)
- run_id (FK)
- rg_node_id (FK; where it “attaches”)
- field_path (string; e.g., schedule.finish_date, metric.target_value)
- value_json (jsonb)
- value_type (enum: DERIVED, SYNTHETIC_PLACEHOLDER)
- inference_reason (string)
- heuristic_used (nullable string)
- certainty_band (enum: LOW, MEDIUM, HIGH)
- epistemic_state (enum: PROPOSED) **(lock this to PROPOSED at DB level if you want)**
- evidence_chain_id (FK)
- status (enum: ACTIVE, SUPERSEDED)
- superseded_by_inferred_element_id (nullable FK to inferred_elements)
- created_at

**Hard constraints**

- If value_type = SYNTHETIC_PLACEHOLDER, then certainty_band must be LOW by default (enforce via app + check constraint if desired).
- Synthetic placeholders must never be “upgraded” here; promotion is a **Knowledge/Governance path**, not Reasoning.

---

### **5.3 Structural signals (raw)**

### **structural_signals**

- signal_id (PK, uuid)
- run_id (FK)
- signal_type (string; e.g., schedule_compression, dependency_tension, assumption_density)
- magnitude (numeric)
- direction (nullable enum: UP, DOWN, FLAT)
- evidence_chain_id (FK)
- created_at

### **signal_affected_nodes**

- signal_id (FK)
- rg_node_id (FK)
- **PK** (signal_id, rg_node_id)

---

## **6) Output supersession + persistence semantics**

If you want strict “supersede-not-delete” at the DB level, keep:

- status + superseded_by_* on each output table (issues, inferred_elements, signals if needed)
- reasoning_runs.supersedes_run_id to tie the lineage together

This supports:

- Viewing the “current” run as the latest COMPLETE run for project + context
- Auditing historical states without mutation

---

## **7) Minimal indexing (practical)**

- reasoning_runs(project_id, context_mode, created_at desc)
- rg_nodes(run_id, node_kind)
- rg_edges(run_id, edge_type)
- issues(run_id, type, status)
- inferred_elements(run_id, value_type, status)
- structural_signals(run_id, signal_type)
- evidence_chains(run_id)

---

## **8) What this model intentionally does NOT include**

- Any **user-facing messaging**
- Any **severity/priority** (Judgment/Governance concern)
- Any **canonical mutation** pathway
- Any “promotion” of inferred → canonical (must go through G-03 + Knowledge)

---

If you want the next step, I can produce either:

1. **SQL DDL (Postgres)** with constraints/checks/enums, or
2. A **Knowledge → Reasoning projection spec** (exact mapping rules + snapshot manifest format).