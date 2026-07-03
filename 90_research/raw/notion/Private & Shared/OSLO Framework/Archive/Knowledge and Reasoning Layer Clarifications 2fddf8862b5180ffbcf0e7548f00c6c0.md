# Knowledge and Reasoning Layer Clarifications

Below is an implementation-explicit answer set that resolves each question **without ambiguity**. I’m going to be crisp on: **what lives where, what gets written by whom, and what identifiers must be stable**.

---

## **0) Non-negotiable definitions (so we stop colliding terms)**

### **Canonical Store (CS)**

**Purpose:** OSLO’s authoritative, user-visible, versioned project state (facts + accepted inferences + decisions).

**Write permission:** **Only** via **Judgment** outcomes (user accept/reject, or policy-based acceptance).

**Read permission:** All layers.

**Contains:**

- User-provided facts (as structured elements)
- Inferences *only if accepted* (by user or governance policy)
- User rejections (explicit “do not suggest again” constraints)
- Stable issue/finding “case” records (persistence)
- Audit references to machine outputs (by pointer), not the bulky machine payload

### **Machine Repository (MR)**

**Purpose:** High-volume, ephemeral or replayable *machine-generated* artifacts and raw ingestion products.

**Write permission:** Knowledge ingestion + Reasoning + system pipelines.

**Read permission:** All layers.

**Contains:**

- Raw document ingests + OCR text + page images (or pointers)
- RAG chunks + embeddings
- Extracted candidates (claims) with provenance
- Reasoning “runs” and raw “findings”
- Evidence graph edges and payloads
- Cached computations for replay

### **Synchronization rule**

There is **no bidirectional sync**. There is **promotion** (MR → CS) when and only when Judgment/Governance says so.

---

# **Knowledge Layer questions**

## **1) “Two separate databases… how keep sync between both?”**

**Answer:** They are **not kept in sync** as mirrors.

**Rule:**

- MR is the *derivation substrate* (raw + machine outputs).
- CS is the *authoritative accepted state*.

**Mechanism:** Promotion by reference.

- CS stores a canonical element (or constraint) that includes a **source pointer** to MR (run_id / evidence_id / claim_id).
- MR never “syncs back” from CS. If you need CS data in MR for computation, you **read CS** at runtime or copy into a run snapshot.

**Implementation detail:**

- Use separate DBs or separate schemas; either is fine. The requirement is logical separation + write-gates, not physical infra.

---

## **2) “Where will the system store RAG chunks?”**

**Answer:** **Machine Repository. Always.**

Reason: RAG chunks are **derived representations of documents** and are not “accepted project truth.” They are retrieval infrastructure.

**MR tables:**

- document_blob (file metadata + storage pointer)
- document_text_span (page/offset spans)
- rag_chunk (chunk text + span pointers)
- embedding (vector store id + chunk_id mapping)

**Canonical store may store only:**

- user-approved document metadata (optional)
- citations/pointers to MR spans when something is accepted into CS

---

## **3) “Elements are core; what can Reasoning reference as evidence?”**

**Answer:** Reasoning may reference **only three evidence source types**, explicitly:

1. **Document evidence** (from MR):
    
    “This claim was derived from these exact spans in uploaded docs.”
    
2. **Canonical evidence** (from CS):
    
    “This finding was derived from canonical elements/constraints already accepted.”
    
3. **Run evidence** (from MR):
    
    “This finding depends on outputs of an earlier reasoning run (e.g., a computed dependency graph).”
    

Reasoning **must never cite itself without a pointer**. Every evidence link must resolve to one of the above.

---

## **4) “How will evidence look in the database?”**

**Answer:** Evidence is a first-class entity with **typed pointers**, not free-text.

Minimum schema (MR):

- evidence_node
    - evidence_id (uuid)
    - type ENUM: DOC_SPAN | CANON_ELEMENT | RUN_OUTPUT
    - ref JSON (typed payload; see below)
    - hash (content hash for immutability verification)
    - created_at
- evidence_edge
    - from_evidence_id
    - to_evidence_id
    - relation ENUM: SUPPORTS | CONTRADICTS | DERIVED_FROM | DEPENDS_ON

Typed ref payloads:

- DOC_SPAN:
    - {doc_id, page, start_offset, end_offset, excerpt_hash, storage_uri?}
- CANON_ELEMENT:
    - {project_id, element_id, element_version_id}
- RUN_OUTPUT:
    - {run_id, finding_id, output_field}

---

## **5) “Where will evidence store?”**

**Answer:** **Evidence payload lives in MR.**

CS stores **only pointers** to evidence.

- MR: stores nodes/edges + doc spans + excerpts + hashes
- CS: stores accepted_element.source_evidence_ids[] and finding_case.latest_run_id

---

## **6) “How keep track of evidence chain between two storages?”**

**Answer:** You don’t “chain between storages.” You chain in MR and **reference into CS**.

- Evidence chain graph: MR only.
- Canonical records: store pointers to evidence root(s).

**Implementation requirement:**

- Every canonical “accepted element” and every canonical “finding case status” must include:
    - provenance: {run_id, evidence_root_ids[]}
- This allows full replay via MR.

---

## **7) “Knowledge Layer holds everything vs only confirmed data”**

**Answer:** The phrase “Knowledge Layer holds everything” means:

- The **Knowledge Layer subsystem** governs both CS + MR as one logical layer.
- **But** the **Canonical Store** holds only confirmed/accepted items.

So:

- “Everything” (raw + machine + confirmed) = MR + CS combined.
- “Confirmed data only” = CS.

---

# **Reasoning Layer questions**

## **8) “If user rejects an inferred element… no defined way to remember”**

**Answer:** Rejection memory is **canonical**, not reasoning.

**Where stored:** CS table user_constraints (or rejection_constraints).

**Schema (CS):**

- constraint_id
- project_id
- scope (element_type or element_id)
- constraint_type ENUM: REJECT_VALUE | REJECT_PATTERN | DO_NOT_SUGGEST | LOCK_FIELD
- payload JSON, e.g. {field:"start_date", rejected_value:"2026-03-01", reason?}
- created_by (USER or GOVERNANCE)
- created_at
- expires_at (nullable; optional)

**Reasoning behavior:** On every run, Reasoning reads constraints from CS and filters candidates before emitting findings.

This does **not** violate “Reasoning can’t write/remember.” It only reads CS.

---

## **9) “How prevent suggesting same rejected date next time?”**

**Answer:** Same as above: Reasoning must apply CS constraints deterministically.

Implementation detail:

- Candidate generation → **constraint filter** → output
- Filtering must run **before** scoring/ranking so rejected values never surface.

---

## **10) “Blind spot: user asks ‘show me sentence in my PDF’ but Reasoning never saw PDF”**

**Answer:** Reasoning must have access to **document spans** through MR. It does not need to “see the PDF”; it must be able to resolve evidence pointers.

Requirement:

- Every extracted claim/fact used by reasoning must include a DOC_SPAN evidence node with offsets.
- UI query “show me sentence” resolves to MR document_text_span + doc_id/page/offsets, and renders the excerpt.

So Reasoning can answer because:

- It references evidence nodes that point to doc spans.
- The UI renders the span; Reasoning doesn’t “open PDFs,” it returns pointers that the system can render.

---

## **11) “What is ‘Fragility’ and ‘dependency tension’?”**

These are **explicit computed attributes** Reasoning must output.

### **Fragility**

**Definition:** Likelihood that an element/finding becomes invalid when upstream assumptions or dependencies change.

**Computation (deterministic):**

- fragility_score = f(num_dependencies, dependency_confidence, volatility, assumption_count)
- Where:
    - num_dependencies = count of upstream elements/assumptions it relies on
    - dependency_confidence = min/avg confidence of those upstream supports
    - volatility = whether dependencies are tagged as “high-change” (dates, resourcing, vendor SLAs)
    - assumption_count = number of inferences (non-fact supports)

**Output:** fragility = LOW | MEDIUM | HIGH + numeric score.

### **Dependency tension**

**Definition:** A detected structural conflict where two or more dependencies impose constraints that cannot all be satisfied simultaneously **without tradeoff**.

Examples:

- Schedule date requires resource availability that contradicts capacity.
- Scope constraint contradicts time constraint given fixed staffing.

**Computation:**

- Identify constraint set; check satisfiability (simple rule checks are enough v1):
    - If constraints mutually exclusive → tension = TRUE
- Output: tension_type, conflicting_dependencies[], resolution_options[] (as recommendations, not decisions)

---

## **12) “Finding IDs will change across rule version updates… UI flicker. How maintain ID persistence?”**

**Answer:** Separate **Case Identity** from **Run Instance Identity**.

### **Stable:**

### **finding_case_id**

### **(CS)**

Represents the persistent “issue” as understood by the user.

### **Unstable per run:**

### **finding_instance_id**

### **(MR)**

Represents a specific detection event from a specific ruleset/run.

**How to generate stable finding_case_id (deterministic):**

Use a **case key** that excludes rule version:

- case_key = hash(project_id + finding_type + subject_element_id + normalized_parameters)
    
    Examples:
    
- Missing mandatory element “Risk Register”: subject = artifact:risk_register
- Misalignment between dates: subject = element:milestone_X

**Promotion flow:**

- Reasoning emits instances with case_key
- System resolves case_key to existing finding_case_id in CS (upsert)
- CS updates the case with latest_instance_id, latest_run_id, status, etc.

**UI renders:**

- the case (stable)
- latest instance details (may change)
    
    This prevents flicker across ruleset changes.
    

---

## **13) “Retain outputs and evidence chains indefinitely… no prune/archive policy”**

**Answer:** You need explicit **hot vs cold retention**. “Indefinite retention” does not mean “hot query path forever.”

### **Policy (required)**

1. **CS (canonical):** retained indefinitely (small, curated).
2. **MR hot window:** keep last **N days** of full run payloads in primary DB (e.g., 30–90 days).
3. **MR cold archive:** move older runs/evidence payloads to cheap storage (object store) but keep indexes.

### **Implementation**

- reasoning_run table stays in MR with minimal metadata forever:
    - run_id, project_id, ruleset_version, created_at, archive_uri, root_evidence_ids[]
- Large payload tables (evidence_node.ref, extracted excerpts, intermediate graphs) are:
    - partitioned by date
    - archived to object storage after threshold
    - deleted from hot DB after verification

### **Replay requirement**

Replay is satisfied if:

- You can fetch run_id → locate archive_uri → load full evidence graph offline/on-demand.

### **Performance guarantee**

All normal UI operations must only query:

- CS finding cases + latest instance pointers
- MR latest run(s) + bounded evidence excerpt fetch
    
    Never scan historical millions of rows for normal screens.
    

---

# **Summary you can give your engineer (one paragraph, implementable)**

- MR holds all raw docs, chunks, embeddings, extracted claims, reasoning runs, and full evidence graphs. CS holds only accepted elements, constraints (including rejection memory), and stable finding cases. There is no sync; there is promotion by reference. Evidence is stored as typed nodes/edges in MR, while CS stores pointers to evidence roots. Reasoning reads CS constraints to avoid resurfacing rejected suggestions. “Show me the PDF sentence” is resolved via doc span pointers in MR. Fragility and dependency tension are deterministic computed outputs. Finding persistence is achieved by stable finding_case_id derived from a versionless case key, while per-run finding_instance_id changes. Retention is indefinite logically but implemented via hot/cold storage with archived runs accessible by run_id.

If you want, I can convert the above into a **v1.0 “Knowledge Layer Storage Contract + Reasoning Output Contract”** with concrete JSON schemas and required indexes (so implementation is even more mechanical).