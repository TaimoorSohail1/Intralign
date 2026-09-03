# Five-PDF End-User QA Plan

## Objective

Test Intralign as a real end user using a fresh, coherent five-document business
project. Verify whether the LLM places complete and accurate data in the correct
sections and whether every Slice 1-10 workflow works end to end.

This is an audit only. No application code will be changed during testing.

## Controlled business project

Create five text-native, table-rich PDFs for one realistic project:
`Atlas B2B Commerce Launch`.

1. **Executive Charter and Benefits Case**
   - purpose, objectives, success measures, funding ceiling, constraints
2. **Stakeholder and Governance Plan**
   - stakeholders, decision rights, governance forums, approvals, budget owner
3. **Scope, Requirements and Acceptance Specification**
   - inclusions, exclusions, deliverables, functional/non-functional requirements,
     acceptance criteria
4. **Delivery, Schedule, Resources and RACI Plan**
   - work packages, milestones, dependencies, owners, allocations, vendors, RACI
5. **RAID, Status, Change and Decision Log**
   - risks, issues, assumptions, dependencies, decisions, changes and current status

The pack will intentionally include:

- one explicit scope exclusion;
- one dated dependency conflict;
- one budget conflict;
- four explicit assumptions;
- one unowned action;
- one unconfirmed dependency;
- one ambiguous numeric target;
- named owners, backups, milestones and acceptance criteria.

These controlled cases make it possible to test whether the LLM preserves,
misplaces, compresses, invents or loses information.

## Ground-truth oracle

Before upload, create a manifest containing every expected fact and its correct
destination:

- expected artifact;
- expected section;
- exact source PDF and page;
- expected provenance state;
- whether it is an assumption, conflict, issue or ordinary confirmed row.

Each extracted item will be classified as:

- Correct
- Missing
- Misplaced
- Compressed/lost detail
- Unsupported/invented
- Wrong provenance
- Conflict not retained

## Test sequence

### Phase 1 - Clean setup

- Confirm frontend, API, database and Mailpit health.
- Create a fresh project so previous Northstar data cannot affect results.
- Record initial workspace project count and plan limits.
- Use a dedicated local reviewer identity.

### Phase 2 - Slice 1: Access and onboarding

- Create an invitation.
- Verify Mailpit delivery and activation link.
- Test accepted/repeated/revoked link behavior.
- Log in, stay signed in, log out and return.
- Confirm role and workspace isolation.

### Phase 3 - Slice 2: Intake and analysis

- Select all five PDFs.
- Verify filename, count, size/type handling and upload progress.
- Confirm empty intake cannot start.
- Start analysis and observe Fast Pass.
- Refresh during an active run and verify reconnect.
- Wait for Extended Analysis to supersede the provisional read.
- Confirm all five source documents are represented.
- Record provider/model metadata, duration, retries and safe failures.

### Phase 4 - Slices 3 and 4: Overview and Attention Map

- Verify project name, confidence, CAF dimensions and reliability explanation.
- Check grounded/inferred progress against structured row states.
- Open ranked issues and evidence.
- Ask OSLO project-specific questions and assess factuality.
- Submit one clarification and verify re-analysis/history/version updates.
- Test the Attention Map in both views.
- Open cells, verify issue filtering and return/scroll behavior.
- Check keyboard and narrow-screen behavior.

### Phase 5 - Slice 5: Seven artifacts

Audit every artifact against the ground-truth manifest:

- Intent
- Context
- Scope
- Requirements
- Work breakdown
- Schedule
- Resources

For every section verify:

- correct heading and representation;
- complete rows and columns;
- correct placement;
- source/page evidence;
- confirmed/inferred/conflicting/unknown state;
- assumptions and conflicts;
- issue links and badges;
- version number;
- add, edit, delete and reorder behavior without losing row metadata.

Any edit will use clearly marked QA text and will be reverted through the UI when
possible. Re-analysis must preserve the user's draft.

### Phase 6 - Slices 6, 7 and 8

**Issues**

- Search, group and filter by artifact, CAF dimension, severity and status.
- Open evidence and suggested actions.
- Answer a clarification and verify status behavior.

**History**

- Verify initial, Extended, clarification, version and decision events.
- Open retained snapshots and confirm they are read-only.
- Check filters and current/historical labels.

**Workspace**

- Verify project card, project switcher, breadcrumbs and notifications.
- Mark notifications read and confirm no analysis starts.
- Check appearance/settings and project-limit messaging.

### Phase 7 - Slices 9 and 10

**Collaboration and review**

- Create a scoped reviewer link.
- Open it without a workspace session.
- Verify read-only access and clearly labelled Outcome Confidence out of 100.
- Submit a review response and confirm the History event.
- Revoke the link and confirm access is denied afterward.
- Check desktop and mobile layouts.

**Inference Map**

- Verify per-artifact counts reconcile with artifact row states.
- Verify the four planted assumptions appear without invented assumptions.
- Check unconfirmed dependencies, unowned parties and untraceable numbers.
- Follow links back to artifacts/issues.

**Reports**

- Verify Summary, What changed, Key risks, Assumptions, Plan of action,
  Decisions needed and Appendix.
- Change recipient and section selections.
- Test edit, undo, redo, find and formatting controls.
- Verify five source documents are not reported as seven documents.
- Test send/schedule controls and honest unavailable states.
- Download the governed PDF directly.
- Render every exported page and inspect clipping, overlap, pagination, glyphs,
  titles, source names and page references.

**Tiering and limits**

- Open plan comparison.
- Verify project/document/analysis/collaboration/export limits.
- Confirm limit prompts preserve existing work.

## LLM accuracy checks

The analysis will be scored on:

- Accuracy: extracted values match the PDFs.
- Completeness: expected rows are not lost.
- Placement: data appears in the correct artifact and section.
- Provenance: citations and row states are correct.
- Conflict handling: competing values remain visible.
- Assumption discipline: planted assumptions appear; invented ones do not.
- Cross-document reasoning: schedule, budget, ownership and dependency links agree.
- Advisor factuality: answers use retained project evidence.

## Rating

Each slice and each artifact receives a score:

- **5/5 - Ready:** correct and comfortable for an end user.
- **4/5 - Usable:** minor issue, no important data loss.
- **3/5 - Caution:** usable, but manual verification is required.
- **2/5 - Not ready:** important data or workflow failure.
- **1/5 - Blocked:** core flow cannot be completed.

Overall weighting:

- Data accuracy: 30%
- Completeness: 20%
- Correct placement: 15%
- Provenance and inference: 15%
- Functionality: 15%
- End-user usability: 5%

## Final report format

The final response will remain short and issue-focused:

`Slice / section - rating - issue`

It will include:

- one overall end-user readiness rating;
- Slice 1-10 ratings;
- seven artifact ratings;
- LLM accuracy and hallucination summary;
- share/reviewer/export result;
- only confirmed issues, with screenshots or evidence retained separately;
- no fixes or code changes.
