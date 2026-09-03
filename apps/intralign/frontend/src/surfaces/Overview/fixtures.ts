/**
 * Project Overview + Dashboard / Project List fixtures (DTM-0024, IC-WE-DISCLOSE E1).
 *
 * These mirror the generated DTO types VERBATIM (no invented fields). They are the
 * mocked shape of the DTM-0018 Orval hooks the two surfaces consume read-only:
 *   - Dashboard       → `useListProjects…`     (GET /projects)
 *                       `useGetConfidence…`    (GET /projects/{pid}/confidence — per row)
 *   - Project Overview → `useGetConfidence…`   (GET /projects/{pid}/confidence)
 *                        `useGetCaf…`          (GET /projects/{pid}/caf)
 *                        `useListFindings…`    (GET /projects/{pid}/findings)
 *                        `useListRecommendations…` (GET /projects/{pid}/recommendations)
 *
 * THE COUNTS-DATA FINDING (binding to this slice — see the worker report): there is
 * **no aggregate "overview" / "counts" DTO** in the DTM-0018 REST surface — no field
 * carries findings/issues/recommendations totals. The Project Overview therefore
 * derives the counts by PRESENTING the length of the already-governed list reads
 * (findings, the subset of findings that are issues = a Finding with a severity, and
 * recommendations). A count is a count OF governed objects — never a computed score
 * or a health metric. We do NOT invent a counts endpoint — the gap is flagged.
 */
import type {
  Project,
  ConfidenceState,
  CAFState,
  Finding,
  Recommendation,
  Overview,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

// ── Dashboard / Project List ────────────────────────────────────────────────────

/** Three workspace projects across lifecycle states (presented, never computed). */
export const projectsFixture: Project[] = [
  {
    project_id: "proj-001",
    workspace_id: "ws-1",
    title: "Atlas platform migration",
    description: "Lift the legacy platform onto the new runtime.",
    lifecycle_state: "analyzed",
    current_confidence_state_id: "cs-001",
    created_at: "2026-05-01T10:00:00Z",
    updated_at: "2026-06-20T12:00:00Z",
  },
  {
    project_id: "proj-002",
    workspace_id: "ws-1",
    title: "Q3 onboarding revamp",
    description: "Rework the first-run onboarding flow.",
    lifecycle_state: "oriented",
    current_confidence_state_id: "cs-002",
    created_at: "2026-05-10T10:00:00Z",
    updated_at: "2026-06-18T09:00:00Z",
  },
  {
    project_id: "proj-003",
    workspace_id: "ws-1",
    title: "Compliance evidence pack",
    description: "Assemble the audit evidence package.",
    lifecycle_state: "created",
    created_at: "2026-06-22T10:00:00Z",
    updated_at: "2026-06-22T10:00:00Z",
  },
];

/**
 * Per-project current Outcome Confidence, keyed by project id (the Dashboard fetches
 * one per row). proj-003 has none yet (created, not analyzed) → its row presents a
 * clean "not yet available" instead of a fabricated value.
 */
export const confidenceByProject: Record<string, ConfidenceState | undefined> = {
  "proj-001": {
    project_id: "proj-001",
    confidence_state_id: "cs-001",
    confidence_band: "high",
    outcome_confidence_value: 82,
    reliability_qualifier: "High reliability",
    basis: ["Coverage broad", "Evidence available"],
    label: {
      epistemic_label: "derived",
      confidence_band: "high",
      confidence_value: 82,
      conflict_state: "none",
      current_chr_ref: "chr-cs-001",
    },
  },
  "proj-002": {
    project_id: "proj-002",
    confidence_state_id: "cs-002",
    confidence_band: "low",
    outcome_confidence_value: 34,
    reliability_qualifier: "Moderate reliability",
    basis: ["Alignment provisional"],
    label: {
      epistemic_label: "derived",
      confidence_band: "low",
      confidence_value: 34,
      conflict_state: "contested",
      current_chr_ref: "chr-cs-002",
    },
  },
  "proj-003": undefined,
};

// ── Project Overview ────────────────────────────────────────────────────────────

/** The project's aggregate Outcome Confidence (Derived; banded, reliability-qualified). */
export const overviewConfidenceFixture: ConfidenceState = confidenceByProject[
  "proj-001"
] as ConfidenceState;

/** The project's CAF assessment — three co-equal dimensions, each Derived/banded. */
export const overviewCafFixture: CAFState = {
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
 * Findings for the project. Two carry a `severity` → they are Issues (prioritized
 * findings). The third has no severity → a finding that is not yet an Issue. So the
 * overview presents: findings = 3, issues = 2 (the count split is presentation of
 * governed objects, never a health metric).
 */
export const overviewFindingsFixture: Finding[] = [
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
  {
    finding_id: "f-3",
    project_id: PROJECT_ID,
    finding_type: "ambiguity",
    status: "detected",
    summary: '"Soon" is used for the rollout window without a date.',
    affected_dimensions: ["clarity"],
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 60,
      conflict_state: "none",
      current_chr_ref: "chr-f-3",
    },
  },
];

/**
 * The first-class `/overview` DTO (DTM-0038): the aggregate understanding summary in
 * ONE read — outcome confidence + CAF + the governed-object counts
 * (finding=3, issue=2, recommendation=2). This is the mocked shape of the
 * `useGetOverview…` hook the Project Overview now consumes.
 */
export const overviewFixture: Overview = {
  project_id: PROJECT_ID,
  outcome_confidence: overviewConfidenceFixture,
  caf: overviewCafFixture,
  counts: [
    { kind: "finding", label: "Findings", count: 3 },
    { kind: "issue", label: "Issues", count: 2 },
    { kind: "recommendation", label: "Recommendations", count: 2 },
  ],
};

/** Recommendations for the project (Derived advisory candidates). Count = 2. */
export const overviewRecommendationsFixture: Recommendation[] = [
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
