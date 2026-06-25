/**
 * DTM-0024 — Project Overview (IC-WE-DISCLOSE E1).
 *
 * A project-level **understanding summary** — the answer to "how much can I trust
 * what OSLO understands about this project?" — presented in one read:
 *
 *   - **aggregate Outcome Confidence** (Derived; banded, reliability-qualified) via
 *     `fromDerivedEnvelope` → `EpistemicLabel` — a recomputable projection, never
 *     shown as settled; confidence = trust-in-understanding, NEVER project
 *     health / readiness / probability;
 *   - **CAF** — Clarity · Alignment · Feasibility, three **co-equal** dimensions,
 *     each carried through `EpistemicLabel` (banded, never ranked/scored);
 *   - **counts** of governed objects — findings, issues (findings Evaluate
 *     prioritized with a `severity`), recommendations — each a count OF governed
 *     objects, NEVER a computed score or a project-health metric.
 *
 * THE COUNTS-DATA FINDING (see fixtures.ts + the worker report): there is **no
 * aggregate "overview"/counts DTO** in the DTM-0018 REST surface — no field carries
 * the totals. So the counts are simply the LENGTHS of the already-governed list
 * reads. We do NOT invent a counts endpoint — the gap is flagged, not filled.
 *
 * Read-only: there is no edit / score / accept / generate / recompute control
 * anywhere (decision #3 — Disclose presents, never generates; only reanalysis
 * changes an assessment, and reanalysis is not a Disclose affordance). The numeric
 * 0–100 confidence/CAF index is NEVER rendered to the user (only the band is) and no
 * percentage is shown — the screen is a console for understanding, not a metrics
 * cockpit. Loading / empty states render cleanly (none-found, not a failure).
 *
 * It consumes the DTM-0018 Orval hooks read-only.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import CircularProgress from "@mui/material/CircularProgress";

import {
  useGetConfidenceV1ProjectsProjectIdConfidenceGet,
  useGetCafV1ProjectsProjectIdCafGet,
} from "../../api/generated/confidence/confidence";
import { useListFindingsV1ProjectsProjectIdFindingsGet } from "../../api/generated/findings/findings";
import { useListRecommendationsV1ProjectsProjectIdRecommendationsGet } from "../../api/generated/recommendations/recommendations";

import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import type {
  ConfidenceState,
  CAFState,
  CAFDimensionView,
  Finding,
  Recommendation,
  Dimension,
} from "../../api/generated/oSLORelease1API.schemas";

export interface ProjectOverviewProps {
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

/** One co-equal CAF dimension — its name + a Derived banded label (no score). */
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
      {/* Per-dimension band — Derived, never settled; index is NOT rendered. */}
      <EpistemicLabel epistemic={{ standing: "derived", band: dim.band }} />
      {dim.reliability ? (
        <Typography variant="caption" color="text.secondary">
          {dim.reliability}
        </Typography>
      ) : null}
    </Box>
  );
}

/** One count of governed objects — a count, never a score / health metric. */
function CountItem({
  testId,
  value,
  label,
}: {
  testId: string;
  value: number;
  label: string;
}) {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", minWidth: 96 }}>
      <Typography
        data-testid={testId}
        variant="h5"
        component="span"
        sx={{ fontWeight: 700 }}
      >
        {value}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
    </Box>
  );
}

export function ProjectOverview({ projectId }: ProjectOverviewProps) {
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(projectId);
  const cafQ = useGetCafV1ProjectsProjectIdCafGet(projectId);
  const findingsQ = useListFindingsV1ProjectsProjectIdFindingsGet(projectId);
  const recsQ = useListRecommendationsV1ProjectsProjectIdRecommendationsGet(projectId);

  const confidence = isRecord(confidenceQ.data?.data)
    ? (confidenceQ.data?.data as ConfidenceState)
    : undefined;
  const caf = isRecord(cafQ.data?.data) ? (cafQ.data?.data as CAFState) : undefined;
  const findings = asArray<Finding>(findingsQ.data?.data);
  const recommendations = asArray<Recommendation>(recsQ.data?.data);

  // Counts are presentation of governed objects — the lengths of the list reads.
  // An Issue IS a Finding Evaluate prioritized by assigning a severity.
  const findingsCount = findings.length;
  const issuesCount = findings.filter((f) => Boolean(f.severity)).length;
  const recommendationsCount = recommendations.length;

  const anyLoading =
    confidenceQ.isLoading || cafQ.isLoading || findingsQ.isLoading || recsQ.isLoading;

  const cafDimensions: CAFDimensionView[] | undefined = caf
    ? [caf.clarity, caf.alignment, caf.feasibility].filter(Boolean)
    : undefined;

  return (
    <Box data-testid="project-overview" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Project overview
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        How much OSLO trusts what it understands about this project, and where attention
        is most needed. OSLO presents this understanding; it does not resolve or
        complete it here — only reanalysis changes the assessment.
      </Typography>

      {anyLoading ? (
        <Box
          data-testid="overview-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading the project&apos;s understanding…
          </Typography>
        </Box>
      ) : null}

      <Stack spacing={2}>
        {/* Aggregate Outcome Confidence — the headline trust signal. */}
        <Section title="Outcome Confidence" testId="overview-confidence">
          {confidence ? (
            <Stack spacing={1}>
              <EpistemicLabel epistemic={fromDerivedEnvelope(confidence.label)} />
              <Typography variant="body2" color="text.secondary">
                How much OSLO trusts its understanding of where this project stands
                against its declared outcome. This is trust in understanding — it does
                not predict the project&apos;s outcome or whether it will succeed.
              </Typography>
              {confidence.reliability_qualifier ? (
                <Typography variant="caption" color="text.secondary">
                  Reliability: {confidence.reliability_qualifier}
                </Typography>
              ) : null}
              {confidence.basis && confidence.basis.length > 0 ? (
                <Typography variant="caption" color="text.secondary">
                  Basis: {confidence.basis.join("; ")}
                </Typography>
              ) : null}
            </Stack>
          ) : (
            <Typography
              data-testid="overview-confidence-empty"
              variant="body2"
              color="text.secondary"
            >
              Outcome Confidence not yet available. (Not an incomplete or pending
              result — it appears once this project has been analyzed.)
            </Typography>
          )}
        </Section>

        {/* CAF — three co-equal dimensions. */}
        <Section
          title="CAF — Clarity · Alignment · Feasibility"
          testId="overview-caf"
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
              data-testid="overview-caf-empty"
              variant="body2"
              color="text.secondary"
            >
              CAF assessment not yet available.
            </Typography>
          )}
        </Section>

        {/* Counts of governed objects — never a health/score metric. */}
        <Section
          title="What OSLO has surfaced"
          testId="overview-counts"
          subtitle="How many governed objects OSLO has surfaced in this project. These are counts of what exists — not a rating of the project."
        >
          <Box sx={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
            <CountItem testId="count-findings" value={findingsCount} label="Findings" />
            <CountItem testId="count-issues" value={issuesCount} label="Issues" />
            <CountItem
              testId="count-recommendations"
              value={recommendationsCount}
              label="Recommendations"
            />
          </Box>
        </Section>
      </Stack>
    </Box>
  );
}

export default ProjectOverview;
