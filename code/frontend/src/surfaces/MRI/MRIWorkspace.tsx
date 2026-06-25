/**
 * MRIWorkspace — the MRI umbrella surface (IC-WE-DISCLOSE E1 · DL-047 MRI-04…07).
 *
 * The Project Workspace's understanding view. It PRESENTS a project's understanding
 * state + diagnostics — Findings (grouped into the MRI Experience categories
 * Missing/Risky/Incomplete), CAF, Outcome Confidence, and history — and NEVER
 * recomputes. There is no compute / recompute / score / accept / generate control
 * anywhere on it (the spine of Disclose; decision #3). Every governed Derived value
 * is carried through `EpistemicLabel` (decision #5), so a Derived value can never
 * read as settled.
 *
 * It hosts the four DL-047 sub-components:
 *   MRI-04 Artifact Understanding Heatmap
 *   MRI-05 CAF Triangle
 *   MRI-06 Understanding Timeline (current + history)
 *   MRI-07 Understanding Dependencies (blocked / awaiting review)
 *
 * It consumes the DTM-0018 Orval hooks read-only; lists may be empty until upstream
 * projections are populated → loading + empty states render cleanly.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";

import { useListFindingsV1ProjectsProjectIdFindingsGet } from "../../api/generated/findings/findings";
import {
  useGetCafV1ProjectsProjectIdCafGet,
  useGetConfidenceV1ProjectsProjectIdConfidenceGet,
} from "../../api/generated/confidence/confidence";
import { useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet } from "../../api/generated/analysis-runs/analysis-runs";

import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { UnderstandingHeatmap } from "./UnderstandingHeatmap";
import { CafTriangle } from "./CafTriangle";
import { UnderstandingTimeline } from "./UnderstandingTimeline";
import { UnderstandingDependencies } from "./UnderstandingDependencies";
import { FindingRow } from "./FindingRow";
import {
  groupByCategory,
  MRI_CATEGORY_ORDER,
  MRI_CATEGORY_LABEL,
  MRI_CATEGORY_BLURB,
} from "./categories";
import type {
  Finding,
  CAFState,
  ConfidenceState,
} from "../../api/generated/oSLORelease1API.schemas";

export interface MRIWorkspaceProps {
  projectId: string;
}

/** True for a plain object DTO (not an array, string, or null). */
function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

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

export function MRIWorkspace({ projectId }: MRIWorkspaceProps) {
  const findingsQ = useListFindingsV1ProjectsProjectIdFindingsGet(projectId);
  const cafQ = useGetCafV1ProjectsProjectIdCafGet(projectId);
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(projectId);
  const runsQ = useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet(projectId);

  // Defensive coercion: lists may be empty until upstream projections are
  // populated, and a partial/unexpected response must never crash the surface.
  // We only present well-shaped governed DTOs (objects/arrays); anything else
  // resolves to the clean empty state.
  const findings: Finding[] = Array.isArray(findingsQ.data?.data)
    ? (findingsQ.data?.data as Finding[])
    : [];
  const caf = isRecord(cafQ.data?.data)
    ? (cafQ.data?.data as CAFState)
    : undefined;
  const confidence = isRecord(confidenceQ.data?.data)
    ? (confidenceQ.data?.data as ConfidenceState)
    : undefined;
  const runs = Array.isArray(runsQ.data?.data) ? runsQ.data?.data : [];

  const anyLoading =
    findingsQ.isLoading || cafQ.isLoading || confidenceQ.isLoading || runsQ.isLoading;

  const grouped = groupByCategory(findings);

  return (
    <Box data-testid="mri-surface" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Understanding (MRI)
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Where are the weaknesses in this project&apos;s understanding? OSLO presents what
        it understands — it does not resolve findings here; only reanalysis changes the
        assessment.
      </Typography>

      {anyLoading ? (
        <Box
          data-testid="mri-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading the current understanding…
          </Typography>
        </Box>
      ) : null}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
          gap: 2,
          mb: 2,
        }}
      >
        {/* Outcome Confidence — trust-in-understanding, banded, reliability-qualified */}
        <Section title="Outcome Confidence" testId="mri-confidence">
          {confidence ? (
            <Stack spacing={1}>
              <EpistemicLabel epistemic={fromDerivedEnvelope(confidence.label)} />
              <Typography variant="body2" color="text.secondary">
                How much OSLO trusts its understanding of where this project stands
                against its declared outcome.
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
              data-testid="mri-confidence-empty"
              variant="body2"
              color="text.secondary"
            >
              Outcome Confidence not yet available.
            </Typography>
          )}
        </Section>

        {/* MRI-05 CAF Triangle */}
        <Section title="CAF — Clarity · Alignment · Feasibility">
          <CafTriangle caf={caf} />
        </Section>

        {/* MRI-04 Heatmap */}
        <Section title="Weakness heatmap" subtitle="Where weakness concentrates (qualitative).">
          <UnderstandingHeatmap findings={findings} projectId={projectId} />
        </Section>

        {/* MRI-06 Timeline */}
        <Section title="Understanding timeline" subtitle="Current understanding and its history.">
          <UnderstandingTimeline runs={runs} projectId={projectId} />
        </Section>
      </Box>

      {/* MRI-07 Dependencies */}
      <Section
        title="Understanding dependencies"
        subtitle="Open findings your understanding depends on resolving — blocked / awaiting review."
        testId="mri-dependencies-section"
      >
        <UnderstandingDependencies findings={findings} projectId={projectId} />
      </Section>

      <Divider sx={{ my: 2 }} />

      {/* Findings, grouped into the MRI Experience categories (Missing/Risky/Incomplete) */}
      <Box data-testid="mri-findings">
        <Typography variant="subtitle1" sx={{ fontWeight: 700 }} gutterBottom>
          What needs attention
        </Typography>
        {findings.length === 0 ? (
          <Typography
            data-testid="mri-findings-empty"
            variant="body2"
            color="text.secondary"
          >
            No findings yet — nothing needs attention. (Distinct from “not yet
            analyzed”.)
          </Typography>
        ) : (
          <Stack spacing={2}>
            {MRI_CATEGORY_ORDER.map((cat) => (
              <Paper
                key={cat}
                variant="outlined"
                sx={{ p: 2 }}
                data-testid={`mri-category-${cat}`}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
                  {MRI_CATEGORY_LABEL[cat]}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {MRI_CATEGORY_BLURB[cat]}
                </Typography>
                {grouped[cat].length === 0 ? (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 1 }}
                    data-testid={`mri-category-${cat}-empty`}
                  >
                    Nothing needs attention here.
                  </Typography>
                ) : (
                  <Box sx={{ mt: 1 }}>
                    {grouped[cat].map((f) => (
                      <FindingRow key={f.finding_id} finding={f} projectId={projectId} />
                    ))}
                  </Box>
                )}
              </Paper>
            ))}
          </Stack>
        )}
      </Box>
    </Box>
  );
}

export default MRIWorkspace;
