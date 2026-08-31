/**
 * Confidence band resolution with the ±3 CONSERVATIVE edge guard.
 *
 * Source of truth: CONTEXT.md (Wave E — Epistemic-safety labeling) and
 * deep-task-0019.md. Confidence is *trust in OSLO's understanding*, banded:
 *   0–49  -> low
 *   50–74 -> medium
 *   75–100-> high
 *
 * The edge guard is CONSERVATIVE: a value that sits *just above* a band boundary
 * (50 or 75) is pulled DOWN into the lower band, so we never overstate trust. The
 * boundary value itself (50, 75) keeps the higher band; a value 1–2 points above a
 * boundary drops; by +3 it has cleared the guard and keeps the natural band.
 *
 * Locked boundary cases (from the task — these are the contract):
 *   48 -> low     (already low; below the boundary, unaffected)
 *   50 -> medium  (boundary value keeps the higher band)
 *   52 -> low     (50+2, within the guard -> drop)
 *   53 -> medium  (50+3, cleared the guard)
 *   74 -> medium  (no boundary above it)
 *   75 -> high    (boundary value keeps the higher band)
 *   77 -> medium  (75+2, within the guard -> drop)
 *   78 -> high    (75+3, cleared the guard)
 *
 * The guard only ever rounds DOWN (never up), which is why low can never display
 * as high and a Derived value can never be overstated.
 */
export type ConfidenceBand = "low" | "medium" | "high";

const BOUNDARIES: Array<{ at: number; lower: ConfidenceBand }> = [
  { at: 50, lower: "low" }, // the low/medium boundary
  { at: 75, lower: "medium" }, // the medium/high boundary
];

/** The natural (un-guarded) band for a 0–100 value. */
function naturalBand(value: number): ConfidenceBand {
  if (value < 50) return "low";
  if (value < 75) return "medium";
  return "high";
}

/**
 * Resolve a 0–100 confidence value to its user-facing band, applying the ±3
 * conservative edge guard. Out-of-range values are clamped conservatively.
 */
export function resolveBand(value: number): ConfidenceBand {
  // Clamp: a NaN or out-of-range value resolves to the nearest end conservatively.
  if (!Number.isFinite(value)) return "low";
  const v = Math.max(0, Math.min(100, value));

  let band = naturalBand(v);
  // If v sits within (boundary, boundary+2] for any boundary, drop to the lower band.
  for (const { at, lower } of BOUNDARIES) {
    if (v > at && v <= at + 2) {
      band = lower;
    }
  }
  return band;
}

/** Human band label — trust-in-understanding wording, never project health. */
export const BAND_LABEL: Record<ConfidenceBand, string> = {
  low: "Low understanding",
  medium: "Moderate understanding",
  high: "High understanding",
};
