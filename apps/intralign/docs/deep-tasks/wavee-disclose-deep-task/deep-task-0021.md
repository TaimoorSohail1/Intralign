# DTM-0021 — Finding Panel (Finding + Attested evidence lineage + confidence; entry to Recommendation Panel)

**Status:** In progress — DTM-0020 approved (`b4b3223`) · **Module:** DTM-0021 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Finding Panel) · **Depends:** DTM-0018/0019/0020.

## Goal / observable behavior

The **Finding Panel** mounts at the Finding-detail route (`/projects/$projectId/findings/$findingId`)
and presents one Finding with its **Attested evidence anchors** (the evidence lineage) and its
Derived/confidence labels, and is the **entry point** from which the Recommendation Panel opens
(RP-C1). Conflicts are **surfaced, not resolved**. Read-only.

## Source docs / constraints

- Contract E1 (Finding Panel row); UX: `10_product/experience/FINDING_PANEL_SPECIFICATION_V1.md`.
- `code/CONTEXT.md` (Finding = derived gap/conflict/risk anchored to Attested evidence; conflicts
  surfaced not resolved; Recommendation only-in-Finding-context). Decisions #3, #5, #6.
- Consume DTM-0018 finding DTO + its evidence anchors; reuse `EpistemicLabel` (Attested variant for
  evidence, Derived for the finding/confidence). The route placeholder is in `src/app/router.tsx`.

## Locked decisions (do not re-derive)

- **Presents, never generates.** No edit/accept/resolve control on the finding itself.
- **Evidence anchors render as Attested** (`EpistemicLabel` attested/evidence variant); the finding
  + its confidence render as Derived. Conflict shown, not resolved.
- **RP-C1 entry point:** the Recommendation Panel is reachable ONLY from here (the route already
  nests recommendations under the finding — DTM-0019). The Finding Panel renders the affordance to
  open it; it does NOT render recommendations itself (that's DTM-0022).
- No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Panels/FindingPanel/**` (+ tests) and wiring the
  finding-detail route element in `router.tsx` (that one placeholder). Vitest + a Playwright path.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, MRI + other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): renders the finding summary/type + confidence (Derived label) + each evidence
   anchor (Attested label); shows a conflict marker when conflicted; renders a "view
   recommendations" affordance that routes to the nested rec route. **Negatives:** no
   edit/accept/resolve/generate control; evidence never rendered as Derived; the finding never
   rendered as Attested/settled; recommendations are NOT rendered inline (RP-C1 — that's the
   Recommendation Panel's job).
2. Build the panel consuming the DTM-0018 hook; mount at the route; clean loading/empty/not-found
   states.

## API / data / schema contracts

- Consumes the DTM-0018 Finding DTO (with evidence anchors + `DerivedEnvelope`). No backend change.

## Test plan

- **Positive:** finding + confidence (Derived) + evidence anchors (Attested) + conflict marker;
  affordance routes to the nested recommendation route; loading/not-found clean.
- **Negative:** no edit/accept/resolve control; evidence-as-Derived impossible; finding-as-settled
  impossible; no inline recommendations.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → open a finding → see its evidence lineage (Attested) + confidence (Derived) +
  the affordance to view recommendations; no accept/resolve button.

## Done criteria

- Finding Panel presents the finding + Attested evidence + confidence, conflict surfaced, RP-C1
  entry only, read-only, no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0022.

## Worker report

**Status: Ready for review.** Finding Panel built TDD (red → green), mounted at the
Finding-detail route. Contract: **IC-WE-DISCLOSE E1**.

### Files (all under the owned boundary)

- `code/frontend/src/surfaces/Panels/FindingPanel/FindingPanel.tsx` — the panel.
  Presents ONE Finding: summary + user-friendly type + severity + affected CAF
  dimension(s) (descriptive header); the finding's **Derived** confidence label via
  `fromDerivedEnvelope` → `EpistemicLabel`; its **Attested evidence anchors**
  (`evidence_links`) each via the `EpistemicLabel` **attested/evidence** variant
  (`EvidenceAnchor` sub-component); a **conflict marker** when the label is
  `contested` (surfaced, not resolved); and the **RP-C1 affordance** only. Read-only;
  consumes the DTM-0018 `useGetFindingV1FindingsFindingIdGet` hook. Clean
  loading / not-found / empty-evidence states.
- `code/frontend/src/surfaces/Panels/FindingPanel/FindingPanelRoute.tsx` — thin route
  element adapting `$projectId`/`$findingId` params into the panel (mirrors `MRIRoute`).
- `code/frontend/src/surfaces/Panels/FindingPanel/fixtures.ts` — `Finding` DTOs
  (verbatim Data Model v1.2): conflicted (3 anchors, `contested`), clean (1 anchor,
  `none`), and no-evidence (empty `evidence_links`).
- `code/frontend/src/surfaces/Panels/FindingPanel/testHarness.tsx` — in-memory router
  mirroring the real RP-C1 nesting (finding-detail + nested `recommendations` child),
  so the affordance resolves and navigation can be asserted.
- `code/frontend/src/surfaces/Panels/FindingPanel/FindingPanel.test.tsx` — Vitest (13).
- `code/frontend/e2e/finding-panel.spec.ts` — Playwright (3).
- `code/frontend/src/app/router.tsx` — the one allowed swap: finding-detail route
  element placeholder → `FindingPanelRoute` (the nested recommendations route is
  untouched; RP-C1 nesting preserved).

### Exact verification results

- `npm run build` → **pass** (`tsc -b && vite build`; 717 modules; built in ~1.1s).
- `npx vitest run` → **5 files, 58 tests passed** (13 new + 45 existing; all pass).
- `npx playwright test` → **7 passed** (3 new finding-panel + 4 existing). The new
  finding-panel path is added (no skip).
- `npm audit --omit=dev --audit-level=high` → **found 0 vulnerabilities**.
- No new dependency: `package.json` / `package-lock.json` unchanged. Out-of-scope:
  none — only `router.tsx` (the one placeholder swap) + new files under
  `src/surfaces/Panels/FindingPanel/**` and `e2e/finding-panel.spec.ts`.

### Negatives proven (Vitest + Playwright)

- **No edit/accept/reject/defer/resolve/approve/govern/generate/recompute/apply
  control** in the DOM (scans `button`/`[role=button]`/`input`/`textarea` + e2e roles).
- **Evidence-as-Derived impossible:** every evidence-anchor label asserts
  `data-standing="attested"` + `data-source="evidence"`, and `not` Derived.
- **Finding-as-settled impossible:** the finding's confidence label is Derived; no
  "settled"/"resolved" text on the panel; the label is a discriminated union so a
  Derived value cannot pass attested wording (by construction in `EpistemicLabel`).
- **No inline recommendation list:** `recommendation-list` / `recommendation-item`
  absent; the nested `rec-panel-target` is NOT rendered until navigation.
- **Conflict surfaced, not resolved:** `conflict-marker` present on the contested
  finding, absent on the non-contested one.

### RP-C1 handling

The Recommendation Panel is reachable ONLY via the `view-recommendations` affordance,
a TanStack `<Link to="/projects/$projectId/findings/$findingId/recommendations">` — it
routes to the existing nested recommendations route (DTM-0022's surface). No
recommendation content is rendered inline. A Vitest test clicks the affordance and
asserts `router.state.location.pathname` ends with
`/findings/$findingId/recommendations`; the link's `href` is asserted exact.

**Note (no scope creep):** the DTM-0018 `Finding` DTO exposes evidence anchors as
`evidence_links: string[]` (anchor ids), not a rich anchor object — anchors are
rendered as their ids with the Attested/evidence label. No DTO/backend change.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Finding Panel (`surfaces/Panels/FindingPanel/**`) at the finding-detail route: presents the
  finding + confidence as Derived, evidence anchors (`evidence_links`) as Attested/evidence, conflict
  surfaced not resolved, and the RP-C1 affordance only (no inline recommendations). Read-only.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **58 passed** (13 new + 45);
worker playwright 7, `npm audit --omit=dev` 0. Scope = `FindingPanel/**` + one router placeholder
swap; dependency delta **NONE**.

Negatives proven: no edit/accept/reject/defer/resolve/generate/recompute control in the DOM;
evidence-as-Derived impossible; finding-as-settled impossible; no inline recommendation list;
conflict marker present only when contested. RP-C1: the only path to recommendations is the
`view-recommendations` link to the nested route (asserted).

Manual test plan: `npm run dev` → open a finding → evidence lineage (Attested) + confidence
(Derived) + view-recommendations affordance; no accept/resolve button.

Remaining risks: evidence anchors are ids (`evidence_links: string[]`) in the DTO — rendered as
ids; richer anchor objects would be a backend DTO change (out of scope, none made).
