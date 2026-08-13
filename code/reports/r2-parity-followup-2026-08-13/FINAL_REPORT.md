# R2 parity follow-up — final report

Date: 2026-08-13
Branch: `codex/release-2-build`

## Result

All four UI defects reported in this follow-up are fixed and verified in the live app.

| Defect | Fix | Browser evidence | Result |
|---|---|---|---|
| Quick Tour, Feedback, plan, and account controls drift outside the sidebar | Split the sidebar into one scrollable content region and one contained, fixed footer region. | At 1280 × 720 the sidebar is `634px` high; its content ends at `y=501` and its footer starts at `y=501`, ends at `y=720`, and is a descendant of the sidebar. | FIXED |
| Existing-client upload enters the first-time guided animation | Established workspaces add `returning=1` through workspace → intake → analysis, and the analysis page selects watch mode from that explicit server-readable state. | Both prototype and app report `Returning · Watch-it-work` active and the watch panel rendered as `display:flex`. | FIXED |
| Returning playback control is not visibly selected | The copied prototype engine now synchronizes the First/Returning active classes every time playback starts or restarts. | Prototype and app both show `d-ret.className = "act"`; all six prototype controls are present. | FIXED |
| Dismissing “Your workspace is open” leaves an empty gap | The dismissed banner is removed from layout instead of kept as a hidden reserved-height element. | Banner height before close: `157.5px`; worklist top moves from `354.97px` to `179.47px`; the banner element is absent after close. | FIXED |

The existing first-run focus layer also remains active: when `first_run.freeze_on` is true, the root shell receives `is-first-run-frozen`, which applies the prototype blur/dim treatment while leaving the focused issue actionable.

## Side-by-side evidence

- [Combined prototype/app comparison](./screenshots/prototype-vs-app-side-by-side.png)
- [Prototype overview reference](./screenshots/prototype-overview-reference.png)
- [App overview with workspace notice](./screenshots/app-overview-banner-open.png)
- [App overview after dismiss and reflow](./screenshots/app-overview-banner-dismissed.png)
- [Prototype returning-client analysis](./screenshots/prototype-returning-watch.png)
- [App returning-client analysis](./screenshots/app-returning-watch.png)

## Regression evidence

- Full web suite: 24 files, 156 tests passed.
- Focused follow-up suite: 4 files, 71 tests passed.
- R2 guardrails: 4 infrastructure tests and 17 active tests passed; 6/6 prototype corrections present.
- ESLint: passed.
- Next.js production build and TypeScript: passed.
- Manual browser: sidebar containment, banner dismiss/reflow, returning route selection, visible playback controls, active Returning state, and prototype/app watch-mode geometry passed.

## Files changed

- `code/apps/web/src/components/overview/project-overview.tsx`
- `code/apps/web/src/app/globals.css`
- `code/apps/web/src/components/workspace/workspace-home.tsx`
- `code/apps/web/src/app/intake/page.tsx`
- `code/apps/web/src/components/intake/intake-experience.tsx`
- `code/apps/web/src/app/projects/[projectId]/analysis/[runId]/page.tsx`
- `code/apps/web/public/r2/onboarding-arc.html`
- Related tests in the Overview, workspace, intake, and onboarding parity suites.

## Remaining

No UI defect listed in this follow-up remains open. Broader real-document semantic extraction and evidence-answer quality items already recorded in the release ledger remain separate from this visual parity pass.
