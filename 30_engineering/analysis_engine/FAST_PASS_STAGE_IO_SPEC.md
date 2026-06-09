# Fast Pass — Stage I/O Specification

**Type:** Locked workflow spec — Fast Analysis Pass stages (intake → orientation)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Authority order:** Planning Intelligence > State Model > Event Model > Data Model v1.1 > Analysis Engine > NFR > API/UI/Testing > Supporting models > Proposal notes
**Grounded in:** `PLANNING_INTELLIGENCE_SPECIFICATION_V1.md` · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` §9 · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md`

> **Scope.** Active Release 1 only. The Fast Pass produces the **60-Second Orientation**, which is **not final understanding**. No governance, accepted understanding, agent governance, autonomous execution, actuation, or outcome-orchestration runtime. No invented formulas, weights, percentages, or thresholds. Each stage is tagged `canonical` / `derived` / `proposal` / `TBD`. Stage time budgets are **proposal** (load-test pending); the only `canonical` numeric target is Time-to-First-MRI **< 60s** (NFR §3).
>
> **Trigger (canonical).** A Fast run is requested once per project when it has ≥1 analyzable input and no completed fast run (Event Model §15). Project: `created → orienting`. AnalysisRun: `run_type=fast_analysis_pass`, `run_status=queued`.

---

## Legend
**Execution type:** `rule` (deterministic, no LLM) · `llm` · `hybrid`. **Tag:** `canonical` (in an authoritative spec) · `derived` (logically entailed) · `proposal` (this pack's recommendation) · `TBD` (owner decision).

---

## Stage 0 — Intake & Acquisition

- **Purpose** `canonical` — Receive submitted evidence and assemble the run's input set.
- **Owner layer/component** `canonical` — Context Plane (acquisition); Analysis Engine (run creation).
- **Execution type** — `rule`.
- **Input spec** `derived` — Project id; submitted `Evidence` (source_type ∈ {free_text, uploaded_document, structured_input, imported_content}); project intent; prior run state (if any).
- **Output spec** `derived` — Persisted `Evidence` rows; an enqueued `AnalysisRun` (fast); validated input set.
- **Required entities** `canonical` — `Project`, `Evidence`, `AnalysisRun`.
- **Required fields** `canonical` — `evidence_id`, `project_id`, `source_type`, `content_ref`, `provenance`; `analysis_run_id`, `run_type=fast_analysis_pass`, `run_status=queued`, `trigger_source`.
- **Entry criteria** `canonical` — First analyzable input present; no completed fast run for the project.
- **Exit criteria** `derived` — Input set assembled and within the ingestion envelope (or flagged oversize).
- **Rule responsibilities** `derived` — Envelope/type validation; provenance capture; oversize routing decision; run enqueue.
- **LLM responsibilities** — none.
- **Validation rules** `proposal` — Reject unsupported `source_type`; enforce ingestion envelope (≈20k-token design point / ≈33k hard ceiling — **proposal/TBD**, see OPEN_DECISIONS); oversize ⇒ accept but route Deep-only with honest messaging.
- **Fallback/failure behavior** `derived` — Acquisition failure ⇒ run not created; surface input error; no state change.
- **Events emitted** `canonical` — `fast_analysis_requested`.
- **State transitions** `canonical` — Project `created → orienting`; run → `queued`.
- **Traceability requirements** `canonical` — Each `Evidence` carries `provenance`; downstream items link back via `evidence_id`.
- **Open decisions** — Ingestion envelope value; oversize-routing policy (`TBD`).

---

## Stage 1 — Normalization

- **Purpose** `canonical` — Canonicalize raw inputs into the working representation reasoning consumes.
- **Owner layer/component** `canonical` — Context Plane.
- **Execution type** — `rule`.
- **Input spec** `derived` — Persisted `Evidence` (raw `content_ref`).
- **Output spec** `derived` — Segmented, span-tagged normalized units (addressable text with source offsets).
- **Required entities** `canonical` — `Evidence`; (working units precede `ContextItem`).
- **Required fields** `derived` — Per unit: source `evidence_id` + character offsets (span); normalized text.
- **Entry criteria** `derived` — Input set assembled (Stage 0 exit).
- **Exit criteria** `derived` — All evidence segmented with span attribution.
- **Rule responsibilities** `derived` — Document parsing, boilerplate stripping, sentence/unit segmentation, span tagging, encoding normalization.
- **LLM responsibilities** — none.
- **Validation rules** `derived` — Every normalized unit must retain a resolvable source span; no unit without provenance.
- **Fallback/failure behavior** `derived` — Unparseable evidence ⇒ skip with a recorded parse-warning; continue with remaining inputs (do not fail the run).
- **Events emitted** — none (internal).
- **State transitions** — none (run remains `queued`/`running`).
- **Traceability requirements** `canonical` — Span fidelity is mandatory (explainability to basis).
- **Open decisions** — Segmentation granularity (`TBD`).

---

## Stage 2 — Global Skeleton

- **Purpose** `proposal` — Build a compact global representation (intent restatement, claim/entity index, relationship skeleton, cross-references) so later isolated evaluations are globally informed. *(Resolves the chunking-vs-global-understanding tension; PROPOSAL — see CONSOLIDATED_ARCHITECTURE_GUIDELINES.)*
- **Owner layer/component** `derived` — Context Plane (index build) + Planning Intelligence reasoning executed by Analysis Engine (semantic synthesis).
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Normalized units (full corpus; ≤ envelope ⇒ single model context, no capacity chunking).
- **Output spec** `proposal` — Global map: restated intent, entity index, relationship skeleton, cross-reference list; persisted as deep/fast-horizon `ContextItem`s where applicable.
- **Required entities** `canonical` — `ContextItem` (item_type ∈ {entity, relationship, claim, …}).
- **Required fields** `canonical` — `context_item_id`, `project_id`, `item_type`, `extraction_horizon=fast`, `produced_by_run_id`, `content`, `source_attribution`.
- **Entry criteria** `derived` — Normalization complete.
- **Exit criteria** `proposal` — Global map available to Stages 3–6.
- **Rule responsibilities** `proposal` — Entity index (NER), term/keyword index, cross-reference linking by repeated-entity match.
- **LLM responsibilities** `proposal` — Intent restatement; relationship-skeleton semantics (low output volume).
- **Validation rules** `proposal` — LLM output validated against a fixed schema; entities/relationships must reference source spans; reject items lacking attribution.
- **Fallback/failure behavior** `derived` — Skeleton failure ⇒ degrade to Stage-3 isolation-only with **reduced reliability** (Reliability ↓ via Coverage), not run failure.
- **Events emitted** — none (internal).
- **State transitions** — run → `running` (if not already).
- **Traceability requirements** `derived` — Every map element links to source spans; basis preserved.
- **Open decisions** — Whether the global skeleton is adopted; skeleton output budget (`TBD`).

---

## Stage 3 — Claim Extraction

- **Purpose** `canonical` — Extract the bounded salient claim subset for orientation (fast horizon; not exhaustive).
- **Owner layer/component** `canonical` — Planning Intelligence reasoning executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Normalized units + global map (Stage 2) as shared context.
- **Output spec** `canonical` — `ContextItem`s of `item_type=claim` (`extraction_horizon=fast`), each with attributes per RULE_LLM_GUIDELINES / claim contract.
- **Required entities** `canonical` — `ContextItem`.
- **Required fields** `canonical` + `proposal` — `context_item_id`, `project_id`, `evidence_id`, `item_type=claim`, `extraction_horizon=fast`, `produced_by_run_id`, `content`, `source_attribution`; **proposed claim attributes**: verbatim_span, normalized_text, modality, support_status, clarity flags, dedup_key *(proposal — not yet Data Model fields; see OPEN_DECISIONS)*.
- **Entry criteria** `derived` — Normalization complete (Stage 2 optional but recommended).
- **Exit criteria** `proposal` — Bounded claim set produced (target ≈ **50–100** salient claims — **proposal/TBD**).
- **Rule responsibilities** `proposal` — Assertion pre-filter (modal/declarative patterns) to bound LLM load; dedup_key/hash for dedup + determinism.
- **LLM responsibilities** `canonical` — Identify claims incl. paraphrased/implicit; produce normalized_text.
- **Validation rules** `proposal` — Each claim must carry a resolvable source span; output schema-validated; duplicates collapsed by dedup_key.
- **Fallback/failure behavior** `derived` — Extraction failure ⇒ run `failed`; retry = new run (`previous_run_id`).
- **Events emitted** — none at stage; claims surface via `finding_created` downstream and `fast_analysis_completed`.
- **State transitions** — run `running`.
- **Traceability requirements** `canonical` — `first_seen_run_id` set; `evidence_links`/span retained.
- **Open decisions** — Fast claim-count bound; per-claim output budget; model tier (`TBD`).

---

## Stage 4 — CAF Evaluation

- **Purpose** `canonical` — Assess Clarity, Alignment, Feasibility on the (shallow) understanding; qualify each by reliability.
- **Owner layer/component** `canonical` — Planning Intelligence (reasoning) executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Fast claims + global map; evidence/context.
- **Output spec** `canonical` — One `CAFState` (per-dimension assessed level + per-dimension reliability qualifier).
- **Required entities** `canonical` — `CAFState`.
- **Required fields** `canonical` + `proposal` — `caf_state_id`, `analysis_run_id`, `project_id`, `clarity_index`, `alignment_index`, `feasibility_index`, `clarity_reliability`, `alignment_reliability`, `feasibility_reliability`; **proposed**: per-dimension `evaluation_completeness`, `contributing_findings` *(proposal — see OPEN_DECISIONS)*.
- **Entry criteria** `derived` — Claims available (Stage 3).
- **Exit criteria** `canonical` — CAFState produced with all three dimensions reliability-qualified.
- **Rule responsibilities** `proposal` — Intrinsic Clarity detectors (vagueness lexicon, missing units, unsupported-assertion graph check); constraint extraction (dates/budgets); coverage-gap set-difference vs the 8 artifact types.
- **LLM responsibilities** `canonical` — Relational Alignment/Feasibility judgment (preliminary in Fast).
- **Validation rules** `canonical` — **No formula/weight/threshold may be introduced** (CAF/Reliability models). Alignment/Feasibility must be marked lower-reliability when evaluated without full relational context.
- **Fallback/failure behavior** `derived` — Partial CAF ⇒ emit with reduced reliability rather than fail.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `derived` — Each dimension explainable from contributing findings/claims; reliability explainable by Coverage/Evidence Availability/Assessability (Reliability Model §11).
- **Open decisions** — CAF assessed-level scale; reliability scale (`TBD`).

---

## Stage 5 — Finding Generation

- **Purpose** `canonical` — Emit initial descriptive findings (7-type taxonomy) from the evaluation.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid` (detection in Stage 4 may be rule; emission is `rule`).
- **Input spec** `derived` — CAF evaluation results + claims + basis links.
- **Output spec** `canonical` — `Finding`s with `status=detected`.
- **Required entities** `canonical` — `Finding`.
- **Required fields** `canonical` — `finding_id`, `project_id`, `first_seen_run_id`, `finding_type` ∈ {missing_information, ambiguity, assumption, inference, conflict, constraint, coverage_gap}, `affected_dimensions`, `severity` ∈ {critical, moderate, warning}, `status=detected`, `evidence_links`.
- **Entry criteria** `derived` — CAFState produced.
- **Exit criteria** `canonical` — Initial findings persisted; each basis-linked.
- **Rule responsibilities** `derived` — Object assembly (type, dimension, basis links); severity heuristic *(severity basis = `TBD`)*.
- **LLM responsibilities** `derived` — Only where detection required semantic judgment (Stage 4).
- **Validation rules** `canonical` — Findings are **descriptive only** (no prescriptive content); every finding must link to ≥1 evidence/claim.
- **Fallback/failure behavior** `derived` — Emission failure ⇒ run `failed`; atomic publication (Stage 8) prevents partial commit.
- **Events emitted** `canonical` — `finding_created` (×N, on publication).
- **State transitions** `canonical` — Finding → `detected`.
- **Traceability requirements** `canonical` — `first_seen_run_id` + `evidence_links` mandatory.
- **Open decisions** — Severity assignment basis (`TBD`).

---

## Stage 6 — Recommendation Generation

- **Purpose** `canonical` — Generate initial advisory recommendations from findings.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Findings + basis.
- **Output spec** `canonical` — `Recommendation`s with `status=generated`.
- **Required entities** `canonical` — `Recommendation`.
- **Required fields** `canonical` — `recommendation_id`, `project_id`, `finding_id`, `first_seen_run_id`, `recommendation_type` ∈ {improvement, validation, suggested_fix}, `status=generated`, `rationale`, `expected_dimension`.
- **Entry criteria** `derived` — Findings exist.
- **Exit criteria** `canonical` — Recommendations persisted, each tied to a finding.
- **Rule responsibilities** `proposal` — Finding-type → recommendation-type selection (near-deterministic mapping).
- **LLM responsibilities** `derived` — Rationale phrasing.
- **Validation rules** `canonical` — Recommendations are **advisory only**; never auto-applied; must reference a `finding_id`.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed` (atomic).
- **Events emitted** `canonical` — `recommendation_created` (×M, on publication).
- **State transitions** `canonical` — Recommendation → `generated`.
- **Traceability requirements** `canonical` — `finding_id` + `first_seen_run_id` mandatory.
- **Open decisions** — none beyond rationale-quality calibration.

---

## Stage 7 — Confidence & State

- **Purpose** `canonical` — Produce the reliability-qualified Outcome Confidence summary of CAF.
- **Owner layer/component** `canonical` — Planning Intelligence (Confidence/Reliability models) executed by Analysis Engine.
- **Execution type** — `rule` mechanics (assembly); confidence **synthesis method = `TBD`** (formula-free; may involve bounded LLM judgment — owner decision).
- **Input spec** `canonical` — CAFState + reliability (Coverage/Evidence Availability/Assessability).
- **Output spec** `canonical` — One `ConfidenceState` (reliability-qualified summary).
- **Required entities** `canonical` — `ConfidenceState`.
- **Required fields** `canonical` — `confidence_state_id`, `analysis_run_id`, `project_id`, `outcome_confidence_value`, `confidence_band` ∈ {very_low, low, moderate, high, very_high}, `reliability_qualifier`, `supersedes_confidence_state_id` (null on first run).
- **Entry criteria** `canonical` — CAFState exists.
- **Exit criteria** `canonical` — ConfidenceState produced; never a bare value (always reliability-qualified).
- **Rule responsibilities** `derived` — State assembly; supersession pointer; reliability-qualifier attachment.
- **LLM responsibilities** — none mandated (synthesis method TBD).
- **Validation rules** `canonical` — Confidence **derived from CAF + Reliability only**; not primary; **no weights/percentages/thresholds/formula** introduced.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed` (atomic).
- **Events emitted** `canonical` — `confidence_created` (on publication; first run has no supersede).
- **State transitions** `canonical` — ConfidenceState → current.
- **Traceability requirements** `canonical` — Links to `analysis_run_id`; reliability explainable by its basis.
- **Open decisions** — CAF→Confidence synthesis method; confidence value scale; reliability scale (`TBD`).

---

## Stage 8 — MRI & Publication

- **Purpose** `canonical` — Build the MRI visualization, atomically persist all outputs, and publish the orientation.
- **Owner layer/component** `canonical` — Analysis Engine (publication); Knowledge Layer (canonical store).
- **Execution type** — `rule`.
- **Input spec** `derived` — CAFState, ConfidenceState, findings, recommendations.
- **Output spec** `canonical` — `MRISnapshot`; completed `AnalysisRun`; published orientation.
- **Required entities** `canonical` — `MRISnapshot`, `AnalysisRun`, plus all Stage 3–7 outputs.
- **Required fields** `canonical` — `mri_snapshot_id`, `analysis_run_id`; run `completed_at`, `run_status=completed`.
- **Entry criteria** `derived` — Stages 3–7 outputs ready.
- **Exit criteria** `canonical` — Atomic, all-or-nothing publication (Engine §20); run `completed`; orientation available.
- **Rule responsibilities** `derived` — MRI render from structured outputs; atomic persist; event emission; state transition.
- **LLM responsibilities** — none.
- **Validation rules** `canonical` — **No partial commit** — publish all outputs or none; orientation labeled **"not final — Deep Analysis to follow."**
- **Fallback/failure behavior** `canonical` — Publication failure ⇒ run `failed`; Project reverts to `created` (no half-written state).
- **Events emitted** `canonical` — `fast_analysis_completed` → ordered fan-out `confidence_created` → `finding_created` → `recommendation_created` → `notification_created` (Event Model §16). On completion, prior current run (if any) → `analysis_superseded`.
- **State transitions** `canonical` — Project `orienting → oriented`; run → `completed`.
- **Traceability requirements** `canonical` — Single `correlation_id` across the fan-out; full lineage persisted.
- **Open decisions** — none.

---

## Fast Pass budget roll-up (proposal — load-test pending)

| Stage | Exec | Budget (proposal) |
|---|---|---|
| 0 Intake | rule | 2–4s |
| 1 Normalization | rule | 2–3s |
| 2 Global skeleton | hybrid | 8–10s |
| 3 Claim extraction | hybrid | 12–17s |
| 4 CAF evaluation | hybrid | 10–14s (overlaps 3) |
| 5 Finding generation | rule/hybrid | ~1s |
| 6 Recommendation generation | hybrid | 4–6s |
| 7 Confidence & state | rule | 1–3s |
| 8 MRI & publication | rule | 3–5s |
| **Target (canonical)** | | **< 60s Time-to-First-MRI** |
| **Effective with overlap (proposal)** | | ~40–50s |

*All budgets `proposal`; the < 60s ceiling is `canonical` (NFR §3). Queue-time counts against the budget (NFR §18).*
