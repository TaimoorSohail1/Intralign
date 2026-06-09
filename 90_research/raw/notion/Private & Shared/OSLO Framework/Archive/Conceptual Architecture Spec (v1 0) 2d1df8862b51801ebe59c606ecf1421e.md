# Conceptual Architecture Spec (v1.0)

**Product:** Intralign

**System:** OSLO (Outcome-Driven Strategic Lifecycle Orchestration)

**Component:** OSLO Communication Engine (OCE)

**Version:** 1.0

**Audience:** Product, Engineering, AI/ML, Design, QA

**Purpose:** Define the conceptual architecture that satisfies the BRS v1.1 for OSLO communication (trust-first, non-opaque, canonical, policy-driven, consistent across surfaces).

---

## **1. Architecture Goals**

### **1.1 Primary Goals**

- **Trust-first communication**: OSLO communications must be explainable and defensible.
- **Non-opaque by default**: Communications must expose “how OSLO knows” at a minimum trust bar.
- **Canonical, reusable communication units**: One source of truth for what OSLO “said.”
- **Policy-driven behavior**: When/what/how OSLO communicates is governed by versioned policies.
- **Cross-surface consistency**: Chat, panels, and exports render from the same canonical RCUs.

### **1.2 Non-Goals for v1.0**

- Persuasive / emotionally optimized messaging
- Engagement-first nudges as a standalone intent
- Autonomous actions without explanation
- Fully declarative communication DSL

---

## **2. Conceptual System Context**

### **2.1 Upstream Systems (Inputs)**

- **Scoring Engine** (health scores, sub-scores, deltas)
- **Issue Diagnosis Engine** (issue taxonomy, detected issues, severity, confidence)
- **Artifact Graph / Plan Model** (artifact elements and relationships)
- **User Context Signals** (mode, current surface, recent actions; minimal in MVP)
- **Event Stream** (plan updates, new detection runs, user interactions)

### **2.2 Downstream Surfaces (Outputs)**

- **OSLO Chat** (system-initiated, critical-only in MVP)
- **Issue / Context Panel** (primarily user-initiated)
- **Exports** (PDF) and future surfaces (reports, exec views)

---

## **3. Architecture Overview**

### **3.1 Core Architectural Principle**

> Communication is a projection of canonical state, not a free-form narrative generator.
> 

### **3.2 High-Level Components**

1. **Communication Orchestrator**
2. **Policy Engine**

1. **RCU Builder**
2. **Reasoning & Evidence Assembler**
3. **Suppression & Prioritization Gate**
4. **Surface Router**
5. **Renderer Layer (per surface)**
6. **RCU Store (Canonical Record)**
7. **Telemetry & Feedback Logger**
8. **Correction & Versioning Manager**

---

## **4. Component Responsibilities**

### **4.1 Communication Orchestrator**

**Role:** Entry point for all communication decisions.

**Responsibilities:**

- Receives triggers (diagnosis results, score deltas, user queries, workflow moments)
- Requests intent candidates from upstream signals
- Invokes Policy Engine to select intents, ordering, tone strength, and persistence
- Produces a finalized “communication plan” (one or more RCUs)

**Key outputs:** CommunicationPlan, RCUCreate requests.

---

### **4.2 Policy Engine (Versioned)**

**Role:** Determines behavior without hard-coded branching.

**Responsibilities:**

- Applies **Intent selection rules** (MVP: Diagnostic, Boundary, Advisory)
- Applies **Ordering** (Diagnostic → Boundary → Advisory)
- Applies **Interruption posture** (MVP: critical-only)
- Applies **suppression heuristic** (confidence × impact)
- Defines **uncertainty disclosure mode** (layered)
- Defines **accountability mode** (contextual)
- Defines **persistence rules** (contextual)

**Artifacts:**

- **Policy Set** with version ID (e.g., OCE_POLICY_1.0.0)
- Policy evaluation produces **PolicyDecision** attached to each RCU.

---

### **4.3 Suppression & Prioritization Gate**

**Role:** Prevent noise and preserve credibility.

**Responsibilities:**

- Computes “should communicate” decision using policy thresholds
- De-duplicates similar candidates
- Batches low-priority candidates into panel-only visibility
- Enforces critical-only proactive delivery for MVP

**Outputs:** ApprovedCandidateRCUs + Surface constraints (chat vs panel).

---

### **4.4 RCU Builder (Canonical Unit Constructor)**

**Role:** Creates the authoritative Reasoned Communication Unit.

**Responsibilities:**

- Constructs RCU metadata (intent, subtype, scope, references)
- Enforces minimum explanation completeness:
    - What is wrong
    - Why it matters
    - What OSLO used to determine this
- Attaches confidence indicators (layered) and policy version
- Produces “render-agnostic” canonical representation

**Output:** RCU (canonical JSON-like object) persisted to RCU Store.

---

### **4.5 Reasoning & Evidence Assembler**

**Role:** Builds defensible “grounds” for communication.

**Responsibilities:**

- Pulls evidence references:
    - issue signals (taxonomy, rule hits, model outputs)
    - artifact pointers (element IDs, relationship paths)
    - scoring deltas (before/after)
- Produces a “reasoning bundle” appropriate to the user’s depth level
- Ensures no fabricated certainty or sources

**Outputs:** ReasoningBundle (summary + expandable details).

---

### **4.6 Surface Router**

**Role:** Determines delivery surface(s) per RCU.

**Responsibilities:**

- Enforces surface constraints:
    - **Chat**: OSLO-initiated allowed
    - **Panel**: default user-initiated; can still display RCUs when opened
- Routes critical items to chat (in MVP posture)
- Routes all items to canonical store + panel availability

**Output:** DeliveryPlan per RCU.

---

### **4.7 Renderer Layer (per surface)**

**Role:** Converts canonical RCU → surface-specific presentation.

**Responsibilities:**

- Chat renderer produces concise, trust-complete message with expand links
- Panel renderer shows deeper inspection view (evidence, confidence, references)
- Export renderer produces static explanations tied to artifacts/issues

**Constraint:** Renderers may vary wording but cannot alter meaning, reasoning, or state.

---

### **4.8 RCU Store (Canonical Record)**

**Role:** Single source of truth for “what OSLO communicated.”

**Responsibilities:**

- Persist RCU with versioned policy reference
- Support retrieval by:
    - project
    - artifact element
    - issue
    - time window
    - surface delivery status

**Why it exists:** Enables consistency, supportability, defensibility.

---

### **4.9 Telemetry & Feedback Logger**

**Role:** Implements layered learning.

**Responsibilities:**

- Logs interactions with RCUs:
    - viewed, expanded, accepted, dismissed, ignored
    - “why?” requests
- Logs delivery outcomes:
    - delivered, suppressed, failed, retried
- Provides datasets for policy refinement (offline in MVP)

---

### **4.10 Correction & Versioning Manager**

**Role:** Handles “being wrong” responsibly.

**Responsibilities:**

- Detects when an RCU becomes invalid/superseded (new diagnosis run, new evidence)
- Applies contextual accountability policy:
    - explicit correction for high-impact RCUs
    - silent correction allowed for low-impact refinements
- Records supersession relationships: RCU_A superseded_by RCU_B

---

## **5. Data Model (Conceptual)**

### **5.1 Reasoned Communication Unit (RCU) — Canonical Fields**

- rcu_id
- created_at
- project_id
- intent_type (MVP: diagnostic | boundary | advisory)
- subtype (diagnostic/…; future extensibility)
- scope (artifact-scoped | issue-scoped | global)
- references:
    - artifact_element_ids[]
    - issue_ids[]
    - score_ids[] / score_delta_refs[]
- message_core:
    - what (claim)
    - why_it_matters (impact framing)
    - how_oslo_knows (grounds summary)
- confidence:
    - band (high/med/low)
    - details_ref (expandable)
- reasoning_bundle_ref (points to evidence/trace object)
- policy_version
- delivery_state[] (per surface)
- persistence_class (contextual)
- supersession:
    - supersedes_rcu_id?
    - superseded_by_rcu_id?
- accountability_mode (contextual outcome)

### **5.2 ReasoningBundle (Evidence Trace)**

- bundle_id
- grounds (rule hits, model signals, heuristic checks)
- artifact_pointers (paths/relationships)
- assumptions (explicit)
- limitations (explicit)
- generated_at
- source_versions (diagnosis engine version, scoring version)

---

## **6. Key Flows**

### **6.1 Flow A — New Diagnosis Run Produces Issues (Primary)**

1. Diagnosis Engine emits IssueDetected events (with severity/confidence)
2. Orchestrator pulls candidates → Policy Engine
3. Gate computes confidence×impact → approves/suppresses
4. RCU Builder constructs:
    - Diagnostic RCU
    - Boundary RCU (if uncertainty/limits relevant)
    - Advisory RCU (derived from diagnostic)
5. Store canonical RCUs
6. Router:
    - If critical-only criteria met → deliver to chat
    - Otherwise → available in panel upon user open
7. Telemetry logs interactions

### **6.2 Flow B — User Opens Issue Panel (User-Initiated Depth)**

1. Panel requests RCUs by project/artifact/issue
2. Renderer shows canonical list
3. User expands “how OSLO knows” → fetch ReasoningBundle
4. Telemetry records expansions and dwell

### **6.3 Flow C — Correction/Supersession After Recompute**

1. New run changes status/severity/confidence
2. Correction Manager determines if prior RCU is invalid
3. Policy determines explicit vs silent correction
4. Store new RCU and supersession link
5. If high-impact and previously delivered via chat → emit correction note in chat

---

## **7. Policy Model (Conceptual)**

### **7.1 Policy Categories (v1.0)**

- **Intent eligibility**: allowed intents = {Diagnostic, Boundary, Advisory}
- **Ordering**: Diagnostic → Boundary → Advisory
- **Interruption posture**: critical-only
- **Suppression**: confidence×impact decision matrix
- **Tone strength**: contextual (severity, confidence)
- **Uncertainty disclosure**: layered
- **Persistence**: contextual mapping
- **Accountability**: contextual mapping
- **Failure handling**: contextual mapping
- **Surface routing**: chat vs panel constraints

### **7.2 Policy Versioning**

- Every RCU MUST reference policy_version
- Policy changes are treated as product behavior changes and must be reviewable

---

## **8. Surface Semantics and Consistency Rules**

### **8.1 Chat (Proactive)**

- MVP: only for critical items
- Must be trust-complete in the initial message
- Must offer expansion into “how OSLO knows” and “limits”

### **8.2 Panel (Reactive)**

- Primary locus of dense inspection
- Should display the canonical set (including suppressed-from-chat RCUs)
- Enables deeper reasoning bundle exploration

### **8.3 Exports (PDF)**

- Render canonical RCUs attached to artifacts/issues
- Ensure stable references and policy version for defensibility

---

## **9. Reliability and Failure Posture (Conceptual)**

- Communication generation is allowed to degrade, but must not become deceptive.
- High-impact failures must produce explicit disclosure (per policy).
- The system must never substitute fabricated reasoning for missing evidence.

---

## **10. Acceptance Targets for v1.0 Architecture (Conceptual)**

These are architecture-level targets aligned to the BRS exit logic:

- Canonical RCU store is the **single source** for all surfaces
- Policy engine controls behavior (not scattered branching)
- Minimum trust-complete explanation is enforced at RCU build time
- Critical-only proactive behavior is enforceable and testable
- Supersession and accountability are representable in the data model

---

## **11. Traceability to BRS (Summary)**

- **Opacity avoidance / trust-first** → ReasoningBundle + trust-complete RCU fields
- **Full consistency** → Canonical RCU Store + renderer constraint
- **Hybrid initiation (chat proactive, panel reactive)** → Surface Router semantics
- **Suppression (confidence×impact)** → Gate + Policy Engine
- **Policy-driven + versioned** → Policy Engine + policy_version on RCU
- **Contextual accountability** → Correction Manager + policy mapping
- **Layered learning** → Telemetry Logger (no auto behavior change in MVP)

---

## **12. Open Decisions (Intentionally Deferred)**

(These are architectural “slots” to fill later without changing core direction.)

- Exact confidence and impact scale definitions
- Exact “critical-only” thresholds and categories
- Depth modes and expansion UX patterns per surface
- Reasoning bundle granularity (rule-level vs aggregated)
- Enterprise-grade audit trail (beyond canonical record)

---

# **OSLO Communication Engine — Layer Mapping Addendum (v1.0)**

*(Authoritative clarification for architecture & implementation)*

This section augments the existing **Conceptual Architecture Spec (v1.0)** by explicitly identifying **which canonical OSLO layer** each system, component, and surface belongs to.

---

## **Canonical OSLO Layers (Reminder)**

1. **Project Knowledge Layer**
2. **Reasoning Layer**
3. **Judgment Layer**
4. **Governance Layer**
5. **Communication Layer**
6. **Rendering / Surface Layer** *(presentation-only)*

> Rule:
> 

> A component may
> 
> 
> *consume outputs*
> 
> **reside in exactly one layer of authority**
> 

---

## **1. Upstream Systems → Layer Placement**

| **System** | **Canonical Layer** | **Rationale** |
| --- | --- | --- |
| Artifact Graph / Plan Model | **Project Knowledge** | Canonical representation of explicit project state |
| Scoring Engine (CAF) | **Judgment** | Interprets findings into Clarity, Alignment, Feasibility health |
| Issue Diagnosis Engine | **Judgment** | Classifies findings into issues with severity & confidence |
| Event Stream | **Governance (Input Signal)** | Triggers timing and eligibility, not meaning |
| User Context Signals | **Governance** | Determines posture, timing, suppression |

---

## **2. Core Components → Layer Placement**

### **Communication Orchestrator**

- **Layer:** **Governance**
- **Why:**
    
    Decides *whether*, *when*, and *how many* communications occur — not what they mean or how they’re worded.
    

---

### **Policy Engine (Versioned)**

- **Layer:** **Governance**
- **Why:**
    
    Encodes behavioral constraints, suppression rules, ordering, posture, and accountability logic.
    

---

### **Suppression & Prioritization Gate**

- **Layer:** **Governance**
- **Why:**
    
    Enforces restraint, deduplication, batching, and interruption posture.
    

---

### **Reasoning & Evidence Assembler**

- **Layer:** **Reasoning**
- **Why:**
    
    Produces **evidence chains and reasoning bundles** (facts + traces only).
    
    Does **not** assign severity, confidence, or meaning.
    

---

### **RCU Builder (Canonical Unit Constructor)**

- **Layer:** **Communication**
- **Why:**
    
    Assembles governed meaning into a structured, render-agnostic message unit.
    
    Does not decide *if* communication should occur.
    

---

### **Surface Router**

- **Layer:** **Governance**
- **Why:**
    
    Determines *where* an RCU may appear (chat vs panel), not what it says.
    

---

### **RCU Store (Canonical Record)**

- **Layer:** **Communication (Canonical Memory)**
- **Why:**
    
    Single source of truth for what OSLO has communicated — independent of rendering.
    

---

### **Telemetry & Feedback Logger**

- **Layer:** **Governance (Learning Input)**
- **Why:**
    
    Observes outcomes to inform future policy, without altering meaning or truth.
    

---

### **Correction & Versioning Manager**

- **Layer:** **Governance**
- **Why:**
    
    Applies accountability policy when truth changes; does not reinterpret findings.
    

---

## **3. Data Structures → Layer Placement**

| **Data Object** | **Layer** |
| --- | --- |
| Artifact entities, relationships | **Project Knowledge** |
| EvidenceChain / ReasoningBundle | **Reasoning** |
| Issue records (severity, confidence) | **Judgment** |
| CAF Health Scores | **Judgment** |
| PolicyDecision | **Governance** |
| CommunicationPlan | **Governance** |
| RCU (Reasoned Communication Unit) | **Communication** |

---

## **4. Surfaces → Layer Placement**

> Surfaces
> 
> 
> **never own logic**
> 

| **Surface** | **Layer** |
| --- | --- |
| OSLO Chat | **Rendering / Surface Layer** |
| Issue / Context Panel | **Rendering / Surface Layer** |
| PDF / Export | **Rendering / Surface Layer** |

**Hard rule:**

Surfaces may **not**:

- change meaning
- re-evaluate confidence
- infer new facts
- override suppression or policy

---

## **5. Flow-to-Layer Trace (Example)**

**Diagnosis Run → Chat Message**

```
Project Knowledge
   ↓
Reasoning
   (evidence chains)
   ↓
Judgment
   (issue + CAF impact)
   ↓
Governance
   (policy + suppression + routing)
   ↓
Communication
   (RCU construction)
   ↓
Rendering
   (chat/panel/export)
```

If any step is skipped or merged → **architecture violation**.

---

## **6. Explicit Non-Responsibilities (Lock These In)**

| **Layer** | **Must NOT Do** |
| --- | --- |
| Project Knowledge | Infer, evaluate, judge |
| Reasoning | Assign severity, confidence, or importance |
| Judgment | Discover facts or generate language |
| Governance | Reinterpret truth or meaning |
| Communication | Decide timing, suppression, or severity |
| Rendering | Change meaning or policy |

---

## **Canonical Summary Statement**

> Each OSLO communication component resides in exactly one canonical layer of authority—ensuring truth, meaning, behavior, and presentation remain cleanly separated and auditable.
> 

---

If you want next, I can:

- Produce a **one-page layer diagram** for the team
- Add **PR review guardrails** (“this change violates layer X”)
- Rewrite the spec with **layer headers embedded per section**
- Convert this into a **Notion-ready engineering standard**

Just say which.