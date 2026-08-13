# Design QA

## 2026-08-13 — R2 workspace-banner alignment

### Source and implementation evidence

- Source visual truth: `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-2885223a-b349-4b9a-ba10-42d65519a01c.png`
- Implementation screenshot: `C:/Users/Hp/Documents/ChatGPT/oslo-knowledge/code/reports/r2-parity-followup-2026-08-13/screenshots/09-workspace-banner-aligned.png`
- Viewport: 1280 × 720 CSS pixels; browser capture density unchanged.
- State: desktop Issues overview, OSLO rail closed so the shared 820px issue column is visible.

### Comparison and findings

- Full-view comparison found the banner width was correct but its automatic horizontal margins centered it in a 900px parent, shifting it 40px right of the issue, proposal, and resolved cards.
- Focused bounding-box verification after the fix measured the workspace banner, first issue, proposals, and resolved tray at the identical left edge (`x = 318`) and identical width (`820px`).
- Typography, colors, radii, shadows, icons, and copy were unchanged because the requested defect was alignment-only.
- No remaining P0, P1, or P2 finding exists for this focused correction.

### Iteration history

- P2: workspace banner shifted 40px right in the wide desktop layout.
- Fix: removed automatic horizontal centering and anchored the banner to the shared content-column start.
- Post-fix evidence: `09-workspace-banner-aligned.png` and live equal-edge measurements above.

final result: passed

## 2026-08-12 — R2 Slice 3 implementation review

### Current result

**The production first-read journey, kinetic animation, outcome confirmation, Overview landing, issue action, freshness/reanalysis feedback, queue refresh, responsive layout, and matched-state prototype comparison pass in the approved in-app browser. One live-state defect was found and fixed at `6dfdebe`: queued issue actions now expose the stale-read banner and Undo control immediately.**

final result: partial pass

### Implemented Slice 3 surfaces

- The former simplified canvas approximation has been removed. The shipped first-analysis screen now runs the prototype's actual `onboarding-arc-prototype.html` kinetic graph engine, narration sequence, pillar illumination, outcome decision card, refine/defer states, and acknowledgment motion.
- Production-only adapters bind that source to real run-event progress, the real project title/outcome, honest 45/60-second messages, secure same-origin messaging, outcome persistence, save failure/retry, responsive layout, reduced motion, dialog naming, and focus entry.
- Overview freshness states for STALE, reanalyzing, fresh, Reanalyze now, pending Undo, last-good preservation, and causal read-moved feedback.
- Presentation-only first-run freeze and a durable, latched two-grounding-act unlock.

### Automated evidence

- Focused Slice 3 parity/flow: 2 files / 10 passed, including exact `buildGraph` and animation-loop source comparison, every visible narration/decision state, live event synchronization, confirm/refine/defer, persistence failure, and cross-origin rejection.
- API: 303 passed.
- Web: 24 files / 138 passed.
- R2 guardrails: 4 infrastructure tests passed; the active runner passed 9 tests across 6 active guard IDs, with all 6 prototype corrections present.
- Ruff and ESLint: passed.
- TypeScript and Next.js production build: passed.
- Shipped animation asset: JavaScript syntax check passed; production HTTP returned 200 with `text/html; charset=UTF-8`; API health returned 200/ready.
- Local Slice 3 database migration: applied successfully.

### Live manual and visual evidence

- Ran the real sample-plan intake through the first analysis, watched the graph reveal and pillar animation, confirmed the inferred outcome, and landed on the real Overview.
- Opened an issue, submitted a user-owned clarification, observed `Addressed` plus `Saved · Analysis pending`, completed reanalysis, and confirmed that the queue and evidence projection refreshed without breaking navigation or the advisor rail.
- Exercised the recommended action path. The first run exposed a UI synchronization defect: the server queued the change but the top-level stale/Undo state was not projected immediately. The production fix now projects that state from the action response, and focused assertions cover both clarification and recommended-action paths.
- Verified the Undo control is visible and actionable while the run is pending. When analysis had already acquired the change, the server correctly rejected the late withdrawal and the UI announced `The change can no longer be undone.`
- Tested the production Overview at a narrow mobile viewport. The page reflowed without horizontal page overflow and kept the integrity read reachable.
- Opened the signed prototype and production animation in separate approved tabs, captured graph and outcome-decision states, and produced same-run comparison images. The core kinetic engine, card geometry, typography, colors, and controls match; live project/outcome values and animation timing remain truthfully dynamic, and prototype-only developer controls remain intentionally absent from production.
- A fresh direct production run and a fresh direct prototype run had zero reproducible console errors. One earlier `MutationObserver` error existed on the initially claimed browser tab during tooling startup but did not reproduce in either clean tab. The prototype's own anti-jargon debug warning remains source behavior and does not interrupt the flow.

### Evidence files

- `reports/r2-slice-3-qa-2026-08-12/manual-live/01-intake-populated.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/03-graph-reveal.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/06-outcome-decision.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/09-reanalysis-complete.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/10-mobile-overview.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/15-prototype-vs-implementation.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/17-decision-prototype-vs-implementation.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/18-fixed-stale-undo.png`
- `reports/r2-slice-3-qa-2026-08-12/manual-live/19-stale-undo-visible.png`

### Remaining limitation

- The owner-deferred shared spoken screen-reader session for Slices 1–3 remains open because the QA environment cannot capture synthesized screen-reader speech. Failure/retry, Deep supersession, read-moved, origin rejection, reduced-motion, and persistence recovery remain covered by passing automated tests rather than being artificially forced during this visible happy-path session.

### Final outcome-control verification

- A fresh approved-browser run rendered all three production decisions together: `Yes — this is my outcome`, `Close — I’ll refine it`, and `Not sure yet — keep it as OSLO’s inference`.
- **Confirm passed:** the decision entered a disabled saving state, persisted successfully, and landed on Overview with `Your workspace is open`.
- **Refine passed:** the editor opened with the inferred outcome, accepted replacement text, exposed Save and Cancel, and Cancel returned to the original decision without changing ownership.
- **Keep as inference passed:** the flow preserved the outcome as OSLO’s inference and landed on the usable Overview without falsely claiming user confirmation.
- Visible evidence: `reports/r2-slice-3-button-qa-2026-08-12/01-decision-controls.jpg` through `04-confirmed-overview.jpg`.

## 2026-08-12 — R2 Slice 1 manual completion audit

### Final result

**Passed every browser-executable remaining gate; spoken screen-reader output remains unverified because no screen reader is installed in the QA environment.**

final result: partial pass

### Manual evidence

- Forced timeout preserved the last successful issue queue and integrity read, did not publish an incomplete result, and exposed a clear retry action.
- Retry displayed an in-progress state and completed successfully; the run returned to `completed` / `extended_transition` without losing the last-good read.
- A 200%-zoom-equivalent 482 CSS-pixel viewport had no horizontal overflow, preserved all three issues, and exposed the mobile OSLO entry point.
- With the real operating-system reduced-motion preference enabled, the browser reported `prefers-reduced-motion: reduce`; transitions collapsed to effectively zero and no animated spinner remained. The operating-system preference was restored after the check.
- The issue disclosure exposes a labeled non-modal `dialog`, `aria-controls`, `aria-expanded`, a polite advisor live region, named landmarks, initial focus on Close, Escape-to-close, and focus restoration to the originating issue row.
- Browser console: 0 errors. Five repeated Next.js image-development warnings remain and do not affect the Slice 1 flow.

### Evidence files

- `reports/r2-slice-1-qa-2026-08-12/manual-completion/02-timeout-last-good.png`
- `reports/r2-slice-1-qa-2026-08-12/manual-completion/03-retry-running.png`
- `reports/r2-slice-1-qa-2026-08-12/manual-completion/04-retry-complete.png`
- `reports/r2-slice-1-qa-2026-08-12/manual-completion/05-zoom-200-equivalent.png`
- `reports/r2-slice-1-qa-2026-08-12/manual-completion/06-reduced-motion.png`
- `reports/r2-slice-1-qa-2026-08-12/manual-completion/07-screen-reader-dialog.png`

### Remaining limitation

- NVDA is not installed, and synthesized screen-reader speech cannot be captured or asserted through the in-app browser. Accessibility-tree, landmark, live-region, keyboard, dialog, Escape, and focus-return behavior pass, but the ledger conservatively keeps the real spoken assistive-technology session open.

## 2026-08-12 — R2 Slice 1 queue and inline-issue parity correction

### Final result

**Passed for the implemented Slice 1 header, workspace-open notice, exposure-ranked queue, inline issue read, and persistent OSLO advisor.**

## R2 Slices 1-3 exact-prototype remediation — 13 August 2026

The final approved-browser pass closes every UI defect raised for onboarding controls, first-grounding-act focus, lifecycle tray reopening, sidebar actions, inline issue review, returning-client analysis motion, and compact masthead pillar colors.

### Combined evidence

- `code/reports/r2-exact-parity-2026-08-13/screenshots/comparison-returning-animation.png`
- `code/reports/r2-exact-parity-2026-08-13/screenshots/comparison-first-run-focus.png`
- `code/reports/r2-exact-parity-2026-08-13/screenshots/comparison-workspace-open.png`
- `code/reports/r2-exact-parity-2026-08-13/screenshots/comparison-inline-issue.png`

### Browser evidence

- Quick Tour and Feedback are inside the sidebar and open functional named dialogs.
- Resolved and OSLO Proposes close and reopen with correct `aria-expanded`, `aria-hidden`, and display state.
- Issue click creates an inline `Issue details` region with zero dialogs; close removes it without changing `window.scrollY`.
- First-run focus shows the recorded outcome, one-call-down lock, Start here prompt, inline issue, background blur, and collapsed OSLO rail.
- Returning-client analysis uses the prototype-derived two-circle kinetic scene, reading feed, Replay intro, and bottom controls without the first-time gate.
- Viability, Grounding, and Adaptability use their prototype blue, green, and magenta masthead states.

### Regression evidence

- Web: 24 files / 154 tests passed.
- API: 323 tests passed.
- R2 guardrails: 4 infrastructure and 17 active tests passed; 6/6 prototype corrections.
- ESLint, Ruff, TypeScript, Next.js production build, and diff check passed.

No actionable P0, P1, or P2 mismatch remains. Live issue names, counts, and analysis events remain backend-driven instead of being replaced by prototype fixtures.

final result: passed

## R2 sidebar, returning-client, and banner-reflow parity — 13 August 2026

- Sidebar utility controls are contained inside the sidebar at the audited 1280 × 720 viewport.
- Existing clients carry an explicit returning state through intake and land in the prototype watch-it-work analysis path.
- First/Returning playback controls synchronize their active state on initial load and restart.
- Dismissing the workspace-open notice removes it from layout; the worklist advances by the full former banner height with no retained blank slot.
- The root first-run shell continues to apply the prototype blur/focus state when `freeze_on` is active.
- The combined source/application comparison is stored at `reports/r2-parity-followup-2026-08-13/screenshots/prototype-vs-app-side-by-side.png`.
- Full web tests: 156 passed; focused follow-up tests: 71 passed.
- R2 guardrails: 4 infrastructure tests and 17 active tests passed.
- ESLint: passed.
- TypeScript and Next.js production build: passed.

final result: passed

### Source and implementation evidence

- Source: the signed R2 prototype Issues queue and expanded issue states in `release-2/oslo-prototype-r2.html`, including the owner-provided reference captures.
- Implementation: `http://127.0.0.1:3002/projects/cb25ee1c-82ed-407f-a46c-b591088fbdc6/overview` at a 1600 × 900 viewport.
- Queue comparison: `reports/r2-slice-1-qa-2026-08-12/inline-issue-pass/queue-comparison.png` physically combines the prototype and corrected implementation.
- Expanded issue comparison: `reports/r2-slice-1-qa-2026-08-12/inline-issue-pass/inline-comparison.png` physically combines the prototype and corrected implementation.

### Findings and corrections

- P1 header drift fixed: added the R2 prototype masthead, OFFICIAL treatment, SAMPLE badge, compact Outcome Integrity state, and aligned 86px content start.
- P1 queue hierarchy fixed: added the prototype workspace-open notice and preserved the ranked queue, first-action emphasis, pillar/severity pills, and persistent advisor rail.
- P1 interaction drift fixed: an issue now expands inline at its ranked position instead of replacing the queue; the other issue rows remain visible.
- P2 detail hierarchy fixed: the inline read now includes the prototype's title/pillar/severity treatment, issue summary, Affects/Holds up context, first-time guide, recommendation, evidence, why-it-matters, weakening, and possible resolution paths.
- The inline read is a non-modal dialog with `aria-controls`/`aria-expanded`, Escape-to-close, and focus restoration to its issue row.
- No actionable P0, P1, or P2 mismatch remains in Slice 1. Dynamic project names, issue counts/copy, integrity values, and advisor text remain truthful live data rather than copied DevNorth fixtures.
- OSLO Proposes and Resolved are intentionally excluded because the signed slice documentation assigns them to Slice 2, not Slice 1.

### Verification

- In-app browser: queue, inline opening/closing, keyboard focus restoration, persistent advisor, pillar navigation, desktop layout, and no horizontal document overflow passed.
- Focused Overview suite: 38 passed.
- Full web suite: 23 files / 128 passed.
- Slice 1 API contract suite: 19 passed earlier in the same run; no API code changed in this correction.
- R2 guardrails: 4 infrastructure tests and 9 active selectors passed earlier in the same run; no guard mapping changed.
- ESLint: passed.
- TypeScript and Next.js production build: passed.


## 2026-08-12 — R2 Slice 1 bounded-shell correction

### Final result

**Passed for the implemented Slice 1 shell, live work queue, and governed advisor scope.**

final result: passed

### Source and implementation evidence

- Source: the activated R2 Slice 1 Issues state in `release-2/oslo-prototype-r2.html`.
- Implementation: `http://127.0.0.1:3002/projects/cb25ee1c-82ed-407f-a46c-b591088fbdc6/overview`.
- Exact-size comparison: `reports/r2-slice-1-qa-2026-08-12/exact-shell-pass/03-prototype-vs-implementation-1600x900.png` physically combines the source and implementation at the same 1600 × 900 CSS-pixel viewport.
- Responsive evidence: `reports/r2-slice-1-qa-2026-08-12/exact-shell-pass/04-implementation-375x812.png` and `05-implementation-mobile-queue.png`.

### Findings and fixes

- P1 layout drift fixed: the production workspace was unconstrained while the prototype is bounded to 1600px. The Slice 1 shell now uses the same maximum width and stays centered on wider displays.
- P1 hierarchy drift fixed: the 198px Outcome Integrity read was permanently expanded. Desktop now starts in the prototype's compact 52px masthead + 34px Outcome anchor state, with an accessible expand/collapse control for the full read.
- P1 density drift fixed: the central reading body is capped at 900px and issue rows at 820px, matching the prototype instead of stretching across the available center column.
- P2 responsive clipping fixed: the narrow-screen grid now uses `minmax(0, 1fr)` and zero minimum widths, keeping the full issue queue usable without page-level horizontal overflow.
- The prototype's developer annotation strip and transient sample-only notices are not production UI. Project name, issue count/copy, integrity values, and advisor copy remain truthful live data rather than copied DevNorth fixtures.
- Final comparison found no remaining actionable P0, P1, or P2 mismatch in the implemented Slice 1 scope.

### Functional and accessibility verification

- Compact Outcome Integrity expands and collapses with correct `aria-expanded`, accessible labels, and visible full-summary state.
- The top-ranked issue opens the governed issue detail and closes back to the unchanged queue.
- The advisor's suggested prompt returns a grounded next-step response from the existing API.
- Outcome navigation opens the live Intent artifact and browser Back returns to Overview.
- The mobile work queue remains reachable and readable in the narrow layout; the document has no horizontal page overflow.
- Browser console errors: 0. One existing Next.js image aspect-ratio development warning remains outside this Slice 1 shell change.

### Automated evidence

- Focused Overview component suite: 37 passed
- Full web suite: 23 files / 127 passed
- Slice 1 API integrity and UI-contract tests: 19 passed
- R2 guardrails: 4 infrastructure tests and 9 active selectors passed; 60 registered / 6 active / 54 pending
- ESLint: passed
- TypeScript and Next.js production build: passed
- `git diff --check`: passed

## 2026-08-12 — R2 Slice 1 exact-prototype parity pass

### Final result

**Passed for the implemented Slice 1 UI scope after an exact-size source/target comparison and live functional regression.**

final result: passed

### Source and implementation evidence

- Source: the unlocked, expanded **Issues** state in `release-2/oslo-prototype-r2.html`.
- Implementation: the seeded project Overview at `http://127.0.0.1:3002/projects/cb25ee1c-82ed-407f-a46c-b591088fbdc6/overview`.
- Comparison: source and implementation were captured into one side-by-side image in the Codex in-app browser at the same **1280 × 720 CSS-pixel viewport**.
- Measured structure: production shell begins at `y=284` after excluding the prototype-only 33px banner; left rail is `265px`; advisor rail is `330px`; the three-pillar group begins at `x≈616`, matching the prototype at `x=617`.

### Visual findings

- The real Intralign source logo, project switcher, current-surface breadcrumb, grounded Outcome anchor, expanded Outcome Integrity masthead, five-band maturity rail, three pillar cards, weakest-pillar treatment, Views/Documents taxonomy, exposure-ranked work queue, and persistent OSLO advisor follow the R2 prototype hierarchy and styling.
- The queue exposes every server-ranked issue; the first issue carries the orange “Do this next” treatment and each row retains pillar, severity, rationale, rank, and affordance.
- The OSLO rail now exposes the prototype hierarchy using governed live data: session context, Reasoning, Reliability basis, Your next move, prompts, and composer.
- No actionable P0, P1, or P2 mismatch remains inside Slice 1. Accepted dynamic differences are the project name, pillar readings, issue copy/count, and advisor copy because the implementation renders the real seeded project while the prototype renders its fixed DevNorth fixture.
- The prototype-only explanatory banner and fixed sample-only notices are intentionally not shipped. The implementation does not fabricate the prototype's ten issues or moved-read notice when the live snapshot truthfully contains three open issues and no moved-read event.

### Interaction and accessibility findings

- The top-ranked issue opens a working governed issue detail beside OSLO; closing it returns to the ranked queue.
- Selecting the Adaptability pillar opens the related highest-exposure issue.
- The Outcome anchor navigates to the live Intent artifact and browser Back returns to the same Overview.
- A live advisor prompt returned the grounded next-step response from the existing advisor API.
- Viability detail expands into a visible, readable region rather than leaving a hidden control target.
- Desktop regions retain independent scroll ownership. At a 375px mobile viewport, document scroll width remained 375px with no horizontal page overflow.
- Regions and controls expose names for the brand, outcome, Outcome Integrity, exposure-ranked queue, issue details, and advisor actions. Live-browser console errors: 0.

### Automated evidence

- Focused Overview component suite: 36 passed
- Full web suite: 23 files / 126 passed
- Slice 1 API contract and integrity tests: 19 passed
- R2 guardrails: 4 infrastructure tests and 9 active selectors passed; 60 registered / 6 active / 54 pending
- ESLint: passed with zero warnings
- TypeScript and Next.js production build: passed
- `git diff --check`: passed

## Prototype 10 design QA

## Final result

**Passed**

final result: passed

## 2026-08-05 - Seven-document analysis and owner-only access

This pass supersedes the role model described in the preceding Settings QA section. Workspace membership and invitations are now owner-only; external review remains a separate, read-only workflow.

### Source and implementation evidence

- Source: `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-28df2da2-f39d-4a46-b019-31a09d76ff62.png`
- Final implementation: `C:/Users/Hp/Downloads/oslo-app/design-qa-analysis-owner-only-final.png`
- Final side-by-side comparison: `C:/Users/Hp/Downloads/oslo-app/design-qa-analysis-comparison-final.png`
- Comparison viewport: 1011 x 773, constructing-documents state, seven documents completed

### Visual verification

- Typography, spacing, layout, scanner treatment, stage pill, progress dots, trace rows, and colors match the supplied prototype at the target viewport.
- The timing pill intentionally uses truthful runtime wording instead of promising a fixed 30-second duration.
- No raster image assets are used by this state; the scanner uses the product's existing CSS treatment.
- The progress region remains announced through its accessible live status, and reduced-motion handling is retained.
- Pass 1 found P2 spacing, typography, and trace-width differences; the implementation was adjusted to the prototype tokens.
- Pass 2 found a P2 vertical-position difference caused by a collapsed trace region; a stable trace height fixed it.
- Final comparison found no remaining P0, P1, or P2 mismatch.

### Functional verification

- Analysis explicitly constructs and reports all seven documents.
- Admin invitations no longer expose a role selector and every invitation is an Owner invitation.
- The project Share dialog no longer exposes Collaborator or Viewer membership controls.
- API requests reject injected role fields; existing memberships and invitations are migrated to Owner.
- Seat counting and authorization now follow the owner-only membership model.
- External reviewer links remain separate from workspace membership and do not grant an application role.

### Automated evidence

- Analysis progress component tests: 2 passed
- Affected web component tests: 26 passed
- Full web suite: 112 passed
- Invitation API/domain tests: 26 passed
- Full API suite: passed
- ESLint, Ruff, TypeScript, and production build: passed
- Owner-only database migration applied successfully to the local stack

final result: passed

## Guided tour, usage limits, Inference Map, and Reports parity — 4 August 2026

The four reported Prototype 10 mismatches are corrected and verified in the live application.

### Verified behavior

- **Quick tour:** opens directly into a six-step walkthrough with Step 1–6 labels, Skip, Back, Next, and Done. Each step uses a distinct anchored position and the prototype wording hierarchy.
- **Your plan:** opens Usage & limits with monthly-analysis, refresh, project, collaborator, document, and never-limited rows instead of the plan comparison screen.
- **Inference Map:** claim marks and exact totals have separate layout columns. All seven rows measured a 12px gap and zero overlap.
- **Reports:** Send and Export remain visible and unclipped at 1365px and 960px widths. Send uses the retained-readout explanation and Change recipient path; Export opens the PDF/memo panel.
- **Console:** zero browser errors during route and interaction QA.

### Comparison evidence

- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/compare-tour.png`
- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/compare-usage.png`
- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/compare-inference.png`
- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/compare-send.png`
- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/compare-export.png`
- `C:/Users/Hp/Downloads/oslo-app/output/prototype-parity-pass/report-narrow.png`

### Automated evidence

- Focused component tests: 54 passed
- Full suite: 109 passed in the parallel run; three 5-second worker timeouts passed when rerun in isolation (112/112 functional assertions green)
- ESLint for changed components: passed
- Next.js production build and TypeScript: passed

final result: passed

## Sidebar footer parity QA — 4 August 2026

The persistent project controls now follow the Prototype 10 order at the bottom of the left navigation: **Take a quick tour → plan summary → account**. The account menu opens upward so it remains visible above the fixed footer.

### Source and implementation evidence

- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-bee9443b-6542-4b95-8aa5-bfd6914e7936.png` — Prototype 10 footer
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-fe730f63-3b9f-4866-8dbf-a96c82fe8602.png` — Prototype 10 upward account menu
- `C:/Users/Hp/Downloads/oslo-app/output/sidebar-footer/sidebar-footer-desktop-clean.png` — verified implementation
- `C:/Users/Hp/Downloads/oslo-app/output/sidebar-footer/sidebar-footer-comparison-clean.png` — focused side-by-side comparison

### Verified behavior

- The three controls stay pinned to the sidebar bottom while the navigation remains independently scrollable.
- The plan summary opens the plan comparison dialog.
- The quick-tour control opens the orientation flow.
- The account menu opens above the account row and exposes account, settings, replay, and logout actions.
- Live workspace data is retained, so the implementation may show a different account name or project count from the static prototype.
- Browser console errors: `0`.
- Focused regression tests: `39 passed`.
- ESLint, TypeScript, and the Next.js production build: passed.
- The full web suite has one unrelated existing failure in `history-workspace.test.tsx`; the sidebar-focused suites are green.

final result: passed

The implemented Export, Share, Notifications, plan-comparison, and OSLO advisor surfaces match the supplied Prototype 10 visual language and interaction hierarchy. No actionable P0, P1, or P2 visual mismatch remains.

## Independent scroll-region QA — 4 August 2026

The project console now uses separate scroll owners for the left navigation, the central project content, and the OSLO conversation. The browser page itself remains fixed, so scrolling one region does not move either of the others.

### Scroll-layout source of truth

- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-3f9c10f6-1b50-483c-964f-55f9f14f9031.png` — previous application layout
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-7ad855ee-6401-4f56-a489-b2d4541f10f0.png` — Prototype 10 independent-scroll layout

### Scroll-layout implementation evidence

- `C:/Users/Hp/Downloads/oslo-app/output/scroll-layout/reports-independent-scroll-1365x600.png` — compact desktop; navigation and content overflow independently
- `C:/Users/Hp/Downloads/oslo-app/output/scroll-layout/reports-independent-scroll-1365x768.png` — standard desktop
- `C:/Users/Hp/Downloads/oslo-app/output/scroll-layout/reports-independent-scroll-1912x1024.png` — large desktop; content remains independently scrollable while the navigation fits
- `C:/Users/Hp/Downloads/oslo-app/output/scroll-layout/prototype10-vs-independent-scroll.png` — side-by-side Prototype 10 comparison

### Measured behavior

- At 1365 × 600, the central region had `518px` visible height and `2718px` scroll height; the navigation had `528px` visible height and `694px` scroll height.
- A wheel action over the central region changed only its scroll position from `0` to `420`.
- A wheel action over the navigation then changed only its scroll position from `0` to `166`; central content stayed at `420`.
- The browser remained at `scrollY = 0` throughout and `document.scrollHeight` always equalled the viewport height.
- The OSLO conversation owns `overflow-y: auto`; its scrollbar appears only when conversation content exceeds the available height.
- At 1912 × 1024, navigation content fits without a redundant scrollbar while the long central report remains independently scrollable.
- Browser console warnings and errors: `0`.

### Scroll-layout findings

No remaining P0, P1, or P2 mismatch was found for scroll ownership. Short desktop layouts expose the additional navigation scrollbar only when required. Large desktop layouts keep the two long-content regions independently scrollable, matching the Prototype 10 behavior.

## Visual source of truth

- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-45eca556-b336-47db-b6f1-51fa7e874137.png` — Export, upper state
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-53c48407-33ec-48ff-854c-af3ecd5b7c09.png` — Export, lower state
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-c8d0ea89-298d-4cf4-b307-96877b594ec8.png` — Share, upper state
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-208a1c9a-a256-454b-bae1-0db39ae5de82.png` — Share, lower state
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-a4ec2854-e15e-4331-bded-a4a48e59323d.png` — Notifications
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-f9f3e641-0cab-448f-a6df-ee3b78e2baa8.png` — Advisor composer
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-5ab2c3e7-c429-463d-a51e-146834d33640.png` — Plan comparison, upper state
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-1fc4612f-2ccc-4ef9-bf7a-993b4b7ab3d9.png` — Plan comparison, lower state

## Implementation evidence

- `C:/Users/Hp/Downloads/oslo-app/output/ui-parity/export-after.png`
- `C:/Users/Hp/Downloads/oslo-app/output/ui-parity/share-after.png`
- `C:/Users/Hp/Downloads/oslo-app/output/ui-parity/notifications-after.png`
- `C:/Users/Hp/Downloads/oslo-app/output/ui-parity/plan-after.png`
- `C:/Users/Hp/Downloads/oslo-app/output/ui-parity/prototype10-comparison.png`

## Comparison setup

- Theme: dark
- Desktop implementation viewport: 1264 × 712 CSS pixels
- Mobile verification viewport: 390 × 844 CSS pixels
- Comparison method: full modal/drawer state followed by focused region comparison for headers, tier notices, audience controls, document body, format cards, participant rows, notification entries, plan cards, sticky footers, and advisor controls.

## Findings and iteration history

The initial application used a small export panel, enterprise-style sharing cards, a sparse plan modal, large notification cards, and a one-line advisor input. These were replaced with the Prototype 10 information hierarchy, sizing, borders, typography, spacing, tier messaging, scroll regions, and sticky footer behavior.

Accepted dynamic differences:

- Project name, confidence, reliability, issue counts, participants, and notification content come from live project data instead of prototype fixtures.
- Owner-only invitation controls are hidden for a collaborator account; the owner path remains implemented and unit tested.
- Basic-only export formats remain visibly gated. PDF is functional; frozen Export Link is clearly unavailable rather than simulated.

Residual P3 observation:

- Export waits for live overview and collaboration requests before showing project-specific content. This preserves correctness, but the perceived delay depends on the local API response time.

## Interaction and responsive QA

- Export opens and closes correctly.
- Switching the recipient to Programme lead updates only section 4 of the readout.
- Share opens with live seat, role, participant, and link information.
- Plan comparison displays Free, Basic, and the future plan ladder.
- Notifications opens with unread state and Mark all read.
- Advisor displays all five suggested questions and the expanded composer.
- Mobile viewport has no horizontal page overflow; the Export dialog stays fully within the viewport.
- Browser console errors after route and interaction testing: 0.

## Automated evidence

- Web unit/component tests: 111 passed
- ESLint: passed
- TypeScript: passed
- Next.js production build: passed
- `git diff --check`: passed

## Prototype 10 Settings parity QA — 4 August 2026

Settings now follows the Prototype 10 navigation and content model for Access & Invites, Membership, Subscription, Billing, and Integrations while retaining live workspace values.

### Source and implementation evidence

- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-4f380dda-df3e-4b16-992d-ad3268518c20.png` — Access & Invites source
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-52967879-31c4-4f19-a4f9-08f4cd3fdfd1.png` and `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-c30a627d-0c9f-441b-b4d0-8ad490f55383.png` — Membership and Subscription sources
- `C:/Users/Hp/AppData/Local/Temp/codex-clipboard-cc543daa-bef6-49ec-848a-70be128f65e2.png` — Billing and Integrations source
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/access-implementation-final.png`
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/subscription-implementation-final.png`
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/later-sections-implementation.png`
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/plan-dialog-from-settings.png`
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/access-comparison.png` — combined source and implementation comparison
- `C:/Users/Hp/Downloads/oslo-app/output/settings-parity/subscription-comparison.png` — combined source and implementation comparison

### Verified behavior

- Access & Invites is present and exposes GA/tier-based allocation language.
- Workspace owners can follow Manage invitations to the working invitation screen, choose owner, collaborator, or viewer, and send an invitation. No external invitation was sent during QA.
- Membership and Subscription use live project, member, collaborator-seat, and analysis counts.
- The plan comparison opens from Free vs Basic and retains the existing functional plan preview.
- Billing is explicitly marked as a stub and Integrations as later; neither exposes a misleading action.
- Invitation expiry is consistently 14 days in the service, screen copy, and tests.
- Desktop navigation active state follows the selected section.
- At 390 × 844, the layout has no horizontal page overflow (`clientWidth = scrollWidth = 375`).
- No remaining P0, P1, or P2 visual mismatch was found. Live values may differ from prototype fixtures by design.

### Automated evidence

- Settings component tests: 5 passed
- Invitation and workspace API tests: 7 passed
- ESLint: passed
- TypeScript and Next.js production build: passed
- `git diff --check`: passed

final result: passed
