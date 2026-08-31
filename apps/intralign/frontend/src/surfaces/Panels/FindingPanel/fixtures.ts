/**
 * Finding Panel fixtures — Finding DTOs (Data Model v1.2 §11) used to drive the
 * panel in tests and as the mocked shape of the DTM-0018 `useGetFinding…` hook.
 * These mirror the generated `Finding` type VERBATIM (no invented fields).
 *
 * The Finding is a Derived projection: it carries its `label` (DerivedEnvelope)
 * which the panel hands to `fromDerivedEnvelope` → `EpistemicLabel` (decision #5).
 * Its `evidence_links` are the Attested evidence anchors (the evidence lineage) —
 * each rendered with the EpistemicLabel attested/evidence variant. The panel
 * PRESENTS them read-only; it never recomputes, resolves, or accepts.
 */
import type { Finding } from "../../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

/**
 * A conflicted finding: its Derived label is `contested`, so the panel surfaces a
 * conflict marker (presented, never resolved). It is anchored to three Attested
 * evidence anchors — its evidence lineage.
 */
export const conflictedFindingFixture: Finding = {
  finding_id: "f-conflict-1",
  project_id: PROJECT_ID,
  finding_type: "conflict",
  severity: "critical",
  status: "detected",
  summary: "Two stakeholders state conflicting go-live dates.",
  affected_dimensions: ["alignment"],
  evidence_links: ["ev-stakeholder-a", "ev-stakeholder-b", "ev-charter-1"],
  first_seen_run_id: "run-1",
  last_updated_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 55,
    // an unresolved conflict — surfaced by the panel, never resolved
    conflict_state: "contested",
    current_chr_ref: "chr-r2-003",
  },
};

/**
 * A non-conflicted finding anchored to one Attested evidence anchor. Used to
 * assert the conflict marker is ABSENT when the finding is not contested.
 */
export const cleanFindingFixture: Finding = {
  finding_id: "f-missing-1",
  project_id: PROJECT_ID,
  finding_type: "missing_information",
  severity: "warning",
  status: "detected",
  summary: "No success criteria are recorded for the launch milestone.",
  affected_dimensions: ["clarity"],
  evidence_links: ["ev-milestone-doc"],
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
 * A finding with NO reachable evidence anchors — drives the (rare) explanatory
 * empty-evidence state. Per the spec a finding with no reachable evidence is a
 * conformance edge; the panel presents it explicitly rather than crashing.
 */
export const noEvidenceFindingFixture: Finding = {
  finding_id: "f-no-evidence-1",
  project_id: PROJECT_ID,
  finding_type: "ambiguity",
  severity: "moderate",
  status: "detected",
  summary: '"Soon" is used for the rollout window without a date.',
  affected_dimensions: ["clarity"],
  evidence_links: [],
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 62,
    conflict_state: "none",
    current_chr_ref: "chr-r2-005",
  },
};
