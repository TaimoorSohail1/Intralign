# R2 Prototype Slice 8 — Workspace & Awareness implementation plan

Status: **Implemented locally and verified on 2026-08-15; deployment remains owner-controlled**

This plan does not ratify or modify OSLO canon. It translates the accepted Slice 8 grill recommendations and the non-canonical research prototype into an executable completion plan for the application repository.

## 1. Outcome

Slice 8 will add a trustworthy workspace layer around the existing project experience. A user will be able to see and switch between projects, understand which project needs attention, manage awareness and personal/workspace preferences, create or archive projects safely, and use the application in dark, light, system, desktop and mobile modes without changing the governed analysis.

The implementation is a **completion and parity pass**, not a greenfield rebuild. The application already has Workspace and Settings routes, real API-backed project data, project switching, notifications, archive/restore, plan-capacity handling and unit coverage. Slice 8 closes the remaining product, visual, consistency, accessibility and end-to-end verification gaps.

## 2. Scope authority and naming

The working scope in this plan is the prototype sequence named **Slice 8 — Multi-Project Workspace & Awareness** in:

- `90_research/oslo-product-grill/vertical-slices/slice-08-workspace-awareness/`

That package is non-canonical research material. Canonical R2 material currently uses Slice 8 for feedback/survey/telemetry. The implementation may proceed under the working label **Prototype Slice 8 — Workspace & Awareness**, but the repository owner must decide how the final release map and test naming are reconciled. This plan must not silently overwrite the canonical Slice 8 definition.

The golden prototype controls interaction hierarchy and visual intent. Current owner canon and product-authoritative terminology control semantics where the historical prototype differs. In particular:

- Confidence remains trust in OSLO's understanding, never project health or a portfolio score.
- Awareness, Settings and workspace projections are Disclose surfaces; they produce no cognition.
- Only a governed recomputation can change assessment or issue state.
- Existing Slice 6 collaboration and Slice 7 reporting behavior must remain real; they must not be relabelled as future seams merely because the older prototype deferred them.

## 3. Agreed scope

### In scope

- API-backed Workspace Home using only real accessible projects.
- Honest zero-project, one-project, multi-project and archived-project states.
- Project switcher with search, current-project indication, Workspace Home and New Project actions.
- Awareness panel with unread state, source routing and existing analysis/collaboration events.
- Settings surface covering Account, Profile, Appearance, Notifications, Workspace, Project defaults, Collaboration, Membership, Subscription, Billing and Integrations.
- Real profile/workspace/preference persistence through existing APIs, subject to actor permissions.
- Dark, light and system theme modes without first-paint flash.
- Honest active-project capacity choice: compare plans or archive, without losing data.
- Tenant authorization, RLS, failure states, keyboard operation, focus management and responsive layouts.
- Shared projection consistency across Workspace Home, switcher, Settings, notifications, History and project routes.
- Full regression protection for Slices 1–7.

### Out of scope

- A portfolio score, project ranking, health score or cross-project confidence average.
- New cognition, analysis, issue-lifecycle or recommendation behavior.
- Automatic project archiving, automatic billing or automatic upgrade.
- Per-seat pricing or reviewer/viewer capacity charges.
- A replacement for Slice 6 collaboration or Slice 7 reports/export.
- Real integrations that have not been owner-approved.
- Canonical renumbering or adoption of the research prototype.
- A rewrite of the existing workspace API or components when targeted changes are sufficient.

## 4. Current implementation and gap analysis

| Capability | Existing baseline to reuse | Completion work |
|---|---|---|
| Workspace Home | `/workspace`, `WorkspaceHome`, real `WorkspaceSummary`, archive/restore and plan comparison exist. | Match prototype hierarchy and spacing; make zero/one/many states internally consistent; ensure only real accessible projects render; add visual snapshots. |
| Project switcher | `ProjectWorkspaceControls` lists active projects, search, Workspace Home and New Project; Escape coverage exists. | Add complete keyboard navigation, focus return, outside-click coverage, stable header positioning and status/reliability copy parity. |
| Notifications | API-backed panel, deduplication, unread count, Mark all read and collaboration events exist. | Normalize categories and source routes; prove read state never triggers analysis; add empty/error/large-history/mobile states and focus trapping. |
| Settings | `/settings`, 11+ sections, search, profile/workspace preferences, theme and plan facts exist. | Reconcile the additional Access section with the approved 11-section information architecture; remove dead/inert controls; restore focus/scroll correctly; add permission and failure feedback. |
| Appearance | Dark/Light/System preferences and a theme initializer exist. | Prove persistence before paint, OS theme changes, reduced motion, WCAG AA and no severity/maturity color regression. |
| Capacity | Project creation returns the real gate; plan comparison and archive/restore APIs exist. | Align the choice UI with the prototype, make error/retry explicit, prove double-click idempotency and guarantee archive preserves every related record. |
| Backend | Workspace summary, preferences, notifications/read, archive and restore endpoints exist. | Treat one DTO/projection as authoritative; add multi-workspace authorization and stale/read consistency tests; remove frontend-only assumptions. |
| Unit tests | Workspace Home, controls, Settings and API tests cover important behavior. | Add the missing edge, keyboard, permission and shared-projection cases. |
| E2E | `tests/e2e/specs/slice-eight.spec.ts` exists. | It still asserts an older Workspace UI (`OSLO Product Grill`, `Active projects`, `Open project`). Replace it with current prototype-aligned selectors and desktop/mobile visual tracing. |

## 5. User-visible flows

### Flow A — Workspace Home

1. Open Workspace Home from the Intralign logo or project switcher.
2. Render only projects the current actor may access.
3. At one active project, show one detailed project card and New Project; do not show a fake portfolio grid.
4. At multiple active projects, show pinned/current and recent projects without calculating a portfolio score.
5. Show archived projects separately with explicit Restore actions.
6. Opening an analyzed project enters Overview; an unanalyzed project enters Intake.
7. Every project card shows name, ownership/access, analysis freshness, reliability-qualified understanding, open issues, artifacts and last activity.

### Flow B — Project switcher

1. Open from the project chip without moving the header or document center.
2. Show Workspace Home, the current project, accessible active projects and New Project.
3. Search appears for a large project list; no-match state is explicit.
4. Arrow keys move through options; Enter selects; Escape or outside click closes; focus returns to the trigger.
5. Archived and unauthorized projects never appear.

### Flow C — Notifications and awareness

1. Open the bell from project or Workspace Home.
2. Show a neutral unread badge and a right-side fixed-width panel that overlays rather than reflows the document.
3. Include analysis complete/failed/stale plus existing reviewer response, invitation, mention and comment events when applicable.
4. Deduplicate by stable event identity, not display text.
5. Opening an item marks only that item read and routes to its source.
6. Mark all read changes awareness presentation only; it never starts analysis or changes a read.
7. Empty, loading, error and long-history states remain usable on desktop and mobile.

### Flow D — Settings

1. Open Settings from the account entry point and return to the previous app location.
2. Use a left navigation and search across the approved sections.
3. Profile and owner-authorized workspace edits save through the API with pending, success and retry states.
4. Notification preferences control visibility only.
5. Collaboration and Membership reflect the real Slice 6 system rather than an obsolete “later” seam.
6. Subscription and Billing state facts and real supported actions without implying a successful plan change before server confirmation.
7. Integrations remain visibly deferred unless an approved integration exists.

### Flow E — Appearance

1. Choose Dark, Light or Match system.
2. Apply immediately and persist safely.
3. Restore the correct theme before the first application paint.
4. Follow OS changes only while System is selected.
5. Preserve visible focus, reduced motion and AA contrast in every mode.

### Flow F — Capacity, archive and restore

1. New Project calls the server; the client never decides entitlement locally.
2. If capacity is available, create once and enter Intake.
3. If capacity is exhausted, present Compare plans and Archive a project as explicit choices.
4. Archive is actor-authorized, non-destructive and immediately removes the project from active lists.
5. Restore returns the same project, artifacts, issues, history, collaboration and latest assessment.
6. If zero projects remain active, show a clean empty state without a contradictory active card.

## 6. Architecture and contracts

### 6.1 Shared workspace projection

Use one API-produced workspace projection as the source for Workspace Home, the project switcher, plan/capacity facts and notification identity. Do not recompute project state independently in multiple React components.

The projection must expose, at minimum:

- workspace ID/name and actor role;
- plan label and active-project limit;
- `can_create_project` as server-derived guidance;
- accessible projects with archived state, analysis freshness, understanding band, reliability, weakest pillar, issue count, artifact count, ownership/access and updated time;
- awareness items with stable event ID, category, read state, source route, project ID/name and timestamp.

FastAPI/OpenAPI remains the contract source of truth; update the typed frontend client contract when the DTO changes.

### 6.2 Mutations

Reuse and harden the existing endpoints for:

- creating a project;
- archiving/restoring a project;
- reading and updating workspace preferences;
- marking one/all awareness items read;
- real plan comparison/checkout entry where already supported.

Every mutation must be workspace-scoped, actor-authorized and idempotent or protected from repeated submission. UI success appears only after a server-confirmed response.

### 6.3 Security and privacy

- Enforce tenant scope in API queries and PostgreSQL RLS.
- Owners may rename the workspace and archive/restore projects; members see only permitted controls.
- Never reveal unauthorized project names through the switcher, notifications, search or error copy.
- Notification routes must re-check current access; removed access leads to a neutral unavailable state.
- Do not log raw invitation, review, share or session tokens.
- Awareness preferences and read state carry no cognition side effects.

## 7. UI/UX specification

### Shell and positioning

- Preserve the established centered project shell, fixed left navigation and fixed-width OSLO rail.
- Workspace menus and notifications overlay the content; they do not shift the breadcrumb, title or integrity controls.
- The notification panel is flush to the right and owns its internal scroll.
- The Workspace and Settings content columns use the prototype’s hierarchy, spacing, compact cards and restrained neutral chrome.
- Use the current icon library; do not reproduce prototype text glyphs as fake icons.

### Workspace Home states

- **Zero active:** one clear empty-state panel, Restore if archived projects exist, and New Project. No active project card may remain visible.
- **One active:** “Your project” detailed card plus New Project and Archived.
- **Two or more:** current/pinned and recent groups, still without aggregate scoring.
- **Stale:** neutral freshness label with a next step; stale is not severity.
- **Loading/error:** skeleton or stable placeholder; retry without losing navigation.

### Settings information architecture

The approved navigation is:

1. Account
2. Profile
3. Appearance
4. Notifications
5. Workspace
6. Project defaults
7. Collaboration
8. Membership
9. Subscription
10. Billing
11. Integrations

The current separate **Access & invites** area must be reviewed against product-authoritative GA access requirements. Prefer integrating its content into Collaboration or Membership if that preserves the authoritative contract. Do not delete it solely for screenshot parity.

### Responsive behavior

- Desktop: left navigation, centered main content and fixed OSLO rail remain stable.
- Tablet: workspace/settings content narrows; menus stay anchored and panels use available width.
- Mobile: Settings navigation becomes a drawer or compact section chooser; notification panel becomes a full-width sheet; project cards become one column; all primary actions remain visible.
- No horizontal overflow at 390px, 768px, 1280px and 1536px.
- Touch targets are at least 44px where practical.

### Accessibility

- Semantic headings, navigation, menus, dialogs, lists and status regions.
- Visible focus and correct focus trap/restore for modal and panel surfaces.
- Full keyboard operation for switcher, Settings navigation, notifications, archive/restore and plan choices.
- Textual states in addition to color and icons.
- Reduced-motion behavior for panels and theme transitions.
- WCAG 2.1 AA contrast in dark and light modes.

## 8. Delivery increments and TDD sequence

### Increment 0 — Characterize and freeze the baseline

- Capture desktop/mobile screenshots of the current Workspace, switcher, notifications, Settings and capacity modal.
- Run existing workspace unit/API tests and the current Slice 8 E2E to identify stale assertions and real failures.
- Add failing tests for the zero-active contradiction, notification side-effect guard and switcher focus return.

Exit: existing behavior and visible gaps are reproducible; no feature code changed before red tests exist.

### Increment 1 — Shared projection tracer bullet

- Normalize the workspace/project/awareness DTO.
- Render the same real project state in Workspace Home and switcher.
- Add tenant and removed-access negative tests.
- Keep a compatibility adapter if the DTO must transition incrementally.

Exit: one API state produces matching Workspace Home and switcher output.

### Increment 2 — Workspace Home parity and state correctness

- Implement zero/one/many/archived layouts.
- Correct card hierarchy, reliability qualification, freshness and no-portfolio-score disclosure.
- Fix archive/restore optimistic state and error recovery.
- Add desktop/mobile component and visual tests.

Exit: all workspace states match the prototype’s intent using real data, including a clean zero-active state.

### Increment 3 — Project switcher completion

- Add complete keyboard navigation, focus return and outside-click behavior.
- Add large-list search/no-results and permission filtering.
- Stabilize menu/header positioning at every project route and viewport.

Exit: the switcher is fully operable by keyboard and never exposes inaccessible projects.

### Increment 4 — Awareness completion

- Normalize analysis and Slice 6 collaboration categories.
- Route every item to a valid authorized source.
- Add one-item/all-items read operations and durable or explicitly scoped read-state semantics.
- Complete empty/error/long-history/mobile UI and the persistent no-analysis disclosure.

Exit: awareness is actionable, deduplicated and proven presentation-only.

### Increment 5 — Settings and appearance completion

- Reconcile the section information architecture.
- Remove or relabel inert controls.
- Complete API save/error/permission states for profile, workspace and notification preferences.
- Finish dark/light/system persistence, no-flash initialization, OS-change listening and AA fixes.

Exit: every visible control works or is honestly read-only/deferred; theme and preferences survive reload.

### Increment 6 — Capacity and data-retention proof

- Align the server-driven capacity modal to prototype intent.
- Protect repeated project creation and archive/restore submissions.
- Prove archive/restore retains artifacts, issues, history, snapshots, review records and latest assessment.
- Add owner/member authorization negatives.

Exit: capacity choices are honest, non-destructive and race-safe.

### Increment 7 — Responsive, accessibility and visual parity

- Compare prototype and implementation at the same desktop and mobile states.
- Correct spacing, alignment, panel width, typography, overflow, focus and motion.
- Add automated accessibility checks plus manual keyboard/screen-reader smoke checks.

Exit: no release-blocking prototype mismatch, overflow, focus or contrast defect remains.

### Increment 8 — Full regression and release candidate

- Run the updated Slice 8 desktop/mobile tracer.
- Upload and analyze five representative real documents across the supported intake formats, then verify Slices 1–7 remain intact.
- Run full web/API suites, lint, type checks, production build and guardrails.
- Record AI review, human review and manual QA evidence before deployment approval.

Exit: Slice 8 and all inherited slices are release-candidate green.

## 9. Trackable implementation issues

| ID | Outcome | Primary acceptance test |
|---|---|---|
| S8-01 | Characterize the existing Slice 8 baseline | Current screenshots, unit/API results and E2E failures are recorded before implementation changes. |
| S8-02 | Create one authoritative workspace projection | Workspace Home and switcher render identical project state from one DTO. |
| S8-03 | Complete zero/one/many Workspace Home states | Archiving the only project shows no active card; restoring returns the exact retained project. |
| S8-04 | Match project cards to the prototype’s information hierarchy | Cards show ownership, freshness, qualified understanding, issues, artifacts and recency without a portfolio score. |
| S8-05 | Finish accessible project switching | Keyboard, Escape, outside click, focus return, search and unauthorized filtering pass. |
| S8-06 | Normalize and route awareness items | Every supported event routes correctly; duplicate events appear once. |
| S8-07 | Prove awareness has no cognition side effects | Marking one/all read produces no analysis run, issue change or confidence change. |
| S8-08 | Complete Settings controls and information architecture | All approved sections are reachable; controls work or are clearly factual/deferred. |
| S8-09 | Complete theme and accessibility behavior | Dark/Light/System persists without flash and clears AA/keyboard/reduced-motion checks. |
| S8-10 | Harden capacity, archive and restore | Double-submit is safe; permissions hold; every related record survives archive/restore. |
| S8-11 | Achieve desktop/mobile prototype parity | Same-state comparisons pass at 390, 768, 1280 and 1536 widths with no overflow. |
| S8-12 | Replace the stale Slice 8 E2E and close regression | Updated tracer and full Slices 1–7 regression suite pass with five real documents. |

Every issue follows RED → GREEN → REFACTOR and includes contract, component, integration or E2E coverage proportional to its boundary.

## 10. Test and QA matrix

### Backend/API

- Workspace summary tenant isolation across two workspaces.
- Actor-specific project visibility and permission-aware actions.
- Archive/restore preservation of all dependent records.
- Capacity checked by the server; repeated create requests do not create duplicates.
- Preferences round-trip for theme, identity and awareness categories.
- Notification deduplication, read state and inaccessible target handling.
- Pinned negative: notification read/preference mutations enqueue zero analysis runs and change zero cognition records.

### Frontend component/integration

- Zero, one, many, stale and archived Workspace Home states.
- Project card field and canonical terminology assertions.
- Switcher keyboard navigation, focus return, large search and no results.
- Notification loading, empty, error, long history, one-read/all-read and source routes.
- Settings search, section navigation, owner/member permissions, saving and retry.
- Dark/Light/System state, no-flash initialization and OS preference changes.
- Capacity modal success/failure/double-click and archive/restore state.

### Playwright desktop/mobile tracer

1. Sign in as an owner and open Workspace Home.
2. Verify one-project state and absence of a portfolio score.
3. Create enough real projects to exercise multi-project switching and search.
4. Open an analyzed and an unanalyzed project through the switcher.
5. Open notifications, route each supported category and prove read actions do not create analysis.
6. Change profile/workspace/notification preferences and verify persistence after reload.
7. Test Dark, Light and Match system with visual snapshots.
8. Reach the active-project cap, open the choice, archive one project and create another.
9. Restore the archived project and verify all retained records.
10. Repeat critical flows as a non-owner and across a second workspace.
11. Repeat the shell, switcher, notification panel, Settings and capacity choice at mobile width.
12. Assert no horizontal overflow and stable header/OSLO rail positioning.

### Five-document regression

Use representative PDF, DOCX, PPTX, XLSX/CSV and TXT/MD inputs containing purpose, scope, requirements, constraints, work breakdown, schedule and resources. Confirm:

- Intake and Fast/Deep analysis still complete.
- Overview, Issues, seven plan artifacts, Grounding map, collaboration, History and Reports remain coherent.
- Workspace cards and notifications reflect the resulting real project state.
- No duplicate content, lost reviewer evidence or stale projection appears after switching projects.

### Build gate

- Web unit/integration tests.
- API unit/integration tests and Ruff.
- ESLint, TypeScript and production build.
- Active R2 guardrails.
- Updated desktop/mobile Slice 8 tracer.
- Full Slices 1–7 Playwright regression.
- Git whitespace check.

## 11. Observability

Reuse existing events where available and add only approved missing coverage:

- `workspace.viewed`
- `project.switched`
- `project.archive_requested`
- `project.archived`
- `project.restored`
- `project.capacity_gate_shown`
- `notification.opened`
- `notification.read`
- `notification.mark_all_read`
- `settings.preference_updated`
- `settings.workspace_renamed`
- `appearance.theme_changed`

Events carry workspace/project correlation IDs, actor role, outcome and failure reason. They contain no raw tokens, document content or sensitive notification excerpts. Awareness events never serve as analysis triggers.

## 12. Risks and controls

| Risk | Control |
|---|---|
| Prototype Slice 8 conflicts with canonical numbering | Keep the working prototype label and require owner resolution before release documentation changes. |
| Existing functionality is accidentally rebuilt | Characterize first and prefer targeted changes to current components/contracts. |
| Workspace surfaces disagree about project state | One server-produced projection plus contract consistency tests. |
| Notifications accidentally trigger analysis | Pinned zero-side-effect tests at API and integration layers. |
| Archive hides or deletes dependent records | Transactional archive flag and full retention/restore integration tests. |
| Unauthorized project names leak through switching/awareness | Tenant/actor filtering in API/RLS and cross-workspace negative tests. |
| Theme flashes or loses contrast | Pre-paint initializer and automated/manual contrast snapshots. |
| Settings accumulates dead controls | Each affordance must work or be styled and labelled as factual/deferred. |
| UI parity work destabilizes the fixed shell | Same-viewport visual comparison and overflow assertions on every target width. |
| Existing dirty worktree is overwritten | Isolate Slice 8 edits, preserve unrelated Slice 6/7 changes and review the diff per increment. |
| The current E2E gives false confidence | Replace stale selectors/states before calling the slice complete. |

## 13. Definition of done

Slice 8 is complete only when:

- S8-01 through S8-12 meet their acceptance tests.
- Workspace Home uses real authorized data and correctly handles zero, one, many and archived states.
- No portfolio score, project ranking or health interpretation exists.
- Project switching is complete on keyboard, desktop and mobile.
- Awareness items route correctly and are proven incapable of changing analysis.
- Settings controls work or are honestly factual/deferred, with existing collaboration represented accurately.
- Dark, Light and System themes persist without flash and pass accessibility checks.
- Capacity choices are server-confirmed, non-destructive and race-safe.
- Prototype same-state visual comparisons pass at desktop and mobile widths.
- The updated Slice 8 E2E, full Slices 1–7 regressions and five-document QA pass.
- API tests, web tests, lint, type checks, production build and guardrails pass.
- AI review, human code review and manual QA evidence are recorded.
- Deployment happens only after owner approval, followed by live authenticated smoke, health and log verification.

## 14. Recommended execution order

Execute in this order:

**S8-01 → S8-02 → S8-03/S8-04 → S8-05 → S8-06/S8-07 → S8-08/S8-09 → S8-10 → S8-11 → S8-12**

This order first protects the existing implementation, then proves shared state, completes the core user journeys, and leaves visual polish and full regression until the functional contracts are stable.
