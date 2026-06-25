/**
 * A single finding SUMMARY row inside the MRI discovery list. MRI lists, never
 * duplicates, a finding (MRIE-2): it shows a summary + the finding's epistemic
 * label and routes to its Finding Panel (why). It is descriptive, never an
 * action/command (MRIE-7), and offers no edit/resolve affordance.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import { Link } from "@tanstack/react-router";
import type { Finding, Severity } from "../../api/generated/oSLORelease1API.schemas";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { epistemicTones } from "../../theme/tokens";

const SEV_LABEL: Record<Severity, string> = {
  critical: "Critical",
  moderate: "Moderate",
  warning: "Warning",
};

export interface FindingRowProps {
  finding: Finding;
  projectId: string;
}

export function FindingRow({ finding, projectId }: FindingRowProps) {
  const sev = (finding.severity ?? "warning") as Severity;
  return (
    <Box
      data-testid="finding-row"
      data-finding-id={finding.finding_id}
      sx={{ py: 1, borderBottom: 1, borderColor: "divider" }}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
        <Chip
          size="small"
          label={SEV_LABEL[sev]}
          variant="outlined"
          data-testid="finding-severity"
          sx={{ color: epistemicTones.bandLow, borderColor: epistemicTones.bandLow }}
        />
        <Link
          to="/projects/$projectId/findings/$findingId"
          params={{ projectId, findingId: finding.finding_id }}
          style={{ color: "inherit" }}
        >
          <Typography variant="body2" component="span" sx={{ fontWeight: 600 }}>
            {finding.summary ?? finding.finding_id}
          </Typography>
        </Link>
      </Box>
      <Box sx={{ mt: 0.5 }}>
        {/* the finding's epistemic standing — Derived projection, banded, conflict-aware */}
        <EpistemicLabel epistemic={fromDerivedEnvelope(finding.label)} />
      </Box>
    </Box>
  );
}

export default FindingRow;
