# R2 Slices 1–3 Remediation Plan

**Date:** 2026-08-13
**Scope:** only Slices 1–3. Slices 4–10 remain owner-blocked.
**Source evidence:** `../code/reports/r2-full-flow-rerun-2026-08-13/FINAL_REPORT.md`

## Goal

Close the four live-QA failures without breaking onboarding, issue lifecycle, or reanalysis:

1. Expanded issues match the prototype and cause zero layout shift.
2. Uploaded documents produce seven distinct, structured, evidence-linked artifacts.
3. Expected source gaps and conflicts become accurate, traceable issues.
4. OSLO answers evidence questions from the uploaded sources and cites the basis.

## Implementation order

| Step | Work | TDD / verification | Completion gate |
|---|---|---|---|
| **1. Lock the baseline** | Turn the current failures into regression tests before changing production code. | Add browser geometry assertions, Atlas ground-truth fixtures, issue-mapping assertions, and an evidence-question advisor test. | Each new test fails for the documented reason. |
| **2. Fix expanded issue parity** | Present issue details in the prototype’s stable focus layer. Preserve queue, header, rails, scroll position, close/Escape, and focus restoration. | Component tests plus live same-viewport screenshots and bounding-box comparison. | No page growth, scroll jump, or content displacement; layout shift is zero; open and closed states match the prototype. |
| **3. Fix structured extraction** | Produce artifact-specific Intent, Scope, Requirements, Constraints, Work breakdown, Schedule, and Resources content with evidence references and conflicts. Remove generic duplicated artifact bodies. | Run the clean Atlas documents through the real ingestion pipeline and compare field by field with `ground_truth.json`. | All required fields are represented in the correct artifact with a valid source reference; no cross-artifact duplication. |
| **4. Fix issue derivation** | Convert the extracted Atlas gaps/conflicts into deterministic, deduplicated issues with correct dimension, severity, recommendation, and evidence. | Assert the expected missing unit, TBD owner, unconfirmed dependency, capacity gaps, vendor gap, budget variance, date conflict, cost conflict, and excluded change. | Expected issues appear once, unrelated generic defaults do not replace evidence-derived issues, and every issue has evidence. |
| **5. Fix OSLO evidence answers** | Make the deterministic advisor understand source/evidence, conflict, and “what next” questions. Keep the model fallback safe and grounded. | Ask about the £45,000 variance and other planted conflicts with and without the model provider. | Answer identifies the exact source evidence, distinguishes fact from inference, gives the next verification action, and never invents data. |
| **6. Verify correction-triggered reanalysis** | Re-test answer/confirm/correct → stale → reanalysis → refreshed artifacts/issues → Resolved. Verify Withdraw reverses the act and reopens the issue. | API integration tests plus manual browser run. | Only supported corrections resolve an issue; unsupported answers remain open; counts, history, evidence, and advisor all refresh correctly. |
| **7. Full regression and parity pass** | Run Slices 1–3 end to end for a new user and an existing client, including mixed large PDF/DOCX/XLSX upload, all buttons, loading/error/empty states, and responsive layouts. | Full web/API/guardrail suites plus manual browser comparison against both prototypes. | All automated tests pass; no major/minor parity gaps remain; Atlas ground truth passes; no functional regression. |
| **8. Close and record** | Update the ledger with exact evidence and commit the completed fix. | Review changed files and the final QA report. | Slices are marked COMPLETE only if every gate above passes; otherwise the ledger keeps the exact open item. |

## Required test additions

- Issue open/close: zero layout shift, stable scroll, Escape, focus restoration, desktop and narrow width.
- Artifact extraction: distinct schemas and required Atlas values per artifact.
- Conflict detection: milestone dates, project costs, and excluded/rejected change.
- Gap detection: missing unit, TBD owner, unconfirmed dependency, role shortages, vendor, and approval variance.
- Advisor: exact evidence citation, insufficient-evidence response, provider unavailable, and no hallucination.
- Reanalysis: correction accepted, correction unsupported, failure/retry, resolved movement, and withdrawal.
- Regression: first-time guided path, returning watch path, proposal lifecycle, and OSLO rail controls.

## Definition of done

The work is done only when:

- the expanded issue is visually and behaviorally identical to the applicable prototype state;
- Atlas field-by-field extraction and expected issue assertions pass;
- OSLO answers the source-specific evidence question correctly;
- correction-triggered reanalysis and withdrawal work end to end;
- all Slice 1–3 automated and manual regression gates pass; and
- the final QA report and source-of-truth ledger contain the new evidence.
