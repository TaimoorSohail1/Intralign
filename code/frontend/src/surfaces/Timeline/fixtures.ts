/**
 * History / Timeline fixtures (DTM-0027, IC-WE-DISCLOSE E1).
 *
 * The History / Timeline surface reconstructs THE TRAIL — record-exact, append-only —
 * from THREE already-retained, append-only DTM-0018 reads. There is **no dedicated
 * CHR/history endpoint** in the generated client (see the worker report): the CHR
 * trail is reconstructed from the analysis runs that appended the Cognition History
 * Records, exactly as the MRI Understanding Timeline does. The three reads:
 *
 *   1. `AnalysisRun` (`useListAnalysisRuns…`) — the runs that appended CHRs. Each is
 *      a **Derived** trail entry (a recomputable projection of OSLO's understanding,
 *      never "settled"). `previous_run_id` + `run_status: 'superseded'` carry the
 *      append-only SUPERSESSION chain; the prior (superseded) run STAYS visible.
 *
 *   2. `UserAcceptanceRecord` (`useListAcceptances…`) — what the user confirmed.
 *      **user-attested** (`epistemic_label: 'attested-user'`), version-pinned. It is
 *      a HUMAN DECISION receipt — it marks nothing world-true/approved/canonical.
 *
 *   3. `PlanFact` (`useListPlanFacts…`) — the user-attested confirmed planning item.
 *      "factual in the plan, attributed to the user" — **NOT world-truth**, NOT
 *      OSLO-approved. `epistemic_label: 'attested-user'`.
 *
 * These fixtures mirror the generated DTOs VERBATIM (no invented fields). They are
 * the mocked shapes of the three DTM-0018 reads. They are intentionally authored
 * OUT of chronological order so a test can prove the surface renders APPEND-EXACT
 * (record order preserved per source), never reordered destructively.
 */
import type {
  AnalysisRun,
  UserAcceptanceRecord,
  PlanFact,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

// ── CHR trail — the analysis runs that appended Cognition History Records ─────────
// Authored in APPEND ORDER (oldest first, as the source returns them). The CURRENT
// understanding is the last completed run; an earlier run is SUPERSEDED but stays
// in the trail (append-only — supersession is additive, the prior is never erased).

/** The first (oldest) fast pass — later SUPERSEDED by run-003. Stays visible. */
export const supersededRun: AnalysisRun = {
  analysis_run_id: "run-001",
  project_id: PROJECT_ID,
  run_type: "fast_analysis_pass",
  run_status: "superseded",
  started_at: "2026-05-01T09:00:00Z",
  completed_at: "2026-05-01T09:00:42Z",
  previous_run_id: null,
};

/** A failed reanalysis — shown honestly as failed, last-known-good retained. */
export const failedRun: AnalysisRun = {
  analysis_run_id: "run-002",
  project_id: PROJECT_ID,
  run_type: "deep_analysis_pass",
  run_status: "failed",
  started_at: "2026-05-10T12:00:00Z",
  completed_at: null,
  previous_run_id: "run-001",
};

/** The CURRENT understanding — the newest completed run; supersedes run-001. */
export const currentRun: AnalysisRun = {
  analysis_run_id: "run-003",
  project_id: PROJECT_ID,
  run_type: "deep_analysis_pass",
  run_status: "completed",
  started_at: "2026-05-20T08:00:00Z",
  completed_at: "2026-05-20T08:02:10Z",
  previous_run_id: "run-001",
};

/** Append order (oldest→newest), exactly as the analysis-runs read returns them. */
export const analysisRunsFixture: AnalysisRun[] = [
  supersededRun,
  failedRun,
  currentRun,
];

// ── UAR trail — what the user confirmed (user-attested, version-pinned) ──────────

export const acceptUar: UserAcceptanceRecord = {
  uar_id: "uar-001",
  project_id: PROJECT_ID,
  action: "accept",
  target_kind: "recommendation",
  version_pin: "chr-ref-aaa",
  epistemic_label: "attested-user",
  user_id: "user-1",
  confirmed_at: "2026-05-05T10:00:00Z",
  created_at: "2026-05-05T10:00:00Z",
};

export const editUar: UserAcceptanceRecord = {
  uar_id: "uar-002",
  project_id: PROJECT_ID,
  action: "direct-edit",
  target_kind: "artifact",
  version_pin: "chr-ref-bbb",
  epistemic_label: "attested-user",
  user_id: "user-1",
  confirmed_at: "2026-05-12T14:30:00Z",
  created_at: "2026-05-12T14:30:00Z",
};

/** Append order as the acceptance read returns them. */
export const acceptancesFixture: UserAcceptanceRecord[] = [acceptUar, editUar];

// ── Plan-fact trail — user-attested confirmed planning items (NOT world-truth) ───

export const planFactOne: PlanFact = {
  plan_fact_id: "pf-001",
  project_id: PROJECT_ID,
  proposition: "The launch milestone is fixed at 2026-09-01.",
  content_type: "milestone",
  version_pin: "chr-ref-aaa",
  attested_by_user: "user-1",
  epistemic_label: "attested-user",
  created_at: "2026-05-05T10:00:05Z",
};

export const planFactTwo: PlanFact = {
  plan_fact_id: "pf-002",
  project_id: PROJECT_ID,
  proposition: "The data-migration scope excludes legacy archives.",
  content_type: "scope",
  version_pin: "chr-ref-bbb",
  attested_by_user: "user-1",
  epistemic_label: "attested-user",
  created_at: "2026-05-12T14:30:05Z",
};

/** Append order as the plan-facts read returns them. */
export const planFactsFixture: PlanFact[] = [planFactOne, planFactTwo];
