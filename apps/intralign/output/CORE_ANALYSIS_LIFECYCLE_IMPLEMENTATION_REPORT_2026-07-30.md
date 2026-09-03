# OSLO core analysis and lifecycle implementation report

Date: 30 July 2026

## Outcome

The approved high-priority remediation is implemented and regression-tested:

- Saving a clarification or fix no longer changes an issue status before analysis.
- The UI now shows `Saved - Analysis pending` while retaining the last published status.
- A completed analysis marks a still-observed corrected weakness `Addressed`.
- An issue becomes `Resolved` only when the completed analysis no longer observes it.
- Applied and custom fixes carry evidence tied to the exact issue into reanalysis.
- Stale reports remain available for internal preview but external Send and Schedule are blocked.
- Corveth is now part of the governed benchmark corpus.
- General deterministic contract checks cover the major Corveth defect families.
- Release gates now require 100% critical recall, at least 90% overall recall, zero traps, zero duplicates, full locators, and a 180-second maximum benchmark duration.

No historical snapshot was rewritten and no project data was mutated during browser QA.

## Implemented behavior

### Issue lifecycle

- Removed immediate `Addressed` database mutations from clarification and issue-action saves.
- Removed action overlays that could make Overview or artifact pages show a lifecycle state not published by analysis.
- Preserved saved resolution text separately from issue status.
- Changed pending UI copy and accessibility state to `Saved - Analysis pending`.
- Changed lifecycle evaluation so a complete answer does not resolve a weakness that analysis still reports.
- Preserved resolution when a completed analysis omits the corrected weakness.
- Added issue-tied evidence to applied and custom artifact fixes.

### Report currency

- Stale external delivery now fails with `REPORT_PREVIOUS_ANALYSIS_BLOCKED`.
- Sender confirmation no longer bypasses the block.
- Send and Schedule are blocked in the UI when the report is based on a previous analysis.
- Current reports continue to save, send, schedule, edit and export normally.
- Historical report content remains previewable and clearly labelled.

### Analysis quality

Added or strengthened general, evidence-backed checks for:

- committed multi-site scope versus optional-site deliverables and pricing;
- regulated traceability outcomes versus laboratory, allergen and validation exclusions;
- front-loaded payment before system proof;
- deemed acceptance without measurable acceptance criteria;
- undefined effective dates and deferred schedule baselines;
- operational liability transfer and excluded loss exposure;
- asymmetric client and supplier obligations and remedies;
- asymmetric personnel substitution controls;
- client-run testing without acceptance or payment control;
- early deliverable warranty expiry before integrated go-live;
- unmeasurable data-cleansing obligations with priced consequences;
- component-total reconciliation;
- conflicting change-control rates;
- operational-record data protection;
- hosted-service exit and transition controls;
- system-level and go-live acceptance.

The rules are based on contract structure and evidence patterns. They do not check the Corveth document name or expected finding IDs.

### Governed benchmarks

- Added `corveth.json` with 17 expected findings, 8 documented traps and expected ratings.
- Tightened duplicate tolerance from 5% to 0%.
- Tightened the default and manifest runtime gate to 180 seconds.
- Retained 90% overall recall, 100% critical recall, zero traps, full locator coverage, rating stability and issue-ID stability gates.

## Verification

### Automated

| Check | Result |
|---|---:|
| API tests | 231 passed |
| Web tests | 110 passed |
| Ruff | Passed |
| ESLint | Passed |
| Next.js production build | Passed |
| Real-database lifecycle and report integration tests | Passed |

Three existing dependency deprecation warnings remain. They are unrelated to this implementation.

### Real Corveth PDF audit

The six-page source PDF was rendered and visually inspected, then its extracted page evidence was passed through the production deterministic audit and governed Corveth evaluator.

| Metric | Result |
|---|---:|
| Expected findings found | 17 of 17 |
| Overall recall | 100% |
| Critical recall | 4 of 4 |
| Documented traps raised | 0 of 8 |
| Duplicate findings | 0 |
| Evidence locator coverage | 100% |
| Benchmark gate | Passed |

The audit produced one additional generic dependency-register finding outside the 17-item expected manifest. It did not match a documented trap. This should be reviewed during broader false-positive calibration.

### Browser smoke check

- Authenticated Overview loaded with matching issue and Attention Map counts.
- Reports loaded with the current-analysis label and working editor controls.
- No project answer, fix, email or reanalysis was submitted during manual smoke testing.

## Important limits

This implementation materially improves the documented failure areas, but it does not prove universal 9/10 behavior yet:

- The Corveth result above validates the deterministic audit plus evaluator, not three live OpenAI runs.
- Initial p95 under 90 seconds and extended p95 under 180 seconds still require repeated deployed-provider measurements.
- Wayfarer, Greenway, Thornfield and Corveth must each run repeatedly in CI or the deployed environment to prove rating and issue-ID stability.
- The additional Corveth dependency-register finding needs human false-positive review.
- Progressive shadow rollout, operational alerting and a controlled production release remain deployment activities.

The defensible status is: **implementation complete for this remediation slice, all local regression gates green, Corveth benchmark passing, production-wide 9/10 claim pending repeated multi-document live evaluation.**
