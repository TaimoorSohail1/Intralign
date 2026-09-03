# R2 staging invitation and authentication fix report

**Date:** 29 August 2026  
**Environment:** Heroku staging only  
**Branch:** `feature/r2-defect-remediation`  
**Fix commit:** `59ea9a9b`  
**Result:** **PASS — the verified activation/login timeout defect is fixed on staging.**

## Root cause

Invitation activation and existing-user invitation acceptance acquired a PostgreSQL advisory lock using the only available pooled database connection. Nested helper calls then attempted to acquire a second connection. With a pool size of one, the request waited for itself, timed out after 30 seconds, and Heroku returned H12/503.

The buttons were working. The backend transaction was deadlocked by its own connection usage.

## Fix implemented

- Replaced the session advisory lock with a transaction-scoped advisory lock.
- Reused one database connection for invitation resolution, membership/profile/access updates, and accepted-invitation resumption.
- Added regression coverage for a pool-size-one environment.
- Added recoverable activation and login error states so temporary service failures produce a retry message rather than a dead page.

## Local verification

| Check | Result |
|---|---:|
| API unit and API tests | 66 passed |
| Web tests | 297 passed |
| Web lint | Passed |
| Production build and TypeScript | Passed |
| R2 guardrail meta-tests | 8 passed |
| Diff validation | Passed |

The full local guardrail integration suite was not completed because the local Supabase integration database was unavailable. This was an environment limitation, not a failing assertion.

## Staging deployment

| Component | Release | Commit | Result |
|---|---:|---|---:|
| API | v65 | `a674d2ed` | Healthy |
| Web | v46 | `a674d2ed` | Healthy |
| Worker | API v65 | `a674d2ed` | Healthy |

Production was not changed.

## Live end-to-end evidence

| Journey | Result | Evidence |
|---|---:|---|
| Invitation activation | Pass | Two fresh `POST /v1/invitations/activate` requests returned HTTP 200 |
| Activation response time | Pass | Browser submissions completed in approximately 542 ms and 807 ms |
| Welcome/onboarding | Pass | Welcome form redirected successfully in approximately 241 ms and 166 ms |
| Project creation | Pass | Project API returned HTTP 201 |
| Analysis start | Pass | Analysis API returned HTTP 202 |
| Real OpenAI pipeline | Pass | Multiple OpenAI Responses API calls returned HTTP 200 |
| Project overview | Pass | Authenticated overview loaded with the project, issues, seven artifacts, and navigation |
| Browser console | Pass | No errors on the authenticated project page |
| Activation H12 after release | Pass | No QueuePool timeout or activation H12 occurred after the v65/v46 release |

## Notes

- A browser form left open during the deployment produced one stale Next.js Server Action error. Reloading the freshly deployed page resolved it; fresh activation flows then passed. This is a deployment-version mismatch, not the original database deadlock.
- The existing-user acceptance route shares the corrected transactional code and is regression-tested. Normal authenticated staging sessions were also verified. A separate permanent invitation record was not created solely to repeat that exact variant during this final pass.

## Recommendation

The reported staging invitation activation/login timeout is resolved and verified end to end. The staging build is ready for client retesting. Keep production unchanged until the owner approves promotion.
