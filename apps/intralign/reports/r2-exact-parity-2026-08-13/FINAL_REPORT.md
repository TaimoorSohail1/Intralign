# R2 Slices 1-3 exact-prototype parity report

Date: 2026-08-13

## Outcome

All UI defects raised in the final parity review are fixed and verified in the approved in-app browser. The requested R2 states have no remaining P0, P1, or P2 visual or interaction gap. The application continues to render truthful live project data, so issue names, counts, recommendation copy, and analysis events are intentionally not replaced with the prototype's DevNorth fixtures.

## Fixed gap list

| Requested gap | Final status | Evidence |
| --- | --- | --- |
| Onboarding bottom controls missing | **FIXED** | First run, Returning / Watch-it-work, ~60s, 15s, Gates, fast, and Restart are present in the embedded production animation. |
| First grounding act did not create the prototype focus state | **FIXED** | Background blur/dim, recorded outcome, one-call-down lock, Start here prompt, inline issue card, and collapsed OSLO rail match the prototype state. |
| Resolved and OSLO Proposes would not reopen | **FIXED** | Both controls transition `aria-expanded` true → false → true; their bodies transition `aria-hidden` false → true → false and return to `display: block`. |
| Quick Tour and Feedback were outside the sidebar | **FIXED** | Both controls are in the sidebar footer; both open functional, named dialogs and close normally. |
| Issue click opened a modal and shifted the page | **FIXED** | Clicking an issue creates one inline `Issue details` region and zero dialogs. Closing it preserves `window.scrollY` exactly. |
| OSLO advisor disappeared while reviewing an issue | **FIXED** | The governed OSLO rail remains adjacent to the inline issue in the normal workspace and intentionally collapses only in first-run focus. |
| Existing-client analysis animation differed from the prototype | **FIXED** | The source-derived kinetic scene, two-circle motion, right-side reading feed, Replay intro, and bottom controls match the Returning / Watch-it-work prototype. |
| Header pillar colors were missing | **FIXED** | Viability, Grounding, and Adaptability use the prototype blue, green, and magenta states in the compact masthead. |
| Windows guardrail could fail while decoding Vitest output | **FIXED** | The guard now reads subprocess output as UTF-8 with replacement-safe diagnostics. |

## Side-by-side evidence

Each combined image labels the R2 prototype on the left and the application on the right.

- `screenshots/comparison-returning-animation.png`
- `screenshots/comparison-first-run-focus.png`
- `screenshots/comparison-workspace-open.png`
- `screenshots/comparison-inline-issue.png`

## Functional evidence

- Quick Tour: opens the six-step guided dialog; Skip closes it.
- Feedback: opens a named feedback dialog; close works.
- Resolved: closes and reopens without losing its state contract.
- OSLO Proposes: closes and reopens without losing proposal rows.
- Issue open: inline region, no modal, no scrim, advisor retained.
- Issue close: inline region removed; page scroll position unchanged (`0` before and after in the final run).
- First-run focus: presentation freeze, recorded outcome, lock prompt, inline issue, and collapsed OSLO rail verified.
- Returning-client path: uses the same prototype animation without first-time gating.

## Automated verification

- Web: **24 files / 154 tests passed**.
- API: **323 tests passed** in the final Slices 1-3 regression run.
- R2 guardrails: **4 infrastructure + 17 active tests passed**; 18 active guards, 42 pending, 6/6 prototype corrections.
- ESLint: passed.
- Ruff: passed.
- TypeScript and Next.js production build: passed.
- `git diff --check`: passed.

## Per-slice status

| Slice | What works | Remaining |
| --- | --- | --- |
| Slice 1 — Outcome Integrity | Prototype masthead, colored pillars, workspace notice, ranked queue, inline non-modal issue review, advisor, sidebar actions, and first-run focus. | No requested UI gap. The previously owner-deferred combined spoken screen-reader session remains the only non-visual completion gate. |
| Slice 2 — Issue Lifecycle | Recommendation actions, proposals, Resolved lifecycle tray, advisor continuity, stable expand/collapse, and no-popup issue review. | No requested UI gap. Same shared spoken screen-reader gate remains deferred. |
| Slice 3 — Reanalysis / onboarding | First-client onboarding, source-derived kinetic animation, outcome decision, returning-client watch-it-work flow, upload/reanalysis state, and handoff. | No requested UI gap. Same shared spoken screen-reader gate remains deferred. |

Slices 4-10 remain owner-blocked and were not changed.

## Files changed

- `code/apps/web/public/r2/onboarding-arc.html`
- `code/apps/web/src/app/globals.css`
- `code/apps/web/src/components/analysis/onboarding-arc-parity.test.ts`
- `code/apps/web/src/components/overview/project-overview.tsx`
- `code/apps/web/src/components/overview/project-overview.test.tsx`
- `code/services/api/tests/r2/test_slice_two_ui_contract.py`
- Existing Slices 1-3 live-data extraction/advisor remediation files included in this branch are covered by the 323-test API pass.

final result: passed
