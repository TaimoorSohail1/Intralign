/**
 * Honest-limit disclosure fixtures (DTM-0029, DL-048 UP-4).
 *
 * DATA FINDING (binding — see the worker report): there is NO scope/budget-limit DTO
 * in the DTM-0018 REST surface. The generated client exposes confidence/CAF/findings/
 * recommendations/analysis-runs/notifications — none carries a "partial orientation" /
 * "envelope exceeded" / "tier limit" flag. DL-048 constraint-detection signals (cap-hit,
 * envelope-exceeded, budget gate) are produced backend-side and are NOT yet exposed over
 * REST. We therefore model the honest-limit input as a NON-canonical presentation shape
 * (`HonestLimit`) the component consumes — and FLAG the dependency. We invent no DTO and
 * write nothing; this is a presentation contract for when the signal is exposed.
 *
 * The upgrade copy is commodity (MON-04, `12_freemium_tier_behavior_logic.md` UP-4) — the
 * honest disclosure is the contracted part. The copy below is placeholder per the spec.
 */
import type { HonestLimit } from "./HonestLimitDisclosure";

/** Envelope exceeded → partial orientation, WITH the commodity upgrade prompt (UP-4). */
export const partialLimitFixture: HonestLimit = {
  limited: true,
  // The reason the coverage is reduced — shown verbatim (epistemic-safety obligation).
  reason: "This project exceeds the Free tier size, so the analysis covered only part of it.",
  coverage_note: "Roughly the first portion of the project content was analyzed.",
  // The commodity Upgrade-Prompt (UP-4) — rendered ALONGSIDE, never instead of.
  upgrade: {
    message: "Basic analyzes projects up to ~100k words.",
    cta_label: "See Basic",
  },
};

/** Limited, but NO upgrade prompt supplied — the disclosure must still render. */
export const partialLimitNoUpgradeFixture: HonestLimit = {
  limited: true,
  reason: "The monthly analysis budget was reached, so this run is partial.",
  coverage_note: "Coverage was reduced to stay within the remaining budget.",
};

/** Not limited — a complete run. The component renders NOTHING. */
export const completeRunFixture: HonestLimit = {
  limited: false,
};
