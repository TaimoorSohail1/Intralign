# DTM-0042 — Frontend navigation reconciliation (project-context nav; no dead-end placeholders)

**Status:** In progress · **Module:** DTM-0042 · **Phase:** Completion (UX gap) · **Contract:**
`RELEASE_1_UI_SPECIFICATION_V1` §2 (Information Architecture / navigation) + `UI_SCREEN_INVENTORY`.
**Depends:** the Wave E surfaces (all built). **Branch:** `feat/release1-completion`.

## Problem / root cause (observed live)

The AppShell nav rail (DTM-0019) links to **top-level cross-project routes** (`/findings`,
`/recommendations`, `/reports`, `/shared`, `/settings`), but the real surfaces are **project-scoped**
(`/projects/$projectId/findings`, `/projects/$projectId/` MRI, etc.). So:
- **Findings, Recommendations** → surfaces EXIST but the nav points at leftover DTM-0019
  `PlaceholderSurface` routes ("Surface pending (DTM-0020+)").
- **MRI, Project Overview, History, Export, Companion, Chat** → real surfaces with **no nav entry
  at all** (only reachable by direct URL / drilling in from the Dashboard).
- **Reports, Shared, Settings** → **no surface built** (Category-E commodity / out of Wave E scope).

Root cause: a single **flat global nav** that was never reconciled with the **project-scoped** surface
routing the Wave E slices (DTM-0020+) landed. The DTM-0019 comment literally deferred it ("resolve
within the active project at build-out").

## Goal / observable behavior

Every **built** surface is reachable from the nav, and no nav link dead-ends at a "Surface pending"
placeholder for a surface that exists. Per the UI spec IA:
- **Global nav** (always): Projects (Dashboard), Notifications, Settings.
- **Project-context nav** (shown when a project is active, i.e. the route is under
  `/projects/$projectId`): **Workspace/MRI**, **Overview**, **Findings**, **History/Timeline**,
  **Export**, **Companion**, **Chat** — each routing to `/projects/$activeProjectId/…`. (Recommendation
  Panel stays RP-C1 — reached from a Finding, NOT a standalone nav entry.)
- **Genuinely-unbuilt (Category-E) entries** (Reports, Shared Artifacts) are handled **honestly**:
  per the UI spec / DL-043 J classification, either **removed from the R1 nav** or shown **disabled
  with a "not in Release 1" affordance** — do NOT leave them as a silent "Surface pending" dead-end.
  **Settings:** keep a minimal real Settings stub OR mark deferred per the spec — confirm from the
  inventory; do not invent settings UI.

## Source docs / constraints

- `10_product/experience/RELEASE_1_UI_SPECIFICATION_V1.md` §2 (the IA / navigation model — global
  vs project context; what's top-level vs project-scoped) + `UI_SCREEN_INVENTORY.md` (which screens
  exist + their nav placement + which are Category-E/commodity). `code/CONTEXT.md`. If the spec's IA
  and the current flat nav conflict, the **spec wins**; if the spec is silent on a detail, prefer the
  project-context split above and flag.
- Code: `frontend/src/app/AppShell.tsx` (the `NAV` array + the rail), `frontend/src/app/router.tsx`
  (the route tree — `projectRoute` children are the real surfaces; the top-level `/findings` etc.
  are the placeholders), the surfaces under `frontend/src/surfaces/**` (their real paths).

## Locked decisions (do not re-derive)

- **Active-project-aware nav.** Derive the active project from the current route params
  (`/projects/$projectId`); the project-context nav links target `/projects/$activeProjectId/…`. On
  the Dashboard (no active project) the project-context group is hidden (or shown with a "open a
  project" hint) — do NOT route a project-scoped link with no project.
- **No dead-end placeholders for built surfaces.** Every nav link resolves to a real surface or an
  honest deferred state. Remove/relabel the leftover top-level `/findings` + `/recommendations`
  placeholders OR redirect them into the active project (pick per the spec).
- **RP-C1 preserved** — Recommendation Panel is NOT a standalone nav entry (only reached from a
  Finding). Don't add a route that breaks RP-C1.
- **No backend change, no new dependency.** Theme + EpistemicLabel + the surfaces themselves
  unchanged — this is nav/routing wiring + honest handling of unbuilt entries.

## Owned files / boundaries

- **OWN:** `frontend/src/app/AppShell.tsx` (the nav model — global + project-context) ·
  `frontend/src/app/router.tsx` (reconcile/redirect the leftover top-level placeholder routes;
  remove dead ones or wire them) · a small nav-config/helper if useful · the AppShell/router tests
  (vitest) + an e2e nav spec (playwright).
- **READ-ONLY:** the surfaces (`surfaces/**`), theme, EpistemicLabel, backend, the generated client.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (vitest): the nav renders the global group always; when on a `/projects/$projectId/...` route
   the project-context group renders with links to `/projects/$projectId/{,/orientation,/findings,
   /history,/export,/companion,/chat}`; clicking **Findings** in a project context lands on the
   **Issue Cards** surface (NOT a placeholder); on the Dashboard the project-context group is
   hidden/disabled. **Negatives:** no nav link resolves to a `PlaceholderSurface` for a BUILT surface;
   RP-C1 — no standalone Recommendation nav entry; Category-E entries (Reports/Shared) are removed or
   explicitly-deferred (asserted), never a silent "Surface pending".
2. Implement the active-project-aware nav + reconcile the router (redirect or remove the leftover
   top-level placeholders); ground the exact entry set + Category-E handling in the UI spec.
3. Playwright: from the Dashboard → open a project → the project nav appears → Findings opens Issue
   Cards; the previously-broken `/findings`-from-nav no longer shows "Surface pending".

## Test plan

- **Positive:** global + project-context nav; every built surface reachable; active-project routing.
- **Negative:** no built-surface nav link → placeholder; RP-C1 (no standalone rec nav); Category-E
  entries honestly handled (not silent dead-ends).
- `npm run build` + `vitest run` + Playwright + drift gate + `npm audit --omit=dev` green.

## Manual checks (EM) — against the running app

- Open the app → Dashboard → open *Atlas Migration* → the project nav shows MRI/Overview/Findings/
  History/Export/Companion/Chat; click **Findings** → the real Issue Cards (the 3 seeded findings),
  NOT "Surface pending". No nav link dead-ends.

## Done criteria

- Nav is active-project-aware; every built surface reachable from the nav; no built-surface link
  dead-ends at a placeholder; RP-C1 preserved; Category-E (Reports/Shared/Settings) handled honestly
  per the spec; no backend change/new dep; build + vitest + playwright + drift + audit green. PR
  cites UI_SPEC §2.

## Worker report

**Status: Ready for review.**

### What UI_SPEC §2 (IA) said — and the reconciliation

§2 describes a single flat persistent left rail: `Projects · Findings · Recommendations ·
Reports · Shared Artifacts · Notifications` (+ `Settings` via the user menu), and states that
"Findings/Recommendations/Reports/Shared/Notifications are top-level entries that **resolve
within the active project** (or workspace, for Shared/Notifications) — mirroring the API
resource scoping." Wave E landed those entries as project-SCOPED surfaces
(`/projects/$projectId/findings`, the MRI at `/projects/$projectId/`, …), so the flat rail
linked at top-level routes that were leftover DTM-0019 placeholders → "Surface pending"
dead-ends. The spec is **silent on the exact split mechanism** ("resolve within the active
project"); I implemented the global + project-context model from the task's locked decisions and
flagged that as the reconciliation (spec wins where it speaks; this fills the silence).

### The nav model built (`frontend/src/app/navModel.ts` + `AppShell.tsx`)

Two groups, derived purely from the current route:
- **GLOBAL_NAV** (always): **Projects** (`/`, exact), **Notifications** (`/notifications`),
  **Settings** (deferred — see below).
- **PROJECT_NAV** (only when a project is active): **Workspace** (`/projects/$pid/` — MRI),
  **Overview** (`/orientation`), **Findings** (`/findings` — Issue Cards), **History**
  (`/history`), **Export** (`/export`), **Companion** (`/companion`), **Chat** (`/chat`). Order
  follows the §2 Workspace→Orientation→Findings→secondary hierarchy.

**Active-project derivation:** `activeProjectIdFromPath()` matches `^/projects/([^/]+)` (excluding
`/projects/new`); AppShell reads the pathname via `useRouterState({ select })` so it stays reactive
to navigation. On the Dashboard (no active project) the project group is **hidden** and replaced by
an "Open a project to see its surfaces." hint (`data-testid="nav-project-hint"`) — never a
project-scoped link with no id.

### Leftover top-level placeholders — reconciled

Removed from `router.tsx`: the flat `/findings`, `/recommendations`, `/reports`, `/shared`,
`/shared/$shareId` routes, **plus** the orphan project-scoped `projectRecommendationsRoute`
(Recommendation Workspace) and `projectReportsRoute` (Report Viewer) — none had any inbound nav or
surface affordance, all were `PlaceholderSurface` dead-ends. The nav now routes Findings et al.
into the active project's built surfaces, so the flat routes are gone, not stubbed.

### Reports / Shared / Settings (Category-E) — handled honestly

- **Reports, Shared Artifacts:** commodity, no R1 surface → **removed from the nav entirely** and
  their placeholder routes deleted. No silent "Surface pending."
- **Settings:** kept as a **global entry but rendered DISABLED** ("Not in Release 1",
  `data-testid="nav-deferred"`, no `<a>`); the `/settings` route remains a direct-URL stub titled
  "User Settings" (no settings UI invented). It is never a nav dead-end.
- **RP-C1 preserved:** no standalone Recommendations entry anywhere; the Recommendation Panel route
  still lives only under a Finding (`/projects/$pid/findings/$findingId/recommendations`).

### Negatives proven (vitest + playwright)

- No nav link resolves to a `PlaceholderSurface` for a BUILT surface — clicking **Findings** in a
  project context lands on the Issue Cards surface (`surface-title` = "Issues"), asserting **no**
  "Surface pending" and **no** old "Findings across the active project context" copy.
- RP-C1: project nav exposes no Recommendations link (asserted in the model and in the rendered nav).
- Category-E: GLOBAL_NAV has no Reports / Shared Artifacts entry; Settings is asserted disabled
  ("Not in Release 1").
- Removed top-level routes: the route tree no longer contains `/findings`, `/recommendations`,
  `/reports`, `/shared` as top-level children; direct `/findings` no longer renders the old stub.

### Exact verify results (from `code/frontend`)

- `npx tsc --noEmit` (drift gate) → exit 0, no errors.
- `npm run build` (`tsc -b && vite build`) → ✓ built in 1.27s, 821 modules.
- `npx vitest run` → **18 files, 258 tests passed** (new AppShell suite: 13 tests).
- `npx playwright test` → **43 passed** (incl. 4 new DTM-0042 shell tests).
- `npm audit --omit=dev --audit-level=high` → **found 0 vulnerabilities**.

### Boundaries honored

No backend change. No new dependency (`package.json`/`package-lock.json` untouched; tests use
`fireEvent` from `@testing-library/react`, not `user-event`). Surfaces / theme / EpistemicLabel
unchanged. `vite.config.ts` (pre-existing dev-proxy edit) left as-is. Changed files: `navModel.ts`
(new), `AppShell.tsx`, `router.tsx`, `AppShell.test.tsx` (new), `e2e/shell.spec.ts`. Staged, not
committed.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Nav reconciled to active-project-aware: `navModel.ts` (GLOBAL_NAV + buildProjectNav +
  activeProjectIdFromPath) + AppShell uses `useRouterState` → global group always; project-context
  group (MRI/Overview/Findings/History/Export/Companion/Chat) only when a project is active, links
  targeting `/projects/$activeProjectId/…`; Dashboard hides it with an "open a project" hint. Leftover
  top-level `/findings`/`/recommendations`/`/reports`/`/shared` placeholder routes removed; Reports/
  Shared dropped from nav; Settings shown disabled "Not in Release 1". RP-C1 preserved (no standalone
  Recommendation nav). UI_SPEC §2.

Verification (EM re-ran): `npm run build` built; `npx vitest run` → **258 passed** (13 new AppShell);
worker playwright 43 (4 new nav), audit 0, tsc drift exit 0. Scope = `app/` (AppShell/navModel/router
+ tests) + e2e; **no backend change, no new dependency**; surfaces/theme/EpistemicLabel + the
dev-only `vite.config.ts` untouched.

Negatives proven: no nav link resolves to a PlaceholderSurface for a BUILT surface; no standalone
Recommendation nav entry (RP-C1); Reports/Shared removed (not silent dead-ends); Settings explicitly
deferred. The 4 remaining router placeholders (`/projects/new`, `/analysis-runs/$runId`, Settings
stub, one project stub) are genuinely-deferred screens NOT linked from nav.

Manual: Dashboard → open Atlas Migration → project nav appears → Findings opens the real Issue Cards
(not "Surface pending").

Remaining risks / accepted: UI_SPEC §2 describes a flat rail and is silent on the global-vs-project
split mechanism; the split was implemented from the locked decisions (flagged). Worker also removed
two orphan project-scoped placeholder routes (no inbound nav) — consistent with "remove the dead ones".
