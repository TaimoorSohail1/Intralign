/**
 * Issue Cards fixtures (DTM-0023, IC-WE-DISCLOSE E1).
 *
 * THE ISSUES-DATA FINDING (binding to this slice — see the worker report):
 * There is **no dedicated Issue endpoint or Issue DTO** in the DTM-0018 REST
 * surface. The internal cognition `Issue` (`shared/epistemic.py`) — Evaluate's
 * *prioritized Finding* (a Finding + an assigned `severity`, carrying the source
 * Finding lineage) — is NOT exposed verbatim over REST (no `Issue` class in
 * `shared/entities.py`; nothing named "issue" in the generated client). The
 * governed carrier of exactly the data an Issue Card needs is therefore the
 * **Finding DTO**: it already carries `severity` (the very attribute Evaluate
 * assigns to FORM an Issue), the Derived confidence `label` (DerivedEnvelope +
 * band), and the source-finding identity (`finding_id` / `finding_type` /
 * `evidence_links`). So the cards render from the `listFindings` read and link
 * each card back to its source Finding (the Finding Panel route). We do NOT
 * invent an Issue endpoint — the gap is flagged, not filled.
 *
 * These fixtures mirror the generated `Finding` type VERBATIM (no invented
 * fields). They are the mocked shape of the DTM-0018 `useListFindings…` hook.
 */
import type { Finding } from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

/**
 * A critical, contested issue (its source Finding's Derived label is
 * `contested`) — the card surfaces a conflict marker (presented, never
 * resolved). Anchored to its source Finding `f-conflict-1`.
 */
export const criticalIssueFixture: Finding = {
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
export const moderateIssueFixture: Finding = {
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
export const warningIssueFixture: Finding = {
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
export const issuesFixture: Finding[] = [
  criticalIssueFixture,
  moderateIssueFixture,
  warningIssueFixture,
];
