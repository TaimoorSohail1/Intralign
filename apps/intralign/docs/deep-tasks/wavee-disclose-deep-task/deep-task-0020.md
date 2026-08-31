# DTM-0020 — MRI (umbrella) + sub-components (Heatmap, CAF Triangle, Understanding Timeline, Dependencies)

**Status:** In progress — DTM-0019 approved (`d44a467`) · **Module:** DTM-0020 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (MRI) + **DL-047** MRI-04…07 · **Depends:**
DTM-0018 (DTOs/endpoints), DTM-0019 (shell, theme, EpistemicLabel).

## Goal / observable behavior

The **MRI** umbrella surface mounts at the Project Workspace route and visualises a project's
understanding state + diagnostics — presenting Findings, Issues, CAF, Confidence/Outcome
Confidence, and history — **never recomputing**. It hosts four sub-components (DL-047): **Artifact
Understanding Heatmap** (MRI-04), **CAF Triangle** (MRI-05), **Understanding Timeline** (MRI-06),
**Understanding Dependencies** (blocked-awaiting-review) (MRI-07). Every shown item carries its
epistemic label via the DTM-0019 `EpistemicLabel`; current foreground + history both visible.

## Source docs / constraints

- Contract: `20_handoff/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md` E1 (MRI row) +
  DL-047 additions (MRI-04…07). UX spec: `10_product/experience/MRI_*SPECIFICATION_V1.md` (read
  the actual filename — `MRI_EXPERIENCE_SPECIFICATION_V1.md` or `MRI_WORKSPACE_SPECIFICATION_V1.md`).
- `code/CONTEXT.md` Wave E glossary (Disclose, MRI, epistemic-safety labeling); decisions file
  #3, #5, #9.
- Consume the DTM-0018 generated hooks (`src/api/generated/**`) for findings/confidence/CAF; the
  DTM-0019 `EpistemicLabel` + theme + the MRI route in `src/app/router.tsx`.

## Locked decisions (do not re-derive)

- **Presents, never generates/recomputes** (the spine). MRI reads governed objects; it computes no
  cognition, scores nothing, accepts nothing. Negative-proven.
- **Epistemic-safety everywhere:** every Finding/Issue/CAF/Confidence rendered through
  `EpistemicLabel` (Attested/Derived + band + conflict). Confidence reads as trust-in-understanding,
  never project health. Derived never shown settled.
- **Current + history:** show the latest understanding prominently AND a history view (the
  Understanding Timeline MRI-06 reads the CHR trail; presentation is append-only).
- **No new dependency.** If a viz genuinely needs a charting lib ⇒ STOP and escalate in the report
  (prefer SVG/MUI primitives for Heatmap/Triangle/Timeline rather than adding a dep).

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/MRI/**` (the MRI surface + the 4 sub-components + their
  tests), and wiring the MRI route element in `src/app/router.tsx` (replace the placeholder for the
  workspace/MRI route only). Component tests (Vitest) + an E2E happy-path (Playwright) for MRI.
- **READ-ONLY:** backend, generated client (consume), theme/EpistemicLabel (reuse, don't fork),
  other surfaces' routes/placeholders.

## Packages / refactors

- None new (use MUI + SVG). The 3 dev-test deps from DTM-0019 are available.

## Implementation instructions (TDD)

1. Red (Vitest): MRI renders Findings/Issues/CAF/Confidence each wrapped in `EpistemicLabel`;
   the 4 sub-components render from fixture DTOs; the Timeline shows history (current + past CHR
   refs). **Negatives:** a Derived value can't render as settled; MRI exposes no
   compute/recompute/accept control (it's read-only presentation); confidence label never says
   "health/ready/probability".
2. Build the MRI surface + sub-components consuming the generated hooks; mount at the MRI route.
   Use loading/empty states (lists may be empty until projections are populated — render cleanly).

## API / data / schema contracts

- Consumes DTM-0018 DTOs (Finding, CAFState, ConfidenceState + their `DerivedEnvelope`). No backend
  change. Empty-list and loading states must render (projection-write is upstream).

## Test plan

- **Positive:** each governed object rendered with its label; 4 sub-components present; current +
  history both shown; empty/loading states clean.
- **Negative:** Derived-as-settled impossible; no recompute/accept affordance on MRI; confidence
  not shown as health/probability.
- `npm run build` + `vitest run` + (Playwright MRI happy-path) + drift gate + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → open a project workspace → MRI renders the 4 sub-components + labelled
  findings/CAF/confidence; no compute/accept button; history view present.

## Done criteria

- MRI + MRI-04…07 present governed objects with epistemic labels + current/history, read-only,
  no new dep, tests green. PR cites IC-WE-DISCLOSE / DL-047. Ready for DTM-0021 (Finding Panel).

## Worker report

**Status: Ready for review.** Cites IC-WE-DISCLOSE E1 + DL-047 (MRI-04…07). Staged, not
committed; unrelated working-tree changes preserved.

### Files added (`code/frontend/src/surfaces/MRI/**`)

| File | Role |
|---|---|
| `MRIWorkspace.tsx` | The MRI umbrella surface. Consumes the DTM-0018 read hooks, presents Outcome Confidence, CAF, and Findings (grouped into Missing/Risky/Incomplete), mounts the four sub-components. Read-only. |
| `MRIRoute.tsx` | Thin route adapter — pulls `projectId` from the route param via `getRouteApi("/projects/$projectId/")` → `<MRIWorkspace/>`. Mounted at the Project Workspace route. |
| `UnderstandingHeatmap.tsx` | **MRI-04** — Artifact Understanding Heatmap. |
| `CafTriangle.tsx` | **MRI-05** — CAF Triangle. |
| `UnderstandingTimeline.tsx` | **MRI-06** — Understanding Timeline (CHR history trail). |
| `UnderstandingDependencies.tsx` | **MRI-07** — Understanding Dependencies (blocked / awaiting review). |
| `FindingRow.tsx` | A single finding summary row (lists, never duplicates; routes to Finding Panel). |
| `categories.ts` | The Missing/Risky/Incomplete lens over the canonical 7-type finding taxonomy (§E) + qualitative severity ordering + `isAwaitingReview`. No new ontology. |
| `fixtures.ts` | Governed-object DTO fixtures (verbatim Data Model v1.2 shapes). |
| `testHarness.tsx` | Test-only render harness (theme + query + in-memory router); never imported by the app bundle. |
| `MRIWorkspace.test.tsx`, `subcomponents.test.tsx` | Vitest suites (21 tests). |
| `e2e/mri.spec.ts` | Playwright MRI happy-path + a presents-never-generates negative. |

Wiring: `src/app/router.tsx` — the single allowed change (the Project Workspace placeholder
component swapped for `MRIRoute`; `PlaceholderSurface` import retained for the other routes).

### The sub-components and how they were rendered (SVG + MUI only — no charting library)

- **MRI-04 Heatmap** — an SVG `<rect>` grid (rows = MRI categories, cols = the existing severity
  concept). Intensity is a **qualitative** opacity tier (none/light/strong) via `<title>` words —
  no number/percentage/rank. Clean empty state when there are no findings.
- **MRI-05 CAF Triangle** — an SVG `<polygon>` with three **co-equal** vertices (Clarity/Alignment/
  Feasibility), each a banded `<circle>` + label; per-dimension reliability listed below. The whole
  CAF assessment carries its `EpistemicLabel` (Derived + band). Indices are NOT shown as numbers —
  only bands. Empty state when CAF is absent/malformed.
- **MRI-06 Timeline** — a vertical SVG rail with one node per analysis run (newest = current,
  highlighted), alongside MUI text per entry. **Current + history both shown**, append-only
  presentation. Empty state when there is no history.
- **MRI-07 Dependencies** — a MUI `<List>` of open (not closed/superseded) findings = blocking
  understanding dependencies, each with a small SVG link glyph, a route to its Finding Panel, and
  its `EpistemicLabel`. Empty state when nothing is awaiting review.

Every governed Derived value (each Finding, the CAF assessment, Outcome Confidence, each blocking
dependency) renders through `EpistemicLabel` using `fromDerivedEnvelope(dto.label)` — the labeling
rule is reused, never re-implemented.

### Epistemic-safety negatives proven (Vitest + Playwright)

- **Presents, never generates:** scanned every `button`/`[role=button]`/`input` (Vitest) and every
  button/menuitem/checkbox/switch/radio (Playwright) — none match
  `recompute|reanalyze|compute|score|accept|reject|approve|generate|run analysis|apply|edit`. MRI
  has no compute/recompute/score/accept control in the DOM.
- **Derived never settled:** every label that is Derived keeps `data-standing="derived"`; the
  surface contains no "settled"/"confirmed by oslo" text. (The discriminated-union `EpistemicLabel`
  makes a Derived value structurally unable to render attested.)
- **Confidence ≠ health/readiness/probability:** the confidence panel text never matches
  `health|ready|readiness|probability|on track|likelihood`.
- **Qualitative only:** the surface text shows no `\d%`, `score`, `rank`, or `\d/100`.
- **Conflict surfaced, not resolved:** the contested finding renders the conflict marker.
- **Current + history:** the Timeline shows `timeline-current` plus the prior run entry.

### Exact command results (`cd code/frontend`)

- `npm run build` (tsc -b + vite) → **pass** — `✓ built in 1.15s`, `710 modules transformed`
  (pre-existing >500 kB chunk advisory only, not an error).
- `npx vitest run` → **pass** — `Test Files 4 passed (4) · Tests 45 passed (45)` (21 new MRI +
  the 24 existing from DTM-0019).
- `npx playwright test` → **pass** — `4 passed` (2 existing shell + 2 new MRI). Chromium available.
- `npm audit --omit=dev --audit-level=high` → **`found 0 vulnerabilities`**.
- Drift gate (`tsc --noEmit`, ADR-0003) → **clean**.

### Constraints confirmed

- **No new dependency** (runtime or dev) — `package.json` unchanged; Heatmap/Triangle/Timeline are
  SVG + MUI primitives.
- **No backend / generated-client / theme / EpistemicLabel edits** — `git diff` touches only
  `src/app/router.tsx` (the one allowed placeholder swap); everything else under
  `src/surfaces/MRI/**` + `e2e/mri.spec.ts` is new.
- **Loading + empty states render cleanly** — verified live against the (unbuilt) backend: the read
  hooks resolve empty and all four sub-components show their empty states with **zero page errors**
  (`pageerror` count = 0). The surface defensively coerces non-array/non-object responses to the
  empty state so a malformed/absent projection can never crash MRI.

### Notes / nothing blocked

- The `src/v1/...` reads have no dev-server proxy in this environment, so the live route shows the
  empty states (expected — projection-write is upstream). No charting library was needed; no
  escalation required.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- MRI umbrella surface (`surfaces/MRI/**`) mounted at the Project Workspace route + the 4 DL-047
  sub-components (Heatmap, CAF Triangle, Understanding Timeline, Dependencies), all SVG+MUI (no
  charting lib). Read-only presentation of Findings/CAF/Outcome-Confidence/history, every Derived
  value through `EpistemicLabel`/`fromDerivedEnvelope`. Current + history both shown.

Verification (EM re-ran):
- `npm run build` → built. `npx vitest run` → **45 passed** (21 new + 24 existing). Worker:
  playwright 4 passed, `npm audit --omit=dev` 0 vulns, drift gate clean.
- Scope clean: tracked changes are `surfaces/MRI/**` + the one Project-Workspace placeholder swap
  in `router.tsx`. Dependency delta: **NONE** (no charting lib added — SVG+MUI).
- Epistemic-safety negatives proven (Vitest + Playwright): no compute/recompute/score/accept/
  generate control in the DOM; Derived never renders settled; confidence text never reads
  health/readiness/probability; no numeric score/percentage — bands only.

Manual test plan:
- `npm run dev` → project workspace → MRI shows the 4 sub-components + labelled findings/CAF/
  confidence; no compute/accept button; Timeline shows current+history; empty/loading states clean.

Remaining risks / accepted follow-ups:
- **Vite dev has no `/v1` proxy** → reads hit the SPA fallback (HTML) in `npm run dev`; the surface
  defensively coerces non-JSON to clean empty states (no crash). A dev-proxy to `:8000` is a small
  follow-up so surfaces exercise real DTO shapes locally — flagged, not blocking (live data also
  waits on the upstream projection-write).
- Missing/Risky/Incomplete grouping is a presentation lens over the canonical 7-type taxonomy — no
  new ontology (verified in `categories.ts`).
