/**
 * EpistemicLabel — the single reusable epistemic-safety label (IC-WE-DISCLOSE E0).
 *
 * Every Wave E surface mounts THIS component to carry an item's epistemic standing,
 * so the labeling rule is enforced in exactly one place (decision #5). It renders:
 *   - standing: Attested (on record) vs Derived (a recomputable projection)
 *   - the plan-fact variant: Attested by the USER ("you confirmed") — not world-truth
 *   - the confidence band (low/medium/high) with the ±3 conservative edge guard
 *   - a conflict / contested marker
 *
 * Safety by construction (the negatives are the point):
 *   - The prop is a DISCRIMINATED UNION on `standing`. A Derived item literally has
 *     no way to pass attested/"settled" wording — confidence + conflict live ONLY on
 *     the derived arm; standing-source ("user"/"evidence"/"oslo") lives ONLY on the
 *     attested arm. You cannot render a Derived value as settled/confirmed.
 *   - The band always comes from `resolveBand` (rounds DOWN), so low can never show
 *     as high. The numeric value is never shown as a bare project-health number.
 */
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Tooltip from "@mui/material/Tooltip";
import { resolveBand, BAND_LABEL, type ConfidenceBand } from "./confidenceBand";
import { epistemicTones } from "../theme/tokens";
import type {
  DerivedEnvelope,
  ConfidenceBand as DtoBand,
} from "../api/generated/oSLORelease1API.schemas";

/** Who attested an on-record item. `user` is the plan-fact variant. */
export type AttestedSource = "user" | "evidence" | "oslo";

/** Attested arm — an on-record receipt. Carries no confidence/conflict. */
export interface AttestedStanding {
  standing: "attested";
  source: AttestedSource;
}

/**
 * Derived arm — a recomputable projection. Carries the confidence band + conflict.
 * Pass `confidenceValue` (0–100, banded via the edge guard) OR a pre-resolved
 * `band` straight off the DTO. Never both is required.
 */
export interface DerivedStanding {
  standing: "derived";
  confidenceValue?: number;
  band?: ConfidenceBand;
  conflict?: boolean;
}

export type EpistemicStanding = AttestedStanding | DerivedStanding;

export interface EpistemicLabelProps {
  epistemic: EpistemicStanding;
  /** Optional size pass-through for dense surfaces (e.g. issue cards). */
  size?: "small" | "medium";
}

const ATTESTED_SOURCE_TEXT: Record<AttestedSource, string> = {
  // plan fact: user-attested, explicitly NOT world-truth
  user: "You confirmed",
  evidence: "Attested (evidence)",
  oslo: "Attested (on record)",
};

const ATTESTED_SOURCE_HELP: Record<AttestedSource, string> = {
  user: "Recorded as factual in your plan because you confirmed it — not asserted as world-truth.",
  evidence: "On record, backed by attested evidence.",
  oslo: "On record in OSLO's canonical history.",
};

function bandColor(band: ConfidenceBand): string {
  switch (band) {
    case "low":
      return epistemicTones.bandLow;
    case "medium":
      return epistemicTones.bandMedium;
    case "high":
      return epistemicTones.bandHigh;
  }
}

function StandingChip({ epistemic, size }: EpistemicLabelProps) {
  if (epistemic.standing === "attested") {
    return (
      <Tooltip title={ATTESTED_SOURCE_HELP[epistemic.source]}>
        <Chip
          size={size === "medium" ? "medium" : "small"}
          label={ATTESTED_SOURCE_TEXT[epistemic.source]}
          variant="outlined"
          sx={{
            color: epistemicTones.attested,
            borderColor: epistemicTones.attested,
            fontWeight: 600,
          }}
        />
      </Tooltip>
    );
  }
  // Derived — always reads as a projection, never settled/confirmed.
  return (
    <Tooltip title="A recomputable projection from OSLO's current understanding — not settled; it updates as understanding changes.">
      <Chip
        size={size === "medium" ? "medium" : "small"}
        label="Derived"
        variant="outlined"
        sx={{
          color: epistemicTones.derived,
          borderColor: epistemicTones.derived,
          fontWeight: 600,
        }}
      />
    </Tooltip>
  );
}

function ConfidenceBandChip({ standing }: { standing: DerivedStanding }) {
  const band: ConfidenceBand =
    standing.band ??
    (typeof standing.confidenceValue === "number"
      ? resolveBand(standing.confidenceValue)
      : "low");
  return (
    <Tooltip title="How much OSLO trusts its understanding here — not project health, readiness, or probability.">
      <Chip
        data-testid="confidence-band"
        data-band={band}
        size="small"
        label={BAND_LABEL[band]}
        variant="outlined"
        sx={{ color: bandColor(band), borderColor: bandColor(band) }}
      />
    </Tooltip>
  );
}

function ConflictMarker() {
  return (
    <Tooltip title="This item surfaces an unresolved conflict — OSLO presents it, it does not resolve it.">
      <Chip
        data-testid="conflict-marker"
        size="small"
        label="Conflict"
        variant="filled"
        sx={{
          color: "#fff",
          backgroundColor: epistemicTones.conflict,
          fontWeight: 600,
        }}
      />
    </Tooltip>
  );
}

export function EpistemicLabel({ epistemic, size = "small" }: EpistemicLabelProps) {
  return (
    <Box
      data-testid="epistemic-label"
      data-standing={epistemic.standing}
      data-source={epistemic.standing === "attested" ? epistemic.source : undefined}
      sx={{ display: "inline-flex", gap: 0.75, alignItems: "center", flexWrap: "wrap" }}
    >
      <StandingChip epistemic={epistemic} size={size} />
      {epistemic.standing === "derived" && (
        <>
          <ConfidenceBandChip standing={epistemic} />
          {epistemic.conflict ? <ConflictMarker /> : null}
        </>
      )}
    </Box>
  );
}

/**
 * Adapter: map a generated `DerivedEnvelope` DTO (the `label` field on every
 * Derived entity DTO) into the safe Derived prop. Surfaces consume the Orval
 * client and hand the envelope straight to the label — they never re-implement
 * the labeling rule. By construction this only ever yields a Derived standing,
 * so a Derived DTO can never be rendered as attested/settled.
 */
export function fromDerivedEnvelope(
  label: DerivedEnvelope | undefined | null,
): DerivedStanding {
  const dtoBand = label?.confidence_band as DtoBand | null | undefined;
  return {
    standing: "derived",
    band: dtoBand ?? undefined,
    confidenceValue:
      typeof label?.confidence_value === "number" ? label.confidence_value : undefined,
    conflict: label?.conflict_state === "contested",
  };
}

export default EpistemicLabel;
