/**
 * Assisted Editing / Persistent Intelligence fixtures (DTM-0029, AW-04/05).
 *
 * Mirror the generated DTO types VERBATIM (no invented fields). These are the mocked
 * shape of the DTM-0018 Orval reads the panel consumes READ-ONLY:
 *   - useGetConfidence…       (GET /projects/{pid}/confidence)      — Outcome Confidence
 *   - useGetCaf…              (GET /projects/{pid}/caf)             — CAF (C/A/F)
 *   - useListAnalysisRuns…    (GET /projects/{pid}/analysis-runs)   — Understanding-State
 *
 * UNDERSTANDING-STATE DATA FINDING (binding — see the worker report): there is NO
 * aggregate "understanding state" / "orientation state" DTO and NO is_stale flag in the
 * DTM-0018 REST surface. AW-04/05 names "Understanding-State"; we derive it from the
 * governed `AnalysisRun` list exactly as the Companion does — a latest run with
 * `run_status: "superseded"` is, by its own governed status, no-longer-current
 * understanding ("based on the previous analysis"). We invent no state flag.
 */
import type {
  ConfidenceState,
  CAFState,
  AnalysisRun,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";
export const ARTIFACT_ID = "artf-001";

/** Outcome Confidence (Derived; banded, reliability-qualified). */
export const confidenceFixture: ConfidenceState = {
  project_id: PROJECT_ID,
  confidence_state_id: "cs-001",
  confidence_band: "medium",
  outcome_confidence_value: 64,
  reliability_qualifier: "Moderate reliability",
  basis: ["Coverage partial"],
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 64,
    conflict_state: "none",
    current_chr_ref: "chr-cs-001",
  },
};

/** CAF — three co-equal dimensions, each Derived/banded. */
export const cafFixture: CAFState = {
  project_id: PROJECT_ID,
  clarity: { dimension: "clarity", index: 78, band: "high", reliability: "High reliability" },
  alignment: {
    dimension: "alignment",
    index: 35,
    band: "low",
    reliability: "Moderate reliability",
  },
  feasibility: {
    dimension: "feasibility",
    index: 60,
    band: "medium",
    reliability: "Moderate reliability",
  },
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 64,
    conflict_state: "none",
    current_chr_ref: "chr-caf-001",
  },
};

/** Current understanding — latest run completed (Understanding-State = current). */
export const runsCurrentFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-002",
    project_id: PROJECT_ID,
    run_type: "deep_analysis_pass",
    run_status: "completed",
    started_at: "2026-06-24T10:00:00Z",
    completed_at: "2026-06-24T10:02:00Z",
    previous_run_id: "run-001",
  },
];

/** Stale understanding — latest run superseded (Understanding-State = previous analysis). */
export const runsStaleFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-001",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "superseded",
    started_at: "2026-06-20T10:00:00Z",
    completed_at: "2026-06-20T10:01:00Z",
  },
];
