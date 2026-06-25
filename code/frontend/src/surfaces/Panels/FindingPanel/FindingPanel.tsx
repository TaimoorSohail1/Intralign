/**
 * DTM-0021 — the Finding Panel (IC-WE-DISCLOSE E1).
 *
 * The contextual Finding-detail surface (Finding Panel Spec v1). It PRESENTS one
 * Finding and NEVER GENERATES:
 *
 *   - Finding summary + a user-friendly finding type + severity + affected CAF
 *     dimension(s) (descriptive header, §E/§F).
 *   - The finding's own Derived confidence label via `fromDerivedEnvelope` →
 *     `EpistemicLabel`; a Derived projection, banded, never shown as settled.
 *   - Its **Attested evidence anchors** — the evidence lineage (`evidence_links`),
 *     each rendered with the EpistemicLabel attested/evidence variant (§G). The
 *     finding is traceable to its evidence; evidence is never rendered as Derived.
 *   - A **conflict marker** when the finding is contested — surfaced, NOT resolved
 *     (CONTEXT.md: conflicts surfaced, not resolved).
 *   - The **RP-C1 affordance**: a link to the nested Recommendation Panel route
 *     (`…/findings/$findingId/recommendations`). Recommendations are NOT rendered
 *     inline here (that's DTM-0022) — only the affordance to open them.
 *
 * Read-only: there is no edit / accept / reject / defer / resolve / generate /
 * recompute control anywhere on the panel (Finding Panel Spec §K prohibitions;
 * decision #3 — only reanalysis changes assessment, and reanalysis is not a
 * Disclose affordance). Loading / not-found / empty-evidence states render
 * cleanly because projections may be absent until upstream populates them.
 *
 * It consumes the DTM-0018 `useGetFinding…` hook read-only.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";
import { Link } from "@tanstack/react-router";

import { useGetFindingV1FindingsFindingIdGet } from "../../../api/generated/findings/findings";
import { EpistemicLabel, fromDerivedEnvelope } from "../../../components/EpistemicLabel";
import { epistemicTones } from "../../../theme/tokens";
import type {
  Finding,
  FindingType,
  Severity,
  Dimension,
} from "../../../api/generated/oSLORelease1API.schemas";

export interface FindingPanelProps {
  projectId: string;
  findingId: string;
}

/** User-friendly labels for the finding type (descriptive, never an action). */
const FINDING_TYPE_LABEL: Record<FindingType, string> = {
  missing_information: "Missing information",
  ambiguity: "Ambiguity",
  assumption: "Assumption",
  inference: "Inference",
  conflict: "Conflict",
  constraint: "Constraint",
  coverage_gap: "Coverage gap",
};

const SEVERITY_LABEL: Record<Severity, string> = {
  critical: "Critical",
  moderate: "Moderate",
  warning: "Warning",
};

const DIMENSION_LABEL: Record<Dimension, string> = {
  clarity: "Clarity",
  alignment: "Alignment",
  feasibility: "Feasibility",
};

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

/**
 * One Attested evidence anchor — an item of the finding's evidence lineage. It is
 * ON RECORD (attested), sourced from evidence, so it carries the EpistemicLabel
 * attested/evidence variant. It can never read as a Derived projection.
 */
function EvidenceAnchor({ anchorId }: { anchorId: string }) {
  return (
    <Box
      data-testid="evidence-anchor"
      data-anchor-id={anchorId}
      sx={{
        display: "flex",
        gap: 1,
        alignItems: "center",
        flexWrap: "wrap",
        py: 0.75,
        borderBottom: 1,
        borderColor: "divider",
      }}
    >
      <Typography variant="body2" sx={{ fontFamily: "monospace" }}>
        {anchorId}
      </Typography>
      {/* Attested, sourced from evidence — the evidence the finding is grounded in. */}
      <EpistemicLabel epistemic={{ standing: "attested", source: "evidence" }} />
    </Box>
  );
}

export function FindingPanel({ projectId, findingId }: FindingPanelProps) {
  const findingQ = useGetFindingV1FindingsFindingIdGet(findingId);

  // Defensive coercion: the projection may be absent until upstream populates it,
  // and a partial/unexpected response must never crash the panel.
  const finding: Finding | undefined = isRecord(findingQ.data?.data)
    ? (findingQ.data?.data as Finding)
    : undefined;

  const loading = findingQ.isLoading;

  return (
    <Box data-testid="finding-panel" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Finding
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Why this finding exists, the evidence it rests on, and how confident OSLO is in
        its understanding. OSLO presents this; it does not resolve it — only reanalysis
        changes the assessment.
      </Typography>

      {loading ? (
        <Box
          data-testid="finding-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading the finding…
          </Typography>
        </Box>
      ) : !finding ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="finding-not-found" variant="body2" color="text.secondary">
            This finding is unavailable. It may be outside your scope, or not yet
            projected. (Distinct from “not yet analyzed”.)
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {/* ── Header (§E) — descriptive: type · severity · affected dimensions ── */}
          <Section title="Summary" testId="finding-summary">
            <Box
              sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 1 }}
            >
              <Chip
                size="small"
                variant="outlined"
                label={FINDING_TYPE_LABEL[finding.finding_type] ?? finding.finding_type}
                data-testid="finding-type"
                data-finding-type={finding.finding_type}
              />
              {finding.severity ? (
                <Chip
                  size="small"
                  variant="outlined"
                  label={SEVERITY_LABEL[finding.severity as Severity] ?? finding.severity}
                  data-testid="finding-severity"
                  sx={{
                    color: epistemicTones.bandLow,
                    borderColor: epistemicTones.bandLow,
                  }}
                />
              ) : null}
              {(finding.affected_dimensions ?? []).map((d) => (
                <Chip
                  key={d}
                  size="small"
                  variant="outlined"
                  label={DIMENSION_LABEL[d] ?? d}
                  data-testid="finding-dimension"
                />
              ))}
            </Box>
            <Typography variant="body1">
              {finding.summary ?? finding.finding_id}
            </Typography>
          </Section>

          {/* ── Confidence — the finding's Derived label (banded, conflict-aware) ── */}
          <Section
            title="Confidence in this understanding"
            testId="finding-confidence"
            subtitle="How much OSLO trusts its understanding here — not project health, readiness, or probability."
          >
            <EpistemicLabel epistemic={fromDerivedEnvelope(finding.label)} />
          </Section>

          {/* ── Evidence (§G) — the Attested evidence lineage, traceable ── */}
          <Section
            title="Evidence"
            testId="finding-evidence"
            subtitle="The attested evidence this finding is grounded in — traceable, on record."
          >
            {(finding.evidence_links ?? []).length === 0 ? (
              <Typography
                data-testid="finding-evidence-empty"
                variant="body2"
                color="text.secondary"
              >
                No reachable evidence anchors are recorded for this finding.
              </Typography>
            ) : (
              <Box>
                {(finding.evidence_links ?? []).map((anchorId) => (
                  <EvidenceAnchor key={anchorId} anchorId={anchorId} />
                ))}
              </Box>
            )}
          </Section>

          <Divider />

          {/* ── RP-C1 — affordance ONLY; recommendations are NOT rendered inline ── */}
          <Section
            title="Recommendations"
            testId="finding-recommendations-affordance"
            subtitle="Advisory recommendations for this finding open in the Recommendation Panel (only in this finding's context)."
          >
            <Link
              to="/projects/$projectId/findings/$findingId/recommendations"
              params={{ projectId, findingId }}
              style={{ textDecoration: "none" }}
              data-testid="view-recommendations"
            >
              <Button variant="outlined" component="span">
                View recommendations
              </Button>
            </Link>
          </Section>
        </Stack>
      )}
    </Box>
  );
}

export default FindingPanel;
