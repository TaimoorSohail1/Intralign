# OSLO staging release-blockers report

Date: 5 August 2026  
Branch: `fix/staging-release-blockers`  
Deployed API code commit: `61a1989`  
Deployed web code commit: `85c9925`

## Executive result

The targeted lifecycle, queueing, invitation, tier-limit, evidence-validation, advisor, real-AI, and Postmark integration failures have been fixed and deployed to staging. The staging application is suitable for stakeholder demonstrations, but it is not ready for a public production launch because the configured Postmark sender still needs verification, the Supabase project has a quota warning, a failed-project retry UI gap remains, and a full multi-document production benchmark is outstanding.

Recommendation: **GO for staging/demo; NO-GO for public production.**

## Fix status

| Problem | Result | Evidence |
|---|---|---|
| Slow and unreliable process-local analysis queue | Fixed in architecture | Durable PostgreSQL job queue added; a separate Heroku worker dyno is running and processed the staging tracer reanalysis. |
| Evidence validation failed the whole analysis | Fixed | Unsupported evidence locators are quarantined when verified evidence remains; incomplete findings are not published. |
| OSLO chat failed without OpenAI | Fixed and configured | Advisor has a grounded fallback, and staging now has a valid OpenAI key for live responses. |
| Reanalysis, History and Overview counters disagreed | Fixed | One analysis version now drives Issues, artifacts, History, Overview, Reports and notifications. |
| Failed invitation left active/pending access | Fixed | Failed first sends are revoked; failed resends restore the prior invitation. Staging test ended as `REVOKED`, not `PENDING`. |
| Tier limits differed between UI and server | Fixed | Free/Basic limits are centralized, displayed by the UI and enforced transactionally by the API. |
| Duplicate completion notifications from one run | Fixed | The staging tracer created exactly one new completion notification. Older entries represent separate historical runs. |
| Real AI analysis in staging | Fixed and verified | The existing key is configured in Heroku, `ANALYSIS_HARNESS=openai`, and a live analysis completed successfully. |
| Real email delivery | Integration deployed; sender verification blocked | Postmark HTTPS delivery is configured for invitations and reports. The server token is valid, but Postmark rejected the configured Gmail From address because it is not yet a confirmed Sender Signature. |
| Heroku OpenCV runtime | Fixed | The desktop OpenCV/libGL dependency was replaced at build time with headless OpenCV, and all Heroku shell hooks are forced to Linux line endings. API health returned `200 ready` after deployment. |
| Invalid login produced a full-page server error | Fixed and deployed | Invalid credentials now return to `/login` with an inline message instead of producing HTTP 500. The live staging path was verified after deployment. |

## 05 August configuration and login recheck

- Staging had drifted back to `ANALYSIS_HARNESS=deterministic` with no OpenAI key in the API app.
- The valid local OpenAI credential was restored to Heroku and accepted by the OpenAI API.
- Staging now reports `ANALYSIS_HARNESS=openai`, the key is present, and API health returns `200 ready`.
- The live web login returns HTTP 200. An invalid login stays on the sign-in page and shows a clear inline error.
- Supabase currently contains only one synthetic confirmed staging account; a real owner account must still be provisioned before client handover.

## Staging functional test

The existing Wayfarer staging project was used for a live end-to-end tracer.

1. Opened a Requirements issue and applied a correction.
2. The issue immediately became **Addressed**, not incorrectly Resolved.
3. The artifact showed **Saved · Analysis pending**.
4. The durable worker completed reanalysis.
5. Requirements advanced to version 4 and became **Up to date**.
6. History added the new current Extended Analysis run.
7. Reports updated to the same current analysis time.
8. Issues retained the correct Addressed state.
9. Overview showed matching issue and answered-question counts.
10. Notifications added one completion event for this run.

Observed end-to-end time was approximately 73 seconds, including interaction and page refresh time. This is a successful tracer result, not a statistically valid p95 benchmark.

### Real OpenAI validation

Staging was subsequently switched from the deterministic harness to the real OpenAI provider. A second governed Requirements correction was submitted after the configuration restart:

- API health returned `200 ready`.
- The durable worker processed the new OpenAI job.
- The live analysis completed successfully in approximately **35 seconds**.
- Requirements advanced to version 5 and retained both confirmed resolutions.
- History, Overview, Issues, Attention Map, Inference Map, Reports, all seven artifacts, and notifications reflected the same current run.
- Reports were current as of `05 Aug 2026, 16:03 UTC`.
- One completion notification was created for the new run.

## Route and feature coverage

Passed on staging:

- Overview
- Issues and issue lifecycle
- History and current snapshot
- Attention Map
- Inference Map
- Reports and current-analysis synchronization
- Intent, Context, Scope, Requirements, Work Breakdown, Schedule and Resources
- Workspace and server-backed project limits
- Settings sections
- Advisor fallback
- Invitation failure compensation
- Six-step product tour
- PDF export API (`200`, 11,333 bytes)

The browser automation did not capture the native PDF download event, but the staging router recorded a successful export response.

## Automated verification

- Web tests: **117 passed**
- Targeted API regression tests: **73 passed**
- Ruff: **passed**
- ESLint: **passed**
- Production web build: **passed**
- Git diff check: **passed**
- Staging API health: **ready**
- Heroku web and worker dynos: **up**
- Postmark mailer tests: **4 passed**
- Postmark provider test: valid token; sender rejected until Sender Signature confirmation

The full API non-integration suite did not finish within the local timeout during this validation run. The targeted changed-area suite passed, but the long-running full-suite test must be identified before production approval.

## Remaining production blockers

1. Confirm the configured From address as a Postmark Sender Signature (or use a verified domain), then test invite, report-send and failure/retry delivery.
2. Resolve the Supabase billing/quota warning so the service cannot be suspended after quota exhaustion.
3. Repair the failed-project retry route: the current “Retry from Analysis” journey opens a blank intake instead of restoring the retained document.
4. Run repeated uploads for multiple PDFs and measure analysis recall, success rate and p95 duration with the real provider.
5. Diagnose the full API-suite timeout and obtain a clean complete run.
6. Add production monitoring and alerts for queue depth, job age, failure type, AI latency and email failures.

## Final assessment

The original staging lifecycle defects are resolved, the real OpenAI pipeline is active, Postmark is integrated, and the application now fails safely. Code reliability is materially improved, but Postmark sender verification, the failed-project retry repair, quota resolution and production-scale multi-document validation are still required before public launch.
