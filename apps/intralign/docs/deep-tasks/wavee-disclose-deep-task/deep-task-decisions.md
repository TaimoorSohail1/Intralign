# Deep-task decisions — Wave E: Disclose Surfaces (presentation)

Implementation-control record for Phase VI / Wave E — the **final phase** (Release 1
feature-complete gate). Cites source-of-truth; does not restate it. **Branch:**
`feat/phase6-wavee-disclose` (do NOT create another).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **Contract:** `20_handoff/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md` (E0–E3
  IC/QA/OBS-WE-DISCLOSE + DL-047 additions: OSLO Chat CHAT-01…04, MRI-04…07, AW-04/05, CRR-05;
  DL-048 honest-limit UP-4). The contract + UX specs WIN over any summary.
- **Plan:** `30_engineering/implementation/Phase_VI_Wave_E_Disclose_Surfaces/IMPLEMENTATION_PLAN.md`.
- **ADR-0010** (`code/docs/adr/0010-wave-e-disclose-build-plan.md`) — the locked build plan + the
  20 locked decisions; **CONTEXT.md** Wave E glossary (Disclose, Render, epistemic-safety label,
  MRI, RP-C1, OSLO Chat, honest-limit).
- **UX specs** (`10_product/experience/`): `RELEASE_1_UI_SPECIFICATION_V1` · `UI_SCREEN_INVENTORY`
  · `MRI_*` · `FINDING_PANEL_*` · `RECOMMENDATION_PANEL_*` (RP-C1) · `PROJECT_OVERVIEW_*` +
  `PROJECT_DASHBOARD_AND_PROJECT_LIST_*` · `UNDERSTANDING_COMPANION_*` · `NOTIFICATION_AND_AWARENESS_*`
  · `HISTORY_AND_TIMELINE_*` · `EXPORT_AND_SHARE_OUT_*` · `OSLO_CHAT_*` · `ARTIFACT_AUTHORING_*`
  (AW-04/05). **Palette/access:** Intralign (CHG-068) + WCAG 2.1 AA + evergreen.
- **Interfaces:** the API Contract Spec (`20_handoff/interfaces/`) + Data Model v1.2
  (`shared/entities.py`). ADR-0003 (REST `/v1` + Orval drift gate). DL-043/047/048/055;
  ANTI_ASSUMPTION protocol.

## Repo facts (the scaffold this builds on)

- **Backend REST is unbuilt:** `backend/api/v1/` wires only `GET /health` (tags `platform`);
  `v1/routers/__init__.py` lists the intended resources (projects, artifacts, evidence,
  analysis_runs, findings, recommendations, reports, comments, shares, notifications) as a
  **commented catalog — none included**. `services/render/__init__.py` is a 1-line stub.
  `shared/entities.py` has Data-Model-v1.2 enums + skeleton DTOs (Project, AnalysisRun,
  SynthesizedPlanningModel, PlanningArtifact; FindingStatus/RecommendationStatus/etc.).
- **Frontend is a bare scaffold:** React 18.3 · Vite 5.3 · MUI 5.16 · Emotion · TanStack Query
  5.51 + Router 1.45 · Orval 6.31 · Axios. `main.tsx` = `QueryClientProvider` + a placeholder div;
  **no router/theme/components**. `src/surfaces/{MRI,Panels,Overview,Timeline,Notifications,Export}/`
  exist but are **empty**. Orval (`orval.config.ts`, tags-split/react-query/axios) generates from
  `http://localhost:8000/openapi.json` → currently only the `/health` client.
  `scripts/check-openapi-drift.sh` regenerates + `tsc --noEmit` (the drift gate).
- **Cognition is built (Waves A–U):** the governed objects exist as internal cognition
  (`shared/epistemic.py`: Finding/Issue/Confidence/CAFAssessment/OutcomeConfidence/Recommendation/
  ClarificationRequest/SuggestedFix/CognitionHistoryRecord/UserAcceptanceRecord/PlanFact/
  AcceptanceImpactAssessment) — but reached only via orchestration/persistence, **not REST**.
- **CI:** `app-ci.yml` Gate 1 builds the frontend (`npm ci && npm run build` = tsc -b + vite);
  Gate 6 `npm audit`. The Orval drift gate is enforced implicitly via `tsc` (ADR-0003).

## Locked decisions (apply across slices)

1. **One fresh worker per slice, strictly sequential** (ADR-0010). No slice starts until the
   prior is reviewed/fixed/verified/approved.
2. **REST-exposure FIRST (DTM-0018), then app-shell+theme (DTM-0019), then one surface per slice.**
   The surface slices (DTM-0020+) are authored **after** DTM-0018 lands (they bind to its concrete
   endpoints/DTOs — authoring them before is premature).
3. **Disclose presents, never generates** (the spine): no surface/router computes, scores,
   recommends, promotes Derived→Attested, **accepts** (the Recommendation Panel renders the
   accept/reject/defer *affordance* → routes to the **existing Wave U capture**; Disclose never
   accepts), or changes an assessment. Negative-proven per QA-WE-DISCLOSE.
4. **REST is read-mostly** (DTM-0018): `api/v1` GET endpoints present governed objects via
   `services/render` mappers → **Data Model v1.2 DTOs** (`shared/entities.py`, exposed verbatim
   per ADR-0003). Writes reuse the **existing** capture/acceptance seams (no new write paths in
   Disclose). Internal `epistemic.py` types are **not** exposed verbatim — render maps them.
5. **Epistemic-safety labeling everywhere:** one reusable label component (DTM-0019) renders
   **Attested/Derived + confidence band (0–49/50–74/75–100, ±3 conservative edge guard) + conflict**;
   plan facts shown user-attested; confidence = trust-in-understanding, never project health.
   Derived never shown settled (Critical negative).
6. **RP-C1:** Recommendation Panel renders only in a Finding context (enforced in the UI/router).
7. **Visual system (ANTI_ASSUMPTION):** Intralign palette (charcoal `#111315` / warm-white
   `#F5F4F0` / orange `#D97A3A`, CHG-068) + WCAG 2.1 AA + evergreen are owner-ratified → build to
   them. Type scale/fonts/logo/redlines/microcopy are **designer-pending (OPEN_TBD E4)** → use a
   sensible MUI default type scale + the UX-spec copy as placeholder; **do not invent** final
   brand; leave a clean theme seam.
8. **Stack frozen — NO new framework.** Reuse the scaffold. **E2E = Playwright** (add as a dev
   dep — the one approved test-tooling addition); component tests = **Vitest**. Orval drift gate
   (tsc) stays; gate-6 `npm audit` stays. Any other new dependency ⇒ STOP/escalate.
9. **Observability:** emit OBS-WE events (`Disclosure Rendered`, `Notification Raised`,
   `Acceptance-Impact surfaced`, `Export produced`; platform read/dismiss non-canonical);
   what-was-shown reconstructable from the governed source + the CHR version presented.
10. **OSLO Chat** (DL-047, Wave I contract) is a Disclose-class surface: consumes/triggers
    cognition; **writes no canonical, mutates no artifact, changes no assessment** (Critical
    negative). DL-048 **honest-limit disclosure** (partial shown truthfully; upgrade prompt
    alongside, never instead of).
11. **No migration** (Wave E presents existing canonical data; adds none). If a surface seems to
    need a schema change ⇒ STOP/escalate.

## Packages / refactors

- **Approved new dev deps (test tooling only):** `@playwright/test` (E2E), `vitest` +
  `@testing-library/react` (component). **No new runtime dependency** beyond the frozen scaffold.
- Backend DTM-0018 adds the `api/v1` routers + `services/render` mappers (additive; the routers
  catalog already anticipates them) — no change to cognition/orchestration/migrations.

## Open items / residuals (minor — none blocking)

- **GATE — Wave E coding is BLOCKED on:** the **Wave E owner authorization** (DL-044) + readiness
  gate; ideally **Wave U (#69) merged** first (Wave E presents plan facts + acceptance-impact).
  **These files are planning only; no worker is spawned until the owner authorizes Wave E.**
- Designer-pending visual details (E4) — locked #7 (palette/AA/evergreen build; redlines deferred).
- Exact REST endpoint set/DTO shapes — DTM-0018 binds them to the API Contract Spec + Data Model
  v1.2 (the UI_SCREEN_INVENTORY lists the operations each screen needs).
- This branch is stacked on the A–U work; it syncs onto `main` as the upstream waves merge.

## Slice index

| Task | Scope | File |
|---|---|---|
| DTM-0018 | REST exposure — `api/v1` routers + `services/render` DTOs (read-mostly) + Orval regen | `deep-task-0018.md` |
| DTM-0019 | App shell + design system — router, MUI theme (Intralign), epistemic-safety label, query client | `deep-task-0019.md` |
| DTM-0020 | **MRI** (umbrella + MRI-04…07) — the lead/representative surface | `deep-task-0020.md` |
| DTM-0021… | Finding Panel · Recommendation Panel (RP-C1) · Issue Cards · Project Overview · Companion · Notification/Awareness · History/Timeline · Export · OSLO Chat + Assisted Editing | authored after DTM-0018 |
