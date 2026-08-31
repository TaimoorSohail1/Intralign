/**
 * DTM-0029 — Assisted Editing / Persistent Intelligence (AW-04/05, IC-WE-DISCLOSE).
 *
 * An always-visible panel that PRESENTS the governed intelligence during artifact
 * editing — Outcome Confidence + CAF (Clarity / Alignment / Feasibility) +
 * Understanding-State — each via EpistemicLabel (Derived, banded, never settled). It is
 * READ-ONLY (decision #3, Disclose presents, never generates; AW spec: editing changes
 * no assessment, only reanalysis does — and this panel is even further upstream: it
 * renders no editor, computes nothing).
 *
 * AW-04/05 ROUTING — the panel ROUTES assists, performing NONE of them:
 *   - B1: "Ask OSLO about this" → the project Chat surface (consume/trigger cognition
 *     happens in Chat, never here).
 *   - B3: "See the suggested fix" → the Suggested Fix, reached via its Finding
 *     (RP-C1: a Recommendation/Suggested Fix lives only in a Finding context — never a
 *     standalone recommendation route).
 * It exposes NO generate / score / accept / apply control (the negative).
 *
 * UNDERSTANDING-STATE DATA FINDING (flagged): there is no aggregate "understanding
 * state" DTO in the DTM-0018 REST surface. We derive it from the governed `AnalysisRun`
 * list (latest run `superseded` ⇒ "based on the previous analysis"), exactly as the
 * Companion does — inventing no state flag.
 */
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import { Link } from "@tanstack/react-router";

import { useGetConfidenceV1ProjectsProjectIdConfidenceGet } from "../../api/generated/confidence/confidence";
import { useGetCafV1ProjectsProjectIdCafGet } from "../../api/generated/confidence/confidence";
import { useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet } from "../../api/generated/analysis-runs/analysis-runs";

import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import type {
  ConfidenceState,
  CAFState,
  CAFDimensionView,
  AnalysisRun,
  Dimension,
} from "../../api/generated/oSLORelease1API.schemas";

export interface AssistedEditingProps {
  projectId: string;
  artifactId: string;
  /**
   * The Finding the editing context is anchored to, when known — the B3 Suggested-Fix
   * assist routes to this Finding (RP-C1). Optional: when absent, the B3 affordance is
   * omitted rather than routing to a standalone recommendation route.
   */
  findingId?: string;
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
function asArray<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as T[]) : [];
}

const DIMENSION_LABEL: Record<Dimension, string> = {
  clarity: "Clarity",
  alignment: "Alignment",
  feasibility: "Feasibility",
};

function CafDimension({ dim }: { dim: CAFDimensionView }) {
  return (
    <Box
      data-testid="ae-caf-dimension"
      data-dimension={dim.dimension}
      sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}
    >
      <Box data-testid={`ae-caf-${dim.dimension}`}>
        <Typography variant="caption" sx={{ fontWeight: 700 }}>
          {DIMENSION_LABEL[dim.dimension] ?? dim.dimension}
        </Typography>
      </Box>
      <EpistemicLabel epistemic={{ standing: "derived", band: dim.band }} />
    </Box>
  );
}

export function AssistedEditing({ projectId, artifactId, findingId }: AssistedEditingProps) {
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(projectId);
  const cafQ = useGetCafV1ProjectsProjectIdCafGet(projectId);
  const runsQ = useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet(projectId);

  const confidence = isRecord(confidenceQ.data?.data)
    ? (confidenceQ.data?.data as ConfidenceState)
    : undefined;
  const caf = isRecord(cafQ.data?.data) ? (cafQ.data?.data as CAFState) : undefined;
  const runs = asArray<AnalysisRun>(runsQ.data?.data);

  const anyLoading = confidenceQ.isLoading || cafQ.isLoading || runsQ.isLoading;

  const cafDimensions: CAFDimensionView[] | undefined = caf
    ? [caf.clarity, caf.alignment, caf.feasibility].filter(Boolean)
    : undefined;

  // Understanding-State — derived from the governed run status (no invented flag).
  const latestRun = [...runs].sort((a, b) =>
    (b.started_at ?? "").localeCompare(a.started_at ?? ""),
  )[0];
  const isStale = latestRun?.run_status === "superseded";

  return (
    <Paper
      variant="outlined"
      data-testid="assisted-editing"
      data-artifact-id={artifactId}
      sx={{ p: 2 }}
    >
      <Typography variant="subtitle1" sx={{ fontWeight: 700 }} gutterBottom data-testid="ae-title">
        Persistent intelligence
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        What OSLO currently understands about this artifact&apos;s project, kept visible as
        you edit. This panel presents understanding — it does not generate, score, accept,
        or apply anything. Editing changes no assessment; only reanalysis does.
      </Typography>

      {anyLoading ? (
        <Box
          data-testid="ae-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={16} />
          <Typography variant="caption" color="text.secondary">
            Loading the current understanding…
          </Typography>
        </Box>
      ) : null}

      <Stack spacing={2}>
        {/* Outcome Confidence — Derived, banded, never settled. */}
        <Box data-testid="ae-confidence">
          <Typography variant="caption" sx={{ fontWeight: 700 }} display="block" gutterBottom>
            Outcome Confidence
          </Typography>
          {confidence ? (
            <EpistemicLabel epistemic={fromDerivedEnvelope(confidence.label)} />
          ) : (
            <Typography variant="caption" color="text.secondary" data-testid="ae-confidence-empty">
              Not yet available — appears once this project has been analyzed.
            </Typography>
          )}
        </Box>

        {/* CAF — three co-equal dimensions, each Derived/banded. */}
        <Box data-testid="ae-caf">
          <Typography variant="caption" sx={{ fontWeight: 700 }} display="block" gutterBottom>
            CAF — Clarity · Alignment · Feasibility
          </Typography>
          {cafDimensions && cafDimensions.length > 0 ? (
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr 1fr" },
                gap: 1.5,
              }}
            >
              {cafDimensions.map((dim) => (
                <CafDimension key={dim.dimension} dim={dim} />
              ))}
            </Box>
          ) : (
            <Typography variant="caption" color="text.secondary" data-testid="ae-caf-empty">
              CAF assessment not yet available.
            </Typography>
          )}
        </Box>

        {/* Understanding-State — current vs based-on-previous-analysis (governed run). */}
        <Box data-testid="ae-understanding-state">
          <Typography variant="caption" sx={{ fontWeight: 700 }} display="block" gutterBottom>
            Understanding-State
          </Typography>
          {isStale ? (
            <Chip
              size="small"
              color="warning"
              variant="outlined"
              label="Based on the previous analysis"
              data-testid="ae-state-stale"
            />
          ) : (
            <Chip
              size="small"
              variant="outlined"
              label="Current understanding"
              data-testid="ae-state-current"
            />
          )}
          {isStale ? (
            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>
              The latest analysis is superseded — what is shown reflects a previous
              analysis, not OSLO&apos;s most current understanding. Reanalysis updates it.
            </Typography>
          ) : null}
        </Box>

        {/* AW-04/05 assists — ROUTE only; the panel performs none of them. */}
        <Box sx={{ pt: 1, borderTop: "1px solid", borderColor: "divider" }}>
          <Typography variant="caption" sx={{ fontWeight: 700 }} display="block" gutterBottom>
            Assists
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            {/* B1 — routes to Chat. */}
            <Link
              to="/projects/$projectId/chat"
              params={{ projectId }}
              search={{
                context_kind: "artifact",
                context_id: artifactId,
              }}
              style={{ textDecoration: "none" }}
              data-testid="ae-route-chat"
            >
              <Typography variant="body2" color="primary">
                Ask OSLO about this
              </Typography>
            </Link>
            {/* B3 — routes to the Suggested Fix VIA its Finding (RP-C1). */}
            {findingId ? (
              <Link
                to="/projects/$projectId/findings/$findingId"
                params={{ projectId, findingId }}
                style={{ textDecoration: "none" }}
                data-testid="ae-route-suggested-fix"
              >
                <Typography variant="body2" color="primary">
                  See the suggested fix in its finding
                </Typography>
              </Link>
            ) : null}
          </Stack>
        </Box>
      </Stack>
    </Paper>
  );
}

export default AssistedEditing;
