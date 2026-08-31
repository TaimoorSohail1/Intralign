# R2 Your Outcome page — final implementation plan

Status: Approved planning baseline based on the grill-me recommendations. This document is an implementation proposal, not ratified doctrine. No application code was changed while creating it.

## 1. Requirement

Users need a dedicated **Your Outcome** dashboard that matches the R2 prototype. Selecting Your Outcome must no longer open the Intent artifact. The dashboard must explain where the outcome stands, what changed, what needs the user, and what is moving with collaborators, while keeping every governed write in Intent, Issues, or the existing outcome-management flows.

## 2. Shared understanding

### In scope

- A dedicated `/projects/{projectId}/outcome` page.
- `/projects/{projectId}/roll-up` redirects to the new canonical route.
- One visible **Your Outcome** workspace-navigation item; the duplicate Roll-up item is removed.
- The prototype page hierarchy, actions, empty states, themes, responsive behavior, and OSLO context.
- Primary, visible-secondary, and held-secondary outcomes.
- Evidence-backed outcome ranking and explanation.
- Durable disclosure, dismissal, and last-looked state.
- Outcome Integrity, change deltas, Needs you, and In motion.
- Governed deep links to Intent, Issues, History, reviewer state, and capacity choices.
- Server-side permissions, integration tests, visual QA, accessibility checks, and regression coverage.

### Out of scope

- A new assessment score or dashboard-only truth.
- Editing evidence, artifacts, or issue state directly inside the dashboard.
- Silent primary-outcome changes.
- Changing tier names, prices, or canonical capacity limits.
- Replacing the Intent editor, Issues workflow, History, Grounding Map, or OSLO advisor.

## 3. Locked decisions from the grill

1. Canonical route: `/outcome`; `/roll-up` becomes a compatibility redirect.
2. Your Outcome is a read-only projection. Every governed mutation happens on its canonical surface.
3. **Manage in Intent** and **Declare an outcome** open Intent with the correct outcome row focused.
4. Lifecycle and optimization are distinct: an outcome can be active or archived, and separately optimized or recorded.
5. Declaring is free; optimizing more than the current entitlement permits invokes the named capacity choice.
6. Inferred secondaries remain held through first-run activation. Automatic disclosure eligibility starts after unlock plus one additional governed action; **Review now** remains available.
7. Secondary detection uses a high-confidence standard: explicit, independently measurable end states only.
8. Primary ranking requires an evidence-backed rationale. Low-confidence selection is presented for user confirmation rather than asserted as fact.
9. Disclosure and dismissal persist per user and project across sessions.
10. Deep Analysis never silently replaces a disclosed outcome. It creates a proposed refinement for user acceptance.
11. Changing the primary outcome marks dependent inferred content stale, preserves the last-good read, records History, and follows governed reanalysis.
12. “Since you last looked” is marked seen only after the complete dashboard renders successfully.
13. Owners and delegates receive the full projection; collaborators/viewers receive read-only access; scoped external reviewers cannot enter the page.
14. Needs you contains unresolved, unrouted decisions ranked by exposure. Critical items lead; lower-stakes items are collapsed behind an honest count.
15. In motion distinguishes awaiting evidence, response received/analysis pending, and grounded after reanalysis.
16. Stale or failed analysis keeps the last-good projection visible with explicit status and recovery.
17. Integrity pillars open Issues filtered to the selected pillar.
18. Full History opens History focused on events since the previous successful dashboard view.
19. The dashboard never directly changes evidence, resolves issues, or starts analysis.
20. Release requires desktop/mobile, dark/light, keyboard/accessibility, real-document, and full Slice 1–8 regression verification.

## 4. Information architecture

### Workspace navigation

- Issues
- Your Outcome
- Grounding Map
- Attention Map
- Reports
- History

Intent remains under **Documents → Understanding**.

### Navigation rules

- Workspace **Your Outcome** → `/projects/{projectId}/outcome`.
- Masthead outcome anchor → `/projects/{projectId}/outcome`.
- Legacy `/projects/{projectId}/roll-up` → server redirect to `/outcome`.
- **Manage in Intent** → `/artifacts/intent?focus=primary-outcome&return=outcome`.
- **Declare an outcome** → `/artifacts/intent?new=outcome&return=outcome`.
- **Review now** → `/artifacts/intent?review=held-outcomes&return=outcome`.
- Needs you/In motion rows → the exact Issue route and item anchor.
- Pillar cards → Issues with a pillar filter.
- Full History → History with a since-last-looked focus.

Back/return state must preserve the dashboard scroll position where practical.

## 5. Target UI

### Shell

- Prototype-centered content column.
- Existing left navigation and document groups.
- Fixed OSLO rail on desktop; collapsible drawer on smaller screens.
- Breadcrumb `Outcome › Your Outcome` and masthead context `The read`.
- Existing workspace-open banner reused without duplication.

### Page sections

1. **Page heading**
   - `Your Outcome`
   - `at a glance — where it stands, and what needs you`

2. **Outcome definition card**
   - Primary outcome and provenance.
   - Project label.
   - Visible secondaries after disclosure.
   - Evidence-backed primary rationale.
   - Held-outcome count and Review now path.
   - Goal, success-criteria, and KPI counts from Intent.
   - Manage in Intent action.

3. **Declare outcome**
   - Always enabled and labelled free.
   - Opens Intent rather than creating a second editor.
   - A subsequent optimization attempt can open the named Basic capacity choice.

4. **Since you last looked**
   - Up to three real unseen changes.
   - Full History action.
   - Hidden when there are no unseen changes.

5. **Outcome Integrity**
   - Current band and session trend.
   - Grounding, Adaptability, and Viability.
   - Limiting gate.
   - Grounded-detail progress.
   - “Maturity, not a forecast.”

6. **Needs you**
   - True total count.
   - Critical or top two items visible first.
   - Honest lower-stakes disclosure with `aria-expanded`.
   - Rows deep-link to Issues.

7. **In motion**
   - Awaiting reviewer evidence.
   - Response received and analysis pending.
   - Grounded/attributed after reanalysis.
   - Accurate empty state.

8. **Projection footer**
   - Explains that the page is read-only and that decisions are made and recorded on governed surfaces.

9. **OSLO advisor**
   - Session context: `On Your Outcome`.
   - Explains the current state and recommends the next governed destination.
   - Never acts from chat without the existing governed action flow.

## 6. Domain and persistence design

### Outcome state

The outcome contract must represent two independent concerns:

- `lifecycle_status`: `active | archived`
- `optimization_status`: `optimized | recorded`

Additional persisted/derived fields:

- `is_primary` — singleton among active outcomes;
- `provenance` — declared or inferred;
- `disclosure_status` — held or visible;
- `ranking_rationale` and supporting evidence references;
- `refinement_status` — current or proposed;
- created/updated/archived timestamps.

The capacity policy counts optimized outcomes, not merely recorded declarations. Archive remains reversible and must never be used as a synonym for “declared but not optimized.”

### Per-user project state

Persist:

- held-outcome disclosure time;
- disclosure-nudge dismissal time;
- last successful dashboard-view time;
- optional last focused dashboard section for return navigation.

### Analysis contract

Fast Pass returns:

- one confirm-ready primary candidate;
- zero or more high-confidence secondary candidates;
- per-candidate provenance and evidence references;
- an evidence-backed primary-selection rationale;
- a low-confidence flag when human confirmation is required.

Deep Analysis may propose refinements but cannot silently overwrite an accepted outcome.

## 7. Outcome dashboard projection

Create one server-authored projection so the UI does not independently recompute counts.

Suggested response shape:

```text
OutcomeDashboardProjection
  project
  freshness
  primary_outcome
  visible_secondary_outcomes[]
  held_outcome_count
  disclosure_eligibility
  intent_counts
  integrity
  unseen_changes[]
  needs_you[]
  in_motion[]
  role_capabilities
  deep_links
```

The projection must reuse the same authoritative sources as Issues, History, Grounding Map, reviewer state, and the OSLO rail.

### Reads

- Current/last-good analysis snapshot.
- Persisted project outcomes.
- Intent artifact counts.
- History and unread read-moved events.
- Current issue lifecycle state.
- Reviewer routing and response state.
- Workspace entitlement and current user role.

### Writes kept outside the projection

- Declare outcome.
- Disclose/dismiss held outcomes.
- Set primary outcome.
- Archive/reactivate.
- Accept a proposed refinement.
- Record a capacity choice.
- Mark the dashboard successfully viewed.

The projection handler itself has no write-capable dependency except the narrowly separated “mark viewed” acknowledgement after successful rendering.

## 8. User flows

### Flow A — open Your Outcome

1. Select Your Outcome.
2. Load the last-good projection.
3. Render the full dashboard.
4. Acknowledge the successful view and mark only the displayed deltas seen.
5. OSLO updates its visible context without changing the read.

### Flow B — manage the primary outcome

1. Select Manage in Intent.
2. Intent opens with the primary outcome focused.
3. User edits or confirms through the existing governed action.
4. Dependent inferred items become stale.
5. History records the act and governed reanalysis starts.
6. Return to Your Outcome with last-good/stale state until reanalysis lands.

### Flow C — review held outcomes

1. Select Review now.
2. Held outcomes open in Intent with evidence-backed rationale.
3. User accepts, refines, defers, or rejects each candidate.
4. Disclosure state persists.
5. Returning to Your Outcome shows only the accepted visible outcomes.

### Flow D — declare an outcome

1. Select Declare an outcome.
2. Intent opens with a blank secondary-outcome row focused.
3. Saving creates a recorded, declared outcome for free.
4. If the user asks OSLO to optimize beyond the entitlement, show the named capacity choices.
5. Every capacity branch records an intent signal.

### Flow E — act on Needs you

1. Select a row.
2. Open the exact Issue and relevant section.
3. User takes the governed action there.
4. Dashboard remains last-good/stale until reanalysis lands.
5. The row changes only from authoritative issue/reanalysis state.

### Flow F — follow In motion

1. Select a reviewer row.
2. Open the exact Issue/reviewer context.
3. Awaiting remains until response.
4. Response becomes analysis pending.
5. Grounded state appears only after reanalysis lands.

## 9. Empty, loading, stale, and error states

- **Loading:** stable skeleton preserving the final layout; no full-page jump.
- **No outcome:** honest state with `Define your outcome in Intent`.
- **No unseen changes:** omit the delta ribbon.
- **No Needs you:** positive but factual settled state.
- **No In motion:** explain that routed/reviewer work appears here.
- **Stale:** retain last-good projection with pending-change count and reanalysis status.
- **Reanalysis failed:** retain last-good projection, explain failure, provide retry where authorized.
- **Projection unavailable:** bounded error with retry and safe navigation to Issues/Intent.
- **Unauthorized reviewer:** server-enforced 403 or safe project boundary; never render then hide.

## 10. Accessibility and responsive requirements

- Semantic headings, regions, lists, links, and buttons.
- Keyboard-accessible rows; no clickable `div` elements.
- Visible focus, logical reading/focus order, and restored focus after return.
- `aria-expanded` and controlled-region references for lower-stakes disclosure.
- Text labels and icons in addition to color for every state.
- Accessible progress labels for grounding and integrity.
- Status/error messages use appropriate live-region behavior without announcing the whole dashboard.
- Reduced-motion support.
- 200% zoom without clipped actions or horizontal page overflow.
- Mobile: single-column cards, compact outcome card, horizontally safe pills, and OSLO drawer.
- Dark and light themes use shared semantic tokens across every section.

## 11. Delivery plan

### Tracer bullet — navigation to real projection

Goal: prove the full route/API/UI path before adding breadth.

- Add failing navigation and redirect tests.
- Add `/outcome` route and `/roll-up` compatibility redirect.
- Return a minimal server projection with primary outcome and Integrity.
- Render the page heading and primary card.
- Verify owner permissions, failure handling, and no-write behavior.

### Work item 1 — align the outcome contract

- Separate lifecycle from optimization.
- Add disclosure, rationale, and proposed-refinement fields/state.
- Migrate existing outcomes without changing their visible meaning.
- Add repository and API tests for active/archived, optimized/recorded, and primary singleton invariants.

### Work item 2 — produce the dashboard projection

- Aggregate outcomes, Intent counts, freshness, Integrity, deltas, Issues, and reviewer state.
- Apply role scoping and generate exact deep links.
- Add pinned no-write and projection-consistency tests.

### Work item 3 — correct the workspace navigation

- Point Your Outcome and the masthead anchor to `/outcome`.
- Remove the duplicate visible Roll-up item.
- Keep Intent under Documents.
- Add desktop/mobile navigation regression tests.

### Work item 4 — build the outcome card and Intent hand-offs

- Primary/secondary/held variants.
- Manage, Declare, Review now, and return-navigation flows.
- Low-confidence and proposed-refinement states.
- Tests for focus, URL state, persistence, and error recovery.

### Work item 5 — build deltas and Integrity

- Since-you-last-looked semantics and acknowledgement.
- Integrity band, trend, pillars, limiting gate, and progress.
- Pillar-to-filtered-Issues and History links.
- Cross-route count-consistency tests.

### Work item 6 — build Needs you and In motion

- Exposure ranking and lower-stakes disclosure.
- Reviewer lifecycle states and issue deep links.
- Empty states and role wording.
- Tests covering routing, response, analysis-pending, and grounded transitions.

### Work item 7 — prototype fidelity and accessibility

- Match geometry, hierarchy, typography, borders, badges, meters, and spacing.
- Dark/light, desktop/mobile, zoom, keyboard, focus, screen-reader labels, and reduced motion.
- Matched-viewport prototype comparisons before sign-off.

### Work item 8 — regression and release evidence

- Run component, API, integration, doctrine-guardrail, and production-build checks.
- Run desktop/mobile E2E.
- Test real documents covering the required data states.
- Produce a manual QA report with screenshots and known limitations.

## 12. Test matrix

### Component

- Primary-only, held-secondary, visible-secondary, and no-outcome cards.
- Read-only permissions and disabled/unavailable destinations.
- Deltas, Integrity, Needs you, In motion, stale, error, and empty states.
- Lower-stakes expansion, focus, and accessible labels.

### API and persistence

- Primary singleton.
- Declared-recorded outcome succeeds without consuming an optimization slot.
- Optimization capacity invokes the named gate.
- Archive/reactivate remains reversible.
- Disclosure/dismissal persists per user/project.
- Last-looked acknowledgement marks only delivered events.
- Deep Analysis produces proposals rather than silent replacement.
- Owner/delegate/collaborator/viewer/external-reviewer authorization.
- Projection reads emit no domain write or analysis run.

### End to end

- Your Outcome navigation never opens Intent.
- Legacy Roll-up URL redirects correctly.
- Manage/Declare/Review return flows.
- Primary change → stale → reanalysis → updated dashboard and History.
- Needs you → Issue action → updated state after reanalysis.
- Reviewer request → response → analysis pending → grounded.
- Full History and pillar-filter navigation.
- Dark/light persistence, desktop/mobile, keyboard-only, reload, and failure recovery.

### Real-document scenarios

1. One explicit outcome with complete metrics.
2. One explicit outcome with missing success criteria.
3. Multiple explicit outcomes with a clear primary.
4. Ambiguous goal/benefit language that must not inflate outcomes.
5. Critical unresolved issues plus routed and answered reviewer evidence.

For every document, compare Your Outcome, Intent, Issues, History, Grounding Map, and OSLO for identical authoritative state.

## 13. Acceptance criteria

1. Your Outcome has a dedicated route and never redirects to Intent on entry.
2. The visible navigation contains Your Outcome once and no duplicate Roll-up item.
3. The page matches the supplied prototype at matched desktop and mobile viewports.
4. Intent remains the editable canonical home.
5. The dashboard is a server-authored read-only projection.
6. Primary, visible-secondary, held-secondary, provenance, rationale, and Intent counts are accurate.
7. Held outcomes never leak before disclosure.
8. Disclosure and dismissal persist per user/project.
9. Declaring is free; optimization capacity shows named choices and never a raw API error.
10. Primary change is singleton, recorded, stale-producing, and governed by reanalysis.
11. Unseen changes are real, durable, and marked seen only after successful rendering.
12. Integrity and all counts agree across adjacent surfaces.
13. Needs you is exposure-ranked and every row opens the correct Issue.
14. In motion accurately represents reviewer lifecycle state.
15. Merely viewing or expanding the page creates no domain write and starts no analysis.
16. Permissions are enforced server-side.
17. Loading, empty, stale, failed, dark/light, responsive, zoom, keyboard, and reduced-motion states pass.
18. Existing Slice 1–8 tests, doctrine guardrails, lint, and production build remain green.

## 14. Risks and controls

| Risk | Control |
|---|---|
| Lifecycle and optimization remain conflated | Complete the contract/migration work before UI breadth |
| Counts drift across routes | One server-authored projection over authoritative state |
| Dashboard becomes a second write surface | Pinned no-write test and deep links to governed destinations |
| Held outcomes leak during activation | Server-side disclosure state and negative tests |
| Viewing erases unseen changes too early | Acknowledge only after successful full render |
| Reviewer response appears resolved prematurely | Preserve response-received/analysis-pending state until reanalysis lands |
| Prototype styling breaks current shell | Reuse existing shell/tokens and run matched-viewport visual QA |
| Migration changes existing outcome meaning | Backfill deterministically and compare pre/post projections |

## 15. Definition of done

The feature is complete only when:

- every acceptance criterion passes;
- component, API, integration, E2E, doctrine, lint, and production-build checks pass;
- all five real-document scenarios pass without cross-route state drift;
- desktop/mobile and dark/light screenshots match the prototype within the agreed visual tolerance;
- no P0, P1, or P2 UX/accessibility defect remains;
- manual QA confirms every action and return path;
- the final report records evidence, remaining P3 polish, and deployment status.
