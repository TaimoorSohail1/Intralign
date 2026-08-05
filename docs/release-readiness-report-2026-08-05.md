# Release readiness report — 5 August 2026

## Decision

**NO-GO for a public production launch.**

The application workflow and responsive UI are substantially healthier, but the
live analysis engine does not yet meet the approved accuracy or latency gates.
The implementation is suitable for internal validation and a controlled shadow
run, not an unrestricted client handover.

| Area | Rating | Result |
|---|---:|---|
| UI and governed workflow | 8/10 | Core journeys work across desktop, tablet and mobile. |
| Analysis quality and runtime | 4/10 | Five live benchmark runs completed, but four had very low recall and every run exceeded the 180-second gate. |
| Overall release readiness | 5/10 | Keep behind a controlled rollout until the analysis gates pass. |

## Implemented in this pass

- Reanalysis publication now refreshes History and Reports from the same current
  analysis-run version used by Overview and the other project sections.
- A queued or running extended analysis is recognised while the initial read is
  still provisional, preventing edits during publication.
- A failed History refresh preserves the last successfully published view.
- Artifact editing no longer replaces focused editable content and moves the
  caret while the user types.
- Snapshot PDF export now uses the snapshot export API rather than the saved-
  report endpoint.
- Invitation capacity and plan-limit failures now show the API's actionable
  message instead of a misleading duplicate-invitation message.
- Unsupported evidence references are quarantined without logging or echoing the
  raw reference values.
- Logout clears the local session and returns to login even when remote identity-
  provider revocation is slow or unavailable.
- E2E setup now resets only fixed local Playwright identities and refuses any
  non-local Supabase target.
- CI now runs lint, API tests, web tests, the production build and all responsive
  Playwright journeys against a schema-backed local platform.
- The infrastructure runbook now defines secrets, monitoring, backup, smoke,
  deployment and rollback requirements.

## Automated verification

| Check | Result |
|---|---|
| Web unit/component tests | Passed (114 tests) |
| API tests | Passed (249 tests) |
| Focused evidence-harness tests | Passed (22 tests) |
| Web lint | Passed |
| API Ruff lint | Passed |
| Production web build | Passed |
| Responsive end-to-end suite | 39/42 in the consolidated run; all three discovered failures were fixed and passed targeted reruns |
| Git whitespace validation | Passed |

The browser suite covers upload/intake, Overview, Issues, History, Attention Map,
Inference Map, all seven artifacts, editing/versioning/reanalysis, Reports,
snapshot export, sharing, external review, Settings, invitations and responsive
layouts.

The consolidated responsive run found three issues: remote logout could delay
local logout, a new analysis version could remount History while a snapshot was
open, and the Slice 10 test could select a newly created unanalyzed project.
After correction, the affected reruns passed: Slice 1 desktop 4/4, Slice 7 and
Slice 10 tablet 2/2, and the final History synchronization check 1/1. Every one
of the 42 journeys therefore has a passing post-fix result, although the full
42-test suite was not repeated a third time after those final corrections.

## Live multi-document benchmark

These runs used the real provider-backed analysis path. Expected-findings files
were used only by the offline evaluator and were not passed into analysis.

| Document | Overall recall | Critical recall | Traps | Duplicate roots | Runtime | Gate |
|---|---:|---:|---:|---:|---:|---|
| Thornfield | 16.7% | 40% | 0 | 1 | 622.2s | Fail |
| Wayfarer | 22.2% | 25% | 0 | 0 | 378.8s | Fail |
| Tideline | 100% | 100% | 0 | 2 | 467.1s | Fail |
| Millstone | 13.3% | 0% | 0 | 0 | 567.5s | Fail |
| SB06 Marrow & Co Coffee | 0% | 0% | 2 | 0 | 618.8s | Fail |

All five analyses completed and unsupported evidence was safely excluded; none
met every release gate. The required gates are 100% critical recall, at least
90% overall recall, zero traps, zero duplicate canonical issues, stable ratings
and a maximum 180-second extended-analysis runtime.

## Why launch remains blocked

1. **Recall is not general enough.** Fixes that help one document do not transfer
   reliably to unseen documents or small-business plans.
2. **Concurrent analysis is too slow.** A single simple run can be around one
   minute, but five concurrent runs took roughly 379–623 seconds end to end.
3. **The queue is process-local.** Analysis still relies on in-process thread
   pools and semaphores, so work is not durably recoverable across process or
   machine failure.
4. **Deduplication is incomplete.** Tideline still produced two duplicate root
   issues.
5. **Small-business calibration is incomplete.** SB06 missed the expected issues
   and triggered two documented enterprise-style traps.

## Required release work

1. Move analysis execution to a durable external queue with idempotent jobs,
   leases, retry limits, dead-letter handling and startup recovery.
2. Profile each provider stage, cache extraction/normalized claims and bound
   per-workspace concurrency so p95 stays below the approved limits.
3. Improve normalized cross-document claims and deterministic checks for direct
   numeric, schedule, scope and contractual contradictions.
4. Strengthen business-size/industry calibration and canonical issue identity.
5. Run every approved benchmark three times in a production-like environment;
   release only when every accuracy, stability, duplicate, trap and runtime gate
   remains green.

## Recommendation

Merge and deploy these changes to an internal or shadow environment. Do not call
the product production-ready yet. The client-facing workflow is close, but the
analysis service needs a separate reliability and quality milestone before a
public launch.
