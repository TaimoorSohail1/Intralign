/**
 * Notification / Awareness fixtures (DTM-0026, IC-WE-DISCLOSE E1).
 *
 * TWO distinct governed/platform shapes feed this surface, and the difference is
 * the WHOLE POINT of the slice:
 *
 *   1. `Notification` (DTM-0018 `useListNotifications…`) — **platform awareness
 *      state, NON-canonical**. The generated DTO carries NO `label`/DerivedEnvelope
 *      (see the schema docstring: "Platform awareness state (non-canonical): …
 *      carries no epistemic cognition label — it is not a Derived projection — it
 *      references a source object"). Its `state` (created/viewed/dismissed/expired)
 *      is presentation state; read/unread/dismiss writes NO canonical and changes
 *      NO assessment.
 *
 *   2. `AcceptanceImpactAssessment` (DTM-0018 `useListAcceptanceImpact…`) — a
 *      **Derived** cognition: "a decision you confirmed is affected" (drift ≥10pts
 *      or a band change vs the version-pinned acceptance). It DOES carry a
 *      `label` (DerivedEnvelope, `epistemic_label='derived'`) → surfaced via
 *      `EpistemicLabel`. Derived, never settled, never auto-resolved.
 *
 * These fixtures mirror the generated DTOs VERBATIM (no invented fields). They are
 * the mocked shapes of the two DTM-0018 reads.
 */
import type {
  Notification,
  AcceptanceImpactAssessment,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";
export const WORKSPACE_ID = "ws-001";

// ── Notifications — platform awareness state (NON-canonical) ────────────────────

/** An unread finding emission (state `created` = unread). Routes to its source. */
export const unreadFindingNotification: Notification = {
  notification_id: "ntf-001",
  workspace_id: WORKSPACE_ID,
  project_id: PROJECT_ID,
  event_type: "finding_emitted",
  source_object_type: "finding",
  source_object_id: "f-conflict-1",
  state: "created",
  created_at: "2026-06-25T09:00:00Z",
  viewed_at: null,
  dismissed_at: null,
  expired_at: null,
  target_user_id: "user-1",
};

/** A reanalysis-complete emission, already viewed (read). */
export const readAnalysisNotification: Notification = {
  notification_id: "ntf-002",
  workspace_id: WORKSPACE_ID,
  project_id: PROJECT_ID,
  event_type: "analysis_run_completed",
  source_object_type: "analysis_run",
  source_object_id: "run-2",
  state: "viewed",
  created_at: "2026-06-24T17:30:00Z",
  viewed_at: "2026-06-24T18:00:00Z",
  dismissed_at: null,
  expired_at: null,
  target_user_id: "user-1",
};

/** A new-comment emission, unread. */
export const unreadCommentNotification: Notification = {
  notification_id: "ntf-003",
  workspace_id: WORKSPACE_ID,
  project_id: PROJECT_ID,
  event_type: "comment_added",
  source_object_type: "comment",
  source_object_id: "cmt-7",
  state: "created",
  created_at: "2026-06-25T11:15:00Z",
  viewed_at: null,
  dismissed_at: null,
  expired_at: null,
  target_user_id: "user-1",
};

export const notificationsFixture: Notification[] = [
  unreadCommentNotification,
  unreadFindingNotification,
  readAnalysisNotification,
];

// ── Acceptance-Impact — Derived "a decision you confirmed is affected" ───────────

/**
 * A band-changing impact: the value behind a user-accepted item dropped a band
 * (medium → low) — Derived, carries its DerivedEnvelope label. Links to the
 * affected accepted item via the UAR reference. NOT auto-resolved.
 */
export const bandChangeImpactFixture: AcceptanceImpactAssessment = {
  project_id: PROJECT_ID,
  uar_ref: "uar-101",
  pinned_chr: "chr-r1-004",
  latest_chr: "chr-r2-011",
  pinned_band: "medium",
  latest_band: "low",
  band_changed: true,
  delta: -18,
  label: {
    epistemic_label: "derived",
    confidence_band: "low",
    confidence_value: 41,
    conflict_state: "none",
    current_chr_ref: "chr-r2-011",
  },
};

/**
 * A magnitude-only impact (≥10pts, no band change) on a contested item — exercises
 * the conflict marker on a Derived label and a same-band drift.
 */
export const magnitudeImpactFixture: AcceptanceImpactAssessment = {
  project_id: PROJECT_ID,
  uar_ref: "uar-102",
  pinned_chr: "chr-r1-009",
  latest_chr: "chr-r2-014",
  pinned_band: "high",
  latest_band: "high",
  band_changed: false,
  delta: -12,
  label: {
    epistemic_label: "derived",
    confidence_band: "high",
    confidence_value: 76,
    conflict_state: "contested",
    current_chr_ref: "chr-r2-014",
  },
};

export const acceptanceImpactFixture: AcceptanceImpactAssessment[] = [
  bandChangeImpactFixture,
  magnitudeImpactFixture,
];
