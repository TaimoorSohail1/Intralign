# R2 seven-artifact workspace implementation plan

**Status:** Draft implementation plan; planning is owner-directed, but implementation is blocked by the authority gates in Section 1.

**Visual source:** `release-2/oslo-prototype-r2.html`

**Prototype audit:** `code/reports/r2-slice-5-prototype-audit-2026-08-14/REPORT.md`

## 1. Authority and acquisition gates

The conversation calls this work **Slice 5**, but the signed R2 ledger currently defines **R2 Slice 5** as **Multi-Outcome Read & Deferred Disclosure** in `release-2/slices/05-multi-outcome-deferred-disclosure.md`.

The seven-artifact workspace is an existing Release-1 implementation area and a historical Slice-5 design. It must not silently replace the signed R2 Slice 5.

Before code begins, the owner must choose one of these paths:

1. **Recommended:** preserve signed R2 Slice 5 and authorize this as a separately named **R2 Artifact Workspace parity increment**.
2. Explicitly supersede/resequence the signed R2 Slice-5 definition through the repository governance process.

Additional gates:

- Explicitly reopen this increment in `release-2/R2_VERTICAL_SLICE_STATUS_LEDGER.md`.
- Resolve and record the canonical artifact taxonomy change from `Context` to `Constraints`.
- Map every cognitive behavior to an approved contract in the Build/Test/Observe traceability matrix.
- Keep the `r2-vertical-slice-delivery-team` scheduler paused until the plan and acquisition record are approved.
- Do not start while the ledger says `OWNER-BLOCKED`.

## 2. Outcome

Deliver a production seven-artifact workspace that matches the R2 prototype visually and behaviorally while using real project data:

1. Intent
2. Scope
3. Requirements
4. Constraints
5. Work breakdown
6. Schedule
7. Resources

The user can read and edit plan content, distinguish their evidence from OSLO inference and proposals, see the assessment remain stable until reanalysis completes, and work across synchronized execution views without data drift.

## 3. Accepted planning decisions

- The R2 prototype is the visual and interaction reference.
- Use **Constraints**, not **Context**, in the active workspace.
- All seven artifacts use real backend data and are functional.
- `Full plan · export` may be a read-only local aggregation; critical-path computation and live external PM-tool export remain out of this increment.
- Understanding artifacts support Statements and read-only Narrative views.
- Editing is inline and quiet; save after approximately 1.5 seconds of idle time or on blur.
- A committed edit triggers reanalysis automatically; there is no manual Reanalyze button.
- Editing changes content/provenance, not the assessment. Only completed reanalysis changes Viability, Grounding, Adaptability, issues, or finding state.
- Editing an inferred statement makes the edited wording `Confirmed by you`.
- Accepting a proposal adds user-owned content; rejecting removes it from the active proposal queue. Both decisions remain in append-only history.
- Work breakdown, Schedule, and Resources are synchronized views over one approved task identity/model.
- Outcome checkpoints are persisted plan data and affect Adaptability only after reanalysis.
- Non-human resources link to their defining Requirements or Constraints instead of duplicating values.
- OSLO remains contextual and advisory; it cannot modify plan content without an explicit user act.
- The workspace-open banner is first-use, dismissible, and recoverable through the quick tour.
- Owners/editors can edit; viewers/shared-link users are read-only.
- Desktop prototype parity is the first visual target; tablet rail collapse, keyboard access, WCAG 2.1 AA, and non-color state cues are required.
- Production deployment remains human-approved.

## 4. Scope

### In scope

- Three-column R2 workspace shell and persistent navigation.
- Prototype artifact ordering, labels, active states, counts, badges, and right-rail context.
- Artifact-specific editors rather than one generic visual treatment.
- Statements/Narrative modes for Intent, Scope, Requirements, and Constraints.
- Row-level provenance: `Confirmed by you`, OSLO inference, and OSLO proposal.
- Proposal accept/reject integration.
- Inline artifact issue markers and navigation to contextual issue details.
- Work-breakdown hierarchy and WBS/Agile framing.
- Schedule date editing, timeline projection, missing-date states, and outcome checkpoints.
- Resource summaries, task ownership, teammate addition, and non-human dependency links.
- Shared execution synchronization.
- Append-only artifact versions and decision history.
- Automatic reanalysis lifecycle with last-known-good content/read visible.
- Existing-project migration from the active Context taxonomy to Constraints without deleting legacy history.
- Loading, empty, unavailable, conflict, failed-save, stale, and reanalysis states.
- Permission, tenant-isolation, accessibility, responsive, and regression coverage.

### Out of scope

- Changing CAF, Reliability, Viability, Grounding, Adaptability, or Outcome Integrity formulas.
- Critical-path computation.
- Live Asana or other PM-tool synchronization.
- Autonomous OSLO edits or proposal acceptance.
- Replacing artifact content with a finding/recommendation list.
- Deleting or rewriting historical Context/artifact versions.
- Slices 6–10 or unrelated R2 work.
- Production deployment without explicit human approval.

## 5. Governing boundaries

### Commodity UI/platform work

The shell, navigation, direct editing controls, panel layout, responsive behavior, and visual parity are commodity/platform work under the traceability matrix.

### Contracted cognitive behavior

The implementation must remain within these approved contract families:

- `PS-02 / IC-WS-SYNTH`: generated artifacts remain Derived; no autonomous write or Attested-as-truth presentation.
- `PS-04 / IC-WA-002`: artifact versions are append-only and supersession remains traceable.
- `AE-03 / IC-WA-00R`: information changes trigger coalesced recompute with last-known-good preservation.
- `AE-05`: progressive disclosure never presents Unknown as final truth.
- `REC-04 / IC-WI-INTERACT`: suggested fixes remain advisory.
- `CHAT-01…04 / IC-WI-INTERACT`: chat cannot write artifacts or change assessment.
- `OVL-01…03 / IC-WE-DISCLOSE`: issue/CAF overlays remain contextual presentation.

### Stop conditions

Stop and escalate if implementation requires:

- A new cognitive object or unapproved contract.
- A new artifact taxonomy that has not been owner-recorded.
- A persistence model that makes Derived content Attested automatically.
- Editing that changes an assessment without a completed reanalysis.
- Destructive migration of Context or artifact history.
- A new guard identifier or contract-traceability bypass.

## 6. Existing implementation to reuse

The current application already provides useful seams:

- Generic artifact routes and the artifact workspace component.
- `artifact_drafts` and append-only `artifact_draft_versions`.
- Structured `content_json`, revisions, provenance, evidence references, and reliability data.
- Expected-version/idempotency save behavior.
- Reanalysis start/refresh handling.
- Undo/redo, find, issue stepping, proposals, and contextual Ask OSLO actions.
- Project shell, left navigation, OSLO rail, history, and proposal APIs.

Primary areas expected to change:

- `code/shared/epistemic.py`
- `code/shared/entities.py`
- `code/supabase/migrations/`
- `code/backend/responsibilities/infer/synthesis.py`
- Backend artifact/read/edit services and OpenAPI schemas
- `code/apps/web/src/components/artifacts/artifact-workspace.tsx`
- `code/apps/web/src/components/overview/project-overview.tsx`
- Artifact routing, analysis progress, history, and API adapters
- Unit, API, migration, integration, R2 guardrail, and E2E tests

## 7. Data and migration plan

### Taxonomy migration

1. Add `constraints` to the database enum and application DTOs; do not delete or rename historical enum values in place.
2. Update generated planning-artifact types only after the canonical taxonomy decision is recorded.
3. Keep historical `context` versions immutable and visible through History.
4. On the next approved reanalysis, generate Constraints from source-attributed project evidence and explicitly flagged inference; do not mechanically relabel all Context prose as a constraint.
5. Hide Context from the active seven-artifact navigation only when the approved migration/read behavior is available.
6. For an existing project without a Constraints version, show a truthful `Not yet analyzed` state and offer the normal reanalysis path.
7. Add forward and rollback-safe migration tests. Rollback must not destroy Constraints or Context history.

### Understanding content

- Store committed Statements as the editable source.
- Generate Narrative as a read-only projection; do not persist a second editable truth.
- Preserve section/row identifiers, evidence references, provenance, and proposal linkage across revisions.

### Shared execution content

- Establish one approved task identity across Work breakdown, Schedule, Resources, and the read-only combined view.
- Work breakdown owns structural hierarchy; Schedule owns the date/checkpoint facet; Resources owns the assignment facet.
- All facets must update through one approved persistence seam so task identity cannot drift.
- Do not invent a new execution domain object in code. If the existing artifact lifecycle cannot represent the shared seam, obtain an owner-approved contract/model amendment first.
- Every execution mutation creates append-only evidence/version history and triggers at most one coalesced reanalysis.

## 8. API and event plan

- Reuse authenticated, tenant-scoped artifact GET/PATCH boundaries.
- Keep expected-version conflict handling and idempotency keys.
- Support quiet autosave without duplicate versions or duplicate reanalysis runs.
- Return the saved revision immediately; keep the previous assessment visible while reanalysis runs.
- Refresh artifact, issues, pillars, advisor context, and proposal state after the completed run.
- Reuse proposal decision endpoints; never let the browser mutate assessment directly.
- Carry artifact type, section/row identity, provenance, evidence references, and affected execution task identity in typed contracts.
- Preserve append-only `Version Recorded`, recompute, proposal-decision, and history events.
- Enforce owner/editor write permission and viewer/shared-link read-only permission in API and RLS, not only in UI.

## 9. UI implementation plan

### Shared shell

- Match the prototype’s default `266px / flexible center / 330px` desktop structure and centered content measure.
- Keep left navigation, center workspace, and OSLO thread independently usable.
- Match masthead, artifact identity, pillar chips, active states, borders, spacing, typography, and responsive rail states.
- Preserve current real counts and backend-derived copy; do not copy fixture values.

### Understanding artifacts

- Intent: Purpose, Outcomes, Goals, Success criteria, KPIs/metrics, primary outcome treatment, grouped adds.
- Scope: In scope, Out of scope, Edge/undecided, grouped adds.
- Requirements: flat requirement rows, add action, proposal block.
- Constraints: compact hard-limit rows, add action, cross-artifact references.
- Shared: Statements/Narrative toggle, OSLO read, provenance legend, undo/redo, contextual proposals, automatic save/reanalysis state.

### Work breakdown

- Render deliverable → work package → task hierarchy.
- Provide Outline/WBS and Backlog/Agile framing over the same task identities.
- Support inline rename, add/remove, confirm inference, accept/dismiss proposal, and inline warnings.

### Schedule

- Render the shared tasks with owner, start/end inputs, timeline bar, and missing-date state.
- Validate start/end ordering without silently inventing dates.
- Add/remove persisted outcome checkpoints.
- Keep the no-checkpoint Adaptability warning truthful until reanalysis completes.

### Resources

- Render People, Budget, Facility, Vendors, and Equipment summaries.
- Link non-human values to Requirements or Constraints.
- Provide per-task owner selection, unassigned state, provenance, task path, and date range.
- Support teammate addition without granting workspace membership implicitly.

### OSLO rail

- Keep the governed identity, current artifact context, OSLO read, reliability basis, suggested questions, and composer persistent.
- Keep answers evidence-qualified and artifact-specific.
- Never imply that chat edited or accepted content.

## 10. Delivery phases and TDD gates

Each phase uses one observable **RED → GREEN → REFACTOR** behavior at a time.

### Phase 0 — authority, contract, and fixtures

1. Resolve the R2 slice-identity conflict.
2. Record the Constraints taxonomy decision and contract/traceability mapping.
3. Approve the shared execution persistence seam.
4. Define fixture expectations from real sample documents and the R2 prototype.
5. Record acquisition in the R2 ledger; update scheduler scope but leave it paused until implementation approval.

**Gate:** no unresolved doctrine/contract/taxonomy gap.

### Phase 1 — Constraints vertical tracer

Build the smallest end-to-end path:

1. Failing migration/domain/API/web/E2E tests for `constraints`.
2. Add non-destructive taxonomy support.
3. Generate/load one real Constraints artifact.
4. Edit one row, autosave one version, trigger one reanalysis, and reload the persisted result.
5. Prove historical Context remains intact.

**Gate:** one real project completes the full UI → API → persistence → reanalysis → refresh path.

### Phase 2 — shared shell and navigation parity

1. Match the R2 three-column shell at the reference desktop viewport.
2. Implement the seven-artifact order, grouping, active state, counts, and contextual right rail.
3. Add loading, missing, unavailable, and read-only states.

**Gate:** visual comparison and keyboard navigation pass without changing artifact behavior.

### Phase 3 — Understanding artifacts

1. Implement artifact-specific Statements structures.
2. Add read-only Narrative projections.
3. Add quiet autosave, provenance changes, proposals, undo/redo, and contextual issue markers.
4. Verify edits do not change assessment before reanalysis completes.

**Gate:** Intent, Scope, Requirements, and Constraints pass unit, API, E2E, and prototype-parity checks.

### Phase 4 — shared execution tracer and Work breakdown

1. Implement the approved shared task identity/persistence seam.
2. Render WBS hierarchy and Agile framing.
3. Add task CRUD, rename, confirm, proposal decision, and warnings.
4. Prove both framings show identical task identities.

**Gate:** one task mutation is visible in every execution projection without duplicate storage drift.

### Phase 5 — Schedule

1. Render task dates and timeline bars.
2. Implement date validation, clear, missing-date, and unscheduled states.
3. Persist outcome checkpoints and trigger coalesced reanalysis.
4. Verify Adaptability changes only after the completed run.

**Gate:** date and checkpoint workflows persist across reload and appear in the combined view.

### Phase 6 — Resources

1. Render non-human resource summaries and source links.
2. Implement task-owner assignment and unassigned warnings.
3. Add teammate names without changing membership/authorization.
4. Verify ownership changes synchronize everywhere.

**Gate:** Resources, Work breakdown, Schedule, and combined view remain consistent after reload/reanalysis.

### Phase 7 — advisor, resilience, and migration completion

1. Ground the OSLO rail in the selected artifact and evidence.
2. Complete existing-project migration and not-yet-analyzed states.
3. Cover version conflicts, save retry, offline/interrupted reanalysis, last-known-good, and permission failures.
4. Confirm first-use banner/tour persistence.

**Gate:** no destructive migration, unauthorized edit, duplicate run, or false-completion state.

### Phase 8 — full QA and release candidate

1. Run all API/web/unit/integration/migration/guardrail/lint/build checks.
2. Run the seven-artifact real-document E2E journey.
3. Capture matched-state prototype/application screenshots at the same viewport.
4. Perform keyboard, focus, reduced-motion, 200%-zoom, tablet, and mobile/no-overflow checks.
5. Review security, privacy, tenant isolation, error handling, and append-only history.
6. Update the R2 ledger with current-run evidence.

**Gate:** human code review and manual QA approve; deployment remains a separate explicit owner action.

## 11. Kanban-ready work items

1. Resolve R2 artifact-workspace increment identity and traceability.
2. Add non-destructive Constraints taxonomy and migration.
3. Generate and expose Constraints from real evidence.
4. Replace the generic workspace chrome with R2 shell parity.
5. Build Intent Statements/Narrative behavior.
6. Build Scope Statements/Narrative behavior.
7. Build Requirements Statements/Narrative behavior.
8. Build Constraints Statements/Narrative behavior.
9. Introduce the approved shared execution persistence seam.
10. Build Work-breakdown WBS/Agile views.
11. Build Schedule dates, bars, and checkpoints.
12. Build Resources summaries and owner assignment.
13. Build the read-only combined plan projection.
14. Integrate contextual OSLO reasoning and proposal actions.
15. Complete existing-project compatibility and failure states.
16. Add accessibility, responsive, visual-regression, and real-document E2E coverage.
17. Run full regression, human review, manual QA, and ledger evidence update.

Every work item must include its contract/commodity classification, positive acceptance test, negative invariant test, observability expectation, and screenshot/manual-evidence expectation where applicable.

## 12. Test matrix

### Positive

- All seven artifacts load from real project data.
- Understanding edits autosave once and create one new version.
- Reanalysis starts once and refreshes the read after completion.
- Proposals accept/reject across relevant surfaces.
- Narrative reflects committed Statements and is not independently editable.
- WBS/Agile share identities.
- Dates, checkpoints, and owner changes survive reload.
- Execution changes synchronize across all projections.
- Legacy projects gain Constraints through the approved reanalysis path.
- Owners/editors can edit; viewers can read.

### Required negative tests

- Context history is never deleted or rewritten.
- Derived content is never labeled Attested/Confirmed without a user act.
- Editing does not change assessment before reanalysis.
- OSLO chat never writes, accepts, rejects, or changes assessment.
- A stale expected version cannot overwrite a newer revision.
- Repeated autosave/idempotency keys do not create duplicate versions or runs.
- Schedule cannot invent dates or silently repair invalid input.
- Schedule/Resources cannot create duplicate tasks.
- Non-human resource values are not duplicated into a competing source of truth.
- Viewer/shared-link users cannot mutate through UI, API, or direct database access.
- A failed or interrupted run cannot replace last-known-good results.
- No unapproved Slice 6–10 behavior is introduced.

### Visual/manual

- Matched viewport/state comparison for every artifact and both Work-breakdown framings.
- Desktop, tablet, narrow/mobile, and 200%-zoom-equivalent reflow.
- Independent scroll regions, sticky composer, and no horizontal overflow.
- Keyboard order, visible focus, Escape/close restoration, and hover/focus parity.
- WCAG 2.1 AA contrast and text/icon cues for provenance and warnings.
- Reduced-motion behavior.

## 13. Scheduler plan

The current automation is paused and authorizes only Slices 1–4. After Phase-0 approval:

1. Update its mission to the exact authorized artifact-workspace increment name and scope.
2. Point it to this plan plus the R2 ledger and prototype audit.
3. Preserve the rule: resume existing in-progress work before acquiring another item.
4. Permit one public behavior per run using RED → GREEN → REFACTOR.
5. Require scoped tests on each run and full regression only at defined gates.
6. Require same-run ledger evidence.
7. Keep push, merge, deployment, canonical changes, and self-ratification prohibited.
8. Resume only after explicit owner instruction; pause again when the increment is complete or blocked.

## 14. Definition of done

- Authority, taxonomy, and contract gates are resolved and recorded.
- The seven active artifacts use the approved prototype names and order.
- All artifacts are functional with real data.
- Context history is preserved; Constraints is generated truthfully.
- Provenance, proposals, editing, autosave, versions, reanalysis, and history obey the epistemic invariants.
- Work breakdown, Schedule, Resources, and combined view cannot drift.
- All positive and negative tests pass.
- Slices 1–4 regression passes.
- Current-run visual evidence matches the prototype with no open P0/P1/P2 mismatch.
- Accessibility, responsive, permission, security, migration, and recovery checks pass.
- Human review and manual QA are complete.
- The R2 ledger contains fresh evidence.
- Production deployment occurs only after a separate explicit owner instruction.

## 15. Implementation start point

After the owner resolves the identity gate and explicitly reopens the increment, start with **Phase 1: the Constraints vertical tracer**. It is the smallest end-to-end behavior that proves the taxonomy, migration, real-data generation, editing, append-only versioning, reanalysis, UI, and regression path before broader visual work begins.
