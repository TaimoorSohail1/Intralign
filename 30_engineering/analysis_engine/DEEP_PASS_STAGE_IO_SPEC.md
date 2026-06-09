# Deep Pass — Stage I/O Specification

**Type:** Locked workflow spec — Deep Analysis Pass stages (expansion → supersession)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Authority order:** Planning Intelligence > State Model > Event Model > Data Model v1.1 > Analysis Engine > NFR > API/UI/Testing > Supporting models > Proposal notes
**Grounded in:** `PLANNING_INTELLIGENCE_SPECIFICATION_V1.md` §17 · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` §10 · Data Model v1.1 · State Model · Event Model · NFR.

> **Scope.** Active Release 1 only. The Deep Pass runs **after** orientation and **expands understanding**; it **performs no governance**. No accepted understanding, agent governance, autonomous execution, actuation, or outcome-orchestration runtime. No invented formulas/weights/percentages/thresholds. Prior outputs are **superseded, not deleted**. Deep timing targets are **`TBD – Owner Decision Required`** (only Fast has an approved target). Tags: `canonical` / `derived` / `proposal` / `TBD`.
>
> **Trigger (canonical).** A Deep run is requested on a qualifying event (orientation completion; substantive artifact/context change; fix applied; chat edit; collaboration-derived evidence; manual) when no deep run is currently `running`; rapid events are coalesced (Event Model §15). Project: `oriented`/`analyzed` → `deep_analyzing`. AnalysisRun: `run_type=deep_analysis_pass`, `previous_run_id` linked.

---

## Stage 1 — Context Expansion

- **Purpose** `canonical` — Deep-horizon extraction; enrich context items beyond the fast read.
- **Owner layer/component** `canonical` — Context Plane (deep extraction) feeding Planning Intelligence via Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Full evidence/artifacts; fast-horizon context; global map; prior run outputs.
- **Output spec** `canonical` — `ContextItem`s with `extraction_horizon=deep`.
- **Required entities** `canonical` — `ContextItem`.
- **Required fields** `canonical` — `context_item_id`, `project_id`, `evidence_id`, `item_type`, `extraction_horizon=deep`, `produced_by_run_id`, `content`, `source_attribution`.
- **Entry criteria** `canonical` — Orientation complete or qualifying event; no deep run running.
- **Exit criteria** `derived` — Enriched context available for later stages.
- **Rule responsibilities** `proposal` — Re-index entities/terms over full corpus; carry global map as shared context to parallel chunks.
- **LLM responsibilities** `canonical` — Deeper semantic extraction.
- **Validation rules** `proposal` — Items schema-validated; source spans required; dedup by dedup_key.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`; Project reverts to last completed state; retry = new run.
- **Events emitted** `canonical` — `deep_analysis_started` (at run begin).
- **State transitions** `canonical` — Project `deep_analyzing`; run `queued → running`.
- **Traceability requirements** `canonical` — Span + `produced_by_run_id`.
- **Open decisions** — Deep/parallel chunking strategy; coalescing window (`TBD`).

---

## Stage 2 — Relationship Expansion

- **Purpose** `canonical` — Extend the relationship web among claims/entities/artifacts.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Enriched context items + global skeleton.
- **Output spec** `canonical` — `ContextItem`s (`item_type=relationship`) / relationship links among claims.
- **Required entities** `canonical` — `ContextItem` (relationship).
- **Required fields** `canonical` + `proposal` — context-item fields; **proposed** relationship_links on claims *(see OPEN_DECISIONS)*.
- **Entry criteria** `derived` — Context expansion done.
- **Exit criteria** `derived` — Relationship web available to conflict discovery.
- **Rule responsibilities** `proposal` — Candidate links by shared-entity/reference matching.
- **LLM responsibilities** `canonical` — Relationship semantics (depends-on/refines/contradicts).
- **Validation rules** `proposal` — Links must reference existing claim/entity ids + spans; schema-validated.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `derived` — Links basis-traceable.
- **Open decisions** — Relationship-discovery depth limit (`TBD`).

---

## Stage 3 — Assumption Expansion

- **Purpose** `canonical` — Surface more/deeper assumptions in the enriched understanding.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Claims + relationships + evidence links.
- **Output spec** `derived` — Assumption-bearing claims / candidate Assumption findings.
- **Required entities** `canonical` — `ContextItem` (claim), `Finding` (assumption, later stages).
- **Required fields** `canonical` — claim fields; `support_status` *(proposal)*.
- **Entry criteria** `derived` — Relationship web available.
- **Exit criteria** `derived` — Assumptions identified for finding expansion.
- **Rule responsibilities** `proposal` — Flag claims with no evidence link (corpus-wide absence check via index).
- **LLM responsibilities** `canonical` — Judge implicit assumptions requiring semantics.
- **Validation rules** `derived` — Each assumption traces to the claim/absence that produced it.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `canonical` — basis links.
- **Open decisions** — none beyond support-status field adoption (`proposal`).

---

## Stage 4 — Conflict Discovery

- **Purpose** `canonical` — Discover contradictions revealed by the enriched relationship web (signature Deep activity).
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `llm` (relational reasoning; rule-assisted candidate pairing).
- **Input spec** `derived` — Claims + relationship web + intent.
- **Output spec** `canonical` — Candidate `Conflict` findings (Alignment).
- **Required entities** `canonical` — `Finding` (conflict).
- **Required fields** `canonical` — finding fields; `finding_type=conflict`, `affected_dimensions ⊇ {alignment}`.
- **Entry criteria** `derived` — Relationship web available.
- **Exit criteria** `derived` — Conflicts identified for expanded findings.
- **Rule responsibilities** `proposal` — Pair candidate claims for comparison (shared subject, opposing modality) to bound LLM work.
- **LLM responsibilities** `canonical` — Judge logical incompatibility / intent drift.
- **Validation rules** `canonical` — A conflict must cite both sides (the contradicting claims) as basis.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `canonical` — Both-sides basis mandatory.
- **Open decisions** — Bounded-equivalence tolerance for conflict detection (`TBD`).

---

## Stage 5 — Additional Claim Discovery

- **Purpose** `canonical` — Surface claims the fast horizon missed.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Full corpus + enriched context (deep horizon).
- **Output spec** `canonical` — Additional `ContextItem` claims (`extraction_horizon=deep`).
- **Required entities** `canonical` — `ContextItem` (claim).
- **Required fields** `canonical` — claim fields; `first_seen_run_id` = this deep run.
- **Entry criteria** `derived` — Context expansion done.
- **Exit criteria** `proposal` — Fuller claim set (toward the ~350–850 total estimate — **proposal/TBD**).
- **Rule responsibilities** `proposal` — Assertion pre-filter on previously-skipped units.
- **LLM responsibilities** `canonical` — Identify additional/implicit claims.
- **Validation rules** `proposal` — Dedup against existing claims by dedup_key; spans required.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `canonical` — `first_seen_run_id` marks expanded claims.
- **Open decisions** — Total claim-count bound; parallelism (`TBD`).

---

## Stage 6 — CAF Reassessment

- **Purpose** `canonical` — Re-evaluate Clarity/Alignment/Feasibility on the enriched understanding (reliability typically rises).
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Expanded claims, relationships, conflicts, assumptions.
- **Output spec** `canonical` — A new `CAFState` (supersedes prior as current; prior retained).
- **Required entities** `canonical` — `CAFState`.
- **Required fields** `canonical` — caf fields; per-dimension reliability now reflects fuller Coverage/Evidence Availability/Assessability.
- **Entry criteria** `derived` — Stages 1–5 complete.
- **Exit criteria** `canonical` — New CAFState with full relational evaluation of Alignment/Feasibility (higher reliability than Fast).
- **Rule responsibilities** `proposal` — Re-run intrinsic Clarity detectors over fuller set; recompute coverage-gap set difference.
- **LLM responsibilities** `canonical` — Full relational Alignment/Feasibility reasoning.
- **Validation rules** `canonical` — **No formula/weight/threshold**; reliability determined from Coverage/Evidence Availability/Assessability, independent of CAF (Reliability Model §6).
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`; prior CAFState remains current.
- **Events emitted** — none at stage.
- **State transitions** — run `running`.
- **Traceability requirements** `canonical` — dimension basis links; reliability basis.
- **Open decisions** — CAF scale; reliability scale (`TBD`).

---

## Stage 7 — Confidence Recalculation

- **Purpose** `canonical` — Produce a recalculated Outcome Confidence summarizing the reassessed CAF; supersede prior.
- **Owner layer/component** `canonical` — Planning Intelligence (Confidence/Reliability) executed by Analysis Engine.
- **Execution type** — `rule` mechanics; synthesis method `TBD`.
- **Input spec** `canonical` — New CAFState + reliability.
- **Output spec** `canonical` — A new `ConfidenceState` with `supersedes_confidence_state_id` → prior current.
- **Required entities** `canonical` — `ConfidenceState`.
- **Required fields** `canonical` — confidence fields; `supersedes_confidence_state_id` set.
- **Entry criteria** `canonical` — New CAFState exists.
- **Exit criteria** `canonical` — New current ConfidenceState; prior → superseded (retained).
- **Rule responsibilities** `derived` — Supersession chain maintenance; reliability-qualifier attachment.
- **LLM responsibilities** — none mandated.
- **Validation rules** `canonical` — Derived from CAF + Reliability only; **no formula/weight/threshold**; never a bare value.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed`; prior confidence remains current.
- **Events emitted** `canonical` — `confidence_recalculated` + `confidence_superseded` (on publication, Stage 10).
- **State transitions** `canonical` — New ConfidenceState current; prior superseded.
- **Traceability requirements** `canonical` — Supersession chain reconstructs the confidence trend.
- **Open decisions** — Synthesis method; scales (`TBD`).

---

## Stage 8 — Expanded Findings

- **Purpose** `canonical` — Emit findings first surfaced/deepened by this deep run (Expanded Findings).
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Conflicts, assumptions, additional claims, reassessed CAF.
- **Output spec** `canonical` — New `Finding`s (`first_seen_run_id` = this deep run); existing findings re-evaluated (may → `superseded`).
- **Required entities** `canonical` — `Finding`.
- **Required fields** `canonical` — finding fields; `first_seen_run_id` = deep run; `status` ∈ {detected, …, superseded}.
- **Entry criteria** `derived` — Discovery stages complete.
- **Exit criteria** `canonical` — Expanded findings persisted; superseded findings retained.
- **Rule responsibilities** `derived` — Object assembly; supersession flagging.
- **LLM responsibilities** `derived` — Where detection needed semantics (Stages 2–5).
- **Validation rules** `canonical` — Findings **descriptive**; superseded findings **retained, not deleted**; basis-linked.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed` (atomic at Stage 10).
- **Events emitted** `canonical` — `finding_created` (expanded), `finding_superseded` (on publication).
- **State transitions** `canonical` — New Finding → `detected`; replaced → `superseded`.
- **Traceability requirements** `canonical` — `first_seen_run_id` distinguishes expanded findings.
- **Open decisions** — Expansion prioritization/ordering (`TBD`).

---

## Stage 9 — Expanded Recommendations

- **Purpose** `canonical` — Generate recommendations for new/updated findings.
- **Owner layer/component** `canonical` — Planning Intelligence executed by Analysis Engine.
- **Execution type** — `hybrid`.
- **Input spec** `derived` — Expanded findings.
- **Output spec** `canonical` — New `Recommendation`s; prior may → `superseded`.
- **Required entities** `canonical` — `Recommendation`.
- **Required fields** `canonical` — recommendation fields; `first_seen_run_id` = deep run.
- **Entry criteria** `derived` — Expanded findings exist.
- **Exit criteria** `canonical` — Expanded recommendations persisted; superseded retained.
- **Rule responsibilities** `proposal` — Finding-type → recommendation-type mapping.
- **LLM responsibilities** `derived` — Rationale phrasing.
- **Validation rules** `canonical` — Advisory only; tied to a finding; superseded retained.
- **Fallback/failure behavior** `derived` — Failure ⇒ run `failed` (atomic).
- **Events emitted** `canonical` — `recommendation_created` (expanded), `recommendation_superseded`.
- **State transitions** `canonical` — New → `generated`; replaced → `superseded`.
- **Traceability requirements** `canonical` — `finding_id` + `first_seen_run_id`.
- **Open decisions** — none beyond prioritization (`TBD`).

---

## Stage 10 — Publication & Supersession

- **Purpose** `canonical` — Atomically publish expanded outputs; supersede prior assessment while preserving history.
- **Owner layer/component** `canonical` — Analysis Engine (publication); Knowledge Layer (canonical store).
- **Execution type** — `rule`.
- **Input spec** `derived` — New CAFState, ConfidenceState, expanded findings/recommendations, MRI.
- **Output spec** `canonical` — Completed deep `AnalysisRun`; updated current pointers; retained superseded chain.
- **Required entities** `canonical` — `AnalysisRun`, `MRISnapshot`, all expanded outputs.
- **Required fields** `canonical` — run `run_status=completed`, `completed_at`; supersession pointers on prior run/states.
- **Entry criteria** `derived` — Stages 6–9 outputs ready.
- **Exit criteria** `canonical` — Atomic all-or-nothing publication (Engine §20); run `completed`; Project `deep_analyzing → analyzed`.
- **Rule responsibilities** `derived` — Atomic persist; supersession pointer updates; event fan-out; MRI refresh.
- **LLM responsibilities** — none.
- **Validation rules** `canonical` — **No partial commit**; **prior outputs superseded, not deleted**.
- **Fallback/failure behavior** `canonical` — Failure ⇒ run `failed`; Project stays at prior `analyzed`/`oriented`; expanded results simply not added.
- **Events emitted** `canonical` — `deep_analysis_completed` → ordered fan-out (`confidence_recalculated` + `confidence_superseded` → expanded `finding_created`/`finding_superseded` → expanded `recommendation_created`/`recommendation_superseded` → `notification_created`); prior current run → `analysis_superseded`.
- **State transitions** `canonical` — Project `deep_analyzing → analyzed` (recurs on new events); run → `completed`; prior → `superseded`.
- **Traceability requirements** `canonical` — Single `correlation_id`; supersession chains reconstruct full history (replay).
- **Open decisions** — Deep timeout, retry bound, debounce window (`TBD`).

---

## Deep Pass notes (proposal)

- **Timing:** Deep completion target, timeout, and debounce window are **`TBD – Owner Decision Required`** (NFR §4). Deep is async, coalesced, single-active-per-project; oversized inputs (above the Fast envelope) are fully analyzed here via parallel chunking carrying the global map (CONSOLIDATED_ARCHITECTURE_GUIDELINES).
- **Recurrence:** Deep recurs as evidence/action accumulate; each run supersedes prior assessment while preserving history.
- **No governance:** expansion only — no acceptance, disposition, or accepted understanding.
