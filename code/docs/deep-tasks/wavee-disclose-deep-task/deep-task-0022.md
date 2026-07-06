# DTM-0022 — Recommendation Panel (RP-C1; Resolution Paths; accept/reject/defer affordance → Wave U)

**Status:** In progress — DTM-0021 approved (`9cad36a`) · **Module:** DTM-0022 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Recommendation Panel) + DL-055 (rec states) ·
**Depends:** DTM-0018/0019/0020/0021.

## Goal / observable behavior

The **Recommendation Panel** renders at the **nested** route
(`/projects/$projectId/findings/$findingId/recommendations`) — **only in a Finding context (RP-C1)**.
It presents the Recommendations anchored to that Finding, grouping multiple alternatives as
**"Resolution Paths"** (a presentation substructure — **never a created object**), each with its
epistemic label, and renders the **accept / reject / defer affordance**. Per E0 + decisions #3:
**Disclose renders the affordance but never performs acceptance** — the affordance routes to /
invokes the **existing Wave U capture seam**; Disclose changes no state itself.

## Source docs / constraints

- Contract E1 (Recommendation Panel row; RP-C1; "Resolution Paths" = presentation grouping, no
  object; render accept/reject/defer → Wave U capture). UX:
  `10_product/experience/RECOMMENDATION_PANEL_SPECIFICATION_V1.md`.
- `code/CONTEXT.md` (Recommendation only-in-Finding-context; Resolution path = presentation-only,
  emitting a standalone object is a rejected negative; Recommendation state DL-055 —
  Generated→{Accepted|Rejected|Deferred}→Implemented(+Superseded); **Accept/Defer/Reject are user
  actions recorded by Wave U, not Disclose**). Decisions #3, #6.

## Locked decisions (do not re-derive)

- **RP-C1 structural** — renders only at the nested-under-Finding route (already in `router.tsx`).
  A standalone Recommendation Panel is a rejected negative.
- **Resolution Paths = presentation grouping only.** Render alternatives as paths; create/emit **no**
  Resolution-Path object, write nothing.
- **Disclose never accepts (Critical).** The accept/reject/defer control is an **affordance** that
  hands off to the **existing Wave U acceptance capture** — it does NOT mutate a recommendation's
  state client-side, does NOT mark it accepted locally, and the panel itself writes no canonical.
  version-pin is mandatory on any acceptance (Wave U owns that).
- **Acceptance-write dependency (ANTI_ASSUMPTION — flag, do not invent):** DTM-0018 built a
  **read-only** REST surface; there is no acceptance POST endpoint yet. Inspect the generated client
  + `backend/api/v1` + the Wave U seam (`responsibilities/acceptance` / `record_acceptance`). If an
  acceptance **command** endpoint exists, wire the affordance to it. **If none exists, render the
  affordance and STOP/flag in the report that the Wave U acceptance-command endpoint is the
  dependency — do NOT add a backend write path, and do NOT have Disclose perform acceptance
  locally.** (The affordance may navigate to a confirm step / be disabled-with-explanation pending
  that endpoint.)
- No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Panels/RecommendationPanel/**` (+ tests) and wiring the
  nested recommendations route element in `router.tsx` (that one placeholder). Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): renders recommendations for the finding, each with its epistemic label + DL-055
   state; multiple alternatives render as **Resolution Paths** (grouping markup, no object); the
   accept/reject/defer affordance is present. **Negatives:** the panel does NOT render outside a
   finding context (RP-C1); no Resolution-Path object is constructed/emitted; clicking accept does
   NOT locally flip a rec to "Accepted" / write state — it hands off to the Wave U capture (assert
   the handoff: navigation or the command call, NOT a local state mutation); no generate/score
   control.
2. Build the panel consuming the DTM-0018 recommendations hook; mount at the nested route; handle
   the acceptance-command per the dependency decision above.

## API / data / schema contracts

- Consumes the DTM-0018 Recommendation DTO (state, type, anchor, alternatives + `DerivedEnvelope`).
  Acceptance write: the existing Wave U seam (see locked decision — flag if no endpoint).

## Test plan

- **Positive:** recs rendered with label + state; Resolution Paths grouping; accept/reject/defer
  affordance present; opens only under a finding.
- **Negative:** RP-C1 (no standalone render); no Resolution-Path object; accept does not locally
  accept (handoff only); no generate/score control.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → from a Finding Panel, open recommendations → alternatives as Resolution Paths,
  each labelled + stated; accept/reject/defer present; accepting hands off to Wave U (or shows the
  pending-endpoint explanation) — the panel never marks it accepted itself.

## Done criteria

- Recommendation Panel presents recs as Resolution Paths with labels + DL-055 states under RP-C1,
  renders the accept/reject/defer affordance that hands off to Wave U (Disclose never accepts), no
  object emitted, no new dep, tests green; acceptance-command dependency wired-or-flagged. PR cites
  IC-WE-DISCLOSE. Ready for DTM-0023.

## Worker report

**Status: Ready for review.**

### Files (all within owned boundaries)

- `code/frontend/src/surfaces/Panels/RecommendationPanel/RecommendationPanel.tsx` — the panel (NEW).
- `code/frontend/src/surfaces/Panels/RecommendationPanel/RecommendationPanelRoute.tsx` — thin route adapter (NEW).
- `code/frontend/src/surfaces/Panels/RecommendationPanel/fixtures.ts` — Recommendation DTO fixtures (NEW).
- `code/frontend/src/surfaces/Panels/RecommendationPanel/testHarness.tsx` — theme+query+router harness (NEW).
- `code/frontend/src/surfaces/Panels/RecommendationPanel/RecommendationPanel.test.tsx` — Vitest (NEW, 12 tests).
- `code/frontend/e2e/recommendation-panel.spec.ts` — Playwright (NEW, 3 tests incl. RP-C1 negative).
- `code/frontend/src/app/router.tsx` — MODIFIED: the **one** nested-route swap — the
  `…/findings/$findingId/recommendations` placeholder → `RecommendationPanelRoute`. No other route changed
  (the project-level `/recommendations` workspace placeholder stays as the Wave U hand-off target).

No backend, generated-client, theme, EpistemicLabel, or other-surface edits. No new dependency.

### Resolution-Paths grouping approach

The panel reads the finding's Recommendations via the DTM-0018
`useListRecommendationsForFindingV1FindingsFindingIdRecommendationsGet` hook (read-only). The **first**
recommendation is shown as **"OSLO recommended"** (presentation ordering, no score). The **remaining**
recommendations are grouped under a **"Resolution Paths"** section (`data-testid="resolution-paths"`), each
rendered as a `resolution-path` keyed on its **own `recommendation_id`** (`data-recommendation-id`). The
grouping is **pure markup over the same DTOs** — no object/field/lifecycle/event is constructed, and no
fabricated `resolution-path-*` id is ever emitted (negative-proven). With a single recommendation the panel
shows an explicit **"No alternative recommendations"** state (§O) instead of an empty grouping shell.
Alternatives stay visible regardless of any card's status (RP-5).

### Acceptance-write seam finding (ANTI_ASSUMPTION — FLAGGED AS THE DEPENDENCY)

**No acceptance COMMAND endpoint exists.** I inspected:

- **Generated client** (`code/frontend/src/api/generated/**`): the entire client is **GET-only** —
  `grep` for `useMutation` / `axios.default.post` / `.post(` returns **zero** matches. The
  `acceptance/acceptance.ts` client exposes only three **reads** (`useListAcceptances…`,
  `useListPlanFacts…`, `useListAcceptanceImpact…`). The `recommendations/recommendations.ts` client is
  three GET queries. The `Recommendation` DTO's own docstring confirms: *"Disclose presents the
  accept/reject/defer/implement AFFORDANCE but the read surface itself NEVER mutates it … acceptance
  routes to the existing Wave U capture seam."*
- **Backend** (`code/backend/api/v1/routers/acceptance.py`): only three `@router.get` endpoints
  (`/projects/{id}/acceptance`, `/plan-facts`, `/acceptance-impact`). No POST/command.
  `backend/responsibilities/acceptance/` exposes the internal `record_acceptance` Wave U seam but it is
  **not exposed over REST**.

**How the affordance is wired (per the locked dependency decision):** the accept/reject/defer control is
rendered as navigation `<Link>`s that **hand off to the existing Wave U capture surface** — the project
Recommendation Workspace route (`/projects/$projectId/recommendations`), carrying the `recommendation` id +
intended `action` as search params. Clicking it performs a **navigation hand-off, not a write**: Disclose
mutates no recommendation state, marks nothing accepted, and writes no canonical / version-pin (version-pin
is Wave U's). **I added no backend write path and no local acceptance.** When a Wave U acceptance-command
endpoint lands in the generated client, the affordance wires to it inside `AcceptanceAffordance` — that is
**the dependency for full accept-through**.

### Exact verification commands + results (run in `code/frontend`)

- `npm run build` (tsc -b && vite build) → **PASS**. 720 modules; `dist/assets/index-*.js 538.23 kB`. tsc
  clean (the `<Link search>` hand-off typechecks against the route tree).
- `npx tsc --noEmit` → **PASS** (exit 0) — the drift-gate's effective typecheck; generated client untouched.
  (`scripts/check-openapi-drift.sh` regenerates from a live backend at `localhost:8000`, unavailable in this
  env; its enforcement is the `tsc` step, which passes.)
- `npx vitest run src/surfaces/Panels/RecommendationPanel` → **12 passed**.
- `npx vitest run` (full suite) → **70 passed (6 files)** — all existing suites still green.
- `npx playwright test` → **10 passed** (3 new RecommendationPanel + 7 prior).
- `npm audit --omit=dev --audit-level=high` → **found 0 vulnerabilities**.
- `git status --short`: only `M src/app/router.tsx` + the new RecommendationPanel dir + new e2e spec +
  this task file. No out-of-scope edits; no new dependency.

### Negatives proven

- **RP-C1 (only-in-Finding-context):** route tree mounts the panel solely under a Finding; as defence in
  depth, with no `findingId` the panel renders an explicit no-context guard (`recommendation-panel-no-context`)
  and **no** items / resolution-paths / affordances (Vitest). Playwright: the standalone top-level
  `/recommendations` route renders **no** `recommendation-panel` / `recommendation-item` / `resolution-paths`.
- **Disclose-never-accepts (Critical):** clicking **Accept** navigates to the Wave U capture
  (`…/recommendations`, **not** `/findings/…`) and does **not** flip the primary (`generated`) recommendation
  to "Accepted" client-side — asserted as a navigation hand-off, not a local state mutation.
- **No Resolution-Path object:** the grouping is markup over the source `recommendation_id`s; no
  `resolution-path-*` object id is ever produced (Vitest).
- **No generate/score/recompute/resolve-finding/govern/approve/execute/apply control** anywhere on the
  surface (Vitest scan over buttons/inputs + Playwright role scan). The advisory accept/reject/defer
  affordance is intentionally present and is the hand-off, not a directive; no recommendation is shown as
  "settled" (its own label stays Derived).

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Recommendation Panel (`surfaces/Panels/RecommendationPanel/**`) at the nested-under-finding route
  (RP-C1). Presents the finding's recs (first = "OSLO recommended"), alternatives grouped as
  "Resolution Paths" (pure markup, keyed on each rec's own id — no object/field/event minted), each
  with EpistemicLabel + DL-055 state; accept/reject/defer affordance = navigation hand-off to the
  Wave U capture. Read-only; the panel mutates/writes nothing.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **70 passed** (12 new + 58);
worker playwright 10, audit 0. Scope = RecommendationPanel/** + one nested-route swap; dependency
delta **NONE**. Confirmed no `useMutation`/`.post` in the surface (grep hits are docstrings only).

Negatives proven: RP-C1 (standalone renders a no-context guard, no items/paths/affordances);
Disclose-never-accepts (Accept navigates to the Wave U capture, does NOT flip the `generated` rec to
"Accepted" locally, writes nothing); no Resolution-Path object/id emitted; no generate/score/
recompute/govern/apply control.

Manual test plan: `npm run dev` → from a Finding → recommendations → alternatives as Resolution
Paths, labelled + stated; accept/reject/defer present; accepting navigates to the Wave U capture
(carrying recommendation + action params) — the panel never marks it accepted.

Remaining risks / TRACKED DEPENDENCY:
- **No Wave U acceptance-COMMAND endpoint exists** (the generated client is GET-only; `record_
  acceptance` is internal, not REST-exposed). The affordance hands off by navigation today; for it
  to actually record a UAR + plan fact (version-pinned), a **Wave U acceptance-command POST
  endpoint** must be added — a backend WRITE slice (idempotency + mandatory version-pin; owner-
  approval territory). **Tracked as a follow-up slice (DTM-0030), to land after the read surfaces.**
  Until then the accept affordance is presentational/navigational only — correct per "Disclose never
  accepts", but the end-to-end acceptance write is not yet wired.
