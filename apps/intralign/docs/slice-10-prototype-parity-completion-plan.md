# Slice 10 Prototype Parity and Completion Plan

## 1. Outcome

Bring the executable application to the signed-off Slice 10 experience:

- the project dashboard uses the prototype's information hierarchy and desktop shell;
- Reports is a visible, first-class project destination with a real Readout workflow;
- Inference Map is a visible, first-class project destination backed by real provenance data;
- tiering and limits remain honest and do not weaken the underlying analysis;
- all Slice 10 behavior is traceable from requirement to implementation to test;
- the final handoff includes a pass/fail acceptance matrix and matched screenshots.

The five supplied screenshots are the visual acceptance references. The cumulative Slice 10 prototype and its later signed-off amendments are the behavioral references.

## 2. Sources of truth

Use these in order when implementing:

1. Ratified doctrine, decisions, and later Slice 10 amendments.
2. Signed-off Slice 10 success criteria and E2E scenarios.
3. The cumulative Slice 10 prototype for layout and interaction details.
4. The supplied prototype screenshots for visible fidelity.
5. Existing application behavior where it does not conflict with items 1–4.

Primary references:

- `vertical-slices/slice-10-tiering-limits/prototype.html`
- `vertical-slices/slice-10-tiering-limits/success-criteria.md`
- `vertical-slices/slice-10-tiering-limits/e2e-test-scenarios.md`
- `vertical-slices/slice-10-tiering-limits/frontend-ui.md`
- `vertical-slices/slice-10-tiering-limits/user-experience.md`
- `vertical-slices/slice-10-tiering-limits/product-data.md`
- `vertical-slices/slice-10-tiering-limits/workflow.md`
- `vertical-slices/slice-10-tiering-limits/work-item-WI-R1-readout-composer.md`
- `vertical-slices/slice-10-tiering-limits/work-item-WI-R5-progress-panel-foundation-bar.md`
- `vertical-slices/slice-10-tiering-limits/work-item-WI-R6-fraction-hero.md`

## 3. Current-state findings

| Area | Current state | Required state | Gap |
|---|---|---|---|
| Project navigation | Reports route exists in the uncommitted Slice 10 work. Inference Map is absent. | Overview, Issues, History, Attention Map, Inference Map, and Reports are peer destinations. | Major |
| Dashboard shell | Sidebar and header exist, but spacing, width, top-bar structure, content order, and desktop right rail differ from the prototype. | Compact prototype shell with project switcher, breadcrumb, confidence pill, left navigation, central read, and persistent OSLO rail on desktop. | Major |
| Outcome Confidence | Current Overview emphasizes a numeric `45/100` score. | Latest signed-off prototype uses a five-band maturity ramp, grounding qualifier, limiting dimension, and neutral movement. | Major |
| Progress | Current UI shows resolved issues, critical issues, dependencies, and artifacts read. | Fraction hero such as `17 of 28`, provenance split, load-bearing inference link, and open/closed work stats derived from one context-item registry. | Major |
| Inference Map data | No route, API response, or persisted context-item model exists. | Live projection of grounded and inferred context items, assumptions, structural facts, ageing, and velocity. | Missing |
| Inference Map UI | No component or navigation item exists. | Prototype-matched map with per-artifact pips, verification flag, assumptions, structure, and weekly movement. | Missing |
| Reports route | `/projects/[projectId]/reports` exists. | First-class Reports workspace. | Partial |
| Readout editing | Seven textareas stored only in React state. | One continuous rendered document using the same rich editor behavior as plan artifacts. | Major |
| Readout content | Generated from Overview data but includes internal OSLO/assessment vocabulary. | Reader-facing seven-section document, zero OSLO vocabulary in OSLO-authored body, risks before assumptions, PM-owned action plan, recipient-specific ask only. | Major |
| Readout persistence | No readout tables or APIs. Reload loses edits. | Living Readout and persisted sections with tier-aware reuse behavior. | Missing |
| Memo snapshot | Generic project PDF export only. | Immutable dated memo bytes tied to a source analysis and currency marker. | Missing |
| Send and schedule | UI explicitly simulates both locally. | Durable delivery and schedule records; currency checked at send time; no analysis triggered. | Missing |
| History integration | Reports do not produce History events or open exact sent bytes. | Sent/exported memo appears in History and reopens the exact frozen memo. | Missing |
| Tiering and limits | Subscription and usage infrastructure exists, but payment is simulated and some values are hard-coded. | Full requirement census with ratified values enforced and unset values kept visibly unset. | Partial |
| Automated coverage | Slice 10 E2E covers plan switching and basic report visibility/editing. | Coverage for dashboard parity, Inference Map, Readout invariants, persistence, snapshots, delivery, scheduling, responsive behavior, and failure states. | Major |

## 4. Guardrails

- Preserve all existing uncommitted user work. Do not overwrite or reset the dirty worktree.
- Do not fabricate Inference Map values from UI labels or hard-coded demo numbers.
- Use one provenance/context-item projection for Overview Progress, Inference Map, and Readout provenance sections.
- Reports package existing understanding; opening, editing, exporting, sending, or scheduling a report must never run analysis or change confidence.
- Recipient selection may tailor the ask, not the assessment or the rest of the read.
- Editing remains available on Free. Tier checks may govern persistence, optional composition, branding, or automation—not access to the read.
- Manual sharing is not seat-metered. Scheduled automation may be a Basic capability.
- Frozen memo snapshots are immutable and must retain their original source analysis and currency state.
- User-visible copy must follow the signed-off word budgets and must not expose internal doctrine identifiers.
- Desktop visual parity must not break responsive navigation, keyboard access, reduced motion, or focus visibility.

## 5. Delivery sequence

### Phase 0 — Baseline and traceability

Goal: make changes safely and prove what Slice 10 means before modifying behavior.

Tasks:

1. Capture the current app at the same viewport and state as each supplied reference.
2. Record the current git status and identify all pre-existing Slice 10 edits.
3. Build a requirement matrix covering tiering, limits, Overview/Progress, Inference Map, Reports, responsive behavior, accessibility, and failure states.
4. Map every requirement to its intended UI, API, database object, and test.
5. Fix the empty `start-project-analysis.test.ts` suite blocker before using the global web test result as a release gate.

Exit gate:

- every signed-off Slice 10 requirement is classified as implemented, partial, missing, conflicting, or intentionally deferred;
- no existing user change has been lost.

### Phase 1 — Shared project shell and dashboard parity

Goal: make every project page use the prototype shell before adding new peer pages.

Tasks:

1. Extract the 2,500-line `ProjectOverview` shell into cohesive components:
   - `ProjectShell`
   - `ProjectHeader`
   - `ProjectSidebar`
   - `ProjectContent`
   - `OsloAdvisorRail`
   - view-specific Overview, Issues, History, Attention, Inference, Reports, and Artifact content
2. Add a central project-navigation registry so desktop sidebar, mobile drawer, breadcrumbs, search, and active states cannot drift.
3. Match the prototype top bar:
   - Intralign brand;
   - real project switcher;
   - sample marker when applicable;
   - current-view breadcrumb;
   - five-band Outcome Confidence pill;
   - search, collaboration/export/report/notification actions;
   - plan badge and account access.
4. Match the desktop three-column structure:
   - persistent left sidebar;
   - central project surface at the prototype measure;
   - persistent OSLO advisor rail unless an issue/detail panel temporarily replaces it.
5. Replace the numeric `/100` Overview hero with the signed-off maturity ramp and grounding qualifier.
6. Replace the old Progress panel with the signed-off fraction hero and foundation bar.
7. Implement state-based ordering: Start Here leads before first value; Progress leads after first value.
8. Match prototype spacing, border, typography, color, density, hover, active, and focus states.
9. Convert the sidebar to the prototype drawer behavior at narrow widths instead of hiding important destinations.

Tests:

- component tests for navigation registry and active state;
- component tests for first-value ordering;
- component tests proving no `/100` hero remains;
- desktop/tablet/mobile shell E2E;
- keyboard and focus-order checks.

Exit gate:

- Overview matches the supplied prototype dashboard at the same desktop viewport;
- all project routes render through the same shell;
- OSLO remains reachable on every project page.

### Phase 2 — Context-item provenance foundation

Goal: create the single factual source needed by both Progress and Inference Map.

Tracer bullet:

> Persist one real context item from analysis, expose it through a project provenance endpoint, and render it in one Inference Map artifact row.

Data model:

- `context_items`
  - workspace and project scope;
  - source analysis run and snapshot;
  - artifact type;
  - item type: claim, assumption, relationship, entity, metric, or interpretation;
  - text/value;
  - evidence reference or null when inferred;
  - source attribution;
  - load-bearing metadata derived from current issues/read relationships;
  - created and superseded timestamps.
- optional normalized support links only if required by the signed-off data contract.

Implementation:

1. Extend structured analysis output so context items are explicit rather than reverse-engineered from prose.
2. Validate every non-null evidence reference against the supplied evidence allowlist.
3. Persist context items transactionally with the published assessment snapshot.
4. Preserve last-good semantics: a failed run cannot replace the current provenance plane.
5. Add a project-scoped API read model containing:
   - per-artifact grounded/inferred totals;
   - false-confidence verification candidates;
   - ordered unbacked assumptions and dependent issue links;
   - unconfirmed dependencies;
   - unowned parties;
   - untraceable numbers;
   - this-week user-grounded and OSLO-inferred counts;
   - empty and insufficient-data states.
6. Reuse this projection for the Overview Progress fraction and provenance split.

Tests:

- tenant isolation and RLS;
- citation allowlist enforcement;
- null evidence means inferred;
- attested evidence means grounded;
- failed analysis preserves the last-good projection;
- count consistency across Overview and Inference Map.

Exit gate:

- the UI receives no invented or duplicated provenance counts;
- the same API projection drives all provenance surfaces.

### Phase 3 — Inference Map route and experience

Goal: make Inference Map a complete peer project view.

Tasks:

1. Add `/projects/[projectId]/inference`.
2. Add Inference Map to the shared navigation registry between Attention Map and Reports.
3. Build the prototype sections:
   - title and `Where OSLO inferred` subtitle;
   - neutral verification flag naming the artifact to inspect;
   - By document rows with one pip per item;
   - Grounded and From OSLO legend;
   - load-bearing-first assumptions register;
   - Structure facts;
   - This week grounding/inference movement.
4. Make artifact rows open the corresponding artifact workspace.
5. Make linked assumption dependencies open the corresponding issue.
6. Keep marks neutral: inferred is not an error and rising inference is not automatically regression.
7. Add loading, empty, no-assumptions, partial-data, stale, and API-failure states.
8. Add accessible names, keyboard activation, tooltip alternatives, and non-color-only distinctions.

Tests:

- route/auth/tenant behavior;
- per-artifact count rendering;
- false-confidence flag appearance and retirement;
- assumption ordering;
- structural facts omit uncomputable zeroes;
- artifact and issue deep links;
- empty/error/last-good behavior;
- desktop and mobile visual regression.

Exit gate:

- Inference Map is visible, navigable, data-backed, and visually matched to the supplied prototype.

### Phase 4 — Readout reading surface

Goal: replace the partial textarea draft with the signed-off Reports experience.

Tasks:

1. Keep `/projects/[projectId]/reports` as a peer workspace.
2. Match the prototype's slim Readout toolbar:
   - editor actions;
   - Recipient;
   - Sections;
   - Format;
   - Schedule;
   - Send;
   - Export.
3. Keep all popovers closed by default and return focus correctly on Escape.
4. Render one continuous reader-facing document at a comfortable measure.
5. Generate the fixed seven-section order:
   - Summary;
   - What changed;
   - Key risks;
   - Assumptions;
   - Plan of action;
   - Decisions needed;
   - Appendix.
6. Enforce the content rules:
   - risk consequence for the plan and for the goal;
   - PM-owned first-person plan of action;
   - only the ask/decision section changes by recipient;
   - no internal OSLO assessment vocabulary in OSLO-authored prose;
   - no health, readiness, RAG, or probability framing;
   - visible analysis-currency attribution;
   - triggered forecast note is non-blocking and not resident by default.
7. Use the same rich-document editor engine as artifacts:
   - continuous contenteditable document;
   - bold, italic, underline, lists, links, tables;
   - undo/redo;
   - slash menu;
   - find/replace;
   - sanitized paste;
   - block reordering;
   - keyboard parity.
8. Explicitly disable artifact-only semantics in Readout:
   - no issue stepper;
   - no artifact provenance chips in the body;
   - no artifact reanalysis commit;
   - no confidence movement.

Tests:

- seven-section structure;
- audience invariance outside the ask;
- rich-content round trip;
- no analysis request during open/edit/export/send;
- no banned framing in generated body;
- responsive toolbar/popovers;
- keyboard editor behavior.

Exit gate:

- the visible Reports workspace matches the prototype and edits as one document rather than seven textareas.

### Phase 5 — Durable Readouts, memo snapshots, delivery, and schedules

Goal: replace all client-local and simulated behavior with honest durable behavior.

Data model:

- `readouts`
- `readout_sections`
- `memo_snapshots`
- `memo_deliveries`
- `report_schedules`

Required properties:

- every object is workspace/project scoped;
- a Readout references a completed analysis snapshot;
- PM edits retain authorship separately from OSLO-generated seed content;
- a memo snapshot stores immutable bytes/content plus source analysis and currency marker;
- delivery points to one exact memo snapshot;
- schedule stores recipient, cadence, timezone, status, and next run;
- History references the exact frozen memo.

API:

- get/create current Readout;
- update sections with optimistic concurrency;
- freeze memo snapshot;
- list/open memo snapshots;
- export exact snapshot;
- send exact snapshot;
- create/update/disable schedule;
- open a scoped, revocable read-only memo link.

Behavior:

1. Free users can read, edit for the current session, manually send/share, and export the seed snapshot.
2. Basic can persist custom wording and optional sections according to ratified limits.
3. Manual send is never seat-metered.
4. Schedule automation checks the plan at execution time.
5. If the source analysis is no longer current, the outgoing memo is clearly marked `previous analysis`.
6. Schedule/send/export never trigger analysis.
7. If no delivery provider is configured, show an explicit unavailable state—never a false success.
8. Delivery failures are retriable and do not mutate the frozen memo.

Tests:

- immutable snapshots;
- optimistic-write conflicts;
- exact-byte reopen from History;
- stale currency marker;
- delivery retry/idempotency;
- schedule timezone and disabled state;
- provider-unavailable state;
- Free/Basic entitlement boundaries;
- tenant isolation and RLS.

Exit gate:

- reload preserves entitled Readout state;
- History opens exact sent bytes;
- no UI claims an external send occurred when it did not.

### Phase 6 — Complete Slice 10 tiering and limits audit

Goal: ensure the rest of Slice 10 is not visually complete but behaviorally incomplete.

Audit and close:

1. Active-project caps and upgrade-or-archive recovery.
2. Seat limits without limiting evidence/reviewer access.
3. Document count and word-envelope behavior.
4. Monthly analysis budget and last-good behavior.
5. Assisted-apply cap behavior and always-available manual editing.
6. Free `Update now` behavior.
7. No latency/priority-queue selling.
8. No outcome-based pricing.
9. Downgrade preserves understanding and never deletes data.
10. Every displayed plan value comes from one tier-definition source.
11. Ratified values are enforced; owner-unset values are not invented.
12. Payment and subscription UI clearly distinguish simulation, configured provider behavior, and unavailable behavior.
13. Word budgets, prompt placement, and duplicate explanations.

Exit gate:

- a completed requirement matrix has no unexplained `partial` or `missing` row.

### Phase 7 — Verification and visual convergence

Automated:

1. API unit tests and Ruff.
2. Database integration tests against local Supabase.
3. Web unit tests, ESLint, and production build.
4. E2E happy/failure paths for every Slice 10 workstream.
5. Accessibility checks for semantic structure, labels, focus, keyboard access, reflow, and reduced motion.
6. Visual snapshots at matched desktop, tablet, and mobile viewports.

Visual convergence loop:

1. Capture the prototype and implementation at the same viewport and state.
2. Compare them side-by-side.
3. Correct layout, spacing, typography, borders, density, colors, overflow, and states.
4. Repeat until no material mismatch remains.

Required captured states:

- Overview with OSLO rail;
- Outcome Confidence popover;
- Progress foundation bar;
- Inference Map top and lower sections;
- Reports default reading surface;
- Reports recipient/sections/schedule popovers;
- frozen memo preview;
- Free limit prompt;
- Basic plan state;
- tablet and mobile navigation.

Exit gate:

- all automated gates pass;
- there are no console or page errors;
- the implementation and prototype screenshots have no material structural mismatch.

## 6. Final acceptance checklist

### Dashboard

- [ ] Shared prototype-matched project shell.
- [ ] All six project destinations visible.
- [ ] OSLO advisor rail present on desktop and reachable everywhere.
- [ ] Five-band Outcome Confidence presentation; no misleading `/100` hero.
- [ ] Signed-off Progress fraction and provenance foundation bar.
- [ ] Correct Start Here/Progress order by state.

### Inference Map

- [ ] Dedicated route and active navigation state.
- [ ] Real context-item projection.
- [ ] By-document grounded/inferred pips.
- [ ] Neutral verification flag.
- [ ] Load-bearing-first assumptions.
- [ ] Structure and weekly movement.
- [ ] Artifact and issue deep links.
- [ ] Honest empty, partial, stale, and failure states.

### Reports

- [ ] Dedicated Reports workspace.
- [ ] One continuous rich Readout document.
- [ ] Seven signed-off sections.
- [ ] Recipient changes only the ask.
- [ ] PM action wording preserved.
- [ ] No health/forecast/internal-OSLO framing.
- [ ] Persistent entitled edits.
- [ ] Immutable memo snapshot.
- [ ] Exact snapshot export/share/send.
- [ ] Durable scheduling with send-time currency check.
- [ ] History reopens exact bytes.
- [ ] No report path runs analysis.

### Tiering and limits

- [ ] Same analysis quality on every plan.
- [ ] Only labour/capacity/convenience levers are gated.
- [ ] Manual understanding paths remain available.
- [ ] Downgrade preserves all understanding.
- [ ] No invented tier values.
- [ ] Billing behavior is honest about simulation/configuration.

### Quality

- [ ] API tests and Ruff pass.
- [ ] Database integration tests pass.
- [ ] Web tests, ESLint, and build pass.
- [ ] E2E tests pass.
- [ ] Desktop/tablet/mobile visual checks pass.
- [ ] Keyboard, focus, reflow, and reduced-motion checks pass.

## 7. Final report format

The completion report will contain:

1. Executive verdict: complete, complete with named exceptions, or incomplete.
2. Requirement-by-requirement pass/fail matrix.
3. Before/after screenshots for Overview, Inference Map, and Reports.
4. Architecture and migration summary.
5. Routes and major files changed.
6. Tests run with exact results.
7. Accessibility and responsive findings.
8. Remaining production dependencies, if any.
9. No-secrets statement.
