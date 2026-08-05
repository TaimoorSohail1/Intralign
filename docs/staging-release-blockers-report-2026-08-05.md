# OSLO staging release-blockers report

Date: 5 August 2026  
Branch: `fix/staging-release-blockers`  
Deployed code commit: `2bafe3343ff1a7f389410bcfde9e027df4e5dc23`

## Executive result

The targeted lifecycle, queueing, invitation, tier-limit, evidence-validation, and advisor failures have been fixed in code and deployed to staging. The staging application is suitable for stakeholder demonstrations, but it is not ready for a public production launch because real AI analysis and outbound email are not configured, the Supabase project has a quota warning, and a full multi-document production benchmark remains outstanding.

Recommendation: **GO for staging/demo; NO-GO for public production.**

## Fix status

| Problem | Result | Evidence |
|---|---|---|
| Slow and unreliable process-local analysis queue | Fixed in architecture | Durable PostgreSQL job queue added; a separate Heroku worker dyno is running and processed the staging tracer reanalysis. |
| Evidence validation failed the whole analysis | Fixed | Unsupported evidence locators are quarantined when verified evidence remains; incomplete findings are not published. |
| OSLO chat failed without OpenAI | Fixed safely | Advisor now returns a grounded current-snapshot fallback instead of an API failure. Real AI chat still needs an OpenAI key. |
| Reanalysis, History and Overview counters disagreed | Fixed | One analysis version now drives Issues, artifacts, History, Overview, Reports and notifications. |
| Failed invitation left active/pending access | Fixed | Failed first sends are revoked; failed resends restore the prior invitation. Staging test ended as `REVOKED`, not `PENDING`. |
| Tier limits differed between UI and server | Fixed | Free/Basic limits are centralized, displayed by the UI and enforced transactionally by the API. |
| Duplicate completion notifications from one run | Fixed | The staging tracer created exactly one new completion notification. Older entries represent separate historical runs. |
| Real AI analysis in staging | Blocked by configuration | Staging still uses `ANALYSIS_HARNESS=deterministic` and has no `OPENAI_API_KEY`. |
| Real email delivery | Blocked by configuration | No SMTP host, username or password is configured. |

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

- Web tests: **116 passed**
- Targeted API regression tests: **73 passed**
- Ruff: **passed**
- ESLint: **passed**
- Production web build: **passed**
- Git diff check: **passed**
- Staging API health: **ready**
- Heroku web and worker dynos: **up**

The full API non-integration suite did not finish within the local timeout during this validation run. The targeted changed-area suite passed, but the long-running full-suite test must be identified before production approval.

## Remaining production blockers

1. Configure `OPENAI_API_KEY` and switch staging from deterministic harness to the real provider, then rerun accuracy and latency benchmarks.
2. Configure a verified SMTP/email provider and test invite, report-send and failure/retry delivery.
3. Resolve the Supabase billing/quota warning so the service cannot be suspended after quota exhaustion.
4. Run repeated uploads for multiple PDFs in a supported browser and measure analysis success rate and p95 duration.
5. Diagnose the full API-suite timeout and obtain a clean complete run.
6. Add production monitoring and alerts for queue depth, job age, failure type, AI latency and email failures.

## Final assessment

The original staging lifecycle defects are resolved and the application now fails safely. Local and staging previously behaved differently because staging lacked provider configuration and used the deterministic harness. Code reliability is materially improved, but external provider setup and production-scale validation are still required before public launch.
