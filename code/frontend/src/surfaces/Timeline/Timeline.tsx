/**
 * DTM-0027 — History / Timeline (IC-WE-DISCLOSE E1).
 *
 * A Companion-Surface-class secondary project-context surface
 * (HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1 §D) that reconstructs THE TRAIL —
 * record-exact, append-only — and routes to retained context. It PRESENTS retained
 * history only: it computes nothing, generates nothing, governs nothing, executes
 * nothing, and changes NO assessment (only reanalysis changes an assessment, and
 * reanalysis is not a Disclose affordance). It hosts NO structured actions
 * (no restore/rollback/approve/edit/delete — §D, §J, HT-6).
 *
 * It reconstructs the trail from THREE already-retained, append-only DTM-0018 reads
 * (there is NO dedicated CHR/history endpoint — see the worker report; the CHR
 * trail is reconstructed from the analysis runs that appended the Cognition History
 * Records, exactly as the MRI Understanding Timeline does — the visual idiom is
 * reused, the component is NOT forked):
 *
 *   1. `useListAnalysisRuns…` — the CHR trail (runs that appended CHRs). Each entry
 *      is **Derived** (a recomputable projection of OSLO's understanding, never
 *      "settled"). `run_status: 'superseded'` / `'failed'` carry the append-only
 *      lifecycle; the superseded/failed entry STAYS visible (supersession additive).
 *   2. `useListAcceptances…` — UARs (what the user confirmed). **user-attested**,
 *      version-pinned — a human decision receipt, NOT world-truth/approval.
 *   3. `useListPlanFacts…` — plan facts. **user-attested** ("You confirmed …") —
 *      factual in the plan, NOT world-truth, NOT evidence-attested, NOT OSLO-attested.
 *
 * APPEND-EXACT: each source's records render in the EXACT order the read returned
 * them — never re-sorted, never reversed, never destructively reordered. The
 * surface presents the records read-only; it writes nothing back.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import { Link } from "@tanstack/react-router";

import { useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet } from "../../api/generated/analysis-runs/analysis-runs";
import {
  useListAcceptancesV1ProjectsProjectIdAcceptanceGet,
  useListPlanFactsV1ProjectsProjectIdPlanFactsGet,
} from "../../api/generated/acceptance/acceptance";
import { EpistemicLabel } from "../../components/EpistemicLabel";
import { epistemicTones, surfaces } from "../../theme/tokens";
import type {
  AnalysisRun,
  UserAcceptanceRecord,
  PlanFact,
} from "../../api/generated/oSLORelease1API.schemas";

export interface TimelineProps {
  projectId: string;
}

const RUN_TYPE_LABEL: Record<string, string> = {
  fast_analysis_pass: "Fast pass",
  deep_analysis_pass: "Deep pass",
};

/** Presentation label for a run's lifecycle state — a presentation of the
 *  upstream-owned status (HT-7); History computes/changes none of it. */
const RUN_STATUS_LABEL: Record<string, string> = {
  queued: "Queued",
  running: "Running",
  completed: "Completed",
  failed: "Failed",
  cancelled: "Cancelled",
  superseded: "Superseded",
};

const UAR_ACTION_LABEL: Record<string, string> = {
  accept: "Accepted",
  reject: "Declined",
  defer: "Deferred",
  "direct-edit": "Direct edit",
};

/** True for a plain array of objects (defensive against partial responses). */
function asArray<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as T[]) : [];
}

function whenLabel(ts?: string | null): string {
  if (!ts) return "time pending";
  try {
    return new Date(ts).toLocaleString();
  } catch {
    return ts;
  }
}

/**
 * One CHR trail entry — a run that appended a Cognition History Record. ALWAYS
 * Derived (a recomputable projection, never settled). The current understanding is
 * marked distinctly; a superseded/failed run is shown honestly and STAYS visible
 * (append-only — supersession is additive, the prior is never erased).
 */
function ChrEntry({
  run,
  isCurrent,
  projectId,
}: {
  run: AnalysisRun;
  isCurrent: boolean;
  projectId: string;
}) {
  const isSuperseded = run.run_status === "superseded";
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2 }}
      data-testid="chr-entry"
      data-run-id={run.analysis_run_id}
      data-current={isCurrent ? "true" : undefined}
      data-superseded={isSuperseded ? "true" : undefined}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 0.5 }}>
        <Typography variant="subtitle2">
          {RUN_TYPE_LABEL[run.run_type] ?? run.run_type}
        </Typography>
        {/* CHR entries are Derived — never settled (rendered via the single label). */}
        <EpistemicLabel epistemic={{ standing: "derived" }} />
        {isCurrent ? (
          <Chip
            data-testid="chr-current"
            size="small"
            variant="outlined"
            label="Current understanding"
            sx={{ color: epistemicTones.attested, borderColor: epistemicTones.attested }}
          />
        ) : (
          <Chip
            size="small"
            variant="outlined"
            label={isSuperseded ? "Superseded (prior)" : "Prior"}
            sx={{ color: epistemicTones.derived, borderColor: epistemicTones.derived }}
          />
        )}
      </Box>
      <Typography variant="caption" color="text.secondary" display="block">
        {whenLabel(run.completed_at ?? run.started_at)} ·{" "}
        {RUN_STATUS_LABEL[run.run_status] ?? run.run_status}
      </Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        {run.analysis_run_id}
        {run.previous_run_id ? ` · follows ${run.previous_run_id}` : ""}
      </Typography>
      {/* Route to retained context (the project's understanding) — never an action. */}
      <Link
        to="/projects/$projectId"
        params={{ projectId }}
        style={{ textDecoration: "none" }}
        data-testid="chr-context-link"
      >
        <Button variant="text" component="span" size="small">
          View this understanding
        </Button>
      </Link>
    </Paper>
  );
}

/**
 * One UAR entry — what the user confirmed. user-attested, version-pinned (the exact
 * CHR accepted). A human decision receipt — it marks nothing world-true/approved.
 */
function UarEntry({ uar }: { uar: UserAcceptanceRecord }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2 }}
      data-testid="uar-entry"
      data-uar-id={uar.uar_id}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 0.5 }}>
        <Typography variant="subtitle2">
          {UAR_ACTION_LABEL[uar.action] ?? uar.action}
          {uar.target_kind ? ` · ${uar.target_kind}` : ""}
        </Typography>
        {/* user-attested — "You confirmed", not world-truth. */}
        <EpistemicLabel epistemic={{ standing: "attested", source: "user" }} />
      </Box>
      <Typography variant="caption" color="text.secondary" display="block">
        {whenLabel(uar.confirmed_at ?? uar.created_at)}
      </Typography>
      <Typography variant="caption" color="text.secondary" display="block">
        {uar.uar_id} · pinned to {uar.version_pin}
      </Typography>
    </Paper>
  );
}

/**
 * One plan-fact entry — a user-attested confirmed planning item. "You confirmed …"
 * — recorded as factual in the plan, NOT world-truth, NOT evidence/OSLO-attested.
 * The proposition is presented VERBATIM (record-exact).
 */
function PlanFactEntry({ fact }: { fact: PlanFact }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2 }}
      data-testid="plan-fact-entry"
      data-plan-fact-id={fact.plan_fact_id}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 0.5 }}>
        {/* user-attested — the plan-fact variant: "You confirmed", not world-truth. */}
        <EpistemicLabel epistemic={{ standing: "attested", source: "user" }} />
        {fact.content_type ? (
          <Chip size="small" variant="outlined" label={fact.content_type} />
        ) : null}
      </Box>
      <Typography variant="body2" sx={{ mb: 0.5 }}>
        {fact.proposition}
      </Typography>
      <Typography variant="caption" color="text.secondary" display="block">
        {whenLabel(fact.created_at)}
        {fact.version_pin ? ` · pinned to ${fact.version_pin}` : ""}
      </Typography>
    </Paper>
  );
}

export function Timeline({ projectId }: TimelineProps) {
  const runsQ = useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet(projectId);
  const acceptancesQ = useListAcceptancesV1ProjectsProjectIdAcceptanceGet(projectId);
  const planFactsQ = useListPlanFactsV1ProjectsProjectIdPlanFactsGet(projectId);

  // APPEND-EXACT: present each source's records in the order the read returned them.
  // No re-sort, no reverse — the trail is record-exact. We derive "current" WITHOUT
  // mutating order: the current understanding is the LAST completed run.
  const runs = asArray<AnalysisRun>(runsQ.data?.data);
  const acceptances = asArray<UserAcceptanceRecord>(acceptancesQ.data?.data);
  const planFacts = asArray<PlanFact>(planFactsQ.data?.data);

  // Identify the current understanding (latest completed run) for distinct marking —
  // a read-only lookup, it does NOT reorder the append-exact trail.
  let currentRunId: string | undefined;
  for (const r of runs) {
    if (r.run_status === "completed") currentRunId = r.analysis_run_id;
  }

  const loading =
    runsQ.isLoading || acceptancesQ.isLoading || planFactsQ.isLoading;
  const isEmpty =
    !loading &&
    runs.length === 0 &&
    acceptances.length === 0 &&
    planFacts.length === 0;

  return (
    <Box data-testid="timeline" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        History &amp; Timeline
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        The trail of how this project&apos;s understanding evolved — what OSLO derived
        and when, and what you confirmed. It is read-only and append-only: prior
        states stay visible (supersession is additive, never erased), and viewing
        history changes nothing — only reanalysis changes an assessment.
      </Typography>

      {loading ? (
        <Box
          data-testid="timeline-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Reconstructing the trail…
          </Typography>
        </Box>
      ) : isEmpty ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="timeline-empty" variant="body2" color="text.secondary">
            No history yet. As OSLO analyses this project and you confirm planning
            items, the trail will appear here.
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={4}>
          {/* CHR trail — the analysis runs that appended Cognition History Records. */}
          <Box>
            <Typography variant="subtitle2" sx={{ mb: 1 }} data-testid="chr-section-title">
              How OSLO&apos;s understanding evolved
            </Typography>
            {runs.length > 0 ? (
              <TrailRail count={runs.length} currentIndex={runs.findIndex((r) => r.analysis_run_id === currentRunId)}>
                {runs.map((run) => (
                  <ChrEntry
                    key={run.analysis_run_id}
                    run={run}
                    isCurrent={run.analysis_run_id === currentRunId}
                    projectId={projectId}
                  />
                ))}
              </TrailRail>
            ) : (
              <Typography
                data-testid="chr-empty"
                variant="body2"
                color="text.secondary"
              >
                No analysis history yet.
              </Typography>
            )}
          </Box>

          {/* UARs — what the user confirmed (user-attested, version-pinned). */}
          <Box>
            <Typography variant="subtitle2" sx={{ mb: 1 }} data-testid="uar-section-title">
              What you confirmed
            </Typography>
            {acceptances.length > 0 ? (
              <Stack spacing={2}>
                {acceptances.map((uar) => (
                  <UarEntry key={uar.uar_id} uar={uar} />
                ))}
              </Stack>
            ) : (
              <Typography
                data-testid="uar-empty"
                variant="body2"
                color="text.secondary"
              >
                You haven&apos;t confirmed anything yet.
              </Typography>
            )}
          </Box>

          {/* Plan facts — user-attested confirmed planning items (NOT world-truth). */}
          <Box>
            <Typography
              variant="subtitle2"
              sx={{ mb: 1 }}
              data-testid="plan-fact-section-title"
            >
              Planning items you attested
            </Typography>
            {planFacts.length > 0 ? (
              <Stack spacing={2}>
                {planFacts.map((fact) => (
                  <PlanFactEntry key={fact.plan_fact_id} fact={fact} />
                ))}
              </Stack>
            ) : (
              <Typography
                data-testid="plan-fact-empty"
                variant="body2"
                color="text.secondary"
              >
                No attested planning items yet.
              </Typography>
            )}
          </Box>
        </Stack>
      )}
    </Box>
  );
}

/**
 * The shared visual idiom from the MRI Understanding Timeline — a simple vertical
 * SVG rail alongside the entries (SVG + MUI primitives only, no charting library).
 * Reused here (NOT forked from MRI) so the History surface reads in the same idiom.
 */
function TrailRail({
  count,
  currentIndex,
  children,
}: {
  count: number;
  currentIndex: number;
  children: React.ReactNode;
}) {
  const railX = 10;
  const step = 96;
  const top = 24;
  const height = top * 2 + Math.max(0, count - 1) * step;
  return (
    <Box sx={{ display: "flex", gap: 1.5 }}>
      <Box
        component="svg"
        viewBox={`0 0 24 ${height}`}
        role="img"
        aria-label="History trail"
        sx={{ width: 24, flexShrink: 0, height: "auto" }}
      >
        <line
          x1={railX}
          y1={top}
          x2={railX}
          y2={top + Math.max(0, count - 1) * step}
          stroke={surfaces.divider}
          strokeWidth={2}
        />
        {Array.from({ length: count }).map((_, i) => (
          <circle
            key={i}
            cx={railX}
            cy={top + i * step}
            r={i === currentIndex ? 7 : 5}
            fill={i === currentIndex ? epistemicTones.attested : epistemicTones.derived}
          />
        ))}
      </Box>
      <Stack spacing={2} sx={{ flexGrow: 1, minWidth: 0 }}>
        {children}
      </Stack>
    </Box>
  );
}

export default Timeline;
