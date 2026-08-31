/**
 * History / Timeline fixtures (DTM-0027 → DTM-0039 read-swap).
 *
 * The History / Timeline surface reconstructs THE TRAIL — record-exact, append-only —
 * from THREE already-retained, append-only reads:
 *
 *   1. `HistoryEntry` (`useListHistory…`) — the first-class CHR trail (DTM-0038): the
 *      Cognition History Records appended over the project's life. Each is a
 *      **Derived** trail entry (a recomputable projection of OSLO's understanding,
 *      never "settled"). `supersedes_chr_id` carries the append-only SUPERSESSION
 *      chain; the prior (superseded) CHR STAYS visible.
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
 * the mocked shapes of the three reads, authored in APPEND ORDER so a test can prove
 * the surface renders APPEND-EXACT (record order preserved), never reordered.
 */
import type {
  HistoryEntry,
  UserAcceptanceRecord,
  PlanFact,
} from "../../api/generated/oSLORelease1API.schemas";

export const PROJECT_ID = "proj-001";

// ── CHR trail — the first-class /history Cognition History Records ────────────────
// Authored in APPEND ORDER (oldest first, as the read returns them). The CURRENT
// understanding is the newest CHR nothing supersedes; an earlier CHR is SUPERSEDED
// but stays in the trail (append-only — supersession is additive, never erased).

/** The first (oldest) CHR — later SUPERSEDED by chr-003. Stays visible. */
export const supersededRun: HistoryEntry = {
  chr_id: "chr-001",
  project_id: PROJECT_ID,
  output_kind: "fast_analysis_pass",
  epistemic_label: "derived",
  emitted_at: "2026-05-01T09:00:42Z",
  recompute_trigger: "initial",
  supersedes_chr_id: null,
};

/** A prior deep-pass CHR — not current, not superseded; stays in the trail. */
export const failedRun: HistoryEntry = {
  chr_id: "chr-002",
  project_id: PROJECT_ID,
  output_kind: "deep_analysis_pass",
  epistemic_label: "derived",
  emitted_at: "2026-05-10T12:02:00Z",
  recompute_trigger: "evidence_added",
  supersedes_chr_id: null,
};

/** The CURRENT understanding — the newest CHR; supersedes chr-001. */
export const currentRun: HistoryEntry = {
  chr_id: "chr-003",
  project_id: PROJECT_ID,
  output_kind: "deep_analysis_pass",
  epistemic_label: "derived",
  emitted_at: "2026-05-20T08:02:10Z",
  recompute_trigger: "reanalysis",
  supersedes_chr_id: "chr-001",
};

/** Append order (oldest→newest), exactly as the /history read returns them. */
export const analysisRunsFixture: HistoryEntry[] = [
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
