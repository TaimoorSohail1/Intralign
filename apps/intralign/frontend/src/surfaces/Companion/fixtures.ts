/**
 * Understanding Companion fixtures (DTM-0025, IC-WE-DISCLOSE E1).
 *
 * These mirror the generated DTO types VERBATIM (no invented fields). They are the
 * mocked shape of the DTM-0018 Orval reads the Companion consumes read-only:
 *   - `useGetConfidence…`      (GET /projects/{pid}/confidence)   — Outcome Confidence
 *   - `useGetCaf…`             (GET /projects/{pid}/caf)          — CAF summary
 *   - `useListFindings…`       (GET /projects/{pid}/findings)     — Top Findings
 *   - `useListRecommendations…`(GET /projects/{pid}/recommendations) — Top Recommendations
 *   - `useListAnalysisRuns…`   (GET /projects/{pid}/analysis-runs) — stale-analysis state
 *
 * THE STALE-STATE DATA FINDING (binding to this slice — see the worker report):
 * there is **no aggregate "companion" / "understanding state" DTO** and **no
 * boolean "is_stale" field** in the DTM-0018 REST surface. The Companion presents
 * "Previous Analysis" by reading the governed `AnalysisRun` list: a run carrying
 * `run_status: "superseded"` is, by the governed object's own status, no-longer-
 * current understanding. We do NOT invent a stale flag — the gap is flagged, not
 * filled; the marker is a presentation of the governed run status.
 *
 * THE OPTION-B DATA FACT: each `Recommendation` DTO carries its `finding_id` (the
 * Finding it is anchored to — "Recommendation-only-in-Finding-context"). That is
 * exactly the field the Companion routes through to reach a Recommendation via its
 * associated Finding (Option B / RP-C1) — never a standalone Recommendation Panel.
 */
import type {
  ConfidenceState,
  CAFState,
  Finding,
  Recommendation,
  AnalysisRun,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

/** Outcome Confidence (Derived; banded, reliability-qualified) — trust-in-understanding. */
export const companionConfidenceFixture: ConfidenceState = {
  project_id: PROJECT_ID,
  confidence_state_id: "cs-001",
  confidence_band: "medium",
  outcome_confidence_value: 66,
  reliability_qualifier: "Moderate reliability",
  basis: ["Coverage partial", "Alignment provisional"],
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 66,
    conflict_state: "none",
    current_chr_ref: "chr-cs-001",
  },
};

/** CAF — three co-equal dimensions, each Derived/banded. */
export const companionCafFixture: CAFState = {
  project_id: PROJECT_ID,
  clarity: { dimension: "clarity", index: 72, band: "medium", reliability: "High reliability" },
  alignment: { dimension: "alignment", index: 40, band: "low", reliability: "Moderate reliability" },
  feasibility: {
    dimension: "feasibility",
    index: 85,
    band: "high",
    reliability: "High reliability",
  },
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 66,
    conflict_state: "none",
    current_chr_ref: "chr-caf-001",
  },
};

/**
 * Top Findings — the most relevant existing findings. The first is contested → it
 * carries a conflict marker (presented, not resolved). Each links to its Finding
 * Panel (Q5). The `low` (band-low) fixture is here to prove the band is carried
 * VERBATIM (never upgraded to high).
 */
export const companionFindingsFixture: Finding[] = [
  {
    finding_id: "f-1",
    project_id: PROJECT_ID,
    finding_type: "conflict",
    severity: "critical",
    status: "detected",
    summary: "Two stakeholders state conflicting go-live dates.",
    affected_dimensions: ["alignment"],
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 55,
      conflict_state: "contested",
      current_chr_ref: "chr-f-1",
    },
  },
  {
    finding_id: "f-2",
    project_id: PROJECT_ID,
    finding_type: "missing_information",
    severity: "warning",
    status: "detected",
    summary: "No success criteria recorded for the launch milestone.",
    affected_dimensions: ["clarity"],
    label: {
      epistemic_label: "derived",
      confidence_band: "low",
      confidence_value: 30,
      conflict_state: "none",
      current_chr_ref: "chr-f-2",
    },
  },
];

/**
 * Top Recommendations — Derived advisory candidates, each ANCHORED TO A FINDING via
 * `finding_id` (Recommendation-only-in-Finding-context). This is the field the
 * Companion routes through for Option B: select a recommendation → open its
 * associated Finding Panel (never a standalone Recommendation Panel).
 */
export const companionRecommendationsFixture: Recommendation[] = [
  {
    recommendation_id: "r-1",
    project_id: PROJECT_ID,
    finding_id: "f-1",
    title: "Confirm the go-live date with both stakeholders",
    recommendation_type: "validation",
    status: "generated",
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 58,
      conflict_state: "none",
      current_chr_ref: "chr-r-1",
    },
  },
  {
    recommendation_id: "r-2",
    project_id: PROJECT_ID,
    finding_id: "f-2",
    title: "Record explicit success criteria for the launch milestone",
    recommendation_type: "suggested_fix",
    status: "generated",
    label: {
      epistemic_label: "derived",
      confidence_band: "low",
      confidence_value: 32,
      conflict_state: "none",
      current_chr_ref: "chr-r-2",
    },
  },
];

/**
 * Analysis runs — CURRENT understanding (latest run completed). No superseded run,
 * so the Companion presents NO "Previous Analysis" marker (understanding is current).
 */
export const companionRunsCurrentFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-002",
    project_id: PROJECT_ID,
    run_type: "deep_analysis_pass",
    run_status: "completed",
    started_at: "2026-06-24T10:00:00Z",
    completed_at: "2026-06-24T10:02:00Z",
    previous_run_id: "run-001",
  },
  {
    analysis_run_id: "run-001",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "superseded",
    started_at: "2026-06-20T10:00:00Z",
    completed_at: "2026-06-20T10:01:00Z",
  },
];

/**
 * Analysis runs — STALE understanding: the latest run is itself `superseded` (its
 * results are governed-marked as no-longer-current). The Companion prominently
 * surfaces this as "Previous Analysis" and never presents it as current (Q8 / COMP-11).
 */
export const companionRunsStaleFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-001",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "superseded",
    started_at: "2026-06-20T10:00:00Z",
    completed_at: "2026-06-20T10:01:00Z",
  },
];
