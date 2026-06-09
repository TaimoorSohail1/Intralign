# Outcome Graph Minimal Schema v1

---

Status: Draft for Implementation

Purpose: Define the minimum canonical entity/edge model to enable outcome governance now and coordination later, without constraining future evolution.

---

## **1) Core Requirements**

The schema MUST support:

- Many-to-many relationships (no rigid tree assumptions)
- Multi-tool execution mappings (Jira/Asana/Planner/etc.)
- Human + machine actors as first-class nodes
- Temporal history (event-time + ingestion-time + effective-time)
- Evidence linkage back to immutable raw records
- Deterministic snapshots for Reasoning/Judgment consumption

---

## **2) Identity, Versioning, and Time (Non-Negotiable)**

### **2.1 Canonical IDs**

Every canonical node/edge has a stable ID:

- node_id: og:n:<type>:<ulid>
- edge_id: og:e:<rel_type>:<ulid>

Use ULID (or UUIDv7) to preserve sortability by creation time.

### **2.2 External Identity Map (dedupe + multi-source)**

Maintain separate mapping objects:

- external_ref_id: og:xref:<ulid>
- Fields:
    - system: e.g., jira, asana, ms_planner, email, slack, crm
    - object_type: e.g., issue, task, message, deal
    - external_id: provider ID
    - external_url (optional)
    - first_seen_at, last_seen_at
    - confidence (0–1)

### **2.3 Time Fields (all nodes/edges)**

Every node/edge MUST carry:

- occurred_at (event-time; when reality happened)
- ingested_at (when OSLO saw it)
- effective_from (when this state becomes authoritative)
- effective_to (nullable; closed when superseded)

**Rule:** Reasoning reads a *snapshot at time T* using effective-time.

### **2.4 Evidence Pointer (chain-of-custody)**

Every node/edge mutation must reference evidence:

- evidence_refs: list of pointers to immutable raw records (staging/raw store IDs)
- Each evidence_ref includes:
    - raw_record_id
    - source_system
    - hash (or content signature)
    - occurred_at, ingested_at

---

## **3) Minimal Node Types**

Each node shares common base fields:

### **3.1 BaseNode (applies to all)**

- node_id
- node_type (enum)
- title (human-readable)
- status (enum; type-specific allowed values)
- created_at, updated_at
- occurred_at, ingested_at, effective_from, effective_to
- source_attribution (who/what asserted it; human/system/agent)
- evidence_refs[]
- labels[] (tags)
- properties (JSON; typed by node_type schema)

---

### **3.2 Outcome Node (**

### **OUTCOME**

### **)**

Minimum fields in properties:

- intent (text)
- success_criteria[] (list of measurable or testable statements)
- owner_actor_id (node_id of Actor)
- priority (optional)
- target_date (optional)
- confidence (0–1; optional)
- viability_state (enum: viable, at_risk, non_viable, unknown)
- version_label (e.g., v1.0 for the outcome definition *instance*)

**Note:** Outcome definition revisions are represented as new effective-time versions of the same node_id (or via explicit OutcomeRevision events; see Section 7).

---

### **3.3 Initiative / Workstream Node (**

### **INITIATIVE**

### **)**

properties:

- summary
- scope (text; optional)
- start_date (optional)
- target_date (optional)
- owner_actor_id (optional)
- methodology (optional: agile/waterfall/hybrid/custom)

---

### **3.4 Work Unit Node (**

### **WORK_UNIT**

### **)**

Represents tickets/tasks/deliverables/automations.

properties:

- work_kind (enum: task, ticket, deliverable, milestone, automation_run, agent_task)
- execution_system_refs[] (list of external_ref_id)
- state (execution state; normalized enum: not_started, in_progress, blocked, done, canceled, unknown)
- estimate (optional)
- start_date, due_date (optional)

---

### **3.5 Actor Node (**

### **ACTOR**

### **)**

First-class for humans and machines.

properties:

- actor_kind (enum: human, team, org_unit, system, agent, automation, vendor)
- display_name
- email (optional)
- org (optional)
- capabilities[] (optional; esp. for agents/systems)
- trust_level (optional: low, medium, high)
- external_refs[] (optional mapping to HRIS/IdP/etc.)

---

### **3.6 Decision Node (**

### **DECISION**

### **)**

properties:

- decision_text (what was decided)
- rationale (optional)
- decision_type (enum: scope_change, priority_change, approval, design_choice, go_no_go, resource_change, other)
- made_by_actor_ids[]
- approval_state (enum: proposed, approved, rejected, superseded)
- decision_timestamp (often equals occurred_at)

---

### **3.7 Signal Node (**

### **SIGNAL**

### **)**

Used for execution + validation signals (progress, KPIs, metrics).

properties:

- signal_kind (enum: execution_status, kpi, metric, risk_indicator, customer_signal, financial_signal, quality_signal)
- name
- value (typed union: number/string/bool/json)
- unit (optional)
- directionality (optional: higher_is_better, lower_is_better, neutral)
- thresholds (optional)
- source_system_ref (external_ref_id optional)

---

### **3.8 Constraint Node (**

### **CONSTRAINT**

### **)**

Constraints and assumptions are separable later, but keep minimal now.

properties:

- constraint_kind (enum: assumption, dependency, limit, policy, external_condition)
- statement
- severity (optional)
- validity_state (enum: valid, invalid, unknown)
- review_date (optional)

---

## **4) Minimal Edge Types (Relationships)**

Every edge uses a shared structure:

### **4.1 BaseEdge**

- edge_id
- rel_type (enum)
- from_node_id
- to_node_id
- strength (0–1 optional)
- status (enum: active, inactive, superseded)
- occurred_at, ingested_at, effective_from, effective_to
- source_attribution
- evidence_refs[]
- properties (JSON; typed by rel_type)

---

### **4.2 Required Relationship Enums**

### **Outcome structure**

- DECOMPOSES_TO
    
    OUTCOME -> INITIATIVE (and optionally INITIATIVE -> INITIATIVE)
    
- CONTRIBUTES_TO
    
    WORK_UNIT -> INITIATIVE and/or WORK_UNIT -> OUTCOME (allow both)
    

### **Ownership & responsibility**

- OWNED_BY
    
    {OUTCOME|INITIATIVE|WORK_UNIT|DECISION} -> ACTOR
    
- EXECUTED_BY
    
    WORK_UNIT -> ACTOR (humans/agents/systems)
    

### **Dependencies**

- DEPENDS_ON
    
    {WORK_UNIT|INITIATIVE|OUTCOME} -> {WORK_UNIT|INITIATIVE|OUTCOME|CONSTRAINT}
    

### **Decision impact**

- DECIDES
    
    DECISION -> {OUTCOME|INITIATIVE|WORK_UNIT|CONSTRAINT}
    
    (what the decision changed/authorized)
    

### **Signals & validation**

- PRODUCES_SIGNAL
    
    {WORK_UNIT|ACTOR|SYSTEM} -> SIGNAL
    
- VALIDATES
    
    SIGNAL -> OUTCOME (or SIGNAL -> INITIATIVE)
    

### **Constraints**

- CONSTRAINS
    
    CONSTRAINT -> {OUTCOME|INITIATIVE|WORK_UNIT}
    

---

## **5) Normalized Statuses (keep simple)**

### **Outcomes**

- draft, active, at_risk, achieved, abandoned

### **Initiatives**

- planned, active, paused, completed, canceled

### **Work Units**

- not_started, in_progress, blocked, done, canceled, unknown

### **Decisions**

- proposed, approved, rejected, superseded

### **Signals**

- observed (default), anomalous (optional)

### **Constraints**

- active, invalid, unknown

---

## **6) Minimal Read/Write Interfaces (contracts)**

### **6.1 Writes (canonical)**

Only via **Graph Mutation API** (single choke point).

Mutation types (minimal set):

- UPSERT_NODE
- UPSERT_EDGE
- CLOSE_NODE_VERSION (sets effective_to)
- CLOSE_EDGE_VERSION
- LINK_EXTERNAL_REF (creates/updates xref mapping)

Every mutation requires:

- mutation_id (ulid)
- proposed_by (actor/system/agent)
- approved_by (if governance required; optional per rule)
- evidence_refs[]
- occurred_at, ingested_at
- effective_from

### **6.2 Reads**

Reasoning/Judgment read **graph snapshots**:

- GET_SNAPSHOT(time=T, scope={project/org}, filters=...)
- Snapshot is a consistent set of node/edge versions where:
    - effective_from <= T < effective_to (or null)

---

## **7) Two Minimal Patterns to Prevent Future Dead Ends**

### **Pattern A — Event log + materialized snapshot**

- Store mutation events append-only.
- Materialize “current graph” views for performance.
- Snapshots must be reproducible.

### **Pattern B — Don’t embed tool semantics in node types**

Do NOT create node types like JIRA_ISSUE or ASANA_TASK.

Instead:

- Use WORK_UNIT + execution_system_refs[].

This preserves execution neutrality forever.

---

## **8) Minimal “Coordination-Ready” Queries This Schema Enables**

With this v1, OSLO can later answer:

- “Which actors (human/agent) are executing work contributing to Outcome X?”
- “What decisions changed Outcome X’s viability?”
- “Which work units are blocked and threaten Outcome X?”
- “What signals validate or invalidate Outcome X?”
- “Where are constraints undermining feasibility?”
- “What should act next?” (coordination layer builds on top of these relations)

---

## **9) Implementation Guardrails**

Engineering MUST avoid:

- Enforcing a strict tree: Outcome → Initiative → Task only
- Assuming 1-to-1 mapping between Work Unit and Outcome
- Storing only “current state” without effective-time history
- Allowing integrations to write canonical nodes directly
- Letting Reasoning read staging/raw directly

---

## **10) Deliverable Summary (what to implement first)**

Minimum to ship safely:

1. Node/edge storage with effective-time versioning
2. External identity map (xref)
3. Evidence pointer model (raw_record_id + signature)
4. Graph Mutation API (single choke point)
5. Snapshot query semantics

Everything else (advanced inference, coordination UX, benchmarks) can come later.

---

If you want, I can follow this with a **Read/Write Matrix v1** that spells out exactly which OSLO components may mutate which node/edge types (e.g., Planning may create Outcomes/Initiatives; Integrations may only emit staging events; Governance approves Outcome/Constraint changes; etc.).