/**
 * DTM-0023 — Issue Cards (IC-WE-DISCLOSE E1).
 *
 * Presents Issues as cards. An **Issue** is Evaluate's *prioritized Finding* — a
 * Finding to which Evaluate has assigned a `severity` (CONTEXT.md / `Issue` in
 * `shared/epistemic.py`). Each card carries:
 *
 *   - the issue **severity** as a governed qualifier (critical / moderate /
 *     warning) — a LABEL, never a leaked score / probability / health number;
 *   - the source Finding's **Derived confidence** via `fromDerivedEnvelope` →
 *     `EpistemicLabel` (banded, conflict-aware) — a recomputable projection,
 *     never shown as settled; confidence = trust-in-understanding, never project
 *     health / readiness / probability;
 *   - a **link back to the source Finding** (the Finding Panel route,
 *     `/projects/$projectId/findings/$findingId`) — the audit answer to "which
 *     Finding became this Issue".
 *
 * FIRST-CLASS ISSUES READ (DTM-0039 → DTM-0038): the cards now render from the dedicated
 * `/issues` read (`useListIssues…`) — the first-class `Issue` DTO (Evaluate's prioritized
 * Finding). Each Issue carries its `issue_id`, the source `finding_id` lineage, the
 * governed `severity`, and the Derived confidence `label`. This replaces the DTM-0023
 * placeholder that filtered the findings list by severity.
 *
 * Read-only: there is no edit / score / accept / defer / prioritise / generate /
 * recompute control anywhere on the surface (decision #3 — Disclose presents,
 * never generates; only reanalysis changes an assessment, and reanalysis is not
 * a Disclose affordance). Loading / empty states render cleanly and positively.
 *
 * It consumes the `useListIssues…` hook read-only.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import { Link } from "@tanstack/react-router";

import { useListIssuesV1ProjectsProjectIdIssuesGet } from "../../api/generated/issues/issues";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { epistemicTones } from "../../theme/tokens";
import type {
  Issue,
  FindingType,
  Severity,
} from "../../api/generated/oSLORelease1API.schemas";

export interface IssueCardsProps {
  projectId: string;
}

/** User-friendly governed severity labels (a label, never a score). */
const SEVERITY_LABEL: Record<Severity, string> = {
  critical: "Critical",
  moderate: "Moderate",
  warning: "Warning",
};

/** Severity tone — conservative; severe reads in the low-band tone, not green. */
const SEVERITY_TONE: Record<Severity, string> = {
  critical: epistemicTones.bandLow,
  moderate: epistemicTones.bandMedium,
  warning: epistemicTones.bandMedium,
};

const FINDING_TYPE_LABEL: Record<FindingType, string> = {
  missing_information: "Missing information",
  ambiguity: "Ambiguity",
  assumption: "Assumption",
  inference: "Inference",
  conflict: "Conflict",
  constraint: "Constraint",
  coverage_gap: "Coverage gap",
};

/** True for a plain array of objects (defensive against partial responses). */
function asIssueArray(v: unknown): Issue[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as Issue[]) : [];
}

/**
 * One Issue card — a prioritized Finding. Renders its severity + Derived
 * confidence label + a link to its source Finding. Pure presentation; no control.
 */
function IssueCard({ issue, projectId }: { issue: Issue; projectId: string }) {
  const severity = issue.severity as Severity;
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2 }}
      data-testid="issue-card"
      data-finding-id={issue.finding_id}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 1 }}>
        {/* Severity — a governed qualifier (the Issue's defining attribute). */}
        <Chip
          size="small"
          variant="outlined"
          label={SEVERITY_LABEL[severity] ?? severity}
          data-testid="issue-severity"
          data-severity={severity}
          sx={{ color: SEVERITY_TONE[severity], borderColor: SEVERITY_TONE[severity], fontWeight: 600 }}
        />
        {/* The source Finding's type (descriptive lineage label). */}
        <Chip
          size="small"
          variant="outlined"
          label={FINDING_TYPE_LABEL[issue.finding_type] ?? issue.finding_type}
          data-testid="issue-finding-type"
          data-finding-type={issue.finding_type}
        />
        {/* Derived confidence — banded, conflict-aware; never settled. */}
        <EpistemicLabel epistemic={fromDerivedEnvelope(issue.label)} />
      </Box>

      <Typography variant="body1" sx={{ mb: 1.5 }}>
        {issue.summary ?? issue.finding_id}
      </Typography>

      {/* Link back to the SOURCE FINDING — the Finding Panel context. */}
      <Link
        to="/projects/$projectId/findings/$findingId"
        params={{ projectId, findingId: issue.finding_id }}
        style={{ textDecoration: "none" }}
        data-testid="view-source-finding"
      >
        <Button variant="text" component="span" size="small">
          View source finding
        </Button>
      </Link>
    </Paper>
  );
}

export function IssueCards({ projectId }: IssueCardsProps) {
  const issuesQ = useListIssuesV1ProjectsProjectIdIssuesGet(projectId);

  // The first-class /issues read returns the governed Issues directly (Evaluate's
  // prioritized Findings) — no client-side severity filter needed.
  const issues = asIssueArray(issuesQ.data?.data);

  const loading = issuesQ.isLoading;

  return (
    <Box data-testid="issue-cards" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Issues
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Prioritized findings, each with how confident OSLO is in its understanding and a link
        to the finding it came from. OSLO presents these; it does not resolve or prioritize them
        for you — only reanalysis changes the assessment.
      </Typography>

      {loading ? (
        <Box
          data-testid="issue-cards-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading issues…
          </Typography>
        </Box>
      ) : issues.length === 0 ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="issue-cards-empty" variant="body2" color="text.secondary">
            No issues here yet — understanding looks clear in this area. (This reflects the
            current analysis; it is not an incomplete or pending result.)
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {issues.map((issue) => (
            <IssueCard key={issue.issue_id} issue={issue} projectId={projectId} />
          ))}
        </Stack>
      )}
    </Box>
  );
}

export default IssueCards;
