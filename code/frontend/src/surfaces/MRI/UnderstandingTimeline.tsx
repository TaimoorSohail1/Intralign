/**
 * MRI-06 — Understanding Timeline (DL-047).
 *
 * Presents the CHR history trail of how understanding evolved — the project's
 * analysis runs newest-first (the runs that appended Cognition History Records).
 * It shows the CURRENT understanding prominently AND the prior history (append-only
 * presentation, MRI Workspace Spec §15): history is never silently discarded, and
 * the Timeline mutates nothing.
 *
 * Built with **SVG + MUI primitives only** — a simple vertical SVG rail with one
 * node per run, alongside MUI text. No charting library.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import type { AnalysisRun } from "../../api/generated/oSLORelease1API.schemas";
import { epistemicTones, surfaces } from "../../theme/tokens";

export interface UnderstandingTimelineProps {
  runs: AnalysisRun[];
  projectId: string;
}

const RUN_TYPE_LABEL: Record<string, string> = {
  fast_analysis_pass: "Fast pass",
  deep_analysis_pass: "Deep pass",
};

function whenLabel(run: AnalysisRun): string {
  const ts = run.completed_at ?? run.started_at;
  if (!ts) return "time pending";
  try {
    return new Date(ts).toLocaleString();
  } catch {
    return ts;
  }
}

export function UnderstandingTimeline({ runs }: UnderstandingTimelineProps) {
  if (runs.length === 0) {
    return (
      <Box data-testid="mri-timeline">
        <Box data-testid="mri-timeline-empty" sx={{ p: 2 }}>
          <Typography variant="body2" color="text.secondary">
            No analysis history yet.
          </Typography>
        </Box>
      </Box>
    );
  }

  const railX = 10;
  const step = 64;
  const top = 16;
  const height = top * 2 + (runs.length - 1) * step + 24;

  return (
    <Box data-testid="mri-timeline" sx={{ display: "flex", gap: 1 }}>
      {/* SVG rail — one node per run, newest at the top */}
      <Box
        component="svg"
        viewBox={`0 0 24 ${height}`}
        role="img"
        aria-label="Understanding history trail"
        sx={{ width: 24, flexShrink: 0, height: "auto" }}
      >
        <line
          x1={railX}
          y1={top}
          x2={railX}
          y2={top + (runs.length - 1) * step}
          stroke={surfaces.divider}
          strokeWidth={2}
        />
        {runs.map((run, i) => (
          <circle
            key={run.analysis_run_id}
            cx={railX}
            cy={top + i * step}
            r={i === 0 ? 7 : 5}
            fill={i === 0 ? epistemicTones.attested : epistemicTones.derived}
          />
        ))}
      </Box>

      <Box sx={{ flexGrow: 1 }}>
        {runs.map((run, i) => {
          const isCurrent = i === 0;
          return (
            <Box
              key={run.analysis_run_id}
              data-testid="timeline-entry"
              data-current={isCurrent ? "true" : undefined}
              sx={{ minHeight: 64, pb: 1 }}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}>
                <Typography variant="subtitle2">
                  {RUN_TYPE_LABEL[run.run_type] ?? run.run_type}
                </Typography>
                {isCurrent ? (
                  <Chip
                    data-testid="timeline-current"
                    size="small"
                    label="Current understanding"
                    variant="outlined"
                    sx={{ color: epistemicTones.attested, borderColor: epistemicTones.attested }}
                  />
                ) : (
                  <Chip
                    size="small"
                    label="History"
                    variant="outlined"
                    sx={{ color: epistemicTones.derived, borderColor: epistemicTones.derived }}
                  />
                )}
              </Box>
              <Typography variant="caption" color="text.secondary" display="block">
                {whenLabel(run)} · {run.run_status}
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block">
                {run.analysis_run_id}
              </Typography>
            </Box>
          );
        })}
      </Box>
    </Box>
  );
}

export default UnderstandingTimeline;
