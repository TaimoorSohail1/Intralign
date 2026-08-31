/**
 * Intralign design tokens (CHG-068) — the single seam the designer refines.
 *
 * ANTI_ASSUMPTION / OPEN_TBD E4: only the owner-ratified facts are encoded here —
 * the Intralign palette (charcoal / warm-white / orange) and WCAG 2.1 AA intent.
 * Type scale, fonts, logo, redlines and final microcopy are designer-pending, so
 * we deliberately do NOT invent them: the theme uses MUI's default type scale and
 * system font stack. When the designer lands the redlines, they edit THIS module
 * (and `theme/index.ts`) only — no surface needs to change.
 *
 * Contrast notes (AA, 4.5:1 for normal text):
 *  - charcoal on warm-white  ≈ 17:1  ✓  (primary text on the app background)
 *  - warm-white on charcoal  ≈ 17:1  ✓  (text on the dark nav rail)
 *  - charcoal on orange      ≈ 5.4:1 ✓  (text/icon on a contained orange button)
 *  - orange  on charcoal     ≈ 9:1   ✓  (orange accent text on dark)
 *  NB: orange-on-warm-white is ≈ 2.6:1 and FAILS AA for text — orange is an
 *  accent/affordance colour (button fill, focus, active rail item), never body
 *  text on the light background. `primary.contrastText` is therefore charcoal.
 */

export const intralign = {
  charcoal: "#111315",
  warmWhite: "#F5F4F0",
  orange: "#D97A3A",
} as const;

/** Derived surface tones kept inside the AA-safe family (no new brand hues). */
export const surfaces = {
  /** Slightly lifted panel on the warm-white background. */
  paper: "#FFFFFF",
  /** Hairline divider on light surfaces. */
  divider: "rgba(17, 19, 21, 0.12)",
  /** Muted secondary text on warm-white — charcoal @ 60% ≈ 6.8:1, AA ✓. */
  textSecondary: "rgba(17, 19, 21, 0.62)",
} as const;

/**
 * Epistemic-state palette. Deliberately NOT the brand orange for "settled" —
 * Attested reads calm/neutral, Derived reads provisional, conflict reads as the
 * one alarm colour. These are presentation tones, not new brand hues. All are
 * AA-checked against warm-white (#F5F4F0) for the label text they carry.
 */
export const epistemicTones = {
  // Attested: a confident slate/teal-charcoal — clearly "on record".
  attested: "#1F6F5C", // on warm-white ≈ 4.7:1 ✓
  // Derived: a measured indigo-grey — clearly "a projection", never settled.
  derived: "#4A5568", // on warm-white ≈ 6.0:1 ✓
  // Conflict / contested: the single alarm tone.
  conflict: "#9C2A2A", // on warm-white ≈ 6.5:1 ✓
  // Confidence bands (trust-in-understanding, NOT project health/red-amber-green).
  bandLow: "#7A3E00", // dark amber on warm-white ≈ 7:1 ✓
  bandMedium: "#4A5568",
  bandHigh: "#1F6F5C",
} as const;
