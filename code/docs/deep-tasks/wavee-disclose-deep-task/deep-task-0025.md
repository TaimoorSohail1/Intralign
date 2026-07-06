# DTM-0025 — Understanding Companion (contextual understanding; routes to Recommendation via Finding — Option B)

**Status:** In progress — DTM-0024 approved (`0217e80`) · **Module:** DTM-0025 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Companion) · **Depends:** DTM-0018/0019/0021/0022.

## Goal / observable behavior

The **Understanding Companion** is a contextual surface presenting **epistemic-safe summaries** of
the current understanding in context, and routing to a Recommendation **via its associated Finding
(Option B)** — i.e. it does not open the Recommendation Panel directly; it routes through the
Finding (preserving RP-C1). Surface-transition consistency: the same governed object reads the same
across surfaces. Read-only.

## Source docs / constraints

- Contract E1 (Companion row: "route to Recommendation via the associated Finding — Option B;
  surface-transition consistency; epistemic-safe summaries"). UX:
  `10_product/experience/UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md`.
  `code/CONTEXT.md` (epistemic-safety labeling; RP-C1). Decisions #3, #5, #6.
- Consume the DTM-0018 reads (confidence/findings summaries); reuse `EpistemicLabel`; route to the
  Finding Panel (which holds the RP-C1 entry), never to a standalone Recommendation Panel.

## Locked decisions (do not re-derive)

- **Presents, never generates.** Summaries are presentation of governed objects; no
  generate/score/accept control. Every summarized value carries its epistemic label; Derived never
  settled.
- **Option B routing (preserves RP-C1):** to reach a Recommendation, the Companion routes to the
  **associated Finding** (the Finding Panel), NOT directly to the Recommendation Panel.
- No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Companion/**` (+ tests) and wiring the Companion route/
  placeholder in `router.tsx` (or as a contextual panel per the spec — the one swap). Vitest +
  Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): renders contextual epistemic-safe summaries (each value labelled); a route-to-
   recommendation affordance goes **to the associated Finding** (Option B). **Negatives:** no
   generate/score/accept control; Derived-as-settled impossible; the Companion does NOT route
   directly to a standalone Recommendation Panel (RP-C1 preserved — assert it routes via the
   Finding); summaries never overstate confidence (band carried verbatim).
2. Build from the DTM-0018 reads; mount; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 reads (+ `DerivedEnvelope`). No backend change.

## Test plan

- **Positive:** contextual summaries with labels; route-to-rec via the Finding (Option B);
  empty/loading clean.
- **Negative:** no generate/score/accept control; Derived-as-settled impossible; no direct
  standalone Recommendation route (Option B / RP-C1); no overstated confidence.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → Companion shows contextual labelled summaries; "see recommendations" routes via
  the Finding, not a standalone panel; no generate/accept control.

## Done criteria

- Companion presents epistemic-safe contextual summaries + Option-B routing (via Finding, RP-C1
  preserved), read-only, no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0026.

## Worker report — Ready for review

**Completed an interrupted run.** A prior run had written the RED tests + fixtures + harness;
the implementation was missing. I treated the three pre-existing files as the spec and built the
surface to satisfy them.

### Files — pre-existing vs added

- **Pre-existing (RED, untouched as spec):**
  - `src/surfaces/Companion/Companion.test.tsx` (20 tests)
  - `src/surfaces/Companion/fixtures.ts`
  - `src/surfaces/Companion/testHarness.tsx`
- **Added (the missing implementation):**
  - `src/surfaces/Companion/Companion.tsx` — the surface.
  - `src/surfaces/Companion/CompanionRoute.tsx` — thin route adapter (mirrors
    `FindingPanelRoute` / `DashboardRoute`; reads `projectId` from the route params).
  - `e2e/companion.spec.ts` — Playwright (mount + Option-B/RP-C1 negative + Disclose negatives).
- **Modified (the one wiring swap):** `src/app/router.tsx` — added the Companion route at
  `/projects/$projectId/companion` (component `CompanionRoute`). Also added a sibling `/chat`
  PlaceholderSurface route, because the Companion's typed "Ask OSLO" `Link` needs a registered
  target route to type-check; it is additive placeholder wiring (no existing route changed).

### Where the Companion mounts

`/projects/$projectId/companion` (project-scoped contextual surface). It consumes the DTM-0018
Orval reads read-only: confidence, CAF, findings, recommendations, analysis-runs.

### Contract behaviors proven

- **Presents, never generates.** No generate/score/accept/reject/defer/edit/govern control —
  asserted over every button/role-button/input/textarea/select (Vitest) and over nav controls
  (Playwright).
- **Every summarized value carries its `EpistemicLabel`** (Outcome Confidence, all three CAF
  dimensions, each Top Finding, each Top Recommendation) — all `data-standing="derived"`, never
  attested/settled. Bands carried VERBATIM off the DTO (medium confidence stays medium; the
  band-low finding f-2 stays low; the contested finding f-1 shows the conflict marker). The raw
  0–100 index and `%` are never rendered.
- **Option B / RP-C1 (the headline), proven by negative test:** each Top Recommendation's
  "See in its finding" affordance routes to the recommendation's ASSOCIATED FINDING via
  `Recommendation.finding_id` → `/projects/$projectId/findings/$findingId` (the Finding Panel),
  NEVER to a standalone or nested Recommendation Panel. Vitest asserts the landing target is the
  `finding-panel-target` and NOT `recommendation-panel-target` / `standalone-recommendation-target`,
  and that no anchor hrefs a `/recommendations` route. Playwright re-proves the no-`/recommendations`-href
  invariant scoped to the surface.
- **Stale analysis (Q8 / COMP-11):** presents "Previous Analysis" only when the latest
  `AnalysisRun.run_status === "superseded"` — never when current.
- **Clean loading/empty states:** `companion-loading`, `companion-confidence-empty`,
  `companion-caf-empty`, `companion-findings-empty`, `companion-recommendations-empty`.

### Data gap flagged (not filled)

Confirmed the prior run's finding: there is **no aggregate "companion"/"understanding-state" DTO
and no boolean `is_stale` field** in the DTM-0018 REST surface. The Companion presents "Previous
Analysis" from the governed `AnalysisRun.run_status === "superseded"` — a presentation of the
governed object's own status, not an invented flag. Likewise, "Top" findings/recommendations are
the governed list reads (no server-side ranking DTO). No backend change made.

### Verify — exact commands + results

```
$ npm run build
> tsc -b && vite build   →  ✓ built in 1.15s   (no type errors)

$ npx vitest run src/surfaces/Companion/Companion.test.tsx
Test Files  1 passed (1) ·  Tests  20 passed (20)

$ npx vitest run            (full suite — no regressions)
Test Files  10 passed (10) ·  Tests  126 passed (126)

$ npx playwright test companion
4 passed (incl. the Option-B / RP-C1 negative)

$ npx playwright test       (full suite — no regressions)
22 passed

$ npm audit --omit=dev --audit-level=high
found 0 vulnerabilities
```

### Scope / dependency confirmation

- **No new dependency** — `package.json` / `package-lock.json` unchanged.
- **No out-of-scope edits** — touched only `src/surfaces/Companion/**`, `e2e/companion.spec.ts`,
  and the one `src/app/router.tsx` wiring swap (+ the additive `/chat` placeholder the typed Ask-OSLO
  link requires). Backend, generated client, theme, `EpistemicLabel`, and other surfaces untouched.
- Working tree changes staged (green); unrelated working-tree state preserved. Not committed.

**Status: Ready for review.**

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Understanding Companion (`surfaces/Companion/**`) at `/projects/$projectId/companion`: contextual
  epistemic-safe summaries (Outcome Confidence + CAF + top findings/recs), every value via
  `EpistemicLabel`, routing to a recommendation **via its associated Finding (Option B)**. Read-only.
  (Completed an interrupted run — prior run's red tests/fixtures kept as spec; impl added to green.)

Verification (EM re-ran): `npm run build` built; `npx vitest run` **126 passed** (20 new + 106);
worker playwright 22, audit 0. Scope = Companion/** + one router swap (+ an additive `/chat`
placeholder the typed Ask-OSLO link needs; anticipates DTM-0029); dependency delta **NONE**.

Negatives proven: no generate/score/accept control; Derived-as-settled impossible, bands verbatim;
**Option B / RP-C1** — each Top Recommendation routes to its associated Finding Panel, never to a
standalone/nested Recommendation Panel (no `/recommendations` href on the surface).

Remaining risks / flagged (not invented): no aggregate companion/`is_stale` DTO — "Previous
Analysis" is presented from `AnalysisRun.run_status === "superseded"`; "Top" lists are the governed
list reads (no server ranking). Read-surface follow-ups, non-blocking.
