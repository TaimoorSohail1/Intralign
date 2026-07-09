# R1 Visual-Regression Harness

Enforces that the **built app matches the ratified prototype** (`product-design/oslo_r1_experience_mockup_v3.html` — the reference of record). Pairs pixel-diff baselines with the objective `ACCEPTANCE_CRITERIA.md` so "built exactly as designed" is verified at the gate, not trusted.

## Layout
- `surfaces.json` — the surface manifest (viewport, diff threshold, per-surface prototype prep + app route).
- `baselines/` — golden PNGs captured from the prototype (committed; the source of truth for diffs).
- `capture.mjs` — renders surfaces from the prototype (`--mode proto`) or the built app (`--mode app`).
- `compare.mjs` — pixel-diffs `candidate/` vs `baselines/`, writes `diffs/`, fails over `diffThreshold`.
- `behavioral.mjs` — invariants the pixel diff can't see (quick-tour steps resolve, Confidence never bare, reliability basis in the explainer). Run with `npm run behavioral`; `npm run behavioral:proto` needs no running app.
- `ACCEPTANCE_CRITERIA.md` — per-surface structural/behavioral checks (traceable to DL-085…090).
- `ci/visual-regression.sample.yml` — drop-in GitHub Actions job for the **app** repo.

## Install
```
cd 30_engineering/visual_regression
npm install
npx playwright install chromium
```

## Regenerate baselines (only when a ratified UX decision changes the prototype)
```
npm run baseline
```
Commit the updated `baselines/`. Baselines change **only** through a ratified UX decision (Framework 001) that updates the prototype — never to "make a failing test pass."

## Run against the built app
1. In `surfaces.json`, fill each surface's `app.path` (and optional `app.prep`) with your app's real route/state for that surface, and seed the sample project so the routes resolve.
2. Start the app, then:
```
APP_BASE_URL=http://localhost:3000 npm test    # capture candidate + compare
```
Failures write annotated images to `diffs/`.

## Two-gate rule
A surface passes only if **(A)** its pixel diff ≤ `diffThreshold` **and (B)** its `ACCEPTANCE_CRITERIA.md` checks pass. (A) catches visual drift; (B) catches behavior/binding drift a screenshot can't see.

## Determinism
Run in a fixed container: viewport `1440×960`, `reduced-motion`, `srgb`. Mask genuinely dynamic regions (timestamps, "just now") with Playwright `mask`. Sub-±7 Confidence jitter must not render as a change (DL-086).

## Where this runs
This is **app-repo CI** (the six-gate app-ci), not the canon `doc-integrity` gate. The canon repo hosts the baselines + criteria as the reference; the app repo runs the harness on every PR.
