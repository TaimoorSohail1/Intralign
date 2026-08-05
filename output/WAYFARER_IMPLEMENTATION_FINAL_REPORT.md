# Wayfarer lifecycle and report-currency implementation report

Date: 30 July 2026

## Outcome

The two approved product decisions are implemented:

1. A saved clarification or applied fix becomes **Addressed** immediately and is shown as **Waiting for analysis**. Only a completed governed analysis can mark it **Resolved**.
2. A report based on an older snapshot remains sendable, but it is labelled **Previous analysis** and requires explicit sender confirmation.

The work also fixes two related failures found during QA:

- Issue and report proxy routes now preserve useful API status codes and messages instead of replacing them with a generic 400 error.
- PDF exports now use a header-safe Unicode filename, fixing the crash caused by project names containing characters such as an em dash.

## Implemented behavior

### Issue lifecycle

- Clarification answers are persisted before re-analysis starts.
- The related issue is durably marked Addressed in the same save transaction.
- Addressed clarification state survives refreshes and failed or delayed analysis.
- While re-analysis is active, the panel visibly shows:
  - `Addressed · Waiting for analysis`
  - confirmation that the change is saved
  - confirmation that only analysis may resolve the issue
- Issue-answer and issue-action routes return the real API error and status where available.
- Idempotency behavior remains in place to prevent duplicate saves or duplicate analysis runs.

### Report currency

- The UI compares the report snapshot with the current project snapshot.
- A stale report displays a clear `Previous analysis` warning.
- Send and Schedule require the sender to check:
  - `I understand this report is based on a previous analysis`
- The API rechecks currency at delivery time to protect against race conditions.
- Without confirmation, stale delivery returns:
  - `REPORT_PREVIOUS_ANALYSIS_CONFIRMATION_REQUIRED`
- With confirmation, delivery remains allowed and records:
  - `currency_state = previous_analysis`
  - `previous_analysis_confirmed = true`
- The delivered email is labelled in both places:
  - subject prefix: `Previous analysis -`
  - first report section: previous-analysis warning
- Report history payloads include the currency state.
- Current reports continue to save and send normally without an extra confirmation.

### PDF export

- Content-Disposition now supplies:
  - a safe ASCII fallback filename
  - an RFC 5987 UTF-8 filename
- Project names containing Unicode punctuation no longer cause a server error.

## Database

Applied migration:

- `20260730160000_report_currency_state.sql`

New delivery audit fields:

- `currency_state`
- `previous_analysis_confirmed`

The migration was applied successfully to the local Supabase database.

## Verification

### Automated

| Check | Result |
|---|---:|
| Web tests | 105 passed |
| API tests | 208 passed |
| Web lint | Passed |
| API Ruff lint | Passed |
| Next.js production build | Passed |
| Real-DB clarification lifecycle test | Passed |
| Real-DB stale-report confirmation test | Passed |
| Unicode PDF filename regression test | Passed |

Three existing dependency deprecation warnings remain; they do not affect these flows.

### Manual browser QA

Tested against the live local Wayfarer project:

- Report loaded the current 22-issue analysis rather than the earlier 14-issue report.
- PDF export started successfully.
- Issue detail showed the correct apply-and-reanalyze explanation.
- Reports and Issues pages produced no browser console errors.

No clarification, fix, report email, or re-analysis was submitted against the Wayfarer project during manual QA. The PDF export test created the expected export audit event.

## Files affected

The implementation spans:

- issue answer/action API proxies and issue panel UI
- analysis persistence and issue-state overlay
- report API, service, UI, and delivery audit model
- collaboration PDF response headers
- Supabase migration
- web, API, and real-database regression tests

## Final assessment

The approved lifecycle and report-currency decisions are production-implemented and covered by API, UI, integration, build, lint, and manual checks. The earlier issue-save opacity, stale-report blocking, and Unicode export failure are resolved within this scope.
