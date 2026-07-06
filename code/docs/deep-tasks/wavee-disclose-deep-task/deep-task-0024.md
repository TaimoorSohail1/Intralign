# DTM-0024 — Project Overview (+ Dashboard / Project List): aggregate Outcome Confidence/CAF + counts

**Status:** In progress — DTM-0023 approved (`494d715`) · **Module:** DTM-0024 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Overview) · **Depends:** DTM-0018/0019/0020.

## Goal / observable behavior

**Project Overview** presents a project-level **understanding summary** — aggregate **Outcome
Confidence / CAF** (banded) + counts (findings/issues/recommendations) — and the **Dashboard /
Project List** lists the user's projects with their current confidence. Read-only; epistemic labels
everywhere. Confidence is **trust in understanding, NOT project health/readiness**.

## Source docs / constraints

- Contract E1 (Overview row: "Project-level understanding summary; bands; **not** project-health").
  UX: `10_product/experience/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` + any
  `PROJECT_DASHBOARD_AND_PROJECT_LIST*` spec + `UI_SCREEN_INVENTORY.md` (Dashboard + Project
  Overview screens). `code/CONTEXT.md` (Confidence/CAF/Outcome Confidence — Derived; never health).
  Decisions #3, #5.
- Consume the DTM-0018 projects + confidence/CAF reads; reuse `EpistemicLabel`. Mount at the
  Dashboard + Project-Overview route placeholders in `router.tsx`.

## Locked decisions (do not re-derive)

- **Presents, never generates.** No edit/score/accept control. Aggregate Outcome Confidence + CAF
  shown via `EpistemicLabel` (Derived + band). **Confidence ≠ project health/readiness/probability**
  (negative-proven). Counts are presentation of governed objects, not a computed health score.
- No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Overview/**` (Project Overview + Dashboard/Project List +
  tests) and wiring the Dashboard + Project-Overview route placeholders in `router.tsx`. Vitest +
  Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): Project Overview renders aggregate Outcome Confidence + CAF (Derived labels) +
   counts; Dashboard lists projects each with current confidence (labelled) + a link to its
   workspace. **Negatives:** no edit/score/accept/generate control; Derived-as-settled impossible;
   **confidence/overview never reads health/readiness/probability/% or a project-health score**;
   counts are not surfaced as a health metric.
2. Build from the DTM-0018 reads; mount; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 Project + ConfidenceState + CAFState DTOs (+ `DerivedEnvelope`). No backend
  change. (Project list may be empty/loading until platform persistence lands — render cleanly.)

## Test plan

- **Positive:** overview with aggregate confidence + CAF labels + counts; dashboard project list
  with per-project confidence; empty/loading clean.
- **Negative:** no edit/score/accept control; Derived-as-settled impossible; not-project-health
  (no health/readiness/probability wording or score).
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → dashboard lists projects w/ confidence; overview shows aggregate confidence + CAF
  + counts; nothing reads as project health; no edit/accept control.

## Done criteria

- Project Overview + Dashboard present aggregate understanding (confidence/CAF/counts) with labels,
  not-project-health, read-only, no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0025.

## Worker report

**Status: Ready for review.** TDD (red → green). Contract: IC-WE-DISCLOSE E1 (Overview).
No new dependency; no out-of-scope edits. Not committed — staged-ready (working tree green).

### Files

New — `code/frontend/src/surfaces/Overview/**`:
- `Dashboard.tsx` — Dashboard / Project List. Lists the caller's workspace projects
  (`useListProjects…`); each row presents name + presented lifecycle/status + **current
  Outcome Confidence** as a Derived `EpistemicLabel` (banded, conflict-aware) + an **Open
  workspace** link (`/projects/$projectId`). Per-row confidence is fetched via
  `useGetConfidence…` (the Project DTO carries no embedded confidence — only
  `current_confidence_state_id`). A project with no confidence yet → clean
  `confidence-unavailable`, never a fabricated value. Read-only.
- `ProjectOverview.tsx` — project-level **understanding summary**: aggregate **Outcome
  Confidence** (Derived label) + **CAF** (Clarity · Alignment · Feasibility, three co-equal
  dimensions, each a Derived banded label) + **counts** (findings / issues / recommendations).
  Read-only.
- `DashboardRoute.tsx`, `ProjectOverviewRoute.tsx` — thin route adapters.
- `fixtures.ts`, `testHarness.tsx`, `Dashboard.test.tsx`, `ProjectOverview.test.tsx` (Vitest).

Modified:
- `code/frontend/src/app/router.tsx` — swapped the `/` placeholder → `DashboardRoute` and the
  project `/orientation` placeholder → `ProjectOverviewRoute` (the only changes; route swaps only).

New (e2e):
- `code/frontend/e2e/overview.spec.ts` — Playwright happy-path + negatives for both surfaces.

### Mount points

- **Dashboard** → top-level `/` (UI_SCREEN_INVENTORY Dashboard: `GET /projects`,
  `GET /projects/{pid}/confidence`).
- **Project Overview** → `/projects/$projectId/orientation`. The Workspace root
  (`/projects/$projectId/`) is the MRI umbrella (DTM-0020); UI_SCREEN_INVENTORY maps the
  "60-Second Orientation" to the project-level understanding summary (confidence, CAF, counts) —
  i.e. the Project Overview — so it mounts at the orientation route.

### Exact verification results (`cd code/frontend`)

- `npm run build` (`tsc -b && vite build`): **PASS** — 727 modules, built in 1.15s.
- `npx vitest run`: **PASS** — 9 files, **106/106** tests (new Overview suite = 23: Dashboard 13,
  ProjectOverview 10; all pre-existing suites still green).
- `npx vitest run src/surfaces/Overview`: **PASS** — 23/23.
- `npx playwright test`: **PASS** — **18/18** (new `overview.spec.ts` = 6; existing 12 unchanged).
- `npm audit --omit=dev --audit-level=high`: **found 0 vulnerabilities.**
- `npx tsc --noEmit` (Orval drift gate, ADR-0003): **exit 0** — no drift.
- `package.json` / `package-lock.json`: **untouched** (confirmed — no new dependency).

### "Not project health" negatives proven (Vitest + Playwright)

- **Presents, never generates:** scanning every `button` / `[role=button]` / `input` / `textarea` /
  `select` (Vitest) and every `button`/`menuitem`/`checkbox`/`switch`/`radio` (Playwright), no
  control matches `edit|score|accept|reject|defer|resolve|approve|govern|generate|recompute|
  re-analyze|run analysis|apply`. No edit/score/accept/generate affordance exists.
- **Derived never settled:** every confidence/CAF value renders through `EpistemicLabel` with
  `data-standing="derived"`; asserted it is never `attested`; no "settled" text. (The label is a
  discriminated union — a Derived value cannot pass attested wording by construction.)
- **Never project health/readiness/probability/%/score:** asserted neither surface renders the
  words `health`, `readiness`, `probability`, `on-track`, a `%`, or a bare 0–100 confidence/CAF
  index value (only the band is shown). The Dashboard asserts the same. (Note: I reworded my own
  reassurance microcopy so it does not even contain those literal words — the negatives reject the
  terms appearing anywhere on the surface.)
- **Counts are not a health metric:** the counts read as counts OF governed objects
  (findings / issues / recommendations) and contain no `health`/`score`/`readiness`/`%` framing
  (negative-tested explicitly). Issues = the subset of findings carrying a `severity` (an Issue is
  Evaluate's prioritized Finding), so issues ≤ findings — a count split, not a computed score.
- **Clean states:** loading, empty-workspace (positive "create your first project"), and
  not-yet-available confidence/CAF all render cleanly and are negative-tested (none-found ≠ failure).

### Data gaps flagged (NOT invented)

1. **No aggregate "overview"/counts DTO.** Nothing in the DTM-0018 REST surface carries
   findings/issues/recommendations totals. The Project Overview therefore **presents the lengths of
   the already-governed list reads** (`useListFindings…`, the severity-bearing subset = issues,
   `useListRecommendations…`). A count is presentation of governed objects, never a computed metric.
   No counts endpoint was invented — flagged here.
2. **Project DTO carries no embedded confidence** — only `current_confidence_state_id`. The
   Dashboard fetches each row's current Outcome Confidence via `GET /projects/{pid}/confidence`
   (per UI_SCREEN_INVENTORY's Dashboard operations). Matches the spec; noted for visibility.
3. **Dashboard affordances deferred:** search / filter / sort / archive / pin (Dashboard & Project
   List Experience Spec §H–§O) are presentation affordances out of scope for this read slice. Not
   built, not stubbed — noted, not invented. The list may be empty until platform persistence lands;
   the empty state renders cleanly.

### Scope confirmation

Only `src/surfaces/Overview/**` + the two route swaps in `router.tsx` + `e2e/overview.spec.ts` were
touched. Backend, generated client, theme, `EpistemicLabel`, `confidenceBand`, and other surfaces are
unchanged. No new runtime/test dependency. Unrelated working-tree changes preserved.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Project Overview (`/projects/$projectId/orientation`) + Dashboard/Project List (`/`) under
  `surfaces/Overview/**`: aggregate Outcome Confidence + CAF (Derived labels) + counts; per-project
  confidence on the dashboard. Read-only; not-project-health framing enforced.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **106 passed** (23 new + 83);
worker playwright 18, audit 0, drift exit 0. Scope = Overview/** + two route swaps; dependency
delta **NONE**.

Negatives proven: no edit/score/accept/generate control; Derived-as-settled impossible; neither
surface renders health/readiness/probability/on-track/%/bare-index — bands only; counts are counts
of governed objects, not a health metric.

Remaining risks / flagged (not invented): no aggregate counts/overview DTO → counts are the lengths
of the governed list reads; Project DTO has no embedded confidence (fetched per row per the
inventory); dashboard search/filter/sort/archive deferred. All read-surface follow-ups, non-blocking.
