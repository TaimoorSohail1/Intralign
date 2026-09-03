/**
 * MRI-05 — CAF Triangle (DL-047).
 *
 * Presents the CAF assessment — Clarity / Alignment / Feasibility — as three
 * CO-EQUAL dimensions on an equilateral SVG triangle (one vertex each, no apex /
 * hierarchy). Each vertex shows its band qualitatively (Low / Moderate / High
 * understanding) and its reliability qualifier; the whole assessment carries its
 * `EpistemicLabel` (Derived + band) so it can never read as settled.
 *
 * Built with **SVG + MUI only** (no charting library). PRESENTS, never computes:
 * the indices come straight from the governed DTO and are NOT rendered as numbers
 * to the user (qualitative bands only — MRIW-C3).
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import type { CAFState, CAFDimensionView } from "../../api/generated/oSLORelease1API.schemas";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { BAND_LABEL } from "../../components/confidenceBand";
import { epistemicTones, surfaces } from "../../theme/tokens";

export interface CafTriangleProps {
  caf: CAFState | undefined | null;
}

function bandColor(band: CAFDimensionView["band"]): string {
  switch (band) {
    case "low":
      return epistemicTones.bandLow;
    case "medium":
      return epistemicTones.bandMedium;
    case "high":
      return epistemicTones.bandHigh;
  }
}

/** A CAF DTO is presentable only when all three dimensions carry a band. */
function isPresentableCaf(caf: CAFState | undefined | null): caf is CAFState {
  if (!caf) return false;
  const dims = [caf.clarity, caf.alignment, caf.feasibility];
  return dims.every((d) => d != null && typeof d.band === "string");
}

export function CafTriangle({ caf }: CafTriangleProps) {
  if (!isPresentableCaf(caf)) {
    return (
      <Box data-testid="mri-caf-triangle">
        <Box data-testid="mri-caf-triangle-empty" sx={{ p: 2 }}>
          <Typography variant="body2" color="text.secondary">
            CAF assessment not yet available.
          </Typography>
        </Box>
      </Box>
    );
  }

  // Equilateral triangle: top, bottom-left, bottom-right (co-equal vertices).
  const W = 260;
  const H = 230;
  const verts = [
    { key: "clarity", dim: caf.clarity, x: W / 2, y: 28, anchor: "middle", dy: -10 },
    { key: "alignment", dim: caf.alignment, x: 34, y: H - 36, anchor: "start", dy: 22 },
    {
      key: "feasibility",
      dim: caf.feasibility,
      x: W - 34,
      y: H - 36,
      anchor: "end",
      dy: 22,
    },
  ] as const;

  const points = verts.map((v) => `${v.x},${v.y}`).join(" ");

  return (
    <Box data-testid="mri-caf-triangle">
      <Box sx={{ mb: 1 }}>
        {/* the governed CAF assessment's epistemic standing — Derived, banded */}
        <EpistemicLabel epistemic={fromDerivedEnvelope(caf.label)} />
      </Box>
      <Box
        component="svg"
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label="CAF triangle — Clarity, Alignment and Feasibility as three co-equal dimensions of understanding"
        sx={{ width: "100%", maxWidth: W, height: "auto" }}
      >
        <polygon
          points={points}
          fill="rgba(74, 85, 104, 0.06)"
          stroke={surfaces.divider}
          strokeWidth={1.5}
        />
        {verts.map((v) => (
          <g key={v.key} data-testid={`caf-vertex-${v.key}`}>
            <circle cx={v.x} cy={v.y} r={7} fill={bandColor(v.dim.band)}>
              <title>{`${v.key}: ${BAND_LABEL[v.dim.band]} · ${v.dim.reliability}`}</title>
            </circle>
            <text
              x={v.x}
              y={v.y + v.dy}
              textAnchor={v.anchor}
              fontSize={13}
              fontWeight={600}
              fill={epistemicTones.derived}
              style={{ textTransform: "capitalize" }}
            >
              {v.dim.dimension}
            </text>
            <text
              x={v.x}
              y={v.y + v.dy + 16}
              textAnchor={v.anchor}
              fontSize={11}
              fill={bandColor(v.dim.band)}
            >
              {BAND_LABEL[v.dim.band]}
            </text>
          </g>
        ))}
      </Box>
      {/* reliability qualifiers — understanding is never shown as fully supported when it isn't */}
      <Stack spacing={0.25} sx={{ mt: 1 }}>
        {verts.map((v) => (
          <Typography
            key={`rel-${v.key}`}
            variant="caption"
            color="text.secondary"
            sx={{ textTransform: "capitalize" }}
          >
            {`${v.dim.dimension}: ${v.dim.reliability} reliability`}
          </Typography>
        ))}
      </Stack>
    </Box>
  );
}

export default CafTriangle;
