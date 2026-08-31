/**
 * MRI-07 — Understanding Dependencies / blocked-awaiting-review (DL-047).
 *
 * Presents the findings that BLOCK understanding — those still open / awaiting
 * review (not closed or superseded). These are the weaknesses the user's
 * understanding depends on resolving. PRESENTATION ONLY: it surfaces them and
 * routes to their Finding Panel; it never resolves, accepts, or changes a finding's
 * lifecycle state (only reanalysis does — MRIE-6).
 *
 * Each blocking item carries its `EpistemicLabel` (Derived + band + conflict). No
 * charting library — a simple MUI list with a small SVG dependency glyph per node.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import { Link } from "@tanstack/react-router";
import type { Finding } from "../../api/generated/oSLORelease1API.schemas";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { isAwaitingReview, severityRank } from "./categories";
import { epistemicTones } from "../../theme/tokens";

export interface UnderstandingDependenciesProps {
  findings: Finding[];
  projectId: string;
}

const STATUS_LABEL: Record<string, string> = {
  detected: "Awaiting review",
  acknowledged: "Acknowledged — awaiting review",
  addressed: "Addressed — awaiting confirmation",
  reopened: "Reopened — awaiting review",
};

function DependencyGlyph() {
  // a tiny SVG "link" glyph — purely decorative, presentation only
  return (
    <Box
      component="svg"
      viewBox="0 0 16 16"
      aria-hidden="true"
      sx={{ width: 16, height: 16, flexShrink: 0, mt: 0.5 }}
    >
      <circle cx={4} cy={4} r={2.5} fill={epistemicTones.derived} />
      <circle cx={12} cy={12} r={2.5} fill={epistemicTones.derived} />
      <line x1={4} y1={4} x2={12} y2={12} stroke={epistemicTones.derived} strokeWidth={1.5} />
    </Box>
  );
}

export function UnderstandingDependencies({
  findings,
  projectId,
}: UnderstandingDependenciesProps) {
  const blocking = findings
    .filter(isAwaitingReview)
    .sort((a, b) => severityRank(a.severity) - severityRank(b.severity));

  if (blocking.length === 0) {
    return (
      <Box data-testid="mri-dependencies">
        <Box data-testid="mri-dependencies-empty" sx={{ p: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Nothing is blocked or awaiting review.
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box data-testid="mri-dependencies">
      <List dense disablePadding>
        {blocking.map((f) => (
          <ListItem
            key={f.finding_id}
            data-testid="dependency-node"
            alignItems="flex-start"
            sx={{ gap: 1, py: 0.75 }}
          >
            <DependencyGlyph />
            <Box sx={{ flexGrow: 1 }}>
              <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
                <Link
                  to="/projects/$projectId/findings/$findingId"
                  params={{ projectId, findingId: f.finding_id }}
                  style={{ color: "inherit" }}
                >
                  <Typography variant="body2" sx={{ fontWeight: 600 }} component="span">
                    {f.summary ?? f.finding_id}
                  </Typography>
                </Link>
                <EpistemicLabel epistemic={fromDerivedEnvelope(f.label)} />
              </Box>
              <Typography variant="caption" color="text.secondary">
                {STATUS_LABEL[f.status ?? "detected"] ?? "Awaiting review"}
              </Typography>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default UnderstandingDependencies;
