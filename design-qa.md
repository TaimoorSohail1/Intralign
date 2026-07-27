# Slice 7 History Design QA

## Evidence

- Source visual truth: `C:\Users\Hp\AppData\Local\Temp\codex-clipboard-9b2b0dc7-d91e-4570-a6d0-db7fd0d84bdd.png`
- Rendered implementation: `C:\Users\Hp\Downloads\oslo-app\.artifacts\slice7-history-final-1200x876.png`
- Side-by-side comparison: `C:\Users\Hp\Downloads\oslo-app\.artifacts\slice7-history-comparison.png`
- Route: `http://localhost:3000/projects/d043536c-f5e7-4588-bf8a-24457f52cb77/history`
- State: authenticated desktop, All filter, current run expanded, retained historical runs collapsed.
- CSS viewport: `1200 x 876` for both source and implementation.
- Device pixel ratio: `1`.

## Findings

No actionable P0, P1, or P2 differences remain.

- Layout: the production view preserves the prototype's persistent project navigation, centered 720px history workspace, heading, trend card, filters, run cards, and read-only note.
- Typography and density: heading, metadata, filter chips, change pills, event rows, and timestamps follow the prototype's compact hierarchy.
- Colors and tokens: dark surfaces, muted dividers, OSLO orange actions, green current state, and neutral historical state use the existing product design system.
- Content: the implementation renders real retained project runs, so it contains more history entries than the two-run prototype sample.
- Expansion: only the current run opens initially; historical runs remain collapsed and can be expanded independently, matching the prototype.
- Responsiveness: the trend labels wrap inside the card and no longer overflow the viewport.
- Empty state: it appears only when the selected filter genuinely has no retained events.

## Comparison History

### Pass 0 — P1 missing retained history

- Finding: the database contained assessment snapshots but no legacy history events, so the timeline showed trend points while the run list incorrectly displayed an empty state.
- Fix: synthesize read-only history groups from retained assessment snapshots whenever legacy events are absent.

### Pass 1 — P1 horizontal overflow

- Finding: many live runs forced trend labels beyond the history card and viewport.
- Fix: constrain the trend card, wrap labels into the available grid, and preserve the prototype width.

### Pass 2 — P2 expansion and density

- Finding: all retained runs initially opened, making the page much taller and denser than the prototype.
- Fix: open only the current run by default and keep historical runs collapsed.

### Pass 3 — final

- Rechecked typography, spacing, colors, run states, filters, overflow, real retained data, and empty-state behavior at the shared viewport.
- No actionable P0/P1/P2 findings remain.

## Verification

- History component regression: passed.
- Full web test suite: 44 tests passed.
- Web lint: passed.
- Production web build: passed.
- History API integration suite: 6 tests passed.
- Live route: four retained runs rendered, current expanded, three historical runs collapsed, and no trend overflow.

final result: passed

# Slice 9 Collaboration History and Issue Review Design QA

## Evidence

- Source visual truth: user-provided History and issue-sidebar screenshots.
- Rendered implementation: project History filters and the issue `Share for review` card.
- State: authenticated desktop project with retained analysis runs, reviewer activity, and an open issue.

## Findings

No actionable P0, P1, or P2 visual differences remain.

- History now exposes a dedicated `Collaboration & invites` filter instead of hiding reviewer activity inside the general timeline.
- A concise collaboration legend explains which comments, invitations, shared snapshots, exports, and reviewer decisions are retained.
- Existing review invitations are backfilled into append-only project history, while new collaboration actions are recorded at creation time.
- The issue sidebar review form is a separate bordered card with a clear heading, labeled inputs, consistent spacing, a full-width primary action, and safe bottom clearance.

## Verification

- History and Overview component tests: 31 passed.
- Collaboration API tests: 5 passed.
- Production web build: passed.
- Local database migration and reviewer-invitation backfill: passed.
- Workspace recent activity exposes the retained reviewer response and links to project History.

final result: passed

# Slice 9 Project Header Actions Design QA

## Evidence

- Source visual truth: the supplied project-header screenshot at `2550 × 310`.
- Rendered implementation: `http://localhost:3000/projects/65ba2e0a-e818-4719-9c05-7dcfb95a0012/overview`.
- Comparison method: live authenticated browser inspection, screenshot review, and DOM geometry checks.

## Findings

No actionable P0, P1, or P2 visual differences remain.

- Share and Export now occupy a dedicated header grid area beside the confidence control.
- The controls use a compact 32px height, consistent spacing, icon alignment, OSLO borders, and a restrained orange primary treatment.
- Notification, search, advisor, and account controls remain on the same header row.
- The header has no horizontal or vertical overflow; every control is fully inside the 48px header.
- At narrow breakpoints, Share and Export retain accessible icon buttons while their labels collapse to preserve space.

## Verification

- Live header geometry: 48px header; all action controls at `top: 7.5px`, `bottom: 39.5px`.
- Header overflow: `scrollWidth === clientWidth` and `scrollHeight === clientHeight`.
- Collaboration and workspace-control tests: 11 passed.
- Web lint: passed.
- Production web build and TypeScript validation: passed.

final result: passed

# Slice 9 Collaboration, Sharing, and Export Design QA

## Evidence

- Source visual truth: Slice 9 prototype at `http://127.0.0.1:4180/prototype.html`.
- Authenticated implementation: `http://localhost:3000/projects/65ba2e0a-e818-4719-9c05-7dcfb95a0012/overview`.
- Public snapshot: `http://localhost:3000/share/euA3XnlycO8nzdJs4Aum0wkNoiEPGgSlUooseBMmPYY`.
- Public review: `http://localhost:3000/review/ZAnjOuXGA2Tzabm9sRaf6tDWkU4GXmbItgwI6x78io0`.
- Comparison method: live prototype and implementation DOM, layout, responsive states, keyboard interactions, and complete share/review flows inspected at the same desktop viewport.
- Focused screenshots were not added because the in-app browser security policy blocks local-URL screenshot capture; live side-by-side inspection and interaction testing covered the same states.

## Findings

No actionable P0, P1, or P2 visual differences remain.

- Collaboration actions use the established OSLO dark surfaces, orange emphasis, compact controls, spacing, and responsive dialog treatment.
- Snapshot sharing and reviewer access are visually distinct and explain their different permissions before a link is created.
- Public snapshot and review pages remain readable without the authenticated project shell.
- Reviewer actions are clear, keyboard accessible, and preserve the read-only source evidence.
- The export control communicates scope and produces a governed PDF containing all seven artifacts, findings, evidence references, currency marker, and disclaimer.

## Comparison History

### Pass 0 — review completion linkage

- Finding: a reviewer response could be stored before its Extended Analysis run was linked.
- Fix: make submission idempotent, retry unlinked responses safely, and resolve the grant only after the analysis run is linked.

### Pass 1 — notification timestamp

- Finding: reviewer-response notifications queried a non-existent generic timestamp.
- Fix: project `occurred_at` consistently as the notification creation timestamp.

### Pass 2 — export completeness

- Finding: the first export summary did not include the promised seven artifacts and evidence references.
- Fix: generate a multipage PDF with artifact content, open findings, evidence references, currency context, and governance disclaimer.

### Pass 3 — final

- Rechecked member and reviewer permissions, seat and invitation limits, invitation revocation, snapshot creation, reviewer submission, Extended Analysis, owner notification, public links, and export.
- No actionable P0/P1/P2 findings remain.

## Verification

- Focused collaboration, invitation, and export API tests: 29 passed.
- Full web suite: 70 tests passed.
- Web lint: passed.
- TypeScript check: passed.
- Python Ruff checks: passed.
- Production web build: passed.
- Live snapshot, reviewer response, Extended Analysis, owner notification, and no-analysis export checks: passed.
- Full API suite is not claimed in this pass because it exceeded the local execution window; no failure was reported before timeout, and Slice 9 focused coverage passed.

final result: passed

# Slice 8 Project Header Polish Design QA

## Evidence

- User reference: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice-8-project-header-reference.png`
- Rendered implementation: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice-8-project-header-implementation.png`
- Account-menu implementation: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice-8-account-menu-implementation.png`
- Normalized visual comparison: `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice-8-project-header-comparison.png`
- Route: `http://localhost:3000/projects/d043536c-f5e7-4588-bf8a-24457f52cb77/overview`
- State: authenticated desktop project with the OSLO advisor expanded.

## Findings

No actionable P0, P1, or P2 visual differences remain.

- The former wrapping bug is removed by giving brand, project switcher, context, confidence, notifications, search, and account controls deliberate grid areas.
- The project switcher is now a clear project-level control with a folder icon, stronger affordance, bounded width, and accessible label.
- Search, notifications, and account actions use one consistent control size, border treatment, spacing rhythm, hover state, and keyboard focus treatment.
- The account menu is anchored to the account control and presents identity, help, settings, and logout actions in a compact professional hierarchy.
- The header remains readable across desktop, compact desktop, tablet, and mobile breakpoints without controls dropping into the advisor region.
- The treatment stays within the existing OSLO dark surfaces, typography, orange accent, muted borders, and icon library.

## Verification

- Header and account-menu regression tests: passed.
- Full web suite: 62 tests passed.
- Web lint: passed.
- TypeScript check: passed.
- Production web build: passed.
- Live authenticated header, project switcher, action controls, and account menu: passed.

final result: passed

# Slice 8 Workspace Awareness Design QA

## Evidence

- Source visual truth: Slice 8 prototype at `http://127.0.0.1:4179/prototype.html`.
- Rendered implementation: `http://localhost:3000/workspace`, `/settings`, and the project-level workspace controls.
- State: authenticated desktop workspace with active projects, limit prompt, project switcher, notifications, and system theme.
- Comparison method: prototype and production routes inspected at the same desktop viewport and interaction states.

## Findings

No actionable P0, P1, or P2 visual differences remain.

- Workspace Home follows the prototype's dark OSLO shell, compact top bar, plan context, project cards, recent activity, and clear primary action.
- The project switcher preserves Workspace Home and New project actions while bounding large legacy workspaces to eight recent projects, searchable by name.
- The Free-plan prompt explains the one-active-project rule and offers upgrade or a bounded recent-project archive choice.
- Notifications retain the prototype's compact overlay, unread state, settings entry, and activity link without growing beyond the viewport.
- Settings uses the existing OSLO typography, surfaces, spacing, and orange/green state accents; light, dark, and system preferences apply immediately.
- The old standalone top-bar `+ New project` action is removed from project screens so project creation has one governed Slice 8 entry point.

## Comparison History

### Pass 0 — P1 unbounded legacy data

- Finding: the local development database predates the Free-plan cap and contains 221 active test projects, causing the limit prompt and project switcher to render hundreds of options.
- Fix: show recent, useful subsets with search and direct Workspace Home access while leaving historical data untouched.

### Pass 1 — P1 hydration mismatch

- Finding: locale-dependent project dates differed between server and browser rendering.
- Fix: format dates deterministically in UTC using `en-GB`.

### Pass 2 — P2 notification density

- Finding: a large unread history could extend the notification panel beyond a useful desktop viewport.
- Fix: bound the overlay to the eight most recent notifications and preserve the full workspace activity link.

### Pass 3 — final

- Rechecked workspace search, project-limit prompt, project switcher search, notifications, settings themes, and entry back into the existing project experience.
- No actionable P0/P1/P2 findings remain.

### Pass 4 — cross-slice lifecycle hardening

- Finding: a returning user with an active project could still reach the legacy Welcome action and receive a project-limit conflict.
- Fix: redirect returning users from Welcome to Workspace Home and route any concurrent limit conflict into the governed Slice 8 project-limit prompt.
- Finding: legacy local workspaces can remain above the new one-active-project cap after archiving a single project.
- Fix: keep the capacity dialog open, show the exact remaining archive count, and never issue a create request until capacity is genuinely available.

## Verification

- Dedicated Slice 8 component and route tests: passed.
- Project switcher large-workspace and notification-density regression tests: passed.
- Welcome-to-workspace lifecycle and legacy over-limit regression tests: passed.
- Full web suite: 61 tests passed.
- Full API suite: 130 tests passed.
- Web lint and TypeScript checks: passed.
- Production web build: passed.
- Live authenticated workspace, settings, limit prompt, switcher, and notification states: passed.
- Cross-slice route audit from Invitations through Workspace, Overview, Issues, History, Attention Map, and Artifacts: passed with no page-load failures.

## Final screenshots

- `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice8-workspace.png`
- `C:\Users\Hp\Downloads\oslo-app\reports\screenshots\slice8-settings.png`

final result: passed
