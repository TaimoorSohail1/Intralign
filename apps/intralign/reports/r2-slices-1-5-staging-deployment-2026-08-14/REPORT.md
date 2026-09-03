# R2 Slices 1–5 staging deployment report

Date: 2026-08-14

Branch: `codex/release-2-build`

Source commit: `857c23b7ed3f2f71654ae0670119a385aae1054a`

Deployed `code/` subtree: `36e28248291440196a532e2dfecabb650b73fb1c`

## Release result

R2 Slices 1–5 passed the release gate and are deployed to the staging environment.

- Web: https://intralign-oslo-web-staging-9f21dcd15274.herokuapp.com/ — Heroku release `v20`
- API: https://intralign-oslo-api-staging-589e061af756.herokuapp.com/ — Heroku release `v36`
- Web dyno: up
- API web dyno: up
- API worker dyno: up
- API health: `ready` / `oslo-api`
- Web login: HTTP `200`; expected OSLO sign-in content rendered
- Unauthenticated web root: HTTP `307` redirect to sign-in, as designed
- Post-release application logs: no new crash, fatal, exception, or traceback signal

## Slice status

| Slice | Scope verified | Result |
|---|---|---|
| 1 — Intake and outcome flow | Sign-in boundary, project/intake journey, document submission, extraction handoff, outcome confirmation and routing | Pass |
| 2 — Staged analysis loader | Analysis phase progression, completed-state handoff, durable API/worker execution and failure-safe transitions | Pass |
| 3 — Overview, issues and workspace | Overview/workspace shell, issues, navigation, responsive layout and OSLO reasoning sidebar behavior | Pass |
| 4 — Integrity, grounding and actions | Viability/Grounding/Adaptability integrity surfaces, evidence/provenance, issue detail and governed actions | Pass |
| 5 — Seven plan artifacts | Intent, Scope, Requirements, Constraints, Work Breakdown, Schedule and Resources; real data, uniqueness and artifact actions | Pass |

## Verification evidence

All exhaustive tests below ran against the exact source used to create the deployed subtree.

| Gate | Result |
|---|---|
| Frontend unit/integration tests | 27 files, 189/189 passed |
| Backend tests | 364/364 passed |
| Document ingestion focused regression | 6/6 passed |
| R2 infrastructure guardrails | 4/4 passed |
| Active R2 runner tests | 21/21 passed |
| R2 registry audit | 60 registered, 22 active, 38 pending, 58 mapped surfaces, 6/6 prototype corrections |
| Slice 5 desktop/mobile Playwright tracer | 4/4 passed |
| Frontend production build and TypeScript | Passed |
| ESLint | Passed |
| Ruff | Passed |
| Git whitespace check | Passed |

The Slice 5 tracer visited all seven artifact routes at desktop and mobile sizes. It checked route content, cross-section uniqueness, horizontal overflow, the Intent view toggle, Scope edit/undo, Work Breakdown outline/backlog switching, and responsive behavior.

## Corrections included in this release

- Centered the main document workspace to match the R2 prototype shell.
- Corrected the issue-detail disclosure so its card sections expand instead of incorrectly opening the outcome surface.
- Corrected OSLO sidebar open/collapsed geometry and fixed-width behavior.
- Stabilized notification/header positioning so opening notifications does not shift page titles or integrity controls.
- Corrected Slice 5 duplicate-content handling and made resource verification work with real project data instead of one fixture's exact values.
- Updated the desktop/mobile Playwright tracer for required outcome confirmation and analysis-to-overview routing.

## Release conclusion

No release-blocking defect remains in Slices 1–5. The deployed web and API releases are healthy, and the exact deployed code passed the complete local functional, UI, responsive, action, document-ingestion and production-build gate before deployment.
