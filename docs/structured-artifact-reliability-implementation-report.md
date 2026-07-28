# Structured Artifact Reliability - Implementation Report

Date: 28 July 2026

## Outcome

The structured artifact reliability work is implemented and verified against the
Northstar CRM Modernization ten-PDF project pack.

The live Extended Analysis completed successfully and published:

- 10 source documents
- 7 governed plan artifacts
- 23 structured sections
- 164 structured rows
- 164 row-level provenance states
- 4 explicit assumptions
- 3 retained conflicts
- artifact revision 5
- evidence-backed project title: Northstar CRM Modernization

## Resolved issues

1. Structured PDF rows are retained as typed sections, columns, rows, citations,
   and provenance states instead of being compressed into generic summaries.
2. Scope inclusions, exclusions, deferrals, and conflicting pressure items remain
   separate, so the artifact no longer silently contradicts itself.
3. Repeated governed document headers can promote an Untitled project to an
   evidence-backed project name.
4. Reports distinguish the 10 uploaded source documents from the 7 constructed
   plan artifacts.
5. Requirements, stakeholders, schedules, resources, vendors, budgets, RACI,
   ownership, dependencies, and acceptance detail use structured rows.
6. Explicit and necessary labelled assumptions are persisted and shown in the
   Inference Map and report.
7. Artifact revisions increment monotonically across analysis runs while user
   drafts are rebased without losing edits.
8. Invitation validation returns a friendly inline message and preserves the
   submitted email instead of exposing API/developer errors.
9. The reviewer readout labels Outcome Confidence clearly as a value out of 100
   and includes responsive layout fixes.
10. Report dates use stable UTC rendering, and Export downloads a governed PDF
    directly. The PDF uses readable source filenames and page locations, safe
    glyphs, and verified pagination.

## Scalability design

- Dense projects use seven artifact-specific construction shards.
- Concurrency is bounded to three workers.
- Every shard receives a capped, artifact-relevant evidence set while preserving
  at least one representative fragment from each source document.
- Perception facts, claims, and gaps are filtered per artifact instead of being
  repeated in full.
- Provider timeouts allow dense schema-bound responses to complete without
  premature retries.
- Checkpoints preserve completed parsing and perception work, so a retry resumes
  from the failed phase.
- Publication uses a per-project advisory lock and monotonic revisions.
- The canonical schema validates section shape, row width, row citations, and
  row-state alignment at the model, persistence, API, and frontend boundaries.

## User-facing verification

- Overview shows Northstar CRM Modernization, five-band Outcome Confidence, and
  provenance-led progress.
- Scope shows explicit exclusions and separately flags unresolved scope pressure.
- Inference Map is visible and reports grounded/inferred counts by artifact plus
  the four assumptions.
- Reports shows Summary, What changed, Key risks, Assumptions, Plan of action,
  Decisions needed, and Appendix in one editable readout.
- The report appendix shows 10 source documents and 7 plan artifacts.
- Direct PDF export downloaded and all three rendered pages were visually checked
  for clipping, overlap, orphaned headings, broken glyphs, and internal locator
  leakage.
- Invalid invitation data displays `Enter a valid email address.` inline.

## Automated verification

- API: 144 tests passed.
- Web: 17 test files and 80 tests passed.
- Python lint: Ruff passed.
- Web lint: ESLint passed.
- Production web build: passed.
- Database migration: applied successfully to the local Supabase database.

## Remaining production considerations

The implementation is stable for the current ten-document product limit, but no
LLM-backed document analysis can guarantee perfect extraction for every possible
PDF. Production rollout should retain schema validation, observability, retry
metrics, model-quality evaluation packs, and human review for low-confidence or
conflicting rows.
