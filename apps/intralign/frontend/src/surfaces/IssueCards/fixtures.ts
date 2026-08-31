/**
 * Issue Cards fixtures (DTM-0023 → DTM-0039 read-swap).
 *
 * DTM-0039: the cards now render from the FIRST-CLASS `/issues` read (DTM-0038) — the
 * dedicated `Issue` DTO (Evaluate's *prioritized Finding*). Each Issue carries its
 * `issue_id`, the source `finding_id` lineage, the governed `severity`, the Derived
 * confidence `label` (DerivedEnvelope + band), and the workflow `status`. These
 * fixtures mirror the generated `Issue` type VERBATIM (no invented fields). They are
 * the mocked shape of the `useListIssues…` hook.
 */
import type { Issue } from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

/**
 * A critical, contested issue (its Derived label is `contested`) — the card surfaces a
 * conflict marker (presented, never resolved). Anchored to its source Finding
 * `f-conflict-1`.
 */
export const criticalIssueFixture: Issue = {
  issue_id: "iss-conflict-1",
  finding_id: "f-conflict-1",
  project_id: PROJECT_ID,
  finding_type: "conflict",
  severity: "critical",
  status: "detected",
  summary: "Two stakeholders state conflicting go-live dates.",
  affected_dimensions: ["alignment"],
  evidence_links: ["ev-stakeholder-a", "ev-stakeholder-b"],
  first_seen_run_id: "run-1",
  last_updated_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 55,
    conflict_state: "contested",
    current_chr_ref: "chr-r2-003",
  },
};

/**
 * A moderate issue, not contested — used to assert the conflict marker is ABSENT
 * and that a distinct severity renders as a governed qualifier.
 */
export const moderateIssueFixture: Issue = {
  issue_id: "iss-ambiguity-1",
  finding_id: "f-ambiguity-1",
  project_id: PROJECT_ID,
  finding_type: "ambiguity",
  severity: "moderate",
  status: "detected",
  summary: '"Soon" is used for the rollout window without a date.',
  affected_dimensions: ["clarity"],
  evidence_links: ["ev-rollout-doc"],
  first_seen_run_id: "run-1",
  last_updated_run_id: "run-1",
  label: {
    epistemic_label: "derived",
    confidence_band: "low",
    confidence_value: 30,
    conflict_state: "none",
    current_chr_ref: "chr-r2-001",
  },
};

/**
 * A warning-severity issue with high-confidence understanding — exercises the
 * full severity range + a high band.
 */
export const warningIssueFixture: Issue = {
  issue_id: "iss-missing-1",
  finding_id: "f-missing-1",
  project_id: PROJECT_ID,
  finding_type: "missing_information",
  severity: "warning",
  status: "detected",
  summary: "No success criteria are recorded for the launch milestone.",
  affected_dimensions: ["clarity", "feasibility"],
  evidence_links: ["ev-milestone-doc"],
  first_seen_run_id: "run-2",
  last_updated_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "high",
    confidence_value: 88,
    conflict_state: "none",
    current_chr_ref: "chr-r2-009",
  },
};

/** The ordered set of issues the surface presents (most severe first is the UI's job). */
export const issuesFixture: Issue[] = [
  criticalIssueFixture,
  moderateIssueFixture,
  warningIssueFixture,
];
