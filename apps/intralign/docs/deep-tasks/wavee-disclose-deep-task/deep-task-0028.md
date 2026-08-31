# DTM-0028 — Export / Share-out (packages existing understanding; labels + provenance preserved; no new claims)

**Status:** In progress — DTM-0027 approved (`79fab30`) · **Module:** DTM-0028 · **Phase:** VI
(Wave E) · **Contract:** **IC-WE-DISCLOSE** E1 (Export/Share-out) + OBS-WE (`Export produced`) ·
**Depends:** DTM-0018/0019.

## Goal / observable behavior

**Export / Share-out** packages the **existing** governed outputs (current + history) into an
exportable artifact that **honors epistemic labels** (Derived/Attested, confidence band, plan-fact
attribution) and **preserves provenance** — and introduces **no new claim** (exposure = epistemic-
safety labeling; no Authority gate in R1). Read-only over governed objects; produces an export
artifact (client-side packaging of the fetched governed DTOs) and conceptually emits `Export
produced`.

## Source docs / constraints

- Contract E1 (Export row: "honors epistemic labels … preserves provenance; no new claims") +
  E2 negative (export emitting a claim not in the governed source) + OBS-WE (`Export produced` with
  provenance audit). UX: `10_product/experience/EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1.md`.
- `code/CONTEXT.md` (epistemic-safety labeling; plan-fact user-attested). Decisions #3, #5.
- Consume the DTM-0018 governed reads; reuse `EpistemicLabel` semantics in the exported artifact
  (the export must carry the same labels the surfaces show). If no server export endpoint exists,
  package client-side from the fetched DTOs and flag (do not invent a server export claim).

## Locked decisions (do not re-derive)

- **Packages existing understanding only (Critical negative):** every line in the export traces to
  a governed source object; the export emits **no claim absent from the governed source** (no
  summarization that invents, no synthesized conclusion). Labels (Attested/Derived + band) + plan-
  fact attribution + provenance (the CHR version/source) travel into the export.
- **No Authority/exposure gate in R1:** exposure = labeling, not permission gating. (No share-
  permission control — that's prohibited/owner territory anyway.)
- **Presents, never generates.** No generate/score/accept control. No new dependency (use the
  browser's built-in download/Blob or a simple in-app preview — do NOT add an export/PDF library;
  if a format genuinely needs one ⇒ STOP and flag).

## Owned files / boundaries

- **OWN:** `code/frontend/src/surfaces/Export/**` (+ tests) and wiring the export route/affordance
  in `router.tsx` (the one swap/add). Vitest + Playwright.
- **READ-ONLY:** backend, generated client, theme/EpistemicLabel, other surfaces.

## Packages / refactors — none new (browser Blob/download only).

## Implementation instructions (TDD)

1. Red (Vitest): builds an export of the governed outputs (findings/recs/confidence/history) with
   each item carrying its epistemic label + provenance + plan-fact attribution; a download/preview
   affordance. **Negatives:** the export contains **no claim not present in a governed source**
   (assert every exported claim maps to an input DTO field — no invented/summarized conclusion);
   Derived labelled Derived (not settled) in the export; plan-fact attributed user-attested;
   provenance preserved (CHR ref/source present); no generate/score/accept control.
2. Build client-side packaging from the DTM-0018 reads; mount; clean loading/empty states.

## API / data / schema contracts

- Consumes the DTM-0018 governed reads (+ `DerivedEnvelope`/provenance). Export is client-side
  packaging (Blob/download or preview). No backend change.

## Test plan

- **Positive:** export packages governed outputs with labels + provenance + plan-fact attribution;
  download/preview works; empty/loading clean.
- **Negative:** unsourced claim in export rejected (every claim ← a governed source); Derived-as-
  settled in export impossible; provenance preserved; no generate/accept control.
- `npm run build` + `vitest run` + Playwright + drift + `npm audit --omit=dev`.

## Manual checks (EM)

- `npm run dev` → export a project → the artifact carries Attested/Derived labels + confidence bands
  + plan-fact attribution + provenance; contains nothing not in the governed source; no new claim.

## Done criteria

- Export packages existing understanding with labels + provenance preserved, no new claim (negative-
  proven), read-only, no new dep, tests green. PR cites IC-WE-DISCLOSE. Ready for DTM-0029.

## Worker report

**Status: Ready for review.**

### Files (all in scope)

- `code/frontend/src/surfaces/Export/buildExportPackage.ts` — **the packaging core**
  (pure, no fetch/mutation/compute). Takes the already-fetched governed DTOs and emits
  an `ExportPackage` whose every `ExportClaim` is a `{ label, value, epistemic,
  provenance }` quad where `value` is lifted VERBATIM off a governed DTO field and
  `provenance = { sourceObject, sourceField, sourceId?, chrRef? }` names that exact
  field. Also `toPlainText` / `toJson` serialisers (browser-native), `resolveCurrency`,
  `allClaims`, and the mandatory `EXPORT_DISCLAIMER`.
- `code/frontend/src/surfaces/Export/Export.tsx` — the surface: consumes the 8 DTM-0018
  reads read-only, packages via `buildExportPackage`, renders an in-app **preview** (each
  claim group carries its `EpistemicLabel` + a visible provenance row `source:
  object.field @ chrRef`), and offers browser-native **download** (JSON + text Blob via
  `URL.createObjectURL` + transient anchor) and **copy**. Clean loading / empty / stale
  states + the always-present disclaimer.
- `code/frontend/src/surfaces/Export/ExportRoute.tsx` — thin route adapter.
- `code/frontend/src/surfaces/Export/fixtures.ts` — DTO-verbatim fixtures.
- `code/frontend/src/surfaces/Export/testHarness.tsx` — theme + query + in-memory router.
- `code/frontend/src/surfaces/Export/buildExportPackage.test.ts` — packager unit + the
  no-new-claim oracle (the Critical negative).
- `code/frontend/src/surfaces/Export/Export.test.tsx` — surface tests + negatives.
- `code/frontend/e2e/export.spec.ts` — Playwright mount + no-generate-control negative.
- `code/frontend/src/app/router.tsx` — the **one route add**: `exportRoute` under
  `projectRoute` at `/projects/$projectId/export`. (No `shell.spec.ts` placeholder probe
  was orphaned — the probe still targets the untouched `/settings` placeholder.)

### Export format + how no-new-claim is guaranteed + provenance preserved

- **Format:** browser-native only — a downloadable **JSON** artifact (the full
  provenance-carrying `ExportPackage`) + a **copyable plain-text** summary + an in-app
  **preview**. No export/PDF/CSV library added (PDF/shareable-link formats from the UX
  spec §H are tier-gated/deferred per §N/§T — not built here; no library was needed, so
  no STOP/flag was triggered).
- **No-new-claim (structural):** the surface renders ONLY what `buildExportPackage`
  produced, and the packager NEVER synthesises a value — it reads a governed field and
  copies it, attaching the `{sourceObject, sourceField}` that field came from. There is
  no code path that emits a claim without a backing field (no summary, no verdict, no
  count beyond `array.length`). The numeric 0–100 confidence/CAF index is never surfaced
  (band only); no `%`/project-health/readiness/probability framing in any claim value.
- **Provenance preserved:** every Derived claim carries the `current_chr_ref` (the CHR
  version presented) as `provenance.chrRef`, and the package carries the de-duped
  `chrRefs` set — so what-was-shown is reconstructable (OBS-WE-DISCLOSE). The preview
  shows the CHR ref/source inline; the JSON carries it on every claim.
- **Labels travel:** Derived items map through `fromDerivedEnvelope` → render Derived +
  band (never upgraded, never settled); plan facts + UARs render `attested/user` ("You
  confirmed", not world-truth). `EpistemicLabel`'s discriminated union makes Derived-as-
  settled / plan-fact-as-world-truth unconstructable.

### The Critical negative, proven

`buildExportPackage.test.ts` builds an **independent oracle** (`resolveSourceValue`) that
re-walks each claim's `provenance.{sourceObject, sourceField, sourceId}` against the RAW
input DTOs via a separate path-reader, and asserts for EVERY claim:
`String(sourceValue) === claim.value` **and** `sourceValue !== undefined`. A claim with
no backing input field (an invented/summarised conclusion) would fail both. Companion
negatives: Derived stays Derived and band-low is never upgraded to high; plan facts/UARs
stay user-attested; currency `previous` is read off the governed `AnalysisRun.run_status:
"superseded"` (not a fabricated `is_stale`); no input mutation (record-exact). The surface
+ e2e suites prove no generate/score/accept/reject/defer/edit/govern/reanalyze control.

### Verify (exact results)

- `npm run build` (`tsc -b && vite build`): **clean**, 751 modules, built in 1.17s.
- `npx vitest run`: **193 passed (14 files)** — 31 new Export tests + all existing pass.
- `npx playwright test`: **28 passed** (incl. 2 new export specs).
- `npm audit --omit=dev --audit-level=high`: **found 0 vulnerabilities.**
- No new dependency (`package.json`/`-lock` unchanged); no out-of-scope edits
  (`git status`: only `router.tsx` modified + `src/surfaces/Export/` + `e2e/export.spec.ts`
  + this task file). Backend/generated-client/theme/EpistemicLabel/other surfaces untouched.

### Data gap flagged (not filled)

- **No server export/report/share endpoint** exists in the generated Orval client (only
  the 8 governed reads). The export is packaged **client-side** from the fetched DTOs, as
  the contract permits ("If no server export endpoint exists, package client-side … and
  flag — do not invent a server export claim"). The `Export produced` OBS-WE event is
  therefore conceptual here, not emitted by a backend call. No server "export produced"
  claim was invented.
- **No `is_stale` field**: the analysis-currency marker reads the governed
  `AnalysisRun.run_status` (`superseded` ⇒ previous analysis), consistent with the
  Companion/Timeline slices. The gap is flagged, not filled.
- Shareable-link / PDF formats (UX §H) are tier-gated/deferred (§N/§T) and not built;
  no Authority/share-permission gate (exposure = labeling only, decision #5).

Did **not** add an EM approval section; did **not** commit. Changes are ready to stage.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Export/Share-out (`surfaces/Export/**`) at `/projects/$projectId/export`: a pure packaging core
  (`buildExportPackage.ts`) turns the governed reads into `{label, value, epistemic, provenance}`
  claims (value lifted verbatim off a DTO field), rendered as preview + browser-native JSON/text
  download/copy. Labels + plan-fact attribution + CHR provenance travel into the artifact. Read-only.

Verification (EM re-ran): `npm run build` built; `npx vitest run` **193 passed** (31 new + 162);
worker playwright 28, audit 0. Scope = Export/** + one route add; dependency delta **NONE** (browser
Blob/anchor only — no export/PDF library).

Negatives proven (the Critical one): a provenance **oracle** re-walks every exported claim back to
its raw input DTO field and asserts `String(sourceValue) === claim.value` (an invented/summarized
conclusion would fail); Derived stays Derived (band never upgraded, never settled); plan-fact/UAR
user-attested (not world-truth); provenance (`current_chr_ref`) preserved; numeric index never
surfaced; no generate/score/accept control.

Remaining risks / flagged: no server export/report/share endpoint → client-side packaging,
`Export produced` is conceptual; PDF/shareable-link deferred (tier-gated); no Authority/share-
permission gate (exposure = labeling only). Non-blocking.
