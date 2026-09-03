/**
 * MRI-04 — Artifact Understanding Heatmap (DL-047).
 *
 * The Workspace's primary discovery-through-visualization surface: it makes the
 * CONCENTRATION of weakness visible at a glance (MRI Workspace Spec §8) so the user
 * sees "where should I look?" without reading a flat list. Built with **SVG + MUI
 * primitives only** — no charting library (decision: no new dependency).
 *
 * Qualitative ONLY (MRIW-C3 / MRIE-C4): intensity expresses more/less concentration
 * via opacity tiers (none / light / strong) — never a numeric score, percentage, or
 * rank. It PRESENTS the current findings; it computes and resolves nothing.
 *
 * Grid: rows = MRI categories (Missing / Risky / Incomplete); columns = the existing
 * qualitative severity concept (Critical / Moderate / Warning).
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import type { Finding, Severity } from "../../api/generated/oSLORelease1API.schemas";
import { epistemicTones, surfaces } from "../../theme/tokens";
import {
  MRI_CATEGORY_ORDER,
  MRI_CATEGORY_LABEL,
  categoryOf,
  type MriCategory,
} from "./categories";

const SEVERITIES: Severity[] = ["critical", "moderate", "warning"];
const SEV_LABEL: Record<Severity, string> = {
  critical: "Critical",
  moderate: "Moderate",
  warning: "Warning",
};

/** Qualitative concentration tier — NEVER a number shown to the user. */
type Tier = "none" | "light" | "strong";
function tierFor(count: number): Tier {
  if (count <= 0) return "none";
  if (count === 1) return "light";
  return "strong";
}
function tierFill(tier: Tier): string {
  switch (tier) {
    case "none":
      return surfaces.paper;
    case "light":
      return "rgba(122, 62, 0, 0.30)"; // dark-amber wash, qualitative
    case "strong":
      return "rgba(122, 62, 0, 0.70)";
  }
}
const TIER_WORD: Record<Tier, string> = {
  none: "no weakness",
  light: "some weakness",
  strong: "concentrated weakness",
};

export interface UnderstandingHeatmapProps {
  findings: Finding[];
  projectId: string;
}

export function UnderstandingHeatmap({ findings }: UnderstandingHeatmapProps) {
  if (findings.length === 0) {
    return (
      <Box data-testid="mri-heatmap">
        <Box data-testid="mri-heatmap-empty" sx={{ p: 2 }}>
          <Typography variant="body2" color="text.secondary">
            No weaknesses found — understanding looks clear.
          </Typography>
        </Box>
      </Box>
    );
  }

  // Tally concentration per (category × severity) — qualitative grouping only.
  const counts: Record<MriCategory, Record<Severity, number>> = {
    missing: { critical: 0, moderate: 0, warning: 0 },
    risky: { critical: 0, moderate: 0, warning: 0 },
    incomplete: { critical: 0, moderate: 0, warning: 0 },
  };
  for (const f of findings) {
    const sev = (f.severity ?? "warning") as Severity;
    counts[categoryOf(f)][sev] += 1;
  }

  // SVG layout — a labelled grid. Pure presentation; dimensions are layout, not data.
  const cell = 56;
  const gap = 8;
  const rowLabelW = 110;
  const colLabelH = 28;
  const cols = SEVERITIES.length;
  const rows = MRI_CATEGORY_ORDER.length;
  const width = rowLabelW + cols * (cell + gap);
  const height = colLabelH + rows * (cell + gap);

  return (
    <Box data-testid="mri-heatmap">
      <Box
        component="svg"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Weakness concentration heatmap across understanding categories and severity"
        sx={{ width: "100%", maxWidth: width, height: "auto" }}
      >
        {/* column headers — severity (qualitative) */}
        {SEVERITIES.map((sev, c) => (
          <text
            key={`col-${sev}`}
            x={rowLabelW + c * (cell + gap) + cell / 2}
            y={colLabelH - 10}
            textAnchor="middle"
            fontSize={12}
            fill={epistemicTones.derived}
          >
            {SEV_LABEL[sev]}
          </text>
        ))}
        {MRI_CATEGORY_ORDER.map((cat, r) => (
          <g key={`row-${cat}`}>
            {/* row header — MRI category */}
            <text
              x={0}
              y={colLabelH + r * (cell + gap) + cell / 2 + 4}
              fontSize={13}
              fontWeight={600}
              fill={epistemicTones.derived}
            >
              {MRI_CATEGORY_LABEL[cat]}
            </text>
            {SEVERITIES.map((sev, c) => {
              const n = counts[cat][sev];
              const tier = tierFor(n);
              return (
                <rect
                  key={`cell-${cat}-${sev}`}
                  data-testid="heatmap-cell"
                  data-category={cat}
                  data-severity={sev}
                  data-tier={tier}
                  x={rowLabelW + c * (cell + gap)}
                  y={colLabelH + r * (cell + gap)}
                  width={cell}
                  height={cell}
                  rx={6}
                  fill={tierFill(tier)}
                  stroke={surfaces.divider}
                  strokeWidth={1}
                >
                  <title>{`${MRI_CATEGORY_LABEL[cat]} · ${SEV_LABEL[sev]}: ${TIER_WORD[tier]}`}</title>
                </rect>
              );
            })}
          </g>
        ))}
      </Box>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
        Intensity shows where weakness concentrates — qualitative, not a measurement.
      </Typography>
    </Box>
  );
}

export default UnderstandingHeatmap;
