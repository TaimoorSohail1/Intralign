# DTM-0019 — App shell + design system: router, MUI/Intralign theme, epistemic-safety label

**Status:** In progress — DTM-0018 approved (`36d3a2c`); owner authorized Wave E · **Module:**
DTM-0019 · **Phase:** VI (Wave E) · **Contract:** **IC-WE-DISCLOSE** (E0 epistemic safety) + the
UX master · **Depends:** DTM-0018 (the generated client — 16 GET paths now in OpenAPI).

## Goal / observable behavior

The frontend becomes a real app shell: a **TanStack Router** tree with the screen routes, a **MUI
`ThemeProvider`/`CssBaseline`** carrying the **Intralign palette** (WCAG 2.1 AA), the `QueryClient`
wired to the DTM-0018-generated Orval client, and — the reusable centerpiece — a single
**epistemic-safety label** component (Attested/Derived + confidence band + conflict) that every
surface uses so the labeling rule is enforced in one place. Playwright (E2E) + Vitest (component)
are set up. No surface content yet — this is the frame every DTM-0020+ surface mounts into.

## Source docs / constraints

- IC-WE-DISCLOSE E0 (epistemic-safety labeling is the core duty); `RELEASE_1_UI_SPECIFICATION_V1`
  + `UI_SCREEN_INVENTORY` (routes/IA); CHG-068 Intralign palette; WCAG 2.1 AA; evergreen browsers;
  ADR-0010; `deep-task-decisions.md` #5, #7, #8; ANTI_ASSUMPTION (designer-pending E4).

## Locked decisions (from decisions file — do not re-derive)

- **Stack frozen:** React 18 + Vite + MUI + Emotion + TanStack Query + Router + Orval/Axios (the
  scaffold). **Approved new dev deps:** `@playwright/test`, `vitest`, `@testing-library/react`.
  **No other new dependency** (⇒ STOP).
- **Theme (ANTI_ASSUMPTION):** MUI theme with the **Intralign palette** (charcoal `#111315` /
  warm-white `#F5F4F0` / orange `#D97A3A`) + WCAG 2.1 AA contrast; a **sensible MUI default type
  scale** (designer to refine — OPEN_TBD E4). **Do not invent** logo/fonts/redlines/final
  microcopy — leave a clean theme seam. `CssBaseline` for the reset.
- **Epistemic-safety label component** (the centerpiece, reused by every surface): renders
  **Attested vs Derived** + the **confidence band** (0–49/50–74/75–100, **±3 conservative
  edge-guard → round to the lower band**) + **conflict** marker; plan-fact variant = user-attested;
  **never** renders a Derived item as settled or low-confidence as high (component-tested
  negatives). Confidence label text = trust-in-understanding, never project-health.
- **Router:** TanStack Router tree with the screen routes from the inventory (placeholder route
  elements for now); the app shell layout (nav + content) lives here; surfaces mount under it.
- `QueryClientProvider` wired to the generated client (extend the existing `main.tsx`).

## Owned files / boundaries

- **OWN (additive):** `code/frontend/src/` — `app/` (shell + router tree), `theme/` (MUI theme +
  Intralign tokens), `components/EpistemicLabel*` (the reusable label), `main.tsx` (extend: theme
  + router providers), test setup (`vitest.config`, `playwright.config`, `src/**/*.test.tsx`) ·
  `code/frontend/package.json` (add the 3 approved dev deps + test scripts) ·
  `code/frontend/vite.config.ts`/`tsconfig.json` (path alias if needed).
- **READ-ONLY:** backend, the generated `src/api/generated/**` (consume, don't hand-edit),
  migrations, gates. Empty `src/surfaces/**` dirs are filled by DTM-0020+ (not here).

## Packages / refactors

- Add `@playwright/test`, `vitest`, `@testing-library/react` (dev). No runtime dependency added.

## Implementation instructions (TDD)

1. Red: Vitest component tests for the epistemic-safety label — Attested vs Derived; band
   mapping + ±3 edge-guard (round down); conflict shown; **negatives:** a Derived value can't be
   rendered as "settled/confirmed"; a 48 reads Low not Medium (edge guard). A Playwright smoke
   test: the shell renders + a route resolves.
2. Theme (Intralign tokens) + `CssBaseline`; router tree (placeholder routes); wire providers in
   `main.tsx`; the label component.

## API / data / schema contracts

- Consumes the DTM-0018 DTOs' `epistemic_label` + band + conflict fields. No backend change.

## Test plan

- **Positive:** label renders Attested/Derived + band + conflict + user-attested plan-fact variant;
  shell + a route render; theme applies the Intralign palette; AA contrast holds.
- **Negative:** Derived-as-settled impossible via the label API; band-edge guard (48→Low);
  low-confidence-as-high impossible.
- `npm run build` (tsc -b + vite) green; Vitest + Playwright smoke green; `npm audit` (gate-6) green.

## Manual checks (EM)

- `npm run dev` → the shell loads with the Intralign theme; a placeholder route resolves; the label
  component demoed in Storybook/a sandbox route shows each epistemic state correctly.

## Done criteria

- App shell (router + theme + providers) + the reusable epistemic-safety label in place and tested;
  Playwright/Vitest set up; build + drift gate + audit green; PR cites IC-WE-DISCLOSE. Ready for
  DTM-0020 (MRI) and the surface slices.

## Worker report

**Status: Ready for review.** App shell (router + Intralign theme + providers) + the reusable
epistemic-safety label are in place and tested; Vitest + Playwright are wired; build, drift gate,
and prod audit are green. No surface content (DTM-0020+).

### Files added / changed (all additive under `code/frontend/`)

- **Theme (the clean seam):**
  - `src/theme/tokens.ts` — Intralign palette (`charcoal #111315` / `warm-white #F5F4F0` /
    `orange #D97A3A`), AA-checked surface tones + an epistemic-state tone set (attested / derived /
    conflict / band tones). The only owner-ratified facts; no invented fonts/logo/redlines.
  - `src/theme/index.ts` — `createTheme` MUI theme. `primary = orange` with **`contrastText =
    charcoal`** (charcoal-on-orange ≈ 5.4:1 passes AA; white-on-orange does not). Default MUI type
    scale + system font stack (OPEN_TBD E4 — designer refines this module only).
- **Epistemic-safety label (centerpiece):**
  - `src/components/confidenceBand.ts` — `resolveBand(value)` (the ±3 edge guard) + `BAND_LABEL`.
  - `src/components/EpistemicLabel.tsx` — the reusable label; discriminated-union prop on
    `standing` ("attested" | "derived") so Derived-as-settled is impossible by construction; plus
    `fromDerivedEnvelope()` adapter that maps the generated `DerivedEnvelope` DTO `label` field.
  - `src/components/confidenceBand.test.ts`, `src/components/EpistemicLabel.test.tsx` — Vitest.
- **Router + shell:**
  - `src/app/AppShell.tsx` — persistent AppBar (wordmark `OSLO`, text not logo) + permanent nav
    rail (UI spec §2 IA) + `<Outlet/>` content region.
  - `src/app/router.tsx` — code-based TanStack Router tree from `UI_SCREEN_INVENTORY.md` (13
    screens). **RP-C1 encoded structurally:** the Recommendation Panel route lives only under a
    Finding (`/projects/$projectId/findings/$findingId/recommendations`), never standalone.
  - `src/app/PlaceholderSurface.tsx` — placeholder route element (renders no governed cognition).
- **Providers:** `src/main.tsx` extended — `ThemeProvider` + `CssBaseline` → `QueryClientProvider`
  (DTM-0018 client) → `RouterProvider`.
- **Test setup / configs:** `vitest.config.ts`, `src/test/setup.ts`, `playwright.config.ts`,
  `e2e/shell.spec.ts`; `package.json` scripts (`test`, `test:watch`, `test:e2e`);
  `code/.gitignore` — ignore Playwright `test-results/` + `playwright-report/`.

### Band / ±3 conservative edge-guard rule (implemented)

Natural bands `0–49 low / 50–74 medium / 75–100 high`. The guard rounds **DOWN** (never up): a value
strictly above a boundary (50 or 75) by **1 or 2** points drops to the lower band; the boundary value
itself keeps the higher band; by **+3** the value has cleared the guard. So a low value can never
display as high. Locked boundary cases (all asserted in `confidenceBand.test.ts`):

| value | band | why |
|---|---|---|
| 48 | low | below 50; natural low |
| 50 | medium | boundary value keeps the higher band |
| 52 | low | 50+2, within the guard → drop |
| 53 | medium | 50+3, cleared the guard |
| 74 | medium | no boundary above it |
| 75 | high | boundary value keeps the higher band |
| 77 | medium | 75+2, within the guard → drop |
| 78 | high | 75+3, cleared the guard |

`50→medium` and `75→high` are the symmetric "boundary keeps the higher band" rule (the task names
the `75→High` case explicitly; `50→medium` is its mirror). Confidence text is
trust-in-understanding (`Low/Moderate/High understanding`) — never project-health/probability
(negative-tested).

### Negatives proven (Vitest — the point of E0)

- A Derived item renders as **Derived**, never "settled"/"confirmed"/"attested" (the prop type has no
  attested wording on the derived arm).
- A value of 77 resolves to `medium` (`data-band="medium"`), never `high` — low-as-high is impossible.
- Plan fact = `attested + source:user` → renders "You confirmed", not world-truth/Derived.

### Exact commands + results

- `npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom @playwright/test`
  → `added 102 packages`. (`jest-dom` + `jsdom` are the approved supporting deps for the 3 named.)
- `npm run build` (`tsc -b && vite build`) → **PASS**, `✓ 564 modules transformed`, `✓ built`.
- `npx vitest run` → **PASS**, `Test Files 2 passed (2)`, `Tests 24 passed (24)`.
- `bash scripts/check-openapi-drift.sh` (live) → started backend via
  `.venv/bin/python -m uvicorn backend.api.app:app --port 8000` (16 GET paths confirmed), regenerated
  the Orval client, `npx tsc --noEmit` → **"Frontend is in sync with the backend OpenAPI contract."**
  The regen produced **no tracked change** (the generated client is gitignored) — not hand-edited.
- `npx playwright install chromium` then `npx playwright test` → **PASS**, `2 passed` (shell renders +
  nav; `/notifications` placeholder route resolves).
- `npm audit --omit=dev --audit-level=high` (gate-6) → **`found 0 vulnerabilities`**. (Dev-tree
  advisories exist in the vitest/playwright chains but are out of the prod-audit scope.)

### Dependency confirmation

- **No new runtime dependency.** The `dependencies` block is byte-identical in content (npm only
  re-alphabetized it). New devDeps: `@playwright/test`, `vitest`, `@testing-library/react` (the 3
  approved) + `@testing-library/jest-dom`, `jsdom` (the supporting deps the task lists as
  already-present/approved). Used the code-based TanStack Router API (no new file-router plugin dep).

### Notes / environment

- Backend was startable from the repo `.venv` (uvicorn), so the **live** drift regen ran (not just
  `tsc --noEmit`). The backend was stopped after the gate.
- Working tree preserved: the only pre-existing change was the EM's status edit at the top of this
  file. Nothing committed (staging/commit left to the EM).

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- The bare scaffold is now a real Wave E app shell: MUI/Intralign theme (`theme/tokens.ts` +
  `theme/index.ts`, charcoal-on-orange ≈5.4:1 AA), TanStack Router tree of the 13 inventory
  screens + `AppShell`, providers wired in `main.tsx`, and the centerpiece reusable
  **EpistemicLabel** (+ `confidenceBand` ±3 guard + `fromDerivedEnvelope` DTO adapter). No surface
  content (correct — that's DTM-0020+).

Verification (EM re-ran, all green):
- `npm run build` → built (tsc -b + vite). `npx vitest run` → **24/24 passed**.
- Worker reported `npx playwright test` 2/2 + `check-openapi-drift.sh` "in sync" + `npm audit
  --omit=dev` 0 vulns; build+vitest reproduced here.
- **Epistemic safety verified at the source:** `EpistemicLabel` prop is a **discriminated union on
  `standing`** — the Derived arm carries no attested/"settled" wording (Derived always reads "a
  recomputable projection — not settled"); the plan-fact (`user`) variant reads "You confirmed …
  not asserted as world-truth." Derived-as-settled is impossible by construction (decision #5).
- **Band authority correct:** `fromDerivedEnvelope` uses the DTO's authoritative `confidence_band`
  (does NOT recompute) → the label can never disagree with the backend's governed band; the ±3
  `resolveBand` guard is only the raw-value fallback.
- **RP-C1 structural:** the Recommendation route exists only nested under a Finding
  (`/projects/$projectId/findings/$findingId/recommendations`) — no standalone route.
- No net-new runtime dependency (original 8 unchanged); only the 3 approved dev deps (+ jsdom,
  jest-dom). No backend/migration change.

Manual test plan:
- `cd code/frontend && npm run dev` → shell loads with the Intralign theme; nav rail resolves
  placeholder routes; the Recommendation route is unreachable except under a Finding.

Remaining risks / accepted follow-ups:
- Dev-tree `npm audit` (full) shows advisories in the vitest/playwright chains — OUT of gate-6's
  `--omit=dev` scope (gate stays green); noted, not blocking. Bundle is ~390kB un-split — fine for
  the shell; code-split per-surface as the surfaces land.
- Placeholder routes render no governed cognition yet (by design — DTM-0020+).
