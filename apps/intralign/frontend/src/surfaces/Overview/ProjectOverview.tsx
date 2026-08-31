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
 * FIRST-CLASS OVERVIEW READ (DTM-0039 → DTM-0038): the aggregate confidence + CAF +
 * governed-object counts now come from the dedicated `/overview` read
 * (`useGetOverview…`) in ONE call — replacing the DTM-0024 placeholder that composed
 * four list/scalar reads and computed the counts client-side.
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
import { useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import { useQueryClient } from "@tanstack/react-query";

import { useGetOverviewV1ProjectsProjectIdOverviewGet } from "../../api/generated/overview/overview";
import {
  useStartFastAnalysisV1ProjectsProjectIdAnalysisRunsFastPost,
  useStartDeepAnalysisV1ProjectsProjectIdAnalysisRunsDeepPost,
} from "../../api/generated/analysis-commands/analysis-commands";
import { useAddEvidenceV1ProjectsProjectIdEvidencePost } from "../../api/generated/project-commands/project-commands";
import { getListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGetQueryKey } from "../../api/generated/analysis-runs/analysis-runs";

import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import type {
  Overview,
  ConfidenceState,
  CAFState,
  CAFDimensionView,
  GovernedCount,
  Dimension,
} from "../../api/generated/oSLORelease1API.schemas";

export interface ProjectOverviewProps {
  projectId: string;
}

/**
 * The project-action affordances (DTM-0039 → DTM-0032/0034). These are user-initiated
 * COMMANDS:
 *   - **Start Fast Pass / Deep Pass** trigger an analysis run (the user, not Disclose,
 *     asks OSLO to (re)analyze) — the recompute, not the surface, appends the CHR.
 *   - **Add evidence** submits new Attested intake → feeds Perceive → recompute.
 * The surface performs no cognition; on success the analysis-runs read is invalidated.
 */
function ProjectActions({ projectId }: { projectId: string }) {
  const queryClient = useQueryClient();
  const invalidateRuns = () =>
    queryClient.invalidateQueries({
      queryKey: getListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGetQueryKey(projectId),
    });

  const fastM = useStartFastAnalysisV1ProjectsProjectIdAnalysisRunsFastPost({
    mutation: { onSuccess: invalidateRuns },
  });
  const deepM = useStartDeepAnalysisV1ProjectsProjectIdAnalysisRunsDeepPost({
    mutation: { onSuccess: invalidateRuns },
  });
  const evidenceM = useAddEvidenceV1ProjectsProjectIdEvidencePost({
    mutation: { onSuccess: invalidateRuns },
  });

  const [sourceType, setSourceType] = useState("");
  const [contentRef, setContentRef] = useState("");

  const submitEvidence = (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceType.trim() || !contentRef.trim()) return;
    evidenceM.mutate(
      {
        projectId,
        data: { source_type: sourceType.trim(), content_ref: contentRef.trim() },
      },
      {
        onSuccess: () => {
          setSourceType("");
          setContentRef("");
          invalidateRuns();
        },
      },
    );
  };

  const triggering = fastM.isPending || deepM.isPending;

  return (
    <Section
      title="Move this project forward"
      testId="overview-actions"
      subtitle="Ask OSLO to (re)analyze, or add new evidence. These are your actions — OSLO presents understanding; it analyzes only when you ask, and adding evidence feeds the next analysis."
    >
      <Stack spacing={2}>
        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
          <Button
            variant="contained"
            disabled={triggering}
            data-testid="trigger-fast"
            onClick={() => fastM.mutate({ projectId })}
          >
            Start Fast Pass
          </Button>
          <Button
            variant="outlined"
            disabled={triggering}
            data-testid="trigger-deep"
            onClick={() => deepM.mutate({ projectId, data: { trigger_source: "overview" } })}
          >
            Start Deep Pass
          </Button>
        </Box>

        <Box component="form" onSubmit={submitEvidence} data-testid="add-evidence-form">
          <Stack spacing={1} direction={{ xs: "column", sm: "row" }}>
            <TextField
              size="small"
              label="Evidence source"
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
              inputProps={{ "data-testid": "evidence-source-type" }}
            />
            <TextField
              size="small"
              fullWidth
              label="Evidence content / reference"
              value={contentRef}
              onChange={(e) => setContentRef(e.target.value)}
              inputProps={{ "data-testid": "evidence-content-ref" }}
            />
            <Button type="submit" variant="outlined" data-testid="add-evidence-submit">
              Add evidence
            </Button>
          </Stack>
        </Box>

        {fastM.isSuccess || deepM.isSuccess ? (
          <Alert severity="info" icon={false} data-testid="analysis-triggered-notice">
            Analysis requested. OSLO is (re)analyzing — its understanding updates when the
            run completes; this view will reflect it then.
          </Alert>
        ) : null}
        {evidenceM.isSuccess ? (
          <Alert severity="info" icon={false} data-testid="evidence-added-notice">
            Evidence added. It feeds the next analysis — it changes no assessment on its own.
          </Alert>
        ) : null}
      </Stack>
    </Section>
  );
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

/** Pull a governed count by kind from the first-class overview (0 when absent). */
function countOf(counts: GovernedCount[], kind: string): number {
  return counts.find((c) => c.kind === kind)?.count ?? 0;
}

export function ProjectOverview({ projectId }: ProjectOverviewProps) {
  // The first-class /overview read (DTM-0038): the aggregate understanding summary in
  // ONE read — outcome confidence + CAF + the governed-object counts. Replaces the
  // DTM-0024 placeholder that composed four list/scalar reads + a client-side count.
  const overviewQ = useGetOverviewV1ProjectsProjectIdOverviewGet(projectId);

  const overview = isRecord(overviewQ.data?.data)
    ? (overviewQ.data?.data as Overview)
    : undefined;

  const confidence = isRecord(overview?.outcome_confidence)
    ? (overview?.outcome_confidence as ConfidenceState)
    : undefined;
  const caf = isRecord(overview?.caf) ? (overview?.caf as CAFState) : undefined;
  const counts = asArray<GovernedCount>(overview?.counts);

  // Counts come from the governed overview (kind = finding|issue|recommendation).
  const findingsCount = countOf(counts, "finding");
  const issuesCount = countOf(counts, "issue");
  const recommendationsCount = countOf(counts, "recommendation");

  const anyLoading = overviewQ.isLoading;

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
        {/* Project actions — trigger analysis / add evidence (user-initiated commands). */}
        <ProjectActions projectId={projectId} />

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
