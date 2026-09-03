# R2 senior QA, UI/UX, and full-flow report

**Date:** 25 August 2026  
**Branch:** `feature/r2-defect-remediation`  
**Merge/deployment:** Not performed  
**Overall functional result:** **9/10 — code-review ready**  
**Public-release result:** **Conditional NO-GO** until the Fast Pass performance gate and Delegate-PM authorization contract are resolved.

## Executive result

The R2 journey was tested from authenticated entry through workspace creation, intake, analysis, all seven plan documents, issues, outcome, grounding, reports, history, collaboration, tiering, and reanalysis. The application remained on the R2 shell and the current analysis version stayed synchronized across the audited sections.

A real three-page PDF completed the live **OpenAI + deterministic validation** path. It produced an initial read, an automatic extended read, and an answer-triggered reanalysis. No run used the deterministic test harness or a provider fallback.

The client-reported functional and copy defects covered by the authorised handoff are fixed or were not reproducible, except for:

1. **Batch 0 Delegate-PM authorization measurement** — blocked by the current owner-only authenticated workspace-role model. A new role was not invented without a product decision.
2. **Fast Pass performance** — the real sample took 146.6 seconds, above the 60-second P95 gate.

## Fixes completed during this QA pass

| Issue found | Root cause | Fix | Regression evidence |
|---|---|---|---|
| Project title changed back to generic `Project` after clarification reanalysis | A clarification-only OpenAI run did not restate the title, and the publication path accepted the missing value | Reanalysis now retains the previous title; publication also normalizes a missing legacy title from the canonical project name | Targeted integration test plus complete 423-test API suite |
| Stored and returned snapshots disagreed about a missing title | Legacy read fallback was applied only when loading the current snapshot | Title normalization now happens before atomic publication, so stored, returned, and displayed snapshots match | Three durable-resume integration cases and full API suite |
| One responsive E2E teardown deadlocked and skipped the following journey | Concurrent fixture cleanup transactions could deadlock | The complete invitation-fixture reset transaction retries only PostgreSQL deadlocks with bounded backoff | Five sequential reset checks and targeted mobile rerun |

## Ten-slice result

| Slice | Main flow tested | Result | Notes |
|---:|---|---|---|
| 1 | Login, onboarding, workspace, first project, intake | **Pass** | Authenticated entry and new-project journey work across desktop, tablet, and mobile fixtures. |
| 2 | Document ingestion, initial analysis, extended analysis, seven-document publication | **Pass with speed warning** | Real OpenAI runs completed and deterministic evidence contracts passed before atomic publication. Fast Pass remains too slow. |
| 3 | Stable R2 shell, navigation, error recovery, notifications | **Pass** | No audited route fell back to the R1 CAF shell or showed an artifact-load error. |
| 4 | Your Outcome, Outcome Integrity, Viability/Grounding/Adaptability | **Pass** | Canonical R2 projection is used; no numeric-confidence or CAF peer-pillar leak was found. |
| 5 | Seven documents, document editing, issue links, versioned content | **Pass** | Intent, Scope, Requirements, Constraints, Work Breakdown, Schedule, and Resources loaded from the real read. |
| 6 | Issues, clarification, recommendations, Addressed/pending/reanalysis lifecycle | **Pass** | Answer stayed pending until a successful read; exactly one debounced reanalysis ran; the issue set refreshed afterward. |
| 7 | History, retained snapshots, failure-safe history rows | **Pass** | Initial, extended, answer, and reanalysis events were visible; null-snapshot failures render safely. |
| 8 | Workspace, settings, archive/restore, usage and capacity | **Pass** | Cross-viewport automated flows passed; active-project controls use the current workspace state. |
| 9 | Reports, exports, share/review, revocation and collaboration | **Pass** | Current report follows the latest run; retained exports remain intentionally frozen. |
| 10 | Tier limits, load-bearing integrity, proposal/decision lifecycle | **Pass** | Active R2 entitlement, lifecycle, and load-bearing guardrails passed. |

## Real-document hybrid analysis proof

Test document: `Detailed_Software_Launch_Project_Plan.pdf` (three pages).

| Run | Model | Runtime | Result |
|---|---|---:|---|
| Initial/Fast | OpenAI `gpt-5.6-luna` | **146.6s** | Completed; published seven provisional documents and 16 issues. |
| Automatic Extended | OpenAI `gpt-5.6-terra` | **140.7s** | Completed; published the current seven-document read. |
| Answer-triggered Extended | OpenAI `gpt-5.6-luna` | **102.4s** | Completed; refreshed all dependent sections from one current run. |

Hybrid-path checks:

- OpenAI performed perception, document construction, semantic interpretation, and evaluation.
- Deterministic validation then checked evidence references, document completeness, contradictions, canonical issue identity, deduplication, and publication contracts.
- Unsupported or incomplete data could not replace the last successful read.
- All seven latest document versions, Overview, History, and the current Report resolved to the same final analysis-run version.

## Section-by-section real-document audit

| Section | Data check | Actions check | Result |
|---|---|---|---|
| Overview | Current R2 integrity and issue summary loaded | Navigation and issue entry worked | **Pass** |
| Issues | Current issues, evidence, dimensions, and statuses loaded | Open issue, answer clarification, and reanalyse worked | **Pass** |
| Your Outcome | Primary outcome and R2 pillars loaded | Outcome navigation and supporting reasoning loaded | **Pass** |
| Grounding Map | Canonical provenance projection loaded | Drill-down navigation worked | **Pass** |
| Reports | Latest analysis version loaded | Report route and retained-report behaviour worked | **Pass** |
| History | Initial, extended, answer, and reanalysis records loaded | Snapshot/history navigation worked | **Pass** |
| Intent | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Scope | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Requirements | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Constraints | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Work Breakdown | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Schedule | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Resources | Extracted real-document content loaded | Document navigation worked | **Pass** |
| Full plan/export | Current seven-document read loaded | Full-plan route loaded | **Pass** |
| OSLO advisor | Current-read context loaded | Advisor surface remained available on audited routes | **Pass** |

No audited real-document route displayed `Artifact could not be loaded`, a failed-analysis page, stale R1 CAF wording, or a mismatched current-run marker.

## Client defect handoff status

| Batch | Status | Summary |
|---|---|---|
| 0 — Delegate-PM request | **Needs product/auth contract** | The product currently authenticates workspace owners only. There is no independent Delegate-PM principal to measure safely. |
| 1 — eight copy defects | **Fixed** | Intralign title, neutral progress copy, project casing/fallback, Share/Reports/export wording, R2 pillar language, and prototype-only copy are corrected. |
| 2 — confidence/trend/Understanding/dependency projection | **Fixed** | Numeric confidence is not public, zero/no-history trends stay steady, Understanding is not graded, and dependency paths replace duplicate prose. |
| 3.1 — automatic reanalysis | **Fixed** | One durable debounced run is scheduled; manual refresh remains an override. |
| 3.2 — conflicting Grounding calculations | **Fixed** | Outcome, Overview, History, Reports, and collaboration use the canonical projection. |
| 3.3/3.3b — confirmation and clarification evidence | **Fixed** | Basis, actor, timestamp, and user-stated evidence are retained without an invented second attestation. |
| 3.4 — outcome fallback/provenance | **Fixed** | Only an explicit primary outcome populates the primary slot. |
| 3.5a/c/d — narration, workspace promise, CAF-only surfaces | **Fixed** | Live provenance is authoritative; access-lock promise is gone; R2 pillar wording is used. |
| 3.5b — identical sentence on two surfaces | **Not reproduced** | Intent and Your Outcome showed distinct content in the real-document audit. |
| 4 — Fast/Deep performance | **Partially passes** | Deep runs stayed below the 180s ceiling; Fast Pass missed the 60s P95 gate. |

## Automated verification

| Gate | Result |
|---|---|
| API unit/integration suite | **423 passed** |
| Web component/unit suite | **279 passed** across 39 files |
| R2 guardrail infrastructure | **8 passed** |
| Active R2 API contracts | **43 passed** |
| Protected R2 web contracts | **117 passed** |
| Guardrail registry | **60 registered; 53 active; 7 pending; 58 mapped surfaces; 6/6 prototype corrections** |
| Cross-viewport Playwright evidence | **81/81 journeys covered as passing** — 27 desktop, 27 tablet, 27 mobile |
| API Ruff | **Passed** |
| Web ESLint | **Passed** |
| Production build and TypeScript | **Passed**; 21 static/dynamic pages generated |

The first complete cross-viewport invocation produced 79 passes, one fixture-teardown deadlock failure, and one following skip. After the bounded deadlock retry was added, the affected mobile journeys passed. Therefore all 81 journeys have passing post-fix evidence, although they were not repeated in one additional 60-minute invocation.

The browser automation environment could not attach the native local file chooser. The visible intake/upload interaction is covered by Playwright; the real PDF was sent through the same authenticated product document API and the resulting live OpenAI project was then audited end-to-end in the browser.

## Remaining risks and recommendation

### Must resolve before public release

1. Reduce Fast Pass from 146.6s to the ratified 60-second P95 target, then measure multiple representative PDFs.
2. Define whether Delegate-PM is an authenticated workspace role, a project collaborator, or a share/review principal; then execute the authorised Batch 0 request and add its security regression test.

### Follow-up quality work

- Activate the seven pending R2 guardrails when their product contracts are ratified.
- Repeat the full 81-journey matrix once in CI after review to remove the split-run qualification.
- Run a multi-document performance sample before production capacity sign-off.

**Recommendation:** proceed to human code review. Do not merge, deploy, or call the release fully production-ready until the two must-resolve items above are closed.
