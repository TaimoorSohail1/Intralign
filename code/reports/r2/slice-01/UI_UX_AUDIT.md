# R2 Slice 01 UI/UX and accessibility audit

**Mode:** combined UX/accessibility audit
**Target:** executable Outcome Integrity overview and breakdown
**Reference:** `release-2/oslo-prototype-r2.html` and Slice 1 AC-1…AC-10
**Verdict:** **BLOCKED — captured comparison images are different workflow states; do not treat as a passing audit.**

## Steps inspected

1. **Outcome Integrity overview — functionally healthy.** The five-step Fragile→Sound ramp, single limiting pillar, three decomposed pillar controls, moment-in-time framing, and pending live-tracking marker are exposed with accessible names. No 0–100 confidence or success-probability number appears on the integrity surface.
2. **Integrity breakdown — functionally healthy after fix.** The toolbar trigger opens a named dialog, initial focus moves to its close control, Escape closes it, and the trigger regains focus in the verified component test. The dialog repeats anti-forecast copy and all three pillar explanations.
3. **Tablet layout — geometry healthy.** At 768×1024 the header fits the viewport, body width equals client width, the main integrity card fits beside the compact navigation rail, and the three pillar controls remain readable.
4. **Mobile layout — geometry healthy.** At 390×844 the page has no horizontal overflow, navigation becomes a bottom bar, the integrity card fits within 338px, and pillar controls stack vertically with approximately 292×75px targets.

## Strengths

- Hierarchy leads with the maturity band and immediately names the gate.
- Pillar controls expose both band and legible count basis.
- Copy consistently says moment-in-time maturity and explicitly rejects health/readiness/probability framing.
- Click targets are substantially larger than the WCAG 2.1 AA minimum target guidance.
- Mobile and tablet reflow preserve content order and avoid horizontal scrolling.

## Rejected screenshot evidence

- `screenshots/comparison-desktop.png`
- `screenshots/comparison-tablet.png`
- `screenshots/comparison-mobile.png`

All three comparisons were opened and inspected. In each pair, the reference is on the outcome-confirmation gate while the application is on the analyzed Overview. The mobile reference also visibly extends beyond its expected capture width in that state. Because the states differ, none can support a parity judgment.

## Risks and open checks

- Fresh screenshot capture failed in the chosen in-app browser, so typography, color, spacing, icon alignment, contrast, cropping, and visual focus styling were not accepted from same-state image evidence.
- The reference prototype keeps all three pillar chips in the compact header; the executable app keeps the compact header to the headline and exposes pillars in the overview card/dialog. This is a visible structural difference that requires screenshot comparison and correction or an already-recorded waiver before parity can pass.
- A full keyboard traversal, screen-reader announcement check, reduced-motion check, and 200% zoom inspection remain open.
- Full WCAG compliance is not claimed from DOM/geometry evidence.

## Required next action

Repeat the audit in the in-app browser once its page can attach and capture. Advance the prototype through outcome confirmation before comparing it with the executable Overview. Capture and inspect matching desktop/tablet/mobile states, then resolve the header-structure difference and any image-visible defects.
