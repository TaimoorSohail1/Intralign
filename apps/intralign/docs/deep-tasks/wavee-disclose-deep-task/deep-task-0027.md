# DTM-0027 — History / Timeline (CHR + UAR + plan facts; the append-only trail)

**Status:** In progress — DTM-0026 approved (`25c1ef6`) · **Module:** DTM-0027 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (History/Timeline) · **Depends:** DTM-0018/0019.

## Goal / observable behavior

The **History / Timeline** surface reconstructs **the trail** — what OSLO said when (Cognition
History Records), what the user confirmed (User Acceptance Records + plan facts) — **record-exact**,
the "why did it change" narrative. Presentation is **append-only** (history is never edited/
reordered destructively). Plan facts display as **user-attested**. Read-only.

## Source docs / constraints

- Contract E1 (History/Timeline row: "reconstruct the trail … record-exact; history append-only").
  UX: `10_product/experience/HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1.md`.
- `code/CONTEXT.md` (CHR = append-only, recompute appends never overwrites; UAR = user-attested,
  version-pin; plan fact = user-attested, not world-truth). Decisions #3, #5.
- Consume the DTM-0018 history read (CHR trail) + acceptance read (UAR + plan facts). Reuse
  `EpistemicLabel` (Derived for CHR entries; **user-attested** variant for plan facts/UAR).

## Locked decisions (do not re-derive)

- **Presents, never generates.** No edit/accept/generate control. The timeline is a read-only
  reconstruction.
- **Record-exact + append-only:** render each CHR/UAR exactly as recorded, in append order; never
  present history as editable/mutable; superseded entries remain visible (the trail shows
  supersession, doesn't erase it).
- **Plan facts = user-attested** (`EpistemicLabel` user variant — "you confirmed … not world-truth"),
  distinct from evidence-attested and OSLO-self-attested; CHR entries are Derived. No new dependency.

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Timeline/**` (+ tests) and wiring the history/timeline route/
  placeholder in `router.tsx` (the one swap). Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (Vitest): renders the CHR trail (current + past entries, append order, each labelled) + UARs
   + plan facts (user-attested label); shows supersession without erasing the superseded entry.
   **Negatives:** no edit/accept/generate control; history not presented as editable/mutable;
   plan-fact rendered user-attested (not world-truth, not evidence-attested); CHR entries Derived
   (never settled); ordering is append-exact (no destructive reorder).
2. Build from the DTM-0018 history + acceptance reads; mount; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 history (CHR) + acceptance (UAR/plan-fact) reads (+ `DerivedEnvelope` for
  CHR; user-attested for plan facts). No backend change.

## Test plan

- **Positive:** CHR trail + UARs + plan facts in append order, labelled; supersession visible;
  empty/loading clean.
- **Negative:** no edit/accept/generate control; history-as-editable rejected; plan-fact-as-world-
  truth/evidence-attested rejected; CHR-as-settled impossible; append-exact ordering.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → timeline shows the CHR trail + what the user confirmed (plan facts user-attested);
  superseded entries still visible; no edit/accept control.

## Done criteria

- History/Timeline reconstructs the CHR+UAR+plan-fact trail, record-exact + append-only, plan facts
  user-attested, read-only, no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0028.

## Worker report

**Status: Ready for review.**

### Files

- `code/frontend/src/surfaces/Timeline/Timeline.tsx` — the surface (presentational, `projectId` prop).
- `code/frontend/src/surfaces/Timeline/TimelineRoute.tsx` — thin route element (reads `$projectId`).
- `code/frontend/src/surfaces/Timeline/fixtures.ts` — the three DTM-0018 read shapes (CHR/UAR/plan-fact DTOs, verbatim).
- `code/frontend/src/surfaces/Timeline/testHarness.tsx` — theme + query + in-memory router wrapper.
- `code/frontend/src/surfaces/Timeline/Timeline.test.tsx` — Vitest (17 tests: positive + the critical negatives).
- `code/frontend/e2e/timeline.spec.ts` — Playwright (mounts + no-action negative).
- `code/frontend/src/app/router.tsx` — **the one route add**: `projectRoute` child `path: "/history"` → `TimelineRoute` (import + route def + registered in `projectRoute.addChildren`).

### How the trail + supersession were rendered

There is **no dedicated CHR/history endpoint** in the generated client (data gap, flagged below). Per the binding `CONTEXT.md` (CHR = the records the recompute/analysis runs append) and the house pattern (`MRI/UnderstandingTimeline.tsx`), the **CHR trail is reconstructed from the analysis runs that appended the CHRs** — `useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet`. The full trail is three already-retained, append-only DTM-0018 reads:

- **CHR trail** ← `useListAnalysisRuns…` — each run is a **Derived** entry (`<EpistemicLabel epistemic={{ standing: "derived" }} />`), never settled. Current understanding = the **last completed** run, marked distinctly ("Current understanding") via a read-only lookup that does **not** reorder the trail.
- **UAR trail** ← `useListAcceptances…` — **user-attested** (`standing:"attested"`, `source:"user"`), shows the mandatory **version-pin** (the exact CHR accepted).
- **Plan-fact trail** ← `useListPlanFacts…` — **user-attested** ("You confirmed …"), proposition rendered **verbatim** (record-exact).

**Supersession is additive, not erased:** a run with `run_status: 'superseded'` renders with `data-superseded="true"` + a "Superseded (prior)" chip and **stays in the trail** (never marked current, never removed). A `failed` run is shown honestly as failed (last-known-good retained). The MRI visual idiom (vertical SVG rail + MUI primitives, no charting lib) is **reused fresh** in a local `TrailRail` — the MRI component was **not** forked or imported.

**Append-exact ordering:** each source's records render in the **exact order the read returned them** (`runs.map`/`acceptances.map`/`planFacts.map` over the raw arrays) — no `.sort`, no `.reverse`, no destructive reorder. Fixtures are intentionally authored out of strict chronological order so the test proves render order == source order.

### Negatives proven (Vitest, all green)

- **Presents, never generates** — scans every `button`/`[role=button]`/`input`/`textarea`/`select`/`[contenteditable]` for `edit|accept|reject|defer|generate|delete|restore|rollback|approve|govern|recompute|reanalyze|apply|score|resolve` → none.
- **History not editable/mutable** — same control scan + a record-exact assertion that rendering does **not** mutate the governed DTOs (`toEqual` before/after a deep clone).
- **Append-exact ordering** — rendered `data-run-id` / `data-uar-id` / `data-plan-fact-id` sequences `toEqual` the source fixtures' id sequences (no reorder).
- **Plan-fact user-attested** — every plan-fact label has `data-source="user"`, **not** `evidence`, **not** `oslo`, **not** `data-standing="derived"`; surface never says "world-truth"/"verified".
- **CHR Derived, never settled** — every CHR entry label has `data-standing="derived"` and not `attested`; surface never says "settled".
- Plus: never frames itself as audit/approval/compliance/decision-record; supersession visible without erasing the superseded entry; clean loading + "no history yet" empty states.

### Exact verification results

```
$ cd code/frontend && npm run build
> tsc -b && vite build
✓ 748 modules transformed.
✓ built in 1.14s        # tsc -b clean → no Orval drift, no type errors

$ npx vitest run src/surfaces/Timeline/Timeline.test.tsx
 Test Files  1 passed (1)
      Tests  17 passed (17)

$ npx vitest run            # full suite (new + existing)
 Test Files  12 passed (12)
      Tests  162 passed (162)

$ npx playwright test       # full e2e (incl. new timeline path; shell /settings probe still green)
  26 passed (3.6s)

$ npm audit --omit=dev --audit-level=high
found 0 vulnerabilities
```

### Scope / dependency confirmation

- **No new dependency** — `package.json` / `package-lock.json` unchanged (git diff empty).
- **No out-of-scope edits** — only `src/app/router.tsx` (the one route add), new `src/surfaces/Timeline/**`, and new `e2e/timeline.spec.ts`. Backend, generated client, theme, `EpistemicLabel`, and other surfaces untouched. Untracked `Companion/` working-tree changes preserved.
- **No `shell.spec.ts` repoint needed** — I **added** a project-scoped `/history` route rather than swapping an existing top-level placeholder, so the shell probe (`/settings`) is unaffected; full e2e stays green.

### Data gap flagged

- **No dedicated CHR / history read endpoint** in the generated Orval client. The CHR trail is therefore reconstructed from `GET /v1/projects/{id}/analysis-runs` (the runs that append CHRs), consistent with `CONTEXT.md` and the MRI Understanding Timeline. `AnalysisRun` carries `previous_run_id` + `run_status` (`superseded`/`failed`), which is sufficient to present the append-only supersession lifecycle — but a richer per-CHR history (e.g. the CHR id, the `current_chr_ref` lineage already on `DerivedEnvelope`, or a unified cross-category history feed per spec §G) would let the surface present finding/recommendation supersession and the comment/sharing/awareness **reference** categories (spec §E Q3) that are currently out of reach from the available reads. The UAR + plan-fact reads expose `version_pin` but no link from a UAR to the specific accepted item's panel, so UAR/plan-fact entries currently route to the project context rather than the precise pinned object. None blocks this slice; noting for a future read-shape expansion.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- History/Timeline (`surfaces/Timeline/**`) at `/projects/$projectId/history`: reconstructs the
  trail — CHR entries (Derived, from analysis-runs) + UARs (user-attested + version-pin) + plan
  facts (user-attested, verbatim). Append-only, supersession additive, read-only.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **162 passed** (17 new + 145);
worker playwright 26, audit 0. Scope = Timeline/** + one route ADD (no shell repoint needed);
dependency delta **NONE**.

Negatives proven: no edit/accept/generate/delete/restore/rollback control; render mutates no DTO
(record-exact); append-exact ordering (rendered id sequence == source order, fixtures deliberately
out of order); plan-fact `source:"user"` not evidence/oslo/derived, never "world-truth"; CHR
`standing:"derived"` never settled; supersession visible without erasing.

Remaining risks / flagged: no dedicated CHR/history endpoint → trail reconstructed from
analysis-runs (per CONTEXT.md + the MRI idiom); UAR/plan-fact entries route to project context (no
UAR→pinned-item link in the read); a unified cross-category history feed would be a read-shape
expansion. Non-blocking.
