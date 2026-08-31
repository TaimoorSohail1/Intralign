/**
 * DTM-0025 — Understanding Companion (IC-WE-DISCLOSE E1).
 *
 * The contextual understanding surface: epistemic-safe summaries of the current
 * understanding in context — Outcome Confidence · CAF · Top Findings · Top
 * Recommendations · stale-analysis state · Ask OSLO. It PRESENTS, NEVER GENERATES.
 *
 * THE HEADLINE CONTRACT — Option B (preserves RP-C1): to reach a Recommendation the
 * Companion routes to the Recommendation's ASSOCIATED FINDING (the Finding Panel
 * route), via the `Recommendation.finding_id` anchor — NEVER directly to a
 * standalone Recommendation Panel. Surface-transition consistency: a governed object
 * reads the same here as everywhere (Derived, banded, never settled). Read-only:
 * there is no generate / score / accept / reject / defer / edit / govern control.
 *
 * THE STALE-STATE DATA FINDING (see fixtures.ts + the worker report): there is no
 * aggregate "companion" / "is_stale" DTO in the DTM-0018 REST surface. The Companion
 * presents "Previous Analysis" by reading the governed `AnalysisRun` list — a latest
 * run carrying `run_status: "superseded"` is, by the governed object's own status,
 * no-longer-current understanding. We do NOT invent a stale flag.
 *
 * It consumes the DTM-0018 Orval hooks read-only. The numeric 0–100 confidence/CAF
 * index is NEVER rendered (only the band is) and no percentage is shown.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import { Link } from "@tanstack/react-router";

import {
  useGetConfidenceV1ProjectsProjectIdConfidenceGet,
  useGetCafV1ProjectsProjectIdCafGet,
} from "../../api/generated/confidence/confidence";
import { useListFindingsV1ProjectsProjectIdFindingsGet } from "../../api/generated/findings/findings";
import { useListRecommendationsV1ProjectsProjectIdRecommendationsGet } from "../../api/generated/recommendations/recommendations";
import { useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet } from "../../api/generated/analysis-runs/analysis-runs";

import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import type {
  ConfidenceState,
  CAFState,
  CAFDimensionView,
  Finding,
  Recommendation,
  AnalysisRun,
  Dimension,
} from "../../api/generated/oSLORelease1API.schemas";

export interface CompanionProps {
  projectId: string;
}

/** True for a plain object DTO (not an array, string, or null). */
function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

/** Defensive array coercion — a partial response must never crash the surface. */
function asArray<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as T[]) : [];
}

const DIMENSION_LABEL: Record<Dimension, string> = {
  clarity: "Clarity",
  alignment: "Alignment",
  feasibility: "Feasibility",
};

/** A titled section card — pure presentation scaffolding. */
function Section({
  title,
  testId,
  subtitle,
  children,
}: {
  title: string;
  testId?: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }} data-testid={testId}>
      <Typography variant="subtitle1" sx={{ fontWeight: 700 }} gutterBottom>
        {title}
      </Typography>
      {subtitle ? (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {subtitle}
        </Typography>
      ) : null}
      {children}
    </Paper>
  );
}

/** One co-equal CAF dimension — its name + a Derived banded label (no index). */
function CafDimension({ dim }: { dim: CAFDimensionView }) {
  return (
    <Box
      data-testid="caf-dimension"
      data-dimension={dim.dimension}
      sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}
    >
      <Box data-testid={`caf-dimension-${dim.dimension}`}>
        <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
          {DIMENSION_LABEL[dim.dimension] ?? dim.dimension}
        </Typography>
      </Box>
      {/* Per-dimension band — Derived, never settled; the index is NOT rendered. */}
      <EpistemicLabel epistemic={{ standing: "derived", band: dim.band }} />
      {dim.reliability ? (
        <Typography variant="caption" color="text.secondary">
          {dim.reliability}
        </Typography>
      ) : null}
    </Box>
  );
}

/**
 * One Top Finding — its summary + Derived banded label (conflict carried verbatim)
 * + a link to ITS Finding Panel (Q5 — the same governed object reads the same
 * everywhere). Read-only: a link to context, not an act-on control.
 */
function CompanionFinding({
  projectId,
  finding,
}: {
  projectId: string;
  finding: Finding;
}) {
  return (
    <Box
      data-testid="companion-finding"
      data-finding-id={finding.finding_id}
      sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}
    >
      <Typography variant="body2" sx={{ fontWeight: 600 }}>
        {finding.summary}
      </Typography>
      <EpistemicLabel epistemic={fromDerivedEnvelope(finding.label)} />
      <Link
        to="/projects/$projectId/findings/$findingId"
        params={{ projectId, findingId: finding.finding_id }}
        style={{ textDecoration: "none" }}
        data-testid="open-finding"
      >
        <Typography variant="caption" color="primary">
          Open finding
        </Typography>
      </Link>
    </Box>
  );
}

/**
 * One Top Recommendation — its title + Derived banded label, and the OPTION-B
 * affordance: "See in its finding" routes to the recommendation's ASSOCIATED
 * FINDING (`finding_id`) — the Finding Panel — NEVER to a standalone Recommendation
 * Panel (RP-C1 preserved). It is a presentation link, not an accept/act control.
 */
function CompanionRecommendation({
  projectId,
  recommendation,
}: {
  projectId: string;
  recommendation: Recommendation;
}) {
  return (
    <Box
      data-testid="companion-recommendation"
      data-recommendation-id={recommendation.recommendation_id}
      sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}
    >
      <Typography variant="body2" sx={{ fontWeight: 600 }}>
        {recommendation.title}
      </Typography>
      <EpistemicLabel epistemic={fromDerivedEnvelope(recommendation.label)} />
      {/* Option B: route to the ASSOCIATED FINDING, never a standalone rec panel. */}
      <Link
        to="/projects/$projectId/findings/$findingId"
        params={{ projectId, findingId: recommendation.finding_id }}
        style={{ textDecoration: "none" }}
        data-testid="see-recommendation"
      >
        <Typography variant="caption" color="primary">
          See in its finding
        </Typography>
      </Link>
    </Box>
  );
}

export function Companion({ projectId }: CompanionProps) {
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(projectId);
  const cafQ = useGetCafV1ProjectsProjectIdCafGet(projectId);
  const findingsQ = useListFindingsV1ProjectsProjectIdFindingsGet(projectId);
  const recsQ = useListRecommendationsV1ProjectsProjectIdRecommendationsGet(projectId);
  const runsQ = useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet(projectId);

  const confidence = isRecord(confidenceQ.data?.data)
    ? (confidenceQ.data?.data as ConfidenceState)
    : undefined;
  const caf = isRecord(cafQ.data?.data) ? (cafQ.data?.data as CAFState) : undefined;
  const findings = asArray<Finding>(findingsQ.data?.data);
  const recommendations = asArray<Recommendation>(recsQ.data?.data);
  const runs = asArray<AnalysisRun>(runsQ.data?.data);

  const anyLoading =
    confidenceQ.isLoading ||
    cafQ.isLoading ||
    findingsQ.isLoading ||
    recsQ.isLoading ||
    runsQ.isLoading;

  const cafDimensions: CAFDimensionView[] | undefined = caf
    ? [caf.clarity, caf.alignment, caf.feasibility].filter(Boolean)
    : undefined;

  // Stale-analysis (Q8 / COMP-11): the latest run is the most-recently-started. If
  // its governed status is `superseded`, the current understanding is no-longer-
  // current — present it as "Previous Analysis", never as current. This presents the
  // governed run status; it does NOT invent an is_stale flag.
  const latestRun = [...runs].sort((a, b) =>
    (b.started_at ?? "").localeCompare(a.started_at ?? ""),
  )[0];
  const isStale = latestRun?.run_status === "superseded";

  return (
    <Box data-testid="companion" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Understanding companion
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        What OSLO currently understands, in context. OSLO presents this understanding;
        it does not resolve or complete it here. Each item carries its epistemic
        standing — a recomputable projection that updates as understanding changes.
      </Typography>

      {anyLoading ? (
        <Box
          data-testid="companion-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading the current understanding…
          </Typography>
        </Box>
      ) : null}

      {/* Previous Analysis — surfaced prominently, never presented as current. */}
      {isStale ? (
        <Alert
          severity="warning"
          icon={false}
          data-testid="companion-stale"
          sx={{ mb: 2 }}
        >
          <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
            Previous Analysis
          </Typography>
          <Typography variant="body2">
            The latest analysis run has been superseded — what is shown reflects a
            previous analysis, not OSLO&apos;s most current understanding. Re-running
            analysis is done elsewhere; OSLO surfaces this state, it does not act on it.
          </Typography>
        </Alert>
      ) : null}

      <Stack spacing={2}>
        {/* Outcome Confidence — Derived, banded, never settled. */}
        <Section title="Outcome Confidence" testId="companion-confidence">
          {confidence ? (
            <Stack spacing={1}>
              <EpistemicLabel epistemic={fromDerivedEnvelope(confidence.label)} />
              <Typography variant="body2" color="text.secondary">
                How much OSLO trusts its understanding of where this project stands
                against its declared outcome. This is trust in understanding — not a
                prediction of the project&apos;s outcome.
              </Typography>
              {confidence.reliability_qualifier ? (
                <Typography variant="caption" color="text.secondary">
                  Reliability: {confidence.reliability_qualifier}
                </Typography>
              ) : null}
            </Stack>
          ) : (
            <Typography
              data-testid="companion-confidence-empty"
              variant="body2"
              color="text.secondary"
            >
              Outcome Confidence not yet available. (It appears once this project has
              been analyzed — not an incomplete or pending result.)
            </Typography>
          )}
        </Section>

        {/* CAF — three co-equal dimensions, each Derived/banded. */}
        <Section
          title="CAF — Clarity · Alignment · Feasibility"
          testId="companion-caf"
          subtitle="Three co-equal dimensions of understanding — each banded, none ranked."
        >
          {cafDimensions && cafDimensions.length > 0 ? (
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr 1fr" },
                gap: 2,
              }}
            >
              {cafDimensions.map((dim) => (
                <CafDimension key={dim.dimension} dim={dim} />
              ))}
            </Box>
          ) : (
            <Typography
              data-testid="companion-caf-empty"
              variant="body2"
              color="text.secondary"
            >
              CAF assessment not yet available.
            </Typography>
          )}
        </Section>

        {/* Top Findings — each Derived/banded, each links to its Finding Panel. */}
        <Section
          title="Top findings"
          testId="companion-findings"
          subtitle="The most relevant findings OSLO has surfaced — presented, not resolved."
        >
          {findings.length > 0 ? (
            <Stack spacing={1.5}>
              {findings.map((finding) => (
                <CompanionFinding
                  key={finding.finding_id}
                  projectId={projectId}
                  finding={finding}
                />
              ))}
            </Stack>
          ) : (
            <Typography
              data-testid="companion-findings-empty"
              variant="body2"
              color="text.secondary"
            >
              No findings surfaced yet.
            </Typography>
          )}
        </Section>

        {/* Top Recommendations — Option B: each routes via its associated Finding. */}
        <Section
          title="Top recommendations"
          testId="companion-recommendations"
          subtitle="Advisory candidates — each shown in the context of the finding it belongs to."
        >
          {recommendations.length > 0 ? (
            <Stack spacing={1.5}>
              {recommendations.map((recommendation) => (
                <CompanionRecommendation
                  key={recommendation.recommendation_id}
                  projectId={projectId}
                  recommendation={recommendation}
                />
              ))}
            </Stack>
          ) : (
            <Typography
              data-testid="companion-recommendations-empty"
              variant="body2"
              color="text.secondary"
            >
              No recommendations surfaced yet.
            </Typography>
          )}
        </Section>

        {/* Ask OSLO — launches Chat (a separate surface), never embeds it. */}
        <Section title="Ask OSLO" testId="ask-oslo">
          <Link
            to="/projects/$projectId/chat"
            params={{ projectId }}
            style={{ textDecoration: "none" }}
            data-testid="ask-oslo-link"
          >
            <Typography variant="body2" color="primary">
              Open a conversation about this project&apos;s understanding
            </Typography>
          </Link>
        </Section>
      </Stack>
    </Box>
  );
}

export default Companion;
