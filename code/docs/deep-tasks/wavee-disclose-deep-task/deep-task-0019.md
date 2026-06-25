# DTM-0019 — App shell + design system: router, MUI/Intralign theme, epistemic-safety label

**Status:** Planned — BLOCKED on DTM-0018 approval · **Module:** DTM-0019 · **Phase:** VI (Wave E)
· **Contract:** **IC-WE-DISCLOSE** (E0 epistemic safety) + the UX master · **Depends:** DTM-0018
(the generated client).

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_
