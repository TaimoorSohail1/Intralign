# OSLO Product Grill — Slices 1–4 E2E Final Report

**Date:** 25 July 2026

**Branch:** `feature/slice-4`

**Scope:** Access/onboarding, Intake/Fast Pass, Overview/Understanding Console, and Attention Map

## Executive result

**Result: Pass.**

- 172 automated checks passed.
- All core Slice 1–4 journeys pass on desktop, tablet, and mobile.
- The two previously reported defects are fixed:
  1. Overview restores its prior scroll position after returning from Attention Map.
  2. Failed clarification re-analysis shows a safe failure message and Retry action while preserving the last-good result.
- The live OpenAI account still reports `OPENAI_QUOTA` for the affected retry. The application now handles this external failure correctly and remains safely retryable.

## Automated test evidence

| Suite | Result |
|---|---:|
| Frontend unit/component tests | 36 passed |
| FastAPI/API/integration tests | 115 passed |
| Playwright desktop journeys | 7 passed |
| Playwright tablet journeys | 7 passed |
| Playwright mobile journeys | 7 passed |
| ESLint | Passed, no warnings |
| Next.js production build and TypeScript | Passed |
| **Total automated checks** | **172 passed** |

Commands used:

```text
pnpm --filter @oslo/web test -- --run
uv run --project services/api pytest services/api/tests -q
pnpm --filter @oslo/web lint
pnpm --filter @oslo/web build
pnpm --filter @oslo/e2e test -- specs/slice-one.spec.ts specs/slice-two.spec.ts specs/slice-three.spec.ts specs/slice-four.spec.ts --project=desktop
pnpm --filter @oslo/e2e test -- specs/slice-one.spec.ts specs/slice-two.spec.ts specs/slice-three.spec.ts specs/slice-four.spec.ts --project=tablet --project=mobile
```

## Official scenario disposition

The 80 reference scenarios in the four `e2e-test-scenarios.md` files were reviewed against the production implementation.

| Classification | Count |
|---|---:|
| Production-applicable scenarios passed | 66 |
| Production-applicable scenarios failed | 0 |
| Prototype-only, illustrative, or superseded scenarios | 14 |
| **Total reviewed** | **80** |

The excluded scenarios are prototype controls or superseded UI rather than product failures. They include GA anonymous preview, simulation-only controls, the removed Dimensions/Field toggle, and the unshipped light-theme toggle.

## Fixed-defect verification

### E2E-01 — Overview scroll restoration

**Fixed and verified.**

- The Overview stores the reading position before navigating to Attention Map.
- Restoration now survives React Strict Mode's development remount and delayed layout/hydration.
- Focused component regression passes.
- Live browser result: the Overview position was `28px` before navigation and restored to `28px` after returning.

### E2E-02 — Failed clarification re-analysis

**Fixed and verified.**

- A failed run is now surfaced for both provisional and current snapshots.
- The UI displays `Extended Analysis paused safely`.
- The last-good snapshot remains visible.
- `Retry Extended Analysis` reconnects the UI to the retried run.
- Completion replaces the failed state with the new current read.
- If OpenAI rejects the retry again, the UI returns to the safe failure state and exposes Retry again.
- Focused tests cover current-snapshot failure, retry polling, and successful publication.
- Live browser verification showed `retrying → safe failure + Retry` under `OPENAI_QUOTA`.

## Slice-by-slice result

### Slice 1 — Access and onboarding

**Pass**

- Admin invitation, Mailpit delivery, activation, account creation, and Welcome flow pass.
- Existing-user sign-in and workspace join pass.
- Invalid/anonymous access, resend, revoke, session persistence, logout, orientation, keyboard, responsive, and reduced-motion behavior pass.

### Slice 2 — Intake, Fast Pass, and Extended Analysis

**Pass**

- Refresh reconnects to active analysis.
- Initial Analysis publishes a provisional Overview.
- Extended Analysis publishes a current immutable snapshot.
- Seven artifacts, document parsing, fragments, evidence locators, last-good protection, failure messaging, and Retry pass.

### Slice 3 — Overview and Understanding Console

**Pass**

- Confidence, CAF dimensions, reliability, stage, trend, Start Here, Progress, Project Summary, issues, clarification, and advisor flows pass.
- Clarification re-analysis preserves last-good state, reconnects after refresh, and publishes only validated results.

### Slice 4 — Attention Map

**Pass**

- The 7 × 3 map renders current-snapshot issues with correct counts and severity.
- Keyboard activation, single and multiple finding drill-down, row scoping, status lifecycle, Ask OSLO, responsive layouts, and all-clear state pass.
- Returning to Overview restores the user's prior reading position.

## Database and live-model evidence

Completed initial, extended, and clarification runs show:

- 12 completed workflow nodes per successful run.
- Seven versioned plan artifacts.
- Three live OpenAI calls per run:
  - Perceive
  - Construct Artifacts
  - Evaluate & Advise
- Failed later runs do not replace the last-good published snapshot.

## External dependency

The current OpenAI account can still reject clarification retries with `OPENAI_QUOTA`. Restoring account quota is required for that live model run to complete, but this is no longer an application UX or recovery defect.

## Final recommendation

Slices 1–4 are ready for review and demo. The cumulative automated suites, responsive E2E journeys, focused regression tests, and live browser checks all pass. Restore OpenAI quota before demonstrating a successful live clarification retry.
