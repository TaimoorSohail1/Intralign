# R2 slices 1–10 release report

Date: 2026-08-17
Target: Heroku staging

## Scope verified

Five real Atlas project PDFs were analyzed as one client project. The read produced all seven plan artifacts: Intent, Scope, Requirements, Constraints, Work Breakdown, Schedule, and Resources. Issues, Your Outcome, Grounding Map, Reports, History, reviewer evidence, collaboration, snapshots, notifications, Settings, feedback, onboarding, and the OSLO advisor were exercised in the browser.

## Fixes included

- Real files now replace the built-in sample prompt instead of merging DevNorth data into the client read.
- Counts and summaries now agree across the loader, first-run flow, OSLO sidebar, Grounding Map, Reports, snapshots, and History.
- Reviewer evidence remains cumulative; snapshots freeze current state and revoke immediately.
- Report and snapshot titles remain anchored to the current project.
- Same-band analysis movement is described honestly.
- The prototype-aligned centered shell, fixed advisor, radial map, Settings modal, notifications, walkthrough, and support surfaces remain intact.
- Dense Grounding Maps now keep the six-node prototype constellation readable and move additional findings into a linked, responsive detail grid.

## Live staging verification

- API release v37 and web release v21 started successfully; API health returned `ready`.
- Authenticated workspace, Issues, Your Outcome, all seven artifacts, Grounding Map, Reports, History, and the shared header/advisor shell loaded successfully.
- External review creation, attributed confirmation, governed reanalysis, snapshot creation, snapshot revocation, notifications, History, and discussion-only comments passed in the deployed browser flow.
- The saved light theme persisted from Settings onto project routes.
- One live-only dense-map overlap was found, corrected, regression-tested, rebuilt, and included in the final web redeploy.

## Five-user review

The owner, project-manager, external-reviewer, collaborator, and executive-reader journeys passed after the corrections above. No remaining in-scope P0, P1, or P2 issue was found.

## Gates

- Web: 235 tests passed.
- API: 410 tests passed.
- Focused R2 UI: 99 tests passed.
- R2 guardrails: 60 registered / 53 active / 7 pending; 6/6 prototype corrections.
- ESLint, Ruff, TypeScript, and production build: passed.

Release result: passed.
