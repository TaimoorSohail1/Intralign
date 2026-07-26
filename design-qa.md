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
