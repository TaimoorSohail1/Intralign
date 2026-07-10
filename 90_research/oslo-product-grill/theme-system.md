# Theme System — OSLO R1

Locked from `RELEASE_1_VISUAL_DESIGN_AND_BRANDING` and the v2 mockup (UX Notes §6.2). All slice prototypes MUST use this exact theme. Confirm or override the narrow choices at the end.

## Locked from docs

- **Layout style:** IDE-style app shell — left rail (Project/Object explorer) + center panes + contextual right panel. Three nested contexts: Workspace › Project › Object.
- **Color direction (semantic tokens, dark default):** bg `#111315`, surface `#1B1F24`, border `#343B44`, primary/brand orange `#D97A3A` (Intralign). Light theme overrides the *same token names* (warm-white surfaces, dark text; `--primary-light` `#B45309` for AA text/links). Single `data-theme` attribute flips the app.
- **Neutral maturity ramp (epistemic rule):** Confidence/CAF use a neutral ramp — dark: grey→white; light: single-hue pale→dark. **Never health/traffic-light colored.**
- **Severity ramp:** red/amber/green ONLY on finding severity (critical/moderate/warning) — heatmap cells, weakness list accents, finding chips, count badges.
- **Typography:** Google Fonts (Inter) via CDN, degrades to system fonts. Number-primary confidence — **focal score** (v4 DL-096; the ring is removed) with band as secondary qualifier; top-bar pill retains band + reliability.
- **Confidence/CAF presentation (v4 DL-096/086/098):** Overview leads with a large focal score + meaning line; CAF as **maturity bars** (band word + hover, lowest flagged "the limit"). One shared **5-band scale: Very Low · Low · Moderate · High · Very High**. No confidence ring, no green box, no Current/From-OSLO pills.
- **Component feel:** premium, executive, grounded — no hype, no gamification (no points/streaks/badges).
- **Density:** progressive disclosure — one primary thing per screen; single-open collapsible sections on the Overview; teaching copy sunsets with proficiency; integrity reminders live in one home surface + hover ⓘ elsewhere.
- **Navigation style:** primary views top-center (Overview·MRI·Artifact); secondary (Collaboration·History); Findings/Recommendations are contextual **panels**, not nav destinations; command palette (⌘K).
- **AI interaction style:** advisory, quiet, cause-bound; global persistent chat panel + "engage in context" from a finding; simulated responses only in prototype.
- **State styles:**
  - Empty: four honest distinctions — none-found / none-under-lens / not-yet-analyzed / unavailable.
  - Error: "reanalysis couldn't complete — showing last-good · Retry" banner.
  - Loading/analysis: rails-first hold, streaming trace, pill "Analyzing…"; no MRI animation during Extended Analysis (`.analysis-active`).
  - Success: cause-bound confidence move (▲/▼ with the resolved finding); no celebration of sub-band jitter.
- **Accessibility:** WCAG 2.1 AA target — `:focus-visible` rings (`--color-focus`), `prefers-reduced-motion`, `role="button"`+`tabindex` on non-native clickables, keyboard nav. `color-scheme` per theme.

## Narrow choices to confirm (defaults applied)
1. **Default theme:** Dark (recommended — "dark is primary"). Light available via Settings → Appearance.
2. **Brand tokenization fidelity for prototype:** Use canonical Intralign token values 1:1 (recommended) vs the slightly-darker prototype palette. Residual `rgba()` alphas → `color-mix` at build.
3. **Font:** Keep the mockup's Google Font choice (recommended) vs a specified alternative.

These are low-impact; unless overridden, prototypes proceed on the recommended defaults.
