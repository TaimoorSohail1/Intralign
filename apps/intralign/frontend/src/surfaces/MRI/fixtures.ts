/**
 * MRI fixtures — governed-object DTOs (Data Model v1.2) used to drive the MRI
 * surface and its sub-components in tests and as the mocked shape of the DTM-0018
 * Orval hooks. These mirror the generated DTO types VERBATIM (no invented fields);
 * MRI presents them read-only and never recomputes them.
 *
 * Every Derived DTO carries its `label` (DerivedEnvelope) so the surface can hand
 * it to `fromDerivedEnvelope` → `EpistemicLabel` (decision #5).
 */
import type {
  Finding,
  CAFState,
  ConfidenceState,
  AnalysisRun,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

/**
 * Findings spanning the MRI Experience categories (§E):
 *   Missing    ← missing_information, coverage_gap
 *   Risky      ← assumption, inference, conflict, constraint
 *   Incomplete ← ambiguity
 * Each is a Derived projection carrying its epistemic envelope.
 */
export const findingsFixture: Finding[] = [
  {
    finding_id: "f-missing-1",
    project_id: PROJECT_ID,
    finding_type: "missing_information",
    severity: "critical",
    status: "detected",
    summary: "No success criteria are recorded for the launch milestone.",
    affected_dimensions: ["clarity"],
    label: {
      epistemic_label: "derived",
      confidence_band: "low",
      confidence_value: 30,
      conflict_state: "none",
      current_chr_ref: "chr-r2-001",
    },
  },
  {
    finding_id: "f-missing-2",
    project_id: PROJECT_ID,
    finding_type: "coverage_gap",
    severity: "warning",
    status: "acknowledged",
    summary: "The data-migration workstream has no coverage in scope.",
    affected_dimensions: ["feasibility"],
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 60,
      conflict_state: "none",
      current_chr_ref: "chr-r2-002",
    },
  },
  {
    finding_id: "f-risky-1",
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
      // an unresolved conflict — surfaced, never resolved by MRI
      conflict_state: "contested",
      current_chr_ref: "chr-r2-003",
    },
  },
  {
    finding_id: "f-risky-2",
    project_id: PROJECT_ID,
    finding_type: "assumption",
    severity: "moderate",
    status: "detected",
    summary: "Budget is assumed approved; no attested confirmation found.",
    affected_dimensions: ["feasibility"],
    label: {
      epistemic_label: "derived",
      confidence_band: "low",
      confidence_value: 40,
      conflict_state: "none",
      current_chr_ref: "chr-r2-004",
    },
  },
  {
    finding_id: "f-incomplete-1",
    project_id: PROJECT_ID,
    finding_type: "ambiguity",
    severity: "moderate",
    status: "detected",
    summary: '"Soon" is used for the rollout window without a date.',
    affected_dimensions: ["clarity"],
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 62,
      conflict_state: "none",
      current_chr_ref: "chr-r2-005",
    },
  },
];

/** CAF — three co-equal dimensions, each a (index · band · reliability) triple. */
export const cafFixture: CAFState = {
  project_id: PROJECT_ID,
  clarity: { dimension: "clarity", index: 42, band: "low", reliability: "qualified" },
  alignment: {
    dimension: "alignment",
    index: 68,
    band: "medium",
    reliability: "established",
  },
  feasibility: {
    dimension: "feasibility",
    index: 80,
    band: "high",
    reliability: "established",
  },
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 63,
    conflict_state: "none",
    current_chr_ref: "chr-r2-caf",
  },
};

/** Outcome Confidence — trust-in-understanding, banded, reliability-qualified. */
export const confidenceFixture: ConfidenceState = {
  project_id: PROJECT_ID,
  confidence_state_id: "cs-002",
  confidence_band: "medium",
  outcome_confidence_value: 64,
  reliability_qualifier: "qualified",
  basis: ["3 attested evidence items", "2 open conflicts"],
  false_confidence_flagged: false,
  created_at: "2026-06-20T10:00:00Z",
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 64,
    conflict_state: "none",
    current_chr_ref: "chr-r2-conf",
  },
};

/**
 * Analysis runs — the history trail the Understanding Timeline (MRI-06) reads,
 * newest first. Presentation is append-only: the latest is the current
 * understanding; the prior runs are retained history.
 */
export const analysisRunsFixture: AnalysisRun[] = [
  {
    analysis_run_id: "run-2",
    project_id: PROJECT_ID,
    run_type: "deep_analysis_pass",
    run_status: "completed",
    previous_run_id: "run-1",
    started_at: "2026-06-20T09:55:00Z",
    completed_at: "2026-06-20T10:00:00Z",
  },
  {
    analysis_run_id: "run-1",
    project_id: PROJECT_ID,
    run_type: "fast_analysis_pass",
    run_status: "completed",
    started_at: "2026-06-19T08:00:00Z",
    completed_at: "2026-06-19T08:00:45Z",
  },
];
