/**
 * Export / Share-out fixtures (DTM-0028, IC-WE-DISCLOSE E1).
 *
 * These mirror the generated DTO types VERBATIM (no invented fields). They are the
 * mocked shape of the DTM-0018 Orval reads the Export packages read-only:
 *   - `useGetProjectV1ProjectsProjectIdGet`        (project name / context)
 *   - `useGetConfidenceV1ProjectsProjectIdConfidenceGet` (Outcome Confidence)
 *   - `useGetCafV1ProjectsProjectIdCafGet`         (CAF summary)
 *   - `useListFindingsV1ProjectsProjectIdFindingsGet`     (findings — descriptive)
 *   - `useListRecommendationsV1ProjectsProjectIdRecommendationsGet` (recs — advisory)
 *   - `useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet` (analysis-currency marker)
 *   - `useListAcceptancesV1ProjectsProjectIdAcceptanceGet`  (UARs — user-attested)
 *   - `useListPlanFactsV1ProjectsProjectIdPlanFactsGet`     (plan facts — user-attested)
 *
 * THE NO-EXPORT-ENDPOINT DATA FINDING (binding — see the worker report): there is **no
 * server export / report / share endpoint** in the generated client. The export is
 * packaged CLIENT-SIDE from the already-fetched governed DTOs (Blob/anchor download +
 * in-app preview). We invent no server "export produced" claim.
 *
 * THE ANALYSIS-CURRENCY DATA FACT: there is no boolean `is_stale` field. "Previous
 * analysis" is read off the governed `AnalysisRun.run_status` (`superseded` ⇒ no-longer
 * current), exactly as the Companion/Timeline do — the gap is flagged, not filled.
 */
import type {
  Project,
  ConfidenceState,
  CAFState,
  Finding,
  Recommendation,
  AnalysisRun,
  UserAcceptanceRecord,
  PlanFact,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

export const exportProjectFixture: Project = {
  project_id: PROJECT_ID,
  workspace_id: "ws-1",
  lifecycle_state: "analyzed",
  title: "Apollo launch plan",
  description: "The Apollo product launch.",
  created_at: "2026-05-01T09:00:00Z",
  updated_at: "2026-05-20T08:02:10Z",
};

/** Outcome Confidence (Derived; banded, reliability-qualified) — trust-in-understanding. */
export const exportConfidenceFixture: ConfidenceState = {
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

/** CAF — three co-equal dimensions, each Derived/banded (qualitative). */
export const exportCafFixture: CAFState = {
  project_id: PROJECT_ID,
  clarity: { dimension: "clarity", index: 72, band: "medium", reliability: "High reliability" },
  alignment: {
    dimension: "alignment",
    index: 40,
    band: "low",
    reliability: "Moderate reliability",
  },
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
 * Findings — descriptive. The first is contested (conflict travels into the export);
 * the second is band-low (proves the band is carried VERBATIM, never upgraded to high).
 */
export const exportFindingsFixture: Finding[] = [
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

/** Recommendations — advisory candidates, each anchored to a Finding (`finding_id`). */
export const exportRecommendationsFixture: Recommendation[] = [
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

/** Analysis runs — CURRENT understanding (latest run completed). */
export const exportRunsCurrentFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-001",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "superseded",
    started_at: "2026-05-01T09:00:00Z",
    completed_at: "2026-05-01T09:00:42Z",
    previous_run_id: null,
  },
  {
    analysis_run_id: "run-002",
    project_id: PROJECT_ID,
    run_type: "deep_analysis_pass",
    run_status: "completed",
    started_at: "2026-05-20T08:00:00Z",
    completed_at: "2026-05-20T08:02:10Z",
    previous_run_id: "run-001",
  },
];

/**
 * Analysis runs — STALE: the latest run is itself `superseded` (governed-marked
 * no-longer-current). The export marks "previous analysis" and never presents it as
 * current (spec §J / EX-7).
 */
export const exportRunsStaleFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-001",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "superseded",
    started_at: "2026-05-20T10:00:00Z",
    completed_at: "2026-05-20T10:01:00Z",
    previous_run_id: null,
  },
];

/** UARs — what the user confirmed (user-attested, version-pinned). */
export const exportAcceptancesFixture: UserAcceptanceRecord[] = [
  {
    uar_id: "uar-001",
    project_id: PROJECT_ID,
    action: "accept",
    target_kind: "recommendation",
    version_pin: "chr-ref-aaa",
    epistemic_label: "attested-user",
    user_id: "user-1",
    confirmed_at: "2026-05-05T10:00:00Z",
    created_at: "2026-05-05T10:00:00Z",
  },
];

/** Plan facts — user-attested confirmed planning items (NOT world-truth). */
export const exportPlanFactsFixture: PlanFact[] = [
  {
    plan_fact_id: "pf-001",
    project_id: PROJECT_ID,
    proposition: "The launch milestone is fixed at 2026-09-01.",
    content_type: "milestone",
    version_pin: "chr-ref-aaa",
    attested_by_user: "user-1",
    epistemic_label: "attested-user",
    created_at: "2026-05-05T10:00:05Z",
  },
];
