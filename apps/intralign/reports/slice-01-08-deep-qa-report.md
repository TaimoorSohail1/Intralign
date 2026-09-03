# OSLO Product Grill — Slice 1–8 Deep QA Report

**Date:** 26 July 2026  
**Branch tested:** `feature/slice-8`  
**Overall health:** Green — release-candidate quality for the implemented Slice 1–8 scope.

## Executive result

The complete implemented journey from workspace access through governed project awareness was tested across the web application, API, database-backed flows, and live browser routes. No actionable P0, P1, or P2 defects remain.

- Web tests: **61/61 passed**
- API tests: **130/130 passed**
- ESLint: **passed**
- TypeScript and Next.js production build: **passed**
- Live authenticated route audit: **passed**
- Visual comparison against the Slice 7 and Slice 8 prototypes: **passed**

## Slice-by-slice coverage

| Slice | Tested outcome | Result |
|---|---|---|
| 1 — Access & onboarding | Admin invitations, authentication boundaries, activation/login coverage, returning-user entry, Welcome lifecycle | Passed |
| 2 — Intake & Fast Pass | Intake entry, document-analysis API coverage, provisional/current lifecycle, orientation persistence | Passed |
| 3 — Overview console | Confidence presentation, issues, clarification/re-analysis wiring, advisor interactions, project summary | Passed |
| 4 — Attention Map | Heatmap route, dimension/artifact issue mapping, issue navigation, safe return to Overview | Passed |
| 5 — Artifact workspace | Seven artifact routes, live artifact data, issue links, editing/re-analysis contracts | Passed |
| 6 — Issues & recommendations | Issue grouping/filtering, status presentation, clarification entry, recommendation details | Passed |
| 7 — History & trend | Retained snapshots, current/historical run states, filtering, timeline density and responsive overflow | Passed |
| 8 — Workspace awareness | Workspace Home, project switcher, notifications, settings/preferences, one-active-project governance | Passed |

## Live browser route evidence

The following authenticated routes loaded without application errors:

1. `/admin/invitations`
2. `/welcome` — correctly redirects a returning user with an active project to `/workspace`
3. `/workspace`
4. `/settings`
5. `/projects/{project_id}/overview`
6. `/projects/{project_id}/issues`
7. `/projects/{project_id}/history`
8. `/projects/{project_id}/attention`
9. `/projects/{project_id}/artifacts/intent`
10. `/projects/{project_id}/artifacts/requirements`
11. `/projects/{project_id}/artifacts/resources`

Interactive Slice 8 checks also passed:

- Project switcher opens, searches, and bounds large workspaces.
- Notification panel opens, marks all read, and never starts analysis.
- Dark, Light, and System appearance controls apply and persist.
- Analysis notification preference persists after reload.
- Project-limit prompt explains the constraint and displays bounded archive choices.

## Defects found and fixed

### 1. Welcome could bypass Slice 8 project governance

**Observed:** A returning user with an active project could open the old Welcome page and click “Start first project,” producing a project-limit conflict.

**Fix:** Returning users now redirect to Workspace Home. If a concurrent request still reaches the limit, the action redirects into the governed project-limit prompt instead of surfacing an exception.

**Regression evidence:** Welcome action and page tests pass.

### 2. Legacy over-limit workspaces attempted creation too early

**Observed:** The local database contains legacy test projects created before the one-active-project cap. Archiving one project could still leave the workspace above the cap, but the UI immediately attempted project creation.

**Fix:** The capacity dialog now remains open, states exactly how many additional projects must be archived, and avoids the create request until capacity is genuinely available.

**Regression evidence:** Workspace Home legacy-capacity test passes.

## Visual QA evidence

- Workspace Home: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice8-workspace.png`
- Settings: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice8-settings.png`
- Overview: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice3-overview.png`
- History: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice7-history.png`
- Detailed comparison log: `C:\Users\Hp\Downloads\oslo-app\design-qa.md`

## Residual, non-blocking notes

- The local development database retains **221 legacy active test projects** that predate the Slice 8 cap. The UI now handles this safely; no user data was deleted during QA.
- Vitest logs one harmless jsdom message about navigation to another document; all 61 tests pass.
- Pytest reports three dependency deprecation warnings; these do not affect runtime behavior.
- A destructive live archive operation was intentionally not performed. Archive-and-cap behavior is verified through regression tests.

## Final assessment

The implemented Slice 1–8 scope is internally consistent, visually aligned with the supplied prototypes, and protected by passing regression suites. The two cross-slice lifecycle defects discovered during deep QA were fixed and revalidated. No required flow is currently blocked.
