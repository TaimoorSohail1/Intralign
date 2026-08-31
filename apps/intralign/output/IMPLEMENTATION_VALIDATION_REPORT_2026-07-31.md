# OSLO implementation and validation report — 31 July 2026

## Executive result

The planned architecture and Prototype 10 product flow are substantially implemented, but the product does **not** yet satisfy the analysis-quality release gates. The recommended decision is **internal review only / no production release**.

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| 1. Baseline | Partial | Eighteen strict benchmark manifests now exist, including Ironvale, Millstone and ten small businesses. The evaluator measures recall, critical recall, traps, locators, duplicates, ratings, duration and repeated-run stability. The current database does not contain Thornfield, Greenway, Corveth or Skyline, and Ironvale has no trusted snapshot, so three fresh runs for every fixture remain incomplete. |
| 2. Tracer flow | Implemented | Artifact/clarification actions now become Addressed immediately; reanalysis alone may resolve or reopen them. Lifecycle state is read from the canonical issues table and overlaid consistently in Overview and artifact workspaces. |
| 3. Analysis engine | Implemented, quality gate failing | Normalized evidence claims, deterministic contradiction checks, AI checks, stable issue identity, deduplication, evidence correction/quarantine, retry handling and business-size calibration are present. Fresh SB06 analysis still missed one expected risk and produced one small-business trap. |
| 4. State synchronization | Implemented | Published snapshots remain atomic and last-good state is preserved. Overview, Issues, History, both maps, artifacts, reports, exports and review surfaces use the published analysis state. Previous-analysis reports cannot be sent or scheduled. |
| 5. Prototype 10 | Implemented | Intake limits, analysis states, richer Overview, Addressed filtering, artifact controls, History, collaboration, reports, settings, membership and usage/limit UI are present. Prototype simulation/debug-only controls were not copied into production flows. |
| 6. Deep testing | Partial | Unit/integration suites, lint, type checking, production build and direct browser inspection passed. The shared Playwright database is populated with 37 active projects and exhausted invitations, so the complete 42-test suite is not repeatable without an isolated/resettable E2E database. |

## Verification results

- API: **246 passed**.
- Web: **110 passed**.
- Ruff: passed.
- ESLint: passed.
- TypeScript: passed.
- Next.js production build: passed; all 17 static pages generated.
- E2E suite: all 42 scenarios compile and are discoverable. A complete repeatable run is blocked by shared test-state isolation, stale projects and invitation capacity.
- Direct live-browser check: Overview, Issues, History, Attention Map, Inference Map, Reports, Settings and all seven artifact routes rendered without application or analysis failure.

## Existing published-snapshot audit

These snapshots were generated before the final prompt and evidence changes, so they are a baseline rather than validation of the new engine.

| Fixture | Recall | Critical | Traps | Duplicates | Rating | Runtime | Gate |
|---|---:|---:|---:|---:|---|---:|---|
| Wayfarer | 50.0% | 50.0% | 1 | 0 | Mismatch | 269s | Fail |
| Tideline | 57.1% | 100% | 0 | 2 | Mismatch | 214s | Fail |
| Millstone | 13.3% | 0% | 0 | 0 | Mismatch | 819s | Fail |
| SB01 | 66.7% | 100% | 5 | 0 | Mismatch | 161s | Fail |
| SB02 | 33.3% | 100% | 2 | 0 | Mismatch | 146s | Fail |
| SB03 | 50.0% | 100% | 2 | 0 | Mismatch | 167s | Fail |
| SB04 | 100% | 100% | 2 | 0 | Mismatch | 169s | Fail |
| SB05 | 33.3% | 100% | 1 | 0 | Mismatch | 128s | Fail |
| SB06 | 0% | 0% | 2 | 0 | Mismatch | 161s | Fail |
| SB07 | 0% | 0% | 1 | 0 | Mismatch | 128s | Fail |
| SB08 | 0% | 100% | 3 | 0 | Mismatch | 133s | Fail |
| SB09 | 0% | 0% | 2 | 0 | Mismatch | 133s | Fail |
| SB10 | 33.3% | 0% | 2 | 1 | Mismatch | 132s | Fail |

All available snapshots had 100% evidence-locator coverage.

## Fresh post-change tracer

SB06 Marrow & Co Coffee was reanalysed using the new production pipeline:

- Completed and published atomically; no partial result was exposed.
- Detected **2 of 3** expected findings after correcting the benchmark matcher.
- Critical recall: **100%**.
- Missed: December/Christmas peak rollout risk.
- False-positive trap: unnecessary contingency expectation for a small business.
- Duplicate canonical issues: **0**.
- Evidence locator coverage: **100%**.
- Ratings did not match the expected result.
- Runtime: **291 seconds**, above the 180-second extended-analysis gate.

## Remaining release blockers

1. Analysis recall is below 90% on the fresh tracer.
2. A documented small-business trap is still emitted.
3. Ratings remain inconsistent with governed expectations.
4. Extended analysis is slower than the 180-second p95 target.
5. Three-run stability has not been executed for every fixture.
6. E2E tests need an isolated seeded database and automatic cleanup; the shared developer workspace is unsuitable for a repeatable release gate.
7. Thornfield, Greenway, Corveth and Skyline source projects must be restored or re-uploaded; Ironvale needs a successful trusted analysis.

## Recommendation

Keep the implementation in internal validation. Do not claim 9/10 or production readiness until all 18 fixtures pass three consecutive runs with 100% critical recall, at least 90% overall recall, zero traps, zero duplicates, stable ratings/IDs and the approved runtime limits.
