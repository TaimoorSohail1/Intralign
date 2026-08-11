# Intralign Structured Artifact Reliability Plan

Status: Approved requirements; implementation not started
Source: Northstar 10-PDF audit and approved grill session
Primary objective: Make normal project-management PDFs produce complete, consistent, evidence-linked results without document-specific code changes.

## 1. Outcome

Intralign will preserve structured project data from uploaded sources and expose it consistently across:

- the seven plan artifacts;
- Overview, Issues, Attention Map, History, and Inference Map;
- Reports, reviewer views, and PDF exports;
- re-analysis and user-edited artifact versions.

The system will not promise success for every possible PDF. Unreadable, unsupported, or low-confidence inputs will produce a controlled warning instead of fabricated data or a developer error.

## 2. Agreed scope

### In scope

- A shared structured-artifact base contract plus a strict schema for each artifact.
- Field- and row-level provenance: uploaded document, location, evidence excerpt, and origin.
- Explicit states for confirmed, inferred, conflicting, and unknown values.
- Validation, bounded repair/retry, and controlled partial-result handling.
- Digital PDFs, scanned PDFs, tables, missing data, and conflicting source versions.
- Project-title extraction with a user confirmation fallback.
- Correct artifact versioning and preservation of user-confirmed edits.
- Correct source-document, artifact, evidence, and assumption semantics.
- Friendly form validation, a production-quality reviewer view, stable date rendering, and direct PDF download.
- Automated regression coverage for the Northstar 10-PDF pack and adverse fixtures.

### Out of scope

- New product capabilities unrelated to the ten audited defects.
- Silent guesses for missing project information.
- Destructive rebuilding of historical snapshots.
- Claiming universal support for every PDF layout or image quality.

## 3. Current root causes

1. `Artifact` and the OpenAI construct contract store one prose `summary` per artifact.
2. Perception is capped at a small list of condensed facts and claims, so rich rows disappear early.
3. The API converts summaries into generic UI rows such as `Current plan` and `To confirm`.
4. Scope adds a hard-coded “no exclusions” sentence regardless of extracted evidence.
5. Assumptions are inferred in the frontend from low artifact reliability instead of being domain records.
6. Reports use the seven artifact count as the uploaded-document count.
7. AI snapshots and editable drafts use separate version rules, leaving re-analysis visibly at `v1`.
8. Project creation always writes `Untitled project`, with no title promotion path.
9. Some server actions let backend validation errors escape into the Next.js runtime boundary.
10. Reports format dates differently during server and client rendering and use browser printing for export.

## 4. Target contract

### Shared record fields

Every structured record will contain:

- stable record ID;
- artifact type and record kind;
- structured value;
- state: `confirmed`, `inferred`, `conflicting`, or `unknown`;
- confidence/reliability;
- one or more evidence citations;
- source document ID and source location;
- origin: OSLO or user;
- first-seen and last-updated analysis run IDs.

Conflicts will retain every candidate value and its evidence. Unknown values will remain empty and explicit; they will not be replaced with invented text.

### Artifact-specific schemas

| Artifact | Required structured collections |
|---|---|
| Intent | purpose, objectives, outcomes, success measures |
| Context | stakeholders, governance forums, decision rights, constraints |
| Scope | in-scope items, exclusions, deliverables, boundaries |
| Requirements | functional requirements, non-functional requirements, acceptance criteria, open decisions |
| Work breakdown | workstreams, work packages, deliverables, owners, dependencies |
| Schedule | activities, milestones, dates, dependencies, tolerance/status |
| Resources | people/roles, allocation, capacity gaps, vendors, RACI assignments |

Assumptions and conflicts are shared domain collections referenced by these artifacts, not prose guessed by the reporting UI.

## 5. Delivery slices

### Slice A — Freeze the baseline

Goal: Turn the existing audit into executable expectations before changing behavior.

Work:

- Add the ten Northstar PDFs as stable test fixtures with expected source counts and key records.
- Capture expected results for title, exclusions, requirements, schedule, stakeholders, RACI, assumptions, and report counts.
- Add adverse fixtures: scanned PDF, table-heavy PDF, duplicate version, conflicting values, missing values, malformed PDF, and unreadable scan.
- Record the current failures as tests.

Acceptance:

- Tests fail for the known data-loss and contradiction defects.
- Existing unrelated test suites remain unchanged.

### Slice B — Schedule tracer bullet

Goal: Prove one complete typed path before expanding to all artifacts.

Work:

- Introduce the shared record/provenance models and the strict Schedule schema.
- Extract each milestone/activity as a separate record.
- Validate allowed evidence locators and semantic requirements.
- Persist typed Schedule content and expose it through the API contract.
- Render real milestone rows in the Schedule artifact.
- Remove the generic `Current plan` fallback for Schedule.

Acceptance:

- The Northstar schedule retains all 16 expected activities/milestones.
- Each row links to valid source evidence.
- Missing dates render as unknown; they are never invented.
- API and UI tests prove the same record count and values.

### Slice C — Complete all seven artifact schemas

Goal: Expand the proven typed path without returning to summary-based fallbacks.

Work:

- Add strict schemas for Intent, Context, Scope, Requirements, Work breakdown, and Resources.
- Replace the single condensed construct step with a bounded map/merge workflow:
  - extract typed records from source fragments in parallel;
  - normalize and deduplicate deterministically;
  - retain conflicts instead of silently choosing;
  - construct the seven artifact views from canonical records.
- Apply schema validation after each extraction and after merge.
- Retry only repairable contract failures; publish a controlled partial result when retries are exhausted.
- Retain prose summaries as derived presentation text, never as the source of structured rows.

Acceptance:

- Northstar retains the named stakeholders and decision rights.
- Explicit scope exclusions appear once and are not contradicted.
- All 12 functional and 8 non-functional requirements remain separate records.
- Work packages, named resources, allocations, backups, and RACI assignments are retained.
- Every material row has provenance or an explicit inferred/unknown state.

### Slice D — Naming, provenance, assumptions, and versions

Goal: Make state semantics trustworthy across analysis and re-analysis.

Work:

- Extract a project-title candidate from supported evidence.
- Promote the title automatically only above a defined confidence threshold.
- Ask the user to name the project when no reliable title exists.
- Store assumptions as explicit typed records with evidence and load-bearing status.
- Keep confirmed, inferred, conflicting, and unknown states separate.
- Define one monotonic artifact revision rule across AI snapshots and user drafts.
- Preserve user-confirmed records during re-analysis and surface conflicts for review.
- Backfill existing projects without overwriting retained historical snapshots.

Acceptance:

- The test project becomes `Northstar CRM Modernization`, not `Untitled project`.
- Re-analysis increments the visible artifact revision.
- Earlier versions remain readable.
- User-confirmed edits survive re-analysis.
- The Inference Map and Reports use the same assumption records and counts.

### Slice E — Correct downstream semantics

Goal: Make all consumers use canonical records instead of reconstructing meaning.

Work:

- Generate Overview, Issues, Attention Map, History, Inference Map, and Reports from the typed artifact contract.
- Count uploaded source documents separately from seven plan artifacts.
- Rename “By document” to “By artifact” unless a true source-document view is added.
- Build issue and report evidence from field-level citations.
- Distinguish explicit assumptions from OSLO inferences.
- Generate report sections on the server from a stable report view model.

Acceptance:

- Reports say `10 source documents` and `7 plan artifacts`.
- Inference and report assumption lists agree.
- No consumer parses artifact prose to reconstruct structured meaning.
- All seven report sections remain visible and internally consistent.

### Slice F — User-facing defect fixes

Goal: Remove the remaining trust-breaking UX failures.

Work:

- Convert API validation errors into inline invitation/form messages.
- Add route-level error handling so expected 4xx responses never become developer runtime screens.
- Repair reviewer spacing, labels, responsive layout, radio controls, and focus behavior.
- Replace the unexplained `68` with a labelled confidence value and scale, or remove it where it adds no value.
- Use a server-provided, locale-stable date string to prevent hydration mismatches.
- Connect Reports export to the governed PDF endpoint and generate a complete styled report PDF.

Acceptance:

- Invalid email remains on the form and shows a useful message.
- Reviewer page works at desktop and mobile widths and contains no unexplained number.
- Reports produce no hydration warning.
- Export downloads a PDF directly without requiring print-to-PDF.
- Exported content matches the current retained report and its seven sections.

### Slice G — Hardening and release

Goal: Demonstrate stability across document types and all ten product slices.

Work:

- Run parser, schema, merge, persistence, API, frontend, and end-to-end tests.
- Run the complete Northstar 10-PDF journey: upload, Initial, Extended, clarification re-analysis, edit, review, and export.
- Test scan/OCR, table-heavy, conflict, missing-data, malformed, and unreadable inputs.
- Add telemetry for schema failures, retries, missing required collections, processing time, and fallback use without logging source content.
- Compare latency to the target and parallelize bounded extraction work where safe.
- Perform AI review, human code review, desktop QA, mobile QA, and accessibility smoke checks.

Acceptance:

- All Northstar golden expectations pass without document-specific logic.
- Unsupported inputs show controlled, actionable states.
- Normal analysis shows immediate progress and completes under 60 seconds where practical.
- API tests and Ruff pass.
- Web tests, ESLint, and Next.js production build pass.
- Desktop and mobile end-to-end journeys pass.

## 6. Implementation areas

### API and domain

- `services/api/src/oslo_api/analysis/models.py`
- `services/api/src/oslo_api/analysis/openai_harness.py`
- `services/api/src/oslo_api/analysis/workflow.py`
- `services/api/src/oslo_api/analysis/persistence.py`
- `services/api/src/oslo_api/analysis/service.py`
- `services/api/src/oslo_api/analysis/documents.py`
- `services/api/src/oslo_api/api/analysis.py`
- `services/api/src/oslo_api/api/projects.py`
- `services/api/src/oslo_api/collaboration/pdf.py`

### Database

- A new forward-only Supabase migration for typed artifact content, conflicts, assumptions, provenance, and revision metadata.
- Existing snapshot JSON remains readable during migration.

### Web

- Generated/shared API contracts under `packages/contracts`.
- `apps/web/src/components/artifacts/artifact-workspace.tsx`
- `apps/web/src/lib/project-provenance.ts`
- `apps/web/src/components/reports/report-workspace.tsx`
- `apps/web/src/app/review/[token]/page.tsx`
- `apps/web/src/components/collaboration/reviewer-response-form.tsx`
- `apps/web/src/app/admin/invitations/actions.ts`
- Associated pages, route adapters, styles, and tests.

## 7. Test strategy

For each behavior:

1. Add a failing domain or integration test.
2. Implement the smallest change that makes it pass.
3. Refactor only while tests remain green.
4. Add the cross-layer test when the behavior reaches the API or UI.

Required suites:

- parser and OCR unit tests;
- strict-schema and retry tests with mocked model responses;
- deterministic merge, deduplication, conflict, and precedence tests;
- persistence, migration, tenant isolation, and revision tests;
- API contract tests;
- artifact, inference, report, invitation, reviewer, and export component tests;
- Northstar golden end-to-end regression;
- desktop and mobile manual QA.

## 8. Dependency order

`Baseline fixtures → Schedule tracer → Seven schemas → State/version semantics → Downstream consumers → UX defects → Full hardening`

UX work that does not depend on the new contract may be developed independently, but it is not considered releasable until the canonical data flow passes.

## 9. Release gate

The work is ready to ship only when:

- there are no known scope contradictions;
- expected structured rows are not collapsed or omitted;
- source-document and artifact counts are correct;
- assumptions and inferences are labelled consistently;
- each material output is traceable to evidence;
- re-analysis preserves history and user-confirmed edits;
- all expected input failures are friendly and controlled;
- reviewer and report views pass desktop/mobile QA;
- PDF export is direct and stable;
- all automated and manual gates pass.
