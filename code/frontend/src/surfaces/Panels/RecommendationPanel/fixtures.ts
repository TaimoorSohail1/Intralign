/**
 * Recommendation Panel fixtures — Recommendation DTOs (Data Model v1.2 §12) used to
 * drive the panel in tests and as the mocked shape of the DTM-0018
 * `useListRecommendationsForFinding…` hook. These mirror the generated
 * `Recommendation` type VERBATIM (no invented fields).
 *
 * A Recommendation is a Derived projection: each carries its `label`
 * (DerivedEnvelope) which the panel hands to `fromDerivedEnvelope` →
 * `EpistemicLabel` (decision #5). Every Recommendation is anchored to ONE Finding
 * (`finding_id`) — RP-C1 / Recommendation-only-in-Finding-context. The DL-055
 * `status` is read from the governed source as-is; the panel PRESENTS it and the
 * accept/reject/defer affordance, but NEVER mutates it (decision #3 — acceptance
 * is the user's, recorded by the existing Wave U capture, never by Disclose).
 *
 * Multiple Recommendations for the same Finding are *alternatives* — the panel
 * groups them as "Resolution Paths" (presentation grouping only; NO object).
 */
import type { Recommendation } from "../../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";
export const FINDING_ID = "f-conflict-1";

/**
 * The OSLO-Recommended (primary) alternative for the finding — a candidate
 * improvement in the `generated` DL-055 state. Derived, medium-band confidence.
 */
export const primaryRecommendationFixture: Recommendation = {
  recommendation_id: "rec-primary-1",
  project_id: PROJECT_ID,
  finding_id: FINDING_ID,
  recommendation_type: "improvement",
  status: "generated",
  title: "Confirm a single go-live date with both stakeholders",
  description:
    "Resolve the conflicting go-live dates by confirming one date directly with both stakeholders, then update the charter.",
  rationale:
    "Two stakeholders state conflicting go-live dates; a confirmed single date removes the conflict the finding surfaces.",
  expected_dimension: "alignment",
  effort: "medium",
  first_seen_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "medium",
    confidence_value: 60,
    conflict_state: "none",
    current_chr_ref: "chr-r2-101",
  },
};

/**
 * A second alternative addressing the SAME finding — a validation recommendation,
 * `deferred`. Renders as another Resolution Path alongside the primary.
 */
export const alternativeRecommendationFixture: Recommendation = {
  recommendation_id: "rec-alt-2",
  project_id: PROJECT_ID,
  finding_id: FINDING_ID,
  recommendation_type: "validation",
  status: "deferred",
  title: "Run a stakeholder alignment review on the launch milestone",
  description:
    "Convene a short alignment review so both stakeholders confirm the milestone expectations together.",
  rationale:
    "An alignment review confirms the expectation directly with the stakeholders whose statements conflict.",
  expected_dimension: "alignment",
  effort: "high",
  first_seen_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "low",
    confidence_value: 35,
    conflict_state: "none",
    current_chr_ref: "chr-r2-102",
  },
};

/**
 * A third alternative for the same finding — already in the `accepted` DL-055
 * state (the user's Selected Path). The panel PRESENTS this status (it was set by
 * Wave U), but the panel itself never sets it. Alternatives remain visible after
 * acceptance (RP-5) — accepting one does not hide the others.
 */
export const acceptedRecommendationFixture: Recommendation = {
  recommendation_id: "rec-accepted-3",
  project_id: PROJECT_ID,
  finding_id: FINDING_ID,
  recommendation_type: "improvement",
  status: "accepted",
  title: "Adopt the charter date and notify the second stakeholder",
  description:
    "Keep the charter's recorded date and notify the second stakeholder of the confirmed date.",
  rationale: "The charter already records a date; confirming it resolves the conflict fastest.",
  expected_dimension: "alignment",
  effort: "low",
  first_seen_run_id: "run-2",
  label: {
    epistemic_label: "derived",
    confidence_band: "high",
    confidence_value: 80,
    conflict_state: "none",
    current_chr_ref: "chr-r2-103",
  },
};

/** The three alternatives for the finding — the multi-Resolution-Path case. */
export const recommendationsForFinding: Recommendation[] = [
  primaryRecommendationFixture,
  alternativeRecommendationFixture,
  acceptedRecommendationFixture,
];

/** A single recommendation for the finding — the "no alternatives" case (§O). */
export const singleRecommendationForFinding: Recommendation[] = [primaryRecommendationFixture];
